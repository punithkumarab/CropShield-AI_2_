"""Field and Plot Management - CropShield AI 2.0 Farm Spatial Hierarchy."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.cropshield.footer import render_about_footer
from src.cropshield.history import (
    create_farm,
    create_plot,
    list_farms,
    list_plots,
    update_plot_status,
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
    st.set_page_config(page_title="Field & Plot Management - CropShield AI 2.0", page_icon="🗺️", layout="wide")
except Exception:
    pass

inject_theme()
language = get_selected_language()

render_page_header(
    title=translate("field_plot_mgmt", language),
    subtitle="Manage agricultural farms, sub-plots, crop varieties, planting schedules, and surveillance status.",
    tag="Farm & Field Management",
)

farms = list_farms()
plots = list_plots()

# ---------------------------------------------------------
# Farm & Plot Overview KPIs
# ---------------------------------------------------------
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
healthy_plots = sum(1 for p in plots if p.get("health_status") == "Healthy")
monitored_plots = sum(1 for p in plots if p.get("health_status") == "Monitored")
infected_plots = sum(1 for p in plots if p.get("health_status") == "Infected")

kpi1.metric("Registered Farms", f"{len(farms)}")
kpi2.metric("Total Active Plots", f"{len(plots)}")
kpi3.metric("Healthy Plots", f"{healthy_plots}", delta=f"{healthy_plots/max(len(plots),1)*100:.0f}%")
kpi4.metric("Infected / Monitored", f"{infected_plots + monitored_plots}", delta="Attention Needed" if infected_plots > 0 else "Normal", delta_color="inverse" if infected_plots > 0 else "normal")

st.write("")

# ---------------------------------------------------------
# Management Actions (Tabs)
# ---------------------------------------------------------
tab_view, tab_add_plot, tab_add_farm = st.tabs(["Active Plots Directory", "Add New Plot", "Register New Farm"])

with tab_view:
    render_card_start("Current Farm Plots Surveillance Directory", badge_text=f"{len(plots)} Plots", badge_variant="emerald")
    if plots:
        plot_rows = []
        for p in plots:
            status = p.get("health_status", "Healthy")
            plot_rows.append({
                "Plot ID": p["id"],
                "Plot Name": p["name"],
                "Crop Variety": p.get("crop_variety") or "Tomato",
                "Sowing Date": p.get("planting_date") or "Unspecified",
                "Soil Type": p.get("soil_type") or "Loam",
                "Irrigation": p.get("irrigation_type") or "Drip",
                "Health Status": status,
                "Coordinates": f"{p['latitude']:.3f}, {p['longitude']:.3f}" if p.get("latitude") and p.get("longitude") else "Grid",
            })
        st.dataframe(pd.DataFrame(plot_rows), use_container_width=True, hide_index=True)
        
        st.divider()
        st.subheader("Update Plot Health Status")
        u_col1, u_col2, u_col3 = st.columns([1.5, 1.2, 1.0])
        plot_opts = {p["id"]: f"{p['name']} ({p.get('health_status', 'Healthy')})" for p in plots}
        with u_col1:
            sel_plot_id = st.selectbox("Select Plot to Update:", options=list(plot_opts.keys()), format_func=lambda pid: plot_opts[pid])
        with u_col2:
            new_status = st.selectbox("New Surveillance Status:", ["Healthy", "Monitored", "Infected", "Recovering"])
        with u_col3:
            st.write("")
            if st.button("Update Status", type="primary", use_container_width=True):
                update_plot_status(sel_plot_id, new_status)
                st.success("Plot status updated successfully!")
                st.rerun()
    else:
        st.info("No plots created yet. Use the 'Add New Plot' tab to set up your field grid.")
    render_card_end()

with tab_add_plot:
    render_card_start("Create New Monitored Plot", badge_text="Sub-division", badge_variant="forest")
    with st.form("new_plot_form"):
        p_c1, p_c2 = st.columns(2)
        with p_c1:
            farm_selection = st.selectbox(
                "Parent Farm:",
                options=[None] + [f["id"] for f in farms],
                format_func=lambda fid: "General Farm" if fid is None else next((f["name"] for f in farms if f["id"] == fid), "General"),
            )
            plot_name = st.text_input("Plot Name / Designation:", placeholder="e.g. North Greenhouse Block B")
            crop_variety = st.text_input("Crop Variety:", value="Tomato (Arka Rakshak)")
            planting_date = st.date_input("Sowing / Transplanting Date:")
        with p_c2:
            soil_type = st.selectbox("Soil Profile:", ["Red Sandy Loam", "Black Cotton Soil", "Clay Loam", "Alluvial", "Coir Pith / Hydroponic"])
            irrigation_type = st.selectbox("Irrigation Method:", ["Drip Irrigation", "Micro-Sprinkler", "Furrow Irrigation", "Rainfed"])
            lat = st.number_input("Latitude (Optional):", value=12.9716, format="%.5f")
            lon = st.number_input("Longitude (Optional):", value=77.5946, format="%.5f")
            
        submit_plot = st.form_submit_button("Save Plot", type="primary", use_container_width=True)
        if submit_plot:
            if not plot_name.strip():
                st.error("Plot name is required.")
            else:
                create_plot(
                    farm_id=farm_selection,
                    name=plot_name,
                    crop_variety=crop_variety,
                    planting_date=str(planting_date),
                    soil_type=soil_type,
                    irrigation_type=irrigation_type,
                    health_status="Healthy",
                    latitude=lat,
                    longitude=lon,
                )
                st.success(f"Plot '{plot_name}' created successfully!")
                st.rerun()
    render_card_end()

with tab_add_farm:
    render_card_start("Register New Agricultural Holding / Farm", badge_text="Enterprise", badge_variant="neutral")
    with st.form("new_farm_form"):
        f_name = st.text_input("Farm Name:", placeholder="e.g. Green Valley Agro Farm")
        f_loc = st.text_input("District / Location:", placeholder="e.g. Kolar District, Karnataka")
        f_acres = st.number_input("Total Acreage:", min_value=0.1, max_value=10000.0, value=5.0, step=0.5)
        f_crop = st.text_input("Primary Crop:", value="Tomato")
        
        submit_farm = st.form_submit_button("Register Farm", type="primary", use_container_width=True)
        if submit_farm:
            if not f_name.strip():
                st.error("Farm name is required.")
            else:
                try:
                    create_farm(f_name, f_loc, f_acres, f_crop)
                    st.success(f"Farm '{f_name}' registered successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error registering farm: {e}")
    render_card_end()

render_about_footer()
