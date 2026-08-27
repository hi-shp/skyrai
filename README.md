# SKYRAI(ไร่) — Sentinel Hub Multi-Field Precision Agriculture Platform

🛰️ **High-Precision Multi-Field Agriculture Intelligence with 10m Sentinel-2 Multispectral Satellite Data & USDA N-Rich Strip Model**

*⚡ Continuous Automated Synchronization Active (`auto_git_sync`)*

---

## 🌟 Key Features

1. **🌾 Multi-Field Management with Translucent Overlay**
   - Manage multiple farm parcels with persistent `localStorage`.
   - All registered farm fields remain visible on the satellite map as translucent boundaries (`0.15 opacity`) while the active parcel is analyzed.
   - Interactive drawing tools: 📐 Rectangle & 🔷 Freehand Polygon with 100% gapless 4-edge clipping.

2. **📡 Official Sentinel Hub OAuth2 Integration**
   - Native Sentinel-2 L2A (10m BOA reflectance: B04 Red, B05 Red-Edge, B08 NIR, B8A Narrow NIR, B11 SWIR).
   - Real-time OAuth 2.0 token management and process API caching.

3. **📊 11 Spectral & Soil Diagnostics**
   - **Vegetation & Nitrogen**: NDVI, NDRE (Red-Edge Chlorophyll/Nitrogen), EVI, LAI
   - **Moisture & Water**: NDWI (Leaf Canopy Water), Soil Moisture, Irrigation Need
   - **Soil & Crop Health**: ISRIC SoilGrids 250m Baseline (pH 6.2 Clay Loam, CEC 18.4), Growth Stress, Chlorophyll, Harvest Readiness

4. **🧠 Practical 4R Fertilizer Prescription Engine**
   - **⏰ 1. When**: Optimal application window (e.g. Early morning 06:00–08:30 after dew evaporation) and weather-based leaching/volatilization risk alerts.
   - **📍 2. Where**: Exact target deficit zones (NDRE < 0.35) with sub-pixel 10m precision and healthy zone suppression.
   - **⚖️ 3. How Much**: Crop-specific N-P-K dosages (kg/rai and g/tree) for Durian, Cassava, Rice, Mango, Sugarcane, Oil Palm.
   - **🚜 4. How**: Proper placement (e.g. canopy drip-line banding + immediate micro-sprinkler incorporation) and soil pH recommendations.

5. **🌦️ Agrometeorological Intelligence**
   - 7-day Open-Meteo weather forecast, GDD (Growing Degree Days, Tbase 10°C), and 7-day spray suitability calendar.

---

## 🚀 Getting Started

### 1. Requirements
- Python 3.8+
- Modern Web Browser (Chrome, Edge, Firefox, Safari)

### 2. Run the Server
```bash
python server.py
```
Open your browser and navigate to:
👉 **http://localhost:8000/skyrai.html**

---

## 📁 Repository Structure
- `skyrai.html`: Main single-file frontend web application with Leaflet and Chart.js.
- `server.py`: Lightweight Python server handling Sentinel Hub OAuth2 token lifecycle and serving web assets.
- `.env`: API credentials and environment configuration.
- `auto_git_sync.py`: Background synchronization daemon for automated commits and pushes.
