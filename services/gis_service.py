from __future__ import annotations

from pathlib import Path
from typing import Optional

import geopandas as gpd
from pyproj import Transformer
from shapely.geometry import Point
from shapely.ops import transform


# ----------------------------------------------------------------------
# PROJECT PATHS
# ----------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

TEHSIL_PATH = DATA_DIR / "pakistan_tehsil.shp"
DISTRICT_PATH = DATA_DIR / "pakistan_district.shp"


# ----------------------------------------------------------------------
# SHAPEFILE VALIDATION
# ----------------------------------------------------------------------

def _validate_shapefile_components(
    shapefile_path: Path,
) -> None:
    """
    Validate that the required ESRI Shapefile components exist.
    """

    required_extensions = (
        ".shp",
        ".shx",
        ".dbf",
        ".prj",
    )

    missing_files = [
        shapefile_path.with_suffix(extension)
        for extension in required_extensions
        if not shapefile_path.with_suffix(extension).is_file()
    ]

    if missing_files:
        missing_names = ", ".join(
            file.name for file in missing_files
        )

        raise FileNotFoundError(
            f"Required shapefile components are missing for "
            f"'{shapefile_path.name}': {missing_names}"
        )


# ----------------------------------------------------------------------
# TEHSIL DATASET
# ----------------------------------------------------------------------

def load_tehsil_boundaries() -> gpd.GeoDataFrame:
    """
    Load Pakistan tehsil boundaries and convert them to WGS84.

    Returns
    -------
    geopandas.GeoDataFrame
        Tehsil boundaries in EPSG:4326.
    """

    _validate_shapefile_components(TEHSIL_PATH)

    gdf = gpd.read_file(TEHSIL_PATH)

    if gdf.empty:
        raise ValueError(
            "The Pakistan tehsil shapefile contains no features."
        )

    if gdf.crs is None:
        raise ValueError(
            "The Pakistan tehsil shapefile does not contain "
            "a coordinate reference system."
        )

    if gdf.geometry.is_empty.all():
        raise ValueError(
            "The Pakistan tehsil shapefile contains no valid geometries."
        )

    return gdf.to_crs("EPSG:4326")


# ----------------------------------------------------------------------
# COLUMN DETECTION
# ----------------------------------------------------------------------

def _find_column(
    gdf: gpd.GeoDataFrame,
    candidates: list[str],
) -> Optional[str]:
    """
    Find a GeoDataFrame column using case-insensitive matching.
    """

    normalized_columns = {
        str(column).strip().upper(): column
        for column in gdf.columns
    }

    for candidate in candidates:
        column = normalized_columns.get(
            candidate.strip().upper()
        )

        if column is not None:
            return column

    return None


# ----------------------------------------------------------------------
# ADMINISTRATIVE LOCATION
# ----------------------------------------------------------------------

def detect_admin_location(
    latitude: float,
    longitude: float,
) -> tuple[Optional[str], Optional[str]]:
    """
    Determine the district and tehsil containing a coordinate.

    Parameters
    ----------
    latitude : float
        Latitude in decimal degrees.

    longitude : float
        Longitude in decimal degrees.

    Returns
    -------
    tuple
        (district, tehsil), or (None, None) when the coordinate
        does not fall within the supplied boundary dataset.
    """

    gdf = load_tehsil_boundaries()

    point = Point(
        float(longitude),
        float(latitude),
    )

    # ``covers`` is preferable to ``contains`` here because it also
    # handles points lying exactly on a polygon boundary.
    matches = gdf[gdf.geometry.covers(point)]

    if matches.empty:
        return None, None

    district_column = _find_column(
        gdf,
        [
            "DISTRICT",
            "DISTRICT_NAME",
            "DIST_NAME",
        ],
    )

    tehsil_column = _find_column(
        gdf,
        [
            "TEHSIL",
            "TEHSIL_NAME",
            "TEH_NAME",
            "TAHSIL",
        ],
    )

    row = matches.iloc[0]

    district = (
        str(row[district_column]).strip()
        if district_column
        and row[district_column] is not None
        else None
    )

    tehsil = (
        str(row[tehsil_column]).strip()
        if tehsil_column
        and row[tehsil_column] is not None
        else None
    )

    return district, tehsil


# ----------------------------------------------------------------------
# ANALYSIS REGION
# ----------------------------------------------------------------------

def create_analysis_geometry(
    latitude: float,
    longitude: float,
    radius_m: float,
):
    """
    Create a circular analysis region around a coordinate.

    The buffer is generated in a metric UTM projection and then
    transformed back to WGS84. This avoids performing distance
    calculations directly in geographic degrees.
    """

    if radius_m <= 0:
        raise ValueError(
            "Analysis radius must be greater than zero."
        )

    point = Point(
        float(longitude),
        float(latitude),
    )

    utm_zone = int(
        (float(longitude) + 180.0) / 6.0
    ) + 1

    if float(latitude) >= 0:
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

    projected_point = transform(
        to_utm,
        point,
    )

    buffered_geometry = projected_point.buffer(
        float(radius_m)
    )

    return transform(
        to_wgs84,
        buffered_geometry,
    )
