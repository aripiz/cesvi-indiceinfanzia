# layout_home.py — Cesvi Indice Infanzia

import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import plotly.io as pio
import pandas as pd
from dash_bootstrap_templates import load_figure_template

from index import data, geodata
from configuration import (
    FIGURE_TEMPLATE,
    GEO_KEY,
    INDEX_LABELS,
    ZSCORE_BINS,
    ZSCORE_LABELS,
    ZSCORE_TIER_COLORS,
    BRAND_LINK,
    SEQUENCE_COLOR,
    YEAR_DEFAULT,
)

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE


def display_home_map():
    year = YEAR_DEFAULT
    df = data[
        (data["year"] == year) & (data["index"] == "totale") & data["capacity"].isna()
    ][["territory", "code", "score"]].copy()
    df["tier"] = pd.cut(
        df["score"],
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
        custom_data=["territory", "score", "tier"],
    )
    fig.update_layout(
        dragmode=False,
        showlegend=False,
        autosize=True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0, "pad": 0},
        geo=dict(
            fitbounds="locations",
            projection_type="mercator",
            showland=False,
            showocean=False,
            showlakes=False,
            showrivers=False,
            visible=False,
        ),
    )
    fig.update_traces(
        hovertemplate=(
            "<b>%{customdata[0]}</b><br><br>"
            "Indice totale: "
            "%{customdata[1]}<br>"
            "Fascia: %{customdata[2]}<br>"
            "<extra></extra>"
        )
    )
    return fig


# ── Testi ────────────────────────────────────────────────────────────────────

intro_text = f"""
L'*Indice regionale sul maltrattamento e la cura all'infanzia in Italia* è uno strumento
di analisi originale di **[Cesvi]({BRAND_LINK})** che dal 2018 monitora annualmente
la capacità delle regioni italiane di prevenire e contrastare il maltrattamento minorile.

Costruito su **64 indicatori statistici** aggregati in **6 capacità territoriali**
secondo l'approccio delle capacità di Amartya Sen, l'Indice restituisce una
**classifica decrescente delle 20 regioni italiane**: in testa le regioni con
minori fattori di rischio e sistemi di servizi più solidi, in fondo quelle con
maggiori criticità strutturali.

Il quadro che emerge è quello di **un'Italia a due velocità**: le regioni del Nord
si confermano generalmente più virtuose, mentre il Mezzogiorno presenta criticità
persistenti che richiedono interventi strutturali di lungo periodo.
"""

edition_text = f"""
#### Sesta edizione · *Le parole sono importanti* · {YEAR_DEFAULT}

Il focus dell'edizione {YEAR_DEFAULT} è dedicato al ruolo del **linguaggio nel maltrattamento
e nella cura all'infanzia**. Secondo l'OMS, l'abuso psicologico — di cui la violenza
verbale fa parte — è la forma più diffusa di maltrattamento infantile in Europa,
con una prevalenza del **36,1%** tra i 55 milioni di bambine e bambini che subiscono abusi.

Investire sull'educazione al linguaggio positivo — nelle famiglie, nelle scuole,
nei tavoli di coordinamento territoriale — è una delle leve di prevenzione
che l'Indice indica come prioritaria.
"""

cta_text = """
Esplora la dashboard:
**[Regioni](/scorecards)** · **[Esplora](/data)** · **[Metodologia](/methodology)**
"""

# ── Layout ───────────────────────────────────────────────────────────────────

home_layout = dbc.Container(
    children=[
        # Titolo
        dbc.Row(
            dbc.Col(
                html.Div(
                    children=[
                        html.H2(
                            "Indice regionale sul maltrattamento e la cura all'infanzia in Italia",
                            className="fw-bold",
                        ),
                        html.P(
                            f"Le parole sono importanti · Sesta edizione · {YEAR_DEFAULT}",
                            className="text-muted mb-0",
                            style={"font-size": "0.9rem", "letter-spacing": "0.05em"},
                        ),
                        html.Hr(
                            style={
                                "border-color": "#eb6608",
                                "border-width": "2px",
                                "opacity": "1",
                                "width": "100%",
                                "margin": "0.75rem 0 0 0",
                            }
                        ),
                    ]
                ),
                lg=12,
            ),
            className="mt-4 mb-3",
        ),
        # Mappa + testo
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            dcc.Graph(
                                id="home_map",
                                figure=display_home_map(),
                                style={"height": "65vh"},
                                responsive=True,
                                config={"displayModeBar": False, "editable": False},
                            ),
                            color=SEQUENCE_COLOR[0],
                        ),
                        html.P(
                            "Clicca su una regione per aprire la scheda dettagliata.",
                            className="text-muted text-center mt-1",
                            style={"font-size": "0.8rem"},
                        ),
                    ],
                    lg=5,
                    xs=12,
                    align="center",
                    className="order-2 order-lg-1",
                ),
                dbc.Col(
                    children=[
                        dcc.Markdown(intro_text, className="mb-3"),
                        dcc.Markdown(edition_text, className="mb-4"),
                        dcc.Markdown(cta_text),
                    ],
                    lg=7,
                    xs=12,
                    align="center",
                    className="order-1 order-lg-2",
                ),
            ],
        ),
    ],
    fluid=True,
)