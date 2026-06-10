# callbacks/news.py — Cesvi Indice Infanzia

import pandas as pd
from dash import Input, Output

from index import app
from configuration import NEWS_CSV_URL
from layout.layout_news import build_news_list

_MESI = {
    "gennaio": 1, "febbraio": 2, "marzo": 3, "aprile": 4,
    "maggio": 5, "giugno": 6, "luglio": 7, "agosto": 8,
    "settembre": 9, "ottobre": 10, "novembre": 11, "dicembre": 12,
}

def _parse_date(s):
    """Converte una data italiana ('27 maggio 2025') in un valore ordinabile."""
    try:
        parts = s.strip().lower().split()
        day, month, year = int(parts[0]), _MESI.get(parts[1], 0), int(parts[2])
        return (year, month, day)
    except Exception:
        return (0, 0, 0)


def _fetch_news():
    """Scarica il CSV da Google Sheets e restituisce una lista di dizionari."""
    if not NEWS_CSV_URL:
        return []
    try:
        df = pd.read_csv(NEWS_CSV_URL, dtype=str).fillna("")
        df.columns = [c.strip().lower() for c in df.columns]
        df = df.iloc[:, 1:]
        df = df[(df != "").any(axis=1)]
        # Ordina per data decrescente; a parità di data, le righe più in basso nel foglio vengono prima
        df["_row"] = range(len(df))
        df["_sort"] = df["date"].apply(_parse_date)
        df = df.sort_values(["_sort", "_row"], ascending=[False, False]).drop(columns=["_sort", "_row"]).reset_index(drop=True)
        return df.to_dict(orient="records")
    except Exception:
        return []


@app.callback(
    Output("news_list_container", "children"),
    Input("news_refresh_interval", "n_intervals"),
)
def refresh_news(n_intervals):
    news_items = _fetch_news()
    return build_news_list(news_items)
