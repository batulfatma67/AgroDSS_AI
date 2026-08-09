import streamlit as st

from core.recommendations import (
    generate_recommendations,
)


def render_recommendation_page():

    st.title(
        "🌱 Field-Specific Recommendation"
    )

    farm = st.session_state.get(
        "farm_data"
    )

    results = st.session_state.get(
        "analysis_results"
    )

    if not farm:

        st.warning(
            "Complete Farm Data Input first."
        )

        return

    if not results:

        st.warning(
            "Run the Dashboard analysis first."
        )

        return

    weather = results["weather"]
    ndvi = results["ndvi"]

    recommendation = (
        generate_recommendations(
            crop=farm["crop"],
            ndvi=ndvi["mean_ndvi"],
            temperature=weather[
                "temperature_c"
            ],
            humidity=weather[
                "humidity_percent"
            ],
            rainfall=weather[
                "rainfall_today_mm"
            ],
            irrigation_type=farm[
                "irrigation_type"
            ],
        )
    )

    # --------------------------------------------------
    # SUMMARY
    # --------------------------------------------------

    st.subheader("📋 Field Assessment")

    st.write(
        f"""
        **Crop:** {farm['crop']}

        **Coordinates:** \
        {farm['latitude']:.6f}, \
        {farm['longitude']:.6f}

        **Mean NDVI:** \
        {ndvi['mean_ndvi']:.3f}
        """
        if ndvi["mean_ndvi"] is not None
        else "NDVI unavailable."
    )

    # --------------------------------------------------
    # ALERTS
    # --------------------------------------------------

    if recommendation["alerts"]:

        st.subheader("⚠️ Priority Alerts")

        for alert in recommendation[
            "alerts"
        ]:

            st.error(alert)

    # --------------------------------------------------
    # OBSERVATIONS
    # --------------------------------------------------

    if recommendation[
        "observations"
    ]:

        st.subheader("🔎 Observations")

        for observation in recommendation[
            "observations"
        ]:

            st.info(observation)

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    st.subheader(
        "🚜 Recommended Actions"
    )

    for index, item in enumerate(
        recommendation[
            "recommendations"
        ],
        start=1,
    ):

        st.markdown(
            f"**{index}.** {item}"
        )

    # --------------------------------------------------
    # METHODOLOGY NOTE
    # --------------------------------------------------

    st.divider()

    st.caption(
        "Decision-support recommendations are generated "
        "from satellite vegetation indicators and "
        "weather conditions. They are intended to support "
        "field inspection and management decisions, not "
        "replace agronomic diagnosis or soil testing."
    )
