"""Tests for Open-Meteo weather integration and epidemiological risk rules."""

from __future__ import annotations

from src.cropshield.weather import (
    DEFAULT_LOCATIONS,
    DISEASE_EPIDEMIOLOGY_RULES,
    assess_weather_disease_risk,
    fetch_live_weather,
)


def test_default_locations_validity():
    assert "Bengaluru, Karnataka" in DEFAULT_LOCATIONS
    lat, lon = DEFAULT_LOCATIONS["Bengaluru, Karnataka"]
    assert 12.0 < lat < 14.0
    assert 76.0 < lon < 78.0


def test_assess_weather_disease_risk_optimal_conditions():
    # Warm + humid + wet conditions should trigger high early blight risk
    mock_weather = {
        "status": "success",
        "temperature": 26.5,
        "humidity": 88.0,
        "precipitation": 2.4,
    }
    risks = assess_weather_disease_risk(mock_weather)
    assert len(risks) >= 3

    early_blight = next((r for r in risks if r["disease_key"] == "Tomato___Early_blight"), None)
    assert early_blight is not None
    assert early_blight["risk_level"] == "High Risk"
    assert "Alternaria" in early_blight["disease_name"]
    assert "overhead irrigation" in early_blight["advisory"].lower()


def test_assess_weather_disease_risk_cool_damp_late_blight():
    # Cool + high humidity conditions trigger Late blight risk
    mock_weather = {
        "status": "success",
        "temperature": 18.0,
        "humidity": 92.0,
        "precipitation": 1.5,
    }
    risks = assess_weather_disease_risk(mock_weather)
    late_blight = next((r for r in risks if r["disease_key"] == "Tomato___Late_blight"), None)
    assert late_blight is not None
    assert late_blight["risk_level"] == "High Risk"
    assert "Phytophthora" in late_blight["disease_name"]


def test_assess_weather_disease_risk_offline_fallback():
    mock_weather = {
        "status": "unavailable",
        "error": "Network timeout",
    }
    risks = assess_weather_disease_risk(mock_weather)
    assert risks == []
