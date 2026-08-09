def generate_recommendations(
    crop,
    ndvi,
    temperature,
    humidity,
    rainfall,
    irrigation_type,
):

    recommendations = []
    alerts = []
    observations = []

    # --------------------------------------------------
    # VEGETATION CONDITION
    # --------------------------------------------------

    if ndvi is None:

        alerts.append(
            "NDVI could not be calculated. "
            "Avoid making vegetation-health decisions "
            "until satellite observations are available."
        )

    elif ndvi < 0.20:

        alerts.append(
            "Very low vegetation activity detected."
        )

        recommendations.append(
            "Inspect the field immediately for "
            "water stress, crop damage, bare soil, "
            "pest pressure, or poor crop establishment."
        )

    elif ndvi < 0.40:

        alerts.append(
            "Vegetation activity is below the "
            "healthy monitoring range."
        )

        recommendations.append(
            "Inspect soil moisture and crop uniformity "
            "before making irrigation or nutrient decisions."
        )

    elif ndvi < 0.60:

        observations.append(
            "Vegetation condition is moderate."
        )

        recommendations.append(
            "Continue routine field monitoring and "
            "compare future NDVI observations for trends."
        )

    else:

        observations.append(
            "Vegetation activity is currently healthy."
        )

        recommendations.append(
            "Maintain the existing management program "
            "while continuing routine monitoring."
        )

    # --------------------------------------------------
    # TEMPERATURE
    # --------------------------------------------------

    if temperature >= 35:

        alerts.append(
            "High temperature conditions may increase "
            "crop water demand."
        )

        recommendations.append(
            "Prioritize soil-moisture monitoring during "
            "the hottest part of the day."
        )

    # --------------------------------------------------
    # HUMIDITY
    # --------------------------------------------------

    if humidity < 30:

        observations.append(
            "Low atmospheric humidity may increase "
            "evaporative demand."
        )

    # --------------------------------------------------
    # RAINFALL
    # --------------------------------------------------

    if rainfall < 2:

        recommendations.append(
            "Recent rainfall is limited. Check actual "
            "soil moisture before scheduling irrigation."
        )

    elif rainfall >= 20:

        recommendations.append(
            "Recent rainfall is substantial. Verify "
            "field drainage and avoid unnecessary irrigation."
        )

    # --------------------------------------------------
    # IRRIGATION
    # --------------------------------------------------

    if irrigation_type.lower() == "rainfed":

        recommendations.append(
            "Because the field is rainfed, rainfall "
            "and soil-moisture trends should receive "
            "greater monitoring priority."
        )

    elif irrigation_type.lower() == "flood":

        recommendations.append(
            "For flood irrigation, use soil-moisture "
            "observations to avoid unnecessary water application."
        )

    elif irrigation_type.lower() in {
        "drip",
        "sprinkler",
    }:

        recommendations.append(
            "The selected irrigation system allows "
            "more controlled water application; adjust "
            "irrigation according to measured field conditions."
        )

    # --------------------------------------------------
    # FERTILIZER SAFETY
    # --------------------------------------------------

    recommendations.append(
        "Do not infer a fertilizer dose from NDVI alone. "
        "Nutrient recommendations should be supported by "
        "soil testing and crop growth-stage information."
    )

    return {
        "crop": crop,
        "alerts": alerts,
        "observations": observations,
        "recommendations": recommendations,
    }
