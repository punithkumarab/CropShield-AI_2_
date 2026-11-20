"""Treatment and Prevention Guide - CropShield AI 2.0 Integrated Pest Management."""

from __future__ import annotations

import streamlit as st

from src.cropshield.config import LABELS_PATH
from src.cropshield.dataset import detect_dataset_root, iter_class_dirs
from src.cropshield.footer import render_about_footer
from src.cropshield.history import (
    create_action_checklist,
    fetch_action_checklists,
    fetch_tracked_plants,
    set_action_checklist_item,
)
from src.cropshield.knowledge_base import get_verified_guidance, load_disease_knowledge
from src.cropshield.model import load_labels
from src.cropshield.translations import translate
from src.cropshield.treatment_guide import SAFE_PRACTICE_WARNINGS, build_verified_checklist
from src.cropshield.ui import (
    get_selected_language,
    inject_theme,
    render_badge,
    render_card_end,
    render_card_start,
    render_page_header,
)

try:
    st.set_page_config(page_title="Treatment & Prevention Guide - CropShield AI 2.0", page_icon="🩺", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("treatment_guide", language),
    subtitle="Integrated Pest Management (IPM), cultural hygiene, biological controls, and PPE safety protocols.",
    tag="Decision Support",
)

# ---------------------------------------------------------
# Safe Practice Warnings
# ---------------------------------------------------------
render_card_start("Statutory Agricultural Safety Warnings", badge_text="Safety Mandate", badge_variant="crimson")
for warning in SAFE_PRACTICE_WARNINGS:
    st.markdown(f"⚠️ {warning}")
render_card_end()

# ---------------------------------------------------------
# Disease Selection & Tiered Intervention Plan
# ---------------------------------------------------------
records = load_disease_knowledge()
labels = load_labels(LABELS_PATH) if LABELS_PATH.is_file() else []
if not labels:
    labels = sorted(list(records.keys()))

st.write("")
render_card_start("Verified Integrated Pest Management (IPM) Protocols", badge_text="Extension Certified", badge_variant="emerald")
selected_class = st.selectbox(
    "Select Crop Pathology Condition:",
    options=labels,
    format_func=lambda s: s.replace("___", " - ").replace("_", " "),
)

guidance = get_verified_guidance(selected_class, records)
if guidance:
    st.markdown(f"### {guidance.get('crop')} — {guidance.get('disease')}")
    st.markdown(f"**Pathogen Classification:** `{guidance.get('disease_category', 'General')}`")
    st.markdown(f"**Identified Symptoms:**\n{guidance.get('symptoms')}")
    
    tab_cult, tab_bio, tab_chem, tab_prev = st.tabs([
        "1. Cultural Hygiene",
        "2. Biological Controls",
        "3. Chemical Interventions",
        "4. Long-term Prevention",
    ])
    
    with tab_cult:
        st.markdown("**Field Hygiene & Agronomic Adjustments:**")
        for s in guidance.get("cultural_practices", guidance.get("immediate_steps", [])):
            st.markdown(f"- {s}")
            
    with tab_bio:
        st.markdown("**Bio-fungicides & Organic Formulations:**")
        bio_opts = guidance.get("biological_options", [])
        if bio_opts:
            for b in bio_opts:
                st.markdown(f"- {b}")
        else:
            st.info("No standalone biological controls specified. Adhere to strict cultural hygiene.")
            
    with tab_chem:
        st.markdown("**Regulated Chemical Controls (Strict Compliance):**")
        chem_opts = guidance.get("chemical_options", [])
        if chem_opts:
            for c in chem_opts:
                st.markdown(f"- {c}")
        else:
            st.info("Consult regional agricultural extension office for certified registered formulations and pre-harvest intervals.")
        st.caption("Always wear PPE: Nitrile gloves, respirator, eye protection, and protective boots.")
        
    with tab_prev:
        st.markdown("**Preventive Measures for Next Season:**")
        for p in guidance.get("prevention", []):
            st.markdown(f"- {p}")
            
    st.divider()
    st.caption(f"Authoritative Citation: [{guidance.get('source_name', 'ICAR/Extension')}]({guidance.get('source_url', '#')}) · Last Reviewed: `{guidance.get('last_reviewed')}`")
    
else:
    st.info("No verified treatment protocol on file for this specific category. Consult local Krishi Vigyan Kendra.")
render_card_end()

render_about_footer()
