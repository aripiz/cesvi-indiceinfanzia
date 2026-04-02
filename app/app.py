# app.py — Cesvi Indice Infanzia

from content import app

server = app.server

if __name__ == "__main__":
    app.run(debug=True, port=8051)
