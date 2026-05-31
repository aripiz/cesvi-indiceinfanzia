# layout_scorecards.py — Cesvi Indice Infanzia

from dash import dcc, html
import dash_bootstrap_components as dbc

from index import data
from configuration import SEQUENCE_COLOR, YEARS, YEAR_DEFAULT

territories_list = sorted(data["territory"].unique().tolist())


def _section_divider(title):
    """Section divider: short orange line + muted uppercase label + full-width grey rule."""
    return html.Div(
        [
            html.Div(
                className="d-flex align-items-center gap-3",
                children=[
                    html.Div(style={
                        "width": "32px",
                        "height": "3px",
                        "backgroundColor": "#eb6608",
                        "flexShrink": "0",
                    }),
                    html.Span(
                        title,
                        style={
                            "fontSize": "0.7rem",
                            "fontWeight": "700",
                            "textTransform": "uppercase",
                            "letterSpacing": "0.1em",
                            "color": "#6b7280",
                        },
                    ),
                    html.Div(style={
                        "flex": "1",
                        "height": "1px",
                        "backgroundColor": "#e9ecef",
                    }),
                ],
            )
        ],
        className="mt-4 mb-2",
    )


def _kpi_card(label, element_id):
    """KPI card: left orange border, large value, small uppercase label."""
    return html.Div(
        [
            html.P(
                id=element_id,
                className="mb-0",
                style={"fontSize": "1.35rem", "fontWeight": "700", "color": "#1a1a1a"},
            ),
            html.Span(
                label,
                style={"fontSize": "0.72rem", "fontWeight": "600",
                       "textTransform": "uppercase", "letterSpacing": "0.08em",
                       "color": "#6b7280"},
            ),
        ],
        style={
            "borderLeft": "3px solid #eb6608",
            "paddingLeft": "10px",
            "paddingTop": "6px",
            "paddingBottom": "6px",
        },
        className="mb-3",
    )


scorecard_layout = dbc.Container(
    children=[
        # ── Page title ───────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col([
                html.H3("Regioni", className="page-title"),
                html.P(
                    "Approfondisci i risultati di ciascuna regione nell\u2019Indice.",
                    className="text-muted mb-3",
                    style={"fontSize": "0.92rem"},
                ),
                html.Div(
                    [
                        html.Span("\u2139", style={"color": "#eb6608", "fontWeight": "700", "marginRight": "0.5rem", "fontSize": "1rem"}),
                        html.Span("I dati mostrati si riferiscono all\u2019edizione 2026.", style={"fontSize": "0.88rem", "color": "#6b7280"}),
                    ],
                    style={
                        "backgroundColor": "#fff",
                        "border": "1px solid #e9ecef",
                        "borderLeft": "3px solid #eb6608",
                        "borderRadius": "4px",
                        "padding": "8px 14px",
                        "lineHeight": "1.65",
                        "display": "inline-block",
                    },
                    className="mb-2",
                ),
            ], xs=12),
            className="mb-2",
        ),
        # ── Territory selection ───────────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.Div(
                            [
                                html.Span(
                                    "Regione",
                                    style={
                                        "fontSize": "0.7rem",
                                        "fontWeight": "700",
                                        "textTransform": "uppercase",
                                        "letterSpacing": "0.1em",
                                        "color": "#6b7280",
                                        "marginBottom": "4px",
                                        "display": "block",
                                    },
                                ),
                                dcc.Dropdown(
                                    id="scorecard_territory",
                                    options=territories_list,
                                    value=territories_list[0],
                                    clearable=False,
                                    labels={"search": "Cerca..."},
                                ),
                            ],
                            style={"minWidth": "220px", "maxWidth": "320px"},
                        ),
                        html.P(
                            "Seleziona una regione per visualizzare i suoi risultati nell\u2019Indice.",
                            className="mb-0 text-muted",
                            style={"fontSize": "0.88rem"},
                        ),
                    ],
                    className="d-flex align-items-center gap-4 flex-wrap",
                    style={
                        "backgroundColor": "#f8f9fa",
                        "borderLeft": "3px solid #eb6608",
                        "borderRadius": "6px",
                        "padding": "12px 16px",
                    },
                ),
                lg=12,
            ),
            className="mt-2",
        ),

        # ── Region header ─────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                html.H5(id="scorecard_header", className="page-title"),
                lg=12,
            ),
            className="mt-3",
        ),

        # ── Map + KPI cards + evolution ───────────────────────────────────────
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
                    className="d-flex justify-content-center",
                ),

                # KPI block
                dbc.Col(
                    html.Div(
                        [
                            _kpi_card("Punteggio", "scorecard_score"),
                            _kpi_card("Posizione", "scorecard_rank"),
                            _kpi_card("Fascia", "scorecard_tier"),
                            _kpi_card(f"Variazione (dal {YEARS[0]})", "scorecard_change"),
                            dbc.RadioItems(
                                id="scorecard_year",
                                options=[{"label": str(y), "value": y} for y in YEARS],
                                value=YEAR_DEFAULT,
                                inline=True,
                                style={"display": "none"},
                            ),
                        ],
                        style={
                            "backgroundColor": "#f8f9fa",
                            "borderRadius": "6px",
                            "padding": "16px 14px",
                            "height": "100%",
                        },
                    ),
                    lg=2,
                    xs=12,
                    align="start",
                ),

                dbc.Col(
                    [
                        _section_divider("Evoluzione posizione Indici aggregati"),
                        dcc.Loading(
                            dcc.Graph(
                                id="scorecard_evolution",
                                config={"displayModeBar": False, "editable": False, "doubleClick": False},
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

        # Idea 3: section divider
        _section_divider("Posizione e punteggio per capacità"),

        # ── Rank by capacity + Score by capacity ────────────────────────────
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(
                            id="scorecard_lollipop",
                            config={"displayModeBar": False, "editable": False, "doubleClick": False},
                        ),
                        color=SEQUENCE_COLOR[0],
                    ),
                    lg=6,
                    xs=12,
                ),
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(
                            id="scorecard_dim_table",
                            config={"displayModeBar": False, "editable": False, "doubleClick": False},
                        ),
                        color=SEQUENCE_COLOR[0],
                    ),
                    lg=6,
                    xs=12,
                ),
            ],
        ),

        # Idea 3: section divider
        _section_divider("Correlazione fattori di rischio · servizi"),

        # ── Scatter: Services vs Risk ──────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(
                        id="scorecard_scatter",
                        config={"displayModeBar": False, "editable": False, "doubleClick": False},
                    ),
                    color=SEQUENCE_COLOR[0],
                ),
                lg=12,
                xs=12,
            ),
        ),
    ],
    fluid=False,
    class_name="mt-4",
)
