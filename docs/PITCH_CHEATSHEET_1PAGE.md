# 📑 IN-SAR SINKWATCH: BẢN TÓM TẮT THI ĐẤU 1 TRANG (1-PAGE CHEAT-SHEET)
### Đội thi: visionspace_us | Điểm cầu: TP. Hồ Chí Minh | NASA Space Apps Challenge 2026

---

### 1. CÂU NÓI MỞ ĐẦU "GÂY ẤN TƯỢNG" (ELEVATOR PITCH - 30 GIÂY)
> *"Kính thưa Ban giám khảo, TP. Hồ Chí Minh không chỉ đối mặt với nước biển dâng, mà mặt đất dưới chân chúng ta đang chìm xuống từ **15 đến 45 mm mỗi năm**—nhanh gấp **10 lần** tốc độ nước biển dâng. Mây mưa nhiệt đới làm vệ tinh quang học bị mù, nhưng **InSAR-SinkWatch** sử dụng sóng radar L-band của vệ tinh **NASA-ISRO NISAR** để đo độ lún từng milimet từ không gian, tự động cảnh báo nguy cơ cho tuyến Metro số 1 và các công trình trọng điểm."*

---

### 2. CÁC CON SỐ "VÀNG" CẦN THUỘC LÒNG ĐỂ ĐỐI ĐÁP
* **$\lambda = 24.24\text{ cm}$ (242.4 mm):** Bước sóng L-band của NASA NISAR (xuyên thấu tán lá và mây mưa nhiệt đới).
* **12 ngày:** Chu kỳ quỹ đạo lặp của NISAR (quét toàn bộ thành phố định kỳ 12 ngày/lần 24/7).
* **$15 - 45\text{ mm/năm}$:** Tốc độ lún ghi nhận tại Quận 7, Nhà Bè, Bình Chánh (khảo sát JICA/MONRE).
* **$3.5\text{ mm/năm}$:** Tốc độ nước biển dâng toàn cầu $\rightarrow$ **Sụt lún nhanh gấp 5 - 10 lần nước biển dâng!**
* **$30\text{m}$:** Độ dày tầng sét bùn Holocen ($Q_{IV}$) có độ rỗng cao, chịu tải yếu ở phía Nam TP.HCM.
* **$80 - 120\text{m}$:** Độ sâu các tầng chứa nước Pleistocen bị hút cạn làm tụt áp lực nước lỗ rỗng.

---

### 3. PHÂN CHIA LỜI NÓI KHI THUYẾT TRÌNH (3 – 5 PHÚT)

| Phút | Người nói | Nội dung | Thao tác trên màn hình |
| :--- | :--- | :--- | :--- |
| **0:00 – 1:00** | **Bạn (IT)** | Giới thiệu đội, nêu vấn đề sụt lún ngầm và tại sao ảnh quang học bị mù trước mây mưa. | Chiếu **Slide 1 & Slide 2** |
| **1:00 – 2:00** | **Bạn (IT)** | Giới thiệu công nghệ radar L-band NISAR và công thức giao thoa pha $\Delta d = \frac{\lambda}{4\pi}\Delta\phi$. | Chiếu **Slide 3 & Slide 4** |
| **2:00 – 3:30** | **Bạn (IT)** | **DEMO TRỰC TIẾP:** Xoay bản đồ 3D PyDeck lún màu đỏ, chỉ vào bảng rủi ro Ga Metro Bến Thành, bấm tải GeoJSON. | Chuyển sang tab **Web App (localhost:8501)** |
| **3:30 – 4:30** | **Bạn Địa lý** | Luận giải địa chất: Tầng bùn sét Holocen $Q_{IV}$, khai thác nước ngầm, hiểm họa kép với triều cường và kiến nghị đóng giếng khoan. | Chiếu **Slide 6** (hoặc Tab 3 trên Web) |
| **4:30 – 5:00** | **Cả 2 bạn** | Tóm tắt tầm nhìn mã nguồn mở và cảm ơn Ban giám khảo. | Chiếu **Slide 7** |

---

### 4. 3 THAO TÁC DEMO ĂN ĐIỂM NHẤT TRÊN WEB APP
1. **Kéo chuột xoay góc nhìn 3D (Pitch 45°):** Cho giám khảo thấy rõ các cột địa hình sụt lún màu đỏ hạ sâu xuống ở Quận 7 và Bình Tân.
2. **Bật/Tắt Bộ lọc Goldstein:** Cho thấy vân giao thoa pha (Fringes) từ dạng nhiễu hạt trở nên sắc nét rõ ràng.
3. **Bấm nút Tải GeoJSON:** Chứng minh ứng dụng tương thích hoàn hảo với phần mềm QGIS/ArcGIS của giới khoa học không gian.

