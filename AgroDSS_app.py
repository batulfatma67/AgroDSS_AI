from pathlib import Path
from textwrap import dedent

import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AgriDSS AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

DEFAULT_STATE = {
    "farm_data": None,
    "analysis_results": None,
    "recommendations": None,
    "report_data": None,
    "selected_page": "Dashboard",
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def render_html(content: str):
    """
    Safely render custom HTML after removing Python indentation.

    This prevents Streamlit from interpreting indented HTML
    as a Markdown code block.
    """
    st.markdown(
        dedent(content),
        unsafe_allow_html=True,
    )


def load_existing_css():
    """
    Load the existing project CSS if it exists.

    We keep the existing CSS system so the old project
    structure remains usable.
    """

    css_path = Path("styles/main.css")

    if css_path.exists():
        try:
            css = css_path.read_text(encoding="utf-8")

            st.markdown(
                f"<style>{css}</style>",
                unsafe_allow_html=True,
            )

        except Exception:
            # Do not allow an optional CSS problem
            # to crash the complete application.
            pass


# ============================================================
# LOAD EXISTING CSS
# ============================================================

load_existing_css()


# ============================================================
# NEW APPLICATION STYLING
# ============================================================

render_html(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    .main-header {
        padding: 10px 0 5px 0;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #14532d;
        margin-bottom: 0;
        line-height: 1.2;
    }

    .main-subtitle {
        font-size: 16px;
        color: #64748b;
        margin-top: 8px;
        margin-bottom: 25px;
        line-height: 1.6;
    }


    /* ========================================================
       HERO CARD
       ======================================================== */

    .hero-card {
        background:
            linear-gradient(
                135deg,
                #14532d 0%,
                #166534 55%,
                #15803d 100%
            );

        padding: 30px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;

        box-shadow:
            0 10px 30px rgba(15, 23, 42, 0.12);
    }

    .hero-title {
        font-size: 30px;
        font-weight: 800;
        margin-bottom: 10px;
        line-height: 1.3;
    }

    .hero-text {
        font-size: 16px;
        line-height: 1.7;
        color: #ecfdf5;
        max-width: 900px;
    }


    /* ========================================================
       FEATURE CARDS
       ======================================================== */

    .feature-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;

        padding: 22px;

        min-height: 160px;

        box-shadow:
            0 4px 15px rgba(15, 23, 42, 0.05);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .feature-card:hover {
        transform: translateY(-3px);

        box-shadow:
            0 8px 24px rgba(15, 23, 42, 0.10);
    }

    .feature-icon {
        font-size: 30px;
        margin-bottom: 10px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 750;
        color: #14532d;
        margin-bottom: 7px;
    }

    .feature-description {
        font-size: 14px;
        color: #64748b;
        line-height: 1.6;
    }


    /* ========================================================
       STATUS CARD
       ======================================================== */

    .status-card {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 14px;

        padding: 18px;

        margin-top: 20px;
        margin-bottom: 25px;
    }

    .status-title {
        font-weight: 750;
        color: #166534;
        margin-bottom: 5px;
        font-size: 15px;
    }

    .status-text {
        color: #475569;
        font-size: 14px;
        line-height: 1.5;
    }


    /* ========================================================
       SIDEBAR BRAND
       ======================================================== */

    .app-brand {
        text-align: center;
        padding: 10px 5px 20px 5px;
    }

    .app-brand-icon {
        font-size: 42px;
        margin-bottom: 5px;
    }

    .app-brand-title {
        color: white;
        font-size: 25px;
        font-weight: 800;
    }

    .app-brand-subtitle {
        color: #dcfce7;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 6px;
    }


    /* ========================================================
       SIDEBAR INFORMATION
       ======================================================== */

    .sidebar-info {
        color: #dcfce7;
        font-size: 12px;
        line-height: 1.8;
    }

    .sidebar-info-title {
        color: white;
        font-weight: 700;
        margin-bottom: 5px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .app-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding: 35px 0 10px 0;
        line-height: 1.6;
    }


    /* ========================================================
       STREAMLIT BUTTON IMPROVEMENT
       ======================================================== */

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    </style>
    """
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    render_html(
        """
        <div class="app-brand">

            <div class="app-brand-icon">
                🌾
            </div>

            <div class="app-brand-title">
                AgriDSS AI
            </div>

            <div class="app-brand-subtitle">
                AI-Powered Agricultural<br>
                Decision Support System
            </div>

        </div>
        """
    )

    st.divider()

    # --------------------------------------------------------
    # NAVIGATION
    # --------------------------------------------------------

    st.markdown("### 🌐 Navigation")

    page = st.radio(
        "Application",
        [
            "Dashboard",
            "Farm Intelligence",
            "AI Agronomist",
            "Satellite Intelligence",
            "Water Management",
            "Reports",
        ],
        label_visibility="collapsed",
    )

    st.session_state["selected_page"] = page

    st.divider()

    # --------------------------------------------------------
    # SIDEBAR INFORMATION
    # --------------------------------------------------------

    render_html(
        """
        <div class="sidebar-info">

            <div class="sidebar-info-title">
                AgriDSS AI
            </div>

            Precision Agriculture<br>
            GIS & Remote Sensing<br>
            Weather Intelligence<br>
            Water Management<br>
            AI & Generative AI

        </div>
        """
    )


# ============================================================
# DASHBOARD
# ============================================================

def render_dashboard():

    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    render_html(
        """
        <div class="main-header">

            <div class="main-title">
                AgriDSS AI
            </div>

            <div class="main-subtitle">
                Intelligent agricultural decision support for
                farmers, researchers and agricultural professionals.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    render_html(
        """
        <div class="hero-card">

            <div class="hero-title">
                🌱 Farm Intelligence, Powered by AI
            </div>

            <div class="hero-text">
                AgriDSS AI brings together farm information,
                satellite observations, weather intelligence,
                agricultural calculations and generative AI
                to support evidence-based farm decisions.
            </div>

        </div>
        """
    )


    # --------------------------------------------------------
    # QUICK STATUS
    # --------------------------------------------------------

    farm = st.session_state.get("farm_data")

    if farm:

        crop = farm.get(
            "crop",
            "Not specified"
        )

        district = farm.get(
            "district",
            "Not identified"
        )

        render_html(
            f"""
            <div class="status-card">

                <div class="status-title">
                    ✓ Farm Profile Available
                </div>

                <div class="status-text">
                    Current crop:
                    <b>{crop}</b>
                    &nbsp; | &nbsp;
                    Location:
                    <b>{district}</b>
                </div>

            </div>
            """
        )

    else:

        render_html(
            """
            <div class="status-card">

                <div class="status-title">
                    ○ No Farm Profile Yet
                </div>

                <div class="status-text">
                    Configure a farm to begin agricultural
                    intelligence analysis.
                </div>

            </div>
            """
        )


    # --------------------------------------------------------
    # INTELLIGENCE MODULES
    # --------------------------------------------------------

    st.markdown("### 🧠 Intelligence Modules")

    # --------------------------------------------------------
    # ROW 1
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        render_html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    👨‍🌾
                </div>

                <div class="feature-title">
                    Farm Intelligence
                </div>

                <div class="feature-description">
                    Store farm information, crop details,
                    location and field characteristics.
                </div>

            </div>
            """
        )

    with col2:

        render_html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🛰️
                </div>

                <div class="feature-title">
                    Satellite Intelligence
                </div>

                <div class="feature-description">
                    Analyze vegetation conditions using
                    satellite-derived indicators such as NDVI.
                </div>

            </div>
            """
        )

    with col3:

        render_html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🌦️
                </div>

                <div class="feature-title">
                    Weather Intelligence
                </div>

                <div class="feature-description">
                    Combine weather information with farm
                    conditions for agricultural decision support.
                </div>

            </div>
            """
        )


    st.write("")


    # --------------------------------------------------------
    # ROW 2
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        render_html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    💧
                </div>

                <div class="feature-title">
                    Water Management
                </div>

                <div class="feature-description">
                    Calculate crop water requirements,
                    irrigation needs and water-use indicators.
                </div>

            </div>
            """
        )

    with col2:

        render_html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    🤖
                </div>

                <div class="feature-title">
                    AI Agronomist
                </div>

                <div class="feature-description">
                    Ask agricultural questions and receive
                    evidence-grounded AI assistance.
                </div>

            </div>
            """
        )

    with col3:

        render_html(
            """
            <div class="feature-card">

                <div class="feature-icon">
                    📄
                </div>

                <div class="feature-title">
                    Smart Reports
                </div>

                <div class="feature-description">
                    Generate structured farm intelligence
                    reports from available analysis results.
                </div>

            </div>
            """
        )


# ============================================================
# PLACEHOLDER PAGES
# ============================================================

def render_placeholder(
    title: str,
    icon: str,
    description: str,
):

    render_html(
        f"""
        <div class="main-header">

            <div class="main-title">
                {icon} {title}
            </div>

            <div class="main-subtitle">
                {description}
            </div>

        </div>
        """
    )

    st.info(
        "This module will be connected during the next "
        "development step."
    )


# ============================================================
# PAGE ROUTING
# ============================================================

if page == "Dashboard":

    render_dashboard()


elif page == "Farm Intelligence":

    render_placeholder(
        "Farm Intelligence",
        "👨‍🌾",
        "Farm profiles, field information and agricultural data.",
    )


elif page == "AI Agronomist":

    render_placeholder(
        "AI Agronomist",
        "🤖",
        "Generative AI assistance for agricultural questions.",
    )


elif page == "Satellite Intelligence":

    render_placeholder(
        "Satellite Intelligence",
        "🛰️",
        "Satellite imagery, NDVI and vegetation intelligence.",
    )


elif page == "Water Management":

    render_placeholder(
        "Water Management",
        "💧",
        "Agricultural water requirement and irrigation intelligence.",
    )


elif page == "Reports":

    render_placeholder(
        "Reports",
        "📄",
        "Farm intelligence reports and decision summaries.",
    )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="app-footer">

        AgriDSS AI · Agricultural Intelligence Platform<br>
        GIS · Remote Sensing · Weather · Water · AI

    </div>
    """
)
