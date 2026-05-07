FROM python:3.11-slim

# Dipendenze di sistema per geopandas/pyogrio
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

COPY app/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY app/ /app/
COPY data/ /data/

WORKDIR /app

EXPOSE 8080

CMD gunicorn app:server --workers 1 --bind 0.0.0.0:8080