"""
GIS Service
===========

Core geospatial utilities for AgriDSS AI.

Responsibilities
----------------
- Load Pakistan administrative boundary datasets.
- Normalize spatial data to WGS84.
- Detect district and tehsil from geographic coordinates.
- Create a metric analysis area around a farm coordinate.
- Provide reusable spatial utilities for downstream analysis.

Coordinate convention
---------------------
All geographic coordinates exposed by this module use:

    latitude  -> Y
    longitude -> X

The application's geographic reference system is WGS84 (EPSG:4326).
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Tuple

import geopandas as gpd
import streamlit as st
from pyproj import Transformer
from shapely.geometry import Point
from shapely.ops import transform


# ============================================================================
# PROJECT PATHS
# ============================================================================

# services/gis_service.py
#        │
#        └── parent      = services/
#             parent     = project root

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

TEHSIL_PATH = DATA_DIR / "pakistan_tehsil.shp"
DISTRICT_PATH = DATA_DIR / "pakistan_district.shp"


# ============================================================================
# CONSTANTS
# ============================================================================

WGS84_CRS = "EPSG:4326"


# ============================================================================
# DATASET VALIDATION
# ============================================================================


def _validate_shapefile_components(shapefile_path: Path) -> None:
    """
    Validate that the essential components of a shapefile exist.

    Parameters
    ----------
    shapefile_path:
        Path to the .shp file.

    Raises
    ------
    FileNotFoundError
        If the .shp file or required companion files are missing.
    """

    if not shapefile_path.exists():
        raise FileNotFoundError(
            f"Shapefile not found: {shapefile_path}"
        )

    required_extensions = (
        ".shp",
        ".shx",
        ".dbf",
        ".prj",
    )

    missing_files = [
        shapefile_path.with_suffix(extension)
        for extension in required_extensions
        if not shapefile_path.with_suffix(extension).exists()
    ]

    if missing_files:
        missing = "\n".join(
            f"  - {path.name}"
            for path in missing_files
        )

        raise FileNotFoundError(
            "Incomplete shapefile dataset.\n"
            f"Dataset: {shapefile_path.name}\n"
            "Missing files:\n"
            f"{missing}"
        )


# ============================================================================
# COLUMN UTILITIES
# ============================================================================


def _find_column(
    gdf: gpd.GeoDataFrame,
    candidates: list[str],
) -> Optional[str]:
    """
    Find a column using case-insensitive matching.

    Parameters
    ----------
    gdf:
        GeoDataFrame whose columns should be searched.

    candidates:
        Possible column names.

    Returns
    -------
    Optional[str]
        Matching column name or None.
    """

    normalized_columns = {
        str(column).strip().upper(): column
        for column in gdf.columns
    }

    for candidate in candidates:
        normalized_candidate = candidate.strip().upper()

        if normalized_candidate in normalized_columns:
            return normalized_columns[normalized_candidate]

    return None


def _find_administrative_column(
    gdf: gpd.GeoDataFrame,
    level: str,
) -> Optional[str]:
    """
    Identify an administrative attribute column.

    This function handles common naming variations found
    in administrative GIS datasets.
    """

    if level.lower() == "district":

        candidates = [
            "DISTRICT",
            "District",
            "district",
            "DIST_NAME",
            "DISTRICT_NAME",
            "DISTRICT_N",
            "DNAME",
        ]

    elif level.lower() == "tehsil":

        candidates = [
            "TEHSIL",
            "Tehsil",
            "tehsil",
            "TAHSIL",
            "Tahsil",
            "TEHSIL_NAME",
            "TEHSIL_N",
            "TNAME",
        ]

    else:
        return None

    return _find_column(gdf, candidates)


# ============================================================================
# LOAD TEHSIL BOUNDARIES
# ============================================================================


@st.cache_data(show_spinner="Loading tehsil boundaries...")
def load_tehsil_boundaries() -> gpd.GeoDataFrame:
    """
    Load Pakistan tehsil boundaries.

    The source dataset is automatically transformed to WGS84
    (EPSG:4326), which is the standard geographic CRS used
    throughout the application.

    Returns
    -------
    geopandas.GeoDataFrame
        Validated tehsil boundary dataset in WGS84.
    """

    _validate_shapefile_components(TEHSIL_PATH)

    try:
        gdf = gpd.read_file(TEHSIL_PATH)

    except Exception as exc:
        raise RuntimeError(
            "Unable to read the Pakistan tehsil shapefile. "
            f"Dataset: {TEHSIL_PATH}"
        ) from exc

    if gdf.empty:
        raise ValueError(
            "Pakistan tehsil shapefile contains no features."
        )

    if gdf.crs is None:
        raise ValueError(
            "Pakistan tehsil shapefile does not define a CRS."
        )

    # Normalize to geographic WGS84.
    if gdf.crs.to_string() != WGS84_CRS:
        gdf = gdf.to_crs(WGS84_CRS)

    # Remove invalid/empty geometries.
    gdf = gdf[
        gdf.geometry.notna()
        & ~gdf.geometry.is_empty
    ].copy()

    if gdf.empty:
        raise ValueError(
            "No valid geometries remain in the tehsil dataset."
        )

    return gdf


# ============================================================================
# LOAD DISTRICT BOUNDARIES
# ============================================================================


@st.cache_data(show_spinner="Loading district boundaries...")
def load_district_boundaries() -> gpd.GeoDataFrame:
    """
    Load Pakistan district boundaries.

    Returns
    -------
    geopandas.GeoDataFrame
        Validated district boundary dataset in WGS84.
    """

    _validate_shapefile_components(DISTRICT_PATH)

    try:
        gdf = gpd.read_file(DISTRICT_PATH)

    except Exception as exc:
        raise RuntimeError(
            "Unable to read the Pakistan district shapefile. "
            f"Dataset: {DISTRICT_PATH}"
        ) from exc

    if gdf.empty:
        raise ValueError(
            "Pakistan district shapefile contains no features."
        )

    if gdf.crs is None:
        raise ValueError(
            "Pakistan district shapefile does not define a CRS."
        )

    if gdf.crs.to_string() != WGS84_CRS:
        gdf = gdf.to_crs(WGS84_CRS)

    gdf = gdf[
        gdf.geometry.notna()
        & ~gdf.geometry.is_empty
    ].copy()

    if gdf.empty:
        raise ValueError(
            "No valid geometries remain in the district dataset."
        )

    return gdf


# ============================================================================
# COORDINATE VALIDATION
# ============================================================================


def _validate_coordinates(
    latitude: float,
    longitude: float,
) -> None:
    """
    Validate geographic coordinates.
    """

    if not (-90 <= latitude <= 90):
        raise ValueError(
            f"Invalid latitude: {latitude}. "
            "Latitude must be between -90 and 90."
        )

    if not (-180 <= longitude <= 180):
        raise ValueError(
            f"Invalid longitude: {longitude}. "
            "Longitude must be between -180 and 180."
        )


# ============================================================================
# ADMINISTRATIVE LOCATION DETECTION
# ============================================================================


def detect_admin_location(
    latitude: float,
    longitude: float,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Identify the district and tehsil containing a coordinate.

    Parameters
    ----------
    latitude:
        Geographic latitude in decimal degrees.

    longitude:
        Geographic longitude in decimal degrees.

    Returns
    -------
    tuple
        (district, tehsil)

        Returns (None, None) when the coordinate does not
        intersect a known tehsil boundary.
    """

    _validate_coordinates(latitude, longitude)

    gdf = load_tehsil_boundaries()

    point = Point(longitude, latitude)

    # Primary spatial test.
    matches = gdf[gdf.geometry.contains(point)]

    # ``contains`` excludes boundary points. ``intersects``
    # provides a safer fallback for coordinates lying exactly
    # on an administrative boundary.
    if matches.empty:
        matches = gdf[gdf.geometry.intersects(point)]

    if matches.empty:
        return None, None

    row = matches.iloc[0]

    district_col = _find_administrative_column(
        gdf,
        "district",
    )

    tehsil_col = _find_administrative_column(
        gdf,
        "tehsil",
    )

    district = (
        str(row[district_col]).strip()
        if district_col
        and row[district_col] is not None
        else None
    )

    tehsil = (
        str(row[tehsil_col]).strip()
        if tehsil_col
        and row[tehsil_col] is not None
        else None
    )

    return district, tehsil


# ============================================================================
# DISTRICT DETECTION
# ============================================================================


def detect_district(
    latitude: float,
    longitude: float,
) -> Optional[str]:
    """
    Identify the district containing a coordinate.

    This function uses the dedicated district boundary dataset
    rather than relying on attributes stored in the tehsil layer.
    """

    _validate_coordinates(latitude, longitude)

    gdf = load_district_boundaries()

    point = Point(longitude, latitude)

    matches = gdf[gdf.geometry.contains(point)]

    if matches.empty:
        matches = gdf[gdf.geometry.intersects(point)]

    if matches.empty:
        return None

    district_col = _find_administrative_column(
        gdf,
        "district",
    )

    if district_col is None:
        raise ValueError(
            "Unable to identify the district attribute "
            "in the district boundary dataset."
        )

    value = matches.iloc[0][district_col]

    if value is None:
        return None

    return str(value).strip()


# ============================================================================
# ANALYSIS GEOMETRY
# ============================================================================


def create_analysis_geometry(
    latitude: float,
    longitude: float,
    radius_m: float,
):
    """
    Create a circular analysis area around a geographic coordinate.

    Buffering is performed in a local UTM projection so that
    ``radius_m`` represents an actual distance in meters.

    Parameters
    ----------
    latitude:
        Geographic latitude.

    longitude:
        Geographic longitude.

    radius_m:
        Analysis radius in meters.

    Returns
    -------
    shapely.geometry.Polygon
        Circular analysis geometry in WGS84.

    Raises
    ------
    ValueError
        If coordinates or radius are invalid.
    """

    _validate_coordinates(latitude, longitude)

    if radius_m <= 0:
        raise ValueError(
            "Analysis radius must be greater than zero."
        )

    point = Point(longitude, latitude)

    # Determine UTM zone from longitude.
    utm_zone = int((longitude + 180) // 6) + 1

    # EPSG 326xx = WGS84 / UTM northern hemisphere
    # EPSG 327xx = WGS84 / UTM southern hemisphere
    if latitude >= 0:
        utm_epsg = 32600 + utm_zone
    else:
        utm_epsg = 32700 + utm_zone

    to_utm = Transformer.from_crs(
        WGS84_CRS,
        f"EPSG:{utm_epsg}",
        always_xy=True,
    ).transform

    to_wgs84 = Transformer.from_crs(
        f"EPSG:{utm_epsg}",
        WGS84_CRS,
        always_xy=True,
    ).transform

    projected_point = transform(
        to_utm,
        point,
    )

    buffered_geometry = projected_point.buffer(
        radius_m
    )

    return transform(
        to_wgs84,
        buffered_geometry,
    )


# ============================================================================
# COORDINATE → POINT
# ============================================================================


def create_point(
    latitude: float,
    longitude: float,
) -> Point:
    """
    Create a WGS84 Shapely point from latitude/longitude.
    """

    _validate_coordinates(latitude, longitude)

    return Point(
        float(longitude),
        float(latitude),
    )
