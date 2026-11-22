"""Gunicorn configuration shim for Render deployments.

Render defaults Python Web Services to `gunicorn app:app`.
Since CropShield AI is a Streamlit application, this config shim intercepts
and transforms the process into a Streamlit server binding to the port
dynamically allocated by Render via $PORT.
"""

import os
import sys

port = os.environ.get("PORT", "8501")

os.execv(
    sys.executable,
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "app.py",
        "--server.port",
        port,
        "--server.address",
        "0.0.0.0",
        "--server.headless",
        "true",
        "--server.enableCORS",
        "false",
        "--server.enableXsrfProtection",
        "false",
    ],
)
