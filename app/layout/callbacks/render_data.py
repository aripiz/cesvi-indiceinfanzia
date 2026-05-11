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
    YEARS,
    YEAR_DEFAULT,
    BRAND_COLOR,
)
from index import app, data, geodata
from layout.layout_data import tab_content_map

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

_N_REGIONS  = 20


# ── Helpers ───────────────────────────────────────────────────────────────────

def _label(key):
    if key in INDEX_LABELS:
        return INDEX_LABELS[key]
    if key in CAPACITY_DIMS:
        return CAPACITY_DIMS[key]
    return key


def _parse_indicatore(value):
    """Ritorna (type_key, cap_key, pop_key) dal dropdown 'type||capacity||population'."""
    if not value or str(value).startswith("_"):
        return "totale", "totale", "totale"
    parts = str(value).split("||")
    type_key = parts[0] if len(parts) > 0 else "totale"
    cap_key  = parts[1] if len(parts) > 1 else "totale"
    pop_key  = parts[2] if len(parts) > 2 else "totale"
    return type_key, cap_key, pop_key


def _resolve(indicatore):
    """Ritorna (type_key, cap_key, pop_key) dall'indicatore."""
    return _parse_indicatore(indicatore)


_POP_LABELS_ALL = {"adulti": "Adulti", "bambini": "Bambini", "totale": "Totale"}
_TYPE_LABELS     = {"rischio": "Fattori di rischio", "servizi": "Servizi"}

def _indicatore_label(value):
    """Etichetta leggibile coerente col dropdown: Sezione - Sottovoce - Popolazione."""
    if not value or str(value).startswith("_"):
        return "Indici aggregati - Totale"
    type_key, cap_key, pop_key = _parse_indicatore(value)
    if type_key == "totale":
        return "Indici aggregati - Totale"
    type_label = _TYPE_LABELS.get(type_key, type_key)
    if cap_key == "totale":
        # Indice aggregato
        base = f"Indici aggregati - {type_label}"
        if pop_key != "totale":
            base += f" - {_POP_LABELS_ALL.get(pop_key, pop_key)}"
        return base
    # Capacità specifica
    cap_label = CAPACITY_DIMS.get(cap_key, cap_key)
    base = f"Capacità - {type_label} - {cap_label}"
    if pop_key != "totale":
        base += f" - {_POP_LABELS_ALL.get(pop_key, pop_key)}"
    else:
        base += " - Totale"
    return base


def _fetch(year, type_key, cap_key, pop_key):
    return data[
        (data["year"] == year)
        & (data["type"] == type_key)
        & (data["capacity"] == cap_key)
        & (data["population"] == pop_key)
    ][["territory", "code", "score"]].copy()


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


def _compute_ranks(year, type_key, cap_key, pop_key):
    """DataFrame con territory e rank (1=migliore)."""
    df = data[
        (data["year"] == year)
        & (data["type"] == type_key)
        & (data["capacity"] == cap_key)
        & (data["population"] == pop_key)
    ][["territory", "score"]].dropna(subset=["score"])
    if df.empty:
        return pd.DataFrame(columns=["territory", "rank"])
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)
    return df[["territory", "rank"]]


def _cap_avg_for_territory(territory, year, cap_key, type_key="totale", pop_key="totale"):
    """Media z-score per una capacità di un territorio (con filtro opzionale type e pop)."""
    mask = (
        (data["territory"] == territory)
        & (data["year"] == year)
        & (data["capacity"] == cap_key)
    )
    if type_key != "totale":
        mask = mask & (data["type"] == type_key)
    if pop_key != "totale":
        mask = mask & (data["population"] == pop_key)
    df = data[mask]
    if df.empty:
        return None
    v = df["score"].mean()
    return float(v) if pd.notna(v) else None


def _cap_rank_for_territory(territory, year, cap_key, type_key="totale", pop_key="totale"):
    """Posizione del territorio per una capacità."""
    mask = (data["year"] == year) & (data["capacity"] == cap_key)
    if type_key != "totale":
        mask = mask & (data["type"] == type_key)
    if pop_key != "totale":
        mask = mask & (data["population"] == pop_key)
    df = data[mask].copy()
    if df.empty:
        return None
    agg = df.groupby("territory")["score"].mean().reset_index()
    agg = agg.dropna(subset=["score"]).sort_values("score", ascending=False).reset_index(drop=True)
    agg["rank"] = range(1, len(agg) + 1)
    row = agg[agg["territory"] == territory]
    if row.empty:
        return None
    return int(row["rank"].values[0])


# ── Tab content router ────────────────────────────────────────────────────────

@app.callback(
    Output("data_viz_content", "children"),
    Input("data_viz_tabs", "active_tab"),
)
def render_tab(tab):
    return tab_content_map.get(tab, html.P("Tab non disponibile."))


# ── Mappa ─────────────────────────────────────────────────────────────────────

@app.callback(
    Output("data_map", "figure"),
    Input("map_indicatore", "value"),
    Input("map_year",       "value"),
)
def display_map(indicatore, year):
    yr = year or YEAR_DEFAULT
    type_key, cap_key, pop_key = _resolve(indicatore)
    feat_label = _indicatore_label(indicatore)

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


# ── Graduatoria ───────────────────────────────────────────────────────────────

@app.callback(
    Output("data_ranking", "figure"),
    Input("ranking_indicatore", "value"),
    Input("ranking_year",       "value"),
)
def display_ranking(indicatore, year):
    yr = year or YEAR_DEFAULT
    type_key, cap_key, pop_key = _resolve(indicatore)
    feat_label = _indicatore_label(indicatore)

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
        labels={"score": feat_label, "territory": ""},
        text=df["score"].map(lambda v: f"{v:+.2f}"),
        custom_data=["territory", "rank"],
    )
    fig.update_traces(
        textposition="outside",
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            f"{feat_label}: " + "%{x:+.3f}<br>"
            "Posizione: %{customdata[1]} / 20<br><extra></extra>"
        ),
    )
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis_title=None,
        xaxis_title=feat_label,
        margin=dict(l=10, r=60, t=10, b=30),
    )
    fig.add_vline(x=0, line_dash="dash", line_color="#aaaaaa", line_width=1)
    return fig


# ── Serie storica (posizione/rank) ────────────────────────────────────────────

@app.callback(
    Output("data_evolution", "figure"),
    Input("evo_territories", "value"),
    Input("evo_indicatore",  "value"),
)
def display_evolution(territories, indicatore):
    if not territories:
        raise PreventUpdate

    type_key, cap_key, pop_key = _resolve(indicatore)

    rows = []
    for yr in YEARS:
        df_yr = data[
            (data["year"] == yr)
            & (data["type"] == type_key)
            & (data["capacity"] == cap_key)
            & (data["population"] == pop_key)
        ][["territory", "score"]].dropna(subset=["score"])
        if df_yr.empty:
            continue
        df_yr = df_yr.sort_values("score", ascending=False).reset_index(drop=True)
        df_yr["rank"] = range(1, len(df_yr) + 1)
        df_yr["year"] = yr
        rows.append(df_yr)

    if not rows:
        return _no_data(f"Nessun dato per '{_indicatore_label(indicatore)}'")

    df_all = pd.concat(rows)
    df_sel = df_all[df_all["territory"].isin(territories)].copy()

    if df_sel.empty:
        return _no_data("Nessun dato per le regioni selezionate")

    years_present = sorted(df_sel["year"].unique())

    fig = px.line(
        df_sel,
        x="year", y="rank", color="territory", markers=True,
        labels={"year": "Anno", "rank": "Posizione", "territory": "Regione"},
        color_discrete_sequence=SEQUENCE_COLOR,
    )
    fig.update_yaxes(
        range=[_N_REGIONS + 0.5, 0.5],
        tickvals=[1, 5, 10, 15, 20],
        title_text="Posizione",
    )
    fig.update_xaxes(
        tickvals=years_present,
        ticktext=[str(y) for y in years_present],
        title_text="Anno",
    )
    fig.update_layout(
        legend=dict(
            title_text="Regione", orientation="h",
            yanchor="bottom", y=1.02, xanchor="left", x=0,
        ),
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Anno: %{x}<br>Posizione: %{y} / 20<extra></extra>"
    )
    return fig


# ── Profilo per capacità: lollipop ────────────────────────────────────────────

@app.callback(
    Output("data_lollipop", "figure"),
    Input("profilo_territory",  "value"),
    Input("profilo_dim_type",   "value"),
    Input("profilo_year",       "value"),
)
def display_profilo_lollipop(territory, dim_type, year):
    if not territory:
        raise PreventUpdate
    yr       = year or YEAR_DEFAULT
    type_key = dim_type or "rischio"
    pop_key  = "totale"

    cap_keys   = CAPACITY_ORDER
    cap_labels = [CAPACITY_DIMS[k] for k in cap_keys]
    y_order    = list(reversed(cap_labels))

    ranks   = [_cap_rank_for_territory(territory, yr, k, type_key, pop_key) for k in cap_keys]
    zscores = [_cap_avg_for_territory(territory, yr, k, type_key, pop_key)  for k in cap_keys]

    df = pd.DataFrame({"capacity": cap_labels, "rank": ranks, "zscore": zscores})
    df["tier"] = pd.cut(
        df["zscore"].fillna(0), bins=ZSCORE_BINS, labels=ZSCORE_LABELS, right=False,
    ).astype(str)
    df["color"]    = df["tier"].map(ZSCORE_TIER_COLORS)
    df["rank_int"] = df["rank"].apply(
        lambda r: int(r) if r is not None and not pd.isna(r) else None
    )

    fig = go.Figure()

    for _, row in df.iterrows():
        if row["rank_int"] is not None:
            fig.add_shape(
                type="line",
                x0=10, x1=row["rank_int"],
                y0=row["capacity"], y1=row["capacity"],
                line=dict(color="#cccccc", width=2),
                layer="below",
            )

    fig.add_trace(
        go.Scatter(
            x=df["rank_int"],
            y=df["capacity"],
            mode="markers+text",
            marker=dict(size=30, color=df["color"], line=dict(width=1.5, color="white")),
            text=df["rank_int"].apply(lambda r: str(r) if r is not None else ""),
            textfont=dict(color="white", size=11),
            textposition="middle center",
            hovertemplate="<b>%{y}</b><br>Posizione: %{x} / 20<extra></extra>",
        )
    )

    fig.add_vline(x=10, line_dash="dot", line_color="#aaaaaa", line_width=1)
    fig.update_layout(
        xaxis=dict(range=[20.5, -0.5], tickvals=[5, 10, 15, 20], title="Posizione", zeroline=False),
        yaxis=dict(title="", categoryorder="array", categoryarray=y_order, automargin=True),
        showlegend=False,
        margin={"t": 10, "b": 40, "l": 10, "r": 25},
        height=300,
    )
    return fig


# ── Profilo per capacità: dim_table ───────────────────────────────────────────

@app.callback(
    Output("data_dim_table", "figure"),
    Input("profilo_territory",  "value"),
    Input("profilo_dim_type",   "value"),
    Input("profilo_year",       "value"),
)
def display_profilo_dim_table(territory, dim_type, year):
    if not territory:
        raise PreventUpdate
    yr       = year or YEAR_DEFAULT
    type_key = dim_type or "rischio"
    pop_key  = "totale"

    cap_keys   = CAPACITY_ORDER
    cap_labels = [CAPACITY_DIMS[k] for k in cap_keys]
    y_order    = list(reversed(cap_labels))

    values = [_cap_avg_for_territory(territory, yr, k, type_key, pop_key) for k in cap_keys]
    df = pd.DataFrame([
        {"capacity": label, "zscore": v if v is not None else float("nan")}
        for label, v in zip(cap_labels, values)
    ])
    df["tier"] = pd.cut(
        df["zscore"], bins=ZSCORE_BINS, labels=ZSCORE_LABELS, right=False
    ).astype(str)

    fig = px.bar(
        df, x="zscore", y="capacity", orientation="h",
        color="tier", color_discrete_map=ZSCORE_TIER_COLORS,
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
        yaxis=dict(title="", categoryorder="array", categoryarray=y_order, automargin=True),
        margin={"t": 10, "b": 40, "l": 10, "r": 15},
        height=300,
    )
    return fig


# ── Correlazione punteggi: heatmap correlazioni tra indicatori ───────────────

@app.callback(
    Output("data_heatmap", "figure"),
    Input("heatmap_dim_type", "value"),
    Input("heatmap_year",     "value"),
)
def display_heatmap(dim_type, year):
    yr = year or YEAR_DEFAULT

    if dim_type == "indici" or not dim_type:
        cols_config = [
            ("rischio", "totale", "totale", "Fattori di rischio"),
            ("servizi",  "totale", "totale", "Servizi"),
        ]
    else:
        cols_config = [
            (dim_type, cap, None, CAPACITY_DIMS[cap])
            for cap in CAPACITY_ORDER
        ]

    all_territories = sorted(data["territory"].unique())
    scores_data = {}
    for type_k, cap_k, pop_k, col_label in cols_config:
        mask = (
            (data["year"] == yr)
            & (data["type"] == type_k)
            & (data["capacity"] == cap_k)
        )
        if pop_k is not None:
            mask = mask & (data["population"] == pop_k)
        df_col = data[mask][["territory", "score"]].dropna(subset=["score"])
        if not df_col.empty:
            scores_data[col_label] = df_col.groupby("territory")["score"].mean()
        else:
            scores_data[col_label] = pd.Series(dtype=float)

    col_labels = [c[3] for c in cols_config]
    df_wide = pd.DataFrame(scores_data, index=all_territories)[col_labels].dropna(how="all")
    present_cols = [c for c in col_labels if c in df_wide.columns and df_wide[c].notna().sum() > 1]
    if df_wide.empty or len(present_cols) < 2:
        return _no_data("Non ci sono abbastanza dati per calcolare le correlazioni")

    corr = df_wide[present_cols].corr()
    z    = corr.values
    labels = corr.columns.tolist()

    text = [[f"{v:.2f}" for v in row] for row in z]

    fig = go.Figure(data=go.Heatmap(
        z=z, x=labels, y=labels,
        colorscale="RdYlGn",
        zmin=-1, zmax=1,
        zmid=0,
        text=text,
        texttemplate="%{text}",
        colorbar=dict(
            title="r",
            tickvals=[-1, -0.5, 0, 0.5, 1],
            ticktext=["-1", "-0.5", "0", "+0.5", "+1"],
        ),
        hovertemplate="<b>%{x}</b> × <b>%{y}</b><br>r = %{z:.3f}<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=10),
        xaxis=dict(tickangle=-20, side="top"),
        yaxis=dict(autorange="reversed"),
    )
    return fig


# ── Correlazioni: scatter con evidenziazione regione ─────────────────────────

@app.callback(
    Output("data_correlations",    "figure"),
    Output("corr_spearman_badge",  "children"),
    Input("corr_x",          "value"),
    Input("corr_y",          "value"),
    Input("corr_highlight",  "value"),
    Input("corr_year",       "value"),
)
def display_correlations(ind_x, ind_y, highlight, year):
    if not ind_x or not ind_y:
        raise PreventUpdate
    if ind_x == ind_y:
        return _no_data("Seleziona due indicatori diversi per i due assi"), ""

    yr   = year or YEAR_DEFAULT
    df_x = _compute_ranks(yr, *_resolve(ind_x)).rename(columns={"rank": "rank_x"})
    df_y = _compute_ranks(yr, *_resolve(ind_y)).rename(columns={"rank": "rank_y"})
    df   = df_x.merge(df_y, on="territory")

    if df.empty:
        return _no_data("Nessun dato disponibile per il confronto selezionato"), ""

    # ── Spearman ρ ────────────────────────────────────────────────────────────
    from scipy.stats import spearmanr
    rho, pval = spearmanr(df["rank_x"], df["rank_y"])
    p_str = "< 0.001" if pval < 0.001 else f"= {pval:.3f}"
    badge = f"Coefficiente di correlazione: {rho:.2f}"

    lx = _indicatore_label(ind_x)
    ly = _indicatore_label(ind_y)
    median = 10  # centro della scala 1-20

    # Separa la regione evidenziata (come in Regioni scatter)
    df["is_selected"] = df["territory"] == highlight if highlight else False
    df = df.sort_values("is_selected")   # evidenziata disegnata per ultima (sopra)

    other = df[~df["is_selected"]]
    sel   = df[df["is_selected"]]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=other["rank_x"],
        y=other["rank_y"],
        mode="markers+text",
        text=other["territory"],
        textposition="top center",
        textfont=dict(size=9, color="#3d4646"),
        marker=dict(color="#D0DADB", size=9, line=dict(color="#94A4A4", width=1)),
        hovertemplate=(
            "<b>%{text}</b><br>"
            + lx + ": %{x} / 20<br>"
            + ly + ": %{y} / 20<extra></extra>"
        ),
        showlegend=False,
    ))

    if not sel.empty:
        fig.add_trace(go.Scatter(
            x=sel["rank_x"],
            y=sel["rank_y"],
            mode="markers+text",
            text=sel["territory"],
            textposition="top center",
            textfont=dict(size=11, color=BRAND_COLOR),
            marker=dict(color=BRAND_COLOR, size=14, line=dict(color="white", width=1.5)),
            hovertemplate=(
                "<b>%{text}</b><br>"
                + lx + ": %{x} / 20<br>"
                + ly + ": %{y} / 20<extra></extra>"
            ),
            showlegend=False,
        ))

    fig.add_vline(x=median, line_dash="dot", line_color="#aaaaaa", line_width=1)
    fig.add_hline(y=median, line_dash="dot", line_color="#aaaaaa", line_width=1)

    fig.update_xaxes(
        title=lx,
        range=[20.5, -0.5],
        tickvals=[5, 10, 15, 20],
        autorange=False,
        automargin=True,
    )
    fig.update_yaxes(
        title=ly,
        range=[20.5, -0.5],
        tickvals=[5, 10, 15, 20],
        autorange=False,
        automargin=True,
    )
    fig.update_layout(
        margin={"t": 30, "b": 50, "l": 10, "r": 30},
        height=420,
    )
    return fig, badge
