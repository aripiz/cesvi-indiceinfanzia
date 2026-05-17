# configuration.py — Cesvi Indice Infanzia

# App
TITLE = "Indice regionale sul maltrattamento e la cura all'infanzia in Italia"
BRAND_LINK = "https://www.cesvi.org/"
CREDITS_LINK = "https://github.com/aripiz"

# Theme (Bootswatch)
TEMPLATE = "minty"
TEMPLATE_CSS = f"https://cdn.jsdelivr.net/npm/bootswatch@5.3.8/dist/{TEMPLATE}/bootstrap.min.css"
FIGURE_TEMPLATE = TEMPLATE.lower()
DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Font
FONT_FAMILY = "Raleway"
FONT_URL = "https://fonts.googleapis.com/css2?family=Raleway:wght@400;600;700&display=swap"

# Brand colors Cesvi (dal brandbook ufficiale)
BRAND_COLOR = "#eb6608"            # arancione principale
BRAND_SECONDARY_COLOR = "#94A4A4"  # grigio
BRAND_WHITE = "#FFFFFF"            # bianco

# Logo
LOGO = "assets/logos/logo_h_grey.png"
LOGO_VERTICAL = "assets/logos/logo_v_grey.png"

# Palette divergente per z-score: grigio (sotto media) → bianco (media) → arancione (sopra media)
DIVERGING_COLORS = [
    "#3d4646",   # grigio scuro  (z ≤ -1.5)
    "#94A4A4",   # grigio Cesvi  (z ≈ -1.0)
    "#D0DADB",   # grigio chiaro (z ≈ -0.5)
    "#F5F5F5",   # bianco        (z =  0)
    "#F7CFA0",   # arancione chiaro (z ≈ +0.5)
    "#F39840",   # arancione medio  (z ≈ +1.0)
    "#eb6608",   # arancione Cesvi  (z ≥ +1.5)
]

# Palette qualitativa per serie multiple
# Brand primari + varianti interpolate, no verde
SEQUENCE_COLOR = [
    "#eb6608",   # arancione Cesvi (principale)
    "#94A4A4",   # grigio Cesvi
    "#F39840",   # arancione medio
    "#D0DADB",   # grigio chiaro
    "#F7CFA0",   # arancione chiaro
    "#3d4646",   # grigio scuro
    "#439acf",   # azzurro (accento neutro)
    "#a64d79",   # viola (accento neutro)
    "#e8c13a",   # giallo (accento neutro)
    "#3c3c3c",   # antracite
]

# Classificazione z-score
ZSCORE_BINS = [-10, -1.0, -0.5, 0.0, 0.5, 1.0, 10]
ZSCORE_LABELS = [
    "Molto sotto media",
    "Sotto media",
    "Leggermente sotto media",
    "Leggermente sopra media",
    "Sopra media",
    "Molto sopra media",
]
ZSCORE_TIER_COLORS = {
    "Molto sotto media":          "#3d4646",
    "Sotto media":                "#94A4A4",
    "Leggermente sotto media":    "#D0DADB",
    "Leggermente sopra media":    "#F7CFA0",
    "Sopra media":                "#F39840",
    "Molto sopra media":          "#eb6608",
}

# Scala continua per ranking: grigio → arancione
RANK_COLOR_SCALE = [
    [0.0, "#94A4A4"],   # grigio Cesvi (rank peggiore)
    [0.5, "#F39840"],   # arancione medio
    [1.0, "#eb6608"],   # arancione Cesvi (rank migliore)
]

# Map
LAND_COLOR  = "#3B3B3B"
OCEAN_COLOR = "#F2F2F2"
GEO_KEY     = "properties.reg_name"

# Files
DATA_FILE     = "../data/cesvi-indiceinfanzia_data.csv"
GEO_FILE      = "../data/IT_regions.parquet"
METADATA_FILE = "../data/cesvi-indiceinfanzia_metadata.csv"
REPORTS_FILE  = "../data/cesvi-indiceinfanzia_reports.csv"
REPORTS_DIR   = "../data/reports"

# Years
YEARS = [2018, 2019, 2020, 2021, 2022, 2024, 2026]
YEARS_AVAILABLE = YEARS  # alias
YEAR_DEFAULT = 2026
YEAR_MIN = YEARS[0]
YEAR_MAX = YEARS[-1]

# Etichette indici aggregati (chiave CSV → etichetta leggibile)
INDEX_LABELS = {
    "totale":  "Totale",
    "rischio": "Fattori di rischio",
    "servizi": "Servizi",
}

# Capacità — chiave CSV → etichetta breve
CAPACITY_DIMS = {
    "accedere_risorse":  "Accedere alle Risorse",
    "conoscenza_sapere": "Conoscenza e Sapere",
    "cura":              "Cura",
    "lavorare":          "Lavorare",
    "vita_sana":         "Vita Sana",
    "vita_sicura":       "Vita Sicura",
}

# Ordine di visualizzazione delle capacità nei grafici (modifica qui per cambiare l'ordine)
CAPACITY_ORDER = [
    "accedere_risorse",
    "conoscenza_sapere",
    "cura",
    "lavorare",
    "vita_sana",
    "vita_sicura",
]