"""
InSAR Geotechnical Analytics & GIS Vector Export
Calculates spatial deformation area, land settlement volume,
and generates geo-referenced GeoJSON for urban planning in QGIS / ArcGIS.
"""

import json
import numpy as np

def calculate_geotechnical_impact(
    hotspot_results: dict,
    velocity_map: np.ndarray,
    pixel_spacing_meters: float = 20.0,
    urban_population_density: float = 4200.0
) -> dict:
    """
    Computes geotechnical metrics and urban risk indicators.
    """
    pixel_area_m2 = pixel_spacing_meters * pixel_spacing_meters
    m2_to_km2 = 1e-6
    
    crit_px = hotspot_results["critical_pixels"]
    mod_px = hotspot_results["moderate_pixels"]
    
    crit_area_km2 = float(crit_px * pixel_area_m2 * m2_to_km2)
    mod_area_km2 = float(mod_px * pixel_area_m2 * m2_to_km2)
    total_sinking_km2 = crit_area_km2 + mod_area_km2
    
    # Calculate volumetric sediment compaction (m³ per year)
    # Volume = Integral of (vertical velocity in meters * pixel area)
    sinking_mask = velocity_map < -10.0
    sinking_velocities_m = np.abs(velocity_map[sinking_mask]) * 1e-3  # mm to meters
    annual_volume_loss_m3 = float(np.sum(sinking_velocities_m) * pixel_area_m2)
    
    # Population exposed in critical subsidence bowl
    pop_at_risk = int(crit_area_km2 * urban_population_density)
    
    if crit_area_km2 > 15:
        threat_level = "TIER 1 EMERGENCY: Accelerated Subsidence"
        threat_color = "#FF1744"
    elif crit_area_km2 > 5:
        threat_level = "TIER 2 ALERT: High Geotechnical Risk"
        threat_color = "#FF9100"
    else:
        threat_level = "TIER 3: Controlled / Moderate Settlement"
        threat_color = "#FFD600"
        
    return {
        "critical_subsidence_area_km2": round(crit_area_km2, 2),
        "moderate_subsidence_area_km2": round(mod_area_km2, 2),
        "total_impacted_urban_area_km2": round(total_sinking_km2, 2),
        "annual_sediment_loss_million_m3": round(annual_volume_loss_m3 / 1e6, 3),
        "estimated_urban_population_at_risk": pop_at_risk,
        "max_sinking_velocity": hotspot_results["max_subsidence_rate_mm_year"],
        "threat_level": threat_level,
        "threat_color": threat_color
    }

def export_insar_geojson(
    velocity_map: np.ndarray,
    bounds: tuple,
    poi_list: list,
    sample_step: int = 5
) -> str:
    """
    Exports subsidence deformation points and critical infrastructure POIs
    as a standard GeoJSON FeatureCollection.
    """
    min_lon, min_lat, max_lon, max_lat = bounds
    h, w = velocity_map.shape
    
    features = []
    
    # 1. Add Infrastructure POIs
    for poi in poi_list:
        features.append({
            "type": "Feature",
            "properties": {
                "name": poi["name"],
                "type": poi["type"],
                "risk_level": poi.get("risk_level", "Unknown"),
                "marker_symbol": "critical_infrastructure"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [poi["lon"], poi["lat"]]
            }
        })
        
    # 2. Add Subsidence Hotspot sample polygons
    crit_indices = np.argwhere(velocity_map < -20.0)
    if len(crit_indices) > 0:
        sampled = crit_indices[::sample_step]
        for r, c in sampled[:50]:
            lat = max_lat - (r / h) * (max_lat - min_lat)
            lon = min_lon + (c / w) * (max_lon - min_lon)
            vel = float(velocity_map[r, c])
            
            d_lon = (max_lon - min_lon) / w * sample_step * 0.5
            d_lat = (max_lat - min_lat) / h * sample_step * 0.5
            
            poly = [
                [
                    [round(lon - d_lon, 5), round(lat + d_lat, 5)],
                    [round(lon + d_lon, 5), round(lat + d_lat, 5)],
                    [round(lon + d_lon, 5), round(lat - d_lat, 5)],
                    [round(lon - d_lon, 5), round(lat - d_lat, 5)],
                    [round(lon - d_lon, 5), round(lat + d_lat, 5)]
                ]
            ]
            
            features.append({
                "type": "Feature",
                "properties": {
                    "subsidence_rate_mm_year": round(vel, 1),
                    "severity": "CRITICAL",
                    "satellite_source": "NASA-ISRO NISAR L-band InSAR"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": poly
                }
            })
            
    geojson_out = {
        "type": "FeatureCollection",
        "name": "NISAR_Urban_Subsidence_InSAR",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": features
    }
    return json.dumps(geojson_out, indent=2)

