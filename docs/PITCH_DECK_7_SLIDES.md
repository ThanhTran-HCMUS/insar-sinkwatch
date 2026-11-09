# 7-Slide Pitch Deck: InSAR-SinkWatch
**Official Presentation Outline for NASA Space Apps Challenge 2026 (Max 7 Slides)**  
**Team:** visionspace_us | **Local Event:** Ho Chi Minh City, Vietnam  

---

### SLIDE 1: The Hook & Title
* **Visual:** Dark satellite background showing glowing InSAR phase fringes overlaid onto Ho Chi Minh City and the Saigon River.
* **Title:** **InSAR-SinkWatch**
* **Subtitle:** Millimeter-Precision Urban Subsidence & Geohazard Observatory powered by NASA-ISRO NISAR
* **Team:** `visionspace_us` (AI Engineering & Earth Science)
* **Speaker Script (20s):**
  > *"Distinguished judges, Earth's surface is in a constant dance of change. But in Ho Chi Minh City and the Mekong Delta, this dance has become a quiet catastrophe: the ground under our feet is sinking at up to 45 millimeters per year—10 times faster than the sea is rising. We present InSAR-SinkWatch."*

---

### SLIDE 2: The Invisible Crisis (The Problem)
* **Visual:** Split graphic: Left = Street flooding under sunny skies in District 7 (sunny-day tidal flooding). Right = Cloud-covered optical satellite image showing zero ground visibility.
* **Key Points:**
  * **Rapid Urban Subsidence:** $15\text{ to }45\text{ mm/year}$ across District 7, Nhà Bè, and Bình Chánh.
  * **The Optical Blind Spot:** Tropical storm and monsoonal cloud cover blinds optical satellites (Landsat / Sentinel-2) $80\%$ of the year.
  * **Sparsity of Ground Leveling:** Traditional surveying benchmarks are sparse, labor-intensive, and fail to provide contiguous regional coverage.
* **Speaker Script (25s):**
  > *"Why is Ho Chi Minh City drowning? It’s not just rising seas. It’s that our soft clay foundations are collapsing under heavy skyscrapers and excessive groundwater extraction. Optical satellites cannot see through our monsoon clouds, and ground sensors only measure isolated points. We needed a sensor that sees through clouds and measures millimeters from space."*

---

### SLIDE 3: The Space Solution: NASA-ISRO NISAR (L-band InSAR)
* **Visual:** Diagram of the NISAR satellite in orbit with its 12-meter deployable mesh reflector, showing 24 cm L-band waves penetrating canopy foliage to reflect off building foundations and soil.
* **Key Points:**
  * **Why NISAR L-band ($\lambda = 24.24\text{ cm}$)?** C-band decorrelates in tropical humidity and foliage. L-band penetrates vegetation to maintain high temporal coherence ($\gamma > 0.6$).
  * **Millimeter Phase Physics:** $\Delta d = \frac{\lambda}{4\pi} \Delta \phi_{\text{InSAR}}$.
  * **12-Day Orbital Repeat:** Unmatched temporal cadence for routine municipal health checks.
* **Speaker Script (25s):**
  > *"Enter NASA’s flagship NISAR mission. With its 24-centimeter L-band radar, NISAR penetrates tropical tree canopies and monsoon clouds. By comparing the phase difference between orbital passes, we measure ground movements as fine as one millimeter—the thickness of a credit card—from 747 kilometers in space."*

---

### SLIDE 4: Architecture & AI Pipeline
* **Visual:** Clean technical flowchart: Raw SLC Radar Pairs $\rightarrow$ Goldstein Phase Filter $\rightarrow$ Phase-to-Displacement $\rightarrow$ AI Hotspot Clustering $\rightarrow$ 3D Web GIS.
* **Key Points:**
  * **Goldstein Phase Filtering:** Eliminates temporal decorrelation noise while preserving sharp geotechnical fault edges.
  * **AI Hotspot Detection:** Automated spatial clustering isolating critical subsidence bowls ($< -20\text{ mm/year}$).
  * **Soil Consolidation Model:** Projects cumulative settlement forward from 2026 to 2036.
* **Speaker Script (25s):**
  > *"Our pipeline takes raw radar phase pairs, applies Goldstein filtering to strip out phase noise, converts unwrapped phase to millimeter displacement, and runs AI anomaly clustering to automatically pinpoint high-hazard subsidence bowls threatening critical municipal infrastructure."*

---

### SLIDE 5: Live Product Demo (InSAR-SinkWatch 3D Console)
* **Visual:** Screenshot / Live recording of the Streamlit 3D PyDeck console showing the 3D sinking mesh of Ho Chi Minh City and glowing infrastructure warning markers.
* **Key Points:**
  * **Interactive 3D Geospatial Visualization:** Downward terrain extrusion proportional to sinking velocity.
  * **Critical Asset Screening:** Automated vulnerability status for Bến Thành Metro Terminal, Ba Son Bridge, Phú Mỹ Bridge, and Thủ Thiêm Tunnel.
  * **One-Click Vector Export:** Instant GeoJSON download for QGIS and municipal GIS systems.
* **Speaker Script (30s):**
  > *"Here is InSAR-SinkWatch in action. Planners can explore an interactive 3D deformation mesh of Ho Chi Minh City. Red columns highlight deep subsidence bowls in District 7 sinking at 38 mm a year. The system automatically screens key civil assets—alerting engineers that Metro Line 1 stations and bridge abutments are undergoing differential settlement, and allows downloading GeoJSON files directly into QGIS."*

---

### SLIDE 6: Scientific Depth & Ground-Truth Validation
* **Visual:** Geomorphological soil profile map: Holocene soft organic mud layer ($15-30\text{m}$) over Pleistocene sand aquifers, correlated with groundwater extraction well density.
* **Key Points:**
  * **Domain Expertise:** High correlation between soft Holocene alluvial clay distribution and InSAR subsidence hotspots.
  * **Actionable Urban Policy:** Provides empirical evidence to enforce bans on deep groundwater extraction and adjust building foundation codes.
  * **Riverbank Landslide Early Warning:** Detecting tensile creep along outer bends of the Mekong River before catastrophic collapse.
* **Speaker Script (25s):**
  > *"Our geography analysis confirms that our radar hotspots perfectly align with 30-meter thick soft Holocene clay layers and heavy industrial groundwater wells. InSAR-SinkWatch gives city authorities the definitive scientific evidence needed to halt groundwater over-extraction and save billions in structural repairs."*

---

### SLIDE 7: The Team & Global Impact
* **Visual:** Team photos / icons representing Computer Science/AI + Geography/Earth Science, accompanied by a world map showing other vulnerable mega-deltas (Jakarta, Bangkok, Dhaka, New Orleans).
* **Key Points:**
  * **Team `visionspace_us`:** A multidisciplinary synergy of AI Engineering and Geospatial Earth Science.
  * **Global Scalability:** 100% open-source pipeline ready to deploy across any delta megacity worldwide using open NASA NISAR data.
  * **Call to Action:** Transforming NASA space science into community resilience.
* **Speaker Script (20s):**
  > *"We are team visionspace_us—combining AI engineering and Earth science. InSAR-SinkWatch proves that NASA's open radar data can protect vulnerable delta cities across the globe. Thank you, and we welcome your questions!"*

