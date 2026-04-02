"""
Mappa i fogli Fig.X ai 6 sub-indici (capacità) usando la tabella capacità
come riferimento per i rankings. Poi estrae i z-score per ogni sub-indice.

Struttura indice Cesvi (dalla tabella capacità):
- CURA
- VITA SANA
- VITA SICURA
- CONOSCENZA E SAPERE
- LAVORARE
- ACCEDERE RISORSE
- TOTALE CAPACITÀ  (aggregato)
- Totale Indice     (indice complessivo = Capacità + Fattori di rischio)
"""
import pandas as pd
import re
import numpy as np
from pathlib import Path

TABLES_DIR = Path('original/tables')

CAPACITY_DIMS = ['CURA', 'VITA SANA', 'VITA SICURA',
                 'CONOSCENZA E SAPERE', 'LAVORARE', 'ACCEDERE RISORSE']

def clean_region_name(val):
    """Rimuove il numero di classifica dal nome regione: 'Trentino Alto Adige  1' -> 'Trentino Alto Adige'"""
    if not isinstance(val, str):
        return None
    s = re.sub(r'[\s;]+\d+$', '', str(val)).strip()
    # Normalizza varianti
    s = s.replace('Trentino-Alto Adige', 'Trentino Alto Adige')
    s = s.replace('Trentino-alto Adige', 'Trentino Alto Adige')
    if len(s) > 3:
        return s
    return None

def extract_ranking_from_sheet(df_raw):
    """Estrae un dict {region -> rank} da un foglio con ~20 regioni."""
    ranking = {}
    for val in df_raw.values.flatten():
        if not isinstance(val, str):
            continue
        region = clean_region_name(val)
        if region is None:
            continue
        # Trova il numero di classifica (ultima parte)
        m = re.search(r'[\s;]+(\d+)$', str(val))
        if m:
            ranking[region] = int(m.group(1))
    return ranking


def parse_cap_table(df_raw, year):
    """
    Legge il foglio 'tabella capacità' e restituisce dict:
    {dim_name: {region: rank}}
    e separatamente il totale indice {region: zscore}
    """
    # Trova la riga con i nomi delle colonne (cercando "CURA" o "Regioni")
    header_row = None
    for ri in range(min(5, df_raw.shape[0])):
        row = df_raw.iloc[ri].astype(str)
        if any('CURA' in str(v) or 'VITA' in str(v) for v in row):
            header_row = ri
            break

    if header_row is None:
        print("  [WARN] Non trovata riga header in tabella capacità")
        return {}, {}

    headers = [str(v).strip() for v in df_raw.iloc[header_row]]
    print(f"  tabella capacità headers: {headers}")

    # Trova colonne
    totale_idx = None
    region_idx = None
    dim_indices = {}
    for ci, h in enumerate(headers):
        if 'Totale Indice' in h or 'TOT Indice' in h:
            totale_idx = ci
        elif 'Regioni' in h or 'Regione' in h:
            region_idx = ci
        elif h in CAPACITY_DIMS:
            dim_indices[h] = ci

    if region_idx is None:
        # Cerca colonna con regioni in base ai dati
        for ci in range(df_raw.shape[1]):
            col_vals = [clean_region_name(v) for v in df_raw.iloc[header_row+1:, ci] if isinstance(v, str)]
            if sum(1 for v in col_vals if v is not None) >= 15:
                region_idx = ci
                break

    print(f"  region_idx={region_idx} totale_idx={totale_idx} dim_indices={dim_indices}")

    # Estrae dati
    cap_rankings = {d: {} for d in dim_indices}
    totale_zscores = {}
    
    data_rows = df_raw.iloc[header_row+1:]
    for ri in range(data_rows.shape[0]):
        row = data_rows.iloc[ri]
        # Regione
        if region_idx is not None:
            region = clean_region_name(row.iloc[region_idx])
        else:
            continue
        
        if region is None:
            continue
        
        # Z-score totale
        if totale_idx is not None:
            val = row.iloc[totale_idx]
            if isinstance(val, (int, float)) and not pd.isna(val):
                totale_zscores[region] = float(val)
        
        # Rankings dimensioni
        for dim, ci in dim_indices.items():
            val = row.iloc[ci]
            if isinstance(val, (int, float)) and not pd.isna(val):
                cap_rankings[dim][region] = int(val)

    return cap_rankings, totale_zscores


# Test su 2022 e 2024
for year, fname in [(2022, 'TABELLE PER GRAFICO CESVI 2022.xlsx'),
                    (2024, 'TABELLE PER GRAFICO CESVI 2024.xlsx')]:
    fpath = TABLES_DIR / fname
    print(f"\n{'='*60}")
    print(f"ANNO {year}")
    df_raw = pd.read_excel(fpath, sheet_name='tabella capacità', header=None)
    cap_rankings, totale_zscores = parse_cap_table(df_raw, year)
    print(f"\n  Totale Indice z-scores ({len(totale_zscores)} regioni):")
    for k, v in sorted(totale_zscores.items(), key=lambda x: -x[1]):
        print(f"    {k}: {v:.3f}")
    for dim in CAPACITY_DIMS:
        if dim in cap_rankings:
            print(f"\n  {dim} ranking top 5: {dict(sorted(cap_rankings[dim].items(), key=lambda x: x[1])[:5])}")

# Ora mappa i fig. ai dim. per 2022 usando i rankings
print("\n\n" + "="*60)
print("MAPPING FIGURE -> DIMENSIONE per 2022")
f2022 = TABLES_DIR / 'TABELLE PER GRAFICO CESVI 2022.xlsx'
xl = pd.ExcelFile(f2022)

# Cap rankings per 2022
df_cap = pd.read_excel(f2022, sheet_name='tabella capacità', header=None)
cap_rankings_2022, _ = parse_cap_table(df_cap, 2022)

# Per ogni fig con ~20 valori regionali, estrai il ranking e confronta
for sheet in xl.sheet_names:
    try:
        df_raw = pd.read_excel(f2022, sheet_name=sheet, header=None)
        if df_raw.empty:
            continue
        # Estrai ranking
        ranking = extract_ranking_from_sheet(df_raw)
        if 15 <= len(ranking) <= 22:
            # Confronta con ogni dimensione
            for dim, cap_rank in cap_rankings_2022.items():
                # Calcola correlazione
                common = set(ranking.keys()) & set(cap_rank.keys())
                if len(common) >= 15:
                    r1 = [ranking[k] for k in common]
                    r2 = [cap_rank[k] for k in common]
                    # Spearman-like: count inversions
                    corr = np.corrcoef(r1, r2)[0, 1]
                    if abs(corr) > 0.85:
                        print(f"  [{sheet}] ~ {dim}: corr={corr:.3f} (n={len(common)})")
    except Exception as e:
        pass
