# render_scorecards.py — Cesvi Indice Infanzia

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash import Input, Output, html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

from configuration import (
    FIGURE_TEMPLATE,
    GEO_KEY,
    SEQUENCE_COLOR,
    ZSCORE_BINS,
    ZSCORE_LABELS,
    CAPACITY_DIMS,
    INDEX_LABELS,
    YEARS,
    BRAND_COLOR,
)
from index import app, data, geodata
from utilis import zscore_format, get_zscore_tier

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE


# ── Helpers ───────────────────────────────────────────────────────────────────

def _totale(year):
    """Righe dell'indice totale per un dato anno (tutti i territori)."""
    return data[
        (data["year"] == year) & (data["index"] == "totale") & data["capacity"].isna()
    ][["territory", "code", "score"]].copy()


def _get_score(territory, year):
    df = _totale(year)
    row = df[df["territory"] == territory]
    if row.empty:
        return None
    v = row["score"].values[0]
    return float(v) if pd.notna(v) else None


def _get_rank(territory, year):
    """Posizione (1 = migliore z-score) del territorio nell'anno (indice totale)."""
    return _get_rank_by_index(territory, year, "totale")


def _get_rank_by_index(territory, year, index_key):
    """Posizione (1 = migliore) per un qualsiasi index_key (capacity isNaN)."""
    df = data[
        (data["year"] == year) & (data["index"] == index_key) & data["capacity"].isna()
    ][["territory", "score"]].dropna(subset=["score"])
    if df.empty:
        return None
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)
    row = df[df["territory"] == territory]
    if row.empty:
        return None
    return int(row["rank"].values[0])


def _cap_avg(territory, year, capacity):
    """Media dei sotto-indici di una capacità per territorio/anno."""
    df = data[
        (data["territory"] == territory)
        & (data["year"] == year)
        & (data["capacity"] == capacity)
    ]
    if df.empty:
        return None
    v = df["score"].mean()
    return float(v) if pd.notna(v) else None


def _cap_rank(territory, year, capacity):
    """Posizione del territorio per la capacità indicata (media sotto-indici)."""
    df = data[(data["year"] == year) & (data["capacity"] == capacity)].copy()
    if df.empty:
        return None
    agg = df.groupby("territory")["score"].mean().reset_index()
    agg = agg.dropna(subset=["score"]).sort_values("score", ascending=False).reset_index(drop=True)
    agg["rank"] = range(1, len(agg) + 1)
    row = agg[agg["territory"] == territory]
    if row.empty:
        return None
    return int(row["rank"].values[0])


# ── Navigazione da store ──────────────────────────────────────────────────────

@app.callback(
    Output("scorecard_territory", "value"),
    Input("store_territory", "data"),
)
def set_territory_from_store(stored_territory):
    if stored_territory:
        return stored_territory
    raise PreventUpdate


# ── Header ────────────────────────────────────────────────────────────────────

@app.callback(
    Output("scorecard_header", "children"),
    Input("scorecard_territory", "value"),
)
def update_scorecard_header(territory):
    return territory or "—"


# ── Score / Rank / Tier / Variazione ─────────────────────────────────────────

@app.callback(
    Output("scorecard_score", "children"),
    Output("scorecard_rank", "children"),
    Output("scorecard_tier", "children"),
    Output("scorecard_change", "children"),
    Input("scorecard_territory", "value"),
    Input("scorecard_year", "value"),
)
def update_scorecard_info(territory, year):
    score = _get_score(territory, year)
    rank  = _get_rank(territory, year)

    score_str = zscore_format(score) if score is not None else "N/D"
    tier_str  = get_zscore_tier(score) if score is not None else "N/D"
    rank_str  = f"{rank} / 20" if rank is not None else "N/D"

    prev_years = [y for y in YEARS if y < year]
    if prev_years and rank is not None:
        prev_year  = max(prev_years)
        prev_rank  = _get_rank(territory, prev_year)
        if prev_rank is not None:
            delta = rank - prev_rank          # negativo = miglioramento
            if delta < 0:
                delta_str = f"▲ {abs(delta)} posizioni (rispetto al {prev_year})"
            elif delta > 0:
                delta_str = f"▼ {delta} posizioni (rispetto al {prev_year})"
            else:
                delta_str = f"Stabile (rispetto al {prev_year})"
        else:
            delta_str = "N/D"
    else:
        delta_str = "Non disponibile"

    return score_str, rank_str, tier_str, delta_str


# ── Mappa ─────────────────────────────────────────────────────────────────────

@app.callback(
    Output("scorecard_map", "figure"),
    Input("scorecard_territory", "value"),
    Input("scorecard_year", "value"),
)
def update_scorecard_map(territory, year):
    df = _totale(year)
    df["highlight"] = df["territory"].apply(
        lambda t: "Regione selezionata" if t == territory else "Altre regioni"
    )
    fig = px.choropleth(
        df,
        locations="code",
        geojson=geodata,
        featureidkey=GEO_KEY,
        color="highlight",
        color_discrete_map={
            "Regione selezionata": BRAND_COLOR,
            "Altre regioni": "#D0DADB",
        },
        category_orders={"highlight": ["Regione selezionata", "Altre regioni"]},
        custom_data=["territory"],
    )
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><extra></extra>",
    )
    fig.update_layout(
        dragmode=False,
        showlegend=False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            fitbounds="locations", # Applica lo zoom dinamico sulla regione
            projection_type="mercator",
            showland=False,
            showocean=False,
            showlakes=False,
            showrivers=False,
            visible=False,
        ),
    )
    return fig


# ── Andamento posizione in classifica ────────────────────────────────────────

# Usa le etichette definite in configuration
_EVOLUTION_SERIES = INDEX_LABELS  # {"totale": "Indice totale", ...}

@app.callback(
    Output("scorecard_evolution", "figure"),
    Input("scorecard_territory", "value"),
)
def update_scorecard_evolution(territory):
    rows = []
    for y in YEARS:
        for idx_key, idx_label in _EVOLUTION_SERIES.items():
            rank = _get_rank_by_index(territory, y, idx_key)
            if rank is not None:
                rows.append({"year": y, "rank": rank, "serie": idx_label})
    df = pd.DataFrame(rows)

    if df.empty:
        return go.Figure()

    color_map = {
        lbl: SEQUENCE_COLOR[i]
        for i, lbl in enumerate(_EVOLUTION_SERIES.values())
    }

    fig = px.line(
        df,
        x="year",
        y="rank",
        color="serie",
        markers=True,
        labels={"year": "Anno", "rank": "Posizione", "serie": ""},
        color_discrete_map=color_map,
        category_orders={"serie": list(_EVOLUTION_SERIES.values())},
    )
    fig.update_yaxes(
        range=[20.5, 0.5],   # invertito: 1 in cima, 20 in fondo — fisso
        tickvals=list(range(1, 21)),
        title_text="Posizione",
    )
    fig.update_xaxes(
        tickvals=YEARS,
        ticktext=[str(y) for y in YEARS],
        title_text="Anno",
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Anno: %{x}<br>Posizione: %{y}<extra></extra>"
    )
    return fig


# ── Profilo per capacità (radar) ──────────────────────────────────────────────

@app.callback(
    Output("scorecard_radar", "figure"),
    Input("scorecard_territory", "value"),
    Input("scorecard_year", "value"),
)
def update_scorecard_radar(territory, year):
    cap_keys   = list(CAPACITY_DIMS.keys())
    cap_labels = list(CAPACITY_DIMS.values())

    values = [_cap_avg(territory, year, k) for k in cap_keys]
    values = [v if v is not None else 0.0 for v in values]

    # Chiudi il poligono
    vals_closed   = values + [values[0]]
    labels_closed = cap_labels + [cap_labels[0]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatterpolar(
            r=vals_closed,
            theta=labels_closed,
            fill="toself",
            name=str(year),
            line_color=SEQUENCE_COLOR[0],
            fillcolor=SEQUENCE_COLOR[0],
            opacity=0.55,
        )
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[-2.5, 2.5],
                tickformat=".1f",
            )
        ),
        showlegend=False,
        margin={"r": 40, "t": 20, "l": 40, "b": 20},
    )
    return fig


# ── Tabella ranking per capacità ──────────────────────────────────────────────

@app.callback(
    Output("scorecard_dim_table", "children"),
    Input("scorecard_territory", "value"),
    Input("scorecard_year", "value"),
)
def update_scorecard_dim_table(territory, year):
    rows = []
    for key, label in CAPACITY_DIMS.items():
        rank = _cap_rank(territory, year, key)
        rows.append(
            html.Tr([
                html.Td(label),
                html.Td(str(rank) if rank is not None else "N/D", className="text-center"),
            ])
        )
    table = dbc.Table(
        [
            html.Thead(html.Tr([
                html.Th("Capacità"),
                html.Th(f"Posizione {year}", className="text-center"),
            ])),
            html.Tbody(rows),
        ],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        size="sm",
    )
    return table