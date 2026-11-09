"""
Impact Analytics & GIS Export Module
- Translates pixel statistics into physical area units (km², Hectares)
- Evaluates damage risk score and agricultural exposure
- Generates downloadable GeoJSON polygons for GIS integration (QGIS / ArcGIS / Leaflet)
"""

import json
import numpy as np

def calculate_impact_metrics(
    detection_results: dict,
    pixel_spacing_meters: float = 10.0,
    estimated_pop_density_per_km2: float = 450.0,
    agri_fraction: float = 0.65
) -> dict:
    """
    Computes real-world socioeconomic and spatial impact metrics.
    
    Parameters:
    - detection_results: Output from detect_surface_inundation.
    - pixel_spacing_meters: Ground sampling distance (e.g., 10m for Sentinel-1 / NISAR High-Res).
    - estimated_pop_density_per_km2: Regional population density (Mekong Delta avg ~450 people/km²).
    - agri_fraction: Percentage of rural land allocated to rice/aquaculture (~65%).
    """
    pixel_area_m2 = pixel_spacing_meters * pixel_spacing_meters
    m2_to_km2 = 1e-6
    m2_to_hectare = 1e-4
    
    new_flood_px = detection_results["new_flood_pixels"]
    flooded_veg_px = detection_results["flooded_vegetation_pixels"]
    total_inundated_px = new_flood_px + flooded_veg_px
    
    flood_area_km2 = float(new_flood_px * pixel_area_m2 * m2_to_km2)
    flood_area_ha = float(new_flood_px * pixel_area_m2 * m2_to_hectare)
    
    wetland_impact_km2 = float(flooded_veg_px * pixel_area_m2 * m2_to_km2)
    total_impacted_km2 = float(total_inundated_px * pixel_area_m2 * m2_to_km2)
    
    affected_agri_ha = float(flood_area_ha * agri_fraction)
    estimated_affected_people = int(flood_area_km2 * estimated_pop_density_per_km2)
    
    # Severity classification index (1 to 5)
    if flood_area_km2 > 50:
        severity = "CRITICAL (Level 5)"
        severity_color = "#FF1744"
    elif flood_area_km2 > 20:
        severity = "HIGH ALERT (Level 4)"
        severity_color = "#FF9100"
    elif flood_area_km2 > 5:
        severity = "MODERATE (Level 3)"
        severity_color = "#FFD600"
    else:
        severity = "LOW / LOCALIZED (Level 2)"
        severity_color = "#00E676"
        
    return {
        "new_flood_area_km2": round(flood_area_km2, 2),
        "new_flood_area_hectares": round(flood_area_ha, 1),
        "wetland_vegetation_affected_km2": round(wetland_impact_km2, 2),
        "total_water_affected_km2": round(total_impacted_km2, 2),
        "estimated_affected_agriculture_ha": round(affected_agri_ha, 1),
        "estimated_population_at_risk": estimated_affected_people,
        "severity_level": severity,
        "severity_color": severity_color
    }

def generate_flood_geojson(
    classification_mask: np.ndarray,
    bounds: tuple, # (min_lon, min_lat, max_lon, max_lat)
    max_polygons: int = 40
) -> str:
    """
    Generates a simplified, fast GeoJSON FeatureCollection from the detected flood mask.
    This file can be directly opened in QGIS, Google Earth, or ArcGIS by the geography team member.
    """
    min_lon, min_lat, max_lon, max_lat = bounds
    h, w = classification_mask.shape
    
    flood_indices = np.argwhere(classification_mask == 2)
    
    features = []
    
    if len(flood_indices) > 0:
        # Sample or cluster blocks to create responsive geojson polygons
        step = max(1, int(np.sqrt(len(flood_indices) / max_polygons)))
        sampled = flood_indices[::step]
        
        for idx in sampled[:max_polygons]:
            r, c = idx
            # Convert pixel coords to lon/lat
            lat_top = max_lat - (r / h) * (max_lat - min_lat)
            lat_bot = max_lat - ((r + step) / h) * (max_lat - min_lat)
            lon_left = min_lon + (c / w) * (max_lon - min_lon)
            lon_right = min_lon + ((c + step) / w) * (max_lon - min_lon)
            
            poly_coords = [
                [
                    [round(lon_left, 5), round(lat_top, 5)],
                    [round(lon_right, 5), round(lat_top, 5)],
                    [round(lon_right, 5), round(lat_bot, 5)],
                    [round(lon_left, 5), round(lat_bot, 5)],
                    [round(lon_left, 5), round(lat_top, 5)]
                ]
            ]
            
            features.append({
                "type": "Feature",
                "properties": {
                    "class": "Newly Inundated Flood",
                    "source": "NASA-ISRO SAR (NISAR)",
                    "risk_priority": "High"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": poly_coords
                }
            })
            
    geojson_data = {
        "type": "FeatureCollection",
        "name": "NISAR_Flood_Inundation_Zones",
        "crs": {
            "type": "name",
            "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}
        },
        "features": features
    }
    
    return json.dumps(geojson_data, indent=2)

