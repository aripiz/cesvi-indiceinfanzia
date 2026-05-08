# report.py — pagina Edizioni/Report

from dash import register_page
from configuration import TITLE

register_page(__name__, name=TITLE, path="/report")

from layout.layout_report import report_layout

layout = report_layout
