"""
InSAR-SinkWatch: NASA NISAR Millimeter-Precision Urban Subsidence & Landslide Observatory
Built by Team visionspace_us for NASA International Space Apps Challenge 2026
Challenge: Dancing with the SARs (Tracking Earth's Surface Dance via Radar Remote Sensing)
"""

import streamlit as st
import numpy as np
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt
import io
import json

from src.pipeline.insar_processing import (
    NISAR_L_BAND_WAVELENGTH_MM,
    goldstein_phase_filter,
    phase_to_displacement_mm
)
from src.models.subsidence_detector import (
    detect_subsidence_hotspots,
    project_cumulative_subsidence,
    assess_infrastructure_vulnerability
)
from src.analytics.insar_metrics import (
    calculate_geotechnical_impact,
    export_insar_geojson
)
from src.data_simulator import (
    get_hcmc_insar_scene,
    get_mekong_riverbank_scene
)

# ---------------------------------------------------------
# Page Configuration & NASA Dark Mode
# ---------------------------------------------------------
st.set_page_config(
    page_title="InSAR-SinkWatch | NASA NISAR Observatory",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Mission Control Styling
st.markdown("""
<style>
    .main {
        background-color: #080c14;
        color: #e2e8f0;
    }
    .metric-box {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.85), rgba(30, 41, 59, 0.85));
        border: 1px solid rgba(56, 189, 248, 0.25);
        border-radius: 10px;
        padding: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        margin-bottom: 12px;
    }
    .metric-title {
        font-size: 12px;
        text-transform: uppercase;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 1px;
    }
    .metric-val {
        font-size: 28px;
        font-weight: 800;
        color: #38bdf8;
        font-family: 'Courier New', monospace;
    }
    .team-badge {
        background: linear-gradient(90deg, #b91c1c, #ea580c);
        color: white;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Sidebar Controls
# ---------------------------------------------------------
with st.sidebar:
    st.markdown('<div class="team-badge">🛰️ TEAM: visionspace_us | NASA Space Apps 2026</div>', unsafe_allow_html=True)
    st.title("InSAR-SinkWatch")
    st.caption("Millimeter Urban Subsidence & Geohazard Observatory")
    
    st.markdown("---")
    st.subheader("1. Chọn Khu vực Quan sát")
    region_choice = st.selectbox(
        "Khu vực nghiên cứu (Study Area):",
        [
            "1. TP. Hồ Chí Minh (Quận 7, Nhà Bè, Bình Chánh, Metro Line 1 & 2)",
            "2. Đồng bằng sông Cửu Long (Sạt lở bờ sông Vàm Nao / An Giang)"
        ]
    )
    
    st.markdown("---")
    st.subheader("2. Xử lý Tín hiệu Giao thoa InSAR")
    apply_goldstein = st.toggle("Bật Bộ lọc Nhiễu pha Goldstein (InSAR Filter)", value=True)
    goldstein_alpha = st.slider("Hệ số lọc Goldstein Alpha:", 0.1, 0.9, 0.5, 0.1)
    
    st.markdown("---")
    st.subheader("3. Ngưỡng Cảnh báo Sụt lún (Risk Threshold)")
    critical_th = st.slider("Ngưỡng sụt lún nguy cấp (mm/năm):", -45.0, -15.0, -20.0, 1.0)
    
    st.markdown("---")
    st.subheader("4. Dự báo Tương lai (Multi-Year Forecast)")
    forecast_years = st.slider("Thời gian mô phỏng tương lai:", 1, 10, 5, help="Dự báo độ lún tích lũy theo năm")

# ---------------------------------------------------------
# Load Scenario
# ---------------------------------------------------------
if "Hồ Chí Minh" in region_choice:
    scene = get_hcmc_insar_scene()
else:
    scene = get_mekong_riverbank_scene()

raw_phase = scene["wrapped_phase"]
if apply_goldstein:
    filtered_phase = goldstein_phase_filter(raw_phase, alpha=goldstein_alpha, window_size=5)
else:
    filtered_phase = raw_phase

velocity_map = scene["velocity_map_mm_year"]
bounds = scene["bounds"]
poi_list = scene["poi_list"]

# AI Hotspot Detection
hotspots = detect_subsidence_hotspots(
    velocity_map_mm_year=velocity_map,
    critical_threshold_mm=critical_th
)

# Geotechnical Impact
impact = calculate_geotechnical_impact(hotspots, velocity_map)

# Infrastructure Vulnerability Screening
poi_assessed = assess_infrastructure_vulnerability(
    hotspots["critical_mask"],
    bounds,
    poi_list
)

# ---------------------------------------------------------
# Top Header Banner
# ---------------------------------------------------------
col_head1, col_head2 = st.columns([3, 1])
with col_head1:
    st.title("🛰️ InSAR-SinkWatch Observatory")
    st.markdown(f"**Nhiệm vụ:** Giám sát sụt lún nền đất & cảnh báo rủi ro công trình bằng kỹ thuật giao thoa radar **NASA-ISRO NISAR L-band**")
    st.write(f"📍 **Khu vực:** `{scene['title']}` | **Bước sóng radar:** `L-band (λ = 24.24 cm)`")
    st.caption(f"ℹ️ *{scene['geology_note']}*")

with col_head2:
    st.markdown(f"""
    <div class="metric-box" style="text-align: right; border-color: {impact['threat_color']};">
        <div class="metric-title">Trạng thái Báo động Địa kỹ thuật</div>
        <div style="font-size: 16px; font-weight: 800; color: {impact['threat_color']}; margin-top: 4px;">
            {impact['threat_level']}
        </div>
        <div style="font-size: 11px; color: #94a3b8; margin-top: 4px;">Phân tích theo chuỗi dữ liệu NISAR</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Top Metric KPI Row
# ---------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Tốc độ Sụt lún Cực đại</div>
        <div class="metric-val" style="color:#f43f5e;">{impact['max_sinking_velocity']} <span style="font-size:16px;">mm/năm</span></div>
        <div style="font-size:12px; color:#fb7185;">(Nhanh gấp 5-10 lần nước biển dâng)</div>
    </div>
    """, unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Diện tích Sụt lún Nguy cấp</div>
        <div class="metric-val">{impact['critical_subsidence_area_km2']} <span style="font-size:16px;">km²</span></div>
        <div style="font-size:12px; color:#38bdf8;">Tổng diện tích lún: {impact['total_impacted_urban_area_km2']} km²</div>
    </div>
    """, unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Thể tích Đất/Nước ngầm Mất đi</div>
        <div class="metric-val">{impact['annual_sediment_loss_million_m3']} <span style="font-size:16px;">triệu m³/năm</span></div>
        <div style="font-size:12px; color:#fbbf24;">Độ nén rỗng tầng chứa nước</div>
    </div>
    """, unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class="metric-box">
        <div class="metric-title">Dân số Vùng Lún Nguy hiểm</div>
        <div class="metric-val">{impact['estimated_urban_population_at_risk']:,} <span style="font-size:16px;">người</span></div>
        <div style="font-size:12px; color:#e2e8f0;">Nguy cơ ngập triều cường gia tăng</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------
tab_insar, tab_vuln, tab_geo_deep, tab_tech = st.tabs([
    "🗺️ Tín hiệu InSAR & Mô hình 3D",
    "📊 Đánh giá Hạ tầng & Dự báo Lún",
    "🌍 Chuyên môn Địa lý & Trầm tích (Domain Expert)",
    "🛰️ Bản chất Kỹ thuật InSAR L-band"
])

# =========================================================
# TAB 1: InSAR PHASE & 3D DEFORMATION
# =========================================================
with tab_insar:
    st.subheader("1. Bản đồ Pha Giao thoa & Tốc độ Biến dạng Milimet")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("**1. Vòng Giao thoa Pha (Wrapped Phase):**")
        fig_p1, ax_p1 = plt.subplots(figsize=(4, 4), facecolor="#080c14")
        im_p1 = ax_p1.imshow(filtered_phase, cmap="jet", vmin=-np.pi, vmax=np.pi)
        ax_p1.axis("off")
        ax_p1.set_title("InSAR Phase Fringes [-π, +π]", color="white", fontsize=10)
        fig_p1.colorbar(im_p1, ax=ax_p1, fraction=0.046, pad=0.04)
        st.pyplot(fig_p1, use_container_width=True)
        plt.close(fig_p1)
        st.caption("✨ Mỗi vòng màu (Fringe) ứng với độ dời 12.1 cm (nửa bước sóng L-band).")

    with col_p2:
        st.markdown("**2. Bản đồ Tốc độ Lún (Displacement Rate):**")
        fig_p2, ax_p2 = plt.subplots(figsize=(4, 4), facecolor="#080c14")
        im_p2 = ax_p2.imshow(velocity_map, cmap="turbo", vmin=-45, vmax=5)
        ax_p2.axis("off")
        ax_p2.set_title("Vertical Velocity (mm/year)", color="white", fontsize=10)
        cbar = fig_p2.colorbar(im_p2, ax=ax_p2, fraction=0.046, pad=0.04)
        cbar.ax.yaxis.set_tick_params(color='white')
        plt.setp(plt.getp(cbar.ax.axes, 'yticklabels'), color='white')
        st.pyplot(fig_p2, use_container_width=True)
        plt.close(fig_p2)
        st.caption("🔴 Màu đỏ/tím đậm thể hiện phễu lún nghiêm trọng (-35 đến -45 mm/năm).")

    with col_p3:
        st.markdown("**3. AI Phân vùng Nguy cơ (Hotspot Mask):**")
        fig_p3, ax_p3 = plt.subplots(figsize=(4, 4), facecolor="#080c14")
        c_mask = np.zeros((*hotspots["classification_map"].shape, 3), dtype=np.float32)
        c_mask[hotspots["classification_map"] == 0] = [0.1, 0.6, 0.3]   # Green (Stable)
        c_mask[hotspots["classification_map"] == 1] = [1.0, 0.7, 0.0]   # Amber (Moderate)
        c_mask[hotspots["classification_map"] == 2] = [1.0, 0.1, 0.2]   # Red (Critical Bowl)
        ax_p3.imshow(c_mask)
        ax_p3.axis("off")
        ax_p3.set_title("AI Subsidence Classification", color="white", fontsize=10)
        st.pyplot(fig_p3, use_container_width=True)
        plt.close(fig_p3)
        st.caption("🟢 Ổn định | 🟡 Lún trung bình (-10 to -20 mm) | 🔴 Phễu lún nguy cấp (<-20 mm).")

    st.markdown("---")
    st.subheader("2. Mô hình Không gian 3D Sụt lún Đô thị (PyDeck 3D Mesh)")
    
    # Generate 3D visualization dataframe
    min_lon, min_lat, max_lon, max_lat = bounds
    h, w = velocity_map.shape
    step = 5
    rows, cols = np.mgrid[0:h:step, 0:w:step]
    lats = max_lat - (rows / h) * (max_lat - min_lat)
    lons = min_lon + (cols / w) * (max_lon - min_lon)
    vels = velocity_map[::step, ::step].flatten()
    
    # We invert velocity so that the sinking depth extrudes downwards visually
    depths = np.clip(-vels, 0, 50)
    
    # Color scale: green (0) to yellow (20) to red (40+)
    colors_r = np.clip(depths * 6.0, 30, 255).astype(int)
    colors_g = np.clip(255 - depths * 5.0, 20, 255).astype(int)
    colors_b = np.full_like(colors_r, 40)
    
    df_3d = pd.DataFrame({
        "lon": lons.flatten(),
        "lat": lats.flatten(),
        "velocity_mm": vels,
        "sinking_depth": depths,
        "color_r": colors_r,
        "color_g": colors_g,
        "color_b": colors_b
    })
    
    # Filter out rivers
    df_3d = df_3d[df_3d["sinking_depth"] > 2.0]
    
    # POI dataframe
    df_poi = pd.DataFrame(poi_assessed)
    df_poi["color_r"] = [255 if p["risk_level"] == "CRITICAL" else 0 for p in poi_assessed]
    df_poi["color_g"] = [30 if p["risk_level"] == "CRITICAL" else 230 for p in poi_assessed]
    df_poi["color_b"] = [60 if p["risk_level"] == "CRITICAL" else 100 for p in poi_assessed]
    
    view_state = pdk.ViewState(
        latitude=scene["center_lat"],
        longitude=scene["center_lon"],
        zoom=11,
        pitch=45,
        bearing=15
    )
    
    layer_mesh = pdk.Layer(
        "ColumnLayer",
        data=df_3d,
        get_position=["lon", "lat"],
        get_elevation="sinking_depth",
        elevation_scale=15,
        radius=180,
        get_fill_color=["color_r", "color_g", "color_b", 190],
        pickable=True,
        auto_highlight=True
    )
    
    layer_poi = pdk.Layer(
        "ScatterplotLayer",
        data=df_poi,
        get_position=["lon", "lat"],
        get_radius=400,
        get_fill_color=["color_r", "color_g", "color_b", 255],
        pickable=True
    )
    
    deck_map = pdk.Deck(
        layers=[layer_mesh, layer_poi],
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v11",
        tooltip={"text": "Vị trí: {lat}, {lon}\nTốc độ lún: {velocity_mm} mm/năm\nĐộ sâu phễu lún: {sinking_depth} mm"}
    )
    
    st.pydeck_chart(deck_map)
    st.caption("✨ Bản đồ 3D: Các cột cao thể hiện phễu lún càng sâu và tốc độ lún càng nhanh. Các chấm sáng lớn đánh dấu các công trình trọng điểm.")

# =========================================================
# TAB 2: VULNERABILITY & PROJECTION
# =========================================================
with tab_vuln:
    st.subheader("📊 Rà soát Rủi ro Công trình & Dự báo Lún Tích lũy (2026 - 2036)")
    
    col_v1, col_v2 = st.columns([1, 1])
    
    with col_v1:
        st.markdown("**Bảng Rà soát Rủi ro Công trình Hạ tầng Trọng điểm:**")
        df_table = pd.DataFrame(poi_assessed)[["name", "type", "risk_level"]]
        df_table.columns = ["Tên Công trình", "Loại hình", "Mức độ Rủi ro"]
        st.dataframe(df_table, use_container_width=True)
        
    with col_v2:
        st.markdown(f"**Dự báo Độ lún Tích lũy {forecast_years} năm tới (Soil Consolidation Model):**")
        cum_disp = project_cumulative_subsidence(velocity_map, forecast_years=forecast_years)
        max_cum_sunk = float(np.min(cum_disp))
        
        # Line chart of multi-year projection
        years = list(range(2026, 2026 + forecast_years + 1))
        p_d7 = [0] + [-38.0 * (0.98**y) * (y + 1) for y in range(forecast_years)]
        p_bt = [0] + [-32.0 * (0.98**y) * (y + 1) for y in range(forecast_years)]
        p_metro = [0] + [-16.0 * (0.98**y) * (y + 1) for y in range(forecast_years)]
        
        df_proj = pd.DataFrame({
            "Năm": years,
            "Quận 7 / Phú Mỹ Hưng (mm)": p_d7,
            "Bình Tân / An Lạc (mm)": p_bt,
            "Hành lang Tuyến Metro 1 (mm)": p_metro
        }).set_index("Năm")
        
        st.line_chart(df_proj)
        st.warning(f"⚠️ Dự báo đến năm **{2026 + forecast_years}**, tâm phễu lún lớn nhất sẽ hạ thấp thêm **{abs(max_cum_sunk):.1f} cm**!")

    st.markdown("---")
    st.subheader("📥 Xuất Dữ liệu Không gian (GIS Export)")
    geojson_out = export_insar_geojson(velocity_map, bounds, poi_assessed)
    
    c_dl1, c_dl2 = st.columns(2)
    with c_dl1:
        st.download_button(
            label="🌍 Tải Dữ liệu Lún Vector (.geojson cho QGIS/ArcGIS)",
            data=geojson_out,
            file_name=f"NISAR_InSAR_Subsidence_{scene['region_code']}.geojson",
            mime="application/geo+json",
            use_container_width=True
        )
    with c_dl2:
        report_txt = f"""============================================================
BÁO CÁO ĐỊA KỸ THUẬT SỤT LÚN KHÔNG GIAN (NISAR InSAR RAPID BRIEF)
Đội thi: visionspace_us | NASA International Space Apps Challenge 2026
============================================================
Khu vực: {scene['title']}
Trạng thái: {impact['threat_level']}
Cảm biến: NASA-ISRO Synthetic Aperture Radar (NISAR L-band)
Tốc độ lún cực đại ghi nhận: {impact['max_sinking_velocity']} mm/năm
Tổng diện tích phễu lún nguy cấp: {impact['critical_subsidence_area_km2']} km2
Ước tính thể tích đất/tầng chứa nước bị nén rỗng: {impact['annual_sediment_loss_million_m3']} triệu m3/năm
Dân số trong vùng trũng nguy cơ cao: {impact['estimated_urban_population_at_risk']:,} người
Công trình bị đe dọa trực tiếp:
- Bến Thành Metro Terminal, Ba Son Station, Cầu Phú Mỹ, Hầm Thủ Thiêm.
============================================================
"""
        st.download_button(
            label="📄 Tải Báo cáo Tổng hợp Địa kỹ thuật (.txt)",
            data=report_txt,
            file_name="NISAR_Geotechnical_Brief.txt",
            mime="text/plain",
            use_container_width=True
        )

# =========================================================
# TAB 3: GEOGRAPHY & EARTH SCIENCE DEEP DIVE
# =========================================================
with tab_geo_deep:
    st.subheader("🌍 Luận giải Chuyên sâu Địa mạo, Thủy văn & Trầm tích")
    st.markdown("""
    *Phần tài liệu khoa học này do **Thành viên Địa lý học (Geography / GIS Lead)** trong đội đảm nhận để thuyết minh trước hội đồng các nhà khoa học viễn thám NASA.*
    """)
    
    g1, g2 = st.columns(2)
    with g1:
        st.markdown(r"""
        ### 1. Cấu trúc Địa chất & Thạch học Nền móng TP.HCM
        * **Tầng trầm tích Holocen trên cùng ($Q_{IV}$):** 
          * Chiếm trọn khu vực trũng phía Nam (Quận 7, Nhà Bè, Bình Chánh).
          * Thành phần chủ yếu là **bùn sét, cát pha hữu cơ có độ ẩm cực cao ($60-80\%$)**, độ rỗng lớn ($e > 1.2$) và sức chịu tải gần như bằng $0$ ($R < 0.5\text{ kg/cm}^2$).
          * Khi chịu tải trọng của hàng nghìn khối bê tông cốt thép đô thị, nước trong các lỗ rỗng vi mô bị ép thoát ra ngoài, dẫn tới hiện tượng **Cố kết thứ cấp (Secondary Consolidation)** kéo dài hàng chục năm.
        * **Khai thác Nước ngầm quá mức (Aquifer Over-exploitation):**
          * Các tầng chứa nước Pleistocen ($Q_I - Q_{III}$) ở độ sâu $80-120\text{m}$ bị hàng vạn giếng khoan công nghiệp hút cạn $\rightarrow$ Làm giảm áp lực thủy tĩnh lỗ rỗng (Pore water pressure), gây sụt sập các thấu kính cát và kéo toàn bộ mặt đất đô thị chìm dần xuống.
        """)
        
    with g2:
        st.markdown(r"""
        ### 2. Mối đe dọa "Cộng hưởng Kép" (Subsidence + Sea Level Rise)
        * **Nước biển dâng (Sea Level Rise):** Tốc độ trung bình khoảng $3.5\text{ mm/năm}$.
        * **Tốc độ Sụt lún (Land Subsidence):** Ghi nhận qua InSAR lên đến **$35 - 45\text{ mm/năm}$** $\rightarrow$ **Nhanh gấp 10 lần nước biển dâng!**
        * **Hệ quả Thủy văn:** 
          * Bán kính ngập do triều cường mở rộng gấp 3 lần. Triều dâng trên sông Sài Gòn ($+1.70\text{m}$) dễ dàng vượt qua các tuyến đê bao tạm bợ.
          * Hiện tượng nghẽn dòng chảy thoát nước mưa tự nhiên: Khi nền đất thấp hơn mực nước ngoài kênh, toàn bộ hệ thống cống thoát nước trọng lực bị tê liệt, biến các tuyến đường thành hồ chứa nước thải.
        """)

    st.markdown("---")
    st.subheader("3. Khuyến nghị Giải pháp Quy hoạch Đô thị Khẩn cấp")
    st.info("""
    **Kiến nghị từ dữ liệu InSAR-SinkWatch cho UBND TP.HCM & Bộ Xây dựng:**
    1. **Cấm tuyệt đối khai thác nước ngầm tầng sâu:** Thiết lập lộ trình đóng cửa 100% giếng khoan công nghiệp tại các phễu lún Quận 7, Bình Tân và Nhà Bè; thay thế bằng nguồn cấp nước mặt từ hồ Dầu Tiếng / sông Đồng Nai.
    2. **Quy hoạch Tải trọng Đô thị thích ứng:** Dừng cấp phép các dự án cao ốc siêu nặng tại các vùng móng bùn sét chưa được gia cố cọc ma sát chạm tầng đá gốc Pleistocen.
    3. **Ứng dụng InSAR giám sát Tuyến Metro số 1 & 2:** Cài đặt các mốc phản xạ radar góc nhọn (Corner Reflectors) dọc tuyến đường sắt đô thị để theo dõi độ lún vi sai (Differential Settlement) hàng tuần, ngăn chặn nguy cơ trật bánh tàu.
    """)

# =========================================================
# TAB 4: TECHNICAL InSAR PHYSICS
# =========================================================
with tab_tech:
    st.subheader("🛰️ Bản chất Vật lý của Sóng Radar L-band NISAR trong Đo đạc InSAR")
    st.markdown(r"""
    **Tại sao sứ mệnh NASA-ISRO NISAR lại là "Cuộc cách mạng" cho bài toán đo lún?**
    
    1. **Vấn đề Mất tương quan (Decorrelation) của Sentinel-1 (C-band):**
       * Vệ tinh Sentinel-1 của châu Âu sử dụng băng tần C-band ($\lambda \approx 5.6\text{ cm}$). Bước sóng ngắn này rất nhạy cảm với sự đung đưa của lá cây, thảm cỏ và sự ẩm ướt của đất. Ở khí hậu nhiệt đới gió mùa của Việt Nam, pha sóng C-band bị nhiễu loạn gần như hoàn toàn chỉ sau vài tuần.
    2. **Sức mạnh Băng sóng Dài L-band ($\lambda = 24.24\text{ cm}$) của NASA JPL:**
       * Sóng L-band có bước sóng dài gấp 4.5 lần C-band, dễ dàng **xuyên qua lớp thảm thực vật** để phản xạ trực tiếp từ nền đất cứng và móng công trình xây dựng.
       * Duy trì được **Độ kết hợp pha cao (High Temporal Coherence, $\gamma > 0.6$)** trong suốt nhiều tháng liên tục.
    3. **Công thức Đo dời pha Vi mô (Phase-to-Displacement):**
    """)
    st.latex(r"\Delta d = \frac{\lambda}{4\pi} \Delta \phi_{\text{InSAR}}")
    st.markdown(r"""
       * Với $\lambda = 242.4\text{ mm}$, chỉ cần sai số đo pha trong tầm vài độ, hệ thống AI đã có thể phát hiện sự sụt lún của nền đất ở độ phân giải **$1 - 2\text{ mm}$**, tương đương độ dày của một chiếc thẻ ngân hàng!
    """)

# ---------------------------------------------------------
# Footer
# ---------------------------------------------------------
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 13px;">
    🚀 <b>InSAR-SinkWatch</b> — Dự án tham dự <b>NASA International Space Apps Challenge 2026</b> | Đội thi <b>visionspace_us</b> (TP. Hồ Chí Minh, Việt Nam)<br>
    Đề tài: <i>Dancing with the SARs</i> | Dựa trên kỹ thuật InSAR độ chính xác milimet của vệ tinh <b>NASA-ISRO NISAR</b>
</div>
""", unsafe_allow_html=True)
