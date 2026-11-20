"""Reports & Export Center - CropShield AI 2.0 Enterprise Diagnostics."""

from __future__ import annotations

import datetime
import html
import io
import json
import streamlit as st
import pandas as pd

from src.cropshield.config import LABELS_PATH, MODEL_PATH, MODELS_DIR
from src.cropshield.footer import render_about_footer
from src.cropshield.history import (
    fetch_all_predictions,
    list_farms,
    list_plots,
    get_recent_batch_scans,
)
from src.cropshield.model import load_labels
from src.cropshield.readiness import load_model_details
from src.cropshield.translations import translate
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
    title=translate("reports_export_center", language),
    subtitle="Generate certified diagnostic audit sheets, export surveillance telemetry, and download research bundles.",
    tag="CropShield AI 2.0",
)

tab_report, tab_csv, tab_json = st.tabs(
    ["📄 Diagnostic Audit Report", "📊 Surveillance Telemetry CSV", "🔬 Research Data Bundle"]
)

predictions = fetch_all_predictions(limit=500)
farms = list_farms()
plots = list_plots()
labels = load_labels(LABELS_PATH) if LABELS_PATH.is_file() else []
model_meta = load_model_details()

# =========================================================
# TAB 1: Diagnostic Audit Report Generator
# =========================================================
with tab_report:
    render_card_start("Diagnostic Audit Sheet Generator", "Printable", "emerald")
    st.markdown(
        "Generate a formal agronomic diagnosis report suitable for farmer advisory, "
        "insurance documentation, or cooperative certification."
    )

    if not predictions:
        st.info("No scan records found in the database. Perform a scan in AI Crop Scanner to generate reports.")
    else:
        # Build selection dropdown
        pred_options = {
            f"#{p['id']} - {p['prediction']} ({p['confidence']:.1%}) on {p['timestamp'][:19]}": p
            for p in predictions[:50]
        }
        selected_key = st.selectbox("Select Diagnostic Record to Certify:", list(pred_options.keys()))
        selected_record = pred_options[selected_key]

        col_f1, col_f2 = st.columns(2)
        with col_f1:
            inspector_name = st.text_input("Lead Agronomist / Field Officer:", value="Dr. Ramesh Patil, Field Agronomist")
            license_no = st.text_input("Agronomist Certification / License No.:", value="ICAR-KA-2024-8841")
        with col_f2:
            org_name = st.text_input("Issuing Institution / Co-op:", value="District Krishi Vigyan Kendra (KVK)")
            notes = st.text_area("Field Observations / Clinical Notes:", value="Leaf lesions consistent with early stage fungal infection. Immediate cultural hygiene recommended.")

        # Build printable HTML
        scan_id = selected_record["id"]
        crop = selected_record.get("crop", "Tomato")
        pred_label = selected_record.get("prediction", "Unknown")
        conf = selected_record.get("confidence", 0.0)
        calibrated_score = selected_record.get("calibrated_score", conf)
        trust_level = selected_record.get("trust_level", "Medium")
        scan_time = selected_record.get("timestamp", datetime.datetime.now().isoformat())
        farm_name = selected_record.get("farm_name", "Registered Plot")
        plot_name = selected_record.get("plot_name", "Plot 1")

        report_html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>CropShield AI 2.0 - Diagnostic Audit Report #{scan_id}</title>
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif; color: #1E293B; background: #FFF; padding: 40px; margin: 0; }}
    .header {{ border-bottom: 3px solid #1B4332; padding-bottom: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-start; }}
    .brand {{ font-size: 24px; font-weight: 800; color: #1B4332; letter-spacing: -0.5px; }}
    .doc-type {{ font-size: 14px; text-transform: uppercase; color: #2D6A4F; font-weight: 700; letter-spacing: 1px; margin-top: 4px; }}
    .meta-box {{ text-align: right; font-size: 13px; color: #64748B; }}
    .section-title {{ font-size: 16px; font-weight: 750; color: #1B4332; border-bottom: 1px solid #E2E8F0; padding-bottom: 6px; margin-top: 24px; margin-bottom: 12px; }}
    table {{ width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 14px; }}
    th, td {{ padding: 10px 14px; text-align: left; border: 1px solid #E2E8F0; }}
    th {{ background: #F8F9FA; font-weight: 650; color: #334155; width: 30%; }}
    .badge {{ display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 12px; font-weight: 700; }}
    .badge-high {{ background: #D1FAE5; color: #065F46; }}
    .badge-med {{ background: #FEF3C7; color: #92400E; }}
    .badge-low {{ background: #FEE2E2; color: #991B1B; }}
    .sign-off {{ margin-top: 40px; display: flex; justify-content: space-between; }}
    .sign-box {{ width: 45%; border-top: 1px dashed #94A3B8; padding-top: 8px; font-size: 13px; color: #475569; }}
    .disclaimer {{ margin-top: 32px; font-size: 11px; color: #94A3B8; line-height: 1.4; border-top: 1px solid #F1F5F9; padding-top: 12px; }}
</style>
</head>
<body>
    <div class="header">
        <div>
            <div class="brand">CropShield AI 2.0</div>
            <div class="doc-type">Certified Crop Diagnostic Audit Report</div>
            <div style="font-size: 13px; color: #475569; margin-top: 2px;">{html.escape(org_name)}</div>
        </div>
        <div class="meta-box">
            <div><strong>Report Ref:</strong> CS2-CERT-{scan_id:06d}</div>
            <div><strong>Issue Date:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</div>
            <div><strong>Original Scan:</strong> {scan_time[:19].replace('T', ' ')}</div>
        </div>
    </div>

    <div class="section-title">1. Specimen & Location Profile</div>
    <table>
        <tr><th>Target Crop</th><td><strong>{html.escape(str(crop))}</strong></td></tr>
        <tr><th>Registered Farm</th><td>{html.escape(str(farm_name))}</td></tr>
        <tr><th>Field Plot / Sector</th><td>{html.escape(str(plot_name))}</td></tr>
        <tr><th>Diagnostic Pipeline</th><td>MobileNetV2 Transfer Learning + Grad-CAM Explainability</td></tr>
    </table>

    <div class="section-title">2. Computer Vision Diagnostic Findings</div>
    <table>
        <tr><th>Primary Classification</th><td><span style="font-size:16px; font-weight:750; color:#1B4332;">{html.escape(str(pred_label))}</span></td></tr>
        <tr><th>Model Raw Confidence</th><td>{conf:.2%}</td></tr>
        <tr><th>Validation-Calibrated Confidence</th><td>{calibrated_score:.2%}</td></tr>
        <tr><th>Diagnostic Trust Index</th><td><span class="badge badge-{ 'high' if trust_level == 'High' else ('med' if trust_level == 'Medium' else 'low') }">{html.escape(str(trust_level))} Trust</span></td></tr>
    </table>

    <div class="section-title">3. Agronomic Assessment & Notes</div>
    <div style="background:#F8F9FA; border:1px solid #E2E8F0; padding:12px; border-radius:6px; font-size:13px; line-height:1.5; margin-bottom:16px;">
        {html.escape(notes)}
    </div>

    <div class="sign-off">
        <div class="sign-box">
            <strong>Certified Field Agronomist:</strong><br>
            {html.escape(inspector_name)}<br>
            License: {html.escape(license_no)}<br>
            Signature: _______________________
        </div>
        <div class="sign-box">
            <strong>Farm Manager / Cultivator:</strong><br>
            Acknowledgment of Protocol Received<br>
            Date: ___________________________<br>
            Signature: _______________________
        </div>
    </div>

    <div class="disclaimer">
        <strong>Governance & Statutory Notice:</strong> CropShield AI 2.0 decision-support outputs are calibrated using historical research datasets (PlantVillage / ICAR-IARI). Computer vision inferences provide advisory triage and do not constitute statutory certification. Always cross-verify chemical dosages with your regional Krishi Vigyan Kendra (KVK) or extension specialist prior to tank mixing.
    </div>
</body>
</html>"""

        st.subheader("Report Preview")
        st.components.v1.html(report_html, height=520, scrolling=True)

        st.download_button(
            label="📥 Download Certified HTML Audit Report",
            data=report_html,
            file_name=f"cropshield_audit_report_{scan_id}.html",
            mime="text/html",
        )
    render_card_end()

# =========================================================
# TAB 2: Surveillance Telemetry CSV Export
# =========================================================
with tab_csv:
    render_card_start("Surveillance Telemetry Datasets", "Export", "forest")
    st.markdown("Download longitudinal diagnostic records and batch telemetry in standard tabular format.")

    sub_t1, sub_t2, sub_t3 = st.tabs(["Diagnostic Records", "Batch Scans", "Farm Directory"])

    with sub_t1:
        if predictions:
            df_preds = pd.DataFrame(predictions)
            st.dataframe(df_preds.head(20), use_container_width=True)
            csv_preds = df_preds.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Diagnostic Records CSV",
                data=csv_preds,
                file_name=f"cropshield_predictions_{datetime.date.today().isoformat()}.csv",
                mime="text/csv",
            )
        else:
            st.info("No prediction telemetry currently available.")

    with sub_t2:
        batches = get_recent_batch_scans(limit=100)
        if batches:
            df_batch = pd.DataFrame(batches)
            st.dataframe(df_batch, use_container_width=True)
            csv_batch = df_batch.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Batch Scans Telemetry CSV",
                data=csv_batch,
                file_name=f"cropshield_batch_scans_{datetime.date.today().isoformat()}.csv",
                mime="text/csv",
            )
        else:
            st.info("No batch scan logs recorded.")

    with sub_t3:
        if farms or plots:
            df_farms = pd.DataFrame(farms) if farms else pd.DataFrame()
            df_plots = pd.DataFrame(plots) if plots else pd.DataFrame()
            st.write("Farms Registered:")
            st.dataframe(df_farms, use_container_width=True)
            st.write("Plots Registered:")
            st.dataframe(df_plots, use_container_width=True)

            out_buffer = io.StringIO()
            if not df_plots.empty:
                df_plots.to_csv(out_buffer, index=False)
            st.download_button(
                "📥 Download Plot Inventory CSV",
                data=out_buffer.getvalue().encode("utf-8"),
                file_name=f"cropshield_plots_{datetime.date.today().isoformat()}.csv",
                mime="text/csv",
            )
        else:
            st.info("No farm or plot profiles registered.")
    render_card_end()

# =========================================================
# TAB 3: Research Diagnostic Bundle JSON
# =========================================================
with tab_json:
    render_card_start("Academic & Research Diagnostic Bundle", "JSON", "blue")
    st.markdown(
        "Export a machine-readable JSON bundle containing system configurations, "
        "class mappings, evaluation metrics, and sanitized diagnostic telemetry."
    )

    bundle = {
        "platform": "CropShield AI 2.0",
        "exported_at": datetime.datetime.now().isoformat(),
        "model_architecture": model_meta.get("name", "MobileNetV2-Transfer"),
        "model_version": model_meta.get("version", "3.0.0"),
        "evaluation_metrics": model_meta.get("metrics", {}),
        "supported_classes": labels,
        "sample_records": predictions[:100],
        "farms_count": len(farms),
        "plots_count": len(plots),
    }

    json_str = json.dumps(bundle, indent=2, default=str)
    st.code(json_str[:1200] + "\n\n... (truncated for preview)", language="json")

    st.download_button(
        "📥 Download Research Diagnostic Bundle (.json)",
        data=json_str.encode("utf-8"),
        file_name=f"cropshield_research_bundle_{datetime.date.today().isoformat()}.json",
        mime="application/json",
    )
    render_card_end()

render_about_footer()
