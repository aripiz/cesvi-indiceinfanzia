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
    INDEX_KEY,
    ZSCORE_BINS,
    ZSCORE_LABELS,
    ZSCORE_TIER_COLORS,
    DIVERGING_COLORS,
    BRAND_LINK,
    SEQUENCE_COLOR,
    YEAR_DEFAULT,
)

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE


def display_home_map():
    year = YEAR_DEFAULT
    feature = INDEX_KEY
    df = data[(data["year"] == year) & (data["indicator"] == feature)][
        ["territory", "code", "value"]
    ].copy()
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
    )
    fig.update_layout(
        dragmode=False,
        showlegend=False,
        autosize=True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0, "pad": 0},
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
    template = (
        "<b>%{customdata[0]}</b><br><br>"
        + f"Indice totale (z-score): "
        + "%{customdata[1]:.2f}<br>"
        + "Fascia: %{customdata[2]}<br>"
        + "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)
    return fig


# ── Testi ────────────────────────────────────────────────────────────────────

opening_text = f"""
L'**Indice regionale sul maltrattamento e la cura all'infanzia in Italia** è uno strumento di analisi originale di **[Cesvi]({BRAND_LINK})** che da sette anni monitora i punti di forza e di debolezza delle regioni italiane rispetto ai fattori di rischio e ai servizi che riguardano il maltrattamento minorile.

Costruito sulla base di **64 indicatori statistici**, l'Indice misura la capacità dei sistemi territoriali di affrontare un tema così importante — e troppo spesso nascosto al dibattito pubblico — offrendo ai portatori di interesse una lettura articolata per individuare le aree di criticità e gli spiragli di miglioramento.
"""

description_text = """
L'indice classifica le **20 regioni italiane** su **6 anni di osservazione** (2018–2024) analizzando sei capacità territoriali:

| Dimensione | Cosa misura |
|---|---|
| **Cura** | Servizi di cura e protezione dell'infanzia |
| **Vita sana** | Salute, dipendenze e vulnerabilità dei minori |
| **Vita sicura** | Sicurezza domestica e violenza di genere |
| **Conoscenza e sapere** | Istruzione e livello culturale |
| **Lavorare** | Condizioni economiche e occupazione |
| **Accedere alle risorse** | Povertà, servizi e inclusione sociale |

Gli indicatori sono aggregati tramite **z-score** — valori standardizzati rispetto alla media nazionale:

- Un valore **positivo** indica una situazione **migliore della media**
- Un valore **negativo** indica una situazione **peggiore della media**
- Il valore **0** corrisponde alla media nazionale

Esplora la dashboard:
- **[Schede regionali](/scorecards):** Panoramica per singola regione, con storico e confronto dimensionale.
- **[Dati](/data):** Mappa interattiva, classifica, serie storica e profilo dimensionale.
- **[Metodologia](/methodology):** Come è costruito l'indice e cosa misura.
"""

# ── Layout ───────────────────────────────────────────────────────────────────

home_layout = dbc.Container(
    children=[
        # dbc.Row(
        #     dbc.Col(
        #         html.H1("Indice regionale sul maltrattamento e la cura all'infanzia in Italia", className="text-center"),
        #         lg=12,
        #     ),
        #     className="mt-2",
        # ),
        dbc.Row(
            dbc.Col(
                dcc.Markdown(opening_text, className="my-3"),
                lg=12,
            ),
        ),
        # Mappa + descrizione
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(
                            id="home_map",
                            figure=display_home_map(),
                            style={"min-height": "55vh"},
                            config={
                                "displayModeBar": False,
                                "editable": False,
                            },
                        ),
                        color=SEQUENCE_COLOR[0],
                    ),
                    lg=5,
                    xs=12,
                    align="center",
                ),
                dbc.Col(
                    children=[
                        html.H4(f"Indice Infanzia {YEAR_DEFAULT}", className="mt-2"),
                        dcc.Markdown(description_text),
                    ],
                    lg=7,
                    xs=12,
                    align="center",
                ),
            ],
            className="mt-3",
        ),
    ],
    fluid=True,
)
