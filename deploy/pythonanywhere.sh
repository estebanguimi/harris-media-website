#!/bin/bash
# Installs (or updates) the HMG panel on PythonAnywhere. Run it from a PythonAnywhere "Bash console".
set -e
cd "$(dirname "$0")/.."
REPO="$(pwd)"
USER_NAME="$(whoami)"
VENV="$HOME/.virtualenvs/hmg"
WSGI="/var/www/${USER_NAME}_pythonanywhere_com_wsgi.py"

echo "1/4  Downloading the latest version of the repository..."
git pull --ff-only -q || true

echo "2/4  Installing requirements (1-2 minutes the first time)..."
[ -d "$VENV" ] || python3.11 -m venv "$VENV"
"$VENV/bin/pip" install -q --disable-pip-version-check -r requirements.txt

echo "3/4  Preparing the content and the website..."
HMG_PYTHON="$VENV/bin/python" "$VENV/bin/python" -c "import app; app.first_run()"

echo "4/4  Connecting the web app..."
if [ ! -f "$WSGI" ]; then
  echo ""
  echo "  ONE STEP MISSING: first create the web app in the \"Web\" tab"
  echo "  (Add a new web app → Next → Manual configuration → Python 3.11 → Next)"
  echo "  and then paste the same command again."
  exit 1
fi
SITE=$(ls -d "$VENV"/lib/python3*/site-packages | head -1)
cat > "$WSGI" <<PY
import os, sys
sys.path.insert(0, "$SITE")
sys.path.insert(0, "$REPO")
os.environ["HMG_PYTHON"] = "$VENV/bin/python"
from wsgi import application
PY
touch "$WSGI"
echo ""
echo "  Done! Go to the \"Web\" tab and press the green \"Reload\" button."
echo "  Website: https://${USER_NAME}.pythonanywhere.com/"
echo "  Panel: https://${USER_NAME}.pythonanywhere.com/admin"
