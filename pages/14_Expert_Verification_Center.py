"""Expert Verification Center - CropShield AI 2.0 Agronomist Verification Portal."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.cropshield.footer import render_about_footer
from src.cropshield.history import (
    create_expert_review,
    fetch_all_predictions,
    list_expert_reviews,
)
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
    st.set_page_config(page_title="Expert Verification Center - CropShield AI 2.0", page_icon="🧑‍🌾", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("expert_verification", language),
    subtitle="Agronomist review queue, AI diagnosis confirmation, expert oversight, and certified laboratory dossiers.",
    tag="Decision Support",
)

st.info(
    "Human-in-the-loop oversight is foundational to CropShield AI. Predictions remain strictly preliminary "
    "until reviewed and confirmed by an accredited agronomist or plant pathologist."
)

predictions = fetch_all_predictions(limit=50)
reviews = list_expert_reviews()

# ---------------------------------------------------------
# Verification KPIs
# ---------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
total_reviewed = len(reviews)
confirmed_count = sum(1 for r in reviews if r.get("status") == "Confirmed")
corrected_count = sum(1 for r in reviews if r.get("status") == "Corrected / Overridden")
pending_scans = max(0, len(predictions) - total_reviewed)

k1.metric("Total AI Scans", f"{len(predictions)}")
k2.metric("Expert Verified", f"{confirmed_count}", delta="Certified")
k3.metric("Expert Overrides", f"{corrected_count}", delta="Corrected", delta_color="off")
k4.metric("Pending Expert Review", f"{pending_scans}", delta="Review Queue", delta_color="off")

st.write("")

# ---------------------------------------------------------
# Review Form & Queue
# ---------------------------------------------------------
tab_review, tab_history = st.tabs(["Perform Expert Review", "Certified Review History"])

with tab_review:
    render_card_start("Review Diagnostic Scan Queue", badge_text="Agronomist Portal", badge_variant="emerald")
    if predictions:
        pred_options = {
            p["id"]: f"Scan #{p['id']} — {p['predicted_class'].replace('___', ' - ').replace('_', ' ')} ({p['confidence']*100:.1f}%) [{p['timestamp'][:10]}]"
            for p in predictions
        }
        selected_pred_id = st.selectbox("Select Scan to Review:", options=list(pred_options.keys()), format_func=lambda pid: pred_options[pid])
        selected_pred = next(p for p in predictions if p["id"] == selected_pred_id)
        
        c_left, c_right = st.columns(2)
        with c_left:
            st.markdown(f"**AI Preliminary Diagnosis:** `{selected_pred['predicted_class']}`")
            st.markdown(f"**Model Confidence:** `{selected_pred['confidence']*100:.1f}%`")
            st.markdown(f"**Calibrated Trust:** `{selected_pred.get('trust_level', 'Cannot Assess')}`")
            st.markdown(f"**Field User Notes:** {selected_pred.get('user_notes') or 'None entered'}")
            
        with c_right:
            with st.form("expert_review_form"):
                agronomist_name = st.text_input("Agronomist / Reviewer Name:", placeholder="e.g. Dr. Ramesh Kumar, KVK Extension")
                review_status = st.selectbox("Verification Verdict:", ["Confirmed", "Corrected / Overridden", "Inconclusive / Sample Required", "Rejected (Quality)"])
                expert_notes = st.text_area("Pathology Findings & Verification Notes:", placeholder="Enter morphological observations, lesion patterns, and validation details.")
                rec_action = st.text_input("Recommended Agronomic Action:", placeholder="e.g. Apply copper hydroxide; adjust row spacing.")
                
                submit_review = st.form_submit_button("Submit Verification Record", type="primary", use_container_width=True)
                
            if submit_review:
                if not agronomist_name.strip() or not expert_notes.strip():
                    st.error("Agronomist name and findings notes are required.")
                else:
                    create_expert_review(
                        prediction_id=selected_pred_id,
                        plant_id=None,
                        agronomist_name=agronomist_name,
                        status=review_status,
                        expert_notes=expert_notes,
                        recommended_action=rec_action,
                    )
                    st.success("Expert verification submitted and logged to audit trail!")
                    st.rerun()
    else:
        st.info("No AI scans recorded in queue.")
    render_card_end()

with tab_history:
    render_card_start("Certified Agronomist Review Archive", badge_text=f"{len(reviews)} Reviews", badge_variant="forest")
    if reviews:
        review_rows = []
        for r in reviews:
            review_rows.append({
                "Review ID": r["id"],
                "Scan Ref": f"#{r.get('prediction_id') or 'N/A'}",
                "Agronomist": r["agronomist_name"],
                "Verdict": r["status"],
                "Expert Notes": r["expert_notes"][:60] + "..." if len(r["expert_notes"]) > 60 else r["expert_notes"],
                "Date": r["created_at"][:19].replace("T", " "),
            })
        st.dataframe(pd.DataFrame(review_rows), use_container_width=True, hide_index=True)
    else:
        st.info("No expert verification records logged yet.")
    render_card_end()

render_about_footer()
