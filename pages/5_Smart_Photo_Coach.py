"""Smart Photo Coach - CropShield AI 2.0 Real-Time Computer Vision Quality Studio."""

from __future__ import annotations

import cv2
import numpy as np
from PIL import Image
import streamlit as st

from src.cropshield.footer import render_about_footer
from src.cropshield.image_quality import assess_image_quality, crop_largest_leaf_like_region
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
    st.set_page_config(page_title="Smart Photo Coach - CropShield AI 2.0", page_icon="📸", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("photo_coach", language),
    subtitle="Real-time image quality inspection, OpenCV blur detection, glare analysis, and field scouting best practices.",
    tag="Diagnostic Suite",
)

render_card_start("Interactive Image Quality Diagnostic", badge_text="Camera / Upload", badge_variant="emerald")
coach_source = st.radio("Acquisition Mode:", ["Take Photo with Camera", "Upload Existing Photo"], horizontal=True)

photo_file = None
if coach_source == "Take Photo with Camera":
    photo_file = st.camera_input("Point camera directly at a single representative leaf:", key="coach_camera")
else:
    photo_file = st.file_uploader("Upload leaf photograph to analyze quality:", type=["jpg", "jpeg", "png", "webp"], key="coach_upload")
render_card_end()

if photo_file:
    image = Image.open(photo_file).convert("RGB")
    qa = assess_image_quality(image)
    
    col_view, col_cv = st.columns([1.1, 1.2])
    
    with col_view:
        render_card_start("Acquired Leaf Image", badge_text=f"{image.width} × {image.height} px", badge_variant="neutral")
        st.image(image, use_container_width=True)
        render_card_end()
        
    with col_cv:
        render_card_start("OpenCV Quality Metrics & Verdict", badge_text="Diagnostic Quality", badge_variant="forest" if qa.acceptable else "crimson")
        
        status_text = "✓ PASSED - High Diagnostic Quality" if qa.acceptable else "✕ ACTION NEEDED - Quality Restricted"
        st.markdown(f"### {status_text}")
        
        # Focus / Sharpness Gauge
        st.markdown(f"**Focus Score (Laplacian Variance):** `{qa.blur_score:.1f}` (Threshold: >= 20.0)")
        st.progress(min(1.0, qa.blur_score / 100.0))
        
        # Exposure / Brightness
        st.markdown(f"**Brightness Exposure:** `{qa.brightness:.0f} / 255` (Optimal: 40 - 220)")
        st.progress(min(1.0, qa.brightness / 255.0))
        
        # Glare & Reflections
        st.markdown(f"**Glare & Specular Reflections:** `{qa.glare_fraction * 100:.1f}%` (Max Allowed: 15.0%)")
        st.progress(min(1.0, qa.glare_fraction / 0.30))
        
        # Green Leaf Area Coverage
        st.markdown(f"**Color-Segmented Leaf Coverage:** `{qa.leaf_coverage_fraction * 100:.1f}%`")
        st.progress(min(1.0, qa.leaf_coverage_fraction))
        
        if qa.feedback:
            st.divider()
            st.markdown("**Coach Feedback & Improvements:**")
            for tip in qa.feedback:
                st.warning(f"💡 {tip}")
        else:
            st.success("✓ Excellent focus, uniform illumination, and centered framing. Image is ready for AI prediction.")
        render_card_end()

    # ---------------------------------------------------------
    # Visual OpenCV Segmentation Mask Preview
    # ---------------------------------------------------------
    st.write("")
    render_card_start("Computer Vision Segmentation & Region Extraction", badge_text="HSV Green Mask", badge_variant="blue")
    st.write("CropShield AI uses HSV color-space contouring to segment leaf tissue from background soil, plastic mulches, or sky.")
    
    seg_col1, seg_col2 = st.columns(2)
    with seg_col1:
        mask_display = (qa.leaf_mask.astype(np.uint8) * 255)
        st.image(mask_display, caption="OpenCV Binary Leaf Contour Mask (White = Evaluated Leaf Region)", use_container_width=True)
    with seg_col2:
        cropped_region = crop_largest_leaf_like_region(image)
        if cropped_region:
            st.image(cropped_region, caption="Cropped Leaf Region (Bounding Box Extraction)", use_container_width=True)
        else:
            st.info("No distinct dominant leaf contour detected.")
    render_card_end()

# ---------------------------------------------------------
# Field Photography Guidelines
# ---------------------------------------------------------
st.write("")
render_card_start("Field Photography Best Practices Checklist", badge_text="Scouting Protocol", badge_variant="forest")
f1, f2, f3, f4 = st.columns(4)
f1.markdown("**1. Framing & Distance**\n- Fill 60-80% of the frame with a single leaf\n- Avoid extreme wide shots of the whole canopy")
f2.markdown("**2. Focus & Steadiness**\n- Tap phone screen on affected lesions\n- Keep hands steady in windy field conditions")
f3.markdown("**3. Illumination & Glare**\n- Shade direct harsh sunlight with your body\n- Avoid camera flash reflection on wet leaves")
f4.markdown("**4. Neutral Background**\n- Use hand or soil as neutral backing\n- Avoid clutter, feet, or brightly colored clothing")
render_card_end()

render_about_footer()
