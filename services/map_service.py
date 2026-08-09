from staticmap import (
    StaticMap,
    CircleMarker,
)


def create_static_farm_map(
    latitude,
    longitude,
    output_path,
):

    width = 1000
    height = 600

    static_map = StaticMap(
        width,
        height,
        url_template=(
            "https://tile.openstreetmap.org/"
            "{z}/{x}/{y}.png"
        ),
    )

    marker = CircleMarker(
        (
            longitude,
            latitude,
        ),
        "#166534",
        14,
    )

    static_map.add_marker(
        marker
    )

    image = static_map.render(
        zoom=14,
        center=(
            longitude,
            latitude,
        ),
    )

    image.save(
        output_path
    )

    return output_path
