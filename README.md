# 🛰️ InSAR-SinkWatch: NASA NISAR Millimeter-Precision Urban Subsidence & Landslide Observatory

> **Official Project for NASA International Space Apps Challenge 2026**  
> **Team Name:** `visionspace_us` (Local Event: Ho Chi Minh City, Vietnam)  
> **Challenge:** *Dancing with the SARs (Tracking Earth's Surface Dynamics via Radar Remote Sensing)*  
> **Target Mission:** **NASA-ISRO Synthetic Aperture Radar (NISAR)**

---

## 🌍 Executive Summary

Earth's surface is engaged in an intricate, continuous dance of deformation. In major coastal mega-deltas like **Ho Chi Minh City** and the **Mekong River basin (Vietnam)**, the ground is subsiding at an alarming velocity of **$15\text{ to }45\text{ mm/year}$**—sinking **5 to 10 times faster than climate-induced sea-level rise**. Meanwhile, outer concave riverbanks along the Mekong River suffer abrupt collapse, destroying homes and vital infrastructure.

Because optical satellites (Landsat, Sentinel-2) are blinded by the perennial tropical cloud cover, and traditional ground leveling stations are sparse and costly, these critical geohazards often remain invisible until catastrophic failure occurs.

**`InSAR-SinkWatch`** is an end-to-end AI-powered geospatial observatory that harnesses the revolutionary **L-band repeat-pass Interferometric Synthetic Aperture Radar (InSAR)** from the **NASA-ISRO NISAR** mission. By processing the phase difference of radar pulses ($\lambda = 24.24\text{ cm}$), the system reconstructs vertical millimeter-scale surface displacement fields, automatically detects critical subsidence bowls using AI spatial clustering, screens civil infrastructure vulnerability (Metro Line 1 & 2, bridges, ports), and provides an interactive 3D Web GIS dashboard for disaster mitigation and urban adaptation.

---

## 🚀 Key Features

* **Millimeter-Precision InSAR Phase Unwrapping:** Converts radar phase cycles into vertical ground deformation: $\Delta d = \frac{\lambda}{4\pi} \Delta \phi$.
* **Goldstein Adaptive InSAR Filter:** Preserves phase fringe sharpness while suppressing temporal decorrelation noise over dense urban and vegetated terrains.
* **AI Subsidence Hotspot Detection:** Automated spatial clustering and anomaly identification isolating critical subsidence bowls ($< -20\text{ mm/year}$).
* **3D Geospatial Extrusion (PyDeck / Deck.GL):** Real-time interactive 3D mesh visualizing land sinking bowls with illuminated status markers on critical civil assets.
* **Geotechnical Forward Forecasting (2026 - 2036):** Forward multi-year soil consolidation model projecting cumulative vertical displacement.
* **Open GIS Interoperability:** One-click export of GeoJSON vector datasets compatible with QGIS, ArcGIS, and Google Earth.

---

## 🔬 System Architecture

```
┌───────────────────────────────────────────────────────────┐
│       NASA-ISRO NISAR (L-band SAR: λ = 24.24 cm)          │
│       Alaska Satellite Facility (ASF DAAC) / Earthdata    │
└─────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────┐
│ 1. InSAR PHASE PROCESSING PIPELINE                        │
│    - Complex Interferogram Generation: I = M · S*         │
│    - Goldstein Adaptive Phase Filtering                   │
│    - Phase-to-Displacement Conversion (Δd = λ/4π · Δφ)    │
└─────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────┐
│ 2. AI GEOTECHNICAL ANALYTICS & HOTSPOT DETECTOR           │
│    - Spatial Anomaly Detection (Critical: < -20 mm/year)  │
│    - Soil Compaction Consolidation Forecasting (10-Year)  │
│    - Vulnerability Screening for Critical Infrastructure  │
└─────────────────────────────┬─────────────────────────────┘
                              │
                              ▼
┌───────────────────────────────────────────────────────────┐
│ 3. 3D INTERACTIVE WEB GIS MISSION CONTROL (Streamlit)     │
│    - PyDeck 3D Surface Displacement Mesh                  │
│    - Multi-temporal Fringe & Velocity Visualizer          │
│    - Infrastructure Vulnerability Matrix                  │
│    - Standard GeoJSON & Executive Briefing Exporter       │
└───────────────────────────────────────────────────────────┘
```

---

## 🛠️ Installation & Quickstart

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Core dependencies: `streamlit`, `pydeck`, `numpy`, `pandas`, `matplotlib`

### Running the Application Locally
```bash
# Clone the repository
git clone https://github.com/visionspace-us/InSAR-SinkWatch.git
cd InSAR-SinkWatch

# Launch the Streamlit Web GIS Dashboard
streamlit run app.py
```

The application will launch automatically at `http://localhost:8501`.

---

## 🌐 Alignment with NASA Open Science & Datasets

1. **NISAR (NASA-ISRO Synthetic Aperture Radar):** Simulated and calibrated against NISAR L-band repeat-pass interferometry specifications (12-day repeat orbit, 24 cm wavelength).
2. **Alaska Satellite Facility (ASF DAAC):** Leveraging open SAR data standards (SLC, InSAR unwrapped phase rasters).
3. **NASA Earthdata:** Integrating open digital elevation models (SRTM / Copernicus DEM) for topographic phase removal.

---

## 👥 The Team: `visionspace_us`
* **Lead AI & Software Engineer:** Architecture, InSAR phase-displacement algorithms, AI hotspot clustering, and 3D Web GIS engine.
* **Lead Geographer & Earth Scientist:** Geomorphological analysis, Holocene sediment lithology, groundwater depletion modeling, and policy translation.

