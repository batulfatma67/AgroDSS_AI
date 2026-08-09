import json
from datetime import date

import ee
import streamlit as st


COLLECTION_ID = (
    "COPERNICUS/S2_SR_HARMONIZED"
)


def initialize_earth_engine() -> None:

    service_account = st.secrets.get(
        "GEE_SERVICE_ACCOUNT"
    )

    if not service_account:
        raise RuntimeError(
            "GEE_SERVICE_ACCOUNT is missing "
            "from Streamlit secrets."
        )

    credentials = ee.ServiceAccountCredentials(
        service_account["client_email"],
        key_data=json.dumps(
            dict(service_account)
        ),
    )

    ee.Initialize(
        credentials=credentials,
        project=service_account["project_id"],
    )


def get_ndvi_analysis(
    geometry,
    start_date: date,
    end_date: date,
) -> dict:

    initialize_earth_engine()

    ee_geometry = ee.Geometry(
        geometry.__geo_interface__
    )

    collection = (
        ee.ImageCollection(COLLECTION_ID)
        .filterBounds(ee_geometry)
        .filterDate(
            start_date.isoformat(),
            end_date.isoformat(),
        )
        .filter(
            ee.Filter.lt(
                "CLOUDY_PIXEL_PERCENTAGE",
                20,
            )
        )
    )

    image_count = collection.size().getInfo()

    if image_count == 0:
        raise RuntimeError(
            "No suitable Sentinel-2 images were "
            "found for the selected period."
        )

    def mask_clouds(image):

        qa = image.select("QA60")

        cloud_bit = 1 << 10
        cirrus_bit = 1 << 11

        mask = (
            qa.bitwiseAnd(cloud_bit)
            .eq(0)
            .And(
                qa.bitwiseAnd(cirrus_bit)
                .eq(0)
            )
        )

        return (
            image
            .updateMask(mask)
            .divide(10000)
        )

    processed = collection.map(mask_clouds)

    composite = processed.median()

    ndvi = (
        composite
        .normalizedDifference(
            ["B8", "B4"]
        )
        .rename("NDVI")
    )

    stats = ndvi.reduceRegion(
        reducer=ee.Reducer.mean()
            .combine(
                reducer2=ee.Reducer.min(),
                sharedInputs=True,
            )
            .combine(
                reducer2=ee.Reducer.max(),
                sharedInputs=True,
            ),

        geometry=ee_geometry,

        scale=10,

        maxPixels=1_000_000,
    ).getInfo()

    return {
        "image": ndvi.clip(ee_geometry),

        "mean_ndvi": stats.get(
            "NDVI_mean"
        ),

        "minimum_ndvi": stats.get(
            "NDVI_min"
        ),

        "maximum_ndvi": stats.get(
            "NDVI_max"
        ),

        "image_count": image_count,

        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
    }


def get_ndvi_tile_url(image) -> str:

    visualization = {
        "min": -0.2,
        "max": 0.8,

        "palette": [
            "8b0000",
            "ff4d4d",
            "ffff66",
            "66cc66",
            "006400",
        ],
    }

    map_id = image.getMapId(
        visualization
    )

    return map_id[
        "tile_fetcher"
    ].url_format
