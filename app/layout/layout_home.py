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
    SEQUENCE_COLOR,
    YEAR_DEFAULT,
)

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE


def display_home_map():
    year = YEAR_DEFAULT
    df = data[
        (data["year"] == year) & (data["type"] == "totale") & (data["capacity"] == "totale")
    ][["territory", "score"]].copy()
    df["tier"] = pd.cut(
        df["score"],
        bins=ZSCORE_BINS,
        labels=ZSCORE_LABELS,
        right=False,
    ).cat.remove_unused_categories()
    df = df.sort_values("score", ascending=False).reset_index(drop=True)
    df["rank"] = range(1, len(df) + 1)

    fig = px.choropleth(
        df,
        locations="territory",
        geojson=geodata,
        featureidkey=GEO_KEY,
        color="tier",
        color_discrete_map=ZSCORE_TIER_COLORS,
        category_orders={"tier": ZSCORE_LABELS},
        custom_data=["territory", "score", "tier", "rank"],
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
            "Punteggio: %{customdata[1]:.2f}<br>"
            "Posizione: %{customdata[3]} / 20<br>"
            "Fascia: %{customdata[2]}<br>"
            "<extra></extra>"
        )
    )
    return fig


# ── Text content ────────────────────────────────────────────────────────────

intro_text = """
L'Indice regionale sul maltrattamento e la cura all'infanzia in Italia, giunto alla
sua settima edizione, continua a rappresentare uno strumento attraverso il quale leggere
e comprendere i contesti in cui bambini e bambine crescono, con l'obiettivo di migliorare
la capacità dei territori di prevenire e contrastare il maltrattamento all'infanzia.
"""

intro_text_2 = """
In questa edizione si conferma con sempre maggiore evidenza come il maltrattamento
all'infanzia stia assumendo i tratti di un'emergenza strutturale, alimentata da un contesto
sociale segnato da incertezza diffusa, crisi economiche e tensioni geopolitiche, che si
riflettono sul benessere psicologico degli adulti e, di conseguenza, sulle dinamiche familiari.
"""

body_col1_text = """
L'Indice evidenzia una stretta correlazione tra il deterioramento della salute mentale
collettiva, le crisi socio-economiche e l'aumento di trascuratezza e violenza assistita.

I dati più recenti mostrano infatti un aumento significativo dei casi presi in carico dai
servizi sociali, con forme di maltrattamento che si sviluppano spesso in contesti di
fragilità relazionale, stress e difficoltà prolungate.

Il focus di questa edizione è dedicato alla povertà relazionale, una dimensione che negli
ultimi anni è diventata sempre più centrale nel leggere i fattori di rischio.
L'indebolimento dei legami sociali e comunitari, aggravato anche dalle conseguenze della
pandemia, incide infatti profondamente sulla qualità delle relazioni familiari e sul benessere
delle nuove generazioni, rendendo ancora più urgente il ruolo dei servizi e delle politiche
nel sostenere reti di supporto solide e inclusive.
"""

body_col2_text = """
L'Indice, attraverso un sistema articolato di indicatori, offre una lettura dei diversi
territori regionali mettendo in relazione fattori di rischio, fattori protettivi e capacità
di risposta dei servizi. In questo modo consente di osservare non solo la presenza del
problema, ma anche il contesto entro cui esso si sviluppa, restituendo uno strumento utile
per orientare politiche e interventi.

In questa prospettiva, la tutela dell'infanzia si conferma una responsabilità condivisa, che
richiede attenzione continua e la capacità di rafforzare, insieme, le condizioni sociali ed
educative in cui bambini, bambine e adolescenti crescono.
"""

focus_intro_text = """
Questa edizione dell'Indice propone una riflessione sulla povertà relazionale come dimensione fondamentale della
povertà infantile, mettendo al centro lo sguardo e le esperienze dirette di bambini e bambine che vivono in contesti
socio-economicamente svantaggiati. Dalle loro parole emerge soprattutto come la povertà non sia vissuta soltanto come
mancanza di risorse materiali, ma anche come carenza o fragilità di relazioni significative, di ascolto e di opportunità
di condivisione. In questo senso, la qualità dei legami diventa una componente essenziale del loro benessere e sviluppo.
"""

focus_col1_text = """
Le relazioni familiari rappresentano il primo e più importante punto di riferimento nel quale la famiglia, spesso anche
nella sua dimensione allargata, è descritta come uno spazio di protezione, affetto e sostegno, capace di offrire sicurezza
emotiva e supporto concreto. Allo stesso tempo, non mancano elementi di fragilità: conflitti tra genitori, difficoltà
comunicative e, in alcuni casi, situazioni di violenza o anche solo l'assenza incidono profondamente sul vissuto dei più
piccoli. In particolare, emerge una distanza significativa rispetto alla figura paterna, percepita come meno presente sul piano
emotivo, mentre madri e nonni hanno sempre un ruolo centrale nella cura e nell'ascolto.
"""

focus_col2_text = """
Le relazioni tra pari occupano un posto altrettanto rilevante nella vita di bambini e bambine. Gli amici rappresentano una
fonte di gioia, appartenenza e condivisione, ma anche il luogo in cui si manifestano dinamiche problematiche, come ad esempio
il bullismo. I racconti dei bambini e delle bambine, infatti, restituiscono esperienze diffuse di esclusione e discriminazione,
spesso legate all'aspetto fisico, all'origine o all'orientamento sessuale, che producono conseguenze importanti sul piano emotivo,
tra cui tristezza, insicurezza e senso di solitudine. In questo contesto, la possibilità di trovare adulti disponibili all'ascolto
e al supporto rappresenta un fattore decisivo per superare questo tipo di avversità.
"""

focus_col3_text = """
La dimensione economica si intreccia strettamente con quella relazionale, dal momento che le difficoltà materiali influenzano
la qualità della vita quotidiana, limitano il tempo che i genitori possono dedicare ai figli e possono generare tensioni
all'interno della famiglia. Su questo tema i bambini e le bambine mostrano una consapevolezza sorprendente delle condizioni
economiche difficili e dei sacrifici degli adulti, arrivando talvolta a farsi carico di preoccupazioni che hanno un impatto
sul loro benessere.
"""

focus_col4_text = """
Accanto alla famiglia, assume grande importanza anche la rete sociale allargata composta da educatori, educatrici e altri adulti
di riferimento che rappresentano anch'essi figure significative per molti bambini e bambine, capaci di offrire ascolto, sostegno
e opportunità di crescita. I centri educativi, in particolare, vengono percepiti come luoghi sicuri e accoglienti dove è possibile
costruire relazioni positive, sentirsi riconosciuti e sviluppare competenze emotive e relazionali. Anche il contesto territoriale
gioca un ruolo rilevante, soprattutto se si parla di quartieri segnati da insicurezza, violenza e carenza di servizi, alimentando
un senso diffuso di paura e limitando le possibilità di socializzazione. Per questo la presenza di spazi educativi e di comunità
rappresenta un'importante risorsa, capace di offrire alternative e opportunità di crescita.
"""

focus2_col1_text = """
Il benessere dell'infanzia è una condizione dinamica risultante dall'interazione tra famiglia, amici e contesto territoriale,
analizzata attraverso il modello ecologico di Bronfenbrenner. La povertà relazionale è il risultato di un ambiente sfavorevole,
posizionandosi su un continuum tra fattori di rischio e protettivi, influenzato dalle circostanze socio-economiche.

Il maltrattamento all'infanzia e la povertà relazionale sono problematiche strettamente interconnesse che si alimentano a vicenda,
influenzando la vita del minore in ambito familiare, scolastico e territoriale. La protezione dei minori si costruisce attraverso
legami significativi, il supporto alle famiglie e la creazione di spazi educativi accessibili, in cui i bambini agiscono come
soggetti attivi nel definire le priorità per il proprio benessere.
"""

focus2_col2_text = """
Contrastare il maltrattamento e la povertà relazionale richiede un approccio sistemico che ponga il bambino al centro di una
"comunità di cura". Le priorità includono politiche integrate per scuole e servizi, sostegno strutturale alle famiglie e
l'integrazione delle voci dei minori nella ricerca per strategie di prevenzione mirate.
"""

riflessioni_intro_text = """
La settima edizione dell'Indice CESVI conferma che il maltrattamento all'infanzia è un problema strutturale e non
esclusivamente riconducibile alla dimensione privata, influenzato dal contesto sociale e dalla crescente fragilità
familiare. Bisogna quindi rafforzare approcci multidimensionali e di medio-lungo periodo, capaci di agire in modo
integrato su prevenzione, cura e sostegno alle famiglie, riducendo le disuguaglianze territoriali e rafforzando il
capitale sociale delle comunità. In questa prospettiva:
"""

prop1_text = """
È necessario rafforzare la rete dei servizi territoriali integrando pubblico, privato e "antenne" come pediatri
e scuole, per garantire un monitoraggio precoce e interventi multidisciplinari che proteggano i minorenni.
"""

prop2_text = """
È urgente adottare parametri di valutazione omogenei e banche dati condivise tra pubblico e privato per
misurare l'impatto reale degli interventi, trasformando le singole buone pratiche innovative in politiche strutturali
basate su evidenze tempestive.
"""

prop3_text = """
È prioritario investire in una formazione trasversale e specialistica per tutti gli operatori e le "antenne"
del territorio, affinché dispongano di strumenti avanzati per intercettare precocemente le nuove forme di
maltrattamento e agire come una rete coordinata.
"""

prop4_text = """
È prioritario contrastare la povertà relazionale promuovendo politiche che ricostruiscano i legami sociali
e potenzino le capacità affettive, trasformando il supporto della comunità in un fattore protettivo essenziale per
superare l'isolamento e l'incomunicabilità.
"""

prop5_text = """
È necessario un cambio di paradigma che integri stabilmente la prevenzione del maltrattamento nelle politiche
pubbliche, come il Piano Nazionale di Prevenzione Sanitaria, garantendo una governance coordinata e il passaggio da
un approccio emergenziale a strategie preventive strutturate su tutto il territorio.
"""

# ── Key stats ───────────────────────────────────────────────────────────────

_KEY_STATS = [
    {"value": "20",  "label": "Regioni monitorate"},
    {"value": "65",  "label": "Indicatori statistici"},
    {"value": "6",   "label": "Capacità territoriali"},
    {"value": "7",   "label": "Edizioni dal 2018"},
]

# ── Layout ───────────────────────────────────────────────────────────────────

home_layout = html.Div(
    children=[

        # ── 1. Hero split (testo sx | foto dx) ───────────────────────────────
        html.Div(
            className="hero-split",
            children=[
                # Colonna sinistra — testo su sfondo scuro
                html.Div(
                    className="hero-split-left",
                    children=[
                        html.Div(
                            className="hero-left-content",
                            children=[
                                html.H1(
                                    [
                                        "Indice regionale sul maltrattamento",
                                        html.Br(),
                                        "e la cura all\u2019infanzia in Italia ",
                                        html.Span(str(YEAR_DEFAULT), style={"color": "var(--cesvi-orange)"}),
                                    ],
                                    className="hero-title",
                                ),
                                html.Div(
                                    className="hero-focus-tag",
                                    children=[
                                        html.Span("GENERAZIONE", className="d-block"),
                                        html.Span("SOLA", className="d-block"),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="hero-scroll-hint",
                            id="hero-scroll-btn",
                            n_clicks=0,
                        ),
                    ],
                ),
                # Colonna destra — foto
                html.Div(className="hero-split-right"),
            ],
        ),

        # ── 2. Key stats strip ─────────────────────────────────────────────
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

        # ── 3. Map + intro column ──────────────────────────────────────────
        dbc.Container(
            [
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
                                dcc.Markdown(intro_text, className="intro-lead mb-3"),
                                dcc.Markdown(intro_text_2, className="mb-4"),
                                html.Hr(className="my-3"),
                                html.P("Esplora la dashboard:", className="text-muted small mb-2"),
                                html.Div(
                                    [
                                        dbc.Button("Regioni",      href="/scorecards",  color="primary", outline=True, size="sm", className="me-2 mb-2"),
                                        dbc.Button("Dati",         href="/data",        color="primary", outline=True, size="sm", className="me-2 mb-2"),
                                        dbc.Button("Metodologia",  href="/methodology", color="primary", outline=True, size="sm", className="me-2 mb-2"),
                                        dbc.Button("Pubblicazioni", href="/report",     color="primary", outline=True, size="sm", className="me-2 mb-2"),
                                    ],
                                    className="mb-2",
                                ),
                                html.P("Scarica i dati completi:", className="text-muted small mb-2"),
                                dbc.Button("Download", href="/download", color="primary", size="sm", className="me-2"),
                            ],
                            lg=7,
                            xs=12,
                            align="center",
                            className="order-1 order-lg-2",
                        ),
                    ],
                ),
                html.Hr(className="my-4"),
                html.H3("GENERAZIONE SOLA", className="page-title mb-4"),
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Markdown(body_col1_text),
                            lg=6,
                            xs=12,
                        ),
                        dbc.Col(
                            dcc.Markdown(body_col2_text),
                            lg=6,
                            xs=12,
                        ),
                    ],
                    className="mb-4",
                ),

                # ── 4. Edition focus section ────────────────────────────────
                html.Div(
                    [
                        html.H4(
                            "LA POVERTÀ RELAZIONALE E IL MALTRATTAMENTO INFANTILE: "
                            "IL PUNTO DI VISTA DEI BAMBINI E DELLE BAMBINE",
                            className="page-title",
                        ),
                        dcc.Markdown(focus_intro_text, className="intro-lead pt-3 pb-2"),
                    ],
                    className="mb-3",
                ),
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            dcc.Markdown(focus_col1_text),
                            title="Le relazioni familiari",
                        ),
                        dbc.AccordionItem(
                            dcc.Markdown(focus_col2_text),
                            title="Le relazioni tra pari",
                        ),
                        dbc.AccordionItem(
                            dcc.Markdown(focus_col3_text),
                            title="La dimensione economica",
                        ),
                        dbc.AccordionItem(
                            dcc.Markdown(focus_col4_text),
                            title="La rete sociale allargata e il territorio",
                        ),
                    ],
                    start_collapsed=True,
                    flush=True,
                    className="mb-5",
                ),

                # ── 5. Interpretive box ───────────────────────────────────────
                dbc.Card(
                    dbc.CardBody(
                        dbc.Row([
                            dbc.Col(dcc.Markdown(focus2_col1_text), lg=7, xs=12),
                            dbc.Col(dcc.Markdown(focus2_col2_text), lg=5, xs=12),
                        ])
                    ),
                    className="mb-5 interpretive-box",
                ),

                # ── 6. Proposals section ─────────────────────────────────────
                html.H4(
                    "RIFLESSIONI E PROPOSTE PER POLITICHE DI PREVENZIONE, CONTRASTO E CURA",
                    className="page-title mb-3",
                ),
                dcc.Markdown(riflessioni_intro_text, className="intro-lead pb-3"),
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            dcc.Markdown(prop1_text),
                            title="Rafforzare la rete dei servizi territoriali",
                        ),
                        dbc.AccordionItem(
                            dcc.Markdown(prop2_text),
                            title="Adottare parametri di valutazione omogenei e banche dati condivise",
                        ),
                        dbc.AccordionItem(
                            dcc.Markdown(prop3_text),
                            title="Investire nella formazione trasversale e specialistica",
                        ),
                        dbc.AccordionItem(
                            dcc.Markdown(prop4_text),
                            title="Contrastare la povertà relazionale",
                        ),
                        dbc.AccordionItem(
                            dcc.Markdown(prop5_text),
                            title="Un cambio di paradigma nelle politiche pubbliche",
                        ),
                    ],
                    start_collapsed=True,
                    flush=True,
                    className="mb-4",
                ),
            ],
            class_name="py-5",
            fluid=False,
        ),
    ],
)