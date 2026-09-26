import streamlit as st
from datetime import date

import folium
from streamlit_folium import st_folium

from database import (
    add_farmer,
    add_farm,
    add_field,
    get_farmers,
    get_farms,
    get_fields,
    get_farms_by_farmer,
    get_dashboard_statistics,
)

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
    ("🗺️", "GIS & Farm Map"),
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
    stats = get_dashboard_statistics()
    
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
            "Farmers",
            stats["farmers"],
        )

    with col2:
        st.metric(
            "Farms",
            stats["farms"],
        )

    with col3:
        st.metric(
            "Fields",
            stats["fields"],
        )

    with col4:
        st.metric(
            "Active Crops",
            stats["crops"],
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
        "Manage farmers, farms, fields and crop information.",
    )

    tab1, tab2, tab3 = st.tabs(
        [
            "👨‍🌾 Farmers",
            "🚜 Farms",
            "🌱 Fields",
        ]
    )

    # ========================================================
    # FARMERS
    # ========================================================

    with tab1:

        st.subheader("Add Farmer")

        with st.form("farmer_form"):

            col1, col2 = st.columns(2)

            with col1:

                farmer_name = st.text_input(
                    "Farmer Name *",
                    placeholder="Enter farmer name",
                )

                phone = st.text_input(
                    "Phone Number",
                    placeholder="Optional",
                )

            with col2:

                village = st.text_input(
                    "Village / Area",
                    placeholder="Enter village or area",
                )

                province = st.selectbox(
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

            submitted = st.form_submit_button(
                "Save Farmer",
                type="primary",
                use_container_width=True,
            )

            if submitted:

                if not farmer_name.strip():

                    st.error(
                        "Farmer name is required."
                    )

                else:

                    if province == "Select province":
                        province = ""

                    farmer_id = add_farmer(
                        name=farmer_name.strip(),
                        phone=phone.strip(),
                        village=village.strip(),
                        province=province,
                    )

                    st.success(
                        f"Farmer added successfully. Farmer ID: {farmer_id}"
                    )

        st.divider()

        st.subheader("Registered Farmers")

        farmers = get_farmers()

        if farmers:

            for farmer in farmers:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [3, 2, 2]
                    )

                    with col1:

                        st.write(
                            f"**{farmer['name']}**"
                        )

                        st.caption(
                            f"Farmer ID: {farmer['id']}"
                        )

                    with col2:

                        st.write(
                            farmer["village"]
                            if farmer["village"]
                            else "Location not provided"
                        )

                        st.caption(
                            farmer["province"]
                            if farmer["province"]
                            else "Province not provided"
                        )

                    with col3:

                        st.write(
                            farmer["phone"]
                            if farmer["phone"]
                            else "No phone"
                        )

        else:

            st.info(
                "No farmers have been added yet."
            )

    # ========================================================
    # FARMS
    # ========================================================

    with tab2:

        st.subheader("Add Farm")

        farmers = get_farmers()

        if not farmers:

            st.warning(
                "Please add a farmer first before creating a farm."
            )

        else:

            farmer_options = {
                f"{farmer['name']} (ID: {farmer['id']})":
                farmer["id"]
                for farmer in farmers
            }

            with st.form("farm_form"):

                selected_farmer = st.selectbox(
                    "Farmer *",
                    list(farmer_options.keys()),
                )

                col1, col2 = st.columns(2)

                with col1:

                    farm_name = st.text_input(
                        "Farm Name *",
                        placeholder="e.g. Main Farm",
                    )

                    area_acres = st.number_input(
                        "Farm Area (acres)",
                        min_value=0.01,
                        value=1.0,
                        step=0.1,
                    )

                    irrigation_system = st.selectbox(
                        "Irrigation System",
                        [
                            "Canal",
                            "Tubewell",
                            "Drip",
                            "Sprinkler",
                            "Flood",
                            "Other",
                        ],
                    )

                    soil_type = st.selectbox(
                        "Soil Type",
                        [
                            "Not specified",
                            "Sandy",
                            "Sandy Loam",
                            "Loam",
                            "Clay Loam",
                            "Clay",
                            "Silty Loam",
                            "Other",
                        ],
                    )

                with col2:

                    latitude = st.number_input(
                        "Latitude",
                        min_value=-90.0,
                        max_value=90.0,
                        value=31.5204,
                        format="%.6f",
                    )

                    longitude = st.number_input(
                        "Longitude",
                        min_value=-180.0,
                        max_value=180.0,
                        value=74.3587,
                        format="%.6f",
                    )

                    st.caption(
                        "Enter the geographic coordinates of the farm."
                    )

                submitted = st.form_submit_button(
                    "Save Farm",
                    type="primary",
                    use_container_width=True,
                )

                if submitted:

                    if not farm_name.strip():

                        st.error(
                            "Farm name is required."
                        )

                    else:

                        farmer_id = farmer_options[
                            selected_farmer
                        ]

                        farm_id = add_farm(
                            farmer_id=farmer_id,
                            farm_name=farm_name.strip(),
                            area_acres=area_acres,
                            latitude=latitude,
                            longitude=longitude,
                            irrigation_system=irrigation_system,
                            soil_type=soil_type,
                        )

                        st.success(
                            f"Farm added successfully. Farm ID: {farm_id}"
                        )

        st.divider()

        st.subheader("Registered Farms")

        farms = get_farms()

        if farms:

            for farm in farms:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [3, 3, 2]
                    )

                    with col1:

                        st.write(
                            f"**{farm['farm_name']}**"
                        )

                        st.caption(
                            f"Farm ID: {farm['id']}"
                        )

                        st.write(
                            f"Farmer: {farm['farmer_name']}"
                        )

                    with col2:

                        st.write(
                            f"Area: {farm['area_acres']} acres"
                        )

                        st.write(
                            f"Location: "
                            f"{farm['latitude']:.6f}, "
                            f"{farm['longitude']:.6f}"
                        )

                    with col3:

                        st.write(
                            f"Irrigation: "
                            f"{farm['irrigation_system']}"
                        )

                        st.write(
                            f"Soil: "
                            f"{farm['soil_type']}"
                        )

        else:

            st.info(
                "No farms have been added yet."
            )

    # ========================================================
    # FIELDS
    # ========================================================

    with tab3:

        st.subheader("Add Field / Crop")

        farms = get_farms()

        if not farms:

            st.warning(
                "Please add a farm first before creating a field."
            )

        else:

            farm_options = {
                (
                    f"{farm['farm_name']} — "
                    f"{farm['farmer_name']} "
                    f"(ID: {farm['id']})"
                ):
                farm["id"]
                for farm in farms
            }

            with st.form("field_form"):

                selected_farm = st.selectbox(
                    "Farm *",
                    list(farm_options.keys()),
                )

                col1, col2 = st.columns(2)

                with col1:

                    field_name = st.text_input(
                        "Field Name *",
                        placeholder="e.g. Field 1",
                    )

                    crop = st.selectbox(
                        "Crop",
                        [
                            "Select crop",
                            "Wheat",
                            "Rice",
                            "Maize",
                            "Cotton",
                            "Sugarcane",
                            "Potato",
                            "Other",
                        ],
                    )

                    variety = st.text_input(
                        "Variety",
                        placeholder="Optional",
                    )

                    field_area = st.number_input(
                        "Field Area (acres)",
                        min_value=0.01,
                        value=1.0,
                        step=0.1,
                    )

                with col2:

                    sowing_date = st.date_input(
                        "Sowing Date",
                        value=date.today(),
                    )

                    crop_stage = st.selectbox(
                        "Crop Stage",
                        [
                            "Not specified",
                            "Germination",
                            "Vegetative",
                            "Tillering",
                            "Flowering",
                            "Grain Filling",
                            "Maturity",
                            "Harvest",
                        ],
                    )

                    st.caption(
                        "Crop-stage estimation will later be "
                        "connected to sowing date and crop-specific logic."
                    )

                submitted = st.form_submit_button(
                    "Save Field",
                    type="primary",
                    use_container_width=True,
                )

                if submitted:

                    if not field_name.strip():

                        st.error(
                            "Field name is required."
                        )

                    else:

                        farm_id = farm_options[
                            selected_farm
                        ]

                        field_id = add_field(
                            farm_id=farm_id,
                            field_name=field_name.strip(),
                            crop=(
                                ""
                                if crop == "Select crop"
                                else crop
                            ),
                            variety=variety.strip(),
                            sowing_date=str(
                                sowing_date
                            ),
                            crop_stage=crop_stage,
                            area_acres=field_area,
                        )

                        st.success(
                            f"Field added successfully. "
                            f"Field ID: {field_id}"
                        )

        st.divider()

        st.subheader("Registered Fields")

        fields = get_fields()

        if fields:

            for field in fields:

                with st.container(border=True):

                    col1, col2, col3 = st.columns(
                        [3, 3, 2]
                    )

                    with col1:

                        st.write(
                            f"**{field['field_name']}**"
                        )

                        st.caption(
                            f"Field ID: {field['id']}"
                        )

                        st.write(
                            f"Farm: {field['farm_name']}"
                        )

                        st.write(
                            f"Farmer: {field['farmer_name']}"
                        )

                    with col2:

                        st.write(
                            f"Crop: {field['crop'] or 'Not specified'}"
                        )

                        st.write(
                            f"Variety: "
                            f"{field['variety'] or 'Not specified'}"
                        )

                        st.write(
                            f"Area: {field['area_acres']} acres"
                        )

                    with col3:

                        st.write(
                            f"Stage: {field['crop_stage']}"
                        )

                        st.write(
                            f"Sowing: "
                            f"{field['sowing_date']}"
                        )

        else:

            st.info(
                "No fields have been added yet."
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

def show_gis_map():

    section_header(
        "🗺️ GIS & Farm Map",
        "View registered farms and their geographic locations.",
    )

    farms = get_farms()

    if not farms:

        st.info(
            "No farms are available yet. "
            "Go to Farmer & Farm and add a farm first."
        )

        return

    # ========================================================
    # FARM SELECTION
    # ========================================================

    farm_options = {
        (
            f"{farm['farm_name']} — "
            f"{farm['farmer_name']} "
            f"(ID: {farm['id']})"
        ):
        farm["id"]
        for farm in farms
    }

    selected_farm_name = st.selectbox(
        "Select Farm",
        list(farm_options.keys()),
    )

    selected_farm_id = farm_options[
        selected_farm_name
    ]

    selected_farm = None

    for farm in farms:

        if farm["id"] == selected_farm_id:

            selected_farm = farm

            break

    if selected_farm is None:

        st.error(
            "Selected farm could not be found."
        )

        return

    latitude = selected_farm["latitude"]
    longitude = selected_farm["longitude"]

    # ========================================================
    # FARM INFORMATION
    # ========================================================

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Farm",
            selected_farm["farm_name"],
        )

    with col2:

        st.metric(
            "Area",
            f"{selected_farm['area_acres']} acres",
        )

    with col3:

        st.metric(
            "Latitude",
            f"{latitude:.6f}",
        )

    with col4:

        st.metric(
            "Longitude",
            f"{longitude:.6f}",
        )

    # ========================================================
    # MAP
    # ========================================================

    st.subheader("Farm Location")

    farm_map = folium.Map(
        location=[
            latitude,
            longitude,
        ],
        zoom_start=13,
        control_scale=True,
    )

    folium.Marker(
        location=[
            latitude,
            longitude,
        ],
        tooltip=selected_farm["farm_name"],
        popup=(
            f"<b>{selected_farm['farm_name']}</b><br>"
            f"Farmer: {selected_farm['farmer_name']}<br>"
            f"Area: {selected_farm['area_acres']} acres<br>"
            f"Irrigation: {selected_farm['irrigation_system']}<br>"
            f"Soil: {selected_farm['soil_type']}"
        ),
        icon=folium.Icon(
            icon="leaf",
            prefix="fa",
        ),
    ).add_to(farm_map)

    st_folium(
        farm_map,
        width=None,
        height=500,
        returned_objects=[],
    )

    # ========================================================
    # LOCATION DETAILS
    # ========================================================

    st.divider()

    st.subheader("Farm Location Details")

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.write("**Farm Information**")

            st.write(
                f"Farm: {selected_farm['farm_name']}"
            )

            st.write(
                f"Farmer: {selected_farm['farmer_name']}"
            )

            st.write(
                f"Area: {selected_farm['area_acres']} acres"
            )

    with col2:

        with st.container(border=True):

            st.write("**Geographic Information**")

            st.write(
                f"Latitude: {latitude:.6f}"
            )

            st.write(
                f"Longitude: {longitude:.6f}"
            )

            st.write(
                "Coordinate source: Farmer-entered location"
            )

    # ========================================================
    # FIELDS AT THIS FARM
    # ========================================================

    fields = get_fields()

    farm_fields = [
        field
        for field in fields
        if field["farm_id"] == selected_farm_id
    ]

    st.divider()

    st.subheader("Fields at This Farm")

    if not farm_fields:

        st.info(
            "No fields have been registered for this farm yet."
        )

    else:

        for field in farm_fields:

            with st.container(border=True):

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.write(
                        f"**{field['field_name']}**"
                    )

                    st.caption(
                        f"Field ID: {field['id']}"
                    )

                with col2:

                    st.write(
                        f"Crop: "
                        f"{field['crop'] or 'Not specified'}"
                    )

                    st.write(
                        f"Area: "
                        f"{field['area_acres']} acres"
                    )

                with col3:

                    st.write(
                        f"Stage: "
                        f"{field['crop_stage']}"
                    )

                    st.write(
                        f"Sowing: "
                        f"{field['sowing_date']}"
                    )

# ============================================================
# PAGE ROUTER
# ============================================================

page = st.session_state.current_page


if page == "Dashboard":

    show_dashboard()

elif page == "Farmer & Farm":

    show_farmer_farm()

elif page == "GIS & Farm Map":

    show_gis_map()

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
