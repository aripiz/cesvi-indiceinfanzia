# data.py — pagina Dati

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name=TITLE, path="/data")

tabs = dbc.Tabs(
    children=[
        dbc.Tab(label="Mappa", tab_id="map"),
        dbc.Tab(label="Classifica", tab_id="ranking"),
        dbc.Tab(label="Serie storica", tab_id="evolution"),
        dbc.Tab(label="Profilo regionale", tab_id="radar"),
        dbc.Tab(label="Heatmap", tab_id="heatmap"),
        dbc.Tab(label="Correlazioni", tab_id="correlations"),
    ],
    id="data_tabs",
    active_tab="map",
    class_name="d-flex justify-content-around",
)

layout = dbc.Container(
    children=[
        html.P("Esplora — in costruzione.", className="mt-4 text-muted"),
        #dbc.Row(dbc.Col(tabs)),
        #dbc.Row(dbc.Col(id="data_tab_content"), className="mt-2"),
    ],
    class_name="mt-4",
)
