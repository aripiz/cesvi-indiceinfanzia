"""
Script di esplorazione per capire il mapping Figura -> Dimensione
per ogni anno del dataset Cesvi.
"""
import pandas as pd
import re
from pathlib import Path

TABLES_DIR = Path('original/tables')
excel_files = sorted(TABLES_DIR.glob('*.xlsx'))

PYTHON = '/Users/ariele/miniconda3/envs/data/bin/python'

# Mapping anno -> file
YEAR_MAP = {
    2018: 'CESVI TABELLA TOTALE 2018 Per grafico.xlsx',
    2019: 'TABELLE_DEF_per grafico_2019.xlsx',
    2020: 'TABELLE PER GRAFICO INDICE CESVI 2020.xlsx',
    2021: 'TABELLE PER GRAFICO CESVI 2021.xlsx',
    2022: 'TABELLE PER GRAFICO CESVI 2022.xlsx',
    2024: 'TABELLE PER GRAFICO CESVI 2024.xlsx',
}

# Per ogni file, cerca tutti i fogli con dati regionali (18-22 righe)
# e mostra il titolo/header per capire il nome della dimensione
for year, fname in YEAR_MAP.items():
    fpath = TABLES_DIR / fname
    xl = pd.ExcelFile(fpath)
    print(f"\n{'='*70}")
    print(f"ANNO {year}: {fname}")
    
    for sheet in xl.sheet_names:
        try:
            df_raw = pd.read_excel(fpath, sheet_name=sheet, header=None)
            if df_raw.empty or df_raw.shape[0] < 5:
                continue
            
            # Conta valori numerici nell'intervallo z-score
            flat = df_raw.values.flatten()
            nums = [x for x in flat if isinstance(x, (int, float)) 
                    and not pd.isna(x) and -10 < x < 10]
            
            if 15 <= len(nums) <= 25:
                print(f"\n  [{sheet}] shape={df_raw.shape}  {len(nums)} valori regionali")
                # Mostra prime 3 righe per capire titoli
                print(df_raw.head(3).to_string())
        except Exception as e:
            pass
