# render_data.py — Cesvi Indice Infanzia

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash import Input, Output, html
from dash.exceptions import PreventUpdate
from dash_bootstrap_templates import load_figure_template

from configuration import (
    FIGURE_TEMPLATE,
    GEO_KEY,
    SEQUENCE_COLOR,
    ZSCORE_BINS,
    ZSCORE_LABELS,
    ZSCORE_TIER_COLORS,
    DIVERGING_COLORS,
    CAPACITY_DIMS,
    CAPACITY_ORDER,
    INDEX_LABELS,
    YEAR_DEFAULT,
)
from index import app, data, geodata
from layout.layout_data import tab_content_map

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE


# ── Helpers ───────────────────────────────────────────────────────────────────

def _label(key):
    if key in INDEX_LABELS:
        return INDEX_LABELS[key]
    if key in CAPACITY_DIMS:
        return CAPACITY_DIMS[key]
    return key


def _pop_label(pop):
    return {"adulti": "Adulti", "bambini": "Bambini", "totale": "Totale"}.get(pop, pop)


def _resolve_selector(index_type, capacity, population):
    """Traduce selezione utente in (type_key, cap_key, pop_key) per il filtro CSV.

    Logica:
      - index_type == "totale"  → type=totale, cap=totale, pop=totale (aggregato)
      - index_type == "rischio" o "servizi" e capacity == None → aggregato di quella dim
      - index_type == "rischio" o "servizi" e capacity != None → dettaglio capacità
    """
    if index_type == "totale":
        return "totale", "totale", "totale"
    type_key = index_type or "totale"
    cap_key  = capacity if capacity else "totale"
    pop_key  = population if population else "totale"
    return type_key, cap_key, pop_key


def _fetch(year, type_key, cap_key, pop_key):
    return data[
        (data["year"] == year)
        & (data["type"] == type_key)
        & (data["capacity"] == cap_key)
        & (data["population"] == pop_key)
    ][["territory", "code", "score"]].copy()


def _feat_label(index_type, capacity, population):
    if index_type == "totale":
        return INDEX_LABELS["totale"]
    lbl = INDEX_LABELS.get(index_type, index_type)
    if capacity:
        lbl += f" — {_label(capacity)}"
        if population and population != "totale":
            lbl += f" ({_pop_label(population)})"
    return lbl


def _no_data(msg="Nessun dato disponibile"):
    fig = go.Figure()
    fig.add_annotation(
        text=msg, xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False, font=dict(size=14),
    )
    return fig


def _map_geo():
    return dict(
        dragmode=False,
        margin={"r": 10, "t": 10, "l": 10, "b": 10},
        geo=dict(
            projection_type="natural earth", projection_scale=15.4,
            showland=False, showocean=False, showlakes=False,
            showrivers=False, visible=False,
            center=dict(lat=41.9, lon=12.5),
        ),
    )


# ── Toggle capacità/popolazione: abilitati solo se indice != totale ───────────

def _cap_disabled_props(index_type, default_cap):
    """Ritorna (disabled, value) per il dropdown Capacità."""
    if index_type == "totale":
        return True, None
    return False, default_cap


for _prefix, _default in [("map", CAPACITY_ORDER[0]),
                           ("ranking", CAPACITY_ORDER[0]),
                           ("evo", CAPACITY_ORDER[0])]:
    @app.callback(
        Output(f"{_prefix}_capacity", "disabled"),
        Output(f"{_prefix}_capacity", "value"),
        Input(f"{_prefix}_index_type", "value"),
    )
    def _toggle_capacity(index_type, default=_default):
        disabled, value = _cap_disabled_props(index_type, default)
        return disabled, value


# ── Tab content ───────────────────────────────────────────────────────────────

@app.callback(
    Output("data_viz_content", "children"),
    Input("data_viz_tabs", "active_tab"),
)
def render_tab(tab):
    return tab_content_map.get(tab, html.P("Tab non disponibile."))


# ── Mappa ─────────────────────────────────────────────────────────────────────

@app.callback(
    Output("data_map", "figure"),
    Input("map_index_type", "value"),
    Input("map_capacity",   "value"),
    Input("map_population", "value"),
    Input("map_year",       "value"),
)
def display_map(index_type, capacity, population, year):
    yr = year or YEAR_DEFAULT
    type_key, cap_key, pop_key = _resolve_selector(index_type, capacity, population)
    feat_label = _feat_label(index_type, capacity, population)

    df = _fetch(yr, type_key, cap_key, pop_key)
    if df.empty or df["score"].isna().all():
        return _no_data(f"Nessun dato per '{feat_label}' — {yr}")

    df["tier"] = pd.cut(
        df["score"], bins=ZSCORE_BINS, labels=ZSCORE_LABELS, right=False
    ).cat.remove_unused_categories()

    fig = px.choropleth(
        df,
        locations="code", geojson=geodata, featureidkey=GEO_KEY,
        color="tier", color_discrete_map=ZSCORE_TIER_COLORS,
        category_orders={"tier": ZSCORE_LABELS},
        custom_data=["territory", "score", "tier"],
        labels={"tier": "Fascia"},
    )
    fig.update_layout(**_map_geo(), legend=dict(title_text="Fascia"))
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            f"{feat_label}: " + "%{customdata[1]:.3f}<br>"
            "Fascia: %{customdata[2]}<br><extra></extra>"
        )
    )
    return fig


# ── Classifica ────────────────────────────────────────────────────────────────

@app.callback(
    Output("data_ranking", "figure"),
    Input("ranking_index_type", "value"),
    Input("ranking_capacity",   "value"),
    Input("ranking_population", "value"),
    Input("ranking_year",       "value"),
)
def display_ranking(index_type, capacity, population, year):
    yr = year or YEAR_DEFAULT
    type_key, cap_key, pop_key = _resolve_selector(index_type, capacity, population)
    feat_label = _feat_label(index_type, capacity, population)

    df = _fetch(yr, type_key, cap_key, pop_key)
    if df.empty or df["score"].isna().all():
        return _no_data(f"Nessun dato per '{feat_label}' — {yr}")

    df = df.dropna(subset=["score"]).sort_values("score", ascending=True)
    df["rank"] = range(len(df), 0, -1)

    fig = px.bar(
        df,
        x="score", y="territory", orientation="h",
        color="score",
        color_continuous_scale=DIVERGING_COLORS,
        color_continuous_midpoint=0,
        labels={"score": feat_label, "territory": "Regione"},
        text=df["score"].map(lambda v: f"{v:+.3f}"),
        custom_data=["territory", "rank"],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False, coloraxis_showscale=False,
        yaxis_title=None, xaxis_title=feat_label,
        margin=dict(l=10, r=30),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            f"{feat_label}: " + "%{x:.3f}<br>"
            "Rank: %{customdata[1]}<br><extra></extra>"
        )
    )
    fig.add_vline(x=0, line_dash="dash", line_color="gray", line_width=1)
    return fig


# ── Serie storica ─────────────────────────────────────────────────────────────

@app.callback(
    Output("data_evolution", "figure"),
    Input("evo_territories", "value"),
    Input("evo_index_type",  "value"),
    Input("evo_capacity",    "value"),
    Input("evo_population",  "value"),
)
def display_evolution(territories, index_type, capacity, population):
    if not territories:
        raise PreventUpdate

    type_key, cap_key, pop_key = _resolve_selector(index_type, capacity, population)
    feat_label = _feat_label(index_type, capacity, population)

    df = data[
        (data["territory"].isin(territories))
        & (data["type"] == type_key)
        & (data["capacity"] == cap_key)
        & (data["population"] == pop_key)
    ][["territory", "year", "score"]].copy()

    if df.empty:
        return _no_data(f"Nessun dato per '{feat_label}'")

    fig = px.line(
        df, x="year", y="score", color="territory", markers=True,
        labels={"year": "Anno", "score": feat_label, "territory": "Regione"},
        color_discrete_sequence=SEQUENCE_COLOR,
        custom_data=["territory"],
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
    years_present = sorted(df["year"].unique())
    fig.update_layout(
        xaxis=dict(tickvals=years_present, ticktext=[str(y) for y in years_present]),
        legend=dict(title_text="Regione"),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "Anno: %{x}<br>"
            f"{feat_label}: " + "%{y:.3f}<br><extra></extra>"
        )
    )
    return fig


# ── Profilo per capacità (radar) ──────────────────────────────────────────────

@app.callback(
    Output("data_radar", "figure"),
    Input("radar_territories", "value"),
    Input("radar_dim_type",    "value"),
    Input("radar_population",  "value"),
    Input("radar_year",        "value"),
)
def display_radar(territories, dim_type, population, year):
    if not territories:
        raise PreventUpdate

    territories = territories[:3]
    yr      = year or YEAR_DEFAULT
    pop_key = population or "totale"

    if dim_type == "totale":
        # Media tra rischio e servizi per ciascuna capacità
        df = (
            data[
                (data["year"] == yr)
                & (data["capacity"].isin(CAPACITY_ORDER))
                & (data["population"] == "totale")
                & (data["type"].isin(["rischio", "servizi"]))
            ]
            .groupby(["territory", "capacity"])["score"]
            .mean()
            .reset_index()
        )
    else:
        df = data[
            (data["year"] == yr)
            & (data["type"] == dim_type)
            & (data["capacity"].isin(CAPACITY_ORDER))
            & (data["population"] == pop_key)
        ][["territory", "capacity", "score"]].copy()

    if df.empty:
        return _no_data("Nessun dato per il profilo selezionato")

    dim_labels = [CAPACITY_DIMS[k] for k in CAPACITY_ORDER]
    all_vals   = df["score"].dropna()
    r_min = min(-2.0, float(all_vals.min()) - 0.2) if not all_vals.empty else -2.0
    r_max = max(2.0,  float(all_vals.max()) + 0.2) if not all_vals.empty else  2.0

    fig = go.Figure()
    for i, territory in enumerate(territories):
        tdf = df[df["territory"] == territory].set_index("capacity")
        values = [
            float(tdf.loc[k, "score"])
            if k in tdf.index and pd.notna(tdf.loc[k, "score"])
            else 0
            for k in CAPACITY_ORDER
        ]
        values_closed = values + [values[0]]
        labels_closed = dim_labels + [dim_labels[0]]
        fig.add_trace(go.Scatterpolar(
            r=values_closed, theta=labels_closed,
            fill="toself", name=territory,
            line_color=SEQUENCE_COLOR[i % len(SEQUENCE_COLOR)],
            opacity=0.7,
        ))

    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, title="z-score", range=[r_min, r_max])),
        showlegend=True, legend=dict(title_text="Regione"),
    )
    return fig


# ── Heatmap ───────────────────────────────────────────────────────────────────

@app.callback(
    Output("data_heatmap", "figure"),
    Input("heatmap_dim_type",   "value"),
    Input("heatmap_population", "value"),
    Input("heatmap_year",       "value"),
)
def display_heatmap(dim_type, population, year):
    yr      = year or YEAR_DEFAULT
    pop_key = population or "totale"

    if dim_type == "all":
        # Colonne = i 3 indici aggregati (capacity="totale")
        frames = []
        for t in ["rischio", "servizi", "totale"]:
            tmp = data[
                (data["year"] == yr) & (data["type"] == t) & (data["capacity"] == "totale")
            ][["territory", "score"]].copy()
            tmp["col"] = _label(t)
            frames.append(tmp)
        col_order = [_label(t) for t in ["rischio", "servizi", "totale"]]
    else:
        # Colonne = le 6 capacità per la dimensione scelta
        frames = []
        for cap in CAPACITY_ORDER:
            tmp = data[
                (data["year"] == yr)
                & (data["type"] == dim_type)
                & (data["capacity"] == cap)
                & (data["population"] == pop_key)
            ][["territory", "score"]].copy()
            tmp["col"] = CAPACITY_DIMS.get(cap, cap)
            frames.append(tmp)
        col_order = [CAPACITY_DIMS[k] for k in CAPACITY_ORDER]

    if not frames:
        return _no_data()

    df_wide = pd.concat(frames).pivot_table(
        index="territory", columns="col", values="score", aggfunc="first"
    )
    col_order = [c for c in col_order if c in df_wide.columns]
    if df_wide.empty or not col_order:
        return _no_data()

    df_wide = df_wide[col_order]
    df_wide["_avg"] = df_wide.mean(axis=1)
    df_wide = df_wide.sort_values("_avg", ascending=False).drop(columns="_avg")

    z           = df_wide.values
    territories = df_wide.index.tolist()
    cols        = df_wide.columns.tolist()

    fig = go.Figure(data=go.Heatmap(
        z=z, x=cols, y=territories,
        colorscale=DIVERGING_COLORS, zmid=0,
        text=[[f"{v:.3f}" if pd.notna(v) else "N/D" for v in row] for row in z],
        texttemplate="%{text}",
        colorbar=dict(title="z-score"),
        hovertemplate="<b>%{y}</b><br>%{x}: %{z:.3f}<br><extra></extra>",
    ))
    fig.update_layout(margin=dict(l=10, r=10, t=20, b=10))
    return fig


# ── Correlazioni ──────────────────────────────────────────────────────────────

@app.callback(
    Output("data_correlations", "figure"),
    Input("corr_x",          "value"),
    Input("corr_y",          "value"),
    Input("corr_dim_type",   "value"),
    Input("corr_population", "value"),
    Input("corr_year",       "value"),
)
def display_correlations(cap_x, cap_y, dim_type, population, year):
    if not cap_x or not cap_y:
        raise PreventUpdate
    if cap_x == cap_y:
        return _no_data("Seleziona due capacità diverse")

    yr       = year or YEAR_DEFAULT
    type_key = dim_type or "rischio"
    pop_key  = population or "totale"

    def _fetch_cap(cap):
        return data[
            (data["year"] == yr)
            & (data["type"] == type_key)
            & (data["capacity"] == cap)
            & (data["population"] == pop_key)
        ][["territory", "score"]].rename(columns={"score": cap})

    df = _fetch_cap(cap_x).merge(_fetch_cap(cap_y), on="territory")
    if df.empty:
        return _no_data(f"Nessun dato per {_label(cap_x)} vs {_label(cap_y)}")

    lx, ly = _label(cap_x), _label(cap_y)
    fig = px.scatter(
        df, x=cap_x, y=cap_y, text="territory",
        labels={cap_x: lx, cap_y: ly},
        color_discrete_sequence=SEQUENCE_COLOR,
    )
    fig.update_traces(textposition="top center", marker=dict(size=8))
    fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
    fig.add_vline(x=0, line_dash="dash", line_color="gray", line_width=1)
    fig.update_layout(xaxis_title=lx, yaxis_title=ly, margin=dict(l=10, r=10))
    return fig
