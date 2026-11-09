# NASA Space Apps Challenge 2026: Project Page Submission

**Team Name:** visionspace_us  
**Local Event:** Ho Chi Minh City, Vietnam  
**Challenge:** Dancing with the SARs  
**Project Title:** InSAR-SinkWatch: NASA NISAR Millimeter-Precision Urban Subsidence & Landslide Observatory  

---

### 1. High-Level Project Summary (Tagline)
An AI-powered 3D InSAR observatory leveraging NASA-ISRO NISAR L-band radar data to detect millimeter-scale land subsidence and riverbank collapse across Vietnam's sinking delta megacities.

---

### 2. Detailed Project Description

#### The Challenge & Problem Statement
Earth's surface undergoes a ceaseless waltz of subtle vertical displacement. Across the coastal megacities and low-lying deltas of Southeast Asia—most acutely in **Ho Chi Minh City** and the **Mekong River Delta**—this dance has turned perilous. The land is sinking at rates between **15 mm and 45 mm per year**, outpacing global sea-level rise by a factor of ten. Compounded by heavy urban concrete loads, uncurbed industrial groundwater pumping from Pleistocene aquifers, and thick soft Holocene mud layers, thousands of hectares face chronic tidal flooding, road fracture, and critical foundation shear stress. Concurrently, major river bends along the Mekong Delta suffer sudden riverbank collapse.

Conventional ground-survey leveling is spatially sparse, prohibitively expensive, and cannot provide continuous synoptic coverage. Optical remote sensing (Landsat, Sentinel-2) is rendered ineffective by the ubiquitous cloud and monsoon rain cover of equatorial Vietnam.

#### Our Solution: InSAR-SinkWatch
**InSAR-SinkWatch** transforms complex radar physics into actionable civil protection intelligence. Built on the revolutionary repeat-pass **Interferometric Synthetic Aperture Radar (InSAR)** technology of the **NASA-ISRO NISAR** mission, our platform:

1. **Reconstructs Millimeter-Precision Deformation Fields:** By computing the phase differential ($\Delta \phi$) of paired radar acquisitions at L-band wavelength ($\lambda = 24.24\text{ cm}$), the system quantifies line-of-sight surface displacement with millimeter accuracy: $\Delta d = \frac{\lambda}{4\pi} \Delta \phi$.
2. **Maintains High Coherence in Tropical Humid Climates:** Unlike short C-band radar that decorrelates rapidly in tropical vegetation, NISAR's long L-band wave penetrates dense canopy foliage and agricultural crops, preserving phase coherence over extended temporal baselines.
3. **Applies Adaptive InSAR Filtering & AI Hotspot Detection:** Implements Goldstein spatial phase filtering to suppress phase noise, followed by an adaptive clustering algorithm that isolates severe subsidence bowls ($< -20\text{ mm/year}$).
4. **Vulnerability Screening for Critical Civil Infrastructure:** Cross-references sinking bowls with major infrastructure assets (Bến Thành Metro Terminal, Ba Son Station & Bridge, Thủ Thiêm Under-River Tunnel, Phú Mỹ Bridge, and river dikes).
5. **Interactive 3D Mission Control & GIS Export:** Delivers an intuitive 3D Web GIS console with downward-extruding terrain meshes, interactive multi-year forward projections (2026–2036), and instant GeoJSON export for immediate integration into municipal GIS workflows (QGIS / ArcGIS).

---

### 3. How We Addressed the Challenge
The NASA challenge prompt asks participants to *"build an interactive application that uses radar remote sensing data from the NASA-ISRO Synthetic Aperture Radar (NISAR) mission to track and visualize one or more types of surface change at locations around the world."*

We addressed this challenge directly by:
* Selecting one of the most critical and difficult-to-detect types of surface change: **vertical land subsidence and geotechnical riverbank deformation**.
* Utilizing the core physics and mathematical formulation of **NISAR L-band interferometry**.
* Building a full-fledged, responsive **interactive web application** that makes esoteric radar phase fringes understandable, visual, and directly communicative to urban planners, civil engineers, and local residents.

---

### 4. NASA Data & Open Science Resources Used
* **NASA-ISRO SAR (NISAR) Mission Data Specifications:** L-band repeat-pass interferometry standards (24.24 cm wavelength, 12-day orbital repeat cycle, high spatial resolution).
* **Alaska Satellite Facility (ASF DAAC):** Open SAR processing methodologies, Single Look Complex (SLC) interferogram formation guidelines, and OpenSARLab recipes.
* **NASA Earthdata & SRTM DEM:** Digital Elevation Model (DEM) parameters used for synthetic phase reference simulation and topographic phase removal.

---

### 5. Technologies & Libraries
* **Language & Frameworks:** Python 3, Streamlit, PyDeck (Deck.GL WebGL engine)
* **Scientific Computing & Signal Processing:** NumPy, SciPy (adaptive 2D filtering), Matplotlib
* **GIS & Vector Data Standards:** GeoJSON (RFC 7946), OGC CRS:84 coordinate reference standards

---

### 6. Team Contributions
* **AI & Software Lead:** Developed InSAR phase-displacement algorithms, Goldstein phase filtering, AI subsidence hotspot detection, and 3D WebGL rendering engine.
* **Geography & Earth Science Lead:** Conducted geomorphological lithology analysis of Holocene alluvial clays, groundwater aquifer compaction modeling, infrastructure risk evaluation, and spatial narrative alignment.

