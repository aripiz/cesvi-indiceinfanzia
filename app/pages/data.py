# data.py — pagina Dati

from dash import register_page
from configuration import TITLE

register_page(__name__, name=TITLE, path="/data")

from layout.layout_data import data_layout

layout = data_layout
