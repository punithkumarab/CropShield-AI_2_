"""Real-time weather retrieval and epidemiological disease risk assessment for CropShield AI 2.0."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import logging
from typing import Any
import urllib.error
import urllib.request

LOGGER = logging.getLogger(__name__)

# Authoritative agricultural coordinates across key Indian farming hubs
DEFAULT_LOCATIONS = {
    "Bengaluru, Karnataka": (12.9716, 77.5946),
    "Pune (Maharashtra)": (18.5204, 73.8567),
    "Varanasi (Uttar Pradesh)": (25.3176, 82.9739),
    "Ludhiana (Punjab)": (30.9010, 75.8573),
    "Coimbatore (Tamil Nadu)": (11.0168, 76.9558),
    "Shimla (Himachal Pradesh)": (31.1048, 77.1734),
    "Anand (Gujarat)": (22.5645, 72.9289),
}

# Verified epidemiological risk profiles for Tomato and crop diseases
DISEASE_EPIDEMIOLOGY_RULES = {
    "Tomato___Early_blight": {
        "disease_name": "Early Blight (Alternaria solani)",
        "optimal_temp_range": (24.0, 30.0),
        "min_humidity": 80.0,
        "wet_weather_factor": True,
        "advisory": "High humidity combined with warm temperatures accelerates Alternaria spore germination. Avoid overhead irrigation and ensure plant canopy spacing.",
    },
    "Tomato___Late_blight": {
        "disease_name": "Late Blight (Phytophthora infestans)",
        "optimal_temp_range": (15.0, 22.0),
        "min_humidity": 85.0,
        "wet_weather_factor": True,
        "advisory": "Cool, prolonged wet conditions create severe Late Blight risk. Monitor lower foliage closely and improve soil drainage.",
    },
    "Tomato___Bacterial_spot": {
        "disease_name": "Bacterial Spot (Xanthomonas)",
        "optimal_temp_range": (24.0, 32.0),
        "min_humidity": 75.0,
        "wet_weather_factor": True,
        "advisory": "Warm temperatures with splashing rain or wind-driven moisture spread bacterial pathogens rapidly. Sanitize pruning equipment.",
    },
    "Tomato___Septoria_leaf_spot": {
        "disease_name": "Septoria Leaf Spot (Septoria lycopersici)",
        "optimal_temp_range": (20.0, 26.0),
        "min_humidity": 80.0,
        "wet_weather_factor": True,
        "advisory": "Moderate temperatures and frequent leaf wetness favor Septoria spot progression. Remove affected lower leaves.",
    },
}


def fetch_live_weather(latitude: float, longitude: float) -> dict[str, Any]:
    """Retrieve real-time weather from Open-Meteo API without external API keys."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m"
        f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=auto"
    )
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "CropShield-AI-3.0/Agricultural-Platform (https://github.com)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode("utf-8"))
                current = data.get("current", {})
                return {
                    "status": "success",
                    "source": "Open-Meteo Live API",
                    "retrieved_at": datetime.now(timezone.utc).isoformat(),
                    "latitude": latitude,
                    "longitude": longitude,
                    "temperature": float(current.get("temperature_2m", 0.0)),
                    "humidity": float(current.get("relative_humidity_2m", 0.0)),
                    "apparent_temperature": float(current.get("apparent_temperature", 0.0)),
                    "precipitation": float(current.get("precipitation", 0.0)),
                    "wind_speed": float(current.get("wind_speed_10m", 0.0)),
                }
    except (urllib.error.URLError, TimeoutError, ValueError, OSError) as exc:
        LOGGER.warning("Could not retrieve live weather from Open-Meteo: %s", exc)

    return {
        "status": "unavailable",
        "source": "Open-Meteo Live API (Offline/Unreachable)",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "latitude": latitude,
        "longitude": longitude,
        "error": "Real-time weather data is temporarily unreachable. No simulated weather data is generated.",
    }


def assess_weather_disease_risk(weather_data: dict[str, Any]) -> list[dict[str, Any]]:
    """Evaluate weather conditions against verified epidemiological disease rules."""
    if weather_data.get("status") != "success":
        return []

    temp = weather_data.get("temperature", 0.0)
    humidity = weather_data.get("humidity", 0.0)
    precip = weather_data.get("precipitation", 0.0)

    assessments = []
    for class_key, rule in DISEASE_EPIDEMIOLOGY_RULES.items():
        min_temp, max_temp = rule["optimal_temp_range"]
        temp_match = min_temp <= temp <= max_temp
        humidity_match = humidity >= rule["min_humidity"]
        rain_match = precip > 0.1 if rule["wet_weather_factor"] else True

        if temp_match and humidity_match and rain_match:
            risk_level = "High Risk"
            explanation = (
                f"Current temperature ({temp:.1f}°C) and relative humidity ({humidity:.0f}%) "
                f"fall directly within the optimal pathogen proliferation window ({min_temp}-{max_temp}°C, >{rule['min_humidity']:.0f}%)."
            )
        elif temp_match and (humidity_match or humidity >= rule["min_humidity"] - 10.0):
            risk_level = "Moderate Risk"
            explanation = (
                f"Temperature ({temp:.1f}°C) is favorable, with humidity approaching critical threshold ({humidity:.0f}%)."
            )
        else:
            risk_level = "Low Risk"
            explanation = (
                f"Current ambient conditions ({temp:.1f}°C, {humidity:.0f}% humidity) are unfavorable for rapid spore development."
            )

        assessments.append(
            {
                "disease_key": class_key,
                "disease_name": rule["disease_name"],
                "risk_level": risk_level,
                "explanation": explanation,
                "advisory": rule["advisory"],
            }
        )

    return assessments
