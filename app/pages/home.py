# home.py — pagina Home

from dash import register_page
from configuration import TITLE

register_page(__name__, path="/", name=TITLE)

from layout.layout_home import home_layout

layout = home_layout
