"""Batch image inference processor for CropShield AI 2.0."""

from __future__ import annotations

import io
import logging
from typing import Any

import numpy as np
import pandas as pd
from PIL import Image

from .image_quality import assess_image_quality
from .model import load_labels, load_model
from .predict import predict_image_array
from .trust import assess_trust

LOGGER = logging.getLogger(__name__)


def process_batch_images(
    uploaded_files: list[Any],
    model: Any,
    labels: list[str],
    confidence_threshold: float = 0.70,
) -> dict[str, Any]:
    """Process a batch of uploaded leaf images sequentially with memory-safe execution."""
    if not uploaded_files:
        return {"total": 0, "healthy": 0, "diseased": 0, "results": [], "summary_df": pd.DataFrame()}

    results = []
    healthy_count = 0
    diseased_count = 0

    for file in uploaded_files:
        try:
            image_bytes = file.read()
            pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            arr = np.asarray(pil_image)

            # Quality Assessment
            quality = assess_image_quality(pil_image)

            # Inference
            pred_result = predict_image_array(
                image_array=arr,
                labels=labels,
                model=model,
                confidence_threshold=confidence_threshold,
            )

            predicted_class = pred_result.get("predicted_class", "Unknown")
            confidence = float(pred_result.get("confidence", 0.0))
            is_healthy = "healthy" in predicted_class.lower()

            if is_healthy:
                healthy_count += 1
            else:
                diseased_count += 1

            # Trust calculation
            margin = float(pred_result.get("top_prediction_margin", 0.0))
            trust = assess_trust(
                confidence=confidence,
                margin=margin,
                quality=quality,
                validation_threshold=confidence_threshold,
            )

            results.append({
                "filename": file.name,
                "predicted_class": predicted_class,
                "confidence": round(confidence, 4),
                "is_healthy": is_healthy,
                "trust_level": trust.get("level", "Cannot Assess"),
                "blur_score": round(float(quality.blur_score), 1),
                "leaf_coverage": round(float(quality.leaf_coverage_fraction * 100), 1),
                "image_width": pil_image.width,
                "image_height": pil_image.height,
            })

        except Exception as exc:
            LOGGER.warning("Batch processing failed for %s: %s", getattr(file, "name", "unknown"), exc)
            results.append({
                "filename": getattr(file, "name", "unknown"),
                "predicted_class": "Error Processing",
                "confidence": 0.0,
                "is_healthy": False,
                "trust_level": "Cannot Assess",
                "blur_score": 0.0,
                "leaf_coverage": 0.0,
                "image_width": 0,
                "image_height": 0,
            })

    summary_df = pd.DataFrame(results)
    return {
        "total": len(results),
        "healthy": healthy_count,
        "diseased": diseased_count,
        "results": results,
        "summary_df": summary_df,
    }
