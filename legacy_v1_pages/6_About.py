"""About CropShield AI 2.0 - Platform Overview, Mission, Technology, and Verified Contacts."""

from __future__ import annotations

import streamlit as st

from src.cropshield.footer import render_about_footer
from src.cropshield.knowledge_base import load_local_expert_contacts
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
    st.set_page_config(page_title="About CropShield AI 2.0", page_icon="🌿", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

# Modern Branded Page Header
render_page_header(
    title="About CropShield AI 2.0",
    subtitle="Intelligent foliar surveillance, edge computer vision diagnostics, and precision agricultural decision support for Indian farming.",
    tag="Platform Documentation",
)

# Platform Executive Overview Card (Clean, Intentional, Zero Ghost Text)
render_card_start("Platform Overview & Architecture", badge_text="CropShield AI 2.0", badge_variant="emerald")
st.markdown(
    """
    <div style="padding: 0.2rem 0 0.8rem 0;">
        <h2 class="cypa-editorial-heading-gradient" style="margin-bottom: 0.8rem;">
            Intelligence That Protects Every Leaf &amp; Harvest
        </h2>
        <p style="font-size: 1.02rem; line-height: 1.7; color: inherit; opacity: 0.92; margin-bottom: 1.2rem;">
            <strong>CropShield AI 2.0</strong> is an enterprise-grade foliar disease diagnostic and agronomic decision-support platform designed specifically for Indian agriculture. Combining edge deep learning computer vision (MobileNetV2), localized micro-climate epidemiology from Open-Meteo, and ICAR/KVK-aligned integrated pest management (IPM) protocols, the platform empowers cultivators, agronomists, and agricultural researchers to detect foliar pathogens before irreversible canopy loss occurs.
        </p>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 14px; margin-top: 1rem;">
            <div style="background: rgba(45, 106, 79, 0.08); border: 1px solid rgba(45, 106, 79, 0.2); border-radius: 10px; padding: 0.85rem 1rem;">
                <div style="font-size: 1.25rem; margin-bottom: 0.2rem;">🔬</div>
                <strong style="font-size: 0.92rem; color: #1B4332;">Offline Edge Inference</strong>
                <p style="font-size: 0.8rem; opacity: 0.85; margin: 0.2rem 0 0 0;">Sub-second diagnosis with Grad-CAM visual heatmaps and zero mandatory cloud dependency.</p>
            </div>
            <div style="background: rgba(2, 132, 199, 0.08); border: 1px solid rgba(2, 132, 199, 0.2); border-radius: 10px; padding: 0.85rem 1rem;">
                <div style="font-size: 1.25rem; margin-bottom: 0.2rem;">🌦️</div>
                <strong style="font-size: 0.92rem; color: #0369A1;">Micro-Climate Telemetry</strong>
                <p style="font-size: 0.8rem; opacity: 0.85; margin: 0.2rem 0 0 0;">Automated ambient humidity, rain, and spore multiplication risk radar powered by Open-Meteo.</p>
            </div>
            <div style="background: rgba(221, 161, 94, 0.12); border: 1px solid rgba(221, 161, 94, 0.3); border-radius: 10px; padding: 0.85rem 1rem;">
                <div style="font-size: 1.25rem; margin-bottom: 0.2rem;">🛡️</div>
                <strong style="font-size: 0.92rem; color: #9A3412;">Organic IPM Priority</strong>
                <p style="font-size: 0.8rem; opacity: 0.85; margin: 0.2rem 0 0 0;">Prioritizes bio-controls (Trichoderma, Neem) before chemical fungicides to reduce farmer costs.</p>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
render_card_end()

# Mission & Core Capabilities
st.write("")
col1, col2 = st.columns(2)

with col1:
    render_card_start("Agricultural Mission & Vision", badge_text="Purpose", badge_variant="emerald")
    st.markdown(
        """
        **CropShield AI 2.0** bridges cutting-edge deep learning computer vision and everyday farm operations.
        Our mission is to help smallholder cultivators, agronomists, and extension officers:
        
        - 🔍 **Detect foliar pathogens at earliest onset** before irreversible canopy defoliation occurs.
        - 🌿 **Prioritize biological and organic bio-controls** (Trichoderma, Neem formulations) to reduce chemical run-off and input costs.
        - 🌦️ **Leverage real-time micro-climate epidemiological telemetry** to anticipate fungal spore multiplication windows.
        - 📋 **Empower growers with clear, actionable 5-step plans** backed by ICAR and State Agricultural University standards.
        """
    )
    render_card_end()

with col2:
    render_card_start("Technology & Edge Architecture", badge_text="Inference", badge_variant="forest")
    st.markdown(
        """
        - **Inference Engine:** MobileNetV2 with inverted residual blocks optimized for low-latency CPU and edge execution.
        - **Model Formats:** Dual support for native Keras 3 (`.keras`, `.h5`) and TensorFlow Lite (`.tflite`) edge acceleration.
        - **Explainable AI (XAI):** Real-time Grad-CAM attention heatmaps highlighting foliar lesion margins and chlorotic halos.
        - **Offline-First Privacy:** Zero mandatory cloud dependencies; all diagnostic inferences run privately on your local station.
        - **Quality Pre-Screening:** Smart Photo Coach validating blur, illumination, and leaf coverage before diagnostic execution.
        """
    )
    render_card_end()

# Dataset & Validation Benchmark
render_card_start("Benchmark Dataset & Clinical Calibration", badge_text="PlantVillage", badge_variant="neutral")
st.markdown(
    """
    CropShield AI is evaluated across standardized foliar disease categories adapted from the **PlantVillage** benchmark, 
    stratified across healthy foliar tissue and prevalent sub-continental agricultural pathogens:
    
    - **Tomato Pathologies:** Early Blight (*Alternaria solani*), Late Blight (*Phytophthora infestans*), Bacterial Spot (*Xanthomonas*), Septoria Leaf Spot, Leaf Mold, Yellow Leaf Curl Virus (TYLCV), Mosaic Virus, Two-Spotted Spider Mites, Target Spot, and Healthy foliage.
    - **Potato Pathologies:** Early Blight, Late Blight, and Healthy foliage.
    - **Pepper & Horticultural Crops:** Bacterial Spot and Healthy foliage.
    
    *All classification predictions are verified against strict validation confidence thresholds (default 0.70) with automatic routing for agronomist review when confidence is low.*
    """
)
render_card_end()

# Verified Expert Contacts
render_card_start("Verified Agricultural Extension Contacts", badge_text="ICAR / KVK Directory", badge_variant="amber")
st.write(
    "Need personalized crop diagnosis or soil testing? Contact your nearest verified Krishi Vigyan Kendra (KVK) "
    "or State Agricultural University extension center:"
)

contacts = load_local_expert_contacts()
if contacts:
    c_cols = st.columns(min(len(contacts), 3))
    for idx, contact in enumerate(contacts[:6]):
        col_idx = idx % min(len(contacts), 3)
        with c_cols[col_idx]:
            st.markdown(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.9rem; margin-bottom: 0.8rem;">
                    <strong style="color: #0D2818; font-size: 0.95rem;">{contact['name']}</strong>
                    <div style="font-size: 0.82rem; color: #475569; margin: 0.2rem 0;">{contact['organization']}</div>
                    {f'<div style="font-size: 0.8rem; color: #64748B;">📞 {contact.get("phone")}</div>' if contact.get("phone") else ''}
                </div>
                """,
                unsafe_allow_html=True,
            )
            if contact.get("url"):
                st.link_button("🌐 Visit Extension Portal", contact["url"], use_container_width=True)
else:
    st.info("No local contacts configured. Administrators can configure verified extension contacts in `data/local_expert_contacts.json`.")

render_card_end()

# Transparent Model Limitations
with st.expander("⚠️ Transparent Clinical Limitations & Field Guidance"):
    st.markdown(
        """
        - **Lighting & Varietal Shifts:** Computer vision inference accuracy may decrease under intense sunlight glare, deep shadows, or non-foliar backgrounds.
        - **Foliar Scope:** The AI system is calibrated for foliar leaf tissue; it does not diagnose soil-borne root rot, vascular wilt, or subterranean nematodes.
        - **Decision Support Only:** This platform is an intelligent advisory tool designed to assist human farmers and agronomists, not replace certified agricultural extension recommendations.
        - **Chemical Regulations:** All chemical control recommendations must comply with Central Insecticides Board & Registration Committee (CIB&RC) label claims and local agricultural statutes.
        """
    )

# Quick Action Bar
st.markdown("### 🚀 Ready to Protect Your Harvest?")
act1, act2, act3 = st.columns(3)
with act1:
    if st.button("🔬 Start Leaf Diagnosis", use_container_width=True, type="primary"):
        st.switch_page("pages/2_AI_Crop_Scanner.py")
with act2:
    if st.button("🤖 Consult AI Crop Doctor", use_container_width=True):
        st.switch_page("pages/11_AI_Agricultural_Assistant.py")
with act3:
    if st.button("🌦️ View Local Micro-Climate", use_container_width=True):
        st.switch_page("pages/12_Weather_and_Field_Insights.py")

render_about_footer()
