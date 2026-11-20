"""CropShield AI package."""

import os
from pathlib import Path
import tempfile

# Ensure KERAS_HOME points to a writable local directory before tensorflow is loaded
if "KERAS_HOME" not in os.environ:
    _keras_dir = Path(__file__).resolve().parents[1] / ".keras"
    try:
        _keras_dir.mkdir(parents=True, exist_ok=True)
        os.environ["KERAS_HOME"] = str(_keras_dir)
    except OSError:
        os.environ["KERAS_HOME"] = os.path.join(tempfile.gettempdir(), ".keras")

__all__ = [
    "config",
    "dataset",
    "preprocessing",
    "model",
    "train",
    "evaluate",
    "predict",
    "explainability",
    "history",
]
