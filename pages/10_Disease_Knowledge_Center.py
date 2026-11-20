"""Disease Knowledge Center - CropShield AI 2.0 Verified Extension Encyclopedia."""

from __future__ import annotations

import streamlit as st

from src.cropshield.footer import render_about_footer
from src.cropshield.knowledge_base import load_disease_knowledge
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
    st.set_page_config(page_title="Disease Knowledge Center - CropShield AI 2.0", page_icon="📚", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("disease_knowledge", language),
    subtitle="Authoritative agricultural disease catalog verified against ICAR, TNAU, and Indian agricultural extension guidelines.",
    tag="Decision Support",
)

knowledge = load_disease_knowledge()

if not knowledge:
    st.warning("No verified disease knowledge records found in `data/disease_knowledge.json`.")
else:
    # Filter options
    categories = sorted(list({rec.get("disease_category", "General") for rec in knowledge.values()}))
    
    col_filter1, col_filter2 = st.columns([1.5, 2.0])
    with col_filter1:
        selected_category = st.selectbox("Filter by Pathology Category:", ["All Categories"] + categories)
    with col_filter2:
        search_query = st.text_input("Search symptoms, causal agent, or common name:", placeholder="e.g. Alternaria, yellowing, spots")

    st.write("")
    
    displayed_records = []
    for class_key, rec in knowledge.items():
        if selected_category != "All Categories" and rec.get("disease_category") != selected_category:
            continue
        if search_query:
            query = search_query.lower()
            text_haystack = f"{rec.get('disease','')} {rec.get('symptoms','')} {rec.get('crop','')} {class_key}".lower()
            if query not in text_haystack:
                continue
        displayed_records.append((class_key, rec))

    st.caption(f"Displaying **{len(displayed_records)}** verified disease profiles.")

    for class_key, rec in displayed_records:
        clean_name = rec.get("disease", class_key.replace("___", " - ").replace("_", " "))
        crop_name = rec.get("crop", "Tomato")
        cat = rec.get("disease_category", "Pathology")
        is_healthy = "healthy" in class_key.lower()
        
        badge_variant = "forest" if is_healthy else ("amber" if cat == "Fungal" else "crimson")
        
        render_card_start(f"{crop_name} — {clean_name}", badge_text=cat, badge_variant=badge_variant)
        
        col_left, col_right = st.columns([1.4, 1.0])
        with col_left:
            st.markdown(f"**Primary Symptoms:**\n{rec.get('symptoms', 'N/A')}")
            st.markdown(f"**Distinguishing Signs:**\n{rec.get('distinguishing_signs', 'N/A')}")
            st.markdown(f"**Favorable Environmental Conditions:**\n{rec.get('favorable_conditions', 'N/A')}")
            
        with col_right:
            st.markdown(f"**Look-alike Conditions:**\n{rec.get('look_alikes', 'N/A')}")
            st.markdown(f"**Verified Source:** [{rec.get('source_name', 'Agricultural Extension')}]({rec.get('source_url', '#')})")
            st.markdown(f"**Last Reviewed:** `{rec.get('last_reviewed', 'Recent')}`")
            
        with st.expander("View Management & Extension Advice"):
            m_tab1, m_tab2 = st.tabs(["Immediate Steps", "Integrated Prevention"])
            with m_tab1:
                for s in rec.get("immediate_steps", []):
                    st.markdown(f"- {s}")
            with m_tab2:
                for p in rec.get("prevention", []):
                    st.markdown(f"- {p}")
        render_card_end()

render_about_footer()
