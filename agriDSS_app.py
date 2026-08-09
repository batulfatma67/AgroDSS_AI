from pathlib import Path

import streamlit as st

from ui.input_page import render_input_page
from ui.dashboard_page import render_dashboard_page
from ui.recommendation_page import render_recommendation_page
from ui.report_page import render_report_page


# ============================================================
# APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AgriDSS AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# LOAD APPLICATION STYLES
# ============================================================

CSS_PATH = Path("styles/main.css")

if CSS_PATH.exists():
    st.markdown(
        f"<style>{CSS_PATH.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# ============================================================
# SESSION STATE
# ============================================================

if "farm_data" not in st.session_state:
    st.session_state.farm_data = None

if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = None

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "report_map_path" not in st.session_state:
    st.session_state.report_map_path = None


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🌾</div>
            <div class="brand-title">AgriDSS AI</div>
            <div class="brand-subtitle">
                Agricultural Decision Support System
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "01 · Farm Data Input",
            "02 · Dashboard",
            "03 · Recommendation",
            "04 · Report",
        ],
        label_visibility="collapsed",
    )

    st.divider()

    st.caption(
        "Precision agriculture • GIS • Remote sensing • "
        "Weather intelligence"
    )


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "01 · Farm Data Input":

    render_input_page()

elif page == "02 · Dashboard":

    render_dashboard_page()

elif page == "03 · Recommendation":

    render_recommendation_page()

elif page == "04 · Report":

    render_report_page()
