import os
from pathlib import Path
import tempfile

# Ensure KERAS_HOME points to a local or temp directory before any test loads TensorFlow
if "KERAS_HOME" not in os.environ:
    _keras_path = Path(__file__).resolve().parents[1] / ".keras"
    try:
        _keras_path.mkdir(parents=True, exist_ok=True)
        os.environ["KERAS_HOME"] = str(_keras_path)
    except OSError:
        os.environ["KERAS_HOME"] = os.path.join(tempfile.gettempdir(), ".keras")
