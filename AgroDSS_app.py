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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       GLOBAL
    ------------------------------------------------------- */

    .stApp {
        background-color: #f6f8f7;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* -------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #102a24;
    }

    section[data-testid="stSidebar"] * {
        color: #f4f8f6;
    }

    section[data-testid="stSidebar"] .stButton button {
        width: 100%;
        text-align: left;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        background-color: rgba(255, 255, 255, 0.04);
        color: #f4f8f6;
        padding: 0.65rem 0.85rem;
        margin-bottom: 0.25rem;
        transition: 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.10);
        border-color: rgba(255, 255, 255, 0.16);
    }

    /* -------------------------------------------------------
       HEADINGS
    ------------------------------------------------------- */

    h1 {
        color: #173b32;
        font-weight: 750;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #173b32;
        font-weight: 700;
    }

    h3 {
        color: #24564a;
        font-weight: 650;
    }

    /* -------------------------------------------------------
       STREAMLIT CONTAINERS
    ------------------------------------------------------- */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
    }

    /* -------------------------------------------------------
       METRICS
    ------------------------------------------------------- */

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e1e8e4;
        border-radius: 14px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(20, 50, 40, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #60756e;
    }

    div[data-testid="stMetricValue"] {
        color: #173b32;
        font-weight: 750;
    }

    /* -------------------------------------------------------
       BUTTONS
    ------------------------------------------------------- */

    .stButton button {
        border-radius: 9px;
        font-weight: 600;
    }

    /* -------------------------------------------------------
       INFO / SUCCESS / WARNING BOXES
    ------------------------------------------------------- */

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* -------------------------------------------------------
       FOOTER
    ------------------------------------------------------- */

    .footer-text {
        text-align: center;
        color: #71827c;
        font-size: 0.85rem;
        margin-top: 2rem;
        padding-top: 1.5rem;
        border-top: 1px solid #dfe6e2;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:

    st.title("🌾 AgriDSS AI")

    st.caption("AI-Powered Agricultural Decision Support System")

    st.divider()

    st.subheader("Navigation")

    navigation_items = [
        ("📊", "Dashboard"),
        ("👨‍🌾", "Farmer & Farm"),
        ("🛰️", "Satellite Intelligence"),
        ("🌦️", "Weather Intelligence"),
        ("💧", "Water & Irrigation"),
        ("🤖", "AI Agronomist"),
        ("📚", "Knowledge Base"),
        ("📄", "Reports"),
    ]

    for icon, page_name in navigation_items:

        if st.button(
            f"{icon}  {page_name}",
            key=f"nav_{page_name}",
            use_container_width=True,
        ):
            st.session_state.current_page = page_name
            st.rerun()

    st.divider()

    st.subheader("System")

    st.success("Application Online")

    st.caption("AgriDSS AI • Development Version")

    st.caption("Step 1: Application Foundation")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def section_header(title, description=None):

    st.header(title)

    if description:
        st.caption(description)


def feature_card(icon, title, description, status="Coming Soon"):

    with st.container(border=True):

        st.subheader(f"{icon} {title}")

        st.write(description)

        if status == "Available":
            st.success(status)

        elif status == "Development":
            st.warning(status)

        else:
            st.info(status)


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    st.title("🌾 AgriDSS AI")

    st.subheader("AI-Powered Agricultural Decision Support System")

    st.write(
        "A unified platform for farm intelligence, satellite analysis, "
        "weather information, irrigation decision support, agricultural "
        "knowledge retrieval, and AI-assisted recommendations."
    )

    st.divider()

    # --------------------------------------------------------
    # SYSTEM STATUS
    # --------------------------------------------------------

    st.subheader("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "System Status",
            "Online",
            "Ready",
        )

    with col2:
        st.metric(
            "Farm Records",
            "0",
            "To be added",
        )

    with col3:
        st.metric(
            "Satellite",
            "Ready",
            "NDVI module",
        )

    with col4:
        st.metric(
            "AI Engine",
            "Ready",
            "Integration planned",
        )

    st.divider()

    # --------------------------------------------------------
    # FARM INTELLIGENCE
    # --------------------------------------------------------

    st.subheader("Farm Intelligence")

    st.write(
        "AgriDSS AI will combine multiple agricultural information "
        "sources into one decision-support workflow."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        feature_card(
            "👨‍🌾",
            "Farmer & Farm",
            "Create farmer profiles, add farms and fields, "
            "and maintain the agricultural information required "
            "for personalized decision support.",
            "Development",
        )

    with col2:

        feature_card(
            "🛰️",
            "Satellite Intelligence",
            "Analyze vegetation conditions using satellite "
            "imagery and vegetation indices such as NDVI.",
            "Development",
        )

    with col3:

        feature_card(
            "🌦️",
            "Weather Intelligence",
            "Use weather observations and forecasts to support "
            "crop and water-management decisions.",
            "Development",
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        feature_card(
            "💧",
            "Water & Irrigation",
            "Calculate crop water requirements and irrigation "
            "requirements using agricultural engineering equations.",
            "Development",
        )

    with col2:

        feature_card(
            "🤖",
            "AI Agronomist",
            "Provide grounded agricultural explanations and "
            "recommendations using farm data and relevant evidence.",
            "Coming Soon",
        )

    with col3:

        feature_card(
            "📚",
            "Knowledge Base",
            "Retrieve information from agricultural documents "
            "through a Retrieval-Augmented Generation workflow.",
            "Coming Soon",
        )

    st.divider()

    # --------------------------------------------------------
    # CURRENT DEVELOPMENT ROADMAP
    # --------------------------------------------------------

    st.subheader("Development Roadmap")

    roadmap = [
        ("01", "Application Foundation", "Completed"),
        ("02", "Farmer & Farm Management", "Next"),
        ("03", "GIS & Farm Location", "Planned"),
        ("04", "Weather Intelligence", "Planned"),
        ("05", "Irrigation Calculation Engine", "Planned"),
        ("06", "Satellite & NDVI Intelligence", "Planned"),
        ("07", "Agricultural RAG", "Planned"),
        ("08", "AI Agronomist", "Planned"),
        ("09", "Agentic Decision Workflow", "Planned"),
        ("10", "Reports & Final Integration", "Planned"),
    ]

    for number, title, status in roadmap:

        with st.container(border=True):

            col1, col2, col3 = st.columns([1, 5, 2])

            with col1:
                st.markdown(f"### {number}")

            with col2:
                st.write(f"**{title}**")

            with col3:

                if status == "Completed":
                    st.success(status)

                elif status == "Next":
                    st.warning(status)

                else:
                    st.info(status)

    st.divider()

    # --------------------------------------------------------
    # QUICK ACTIONS
    # --------------------------------------------------------

    st.subheader("Quick Actions")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        if st.button(
            "➕ Add Farmer",
            use_container_width=True,
        ):
            st.session_state.current_page = "Farmer & Farm"
            st.rerun()

    with col2:

        if st.button(
            "🛰️ Satellite Analysis",
            use_container_width=True,
        ):
            st.session_state.current_page = "Satellite Intelligence"
            st.rerun()

    with col3:

        if st.button(
            "💧 Water Analysis",
            use_container_width=True,
        ):
            st.session_state.current_page = "Water & Irrigation"
            st.rerun()

    with col4:

        if st.button(
            "🤖 Ask AI Agronomist",
            use_container_width=True,
        ):
            st.session_state.current_page = "AI Agronomist"
            st.rerun()


# ============================================================
# FARMER & FARM
# ============================================================

def show_farmer_farm():

    section_header(
        "👨‍🌾 Farmer & Farm",
        "Manage farmer profiles, farms, fields, crops, and basic "
        "agricultural information.",
    )

    st.info(
        "This module will become the central source of farmer and "
        "farm information used by the AI decision-support workflow."
    )

    tab1, tab2 = st.tabs(
        [
            "Farmer Information",
            "Farm / Field Information",
        ]
    )

    with tab1:

        st.subheader("Farmer Profile")

        col1, col2 = st.columns(2)

        with col1:

            st.text_input(
                "Farmer Name",
                placeholder="Enter farmer name",
            )

            st.text_input(
                "Phone Number",
                placeholder="Optional",
            )

        with col2:

            st.text_input(
                "Village / Area",
                placeholder="Enter village or area",
            )

            st.selectbox(
                "Province",
                [
                    "Select province",
                    "Punjab",
                    "Sindh",
                    "Khyber Pakhtunkhwa",
                    "Balochistan",
                    "Gilgit-Baltistan",
                    "Azad Jammu & Kashmir",
                ],
            )

        if st.button(
            "Save Farmer",
            type="primary",
        ):
            st.success(
                "Farmer interface is ready. Database integration "
                "will be added in the next development stage."
            )

    with tab2:

        st.subheader("Farm / Field")

        col1, col2 = st.columns(2)

        with col1:

            st.text_input(
                "Farm Name",
                placeholder="e.g. Main Farm",
            )

            st.number_input(
                "Farm Area (acres)",
                min_value=0.0,
                step=0.1,
            )

            st.selectbox(
                "Crop",
                [
                    "Select crop",
                    "Wheat",
                    "Rice",
                    "Maize",
                    "Cotton",
                    "Sugarcane",
                    "Other",
                ],
            )

        with col2:

            st.number_input(
                "Latitude",
                value=31.5204,
                format="%.6f",
            )

            st.number_input(
                "Longitude",
                value=74.3587,
                format="%.6f",
            )

            st.selectbox(
                "Irrigation System",
                [
                    "Select irrigation system",
                    "Canal",
                    "Tubewell",
                    "Drip",
                    "Sprinkler",
                    "Flood",
                    "Other",
                ],
            )

        if st.button(
            "Save Farm",
            type="primary",
        ):
            st.success(
                "Farm interface is ready. Persistent farm storage "
                "will be connected in the next stage."
            )


# ============================================================
# SATELLITE INTELLIGENCE
# ============================================================

def show_satellite():

    section_header(
        "🛰️ Satellite Intelligence",
        "Satellite-based agricultural monitoring and vegetation intelligence.",
    )

    st.info(
        "Your existing Sentinel-2 / NDVI functionality will be "
        "integrated into this section rather than rebuilt unnecessarily."
    )

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("Satellite Analysis")

            st.selectbox(
                "Satellite Source",
                [
                    "Sentinel-2",
                    "Landsat",
                    "Other",
                ],
            )

            st.selectbox(
                "Analysis",
                [
                    "NDVI",
                    "Vegetation Health",
                    "Temporal NDVI",
                    "Other",
                ],
            )

            st.date_input(
                "Analysis Date",
            )

            st.button(
                "Run Satellite Analysis",
                type="primary",
                use_container_width=True,
            )

    with col2:

        with st.container(border=True):

            st.subheader("Vegetation Indicators")

            st.metric(
                "NDVI Mean",
                "—",
            )

            st.metric(
                "NDVI Minimum",
                "—",
            )

            st.metric(
                "NDVI Maximum",
                "—",
            )

            st.caption(
                "Live satellite values will appear after farm "
                "location and satellite services are connected."
            )


# ============================================================
# WEATHER INTELLIGENCE
# ============================================================

def show_weather():

    section_header(
        "🌦️ Weather Intelligence",
        "Weather observations and forecasts for agricultural decision support.",
    )

    st.info(
        "The existing Open-Meteo service can be connected here "
        "without changing the overall application architecture."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Temperature",
            "— °C",
        )

    with col2:
        st.metric(
            "Rainfall",
            "— mm",
        )

    with col3:
        st.metric(
            "Humidity",
            "— %",
        )

    with col4:
        st.metric(
            "Wind",
            "— km/h",
        )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("Location")

            st.text_input(
                "Latitude",
                value="31.5204",
            )

            st.text_input(
                "Longitude",
                value="74.3587",
            )

            st.button(
                "Get Weather",
                type="primary",
                use_container_width=True,
            )

    with col2:

        with st.container(border=True):

            st.subheader("Forecast")

            st.write(
                "Weather forecast data will appear here after "
                "the weather service is connected."
            )


# ============================================================
# WATER & IRRIGATION
# ============================================================

def show_water_irrigation():

    section_header(
        "💧 Water & Irrigation",
        "Agricultural water requirement and irrigation decision support.",
    )

    st.info(
        "This module will use agricultural engineering calculations "
        "separately from the AI model. The AI will explain the results "
        "rather than inventing numerical values."
    )

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("Crop Water Inputs")

            crop = st.selectbox(
                "Crop",
                [
                    "Wheat",
                    "Rice",
                    "Maize",
                    "Cotton",
                    "Sugarcane",
                ],
            )

            area = st.number_input(
                "Farm Area (hectares)",
                min_value=0.01,
                value=1.0,
                step=0.1,
            )

            et0 = st.number_input(
                "Reference ET₀ (mm/day)",
                min_value=0.0,
                value=5.0,
                step=0.1,
            )

            kc = st.number_input(
                "Crop Coefficient Kc",
                min_value=0.0,
                value=1.0,
                step=0.05,
            )

            rainfall = st.number_input(
                "Effective Rainfall (mm)",
                min_value=0.0,
                value=0.0,
                step=0.1,
            )

            efficiency = st.number_input(
                "Irrigation Efficiency (%)",
                min_value=1.0,
                max_value=100.0,
                value=70.0,
                step=1.0,
            )

    with col2:

        with st.container(border=True):

            st.subheader("Calculation Preview")

            etc = et0 * kc

            net_irrigation = max(
                etc - rainfall,
                0.0,
            )

            gross_irrigation = (
                net_irrigation / (efficiency / 100)
                if efficiency > 0
                else 0
            )

            water_volume_m3 = (
                gross_irrigation
                * area
                * 10
            )

            st.metric(
                "Crop ETc",
                f"{etc:.2f} mm/day",
            )

            st.metric(
                "Net Irrigation Requirement",
                f"{net_irrigation:.2f} mm",
            )

            st.metric(
                "Gross Irrigation Requirement",
                f"{gross_irrigation:.2f} mm",
            )

            st.metric(
                "Approx. Water Volume",
                f"{water_volume_m3:.2f} m³",
            )

            st.caption(
                f"Calculation preview for {crop}. "
                "The final calculation engine will include "
                "crop stage, soil, rainfall, and other relevant inputs."
            )


# ============================================================
# AI AGRONOMIST
# ============================================================

def show_ai_agronomist():

    section_header(
        "🤖 AI Agronomist",
        "AI-assisted agricultural reasoning and decision support.",
    )

    st.info(
        "The AI Agronomist will later combine farmer data, "
        "satellite observations, weather, numerical calculations, "
        "and the agricultural knowledge base."
    )

    with st.container(border=True):

        st.subheader("Ask the AI Agronomist")

        question = st.text_area(
            "Agricultural Question",
            placeholder=(
                "Example: My wheat field has declining NDVI and "
                "the weather has been unusually dry. What should I check?"
            ),
            height=150,
        )

        if st.button(
            "Ask AI Agronomist",
            type="primary",
        ):

            if question.strip():

                st.warning(
                    "The AI model is not connected yet. "
                    "RAG and agent integration will be added in later stages."
                )

            else:

                st.warning(
                    "Please enter an agricultural question."
                )

    st.divider()

    st.subheader("Planned AI Workflow")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.info(
            "1. Understand\n\n"
            "Identify the farmer's question and intent."
        )

    with col2:

        st.info(
            "2. Retrieve\n\n"
            "Retrieve relevant agricultural evidence."
        )

    with col3:

        st.info(
            "3. Analyze\n\n"
            "Combine tools, calculations and farm information."
        )

    with col4:

        st.info(
            "4. Explain\n\n"
            "Return an evidence-based recommendation."
        )


# ============================================================
# KNOWLEDGE BASE
# ============================================================

def show_knowledge_base():

    section_header(
        "📚 Knowledge Base",
        "Agricultural document retrieval and grounded AI knowledge.",
    )

    st.info(
        "This section will become the RAG knowledge layer of AgriDSS AI."
    )

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader("Knowledge Categories")

            st.write("💧 Irrigation")
            st.write("🌱 Crops")
            st.write("🌍 Climate")
            st.write("💦 Groundwater")
            st.write("🛰️ Remote Sensing")

    with col2:

        with st.container(border=True):

            st.subheader("RAG Pipeline")

            st.write("1. Upload agricultural documents")
            st.write("2. Extract document text")
            st.write("3. Clean and chunk content")
            st.write("4. Generate embeddings")
            st.write("5. Store vectors")
            st.write("6. Retrieve relevant evidence")
            st.write("7. Generate grounded response")

            st.info(
                "FAISS + embeddings + Groq-based LLM integration "
                "will be implemented in the RAG stage."
            )


# ============================================================
# REPORTS
# ============================================================

def show_reports():

    section_header(
        "📄 Reports",
        "Generate structured agricultural decision-support reports.",
    )

    st.info(
        "Your existing ReportLab report functionality will be "
        "integrated into the final workflow."
    )

    with st.container(border=True):

        st.subheader("Report Contents")

        col1, col2 = st.columns(2)

        with col1:

            st.checkbox(
                "Farmer Information",
                value=True,
            )

            st.checkbox(
                "Farm / Field Information",
                value=True,
            )

            st.checkbox(
                "Weather Information",
                value=True,
            )

            st.checkbox(
                "Satellite / NDVI Analysis",
                value=True,
            )

        with col2:

            st.checkbox(
                "Water Requirement",
                value=True,
            )

            st.checkbox(
                "AI Recommendations",
                value=True,
            )

            st.checkbox(
                "Risks & Limitations",
                value=True,
            )

            st.checkbox(
                "Data Sources",
                value=True,
            )

        st.divider()

        st.button(
            "Generate Report",
            type="primary",
            use_container_width=True,
        )


# ============================================================
# PAGE ROUTER
# ============================================================

page = st.session_state.current_page


if page == "Dashboard":

    show_dashboard()

elif page == "Farmer & Farm":

    show_farmer_farm()

elif page == "Satellite Intelligence":

    show_satellite()

elif page == "Weather Intelligence":

    show_weather()

elif page == "Water & Irrigation":

    show_water_irrigation()

elif page == "AI Agronomist":

    show_ai_agronomist()

elif page == "Knowledge Base":

    show_knowledge_base()

elif page == "Reports":

    show_reports()

else:

    show_dashboard()


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer-text">
        AgriDSS AI • Agricultural Intelligence Platform • Development Version
    </div>
    """,
    unsafe_allow_html=True,
)
