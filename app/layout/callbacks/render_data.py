# render_data.py — Cesvi Indice Infanzia

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from dash import Input, Output
from dash_bootstrap_templates import load_figure_template

from configuration import (
    FIGURE_TEMPLATE,
    GEO_KEY,
    SEQUENCE_COLOR,
    ZSCORE_BINS,
    ZSCORE_LABELS,
    ZSCORE_TIER_COLORS,
    DIVERGING_COLORS,
    INDICATOR_LABELS,
    CAPACITY_DIMS,
    INDEX_KEY,
)
from index import app, data, geodata

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE


def _get(year, indicator):
    """Ritorna territory, code, value, rank per un dato year/indicator."""
    return (
        data[(data["year"] == year) & (data["indicator"] == indicator)]
        [["territory", "code", "value", "rank"]]
        .copy()
    )


def _get_wide(year, indicators):
    """Ritorna wide DataFrame (territory, code, ind1, ind2, …) per un dato year."""
    df = data[(data["year"] == year) & (data["indicator"].isin(indicators))]
    return (
        df.pivot_table(
            index=["territory", "code"],
            columns="indicator",
            values="value",
            aggfunc="first",
        )
        .reset_index()
    )


def _label(indicator):
    return INDICATOR_LABELS.get(indicator, indicator)


def _no_data(indicator, year):
    fig = go.Figure()
    fig.add_annotation(
        text=f"Dati non disponibili per '{_label(indicator)}' nell'anno {year}",
        xref="paper", yref="paper", x=0.5, y=0.5,
        showarrow=False, font=dict(size=14),
    )
    return fig


# ── Mappa coropletica ─────────────────────────────────────────────────────────

@app.callback(
    Output("choropleth_map", "figure"),
    Input("map_feature", "value"),
    Input("map_year", "value"),
)
def display_map(feature, year):
    df = _get(year, feature)
    if df.empty or df["value"].isna().all():
        return _no_data(feature, year)

    df["tier"] = pd.cut(
        df["value"],
        bins=ZSCORE_BINS,
        labels=ZSCORE_LABELS,
        right=False,
    ).cat.remove_unused_categories()

    fig = px.choropleth(
        df,
        locations="code",
        geojson=geodata,
        featureidkey=GEO_KEY,
        color="tier",
        color_discrete_map=ZSCORE_TIER_COLORS,
        category_orders={"tier": ZSCORE_LABELS},
        custom_data=["territory", "value", "tier"],
        labels={"tier": "Fascia"},
    )
    fig.update_layout(
        dragmode=False,
        legend=dict(title_text="Fascia"),
        margin={"r": 10, "t": 10, "l": 10, "b": 10},
        geo=dict(
            projection_type="natural earth",
            projection_scale=15.4,
            showland=False, showocean=False, showlakes=False,
            showrivers=False, visible=False,
            center=dict(lat=41.9, lon=12.5),
        ),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br><br>"
            + f"{_label(feature)}: " + "%{customdata[1]:.2f}<br>"
            + "Fascia: %{customdata[2]}<br>"
            + "<extra></extra>"
        )
    )
    return fig


# ── Classifica ────────────────────────────────────────────────────────────────

@app.callback(
    Output("ranking_chart", "figure"),
    Input("ranking_feature", "value"),
    Input("ranking_year", "value"),
)
def display_ranking(feature, year):
    df = _get(year, feature)
    if df.empty or df["value"].isna().all():
        return _no_data(feature, year)

    df = df.dropna(subset=["value"]).sort_values("value", ascending=True)
    feat_label = _label(feature)

    fig = px.bar(
        df,
        x="value",
        y="territory",
        orientation="h",
        color="value",
        color_continuous_scale=DIVERGING_COLORS,
        color_continuous_midpoint=0,
        labels={"value": feat_label, "territory": "Regione"},
        title=f"{feat_label} — {year}",
        text=df["value"].map(lambda v: f"{v:+.2f}"),
        custom_data=["territory", "rank"],
    )
    fig.update_traces(textposition="outside")
    fig.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
        yaxis_title=None,
        xaxis_title=feat_label,
        margin=dict(l=10, r=10),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            + f"{feat_label}: " + "%{x:.2f}<br>"
            + "Rank: %{customdata[1]}<br>"
            + "<extra></extra>"
        )
    )
    fig.add_vline(x=0, line_dash="dash", line_color="gray", line_width=1)
    return fig


# ── Serie storica ─────────────────────────────────────────────────────────────

@app.callback(
    Output("evolution_chart", "figure"),
    Input("evolution_territories", "value"),
    Input("evolution_feature", "value"),
)
def display_evolution(territories, feature):
    if not territories:
        return go.Figure()

    df = data[
        (data["territory"].isin(territories)) & (data["indicator"] == feature)
    ][["territory", "year", "value", "rank"]].copy()

    feat_label = _label(feature)

    fig = px.line(
        df,
        x="year",
        y="value",
        color="territory",
        markers=True,
        labels={"year": "Anno", "value": feat_label, "territory": "Regione"},
        title=f"{feat_label} — serie storica",
        color_discrete_sequence=SEQUENCE_COLOR,
        custom_data=["territory", "rank"],
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
    fig.update_layout(
        xaxis=dict(
            tickvals=sorted(df["year"].unique()),
            ticktext=[str(y) for y in sorted(df["year"].unique())],
        ),
        legend=dict(title_text="Regione"),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            + "Anno: %{x}<br>"
            + f"{feat_label}: " + "%{y:.2f}<br>"
            + "Rank: %{customdata[1]}<br>"
            + "<extra></extra>"
        )
    )
    return fig


# ── Radar (profilo dimensionale) ──────────────────────────────────────────────

@app.callback(
    Output("radar_chart", "figure"),
    Input("radar_territories", "value"),
    Input("radar_year", "value"),
)
def display_radar(territories, year):
    if not territories:
        return go.Figure()

    territories = territories[:3]
    dim_keys   = list(CAPACITY_DIMS.keys())
    dim_labels = list(CAPACITY_DIMS.values())

    df = data[
        (data["year"] == year)
        & (data["indicator"].isin(dim_keys))
        & (data["territory"].isin(territories))
    ]
    df_wide = df.pivot_table(
        index="territory", columns="indicator", values="value", aggfunc="first"
    ).reset_index()

    all_vals = df["value"].dropna()
    r_min = min(-2.0, float(all_vals.min()) - 0.2) if not all_vals.empty else -2.0
    r_max = max(2.0,  float(all_vals.max()) + 0.2) if not all_vals.empty else  2.0

    fig = go.Figure()
    for i, territory in enumerate(territories):
        row = df_wide[df_wide["territory"] == territory]
        if row.empty:
            continue
        values = [row[k].values[0] if k in row.columns else float("nan") for k in dim_keys]
        values = [v if pd.notna(v) else 0 for v in values]
        values_closed = values + [values[0]]
        labels_closed = dim_labels + [dim_labels[0]]
        fig.add_trace(
            go.Scatterpolar(
                r=values_closed,
                theta=labels_closed,
                fill="toself",
                name=territory,
                line_color=SEQUENCE_COLOR[i % len(SEQUENCE_COLOR)],
                opacity=0.7,
            )
        )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, title="z-score", range=[r_min, r_max])
        ),
        title=f"Profilo dimensionale — {year}",
        showlegend=True,
        legend=dict(title_text="Regione"),
    )
    return fig


# ── Heatmap ───────────────────────────────────────────────────────────────────

@app.callback(
    Output("heatmap_chart", "figure"),
    Input("heatmap_year", "value"),
)
def display_heatmap(year):
    all_inds = [INDEX_KEY] + list(CAPACITY_DIMS.keys())
    df_wide = _get_wide(year, all_inds)

    if INDEX_KEY in df_wide.columns:
        df_wide = df_wide.sort_values(INDEX_KEY, ascending=False)

    feats_present = [f for f in all_inds if f in df_wide.columns]
    feat_labels   = [_label(f) for f in feats_present]
    z_values    = df_wide[feats_present].values
    territories = df_wide["territory"].tolist()

    fig = go.Figure(
        data=go.Heatmap(
            z=z_values,
            x=feat_labels,
            y=territories,
            colorscale=DIVERGING_COLORS,
            zmid=0,
            text=[[f"{v:.2f}" if pd.notna(v) else "N/D" for v in row] for row in z_values],
            texttemplate="%{text}",
            colorbar=dict(title="z-score"),
            hovertemplate=(
                "<b>%{y}</b><br>"
                + "%{x}: %{z:.2f}<br>"
                + "<extra></extra>"
            ),
        )
    )
    fig.update_layout(
        title=f"Heatmap delle componenti — {year}",
        xaxis_title=None,
        yaxis_title=None,
        margin=dict(l=20, r=20),
        yaxis=dict(autorange="reversed"),
    )
    return fig


# ── Correlazioni ──────────────────────────────────────────────────────────────

@app.callback(
    Output("corr_chart", "figure"),
    Input("corr_x", "value"),
    Input("corr_y", "value"),
    Input("corr_year", "value"),
)
def display_correlations(x_ind, y_ind, year):
    if not x_ind or not y_ind or x_ind == "_sep" or y_ind == "_sep":
        return go.Figure()

    df = _get_wide(year, [x_ind, y_ind])
    if df.empty or x_ind not in df.columns or y_ind not in df.columns:
        return _no_data(x_ind, year)

    df = df.dropna(subset=[x_ind, y_ind])
    x_label = _label(x_ind)
    y_label = _label(y_ind)

    fig = px.scatter(
        df,
        x=x_ind,
        y=y_ind,
        text="territory",
        labels={x_ind: x_label, y_ind: y_label},
        title=f"{x_label} vs {y_label} — {year}",
        color_discrete_sequence=SEQUENCE_COLOR,
    )
    fig.update_traces(
        textposition="top center",
        marker=dict(size=10),
        hovertemplate=(
            "<b>%{text}</b><br>"
            + f"{x_label}: " + "%{x:.2f}<br>"
            + f"{y_label}: " + "%{y:.2f}<br>"
            + "<extra></extra>"
        ),
    )
    fig.add_vline(x=0, line_dash="dash", line_color="gray", line_width=1)
    fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
    return fig

