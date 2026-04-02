# navigation.py — Cesvi Indice Infanzia

from index import app
from dash import Input, Output
from dash.exceptions import PreventUpdate

from layout.layout_data import tab_content_map


@app.callback(
    Output("data_tab_content", "children"),
    Input("data_tabs", "active_tab"),
)
def render_data_tab(active_tab):
    return tab_content_map.get(active_tab, "Seleziona una scheda.")


# Click sulla mappa home → vai alla scheda della regione
@app.callback(
    Output("store_territory", "data"),
    Output("url", "pathname"),
    Input("home_map", "clickData"),
    prevent_initial_call=True,
)
def home_map_to_scorecard(clickData):
    if not clickData:
        raise PreventUpdate
    territory = clickData["points"][0]["customdata"][0]
    return territory, "/scorecards"


# Click sulla mappa dati → vai alla scheda della regione
@app.callback(
    Output("store_territory", "data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    Input("choropleth_map", "clickData"),
    prevent_initial_call=True,
)
def data_map_to_scorecard(clickData):
    if not clickData:
        raise PreventUpdate
    territory = clickData["points"][0]["customdata"][0]
    return territory, "/scorecards"
