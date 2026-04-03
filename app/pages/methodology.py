# methodology.py — pagina Metodologia

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name=TITLE, path="/methodology")

# TODO: implementare layout metodologia
layout = dbc.Container(
    html.P("Metodologia — in costruzione.", className="mt-4 text-muted"),
    class_name="mt-4",
)
