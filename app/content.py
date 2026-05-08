# content.py — Cesvi Indice Infanzia

from index import app
from dash import dcc, html, page_container
import dash_bootstrap_components as dbc

from layout.callbacks import render_scorecards, navigation, render_data

from configuration import BRAND_LINK, CREDITS_LINK, TITLE, LOGO, BRAND_SECONDARY_COLOR

# ── Navbar ────────────────────────────────────────────────────────────────────

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Panoramica",  active="exact", href="/",            className="fw-bold")),
        dbc.NavItem(dbc.NavLink("Regioni",     active="exact", href="/scorecards",  className="fw-bold")),
        dbc.NavItem(dbc.NavLink("Dati",        active="exact", href="/data",        className="fw-bold")),
        dbc.NavItem(dbc.NavLink("Report",      active="exact", href="/report",      className="fw-bold")),
        dbc.NavItem(dbc.NavLink("Metodologia", active="exact", href="/methodology", className="fw-bold")),
    ],
   brand=html.Div([
        html.Img(
            src=LOGO, 
            height="30px",
            # Rimosso verticalAlign, teniamo solo il margine
            style={"marginRight": "10px"} 
        ),
        html.Span(
            "Indice sul Maltrattamento e la Cura all'Infanzia".upper(),
            className="fw-bold d-none d-md-inline mb-0",
            style={"color": "#eb6608", "letter-spacing": "0.05em"},
        ),
    ], className="d-flex align-items-center"), 
    brand_href=BRAND_LINK,
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
                                "Indice regionale sul maltrattamento e la cura all'infanzia in Italia",
                                className="footer-text mb-0",
                            ),
                        ],
                        md=5, xs=12,
                        className="mb-3 mb-md-0",
                    ),
                    # Navigazione
                    dbc.Col(
                        [
                            html.P("Sezioni", className="footer-heading mb-2"),
                            html.Ul(
                                [
                                    html.Li(html.A("Panoramica",  href="/",            className="footer-link")),
                                    html.Li(html.A("Regioni",     href="/scorecards",  className="footer-link")),
                                    html.Li(html.A("Dati",        href="/data",        className="footer-link")),
                                    html.Li(html.A("Report",      href="/report",      className="footer-link")),
                                    html.Li(html.A("Metodologia", href="/methodology", className="footer-link")),
                                ],
                                className="list-unstyled mb-0",
                            ),
                        ],
                        md=3, xs=6,
                        className="mb-3 mb-md-0",
                    ),
                    # Info
                    dbc.Col(
                        [
                            html.P("Risorse", className="footer-heading mb-2"),
                            html.Ul(
                                [
                                    html.Li(html.A("Scarica i dati", href="#", className="footer-link", target="_blank")),
                                    html.Li(html.A("Scarica il report", href="#", className="footer-link")),
                                ],
                                className="list-unstyled mb-0",
                            ),
                        ],
                        md=2, xs=6,
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
                            ["© 2026 ", html.A("CESVI - Fondazione ETS", href=BRAND_LINK, className="footer-link"),],# " — Tutti i diritti riservati"],
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
