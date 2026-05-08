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
    ZSCORE_TIER_COLORS,
    CAPACITY_DIMS,
    CAPACITY_ORDER,
    INDEX_LABELS,
    YEARS,
    YEAR_DEFAULT,
    BRAND_COLOR,
)
from index import app, data, geodata
from utilis import zscore_format, get_zscore_tier, get_score_change_arrow

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE


# ── Helpers ───────────────────────────────────────────────────────────────────

def _totale(year):
    """Righe dell'indice totale per un dato anno (tutti i territori)."""
    return data[
        (data["year"] == year) & (data["type"] == "totale") & (data["capacity"] == "totale")
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
    """Posizione (1 = migliore) per un qualsiasi type (aggregato, capacity == 'totale')."""
    df = data[
        (data["year"] == year) & (data["type"] == index_key) & (data["capacity"] == "totale")
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
    prevent_initial_call=True,
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
        first_year = YEARS[0]
        first_rank = _get_rank(territory, first_year)
        if first_rank is not None:
            delta = rank - first_rank          # negativo = miglioramento
            arrow = get_score_change_arrow(delta)
            if delta == 0:
                delta_children = [html.Span(className="arrow-right"), f" Stabile"]
            elif delta < 0:
                delta_children = [html.Span(className="arrow-up"), f" {abs(delta)} posizioni"]
            else:
                delta_children = [html.Span(className="arrow-down"), f" {delta} posizioni"]
        else:
            delta_children = "N/D"
    else:
        delta_children = "N/D"

    return score_str, rank_str, tier_str, delta_children


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
    # Evidenzia indice totale: linea più spessa e marker più grandi
    totale_label = INDEX_LABELS["totale"]
    for trace in fig.data:
        if trace.name == totale_label:
            trace.update(line=dict(width=3), marker=dict(size=12))
        else:
            trace.update(line=dict(width=1.5, dash="dot"), marker=dict(size=8))
    fig.update_yaxes(
        range=[20.5, 0.5],   # invertito: 1 in cima, 20 in fondo — fisso
        tickvals=[5, 10, 15, 20],
        title_text="Posizione",
    )
    fig.update_xaxes(
        range=[YEARS[0] - 0.3, YEARS[-1] + 0.3],
        tickvals=list(range(YEARS[0], YEARS[-1] + 1)),
        ticktext=[str(y) for y in range(YEARS[0], YEARS[-1] + 1)],
        title_text="Anno",
    )
    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        margin={"t": 40, "b": 30, "l": 10, "r": 10},
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Anno: %{x}<br>Posizione: %{y} / 20<extra></extra>"
    )
    return fig


# ── Profilo per capacità (lollipop) ───────────────────────────────────────────

_N_REGIONS = 20
_MEDIAN    = (_N_REGIONS + 1) / 2  # 10.5

# ── [RADAR commentato] ────────────────────────────────────────────────────────
# @app.callback(
#     Output("scorecard_radar", "figure"),
#     Input("scorecard_territory", "value"),
#     Input("scorecard_year", "value"),
# )
# def update_scorecard_radar(territory, year):
#     cap_keys   = list(CAPACITY_DIMS.keys())
#     cap_labels = [f.replace(' ', '<br>') for f in CAPACITY_DIMS.values()]
#     ranks = [_cap_rank(territory, year, k) for k in cap_keys]
#     plot_vals  = [(_N_REGIONS + 1 - r) if r is not None else 0 for r in ranks]
#     hover_ranks = [str(r) if r is not None else "N/D" for r in ranks]
#     vals_closed   = plot_vals + [plot_vals[0]]
#     labels_closed = cap_labels + [cap_labels[0]]
#     hover_closed  = hover_ranks + [hover_ranks[0]]
#     fig = go.Figure()
#     fig.add_trace(
#         go.Scatterpolar(
#             r=vals_closed,
#             theta=labels_closed,
#             fill="toself",
#             name=str(year),
#             line_color=SEQUENCE_COLOR[0],
#             fillcolor=SEQUENCE_COLOR[0],
#             opacity=0.55,
#             customdata=hover_closed,
#             hovertemplate="<b>%{theta}</b><br>Posizione: %{customdata}<extra></extra>",
#         )
#     )
#     fig.update_layout(
#         polar=dict(
#             radialaxis=dict(
#                 visible=True,
#                 range=[0, _N_REGIONS],
#                 tickvals=list(range(0, _N_REGIONS + 1, 5)),
#                 ticktext=[str(_N_REGIONS + 1 - v) if v > 0 else str(_N_REGIONS)
#                           for v in range(0, _N_REGIONS + 1, 5)],
#             ),
#             angularaxis=dict(tickpadding=15),
#         ),
#         showlegend=False,
#         margin={"r": 40, "t": 20, "l": 40, "b": 20},
#     )
#     return fig
# ─────────────────────────────────────────────────────────────────────────────

@app.callback(
    Output("scorecard_lollipop", "figure"),
    Input("scorecard_territory", "value"),
    Input("scorecard_year", "value"),
)
def update_scorecard_lollipop(territory, year):
    # Ordine da CAPACITY_ORDER (configurabile in configuration.py)
    cap_keys   = CAPACITY_ORDER
    cap_labels = [CAPACITY_DIMS[k] for k in cap_keys]

    ranks   = [_cap_rank(territory, year, k) for k in cap_keys]
    zscores = [_cap_avg(territory, year, k)  for k in cap_keys]

    df = pd.DataFrame({
        "capacity": cap_labels,
        "rank":     ranks,
        "zscore":   zscores,
        "key":      cap_keys,
    })
    # Ordine y-axis: CAPACITY_ORDER dal basso verso l'alto
    y_order = list(reversed(cap_labels))

    df["tier"] = pd.cut(
        df["zscore"], bins=ZSCORE_BINS, labels=ZSCORE_LABELS, right=False,
    ).astype(str)
    df["color"]    = df["tier"].map(ZSCORE_TIER_COLORS)
    df["rank_int"] = df["rank"].apply(
        lambda r: int(r) if r is not None and not pd.isna(r) else None
    )

    fig = go.Figure()

    # Stems dalla mediana al valore (layer below → coperte dai cerchi)
    for _, row in df.iterrows():
        if row["rank_int"] is not None:
            fig.add_shape(
                type="line",
                x0=10, x1=row["rank_int"],
                y0=row["capacity"], y1=row["capacity"],
                line=dict(color="#cccccc", width=2),
                layer="below",
            )

    # Cerchi con rank scritto dentro
    fig.add_trace(
        go.Scatter(
            x=df["rank_int"],
            y=df["capacity"],
            mode="markers+text",
            marker=dict(
                size=30,
                color=df["color"],
                line=dict(width=1.5, color="white"),
            ),
            text=df["rank_int"].apply(lambda r: str(r) if r is not None else ""),
            textfont=dict(color="white", size=11),
            textposition="middle center",
            hovertemplate="<b>%{y}</b><br>Posizione: %{x} / 20<extra></extra>",
        )
    )

    # Linea di riferimento posizione 10
    fig.add_vline(x=10, line_dash="dot", line_color="#aaaaaa", line_width=1)

    fig.update_layout(
        xaxis=dict(
            range=[20.5, -0.5],   # centro esatto a 10, padding simmetrico
            tickvals=[5, 10, 15, 20],
            title="Posizione",
            zeroline=False,
        ),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=y_order,
            automargin=True,
        ),
        showlegend=False,
        margin={"t": 10, "b": 40, "l": 10, "r": 25},
        height=300,
    )
    return fig


# ── Barre z-score per capacità ────────────────────────────────────────────────

@app.callback(
    Output("scorecard_dim_table", "figure"),
    Input("scorecard_territory", "value"),
    Input("scorecard_year", "value"),
)
def update_scorecard_dim_table(territory, year):
    # Ordine da CAPACITY_ORDER (configurabile in configuration.py)
    cap_keys   = CAPACITY_ORDER
    cap_labels = [CAPACITY_DIMS[k] for k in cap_keys]

    values = [_cap_avg(territory, year, k) for k in cap_keys]

    rows = [
        {"capacity": label, "zscore": v if v is not None else float("nan")}
        for label, v in zip(cap_labels, values)
    ]
    df = pd.DataFrame(rows)
    # Ordine y-axis coerente con lollipop: CAPACITY_ORDER dal basso verso l'alto
    y_order = list(reversed(cap_labels))

    df["tier"] = pd.cut(
        df["zscore"],
        bins=ZSCORE_BINS,
        labels=ZSCORE_LABELS,
        right=False,
    ).astype(str)

    fig = px.bar(
        df,
        x="zscore",
        y="capacity",
        orientation="h",
        color="tier",
        color_discrete_map=ZSCORE_TIER_COLORS,
        category_orders={"tier": ZSCORE_LABELS},
        labels={"zscore": "Punteggio", "capacity": "", "tier": ""},
        custom_data=["tier"],
    )
    fig.add_vline(x=0, line_dash="dot", line_color="#aaaaaa", line_width=1)
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Punteggio: %{x:.2f}<br>%{customdata[0]}<extra></extra>"
    )
    fig.update_layout(
        showlegend=False,
        xaxis=dict(title="Punteggio", zeroline=False),
        yaxis=dict(
            title="",
            categoryorder="array",
            categoryarray=y_order,
            automargin=True,
        ),
        margin={"t": 10, "b": 40, "l": 10, "r": 15},
        height=300,
    )
    return fig


# ── Scatter Servizi vs Fattori di rischio ────────────────────────────────────

@app.callback(
    Output("scorecard_scatter", "figure"),
    Input("scorecard_territory", "value"),
)
def update_scorecard_scatter(territory):
    year = YEAR_DEFAULT

    def _ranks(index_key):
        df = data[
            (data["year"] == year) & (data["type"] == index_key) & (data["capacity"] == "totale")
        ][["territory", "score"]].dropna(subset=["score"])
        df = df.sort_values("score", ascending=False).reset_index(drop=True)
        df["rank"] = range(1, len(df) + 1)
        return df[["territory", "rank"]].rename(columns={"rank": f"rank_{index_key}"})

    df_servizi = _ranks("servizi")
    df_rischio = _ranks("rischio")
    df = df_servizi.merge(df_rischio, on="territory")
    if df.empty:
        return go.Figure()

    df["is_selected"] = df["territory"] == territory
    df = df.sort_values("is_selected")   # regione selezionata disegnata per ultima (sopra)

    n = len(df)
    median = (n + 1) / 2

    fig = go.Figure()

    # Altre regioni
    other = df[~df["is_selected"]]
    fig.add_trace(go.Scatter(
        x=other["rank_servizi"],
        y=other["rank_rischio"],
        mode="markers+text",
        text=other["territory"],
        textposition="top center",
        textfont=dict(size=9, color="#3d4646"),
        marker=dict(color="#D0DADB", size=9, line=dict(color="#94A4A4", width=1)),
        hovertemplate="<b>%{text}</b><br>Servizi: %{x} / 20<br>Fattori di rischio: %{y} / 20<extra></extra>",
        showlegend=False,
    ))

    # Regione selezionata
    sel = df[df["is_selected"]]
    if not sel.empty:
        fig.add_trace(go.Scatter(
            x=sel["rank_servizi"],
            y=sel["rank_rischio"],
            mode="markers+text",
            text=sel["territory"],
            textposition="top center",
            textfont=dict(size=11, color=BRAND_COLOR),
            marker=dict(color=BRAND_COLOR, size=14, line=dict(color="white", width=1.5)),
            hovertemplate="<b>%{text}</b><br>Servizi: %{x} / 20<br>Fattori di rischio: %{y} / 20<extra></extra>",
            showlegend=False,
        ))

    fig.add_vline(x=10, line_dash="dot", line_color="#aaaaaa", line_width=1)
    fig.add_hline(y=10, line_dash="dot", line_color="#aaaaaa", line_width=1)

    fig.update_xaxes(
        title="Servizi",
        range=[20.5, -0.5],   # centro esatto a 10, padding simmetrico
        tickvals=[5, 10, 15, 20],
        autorange=False,
        automargin=True,
    )
    fig.update_yaxes(
        title="Fattori di rischio",
        range=[20.5, -0.5],   # centro esatto a 10, padding simmetrico
        tickvals=[5, 10, 15, 20],
        autorange=False,
        automargin=True,
    )
    fig.update_layout(
        margin={"t": 30, "b": 50, "l": 10, "r": 30},
        height=420,
    )
    return fig