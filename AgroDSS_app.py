import streamlit as st
from datetime import date

import folium
from streamlit_folium import st_folium

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from database import (
    add_farmer,
    update_farmer,
    delete_farmer,
    get_farmer,
    get_farmers,

    add_farm,
    update_farm,
    delete_farm,
    get_farm,
    get_farms,
    get_farms_by_farmer,

    add_field,
    update_field,
    delete_field,
    get_field,
    get_fields,
    get_fields_by_farm,

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
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.10);
    }

    h1 {
        color: #173b32;
        font-weight: 750;
    }

    h2 {
        color: #173b32;
        font-weight: 700;
    }

    h3 {
        color: #24564a;
        font-weight: 650;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 14px;
    }

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

    .stButton button {
        border-radius: 9px;
        font-weight: 600;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

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

if "edit_farmer_id" not in st.session_state:
    st.session_state.edit_farmer_id = None

if "edit_farm_id" not in st.session_state:
    st.session_state.edit_farm_id = None

if "edit_field_id" not in st.session_state:
    st.session_state.edit_field_id = None

if "location_result" not in st.session_state:
    st.session_state.location_result = None


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌾 AgriDSS AI")

    st.caption(
        "AI-Powered Agricultural Decision Support System"
    )

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

            st.session_state.edit_farmer_id = None
            st.session_state.edit_farm_id = None
            st.session_state.edit_field_id = None

            st.rerun()

    st.divider()

    st.subheader("System")

    st.success("Application Online")

    st.caption("AgriDSS AI • Development Version")


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def section_header(title, description=None):

    st.header(title)

    if description:
        st.caption(description)


def feature_card(
    icon,
    title,
    description,
    status="Coming Soon",
):

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
# GEOCODING
# ============================================================

@st.cache_resource
def get_geocoder():

    return Nominatim(
        user_agent="AgriDSS_AI_Farm_Location",
        timeout=10,
    )


def geocode_farm_location(
    province,
    district,
    tehsil,
    place,
):

    geocoder = get_geocoder()

    parts = [
        place.strip(),
        tehsil.strip(),
        district.strip(),
        province.strip(),
        "Pakistan",
    ]

    query = ", ".join(
        part
        for part in parts
        if part
    )

    try:

        location = geocoder.geocode(
            query,
            exactly_one=True,
            addressdetails=True,
            country_codes="pk",
        )

        if location is None:
            return None

        return {
            "latitude": float(location.latitude),
            "longitude": float(location.longitude),
            "display_name": location.address,
            "raw": location.raw,
        }

    except (
        GeocoderTimedOut,
        GeocoderServiceError,
        Exception,
    ):

        return None


# ============================================================
# LOCATION INPUT
# ============================================================

def location_selector(
    key_prefix,
    existing=None,
):

    existing = existing or {}

    province_options = [
        "Punjab",
        "Sindh",
        "Khyber Pakhtunkhwa",
        "Balochistan",
        "Gilgit-Baltistan",
        "Azad Jammu & Kashmir",
    ]

    existing_province = existing.get(
        "province",
        "",
    )

    if existing_province in province_options:
        province_index = province_options.index(
            existing_province
        )
    else:
        province_index = 0

    province = st.selectbox(
        "Province *",
        province_options,
        index=province_index,
        key=f"{key_prefix}_province",
    )

    district = st.text_input(
        "District *",
        value=existing.get("district", ""),
        placeholder="e.g. Faisalabad",
        key=f"{key_prefix}_district",
    )

    tehsil = st.text_input(
        "Tehsil *",
        value=existing.get("tehsil", ""),
        placeholder="e.g. Shahkot",
        key=f"{key_prefix}_tehsil",
    )

    place = st.text_input(
        "Place / Village / Locality *",
        value=existing.get("place_name", ""),
        placeholder="e.g. Chak 123",
        key=f"{key_prefix}_place",
    )

    if st.button(
        "📍 Find Location",
        key=f"{key_prefix}_find_location",
        use_container_width=True,
    ):

        if not district.strip():
            st.error("Please enter the district.")

        elif not tehsil.strip():
            st.error("Please enter the tehsil.")

        elif not place.strip():
            st.error(
                "Please enter the place, village or locality."
            )

        else:

            with st.spinner(
                "Finding geographic coordinates..."
            ):

                result = geocode_farm_location(
                    province,
                    district,
                    tehsil,
                    place,
                )

            if result:

                st.session_state.location_result = result

                st.success(
                    "Location found successfully."
                )

                st.write(
                    f"**Resolved location:** "
                    f"{result['display_name']}"
                )

            else:

                st.session_state.location_result = None

                st.error(
                    "The location could not be found. "
                    "Try a more specific place/village name."
                )

    result = st.session_state.location_result

    existing_lat = existing.get("latitude")
    existing_lon = existing.get("longitude")

    if result:

        latitude = result["latitude"]
        longitude = result["longitude"]

    else:

        latitude = existing_lat
        longitude = existing_lon

    if latitude is not None and longitude is not None:

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Latitude",
                f"{float(latitude):.6f}",
            )

        with col2:

            st.metric(
                "Longitude",
                f"{float(longitude):.6f}",
            )

        st.caption(
            "Coordinates will be stored with the farm."
        )

    return {
        "province": province,
        "district": district.strip(),
        "tehsil": tehsil.strip(),
        "place_name": place.strip(),
        "latitude": latitude,
        "longitude": longitude,
    }


# ============================================================
# DASHBOARD
# ============================================================

def show_dashboard():

    stats = get_dashboard_statistics()

    st.title("🌾 AgriDSS AI")

    st.subheader(
        "AI-Powered Agricultural Decision Support System"
    )

    st.write(
        "A unified platform for farm intelligence, "
        "satellite analysis, weather information, "
        "irrigation decision support, agricultural "
        "knowledge retrieval, and AI-assisted recommendations."
    )

    st.divider()

    st.subheader("System Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Farmers", stats["farmers"])

    with col2:
        st.metric("Farms", stats["farms"])

    with col3:
        st.metric("Fields", stats["fields"])

    with col4:
        st.metric("Active Crops", stats["crops"])

    st.divider()

    st.subheader("Farm Intelligence")

    col1, col2, col3 = st.columns(3)

    with col1:

        feature_card(
            "👨‍🌾",
            "Farmer & Farm",
            "Create farmer profiles, farms and fields.",
            "Development",
        )

    with col2:

        feature_card(
            "🛰️",
            "Satellite Intelligence",
            "Analyze vegetation using satellite imagery and NDVI.",
            "Development",
        )

    with col3:

        feature_card(
            "🌦️",
            "Weather Intelligence",
            "Use weather observations and forecasts.",
            "Development",
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        feature_card(
            "💧",
            "Water & Irrigation",
            "Calculate crop water and irrigation requirements.",
            "Development",
        )

    with col2:

        feature_card(
            "🤖",
            "AI Agronomist",
            "Provide grounded agricultural recommendations.",
            "Coming Soon",
        )

    with col3:

        feature_card(
            "📚",
            "Knowledge Base",
            "Retrieve agricultural information through RAG.",
            "Coming Soon",
        )

    st.divider()

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
            "🗺️ Farm Map",
            use_container_width=True,
        ):

            st.session_state.current_page = "GIS & Farm Map"

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
            "🤖 AI Agronomist",
            use_container_width=True,
        ):

            st.session_state.current_page = "AI Agronomist"

            st.rerun()


# ============================================================
# FARMER MANAGEMENT
# ============================================================

def show_farmers_tab():

    st.subheader("👨‍🌾 Farmers")

    edit_id = st.session_state.edit_farmer_id

    # ========================================================
    # EDIT FARMER
    # ========================================================

    if edit_id:

        farmer = get_farmer(edit_id)

        if farmer:

            st.subheader("✏️ Edit Farmer")

            with st.form(
                f"edit_farmer_{edit_id}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    name = st.text_input(
                        "Farmer Name *",
                        value=farmer["name"] or "",
                    )

                    phone = st.text_input(
                        "Phone Number",
                        value=farmer["phone"] or "",
                    )

                with col2:

                    village = st.text_input(
                        "Village / Area",
                        value=farmer["village"] or "",
                    )

                    provinces = [
                        "Punjab",
                        "Sindh",
                        "Khyber Pakhtunkhwa",
                        "Balochistan",
                        "Gilgit-Baltistan",
                        "Azad Jammu & Kashmir",
                    ]

                    current_province = (
                        farmer["province"]
                        if farmer["province"]
                        in provinces
                        else provinces[0]
                    )

                    province = st.selectbox(
                        "Province",
                        provinces,
                        index=provinces.index(
                            current_province
                        ),
                    )

                col_a, col_b = st.columns(2)

                with col_a:

                    save = st.form_submit_button(
                        "💾 Save Changes",
                        type="primary",
                        use_container_width=True,
                    )

                with col_b:

                    cancel = st.form_submit_button(
                        "Cancel",
                        use_container_width=True,
                    )

                if save:

                    if not name.strip():

                        st.error(
                            "Farmer name is required."
                        )

                    else:

                        update_farmer(
                            farmer_id=edit_id,
                            name=name.strip(),
                            phone=phone.strip(),
                            village=village.strip(),
                            province=province,
                        )

                        st.session_state.edit_farmer_id = None

                        st.success(
                            "Farmer updated successfully."
                        )

                        st.rerun()

                if cancel:

                    st.session_state.edit_farmer_id = None

                    st.rerun()

    # ========================================================
    # ADD FARMER
    # ========================================================

    with st.expander(
        "➕ Add New Farmer",
        expanded=not bool(edit_id),
    ):

        with st.form("add_farmer_form"):

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

                    farmer_id = add_farmer(
                        name=farmer_name.strip(),
                        phone=phone.strip(),
                        village=village.strip(),
                        province=province,
                    )

                    st.success(
                        f"Farmer added successfully. "
                        f"Farmer ID: {farmer_id}"
                    )

                    st.rerun()

    st.divider()

    # ========================================================
    # FARMER LIST
    # ========================================================

    farmers = get_farmers()

    if not farmers:

        st.info(
            "No farmers have been added yet."
        )

        return

    for farmer in farmers:

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(
                [3, 2, 2, 2]
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
                    or "Location not provided"
                )

                st.caption(
                    farmer["province"]
                    or "Province not provided"
                )

            with col3:

                st.write(
                    farmer["phone"]
                    or "No phone"
                )

            with col4:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_farmer_{farmer['id']}",
                    use_container_width=True,
                ):

                    st.session_state.edit_farmer_id = farmer["id"]

                    st.rerun()

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_farmer_{farmer['id']}",
                    use_container_width=True,
                ):

                    st.session_state[
                        f"confirm_delete_farmer_{farmer['id']}"
                    ] = True

                    st.rerun()

            if st.session_state.get(
                f"confirm_delete_farmer_{farmer['id']}",
                False,
            ):

                farms = get_farms_by_farmer(
                    farmer["id"]
                )

                st.warning(
                    f"This farmer has {len(farms)} "
                    f"registered farm(s). Deleting the "
                    f"farmer will also delete the associated "
                    f"farms and fields."
                )

                confirm_col1, confirm_col2 = st.columns(2)

                with confirm_col1:

                    if st.button(
                        "Yes, Delete",
                        key=f"confirm_yes_farmer_{farmer['id']}",
                        type="primary",
                        use_container_width=True,
                    ):

                        delete_farmer(
                            farmer["id"]
                        )

                        st.session_state[
                            f"confirm_delete_farmer_{farmer['id']}"
                        ] = False

                        st.success(
                            "Farmer deleted successfully."
                        )

                        st.rerun()

                with confirm_col2:

                    if st.button(
                        "Cancel",
                        key=f"confirm_no_farmer_{farmer['id']}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            f"confirm_delete_farmer_{farmer['id']}"
                        ] = False

                        st.rerun()


# ============================================================
# FARM MANAGEMENT
# ============================================================

def show_farms_tab():

    st.subheader("🚜 Farms")

    farmers = get_farmers()

    edit_id = st.session_state.edit_farm_id

    # ========================================================
    # EDIT FARM
    # ========================================================

    if edit_id:

        farm = get_farm(edit_id)

        if farm:

            st.subheader("✏️ Edit Farm")

            with st.form(
                f"edit_farm_form_{edit_id}"
            ):

                farmer_options = {
                    f"{f['name']} (ID: {f['id']})":
                    f["id"]
                    for f in farmers
                }

                option_list = list(
                    farmer_options.keys()
                )

                current_farmer_label = next(
                    (
                        label
                        for label, fid
                        in farmer_options.items()
                        if fid == farm["farmer_id"]
                    ),
                    option_list[0],
                )

                selected_farmer = st.selectbox(
                    "Farmer *",
                    option_list,
                    index=option_list.index(
                        current_farmer_label
                    ),
                )

                col1, col2 = st.columns(2)

                with col1:

                    farm_name = st.text_input(
                        "Farm Name *",
                        value=farm["farm_name"] or "",
                    )

                    area_acres = st.number_input(
                        "Farm Area (acres)",
                        min_value=0.01,
                        value=float(
                            farm["area_acres"] or 1.0
                        ),
                        step=0.1,
                    )

                with col2:

                    irrigation_options = [
                        "Canal",
                        "Tubewell",
                        "Drip",
                        "Sprinkler",
                        "Flood",
                        "Other",
                    ]

                    irrigation = (
                        farm["irrigation_system"]
                        if farm["irrigation_system"]
                        in irrigation_options
                        else "Other"
                    )

                    irrigation_system = st.selectbox(
                        "Irrigation System",
                        irrigation_options,
                        index=irrigation_options.index(
                            irrigation
                        ),
                    )

                    soil_options = [
                        "Not specified",
                        "Sandy",
                        "Sandy Loam",
                        "Loam",
                        "Clay Loam",
                        "Clay",
                        "Silty Loam",
                        "Other",
                    ]

                    soil = (
                        farm["soil_type"]
                        if farm["soil_type"]
                        in soil_options
                        else "Other"
                    )

                    soil_type = st.selectbox(
                        "Soil Type",
                        soil_options,
                        index=soil_options.index(
                            soil
                        ),
                    )

                st.markdown("### 📍 Farm Location")

                location = location_selector(
                    "edit_farm_location",
                    farm,
                )

                lat = location["latitude"]
                lon = location["longitude"]

                if lat is None or lon is None:

                    st.warning(
                        "Please find a valid farm location "
                        "before saving."
                    )

                col1, col2 = st.columns(2)

                with col1:

                    save = st.form_submit_button(
                        "💾 Save Changes",
                        type="primary",
                        use_container_width=True,
                    )

                with col2:

                    cancel = st.form_submit_button(
                        "Cancel",
                        use_container_width=True,
                    )

                if save:

                    if not farm_name.strip():

                        st.error(
                            "Farm name is required."
                        )

                    elif lat is None or lon is None:

                        st.error(
                            "Farm coordinates are required."
                        )

                    else:

                        farmer_id = farmer_options[
                            selected_farmer
                        ]

                        update_farm(
                            farm_id=edit_id,
                            farmer_id=farmer_id,
                            farm_name=farm_name.strip(),
                            area_acres=area_acres,
                            latitude=lat,
                            longitude=lon,
                            irrigation_system=irrigation_system,
                            soil_type=soil_type,
                            province=location["province"],
                            district=location["district"],
                            tehsil=location["tehsil"],
                            place_name=location["place_name"],
                        )

                        st.session_state.edit_farm_id = None

                        st.session_state.location_result = None

                        st.success(
                            "Farm updated successfully."
                        )

                        st.rerun()

                if cancel:

                    st.session_state.edit_farm_id = None

                    st.session_state.location_result = None

                    st.rerun()

    # ========================================================
    # ADD FARM
    # ========================================================

    if not farmers:

        st.warning(
            "Please add a farmer first before creating a farm."
        )

    else:

        with st.expander(
            "➕ Add New Farm",
            expanded=not bool(edit_id),
        ):

            farmer_options = {
                f"{farmer['name']} (ID: {farmer['id']})":
                farmer["id"]
                for farmer in farmers
            }

            with st.form("add_farm_form"):

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

                    st.markdown("### 📍 Farm Location")

                    st.caption(
                        "Enter the administrative location first. "
                        "AgriDSS will then find the coordinates."
                    )

                    province = st.selectbox(
                        "Province *",
                        [
                            "Punjab",
                            "Sindh",
                            "Khyber Pakhtunkhwa",
                            "Balochistan",
                            "Gilgit-Baltistan",
                            "Azad Jammu & Kashmir",
                        ],
                        key="new_farm_province",
                    )

                    district = st.text_input(
                        "District *",
                        placeholder="e.g. Faisalabad",
                        key="new_farm_district",
                    )

                    tehsil = st.text_input(
                        "Tehsil *",
                        placeholder="e.g. Shahkot",
                        key="new_farm_tehsil",
                    )

                    place = st.text_input(
                        "Place / Village / Locality *",
                        placeholder="e.g. Chak 123",
                        key="new_farm_place",
                    )

                    find_location = st.form_submit_button(
                        "📍 Find Location",
                        use_container_width=True,
                    )

                    if find_location:

                        if (
                            not district.strip()
                            or not tehsil.strip()
                            or not place.strip()
                        ):

                            st.error(
                                "Please enter district, tehsil "
                                "and place."
                            )

                        else:

                            with st.spinner(
                                "Finding coordinates..."
                            ):

                                result = geocode_farm_location(
                                    province,
                                    district,
                                    tehsil,
                                    place,
                                )

                            if result:

                                st.session_state.location_result = result

                                st.success(
                                    "Location found."
                                )

                                st.write(
                                    result["display_name"]
                                )

                            else:

                                st.session_state.location_result = None

                                st.error(
                                    "Location not found. "
                                    "Try a more specific place name."
                                )

                    result = st.session_state.location_result

                    if result:

                        st.metric(
                            "Latitude",
                            f"{result['latitude']:.6f}",
                        )

                        st.metric(
                            "Longitude",
                            f"{result['longitude']:.6f}",
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

                    elif not st.session_state.location_result:

                        st.error(
                            "Please click 'Find Location' "
                            "before saving the farm."
                        )

                    else:

                        result = st.session_state.location_result

                        farmer_id = farmer_options[
                            selected_farmer
                        ]

                        farm_id = add_farm(
                            farmer_id=farmer_id,
                            farm_name=farm_name.strip(),
                            area_acres=area_acres,

                            latitude=result["latitude"],
                            longitude=result["longitude"],

                            irrigation_system=irrigation_system,
                            soil_type=soil_type,

                            province=province,
                            district=district.strip(),
                            tehsil=tehsil.strip(),
                            place_name=place.strip(),
                        )

                        st.session_state.location_result = None

                        st.success(
                            f"Farm added successfully. "
                            f"Farm ID: {farm_id}"
                        )

                        st.rerun()

    st.divider()

    # ========================================================
    # FARM LIST
    # ========================================================

    farms = get_farms()

    if not farms:

        st.info(
            "No farms have been added yet."
        )

        return

    for farm in farms:

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(
                [3, 3, 2, 2]
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
                    f"📍 {farm['place_name'] or 'Location not specified'}"
                )

                st.caption(
                    f"{farm['tehsil'] or ''}, "
                    f"{farm['district'] or ''}, "
                    f"{farm['province'] or ''}"
                )

                if (
                    farm["latitude"] is not None
                    and farm["longitude"] is not None
                ):

                    st.caption(
                        f"{farm['latitude']:.6f}, "
                        f"{farm['longitude']:.6f}"
                    )

            with col3:

                st.write(
                    f"Area: {farm['area_acres']} acres"
                )

                st.write(
                    f"Irrigation: "
                    f"{farm['irrigation_system']}"
                )

                st.write(
                    f"Soil: {farm['soil_type']}"
                )

            with col4:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_farm_{farm['id']}",
                    use_container_width=True,
                ):

                    st.session_state.edit_farm_id = farm["id"]

                    st.session_state.location_result = None

                    st.rerun()

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_farm_{farm['id']}",
                    use_container_width=True,
                ):

                    st.session_state[
                        f"confirm_delete_farm_{farm['id']}"
                    ] = True

                    st.rerun()

            if st.session_state.get(
                f"confirm_delete_farm_{farm['id']}",
                False,
            ):

                fields = get_fields_by_farm(
                    farm["id"]
                )

                st.warning(
                    f"This farm has {len(fields)} "
                    f"registered field(s). "
                    f"Deleting the farm will also delete "
                    f"those fields."
                )

                c1, c2 = st.columns(2)

                with c1:

                    if st.button(
                        "Yes, Delete",
                        key=f"confirm_yes_farm_{farm['id']}",
                        type="primary",
                        use_container_width=True,
                    ):

                        delete_farm(
                            farm["id"]
                        )

                        st.success(
                            "Farm deleted successfully."
                        )

                        st.rerun()

                with c2:

                    if st.button(
                        "Cancel",
                        key=f"confirm_no_farm_{farm['id']}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            f"confirm_delete_farm_{farm['id']}"
                        ] = False

                        st.rerun()


# ============================================================
# FIELD MANAGEMENT
# ============================================================

def show_fields_tab():

    st.subheader("🌱 Fields")

    farms = get_farms()

    edit_id = st.session_state.edit_field_id

    # ========================================================
    # EDIT FIELD
    # ========================================================

    if edit_id:

        field = get_field(edit_id)

        if field:

            st.subheader("✏️ Edit Field")

            with st.form(
                f"edit_field_{edit_id}"
            ):

                farm_options = {
                    (
                        f"{farm['farm_name']} — "
                        f"{farm['farmer_name']} "
                        f"(ID: {farm['id']})"
                    ):
                    farm["id"]
                    for farm in farms
                }

                option_list = list(
                    farm_options.keys()
                )

                current_farm_label = next(
                    (
                        label
                        for label, fid
                        in farm_options.items()
                        if fid == field["farm_id"]
                    ),
                    option_list[0],
                )

                selected_farm = st.selectbox(
                    "Farm *",
                    option_list,
                    index=option_list.index(
                        current_farm_label
                    ),
                )

                col1, col2 = st.columns(2)

                with col1:

                    field_name = st.text_input(
                        "Field Name *",
                        value=field["field_name"] or "",
                    )

                    crop_options = [
                        "Select crop",
                        "Wheat",
                        "Rice",
                        "Maize",
                        "Cotton",
                        "Sugarcane",
                        "Potato",
                        "Other",
                    ]

                    current_crop = (
                        field["crop"]
                        if field["crop"]
                        in crop_options
                        else "Other"
                    )

                    crop = st.selectbox(
                        "Crop",
                        crop_options,
                        index=crop_options.index(
                            current_crop
                        ),
                    )

                    variety = st.text_input(
                        "Variety",
                        value=field["variety"] or "",
                    )

                    field_area = st.number_input(
                        "Field Area (acres)",
                        min_value=0.01,
                        value=float(
                            field["area_acres"] or 1.0
                        ),
                        step=0.1,
                    )

                with col2:

                    try:

                        existing_date = date.fromisoformat(
                            field["sowing_date"]
                        )

                    except Exception:

                        existing_date = date.today()

                    sowing_date = st.date_input(
                        "Sowing Date",
                        value=existing_date,
                    )

                    stage_options = [
                        "Not specified",
                        "Germination",
                        "Vegetative",
                        "Tillering",
                        "Flowering",
                        "Grain Filling",
                        "Maturity",
                        "Harvest",
                    ]

                    current_stage = (
                        field["crop_stage"]
                        if field["crop_stage"]
                        in stage_options
                        else "Not specified"
                    )

                    crop_stage = st.selectbox(
                        "Crop Stage",
                        stage_options,
                        index=stage_options.index(
                            current_stage
                        ),
                    )

                c1, c2 = st.columns(2)

                with c1:

                    save = st.form_submit_button(
                        "💾 Save Changes",
                        type="primary",
                        use_container_width=True,
                    )

                with c2:

                    cancel = st.form_submit_button(
                        "Cancel",
                        use_container_width=True,
                    )

                if save:

                    if not field_name.strip():

                        st.error(
                            "Field name is required."
                        )

                    else:

                        farm_id = farm_options[
                            selected_farm
                        ]

                        update_field(
                            field_id=edit_id,
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

                        st.session_state.edit_field_id = None

                        st.success(
                            "Field updated successfully."
                        )

                        st.rerun()

                if cancel:

                    st.session_state.edit_field_id = None

                    st.rerun()

    # ========================================================
    # ADD FIELD
    # ========================================================

    if not farms:

        st.warning(
            "Please add a farm first before creating a field."
        )

    else:

        with st.expander(
            "➕ Add New Field",
            expanded=not bool(edit_id),
        ):

            farm_options = {
                (
                    f"{farm['farm_name']} — "
                    f"{farm['farmer_name']} "
                    f"(ID: {farm['id']})"
                ):
                farm["id"]
                for farm in farms
            }

            with st.form("add_field_form"):

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

                        st.rerun()

    st.divider()

    # ========================================================
    # FIELD LIST
    # ========================================================

    fields = get_fields()

    if not fields:

        st.info(
            "No fields have been added yet."
        )

        return

    for field in fields:

        with st.container(border=True):

            col1, col2, col3, col4 = st.columns(
                [3, 3, 2, 2]
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
                    f"Crop: "
                    f"{field['crop'] or 'Not specified'}"
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
                    f"Sowing: {field['sowing_date']}"
                )

            with col4:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_field_{field['id']}",
                    use_container_width=True,
                ):

                    st.session_state.edit_field_id = field["id"]

                    st.rerun()

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_field_{field['id']}",
                    use_container_width=True,
                ):

                    st.session_state[
                        f"confirm_delete_field_{field['id']}"
                    ] = True

                    st.rerun()

            if st.session_state.get(
                f"confirm_delete_field_{field['id']}",
                False,
            ):

                st.warning(
                    "This field will be permanently deleted."
                )

                c1, c2 = st.columns(2)

                with c1:

                    if st.button(
                        "Yes, Delete",
                        key=f"confirm_yes_field_{field['id']}",
                        type="primary",
                        use_container_width=True,
                    ):

                        delete_field(
                            field["id"]
                        )

                        st.success(
                            "Field deleted successfully."
                        )

                        st.rerun()

                with c2:

                    if st.button(
                        "Cancel",
                        key=f"confirm_no_field_{field['id']}",
                        use_container_width=True,
                    ):

                        st.session_state[
                            f"confirm_delete_field_{field['id']}"
                        ] = False

                        st.rerun()


# ============================================================
# FARMER & FARM PAGE
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

    with tab1:
        show_farmers_tab()

    with tab2:
        show_farms_tab()

    with tab3:
        show_fields_tab()


# ============================================================
# GIS MAP
# ============================================================

def show_gis_map():
    st.markdown("## 🗺️ GIS & Farm Map")
    st.caption("Explore registered farms and fields using satellite, street, and terrain basemaps.")

    farms = get_farms()

    if not farms:
        st.info("No farms have been registered yet.")
        return

    # ---------------------------------------------------------
    # Find valid farm coordinates
    # ---------------------------------------------------------
    valid_farms = []

    for farm in farms:
        try:
            lat = float(farm["latitude"])
            lon = float(farm["longitude"])

            if -90 <= lat <= 90 and -180 <= lon <= 180:
                valid_farms.append((farm, lat, lon))
        except (TypeError, ValueError):
            continue

    if not valid_farms:
        st.warning(
            "No farms have valid coordinates yet. "
            "Add latitude and longitude to a farm first."
        )
        return

    # ---------------------------------------------------------
    # Map controls
    # ---------------------------------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Registered Farms", len(farms))

    with col2:
        st.metric("Mapped Farms", len(valid_farms))

    with col3:
        st.metric("Map Layers", "3")

    st.markdown("---")

    # ---------------------------------------------------------
    # Calculate map center
    # ---------------------------------------------------------
    center_lat = sum(item[1] for item in valid_farms) / len(valid_farms)
    center_lon = sum(item[2] for item in valid_farms) / len(valid_farms)

    # ---------------------------------------------------------
    # Create base map
    # ---------------------------------------------------------
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=12,
        control_scale=True,
        zoom_control=True,
        tiles=None
    )

    # ---------------------------------------------------------
    # 1. OpenStreetMap
    # ---------------------------------------------------------
    folium.TileLayer(
        tiles="OpenStreetMap",
        name="🗺️ Street Map",
        overlay=False,
        control=True,
        show=False
    ).add_to(m)

    # ---------------------------------------------------------
    # 2. Esri World Imagery
    # ---------------------------------------------------------
    folium.TileLayer(
        tiles=(
            "https://server.arcgisonline.com/ArcGIS/rest/services/"
            "World_Imagery/MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Esri World Imagery",
        name="🛰️ Satellite",
        overlay=False,
        control=True,
        show=True
    ).add_to(m)

    # ---------------------------------------------------------
    # 3. OpenTopoMap
    # ---------------------------------------------------------
    folium.TileLayer(
        tiles="https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
        attr="OpenTopoMap",
        name="⛰️ Terrain",
        overlay=False,
        control=True,
        show=False
    ).add_to(m)

    # ---------------------------------------------------------
    # Farm marker layer
    # ---------------------------------------------------------
    farm_layer = folium.FeatureGroup(
        name="🌾 Farms",
        show=True
    )

    # ---------------------------------------------------------
    # Field marker layer
    # ---------------------------------------------------------
    field_layer = folium.FeatureGroup(
        name="🌱 Fields",
        show=True
    )

    # ---------------------------------------------------------
    # Add farms
    # ---------------------------------------------------------
    for farm, lat, lon in valid_farms:

        farmer_name = farm["farmer_name"] if "farmer_name" in farm.keys() else "Unknown"

        farm_name = farm["farm_name"]

        area = farm["area_acres"]

        irrigation = farm["irrigation_system"]

        soil = farm["soil_type"]

        popup_html = f"""
        <div style="width:260px;">
            <h4 style="margin-bottom:8px;">
                🌾 {farm_name}
            </h4>

            <b>Farmer:</b> {farmer_name}<br>
            <b>Area:</b> {area} acres<br>
            <b>Irrigation:</b> {irrigation}<br>
            <b>Soil:</b> {soil}<br>
            <b>Latitude:</b> {lat:.6f}<br>
            <b>Longitude:</b> {lon:.6f}
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            tooltip=f"🌾 {farm_name}",
            popup=folium.Popup(
                popup_html,
                max_width=320
            ),
            icon=folium.Icon(
                icon="home",
                prefix="fa"
            )
        ).add_to(farm_layer)

        # -----------------------------------------------------
        # Add fields belonging to this farm
        # -----------------------------------------------------
        try:
            fields = get_fields_by_farm(farm["id"])
        except Exception:
            fields = []

        for field in fields:

            # Fields may not have their own coordinates in the
            # current database, so display them around the farm
            # only if coordinates exist.
            try:
                field_lat = float(field["latitude"])
                field_lon = float(field["longitude"])
            except (KeyError, TypeError, ValueError):
                continue

            field_popup = f"""
            <div style="width:240px;">
                <h4>🌱 {field["field_name"]}</h4>
                <b>Crop:</b> {field["crop"]}<br>
                <b>Variety:</b> {field["variety"]}<br>
                <b>Area:</b> {field["area_acres"]} acres<br>
                <b>Crop Stage:</b> {field["crop_stage"]}
            </div>
            """

            folium.CircleMarker(
                location=[field_lat, field_lon],
                radius=7,
                popup=folium.Popup(
                    field_popup,
                    max_width=300
                ),
                tooltip=f"🌱 {field['field_name']}"
            ).add_to(field_layer)

    farm_layer.add_to(m)
    field_layer.add_to(m)

    # ---------------------------------------------------------
    # Layer switcher
    # ---------------------------------------------------------
    folium.LayerControl(
        position="topright",
        collapsed=False
    ).add_to(m)

    # ---------------------------------------------------------
    # Display map
    # ---------------------------------------------------------
    st.markdown("### 📍 Farm Locations")

    st_folium(
        m,
        width=None,
        height=650,
        returned_objects=[]
    )


# ============================================================
# SATELLITE
# ============================================================

def show_satellite():

    section_header(
        "🛰️ Satellite Intelligence",
        "Satellite-based agricultural monitoring and vegetation intelligence.",
    )

    st.info(
        "Your existing Sentinel-2 / NDVI functionality "
        "will be integrated here."
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
                "Analysis Date"
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


# ============================================================
# WEATHER
# ============================================================

def show_weather():

    section_header(
        "🌦️ Weather Intelligence",
        "Weather observations and forecasts for agricultural decision support.",
    )

    st.info(
        "The existing Open-Meteo service can be connected here."
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Temperature", "— °C")

    with col2:
        st.metric("Rainfall", "— mm")

    with col3:
        st.metric("Humidity", "— %")

    with col4:
        st.metric("Wind", "— km/h")

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
                "Weather forecast data will appear here."
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
        "Numerical calculations are kept separate from "
        "the AI reasoning layer."
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
                net_irrigation
                / (efficiency / 100)
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


# ============================================================
# AI AGRONOMIST
# ============================================================

def show_ai_agronomist():

    section_header(
        "🤖 AI Agronomist",
        "AI-assisted agricultural reasoning and decision support.",
    )

    st.info(
        "RAG and agent integration will be added later."
    )

    with st.container(border=True):

        st.subheader(
            "Ask the AI Agronomist"
        )

        question = st.text_area(
            "Agricultural Question",
            placeholder=(
                "Example: My wheat field has declining NDVI "
                "and the weather has been unusually dry. "
                "What should I check?"
            ),
            height=150,
        )

        if st.button(
            "Ask AI Agronomist",
            type="primary",
        ):

            if question.strip():

                st.warning(
                    "The AI model is not connected yet."
                )

            else:

                st.warning(
                    "Please enter an agricultural question."
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
        "This section will become the RAG knowledge layer."
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

            st.write(
                "1. Upload agricultural documents"
            )

            st.write(
                "2. Extract document text"
            )

            st.write(
                "3. Clean and chunk content"
            )

            st.write(
                "4. Generate embeddings"
            )

            st.write(
                "5. Store vectors"
            )

            st.write(
                "6. Retrieve relevant evidence"
            )

            st.write(
                "7. Generate grounded response"
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
        "Your existing ReportLab functionality "
        "will be integrated here."
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
