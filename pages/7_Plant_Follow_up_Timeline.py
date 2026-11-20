"""Plant Follow-up Timeline - CropShield AI 2.0 Chronological Plant Surveillance."""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pandas as pd
import plotly.express as px
from PIL import Image, UnidentifiedImageError
import streamlit as st

from src.cropshield.config import LABELS_PATH
from src.cropshield.expert_request import build_expert_request
from src.cropshield.footer import render_about_footer
from src.cropshield.history import (
    add_plant_observation,
    create_tracked_plant,
    delete_plant_observation,
    delete_tracked_plant,
    fetch_plant_observations,
    fetch_plot_map,
    fetch_possible_plot_spread,
    fetch_tracked_plants,
    get_plant_timeline_image_path,
)
from src.cropshield.model import load_labels
from src.cropshield.preprocessing import validate_upload
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
    st.set_page_config(page_title="Plant Follow-up Timeline - CropShield AI 2.0", page_icon="🌱", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("plant_timeline", language),
    subtitle="Chronological foliar observation logging, consented photo retention, and disease recovery checklists.",
    tag="Farm & Field Management",
)

st.info(
    "Timeline records are stored locally in SQLite (`crop_history.db`). Photos are never retained unless you explicitly "
    "enable photo retention. Repeated AI model scores are preliminary observations, not conclusive medical proof of recovery."
)

tracked_plants = fetch_tracked_plants()

# ---------------------------------------------------------
# Create Plant Form
# ---------------------------------------------------------
with st.expander("➕ Register a New Plant or Sentinel Crop Marker", expanded=not bool(tracked_plants)):
    render_card_start("Plant Timeline Registration", badge_text="Sentinel Marker", badge_variant="emerald")
    with st.form("create_tracked_plant", clear_on_submit=True):
        f_c1, f_c2 = st.columns(2)
        with f_c1:
            new_name = st.text_input("Plant / Sentinel Identifier:", max_chars=80, placeholder="e.g. Tomato Sentinel #14")
            new_plot = st.text_input("Plot or Bed Reference:", max_chars=80, placeholder="e.g. Greenhouse Bed B")
        with f_c2:
            assign_grid = st.checkbox("Assign field grid coordinate", value=True)
            grid_row = st.number_input("Grid Row:", min_value=1, max_value=100, value=1, disabled=not assign_grid)
            grid_column = st.number_input("Grid Column:", min_value=1, max_value=100, value=1, disabled=not assign_grid)
        create_submitted = st.form_submit_button("Create Plant Timeline", type="primary")
        
    if create_submitted:
        if not new_name.strip():
            st.error("Plant name cannot be empty.")
        else:
            try:
                create_tracked_plant(
                    new_name,
                    plot_name=new_plot,
                    grid_row=int(grid_row) if assign_grid else None,
                    grid_column=int(grid_column) if assign_grid else None,
                )
                st.success(f"Timeline created for '{new_name}'!")
                st.rerun()
            except Exception as exc:
                st.error(f"Error creating timeline: {exc}")
    render_card_end()

# ---------------------------------------------------------
# Active Plant Selector & Timeline History
# ---------------------------------------------------------
if tracked_plants:
    plant_options = {p["id"]: f"{p['name']} ({p.get('plot_name') or 'Unassigned'})" for p in tracked_plants}
    selected_plant_id = st.selectbox(
        "Select Active Plant Timeline:",
        options=list(plant_options.keys()),
        format_func=lambda pid: plant_options[pid],
    )
    
    selected_plant = next(p for p in tracked_plants if p["id"] == selected_plant_id)
    observations = fetch_plant_observations(selected_plant_id)
    
    st.write("")
    render_card_start(f"Timeline History: {selected_plant['name']}", badge_text=f"{len(observations)} Observations", badge_variant="forest")
    
    if observations:
        for obs in observations:
            obs_date = obs.get("observed_on", "")
            rec_type = obs.get("record_type", "user_observation")
            notes = obs.get("notes", "")
            pred = obs.get("predicted_class")
            conf = obs.get("confidence")
            img_file = obs.get("image_filename")
            
            t_col1, t_col2 = st.columns([1.5, 1.0])
            with t_col1:
                badge_type = render_badge("AI Diagnostic Scan", "forest") if pred else render_badge("Field Observation", "neutral")
                st.markdown(f"**Date:** `{obs_date}` · {badge_type}", unsafe_allow_html=True)
                if pred:
                    clean_pred = pred.replace("___", " - ").replace("_", " ")
                    st.markdown(f"**Diagnosis:** `{clean_pred}` ({conf*100:.1f}% confidence)")
                st.write(notes)
                
            with t_col2:
                if img_file:
                    try:
                        img_path = get_plant_timeline_image_path(img_file)
                        st.image(str(img_path), caption="Consented Retained Photo", use_container_width=True)
                    except Exception:
                        st.caption("Photo retained but file missing.")
                else:
                    st.caption("No photo retained for this entry.")
            st.divider()
    else:
        st.info("No dated observations recorded yet for this plant.")
    render_card_end()

    # Add observation form
    render_card_start("Record New Dated Observation", badge_text="Add Log", badge_variant="emerald")
    with st.form("add_observation_form"):
        obs_date_input = st.date_input("Observation Date:", value=date.today())
        obs_notes_input = st.text_area("Field Notes & Observations:", placeholder="e.g. Leaf spot symptoms spreading to adjacent foliage; yellowing visible.")
        user_affected = st.checkbox("I observe foliar disease symptoms today", value=False)
        obs_submit = st.form_submit_button("Save Observation", type="primary")
        
        if obs_submit:
            if not obs_notes_input.strip():
                st.error("Observation notes are required.")
            else:
                add_plant_observation(
                    plant_id=selected_plant_id,
                    observed_on=str(obs_date_input),
                    notes=obs_notes_input,
                    user_marked_affected=user_affected,
                    record_type="user_observation",
                )
                st.success("Observation saved to timeline!")
                st.rerun()
    render_card_end()

render_about_footer()
