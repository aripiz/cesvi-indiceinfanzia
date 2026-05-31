# layout_methodology.py — Cesvi Indice Infanzia

from dash import dcc, html
import dash_bootstrap_components as dbc
from configuration import BRAND_LINK, CAPACITY_DIMS, BRAND_COLOR

# ── Text content ────────────────────────────────────────────────────────────

obiettivi_text = """
**L'Indice regionale sul maltrattamento e la cura all'infanzia in Italia** valuta come il contesto
socio-economico e i servizi presenti nelle varie regioni possano incidere, positivamente o negativamente,
sul benessere dei bambini/e o, viceversa, sulla loro vulnerabilità a fenomeni di maltrattamento.
Dal confronto tra l'indice di contesto e quello relativo alle politiche e ai servizi emerge la
capacità/sensibilità delle amministrazioni locali di prevenire e contrastare questa problematica
attraverso le politiche e i servizi, offrendo indicazioni di policy indispensabili per evidenziare i
punti di forza e di debolezza dei vari territori.
"""

metodologia_col1_text = """
L'Indice propone una **classifica decrescente tra regioni** a partire da quelle che presentano sia minori
rischi di maltrattamento familiare per l'infanzia sia un sistema di politiche e servizi territoriali
adeguato a contrastare e prevenire il problema.

È il risultato dell'aggregazione progressiva di **65 indicatori** relativi ai **fattori di rischio** e ai
**servizi offerti sul territorio** che ha dato origine ai seguenti indici di dettaglio:

- l'indice di contesto dei fattori di rischio (relativo ad adulti e minorenni);
- l'indice dei servizi (relativo ad adulti e minorenni);
- l'indice territoriale generale per capacità (aggregazione dei fattori di rischio e dei servizi).
"""

metodologia_col2_text = """
I **65 indicatori territoriali** sono stati classificati in base alle *capacità*, secondo la teoria
dell'*"Approccio delle capacità nella prospettiva allo Sviluppo Umano"* e rispetto alla distinzione
tra fattori di rischio e servizi da un lato tra adulti/e potenzialmente maltrattanti e bambini/e
potenzialmente maltrattati dall'altro.

L'**Indice aggregato** per ogni categoria in esame è stato costruito attraverso l'applicazione di una
formula di standardizzazione per ciascun indicatore, seguita dal calcolo della media tra tutti gli
indicatori regionali e l'ordinamento in ordine decrescente.
"""

note_text = """
**Anni disponibili:** 2018, 2019, 2020, 2021, 2022, 2024, 2026

**Regioni:** 20 regioni italiane (le Province Autonome di Trento e Bolzano sono aggregate come Trentino-Alto Adige)

**Fonte dati:** ISTAT, Ministero dell'Istruzione, Ministero della Salute e altre fonti istituzionali italiane.
"""

# ── 6 Capacità ────────────────────────────────────────────────────────────────

_CAPACITA = [
    ("1", "Cura di sé e degli altri"),
    ("2", "Vivere una vita sana"),
    ("3", "Acquisire conoscenza e sapere"),
    ("4", "Lavorare"),
    ("5", "Accedere alle risorse e ai servizi"),
    ("6", "Vivere una vita sicura"),
]

# ── Indicator tables ────────────────────────────────────────────────────────

_RISCHIO_BAMBINI = {
    "Capacità di vivere una vita sana": "Gravidanze precoci, Obesità infantile, Fumo in età giovanile, Consumo di alcol in età giovanile, Consumo di droghe in età giovanile, Gioco d'azzardo problematico.",
}

_RISCHIO_ADULTI = {
    "Capacità di cura": "Giovane età dei genitori, Famiglie monoparentali, Caratteristiche caratteriali personali (Soddisfazione per la vita), Gravidanze indesiderate (Uso di metodi contraccettivi moderni), Scarsa coesione familiare e famiglie disfunzionali (Separazioni e soddisfazione per le relazioni familiari), Numero componenti della famiglia.",
    "Capacità di vivere una vita sana": "Uso di Alcol, Droghe, Malattia mentale.",
    "Capacità di vivere una vita sicura": "Isolamento sociale, Violenza del partner, Insicurezza e scarso controllo sociale, Valori e norme sociali che approvano il maltrattamento.",
    "Capacità di acquisire conoscenza e sapere": "Basso livello di istruzione e svantaggio socio-economico, Livello di istruzione delle donne.",
    "Capacità di lavorare": "Disoccupazione, Occupati non regolari, Famiglie a bassa intensità lavorativa.",
    "Capacità di accedere alle risorse e ai servizi": "Povertà individuale e familiare, Valutazione soggettiva di difficoltà economica, Disuguaglianza di reddito, Crescita del PIL.",
}

_SERVIZI_BAMBINI = {
    "Capacità di cura": "Servizi socio-educativi per la prima infanzia, Servizi sociali per l'infanzia, Minori ospiti presidi residenziali, Servizi sociali per sostegno socio-educativo e scolastico.",
    "Capacità di vivere una vita sana": "Servizi ospedalieri per disturbi psichici per 0-17 anni, Assistenza medica territoriale (Pediatri), Sostegno alla maternità (Consultori).",
}

_SERVIZI_ADULTI = {
    "Capacità di cura": "Sostegno alla maternità (Gestanti o madri ospiti nei presidi residenziali e consultori), Sostegno alla genitorialità, Servizi per famiglie e minori (Servizio sociale professionale, Assistenza domiciliare socio-assistenziale, Assistenza residenziale e semiresidenziale).",
    "Capacità di vivere una vita sana": "Servizi ospedalieri per disturbi psichici da abuso di alcol, di droghe e affettivi (Tasso di dimissioni ospedaliere), Utenti SERD, Numero strutture di assistenza psichiatrica e centri di salute mentale, Utenti servizio sociale area Dipendenza.",
    "Capacità di vivere una vita sicura": "Persone coinvolte in procedure penali, Ospiti dei presidi residenziali socio-assistenziali e socio-sanitari, Centri antiviolenza e case rifugio, Integrazione sociale.",
    "Capacità di acquisire conoscenza e sapere": "Adulti inoccupati che partecipano ad attività formative e di istruzione.",
    "Capacità di lavorare": "Utenti dei servizi comunali per l'inserimento lavorativo.",
    "Capacità di accedere alle risorse e ai servizi": "Contributi comunali di integrazione al reddito per l'accesso ai servizi, Servizi comunali per gli alloggi e la situazione abitativa.",
}


def _indicator_table(bambini_dict, adulti_dict):
    rows = []
    rows.append(html.Tr([
        html.Td("BAMBINI E BAMBINE", colSpan=2, style={
            "backgroundColor": BRAND_COLOR, "color": "#fff",
            "fontWeight": "700", "padding": "0.5rem 0.75rem",
            "fontSize": "0.85rem", "textTransform": "uppercase",
            "letterSpacing": "0.05em",
        }),
    ]))
    for cap, desc in bambini_dict.items():
        rows.append(html.Tr([
            html.Td(cap, style={
                "color": BRAND_COLOR, "fontWeight": "600",
                "width": "28%", "padding": "0.45rem 0.75rem",
                "fontSize": "0.85rem", "verticalAlign": "top",
                "borderBottom": "1px solid #e0e0e0",
            }),
            html.Td(desc, style={
                "fontSize": "0.85rem", "padding": "0.45rem 0.75rem",
                "borderBottom": "1px solid #e0e0e0",
            }),
        ]))
    rows.append(html.Tr([
        html.Td("ADULTI", colSpan=2, style={
            "backgroundColor": BRAND_COLOR, "color": "#fff",
            "fontWeight": "700", "padding": "0.5rem 0.75rem",
            "fontSize": "0.85rem", "textTransform": "uppercase",
            "letterSpacing": "0.05em",
        }),
    ]))
    for cap, desc in adulti_dict.items():
        rows.append(html.Tr([
            html.Td(cap, style={
                "color": BRAND_COLOR, "fontWeight": "600",
                "width": "28%", "padding": "0.45rem 0.75rem",
                "fontSize": "0.85rem", "verticalAlign": "top",
                "borderBottom": "1px solid #e0e0e0",
            }),
            html.Td(desc, style={
                "fontSize": "0.85rem", "padding": "0.45rem 0.75rem",
                "borderBottom": "1px solid #e0e0e0",
            }),
        ]))
    return html.Table(rows, className="w-100", style={"borderCollapse": "collapse"})


# ── Layout ───────────────────────────────────────────────────────────────────

methodology_layout = dbc.Container(
    [
        # ── Page title ───────────────────────────────────────────────────────
        dbc.Row(dbc.Col([
            html.H3("Metodologia", className="page-title"),
            html.P(
                "La struttura metodologica, gli indicatori e le scelte di aggregazione dell’Indice.",
                className="text-muted mb-3",
                style={"fontSize": "0.92rem"},
            ),
        ], xs=12), className="mb-2"),

        # ── Objectives ───────────────────────────────────────────────────────
        html.H4("Obiettivi dell'indice", className="page-title mb-3"),
        dcc.Markdown(obiettivi_text, className="mb-4"),

        # ── Structure ────────────────────────────────────────────────────────
        html.H4("Struttura", className="page-title mb-3"),
        dbc.Row([
            dbc.Col(dcc.Markdown(metodologia_col1_text), lg=6, xs=12),
            dbc.Col(dcc.Markdown(metodologia_col2_text), lg=6, xs=12),
        ], className="mb-4"),

        # ── Capacity schema + aggregate indices ─────────────────────────────
        dbc.Row([
            dbc.Col(html.P("CAPACITÀ", style={
                "color": BRAND_COLOR, "fontWeight": "700",
                "letterSpacing": "0.08em", "fontSize": "0.8rem",
                "textTransform": "uppercase", "marginBottom": "0.4rem",
                "textAlign": "center",
            }), lg=5, xs=12),
            dbc.Col(lg=1, xs=0),  # spazio per la parentesi (30px fissi nel contenuto)
            dbc.Col(html.P("INDICI AGGREGATI", style={
                "color": BRAND_COLOR, "fontWeight": "700",
                "letterSpacing": "0.08em", "fontSize": "0.8rem",
                "textTransform": "uppercase", "marginBottom": "0.4rem",
                "textAlign": "center",
            }), lg=4, xs=12),
        ], justify="center"),
        dbc.Row([
            # Col 1: griglia 6 capacità dentro contenitore arancione
            dbc.Col(
                html.Div(
                    html.Div(
                        [
                            html.Div([
                                html.Span(num, style={
                                    "fontWeight": "900", "fontSize": "1.15rem",
                                    "color": BRAND_COLOR, "marginRight": "0.4rem",
                                    "lineHeight": "1", "flexShrink": "0",
                                }),
                                html.Span(label, style={
                                    "fontSize": "0.82rem", "color": "#3d1a00",
                                    "fontWeight": "600", "lineHeight": "1.3",
                                }),
                            ], style={
                                "backgroundColor": "#fce8d5",
                                "borderRadius": "0.5rem",
                                "padding": "0.55rem 0.75rem",
                                "display": "flex",
                                "alignItems": "center",
                            })
                            for num, label in _CAPACITA
                        ],
                        style={
                            "display": "grid",
                            "gridTemplateColumns": "1fr 1fr",
                            "gap": "0.5rem",
                        },
                    ),
                    style={
                        "backgroundColor": BRAND_COLOR,
                        "borderRadius": "1.2rem",
                        "padding": "0.85rem",
                        "height": "100%",
                    },
                ),
                lg=5, xs=12,
                className="mb-3 mb-lg-0",
            ),
            # Parentesi centrale: larghezza fissa, non Bootstrap col
            html.Div(
                html.Div(style={
                    "borderTop": f"2px solid {BRAND_COLOR}",
                    "borderRight": f"2px solid {BRAND_COLOR}",
                    "borderBottom": f"2px solid {BRAND_COLOR}",
                    "width": "14px",
                    "height": "100%",
                }),
                style={
                    "display": "flex",
                    "justifyContent": "center",
                    "alignItems": "stretch",
                    "width": "30px",
                    "flexShrink": "0",
                    "padding": "8px 0",
                },
                className="d-none d-lg-flex",
            ),
            # Col 3: Servizi + Fattori di Rischio → parentesi → Totale
            dbc.Col(
                # Wrapper esterno: centra verticalmente nella colonna
                html.Div([
                    # Gruppo interno: altezza naturale dei soli box + parentesi
                    html.Div([
                        # Due box
                        html.Div([
                            html.Div("Servizi", style={
                                "backgroundColor": "#fce8d5",
                                "borderRadius": "0.5rem",
                                "padding": "0.55rem 1rem",
                                "fontSize": "0.85rem", "fontWeight": "600",
                                "color": "#3d1a00", "textAlign": "center",
                            }),
                            html.Div("Fattori di Rischio", style={
                                "backgroundColor": "#fce8d5",
                                "borderRadius": "0.5rem",
                                "padding": "0.55rem 1rem",
                                "fontSize": "0.85rem", "fontWeight": "600",
                                "color": "#3d1a00", "textAlign": "center",
                            }),
                        ], style={
                            "display": "flex", "flexDirection": "column", "gap": "0.75rem",
                        }),
                        # Parentesi destra (abbraccia solo i due box)
                        html.Div(style={
                            "borderTop": f"2px solid {BRAND_COLOR}",
                            "borderRight": f"2px solid {BRAND_COLOR}",
                            "borderBottom": f"2px solid {BRAND_COLOR}",
                            "width": "14px",
                            "alignSelf": "stretch",
                            "margin": "4px 6px",
                            "flexShrink": "0",
                        }),
                        # Totale
                        html.Div("Totale", style={
                            "backgroundColor": BRAND_COLOR,
                            "borderRadius": "0.5rem",
                            "padding": "0.6rem 1.2rem",
                            "color": "#fff",
                            "fontWeight": "800",
                            "alignSelf": "center",
                            "fontSize": "0.88rem",
                            "textAlign": "center",
                            "whiteSpace": "nowrap",
                        }),
                    ], style={
                        "display": "flex",
                        "alignItems": "stretch",
                    }),
                ], style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "flex-start",
                    "height": "100%",
                }),
                lg=4, xs=12,
            ),
        ], className="mb-5 align-items-stretch justify-content-center"),

        # ── Risk factors table ────────────────────────────────────────────────
        html.H4("Fattori di rischio identificati", className="page-title mb-3"),
        _indicator_table(_RISCHIO_BAMBINI, _RISCHIO_ADULTI),

        html.Hr(className="my-4"),

        # ── Services table ────────────────────────────────────────────────────
        html.H4("Servizi identificati", className="page-title mb-3"),
        _indicator_table(_SERVIZI_BAMBINI, _SERVIZI_ADULTI),

        html.Hr(className="my-4"),

        # ── Notes ────────────────────────────────────────────────────────────
        dbc.Card(
            dbc.CardBody(dcc.Markdown(note_text)),
            className="mb-5 interpretive-box",
        ),
    ],
    fluid=False,
    class_name="mt-4",
)

