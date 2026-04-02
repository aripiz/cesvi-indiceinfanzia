"""
Estrai struttura completa da tabella capacità (2022, 2024):
trova la riga header corretta con i nomi delle dimensioni.
"""
import pandas as pd
import re
import numpy as np
from pathlib import Path

TABLES_DIR = Path('original/tables')

CAPACITY_DIMS = ['CURA', 'VITA SANA', 'VITA SICURA',
                 'CONOSCENZA E SAPERE', 'LAVORARE', 'ACCEDERE RISORSE']

def clean_region_name(val):
    if not isinstance(val, str): return None
    s = re.sub(r'[\s;]+\d+$', '', str(val)).strip()
    s = re.sub(r'Trentino.?Alto Adige', 'Trentino Alto Adige', s)
    if len(s) > 3: return s
    return None

def parse_cap_table_v2(df_raw):
    """
    Legge il foglio 'tabella capacità' con header=None.
    Trova la riga header cercando una cella uguale a un nome dimensione ESATTO.
    """
    header_row = None
    for ri in range(df_raw.shape[0]):
        row_vals = [str(v).strip() for v in df_raw.iloc[ri]]
        # La riga header ha CURA UGUALE (non dentro parola più lunga)
        if 'CURA' in row_vals and any(d in row_vals for d in ['VITA SANA', 'LAVORARE']):
            header_row = ri
            break
        # Prova 'Regioni' come marker
        if 'Regioni' in row_vals and 'CURA' in row_vals:
            header_row = ri
            break

    if header_row is None:
        print("  [WARN] Header non trovata")
        print("  Prime righe raw:")
        print(df_raw.head(5).to_string())
        return {}, {}

    headers = [str(v).strip() for v in df_raw.iloc[header_row]]
    print(f"  Header (row {header_row}): {headers}")

    # Mappa colonne
    region_idx = None
    totale_idx = None
    dim_indices = {}
    totale_rank_idx = None

    for ci, h in enumerate(headers):
        if h in ('Regioni', 'Regione'):
            region_idx = ci
        elif h in ('Totale Indice', 'TOT Indice'):
            totale_idx = ci
        elif h in CAPACITY_DIMS:
            dim_indices[h] = ci
        elif h in ('TOTALE CAPACITÀ', 'TOTALE CAPACITA'):
            totale_rank_idx = ci

    # Se "Totale Indice" non trovato, cerca colonna con z-scores
    # I Cesvi z-scores sono nell'intervallo [-2, 2]
    cap_rankings = {d: {} for d in dim_indices}
    totale_zscores = {}

    # I dati sono su righe alternate: riga0 = rank, riga1 = zscore
    # Oppure su righe singole (come in 2024)
    data_rows = df_raw.iloc[header_row+1:].reset_index(drop=True)

    # Capisce se ci sono righe doppie (ogni regione occupa 2 righe: rank + zscore)
    # guardando se la prima colonna non-NaN ha valori interi
    ri = 0
    prev_region = None
    while ri < data_rows.shape[0]:
        row = data_rows.iloc[ri]
        region = clean_region_name(row.iloc[region_idx]) if region_idx is not None else None
        
        if region is None:
            # Riga senza nome regione: potrebbe essere la riga z-score (struttura 2022)
            if prev_region is not None and totale_idx is not None:
                val = row.iloc[totale_idx]
                if isinstance(val, (int, float)) and not pd.isna(val) and -5 < val < 5:
                    totale_zscores[prev_region] = float(val)
            ri += 1
            continue
        
        prev_region = region

        # Rankings dimensioni
        for dim, ci in dim_indices.items():
            val = row.iloc[ci]
            if isinstance(val, (int, float)) and not pd.isna(val) and val > 0:
                cap_rankings[dim][region] = int(val)
        
        # Z-score totale (se su stessa riga - 2024)
        if totale_idx is not None:
            val = row.iloc[totale_idx]
            if isinstance(val, (int, float)) and not pd.isna(val) and -5 < val < 5:
                totale_zscores[region] = float(val)

        ri += 1

    return cap_rankings, totale_zscores


# Test su 2022 e 2024
for year, fname in [(2022, 'TABELLE PER GRAFICO CESVI 2022.xlsx'),
                    (2024, 'TABELLE PER GRAFICO CESVI 2024.xlsx')]:
    fpath = TABLES_DIR / fname
    print(f"\n{'='*60}")
    print(f"ANNO {year}")
    df_raw = pd.read_excel(fpath, sheet_name='tabella capacità', header=None)
    cap_rankings, totale_zscores = parse_cap_table_v2(df_raw)
    
    print(f"\n  Totale Indice z-scores ({len(totale_zscores)} regioni):")
    for k, v in sorted(totale_zscores.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v:.3f}")
    
    if not totale_zscores:
        print("  [DEBUG] cap_rankings:", cap_rankings)


# Mapping Figure -> Dimensione per 2022 con correlazione di Spearman
print("\n\n" + "="*60)
print("MAPPING FIGURE -> DIMENSIONE (2022)")

def extract_ranking_from_sheet_v2(df_raw):
    """Estrae {region -> rank} dal foglio.""" 
    ranking = {}
    for val in df_raw.values.flatten():
        if not isinstance(val, str): continue
        region = clean_region_name(val)
        if region is None: continue
        m = re.search(r'[\s;]+(\d+)\s*$', str(val))
        if m and region not in ranking:
            ranking[region] = int(m.group(1))
    return ranking

f2022 = TABLES_DIR / 'TABELLE PER GRAFICO CESVI 2022.xlsx'
xl = pd.ExcelFile(f2022)
df_cap = pd.read_excel(f2022, sheet_name='tabella capacità', header=None)
cap_rankings_2022, totale_zscores_2022 = parse_cap_table_v2(df_cap)

for sheet in xl.sheet_names:
    if sheet == 'tabella capacità': continue
    try:
        df_raw = pd.read_excel(f2022, sheet_name=sheet, header=None)
        if df_raw.empty: continue
        ranking = extract_ranking_from_sheet_v2(df_raw)
        if 15 <= len(ranking) <= 22:
            for dim, cap_rank in cap_rankings_2022.items():
                common = set(ranking.keys()) & set(cap_rank.keys())
                if len(common) >= 15:
                    r1 = [ranking[k] for k in common]
                    r2 = [cap_rank[k] for k in common]
                    corr = np.corrcoef(r1, r2)[0, 1]
                    if abs(corr) > 0.80:
                        print(f"  [{sheet}] ~ {dim}: corr={corr:.3f} (n={len(common)})")
    except Exception as e:
        pass

# Anche estrai tutti i z-score da Fig.5 (totale indice) per 2022
print("\n\n--- Fig.5 z-scores (indice totale) 2022 ---")
df_fig5 = pd.read_excel(f2022, sheet_name='Fig.5', header=None)
print(df_fig5.to_string())
