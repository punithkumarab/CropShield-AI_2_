"""Batch Image Analysis - CropShield AI 2.0 Bulk Diagnostic Processing."""

from __future__ import annotations

import io
import time

import pandas as pd
import plotly.express as px
from PIL import Image
import streamlit as st

from src.cropshield.batch import process_batch_images
from src.cropshield.config import LABELS_PATH, MODEL_PATH, MODELS_DIR, TFLITE_MODEL_PATH
from src.cropshield.footer import render_about_footer
from src.cropshield.history import list_plots, log_batch_scan
from src.cropshield.model import load_labels, load_model, load_tflite_model
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
    st.set_page_config(page_title="Batch Image Analysis - CropShield AI 2.0", page_icon="📁", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("batch_analysis", language),
    subtitle="High-throughput batch diagnostic processing, population health ratios, and bulk CSV export.",
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

render_card_start("Bulk Image Upload", badge_text="Up to 20 Photos", badge_variant="emerald")
uploaded_files = st.file_uploader(
    "Select multiple leaf images for bulk analysis:",
    type=["jpg", "jpeg", "png", "webp"],
    accept_multiple_files=True,
    help="Process up to 20 images simultaneously with memory-safe sequential inference.",
)

batch_name = st.text_input("Batch Identifier / Scouting Session Name:", value=f"Scouting_Batch_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}")
render_card_end()

if uploaded_files:
    total_files = len(uploaded_files)
    st.info(f"📁 {total_files} images queued for processing.")
    
    if st.button(f"🚀 Analyze {total_files} Images", type="primary", use_container_width=True, disabled=model is None or not labels):
        progress_bar = st.progress(0, text="Initializing batch analysis...")
        start_time = time.perf_counter()
        
        batch_results = process_batch_images(
            uploaded_files=uploaded_files,
            model=model,
            labels=labels,
            confidence_threshold=0.70,
        )
        elapsed_sec = time.perf_counter() - start_time
        progress_bar.progress(100, text=f"✓ Batch analysis complete in {elapsed_sec:.2f} seconds.")
        
        # Log to SQLite
        log_batch_scan(
            batch_name=batch_name,
            total_images=batch_results["total"],
            healthy_count=batch_results["healthy"],
            diseased_count=batch_results["diseased"],
            results=batch_results["results"],
        )
        
        # ---------------------------------------------------------
        # Summary KPI Cards
        # ---------------------------------------------------------
        st.write("")
        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
        
        total = batch_results["total"]
        healthy = batch_results["healthy"]
        diseased = batch_results["diseased"]
        healthy_pct = (healthy / total * 100) if total > 0 else 0.0
        
        b_col1.metric("Total Scanned", f"{total}")
        b_col2.metric("Healthy Leaves", f"{healthy}", delta=f"{healthy_pct:.1f}%")
        b_col3.metric("Pathologies Detected", f"{diseased}", delta="Flagged" if diseased > 0 else "Clean", delta_color="inverse" if diseased > 0 else "normal")
        b_col4.metric("Avg Speed / Leaf", f"{(elapsed_sec / total * 1000):.0f} ms" if total > 0 else "0 ms")
        
        # ---------------------------------------------------------
        # Charts & Aggregates
        # ---------------------------------------------------------
        df = batch_results["summary_df"]
        if not df.empty and diseased > 0:
            st.write("")
            c_col1, c_col2 = st.columns([1.2, 1.0])
            with c_col1:
                render_card_start("Pathology Breakdown in Batch", badge_text="Class Counts", badge_variant="forest")
                class_summary = df["predicted_class"].value_counts().reset_index()
                class_summary.columns = ["Class", "Count"]
                class_summary["Clean Class"] = class_summary["Class"].apply(lambda s: s.replace("___", " - ").replace("_", " "))
                
                fig = px.pie(
                    class_summary,
                    names="Clean Class",
                    values="Count",
                    color_discrete_sequence=["#2D6A4F", "#D8F3DC", "#D97706", "#DC2626", "#0284C7"],
                )
                fig.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=260)
                st.plotly_chart(fig, use_container_width=True)
                render_card_end()
                
            with c_col2:
                render_card_start("Trust Level Distribution", badge_text="Quality", badge_variant="neutral")
                trust_counts = df["trust_level"].value_counts().reset_index()
                trust_counts.columns = ["Trust Level", "Count"]
                fig_trust = px.bar(
                    trust_counts,
                    x="Trust Level",
                    y="Count",
                    color="Trust Level",
                    color_discrete_map={"High": "#1B4332", "Medium": "#D97706", "Low": "#DC2626", "Cannot Assess": "#94A3B8"},
                )
                fig_trust.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=260, showlegend=False)
                st.plotly_chart(fig_trust, use_container_width=True)
                render_card_end()

        # ---------------------------------------------------------
        # Detailed Results Table & CSV Export
        # ---------------------------------------------------------
        st.write("")
        render_card_start("Per-Image Diagnostic Results", badge_text="Table View", badge_variant="emerald")
        display_df = df.copy()
        display_df["Diagnosis"] = display_df["predicted_class"].apply(lambda s: s.replace("___", " - ").replace("_", " "))
        display_df["Confidence"] = display_df["confidence"].apply(lambda c: f"{c*100:.1f}%")
        display_df["Leaf Coverage"] = display_df["leaf_coverage"].apply(lambda l: f"{l:.1f}%")
        
        final_cols = ["filename", "Diagnosis", "Confidence", "trust_level", "blur_score", "Leaf Coverage"]
        st.dataframe(display_df[final_cols], use_container_width=True, hide_index=True)
        
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Batch Results (CSV)",
            data=csv_data,
            file_name=f"{batch_name}_results.csv",
            mime="text/csv",
            type="secondary",
        )
        render_card_end()

render_about_footer()
