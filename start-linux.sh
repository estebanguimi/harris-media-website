#!/bin/bash
cd "$(dirname "$0")"
if ! command -v python3 >/dev/null 2>&1; then
  echo ""; echo "  Python is missing. Install it from https://www.python.org/downloads/ and open this file again."; echo ""
  read -n 1 -s -r -p "Press any key to close"; exit 1
fi
if [ ! -d .venv ]; then echo "Setting up the panel for the first time, please wait..."; python3 -m venv .venv; fi
source .venv/bin/activate
python -m pip install -q --disable-pip-version-check -r requirements.txt
HMG_OPEN=1 PYTHONUTF8=1 python app.py
