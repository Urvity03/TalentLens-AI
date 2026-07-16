"""TalentLens-AI Streamlit application entry point."""

import streamlit as st
from ui.cards import info_card, metric_card
from ui.navbar import render_navbar
from ui.sidebar import render_sidebar
from ui.styles import load_css

# Page Configuration
st.set_page_config(
    page_title="TalentLens-AI - Resume Intelligence",
    page_icon="🔍",
    layout="wide",
)

# Load custom CSS styles
st.markdown(f"<style>{load_css()}</style>", unsafe_allow_html=True)

# Render main header/navbar
theme = render_navbar()

# Render side document upload controls
resume_file, jd_file, analyze_clicked = render_sidebar()

st.markdown("<br>", unsafe_allow_html=True)

# KPI Dashboard Metric Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card("AHRI", "91", "Grade: A+")

with col2:
    metric_card("Resume Quality", "94", "High-quality resume")

with col3:
    metric_card("Skill Match", "88%", "Most required skills met")

with col4:
    metric_card("Potential", "90", "Level: Outstanding")

st.markdown("<br>", unsafe_allow_html=True)

# Dashboard Analysis Tabs
tab_overview, tab_skills, tab_analytics, tab_recruiter, tab_roadmap, tab_export = st.tabs([
    "Overview",
    "Skills",
    "Analytics",
    "Recruiter",
    "Career Roadmap",
    "Export",
])

with tab_overview:
    info_card(
        "Candidate Summary",
        "This section will display overall candidate information.",
    )

with tab_skills:
    info_card(
        "Skills Intelligence",
        "Matched and missing skills.",
    )

with tab_analytics:
    info_card(
        "Data Visualizations",
        "Charts will appear here.",
    )

with tab_recruiter:
    info_card(
        "Recruiter Insights",
        "Recruiter insights.",
    )

with tab_roadmap:
    info_card(
        "Career Roadmap",
        "Career roadmap.",
    )

with tab_export:
    info_card(
        "Download Report",
        "Download report.",
    )
