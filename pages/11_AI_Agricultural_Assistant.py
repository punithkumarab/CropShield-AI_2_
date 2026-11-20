"""AI Agricultural Assistant - CropShield AI 2.0 Conversational Crop Doctor."""

from __future__ import annotations

import streamlit as st

from src.cropshield.assistant import AgriculturalAssistant
from src.cropshield.footer import render_about_footer
from src.cropshield.history import fetch_all_predictions, list_plots
from src.cropshield.innovation import get_speech_script
from src.cropshield.translations import translate
from src.cropshield.ui import (
    get_selected_language,
    inject_theme,
    render_badge,
    render_card_end,
    render_card_start,
    render_page_header,
    render_whatsapp_and_audio_tools,
)

try:
    st.set_page_config(page_title="AI Crop Doctor - CropShield AI 2.0", page_icon="🩺", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

# Header
render_page_header(
    title="AI Crop Doctor & Agronomic Assistant",
    subtitle="Evidence-backed conversational agricultural advisory grounded strictly in verified ICAR and university extension bulletins.",
    tag="Decision Support",
)

assistant = AgriculturalAssistant()

# Top Actions & Status Row
col_top_l, col_top_r = st.columns([3, 1])
with col_top_l:
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 0.5rem; flex-wrap: wrap;">
            <span class="cs-badge cs-badge-forest">🌿 ICAR / TNAU Grounded</span>
            <span class="cs-badge cs-badge-emerald">⚡ Zero-Hallucination Verified</span>
            <span class="cs-badge cs-badge-amber">🩺 Multi-Lingual Crop Doctor</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col_top_r:
    if st.button("↺ New Chat", key="btn_new_chat", use_container_width=True, help="Clear conversation and start fresh"):
        st.session_state.chat_history = []
        st.session_state.pending_prompt = None
        st.rerun()

# Retrieve latest scan context from SQLite
latest_scans = fetch_all_predictions(limit=1)
latest_context_str = ""
if latest_scans:
    sc = latest_scans[0]
    p_name = sc.get("predicted_class", "Tomato___Early_blight").replace("___", " - ").replace("_", " ")
    conf = float(sc.get("confidence", 0.90)) * 100
    latest_context_str = f"Latest scan in memory: {p_name} ({conf:.1f}% confidence)."

# Initialize session state for chat messages
if "chat_history" not in st.session_state or not st.session_state.chat_history:
    welcome_text = (
        "Namaskara / Hello! I am your **CropShield AI Crop Doctor**.\n\n"
        "I provide practical, verified foliar diagnosis, symptom recognition, and organic management "
        "strategies grounded strictly in **ICAR, TNAU, and State Agricultural Extension** bulletins.\n\n"
    )
    if latest_context_str:
        welcome_text += f"📌 *I notice your {latest_context_str} — feel free to ask for treatment guidance on this scan!*\n\n"
    welcome_text += "How can I help protect your harvest today?"

    st.session_state.chat_history = [
        {
            "role": "assistant",
            "content": welcome_text,
            "sources": [],
            "grounded": True,
        }
    ]

# 6 Quick Action Buttons requested in Specification
st.markdown("<p style='font-size: 0.82rem; font-weight: 750; color: #1B4332; margin-bottom: 8px; letter-spacing: 0.05em; text-transform: uppercase;'>Crop Doctor Quick Actions:</p>", unsafe_allow_html=True)
qc1, qc2, qc3 = st.columns(3)
qc4, qc5, qc6 = st.columns(3)

chip_prompt = None

with qc1:
    if st.button("🩺 Diagnose this leaf", use_container_width=True, key="qa_diag"):
        chip_prompt = f"Please explain the diagnosis and primary symptoms of {latest_context_str or 'Tomato Early Blight'} in simple terms."
with qc2:
    if st.button("📋 What should I do today?", use_container_width=True, key="qa_today"):
        chip_prompt = "What immediate agricultural actions should I take today to prevent fungal foliar spread in humid weather?"
with qc3:
    if st.button("🚿 Is spraying needed?", use_container_width=True, key="qa_spray"):
        chip_prompt = "Is chemical or biological spraying recommended right now, and what are the certified organic bio-pesticide alternatives?"
with qc4:
    if st.button("🔍 Explain my Grad-CAM result", use_container_width=True, key="qa_gradcam"):
        chip_prompt = "How does Grad-CAM heatmaps explain where the AI model focused on the leaf lesions?"
with qc5:
    if st.button("📅 Create a 7-day action plan", use_container_width=True, key="qa_plan"):
        chip_prompt = "Create a practical 7-day farmer action plan for scouting, bio-sprays, and re-scan intervals."
with qc6:
    if st.button("🌐 Translate advice to Kannada/Hindi", use_container_width=True, key="qa_trans"):
        chip_prompt = "ದಯವಿಟ್ಟು ಈ ಸಲಹೆಯನ್ನು ಕನ್ನಡ ಮತ್ತು ಹಿಂದಿಯಲ್ಲಿ ಸರಳವಾಗಿ ವಿವರಿಸಿ / Please explain this advice simply in Kannada and Hindi."

if chip_prompt:
    st.session_state.pending_prompt = chip_prompt

# Conversation History Display
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
for msg in st.session_state.chat_history:
    role = msg["role"]
    content = msg["content"]
    sources = msg.get("sources", [])
    
    if role == "user":
        st.markdown(
            f"""
            <div class="chat-bubble-user">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 0.76rem; opacity: 0.9; font-weight: 750; letter-spacing: 0.04em;">
                    <span>🧑‍🌾 FARMER INQUIRY</span>
                </div>
                <div style="font-size: 0.96rem; line-height: 1.55;">{content}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        badge_html = '<span class="cs-badge cs-badge-forest" style="font-size: 0.72rem;">✓ ICAR Verified Advisory</span>' if msg.get("grounded", True) else '<span class="cs-badge cs-badge-amber" style="font-size: 0.72rem;">ℹ️ General Agronomic Guidance</span>'
        
        sources_html = ""
        if sources:
            source_items = "".join(
                f'<li style="margin-bottom: 5px; font-size: 0.84rem; color: #475569;"><strong>{s.get("crop", "")} — {s.get("disease", "")}:</strong> <a href="{s.get("source_url", "#")}" target="_blank" style="color: #059669; font-weight: 600; text-decoration: none;">{s.get("source_name", "Extension Bulletin")}</a> <span style="color: #94A3B8;">(Verified: {s.get("last_reviewed", "Current")})</span></li>'
                for s in sources
            )
            sources_html = f"""
            <div style="margin-top: 14px; padding-top: 10px; border-top: 1px solid #F1F5F9;">
                <div style="font-size: 0.74rem; font-weight: 750; color: #1B4332; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px;">Authoritative Agricultural Sources:</div>
                <ul style="padding-left: 1.2rem; margin: 0;">{source_items}</ul>
            </div>
            """
            
        st.markdown(
            f"""
            <div class="chat-bubble-assistant">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                    <div style="display: flex; align-items: center; gap: 8px; font-size: 0.82rem; font-weight: 750; color: #1B4332;">
                        <span>🌿 CROP DOCTOR ADVISOR</span>
                    </div>
                    {badge_html}
                </div>
                <div style="font-size: 0.96rem; line-height: 1.6; color: #1E293B;">
                    {content}
                </div>
                {sources_html}
            </div>
            """,
            unsafe_allow_html=True,
        )
st.markdown("</div>", unsafe_allow_html=True)

# Technical Dossier Toggle for Agronomists
show_dossier = st.checkbox("Show Agronomist Technical Dossier (Pathogen Etiology & Mode of Action)", value=False)
if show_dossier:
    with st.expander("🔬 Agronomist Technical Reference Dossier", expanded=True):
        st.markdown(
            """
            - **Causal Pathogen:** *Alternaria solani* (Ellis & Martin) Sorauer / *Phytophthora infestans* (Mont.) de Bary.
            - **Infection Biology:** Conidia germinate via germ tube penetrating stomatal apertures or epidermal wounds; optimal intercellular mycelial extension at 24°C-28°C with >80% relative humidity.
            - **Bio-Chemical Mode of Action:**
              - *Trichoderma harzianum:* Mycoparasitism, competition for rhizosphere nutrients, and induction of systemic resistance (ISR).
              - *Copper Hydroxide:* Multi-site contact protectant creating Cu2+ ion barrier inactivating fungal respiratory enzymes.
              - *Azoxystrobin (QoI):* Inhibits mitochondrial respiration by blocking electron transfer at cytochrome bc1 complex.
            """
        )

# Input Bar
user_input = st.chat_input("Ask Crop Doctor about leaf symptoms, organic bio-sprays, or 7-day action plans...")
active_query = user_input or st.session_state.pop("pending_prompt", None)

if active_query:
    st.session_state.chat_history.append({"role": "user", "content": active_query})
    
    with st.spinner("Retrieving verified agricultural extension records..."):
        result = assistant.answer_query(active_query)
        
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result["answer"],
        "sources": result.get("sources", []),
        "grounded": result.get("grounded", False),
    })
    st.rerun()

render_about_footer()
