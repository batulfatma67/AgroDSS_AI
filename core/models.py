from dataclasses import dataclass
from datetime import date
from typing import Optional


@dataclass
class FarmData:
    latitude: float
    longitude: float

    crop: str
    area_acres: float
    irrigation_type: str

    analysis_radius_m: float

    district: Optional[str] = None
    tehsil: Optional[str] = None

    analysis_start: Optional[date] = None
    analysis_end: Optional[date] = None


@dataclass
class WeatherData:
    temperature_c: float
    humidity_percent: float
    rainfall_today_mm: float

    precipitation_24h_mm: float
    precipitation_7d_mm: float

    wind_speed_kmh: float
    weather_description: str

    forecast: Optional[list] = None


@dataclass
class NDVIResult:
    mean_ndvi: Optional[float]
    minimum_ndvi: Optional[float]
    maximum_ndvi: Optional[float]

    image_count: int

    observation_start: str
    observation_end: str

    status: str


@dataclass
class AnalysisResults:
    farm: FarmData
    weather: WeatherData
    ndvi: NDVIResult
