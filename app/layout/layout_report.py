# layout_report.py — Cesvi Indice Infanzia

import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

from configuration import BRAND_COLOR
from index import reports

# ── Helper: single card ─────────────────────────────────────────────────────

def _report_card(report):
    year        = report.get("year", "")
    title       = report.get("title")
    subtitle    = report.get("year", f"Edizione {year}")
    description =  None #report.get("description", "")
    pdf_file    = report.get("pdf_file", "")
    cover_image = report.get("cover_image", "")

    cover_src = f"assets/reports/covers/{cover_image}" if cover_image else None
    pdf_href  = f"/reports/download/{pdf_file}" if pdf_file else None

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

    # Hint cliccabile invece del bottone
    if pdf_href:
        card_body_children.append(
            html.Span(
                [html.I(className="bi bi-box-arrow-up-right me-1"), "Apri il report"],
                style={"fontSize": "0.78rem", "color": BRAND_COLOR, "fontWeight": "600"},
            )
        )

    if cover_src:
        # Tutta la card è un link al PDF
        img_block = html.A(
            [
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
                # overlay sfumato in basso con titolo e hint
                html.Div(
                    dbc.CardBody(card_body_children),
                    style={
                        "position": "absolute", "bottom": 0, "left": 0, "right": 0,
                        "background": "linear-gradient(to top, rgba(255,255,255,0.95) 55%, transparent 100%)",
                        "padding": "1rem",
                    },
                ),
            ],
            href=pdf_href,
            target="_blank",
            style={"textDecoration": "none", "display": "block", "cursor": "pointer"},
        )
        card_inner = html.Div(
            img_block,
            style={"position": "relative", "overflow": "hidden"},
        )
    else:
        card_inner = html.A(
            [
                html.Div(
                    html.Span(str(year), className="display-4 fw-bold text-white"),
                    className="d-flex align-items-center justify-content-center",
                    style={"height": "200px", "backgroundColor": BRAND_COLOR},
                ),
                dbc.CardBody(card_body_children),
            ],
            href=pdf_href or "#",
            target="_blank",
            style={"textDecoration": "none", "color": "inherit"},
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

if reports:
    cards_row = dbc.Row(
        [_report_card(r) for r in reports],
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
                    html.H3("Pubblicazioni", className="page-title"),
                    html.P(
                        "Leggi le pubblicazioni di ogni edizione dell'Indice regionale sul maltrattamento e la cura all'infanzia in Italia.",
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
