# layout_download.py — Cesvi Indice Infanzia

import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc

from configuration import BRAND_COLOR
from index import reports

# ── Helper: riga report ───────────────────────────────────────────────────────

def _report_row(report):
    year      = report.get("year", "")
    title     = report.get("title", f"Report {year}")
    pdf_file  = report.get("pdf_file", "")
    # Route separata che forza il download con nome personalizzato
    dl_href   = f"/reports/download/{pdf_file}" if pdf_file else None

    return dbc.ListGroupItem(
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Strong(title),
                        html.Span(f" — {year}", className="text-muted small ms-1"),
                    ],
                    xs=9,
                    className="d-flex align-items-center",
                ),
                dbc.Col(
                    dbc.Button(
                        [html.I(className="bi bi-download me-1"), "Scarica PDF"],
                        href=dl_href or "#",
                        size="sm",
                        disabled=(dl_href is None),
                        external_link=True,
                        style={
                            "backgroundColor": BRAND_COLOR,
                            "borderColor": BRAND_COLOR,
                            "color": "white",
                        },
                    ),
                    xs=3,
                    className="text-end",
                ),
            ],
            align="center",
        ),
        className="py-2",
    )


# ── Layout ────────────────────────────────────────────────────────────────────

download_layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                [
                    html.H2("Download", className="mb-1"),
                    html.Div(
                        style={
                            "width": "40px",
                            "height": "4px",
                            "backgroundColor": BRAND_COLOR,
                            "marginBottom": "0.5rem",
                        }
                    ),
                    html.P(
                        "Scarica i report annuali e i dataset dell'Indice regionale sul maltrattamento e la cura all'infanzia in Italia.",
                        className="text-muted mb-4",
                        style={"fontSize": "0.92rem"},
                    ),
                ],
                xs=12,
            )
        ),

        # ── Report PDF ───────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                [
                    html.H5("Report annuali", className="fw-bold mb-3"),
                    html.P(
                        "Scarica i report annuali in formato PDF.",
                        className="text-muted small mb-3",
                    ),
                    dbc.ListGroup(
                        [_report_row(r) for r in reports]
                        if reports
                        else [
                            dbc.ListGroupItem(
                                "Nessun report disponibile.",
                                className="text-muted",
                            )
                        ],
                        flush=True,
                        className="mb-5",
                    ),
                ],
                lg=8,
                xs=12,
            )
        ),

        # ── Dataset Excel ─────────────────────────────────────────────────────
        dbc.Row(
            dbc.Col(
                [
                    html.H5("Dataset", className="fw-bold mb-1"),
                    html.P(
                        "Scarica l'intero dataset dell'Indice in formato Excel.",
                        className="text-muted small mb-3",
                    ),
                    dbc.Button(
                        [
                            html.I(className="bi bi-file-earmark-excel me-2"),
                            "Scarica Excel",
                        ],
                        id="download_excel_btn",
                        style={
                            "backgroundColor": BRAND_COLOR,
                            "borderColor": BRAND_COLOR,
                            "color": "white",
                        },
                    ),
                    dcc.Download(id="download_excel"),
                ],
                lg=8,
                xs=12,
            )
        ),
    ],
    class_name="mt-4",
    fluid=False,
)
