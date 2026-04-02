# layout_scorecards.py — Cesvi Indice Infanzia

from dash import dcc, html
import dash_bootstrap_components as dbc

from index import data
from configuration import (
    SEQUENCE_COLOR,
    INDEX_KEY,
    CAPACITY_DIMS,
    YEARS_AVAILABLE,
    YEAR_DEFAULT,
)

territories_list = sorted(data["territory"].unique().tolist())

scorecard_layout = dbc.Container(
    children=[
        dbc.Row(
            [
                dbc.Col(
                    html.P(
                        "Seleziona una regione per visualizzare la scheda di valutazione con i punteggi storici e il profilo dimensionale."
                    ),
                    lg=8,
                    xs=12,
                ),
                dbc.Col(
                    [
                        dbc.Label("Regione"),
                        dcc.Dropdown(
                            id="scorecard_territory",
                            options=territories_list,
                            value=territories_list[0],
                        ),
                    ],
                    lg=4,
                    xs=12,
                    align="end",
                ),
            ],
            className="mt-2",
            justify="evenly",
        ),
        # Header regione
        dbc.Row(
            dbc.Col(html.H2(id="scorecard_header"), lg=12),
            className="mt-3",
            justify="evenly",
        ),
        # Mappa + score sintetico
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(
                            id="scorecard_map",
                            style={"height": "200px", "width": "300px"},
                            config={"displayModeBar": False, "editable": False},
                        ),
                        color=SEQUENCE_COLOR[0],
                    ),
                    lg=3,
                    xs=12,
                    align="center",
                ),
                dbc.Col(
                    [
                        html.H5("Indice totale (z-score)"),
                        html.P(id="scorecard_score"),
                        html.H5("Posizione in classifica"),
                        html.P(id="scorecard_rank"),
                        html.H5("Anno"),
                        dbc.RadioItems(
                            id="scorecard_year",
                            options=[{"label": str(y), "value": y} for y in YEARS_AVAILABLE],
                            value=YEAR_DEFAULT,
                            inline=True,
                        ),
                    ],
                    lg=4,
                    xs=12,
                    align="end",
                ),
                dbc.Col(
                    [
                        html.H5("Fascia"),
                        html.P(id="scorecard_tier"),
                        html.H5("Variazione vs anno precedente"),
                        html.P(id="scorecard_change"),
                    ],
                    lg=5,
                    xs=12,
                    align="end",
                ),
            ],
            className="mt-3",
            justify="evenly",
        ),
        # Serie storica indice totale
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Serie storica — Indice totale"),
                        dcc.Loading(
                            dcc.Graph(
                                id="scorecard_evolution",
                                config={
                                    "displaylogo": False,
                                    "modeBarButtonsToRemove": [
                                        "pan2d", "select2d", "lasso2d",
                                        "zoom2d", "resetScale2d",
                                    ],
                                },
                            ),
                            color=SEQUENCE_COLOR[0],
                        ),
                    ],
                    lg=12,
                    xs=12,
                ),
            ],
            className="mt-4",
        ),
        # Profilo dimensionale radar (2022/2024)
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Profilo dimensionale (2022 – 2024)"),
                        dbc.Alert(
                            "I dati dimensionali sono disponibili solo per il 2022 e il 2024.",
                            color="info",
                            dismissable=True,
                            className="mt-2",
                        ),
                        dcc.Loading(
                            dcc.Graph(
                                id="scorecard_radar",
                                config={"displaylogo": False},
                            ),
                            color=SEQUENCE_COLOR[0],
                        ),
                    ],
                    lg=8,
                    xs=12,
                ),
                dbc.Col(
                    [
                        html.H4("Ranking dimensionale 2024"),
                        html.Div(id="scorecard_dim_table"),
                    ],
                    lg=4,
                    xs=12,
                    align="center",
                ),
            ],
            className="mt-4",
        ),
    ],
    fluid=True,
)
