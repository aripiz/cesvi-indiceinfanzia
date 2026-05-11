# layout_scorecards_new.py — Cesvi Indice Infanzia (versione provvisoria con nuovi stili)
# Idee implementate:
#   1. Accent bar arancione sotto il titolo regione
#   2. KPI card per le 4 metriche (bordo sinistro arancione, valore grande)
#   3. Section divider con accent line prima di ogni sezione grafico
#   4. Sfondo leggero (#f8f9fa + border-radius) sulla colonna dati KPI

from dash import dcc, html
import dash_bootstrap_components as dbc

from index import data
from configuration import SEQUENCE_COLOR, YEARS, YEAR_DEFAULT

territories_list = sorted(data["territory"].unique().tolist())


def _section_divider(title):
    """Separatore di sezione: linea arancione + label testo muted."""
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
    """KPI card con bordo sinistro arancione, valore grande, label piccola."""
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
        # ── Titolo pagina ─────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col([
                html.H2("Regioni", className="mb-1"),
                html.Div(style={
                    "width": "40px", "height": "4px",
                    "backgroundColor": "#eb6608", "marginBottom": "0.5rem",
                }),
                html.P(
                    "Approfondisci i risultati di ciascuna regione nell\u2019Indice. "
                    "I dati mostrati si riferiscono all\u2019edizione 2026.",
                    className="text-muted mb-2",
                    style={"fontSize": "0.92rem"},
                ),
            ], xs=12),
            className="mb-2",
        ),
        # ── Selezione territorio ──────────────────────────────────────────────
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

        # ── Header regione con accent bar ────────────────────────────────────
        dbc.Row(
            dbc.Col(
                [
                    html.H4(id="scorecard_header", className="mb-1 fw-bold"),
                    # Idea 1: accent bar arancione sotto il titolo
                    html.Div(style={
                        "width": "60px",
                        "height": "4px",
                        "backgroundColor": "#eb6608",
                        "marginBottom": "0.75rem",
                    }),
                ],
                lg=12,
            ),
            className="mt-3",
        ),

        # ── Mappa + KPI card + evoluzione ────────────────────────────────────
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

                # Idea 2 + 4: blocco KPI con sfondo grigio chiaro e bordo radius
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
                            "borderRadius": "8px",
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
                                config={"displayModeBar": False},
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

        # ── Posizione per capacità + Punteggio per capacità ──────────────────
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(
                            id="scorecard_lollipop",
                            config={"displayModeBar": False},
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
                            config={"displayModeBar": False},
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

        # ── Scatter Servizi vs Rischio ────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    dcc.Graph(
                        id="scorecard_scatter",
                        config={"displayModeBar": False},
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
