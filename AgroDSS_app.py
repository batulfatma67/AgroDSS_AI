from pathlib import Path

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
# CUSTOM CSS
# ============================================================

def load_css():
    """
    Load the existing CSS file.

    The existing application already has a CSS system,
    so we reuse it instead of creating another stylesheet.
    """

    css_path = Path("styles/main.css")

    if css_path.exists():
        css = css_path.read_text(encoding="utf-8")
        st.markdown(
            f"<style>{css}</style>",
            unsafe_allow_html=True,
        )


load_css()


# ============================================================
# NEW APPLICATION STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* --------------------------------------------------------
       MAIN CONTENT
       -------------------------------------------------------- */

    .main-header {
        padding: 10px 0 5px 0;
    }

    .main-title {
        font-size: 38px;
        font-weight: 800;
        color: #14532d;
        margin-bottom: 0;
    }

    .main-subtitle {
        font-size: 16px;
        color: #64748b;
        margin-top: 4px;
        margin-bottom: 25px;
    }


    /* --------------------------------------------------------
       HERO CARD
       -------------------------------------------------------- */

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
        margin-bottom: 8px;
    }

    .hero-text {
        font-size: 16px;
        line-height: 1.6;
        color: #ecfdf5;
        max-width: 850px;
    }


    /* --------------------------------------------------------
       FEATURE CARDS
       -------------------------------------------------------- */

    .feature-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 16px;

        padding: 22px;

        min-height: 150px;

        box-shadow:
            0 4px 15px rgba(15, 23, 42, 0.05);
    }

    .feature-icon {
        font-size: 30px;
        margin-bottom: 8px;
    }

    .feature-title {
        font-size: 18px;
        font-weight: 750;
        color: #14532d;
        margin-bottom: 5px;
    }

    .feature-description {
        font-size: 14px;
        color: #64748b;
        line-height: 1.5;
    }


    /* --------------------------------------------------------
       STATUS CARD
       -------------------------------------------------------- */

    .status-card {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        border-radius: 14px;

        padding: 18px;

        margin-top: 20px;
    }

    .status-title {
        font-weight: 750;
        color: #166534;
        margin-bottom: 5px;
    }

    .status-text {
        color: #475569;
        font-size: 14px;
    }


    /* --------------------------------------------------------
       SIDEBAR BRAND
       -------------------------------------------------------- */

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
        line-height: 1.4;
        margin-top: 5px;
    }


    /* --------------------------------------------------------
       FOOTER
       -------------------------------------------------------- */

    .app-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 12px;
        padding: 30px 0 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        "### 🌐 Navigation"
    )

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

    st.markdown(
        """
        <div style="
            color:#dcfce7;
            font-size:12px;
            line-height:1.6;
        ">

        <b>AgriDSS AI</b><br>
        Precision Agriculture<br>
        GIS & Remote Sensing<br>
        Weather Intelligence<br>
        AI & Generative AI

        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DASHBOARD
# ============================================================

def render_dashboard():

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # HERO
    # --------------------------------------------------------

    st.markdown(
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
        """,
        unsafe_allow_html=True,
    )


    # --------------------------------------------------------
    # QUICK STATUS
    # --------------------------------------------------------

    farm = st.session_state.get("farm_data")

    if farm:

        crop = farm.get("crop", "Not specified")
        district = farm.get("district", "Not identified")

        st.markdown(
            f"""
            <div class="status-card">

                <div class="status-title">
                    ✓ Farm Profile Available
                </div>

                <div class="status-text">
                    Current crop: <b>{crop}</b>
                    &nbsp; | &nbsp;
                    Location: <b>{district}</b>
                </div>

            </div>
            """,
            unsafe_allow_html=True,
        )

    else:

        st.markdown(
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
            """,
            unsafe_allow_html=True,
        )


    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    st.markdown(
        "### 🧠 Intelligence Modules"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
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
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
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
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
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
            """,
            unsafe_allow_html=True,
        )


    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
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
            """,
            unsafe_allow_html=True,
        )

    with col2:

        st.markdown(
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
            """,
            unsafe_allow_html=True,
        )

    with col3:

        st.markdown(
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
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# PLACEHOLDER PAGES
# ============================================================

def render_placeholder(title, icon, description):

    st.markdown(
        f"""
        <div class="main-header">

            <div class="main-title">
                {icon} {title}
            </div>

            <div class="main-subtitle">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
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

st.markdown(
    """
    <div class="app-footer">

        AgriDSS AI · Agricultural Intelligence Platform<br>
        GIS · Remote Sensing · Weather · Water · AI

    </div>
    """,
    unsafe_allow_html=True,
)
