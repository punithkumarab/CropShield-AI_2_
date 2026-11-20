"""Shared professional agricultural design system and UI components for CropShield AI 2.0."""

from __future__ import annotations

import html
import logging
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

from .translations import LANGUAGES, translate

LOGGER = logging.getLogger(__name__)

# Design System CSS tokens adhering to hallmark, impeccable, and ui-ux-pro-max guidelines:
# Forest green (#1B4332), Emerald green (#2D6A4F), Soft cream (#F8F9FA), White surfaces (#FFFFFF), Charcoal text (#1E293B)
_CSS = """
<style>
:root {
    --cs-forest: #1B4332;
    --cs-emerald: #2D6A4F;
    --cs-mint: #D8F3DC;
    --cs-cream: #F8F9FA;
    --cs-surface: #FFFFFF;
    --cs-border: #E2E8F0;
    --cs-charcoal: #1E293B;
    --cs-slate: #64748B;
    --cs-amber: #D97706;
    --cs-crimson: #DC2626;
    --cs-blue: #0284C7;
}

/* Base Typography & Background */
.stApp {
    background-color: var(--cs-cream);
    color: var(--cs-charcoal);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}

p, li, label, span, div {
    color: var(--cs-charcoal);
}

/* Headings */
[data-testid="stHeading"] h1,
[data-testid="stHeading"] h1 span,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h1 span {
    color: var(--cs-forest) !important;
    font-weight: 750 !important;
    letter-spacing: -0.025em !important;
}

[data-testid="stHeading"] h2,
[data-testid="stHeading"] h2 span {
    color: var(--cs-forest) !important;
    font-weight: 650 !important;
    letter-spacing: -0.015em !important;
}

[data-testid="stHeading"] h3,
[data-testid="stHeading"] h3 span {
    color: var(--cs-emerald) !important;
    font-weight: 600 !important;
}

/* Sidebar Modernization */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid var(--cs-border) !important;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: var(--cs-slate);
    font-size: 0.88rem;
}

/* Elevated Clean Cards */
.cs-card {
    background: var(--cs-surface);
    border: 1px solid var(--cs-border);
    border-radius: 10px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04), 0 1px 2px rgba(0, 0, 0, 0.02);
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.cs-card:hover {
    border-color: #CBD5E1;
    box-shadow: 0 4px 12px rgba(27, 67, 50, 0.06);
}

.cs-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    border-bottom: 1px solid #F1F5F9;
    padding-bottom: 0.5rem;
}

.cs-card-title {
    font-size: 1.05rem;
    font-weight: 650;
    color: var(--cs-forest);
    margin: 0;
}

/* KPI Stat Cards */
div[data-testid="stMetric"] {
    background: var(--cs-surface) !important;
    border: 1px solid var(--cs-border) !important;
    border-radius: 10px !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    transition: border-color 0.2s ease !important;
}

div[data-testid="stMetric"]:hover {
    border-color: var(--cs-emerald) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    color: var(--cs-slate) !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.75rem !important;
    font-weight: 750 !important;
    color: var(--cs-forest) !important;
}

/* Executive Page Header */
.cs-header {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%);
    color: #FFFFFF !important;
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 16px rgba(27, 67, 50, 0.15);
}

.cs-header * {
    color: #FFFFFF !important;
}

.cs-header-tag {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    background: rgba(255, 255, 255, 0.2);
    padding: 0.25rem 0.65rem;
    border-radius: 6px;
    margin-bottom: 0.5rem;
}

.cs-header h1 {
    font-size: 1.85rem;
    font-weight: 750;
    margin: 0 0 0.4rem 0;
}

.cs-header p {
    font-size: 0.98rem;
    opacity: 0.92;
    margin: 0;
    max-width: 48rem;
    line-height: 1.45;
}

/* Badges */
.cs-badge {
    display: inline-flex;
    align-items: center;
    padding: 0.2rem 0.6rem;
    border-radius: 6px;
    font-size: 0.78rem;
    font-weight: 650;
    letter-spacing: 0.02em;
    line-height: 1;
}

.cs-badge-forest { background: #E8F5E9; color: #1B4332; border: 1px solid #C8E6C9; }
.cs-badge-emerald { background: #D8F3DC; color: #2D6A4F; border: 1px solid #B7E4C7; }
.cs-badge-amber { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
.cs-badge-crimson { background: #FEE2E2; color: #991B1B; border: 1px solid #FECACA; }
.cs-badge-blue { background: #E0F2FE; color: #0369A1; border: 1px solid #BAE6FD; }
.cs-badge-neutral { background: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }

/* Buttons & Inputs */
.stButton > button, .stDownloadButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.5rem 1.25rem !important;
    border: 1px solid transparent !important;
    transition: all 0.18s ease !important;
}

.stButton > button[kind="primary"] {
    background-color: var(--cs-emerald) !important;
    color: #FFFFFF !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: var(--cs-forest) !important;
    box-shadow: 0 4px 12px rgba(27, 67, 50, 0.2) !important;
}

.stButton > button[kind="secondary"] {
    background-color: #FFFFFF !important;
    border: 1px solid var(--cs-border) !important;
    color: var(--cs-charcoal) !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--cs-emerald) !important;
    color: var(--cs-emerald) !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--cs-border);
    margin-bottom: 1rem;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 6px 6px 0 0 !important;
    padding: 0.6rem 1.2rem !important;
    font-weight: 600 !important;
    color: var(--cs-slate) !important;
}

.stTabs [aria-selected="true"] {
    color: var(--cs-forest) !important;
    border-bottom: 2px solid var(--cs-emerald) !important;
}

/* Clean Alert Boxes */
div[data-testid="stAlert"] {
    border-radius: 8px !important;
    border: 1px solid var(--cs-border) !important;
    padding: 0.85rem 1.1rem !important;
}

/* =========================================================================
   Crop Yield Website (CYPA) Template Styles
   ========================================================================= */
.cypa-hero-container {
    position: relative;
    border-radius: 16px;
    overflow: hidden;
    margin-bottom: 2rem;
    box-shadow: 0 16px 40px rgba(7, 34, 24, 0.35);
    background: #072218;
}

.cypa-hero-inner {
    padding: 4rem 2.5rem 4.5rem 2.5rem;
    text-align: center;
    color: #FFFFFF;
    background: linear-gradient(180deg, rgba(7, 34, 24, 0.72) 0%, rgba(7, 34, 24, 0.92) 100%);
}

.cypa-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 2rem;
    margin-bottom: 2.5rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
}

.cypa-brand-tag {
    font-size: 1.15rem;
    font-weight: 850;
    color: #FFFFFF;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

.cypa-nav-items {
    display: flex;
    gap: 28px;
}

.cypa-nav-item {
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: rgba(255, 255, 255, 0.85);
    text-transform: uppercase;
    text-decoration: none;
    transition: color 0.18s ease;
}

.cypa-nav-item:hover {
    color: #A7F3D0;
}

.cypa-hero-title {
    font-size: 3.1rem !important;
    font-weight: 850 !important;
    color: #FFFFFF !important;
    letter-spacing: -0.025em !important;
    line-height: 1.12 !important;
    margin: 0 0 1.25rem 0 !important;
    text-shadow: 0 2px 12px rgba(0, 0, 0, 0.5);
}

.cypa-hero-subtitle {
    font-size: 1.15rem !important;
    color: rgba(255, 255, 255, 0.92) !important;
    max-width: 740px !important;
    margin: 0 auto 2.5rem auto !important;
    line-height: 1.65 !important;
    font-weight: 400 !important;
    text-shadow: 0 1px 6px rgba(0, 0, 0, 0.4);
}

.cypa-pill-btn {
    display: inline-flex;
    align-items: center;
    gap: 12px;
    background: #FFFFFF !important;
    color: #072218 !important;
    font-weight: 700 !important;
    font-size: 1.02rem !important;
    padding: 12px 34px !important;
    border-radius: 999px !important;
    text-decoration: none !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.28) !important;
    transition: transform 0.18s ease, box-shadow 0.18s ease !important;
}

.cypa-pill-btn:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 28px rgba(0, 0, 0, 0.4) !important;
}

.cypa-green-dot {
    width: 10px;
    height: 10px;
    background-color: #072218;
    border-radius: 50%;
    display: inline-block;
}

/* Horizontal Ticker Banner (from About Us template) */
.cypa-ticker-banner {
    background: #072218;
    color: #FFFFFF;
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin: 1.8rem 0 2.5rem 0;
    display: flex;
    justify-content: space-around;
    align-items: center;
    border: 1px solid rgba(255, 255, 255, 0.12);
    box-shadow: 0 4px 16px rgba(7, 34, 24, 0.2);
}

.cypa-ticker-cell {
    display: flex;
    align-items: center;
    gap: 16px;
}

.cypa-arrow {
    font-size: 1.9rem;
    color: rgba(255, 255, 255, 0.7);
    font-weight: 300;
}

.cypa-stat-value {
    font-size: 2.1rem;
    font-weight: 850;
    color: #FFFFFF;
    line-height: 1;
}

.cypa-stat-caption {
    font-size: 0.78rem;
    font-weight: 750;
    color: #A7F3D0;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}

/* Editorial Split Sections (matching About Us.png) */
.cypa-editorial-box {
    background: #072218;
    color: #FFFFFF;
    border-radius: 14px;
    padding: 2.8rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
}

.cypa-section-tag {
    font-size: 0.85rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    color: #6EE7B7;
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: block;
}

@keyframes gradientTextShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

@keyframes csFadeInUp {
    from {
        opacity: 0;
        transform: translateY(14px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes csFadeInScale {
    from {
        opacity: 0;
        transform: scale(0.97);
    }
    to {
        opacity: 1;
        transform: scale(1);
    }
}

@keyframes heroGradientWave {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.cypa-editorial-heading {
    font-size: 2rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.22;
    margin-bottom: 1.2rem;
    letter-spacing: -0.015em;
}

.cypa-editorial-heading-gradient {
    font-size: 2.15rem;
    font-weight: 850;
    line-height: 1.24;
    margin-bottom: 1.2rem;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, #74C69D 0%, #52B788 28%, #2D6A4F 55%, #0284C7 80%, #DDA15E 100%);
    background-size: 250% 250%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    color: transparent;
    animation: gradientTextShift 6s ease-in-out infinite;
    display: inline-block;
}

/* Global Subtle Entrance Animations across every page */
.cs-header, [data-testid="stHeading"], h1, h2, h3 {
    animation: csFadeInUp 0.45s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.cs-card, div[data-testid="stMetric"], .cypa-editorial-box {
    animation: csFadeInUp 0.55s cubic-bezier(0.16, 1, 0.3, 1) both;
}

div[data-testid="column"]:nth-child(1) .cs-card,
div[data-testid="column"]:nth-child(1) div[data-testid="stMetric"] {
    animation-delay: 0.04s;
}
div[data-testid="column"]:nth-child(2) .cs-card,
div[data-testid="column"]:nth-child(2) div[data-testid="stMetric"] {
    animation-delay: 0.10s;
}
div[data-testid="column"]:nth-child(3) .cs-card,
div[data-testid="column"]:nth-child(3) div[data-testid="stMetric"] {
    animation-delay: 0.16s;
}
div[data-testid="column"]:nth-child(4) .cs-card,
div[data-testid="column"]:nth-child(4) div[data-testid="stMetric"] {
    animation-delay: 0.22s;
}

.stPlotlyChart, [data-testid="stDataFrame"], [data-testid="stTable"] {
    animation: csFadeInScale 0.6s cubic-bezier(0.16, 1, 0.3, 1) 0.15s both;
}

[data-testid="stImage"] {
    animation: csFadeInScale 0.5s cubic-bezier(0.16, 1, 0.3, 1) 0.10s both;
    border-radius: 10px;
    overflow: hidden;
}

/* Sidebar Navigation Items: Entrance, Spacing, and Hover Glow */
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"] {
    animation: csFadeInUp 0.4s ease-out both;
    transition: all 0.22s ease !important;
    border-radius: 8px !important;
}
[data-testid="stSidebar"] [data-testid="stPageLink-NavLink"]:hover {
    background: rgba(45, 106, 79, 0.09) !important;
    transform: translateX(3px) !important;
    border-left: 3px solid #2D6A4F !important;
}

/* Clean Editorial Box without ghost text */
.cypa-editorial-box {
    background: #072218 !important;
    color: #FFFFFF !important;
    border-radius: 14px !important;
    padding: 2.8rem !important;
    margin-bottom: 2rem !important;
    border: 1px solid rgba(82, 183, 136, 0.22) !important;
    box-shadow: 0 12px 32px rgba(7, 34, 24, 0.25) !important;
    position: relative !important;
    overflow: hidden !important;
}

.cypa-editorial-body {
    font-size: 1.05rem;
    color: #E2E8F0;
    line-height: 1.75;
    margin-bottom: 0;
}

/* =========================================================================
   CropShield AI 2.0 — 3D Motion System & Micro-Interactions
   ========================================================================= */

/* 1. 3D Interactive Buttons */
.stButton > button, .stDownloadButton > button, .cypa-pill-btn, .cs-btn-3d {
    position: relative !important;
    overflow: hidden !important;
    border-radius: 10px !important;
    font-weight: 650 !important;
    letter-spacing: 0.02em !important;
    transform: perspective(600px) translateZ(0) !important;
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), 
                box-shadow 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), 
                background-color 0.2s ease, 
                border-color 0.2s ease !important;
    will-change: transform, box-shadow !important;
}

.stButton > button[kind="primary"], .cs-btn-primary {
    background: linear-gradient(135deg, #10B981 0%, #059669 100%) !important;
    border: 1px solid rgba(16, 185, 129, 0.4) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(16, 185, 129, 0.25) !important;
}

.stButton > button[kind="primary"]:hover, .cs-btn-primary:hover {
    transform: perspective(600px) translateY(-3px) scale(1.02) !important;
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
    box-shadow: 0 10px 25px -4px rgba(16, 185, 129, 0.45), 0 4px 12px rgba(27, 67, 50, 0.2) !important;
    border-color: #34D399 !important;
}

.stButton > button[kind="primary"]:active, .cs-btn-primary:active {
    transform: perspective(600px) translateY(1px) scale(0.98) !important;
    box-shadow: 0 2px 6px rgba(16, 185, 129, 0.3) !important;
}

.stButton > button[kind="secondary"], .cs-btn-secondary {
    background-color: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    color: #1E293B !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04) !important;
}

.stButton > button[kind="secondary"]:hover, .cs-btn-secondary:hover {
    transform: perspective(600px) translateY(-2px) scale(1.015) !important;
    border-color: #10B981 !important;
    color: #059669 !important;
    box-shadow: 0 6px 18px rgba(16, 185, 129, 0.15) !important;
}

.stButton > button[kind="secondary"]:active, .cs-btn-secondary:active {
    transform: perspective(600px) translateY(1px) scale(0.985) !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06) !important;
}

.stButton > button::after {
    content: "";
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: linear-gradient(60deg, transparent 35%, rgba(255, 255, 255, 0.22) 50%, transparent 65%);
    transform: translateX(-100%);
    transition: transform 0.6s ease;
    pointer-events: none;
}

.stButton > button:hover::after {
    transform: translateX(100%);
}

/* 2. Interactive 3D Cards */
.cs-card, div[data-testid="stMetric"], .cypa-editorial-box, .cs-3d-card {
    transform-style: preserve-3d;
    perspective: 1000px;
    transition: transform 0.28s cubic-bezier(0.2, 0.8, 0.2, 1), 
                box-shadow 0.28s cubic-bezier(0.2, 0.8, 0.2, 1), 
                border-color 0.25s ease !important;
    will-change: transform, box-shadow;
}

.cs-card:hover, div[data-testid="stMetric"]:hover {
    transform: perspective(1000px) translateY(-5px) translateZ(8px) !important;
    border-color: #10B981 !important;
    box-shadow: 0 16px 36px rgba(27, 67, 50, 0.1), 0 0 0 1px rgba(16, 185, 129, 0.2) !important;
}

/* 3. Animated Dropzone Pulse */
[data-testid="stFileUploader"] section {
    border: 2px dashed #10B981 !important;
    border-radius: 12px !important;
    background: rgba(16, 185, 129, 0.03) !important;
    transition: all 0.25s ease !important;
    animation: dropzoneGlow 3s infinite alternate ease-in-out;
}

[data-testid="stFileUploader"] section:hover {
    background: rgba(16, 185, 129, 0.07) !important;
    border-color: #059669 !important;
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.18) !important;
}

@keyframes dropzoneGlow {
    0% { border-color: rgba(16, 185, 129, 0.35); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.08); }
    100% { border-color: rgba(16, 185, 129, 0.85); box-shadow: 0 0 16px 2px rgba(16, 185, 129, 0.2); }
}

/* 4. Laser Scanline Animation for Scanner */
.scanner-preview-wrapper {
    position: relative;
    border-radius: 12px;
    overflow: hidden;
    border: 2px solid #10B981;
    box-shadow: 0 8px 28px rgba(16, 185, 129, 0.25);
    background: #000000;
}

.scanner-laser-line {
    position: absolute;
    left: 0;
    width: 100%;
    height: 3px;
    background: #34D399;
    box-shadow: 0 0 14px 3px #10B981, 0 0 28px 6px rgba(52, 211, 153, 0.6);
    animation: laserScan 2.4s ease-in-out infinite alternate;
    z-index: 10;
    pointer-events: none;
}

@keyframes laserScan {
    0% { top: 3%; opacity: 0.95; }
    50% { opacity: 0.45; }
    100% { top: 96%; opacity: 0.95; }
}

/* 5. ChatGPT-Style Chat Micro-Interactions */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 14px;
    padding: 1rem 0;
}

.chat-bubble-user {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 100%);
    color: #FFFFFF !important;
    border-radius: 16px 16px 4px 16px;
    padding: 1rem 1.35rem;
    max-width: 82%;
    margin-left: auto;
    box-shadow: 0 4px 16px rgba(27, 67, 50, 0.2);
    animation: slideInRight 0.32s cubic-bezier(0.16, 1, 0.3, 1) both;
}

.chat-bubble-user * {
    color: #FFFFFF !important;
}

.chat-bubble-assistant {
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-left: 4px solid #10B981;
    border-radius: 16px 16px 16px 4px;
    padding: 1.25rem 1.5rem;
    max-width: 90%;
    margin-right: auto;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.05);
    animation: slideInLeft 0.35s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(24px) scale(0.98); }
    to { opacity: 1; transform: translateX(0) scale(1); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-24px) scale(0.98); }
    to { opacity: 1; transform: translateX(0) scale(1); }
}

.typing-indicator {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 10px 16px;
    background: #FFFFFF;
    border: 1px solid #E2E8F0;
    border-radius: 999px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: #10B981;
    border-radius: 50%;
    animation: typingPulse 1.4s infinite ease-in-out both;
}

.typing-dot:nth-child(1) { animation-delay: -0.32s; }
.typing-dot:nth-child(2) { animation-delay: -0.16s; }
.typing-dot:nth-child(3) { animation-delay: 0s; }

@keyframes typingPulse {
    0%, 80%, 100% { transform: scale(0.6); opacity: 0.35; }
    40% { transform: scale(1.2); opacity: 1; }
}

.prompt-chip {
    display: inline-block;
    padding: 0.5rem 0.9rem;
    background: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 600;
    color: #1E293B;
    cursor: pointer;
    transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
}

.prompt-chip:hover {
    transform: translateY(-2px) scale(1.03);
    border-color: #10B981;
    color: #059669;
    box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2);
}

/* 6. Sidebar Active Navigation & Transition */
[data-testid="stSidebarNav"] a {
    transition: transform 0.2s ease, color 0.2s ease, background 0.2s ease !important;
    border-radius: 8px !important;
}

[data-testid="stSidebarNav"] a:hover {
    transform: translateX(4px) !important;
    color: #10B981 !important;
    background: rgba(16, 185, 129, 0.06) !important;
}

/* 7. Accessibility Reduced Motion */
@media (prefers-reduced-motion: reduce) {
    *, ::after, ::before {
        animation-duration: 0.001s !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.001s !important;
        transform: none !important;
    }
}

</style>
"""


def inject_theme(*, home: bool = False) -> None:
    """Inject CropShield AI 2.0 enterprise styles and design tokens."""
    del home
    st.markdown(_CSS, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str, tag: str = "CropShield AI 2.0") -> None:
    """Render a consistent, branded page header."""
    clean_tag = html.escape(tag)
    clean_title = html.escape(title)
    clean_sub = html.escape(subtitle)
    st.markdown(
        f"""
        <div class="cs-header">
            <span class="cs-header-tag">{clean_tag}</span>
            <h1>{clean_title}</h1>
            <p>{clean_sub}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_asset_base64(filename: str) -> str:
    """Load an asset image as base64 data URI for zero-dependency HTML rendering."""
    for base in (
        Path(__file__).resolve().parents[2] / "assets",
        Path(__file__).resolve().parents[1] / "assets",
        Path("assets"),
    ):
        p = base / filename
        if p.is_file():
            try:
                import base64
                ext = p.suffix.lower().replace(".", "")
                mime = "jpeg" if ext in ("jpg", "jpeg") else ext
                return f"data:image/{mime};base64,{base64.b64encode(p.read_bytes()).decode('ascii')}"
            except Exception:
                pass
    return ""


def render_3d_hero_section() -> None:
    """Render the premium Three.js 3D hero section for CropShield AI 2.0."""
    html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body, html { width: 100%; height: 100%; overflow: hidden; background: #072218; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
  
  #hero-container {
    position: relative;
    width: 100%;
    min-height: 590px;
    height: auto;
    background: radial-gradient(circle at 75% 50%, #0d3d2a 0%, #072218 70%);
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 16px 40px rgba(7, 34, 24, 0.4);
    border: 1px solid rgba(52, 211, 153, 0.25);
  }
  
  #webgl-canvas {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1;
    display: block;
  }
  
  /* Fallback 3D scene if WebGL unavailable */
  .css-fallback {
    position: absolute;
    right: 8%;
    top: 22%;
    width: 320px;
    height: 320px;
    z-index: 1;
    perspective: 800px;
    display: none;
  }
  
  /* UI Content Overlay */
  .hero-overlay {
    position: relative;
    width: 100%;
    min-height: 590px;
    z-index: 3;
    pointer-events: none;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 2.2rem 2.5rem;
  }
  
  .hero-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    padding-bottom: 1.2rem;
    pointer-events: auto;
  }
  
  .hero-brand {
    font-size: 1.15rem;
    font-weight: 850;
    letter-spacing: 0.14em;
    color: #FFFFFF;
    text-transform: uppercase;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .brand-dot {
    width: 9px;
    height: 9px;
    background: #10B981;
    border-radius: 50%;
    box-shadow: 0 0 10px #10B981;
    animation: dotPulse 2s infinite;
  }
  
  @keyframes dotPulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.3); opacity: 0.6; }
  }
  
  .hero-links {
    display: flex;
    gap: 22px;
  }
  
  .hero-link {
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    color: rgba(255, 255, 255, 0.85);
    text-decoration: none;
    text-transform: uppercase;
    transition: color 0.18s ease;
  }
  
  .hero-link:hover {
    color: #6EE7B7;
  }

  .hero-main-layout {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 36px;
    width: 100%;
    margin-top: 1.2rem;
    margin-bottom: 0.8rem;
    pointer-events: auto;
  }
  
  .hero-body {
    flex: 1 1 540px;
    max-width: 600px;
    pointer-events: auto;
  }
  
  .hero-tag {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.76rem;
    font-weight: 800;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    background: rgba(16, 185, 129, 0.18);
    color: #6EE7B7;
    border: 1px solid rgba(52, 211, 153, 0.35);
    padding: 0.3rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 1.2rem;
  }
  
  .hero-heading {
    font-size: 2.85rem;
    font-weight: 850;
    color: #FFFFFF;
    letter-spacing: -0.025em;
    line-height: 1.15;
    margin-bottom: 1.1rem;
    text-shadow: 0 4px 18px rgba(0, 0, 0, 0.5);
  }
  
  .hero-heading-glow {
    background: linear-gradient(135deg, #34D399 0%, #A7F3D0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  
  .hero-subtitle {
    font-size: 1.08rem;
    color: rgba(255, 255, 255, 0.9);
    line-height: 1.6;
    margin-bottom: 1.8rem;
    text-shadow: 0 2px 8px rgba(0, 0, 0, 0.4);
  }
  
  .hero-actions {
    display: flex;
    gap: 16px;
    align-items: center;
    margin-top: 1.8rem;
    margin-bottom: 1rem;
    position: relative;
    z-index: 10;
  }
  
  .hero-btn-primary {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: #FFFFFF;
    color: #072218;
    font-weight: 750;
    font-size: 0.96rem;
    padding: 12px 28px;
    border-radius: 999px;
    text-decoration: none;
    box-shadow: 0 6px 22px rgba(0, 0, 0, 0.35);
    transform: perspective(600px) translateZ(0);
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.22s ease;
  }
  
  .hero-btn-primary:hover {
    transform: perspective(600px) translateY(-3px) scale(1.02);
    box-shadow: 0 12px 30px rgba(16, 185, 129, 0.45);
    color: #072218;
  }
  
  .hero-btn-primary:active {
    transform: perspective(600px) translateY(1px) scale(0.98);
  }
  
  .hero-btn-secondary {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(255, 255, 255, 0.12);
    color: #FFFFFF;
    border: 1px solid rgba(255, 255, 255, 0.25);
    font-weight: 650;
    font-size: 0.94rem;
    padding: 12px 24px;
    border-radius: 999px;
    text-decoration: none;
    backdrop-filter: blur(8px);
    transform: perspective(600px) translateZ(0);
    transition: transform 0.22s cubic-bezier(0.34, 1.56, 0.64, 1), background 0.2s ease, border-color 0.2s ease;
  }
  
  .hero-btn-secondary:hover {
    transform: perspective(600px) translateY(-3px) scale(1.02);
    background: rgba(255, 255, 255, 0.2);
    border-color: #34D399;
    color: #FFFFFF;
    box-shadow: 0 8px 24px rgba(16, 185, 129, 0.25);
  }
  
  .hero-btn-dot {
    width: 8px;
    height: 8px;
    background: #072218;
    border-radius: 50%;
  }

  /* Telemetry Rail with Natural Flex Layout, Zero Absolute Collisions */
  .hero-telemetry-rail {
    display: flex;
    flex-direction: column;
    gap: 16px;
    flex-shrink: 0;
    pointer-events: auto;
    margin-left: auto;
  }
  
  /* Floating Glassmorphism Telemetry Badges */
  .floating-glass {
    position: relative !important;
    top: auto !important;
    right: auto !important;
    bottom: auto !important;
    left: auto !important;
    background: rgba(7, 34, 24, 0.75);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(52, 211, 153, 0.35);
    border-radius: 12px;
    padding: 12px 18px;
    display: flex;
    align-items: center;
    gap: 14px;
    color: #FFFFFF;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    pointer-events: auto;
    min-width: 250px;
    transition: transform 0.3s ease, border-color 0.3s ease;
  }
  
  .floating-glass:hover {
    transform: translateY(-4px) scale(1.03);
    border-color: #34D399;
  }
  
  .fg-badge-1 {
    animation: float1 4.5s ease-in-out infinite;
  }
  
  .fg-badge-2 {
    animation: float2 5s ease-in-out infinite;
  }
  
  .fg-badge-3 {
    animation: float3 4.2s ease-in-out infinite;
  }

  @media (max-width: 900px) {
    #hero-container {
      min-height: 680px;
    }
    .hero-main-layout {
      flex-direction: column;
      align-items: stretch;
      gap: 28px;
    }
    .hero-telemetry-rail {
      width: 100%;
      align-items: stretch;
      gap: 12px;
      margin-left: 0;
    }
    .hero-actions {
      flex-direction: column;
      align-items: stretch;
      gap: 12px;
      margin-top: 24px;
      margin-bottom: 20px;
    }
  }
  
  @keyframes float1 {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
  }
  @keyframes float2 {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
  }
  @keyframes float3 {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-6px); }
  }
  
  .fg-icon {
    font-size: 1.4rem;
  }
  
  .fg-val {
    font-size: 0.92rem;
    font-weight: 750;
    color: #FFFFFF;
    line-height: 1.2;
  }
  
  .fg-sub {
    font-size: 0.72rem;
    font-weight: 600;
    color: #A7F3D0;
    letter-spacing: 0.05em;
    text-transform: uppercase;
  }
</style>
</head>
<body>
<div id="hero-container">
  <canvas id="webgl-canvas"></canvas>
  <div class="hero-overlay">
    <div class="hero-nav">
      <div class="hero-brand">
        <span class="brand-dot"></span>
        <span>CropShield AI 2.0</span>
      </div>
      <div class="hero-links">
        <a class="hero-link" href="pages/1_Overview_Dashboard.py" target="_parent">Overview</a>
        <a class="hero-link" href="pages/2_AI_Crop_Scanner.py" target="_parent">AI Scanner</a>
        <a class="hero-link" href="pages/11_AI_Agricultural_Assistant.py" target="_parent">Assistant</a>
        <a class="hero-link" href="pages/12_Weather_and_Field_Insights.py" target="_parent">Weather</a>
        <a class="hero-link" href="pages/16_Reports_and_Export_Center.py" target="_parent">Reports</a>
      </div>
    </div>
    
    <div class="hero-main-layout">
      <div class="hero-body">
        <div class="hero-tag">
          <span>●</span> AI-Powered Foliar Surveillance
        </div>
        <h1 class="hero-heading">
          Intelligence That<br>
          <span class="hero-heading-glow">Protects Every Leaf</span>
        </h1>
        <p class="hero-subtitle">
          Discover smarter crop monitoring with AI-powered disease detection and agricultural intelligence.
        </p>
        <div class="hero-actions">
          <a href="pages/2_AI_Crop_Scanner.py" target="_parent" class="hero-btn-primary">
            <span>Start Crop Scan</span>
            <span class="hero-btn-dot"></span>
          </a>
          <a href="pages/11_AI_Agricultural_Assistant.py" target="_parent" class="hero-btn-secondary">
            <span>Ask AI Assistance →</span>
          </a>
        </div>
      </div>
      
      <!-- Dedicated Telemetry Rail: Natural Column Flow, Zero Absolute Overlap -->
      <div class="hero-telemetry-rail">
        <div class="floating-glass fg-badge-1">
          <span class="fg-icon">🔬</span>
          <div>
            <div class="fg-val">MobileNetV2 Active</div>
            <div class="fg-sub">Grad-CAM Attentive Focus</div>
          </div>
        </div>
        
        <div class="floating-glass fg-badge-2">
          <span class="fg-icon">🌿</span>
          <div>
            <div class="fg-val">Specimen Integrity: 99.4%</div>
            <div class="fg-sub">Calibrated Trust Validation</div>
          </div>
        </div>
        
        <div class="floating-glass fg-badge-3">
          <span class="fg-icon">🌦️</span>
          <div>
            <div class="fg-val">Low Pathogen Pressure</div>
            <div class="fg-sub">Micro-Climate Risk Telemetry</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
  (function() {
    const container = document.getElementById('hero-container');
    const canvas = document.getElementById('webgl-canvas');
    if (!window.THREE) return;

    const width = container.clientWidth || 980;
    const height = container.clientHeight || 570;

    const scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x072218, 0.035);

    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 0.8, 11);

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));

    // Lights
    const ambientLight = new THREE.AmbientLight(0x0f402b, 1.4);
    scene.add(ambientLight);

    const sunLight = new THREE.DirectionalLight(0xf0fdf4, 1.8);
    sunLight.position.set(6, 10, 8);
    scene.add(sunLight);

    const fillLight = new THREE.DirectionalLight(0x10b981, 0.9);
    fillLight.position.set(-6, -3, -4);
    scene.add(fillLight);

    const mouseLight = new THREE.PointLight(0x34d399, 2.2, 18);
    mouseLight.position.set(2, 0, 4);
    scene.add(mouseLight);

    // -------------------------------------------------------------
    // Procedural 3D Plant Model
    // -------------------------------------------------------------
    const plantGroup = new THREE.Group();
    plantGroup.position.set(2.9, -2.1, 0);
    scene.add(plantGroup);

    // Stem
    const stemCurve = new THREE.CatmullRomCurve3([
      new THREE.Vector3(0, 0, 0),
      new THREE.Vector3(0.12, 1.2, 0.05),
      new THREE.Vector3(-0.08, 2.3, 0.12),
      new THREE.Vector3(0.06, 3.4, 0.04),
      new THREE.Vector3(0, 4.2, 0)
    ]);
    const stemGeo = new THREE.TubeGeometry(stemCurve, 32, 0.14, 12, false);
    const stemMat = new THREE.MeshStandardMaterial({
      color: 0x065f46,
      roughness: 0.35,
      metalness: 0.12
    });
    const stemMesh = new THREE.Mesh(stemGeo, stemMat);
    plantGroup.add(stemMesh);

    // Leaf Shape
    const leafShape = new THREE.Shape();
    leafShape.moveTo(0, 0);
    leafShape.bezierCurveTo(0.6, 0.4, 0.85, 1.3, 0, 2.2);
    leafShape.bezierCurveTo(-0.85, 1.3, -0.6, 0.4, 0, 0);

    const leafGeo = new THREE.ExtrudeGeometry(leafShape, {
      depth: 0.03,
      bevelEnabled: true,
      bevelSegments: 2,
      steps: 1,
      bevelSize: 0.015,
      bevelThickness: 0.015
    });

    const leafMat = new THREE.MeshStandardMaterial({
      color: 0x10b981,
      roughness: 0.28,
      metalness: 0.1,
      side: THREE.DoubleSide
    });

    const leafMeshes = [];
    const numLeaves = 10;
    for (let i = 0; i < numLeaves; i++) {
      const leafMesh = new THREE.Mesh(leafGeo, leafMat);
      const t = 0.2 + (i / numLeaves) * 0.72;
      const pos = stemCurve.getPoint(t);
      leafMesh.position.copy(pos);

      // Fibonacci spiral angle
      const angle = i * 2.39996;
      leafMesh.rotation.y = angle;
      leafMesh.rotation.x = 0.55 + Math.sin(i) * 0.15;
      leafMesh.rotation.z = -0.35;

      const scale = 0.65 + (1 - t * 0.4) * 0.45;
      leafMesh.scale.set(scale, scale, scale);

      leafMesh.userData = {
        baseRotZ: leafMesh.rotation.z,
        phase: i * 0.8
      };

      plantGroup.add(leafMesh);
      leafMeshes.push(leafMesh);
    }

    // Apex Bud
    const budGeo = new THREE.SphereGeometry(0.18, 16, 16);
    const budMat = new THREE.MeshStandardMaterial({
      color: 0x34d399,
      emissive: 0x059669,
      emissiveIntensity: 0.45,
      roughness: 0.2
    });
    const budMesh = new THREE.Mesh(budGeo, budMat);
    budMesh.position.set(0, 4.25, 0);
    plantGroup.add(budMesh);

    // -------------------------------------------------------------
    // 35 Floating Leaves System
    // -------------------------------------------------------------
    const floatingLeaves = [];
    const floatLeafMat = new THREE.MeshStandardMaterial({
      color: 0x34d399,
      roughness: 0.35,
      metalness: 0.1,
      transparent: true,
      opacity: 0.85,
      side: THREE.DoubleSide
    });

    for (let i = 0; i < 35; i++) {
      const fl = new THREE.Mesh(leafGeo, floatLeafMat);
      fl.position.set(
        (Math.random() - 0.4) * 16,
        (Math.random() - 0.5) * 11,
        (Math.random() - 0.5) * 8
      );
      const sc = 0.18 + Math.random() * 0.26;
      fl.scale.set(sc, sc, sc);
      fl.rotation.set(
        Math.random() * Math.PI * 2,
        Math.random() * Math.PI * 2,
        Math.random() * Math.PI * 2
      );
      fl.userData = {
        velY: 0.007 + Math.random() * 0.014,
        rotSpeedX: (Math.random() - 0.5) * 0.02,
        rotSpeedY: (Math.random() - 0.5) * 0.02,
        rotSpeedZ: (Math.random() - 0.5) * 0.015
      };
      scene.add(fl);
      floatingLeaves.push(fl);
    }

    // -------------------------------------------------------------
    // Glowing Emerald Dust Particles
    // -------------------------------------------------------------
    const particleCount = 80;
    const particleGeo = new THREE.BufferGeometry();
    const positions = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount * 3; i += 3) {
      positions[i] = (Math.random() - 0.5) * 18;
      positions[i + 1] = (Math.random() - 0.5) * 12;
      positions[i + 2] = (Math.random() - 0.5) * 8;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    const particleMat = new THREE.PointsMaterial({
      color: 0x6ee7b7,
      size: 0.11,
      transparent: true,
      opacity: 0.75,
      blending: THREE.AdditiveBlending
    });
    const particles = new THREE.Points(particleGeo, particleMat);
    scene.add(particles);

    // -------------------------------------------------------------
    // Mouse Movement Parallax
    // -------------------------------------------------------------
    let mouseX = 0, mouseY = 0;
    let targetRotY = 0, targetRotX = 0;

    window.addEventListener('mousemove', function(e) {
      const rect = container.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      mouseX = (x / rect.width) * 2 - 1;
      mouseY = -(y / rect.height) * 2 + 1;
      targetRotY = mouseX * 0.45;
      targetRotX = mouseY * 0.25;
    });

    // Handle Resize
    window.addEventListener('resize', function() {
      const w = container.clientWidth;
      const h = container.clientHeight;
      if (w && h) {
        camera.aspect = w / h;
        camera.updateProjectionMatrix();
        renderer.setSize(w, h);
      }
    });

    // Animation Loop
    const clock = new THREE.Clock();
    function animate() {
      requestAnimationFrame(animate);
      const time = clock.getElapsedTime();

      // Smooth plant rotation with damped mouse follow
      plantGroup.rotation.y += (targetRotY - plantGroup.rotation.y) * 0.05 + Math.sin(time * 0.8) * 0.001;
      plantGroup.rotation.x += (targetRotX - plantGroup.rotation.x) * 0.05;

      // Soft breeze flutter on leaves
      for (let i = 0; i < leafMeshes.length; i++) {
        const lm = leafMeshes[i];
        lm.rotation.z = lm.userData.baseRotZ + Math.sin(time * 2.2 + lm.userData.phase) * 0.06;
      }

      // Apex bud subtle pulse
      const budPulse = 1.0 + Math.sin(time * 3.0) * 0.08;
      budMesh.scale.set(budPulse, budPulse, budPulse);

      // Light follow mouse
      mouseLight.position.x += (mouseX * 8 - mouseLight.position.x) * 0.06;
      mouseLight.position.y += (mouseY * 6 - mouseLight.position.y) * 0.06;

      // Floating leaves drift and tumble
      for (let i = 0; i < floatingLeaves.length; i++) {
        const fl = floatingLeaves[i];
        fl.position.y += fl.userData.velY;
        fl.rotation.x += fl.userData.rotSpeedX;
        fl.rotation.y += fl.userData.rotSpeedY;
        fl.rotation.z += fl.userData.rotSpeedZ;
        if (fl.position.y > 6.0) {
          fl.position.y = -6.0;
          fl.position.x = (Math.random() - 0.4) * 16;
        }
      }

      // Dust particle wave
      particles.rotation.y = time * 0.03;
      particles.rotation.x = Math.sin(time * 0.02) * 0.05;

      renderer.render(scene, camera);
    }
    animate();
  })();
</script>
</body>
</html>
"""
    try:
        components.html(html_code, height=620, scrolling=False)
    except Exception:
        # Fallback if headless test harness restricts iframe
        render_home_hero_fallback()


def render_home_hero_fallback() -> None:
    """Render lightweight high-impact hero fallback if iframe component is restricted."""
    bg_uri = get_asset_base64("cropyield_hero.jpg")
    bg_style = f"background: linear-gradient(rgba(7, 34, 24, 0.75), rgba(7, 34, 24, 0.88)), url('{bg_uri}') center/cover no-repeat;" if bg_uri else "background: linear-gradient(135deg, #072218 0%, #1B4332 100%);"

    st.markdown(
        f"""
        <div class="cypa-hero-container" style="{bg_style}">
            <div class="cypa-hero-inner">
                <div class="cypa-navbar">
                    <span class="cypa-brand-tag">CROPSHIELD AI 2.0</span>
                    <div class="cypa-nav-items">
                        <span class="cypa-nav-item">OVERVIEW</span>
                        <span class="cypa-nav-item">SCANNER</span>
                        <span class="cypa-nav-item">ASSISTANT</span>
                        <span class="cypa-nav-item">WEATHER</span>
                        <span class="cypa-nav-item">REPORTS</span>
                    </div>
                </div>
                <h1 class="cypa-hero-title">
                    Intelligence That Protects Every Leaf
                </h1>
                <p class="cypa-hero-subtitle">
                    Discover smarter crop monitoring with AI-powered disease detection and agricultural intelligence.
                </p>
                <div>
                    <a href="pages/2_AI_Crop_Scanner.py" target="_self" class="cypa-pill-btn">
                        <span>Start Crop Scan</span>
                        <span class="cypa-green-dot"></span>
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_home_hero() -> None:
    """Render the high-impact hero banner (forwards to 3D hero section)."""
    render_3d_hero_section()


def render_cypa_ticker() -> None:
    """Render horizontal ticker banner matching the Crop Yield Website template."""
    st.markdown(
        """
        <div class="cypa-ticker-banner">
            <div class="cypa-ticker-cell">
                <span class="cypa-arrow">&larr;</span>
                <div>
                    <div class="cypa-stat-value">28+</div>
                    <div class="cypa-stat-caption">Indian States</div>
                </div>
            </div>
            <div class="cypa-ticker-cell">
                <span class="cypa-arrow">&larr;</span>
                <div>
                    <div class="cypa-stat-value">700+</div>
                    <div class="cypa-stat-caption">Districts Monitored</div>
                </div>
            </div>
            <div class="cypa-ticker-cell">
                <span class="cypa-arrow">&larr;</span>
                <div>
                    <div class="cypa-stat-value">38+</div>
                    <div class="cypa-stat-caption">Disease Classes</div>
                </div>
            </div>
            <div class="cypa-ticker-cell">
                <span class="cypa-arrow">&larr;</span>
                <div>
                    <div class="cypa-stat-value">100%</div>
                    <div class="cypa-stat-caption">Private &amp; Offline Edge</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_cypa_about_section() -> None:
    """Render clean platform overview card avoiding oversized base64 markdown payloads."""
    st.markdown(
        """
        <div class="cypa-editorial-box">
            <h2 class="cypa-editorial-heading-gradient">Intelligence That Protects Every Leaf &amp; Harvest</h2>
            <p class="cypa-editorial-body">
                CropShield AI 2.0 combines edge deep learning computer vision and localized epidemiological analytics to deliver early disease identification and yield protection forecasts. We empower farmers, agronomists, and researchers with verified, private decision support.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_badge(text: str, variant: str = "emerald") -> str:
    """Return HTML string for a styled badge."""
    clean_text = html.escape(text)
    variant_class = f"cs-badge-{variant}" if variant in {"forest", "emerald", "amber", "crimson", "blue", "neutral"} else "cs-badge-neutral"
    return f'<span class="cs-badge {variant_class}">{clean_text}</span>'


def render_card_start(title: str = "", badge_text: str = "", badge_variant: str = "emerald") -> None:
    """Open an HTML card container with optional header."""
    badge_html = f"<div>{render_badge(badge_text, badge_variant)}</div>" if badge_text else ""
    title_html = f'<h4 class="cs-card-title">{html.escape(title)}</h4>' if title else ""
    header_html = f'<div class="cs-card-header">{title_html}{badge_html}</div>' if (title or badge_text) else ""
    st.markdown(f'<div class="cs-card">{header_html}', unsafe_allow_html=True)


def render_card_end() -> None:
    """Close an open HTML card container."""
    st.markdown("</div>", unsafe_allow_html=True)


def get_selected_language() -> str:
    """Return the active UI language code, defaulting to English."""
    selected = st.session_state.get("cropshield_language", "en")
    return selected if selected in LANGUAGES else "en"


def render_language_selector() -> None:
    """Render the sidebar language selector."""
    language = get_selected_language()
    st.sidebar.selectbox(
        translate("language", language),
        options=list(LANGUAGES),
        format_func=lambda code: LANGUAGES[code],
        key="cropshield_language",
    )


def render_trust_indicator(trust_level: str, explanation: str = "") -> None:
    """Render an authoritative, validation-calibrated trust badge and summary."""
    variant_map = {
        "High": ("forest", "✓ Calibrated High Trust"),
        "Medium": ("amber", "⚠ Medium Trust"),
        "Low": ("crimson", "✕ Low Trust — Verification Recommended"),
        "Cannot Assess": ("neutral", "⊘ Quality Restricted / Unassessable"),
    }
    variant, label = variant_map.get(trust_level, ("neutral", trust_level))
    badge = render_badge(label, variant)
    clean_expl = html.escape(explanation) if explanation else ""
    expl_html = f'<p style="font-size: 0.85rem; color: #64748B; margin: 0.35rem 0 0 0;">{clean_expl}</p>' if clean_expl else ""
    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 0.8rem 1rem; margin: 0.5rem 0 1rem 0;">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="font-size: 0.82rem; font-weight: 650; color: #1E293B; text-transform: uppercase; letter-spacing: 0.04em;">Trust Level:</span>
                {badge}
            </div>
            {expl_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# INNOVATIVE PRECISION AGRICULTURE & STORYTELLING UI COMPONENTS
# ---------------------------------------------------------------------------

def render_circular_kpi(
    title: str,
    value: str | int,
    percentage: int,
    subtitle: str,
    color: str = "#2D6A4F",
    spark_values: list[float] | None = None,
) -> None:
    """Render an interactive KPI tile with an SVG circular progress ring and optional sparkline."""
    clean_pct = max(0, min(100, int(percentage)))
    radius = 32
    circumference = 2 * 3.14159 * radius
    offset = circumference * (1.0 - (clean_pct / 100.0))

    # Sparkline polyline generator
    sparkline_html = ""
    if spark_values and len(spark_values) >= 2:
        min_v = min(spark_values)
        max_v = max(spark_values)
        rng = (max_v - min_v) if max_v > min_v else 1.0
        points = []
        w, h = 90, 26
        for i, val in enumerate(spark_values):
            x = (i / (len(spark_values) - 1)) * w
            y = h - 3 - ((val - min_v) / rng) * (h - 6)
            points.append(f"{x:.1f},{y:.1f}")
        polyline_str = " ".join(points)
        sparkline_html = f"""
        <div style="margin-top: 0.5rem; display: flex; align-items: center; justify-content: space-between;">
            <span style="font-size: 0.72rem; color: #64748B; font-weight: 550;">7-Day Trend</span>
            <svg width="{w}" height="{h}" style="overflow: visible;">
                <polyline fill="none" stroke="{color}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" points="{polyline_str}" />
            </svg>
        </div>
        """

    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.1rem 1.25rem; box-shadow: 0 4px 16px rgba(0,0,0,0.03); transition: transform 0.2s ease, box-shadow 0.2s ease;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 12px;">
                <div style="flex: 1;">
                    <span style="font-size: 0.76rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">{html.escape(title)}</span>
                    <div style="font-size: 1.65rem; font-weight: 800; color: #0D2818; margin: 0.2rem 0; line-height: 1.2;">{html.escape(str(value))}</div>
                    <div style="font-size: 0.8rem; color: #475569;">{html.escape(subtitle)}</div>
                </div>
                <div style="position: relative; width: 76px; height: 76px; display: flex; align-items: center; justify-content: center; flex-shrink: 0;">
                    <svg width="76" height="76" viewBox="0 0 76 76" style="transform: rotate(-90deg);">
                        <circle cx="38" cy="38" r="{radius}" fill="none" stroke="#E2E8F0" stroke-width="6" />
                        <circle cx="38" cy="38" r="{radius}" fill="none" stroke="{color}" stroke-width="6"
                            stroke-dasharray="{circumference}" stroke-dashoffset="{offset}" stroke-linecap="round" style="transition: stroke-dashoffset 0.8s ease;" />
                    </svg>
                    <span style="position: absolute; font-size: 0.82rem; font-weight: 750; color: #0D2818;">{clean_pct}%</span>
                </div>
            </div>
            {sparkline_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_crop_health_score_card(score_obj: Any) -> None:
    """Render prominent 0-100 Crop Health Score with severity badge and 4-factor breakdown."""
    color = getattr(score_obj, "color_hex", "#2D6A4F")
    score = getattr(score_obj, "score", 85)
    severity = getattr(score_obj, "severity", "Moderate")
    status_tag = getattr(score_obj, "status_tag", "Canopy Vigour")
    summary = getattr(score_obj, "summary", "")
    
    disease_f = getattr(score_obj, "disease_factor", 80.0)
    quality_f = getattr(score_obj, "quality_factor", 90.0)
    weather_f = getattr(score_obj, "weather_factor", 75.0)
    stage_f = getattr(score_obj, "stage_factor", 85.0)

    st.markdown(
        f"""
        <div style="background: linear-gradient(135deg, #FAF7F2 0%, #FFFFFF 100%); border: 1.5px solid {color}44; border-radius: 14px; padding: 1.4rem; box-shadow: 0 6px 20px rgba(0,0,0,0.04); margin-bottom: 1.2rem;">
            <div style="display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: 1rem; margin-bottom: 1rem;">
                <div>
                    <span style="display: inline-block; padding: 0.25rem 0.65rem; border-radius: 20px; background: {color}15; color: {color}; font-size: 0.75rem; font-weight: 750; letter-spacing: 0.05em; text-transform: uppercase;">
                        {html.escape(severity)} • {html.escape(status_tag)}
                    </span>
                    <h3 style="margin: 0.4rem 0 0.1rem 0; font-size: 1.3rem; color: #0D2818; font-weight: 750;">Integrated Crop Health Score</h3>
                    <p style="margin: 0; font-size: 0.85rem; color: #475569;">{html.escape(summary)}</p>
                </div>
                <div style="display: flex; align-items: center; gap: 0.8rem; background: #FFFFFF; border: 1px solid #E2E8F0; padding: 0.6rem 1.1rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
                    <div style="font-size: 2.2rem; font-weight: 850; color: {color}; line-height: 1;">{score}</div>
                    <div style="font-size: 0.78rem; color: #64748B; font-weight: 600; line-height: 1.2;">/ 100<br/><span style="color: {color}; font-weight: 700;">Score</span></div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 10px; margin-top: 0.8rem; border-top: 1px solid #E2E8F0; padding-top: 0.8rem;">
                <div style="background: #FFFFFF; padding: 0.5rem 0.8rem; border-radius: 8px; border: 1px solid #EEF2F6;">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Disease Index</div>
                    <div style="font-size: 0.98rem; font-weight: 750; color: #0D2818;">{disease_f:.0f}%</div>
                </div>
                <div style="background: #FFFFFF; padding: 0.5rem 0.8rem; border-radius: 8px; border: 1px solid #EEF2F6;">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Image Sharpness</div>
                    <div style="font-size: 0.98rem; font-weight: 750; color: #0D2818;">{quality_f:.0f}%</div>
                </div>
                <div style="background: #FFFFFF; padding: 0.5rem 0.8rem; border-radius: 8px; border: 1px solid #EEF2F6;">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Weather Safety</div>
                    <div style="font-size: 0.98rem; font-weight: 750; color: #0D2818;">{weather_f:.0f}%</div>
                </div>
                <div style="background: #FFFFFF; padding: 0.5rem 0.8rem; border-radius: 8px; border: 1px solid #EEF2F6;">
                    <div style="font-size: 0.72rem; color: #64748B; font-weight: 600;">Stage Resilience</div>
                    <div style="font-size: 0.98rem; font-weight: 750; color: #0D2818;">{stage_f:.0f}%</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_confidence_meter(conf_data: dict[str, str], severity: str = "Moderate") -> None:
    """Render calibrated confidence meter with visual progress bar and plain-language explanation."""
    pct_str = conf_data.get("percentage", "85.0%")
    try:
        pct_val = float(pct_str.rstrip("%"))
    except ValueError:
        pct_val = 85.0

    level = conf_data.get("level", "Calibrated Certainty")
    expl = conf_data.get("explanation", "")
    quality_note = conf_data.get("quality_note", "")

    # Meter bar color gradient
    if pct_val >= 80:
        bar_color = "linear-gradient(90deg, #52B788 0%, #2D6A4F 100%)"
        badge_variant = "forest"
    elif pct_val >= 60:
        bar_color = "linear-gradient(90deg, #DDA15E 0%, #BC6C25 100%)"
        badge_variant = "amber"
    else:
        bar_color = "linear-gradient(90deg, #E63946 0%, #9B2226 100%)"
        badge_variant = "crimson"

    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.1rem; margin: 0.8rem 0; box-shadow: 0 2px 8px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 0.8rem; font-weight: 700; color: #1E293B; text-transform: uppercase; letter-spacing: 0.04em;">Model Confidence:</span>
                    <span style="font-size: 1.05rem; font-weight: 800; color: #0D2818;">{pct_str}</span>
                </div>
                <span style="font-size: 0.75rem; font-weight: 650; padding: 0.2rem 0.55rem; border-radius: 12px; background: #EEF2F6; color: #334155;">{html.escape(level)}</span>
            </div>
            <div style="width: 100%; height: 9px; background: #E2E8F0; border-radius: 6px; overflow: hidden; margin-bottom: 0.75rem;">
                <div style="width: {pct_val}%; height: 100%; background: {bar_color}; border-radius: 6px; transition: width 0.6s ease;"></div>
            </div>
            <p style="font-size: 0.84rem; color: #475569; margin: 0; line-height: 1.45;">
                <strong>Why this prediction:</strong> {html.escape(expl)}
            </p>
            {f'<p style="font-size: 0.78rem; color: #BC6C25; margin: 0.35rem 0 0 0; font-weight: 600;">{html.escape(quality_note)}</p>' if quality_note else ""}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_second_opinion_panel(differential_list: list[dict[str, Any]]) -> None:
    """Render top-3 differential diagnoses with key symptoms and recommended next steps."""
    if not differential_list:
        return

    items_html = []
    for item in differential_list:
        rank = item.get("rank", 1)
        disease = item.get("disease", "Unknown")
        crop = item.get("crop", "")
        prob_pct = item.get("probability_pct", "0%")
        symptoms = item.get("symptoms", "")
        signs = item.get("distinguishing_signs", "")
        action = item.get("recommended_action", "")
        is_healthy = item.get("is_healthy", False)

        badge_bg = "#D8F3DC" if is_healthy else ("#FEF3C7" if rank == 2 else "#F1F5F9")
        badge_fg = "#1B4332" if is_healthy else ("#92400E" if rank == 2 else "#475569")
        rank_label = "Primary Diagnosis" if rank == 1 else f"Alternative #{rank}"

        items_html.append(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 0.9rem 1rem; margin-bottom: 0.6rem; border-left: 4px solid {'#2D6A4F' if rank == 1 else ('#DDA15E' if rank == 2 else '#94A3B8')};">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem;">
                <div>
                    <span style="font-size: 0.72rem; font-weight: 750; color: {badge_fg}; background: {badge_bg}; padding: 0.15rem 0.5rem; border-radius: 10px; text-transform: uppercase;">{rank_label}</span>
                    <strong style="font-size: 0.95rem; color: #0D2818; margin-left: 0.4rem;">{html.escape(crop)} {html.escape(disease)}</strong>
                </div>
                <span style="font-size: 0.95rem; font-weight: 800; color: #0D2818;">{prob_pct}</span>
            </div>
            <div style="font-size: 0.8rem; color: #475569; margin-bottom: 0.25rem;">
                <strong>Symptoms:</strong> {html.escape(symptoms[:140])}...
            </div>
            <div style="font-size: 0.76rem; color: #64748B;">
                <strong>Action:</strong> {html.escape(action)}
            </div>
        </div>
        """)

    all_items = "".join(items_html)
    st.markdown(
        f"""
        <div style="margin: 1rem 0;">
            <h4 style="font-size: 1.02rem; color: #0D2818; font-weight: 700; margin-bottom: 0.6rem; display: flex; align-items: center; gap: 0.4rem;">
                <span>🩺 Second Opinion &amp; Differential Diagnoses</span>
            </h4>
            {all_items}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_image_coach_hud(assessment: Any) -> None:
    """Render real-time Image Quality Coach HUD before or alongside analysis."""
    if assessment is None:
        return

    brightness = getattr(assessment, "brightness", 128.0)
    blur_score = getattr(assessment, "blur_score", 100.0)
    coverage = getattr(assessment, "leaf_coverage_fraction", 0.4)
    acceptable = getattr(assessment, "acceptable", True)
    feedback = getattr(assessment, "feedback", ())

    # Metrics
    sharp_tag = ("Sharp Focus", "#2D6A4F", "✓") if blur_score >= 60 else ("Blurry Lens", "#D90429", "⚠")
    light_tag = ("Optimal Lighting", "#2D6A4F", "✓") if 65 <= brightness <= 215 else ("Suboptimal Light", "#BC6C25", "⚠")
    cov_tag = ("Leaf In Frame", "#2D6A4F", "✓") if coverage >= 0.25 else ("Move Closer", "#BC6C25", "⚠")

    tips_html = ""
    if feedback:
        bullets = "".join([f"<li style='margin-bottom: 0.2rem;'>{html.escape(f)}</li>" for f in feedback[:3]])
        tips_html = f"<ul style='margin: 0.4rem 0 0 1rem; padding: 0; font-size: 0.78rem; color: #475569;'>{bullets}</ul>"

    hud_border = "#2D6A4F" if acceptable else "#D97706"
    hud_status = ("Image Quality Coach: Passed ✓ Ready for Diagnosis", "#2D6A4F") if acceptable else ("Image Quality Coach: Advisory Warnings", "#D97706")

    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1.5px solid {hud_border}44; border-radius: 12px; padding: 0.9rem 1.1rem; margin-bottom: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
                <span style="font-size: 0.82rem; font-weight: 750; color: {hud_status[1]}; text-transform: uppercase; letter-spacing: 0.04em;">
                    📸 {hud_status[0]}
                </span>
                <span style="font-size: 0.74rem; color: #64748B;">Offline Pre-Screening</span>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <span style="background: #FAF7F2; border: 1px solid #E2E8F0; padding: 0.25rem 0.6rem; border-radius: 8px; font-size: 0.76rem; font-weight: 650; color: {sharp_tag[1]};">
                    {sharp_tag[2]} {sharp_tag[0]} (Index: {blur_score:.0f})
                </span>
                <span style="background: #FAF7F2; border: 1px solid #E2E8F0; padding: 0.25rem 0.6rem; border-radius: 8px; font-size: 0.76rem; font-weight: 650; color: {light_tag[1]};">
                    {light_tag[2]} {light_tag[0]} (Lux: {brightness:.0f})
                </span>
                <span style="background: #FAF7F2; border: 1px solid #E2E8F0; padding: 0.25rem 0.6rem; border-radius: 8px; font-size: 0.76rem; font-weight: 650; color: {cov_tag[1]};">
                    {cov_tag[2]} {cov_tag[0]} ({coverage:.0%})
                </span>
            </div>
            {tips_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_guided_onboarding_tour() -> None:
    """Render an interactive guided onboarding tour explaining leaf scan, Grad-CAM, and treatment."""
    with st.expander("🎓 First-Time Farmer & Agronomist Guided Tour (Click to Open)", expanded=False):
        st.markdown(
            """
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; margin: 0.5rem 0;">
                <div style="background: #FAF7F2; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem;">
                    <div style="font-size: 1.4rem; margin-bottom: 0.3rem;">📸 Step 1: Capture Foliage</div>
                    <strong style="color: #0D2818; font-size: 0.9rem;">Clean Specimen Photo</strong>
                    <p style="font-size: 0.8rem; color: #475569; margin-top: 0.3rem;">
                        Hold the camera 15-20 cm from the leaf. Ensure sunlight is even and avoid direct dark shadows. The Smart Image Coach will auto-check sharpness.
                    </p>
                </div>
                <div style="background: #FAF7F2; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem;">
                    <div style="font-size: 1.4rem; margin-bottom: 0.3rem;">🔍 Step 2: Understand Grad-CAM</div>
                    <strong style="color: #0D2818; font-size: 0.9rem;">Explainable AI Heatmap</strong>
                    <p style="font-size: 0.8rem; color: #475569; margin-top: 0.3rem;">
                        Adjust the opacity slider to see where the deep neural network focused. Red/yellow regions reveal pathogen lesion margins and chlorotic rings.
                    </p>
                </div>
                <div style="background: #FAF7F2; border: 1px solid #E2E8F0; border-radius: 10px; padding: 1rem;">
                    <div style="font-size: 1.4rem; margin-bottom: 0.3rem;">📋 Step 3: Act with Precision</div>
                    <strong style="color: #0D2818; font-size: 0.9rem;">5-Step Farmer Action Plan</strong>
                    <p style="font-size: 0.8rem; color: #475569; margin-top: 0.3rem;">
                        Follow organic biological options first (Trichoderma/Neem). Only apply chemical options when necessary with certified KVK dosages and safety gear.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_action_plan_interactive(plan: dict[str, Any], key_prefix: str = "plan") -> None:
    """Render structured 5-step farmer action plan with organic IPM first, chemical backup, and checklist."""
    if not plan:
        return

    s1 = plan.get("step1_inspect", "")
    s2 = plan.get("step2_isolate", "")
    treat = plan.get("step3_treat", {})
    s4_date = plan.get("step4_rescan_date", "In 5 days")
    checklist = plan.get("step5_checklist", [])

    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.25rem; margin: 1rem 0; box-shadow: 0 4px 14px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                <h3 style="margin: 0; color: #0D2818; font-size: 1.2rem; font-weight: 750;">📋 Certified 5-Step Farmer Action Plan</h3>
                <span style="font-size: 0.75rem; font-weight: 700; background: #D8F3DC; color: #1B4332; padding: 0.2rem 0.6rem; border-radius: 12px;">ICAR / KVK IPM Standards</span>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 0.8rem; margin-bottom: 1.2rem;">
                <div style="background: #FAF7F2; padding: 0.8rem 1rem; border-radius: 8px; border-left: 4px solid #2D6A4F;">
                    <strong style="color: #0D2818; font-size: 0.88rem;">Step 1: Inspect &amp; Scout</strong>
                    <p style="margin: 0.2rem 0 0 0; font-size: 0.82rem; color: #334155;">{html.escape(s1)}</p>
                </div>
                <div style="background: #FAF7F2; padding: 0.8rem 1rem; border-radius: 8px; border-left: 4px solid #DDA15E;">
                    <strong style="color: #0D2818; font-size: 0.88rem;">Step 2: Quarantine &amp; Sanitize</strong>
                    <p style="margin: 0.2rem 0 0 0; font-size: 0.82rem; color: #334155;">{html.escape(s2)}</p>
                </div>
                <div style="background: #FAF7F2; padding: 0.8rem 1rem; border-radius: 8px; border-left: 4px solid #BC6C25;">
                    <strong style="color: #0D2818; font-size: 0.88rem;">Step 3: Treatment Protocol (Organic First)</strong>
                    <div style="margin-top: 0.3rem; font-size: 0.82rem; color: #334155;">
                        <p style="margin: 0 0 0.3rem 0;"><strong style="color: #2D6A4F;">🌿 Biological / Organic:</strong> {html.escape(treat.get('organic', ''))}</p>
                        <p style="margin: 0 0 0.3rem 0;"><strong style="color: #BC6C25;">🧪 Chemical Backup (if severe):</strong> {html.escape(treat.get('chemical', ''))}</p>
                        <p style="margin: 0 0 0.2rem 0;"><strong>Dosage:</strong> {html.escape(treat.get('dosage', ''))} | <strong>Pre-Harvest Waiting (PHI):</strong> {html.escape(treat.get('phi', '7 days'))}</p>
                        <p style="margin: 0; font-size: 0.75rem; color: #64748B;"><em>{html.escape(treat.get('safety', ''))}</em></p>
                    </div>
                </div>
                <div style="background: #FAF7F2; padding: 0.8rem 1rem; border-radius: 8px; border-left: 4px solid #0284C7;">
                    <strong style="color: #0D2818; font-size: 0.88rem;">Step 4: Scheduled Re-Scan Reminder</strong>
                    <p style="margin: 0.2rem 0 0 0; font-size: 0.82rem; color: #334155;">Next surveillance scan scheduled for: <strong>{html.escape(s4_date)}</strong></p>
                </div>
            </div>
            
            <strong style="color: #0D2818; font-size: 0.88rem;">Step 5: Farmer Field Checklist</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Interactive checkboxes for farmer execution
    for i, item in enumerate(checklist):
        st.checkbox(item, key=f"{key_prefix}_check_{i}")


def render_weather_risk_calendar_tiles(risk_data: list[dict[str, Any]]) -> None:
    """Render 7-day visual color-coded risk forecast tiles."""
    if not risk_data:
        return

    cards_html = []
    for day in risk_data:
        d_name = day.get("day", "Day")
        temp = day.get("temp", "26°C")
        hum = day.get("humidity", "80%")
        risk = day.get("risk", "Low")
        color = day.get("color", "#2D6A4F")

        cards_html.append(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-top: 4px solid {color}; border-radius: 8px; padding: 0.6rem 0.5rem; text-align: center; box-shadow: 0 2px 6px rgba(0,0,0,0.02);">
            <div style="font-size: 0.75rem; font-weight: 700; color: #64748B;">{html.escape(d_name)}</div>
            <div style="font-size: 0.92rem; font-weight: 800; color: #0D2818; margin: 0.2rem 0;">{html.escape(temp)}</div>
            <div style="font-size: 0.74rem; color: #475569;">RH: {html.escape(hum)}</div>
            <span style="display: inline-block; margin-top: 0.35rem; font-size: 0.68rem; font-weight: 750; padding: 0.15rem 0.45rem; border-radius: 10px; background: {color}15; color: {color};">
                {html.escape(risk)}
            </span>
        </div>
        """)

    all_cards = "".join(cards_html)
    st.markdown(
        f"""
        <div style="margin: 1rem 0;">
            <h4 style="font-size: 1rem; color: #0D2818; font-weight: 700; margin-bottom: 0.6rem;">📅 7-Day Disease Risk Forecast Calendar</h4>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(90px, 1fr)); gap: 8px;">
                {all_cards}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_whatsapp_and_audio_tools(whatsapp_url: str, speech_text: str, language: str = "English") -> None:
    """Render WhatsApp share button and interactive text-to-speech voice player for low-literacy accessibility."""
    escaped_speech = html.escape(speech_text).replace('"', '&quot;')
    
    st.markdown(
        f"""
        <div style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: 1rem 0;">
            <a href="{whatsapp_url}" target="_blank" style="text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem; background: #25D366; color: #FFFFFF; font-weight: 650; font-size: 0.85rem; padding: 0.55rem 1.1rem; border-radius: 8px; box-shadow: 0 2px 8px rgba(37,211,102,0.3); transition: transform 0.2s ease;">
                <span>💬 Share Diagnostic on WhatsApp</span>
            </a>
            <button onclick="
                if ('speechSynthesis' in window) {{
                    var utter = new SpeechSynthesisUtterance('{escaped_speech}');
                    utter.rate = 0.95;
                    window.speechSynthesis.cancel();
                    window.speechSynthesis.speak(utter);
                }} else {{
                    alert('Audio speech synthesis is not supported on this device.');
                }}
            " style="cursor: pointer; background: #FAF7F2; border: 1.5px solid #2D6A4F; color: #2D6A4F; font-weight: 650; font-size: 0.85rem; padding: 0.55rem 1.1rem; border-radius: 8px; display: inline-flex; align-items: center; gap: 0.5rem;">
                <span>🔊 Listen to Audio Advice ({html.escape(language)})</span>
            </button>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_what_if_simulator_widget() -> None:
    """Interactive What-If epidemiological disease risk simulator widget."""
    st.markdown("### 🔬 What-If Disease Risk Simulator")
    st.caption("Simulate how temperature, relative humidity, and irrigation shift pathogen spore pressure dynamically.")

    c1, c2, c3 = st.columns(3)
    with c1:
        sim_temp = st.slider("Ambient Temperature (°C)", 14.0, 38.0, 26.0, 0.5, key="sim_temp")
        sim_stage = st.selectbox("Crop Growth Stage", ["Seedling", "Vegetative", "Flowering", "Fruiting", "Harvest"], index=3, key="sim_stage")
    with c2:
        sim_hum = st.slider("Relative Humidity (%)", 30.0, 100.0, 85.0, 1.0, key="sim_hum")
        sim_irrig = st.selectbox("Irrigation Method", ["Drip (Under-canopy)", "Sprinkler (Overhead)", "Furrow / Flood"], index=0, key="sim_irrig")
    with c3:
        sim_rain = st.slider("24h Rainfall (mm)", 0.0, 80.0, 15.0, 1.0, key="sim_rain")

    # Dynamic calculation
    from .innovation import simulate_disease_risk
    sim_res = simulate_disease_risk(
        crop="Tomato",
        growth_stage=sim_stage,
        temp_c=sim_temp,
        humidity_pct=sim_hum,
        rainfall_mm=sim_rain,
        irrigation_type=sim_irrig.split()[0],
    )

    risk_pct = sim_res["composite_risk_pct"]
    risk_col = "#D90429" if risk_pct >= 70 else ("#DDA15E" if risk_pct >= 40 else "#2D6A4F")

    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 12px; padding: 1.2rem; margin-top: 0.8rem; box-shadow: 0 2px 10px rgba(0,0,0,0.03);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                <div>
                    <span style="font-size: 0.76rem; font-weight: 750; color: #64748B; text-transform: uppercase;">Simulated Pathogen Pressure</span>
                    <div style="font-size: 1.4rem; font-weight: 850; color: {risk_col};">{sim_res['risk_level']} Risk ({risk_pct}%)</div>
                </div>
                <div style="display: flex; gap: 8px;">
                    <span style="background: #F8F9FA; padding: 0.3rem 0.6rem; border-radius: 8px; font-size: 0.78rem; font-weight: 650; color: #0D2818;">Early Blight: {sim_res['early_blight_pct']}%</span>
                    <span style="background: #F8F9FA; padding: 0.3rem 0.6rem; border-radius: 8px; font-size: 0.78rem; font-weight: 650; color: #0D2818;">Late Blight: {sim_res['late_blight_pct']}%</span>
                    <span style="background: #F8F9FA; padding: 0.3rem 0.6rem; border-radius: 8px; font-size: 0.78rem; font-weight: 650; color: #0D2818;">Bacterial Spot: {sim_res['bacterial_pct']}%</span>
                </div>
            </div>
            <p style="font-size: 0.84rem; color: #475569; margin: 0;"><strong>Epidemiological Advisory:</strong> {html.escape(sim_res['advisory'])}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
