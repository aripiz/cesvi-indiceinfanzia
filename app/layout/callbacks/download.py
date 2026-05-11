# download.py — Cesvi Indice Infanzia

from io import BytesIO
import pandas as pd
from dash import Input, Output, State, ctx, dcc
from dash.exceptions import PreventUpdate

from index import app, data, metadata


@app.callback(
    Output("download_modal", "is_open"),
    Input("navbar_download_btn", "n_clicks"),
    Input("home_download_btn", "n_clicks"),
    Input("close_download_modal_btn", "n_clicks"),
    State("download_modal", "is_open"),
    prevent_initial_call=True,
)
def toggle_download_modal(open_nav, open_home, close_clicks, is_open):
    triggered = ctx.triggered_id
    if triggered in ("open_download", "home_download_btn"):
        return True
    if triggered == "close_download_modal_btn":
        return False
    return is_open


@app.callback(
    Output("download_wide", "data"),
    Input("download_wide_btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_wide(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    return {"filename": "cesvi-indiceinfanzia_wide.csv", "content": data.to_csv(index=False), "type": "text/csv"}


@app.callback(
    Output("download_long", "data"),
    Input("download_long_btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_long(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    id_vars = ["territory", "year"]
    value_vars = [c for c in data.columns if c not in id_vars]
    df_long = data.melt(id_vars=id_vars, value_vars=value_vars, var_name="indicator", value_name="value")
    return {
        "filename": "cesvi-indiceinfanzia_long.csv",
        "content": df_long.to_csv(index=False),
        "type": "text/csv",
    }


@app.callback(
    Output("download_excel", "data"),
    Input("download_excel_btn", "n_clicks"),
    prevent_initial_call=True,
)
def download_excel_file(n_clicks):
    if not n_clicks:
        raise PreventUpdate
    buf = BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        data.to_excel(writer, sheet_name="Dati", index=False)
        metadata.to_excel(writer, sheet_name="Metadati", index=False)
    buf.seek(0)
    return dcc.send_bytes(buf.read(), "cesvi-indiceinfanzia_dati.xlsx")
