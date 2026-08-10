from pathlib import Path
from typing import Optional, Tuple

import geopandas as gpd
from pyproj import Transformer
from shapely.geometry import Point
from shapely.ops import transform


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"

TEHSIL_PATH = DATA_DIR / "pakistan_tehsil.shp"
DISTRICT_PATH = DATA_DIR / "pakistan_district.shp"


# ============================================================
# DEPLOYMENT DIAGNOSTICS
# ============================================================

def print_project_structure() -> None:
    """
    Print the deployed project structure.

    This is a temporary diagnostic function used to determine
    exactly which files are available on Streamlit Cloud.
    """

    print("=" * 70)
    print("AgriDSS AI — DEPLOYMENT DIAGNOSTICS")
    print("=" * 70)

    print(f"PROJECT_ROOT : {PROJECT_ROOT}")
    print(f"DATA_DIR     : {DATA_DIR}")
    print(f"TEHSIL_PATH  : {TEHSIL_PATH}")
    print(f"DISTRICT_PATH: {DISTRICT_PATH}")

    print("-" * 70)
    print("PATH EXISTENCE")
    print("-" * 70)

    paths_to_check = [
        PROJECT_ROOT,
        DATA_DIR,
        TEHSIL_PATH,
        TEHSIL_PATH.with_suffix(".shx"),
        TEHSIL_PATH.with_suffix(".dbf"),
        TEHSIL_PATH.with_suffix(".prj"),
        TEHSIL_PATH.with_suffix(".cpg"),
        DISTRICT_PATH,
        DISTRICT_PATH.with_suffix(".shx"),
        DISTRICT_PATH.with_suffix(".dbf"),
        DISTRICT_PATH.with_suffix(".prj"),
        DISTRICT_PATH.with_suffix(".cpg"),
    ]

    for path in paths_to_check:
        print(f"{path} -> {path.exists()}")

    print("-" * 70)
    print("ALL FILES VISIBLE FROM PROJECT ROOT")
    print("-" * 70)

    if PROJECT_ROOT.exists():

        for path in sorted(PROJECT_ROOT.rglob("*")):

            if path.is_file():
                print(
                    path.relative_to(PROJECT_ROOT)
                )

    else:
        print("PROJECT ROOT DOES NOT EXIST.")

    print("=" * 70)


# ============================================================
# RUN DIAGNOSTICS ON IMPORT
# ============================================================

print_project_structure()


# ============================================================
# SHAPEFILE VALIDATION
# ============================================================

def _validate_shapefile_components(
    shapefile_path: Path,
) -> None:

    if not shapefile_path.exists():

        raise FileNotFoundError(
            f"Shapefile not found: {shapefile_path}"
        )

    required_components = [
        shapefile_path,
        shapefile_path.with_suffix(".shx"),
        shapefile_path.with_suffix(".dbf"),
    ]

    missing = [
        str(path)
        for path in required_components
        if not path.exists()
    ]

    if missing:

        raise FileNotFoundError(
            "Required shapefile components are missing:\n"
            + "\n".join(missing)
        )

    prj_path = shapefile_path.with_suffix(".prj")

    if not prj_path.exists():

        raise ValueError(
            f"Projection file is missing: {prj_path}"
        )


# ============================================================
# LOAD TEHSIL BOUNDARIES
# ============================================================

def load_tehsil_boundaries() -> gpd.GeoDataFrame:

    _validate_shapefile_components(
        TEHSIL_PATH
    )

    try:

        gdf = gpd.read_file(
            TEHSIL_PATH
        )

    except Exception as exc:

        raise RuntimeError(
            "Unable to read the Pakistan tehsil "
            f"shapefile at {TEHSIL_PATH}. "
            f"Original error: {exc}"
        ) from exc

    if gdf.empty:

        raise ValueError(
            "Pakistan tehsil shapefile contains no features."
        )

    if gdf.crs is None:

        raise ValueError(
            "Pakistan tehsil shapefile has no CRS."
        )

    if gdf.geometry.is_empty.all():

        raise ValueError(
            "Pakistan tehsil shapefile contains "
            "no valid geometries."
        )

    if gdf.crs.to_epsg() != 4326:

        gdf = gdf.to_crs(
            "EPSG:4326"
        )

    return gdf


# ============================================================
# ADMINISTRATIVE LOCATION DETECTION
# ============================================================

def detect_admin_location(
    latitude: float,
    longitude: float,
) -> Tuple[
    Optional[str],
    Optional[str],
]:

    gdf = load_tehsil_boundaries()

    point = Point(
        float(longitude),
        float(latitude),
    )

    matches = gdf[
        gdf.geometry.covers(point)
    ]

    if matches.empty:

        return None, None

    row = matches.iloc[0]

    district_col = _find_column(
        gdf,
        [
            "DISTRICT",
            "DIST_NAME",
            "DISTRICT_NAME",
        ],
    )

    tehsil_col = _find_column(
        gdf,
        [
            "TEHSIL",
            "TAHSIL",
            "TEHSIL_NAME",
            "TAHSIL_NAME",
        ],
    )

    district = (
        str(row[district_col]).strip()
        if district_col
        else None
    )

    tehsil = (
        str(row[tehsil_col]).strip()
        if tehsil_col
        else None
    )

    return district, tehsil


# ============================================================
# ANALYSIS GEOMETRY
# ============================================================

def create_analysis_geometry(
    latitude: float,
    longitude: float,
    radius_m: float,
):

    if radius_m <= 0:

        raise ValueError(
            "radius_m must be greater than zero."
        )

    point = Point(
        float(longitude),
        float(latitude),
    )

    utm_zone = (
        int((longitude + 180) / 6) + 1
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

    buffered = projected_point.buffer(
        radius_m
    )

    return transform(
        to_wgs84,
        buffered
    )


# ============================================================
# COLUMN DETECTION
# ============================================================

def _find_column(
    gdf: gpd.GeoDataFrame,
    candidates: list[str],
) -> Optional[str]:

    normalized = {
        str(column).strip().upper(): column
        for column in gdf.columns
    }

    for candidate in candidates:

        key = (
            str(candidate)
            .strip()
            .upper()
        )

        if key in normalized:

            return normalized[key]

    return None
