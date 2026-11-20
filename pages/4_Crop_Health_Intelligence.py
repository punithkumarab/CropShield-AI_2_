"""Crop Health Intelligence - CropShield AI 2.0 Comparative Analytics & Trajectory."""

from __future__ import annotations

import io
import numpy as np
from PIL import Image
import streamlit as st

from src.cropshield.config import LABELS_PATH, MODEL_PATH, MODELS_DIR, TFLITE_MODEL_PATH
from src.cropshield.footer import render_about_footer
from src.cropshield.image_quality import assess_image_quality
from src.cropshield.model import load_labels, load_model, load_tflite_model
from src.cropshield.predict import predict_image_array
from src.cropshield.translations import translate
from src.cropshield.trust import assess_trust
from src.cropshield.ui import (
    get_selected_language,
    inject_theme,
    render_badge,
    render_card_end,
    render_card_start,
    render_page_header,
)

try:
    st.set_page_config(page_title="Crop Health Intelligence - CropShield AI 2.0", page_icon="🔬", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("crop_health_intel", language),
    subtitle="Comparative leaf diagnosis, multi-temporal symptom progression tracking, and health trajectory delta.",
    tag="Diagnostic Suite",
)

@st.cache_resource
def get_model():
    candidates = (MODEL_PATH, MODELS_DIR / "cropshield_model.keras", MODELS_DIR / "cropshield_model.h5")
    for path in candidates:
        if path.is_file():
            m = load_model(path)
            if m is not None:
                return m, path.name
    if TFLITE_MODEL_PATH.is_file():
        m = load_tflite_model(TFLITE_MODEL_PATH)
        if m is not None:
            return m, TFLITE_MODEL_PATH.name
    return None, None

model, model_name = get_model()
labels = load_labels(LABELS_PATH) if LABELS_PATH.is_file() else []

render_card_start("Dual Scan Comparative Input", badge_text="Baseline vs Follow-up", badge_variant="emerald")
st.write("Upload two leaf images to analyze diagnostic differences, monitor treatment recovery, or evaluate adjacent plant health.")

col_a, col_b = st.columns(2)
with col_a:
    file_a = st.file_uploader("Upload Scan A (e.g., Baseline / Day 0):", type=["jpg", "jpeg", "png", "webp"], key="scan_a")
with col_b:
    file_b = st.file_uploader("Upload Scan B (e.g., Follow-up / Day 7):", type=["jpg", "jpeg", "png", "webp"], key="scan_b")
render_card_end()

if file_a and file_b and model and labels:
    img_a = Image.open(file_a).convert("RGB")
    img_b = Image.open(file_b).convert("RGB")
    
    # Assess Quality & Run Inference
    qa_a = assess_image_quality(img_a)
    qa_b = assess_image_quality(img_b)
    
    pred_a = predict_image_array(np.asarray(img_a), labels, model, confidence_threshold=0.70)
    pred_b = predict_image_array(np.asarray(img_b), labels, model, confidence_threshold=0.70)
    
    trust_a = assess_trust(float(pred_a.get("confidence", 0.0)), float(pred_a.get("top_prediction_margin", 0.0)), qa_a, 0.70)
    trust_b = assess_trust(float(pred_b.get("confidence", 0.0)), float(pred_b.get("top_prediction_margin", 0.0)), qa_b, 0.70)
    
    # ---------------------------------------------------------
    # Visual Side-by-Side Display
    # ---------------------------------------------------------
    c_img1, c_img2 = st.columns(2)
    with c_img1:
        render_card_start("Scan A (Baseline)", badge_text=file_a.name, badge_variant="neutral")
        st.image(img_a, use_container_width=True)
        class_a = pred_a.get("predicted_class", "Unknown").replace("___", " - ").replace("_", " ")
        conf_a = float(pred_a.get("confidence", 0.0)) * 100
        st.markdown(f"**Diagnosis:** `{class_a}`")
        st.markdown(f"**Confidence:** `{conf_a:.1f}%` | **Trust:** `{trust_a.get('level')}`")
        render_card_end()
        
    with c_img2:
        render_card_start("Scan B (Follow-up)", badge_text=file_b.name, badge_variant="neutral")
        st.image(img_b, use_container_width=True)
        class_b = pred_b.get("predicted_class", "Unknown").replace("___", " - ").replace("_", " ")
        conf_b = float(pred_b.get("confidence", 0.0)) * 100
        st.markdown(f"**Diagnosis:** `{class_b}`")
        st.markdown(f"**Confidence:** `{conf_b:.1f}%` | **Trust:** `{trust_b.get('level')}`")
        render_card_end()

    # ---------------------------------------------------------
    # Trajectory & Comparative Analysis
    # ---------------------------------------------------------
    render_card_start("Diagnostic Trajectory & Delta Assessment", badge_text="Comparison", badge_variant="forest")
    healthy_a = "healthy" in pred_a.get("predicted_class", "").lower()
    healthy_b = "healthy" in pred_b.get("predicted_class", "").lower()
    
    if not healthy_a and healthy_b:
        trajectory = "🌱 Positive Recovery Observed"
        traj_variant = "emerald"
        traj_detail = "Scan A showed pathology while Scan B shows healthy leaf tissue, indicating successful treatment or recovery."
    elif healthy_a and not healthy_b:
        trajectory = "⚠️ New Pathology Developed"
        traj_variant = "crimson"
        traj_detail = "Scan A was healthy, but Scan B displays signs of disease. Initiate immediate field scouting."
    elif not healthy_a and not healthy_b:
        if pred_a.get("predicted_class") == pred_b.get("predicted_class"):
            trajectory = "🔄 Persistent Disease Condition"
            traj_variant = "amber"
            traj_detail = f"Both scans indicate {class_a}. Review management efficacy and check for treatment resistance."
        else:
            trajectory = "🔀 Divergent Symptoms Detected"
            traj_variant = "amber"
            traj_detail = f"Scan A diagnosed as {class_a}, while Scan B diagnosed as {class_b}. Possible secondary infection."
    else:
        trajectory = "✓ Consistently Healthy"
        traj_variant = "forest"
        traj_detail = "Both leaves exhibit healthy foliar characteristics."

    st.markdown(f"### {render_badge(trajectory, traj_variant)}", unsafe_allow_html=True)
    st.write(traj_detail)
    
    st.divider()
    comp_col1, comp_col2, comp_col3 = st.columns(3)
    comp_col1.metric("Focus (Sharpness) Delta", f"{qa_b.blur_score - qa_a.blur_score:+.0f}", f"A: {qa_a.blur_score:.0f} vs B: {qa_b.blur_score:.0f}")
    comp_col2.metric("Brightness Delta", f"{qa_b.brightness - qa_a.brightness:+.0f}", f"A: {qa_a.brightness:.0f} vs B: {qa_b.brightness:.0f}")
    comp_col3.metric("Leaf Coverage Delta", f"{(qa_b.leaf_coverage_fraction - qa_a.leaf_coverage_fraction)*100:+.1f}%", f"A: {qa_a.leaf_coverage_fraction*100:.0f}% vs B: {qa_b.leaf_coverage_fraction*100:.0f}%")
    render_card_end()

elif not (file_a and file_b):
    st.info("Please upload both Scan A and Scan B above to perform comparative diagnosis.")

render_about_footer()
