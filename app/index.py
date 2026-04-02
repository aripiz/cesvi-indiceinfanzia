# index.py — Cesvi Indice Infanzia

from dash import Dash
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd

from configuration import (
    DATA_FILE,
    GEO_FILE,
    TITLE,
    DBC_CSS,
    TEMPLATE_CSS,
)

# ── Caricamento dati ──────────────────────────────────────────────────────────

data = pd.read_csv(DATA_FILE)   # long format: territory, year, indicator, value, rank
geodata = gpd.read_file(GEO_FILE)

# Mappa nomi GeoJSON → nomi canonici nel CSV
_REGNAME_NORM = {
    "Valle d'Aosta/Vallée d'Aoste": "Valle d'Aosta",
    "Trentino-Alto Adige/Südtirol": "Trentino-Alto Adige",
}

# Aggiungi colonna 'code' (reg_istat_code_num) al dataframe dati per il join con geodata
if "reg_name" in geodata.columns and "reg_istat_code_num" in geodata.columns:
    code_map = {}
    for _, row in geodata.iterrows():
        name = _REGNAME_NORM.get(row["reg_name"], row["reg_name"])
        code_map[name] = row["reg_istat_code_num"]
    data["code"] = data["territory"].map(code_map)

# ── App Dash ──────────────────────────────────────────────────────────────────

app = Dash(
    __name__,
    title=TITLE,
    external_stylesheets=[TEMPLATE_CSS, DBC_CSS],
    suppress_callback_exceptions=True,
    use_pages=True,
)

server = app.server
