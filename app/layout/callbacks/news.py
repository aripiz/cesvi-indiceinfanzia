# callbacks/news.py — Cesvi Indice Infanzia

import pandas as pd
from dash import Input, Output

from index import app
from configuration import NEWS_CSV_URL
from layout.layout_news import build_news_list


def _fetch_news():
    """Scarica il CSV da Google Sheets e restituisce una lista di dizionari."""
    if not NEWS_CSV_URL:
        return []
    try:
        df = pd.read_csv(NEWS_CSV_URL, dtype=str).fillna("")
        df.columns = [c.strip().lower() for c in df.columns]
        df = df.iloc[:, 1:]
        df = df[(df != "").any(axis=1)]
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
