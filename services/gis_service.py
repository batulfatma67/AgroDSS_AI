from pathlib import Path
from typing import Optional, Tuple

import geopandas as gpd
from pyproj import Transformer
from shapely.geometry import Point
from shapely.ops import transform
import streamlit as st


# ============================================================
# PROJECT PATHS
# ============================================================
# This file is:
#
# AgriDSS_AI/
# └── services/
#     └── gis_service.py
#
# Therefore:
# PROJECT_ROOT = services/..
# DATA_DIR     = PROJECT_ROOT/data
#
# This approach does NOT depend on Streamlit's current
# working directory.
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

TEHSIL_PATH = DATA_DIR / "pakistan_tehsil.shp"
DISTRICT_PATH = DATA_DIR / "pakistan_district.shp"


# ============================================================
# DEBUG PROJECT STRUCTURE
# ============================================================

def debug_project_structure() -> None:
    """
    Display the project paths and GIS files available to the
    running application.

    This is primarily a diagnostic utility for Streamlit Cloud.
    """

    st.subheader("🔧 GIS Data Diagnostics")

    st.write(
        f"**Project root:** `{PROJECT_ROOT}`"
    )

    st.write(
        f"**Data directory:** `{DATA_DIR}`"
    )

    st.write(
        f"**Tehsil shapefile:** `{TEHSIL_PATH}`"
    )

    st.write(
        f"**Tehsil shapefile exists:** `{TEHSIL_PATH.exists()}`"
    )

    st.write(
        f"**District shapefile:** `{DISTRICT_PATH}`"
    )

    st.write(
        f"**District shapefile exists:** `{DISTRICT_PATH.exists()}`"
    )

    if DATA_DIR.exists():
        st.write("**Files found in data directory:**")

        files = sorted(
            file.name
            for file in DATA_DIR.iterdir()
            if file.is_file()
        )

        if files:
            for file_name in files:
                st.write(f"- `{file_name}`")
        else:
            st.warning("The data directory is empty.")

    else:
        st.error(
            f"The data directory does not exist: `{DATA_DIR}`"
        )


# ============================================================
# SHAPEFILE VALIDATION
# ============================================================

def _validate_shapefile_components(
    shapefile_path: Path,
) -> None:
    """
    Validate that the required ESRI Shapefile components exist.

    A shapefile is not a single file. At minimum, the .shp,
    .shx and .dbf components should be present.

    The .prj and .cpg files are strongly recommended.
    """

    if not shapefile_path.exists():
        raise FileNotFoundError(
            f"Shapefile not found: {shapefile_path}"
        )

    required_components = [
        shapefile_path.with_suffix(".shp"),
        shapefile_path.with_suffix(".shx"),
        shapefile_path.with_suffix(".dbf"),
    ]

    missing_components = [
        path.name
        for path in required_components
        if not path.exists()
    ]

    if missing_components:
        raise FileNotFoundError(
            "Required shapefile components are missing: "
            + ", ".join(missing_components)
            + f"\nExpected directory: {shapefile_path.parent}"
        )


# ============================================================
# LOAD TEHSIL BOUNDARIES
# ============================================================

@st.cache_data
def load_tehsil_boundaries() -> gpd.GeoDataFrame:
    """
    Load Pakistan tehsil boundaries and convert them to
    WGS84 geographic coordinates (EPSG:4326).

    The function uses an absolute path derived from the
    project structure, making it reliable on Streamlit Cloud.
    """

    _validate_shapefile_components(TEHSIL_PATH)

    try:
        gdf = gpd.read_file(TEHSIL_PATH)

    except Exception as exc:
        raise RuntimeError(
            f"Unable to read tehsil shapefile:\n"
            f"{TEHSIL_PATH}\n\n"
            f"Original error: {exc}"
        ) from exc

    if gdf.empty:
        raise ValueError(
            "The Pakistan tehsil shapefile contains no features."
        )

    if gdf.geometry is None:
        raise ValueError(
            "The tehsil shapefile does not contain a geometry column."
        )

    if gdf.crs is None:
        raise ValueError(
            "The tehsil shapefile has no CRS information. "
            "The .prj file may be missing or invalid."
        )

    # Convert to WGS84 so that coordinates entered by the
    # user (latitude/longitude) can be compared directly.
    gdf = gdf.to_crs("EPSG:4326")

    # Remove invalid/null geometries.
    gdf = gdf[
        gdf.geometry.notna()
        & ~gdf.geometry.is_empty
    ].copy()

    if gdf.empty:
        raise ValueError(
            "No valid geometries remain after loading the "
            "tehsil shapefile."
        )

    return gdf


# ============================================================
# LOAD DISTRICT BOUNDARIES
# ============================================================

@st.cache_data
def load_district_boundaries() -> gpd.GeoDataFrame:
    """
    Load Pakistan district boundaries and convert them to
    WGS84 geographic coordinates.
    """

    _validate_shapefile_components(DISTRICT_PATH)

    try:
        gdf = gpd.read_file(DISTRICT_PATH)

    except Exception as exc:
        raise RuntimeError(
            f"Unable to read district shapefile:\n"
            f"{DISTRICT_PATH}\n\n"
            f"Original error: {exc}"
        ) from exc

    if gdf.empty:
        raise ValueError(
            "The Pakistan district shapefile contains no features."
        )

    if gdf.crs is None:
        raise ValueError(
            "The district shapefile has no CRS information."
        )

    gdf = gdf.to_crs("EPSG:4326")

    gdf = gdf[
        gdf.geometry.notna()
        & ~gdf.geometry.is_empty
    ].copy()

    if gdf.empty:
        raise ValueError(
            "No valid geometries remain after loading the "
            "district shapefile."
        )

    return gdf


# ============================================================
# FIND ATTRIBUTE COLUMN
# ============================================================

def _find_column(
    gdf: gpd.GeoDataFrame,
    candidates: list[str],
) -> Optional[str]:
    """
    Find a dataframe column using case-insensitive matching.
    """

    normalized = {
        str(column).strip().upper(): column
        for column in gdf.columns
    }

    for candidate in candidates:
        candidate_key = candidate.strip().upper()

        if candidate_key in normalized:
            return normalized[candidate_key]

    return None


# ============================================================
# FIND ADMINISTRATIVE COLUMNS
# ============================================================

def _find_district_column(
    gdf: gpd.GeoDataFrame,
) -> Optional[str]:
    """
    Identify the district attribute column.

    Exact names are preferred first, followed by a conservative
    keyword search.
    """

    exact_candidates = [
        "DISTRICT",
        "District",
        "district",
        "DIST_NAME",
        "DISTNAME",
        "DISTRICT_NAME",
    ]

    column = _find_column(
        gdf,
        exact_candidates,
    )

    if column:
        return column

    for column in gdf.columns:
        name = str(column).strip().upper()

        if (
            "DISTRICT" in name
            or name == "DIST"
        ):
            return column

    return None


def _find_tehsil_column(
    gdf: gpd.GeoDataFrame,
) -> Optional[str]:
    """
    Identify the tehsil attribute column.

    Exact names are preferred first, followed by a conservative
    keyword search.
    """

    exact_candidates = [
        "TEHSIL",
        "Tehsil",
        "tehsil",
        "TAHSIL",
        "Tahsil",
        "TAHSIL_NAME",
        "TEHSIL_NAME",
        "TEHSIL_NAM",
    ]

    column = _find_column(
        gdf,
        exact_candidates,
    )

    if column:
        return column

    for column in gdf.columns:
        name = str(column).strip().upper()

        if (
            "TEHSIL" in name
            or "TAHSIL" in name
            or "TEH" == name
        ):
            return column

    return None


# ============================================================
# DETECT ADMINISTRATIVE LOCATION
# ============================================================

def detect_admin_location(
    latitude: float,
    longitude: float,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Identify the district and tehsil containing the supplied
    latitude/longitude coordinate.

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

        Returns (None, None) when the coordinate is not inside
        any supplied tehsil boundary.
    """

    # Basic coordinate validation.
    if not -90 <= latitude <= 90:
        raise ValueError(
            f"Invalid latitude: {latitude}"
        )

    if not -180 <= longitude <= 180:
        raise ValueError(
            f"Invalid longitude: {longitude}"
        )

    gdf = load_tehsil_boundaries()

    point = Point(
        float(longitude),
        float(latitude),
    )

    # covers() is preferable to contains() here because a
    # point lying exactly on a polygon boundary should still
    # be considered part of that administrative area.
    matches = gdf[
        gdf.geometry.covers(point)
    ]

    if matches.empty:
        return None, None

    row = matches.iloc[0]

    district_col = _find_district_column(gdf)
    tehsil_col = _find_tehsil_column(gdf)

    district = None
    tehsil = None

    if district_col is not None:
        value = row[district_col]

        if value is not None:
            district = str(value).strip()

    if tehsil_col is not None:
        value = row[tehsil_col]

        if value is not None:
            tehsil = str(value).strip()

    return district, tehsil


# ============================================================
# CREATE ANALYSIS GEOMETRY
# ============================================================

def create_analysis_geometry(
    latitude: float,
    longitude: float,
    radius_m: float,
):
    """
    Create a circular analysis region around a coordinate.

    The buffer is calculated in a metric UTM projection and
    transformed back to WGS84.

    Parameters
    ----------
    latitude:
        Latitude in decimal degrees.

    longitude:
        Longitude in decimal degrees.

    radius_m:
        Radius in metres.

    Returns
    -------
    shapely.geometry.Polygon
        Circular analysis region in EPSG:4326.
    """

    if not -90 <= latitude <= 90:
        raise ValueError(
            f"Invalid latitude: {latitude}"
        )

    if not -180 <= longitude <= 180:
        raise ValueError(
            f"Invalid longitude: {longitude}"
        )

    if radius_m <= 0:
        raise ValueError(
            "Analysis radius must be greater than zero."
        )

    point = Point(
        float(longitude),
        float(latitude),
    )

    # Determine the appropriate UTM zone.
    utm_zone = int(
        (float(longitude) + 180) / 6
    ) + 1

    # Clamp zone to valid UTM range.
    utm_zone = max(
        1,
        min(60, utm_zone),
    )

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
