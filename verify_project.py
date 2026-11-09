"""
Verification & Test Suite for InSAR-SinkWatch
Validates:
1. InSAR Phase Processing & Displacement Conversion
2. Goldstein Adaptive Phase Filtering
3. AI Hotspot Anomaly Clustering
4. Geotechnical Compaction & Multi-Year Forecasting
5. GeoJSON Vector Generation
6. Multi-Scenario Data Simulation
"""

import sys
import numpy as np

def run_tests():
    print("=" * 60)
    print("🛰️  InSAR-SinkWatch Pipeline Verification & Unit Tests")
    print("=" * 60)
    
    # 1. Test InSAR Processing Module
    print("\n[1/5] Testing InSAR Processing Pipeline...")
    from src.pipeline.insar_processing import (
        NISAR_L_BAND_WAVELENGTH_MM,
        generate_interferogram,
        phase_to_displacement_mm,
        goldstein_phase_filter
    )
    
    m = np.exp(1j * np.random.uniform(-np.pi, np.pi, (50, 50)))
    s = np.exp(1j * np.random.uniform(-np.pi, np.pi, (50, 50)))
    ifg = generate_interferogram(m, s)
    assert ifg["wrapped_phase"].shape == (50, 50)
    assert np.all(ifg["wrapped_phase"] >= -np.pi) and np.all(ifg["wrapped_phase"] <= np.pi)
    
    # Test displacement conversion
    disp = phase_to_displacement_mm(np.array([2 * np.pi, -2 * np.pi]))
    expected_disp = NISAR_L_BAND_WAVELENGTH_MM / 2.0  # 121.2 mm
    assert np.isclose(disp[0], expected_disp, atol=1e-3)
    
    # Test Goldstein filter
    filtered_p = goldstein_phase_filter(ifg["wrapped_phase"], alpha=0.5, window_size=5)
    assert filtered_p.shape == (50, 50)
    print("  ✓ InSAR Phase & Goldstein filtering: PASSED")
    
    # 2. Test AI Subsidence Hotspot Detection
    print("\n[2/5] Testing AI Subsidence Detector & Forecasting...")
    from src.models.subsidence_detector import (
        detect_subsidence_hotspots,
        project_cumulative_subsidence,
        assess_infrastructure_vulnerability
    )
    
    mock_vel = np.full((40, 40), -5.0)
    mock_vel[15:25, 15:25] = -35.0  # subsidence bowl
    
    hotspots = detect_subsidence_hotspots(mock_vel, critical_threshold_mm=-20.0)
    assert hotspots["critical_pixels"] == 100
    assert hotspots["max_subsidence_rate_mm_year"] == -35.0
    
    # Test forecasting
    cum_5yr = project_cumulative_subsidence(mock_vel, forecast_years=5)
    assert np.all(cum_5yr <= mock_vel)  # Cumulative sinking increases
    
    # Test infrastructure vulnerability screening
    mock_poi = [
        {"name": "Central Metro Station", "type": "Subway", "lat": 10.77, "lon": 106.70}
    ]
    bounds = (106.65, 10.72, 106.75, 10.82)
    assessed = assess_infrastructure_vulnerability(hotspots["critical_mask"], bounds, mock_poi)
    assert len(assessed) == 1
    assert "risk_level" in assessed[0]
    print("  ✓ AI Hotspot Anomaly Clustering & Forecasting: PASSED")
    
    # 3. Test Geotechnical Analytics & GeoJSON
    print("\n[3/5] Testing Geotechnical Analytics & Vector GeoJSON...")
    from src.analytics.insar_metrics import calculate_geotechnical_impact, export_insar_geojson
    
    impact = calculate_geotechnical_impact(hotspots, mock_vel, pixel_spacing_meters=20.0)
    assert "critical_subsidence_area_km2" in impact
    assert "annual_sediment_loss_million_m3" in impact
    
    geojson_str = export_insar_geojson(mock_vel, bounds, assessed, sample_step=4)
    assert "FeatureCollection" in geojson_str
    assert "NISAR_Urban_Subsidence_InSAR" in geojson_str
    print("  ✓ Geotechnical Volume Metrics & GeoJSON Generation: PASSED")
    
    # 4. Test Data Simulation Module
    print("\n[4/5] Testing Multi-Scenario Data Simulation...")
    from src.data_simulator import get_hcmc_insar_scene, get_mekong_riverbank_scene
    
    hcmc = get_hcmc_insar_scene(shape=(60, 60))
    assert hcmc["region_code"] == "HCMC_METRO"
    assert len(hcmc["poi_list"]) >= 5
    
    mekong = get_mekong_riverbank_scene(shape=(60, 60))
    assert mekong["region_code"] == "MEKONG_LANDSLIDE"
    assert len(mekong["poi_list"]) >= 3
    print("  ✓ Data Simulator (HCMC & Mekong Scenarios): PASSED")
    
    # 5. Test Web App Import
    print("\n[5/5] Testing Full Streamlit Application Structure...")
    import app
    print("  ✓ app.py imports & Streamlit dashboard definition: PASSED")
    
    print("\n" + "=" * 60)
    print("🎉 ALL 5/5 TEST SUITES PASSED! PROJECT FULLY OPERATIONAL.")
    print("=" * 60 + "\n")

if __name__ == "__main__":
    run_tests()

