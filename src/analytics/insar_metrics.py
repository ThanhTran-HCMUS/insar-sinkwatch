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
    as a standard GeoJSON FeatureCollection with rich metadata for Google Earth & QGIS.
    """
    min_lon, min_lat, max_lon, max_lat = bounds
    h, w = velocity_map.shape
    
    features = []
    
    # 1. Add Infrastructure POIs
    for poi in poi_list:
        p_lat, p_lon = poi["lat"], poi["lon"]
        if "risk_level" in poi:
            is_crit = poi["risk_level"] == "CRITICAL"
        else:
            r_poi = int(np.clip((max_lat - p_lat) / (max_lat - min_lat) * h, 0, h - 1))
            c_poi = int(np.clip((p_lon - min_lon) / (max_lon - min_lon) * w, 0, w - 1))
            r0, r1 = max(0, r_poi - 2), min(h, r_poi + 3)
            c0, c1 = max(0, c_poi - 2), min(w, c_poi + 3)
            is_crit = bool(np.any(velocity_map[r0:r1, c0:c1] < -20.0))
            
        r_idx = int(np.clip((max_lat - p_lat) / (max_lat - min_lat) * h, 0, h - 1))
        c_idx = int(np.clip((p_lon - min_lon) / (max_lon - min_lon) * w, 0, w - 1))
        vel_est = float(velocity_map[r_idx, c_idx])
        
        status_label = "⚠️ CẦN THEO DÕI SÁT (Nguy cơ lún lệch)" if is_crit else "✅ ỔN ĐỊNH (Móng cọc sâu)"
        
        features.append({
            "type": "Feature",
            "properties": {
                "name": poi["name"],
                "description": (
                    f"<b>Công trình:</b> {poi['name']}<br>"
                    f"<b>Loại kết cấu:</b> {poi.get('type', 'Hạ tầng')}<br>"
                    f"<b>Tốc độ lún InSAR:</b> {vel_est:.1f} mm/năm<br>"
                    f"<b>Đánh giá an toàn:</b> {status_label}<br>"
                    f"<b>Cảm biến:</b> NASA-ISRO NISAR L-band (1.25 GHz)"
                ),
                "type": poi.get("type", "Hạ tầng"),
                "risk_level": "NGUY CƠ LÚN LỆCH" if is_crit else "ỔN ĐỊNH",
                "subsidence_rate_mm_year": round(vel_est, 1),
                "severity": "CRITICAL" if is_crit else "LOW",
                "marker_symbol": "critical_infrastructure" if is_crit else "stable_infrastructure",
                "satellite_source": "NASA-ISRO NISAR L-band InSAR",
                "marker-color": "#ef4444" if is_crit else "#10b981",
                "marker-size": "medium"
            },
            "geometry": {
                "type": "Point",
                "coordinates": [poi["lon"], poi["lat"]]
            }
        })
        
    # 2. Add Subsidence Hotspot sample polygons across entire 2D map (3-Tier Severity Gradient)
    step = sample_step
    for r in range(0, h, step):
        for c in range(0, w, step):
            vel = float(velocity_map[r, c])
            if vel >= -15.0:
                continue
            
            lat = max_lat - ((r + 0.5 * step) / h) * (max_lat - min_lat)
            lon = min_lon + ((c + 0.5 * step) / w) * (max_lon - min_lon)
            
            d_lon = (max_lon - min_lon) / w * step * 0.5
            d_lat = (max_lat - min_lat) / h * step * 0.5
            
            poly = [
                [
                    [round(lon - d_lon, 5), round(lat + d_lat, 5)],
                    [round(lon + d_lon, 5), round(lat + d_lat, 5)],
                    [round(lon + d_lon, 5), round(lat - d_lat, 5)],
                    [round(lon - d_lon, 5), round(lat - d_lat, 5)],
                    [round(lon - d_lon, 5), round(lat + d_lat, 5)]
                ]
            ]
            
            if vel <= -30.0:
                fill_color = "#7f1d1d"
                stroke_color = "#991b1b"
                risk_tier = "NGUY CƠ CỰC ĐẠI"
            elif vel <= -20.0:
                fill_color = "#dc2626"
                stroke_color = "#b91c1c"
                risk_tier = "NGUY CẤP"
            else:
                fill_color = "#d97706"
                stroke_color = "#b45309"
                risk_tier = "CẢNH BÁO SỚM"
            
            features.append({
                "type": "Feature",
                "properties": {
                    "name": f"Phễu lún InSAR ({vel:.1f} mm/năm)",
                    "description": (
                        f"<b>Đối tượng:</b> Tâm phễu sụt lún đô thị<br>"
                        f"<b>Tốc độ sụt lún:</b> <span style='color:{stroke_color}; font-weight:bold;'>{vel:.1f} mm/năm</span><br>"
                        f"<b>Mức độ nguy cơ:</b> {risk_tier} (TCVN 9361:2012)<br>"
                        f"<b>Cơ chế địa mạo:</b> Cố kết tầng bùn sét Holocen do suy giảm áp lực nước lỗ rỗng<br>"
                        f"<b>Cảm biến viễn thám:</b> NASA-ISRO NISAR L-band InSAR (Bước sóng = 24.24 cm)"
                    ),
                    "type": "Tâm phễu lún cố kết",
                    "risk_level": risk_tier,
                    "subsidence_rate_mm_year": round(vel, 1),
                    "severity": "CRITICAL" if vel <= -20.0 else "WARNING",
                    "marker_symbol": "subsidence_polygon",
                    "satellite_source": "NASA-ISRO NISAR L-band InSAR",
                    "fill": fill_color,
                    "fill-opacity": 0.45,
                    "stroke": stroke_color,
                    "stroke-width": 2.0
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


def _xml_escape(val: str) -> str:
    """Escapes XML reserved characters for safe tag insertion (&, <, >, ", ')."""
    if val is None:
        return ""
    return (
        str(val)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )


def export_insar_kml(
    velocity_map: np.ndarray,
    bounds: tuple,
    poi_list: list,
    sample_step: int = 5
) -> str:
    """
    Exports subsidence deformation polygons and infrastructure POIs
    as a native Google Earth KML document with rich popup balloons and styling.
    All XML tags are strictly entity-escaped to prevent parser errors in Google Earth.
    """
    min_lon, min_lat, max_lon, max_lat = bounds
    h, w = velocity_map.shape
    center_lon = (min_lon + max_lon) / 2.0
    center_lat = (min_lat + max_lat) / 2.0
    
    kml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '<Document>',
        '  <name>InSAR-SinkWatch: Quan Trắc Sụt Lún NISAR</name>',
        '  <open>1</open>',
        '  <!-- 3D Cinematic Perspective View (NASA Space Apps Camera Preset) -->',
        '  <LookAt>',
        f'    <longitude>{center_lon:.4f}</longitude>',
        f'    <latitude>{center_lat - 0.025:.4f}</latitude>',
        '    <altitude>0</altitude>',
        '    <heading>14.0</heading>',
        '    <tilt>48.0</tilt>',
        '    <range>24000.0</range>',
        '    <altitudeMode>relativeToGround</altitudeMode>',
        '  </LookAt>',
        '  <!-- 3-Tier Multi-Gradient Subsidence Styles (NASA/USGS Standards) -->',
        '  <Style id="polyExtreme">',
        '    <LineStyle><color>ff151099</color><width>2.2</width></LineStyle>',
        '    <PolyStyle><color>771d1d7f</color></PolyStyle>',
        '  </Style>',
        '  <Style id="polyCritical">',
        '    <LineStyle><color>ff1c1cb9</color><width>1.8</width></LineStyle>',
        '    <PolyStyle><color>662626dc</color></PolyStyle>',
        '  </Style>',
        '  <Style id="polyModerate">',
        '    <LineStyle><color>ff0a62b8</color><width>1.2</width></LineStyle>',
        '    <PolyStyle><color>550677d9</color></PolyStyle>',
        '  </Style>',
        '  <Style id="poiCrit">',
        '    <IconStyle><color>ff4444ef</color><scale>1.2</scale>',
        '      <Icon><href>https://maps.google.com/mapfiles/kml/paddle/red-circle.png</href></Icon>',
        '    </IconStyle>',
        '  </Style>',
        '  <Style id="poiStable">',
        '    <IconStyle><color>ff81b910</color><scale>1.1</scale>',
        '      <Icon><href>https://maps.google.com/mapfiles/kml/paddle/grn-circle.png</href></Icon>',
        '    </IconStyle>',
        '  </Style>',
        '  <Folder><name>1. Công trình Trọng điểm (POIs)</name>'
    ]
    
    for poi in poi_list:
        p_lat, p_lon = poi["lat"], poi["lon"]
        if "risk_level" in poi:
            is_crit = poi["risk_level"] == "CRITICAL"
        else:
            r_poi = int(np.clip((max_lat - p_lat) / (max_lat - min_lat) * h, 0, h - 1))
            c_poi = int(np.clip((p_lon - min_lon) / (max_lon - min_lon) * w, 0, w - 1))
            r0, r1 = max(0, r_poi - 2), min(h, r_poi + 3)
            c0, c1 = max(0, c_poi - 2), min(w, c_poi + 3)
            is_crit = bool(np.any(velocity_map[r0:r1, c0:c1] < -20.0))
            
        r_idx = int(np.clip((max_lat - p_lat) / (max_lat - min_lat) * h, 0, h - 1))
        c_idx = int(np.clip((p_lon - min_lon) / (max_lon - min_lon) * w, 0, w - 1))
        vel_est = float(velocity_map[r_idx, c_idx])
            
        style_id = "poiCrit" if is_crit else "poiStable"
        status_badge = "⚠️ CẦN THEO DÕI SÁT (Nguy cơ lún lệch)" if is_crit else "✅ ỔN ĐỊNH (Móng cọc sâu)"
        poi_name = poi.get("name", "Công trình")
        poi_name_esc = _xml_escape(poi_name)
        poi_type_esc = _xml_escape(poi.get("type", "Hạ tầng"))
        
        rec_poi = "Kiểm định lún vi sai định kỳ &amp; khảo sát biến dạng dầm sàn." if is_crit else "Móng cọc ngàm tầng cát cuội Pleistocen ổn định."
        poi_badge_color = "#ef4444" if is_crit else "#10b981"
        
        kml_lines.append('    <Placemark>')
        kml_lines.append(f'      <name>{poi_name_esc}</name>')
        kml_lines.append(f'      <styleUrl>#{style_id}</styleUrl>')
        kml_lines.append('      <description><![CDATA[')
        kml_lines.append(f'        <div style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif; font-size: 13px; line-height: 1.5; color: #1e293b; max-width: 320px;">')
        kml_lines.append(f'          <div style="background:{poi_badge_color}; color:#ffffff; padding:6px 10px; border-radius:4px; font-weight:bold; font-size:13.5px; margin-bottom:8px;">')
        kml_lines.append(f'            🏗️ {poi_name}')
        kml_lines.append('          </div>')
        kml_lines.append('          <table style="width:100%; border-collapse:collapse; margin-bottom:8px; font-size:12px;">')
        kml_lines.append('            <tr style="border-bottom:1px solid #e2e8f0;">')
        kml_lines.append('              <td style="padding:4px 0; color:#64748b;"><b>Loại kết cấu:</b></td>')
        kml_lines.append(f'              <td style="padding:4px 0; text-align:right; font-weight:500;">{poi.get("type", "Hạ tầng")}</td>')
        kml_lines.append('            </tr>')
        kml_lines.append('            <tr style="border-bottom:1px solid #e2e8f0;">')
        kml_lines.append('              <td style="padding:4px 0; color:#64748b;"><b>Vận tốc lún InSAR:</b></td>')
        kml_lines.append(f'              <td style="padding:4px 0; text-align:right; font-weight:bold; color:{poi_badge_color}; font-size:13px;">{vel_est:.1f} mm/năm</td>')
        kml_lines.append('            </tr>')
        kml_lines.append('            <tr style="border-bottom:1px solid #e2e8f0;">')
        kml_lines.append('              <td style="padding:4px 0; color:#64748b;"><b>Đánh giá an toàn:</b></td>')
        kml_lines.append(f'              <td style="padding:4px 0; text-align:right; font-weight:bold; color:{poi_badge_color};">{status_badge}</td>')
        kml_lines.append('            </tr>')
        kml_lines.append('            <tr>')
        kml_lines.append('              <td style="padding:4px 0; color:#64748b;"><b>Vệ tinh quan trắc:</b></td>')
        kml_lines.append('              <td style="padding:4px 0; text-align:right;">NISAR L-band (12 ngày/lần)</td>')
        kml_lines.append('            </tr>')
        kml_lines.append('          </table>')
        kml_lines.append(f'          <div style="background:#f8fafc; border-left:3px solid {poi_badge_color}; padding:6px 8px; margin-bottom:6px; font-size:11.5px; color:#334155;">')
        kml_lines.append(f'            <b>Khuyến nghị giám định:</b> {rec_poi}')
        kml_lines.append('          </div>')
        kml_lines.append('          <div style="font-size:10px; color:#94a3b8; text-align:center; margin-top:6px; border-top:1px dashed #cbd5e1; padding-top:4px;">')
        kml_lines.append('            NASA SPACE APPS CHALLENGE 2026 | InSAR-SinkWatch Observatory')
        kml_lines.append('          </div>')
        kml_lines.append('        </div>')
        kml_lines.append('      ]]></description>')
        kml_lines.append(f'      <Point><coordinates>{poi["lon"]:.6f},{poi["lat"]:.6f},0</coordinates></Point>')
        kml_lines.append('    </Placemark>')
        
    kml_lines.append('  </Folder>')
    kml_lines.append('  <Folder><name>2. Tâm Phễu Sụt Lún (Hotspot Polygons)</name>')
    
    # 2. Add Subsidence Hotspot sample polygons across entire 2D map (3-Tier Severity Gradient)
    step = sample_step
    for r in range(0, h, step):
        for c in range(0, w, step):
            vel = float(velocity_map[r, c])
            if vel >= -15.0:
                continue
            
            lat = max_lat - ((r + 0.5 * step) / h) * (max_lat - min_lat)
            lon = min_lon + ((c + 0.5 * step) / w) * (max_lon - min_lon)
            d_lon = (max_lon - min_lon) / w * step * 0.5
            d_lat = (max_lat - min_lat) / h * step * 0.5
            
            coords = [
                f"{lon - d_lon:.5f},{lat + d_lat:.5f},0",
                f"{lon + d_lon:.5f},{lat + d_lat:.5f},0",
                f"{lon + d_lon:.5f},{lat - d_lat:.5f},0",
                f"{lon - d_lon:.5f},{lat - d_lat:.5f},0",
                f"{lon - d_lon:.5f},{lat + d_lat:.5f},0"
            ]
            coords_str = " ".join(coords)
            
            if vel <= -30.0:
                style_id = "polyExtreme"
                risk_tier = "NGUY CƠ CỰC ĐẠI"
                title_color = "#991b1b"
            elif vel <= -20.0:
                style_id = "polyCritical"
                risk_tier = "NGUY CẤP"
                title_color = "#ef4444"
            else:
                style_id = "polyModerate"
                risk_tier = "CẢNH BÁO SỚM"
                title_color = "#f59e0b"
                
            poly_name = f"Phễu lún InSAR ({vel:.1f} mm/năm) [{risk_tier}]"
            
            # Ratio exceedance relative to TCVN 9361:2012 allowable foundation settlement (8.0 mm/year)
            exceedance = abs(vel) / 8.0
            if vel <= -30.0:
                rec_action = "Khẩn cấp: Kiểm toán cọc móng, quan trắc Piezometer áp lực lỗ rỗng, cấm khoan hút nước ngầm."
            elif vel <= -20.0:
                rec_action = "Ưu tiên cao: Thiết lập mốc trắc địa quan trắc lún lệch, hạn chế xây dựng công trình tải trọng lớn."
            else:
                rec_action = "Cảnh báo sớm: Bổ sung vào danh mục theo dõi chu kỳ 12 ngày qua vệ tinh viễn thám NISAR."
                
            kml_lines.append('    <Placemark>')
            kml_lines.append(f'      <name>{_xml_escape(poly_name)}</name>')
            kml_lines.append(f'      <styleUrl>#{style_id}</styleUrl>')
            kml_lines.append('      <description><![CDATA[')
            kml_lines.append(f'        <div style="font-family: -apple-system, BlinkMacSystemFont, \'Segoe UI\', Roboto, sans-serif; font-size: 13px; line-height: 1.5; color: #1e293b; max-width: 320px;">')
            kml_lines.append(f'          <div style="background:{title_color}; color:#ffffff; padding:6px 10px; border-radius:4px; font-weight:bold; font-size:13px; margin-bottom:8px;">')
            kml_lines.append(f'            🛰️ {poly_name}')
            kml_lines.append('          </div>')
            kml_lines.append('          <table style="width:100%; border-collapse:collapse; margin-bottom:8px; font-size:12px;">')
            kml_lines.append('            <tr style="border-bottom:1px solid #e2e8f0;">')
            kml_lines.append('              <td style="padding:4px 0; color:#64748b;"><b>Vận tốc lún InSAR:</b></td>')
            kml_lines.append(f'              <td style="padding:4px 0; text-align:right; font-weight:bold; color:{title_color}; font-size:13px;">{vel:.1f} mm/năm</td>')
            kml_lines.append('            </tr>')
            kml_lines.append('            <tr style="border-bottom:1px solid #e2e8f0;">')
            kml_lines.append('              <td style="padding:4px 0; color:#64748b;"><b>Phân cấp rủi ro:</b></td>')
            kml_lines.append(f'              <td style="padding:4px 0; text-align:right; font-weight:bold; color:{title_color};">{risk_tier}</td>')
            kml_lines.append('            </tr>')
            kml_lines.append('            <tr style="border-bottom:1px solid #e2e8f0;">')
            kml_lines.append('              <td style="padding:4px 0; color:#64748b;"><b>Chuẩn TCVN 9361:</b></td>')
            kml_lines.append(f'              <td style="padding:4px 0; text-align:right; font-weight:bold; color:#b91c1c;">Vượt ngưỡng {exceedance:.1f} lần</td>')
            kml_lines.append('            </tr>')
            kml_lines.append('            <tr style="border-bottom:1px solid #e2e8f0;">')
            kml_lines.append('              <td style="padding:4px 0; color:#64748b;"><b>Cơ chế địa mạo:</b></td>')
            kml_lines.append('              <td style="padding:4px 0; text-align:right;">Cố kết bùn sét Holocen</td>')
            kml_lines.append('            </tr>')
            kml_lines.append('            <tr>')
            kml_lines.append('              <td style="padding:4px 0; color:#64748b;"><b>Vệ tinh viễn thám:</b></td>')
            kml_lines.append('              <td style="padding:4px 0; text-align:right;">NASA-ISRO NISAR (λ=24.2cm)</td>')
            kml_lines.append('            </tr>')
            kml_lines.append('          </table>')
            kml_lines.append(f'          <div style="background:#f8fafc; border-left:3px solid {title_color}; padding:6px 8px; margin-bottom:6px; font-size:11.5px; color:#334155;">')
            kml_lines.append(f'            <b>Khuyến nghị kỹ thuật:</b> {rec_action}')
            kml_lines.append('          </div>')
            kml_lines.append('          <div style="font-size:10px; color:#94a3b8; text-align:center; margin-top:6px; border-top:1px dashed #cbd5e1; padding-top:4px;">')
            kml_lines.append('            NASA SPACE APPS CHALLENGE 2026 | InSAR-SinkWatch Observatory')
            kml_lines.append('          </div>')
            kml_lines.append('        </div>')
            kml_lines.append('      ]]></description>')
            kml_lines.append(f'      <Polygon><outerBoundaryIs><LinearRing><coordinates>{coords_str}</coordinates></LinearRing></outerBoundaryIs></Polygon>')
            kml_lines.append('    </Placemark>')
            
    kml_lines.append('  </Folder>')
    kml_lines.append('</Document></kml>')
    return '\n'.join(kml_lines)

