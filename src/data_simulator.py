"""
InSAR Data Simulator for NASA-ISRO NISAR Surface Deformation
Generates physically grounded InSAR phase interferograms and vertical subsidence rates:
1. Ho Chi Minh City Metropolitan Core (District 7, Nha Be, Thu Thiem, Metro Line 1)
2. Mekong Riverbank Landslides & River Meander Collapse (Vam Nao / An Giang)
"""

import numpy as np

def get_hcmc_insar_scene(shape=(220, 220), seed=42):
    """
    Simulates high-precision InSAR deformation for Ho Chi Minh City.
    Bounds: Lon [106.60, 106.82], Lat [10.68, 10.88]
    """
    np.random.seed(seed)
    h, w = shape
    y, x = np.mgrid[0:h, 0:w]
    
    # Geographic Bounds
    bounds = (106.60, 10.68, 106.82, 10.88)
    center_lat, center_lon = 10.775, 106.710
    
    # 1. Base Geography: Saigon River Meander
    river_path = 0.52 * h + 0.3 * h * np.sin(x / 30.0) + 0.1 * h * np.cos(x / 14.0)
    dist_river = np.abs(y - river_path)
    river_mask = dist_river < (0.05 * h)
    
    # 2. SAR Intensity / Amplitude (dB)
    # High urban backscatter (double-bounce) except river
    sar_intensity_db = np.random.normal(loc=-4.5, scale=2.0, size=(h, w))
    sar_intensity_db[river_mask] = -24.5
    
    # 3. True Geological Subsidence Field (mm/year)
    # Major Subsidence Bowl 1: District 7 - Nha Be (South-East soft Holocene mud)
    dist_bowl1 = np.hypot(x - 0.62 * w, y - 0.72 * h)
    subsidence_d7 = -38.0 * np.exp(- (dist_bowl1 ** 2) / (2.0 * (26.0 ** 2)))
    
    # Major Subsidence Bowl 2: Binh Tan / Binh Chanh (South-West industrial groundwater pumping)
    dist_bowl2 = np.hypot(x - 0.22 * w, y - 0.65 * h)
    subsidence_bt = -32.0 * np.exp(- (dist_bowl2 ** 2) / (2.0 * (20.0 ** 2)))
    
    # Major Subsidence Bowl 3: Thanh Da Peninsula / Binh Thanh (Riverbank slip)
    dist_bowl3 = np.hypot(x - 0.55 * w, y - 0.25 * h)
    subsidence_td = -22.0 * np.exp(- (dist_bowl3 ** 2) / (2.0 * (15.0 ** 2)))
    
    # Background regional tectonic/sediment compaction rate (-3 to -6 mm/year)
    background_rate = -4.5 + 1.2 * np.sin(x / 40.0)
    
    true_velocity_mm = background_rate + subsidence_d7 + subsidence_bt + subsidence_td
    true_velocity_mm[river_mask] = 0.0  # Open water decorrelation
    
    # 4. InSAR Phase Interferogram (Wrapped Phase in [-pi, pi])
    # 1 full fringe (2*pi phase cycle) corresponds to lambda / 2 = 121.2 mm (NISAR L-band)
    lambda_mm = 242.4
    unwrapped_phase = (4.0 * np.pi / lambda_mm) * true_velocity_mm
    phase_noise = np.random.normal(loc=0.0, scale=0.35, size=(h, w))
    phase_noise[river_mask] = np.random.uniform(-np.pi, np.pi, size=np.sum(river_mask))
    wrapped_phase = np.angle(np.exp(1j * (unwrapped_phase + phase_noise)))
    
    # 5. Key Infrastructure POIs for Risk Screening
    poi_list = [
        {"name": "Bến Thành Metro Terminal (Line 1 & 2)", "type": "Subway Station", "lat": 10.7718, "lon": 106.6980},
        {"name": "Ba Son Metro Station & Bridge", "type": "Bridge & Station", "lat": 10.7816, "lon": 106.7088},
        {"name": "Phú Mỹ Cable-Stayed Bridge", "type": "Highway Bridge", "lat": 10.7417, "lon": 106.7456},
        {"name": "Thủ Thiêm Under-River Tunnel", "type": "Underwater Tunnel", "lat": 10.7685, "lon": 106.7058},
        {"name": "Cát Lái International Container Port", "type": "Deepwater Port", "lat": 10.7554, "lon": 106.7932},
        {"name": "Phú Mỹ Hưng Urban Center (District 7)", "type": "Residential Complex", "lat": 10.7280, "lon": 106.7160},
        {"name": "Thanh Đa Embankment & Peninsula", "type": "River Embankment", "lat": 10.8220, "lon": 106.7210}
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
    """
    np.random.seed(seed)
    h, w = shape
    y, x = np.mgrid[0:h, 0:w]
    
    bounds = (105.10, 10.50, 105.35, 10.75)
    center_lat, center_lon = 10.625, 105.225
    
    # Sharp meander junction (Vam Nao)
    river = np.abs(y - (0.5 * h + 0.35 * h * np.sin(x / 25.0))) < (0.08 * h)
    
    velocity = -2.0 + 0.8 * np.sin(x / 20.0)
    
    # Outer concave bend experiencing extreme scouring and bank collapse
    collapse_zone = (np.abs(y - 0.55 * h) < 0.12 * h) & (x > 0.4 * w) & (x < 0.7 * w) & (~river)
    velocity[collapse_zone] = -42.0 + np.random.normal(0, 3.0, size=np.sum(collapse_zone))
    velocity[river] = 0.0
    
    lambda_mm = 242.4
    unwrapped = (4.0 * np.pi / lambda_mm) * velocity
    wrapped = np.angle(np.exp(1j * unwrapped))
    
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
        "sar_intensity_db": np.random.normal(-9.0, 3.0, (h, w)),
        "river_mask": river,
        "poi_list": poi_list,
        "geology_note": "Dòng chảy xiết tại đoạn uốn khúc lõm xói lở chân bờ bùn cát rời, gây trượt lở đất đột ngột vào mùa mưa lũ."
    }
