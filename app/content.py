# content.py — Cesvi Indice Infanzia

from index import app
from dash import dcc, html, page_container
import dash_bootstrap_components as dbc

from layout.callbacks import render_scorecards, navigation, render_data, download

from configuration import BRAND_LINK, CREDITS_LINK, TITLE, LOGO, LOGO_VERTICAL

# ── Navbar ────────────────────────────────────────────────────────────────────

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Panoramica",    active="exact", href="/",            className="fw-bold")),
        dbc.NavItem(dbc.NavLink("Regioni",       active="exact", href="/scorecards",  className="fw-bold")),
        dbc.NavItem(dbc.NavLink("Dati",          active="exact", href="/data",        className="fw-bold")),
        dbc.NavItem(dbc.NavLink("Metodologia",   active="exact", href="/methodology", className="fw-bold")),
        dbc.NavItem(dbc.NavLink("Pubblicazioni",  active="exact", href="/report",      className="fw-bold")),
        dbc.NavItem(dbc.NavLink("Download",      active="exact", href="/download",    className="fw-bold")),
    ],
   brand=html.Div([
        html.A(
            html.Img(src=LOGO, height="30px", style={"marginRight": "10px"}),
            href=BRAND_LINK,
            target="_blank",
            style={"lineHeight": "0"},
        ),
        html.A(
            html.Span(
                "Indice sul Maltrattamento e la Cura all'Infanzia".upper(),
                className="fw-bold d-none d-md-inline mb-0",
                style={"letter-spacing": "0.05em"},
            ),
            href="/",
            style={"textDecoration": "none", "color": "inherit"},
        ),
    ], className="d-flex align-items-center"),
    brand_href=None,
    fixed="top",
    color="white",
    dark=False,
    class_name="navbar-cesvi border-bottom",
)

# ── Footer ────────────────────────────────────────────────────────────────────

footer = html.Footer(
    dbc.Container(
        [
            html.Hr(className="footer-rule"),
            dbc.Row(
                [
                    # Brand
                    dbc.Col(
                        [
                            html.Img(
                                src=LOGO,
                                height="28px",
                                className="mb-2",
                            ),
                            html.P(
                                TITLE,
                                className="footer-text mb-0",
                            ),
                        ],
                        md=4, xs=12,
                        className="mb-3 mb-md-0",
                    ),
                    # Navigazione — due colonne
                    dbc.Col(
                        [
                            html.P("Sezioni", className="footer-heading mb-2"),
                            dbc.Row([
                                dbc.Col(
                                    html.Ul(
                                        [
                                            html.Li(html.A("Panoramica",    href="/",            className="footer-link")),
                                            html.Li(html.A("Regioni",       href="/scorecards",  className="footer-link")),
                                            html.Li(html.A("Dati",          href="/data",        className="footer-link")),
                                        ],
                                        className="list-unstyled mb-0",
                                    ),
                                    xs=6,
                                ),
                                dbc.Col(
                                    html.Ul(
                                        [
                                            html.Li(html.A("Metodologia",  href="/methodology", className="footer-link")),
                                            html.Li(html.A("Pubblicazioni", href="/report",      className="footer-link")),
                                            html.Li(html.A("Download",      href="/download",    className="footer-link")),
                                        ],
                                        className="list-unstyled mb-0",
                                    ),
                                    xs=6,
                                ),
                            ]),
                        ],
                        md=4, xs=12,
                        className="mb-3 mb-md-0",
                    ),
                    # Cesvi
                    dbc.Col(
                        [
                            html.P("Cesvi", className="footer-heading mb-2"),
                            html.Ul(
                                [
                                    html.Li(html.A("Home", href="https://cesvi.org/", className="footer-link", target="_blank")),
                                    #html.Li(html.A("Indice regionale", href="https://cesvi.org/approfondimenti/indice-regionale-sul-maltrattamento-allinfanzia-italia/", className="footer-link", target="_blank")),
                                    html.Li(html.A("Chi siamo", href="https://cesvi.org/chi-siamo/", className="footer-link", target="_blank")),
                                ],
                                className="list-unstyled mb-0",
                            ),
                        ],
                        md=4, xs=12,
                        className="mb-3 mb-md-0",
                    ),
                ],
                className="mb-4",
            ),
            html.Hr(className="footer-rule"),
            dbc.Row(
                [
                    dbc.Col(
                        html.P(
                            ["© 2026 CESVI - Fondazione ETS"],# " — Tutti i diritti riservati"],
                            className="footer-text mb-0",
                        ),
                        md=9, xs=12,
                    ),
                    dbc.Col(
                        html.P(
                            ["Credits: ", html.A("aripiz", href=CREDITS_LINK, className="footer-link", target="_blank")],
                            className="footer-text mb-0 text-md-end",
                        ),
                        md=3, xs=12,
                    ),
                ],
                className="align-items-center",
            ),
        ],
        class_name="py-4",
    ),
    className="footer-section mt-5",
)

# ── Page container ────────────────────────────────────────────────────────────

content = dbc.Container(
    children=[
        dcc.Location(id="url", refresh="callback-nav"),
        dcc.Store(id="store_territory", storage_type="session"),
        page_container,
    ],
    fluid=True,
    class_name="px-0",
    style={"padding-top": "56px"},
)

# ── Main layout ───────────────────────────────────────────────────────────────

app.layout = html.Div([navbar, content, footer])
