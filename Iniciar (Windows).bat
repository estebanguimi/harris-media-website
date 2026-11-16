@echo off
title Panel HMG
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo  Falta Python. Instalalo desde https://www.python.org/downloads/
  echo  IMPORTANTE: en el instalador marca la casilla "Add Python to PATH".
  echo  Despues vuelve a abrir este archivo.
  echo.
  pause
  exit /b
)
if not exist .venv (
  echo Preparando el panel por primera vez, espera un momento...
  python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -q --disable-pip-version-check -r requirements.txt
set HMG_ABRIR=1
set PYTHONUTF8=1
python app.py
pause
