# layout_methodology.py — Cesvi Indice Infanzia

from dash import dcc, html
import dash_bootstrap_components as dbc
from configuration import BRAND_LINK, CAPACITY_DIMS

intro_text = f"""
L'**Indice di Infanzia** di **[Cesvi]({BRAND_LINK})** classifica le 20 regioni italiane in base alle condizioni di vita dei bambini, 
combinando indicatori di benessere in 6 dimensioni chiave: {", ".join(CAPACITY_DIMS.values())}.

I punteggi sono espressi come **z-score** (valori standardizzati rispetto alla media nazionale), 
quindi valori positivi indicano una performance migliore della media, valori negativi indicano una performance peggiore.
"""

structure_text = """
### Struttura dell'indice

L'Indice di Infanzia è composto da **6 dimensioni di capacità** che misurano aspetti complementari del benessere infantile:

| Dimensione | Descrizione |
|---|---|
| **Cura** | Accesso a servizi di cura per l'infanzia, asili nido, supporto familiare |
| **Vita sana** | Salute fisica e mentale, accesso a servizi sanitari e prevenzione |
| **Vita sicura** | Sicurezza del contesto di vita, protezione da violenza e rischi ambientali |
| **Conoscenza e sapere** | Istruzione, accesso alla scuola, qualità dell'apprendimento |
| **Lavorare** | Condizioni economiche della famiglia, occupazione genitoriale |
| **Accedere alle risorse** | Accesso a infrastrutture, servizi pubblici, risorse economiche |

Per ogni regione e anno viene calcolato un **indice totale** come media pesata dei punteggi nelle dimensioni disponibili.
"""

methodology_text = """
### Metodologia

**Standardizzazione z-score:**  
Per ciascun indicatore, il valore di ogni regione viene standardizzato rispetto alla distribuzione nazionale:

$$z = \\frac{x - \\mu}{\\sigma}$$

dove $x$ è il valore della regione, $\\mu$ è la media nazionale e $\\sigma$ è la deviazione standard nazionale.

**Interpretazione:**
- $z > 1.0$: molto sopra la media
- $0.5 < z \\le 1.0$: sopra la media
- $0 < z \\le 0.5$: leggermente sopra la media
- $-0.5 \\le z \\le 0$: leggermente sotto la media
- $-1.0 \\le z < -0.5$: sotto la media
- $z < -1.0$: molto sotto la media

**Anni disponibili:** 2018, 2019, 2020, 2021, 2022, 2024  
**Regioni:** 20 regioni italiane (escluse Province Autonome di Trento e Bolzano aggregate come Trentino-Alto Adige)
"""

methodology_layout = dbc.Container(
    children=[
        dbc.Row(
            dbc.Col(
                html.H2("Metodologia", className="text-center"),
                lg=12,
            ),
            className="mt-2",
        ),
        dbc.Row(
            dbc.Col(
                dcc.Markdown(intro_text),
                lg=12,
            ),
            className="mt-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Markdown(structure_text),
                    lg=6,
                    xs=12,
                ),
                dbc.Col(
                    dcc.Markdown(methodology_text, mathjax=True),
                    lg=6,
                    xs=12,
                ),
            ],
            className="mt-3",
        ),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5("Note sui dati"),
                            html.P(
                                "I dati utilizzati per il calcolo dell'indice provengono da fonti istituzionali italiane (ISTAT, Ministero dell'Istruzione, ecc.). "
                                "I dati dell'anno 2023 non sono inclusi nella serie storica. "
                                "I ranking dimensionali (Cura, Vita sana, ecc.) sono disponibili solo per gli anni 2022 e 2024."
                            ),
                        ]
                    ),
                    color="light",
                ),
                lg=12,
            ),
            className="mt-4 mb-4",
        ),
    ],
    fluid=True,
)
