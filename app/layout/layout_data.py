# layout_data.py — Cesvi Indice Infanzia

from dash import dcc, html
import dash_bootstrap_components as dbc

from index import data
from configuration import (
    SEQUENCE_COLOR,
    INDEX_KEY,
    INDICATOR_LABELS,
    SUMMARY_INDICATORS,
    SUB_INDICATORS,
    CAPACITY_DIMS,
    YEARS_AVAILABLE,
    YEAR_DEFAULT,
)

# Opzioni per dropdown
territories_list = sorted(data["territory"].unique().tolist())
years_list = YEARS_AVAILABLE
feature_options = (
    [{"label": INDICATOR_LABELS.get(k, k), "value": k} for k in SUMMARY_INDICATORS]
    + [{"label": "── Componenti di dettaglio ──", "value": "_sep", "disabled": True}]
    + [{"label": INDICATOR_LABELS.get(k, k), "value": k} for k in SUB_INDICATORS]
)

# ── TAB: Mappa ───────────────────────────────────────────────────────────────

tab_map = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Componente"),
                        dcc.Dropdown(
                            id="map_feature",
                            options=feature_options,
                            value=INDEX_KEY,
                            labels={"search": "Cerca..."},
                        ),
                    ],
                    lg=6,
                    xs=12,
                ),
                dbc.Col(
                    [
                        dbc.Label("Anno"),
                        dcc.Slider(
                            years_list[0],
                            years_list[-1],
                            step=None,
                            id="map_year",
                            value=YEAR_DEFAULT,
                            marks={str(y): str(y) for y in years_list},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    lg=6,
                    xs=12,
                ),
            ],
            className="my-2",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(
                        id="choropleth_map",
                        style={"min-height": "65vh"},
                        config={
                            "displaylogo": False,
                            "modeBarButtonsToRemove": [
                                "pan2d", "select2d", "lasso2d", "zoom2d",
                            ],
                        },
                    ),
                    color=SEQUENCE_COLOR[0],
                ),
                lg=12,
                xs=12,
            ),
        ),
    ]
)

# ── TAB: Classifica ──────────────────────────────────────────────────────────

tab_ranking = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Componente"),
                        dcc.Dropdown(
                            id="ranking_feature",
                            options=feature_options,
                            value=INDEX_KEY,
                            labels={"search": "Cerca..."},
                        ),
                    ],
                    lg=6,
                    xs=12,
                ),
                dbc.Col(
                    [
                        dbc.Label("Anno"),
                        dcc.Slider(
                            years_list[0],
                            years_list[-1],
                            step=None,
                            id="ranking_year",
                            value=YEAR_DEFAULT,
                            marks={str(y): str(y) for y in years_list},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    lg=6,
                    xs=12,
                ),
            ],
            className="my-2",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(
                        id="ranking_chart",
                        style={"min-height": "65vh"},
                        config={"displaylogo": False},
                    ),
                    color=SEQUENCE_COLOR[0],
                ),
                lg=12,
                xs=12,
            ),
        ),
    ]
)

# ── TAB: Serie storica ───────────────────────────────────────────────────────

tab_evolution = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Regioni"),
                        dcc.Dropdown(
                            id="evolution_territories",
                            options=territories_list,
                            value=[territories_list[0]],
                            multi=True,
                            labels={"search": "Cerca..."},
                        ),
                    ],
                    lg=8,
                    xs=12,
                ),
                dbc.Col(
                    [
                        dbc.Label("Componente"),
                        dcc.Dropdown(
                            id="evolution_feature",
                            options=feature_options,
                            value=INDEX_KEY,
                            labels={"search": "Cerca..."},
                        ),
                    ],
                    lg=4,
                    xs=12,
                ),
            ],
            className="my-2",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(
                        id="evolution_chart",
                        style={"min-height": "60vh"},
                        config={"displaylogo": False},
                    ),
                    color=SEQUENCE_COLOR[0],
                ),
                lg=12,
                xs=12,
            ),
        ),
    ]
)

# ── TAB: Profilo regionale (radar) ───────────────────────────────────────────

tab_radar = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Regioni (max 3)"),
                        dcc.Dropdown(
                            id="radar_territories",
                            options=territories_list,
                            value=[territories_list[0]],
                            multi=True,
                            labels={"search": "Cerca..."},
                        ),
                    ],
                    lg=6,
                    xs=12,
                ),
                dbc.Col(
                    [
                        dbc.Label("Anno"),
                        dcc.Slider(
                            years_list[0],
                            years_list[-1],
                            step=None,
                            id="radar_year",
                            value=YEAR_DEFAULT,
                            marks={str(y): str(y) for y in years_list},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    lg=6,
                    xs=12,
                ),
            ],
            className="my-2",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(
                        id="radar_chart",
                        style={"min-height": "55vh"},
                        config={"displaylogo": False},
                    ),
                    color=SEQUENCE_COLOR[0],
                ),
                lg=10,
                xs=12,
            ),
            justify="center",
        ),
    ]
)

# ── TAB: Heatmap ─────────────────────────────────────────────────────────────

tab_heatmap = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Anno"),
                        dcc.Slider(
                            years_list[0],
                            years_list[-1],
                            step=None,
                            id="heatmap_year",
                            value=YEAR_DEFAULT,
                            marks={str(y): str(y) for y in years_list},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    lg=6,
                    xs=12,
                ),
            ],
            className="my-2",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(
                        id="heatmap_chart",
                        style={"min-height": "65vh"},
                        config={"displaylogo": False},
                    ),
                    color=SEQUENCE_COLOR[0],
                ),
                lg=12,
                xs=12,
            ),
        ),
    ]
)

# ── TAB: Correlazioni ────────────────────────────────────────────────────────

tab_correlations = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Asse X"),
                        dcc.Dropdown(
                            id="corr_x",
                            options=feature_options,
                            value="indice_rischio",
                            labels={"search": "Cerca..."},
                        ),
                    ],
                    lg=4,
                    xs=12,
                ),
                dbc.Col(
                    [
                        dbc.Label("Asse Y"),
                        dcc.Dropdown(
                            id="corr_y",
                            options=feature_options,
                            value="indice_prevenzione",
                            labels={"search": "Cerca..."},
                        ),
                    ],
                    lg=4,
                    xs=12,
                ),
                dbc.Col(
                    [
                        dbc.Label("Anno"),
                        dcc.Slider(
                            years_list[0],
                            years_list[-1],
                            step=None,
                            id="corr_year",
                            value=YEAR_DEFAULT,
                            marks={str(y): str(y) for y in years_list},
                            tooltip={"placement": "bottom", "always_visible": True},
                        ),
                    ],
                    lg=4,
                    xs=12,
                ),
            ],
            className="my-2",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(
                        id="corr_chart",
                        style={"min-height": "60vh"},
                        config={"displaylogo": False},
                    ),
                    color=SEQUENCE_COLOR[0],
                ),
                lg=12,
                xs=12,
            ),
        ),
    ]
)

# ── Struttura tab content ─────────────────────────────────────────────────────

tab_content_map = {
    "map": tab_map,
    "ranking": tab_ranking,
    "evolution": tab_evolution,
    "radar": tab_radar,
    "heatmap": tab_heatmap,
    "correlations": tab_correlations,
}
