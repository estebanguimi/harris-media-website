"""WSGI entry point for web hosts (PythonAnywhere, gunicorn, uWSGI...).
The web host loads `application` from here; the content and the published site are created on first start."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
os.environ.setdefault('HMG_HTTPS', '1')
os.environ.setdefault('HMG_PROXY', '1')  # web hosts put a reverse proxy in front of the app

from app import app as application, first_run  # noqa: E402

first_run()
