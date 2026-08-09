from datetime import datetime
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors

from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle,
)

from reportlab.lib.units import cm

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)


def generate_pdf_report(
    farm,
    weather,
    ndvi,
    recommendations,
    map_path,
    output_path,
):

    document = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=1.5 * cm,
        leftMargin=1.5 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontSize=20,
        spaceAfter=12,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        textColor=colors.HexColor(
            "#166534"
        ),
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = styles["BodyText"]

    story = []

    story.append(
        Paragraph(
            "AgriDSS AI",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Agricultural Field Intelligence Report",
            styles["Heading2"],
        )
    )

    story.append(
        Paragraph(
            datetime.now().strftime(
                "Generated: %Y-%m-%d %H:%M"
            ),
            body_style,
        )
    )

    story.append(Spacer(1, 12))

    # --------------------------------------------------
    # FARM INFORMATION
    # --------------------------------------------------

    story.append(
        Paragraph(
            "1. Farm Information",
            heading_style,
        )
    )

    farm_table = Table(
        [
            ["Parameter", "Value"],

            [
                "Crop",
                farm["crop"],
            ],

            [
                "Area",
                f"{farm['area_acres']:.2f} acres",
            ],

            [
                "Irrigation",
                farm["irrigation_type"],
            ],

            [
                "Latitude",
                f"{farm['latitude']:.6f}",
            ],

            [
                "Longitude",
                f"{farm['longitude']:.6f}",
            ],

            [
                "District",
                farm.get(
                    "district"
                ) or "Not identified",
            ],

            [
                "Tehsil",
                farm.get(
                    "tehsil"
                ) or "Not identified",
            ],
        ],
        colWidths=[
            6 * cm,
            10 * cm,
        ],
    )

    farm_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#166534"
                    ),
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),

                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
            ]
        )
    )

    story.append(farm_table)

    # --------------------------------------------------
    # MAP
    # --------------------------------------------------

    if map_path and Path(
        map_path
    ).exists():

        story.append(
            Paragraph(
                "2. Farm Location Map",
                heading_style,
            )
        )

        story.append(
            Image(
                str(map_path),
                width=16 * cm,
                height=9 * cm,
            )
        )

    # --------------------------------------------------
    # SATELLITE
    # --------------------------------------------------

    story.append(
        Paragraph(
            "3. Satellite Vegetation Analysis",
            heading_style,
        )
    )

    satellite_data = [
        ["Metric", "Value"],

        [
            "Mean NDVI",
            format_value(
                ndvi["mean_ndvi"]
            ),
        ],

        [
            "Minimum NDVI",
            format_value(
                ndvi["minimum_ndvi"]
            ),
        ],

        [
            "Maximum NDVI",
            format_value(
                ndvi["maximum_ndvi"]
            ),
        ],

        [
            "Scenes Used",
            str(ndvi["image_count"]),
        ],

        [
            "Observation Period",
            f"{ndvi['start_date']} → "
            f"{ndvi['end_date']}",
        ],
    ]

    table = Table(
        satellite_data,
        colWidths=[
            6 * cm,
            10 * cm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#166534"
                    ),
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
            ]
        )
    )

    story.append(table)

    # --------------------------------------------------
    # WEATHER
    # --------------------------------------------------

    story.append(
        Paragraph(
            "4. Weather Conditions",
            heading_style,
        )
    )

    weather_data = [
        ["Metric", "Value"],

        [
            "Temperature",
            f"{weather['temperature_c']:.1f} °C",
        ],

        [
            "Humidity",
            f"{weather['humidity_percent']:.0f} %",
        ],

        [
            "Rainfall Today",
            f"{weather['rainfall_today_mm']:.1f} mm",
        ],

        [
            "Wind Speed",
            f"{weather['wind_speed_kmh']:.1f} km/h",
        ],

        [
            "Condition",
            weather[
                "weather_description"
            ],
        ],
    ]

    weather_table = Table(
        weather_data,
        colWidths=[
            6 * cm,
            10 * cm,
        ],
    )

    weather_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor(
                        "#0369A1"
                    ),
                ),

                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),

                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
            ]
        )
    )

    story.append(weather_table)

    # --------------------------------------------------
    # RECOMMENDATIONS
    # --------------------------------------------------

    story.append(
        Paragraph(
            "5. Decision-Support Recommendations",
            heading_style,
        )
    )

    for index, item in enumerate(
        recommendations[
            "recommendations"
        ],
        start=1,
    ):

        story.append(
            Paragraph(
                f"{index}. {item}",
                body_style,
            )
        )

        story.append(
            Spacer(1, 5)
        )

    # --------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------

    story.append(Spacer(1, 15))

    story.append(
        Paragraph(
            "<b>Methodological note:</b> "
            "Satellite vegetation indices and weather "
            "conditions are decision-support indicators. "
            "They should be interpreted together with "
            "field observations, soil measurements, "
            "crop growth stage and local agronomic knowledge.",
            body_style,
        )
    )

    document.build(story)


def format_value(value):

    if value is None:
        return "N/A"

    return f"{float(value):.3f}"
