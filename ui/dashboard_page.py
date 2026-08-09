from datetime import date, timedelta

import folium
import streamlit as st

from streamlit_folium import st_folium

from services.gis_service import create_analysis_geometry
from services.weather_service import (
    fetch_weather,
    parse_weather_response,
)
from services.ndvi_service import (
    get_ndvi_analysis,
    get_ndvi_tile_url,
)
from core.analysis import (
    calculate_risk,
    classify_ndvi,
)


def render_dashboard_page():

    st.title("📊 Agricultural Intelligence Dashboard")

    farm = st.session_state.get(
        "farm_data"
    )

    if not farm:

        st.warning(
            "Please configure the farm location "
            "from the Data Input page first."
        )

        return

    latitude = farm["latitude"]
    longitude = farm["longitude"]
    radius = farm["analysis_radius_m"]

    # --------------------------------------------------
    # ANALYSIS PERIOD
    # --------------------------------------------------

    default_end = date.today()
    default_start = (
        default_end - timedelta(days=60)
    )

    col1, col2 = st.columns(2)

    with col1:

        start_date = st.date_input(
            "Satellite start date",
            value=default_start,
        )

    with col2:

        end_date = st.date_input(
            "Satellite end date",
            value=default_end,
        )

    if start_date >= end_date:

        st.error(
            "Start date must be earlier than end date."
        )

        return

    # --------------------------------------------------
    # RUN ANALYSIS
    # --------------------------------------------------

    if st.button(
        "🚀 Run Field Analysis",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "Collecting weather and satellite data..."
        ):

            try:

                geometry = create_analysis_geometry(
                    latitude,
                    longitude,
                    radius,
                )

                weather_raw = fetch_weather(
                    latitude,
                    longitude,
                )

                weather = parse_weather_response(
                    weather_raw
                )

                ndvi = get_ndvi_analysis(
                    geometry,
                    start_date,
                    end_date,
                )

                risk = calculate_risk(
                    ndvi["mean_ndvi"],
                    weather["temperature_c"],
                    weather["humidity_percent"],
                    weather["rainfall_today_mm"],
                )

                st.session_state.analysis_results = {
                    "farm": farm,
                    "weather": weather,
                    "ndvi": ndvi,
                    "risk": risk,
                    "analysis_start": start_date,
                    "analysis_end": end_date,
                }

                st.success(
                    "Field analysis completed successfully."
                )

            except Exception as exc:

                st.error(
                    f"Analysis failed: {exc}"
                )

                return

    results = st.session_state.get(
        "analysis_results"
    )

    if not results:
        return

    weather = results["weather"]
    ndvi = results["ndvi"]
    risk = results["risk"]

    # --------------------------------------------------
    # FARM INFORMATION
    # --------------------------------------------------

    st.subheader("📍 Farm Information")

    st.write(
        f"**District:** "
        f"{farm.get('district') or 'Not identified'}"
    )

    st.write(
        f"**Tehsil:** "
        f"{farm.get('tehsil') or 'Not identified'}"
    )

    st.write(
        f"**Coordinates:** "
        f"{latitude:.6f}, {longitude:.6f}"
    )

    # --------------------------------------------------
    # METRICS
    # --------------------------------------------------

    ndvi_value = ndvi["mean_ndvi"]

    if ndvi_value is None:
        ndvi_display = "N/A"
    else:
        ndvi_display = f"{ndvi_value:.3f}"

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "🌿 Mean NDVI",
        ndvi_display,
    )

    c2.metric(
        "🌡 Temperature",
        f"{weather['temperature_c']:.1f} °C",
    )

    c3.metric(
        "💧 Humidity",
        f"{weather['humidity_percent']:.0f} %",
    )

    c4.metric(
        "🌧 Rainfall Today",
        f"{weather['rainfall_today_mm']:.1f} mm",
    )

    # --------------------------------------------------
    # RISK
    # --------------------------------------------------

    classification = classify_ndvi(
        ndvi_value
    )

    st.subheader("🧠 Field Condition")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Vegetation Class",
            classification["class"],
        )

    with col2:

        st.metric(
            "Risk Category",
            risk["category"],
            f"{risk['score']}/100",
        )

    # --------------------------------------------------
    # MAP
    # --------------------------------------------------

    st.subheader("🗺 Field Location & NDVI")

    field_map = folium.Map(
        location=[
            latitude,
            longitude,
        ],
        zoom_start=15,
        tiles="OpenStreetMap",
        control_scale=True,
    )

    folium.Marker(
        [latitude, longitude],
        tooltip="Farm Coordinate",
        popup=(
            f"Latitude: {latitude:.6f}<br>"
            f"Longitude: {longitude:.6f}"
        ),
        icon=folium.Icon(
            color="green",
            icon="leaf",
        ),
    ).add_to(field_map)

    folium.Circle(
        [latitude, longitude],
        radius=radius,
        color="blue",
        fill=True,
        fill_opacity=0.08,
        tooltip=(
            f"NDVI analysis radius: "
            f"{radius:.0f} m"
        ),
    ).add_to(field_map)

    try:

        ndvi_url = get_ndvi_tile_url(
            ndvi["image"]
        )

        folium.TileLayer(
            tiles=ndvi_url,
            attr=(
                "Sentinel-2 / Copernicus / "
                "Google Earth Engine"
            ),
            name="NDVI",
            overlay=True,
        ).add_to(field_map)

    except Exception as exc:

        st.warning(
            f"NDVI map layer unavailable: {exc}"
        )

    folium.LayerControl().add_to(
        field_map
    )

    st_folium(
        field_map,
        width=1200,
        height=650,
    )

    # --------------------------------------------------
    # SATELLITE STATISTICS
    # --------------------------------------------------

    st.subheader(
        "🛰 Satellite Vegetation Statistics"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Mean NDVI",
        (
            f"{ndvi['mean_ndvi']:.3f}"
            if ndvi["mean_ndvi"] is not None
            else "N/A"
        ),
    )

    c2.metric(
        "Minimum NDVI",
        (
            f"{ndvi['minimum_ndvi']:.3f}"
            if ndvi["minimum_ndvi"] is not None
            else "N/A"
        ),
    )

    c3.metric(
        "Maximum NDVI",
        (
            f"{ndvi['maximum_ndvi']:.3f}"
            if ndvi["maximum_ndvi"] is not None
            else "N/A"
        ),
    )

    st.caption(
        f"Sentinel-2 observations used: "
        f"{ndvi['image_count']} | "
        f"{ndvi['start_date']} → "
        f"{ndvi['end_date']}"
    )

    # --------------------------------------------------
    # WEATHER
    # --------------------------------------------------

    st.subheader("🌦 Weather Outlook")

    daily = weather["daily"]

    weather_rows = []

    for i, day in enumerate(
        daily["time"]
    ):

        weather_rows.append(
            {
                "Date": day,
                "Min Temperature (°C)": daily[
                    "temperature_2m_min"
                ][i],
                "Max Temperature (°C)": daily[
                    "temperature_2m_max"
                ][i],
                "Rainfall (mm)": daily[
                    "precipitation_sum"
                ][i],
            }
        )

    st.dataframe(
        weather_rows,
        use_container_width=True,
        hide_index=True,
    )
