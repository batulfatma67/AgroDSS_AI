from datetime import datetime

import requests
import streamlit as st


OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast"
)


@st.cache_data(ttl=900)
def fetch_weather(
    latitude: float,
    longitude: float,
) -> dict:

    params = {
        "latitude": latitude,
        "longitude": longitude,

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "precipitation,"
            "rain,"
            "wind_speed_10m,"
            "weather_code"
        ),

        "hourly": (
            "temperature_2m,"
            "precipitation"
        ),

        "daily": (
            "temperature_2m_max,"
            "temperature_2m_min,"
            "precipitation_sum,"
            "rain_sum"
        ),

        "past_days": 1,
        "forecast_days": 7,

        "timezone": "auto",

        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "precipitation_unit": "mm",
    }

    response = requests.get(
        OPEN_METEO_URL,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    return response.json()


def parse_weather_response(data: dict) -> dict:

    current = data["current"]
    daily = data["daily"]

    precipitation = daily.get(
        "precipitation_sum",
        [],
    )

    rainfall_today = (
        float(precipitation[1])
        if len(precipitation) > 1
        else 0.0
    )

    rainfall_7d = sum(
        float(value or 0)
        for value in precipitation
    )

    return {
        "temperature_c": float(
            current["temperature_2m"]
        ),

        "humidity_percent": float(
            current["relative_humidity_2m"]
        ),

        "precipitation_24h_mm": float(
            current["precipitation"]
        ),

        "rainfall_today_mm": rainfall_today,

        "precipitation_7d_mm": rainfall_7d,

        "wind_speed_kmh": float(
            current["wind_speed_10m"]
        ),

        "weather_code": int(
            current["weather_code"]
        ),

        "weather_description":
            weather_code_description(
                int(current["weather_code"])
            ),

        "daily": daily,
        "hourly": data.get("hourly", {}),
        "retrieved_at": datetime.utcnow().isoformat(),
    }


def weather_code_description(code: int) -> str:

    descriptions = {

        0: "Clear sky",

        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",

        45: "Fog",
        48: "Depositing rime fog",

        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",

        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",

        71: "Slight snowfall",
        73: "Moderate snowfall",
        75: "Heavy snowfall",

        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",

        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail",
    }

    return descriptions.get(
        code,
        "Unknown weather condition",
    )
