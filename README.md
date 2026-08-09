# AgroDSS_AI
# 🌾 AgriDSS AI

## AI-Powered Agricultural Decision Support System

**AgriDSS AI** is a geospatial agricultural decision-support application designed to combine **GIS, satellite remote sensing, weather intelligence, and explainable analytical rules** to provide field-specific agricultural insights.

The system uses an **exact geographic coordinate as the primary field location**, rather than relying only on city, district, or tehsil names. Satellite-derived vegetation information and location-specific weather conditions are then combined to assess the current field condition and generate contextual recommendations.

> **Project focus:** Precision Agriculture · GIS · Remote Sensing · Environmental Data · Agricultural Intelligence · Decision Support

---

## 📌 Project Overview

Traditional agricultural decision-making often depends on generalized information at the district or city level. Such information may not represent the actual conditions of an individual field.

AgriDSS AI addresses this limitation by allowing the user to select the **exact farm coordinate** on an interactive street map.

The application then:

1. Identifies the geographic coordinates of the selected field.
2. Determines the corresponding administrative location.
3. Defines a spatial analysis region around the selected coordinate.
4. Retrieves satellite imagery for the analysis period.
5. Calculates vegetation condition using **NDVI**.
6. Retrieves location-specific weather information.
7. Combines environmental indicators into an interpretable field assessment.
8. Produces agricultural decision-support recommendations.
9. Generates a structured PDF report containing the analysis and field location map.

---

# 🎯 Objectives

The main objectives of AgriDSS AI are to:

* Develop a practical Python-based agricultural decision-support application.
* Integrate GIS and remote-sensing data into a single workflow.
* Use geographic coordinates for more precise field-level analysis.
* Retrieve vegetation information from Sentinel-2 satellite imagery.
* Calculate and interpret the Normalized Difference Vegetation Index (NDVI).
* Integrate location-specific weather information.
* Identify potential vegetation and environmental stress indicators.
* Generate explainable agricultural recommendations.
* Produce a professional, reproducible field assessment report.
* Demonstrate the application of Python in precision agriculture and environmental intelligence.

---

# 🧠 System Architecture

The application follows a modular architecture separating the user interface, analytical logic, external data services, GIS processing, and reporting components.

```text
                    ┌─────────────────────┐
                    │     Farm Input      │
                    │                     │
                    │ Coordinate          │
                    │ Crop                │
                    │ Area                │
                    │ Irrigation          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     GIS Service     │
                    │                     │
                    │ Point Location      │
                    │ Administrative      │
                    │ Boundary Detection  │
                    │ Analysis Geometry   │
                    └──────────┬──────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
     ┌─────────────────────┐       ┌─────────────────────┐
     │ Satellite Service   │       │  Weather Service    │
     │                     │       │                     │
     │ Sentinel-2          │       │ Temperature         │
     │ Cloud Filtering     │       │ Humidity            │
     │ NDVI                │       │ Rainfall            │
     │ Spatial Statistics  │       │ Wind                │
     └──────────┬──────────┘       └──────────┬──────────┘
                │                             │
                └──────────────┬──────────────┘
                               ▼
                    ┌─────────────────────┐
                    │   Analysis Engine   │
                    │                     │
                    │ NDVI Classification │
                    │ Environmental Risk  │
                    │ Field Assessment    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Recommendation      │
                    │ Engine              │
                    │                     │
                    │ Alerts              │
                    │ Observations        │
                    │ Recommended Actions │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Report Generation   │
                    │                     │
                    │ Tables              │
                    │ Analysis            │
                    │ Recommendations     │
                    │ Farm Map            │
                    └─────────────────────┘
```

---

# 🖥️ Application Workflow

The application is organized into four main sections.

## 1. Farm Data Input

The user provides:

* Exact latitude
* Exact longitude
* Crop type
* Farm area
* Irrigation system
* Satellite analysis radius

The location can be entered manually or selected directly from the interactive map.

The selected coordinate becomes the **primary spatial reference** for the analysis.

The system subsequently attempts to identify the corresponding:

* District
* Tehsil

from the supplied administrative boundary dataset.

---

## 2. Agricultural Intelligence Dashboard

The dashboard presents the results of the environmental analysis in one location.

### Satellite indicators

* Mean NDVI
* Minimum NDVI
* Maximum NDVI
* Number of satellite observations
* Analysis period
* Interactive NDVI map

### Weather indicators

* Current temperature
* Relative humidity
* Recent precipitation
* Rainfall
* Wind speed
* Weather condition
* Short-term weather information

### Spatial information

The dashboard displays:

* Exact farm coordinate
* OpenStreetMap street context
* Analysis region
* Sentinel-2 NDVI layer

---

## 3. Field-Specific Recommendation

The recommendation engine interprets the available indicators and generates contextual decision-support information.

The system can identify situations such as:

* Very low vegetation activity
* Low vegetation activity
* Moderate vegetation condition
* Healthy vegetation
* High temperature conditions
* Low atmospheric humidity
* Low recent precipitation
* Potential water-stress conditions

Recommendations are deliberately designed as **decision support rather than automated agronomic prescriptions**.

For example, low NDVI may trigger a recommendation to inspect the field for:

* Water stress
* Crop damage
* Poor establishment
* Pest pressure
* Bare soil
* Other field-level causes

The system does not claim that NDVI alone can determine fertilizer requirements.

---

# 🛰️ Remote Sensing Methodology

AgriDSS AI uses Sentinel-2 Surface Reflectance imagery through Google Earth Engine.

The vegetation index is calculated using the standard NDVI formulation:

[
NDVI = \frac{NIR - Red}{NIR + Red}
]

For Sentinel-2:

* **NIR:** Band 8
* **Red:** Band 4

The application uses a spatial analysis region around the selected field coordinate and calculates summary statistics including:

* Mean NDVI
* Minimum NDVI
* Maximum NDVI

The application also applies cloud-related filtering before generating the vegetation composite.

---

# 📍 Coordinate-Based Analysis

A major design decision in AgriDSS AI is the use of **geographic coordinates instead of administrative names as the primary field reference**.

Instead of assuming:

```text
City → Shahkot → entire area
```

the application works with:

```text
Latitude  → 31.xxxxxx
Longitude → 73.xxxxxx
```

This provides a much more precise geographic reference for environmental data retrieval.

Administrative information such as district and tehsil is treated as **derived metadata**, rather than the primary spatial identifier.

---

# 🗺️ GIS Processing

The GIS subsystem uses:

* GeoPandas
* Shapely
* PyProj

The application performs:

1. Shapefile loading
2. Coordinate reference system validation
3. Coordinate transformation
4. Point-in-polygon administrative identification
5. Spatial buffering
6. Analysis region generation
7. Interactive map visualization

Metric buffering is performed in a projected coordinate system rather than directly in geographic latitude/longitude coordinates.

This avoids treating degrees as if they were constant-distance units.

---

# 🌦️ Weather Data

The application retrieves weather information based directly on the selected geographic coordinate.

The weather component provides information such as:

* Temperature
* Relative humidity
* Precipitation
* Rainfall
* Wind speed
* Weather condition
* Short-term forecast information

Weather information is used as an environmental indicator alongside satellite vegetation information.

---

# 🤖 Decision-Support Engine

The current recommendation engine is intentionally **explainable and rule-based**.

Rather than presenting an opaque prediction, the system identifies the environmental conditions contributing to the recommendation.

For example:

```text
Low NDVI
    +
High Temperature
    +
Low Recent Rainfall
    ↓
Potential Water Stress
    ↓
Inspect Soil Moisture
    ↓
Evaluate Irrigation Requirement
```

This approach makes the reasoning behind recommendations transparent.

---

# 📊 Risk Assessment

AgriDSS AI calculates an environmental risk score using multiple indicators.

Example factors include:

* Vegetation condition
* Temperature stress
* Atmospheric humidity
* Recent precipitation

The resulting score is interpreted into categories such as:

```text
Low Risk
Moderate Risk
High Risk
```

The score is intended as a **decision-support indicator**, not as a scientifically validated disease or yield prediction model.

---

# 📄 Automated Reporting

The application generates a structured PDF report containing information from the complete analysis workflow.

The report includes:

### Farm information

* Coordinates
* Crop
* Farm area
* Irrigation system
* District
* Tehsil

### Satellite analysis

* Mean NDVI
* Minimum NDVI
* Maximum NDVI
* Observation period
* Number of satellite scenes

### Weather analysis

* Temperature
* Humidity
* Rainfall
* Wind speed
* Weather condition

### Decision support

* Field observations
* Priority alerts
* Recommended actions

### Map

A static farm-location map is embedded into the report.

---

# 🧱 Project Structure

```text
AgriDSS_AI/
│
├── agriDSS_app.py
├── README.md
├── requirements.txt
├── .gitignore
│
├── .streamlit/
│   └── config.toml
│
├── data/
│   ├── pakistan_district.*
│   └── pakistan_tehsil.*
│
├── core/
│   ├── __init__.py
│   ├── models.py
│   ├── analysis.py
│   └── recommendations.py
│
├── services/
│   ├── __init__.py
│   ├── gis_service.py
│   ├── weather_service.py
│   ├── ndvi_service.py
│   ├── map_service.py
│   └── report_service.py
│
├── ui/
│   ├── __init__.py
│   ├── input_page.py
│   ├── dashboard_page.py
│   ├── recommendation_page.py
│   └── report_page.py
│
└── styles/
    └── main.css
```

---

# 🛠️ Technology Stack

| Category                  | Technology                |
| ------------------------- | ------------------------- |
| Programming Language      | Python                    |
| Application Framework     | Streamlit                 |
| Geospatial Processing     | GeoPandas                 |
| Geometry Operations       | Shapely                   |
| Coordinate Transformation | PyProj                    |
| Interactive Mapping       | Folium                    |
| Map Integration           | Streamlit-Folium          |
| Satellite Data            | Sentinel-2                |
| Satellite Processing      | Google Earth Engine       |
| Weather Data              | Open-Meteo                |
| Numerical Analysis        | NumPy                     |
| Data Processing           | Pandas                    |
| PDF Reporting             | ReportLab                 |
| Version Control           | Git                       |
| Repository                | GitHub                    |
| Deployment                | Streamlit Community Cloud |

---

# 🔐 Security and Secrets Management

API credentials and service-account credentials must **never be committed to the Git repository**.

Local development uses:

```text
.streamlit/secrets.toml
```

This file must be included in `.gitignore`.

Example:

```text
# Streamlit secrets
.streamlit/secrets.toml
```

The repository should contain only non-sensitive configuration and source code.

For Streamlit Community Cloud, secrets should be configured through the application's Secrets settings rather than committed to GitHub.

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/<your-username>/AgriDSS_AI.git
```

## 2. Enter the project directory

```bash
cd AgriDSS_AI
```

## 3. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate it:

```bash
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. Install dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure secrets

Create:

```text
.streamlit/secrets.toml
```

and add the required Google Earth Engine service-account configuration.

**Never commit this file.**

## 6. Run the application

Run from the project root:

```bash
streamlit run agriDSS_app.py
```

---

# ☁️ Deployment

The application is designed for deployment through Streamlit Community Cloud.

The deployment workflow connects the GitHub repository to Streamlit Community Cloud and specifies:

```text
Entrypoint:
agriDSS_app.py
```

The application dependencies are declared in:

```text
requirements.txt
```

Secrets are configured separately through the deployment platform.

---

# 🔬 Scientific Limitations

AgriDSS AI is a decision-support prototype and should not be interpreted as a replacement for field agronomic assessment.

Important limitations include:

### NDVI limitations

NDVI can indicate vegetation condition but does not uniquely identify the cause of vegetation stress.

Low NDVI can result from:

* Water stress
* Nutrient deficiency
* Pest or disease damage
* Crop growth stage
* Bare soil
* Harvesting
* Cloud contamination
* Other environmental conditions

### Spatial resolution

A highly precise GPS coordinate does not mean that the satellite measurement has the same spatial precision.

The spatial resolution of the satellite data and the selected analysis region must always be considered when interpreting results.

### Fertilizer recommendations

NDVI alone is not sufficient for determining fertilizer type or application rate.

Reliable nutrient recommendations require additional information such as:

* Soil analysis
* Crop growth stage
* Nutrient status
* Crop-specific requirements
* Local agronomic conditions

### Risk score

The current risk score is an explainable analytical indicator and has not yet been presented as a statistically validated crop-risk model.

---

# 🔮 Future Development

The current system provides the foundation for a more advanced agricultural intelligence platform.

Planned research-oriented extensions include:

## 1. Temporal NDVI Analysis

Instead of analyzing only a single composite:

```text
NDVI₁ → NDVI₂ → NDVI₃ → ... → NDVIₙ
```

The system can identify:

* Vegetation trends
* Sudden declines
* Seasonal patterns
* NDVI anomalies
* Crop-development trajectories

---

## 2. Soil Moisture Integration

Integrating satellite or modeled soil-moisture information could improve water-stress assessment.

Potential workflow:

```text
NDVI
+
Soil Moisture
+
Temperature
+
Rainfall
+
ET₀
↓
Water Stress Assessment
```

---

## 3. Evapotranspiration

Future versions can incorporate reference evapotranspiration and crop water demand.

This would enable more scientifically meaningful irrigation decision support.

---

## 4. Machine Learning

A future version can introduce a trained machine-learning model using historical field observations.

Potential inputs include:

```text
NDVI
NDVI Trend
Temperature
Rainfall
Humidity
Soil Moisture
ET₀
Crop Type
Growth Stage
Irrigation System
```

Potential outputs:

```text
Crop Stress Probability
Water-Stress Risk
Irrigation Requirement
```

Candidate models include:

* Random Forest
* Gradient Boosting
* XGBoost
* Explainable ML methods

---

## 5. Field Boundary Upload

Future versions can allow users to upload an actual farm boundary:

```text
Shapefile
GeoJSON
KML
```

This would replace the circular analysis buffer with the actual agricultural field polygon.

---

## 6. Crop-Specific Models

Different crops have different phenological cycles and vegetation characteristics.

Future versions can incorporate crop-specific:

* NDVI thresholds
* Growth stages
* Water requirements
* Temperature sensitivity
* Stress indicators

---

# 🎓 Research and Educational Value

AgriDSS AI is designed as more than a graphical demonstration.

The project brings together several areas of computational science:

```text
Python
   +
GIS
   +
Remote Sensing
   +
Environmental Data
   +
Spatial Analysis
   +
Decision Support
   +
Scientific Computing
```

The architecture is intentionally modular so that individual components can later be replaced with more advanced scientific models without rewriting the entire application.

---

# 👩‍💻 Author

**Batool Fatima**

Agricultural Engineer · Data Analyst · GIS & Remote Sensing Analyst

Areas of interest:

* Precision Agriculture
* Climate Data Science
* GIS & Remote Sensing
* Environmental Modeling
* Agricultural Intelligence
* Python for Scientific Computing
* Machine Learning
* Climate-Resilient Agriculture

---

# 📜 License

This project is intended for educational, research, and demonstration purposes.

A formal open-source license can be added when the project is prepared for public distribution.

---

# ⚠️ Disclaimer

AgriDSS AI provides environmental indicators and decision-support information based on available satellite, weather, and spatial data.

The recommendations should not be considered a substitute for professional agronomic diagnosis, soil testing, irrigation measurement, or field inspection.

Users should verify critical agricultural decisions using field observations and appropriate agronomic expertise.

---

## Project Vision

> **From location-based agricultural information to coordinate-driven, satellite-informed field intelligence.**

AgriDSS AI aims to provide a foundation for integrating geospatial data, Earth observation, environmental information, and machine learning into practical agricultural decision-support systems.

