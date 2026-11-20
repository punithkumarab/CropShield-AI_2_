"""Tests for batch image processing and batch scan telemetry logging."""

from __future__ import annotations

import io
import numpy as np
from PIL import Image
import pytest

from src.cropshield.batch import process_batch_images
from src.cropshield import history


class DummyFile:
    def __init__(self, name: str, image: Image.Image):
        self.name = name
        buf = io.BytesIO()
        image.save(buf, format="PNG")
        buf.seek(0)
        self._bytes = buf.getvalue()

    def read(self) -> bytes:
        return self._bytes


class DummyModel:
    def __init__(self, labels: list[str]):
        self.labels = labels
        self.output_shape = (None, len(labels))
        self.input_shape = (None, 224, 224, 3)

    def predict(self, batch_tensor, verbose=0):
        # Return deterministic probabilities matching number of samples
        batch_size = len(batch_tensor)
        num_classes = len(self.labels)
        probs = np.zeros((batch_size, num_classes), dtype=np.float32)
        probs[:, 0] = 0.85
        probs[:, 1:] = 0.15 / max(1, num_classes - 1)
        return probs


def test_batch_process_empty_input():
    result = process_batch_images([], model=None, labels=["Tomato___healthy"])
    assert result["total"] == 0
    assert result["healthy"] == 0
    assert result["diseased"] == 0
    assert result["summary_df"].empty


def test_batch_process_sequential_inference():
    labels = ["Tomato___Early_blight", "Tomato___healthy"]
    model = DummyModel(labels)

    # Create 3 synthetic green leaf images
    img1 = Image.new("RGB", (224, 224), color=(40, 160, 40))
    img2 = Image.new("RGB", (224, 224), color=(30, 140, 30))
    files = [DummyFile("leaf_1.png", img1), DummyFile("leaf_2.png", img2)]

    res = process_batch_images(files, model=model, labels=labels)
    assert res["total"] == 2
    assert res["diseased"] == 2  # class 0 is Early_blight
    assert len(res["results"]) == 2
    assert not res["summary_df"].empty
    assert "filename" in res["summary_df"].columns
    assert "predicted_class" in res["summary_df"].columns


def test_batch_scan_history_logging(tmp_path, monkeypatch):
    monkeypatch.setattr(history, "DB_PATH", tmp_path / "batch_test.db")
    scan_id = history.log_batch_scan(
        batch_name="Morning Field Surveillance",
        total_images=10,
        healthy_count=7,
        diseased_count=3,
        results=[{"file": "img1.png", "class": "Tomato___healthy"}],
    )
    assert scan_id > 0

    scans = history.list_batch_scans(limit=10)
    assert len(scans) == 1
    assert scans[0]["batch_name"] == "Morning Field Surveillance"
    assert scans[0]["healthy_count"] == 7
    assert scans[0]["diseased_count"] == 3
    assert len(scans[0]["results"]) == 1
