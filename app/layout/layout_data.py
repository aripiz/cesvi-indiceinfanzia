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

# ── Opzioni dropdown / radio riusate più tab ──────────────────────────────────

index_options    = [{"label": v, "value": k} for k, v in INDEX_LABELS.items()]
capacity_options = [{"label": CAPACITY_DIMS[k], "value": k} for k in CAPACITY_ORDER]
pop_options      = [
    {"label": "Adulti",  "value": "adulti"},
    {"label": "Bambini", "value": "bambini"},
    {"label": "Totale",  "value": "totale"},
]
dim_options = [
    {"label": "Fattori di rischio", "value": "rischio"},
    {"label": "Servizi",            "value": "servizi"},
]

# ── Helpers UI (same visual language as layout_scorecards_new) ────────────────

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
    """Riquadro filtri con accent bar a sinistra (come la selezione regione)."""
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

def _year_slider(slider_id, className=""):
    return dcc.Slider(
        years_list[0], years_list[-1],
        step=None,
        id=slider_id,
        value=YEAR_DEFAULT,
        marks={str(y): str(y) for y in years_list},
        tooltip={"placement": "bottom", "always_visible": True},
        className=className,
    )

def _graph(graph_id, min_height="65vh"):
    return dcc.Loading(
        dcc.Graph(
            id=graph_id,
            style={"min-height": min_height},
            config={
                "displaylogo": False,
                "modeBarButtonsToRemove": ["pan2d", "select2d", "lasso2d", "zoom2d"],
            },
        ),
        color=SEQUENCE_COLOR[0],
    )

# ── Tab: Mappa ────────────────────────────────────────────────────────────────

tab_map = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Indice"),
            dbc.RadioItems(
                id="map_index_type",
                options=index_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Capacità"),
            dcc.Dropdown(
                id="map_capacity",
                options=capacity_options,
                value=None,
                placeholder="Solo per indici rischio/servizi…",
                disabled=True,
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Popolazione"),
            dbc.RadioItems(
                id="map_population",
                options=pop_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("map_year"),
        ], lg=3, xs=12),
    ], className="g-3 align-items-start")),
    _graph("data_map"),
])

# ── Tab: Classifica ───────────────────────────────────────────────────────────

tab_ranking = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Indice"),
            dbc.RadioItems(
                id="ranking_index_type",
                options=index_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Capacità"),
            dcc.Dropdown(
                id="ranking_capacity",
                options=capacity_options,
                value=None,
                placeholder="Solo per indici rischio/servizi…",
                disabled=True,
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Popolazione"),
            dbc.RadioItems(
                id="ranking_population",
                options=pop_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("ranking_year"),
        ], lg=3, xs=12),
    ], className="g-3 align-items-start")),
    _graph("data_ranking"),
])

# ── Tab: Serie storica ────────────────────────────────────────────────────────

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
        ], lg=4, xs=12),
        dbc.Col([
            _section_label("Indice"),
            dbc.RadioItems(
                id="evo_index_type",
                options=index_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Capacità"),
            dcc.Dropdown(
                id="evo_capacity",
                options=capacity_options,
                value=None,
                placeholder="Solo per indici rischio/servizi…",
                disabled=True,
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Popolazione"),
            dbc.RadioItems(
                id="evo_population",
                options=pop_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=2, xs=12),
    ], className="g-3 align-items-start")),
    _graph("data_evolution", min_height="60vh"),
])

# ── Tab: Profilo regionale (radar) ────────────────────────────────────────────

tab_radar = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Regioni da confrontare (max 3)"),
            dcc.Dropdown(
                id="radar_territories",
                options=territories_list,
                value=[territories_list[0]],
                multi=True,
                placeholder="Seleziona fino a 3 regioni…",
                className="mt-1",
            ),
        ], lg=4, xs=12),
        dbc.Col([
            _section_label("Dimensione"),
            dbc.RadioItems(
                id="radar_dim_type",
                options=[{"label": "Totale (media)", "value": "totale"}] + dim_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Popolazione"),
            dbc.RadioItems(
                id="radar_population",
                options=pop_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("radar_year"),
        ], lg=2, xs=12),
    ], className="g-3 align-items-start")),
    _graph("data_radar", min_height="55vh"),
])

# ── Tab: Heatmap ──────────────────────────────────────────────────────────────

tab_heatmap = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Dimensione"),
            dbc.RadioItems(
                id="heatmap_dim_type",
                options=[{"label": "Tutti gli indici", "value": "all"}] + dim_options,
                value="all",
                inline=True,
                className="mt-1",
            ),
        ], lg=4, xs=12),
        dbc.Col([
            _section_label("Popolazione"),
            dbc.RadioItems(
                id="heatmap_population",
                options=pop_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("heatmap_year"),
        ], lg=5, xs=12),
    ], className="g-3 align-items-start")),
    _graph("data_heatmap"),
])

# ── Tab: Correlazioni ─────────────────────────────────────────────────────────

tab_correlations = html.Div([
    _filter_box(dbc.Row([
        dbc.Col([
            _section_label("Asse X — capacità"),
            dcc.Dropdown(
                id="corr_x",
                options=capacity_options,
                value=CAPACITY_ORDER[0],
                clearable=False,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Asse Y — capacità"),
            dcc.Dropdown(
                id="corr_y",
                options=capacity_options,
                value=CAPACITY_ORDER[1],
                clearable=False,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Dimensione"),
            dbc.RadioItems(
                id="corr_dim_type",
                options=dim_options,
                value="rischio",
                inline=True,
                className="mt-1",
            ),
        ], lg=3, xs=12),
        dbc.Col([
            _section_label("Popolazione"),
            dbc.RadioItems(
                id="corr_population",
                options=pop_options,
                value="totale",
                inline=True,
                className="mt-1",
            ),
        ], lg=1, xs=12),
        dbc.Col([
            _section_label("Anno"),
            _year_slider("corr_year"),
        ], lg=2, xs=12),
    ], className="g-3 align-items-start")),
    _graph("data_correlations", min_height="60vh"),
])

# ── Mappa tab → contenuto ─────────────────────────────────────────────────────

tab_content_map = {
    "map":          tab_map,
    "ranking":      tab_ranking,
    "evolution":    tab_evolution,
    "radar":        tab_radar,
    "heatmap":      tab_heatmap,
    "correlations": tab_correlations,
}

# ── Layout principale ─────────────────────────────────────────────────────────

data_layout = dbc.Container(
    [
        # Intestazione
        dbc.Row(
            dbc.Col([
                html.H2("Dati", className="mb-1"),
                html.Div(style={
                    "width": "40px", "height": "4px",
                    "backgroundColor": ACCENT, "marginBottom": "0.5rem",
                }),
                html.P(
                    "Esplora i risultati dell\u2019Indice attraverso diverse visualizzazioni: "
                    "mappe, classifiche, serie storiche, profili per capacità e correlazioni.",
                    className="text-muted mb-3",
                    style={"fontSize": "0.92rem"},
                ),
            ], xs=12),
        ),
        # Tab
        dbc.Tabs(
            id="data_viz_tabs",
            active_tab="map",
            class_name="d-flex justify-content-around",
            children=[
                dbc.Tab(label="Mappa",         tab_id="map"),
                dbc.Tab(label="Classifica",    tab_id="ranking"),
                dbc.Tab(label="Serie storica", tab_id="evolution"),
                dbc.Tab(label="Profilo",       tab_id="radar"),
                dbc.Tab(label="Heatmap",       tab_id="heatmap"),
                dbc.Tab(label="Correlazioni",  tab_id="correlations"),
            ],
        ),
        html.Div(id="data_viz_content", className="mt-3"),
    ],
    class_name="mt-4",
    fluid=False,
)
