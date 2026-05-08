# index.py — Cesvi Indice Infanzia

import os
from dash import Dash
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
from flask import send_from_directory, abort

from configuration import (
    DATA_FILE,
    GEO_FILE,
    METADATA_FILE,
    REPORTS_DIR,
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

# ── Route Flask per i PDF (serviti da data/reports/) ─────────────────────────

@server.route("/reports/<path:filename>")
def serve_report(filename):
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), REPORTS_DIR))
    filepath = os.path.join(reports_dir, filename)
    # Verifica che il file sia dentro reports_dir (path traversal prevention)
    if not os.path.abspath(filepath).startswith(reports_dir):
        abort(403)
    return send_from_directory(reports_dir, filename, as_attachment=True)
