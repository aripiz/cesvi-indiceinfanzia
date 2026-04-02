# home.py — pagina Home

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, path="/", name=TITLE)

from layout.layout_home import home_layout

layout = dbc.Container(
    children=home_layout,
    class_name="mt-4",
)
