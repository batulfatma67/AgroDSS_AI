from __future__ import annotations

import folium
import streamlit as st
from streamlit_folium import st_folium

from services.gis_service import detect_admin_location


PAKISTAN_CENTER = (30.3753, 69.3451)


def _initialize_location_state() -> None:
    """Initialize persistent coordinate state for the input page."""

    if "farm_latitude" not in st.session_state:
        st.session_state["farm_latitude"] = 31.450000

    if "farm_longitude" not in st.session_state:
        st.session_state["farm_longitude"] = 73.350000


def render_input_page() -> None:
    """Render the farm location and farm-configuration input page."""

    _initialize_location_state()

    st.title("🌾 Farm Data Input")

    st.markdown(
        """
        Select the **exact farm location** using the interactive map or
        enter its geographic coordinates manually.

        The selected coordinates are used as the primary spatial reference
        for subsequent satellite and environmental analysis.
        """
    )

    # ------------------------------------------------------------------
    # COORDINATES
    # ------------------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input(
            "Latitude",
            min_value=23.5,
            max_value=37.5,
            value=float(st.session_state["farm_latitude"]),
            format="%.6f",
            key="latitude_input",
        )

    with col2:
        longitude = st.number_input(
            "Longitude",
            min_value=60.5,
            max_value=77.5,
            value=float(st.session_state["farm_longitude"]),
            format="%.6f",
            key="longitude_input",
        )

    st.caption(
        "Enter coordinates manually or click a location directly on "
        "the street map."
    )

    # ------------------------------------------------------------------
    # MAP
    # ------------------------------------------------------------------

    farm_map = folium.Map(
        location=[latitude, longitude],
        zoom_start=14,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    folium.Marker(
        location=[latitude, longitude],
        tooltip="Selected Farm Location",
        popup=(
            f"<b>Farm Location</b><br>"
            f"Latitude: {latitude:.6f}<br>"
            f"Longitude: {longitude:.6f}"
        ),
        icon=folium.Icon(
            color="green",
            icon="leaf",
        ),
    ).add_to(farm_map)

    map_data = st_folium(
        farm_map,
        width=1200,
        height=550,
        returned_objects=["last_clicked"],
        key="farm_location_map",
    )

    # ------------------------------------------------------------------
    # MAP CLICK HANDLING
    # ------------------------------------------------------------------

    last_clicked = (
        map_data.get("last_clicked")
        if map_data
        else None
    )

    if last_clicked:
        clicked_latitude = round(
            float(last_clicked["lat"]),
            6,
        )

        clicked_longitude = round(
            float(last_clicked["lng"]),
            6,
        )

        st.session_state["farm_latitude"] = clicked_latitude
        st.session_state["farm_longitude"] = clicked_longitude

        st.rerun()

    # ------------------------------------------------------------------
    # UPDATE SESSION STATE FROM MANUAL INPUT
    # ------------------------------------------------------------------

    st.session_state["farm_latitude"] = float(latitude)
    st.session_state["farm_longitude"] = float(longitude)

    # ------------------------------------------------------------------
    # ADMINISTRATIVE LOCATION
    # ------------------------------------------------------------------

    district, tehsil = detect_admin_location(
        latitude=float(latitude),
        longitude=float(longitude),
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

    if district and tehsil:
        st.success(
            f"Administrative location: "
            f"{district} → {tehsil}"
        )
    elif district:
        st.success(
            f"Administrative district: {district}"
        )
    else:
        st.info(
            "The selected coordinate is outside the supplied "
            "tehsil boundary dataset."
        )

    # ------------------------------------------------------------------
    # FARM INFORMATION
    # ------------------------------------------------------------------

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
            key="crop_input",
        )

        area = st.number_input(
            "Farm Area (acres)",
            min_value=0.01,
            max_value=10000.0,
            value=5.0,
            step=0.5,
            key="area_input",
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
            key="irrigation_input",
        )

        radius = st.number_input(
            "Satellite Analysis Radius (m)",
            min_value=10.0,
            max_value=1000.0,
            value=100.0,
            step=10.0,
            key="analysis_radius_input",
        )

    st.info(
        "The analysis radius defines the region around the selected "
        "coordinate used for satellite statistics. It represents an "
        "analytical region of interest and is not a substitute for a "
        "surveyed farm boundary."
    )

    # ------------------------------------------------------------------
    # SAVE FARM CONFIGURATION
    # ------------------------------------------------------------------

    if st.button(
        "💾 Save Farm Configuration",
        type="primary",
        use_container_width=True,
    ):
        st.session_state["farm_data"] = {
            "latitude": float(latitude),
            "longitude": float(longitude),
            "district": district,
            "tehsil": tehsil,
            "crop": crop,
            "area_acres": float(area),
            "irrigation_type": irrigation,
            "analysis_radius_m": float(radius),
        }

        # Reset downstream analysis because the farm configuration changed.
        st.session_state["analysis_results"] = None
        st.session_state["recommendations"] = None
        st.session_state["report_data"] = None

        st.success(
            "Farm configuration saved successfully."
        )
