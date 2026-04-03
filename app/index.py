# index.py — Cesvi Indice Infanzia

from dash import Dash
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd

from configuration import (
    DATA_FILE,
    GEO_FILE,
    METADATA_FILE,
    TITLE,
    DBC_CSS,
    TEMPLATE_CSS,
    FONT_URL
)

# ── Caricamento dati ──────────────────────────────────────────────────────────

data = pd.read_csv(DATA_FILE)  
metadata = pd.read_csv(METADATA_FILE)
geodata = gpd.read_file(GEO_FILE)

# Aggiungi colonna 'code' (reg_istat_code_num) al dataframe dati per il join con geodata
if "reg_name" in geodata.columns and "reg_istat_code_num" in geodata.columns:
    code_map = dict(zip(geodata["reg_name"], geodata["reg_istat_code_num"]))
    data["code"] = data["territory"].map(code_map)

# ── App Dash ──────────────────────────────────────────────────────────────────

app = Dash(
    __name__,
    title=TITLE,
    external_stylesheets=[FONT_URL, TEMPLATE_CSS, DBC_CSS],
    suppress_callback_exceptions=True,
    use_pages=True,
)

server = app.server
