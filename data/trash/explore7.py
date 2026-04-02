"""
Analisi approfondita: trova l'indice totale composito e i sub-indici
zscores per ogni anno.
"""
import pandas as pd
import re
import numpy as np
from pathlib import Path

TABLES_DIR = Path('original/tables')

def clean_region_name(val):
    if not isinstance(val, str): return None
    s = re.sub(r'[\s;]+\d+$', '', str(val)).strip()
    s = re.sub(r'Trentino.?Alto Adige', 'Trentino Alto Adige', s)
    # Normalizza altre varianti
    replacements = {
        "Valle d'Aosta": "Valle d'Aosta",
        'Friuli-Venezia Giulia': 'Friuli-Venezia Giulia',
        'Friuli Venezia Giulia': 'Friuli-Venezia Giulia',
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    if len(s) > 3: return s
    return None

def extract_zscore_ranking(df_raw):
    """Estrae {region -> zscore} da un foglio di ranking regionale."""
    data = {}
    flat = df_raw.values.flatten()
    
    # Trova le coppie (region_string, float_value)
    # Le region strings seguono il pattern: "Nome Regione  N" 
    # e i float sono adiacenti
    
    all_vals = []
    for val in df_raw.values.flatten():
        if val is not None and not (isinstance(val, float) and np.isnan(val)):
            all_vals.append(val)
    
    # Cerca coppie (text, number) nelle stesse righe
    for ri in range(df_raw.shape[0]):
        row = df_raw.iloc[ri]
        strings_in_row = [(ci, v) for ci, v in enumerate(row) if isinstance(v, str) and len(v) > 3]
        nums_in_row = [(ci, v) for ci, v in enumerate(row) 
                       if isinstance(v, (int, float)) and not pd.isna(v) and -10 < v < 10]
        
        for _, s in strings_in_row:
            region = clean_region_name(s)
            if region is None: continue
            if nums_in_row:
                # Prendi il primo numero della riga non uguale a un rank (>0 integer)
                for _, n in nums_in_row:
                    if not (float(n) == int(n) if n == int(n) else False) or abs(n) < 1:
                        # È un z-score
                        if region not in data:
                            data[region] = n
                        break
                    elif abs(float(n) % 1) > 0.01:  # Ha decimali = z-score
                        if region not in data:
                            data[region] = n
                        break
    
    return data


def extract_zscore_ranking_v2(df_raw):
    """
    Estrae {region_name -> z_score} da un foglio di ranking.
    Strategia: la colonna con z-scores ha valori float tra -5 e 5 con decimali.
    """
    from collections import defaultdict
    
    result = {}
    
    for ri in range(df_raw.shape[0]):
        row = list(df_raw.iloc[ri])
        # Trova il nome regione in questa riga
        region = None
        zscore = None
        
        for val in row:
            if isinstance(val, str):
                r = clean_region_name(val)
                if r is not None:
                    region = r
            elif isinstance(val, (int, float)) and not pd.isna(val):
                # Z-score: float con decimali, range [-5, 5]
                if -5 < val < 5 and abs(val % 1) > 0.001:
                    zscore = float(val)
        
        if region is not None and zscore is not None:
            if region not in result:
                result[region] = zscore
    
    return result


# Estrazione per tutti gli anni e tutti i fogli con ~20 valori regionali
YEAR_MAP = {
    2018: ('CESVI TABELLA TOTALE 2018 Per grafico.xlsx', None),
    2019: ('TABELLE_DEF_per grafico_2019.xlsx', None),
    2020: ('TABELLE PER GRAFICO INDICE CESVI 2020.xlsx', None),
    2021: ('TABELLE PER GRAFICO CESVI 2021.xlsx', None),
    2022: ('TABELLE PER GRAFICO CESVI 2022.xlsx', 'tabella capacità'),
    2024: ('TABELLE PER GRAFICO CESVI 2024.xlsx', 'tabella capacità'),
}

all_data = {}

for year, (fname, cap_sheet) in YEAR_MAP.items():
    fpath = TABLES_DIR / fname
    xl = pd.ExcelFile(fpath)
    year_data = {}
    
    print(f"\n{year}: {fname}")
    
    for sheet in xl.sheet_names:
        if sheet == 'tabella capacità': continue
        try:
            df_raw = pd.read_excel(fpath, sheet_name=sheet, header=None)
            if df_raw.empty: continue
            
            # Conta z-scores (float con decimali in range [-5,5])
            flat = df_raw.values.flatten()
            zscores_flat = [x for x in flat 
                           if isinstance(x, (int,float)) and not pd.isna(x) 
                           and -5 < x < 5 and abs(x % 1) > 0.001]
            
            if 15 <= len(zscores_flat) <= 25:
                data = extract_zscore_ranking_v2(df_raw)
                if len(data) >= 15:
                    year_data[sheet] = data
                    # Elenco top 3 regioni per z-score
                    top3 = sorted(data.items(), key=lambda x: -x[1])[:3]
                    print(f"  [{sheet}] {len(data)} regioni, top3: {top3}")
        except Exception as e:
            print(f"  [{sheet}] ERR: {e}")
    
    all_data[year] = year_data

# Confronta Fig.5 2022 vs tabella capacità 2022
print("\n\n=== Confronto Fig.5 2022 vs tabella capacità 2022 ===")
fpath = TABLES_DIR / 'TABELLE PER GRAFICO CESVI 2022.xlsx'
print("Fig.5:")
df5 = pd.read_excel(fpath, sheet_name='Fig.5', header=None)
d5 = extract_zscore_ranking_v2(df5)
for k, v in sorted(d5.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v:.3f}")
