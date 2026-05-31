# Cesvi — Regional Index on Child Maltreatment and Care in Italy

Interactive dashboard for the **Cesvi Indice regionale sul maltrattamento e la cura all'infanzia in Italia** — an annual index that measures how socio-economic context and local services affect child well-being across Italian regions.

Live: **http://80.211.24.207/**

---

## Tech stack

- [Dash](https://dash.plotly.com/) (multi-page) + [Plotly](https://plotly.com/python/)
- [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/) — Bootswatch Minty theme
- GeoPandas for regional map rendering
- Gunicorn + gevent workers in production
- Docker for deployment

---

## Project structure

```
app/                  # Application source
  app.py              # Dash app entry point
  configuration.py    # Constants (brand colours, years, dimensions)
  content.py          # Navbar and footer
  index.py            # Report index and server-level routes
  utilis.py           # Shared data loading helpers
  layout/             # Per-page layout modules
    callbacks/        # Dash callbacks (rendering, downloads, navigation)
  pages/              # Dash pages (registered with use_pages)
  assets/             # Static files (CSS, JS)
data/                 # Source data
  cesvi-indiceinfanzia_data.csv
  cesvi-indiceinfanzia_metadata.csv
  italy_regions_low.json
  limits_IT_regions.geojson
Dockerfile
docker-compose.yml
```

---

## Run locally

```bash
# From the project root
pip install -r app/requirements.txt

cd app
python app.py          # runs on http://localhost:8051
```

Or with Docker:

```bash
docker compose up --build
# app available on port 8080
```

---

## Data

The dataset covers all 20 Italian regions across 7 editions (2018–2025). Each row combines:

- **Risk factors** (children and adults) — socio-economic indicators related to family vulnerability
- **Services** (children and adults) — availability and quality of social and welfare services
- **Capacity dimensions** — 6 thematic aggregations used to build the composite index

Source files are in `data/`. The build script `data/build_dataset.py` documents how raw tables are processed.

---

---

# Cesvi — Indice regionale sul maltrattamento e la cura all'infanzia in Italia

Dashboard interattiva per l'**Indice regionale CESVI sul maltrattamento e la cura all'infanzia** — un indice annuale che misura come il contesto socio-economico e i servizi locali influenzano il benessere dei bambini nelle regioni italiane.

Online: **http://80.211.24.207/**

---

## Stack tecnologico

- [Dash](https://dash.plotly.com/) (multi-page) + [Plotly](https://plotly.com/python/)
- [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/) — tema Bootswatch Minty
- GeoPandas per la mappa regionale
- Gunicorn + worker gevent in produzione
- Docker per il deployment

---

## Struttura del progetto

```
app/                  # Sorgente applicazione
  app.py              # Entry point Dash
  configuration.py    # Costanti (colori brand, anni, dimensioni)
  content.py          # Navbar e footer
  index.py            # Indice report e route server
  utilis.py           # Helper condivisi per il caricamento dati
  layout/             # Moduli layout per pagina
    callbacks/        # Callback Dash (rendering, download, navigazione)
  pages/              # Pagine Dash (registrate con use_pages)
  assets/             # File statici (CSS, JS)
data/                 # Dati sorgente
  cesvi-indiceinfanzia_data.csv
  cesvi-indiceinfanzia_metadata.csv
  italy_regions_low.json
  limits_IT_regions.geojson
Dockerfile
docker-compose.yml
```

---

## Esecuzione locale

```bash
# Dalla root del progetto
pip install -r app/requirements.txt

cd app
python app.py          # disponibile su http://localhost:8051
```

Con Docker:

```bash
docker compose up --build
# app disponibile sulla porta 8080
```

---

## Dati

Il dataset copre tutte le 20 regioni italiane in 7 edizioni (2018–2025). Ogni riga combina:

- **Fattori di rischio** (bambini e adulti) — indicatori socio-economici legati alla vulnerabilità familiare
- **Servizi** (bambini e adulti) — disponibilità e qualità dei servizi sociali e assistenziali
- **Capacità** — 6 dimensioni tematiche che compongono l'indice aggregato

I file sorgente si trovano in `data/`. Lo script `data/build_dataset.py` documenta l'elaborazione delle tabelle originali.

