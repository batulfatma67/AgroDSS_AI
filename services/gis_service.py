from pathlib import Path
from typing import Optional, Tuple

import geopandas as gpd
from shapely.geometry import Point
from shapely.ops import transform
from pyproj import Transformer


TEHSIL_PATH = Path("data/pakistan_tehsil.shp")


def load_tehsil_boundaries() -> gpd.GeoDataFrame:
    """
    Load Pakistan tehsil boundaries and normalize them
    to WGS84 geographic coordinates.
    """

    gdf = gpd.read_file(TEHSIL_PATH)

    if gdf.empty:
        raise ValueError("Tehsil shapefile contains no features.")

    if gdf.crs is None:
        raise ValueError(
            "Tehsil shapefile has no CRS definition."
        )

    return gdf.to_crs("EPSG:4326")


def detect_admin_location(
    latitude: float,
    longitude: float,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Identify the administrative district and tehsil
    containing the supplied coordinate.
    """

    gdf = load_tehsil_boundaries()

    point = Point(longitude, latitude)

    matches = gdf[gdf.geometry.contains(point)]

    if matches.empty:
        return None, None

    row = matches.iloc[0]

    district_col = _find_column(
        gdf,
        ["DISTRICT", "District", "district"],
    )

    tehsil_col = _find_column(
        gdf,
        ["TEHSIL", "Tehsil", "tehsil"],
    )

    district = (
        str(row[district_col])
        if district_col
        else None
    )

    tehsil = (
        str(row[tehsil_col])
        if tehsil_col
        else None
    )

    return district, tehsil


def create_analysis_geometry(
    latitude: float,
    longitude: float,
    radius_m: float,
):
    """
    Create a metric buffer around the selected coordinate.

    Buffering is performed in an appropriate UTM projection
    rather than directly in latitude/longitude degrees.
    """

    point = Point(longitude, latitude)

    utm_zone = int((longitude + 180) / 6) + 1

    if latitude >= 0:
        epsg = 32600 + utm_zone
    else:
        epsg = 32700 + utm_zone

    to_utm = Transformer.from_crs(
        "EPSG:4326",
        f"EPSG:{epsg}",
        always_xy=True,
    ).transform

    to_wgs84 = Transformer.from_crs(
        f"EPSG:{epsg}",
        "EPSG:4326",
        always_xy=True,
    ).transform

    projected_point = transform(to_utm, point)

    buffered = projected_point.buffer(radius_m)

    return transform(to_wgs84, buffered)


def _find_column(
    gdf: gpd.GeoDataFrame,
    candidates: list[str],
) -> Optional[str]:

    normalized = {
        column.upper(): column
        for column in gdf.columns
    }

    for candidate in candidates:

        if candidate.upper() in normalized:
            return normalized[candidate.upper()]

    return None
