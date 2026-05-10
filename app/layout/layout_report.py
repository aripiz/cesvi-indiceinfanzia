# layout_report.py — Cesvi Indice Infanzia

import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

from configuration import BRAND_COLOR

# ── Carica metadati report ────────────────────────────────────────────────────

REPORTS_FILE = "../data/cesvi-indiceinfanzia_reports.csv"

try:
    _reports_df = pd.read_csv(REPORTS_FILE).sort_values("year", ascending=False)
    _reports = _reports_df.to_dict(orient="records")
except Exception:
    _reports = []

# ── Helper: singola card ──────────────────────────────────────────────────────

def _report_card(report):
    year        = report.get("year", "")
    title       = report.get("title")
    subtitle    = report.get("year", f"Edizione {year}")
    description =  None #report.get("description", "")
    pdf_file    = report.get("pdf_file", "")
    cover_image = report.get("cover_image", "")

    cover_src = f"assets/reports/covers/{cover_image}" if cover_image else None
    pdf_href  = f"/reports/{pdf_file}" if pdf_file else None

    card_body_children = [
        html.H5(title, className="card-title fw-bold mb-1",
                style={"color": "#1a1a1a"}),
    ]
    if subtitle:
        card_body_children.append(
            html.H6(subtitle, className="card-subtitle mb-2",
                    style={"color": "#444"}))
    if description:
        card_body_children.append(
            html.P(description, className="card-text small mb-3",
                   style={"color": "#555"}))
    card_body_children.append(
        dbc.Button(
            [html.I(className="bi bi-file-earmark-pdf me-2"), "Scarica il report"],
            href=pdf_href or "#",
            target="_blank",
            size="sm",
            disabled=(pdf_href is None),
            external_link=True,
            style={"backgroundColor": BRAND_COLOR, "borderColor": BRAND_COLOR, "color": "white"},
        )
    )

    if cover_src:
        card_inner = html.Div(
            [
                # Immagine a piena altezza (formato A4 ≈ 1:1.414)
                html.Div(
                    html.Img(
                        src=cover_src,
                        style={
                            "position": "absolute", "top": 0, "left": 0,
                            "width": "100%", "height": "100%",
                            "objectFit": "cover",
                        },
                    ),
                    style={
                        "position": "relative",
                        "paddingBottom": "141.4%",  # rapporto A4
                        "overflow": "hidden",
                    },
                ),
                # overlay sfumato chiaro in basso
                html.Div(
                    dbc.CardBody(card_body_children),
                    style={
                        "position": "absolute", "bottom": 0, "left": 0, "right": 0,
                        "background": "linear-gradient(to top, rgba(255,255,255,0.95) 55%, transparent 100%)",
                        "padding": "1rem",
                    },
                ),
            ],
            style={"position": "relative", "overflow": "hidden"},
        )
    else:
        card_inner = html.Div(
            [
                html.Div(
                    html.Span(str(year), className="display-4 fw-bold text-white"),
                    className="d-flex align-items-center justify-content-center",
                    style={"height": "200px", "backgroundColor": BRAND_COLOR},
                ),
                dbc.CardBody(card_body_children),
            ]
        )

    return dbc.Col(
        dbc.Card(
            card_inner,
            className="shadow-sm report-card",
            style={"overflow": "hidden", "border": "none"},
        ),
        lg=3, md=4, sm=6, xs=12,
        className="mb-4",
    )


# ── Layout ────────────────────────────────────────────────────────────────────

if _reports:
    cards_row = dbc.Row(
        [_report_card(r) for r in _reports],
        className="g-3",
    )
else:
    cards_row = dbc.Alert(
        "Nessun report disponibile. Aggiungi i dati nel file cesvi-indiceinfanzia_reports.csv.",
        color="warning",
    )

report_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Report", className="mb-1"),
                    html.Div(style={
                        "width": "40px", "height": "4px",
                        "backgroundColor": BRAND_COLOR, "marginBottom": "0.5rem",
                    }),
                    html.P(
                        "Tutti i report annuali dell'Indice regionale sul maltrattamento e la cura all'infanzia in Italia.",
                        className="text-muted mb-4",
                        style={"fontSize": "0.92rem"},
                    ),
                ],
                xs=12,
            )
        ),
        cards_row,
    ],
    class_name="mt-4",
    fluid=False,
)
