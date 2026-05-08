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
    description = report.get("description", "")
    pdf_file    = report.get("pdf_file", "")
    cover_image = report.get("cover_image", "")

    # Copertina: cerca in assets/reports/covers/<file>
    cover_src = f"assets/reports/covers/{cover_image}" if cover_image else None
    pdf_href  = f"/reports/{pdf_file}" if pdf_file else None

    cover_el = (
        html.Img(
            src=cover_src,
            className="card-img-top report-cover",
            style={"objectFit": "cover", "maxHeight": "280px", "width": "100%"},
        )
        if cover_src
        else html.Div(
            html.Span(str(year), className="display-4 fw-bold text-white"),
            className="d-flex align-items-center justify-content-center report-cover-placeholder",
            style={
                "height": "200px",
                "backgroundColor": BRAND_COLOR,
                "borderRadius": "4px 4px 0 0",
            },
        )
    )

    card_body_children = [
        html.H5(title, className="card-title fw-bold mb-1"),
    ]
    if subtitle:
        card_body_children.append(html.H6(subtitle, className="card-subtitle text-muted mb-2"))
    if description:
        card_body_children.append(html.P(description, className="card-text small mb-3"))

    card_body_children.append(
        dbc.Button(
            [html.I(className="bi bi-file-earmark-pdf me-2"), "Scarica il report"],
            href=pdf_href or "#",
            target="_blank",
            color="primary",
            size="sm",
            disabled=(pdf_href is None),
            external_link=True,
        )
    )

    return dbc.Col(
        dbc.Card(
            [
                cover_el,
                dbc.CardBody(card_body_children),
            ],
            className="h-100 shadow-sm report-card",
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
                    html.H2("Edizioni", className="mb-1"),
                    html.P(
                        "Tutti i report annuali dell'Indice regionale sul maltrattamento e la cura all'infanzia in Italia.",
                        className="text-muted mb-4",
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
