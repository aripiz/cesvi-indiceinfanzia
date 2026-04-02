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
    DIVERGING_COLORS,
    CAPACITY_DIMS,
    INDEX_KEY,
    YEARS_AVAILABLE,
)
from index import app, data, geodata
from utilis import zscore_format, get_zscore_tier

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

def _ind(territory, year, indicator):
    """Ritorna la riga long-format per territory/year/indicator."""
    return data[
        (data["territory"] == territory)
        & (data["year"] == year)
        & (data["indicator"] == indicator)
    ]

# ── Header ────────────────────────────────────────────────────────────────────

# Aggiorna il valore del dropdown quando si naviga dallo store
@app.callback(
    Output("scorecard_territory", "value"),
    Input("store_territory", "data"),
    prevent_initial_call=True,
)
def set_territory_from_store(stored_territory):
    if stored_territory:
        return stored_territory
    raise PreventUpdate


@app.callback(
    Output("scorecard_header", "children"),
    Input("scorecard_territory", "value"),
)
def update_scorecard_header(territory):
    return territory or "—"


# ── Score + Rank + Tier + Change ──────────────────────────────────────────────

@app.callback(
    Output("scorecard_score", "children"),
    Output("scorecard_rank", "children"),
    Output("scorecard_tier", "children"),
    Output("scorecard_change", "children"),
    Input("scorecard_territory", "value"),
    Input("scorecard_year", "value"),
)
def update_scorecard_info(territory, year):
    row = _ind(territory, year, INDEX_KEY)
    if row.empty:
        return "N/D", "N/D", "N/D", "N/D"

    score    = row["value"].values[0]
    rank_val = row["rank"].values[0]
    score_str = zscore_format(score) if pd.notna(score) else "N/D"
    tier_str  = get_zscore_tier(score) if pd.notna(score) else "N/D"
    rank_str  = f"{int(rank_val)} / 20" if pd.notna(rank_val) else "N/D"

    # Variazione rispetto all'anno precedente
    prev_years = [y for y in YEARS_AVAILABLE if y < year]
    if prev_years:
        prev_year = max(prev_years)
        prev_row = _ind(territory, prev_year, INDEX_KEY)
        if not prev_row.empty and pd.notna(prev_row["value"].values[0]):
            delta = score - prev_row["value"].values[0]
            delta_str = f"{delta:+.2f} (rispetto al {prev_year})"
        else:
            delta_str = "N/D"
    else:
        delta_str = "Non disponibile (primo anno)"

    return score_str, rank_str, tier_str, delta_str


# ── Mappa regione ─────────────────────────────────────────────────────────────

@app.callback(
    Output("scorecard_map", "figure"),
    Input("scorecard_territory", "value"),
    Input("scorecard_year", "value"),
)
def update_scorecard_map(territory, year):
    df = data[(data["year"] == year) & (data["indicator"] == INDEX_KEY)][
        ["territory", "code", "value"]
    ].copy()

    fig_base = px.choropleth(
        df,
        locations="code",
        geojson=geodata,
        featureidkey=GEO_KEY,
        color="value",
        color_continuous_scale=DIVERGING_COLORS,
        range_color=[df["value"].min(), df["value"].max()],
        custom_data=["territory"],
    )
    fig_base.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><extra></extra>",
    )
    fig_base.update_layout(
        dragmode=False,
        showlegend=False,
        coloraxis_showscale=False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            projection_type="natural earth",
            projection_scale=15.4,
            showland=False,
            showocean=False,
            showlakes=False,
            showrivers=False,
            visible=False,
            center=dict(lat=41.9, lon=12.5),
        ),
    )
    return fig_base


# ── Serie storica (scorecard) ─────────────────────────────────────────────────

@app.callback(
    Output("scorecard_evolution", "figure"),
    Input("scorecard_territory", "value"),
)
def update_scorecard_evolution(territory):
    df = data[
        (data["territory"] == territory) & (data["indicator"] == INDEX_KEY)
    ][["year", "value"]].copy()

    fig = px.line(
        df,
        x="year",
        y="value",
        markers=True,
        labels={"year": "Anno", "value": "Indice totale (z-score)"},
        color_discrete_sequence=[SEQUENCE_COLOR[0]],
    )
    fig.add_hline(y=0, line_dash="dash", line_color="gray", line_width=1)
    fig.update_layout(
        xaxis=dict(
            tickvals=YEARS_AVAILABLE,
            ticktext=[str(y) for y in YEARS_AVAILABLE],
        ),
        showlegend=False,
    )
    fig.update_traces(
        hovertemplate=(
            "Anno: %{x}<br>"
            + "Indice: %{y:.2f}<br>"
            + "<extra></extra>"
        )
    )
    return fig


# ── Radar dimensionale ────────────────────────────────────────────────────────

@app.callback(
    Output("scorecard_radar", "figure"),
    Input("scorecard_territory", "value"),
)
def update_scorecard_radar(territory):
    dim_keys   = list(CAPACITY_DIMS.keys())
    dim_labels = list(CAPACITY_DIMS.values())
    years_dim  = [2022, 2024]

    fig = go.Figure()
    for i, year in enumerate(years_dim):
        df_year = data[
            (data["territory"] == territory)
            & (data["year"] == year)
            & (data["indicator"].isin(dim_keys))
        ]
        if df_year.empty:
            continue
        values = []
        for k in dim_keys:
            sub = df_year[df_year["indicator"] == k]
            values.append(sub["value"].values[0] if not sub.empty else float("nan"))
        if all(pd.isna(v) for v in values):
            continue
        values = [v if pd.notna(v) else 0 for v in values]
        values_closed = values + [values[0]]
        labels_closed = dim_labels + [dim_labels[0]]
        fig.add_trace(
            go.Scatterpolar(
                r=values_closed,
                theta=labels_closed,
                fill="toself",
                name=str(year),
                line_color=SEQUENCE_COLOR[i],
                opacity=0.7,
            )
        )

    all_cap = data[
        (data["territory"] == territory) & (data["indicator"].isin(dim_keys))
    ]["value"].dropna()
    r_min = min(-2.0, float(all_cap.min()) - 0.2) if not all_cap.empty else -2.0
    r_max = max(2.0,  float(all_cap.max()) + 0.2) if not all_cap.empty else  2.0

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, title="z-score", range=[r_min, r_max])
        ),
        title=f"Profilo dimensionale — {territory}",
        showlegend=True,
        legend=dict(title_text="Anno"),
    )
    return fig


# ── Tabella dimensionale ──────────────────────────────────────────────────────

@app.callback(
    Output("scorecard_dim_table", "children"),
    Input("scorecard_territory", "value"),
)
def update_scorecard_dim_table(territory):
    def _rank(yr, key):
        r = _ind(territory, yr, key)
        if r.empty or pd.isna(r["rank"].values[0]):
            return "N/D"
        return str(int(r["rank"].values[0]))

    rows = []
    for key, label in CAPACITY_DIMS.items():
        rows.append(
            html.Tr(
                [
                    html.Td(label),
                    html.Td(_rank(2024, key), className="text-center"),
                    html.Td(_rank(2022, key), className="text-center"),
                ]
            )
        )

    table = dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("Dimensione"),
                        html.Th("Rank 2024", className="text-center"),
                        html.Th("Rank 2022", className="text-center"),
                    ]
                )
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        size="sm",
    )
    return table
