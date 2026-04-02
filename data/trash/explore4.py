"""
Legge il foglio 'tabella capacità' del 2022 per capire struttura indice.
Cerca anche le righe di righe header nei fogli regionali.
"""
import pandas as pd
from pathlib import Path

TABLES_DIR = Path('original/tables')

# 2022 ha un foglio extra 'tabella capacità'
f2022 = TABLES_DIR / 'TABELLE PER GRAFICO CESVI 2022.xlsx'
xl = pd.ExcelFile(f2022)
print("Fogli 2022:", xl.sheet_names)

print("\n--- tabella capacità ---")
df_cap = pd.read_excel(f2022, sheet_name='tabella capacità', header=None)
print(f"Shape: {df_cap.shape}")
print(df_cap.to_string())

# Leggi anche il foglio 2021 "tabella capacità" se esiste
f2024 = TABLES_DIR / 'TABELLE PER GRAFICO CESVI 2024.xlsx'
xl24 = pd.ExcelFile(f2024)
print("\n\nFogli 2024:", xl24.sheet_names)
if 'tabella capacità' in xl24.sheet_names:
    print("\n--- tabella capacità (2024) ---")
    df_cap24 = pd.read_excel(f2024, sheet_name='tabella capacità', header=None)
    print(df_cap24.to_string())

# Cerca in tutti i fogli 2022 le prime righe per header di dimensione
print("\n\n=== Analisi struttura header fogli 2022 ===")
for sheet in xl.sheet_names[:20]:
    df_raw = pd.read_excel(f2022, sheet_name=sheet, header=None)
    if df_raw.empty or df_raw.shape[0] < 3:
        continue
    # Cerca stringhe di titolo nelle prime 2 righe
    for ri in range(min(3, df_raw.shape[0])):
        row = df_raw.iloc[ri]
        strs = [str(v).strip() for v in row if isinstance(v, str) and len(str(v).strip()) > 10]
        if strs:
            print(f"  [{sheet}] row{ri}: {strs}")
            break
