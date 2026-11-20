# CropShield AI 2.0 Deployment & Operations Guide

## 1. Local Production Deployment

CropShield AI 2.0 is designed to run efficiently on smallholder edge workstations, cooperative field computers, and farm management systems without mandatory cloud infrastructure.

### Recommended System Specifications
- **Operating System:** Windows 11 (64-bit) / Ubuntu 22.04 LTS / macOS 13+
- **Memory:** 8 GB RAM minimum (operates comfortably within 2–4 GB active RAM)
- **GPU Accelerator:** NVIDIA GeForce GTX 1650 4 GB (CUDA optional) or Intel/AMD multicore CPU
- **Python Version:** Python 3.13 or 3.14 (64-bit)

### Installation & Launch Commands

```powershell
# 1. Open Windows PowerShell in project root
cd CropShield_AI_-2.0-main

# 2. Create and activate dedicated virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3. Upgrade pip and install pinned dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt

# 4. Launch CropShield AI 2.0 Platform
python -m streamlit run app.py --server.port 8501 --server.address localhost
```

The interface will be accessible at `http://localhost:8501`.

---

## 2. Micro-Climate Telemetry Configuration

CropShield AI 2.0 integrates **zero-key live meteorological telemetry** via the Open-Meteo Global WMO Forecast API:
- Endpoint: `https://api.open-meteo.com/v1/forecast`
- Telemetry Collected: Real-time 2m temperature (°C), relative humidity (%), apparent temperature, precipitation (mm), and wind speed (km/h).
- Privacy: No user location is transmitted to proprietary servers; only geographic coordinates of the target farm are queried.
- Offline Fallback: If external connectivity is interrupted, the platform withholds speculative risk scoring and clearly displays an `Offline/Unreachable` status banner without fabricating synthetic weather data.

---

## 3. Verified Extension Contacts Directory

CropShield AI 2.0 provides verified Indian agricultural extension and emergency helpline numbers directly in the interface:
- **Kisan Call Centre (GoI):** Toll-Free `1800-180-1551` (06:00 AM – 10:00 PM, 22 official languages)
- **ICAR - Indian Agricultural Research Institute (IARI):** New Delhi 110012 · +91-11-25841471
- **ICAR - Indian Institute of Horticultural Research (IIHR):** Hessaraghatta, Bengaluru 560089 · +91-80-23086100
- **Tamil Nadu Agricultural University (TNAU):** Coimbatore 641003
- **University of Agricultural Sciences (UAS):** GKVK, Bengaluru 560065

---

## 4. Edge Model Export (TensorFlow Lite)

For mobile and edge embedded hardware:
```powershell
# Convert trained Keras model into optimized TFLite format
python scripts/export_tflite.py
```
This produces `models/crop_model.tflite` for low-latency CPU and microcontroller inference.
