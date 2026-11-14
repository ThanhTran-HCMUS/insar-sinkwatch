"""
InSAR Data Simulator for NASA-ISRO NISAR Surface Deformation
Generates physically grounded InSAR phase interferograms and vertical subsidence rates:
1. Ho Chi Minh City Metropolitan Core (District 7, Nha Be, Thu Thiem, Metro Line 1)
2. Mekong Riverbank Landslides & River Meander Collapse (Vam Nao / An Giang)
"""

import os
import numpy as np

def get_hcmc_insar_scene(shape=(220, 220), seed=42):
    """
    Simulates high-precision InSAR deformation for Ho Chi Minh City.
    Bounds: Lon [106.60, 106.82], Lat [10.68, 10.88]
    Models smooth geotechnical ground deformation conforming to HCMC urban subsoil geology.
    """
    np.random.seed(seed)
    h, w = shape
    y, x = np.mgrid[0:h, 0:w]
    
    # Geographic Bounds
    bounds = (106.60, 10.68, 106.82, 10.88)
    min_lon, min_lat, max_lon, max_lat = bounds
    center_lat, center_lon = 10.775, 106.710
    
    # 1. Base Geography & Open Water Decoration
    river_mask = np.zeros((h, w), dtype=bool)
    
    # 2. SAR Intensity / Amplitude (dB)
    sar_intensity_db = np.random.normal(loc=-4.5, scale=2.0, size=(h, w))
    
    # 3. True Geological Subsidence Field (mm/year)
    # Major Subsidence Bowl 1: District 7 - Nha Be (South-East soft Holocene mud, centered at Phu My Hung)
    dist_bowl1 = np.hypot(x - 0.527 * w, y - 0.760 * h)
    subsidence_d7 = -38.0 * np.exp(- (dist_bowl1 ** 2) / (2.0 * (24.0 ** 2)))
    
    # Major Subsidence Bowl 2: Binh Tan / Binh Chanh (South-West industrial groundwater pumping)
    dist_bowl2 = np.hypot(x - 0.220 * w, y - 0.650 * h)
    subsidence_bt = -32.0 * np.exp(- (dist_bowl2 ** 2) / (2.0 * (16.0 ** 2)))
    
    # Major Subsidence Bowl 3: Thanh Da Peninsula / Binh Thanh (Riverbank slip within peninsula)
    dist_bowl3 = np.hypot(x - 0.564 * w, y - 0.280 * h)
    subsidence_td = -22.0 * np.exp(- (dist_bowl3 ** 2) / (2.0 * (10.0 ** 2)))
    
    # Background regional tectonic/sediment compaction rate (-3 to -6 mm/year)
    background_rate = -4.5 + 1.2 * np.sin(x / 40.0)
    
    true_velocity_mm = background_rate + subsidence_d7 + subsidence_bt + subsidence_td
    
    # 4. InSAR Phase Interferogram (Wrapped Phase in [-pi, pi])
    # 1 full fringe (2*pi phase cycle) corresponds to lambda / 2 = 121.2 mm (NISAR L-band)
    lambda_mm = 242.4
    unwrapped_phase = (4.0 * np.pi / lambda_mm) * true_velocity_mm
    phase_noise = np.random.normal(loc=0.0, scale=0.35, size=(h, w))
    wrapped_phase = np.angle(np.exp(1j * (unwrapped_phase + phase_noise)))
    
    # 5. Key Infrastructure POIs for Risk Screening
    poi_list = [
        {"name": "Bến Thành Metro Terminal (Line 1 & 2)", "type": "Subway Station", "lat": 10.7718, "lon": 106.6980},
        {"name": "Ba Son Metro Station & Bridge", "type": "Bridge & Station", "lat": 10.7816, "lon": 106.7088},
        {"name": "Phú Mỹ Cable-Stayed Bridge", "type": "Highway Bridge", "lat": 10.7417, "lon": 106.7456},
        {"name": "Thủ Thiêm Under-River Tunnel", "type": "Underwater Tunnel", "lat": 10.7685, "lon": 106.7058},
        {"name": "Cát Lái International Container Port", "type": "Deepwater Port", "lat": 10.7554, "lon": 106.7932},
        {"name": "Phú Mỹ Hưng Urban Center (District 7)", "type": "Residential Complex", "lat": 10.7280, "lon": 106.7160},
        {"name": "Thanh Đa Embankment & Peninsula", "type": "River Embankment", "lat": 10.8220, "lon": 106.7210},
        {"name": "KCN Tân Tạo (Bình Tân - Vùng khai thác nước ngầm)", "type": "Industrial Groundwater Wellfield", "lat": 10.7500, "lon": 106.6480}
    ]
    
    return {
        "title": "TP. Hồ Chí Minh: Sụt lún Nền đất & Rủi ro Hạ tầng Đô thị",
        "region_code": "HCMC_METRO",
        "bounds": bounds,
        "center_lat": center_lat,
        "center_lon": center_lon,
        "velocity_map_mm_year": true_velocity_mm,
        "wrapped_phase": wrapped_phase,
        "sar_intensity_db": sar_intensity_db,
        "river_mask": river_mask,
        "poi_list": poi_list,
        "geology_note": "Tầng đất sét bùn Holocen dày 15-30m chịu tải yếu kết hợp khai thác nước ngầm tầng Pleistocen làm rỗng cấu trúc rỗng thể xốp."
    }

def get_mekong_riverbank_scene(shape=(220, 220), seed=99):
    """
    Simulates InSAR riverbank landslide & erosion along Mekong River (An Giang / Dong Thap).
    Bounds: Lon [105.10, 105.35], Lat [10.50, 10.75]
    Models smooth hydrodynamic geotechnical scour and bank slope failure.
    """
    np.random.seed(seed)
    h, w = shape
    y, x = np.mgrid[0:h, 0:w]
    
    bounds = (105.10, 10.50, 105.35, 10.75)
    center_lat, center_lon = 10.625, 105.225
    
    # 1. Base Geography
    river_mask = np.zeros((h, w), dtype=bool)
    
    # 2. Regional background compaction rate (-2 to -4 mm/year)
    background_rate = -3.0 + 0.8 * np.sin(x / 30.0)
    
    # 3. Geotechnical Erosion & Bank Collapse Slip Zones
    # Hotspot 1: Vàm Nao Meander Junction (Severe scour hole & bank slip)
    # Target Coords: Lat 10.6180, Lon 105.2150 -> row_ratio=0.528, col_ratio=0.460
    dist_vamnao = np.hypot((x - 0.460 * w) / 1.15, (y - 0.528 * h) / 1.35)
    subsidence_vamnao = -42.0 * np.exp(- (dist_vamnao ** 2) / (2.0 * (18.0 ** 2)))
    
    # Hotspot 2: Chợ Mới Embankment Vulnerability Zone
    # Target Coords: Lat 10.6350, Lon 105.2450 -> row_ratio=0.460, col_ratio=0.580
    dist_chomoi = np.hypot(x - 0.580 * w, y - 0.460 * h)
    subsidence_chomoi = -28.0 * np.exp(- (dist_chomoi ** 2) / (2.0 * (14.0 ** 2)))
    
    # Hotspot 3: Sông Tiền Riverbank Settlement near Residential Area
    # Target Coords: Lat 10.6420, Lon 105.2050 -> row_ratio=0.432, col_ratio=0.420
    dist_songtien = np.hypot(x - 0.420 * w, y - 0.432 * h)
    subsidence_songtien = -22.0 * np.exp(- (dist_songtien ** 2) / (2.0 * (12.0 ** 2)))
    
    velocity = background_rate + subsidence_vamnao + subsidence_chomoi + subsidence_songtien
    
    # 4. InSAR Phase Interferogram (NISAR L-band, lambda = 242.4 mm)
    lambda_mm = 242.4
    unwrapped = (4.0 * np.pi / lambda_mm) * velocity
    phase_noise = np.random.normal(loc=0.0, scale=0.30, size=(h, w))
    wrapped = np.angle(np.exp(1j * (unwrapped + phase_noise)))
    
    # 5. POIs for Mekong Delta
    poi_list = [
        {"name": "Ngã ba sông Vàm Nao (Điểm sạt lở xung yếu)", "type": "Riverbank Zone", "lat": 10.6180, "lon": 105.2150},
        {"name": "Kè bảo vệ bờ Chợ Mới", "type": "Embankment", "lat": 10.6350, "lon": 105.2450},
        {"name": "Cụm dân cư bờ sông Tiền", "type": "Residential Cluster", "lat": 10.6420, "lon": 105.2050}
    ]
    
    return {
        "title": "Sông Tiền / Vàm Nao: Sạt lở Bờ sông & Xói lở Châu thổ",
        "region_code": "MEKONG_LANDSLIDE",
        "bounds": bounds,
        "center_lat": center_lat,
        "center_lon": center_lon,
        "velocity_map_mm_year": velocity,
        "wrapped_phase": wrapped,
        "sar_intensity_db": np.random.normal(-6.0, 2.5, (h, w)),
        "river_mask": river_mask,
        "poi_list": poi_list,
        "geology_note": "Dòng chảy xiết tại đoạn uốn khúc lõm xói lở chân bờ bùn cát rời, gây trượt lở đất đột ngột vào mùa mưa lũ."
    }
