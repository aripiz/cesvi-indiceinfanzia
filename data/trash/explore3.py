"""
Cerca titoli testuali nelle figure regionali per capire
il nome di ogni dimensione.
"""
import pandas as pd
import re
from pathlib import Path

TABLES_DIR = Path('original/tables')

YEAR_MAP = {
    2021: 'TABELLE PER GRAFICO CESVI 2021.xlsx',
    2022: 'TABELLE PER GRAFICO CESVI 2022.xlsx',
    2024: 'TABELLE PER GRAFICO CESVI 2024.xlsx',
}

def extract_strings(df):
    """Estrae tutte le stringhe non-NaN dal dataframe."""
    strings = []
    for val in df.values.flatten():
        if isinstance(val, str) and val.strip() and 'NaN' not in val:
            strings.append(val.strip())
    return strings

for year, fname in YEAR_MAP.items():
    fpath = TABLES_DIR / fname
    xl = pd.ExcelFile(fpath)
    print(f"\n{year}: {fname}")
    for sheet in xl.sheet_names:
        try:
            df_raw = pd.read_excel(fpath, sheet_name=sheet, header=None)
            if df_raw.empty:
                continue
            flat = df_raw.values.flatten()
            nums = [x for x in flat if isinstance(x, (int, float))
                    and not pd.isna(x) and -10 < x < 10]
            
            # Solo fogli con ~20 valori regionali
            if 15 <= len(nums) <= 25:
                strings = extract_strings(df_raw)
                # Filtra stringhe che sembrano titoli (non "Regione/Regioni/Totale/NaN/classifica")
                titles = [s for s in strings
                          if len(s) > 15
                          and not re.search(r'^\d', s)
                          and 'assifica' not in s.lower()
                          and 'egioni' not in s.lower()
                          and 'otale' not in s.lower()
                          and 'gione' not in s.lower()]
                if titles:
                    print(f"  [{sheet}] TITOLI: {titles}")
        except:
            pass
