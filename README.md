# 🛰️ InSAR-SinkWatch: NASA NISAR Millimeter-Precision Urban Subsidence & Landslide Observatory

> **Official Project for NASA International Space Apps Challenge 2026**  
> **Team Name:** `VisionSpace_UsxSgu` (Local Event: Ho Chi Minh City, Vietnam)  
> **Members:** Trần Minh Thành (`@minhthanh_tran`) & Phạm Thị Kim Ngân (`@ebnata`)  
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
# 1. Clone the repository
git clone https://github.com/ThanhTran-HCMUS/insar-sinkwatch.git
cd insar-sinkwatch

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the Streamlit Web GIS Dashboard
streamlit run app.py
```
*(On Windows, you can also simply double-click `run_app.bat` to launch instantly).*

The application will launch automatically at `http://localhost:8501`.

---

## 🌐 Alignment with NASA Open Science & Space Agency Datasets

Our project directly integrates and cites the official resources provided in the NASA Space Apps Challenge:

### NASA Data & Resources
1. **ASF Data Search Vertex (Alaska Satellite Facility):** [https://search.asf.alaska.edu/](https://search.asf.alaska.edu/) — Source for SAR SLC acquisitions and baseline queries via ASF DAAC REST API (`src/pipeline/asf_downloader.py`).
2. **NASA Earthdata Search:** [https://search.earthdata.nasa.gov/](https://search.earthdata.nasa.gov/) — Global digital elevation models (SRTM DEM 30m) for topographic phase removal.
3. **NISAR Data User Guide:** [https://nisar-docs.asf.alaska.edu/](https://nisar-docs.asf.alaska.edu/) — Technical specifications for NISAR L-band repeat-pass interferometry ($\lambda = 24.24\text{ cm}$, 12-day repeat orbit).
4. **NISAR Applications White Papers:** [https://nisar.jpl.nasa.gov/applications/overview/](https://nisar.jpl.nasa.gov/applications/overview/) — Frameworks for urban land subsidence and geotechnical hazard mapping.
5. **UAVSAR Postcards:** [https://uavsar.jpl.nasa.gov/education/postcards/](https://uavsar.jpl.nasa.gov/education/postcards/) — NASA airborne L-band polarimetric test data.

### Space Agency Partner Resources
6. **CSA Synthetic Aperture Radar python Tutorial:** [https://github.com/asc-csa/Synthetic_Aperture_Radar_Tutorial](https://github.com/asc-csa/Synthetic_Aperture_Radar_Tutorial) — Open Python & QGIS SAR processing workflows.
7. **CONAE SAOCOM Catalogue:** [https://catalog.saocom.conae.gov.ar/catalog/](https://catalog.saocom.conae.gov.ar/catalog/) — L-band SAR test products and constellation data standards.
8. **CSA Radarsat Constellation Mission (RCM) - Data:** [https://www.asc-csa.gc.ca/eng/satellites/radarsat/](https://www.asc-csa.gc.ca/eng/satellites/radarsat/) — Disaster monitoring SAR specifications.

---

## 👥 The Team: `VisionSpace_UsxSgu`
* **Trần Minh Thành (`@minhthanh_tran`)** — Team Owner & Lead AI / InSAR Pipeline Engineer: System architecture, InSAR phase-displacement algorithms, AI hotspot clustering, and 3D Web GIS engine.
* **Phạm Thị Kim Ngân (`@ebnata`)** — Geospatial Earth Scientist & Environmental Data Analyst: Geomorphological analysis, Holocene sediment lithology, groundwater depletion modeling, and policy translation.

