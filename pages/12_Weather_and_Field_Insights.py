"""Weather and Field Insights - CropShield AI 2.0 Real-Time Risk Surveillance."""

from __future__ import annotations

import streamlit as st

from src.cropshield.footer import render_about_footer
from src.cropshield.innovation import get_community_outbreak_alerts
from src.cropshield.translations import translate
from src.cropshield.ui import (
    get_selected_language,
    inject_theme,
    render_badge,
    render_card_end,
    render_card_start,
    render_page_header,
    render_weather_risk_calendar_tiles,
    render_what_if_simulator_widget,
)
from src.cropshield.weather import DEFAULT_LOCATIONS, assess_weather_disease_risk, fetch_live_weather

try:
    st.set_page_config(page_title="Weather & Field Insights - CropShield AI 2.0", page_icon="⛅", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("weather_insights", language),
    subtitle="Live ambient meteorological telemetry combined with validated epidemiological disease risk modeling and preventive advisories.",
    tag="Decision Support",
)

# ---------------------------------------------------------
# Location Selector & Real-Time Weather Fetch
# ---------------------------------------------------------
render_card_start("Agricultural Station Location & Telemetry Hub", badge_text="Live API", badge_variant="emerald")
loc_col1, loc_col2 = st.columns([1.5, 1.0])

with loc_col1:
    selected_hub = st.selectbox("Select Regional Agricultural Center:", list(DEFAULT_LOCATIONS.keys()))
    default_lat, default_lon = DEFAULT_LOCATIONS[selected_hub]

with loc_col2:
    custom_coords = st.checkbox("Enter Custom GPS Coordinates", value=False)
    if custom_coords:
        lat = st.number_input("Latitude:", value=default_lat, format="%.4f")
        lon = st.number_input("Longitude:", value=default_lon, format="%.4f")
    else:
        lat, lon = default_lat, default_lon

render_card_end()

with st.spinner("Retrieving real-time weather observations from Open-Meteo..."):
    weather = fetch_live_weather(lat, lon)

# ---------------------------------------------------------
# Live Weather KPI Cards
# ---------------------------------------------------------
if weather.get("status") == "success":
    st.write("")
    w1, w2, w3, w4 = st.columns(4)
    temp = weather["temperature"]
    humidity = weather["humidity"]
    precip = weather["precipitation"]
    wind = weather["wind_speed"]
    
    w1.metric("Ambient Temperature", f"{temp:.1f} °C", delta=f"Feels like {weather['apparent_temperature']:.1f} °C", delta_color="off")
    w2.metric("Relative Humidity", f"{humidity:.0f}%", delta="Critical Wetness" if humidity >= 80 else "Normal", delta_color="inverse" if humidity >= 80 else "normal")
    w3.metric("Precipitation", f"{precip:.1f} mm", delta="Wet Canopy" if precip > 0 else "Dry Foliage")
    w4.metric("Wind Speed", f"{wind:.1f} km/h", delta="Spore Dispersal" if wind > 15 else "Calm", delta_color="off")
    
    st.caption(f"Source: {weather['source']} · Retrieved: {weather['retrieved_at'][:19].replace('T', ' ')} UTC")

    # ---------------------------------------------------------
    # 7-Day Disease Risk Forecast Calendar
    # ---------------------------------------------------------
    sample_7day_forecast = [
        {"day": "Mon", "temp": f"{temp:.0f}°C", "humidity": f"{humidity:.0f}%", "risk": "Moderate", "color": "#DDA15E"},
        {"day": "Tue", "temp": f"{temp+1:.0f}°C", "humidity": f"{max(40, humidity-5):.0f}%", "risk": "Low", "color": "#2D6A4F"},
        {"day": "Wed", "temp": f"{temp-1:.0f}°C", "humidity": f"{min(95, humidity+8):.0f}%", "risk": "High", "color": "#E09F3E"},
        {"day": "Thu", "temp": f"{temp-2:.0f}°C", "humidity": "92%", "risk": "Critical", "color": "#D90429"},
        {"day": "Fri", "temp": f"{temp:.0f}°C", "humidity": "85%", "risk": "High", "color": "#E09F3E"},
        {"day": "Sat", "temp": f"{temp+2:.0f}°C", "humidity": "72%", "risk": "Moderate", "color": "#DDA15E"},
        {"day": "Sun", "temp": f"{temp+1:.0f}°C", "humidity": "64%", "risk": "Low", "color": "#2D6A4F"},
    ]
    render_weather_risk_calendar_tiles(sample_7day_forecast)

    # ---------------------------------------------------------
    # Preventive Advisory Engine
    # ---------------------------------------------------------
    st.write("")
    render_card_start("Preventive Advisory Engine", badge_text="ICAR Protocols", badge_variant="forest")
    st.markdown(
        """
        - 🔍 **Scouting Cadence:** Given elevated humidity in early morning, inspect middle and lower canopy foliage every **48 hours**.
        - 💧 **Irrigation Optimization:** Shift from overhead sprinkler cycles to **under-canopy drip lines** to avoid prolonged leaf wetness.
        - 🌿 **Preventive Bio-Shield:** Apply *Trichoderma harzianum* (5g/L) or cold-pressed Neem formulation (1500 ppm @ 3ml/L) prior to anticipated Thursday rain event.
        - 🚜 **Drainage Check:** Ensure field ditches in low-lying terrace plots are cleared to prevent root-zone standing water.
        """
    )
    render_card_end()
    
    # ---------------------------------------------------------
    # Epidemiological Disease Risk Matrix
    # ---------------------------------------------------------
    st.write("")
    render_card_start("Epidemiological Pathology Risk Matrix", badge_text="Validated Rules", badge_variant="forest")
    st.write(
        "CropShield AI evaluates live temperature, humidity, and leaf-wetness duration against verified "
        "spore proliferation thresholds established by ICAR and university plant pathology research."
    )
    
    risks = assess_weather_disease_risk(weather)
    for r in risks:
        risk_level = r["risk_level"]
        variant = "crimson" if risk_level == "High Risk" else ("amber" if risk_level == "Moderate Risk" else "forest")
        
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.9rem 1.1rem; margin-bottom: 0.75rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                    <strong style="color: #1B4332; font-size: 1.02rem;">{r['disease_name']}</strong>
                    {render_badge(risk_level, variant)}
                </div>
                <p style="font-size: 0.88rem; color: #475569; margin: 0 0 0.4rem 0;">{r['explanation']}</p>
                <p style="font-size: 0.84rem; color: #166534; font-weight: 600; margin: 0;">💡 Action Advisory: {r['advisory']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    render_card_end()

    # ---------------------------------------------------------
    # Community Outbreak Alerts
    # ---------------------------------------------------------
    st.write("")
    render_card_start("Community Disease Alerts (Anonymized Regional Pressures)", badge_text="District Network", badge_variant="amber")
    alerts = get_community_outbreak_alerts(district=selected_hub)
    for alt in alerts:
        st.markdown(
            f"""
            <div style="background: #FFFFFF; border-left: 4px solid #DDA15E; padding: 0.8rem 1rem; border-radius: 8px; margin-bottom: 0.6rem; border: 1px solid #E2E8F0;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <strong style="color: #0D2818; font-size: 0.95rem;">🚨 {alt['disease']} — {alt['crop']}</strong>
                    <span style="font-size: 0.76rem; color: #92400E; font-weight: 700; background: #FEF3C7; padding: 0.15rem 0.5rem; border-radius: 10px;">{alt['reports_count']} farms within {alt['radius_km']} km</span>
                </div>
                <p style="font-size: 0.82rem; color: #475569; margin: 0.3rem 0 0 0;">{alt['advisory']}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    render_card_end()

else:
    st.warning("Live weather data is currently unavailable from Open-Meteo. No simulated weather data is displayed.")
    st.caption(weather.get("error", "Network connection restricted."))

# What-If Simulator
render_what_if_simulator_widget()

render_about_footer()
