# download.py — pagina Download

from dash import register_page
from configuration import TITLE

register_page(__name__, name=TITLE, path="/download")

from layout.layout_download import download_layout

layout = download_layout
