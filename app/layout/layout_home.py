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
    ZSCORE_BINS,
    ZSCORE_LABELS,
    ZSCORE_TIER_COLORS,
    BRAND_LINK,
    SEQUENCE_COLOR,
    YEAR_DEFAULT,
    TITLE
)

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE


def display_home_map():
    year = YEAR_DEFAULT
    df = data[
        (data["year"] == year) & (data["type"] == "totale") & (data["capacity"] == "totale")
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
L'*{TITLE}* è uno strumento
di analisi originale di **[CESVI]({BRAND_LINK})** che dal 2018 monitora annualmente
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
#### Settima edizione · *Generazione sola* · {YEAR_DEFAULT}

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
**[Regioni](/scorecards)** · **[Report](/report)** · **[Dati](/data)** · **[Metodologia](/methodology)**

Scarica i report e i dati completi:
**[Download](/download)**
"""

# ── Dati chiave (placeholder — i valori saranno scelti dall'utente) ──────────

_KEY_STATS = [
    {"value": "20",  "label": "Regioni monitorate"},
    {"value": "64",  "label": "Indicatori statistici"},
    {"value": "6",   "label": "Capacità territoriali"},
    {"value": "7",   "label": "Edizioni dal 2018"},
]

# ── Layout ───────────────────────────────────────────────────────────────────

home_layout = html.Div(
    children=[

        # ── 1. Hero ───────────────────────────────────────────────────────────
        # Sostituisci /assets/hero.jpg con l'immagine scelta
        html.Div(
            className="hero-section",
            children=[
                html.Div(className="hero-overlay"),
                html.Div(
                    className="hero-text",
                    children=[
                        html.Span(className="hero-accent"),
                        html.P(
                            f"Settima edizione · {YEAR_DEFAULT}",
                            className="hero-subtitle mb-3",
                        ),
                        html.H1(
                            TITLE,
                            className="display-5 fw-bold mb-3",
                        ),
                        html.P(
                            "Generazione sola",
                            className="fs-5 mb-0",
                            style={"color": "rgba(255,255,255,0.75)"},
                        ),
                    ],
                ),
            ],
        ),

        # ── 2. Fascia dati chiave ─────────────────────────────────────────────
        html.Div(
            className="stats-strip",
            children=[
                dbc.Container(
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    html.H3(s["value"], className="stat-value mb-0"),
                                    html.P(s["label"], className="stat-label mb-0"),
                                ],
                                xs=6,
                                md=3,
                                className="text-center py-3 d-flex flex-column justify-content-center align-items-center"
                                + (" stat-divider" if i > 0 else ""),
                            )
                            for i, s in enumerate(_KEY_STATS)
                        ],
                        className="g-0 align-items-stretch",
                    ),
                    fluid=True,
                    class_name="px-4",
                ),
            ],
        ),

        # ── 3. Mappa + intro ──────────────────────────────────────────────────
        dbc.Container(
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
                        [
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
            class_name="py-5",
            fluid=False,
        ),
    ],
)
