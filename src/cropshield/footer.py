"""Shared "About Me" page footer rendered at the bottom of every page."""

import streamlit as st

from src.cropshield.ui import inject_theme, render_language_selector

_FOOTER_HTML = """
<div style="margin-top:3rem;padding-top:2rem;border-top:1px solid #E2E8F0;text-align:center;">
    <div style="display:flex;justify-content:center;gap:36px;margin-bottom:1.25rem;">
        <a href="https://github.com/punithkumarab" target="_blank" style="color:#1B4332;font-size:0.88rem;font-weight:700;text-decoration:none;letter-spacing:0.04em;">GitHub &nearr;</a>
        <a href="https://icar.org.in" target="_blank" style="color:#1B4332;font-size:0.88rem;font-weight:700;text-decoration:none;letter-spacing:0.04em;">ICAR Portal &nearr;</a>
        <a href="https://kvk.icar.gov.in" target="_blank" style="color:#1B4332;font-size:0.88rem;font-weight:700;text-decoration:none;letter-spacing:0.04em;">KVK Helplines &nearr;</a>
        <a href="https://open-meteo.com" target="_blank" style="color:#1B4332;font-size:0.88rem;font-weight:700;text-decoration:none;letter-spacing:0.04em;">Open-Meteo API &nearr;</a>
    </div>
    <p style="font-size:1.05rem;font-weight:650;color:#1B4332;margin-bottom:0.25rem;">Punith Kumar AB</p>
    <p style="color:#475569;font-size:0.9rem;margin-bottom:0.25rem;">
        Bachelor of Engineering in Artificial Intelligence and Machine Learning<br>
        G M Institute of Technology, Davanagere
    </p>
    <p style="margin-bottom:0.25rem;">
        <a href="mailto:punithkumar0927@gmail.com" style="color:#2D6A4F;text-decoration:none;font-weight:600;">&#9993; punithkumar0927@gmail.com</a>
        &nbsp;&nbsp;|&nbsp;&nbsp;
        <a href="https://github.com/punithkumarab" target="_blank" style="color:#2D6A4F;text-decoration:none;font-weight:600;">&#128736; GitHub Repository</a>
    </p>
    <p style="color:#64748B;font-size:0.8rem;margin-top:0.5rem;">CropShield AI 2.0 &mdash; Autonomous Precision Plant-Health Intelligence for Indian Agriculture.</p>
</div>
"""


def render_about_footer() -> None:
    render_language_selector()
    inject_theme()
    st.markdown(_FOOTER_HTML, unsafe_allow_html=True)


def stop_with_footer() -> None:
    """Render the footer, then stop the page (for early-exit branches)."""
    render_about_footer()
    st.stop()
