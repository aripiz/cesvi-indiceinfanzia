# utilis.py — Cesvi Indice Infanzia

import numpy as np
import pandas as pd
from dash import html

from configuration import GEO_KEY, ZSCORE_BINS, ZSCORE_LABELS


def sig_round(x, precision=3):
    """Arrotonda a cifre significative."""
    return np.float64(f"{x:#.{precision}g}")


def sig_format(x, precision=3):
    """Formatta con cifre significative, gestisce NaN."""
    if pd.isna(x):
        return "N/A"
    if precision == 0:
        return str(x)
    return f"{np.float64(x):#.{precision}g}"


def zscore_format(x):
    """Formatta uno z-score con segno e 2 decimali."""
    if pd.isna(x):
        return "N/A"
    sign = "+" if float(x) >= 0 else ""
    return f"{sign}{float(x):.2f}"


def get_zscore_tier(z):
    """Restituisce il livello testuale (ZSCORE_LABELS) per un dato z-score."""
    if pd.isna(z):
        return "N/A"
    for i in range(len(ZSCORE_BINS) - 1):
        if ZSCORE_BINS[i] <= float(z) < ZSCORE_BINS[i + 1]:
            return ZSCORE_LABELS[i]
    return ZSCORE_LABELS[-1]


def get_score_change_arrow(value, equal_buffer=0.1):
    """Restituisce un'icona HTML per indicare la variazione."""
    if -equal_buffer <= value <= equal_buffer:
        return html.Span("→", className="text-muted")
    elif value > equal_buffer:
        return html.Span("↑", className="text-success fw-bold")
    else:
        return html.Span("↓", className="text-danger fw-bold")


def area_centroid(geodata, regions):
    """Calcola il centroide per le regioni selezionate (per la mappa schede)."""
    col = GEO_KEY.split(".")[-1]
    selected = geodata[geodata[col].isin(regions)]
    if selected.empty:
        return {"lat": 41.9, "lon": 12.5}
    combined = selected.unary_union
    return {"lat": combined.centroid.y, "lon": combined.centroid.x}


def get_value(dataframe, key, format_string, divide=1, default="N/A"):
    """Legge un valore dal DataFrame e lo formatta."""
    try:
        value = dataframe[key]
        if pd.isna(value):
            return default
        if divide != 1:
            value = value / divide
        return format_string.format(value)
    except (KeyError, TypeError, ValueError):
        return default
