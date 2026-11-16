@echo off
title HMG Panel
cd /d "%~dp0"
where python >nul 2>nul
if errorlevel 1 (
  echo.
  echo  Python is missing. Install it from https://www.python.org/downloads/
  echo  IMPORTANT: in the installer, tick the "Add Python to PATH" box.
  echo  Then open this file again.
  echo.
  pause
  exit /b
)
if not exist .venv (
  echo Setting up the panel for the first time, please wait...
  python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -q --disable-pip-version-check -r requirements.txt
set HMG_OPEN=1
set PYTHONUTF8=1
python app.py
pause
