# content.py — Cesvi Indice Infanzia

from index import app
from dash import dcc, html, page_container
import dash_bootstrap_components as dbc

from layout.callbacks import (
    render_data,
    navigation,
    render_scorecards,
)
from configuration import BRAND_LINK, CREDITS_LINK, TITLE

# ── Navbar ────────────────────────────────────────────────────────────────────

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", active="exact", href="/")),
        dbc.NavItem(dbc.NavLink("Schede regionali", active="exact", href="/scorecards")),
        dbc.NavItem(dbc.NavLink("Dati", active="exact", href="/data")),
        dbc.NavItem(dbc.NavLink("Metodologia", active="exact", href="/methodology")),
    ],
    brand=html.Span([
        html.Img(src="assets/logo.png", height="30px",
                 style={"marginRight": "8px"}),
        TITLE,
    ]),
    brand_href="/",
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
