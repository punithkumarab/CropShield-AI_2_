"""Settings & Privacy Governance - CropShield AI 2.0."""

from __future__ import annotations

from pathlib import Path
import streamlit as st

from src.cropshield.config import DB_PATH, MODELS_DIR
from src.cropshield.footer import render_about_footer
from src.cropshield.history import fetch_all_predictions, list_farms, list_plots
from src.cropshield.translations import LANGUAGES, translate
from src.cropshield.ui import (
    get_selected_language,
    inject_theme,
    render_badge,
    render_card_end,
    render_card_start,
    render_page_header,
)

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("settings_privacy", language),
    subtitle="Configure platform localization, regional agronomic defaults, data privacy consent, and storage maintenance.",
    tag="CropShield AI 2.0",
)

col_settings, col_privacy = st.columns([1, 1], gap="medium")

with col_settings:
    render_card_start("Localization & Field Defaults", "Regional", "forest")

    # Language selection
    current_lang = get_selected_language()
    lang_labels = {"en": "English (EN)", "kn": "ಕನ್ನಡ (Kannada)", "hi": "हिन्दी (Hindi)"}
    lang_keys = list(lang_labels.keys())
    selected_idx = lang_keys.index(current_lang) if current_lang in lang_keys else 0

    new_lang = st.selectbox(
        "Application Interface Language:",
        options=lang_keys,
        index=selected_idx,
        format_func=lambda k: lang_labels[k],
        key="settings_lang_select",
    )
    if new_lang != current_lang:
        st.session_state["cropshield_language"] = new_lang
        st.success(f"Language updated to {lang_labels[new_lang]}.")
        st.rerun()

    # Agro-climatic zone default
    agro_zones = [
        "Zone 5 - Southern Dry Zone (Karnataka)",
        "Zone 4 - Central Dry Zone (Karnataka)",
        "Indo-Gangetic Plain (North India)",
        "Western Dry / Arid Zone (Rajasthan / Gujarat)",
        "Eastern Coastal Plains (Tamil Nadu / Andhra Pradesh)",
        "Western Ghats & Coastal Zone",
    ]
    st.selectbox("Default Agro-Climatic Zone:", options=agro_zones, index=0)

    # Primary Crop Specialization
    st.selectbox(
        "Default Primary Specimen Crop:",
        options=["Tomato (Solanum lycopersicum)", "Potato (Solanum tuberosum)", "Bell Pepper (Capsicum annuum)", "General Solanaceae"],
        index=0,
    )

    # Ambient Weather Source
    st.text_input("Active Weather Telemetry Provider:", value="Open-Meteo Global WMO Forecast API (Zero-Key Realtime)", disabled=True)

    render_card_end()

    render_card_start("System Maintenance & Cache", "Storage", "neutral")
    st.markdown("Clear in-memory models and data caches if dataset or model weights were updated on disk.")

    c_b1, c_b2 = st.columns(2)
    with c_b1:
        if st.button("🧹 Clear Model & Data Cache", use_container_width=True):
            st.cache_data.clear()
            st.cache_resource.clear()
            st.success("Caches purged successfully.")
    with c_b2:
        if DB_PATH.is_file():
            db_bytes = DB_PATH.read_bytes()
            st.download_button(
                "💾 Backup SQLite Database",
                data=db_bytes,
                file_name="cropshield_history_backup.db",
                mime="application/x-sqlite3",
                use_container_width=True,
            )
        else:
            st.button("💾 SQLite DB Not Initialized", disabled=True, use_container_width=True)

    render_card_end()

with col_privacy:
    render_card_start("Data Privacy & Ethical AI Governance", "Consent", "emerald")
    st.markdown(
        "CropShield AI operates with strict **data sovereignty principles**. "
        "We believe smallholder farmers must retain complete ownership over their farm telemetry."
    )

    # Opt-in photo retention
    photo_consent = st.checkbox(
        "Enable Opt-In Raw Leaf Photo Retention",
        value=st.session_state.get("opt_in_photo_storage", False),
        help="When disabled, leaf images are processed strictly in memory and discarded immediately. No images are saved.",
    )
    st.session_state["opt_in_photo_storage"] = photo_consent

    if photo_consent:
        st.info("✓ Consented: Leaf photos may be stored in local chronological plant timelines for longitudinal recovery tracking.")
    else:
        st.caption("🔒 Privacy-First: Raw images are discarded immediately after feature extraction and inference.")

    # Telemetry sharing
    telemetry_consent = st.checkbox(
        "Contribute Anonymized Regional Disease Counts to Epidemiological Surveillance",
        value=st.session_state.get("telemetry_consent", True),
        help="Shares disease class names and district-level geo-tags with extension authorities to detect outbreaks early.",
    )
    st.session_state["telemetry_consent"] = telemetry_consent

    render_card_end()

    render_card_start("Verified Agronomic Extension Contacts", "Emergency", "amber")
    st.markdown("Direct hotlines for verified government agricultural advisory services:")

    st.markdown(
        """
        - **Kisan Call Centre (Government of India):**  
          📞 **Toll-Free 1800-180-1551** *(06:00 AM - 10:00 PM, 22 Official Languages)*
        - **ICAR - Indian Agricultural Research Institute (IARI):**  
          🌐 *Pusa, New Delhi 110012* · Helplines: +91-11-25841471
        - **ICAR - Indian Institute of Horticultural Research (IIHR):**  
          🌐 *Hessaraghatta Lake Post, Bengaluru 560089* · Tel: +91-80-23086100
        - **Tamil Nadu Agricultural University (TNAU) Agritech Portal:**  
          🌐 *Coimbatore, Tamil Nadu 641003*
        - **University of Agricultural Sciences (UAS), GKVK:**  
          🌐 *Bengaluru, Karnataka 560065*
        """
    )
    render_card_end()

render_about_footer()
