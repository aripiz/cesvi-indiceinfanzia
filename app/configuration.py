# configuration.py — Cesvi Indice Infanzia

# App
TITLE = "Indice regionale sul maltrattamento e la cura all'infanzia in Italia"
BRAND_LINK = "https://www.cesvi.org/"
CREDITS_LINK = "https://github.com/aripiz"

# Theme (Bootswatch)
TEMPLATE = "minty"
TEMPLATE_CSS = f"https://cdn.jsdelivr.net/npm/bootswatch@5.3.3/dist/{TEMPLATE}/bootstrap.min.css"
FIGURE_TEMPLATE = TEMPLATE.lower()
DBC_CSS = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

# Brand colors Cesvi (arancione = colore principale)
BRAND_COLOR = "#ea7a2d"        # arancione Cesvi

# Palette divergente per z-score: verde (sotto media) → bianco → arancione (sopra media)
DIVERGING_COLORS = [
    "#1B7A70",   # verde scuro  (z ≤ -1.5)
    "#2DA89B",   # verde Cesvi  (z ≈ -1)
    "#8FCFC9",   # verde chiaro (z ≈ -0.5)
    "#F5F5F5",   # bianco       (z ≈ 0)
    "#F3D08E",   # giallo chiaro (z ≈ 0.5)
    "#E7AD49",   # giallo Cesvi  (z ≈ 1)
    "#ea7a2d",   # arancione Cesvi (z ≥ 1.5)
]

# Palette qualitativa per serie multiple
SEQUENCE_COLOR = [
    "#ea7a2d",   # arancione Cesvi (principale)
    "#2DA89B",   # verde Cesvi
    "#E7AD49",   # giallo Cesvi
    "#3c3c3c",   # grigio scuro
    "#a64d79",   # viola
    "#439acf",   # azzurro
    "#2e8b57",   # verde foresta
    "#ff6f00",   # arancione vivido
    "#41c072",   # verde chiaro
    "#1B7A70",   # verde scuro
]

# Classificazione z-score (per etichette e colori mappa)
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
    "Molto sotto media":         "#1B7A70",
    "Sotto media":               "#2DA89B",
    "Leggermente sotto media":   "#8FCFC9",
    "Leggermente sopra media":   "#F3D08E",
    "Sopra media":               "#E7AD49",
    "Molto sopra media":         "#ea7a2d",
}

# Colori per ranking
RANK_COLOR_SCALE = [
    [0.0, "#2DA89B"],    # teal (rank peggiore)
    [0.5, "#E7AD49"],
    [1.0, "#ea7a2d"],    # arancione Cesvi (rank migliore)
]

# Map
LAND_COLOR = "#3B3B3B"
OCEAN_COLOR = "#F2F2F2"
GEO_KEY = "properties.reg_istat_code_num"

# Indici e dimensioni
INDEX_KEY = "indice_totale"

# Indicatori principali (ordinati per visualizzazione)
SUMMARY_INDICATORS = [
    "indice_totale",
    "indice_rischio",
    "indice_prevenzione",
    "cap_cura",
    "cap_vita_sana",
    "cap_vita_sicura",
    "cap_conoscenza_sapere",
    "cap_lavorare",
    "cap_accedere_risorse",
]

# Componenti di dettaglio (15 sotto-indici)
SUB_INDICATORS = [
    "cap_cura_rischio",
    "cap_cura_serv_maltrattanti",
    "cap_cura_serv_infanzia",
    "cap_vita_sana_rischio",
    "cap_vita_sana_sintomi",
    "cap_vita_sana_serv_maltrattanti",
    "cap_vita_sana_serv_infanzia",
    "cap_vita_sicura_rischio",
    "cap_vita_sicura_servizi",
    "cap_conoscenza_rischio",
    "cap_conoscenza_servizi",
    "cap_lavorare_rischio",
    "cap_lavorare_servizi",
    "cap_accedere_risorse_rischio",
    "cap_accedere_risorse_servizi",
]

# Etichette leggibili per ogni indicatore
INDICATOR_LABELS = {
    "indice_totale":                   "Indice totale",
    "indice_rischio":                  "Sottoindice rischio",
    "indice_prevenzione":              "Sottoindice prevenzione",
    "cap_cura":                        "Cura",
    "cap_vita_sana":                   "Vita sana",
    "cap_vita_sicura":                 "Vita sicura",
    "cap_conoscenza_sapere":           "Conoscenza e sapere",
    "cap_lavorare":                    "Lavorare",
    "cap_accedere_risorse":            "Accedere alle risorse",
    "cap_cura_rischio":                "Cura — fattori rischio",
    "cap_cura_serv_maltrattanti":      "Cura — servizi maltrattanti",
    "cap_cura_serv_infanzia":          "Cura — servizi infanzia",
    "cap_vita_sana_rischio":           "Vita sana — fattori rischio",
    "cap_vita_sana_sintomi":           "Vita sana — sintomi vulnerabilità",
    "cap_vita_sana_serv_maltrattanti": "Vita sana — servizi maltrattanti",
    "cap_vita_sana_serv_infanzia":     "Vita sana — servizi infanzia",
    "cap_vita_sicura_rischio":         "Vita sicura — fattori rischio",
    "cap_vita_sicura_servizi":         "Vita sicura — servizi",
    "cap_conoscenza_rischio":          "Conoscenza — fattori rischio",
    "cap_conoscenza_servizi":          "Conoscenza — servizi",
    "cap_lavorare_rischio":            "Lavorare — fattori rischio",
    "cap_lavorare_servizi":            "Lavorare — servizi",
    "cap_accedere_risorse_rischio":    "Accedere risorse — fattori rischio",
    "cap_accedere_risorse_servizi":    "Accedere risorse — servizi",
}

# Le 6 capacità per il radar/profilo
CAPACITY_DIMS = {
    "cap_cura":               "Cura",
    "cap_vita_sana":          "Vita sana",
    "cap_vita_sicura":        "Vita sicura",
    "cap_conoscenza_sapere":  "Conoscenza e sapere",
    "cap_lavorare":           "Lavorare",
    "cap_accedere_risorse":   "Accedere alle risorse",
}

YEARS_AVAILABLE = [2018, 2019, 2020, 2021, 2022, 2024]
YEAR_DEFAULT = 2024

# Files
DATA_FILE = "../data/cesvi-indiceinfanzia_long.csv"
GEO_FILE = "../data/limits_IT_regions.geojson"
