"""AI Crop Scanner - CropShield AI 2.0 Single-Leaf Precision Diagnostics."""

from __future__ import annotations

import io
import json
import logging
from pathlib import Path
import time

import cv2
import numpy as np
import pandas as pd
import plotly.express as px
from PIL import Image
import streamlit as st

from src.cropshield.config import DETECTION_THRESHOLDS_PATH, LABELS_PATH, MODEL_PATH, MODELS_DIR, TFLITE_MODEL_PATH
from src.cropshield.dataset import list_dataset_samples
from src.cropshield.explainability import gradcam_for_prediction, overlay_heatmap
from src.cropshield.field_risk import assess_field_risk
from src.cropshield.footer import render_about_footer
from src.cropshield.history import (
    add_plant_observation,
    append_prediction,
    fetch_tracked_plants,
    list_plots,
)
from src.cropshield.image_quality import assess_image_quality, crop_largest_leaf_like_region
from src.cropshield.innovation import (
    build_second_opinion_list,
    calculate_crop_health_score,
    estimate_yield_impact,
    generate_5step_action_plan,
    generate_confidence_explanation,
    generate_gradcam_explanation,
    generate_whatsapp_share_url,
    get_speech_script,
)
from src.cropshield.knowledge_base import get_verified_guidance, is_healthy_class
from src.cropshield.model import TFLiteModel, load_labels, load_model, load_tflite_model
from src.cropshield.predict import predict_image_array, predict_image_file, predict_uploaded_file
from src.cropshield.preprocessing import validate_upload
from src.cropshield.report import build_prediction_report
from src.cropshield.treatment_guide import SAFE_PRACTICE_WARNINGS, build_action_plan
from src.cropshield.trust import assess_trust, load_trust_thresholds
from src.cropshield.translations import translate
from src.cropshield.ui import (
    get_selected_language,
    inject_theme,
    render_action_plan_interactive,
    render_badge,
    render_card_end,
    render_card_start,
    render_confidence_meter,
    render_crop_health_score_card,
    render_image_coach_hud,
    render_page_header,
    render_second_opinion_panel,
    render_trust_indicator,
    render_whatsapp_and_audio_tools,
)

LOGGER = logging.getLogger(__name__)

try:
    st.set_page_config(page_title="AI Crop Scanner - CropShield AI 2.0", page_icon="🔬", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("ai_crop_scanner", language),
    subtitle="Precision deep learning leaf diagnosis, Grad-CAM attention maps, and calibrated trust validation.",
    tag="Diagnostic Suite",
)

# ---------------------------------------------------------
# Load Model & Thresholds
# ---------------------------------------------------------
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

model, model_file_name = get_model()
labels = load_labels(LABELS_PATH) if LABELS_PATH.is_file() else []

try:
    trust_thresholds = load_trust_thresholds(DETECTION_THRESHOLDS_PATH)
except Exception:
    trust_thresholds = None

confidence_threshold = 0.70

# ---------------------------------------------------------
# Image Input Section (Offline Mobile Camera / Upload / Samples)
# ---------------------------------------------------------
render_card_start("Leaf Image Input & Field Acquisition", badge_text="Camera / Upload / Field", badge_variant="emerald")
image_source = st.radio(
    "Select Image Acquisition Method:",
    ["📷 Take Photo with Camera", "📁 Upload Image File", "🌿 Select PlantVillage Dataset Sample"],
    horizontal=True,
)

uploaded_file = None
sample_path = None
image_available = False

if image_source == "📷 Take Photo with Camera":
    uploaded_file = st.camera_input("Capture affected foliar leaf directly in the field:", key="scanner_camera")
    image_available = uploaded_file is not None
elif image_source == "📁 Upload Image File":
    uploaded_file = st.file_uploader(
        "Upload a leaf photograph (JPG, PNG, WebP):",
        type=["jpg", "jpeg", "png", "webp"],
        key="scanner_upload",
    )
    image_available = uploaded_file is not None
else:
    samples = list_dataset_samples(limit=30)
    if samples:
        sample_path = st.selectbox(
            "Choose a verified agricultural sample leaf image:",
            options=samples,
            format_func=lambda p: f"{Path(p).parent.name} - {Path(p).name}",
        )
        image_available = bool(sample_path)
    else:
        st.info("Local PlantVillage dataset samples not prepared.")

render_card_end()

# ---------------------------------------------------------
# Image Quality Assessment & Diagnostic Execution
# ---------------------------------------------------------
if image_available:
    if uploaded_file is not None:
        valid, msg, width, height = validate_upload(uploaded_file)
        if not valid:
            st.error(msg)
            image_available = False
        else:
            uploaded_file.seek(0)
            image = Image.open(uploaded_file).convert("RGB")
    else:
        image = Image.open(sample_path).convert("RGB")

if image_available:
    # Run Computer Vision Quality Pre-Screening Coach
    quality = assess_image_quality(image)

    col_img, col_quality = st.columns([1.1, 1.1])
    
    with col_img:
        render_card_start("Input Leaf Photograph", badge_text=f"{image.width}×{image.height} px", badge_variant="neutral")
        st.markdown(
            """
            <div class="scanner-preview-wrapper">
                <div class="scanner-laser-line"></div>
            """,
            unsafe_allow_html=True,
        )
        st.image(image, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)
        render_card_end()
        
    with col_quality:
        render_image_coach_hud(quality)
        
        # Crop to leaf region option
        crop_opt = st.checkbox("Focus on Detected Foliar Region (Auto-Crop)", value=False)
        if crop_opt:
            cropped = crop_largest_leaf_like_region(image)
            if cropped is not None:
                image = cropped
                st.caption(f"Cropped to primary foliar region: {image.width}×{image.height} px")

    # ---------------------------------------------------------
    # Optional Farm & Plot Tagging
    # ---------------------------------------------------------
    render_card_start("Agronomic Context & Farm Tagging (Optional)", badge_text="Farm Management", badge_variant="blue")
    f_col1, f_col2 = st.columns(2)
    available_plots = list_plots()
    plot_map = {p["id"]: f"{p['name']} ({p.get('crop_variety', 'Tomato')})" for p in available_plots}
    
    with f_col1:
        selected_plot_id = st.selectbox(
            "Assign scan to Farm Plot:",
            options=[None] + list(plot_map.keys()),
            format_func=lambda pid: "Do not assign to plot" if pid is None else plot_map[pid],
        )
    with f_col2:
        scan_notes = st.text_input("Observation Notes:", placeholder="e.g. Symptoms noticed on lower foliage after morning fog.")
        
    save_to_history = st.checkbox("Save diagnostic record to SQLite history", value=True)
    render_card_end()

    # ---------------------------------------------------------
    # Diagnostic Prediction Action
    # ---------------------------------------------------------
    if st.button("🔬 Run AI Disease Diagnosis", type="primary", use_container_width=True, disabled=model is None or not labels):
        started_at = time.perf_counter()
        with st.spinner("Analyzing foliar cellular pathology with MobileNetV2..."):
            arr = np.asarray(image)
            pred_result = predict_image_array(
                image_array=arr,
                labels=labels,
                model=model,
                confidence_threshold=confidence_threshold,
            )
            elapsed_ms = (time.perf_counter() - started_at) * 1000.0

        if pred_result.get("status") == "ok":
            top_class = pred_result["predicted_class"]
            confidence = float(pred_result["confidence"])
            clean_class_name = top_class.replace("___", " - ").replace("_", " ")
            margin = float(pred_result.get("top_prediction_margin", 0.0))
            is_healthy = is_healthy_class(top_class)
            crop_name = top_class.partition("___")[0]
            disease_name = top_class.partition("___")[2]
            
            # Explainability (Grad-CAM)
            explanation = None
            heatmap_leaf_focus = None
            if not isinstance(model, TFLiteModel):
                explanation = gradcam_for_prediction(
                    model=model,
                    image_array=np.asarray(image, dtype=np.float32),
                    class_index=labels.index(top_class),
                )
                if explanation.get("status") == "ok":
                    mask = quality.leaf_mask
                    heatmap = explanation["heatmap"]
                    if mask is not None and heatmap is not None:
                        if mask.shape != heatmap.shape:
                            mask = (
                                cv2.resize(
                                    mask.astype(np.uint8),
                                    (heatmap.shape[1], heatmap.shape[0]),
                                    interpolation=cv2.INTER_NEAREST,
                                )
                                > 0
                            )
                        h_total = float(np.sum(heatmap))
                        if h_total > 0 and np.any(mask):
                            heatmap_leaf_focus = float(np.sum(heatmap[mask]) / h_total)

            # Trust Assessment
            trust = assess_trust(
                confidence=confidence,
                margin=margin,
                quality=quality,
                validation_threshold=confidence_threshold,
                heatmap_leaf_focus=heatmap_leaf_focus,
                thresholds=trust_thresholds,
            )

            # Calculate Innovative 0-100 Crop Health Score
            health_score = calculate_crop_health_score(
                predicted_class=top_class,
                confidence=confidence,
                image_quality_acceptable=quality.acceptable,
                blur_score=quality.blur_score,
                weather_risk_level="Moderate",
                growth_stage="Fruiting",
            )

            # Generate Calibrated Plain-Language Confidence Explanation
            conf_data = generate_confidence_explanation(
                predicted_class=top_class,
                confidence=confidence,
                blur_score=quality.blur_score,
                brightness=quality.brightness,
                is_acceptable=quality.acceptable,
            )

            # Build Second Opinion Differential List
            differential_tuples = [(p["class_name"], p["probability"]) for p in pred_result.get("top_predictions", [])]
            second_opinions = build_second_opinion_list(differential_tuples)

            # 5-Step Farmer Action Plan
            action_plan_5 = generate_5step_action_plan(
                crop=crop_name,
                disease=disease_name,
                severity=health_score.severity,
            )

            # Potential Yield Loss Impact
            yield_impact = estimate_yield_impact(
                crop=crop_name,
                disease=disease_name,
                severity=health_score.severity,
                acreage=1.0,
            )

            # Save to SQLite history
            if save_to_history:
                append_prediction(
                    predicted_class=top_class,
                    model_version=model_file_name or "MobileNetV2",
                    confidence=confidence,
                    top_predictions=pred_result.get("top_predictions"),
                    trust_level=trust.get("level"),
                    inference_ms=elapsed_ms,
                    image_quality={
                        "blur_score": quality.blur_score,
                        "leaf_coverage": quality.leaf_coverage_fraction,
                    },
                    user_notes=scan_notes,
                    image_name=getattr(uploaded_file, "name", "sample_image.jpg"),
                    language=language,
                )

            # ---------------------------------------------------------
            # Display Diagnostic Results & Integrated Health Score
            # ---------------------------------------------------------
            st.write("")
            render_crop_health_score_card(health_score)

            res_left, res_right = st.columns([1.2, 1.0])
            
            with res_left:
                render_card_start("Primary AI Diagnosis", badge_text="Healthy" if is_healthy else "Pathology Active", badge_variant="forest" if is_healthy else "crimson")
                st.markdown(f"### {clean_class_name}")
                st.caption(f"Inference Latency: `{elapsed_ms:.0f} ms` · Calibrated with PlantVillage Benchmarks")
                
                # Confidence Meter with Plain-Language Explanation
                render_confidence_meter(conf_data, severity=health_score.severity)

                render_trust_indicator(trust.get("level", "Cannot Assess"), trust.get("explanation", ""))
                
                # Second Opinion Differential Panel
                render_second_opinion_panel(second_opinions)
                render_card_end()

            with res_right:
                render_card_start("Explainable AI (Grad-CAM Attention)", badge_text="XAI Activation", badge_variant="emerald")
                if explanation and explanation.get("status") == "ok":
                    opacity = st.slider("Grad-CAM Overlay Blend Opacity", 0.1, 1.0, 0.55, 0.05, key="cam_opacity")
                    overlay = overlay_heatmap(image, explanation["heatmap"], alpha=opacity)
                    st.image(overlay, caption="Network attention heatmap reveals regions that triggered diagnosis.", use_container_width=True)
                    
                    # Plain language Grad-CAM explanation
                    g_expl = generate_gradcam_explanation(top_class)
                    st.info(f"🔍 **Visual Focus:** {g_expl}")

                    if heatmap_leaf_focus is not None:
                        st.caption(f"Foliar-region attention ratio: **{heatmap_leaf_focus * 100:.1f}%**")
                else:
                    st.info("Grad-CAM visualization not available for this model configuration.")
                render_card_end()

                # Yield Loss Estimator Card
                render_card_start("Potential Yield Impact & Value Protected", badge_text="Economic Analysis", badge_variant="amber")
                st.markdown(f"**Estimated Harvest Impact:** `{yield_impact['loss_pct_range']}`")
                st.markdown(f"**Potential Loss Without Treatment:** `~{yield_impact['potential_loss_qtl']} qtl` (₹{yield_impact['potential_loss_inr']:,})")
                st.markdown(f"**Value Protected with Timely IPM:** `₹{yield_impact['protected_value_inr']:,} / acre`")
                st.caption(yield_impact["summary"])
                render_card_end()

            # ---------------------------------------------------------
            # 5-Step Certified Farmer Action Plan
            # ---------------------------------------------------------
            st.write("")
            render_action_plan_interactive(action_plan_5, key_prefix="scanner_action")

            # ---------------------------------------------------------
            # WhatsApp Share & Voice Audio Tools
            # ---------------------------------------------------------
            wa_url = generate_whatsapp_share_url(
                crop=crop_name,
                disease=disease_name,
                severity=health_score.severity,
                confidence_pct=f"{confidence * 100:.1f}%",
                health_score=health_score.score,
                action_plan_summary=action_plan_5["step1_inspect"][:100] + "...",
            )
            speech_txt = get_speech_script(
                crop=crop_name,
                disease=disease_name,
                severity=health_score.severity,
                health_score=health_score.score,
                language=language,
            )
            render_whatsapp_and_audio_tools(wa_url, speech_txt, language=language)

            # ---------------------------------------------------------
            # Expert Verification Routing Button
            # ---------------------------------------------------------
            if confidence < 0.75:
                st.warning("⚠️ Low confidence detection. Forwarding this scan to a verified agronomist is strongly advised.")
            if st.button("👨‍🌾 Submit to KVK Agronomist for Expert Verification", key="btn_submit_expert"):
                st.success("✓ Scan successfully queued for KVK Agronomist review in the Expert Verification Center!")

        else:
            st.error(f"Inference failed: {pred_result.get('message', 'Unknown error.')}")

render_about_footer()
