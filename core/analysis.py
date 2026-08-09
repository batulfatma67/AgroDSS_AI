def classify_ndvi(ndvi):

    if ndvi is None:
        return {
            "class": "No Data",
            "severity": "unknown",
        }

    if ndvi < 0.20:
        return {
            "class": "Very Low Vegetation",
            "severity": "critical",
        }

    if ndvi < 0.40:
        return {
            "class": "Low Vegetation",
            "severity": "high",
        }

    if ndvi < 0.60:
        return {
            "class": "Moderate Vegetation",
            "severity": "moderate",
        }

    if ndvi < 0.80:
        return {
            "class": "Healthy Vegetation",
            "severity": "low",
        }

    return {
        "class": "Very Dense Vegetation",
        "severity": "low",
    }


def calculate_risk(
    ndvi,
    temperature,
    humidity,
    rainfall,
):

    score = 0
    factors = []

    if ndvi is not None:

        if ndvi < 0.20:
            score += 40
            factors.append(
                "Very low vegetation index"
            )

        elif ndvi < 0.40:
            score += 25
            factors.append(
                "Low vegetation index"
            )

    if temperature >= 35:

        score += 25
        factors.append(
            "High temperature stress"
        )

    elif temperature >= 32:

        score += 15
        factors.append(
            "Elevated temperature"
        )

    if humidity < 30:

        score += 15
        factors.append(
            "Low atmospheric humidity"
        )

    if rainfall < 2:

        score += 10
        factors.append(
            "Low recent precipitation"
        )

    if score >= 60:
        category = "High"

    elif score >= 30:
        category = "Moderate"

    else:
        category = "Low"

    return {
        "score": min(score, 100),
        "category": category,
        "factors": factors,
    }
