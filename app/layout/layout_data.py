# layout_data.py — Cesvi Indice Infanzia

from dash import dcc, html
import dash_bootstrap_components as dbc

from index import data
from configuration import (
    SEQUENCE_COLOR,
    CAPACITY_DIMS,
    CAPACITY_ORDER,
    INDEX_LABELS,
    YEARS,
    YEAR_DEFAULT,
)

territories_list = sorted(data["territory"].unique().tolist())
years_list = YEARS

# ── Dropdown options ────────────────────────────────────────────────────────

_POP_LABELS = {"adulti": "Adulti", "bambini": "Bambini", "totale": "Totale"}

# Valid indicator combinations present in the dataset
_valid_combos = set(
    data[["type", "capacity", "population"]]
    .drop_duplicates()
    .apply(lambda r: f"{r['type']}||{r['capacity']}||{r['population']}", axis=1)
)


def _opt(label, value, disabled=False):
    """Crea opzione dropdown solo se la combo è presente nei dati."""
    if not disabled and not value.startswith("_") and value not in _valid_combos:
        return None
    d = {"label": label, "value": value}
    if disabled:
        d["disabled"] = True
    return d


# Dropdown unico "Indicatore": "type||capacity||population"
_raw_options = [
    _opt("── Indici aggregati ──", "_ih", disabled=True),
    _opt("Indici aggregati - Totale",                "totale||totale||totale"),
    _opt("Indici aggregati - Fattori di rischio",            "rischio||totale||totale"),
    _opt("Indici aggregati - Fattori di rischio - Adulti",   "rischio||totale||adulti"),
    _opt("Indici aggregati - Fattori di rischio - Bambini",  "rischio||totale||bambini"),
    _opt("Indici aggregati - Servizi",           "servizi||totale||totale"),
    _opt("Indici aggregati - Servizi - Adulti",  "servizi||totale||adulti"),
    _opt("Indici aggregati - Servizi - Bambini", "servizi||totale||bambini"),
    _opt("── Capacità - Fattori di rischio ──", "_crf", disabled=True),
    *[_opt(f"Capacità - Fattori di rischio - {CAPACITY_DIMS[k]} - {_POP_LABELS[p]}", f"rischio||{k}||{p}") for k in CAPACITY_ORDER for p in ["adulti", "bambini", "totale"]],
    _opt("── Capacità - Servizi ──", "_csf", disabled=True),
    *[_opt(f"Capacità - Servizi - {CAPACITY_DIMS[k]} - {_POP_LABELS[p]}", f"servizi||{k}||{p}") for k in CAPACITY_ORDER for p in ["adulti", "bambini", "totale"]],
]
indicatore_options = [o for o in _raw_options if o is not None]

pop_options = [
    {"label": "Adulti",  "value": "adulti"},
    {"label": "Bambini", "value": "bambini"},
    {"label": "Totale",  "value": "totale"},
]
dim_options = [
    {"label": "Fattori di rischio", "value": "rischio"},
    {"label": "Servizi",            "value": "servizi"},
]

# ── UI helpers ──────────────────────────────────────────────────────────────

ACCENT = "#eb6608"
MUTED  = "#6b7280"


def _section_label(text):
    return html.Span(
        text,
        style={
            "fontSize": "0.7rem",
            "fontWeight": "700",
            "textTransform": "uppercase",
            "letterSpacing": "0.1em",
            "color": MUTED,
        },
    )


def _filter_box(children):
    return html.Div(
        children,
        style={
            "backgroundColor": "#f8f9fa",
            "borderLeft": f"3px solid {ACCENT}",
            "borderRadius": "6px",
            "padding": "12px 16px",
        },
        className="mb-3",
    )


def _info_box(text):
    return html.Div(
        [
            html.Span("ℹ", style={"color": ACCENT, "fontWeight": "700", "marginRight": "0.5rem", "fontSize": "1rem"}),
            html.Span(text, style={"fontSize": "0.88rem", "color": MUTED}),
        ],
        style={
            "backgroundColor": "#fff",
            "border": "1px solid #e9ecef",
            "borderLeft": f"3px solid {ACCENT}",
            "borderRadius": "4px",
            "padding": "8px 14px",
            "lineHeight": "1.65",
        },
        className="mb-3",
    )


def _year_slider(slider_id):
    return dcc.Slider(
        years_list[0], years_list[-1],
        step=None,
        id=slider_id,
        value=YEAR_DEFAULT,
        marks={str(y): str(y) for y in years_list},
        tooltip={"placement": "bottom", "always_visible": False},
    )


def _graph(graph_id, min_height="65vh"):
    return dcc.Loading(
        dcc.Graph(
            id=graph_id,
            style={"min-height": min_height},
            config={"displayModeBar": False, "editable": False},
        ),
        color=SEQUENCE_COLOR[0],
    )


def _indicatore_dropdown(component_id, value="totale||totale||totale"):
    return dcc.Dropdown(
        id=component_id,
        options=indicatore_options,
        value=value,
        clearable=False,
        className="mt-1",
    )


def _pop_radio(component_id, value="totale"):
    return dbc.RadioItems(
        id=component_id,
        options=pop_options,
        value=value,
        inline=True,
        inputCheckedClassName="border-warning bg-warning",
        className="mt-1",
    )


# ── Tab: Map ────────────────────────────────────────────────────────────────

tab_map = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Indicatore"),
            _indicatore_dropdown("map_indicatore"),
        ], lg=8, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("map_year"),
        ], lg=4, xs=12),
    ], className="g-3 align-items-start")),
    _info_box(
        "La mappa mostra il punteggio dell\u2019indicatore selezionato per ciascuna regione italiana. "
        "Scegli l\u2019indicatore (indice aggregato, fattori di rischio o servizi per capacit\u00e0) e l\u2019anno "
        "di riferimento dal pannello sopra. Le regioni sono colorate in base al livello relativo rispetto "
        "alla media nazionale."
    ),
    _graph("data_map"),
])

# ── Tab: Ranking ────────────────────────────────────────────────────────────

tab_ranking = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Indicatore"),
            _indicatore_dropdown("ranking_indicatore"),
        ], lg=8, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("ranking_year"),
        ], lg=4, xs=12),
    ], className="g-3 align-items-start")),
    _info_box(
        "La classifica ordina le regioni italiane in base al punteggio dell\u2019indicatore e dell\u2019anno selezionati. "
        "Punteggi positivi indicano una performance migliore della media nazionale; punteggi negativi indicano "
        "una performance peggiore. Il colore delle barre riflette l\u2019area geografica di appartenenza."
    ),
    _graph("data_ranking"),
])

# ── Tab: Time series ────────────────────────────────────────────────────────

tab_evolution = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Regioni da confrontare"),
            dcc.Dropdown(
                id="evo_territories",
                options=territories_list,
                value=[territories_list[0]],
                multi=True,
                placeholder="Seleziona una o più regioni…",
                className="mt-1",
            ),
        ], lg=5, xs=12),
        dbc.Col([
            _section_label("Indicatore"),
            _indicatore_dropdown("evo_indicatore"),
        ], lg=7, xs=12),
    ], className="g-3 align-items-start")),
    _info_box(
        "Il grafico mostra l\u2019andamento del punteggio nel tempo. "
        "Seleziona una o pi\u00f9 regioni e l\u2019indicatore di interesse per confrontarne l\u2019evoluzione "
        "dalla prima rilevazione disponibile (2018) ad oggi. Le regioni selezionate appaiono come linee distinte."
    ),
    _graph("data_evolution", min_height="60vh"),
])

# ── Tab: Regional profile ────────────────────────────────────────────────────

tab_profilo = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Regione"),
            dcc.Dropdown(
                id="profilo_territory",
                options=territories_list,
                value=territories_list[0],
                clearable=False,
                className="mt-1",
            ),
        ], lg=4, xs=12),
        dbc.Col([
            _section_label("Dimensione"),
            dbc.RadioItems(
                id="profilo_dim_type",
                options=dim_options,
                value="rischio",
                inline=True,
                inputCheckedClassName="border-warning bg-warning",
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("profilo_year"),
        ], lg=5, xs=12),
    ], className="g-3 align-items-start")),
    _info_box(
        "Il pannello mostra il profilo della regione selezionata rispetto alle 6 capacit\u00e0 dell\u2019Indice, "
        "distinguendo tra fattori di rischio e servizi. Il grafico a sinistra indica la posizione in classifica "
        "per ciascuna capacit\u00e0; quello a destra riporta i punteggi normalizzati rispetto alla media nazionale."
    ),
    dbc.Row([
        dbc.Col([
            html.Div(
                html.Span(
                    "Posizione per capacità",
                    style={"fontSize": "0.7rem", "fontWeight": "700",
                           "textTransform": "uppercase", "letterSpacing": "0.08em",
                           "color": MUTED},
                ),
                className="mb-1",
            ),
            _graph("data_lollipop", min_height="40vh"),
        ], lg=6, xs=12),
        dbc.Col([
            html.Div(
                html.Span(
                    "Punteggio per capacità",
                    style={"fontSize": "0.7rem", "fontWeight": "700",
                           "textTransform": "uppercase", "letterSpacing": "0.08em",
                           "color": MUTED},
                ),
                className="mb-1",
            ),
            _graph("data_dim_table", min_height="40vh"),
        ], lg=6, xs=12),
    ]),
])

# ── Tab: Heatmap overview ────────────────────────────────────────────────────

tab_heatmap = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Vista"),
            dbc.RadioItems(
                id="heatmap_dim_type",
                options=[
                    {"label": "Indici aggregati", "value": "indici"},
                    {"label": "Capacità - Fattori di rischio", "value": "rischio"},
                    {"label": "Capacità - Servizi", "value": "servizi"},
                ],
                value="indici",
                inline=True,
                inputCheckedClassName="border-warning bg-warning",
                className="mt-1",
            ),
        ], lg=7, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("heatmap_year"),
        ], lg=5, xs=12),
    ], className="g-3 align-items-start")),
    _graph("data_heatmap"),
])

# ── Tab: Correlations ────────────────────────────────────────────────────────

tab_correlations = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Asse X"),
            _indicatore_dropdown("corr_x", value="rischio||totale||totale"),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Asse Y"),
            _indicatore_dropdown("corr_y", value="servizi||totale||totale"),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Evidenzia regione"),
            dcc.Dropdown(
                id="corr_highlight",
                options=[{"label": t, "value": t} for t in territories_list],
                value=None,
                clearable=True,
                placeholder="Nessuna…",
                className="mt-1",
            ),
        ], lg=2, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("corr_year"),
        ], lg=4, xs=12),
    ], className="g-3 align-items-start")),
    _info_box(
        "Il grafico a dispersione confronta la posizione delle regioni rispetto a due indicatori contemporaneamente. "
        "Ogni punto rappresenta una regione: la distanza dagli assi riflette la performance relativa nelle due "
        "dimensioni selezionate. \u00c8 possibile evidenziare una regione specifica dal menu. "
        "Il coefficiente di correlazione di Spearman \u03c1\u209b \u00e8 riportato sopra il grafico."
    ),
    html.Div(id="corr_spearman_badge", className="mb-2"),
    _graph("data_correlations", min_height="60vh"),
])

# ── Tab content map ─────────────────────────────────────────────────────────

tab_content_map = {
    "map":          tab_map,
    "ranking":      tab_ranking,
    "evolution":    tab_evolution,
    "profilo":      tab_profilo,
    "confronto":    tab_correlations,
}

# ── Main layout ─────────────────────────────────────────────────────────────

data_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col([
                html.H3("Dati", className="page-title"),
                html.P(
                    "Esplora i risultati numerici dell\u2019Indice attraverso diverse visualizzazioni: "
                    "mappe, classifiche, serie storiche, profili per capacità e correlazioni.",
                    className="text-muted mb-3",
                    style={"fontSize": "0.92rem"},
                ),
            ], xs=12),
        ),
        dbc.Tabs(
            id="data_viz_tabs",
            active_tab="map",
            class_name="d-flex justify-content-around",
            children=[
                dbc.Tab(label="Mappa",                  tab_id="map"),
                dbc.Tab(label="Classifica",             tab_id="ranking"),
                dbc.Tab(label="Serie storiche",         tab_id="evolution"),
                dbc.Tab(label="Profili capacità",                tab_id="profilo"),
                dbc.Tab(label="Confronto posizioni",    tab_id="confronto"),
            ],
        ),
        html.Div(id="data_viz_content", className="mt-3"),
    ],
    class_name="mt-4",
    fluid=False,
)
