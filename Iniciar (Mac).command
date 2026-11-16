#!/bin/bash
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo ""; echo "  Falta Python. Instálalo desde https://www.python.org/downloads/ y vuelve a abrir este archivo."; echo ""
  read -n 1 -s -r -p "Pulsa una tecla para cerrar"; exit 1
fi
if [ ! -d .venv ]; then echo "Preparando el panel por primera vez, espera un momento..."; python3 -m venv .venv; fi
source .venv/bin/activate
python -m pip install -q --disable-pip-version-check -r requirements.txt
HMG_ABRIR=1 python app.py
