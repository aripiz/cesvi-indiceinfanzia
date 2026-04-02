import pandas as pd
import re
from pathlib import Path

TABLES_DIR = Path('original/tables')
excel_files = sorted(TABLES_DIR.glob('*.xlsx'))

for f in excel_files:
    xl = pd.ExcelFile(f)
    print(f'\n{"="*60}')
    print(f'FILE: {f.name}')
    print(f'Fogli ({len(xl.sheet_names)}): {xl.sheet_names}')
    for sheet in xl.sheet_names:
        try:
            df = pd.read_excel(f, sheet_name=sheet, header=0)
            if df.empty:
                continue
            flat = df.values.flatten()
            nums = [x for x in flat if isinstance(x, (int, float)) and not pd.isna(x) and abs(x) < 100]
            if 15 <= len(nums) <= 30:
                print(f'  [{sheet}] shape={df.shape}  {len(nums)} valori regionali')
                print(f'    cols: {list(df.columns)}')
                # Trova le righe con dati
                print(df.dropna(how='all').head(3).to_string())
        except Exception as e:
            print(f'  [{sheet}] ERRORE: {e}')
