# news.py — pagina Notizie

from dash import register_page
from configuration import TITLE

register_page(__name__, name=TITLE, path="/news")

from layout.layout_news import news_layout

layout = news_layout
