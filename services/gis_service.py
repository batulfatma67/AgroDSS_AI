from pathlib import Path
from typing import Optional, Tuple

import geopandas as gpd
import streamlit as st
from pyproj import Transformer
from shapely.geometry import Point
from shapely.ops import transform


# ============================================================
# PROJECT PATHS
# ============================================================

# services/gis_service.py
#        ↓ parents[0] = services
#        ↓ parents[1] = project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

TEHSIL_PATH = DATA_DIR / "pakistan_tehsil.shp"
DISTRICT_PATH = DATA_DIR / "pakistan_district.shp"


# ============================================================
# TEMPORARY DEPLOYMENT DEBUGGER
# ============================================================

def debug_project_structure() -> None:
    """
    Temporary diagnostic utility for Streamlit deployment.

    Displays the resolved project root, data directory,
    shapefile paths, existence checks, and files visible
    inside the deployed application directory.

    Remove this function after the deployment issue is resolved.
    """

    st.write("### 🔍 GIS Deployment Diagnostics")

    st.write("**Project root:**")
    st.code(str(PROJECT_ROOT))

    st.write("**Data directory:**")
    st.code(str(DATA_DIR))

    st.write("**Tehsil shapefile:**")
    st.code(str(TEHSIL_PATH))

    st.write("**District shapefile:**")
    st.code(str(DISTRICT_PATH))

    st.write("**Path checks:**")

    st.write(
        {
            "project_root_exists": PROJECT_ROOT.exists(),
            "data_directory_exists": DATA_DIR.exists(),
            "tehsil_shp_exists": TEHSIL_PATH.exists(),
            "tehsil_shx_exists": TEHSIL_PATH.with_suffix(".shx").exists(),
            "tehsil_dbf_exists": TEHSIL_PATH.with_suffix(".dbf").exists(),
            "tehsil_prj_exists": TEHSIL_PATH.with_suffix(".prj").exists(),
            "tehsil_cpg_exists": TEHSIL_PATH.with_suffix(".cpg").exists(),
            "district_shp_exists": DISTRICT_PATH.exists(),
            "district_shx_exists": DISTRICT_PATH.with_suffix(".shx").exists(),
            "district_dbf_exists": DISTRICT_PATH.with_suffix(".dbf").exists(),
            "district_prj_exists": DISTRICT_PATH.with_suffix(".prj").exists(),
            "district_cpg_exists": DISTRICT_PATH.with_suffix(".cpg").exists(),
        }
    )

    st.write("**Files visible inside the project:**")

    if PROJECT_ROOT.exists():

        files = sorted(
            path.relative_to(PROJECT_ROOT).as_posix()
            for path in PROJECT_ROOT.rglob("*")
            if path.is_file()
        )

        if files:
            st.code("\n".join(files))
        else:
            st.warning("No files were found inside the project root.")

    else:
        st.error("Project root does not exist.")


# ============================================================
# SHAPEFILE VALIDATION
# ============================================================

def _validate_shapefile_components(shapefile_path: Path) -> None:
    """
    Validate that all required shapefile components exist.

    A shapefile normally consists of at least:
        .shp
        .shx
        .dbf

    A .prj file is strongly recommended because it defines
    the coordinate reference system.
    """

    if not shapefile_path.exists():
        raise FileNotFoundError(
            f"Shapefile not found: {shapefile_path}"
        )

    required_components = [
        shapefile_path,
        shapefile_path.with_suffix(".shx"),
        shapefile_path.with_suffix(".dbf"),
    ]

    missing_components = [
        str(path)
        for path in required_components
        if not path.exists()
    ]

    if missing_components:
        raise FileNotFoundError(
            "Required shapefile components are missing:\n"
            + "\n".join(missing_components)
        )

    prj_path = shapefile_path.with_suffix(".prj")

    if not prj_path.exists():
        raise ValueError(
            f"Projection file is missing: {prj_path}"
        )


# ============================================================
# LOAD TEHSIL BOUNDARIES
# ============================================================

@st.cache_data(show_spinner="Loading administrative boundaries...")
def load_tehsil_boundaries() -> gpd.GeoDataFrame:
    """
    Load Pakistan tehsil boundaries and normalize them
    to WGS84 geographic coordinates (EPSG:4326).
    """

    _validate_shapefile_components(TEHSIL_PATH)

    try:
        gdf = gpd.read_file(TEHSIL_PATH)

    except Exception as exc:
        raise RuntimeError(
            "Unable to read the Pakistan tehsil shapefile. "
            f"Path: {TEHSIL_PATH}. "
            f"Original error: {exc}"
        ) from exc

    if gdf.empty:
        raise ValueError(
            "Pakistan tehsil shapefile contains no features."
        )

    if gdf.crs is None:
        raise ValueError(
            "Pakistan tehsil shapefile has no CRS definition."
        )

    if gdf.geometry.is_empty.all():
        raise ValueError(
            "Pakistan tehsil shapefile contains no valid geometries."
        )

    # Normalize to WGS84 for coordinate-based spatial queries.
    if gdf.crs.to_epsg() != 4326:
        gdf = gdf.to_crs("EPSG:4326")

    return gdf


# ============================================================
# DETECT ADMINISTRATIVE LOCATION
# ============================================================

def detect_admin_location(
    latitude: float,
    longitude: float,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Identify the administrative district and tehsil
    containing the supplied geographic coordinate.

    Parameters
    ----------
    latitude : float
        Latitude in decimal degrees.

    longitude : float
        Longitude in decimal degrees.

    Returns
    -------
    tuple[str | None, str | None]
        District and tehsil names.

    Notes
    -----
    The input coordinate is assumed to use WGS84
    geographic coordinates (EPSG:4326).
    """

    gdf = load_tehsil_boundaries()

    point = Point(float(longitude), float(latitude))

    # 'covers' is preferable to 'contains' here because it also
    # handles a point that falls exactly on a polygon boundary.
    matches = gdf[gdf.geometry.covers(point)]

    if matches.empty:
        return None, None

    row = matches.iloc[0]

    district_col = _find_column(
        gdf,
        [
            "DISTRICT",
            "District",
            "district",
            "DIST_NAME",
            "DISTRICT_NAME",
        ],
    )

    tehsil_col = _find_column(
        gdf,
        [
            "TEHSIL",
            "Tehsil",
            "tehsil",
            "TAHSIL",
            "TAHSIL_NAME",
            "TEHSIL_NAME",
        ],
    )

    district = (
        str(row[district_col]).strip()
        if district_col and row[district_col] is not None
        else None
    )

    tehsil = (
        str(row[tehsil_col]).strip()
        if tehsil_col and row[tehsil_col] is not None
        else None
    )

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
    Create a metric buffer around a selected coordinate.

    The point is transformed from WGS84 into the appropriate
    UTM zone before buffering so that radius_m represents
    metres rather than degrees.

    Parameters
    ----------
    latitude : float
        Latitude in decimal degrees.

    longitude : float
        Longitude in decimal degrees.

    radius_m : float
        Buffer radius in metres.

    Returns
    -------
    shapely.geometry.Polygon
        Buffered geometry transformed back to WGS84.
    """

    if radius_m <= 0:
        raise ValueError("radius_m must be greater than zero.")

    if not -90 <= latitude <= 90:
        raise ValueError("Latitude must be between -90 and 90 degrees.")

    if not -180 <= longitude <= 180:
        raise ValueError(
            "Longitude must be between -180 and 180 degrees."
        )

    point = Point(float(longitude), float(latitude))

    # Determine the UTM zone from longitude.
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

    projected_point = transform(
        to_utm,
        point,
    )

    buffered = projected_point.buffer(radius_m)

    return transform(
        to_wgs84,
        buffered,
    )


# ============================================================
# COLUMN DETECTION
# ============================================================

def _find_column(
    gdf: gpd.GeoDataFrame,
    candidates: list[str],
) -> Optional[str]:
    """
    Find a GeoDataFrame column using case-insensitive matching.

    Parameters
    ----------
    gdf : geopandas.GeoDataFrame
        Input spatial dataset.

    candidates : list[str]
        Possible column names.

    Returns
    -------
    str | None
        Matching original column name, if found.
    """

    normalized = {
        str(column).strip().upper(): column
        for column in gdf.columns
    }

    for candidate in candidates:

        normalized_candidate = (
            str(candidate).strip().upper()
        )

        if normalized_candidate in normalized:
            return normalized[normalized_candidate]

    return None
