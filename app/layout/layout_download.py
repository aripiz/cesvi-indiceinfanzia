# layout_download.py — Cesvi Indice Infanzia

from dash import dcc, html
import dash_bootstrap_components as dbc

modal_data_download = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Scarica i dati")),
        dbc.ModalBody(
            [
                html.P(
                    "I dataset dell'Indice di Infanzia Cesvi sono disponibili per il download in formato CSV."
                ),
                dbc.ListGroup(
                    [
                        dbc.ListGroupItem(
                            [
                                html.Div(
                                    [
                                        html.Strong("Dataset completo (formato wide)"),
                                        html.P(
                                            "Indice totale, capacità e ranking dimensionali per tutte le regioni e anni.",
                                            className="mb-1 text-muted small",
                                        ),
                                    ]
                                ),
                                dbc.Button(
                                    "Scarica CSV",
                                    id="download_wide_btn",
                                    color="primary",
                                    size="sm",
                                    className="ms-auto",
                                ),
                                dcc.Download(id="download_wide"),
                            ],
                            className="d-flex justify-content-between align-items-center",
                        ),
                        dbc.ListGroupItem(
                            [
                                html.Div(
                                    [
                                        html.Strong("Dataset (formato long)"),
                                        html.P(
                                            "Stessa informazione in formato long/tidy, con una riga per osservazione.",
                                            className="mb-1 text-muted small",
                                        ),
                                    ]
                                ),
                                dbc.Button(
                                    "Scarica CSV",
                                    id="download_long_btn",
                                    color="primary",
                                    size="sm",
                                    className="ms-auto",
                                ),
                                dcc.Download(id="download_long"),
                            ],
                            className="d-flex justify-content-between align-items-center",
                        ),
                    ]
                ),
            ]
        ),
        dbc.ModalFooter(
            dbc.Button("Chiudi", id="close_download_modal_btn", className="ms-auto")
        ),
    ],
    id="download_modal",
    is_open=False,
    size="lg",
)
