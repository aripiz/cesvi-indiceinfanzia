# layout_scorecards.py — Cesvi Indice Infanzia

from dash import dcc, html
import dash_bootstrap_components as dbc

from index import data
from configuration import SEQUENCE_COLOR, YEARS, YEAR_DEFAULT

territories_list = sorted(data["territory"].unique().tolist())

scorecard_layout = dbc.Container(
    children=[
        # ── Selezione territorio ──────────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(
                    html.P(
                        "Seleziona una regione per visualizzare la scheda con il "
                        "profilo e i dati sintetici."
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
        # ── Header regione ────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col(html.H2(id="scorecard_header"), lg=12),
            className="mt-3",
        ),
        # ── Mappa + dati sintetici ────────────────────────────────────────────
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
                        html.H5("Punteggio"),
                        html.P(id="scorecard_score"),
                        html.H5("Posizione"),
                        html.P(id="scorecard_rank"),
                        #html.H5("Anno"),
                        #html.P(str(YEAR_DEFAULT)),
                        # Selezione anno disabilitata — fissa a YEAR_DEFAULT
                        dbc.RadioItems(
                            id="scorecard_year",
                            options=[{"label": str(y), "value": y} for y in YEARS],
                            value=YEAR_DEFAULT,
                            inline=True,
                            style={"display": "none"},
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
                        html.H5("Variazione posizione"),
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
        # ── Grafici: ranking + radar ──────────────────────────────────────────
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Evoluzione posizione"),
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
                    lg=6,
                    xs=12,
                ),
                dbc.Col(
                    [
                        html.H4("Posizione per capacità"),
                        dcc.Loading(
                            dcc.Graph(
                                id="scorecard_radar",
                                config={"displaylogo": False},
                            ),
                            color=SEQUENCE_COLOR[0],
                        ),
                    ],
                    lg=6,
                    xs=12,
                ),
            ],
            className="mt-4",
        ),
        # ── Barre z-score per capacità ──────────────────────────────
        dbc.Row(
            dbc.Col(
                [
                    html.H4("Punteggio per capacità"),
                    dcc.Loading(
                        dcc.Graph(
                            id="scorecard_dim_table",
                            config={"displayModeBar": False},
                        ),
                        color=SEQUENCE_COLOR[0],
                    ),
                ],
                lg=12,
                xs=12,
            ),
            className="mt-4",
        ),
    ],
    fluid=True,
)
