# content.py — Cesvi Indice Infanzia

from index import app
from dash import dcc, html, page_container
import dash_bootstrap_components as dbc

from layout.callbacks import render_scorecards, navigation
# TODO: aggiungere render_data quando implementato

from configuration import BRAND_LINK, CREDITS_LINK, TITLE, LOGO, BRAND_SECONDARY_COLOR

# ── Navbar ────────────────────────────────────────────────────────────────────

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Panoramica",   active="exact", href="/")),
        dbc.NavItem(dbc.NavLink("Regioni",      active="exact", href="/scorecards")),
        dbc.NavItem(dbc.NavLink("Esplora",      active="exact", href="/data")),
        dbc.NavItem(dbc.NavLink("Metodologia",  active="exact", href="/methodology")),
    ],
   brand=html.Div([
        html.Img(
            src="assets/cesvi-logo_horizontal.png", 
            height="30px",
            # Rimosso verticalAlign, teniamo solo il margine
            style={"marginRight": "10px"} 
        ),
        html.Span(
            "Indice sul Maltrattamento e la Cura all'Infanzia", 
            className="fw-bold d-none d-md-inline mb-0",# style={"color": BRAND_SECONDARY_COLOR}
        ),
    ], className="d-flex align-items-center"), 
    brand_href=BRAND_LINK,
    fixed="top",
    color="white",
    dark=False,
    class_name="navbar-cesvi border-bottom",
)

# ── Footer ────────────────────────────────────────────────────────────────────

footer = dbc.Navbar(
    dbc.Container(
        children=[
            html.P(
                children=[
                    "© 2026 ",
                    html.A("CESVI Fondazione — ETS", href=BRAND_LINK, className="link"),
                ],
                style={"font-size": "x-small"},
                className="mb-0",
            ),
            html.P(
                children=["credits: ", html.A("aripiz", href=CREDITS_LINK, className="link")],
                style={"font-size": "x-small"},
                className="mb-0",
            ),
        ]
    ),
    style={
        "display": "flex",
        "justify-content": "space-between",
        "flex": "1",
        "height": "20px",
    },
    fixed="bottom",
    color="white",
)

# ── Page container ────────────────────────────────────────────────────────────

content = dbc.Container(
    children=[
        dcc.Location(id="url", refresh="callback-nav"),
        dcc.Store(id="store_territory", storage_type="session"),
        page_container,
    ],
    class_name="mt-4",
    style={"padding-top": "40px", "padding-bottom": "120px"},
)

# ── Main layout ───────────────────────────────────────────────────────────────

app.layout = html.Div([navbar, content, footer])
