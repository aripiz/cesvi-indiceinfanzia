FROM python:3.11-slim

# Dipendenze di sistema per geopandas/pyogrio
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Installa dipendenze Python
COPY app/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copia il codice mantenendo la struttura attesa dai path relativi
# configuration.py usa "../data/..." relativo a /app → i dati vanno in /data
COPY app/ /app/
COPY data/ /data/

WORKDIR /app

EXPOSE 8080

# Railway inietta $PORT; fallback a 8080
CMD gunicorn app:server --workers 1 --bind 0.0.0.0:${PORT:-8080}
