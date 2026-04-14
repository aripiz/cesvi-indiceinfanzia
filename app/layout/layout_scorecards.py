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
                        "Seleziona una regione per visualizzare i suoi risultati nell'Indice."
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
        # ── Mappa + dati sintetici + evoluzione ──────────────────────────────
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(
                            id="scorecard_map",
                            style={"height": "200px", "width": "220px"},
                            config={"displayModeBar": False, "editable": False},
                        ),
                        color=SEQUENCE_COLOR[0],
                    ),
                    lg=2,
                    xs=12,
                    align="center",
                ),
                dbc.Col(
                    [
                        html.H5("Punteggio"), html.P(id="scorecard_score"),
                        html.H5("Posizione"), html.P(id="scorecard_rank"),
                        html.H5("Fascia"), html.P(id="scorecard_tier"),
                        html.H5("Variazione posizione"), html.P(id="scorecard_change"),
                        dbc.RadioItems(
                            id="scorecard_year",
                            options=[{"label": str(y), "value": y} for y in YEARS],
                            value=YEAR_DEFAULT,
                            inline=True,
                            style={"display": "none"},
                        ),
                    ],
                    lg=2,
                    xs=12,
                    align="start",
                ),
                dbc.Col(
                    [
                        html.H5("Evoluzione posizione"),
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
                    lg=8,
                    xs=12,
                    align="start",
                ),
            ],
            className="mt-3",
            align="start",
        ),
        # ── Posizione per capacità + Punteggio per capacità ───────────────────
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Posizione per capacità"),
                        dcc.Loading(
                            dcc.Graph(
                                id="scorecard_lollipop",
                                config={"displayModeBar": False},
                            ),
                            color=SEQUENCE_COLOR[0],
                        ),
                    ],
                    lg=6,
                    xs=12,
                ),
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
                    lg=6,
                    xs=12,
                ),
            ],
            className="mt-4",
        ),
        # ── Scatter Servizi vs Rischio ─────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                [
                    html.H4("Correlazione Fattori di rischio - Servizi"),
                    dcc.Loading(
                        dcc.Graph(
                            id="scorecard_scatter",
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
    fluid=False,
)
