# CropShield AI 2.0 System Architecture & Engineering Specifications

## 1. High-Level Architecture Overview

CropShield AI 2.0 is an enterprise-grade agricultural decision support, crop health surveillance, and computer vision diagnostic platform. The system operates entirely on edge or local hardware (Windows 11, 8 GB RAM, NVIDIA GTX 1650 4 GB / CPU fallback) without mandatory cloud dependencies.

```text
Field Capture / Drone / Upload / Batch Ingestion
  │
  ├──► Pre-Flight Quality Gate (OpenCV Image Quality Assessment)
  │      ├─ Laplacian focus sharpness score (threshold >= 20.0)
  │      ├─ Exposure distribution (40 <= mean brightness <= 220)
  │      ├─ Specular glare detection (<= 15.0% saturated pixels)
  │      └─ HSV foliage contour extraction (green mask area >= 15%)
  │
  ├──► Diagnostic Computer Vision Engine (MobileNetV2 Transfer Learning)
  │      ├─ Ingestion: 224x224x3 RGB normalized tensor [0, 1]
  │      ├─ Inference: Softmax class probabilities + top-3 ranking
  │      ├─ Calibration: Temperature-scaled confidence thresholding
  │      └─ Explainability: Saliency map & Grad-CAM class activation overlay
  │
  ├──► Micro-Climate & Epidemiological Pathogen Risk Engine
  │      ├─ Ambient Telemetry: Open-Meteo Global WMO Forecast API (zero-key)
  │      ├─ Proliferation Matrix: Alternaria solani, Phytophthora infestans, Xanthomonas
  │      └─ Real-Time Risk Level: High / Moderate / Low Risk with ICAR advisories
  │
  ├──► Spatial Field & Cadastral Plot Management
  │      ├─ SQLite Relational Schema: Farms, Plots, Batch Scans, Expert Reviews
  │      ├─ Plant Timeline: Longitudinal recovery tracking with opt-in photo retention
  │      └─ GIS Spatial Map: Plot GPS markers with health status color coding
  │
  └──► Agronomic Governance & Extension Decision Intelligence
         ├─ Verified Knowledge Base: Indian Council of Agricultural Research (ICAR)
         ├─ AI Agricultural Assistant: Retrieval-grounded Q&A with source citations
         ├─ Certified Agronomist Review Queue: Human-in-the-loop audit trail
         └─ Audit Reports: Printable HTML audit sheets & CSV telemetry dumps
```

---

## 2. The 17 Core Application Modules

CropShield AI 2.0 is partitioned into four operational tiers:

### Tier 1: Core Diagnostic Suite
1. **Overview Dashboard (`1_Overview_Dashboard.py`):** Executive command center displaying active plot surveillance KPIs, calibrated model accuracy, recent pathogen detections, and interactive diagnostic action cards.
2. **AI Crop Scanner (`2_AI_Crop_Scanner.py`):** Single-leaf precision diagnostic studio with automatic camera/file quality gates, calibrated trust level metrics, top-3 ranked predictions, and real-time Grad-CAM attention heatmaps.
3. **Batch Image Analysis (`3_Batch_Image_Analysis.py`):** High-throughput bulk processing pipeline (up to 20 images) with memory-safe sequential micro-batch inference, pathogen breakdown distribution charts, and instant CSV telemetry export.
4. **Crop Health Intelligence (`4_Crop_Health_Intelligence.py`):** Longitudinal comparative pathology studio allowing side-by-side symptom progression tracking (Baseline vs. Follow-up) with delta severity analysis.
5. **Smart Photo Coach (`5_Smart_Photo_Coach.py`):** Live diagnostic pre-flight coach providing real-time Laplacian focus metrics, exposure thresholds, specular glare detection, and foliage mask contour extraction.

### Tier 2: Farm & Field Management
6. **Field and Plot Management (`6_Field_and_Plot_Management.py`):** Enterprise farm profile registry, sub-plot cadastral partitioning, soil and irrigation recording, and pathogen surveillance tier tagging.
7. **Plant Follow-up Timeline (`7_Plant_Follow_up_Timeline.py`):** Chronological specimen observation logging with strict opt-in photo retention and timeline history.
8. **Interactive Farm Map (`8_Interactive_Farm_Map.py`):** Spatial field GIS visualization with GPS coordinate plots, satellite coordinate mapping, and health status color-coding.
9. **Crop Analytics Center (`9_Crop_Analytics_Center.py`):** Longitudinal epidemiology tracking, confidence score histograms, trust index distributions, and temporal outbreak charts.

### Tier 3: Agronomic Decision Support
10. **Disease Knowledge Center (`10_Disease_Knowledge_Center.py`):** Authoritative extension encyclopedia covering Solanaceae and major crop pathogens, with symptom keys and ICAR source citations.
11. **AI Agricultural Assistant (`11_AI_Agricultural_Assistant.py`):** Retrieval-grounded agricultural Q&A assistant backed by verified extension datasets with zero hallucinations and local Ollama hooks.
12. **Weather and Field Insights (`12_Weather_and_Field_Insights.py`):** Zero-key real-time Open-Meteo ambient telemetry paired with verified epidemiological pathogen proliferation risk models.
13. **Treatment and Prevention Guide (`13_Treatment_and_Prevention_Guide.py`):** Tiered Integrated Pest Management (IPM) protocols with cultural, biological, and statutory chemical controls alongside PPE warnings.
14. **Expert Verification Center (`14_Expert_Verification_Center.py`):** Agronomist review queue for manual verification, human-in-the-loop diagnostic overrides, and certification archives.

### Tier 4: Engineering & Governance
15. **Model Performance and Explainability (`15_Model_Performance_and_Explainability.py`):** Test-set confusion matrix, per-class F1/precision/recall radar breakdowns, and Grad-CAM layer parameter inspection.
16. **Reports and Export Center (`16_Reports_and_Export_Center.py`):** Printable HTML agronomic diagnostic audit sheets, CSV prediction logs, batch telemetry dumps, and academic JSON bundles.
17. **Settings and Privacy (`17_Settings_and_Privacy.py`):** Multilingual localization (English, Kannada, Hindi), farmer data sovereignty toggles (opt-in photo retention), SQLite backups, and KVK emergency helplines.

---

## 3. Data Storage & Relational Schema (SQLite)

CropShield AI 2.0 utilizes local SQLite database persistence (`crop_history.db`) with zero remote telemetry leak:

- **`predictions`**: Longitudinal single-leaf diagnostic inference records, including calibrated trust index, top-3 ranked predictions JSON, inference latency in milliseconds, image quality metrics, and farm/plot foreign references.
- **`tracked_plants`**: Chronological specimen registration with plot coordinates and plant observations.
- **`plant_observations`**: Longitudinal observation log entries with opt-in image paths and clinical field notes.
- **`farms`**: Master agricultural enterprise registry with geographic location, total acreage, and primary crop cultivars.
- **`plots`**: Sub-plot sector partitions linked to parent farms with soil classification, irrigation infrastructure, and active surveillance status.
- **`batch_scans`**: High-throughput multi-image surveillance logs containing batch totals, healthy/diseased counts, and per-specimen predictions JSON.
- **`expert_reviews`**: Agronomist certification audit queue containing human-in-the-loop confirmations, clinical notes, and statutory chemical recommendations.

---

## 4. Agronomic Safety & Regulatory Disclaimers

1. **Preliminary Decision Support:** Model inferences serve strictly as triage aids and spatial field surveillance indicators. They do not constitute statutory plant pathology certificates.
2. **Zero Fabricated Prescriptions:** All Integrated Pest Management (IPM) protocols are grounded strictly in published Indian agricultural extension advisories (ICAR, KVK, TNAU, IARI).
3. **Data Sovereignty:** Farmer imagery is processed purely in volatile RAM and immediately discarded unless explicit opt-in consent is toggled.
