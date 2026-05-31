# methodology.py — pagina Metodologia

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name=TITLE, path="/methodology")

from layout.layout_methodology import methodology_layout

layout = methodology_layout

