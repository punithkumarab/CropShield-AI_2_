"""Interactive Farm Map - CropShield AI 2.0 Live Field Health Map & Spatial Surveillance."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.cropshield.footer import render_about_footer
from src.cropshield.history import list_farms, list_plots, update_plot_status
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
    st.set_page_config(page_title="Field Health Map - CropShield AI 2.0", page_icon="🗺️", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title="Field Health Map & Spatial Surveillance",
    subtitle="Live satellite-style plot telemetry, disease pressure heatmaps, and temporal progression timelines.",
    tag="Farm & Field Management",
)

farms = list_farms()
plots = list_plots()

# Standardized Color Map
STATUS_COLOR_MAP = {
    "Healthy": "#2D6A4F",
    "Watch / Monitor": "#DDA15E",
    "Moderate Risk": "#E09F3E",
    "Severe": "#D90429",
}

if not plots:
    # Provide sample interactive plots if user hasn't created any yet
    plots = [
        {
            "id": 1,
            "name": "North Field - Sector A",
            "crop_variety": "Tomato (Arka Rakshak)",
            "health_status": "Healthy",
            "sowing_date": "2026-09-15",
            "irrigation_type": "Drip (Under-Canopy)",
            "last_treatment": "2026-11-10 (Trichoderma)",
            "latitude": 13.0827,
            "longitude": 77.5877,
            "disease": "None (Intact Foliage)",
            "confidence": 96.5,
            "weather_risk": "Low (24°C, 65% RH)",
            "action": "Maintain routine fertigation and weekly scouting.",
        },
        {
            "id": 2,
            "name": "Riverbed Sector - Plot B",
            "crop_variety": "Tomato (Heirloom)",
            "health_status": "Moderate Risk",
            "sowing_date": "2026-09-22",
            "irrigation_type": "Sprinkler (Overhead)",
            "last_treatment": "2026-10-28 (Neem 1500ppm)",
            "latitude": 13.0870,
            "longitude": 77.5920,
            "disease": "Early Blight (Alternaria solani)",
            "confidence": 88.2,
            "weather_risk": "Elevated (88% RH morning fog)",
            "action": "Switch off overhead sprinklers. Apply copper hydroxide barrier.",
        },
        {
            "id": 3,
            "name": "Highland Terrace - Plot C",
            "crop_variety": "Potato (Kufri Jyoti)",
            "health_status": "Watch / Monitor",
            "sowing_date": "2026-10-01",
            "irrigation_type": "Drip",
            "last_treatment": "2026-11-05 (Panchagavya)",
            "latitude": 13.0790,
            "longitude": 77.5840,
            "disease": "Mild Foliar Chlorosis",
            "confidence": 74.0,
            "weather_risk": "Moderate (75% RH)",
            "action": "Inspect leaf undersides with 10x hand lens for mites.",
        },
        {
            "id": 4,
            "name": "Polyhouse Green - Sector D",
            "crop_variety": "Capsicum (Bell Pepper)",
            "health_status": "Healthy",
            "sowing_date": "2026-08-20",
            "irrigation_type": "Automated Drip",
            "last_treatment": "2026-11-12 (Bio-Fungicide)",
            "latitude": 13.0845,
            "longitude": 77.5895,
            "disease": "None (Vigorous Canopy)",
            "confidence": 98.1,
            "weather_risk": "Optimal Climate Controlled",
            "action": "Harvest cycle scheduled in 6 days.",
        },
    ]

# ---------------------------------------------------------
# Timeline Slider: Temporal Disease & Plot Health Simulation
# ---------------------------------------------------------
render_card_start("Temporal Foliar Health & Pathogen Progression", badge_text="Timeline Slider", badge_variant="emerald")
st.write("Slide across temporal checkpoints to inspect how disease pressure evolved or is projected to spread:")

timeline_stage = st.select_slider(
    "Select Temporal Checkpoint:",
    options=["Day -14 (Pre-Season Baseline)", "Day -7 (First Spore Warning)", "Today (Live Real-Time Surveillance)", "Projected +7 (Without IPM Intervention)", "Projected +7 (With Recommended Bio-IPM)"],
    value="Today (Live Real-Time Surveillance)",
)

if "Projected +7 (Without" in timeline_stage:
    st.error("⚠️ Projected +7 Without IPM: Disease pressure spreads to 65% of canopy in Riverbed Plot B. Defoliation risk elevated.")
elif "Projected +7 (With" in timeline_stage:
    st.success("✓ Projected +7 With Bio-IPM: Bio-fungicide barrier halts lesion expansion. Plot B recovers canopy health.")
else:
    st.info(f"Viewing: **{timeline_stage}**")
render_card_end()

# ---------------------------------------------------------
# Spatial Overview Metrics
# ---------------------------------------------------------
m1, m2, m3, m4 = st.columns(4)
h_count = sum(1 for p in plots if "Healthy" in p.get("health_status", "Healthy"))
w_count = sum(1 for p in plots if "Watch" in p.get("health_status", ""))
m_count = sum(1 for p in plots if "Moderate" in p.get("health_status", ""))
s_count = sum(1 for p in plots if "Severe" in p.get("health_status", ""))

m1.metric("Total Field Plots", f"{len(plots)}")
m2.metric("Optimal Health (Green)", f"{h_count}", delta=f"{h_count/len(plots)*100:.0f}% Canopy")
m3.metric("Under Watch (Yellow/Orange)", f"{w_count + m_count}", delta="Requires Inspection")
m4.metric("Severe Outbreak (Red)", f"{s_count}", delta="Emergency Quarantine" if s_count > 0 else "Clean Zero", delta_color="inverse" if s_count > 0 else "normal")

st.write("")

# ---------------------------------------------------------
# Live Geographic / Drone Heatmap Visualization
# ---------------------------------------------------------
render_card_start("Live Drone & Satellite-Style Field Health Heatmap", badge_text="Multispectral Simulation", badge_variant="forest")
st.write("Interactive spatial plot inspector with disease severity color coding, micro-climate risk, and drone heatmap overlay:")

df_plots = pd.DataFrame(plots)

# Plotly Mapbox scatter with color mapping
fig = px.scatter_mapbox(
    df_plots,
    lat="latitude",
    lon="longitude",
    color="health_status",
    color_discrete_map=STATUS_COLOR_MAP,
    hover_name="name",
    hover_data={
        "crop_variety": True,
        "health_status": True,
        "disease": True,
        "irrigation_type": True,
        "latitude": False,
        "longitude": False,
    },
    size=[24] * len(df_plots),
    zoom=13.5,
)

fig.update_layout(
    mapbox_style="open-street-map",
    margin=dict(l=0, r=0, t=0, b=0),
    height=480,
    legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.02, bgcolor="rgba(255,255,255,0.85)"),
)
st.plotly_chart(fig, use_container_width=True)
render_card_end()

# ---------------------------------------------------------
# Interactive Clickable Plot Details Inspector
# ---------------------------------------------------------
render_card_start("Detailed Plot Telemetry & Diagnostic Dossier", badge_text="Plot Inspector", badge_variant="neutral")
selected_plot_name = st.selectbox("Select Plot to Inspect Diagnostic Record:", [p["name"] for p in plots])
sel = next((p for p in plots if p["name"] == selected_plot_name), plots[0])

st.markdown(
    f"""
    <div style="background: #FFFFFF; border: 1.5px solid #2D6A4F33; border-radius: 12px; padding: 1.2rem; box-shadow: 0 4px 14px rgba(0,0,0,0.03);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; flex-wrap: wrap;">
            <div>
                <h3 style="margin: 0; color: #0D2818; font-size: 1.25rem;">{sel['name']}</h3>
                <span style="font-size: 0.82rem; color: #64748B;">Crop: <strong>{sel.get('crop_variety', 'Tomato')}</strong> | Sown: {sel.get('sowing_date', 'N/A')}</span>
            </div>
            <span style="font-size: 0.82rem; font-weight: 750; padding: 0.25rem 0.65rem; border-radius: 20px; background: {STATUS_COLOR_MAP.get(sel['health_status'], '#2D6A4F')}18; color: {STATUS_COLOR_MAP.get(sel['health_status'], '#2D6A4F')};">
                {sel['health_status']}
            </span>
        </div>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-bottom: 1rem;">
            <div style="background: #FAF7F2; padding: 0.6rem 0.9rem; border-radius: 8px;">
                <div style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Latest Pathology Scan</div>
                <strong style="color: #0D2818; font-size: 0.92rem;">{sel.get('disease', 'Healthy')}</strong> ({sel.get('confidence', 95.0)}%)
            </div>
            <div style="background: #FAF7F2; padding: 0.6rem 0.9rem; border-radius: 8px;">
                <div style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Irrigation &amp; Micro-Climate</div>
                <strong style="color: #0D2818; font-size: 0.92rem;">{sel.get('irrigation_type', 'Drip')}</strong> ({sel.get('weather_risk', 'Low')})
            </div>
            <div style="background: #FAF7F2; padding: 0.6rem 0.9rem; border-radius: 8px;">
                <div style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Last Treatment Executed</div>
                <strong style="color: #0D2818; font-size: 0.92rem;">{sel.get('last_treatment', 'N/A')}</strong>
            </div>
        </div>
        
        <p style="font-size: 0.86rem; color: #166534; font-weight: 600; margin: 0; background: #D8F3DC33; padding: 0.6rem 0.9rem; border-radius: 8px;">
            💡 <strong>Recommended Agronomic Action:</strong> {sel.get('action', 'Maintain standard protocol.')}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
render_card_end()

render_about_footer()
