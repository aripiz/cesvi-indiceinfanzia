# index.py — Cesvi Indice Infanzia

import os
from dash import Dash
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd
from flask import send_from_directory, abort
from flask_caching import Cache

from configuration import (
    DATA_FILE,
    GEO_FILE,
    METADATA_FILE,
    REPORTS_DIR,
    TITLE,
    DBC_CSS,
    TEMPLATE_CSS,
    FONT_URL,
    REPORTS_FILE,
    GA_MEASUREMENT_ID,
)

# ── Caricamento dati ──────────────────────────────────────────────────────────

data = pd.read_csv(DATA_FILE)  
metadata = pd.read_csv(METADATA_FILE)
geodata = gpd.read_parquet(GEO_FILE)


reports_df = pd.read_csv(REPORTS_FILE).sort_values("year", ascending=False)
reports = reports_df.to_dict(orient="records")


# ── App Dash ──────────────────────────────────────────────────────────────────

_ga_script = (
    f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_MEASUREMENT_ID}"></script>'
    f'<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}'
    f'gtag("js",new Date());gtag("config","{GA_MEASUREMENT_ID}");</script>'
    if GA_MEASUREMENT_ID else ""
)

app = Dash(
    __name__,
    title=TITLE,
    external_stylesheets=[FONT_URL, TEMPLATE_CSS, DBC_CSS],
    suppress_callback_exceptions=True,
    use_pages=True,
    index_string="""
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        """ + _ga_script + """
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
""",
)

server = app.server

# ── Cache (filesystem, condivisa tra worker via --preload) ────────────────────

cache = Cache(server, config={
    "CACHE_TYPE": "FileSystemCache",
    "CACHE_DIR": "/tmp/cesvi-indiceinfanzia",
    "CACHE_DEFAULT_TIMEOUT": 3600,   # 1 ora
})

# ── Route Flask per i PDF (serviti da data/reports/) ─────────────────────────

@server.route("/reports/<path:filename>")
def serve_report(filename):
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), REPORTS_DIR))
    filepath = os.path.join(reports_dir, filename)
    # Verifica che il file sia dentro reports_dir (path traversal prevention)
    if not os.path.abspath(filepath).startswith(reports_dir):
        abort(403)
    return send_from_directory(reports_dir, filename, as_attachment=False)


@server.route("/reports/download/<path:filename>")
def download_report(filename):
    """Scarica il PDF con nome normalizzato cesvi-indiceinfanzia_report_XXXX.pdf."""
    reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), REPORTS_DIR))
    filepath = os.path.join(reports_dir, filename)
    if not os.path.abspath(filepath).startswith(reports_dir):
        abort(403)
    # Estrai l'anno dal nome originale (primo gruppo di 4 cifre)
    import re
    m = re.search(r"(\d{4})", filename)
    year_str = m.group(1) if m else "0000"
    download_name = f"cesvi-indiceinfanzia_report_{year_str}.pdf"
    return send_from_directory(reports_dir, filename,
                               as_attachment=True,
                               download_name=download_name)
