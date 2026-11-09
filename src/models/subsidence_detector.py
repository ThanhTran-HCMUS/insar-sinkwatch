"""
AI-Driven Ground Subsidence Anomaly Detector & Forecasting Engine
Detects critical subsidence bowls, classifies geotechnical risk,
and projects cumulative vertical ground displacement for 2026-2035.
"""

import numpy as np

def detect_subsidence_hotspots(
    velocity_map_mm_year: np.ndarray,
    critical_threshold_mm: float = -20.0,
    moderate_threshold_mm: float = -10.0
) -> dict:
    """
    Identifies zones experiencing alarming rates of vertical land subsidence.
    Negative values indicate downward displacement (sinking).
    
    Risk Tiers:
    - Tier 3 (CRITICAL / SEVERE): Subsidence rate < -20 mm/year (e.g., -35 mm/year)
    - Tier 2 (MODERATE RISK): -20 mm/year <= rate < -10 mm/year
    - Tier 1 (STABLE / LOW): rate >= -10 mm/year
    """
    critical_mask = velocity_map_mm_year < critical_threshold_mm
    moderate_mask = (velocity_map_mm_year <= moderate_threshold_mm) & (~critical_mask)
    stable_mask = velocity_map_mm_year > moderate_threshold_mm
    
    # Severity classification map: 0 = Stable, 1 = Moderate, 2 = Critical
    classification_map = np.zeros(velocity_map_mm_year.shape, dtype=np.uint8)
    classification_map[moderate_mask] = 1
    classification_map[critical_mask] = 2
    
    total_area_px = velocity_map_mm_year.size
    critical_area_px = int(np.sum(critical_mask))
    moderate_area_px = int(np.sum(moderate_mask))
    
    max_subsidence = float(np.min(velocity_map_mm_year))
    mean_subsidence = float(np.mean(velocity_map_mm_year))
    
    return {
        "classification_map": classification_map,
        "critical_mask": critical_mask,
        "moderate_mask": moderate_mask,
        "critical_pixels": critical_area_px,
        "moderate_pixels": moderate_area_px,
        "total_pixels": total_area_px,
        "max_subsidence_rate_mm_year": round(max_subsidence, 1),
        "mean_subsidence_rate_mm_year": round(mean_subsidence, 1)
    }

def project_cumulative_subsidence(
    velocity_map_mm_year: np.ndarray,
    forecast_years: int = 5,
    consolidation_damping: float = 0.98
) -> np.ndarray:
    """
    Projects cumulative millimeter displacement over future years
    using soil compaction consolidation model.
    """
    # Cumulative displacement: S(t) = Sum_{k=1}^T (v * damping^k)
    cumulative = np.zeros_like(velocity_map_mm_year, dtype=np.float32)
    for year in range(1, forecast_years + 1):
        rate = velocity_map_mm_year * (consolidation_damping ** (year - 1))
        cumulative += rate
    return cumulative

def assess_infrastructure_vulnerability(
    critical_mask: np.ndarray,
    bounds: tuple,
    poi_list: list
) -> list:
    """
    Cross-references critical subsidence hotspots against key civil infrastructure:
    Metro Line 1/2, major bridges, high-density residential towers, and river dykes.
    """
    min_lon, min_lat, max_lon, max_lat = bounds
    h, w = critical_mask.shape
    
    analyzed_poi = []
    for poi in poi_list:
        p_lat, p_lon = poi["lat"], poi["lon"]
        # Pixel coordinates
        r = int(np.clip((max_lat - p_lat) / (max_lat - min_lat) * h, 0, h - 1))
        c = int(np.clip((p_lon - min_lon) / (max_lon - min_lon) * w, 0, w - 1))
        
        # Local window to detect nearby ground instability
        window_r1 = max(0, r - 3)
        window_r2 = min(h, r + 4)
        window_c1 = max(0, c - 3)
        window_c2 = min(w, c + 4)
        
        local_critical = critical_mask[window_r1:window_r2, window_c1:window_c2]
        is_at_risk = bool(np.any(local_critical))
        risk_level = "CRITICAL" if is_at_risk else "LOW"
        
        analyzed_poi.append({
            "name": poi["name"],
            "type": poi["type"],
            "lat": p_lat,
            "lon": p_lon,
            "risk_level": risk_level,
            "alert_color": "#FF1744" if is_at_risk else "#00E676"
        })
    return analyzed_poi

