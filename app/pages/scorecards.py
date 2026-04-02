# scorecards.py — pagina Schede regionali

from dash import register_page
from configuration import TITLE

register_page(__name__, name=TITLE, path="/scorecards")

from layout.layout_scorecards import scorecard_layout

layout = scorecard_layout
