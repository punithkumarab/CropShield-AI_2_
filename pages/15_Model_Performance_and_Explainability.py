"""Model Performance and Explainability - CropShield AI 2.0 ML Transparency."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from src.cropshield.config import ARTIFACTS_DIR, MODELS_DIR, REPORTS_DIR
from src.cropshield.footer import render_about_footer
from src.cropshield.model import load_labels
from src.cropshield.performance import get_evaluation_state, load_json_object
from src.cropshield.translations import translate
from src.cropshield.ui import (
    get_selected_language,
    inject_theme,
    render_badge,
    render_card_end,
    render_card_start,
    render_page_header,
)

try:
    st.set_page_config(page_title="Model Performance - CropShield AI 2.0", page_icon="🧠", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("model_performance", language),
    subtitle="Rigorous test-split evaluation, confusion matrix, per-class F1-scores, and Grad-CAM interpretability.",
    tag="Engineering & Governance",
)

model_candidates = [
    MODELS_DIR / name
    for name in (
        "crop_model.keras",
        "crop_model.h5",
        "cropshield_model.keras",
        "cropshield_model.h5",
        "baseline_best.keras",
        "mobilenet_best.keras",
    )
]
evaluation_candidates = [
    REPORTS_DIR / "evaluation_metrics.json",
    ARTIFACTS_DIR / "evaluation_metrics.json",
    MODELS_DIR / "evaluation_results.json",
]

state, metrics_path, evaluation_error = get_evaluation_state(model_candidates, evaluation_candidates)

if state == "not_trained":
    st.warning("No trained CropShield model is available. Please train the model first with `python scripts/train_model.py`.")
elif state == "trained_not_evaluated":
    render_card_start("Evaluation Status: Pending", badge_text="Action Required", badge_variant="amber")
    st.warning("Model artifact is present, but held-out test evaluation has not been completed.")
    st.code("python scripts/evaluate_model.py", language="powershell")
    st.info("Evaluation calculates real test-set performance after training. It does not run automatically on page open.")
    render_card_end()
else:
    try:
        saved = load_json_object(metrics_path)
        stored_models = saved.get("models", {})
        model_name = next(iter(stored_models))
        result = stored_models[model_name]
        
        # ---------------------------------------------------------
        # Executive ML KPI Cards
        # ---------------------------------------------------------
        m1, m2, m3, m4 = st.columns(4)
        acc = float(result.get("accuracy", 0.0)) * 100
        prec = float(result.get("macro_precision", 0.0)) * 100
        rec = float(result.get("macro_recall", 0.0)) * 100
        f1 = float(result.get("macro_f1", 0.0)) * 100
        
        m1.metric("Overall Accuracy", f"{acc:.1f}%")
        m2.metric("Macro Precision", f"{prec:.1f}%")
        m3.metric("Macro Recall", f"{rec:.1f}%")
        m4.metric("Macro F1-Score", f"{f1:.1f}%")
        
        st.write("")
        
        # ---------------------------------------------------------
        # Confusion Matrix Heatmap
        # ---------------------------------------------------------
        matrix = result.get("confusion_matrix")
        classes = result.get("class_names", [])
        clean_classes = [c.replace("___", " - ").replace("_", " ") for c in classes]
        
        if matrix and len(matrix) == len(classes):
            render_card_start("Held-Out Test Confusion Matrix", badge_text="Heatmap", badge_variant="emerald")
            fig_cm = px.imshow(
                matrix,
                x=clean_classes,
                y=clean_classes,
                color_continuous_scale=["#F8F9FA", "#D8F3DC", "#2D6A4F", "#1B4332"],
                labels=dict(x="Predicted Class", y="True Ground Truth Class", color="Count"),
                text_auto=True,
            )
            fig_cm.update_layout(height=450, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig_cm, use_container_width=True)
            render_card_end()
            
        # ---------------------------------------------------------
        # Per-Class Precision, Recall & F1 Table
        # ---------------------------------------------------------
        per_class = result.get("per_class")
        if isinstance(per_class, dict):
            st.write("")
            render_card_start("Per-Class Metric Breakdown", badge_text="Disaggregated", badge_variant="forest")
            pc_rows = []
            for c_name, c_metrics in per_class.items():
                if isinstance(c_metrics, dict):
                    pc_rows.append({
                        "Pathology Class": c_name.replace("___", " - ").replace("_", " "),
                        "Precision": f"{c_metrics.get('precision', 0)*100:.1f}%",
                        "Recall": f"{c_metrics.get('recall', 0)*100:.1f}%",
                        "F1-Score": f"{c_metrics.get('f1-score', 0)*100:.1f}%",
                        "Test Support": int(c_metrics.get("support", 0)),
                    })
            st.dataframe(pd.DataFrame(pc_rows), use_container_width=True, hide_index=True)
            render_card_end()

    except Exception as e:
        st.error(f"Error loading evaluation metrics: {e}")

# ---------------------------------------------------------
# Architecture Comparison Summary
# ---------------------------------------------------------
st.write("")
render_card_start("Deep Learning Architecture & Deployment Strategy", badge_text="MobileNetV2 vs CNN", badge_variant="neutral")
st.markdown(
    """
    CropShield AI 2.0 employs **MobileNetV2 Transfer Learning** as its primary production backbone:
    - **Inverted Residual Blocks & Depthwise Separable Convolutions:** Delivers high representation capacity with only ~2.2M parameters.
    - **Edge & Mobile Optimization:** Fully exportable to 8-bit quantized TensorFlow Lite (`.tflite`) for real-time mobile and edge field devices.
    - **Baseline 4-Layer CNN:** Available as a lightweight benchmark trained from scratch to demonstrate transfer learning accuracy gains.
    """
)
render_card_end()

render_about_footer()
