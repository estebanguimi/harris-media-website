#!/bin/bash
# Installs (or updates) the HMG panel on PythonAnywhere. Run it from a PythonAnywhere "Bash console".
set -e
cd "$(dirname "$0")/.."
REPO="$(pwd)"
USER_NAME="$(whoami)"
VENV="$HOME/.virtualenvs/hmg"
WSGI="/var/www/${USER_NAME}_pythonanywhere_com_wsgi.py"

echo "1/4  Descargando la última versión del repositorio..."
git pull --ff-only -q || true

echo "2/4  Instalando lo necesario (tarda 1-2 minutos la primera vez)..."
[ -d "$VENV" ] || python3.11 -m venv "$VENV"
"$VENV/bin/pip" install -q --disable-pip-version-check -r requirements.txt

echo "3/4  Preparando el contenido y la web..."
HMG_PYTHON="$VENV/bin/python" "$VENV/bin/python" -c "import app; app.first_run()"

echo "4/4  Conectando la web app..."
if [ ! -f "$WSGI" ]; then
  echo ""
  echo "  FALTA UN PASO: primero crea la web app en la pestaña «Web»"
  echo "  (Add a new web app → Next → Manual configuration → Python 3.11 → Next)"
  echo "  y luego vuelve a pegar el mismo comando."
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
echo "  ¡Listo! Ve a la pestaña «Web» y pulsa el botón verde «Reload»."
echo "  Web:   https://${USER_NAME}.pythonanywhere.com/"
echo "  Panel: https://${USER_NAME}.pythonanywhere.com/admin"
