"""Crop Analytics Center - CropShield AI 2.0 Agronomic Intelligence."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st

from src.cropshield.footer import render_about_footer
from src.cropshield.history import fetch_all_predictions, list_plots
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
    st.set_page_config(page_title="Crop Analytics Center - CropShield AI 2.0", page_icon="📊", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("crop_analytics", language),
    subtitle="Agronomic epidemiological trends, pathogen prevalence, model confidence distributions, and surveillance BI.",
    tag="Farm & Field Management",
)

predictions = fetch_all_predictions(limit=500)
plots = list_plots()

if not predictions:
    st.info("No diagnostic scan data found in SQLite history. Perform leaf scans to generate agronomic intelligence charts.")
else:
    df = pd.DataFrame(predictions)
    df["Timestamp_dt"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df["Date"] = df["Timestamp_dt"].dt.date
    df["Clean_Diagnosis"] = df["predicted_class"].apply(lambda s: str(s).replace("___", " - ").replace("_", " "))
    df["Confidence_pct"] = df["confidence"].astype(float) * 100.0

    # ---------------------------------------------------------
    # Top KPI Metrics
    # ---------------------------------------------------------
    k1, k2, k3, k4 = st.columns(4)
    total_scans = len(df)
    mean_conf = df["Confidence_pct"].mean()
    high_trust_count = sum(1 for t in df.get("trust_level", []) if t == "High")
    avg_speed = df["inference_ms"].dropna().mean() if "inference_ms" in df.columns else 0.0

    k1.metric("Total Historical Scans", f"{total_scans:,}")
    k2.metric("Mean Model Confidence", f"{mean_conf:.1f}%")
    k3.metric("High-Trust Validated", f"{high_trust_count}", delta=f"{high_trust_count/total_scans*100:.0f}%")
    k4.metric("Mean Inference Latency", f"{avg_speed:.0f} ms" if avg_speed > 0 else "N/A")

    st.write("")

    # ---------------------------------------------------------
    # Temporal Trends & Disease Prevalence
    # ---------------------------------------------------------
    c_col1, c_col2 = st.columns([1.3, 1.0])
    
    with c_col1:
        render_card_start("Temporal Diagnostic Volume", badge_text="Timeline", badge_variant="emerald")
        daily_counts = df.groupby("Date").size().reset_index(name="Scan Count")
        fig_time = px.line(
            daily_counts,
            x="Date",
            y="Scan Count",
            markers=True,
            color_discrete_sequence=["#1B4332"],
        )
        fig_time.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            height=280,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_time, use_container_width=True)
        render_card_end()

    with c_col2:
        render_card_start("Top Pathogen Frequency", badge_text="Prevalence", badge_variant="forest")
        top_pathogens = df["Clean_Diagnosis"].value_counts().head(5).reset_index()
        top_pathogens.columns = ["Pathology", "Scans"]
        fig_pie = px.pie(
            top_pathogens,
            names="Pathology",
            values="Scans",
            color_discrete_sequence=["#1B4332", "#2D6A4F", "#D8F3DC", "#D97706", "#DC2626"],
        )
        fig_pie.update_layout(margin=dict(l=0, r=0, t=10, b=0), height=280)
        st.plotly_chart(fig_pie, use_container_width=True)
        render_card_end()

    # ---------------------------------------------------------
    # Confidence Distribution & Quality Analysis
    # ---------------------------------------------------------
    st.write("")
    h_col1, h_col2 = st.columns(2)
    
    with h_col1:
        render_card_start("Model Confidence Histogram", badge_text="Calibration Distribution", badge_variant="blue")
        fig_hist = px.histogram(
            df,
            x="Confidence_pct",
            nbins=20,
            color_discrete_sequence=["#2D6A4F"],
            labels={"Confidence_pct": "Confidence (%)"},
        )
        fig_hist.update_layout(
            margin=dict(l=0, r=0, t=10, b=0),
            height=260,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis_title="Predicted Confidence (%)",
            yaxis_title="Scan Count",
        )
        st.plotly_chart(fig_hist, use_container_width=True)
        render_card_end()

    with h_col2:
        render_card_start("Trust Level Distribution", badge_text="Validation Levels", badge_variant="neutral")
        if "trust_level" in df.columns:
            trust_counts = df["trust_level"].value_counts().reset_index()
            trust_counts.columns = ["Trust Level", "Count"]
            fig_bar = px.bar(
                trust_counts,
                x="Trust Level",
                y="Count",
                color="Trust Level",
                color_discrete_map={"High": "#1B4332", "Medium": "#D97706", "Low": "#DC2626", "Cannot Assess": "#94A3B8"},
            )
            fig_bar.update_layout(
                margin=dict(l=0, r=0, t=10, b=0),
                height=260,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                showlegend=False,
            )
            st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No trust level data recorded.")
        render_card_end()

render_about_footer()
