import folium
import streamlit as st

from streamlit_folium import st_folium

from services.gis_service import (
    detect_admin_location,
    create_analysis_geometry,
    debug_project_structure,
)

PAKISTAN_CENTER = [
    30.3753,
    69.3451,
]

def render_input_page():

    st.title("🌾 Farm Data Input")

    st.markdown(
        """
        Select the **exact farm location** using the map.
        The system will use the geographic coordinates as
        the primary location identifier.
        """
    )

    col1, col2 = st.columns(2)

    with col1:

        latitude = st.number_input(
            "Latitude",
            min_value=23.5,
            max_value=37.5,
            value=31.450000,
            format="%.6f",
        )

    with col2:

        longitude = st.number_input(
            "Longitude",
            min_value=60.5,
            max_value=77.5,
            value=73.350000,
            format="%.6f",
        )

    st.caption(
        "You can enter coordinates manually or click "
        "directly on the street map below."
    )

    # --------------------------------------------------
    # MAP
    # --------------------------------------------------

    map_object = folium.Map(
        location=[
            latitude,
            longitude,
        ],
        zoom_start=14,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    folium.Marker(
        [latitude, longitude],
        tooltip="Selected Farm",
        popup=(
            f"Latitude: {latitude:.6f}<br>"
            f"Longitude: {longitude:.6f}"
        ),
        icon=folium.Icon(
            color="green",
            icon="leaf",
        ),
    ).add_to(map_object)

    map_data = st_folium(
        map_object,
        width=1200,
        height=550,
        returned_objects=[
            "last_clicked"
        ],
    )

    # --------------------------------------------------
    # MAP CLICK
    # --------------------------------------------------

    if map_data and map_data.get(
        "last_clicked"
    ):

        latitude = round(
            map_data["last_clicked"]["lat"],
            6,
        )

        longitude = round(
            map_data["last_clicked"]["lng"],
            6,
        )

        st.rerun()

    # --------------------------------------------------
    # ADMINISTRATIVE LOCATION
    # --------------------------------------------------

    district, tehsil = (
        detect_admin_location(
            latitude,
            longitude,
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Latitude",
            f"{latitude:.6f}",
        )

    with col2:

        st.metric(
            "Longitude",
            f"{longitude:.6f}",
        )

    if district:

        st.success(
            f"Administrative location: "
            f"{district} → {tehsil}"
        )

    else:

        st.info(
            "The selected coordinate is outside "
            "the supplied tehsil boundary dataset."
        )

    # --------------------------------------------------
    # FARM INFORMATION
    # --------------------------------------------------

    st.subheader("🌱 Farm Information")

    col1, col2 = st.columns(2)

    with col1:

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
            "Farm Area (acres)",
            min_value=0.01,
            max_value=10000.0,
            value=5.0,
            step=0.5,
        )

    with col2:

        irrigation = st.selectbox(
            "Irrigation System",
            [
                "Flood",
                "Drip",
                "Sprinkler",
                "Canal",
                "Rainfed",
            ],
        )

        radius = st.number_input(
            "Satellite Analysis Radius (m)",
            min_value=10.0,
            max_value=1000.0,
            value=100.0,
            step=10.0,
        )

    st.info(
        "The analysis radius defines the area around "
        "the selected coordinate used for NDVI statistics. "
        "It is an analytical region of interest, not a "
        "replacement for a surveyed farm boundary."
    )

    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    if st.button(
        "💾 Save Farm Configuration",
        type="primary",
        use_container_width=True,
    ):

        st.session_state.farm_data = {
            "latitude": latitude,
            "longitude": longitude,
            "district": district,
            "tehsil": tehsil,
            "crop": crop,
            "area_acres": area,
            "irrigation_type": irrigation,
            "analysis_radius_m": radius,
        }

        st.session_state.analysis_results = None
        st.session_state.recommendations = None

        st.success(
            "Farm configuration saved successfully."
        )
