# layout_news.py — Cesvi Indice Infanzia
#
# Le notizie sono lette da un Google Sheet pubblicato come CSV.
# Imposta NEWS_CSV_URL in configuration.py con il link del foglio.
# La pagina si aggiorna automaticamente ogni ora senza riavviare l'app.
#
# Colonne attese nel foglio:
#   date   | title | source | url

from dash import html, dcc
import dash_bootstrap_components as dbc

# ── Aggiornamento automatico: ogni ora ───────────────────────────────────────

NEWS_REFRESH_MS = 60 * 60 * 1000  # 1 ora in millisecondi

# ── Helper: singola card notizia ─────────────────────────────────────────────

def _news_item(item):
    return dbc.ListGroupItem(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Span(
                            item.get("date", ""),
                            className="text-muted small me-2",
                        ),
                        html.Span(
                            item.get("source", ""),
                            className="badge me-2",
                            style={"backgroundColor": "#eb6608", "color": "#fff",
                                   "fontSize": "0.72rem", "verticalAlign": "middle"},
                        ),
                        html.A(
                            item.get("title", ""),
                            href=item.get("url", "#"),
                            target="_blank",
                            className="fw-semibold text-decoration-none",
                            style={"color": "#1a1a1a"},
                        ),
                    ],
                    xs=12,
                    className="d-flex align-items-center flex-wrap gap-1 py-1",
                ),
            ],
            align="center",
        ),
        className="py-2 px-3",
    )


def build_news_list(news_items):
    """Costruisce il ListGroup da una lista di dizionari."""
    if not news_items:
        return html.P("Nessuna notizia disponibile al momento.", className="text-muted fst-italic")
    return dbc.ListGroup(
        [_news_item(n) for n in news_items],
        flush=True,
    )


# ── Layout ────────────────────────────────────────────────────────────────────

news_layout = dbc.Container(
    [
        dcc.Interval(
            id="news_refresh_interval",
            interval=NEWS_REFRESH_MS,
            n_intervals=0,
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.H3("Notizie", className="page-title"),
                    html.P(
                        "Aggiornamenti e notizie relativi all'Indice regionale sul maltrattamento e la cura all'infanzia in Italia.",
                        className="text-muted mb-4",
                        style={"fontSize": "0.92rem"},
                    ),
                ],
                xs=12,
            )
        ),
        dbc.Row(
            dbc.Col(
                dcc.Loading(
                    html.Div(id="news_list_container"),
                    color="#eb6608",
                ),
                lg=9, xs=12,
            )
        ),
    ],
    class_name="mt-4",
    fluid=False,
)
