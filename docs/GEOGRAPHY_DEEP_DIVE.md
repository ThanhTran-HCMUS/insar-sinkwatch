# SỔ TAY CHUYÊN MÔN ĐỊA LÝ & KHOA HỌC TRÁI ĐẤT
## Dự án: InSAR-SinkWatch | Đội thi: visionspace_us | NASA Space Apps 2026
*(Tài liệu dành riêng cho Thành viên phụ trách Địa lý học / GIS để làm chủ phần thuyết minh khoa học và trả lời phản biện trước hội đồng Ban giám khảo NASA)*

---

### PHẦN 1: BẢN CHẤT ĐỊA MẠO & ĐỊA CHẤT CÔNG TRÌNH TP. HỒ CHÍ MINH

Khi ban giám khảo hỏi: *"Tại sao TP.HCM lại bị sụt lún nghiêm trọng ở khu vực phía Nam (Quận 7, Nhà Bè, Bình Chánh) mà không phải ở phía Bắc (Củ Chi, Hóc Môn)?"*, bạn hãy trả lời bằng 2 luận điểm cốt lõi:

#### 1. Sự phân hóa tầng trầm tích Đệ Tứ (Quaternary Stratigraphy)
* **Khu vực phía Bắc & Đông Bắc (Củ Chi, TP. Thủ Đức gò cao):** Nằm trên bậc thềm tích tụ - bóc mòn Pleistocen cổ ($Q_I - Q_{III}$), cấu tạo từ đất sét hoa thảo, cát sạn cuội kết chặt, có sức chịu tải cao ($R > 1.5 - 2.5\text{ kg/cm}^2$). Do đó khu vực này ổn định, độ lún vi mô chỉ $< 3 - 5\text{ mm/năm}$.
* **Khu vực trũng phía Nam & Tây Nam (Quận 7, Nhà Bè, Bình Chánh, Bình Tân):** Là vùng đầm lầy châu thổ bồi tụ biển - đầm lầy trẻ thuộc kỷ Holocen ($Q_{IV}$). 
  * Tầng sét bùn dày từ **$15\text{m}$ đến hơn $30\text{m}$**.
  * Đặc tính cơ lý cực kỳ yếu: Độ ẩm tự nhiên $W = 60 - 85\%$, hệ số rỗng $e = 1.3 - 1.8$, sức chịu tải gần như bằng $0$ ($R < 0.3 - 0.5\text{ kg/cm}^2$), độ sệt ở trạng thái chảy.

#### 2. Nguyên lý Cơ học Đất Terzaghi (Effective Stress Principle)
Hiện tượng lún đô thị ở TP.HCM bị chi phối bởi nguyên lý ứng suất hữu hiệu:
$$\sigma' = \sigma - u$$
Trong đó:
* $\sigma$: Tổng ứng suất do tải trọng các khối nhà cao tầng và lớp đất phủ.
* $u$: Áp lực nước lỗ rỗng (Pore water pressure) trong các tầng chứa nước.
* $\sigma'$: Ứng suất hữu hiệu truyền lên khung hạt đất.

**Cơ chế tác động kép:**
1. **Hút cạn nước ngầm tầng sâu:** Hàng vạn giếng khoan công nghiệp và dân sinh khai thác nước ngầm từ các tầng Pleistocen ($80 - 120\text{m}$) làm tụt mực nước áp lực hàng chục mét $\rightarrow$ Áp lực nước lỗ rỗng $u$ giảm đột ngột $\rightarrow$ Ứng suất hữu hiệu $\sigma'$ tăng vọt $\rightarrow$ Các thấu kính sét bị ép nén thể tích không phục hồi (Consolidation settlement).
2. **Quá tải xây dựng trên nền đất yếu:** Các khu đô thị mới xây dựng ồ ạt trên nền đầm lầy móng cọc ma sát chưa chạm tới tầng đá gốc cứng làm trầm trọng thêm quá trình cố kết thứ cấp.

---

### PHẦN 2: CƠ CHẾ SẠT LỞ BỜ SÔNG ĐỒNG BẰNG SÔNG CỬU LONG (VÀM NAO / AN GIANG)

* **Hiện tượng uốn khúc dòng hàn (Meandering River Dynamics):**
  * Tại các đoạn cong của sông Tiền và sông Hậu (như ngã ba Vàm Nao), dòng chảy sinh ra dòng tuần hoàn thứ cấp (Helicoidal flow). Bờ lõm (bờ ngoài) chịu vận tốc dòng chảy cực đại, tạo thành các hố xói sâu từ $20\text{m}$ đến $40\text{m}$ dưới đáy sông, khoét rỗng chân cơ bờ.
* **Hiện tượng rút nước nhanh sau lũ (Rapid Drawdown):**
  * Đỉnh điểm sạt lở xảy ra khi lũ bắt đầu rút nhanh vào tháng 11. Nước sông rút nhanh trong khi nước ngầm trong thân đê/bờ bùn cát vẫn còn ứ đọng tạo ra chênh lệch áp lực thủy tĩnh từ trong bờ đẩy ra ngoài sông, kích hoạt các cung trượt tròn làm hàng trăm mét đất sụp đổ xuống sông trong chớp mắt.
* **InSAR giúp gì?** Trước khi sạt lở hoàn toàn, bờ sông luôn trải qua pha **trượt dão dẻo vi mô (Creep deformation)** ở cấp độ milimet. Vệ tinh InSAR phát hiện được giai đoạn biến dạng dẻo này trước 2-4 tuần để chính quyền di dời người dân kịp thời!

---

### PHẦN 3: HƯỚNG DẪN MỞ DỮ LIỆU CỦA APP TRONG QGIS

Bạn có thể mở dữ liệu xuất ra từ app để trình chiếu trực tiếp trên máy trong lúc pitch:

1. **Bước 1:** Trên Web Dashboard của dự án, chuyển qua Tab 2 và bấm nút **"🌍 Tải Dữ liệu Lún Vector (.geojson cho QGIS/ArcGIS)"**.
2. **Bước 2:** Mở phần mềm QGIS $\rightarrow$ Chọn `Layer` $\rightarrow$ `Add Layer` $\rightarrow$ `Add Vector Layer` $\rightarrow$ Chọn file `.geojson` vừa tải.
3. **Bước 3 (Thêm bản đồ vệ tinh làm nền):** Vào tab `Browser` của QGIS $\rightarrow$ `XYZ Tiles` $\rightarrow$ Kéo thả `Google Satellite` hoặc `OpenStreetMap` vào bản đồ.
4. **Bước 4 (Đổi màu hiển thị chuyên nghiệp):**
   * Nhấp đúp vào layer trong QGIS $\rightarrow$ Chọn thẻ `Symbology`.
   * Chọn `Categorized` hoặc `Graduated` theo trường `subsidence_rate_mm_year`.
   * Chọn bảng màu `Spectral` hoặc `Turbo` (Màu đỏ cho vùng lún nguy cấp, màu xanh lá cho vùng ổn định).

---

### PHẦN 4: BỘ CÂU HỎI VÀ ĐÁP ÁN PHẢN BIỆN TRƯỚC BAN GIÁM KHẢO NASA

#### Câu hỏi 1: *"Tại sao các bạn lại sử dụng InSAR L-band của NISAR thay vì dữ liệu Sentinel-1 C-band miễn phí có sẵn?"*
* **Đáp án chuẩn:**
  > *"Sentinel-1 dùng băng tần C-band có bước sóng ngắn ($\approx 5.6\text{ cm}$). Ở khu vực nhiệt đới gió mùa của Việt Nam với độ ẩm cao, thảm cỏ, tán cây và nền đất ướt liên tục thay đổi, tín hiệu C-band bị hiện tượng mất tương quan pha (Temporal Decorrelation) rất nặng chỉ sau 1-2 chu kỳ. Ngược lại, vệ tinh NISAR sử dụng băng tần L-band bước sóng dài ($24.24\text{ cm}$) có khả năng xuyên qua thảm thực vật để phản xạ từ nền đất và móng công trình, duy trì độ kết hợp pha cao ($\gamma > 0.6$) trong suốt nhiều tháng. Đây chính là bước đột phá mà giới viễn thám toàn cầu mong đợi từ NISAR."*

#### Câu hỏi 2: *"Dữ liệu của các bạn có giá trị thực tiễn gì cho chính sách quy hoạch của chính quyền địa phương?"*
* **Đáp án chuẩn:**
  > *"Hiện nay, TP.HCM mới chỉ có khoảng 10-15 trạm quan trắc lún mặt đất cố định bằng phương pháp thủy chuẩn hình học truyền thống. Số lượng này quá thưa thớt để phản ánh toàn cảnh. InSAR-SinkWatch cung cấp bản đồ độ phủ liên tục toàn thành phố với hàng triệu điểm đo mỗi 12 ngày. Kết quả này cung cấp bằng chứng định lượng chính xác để:
  > 1. Thiết lập các vùng cấm khai thác nước ngầm công nghiệp.
  > 2. Cảnh báo sớm độ lún vi sai (differential settlement) cho tuyến đường sắt đô thị Metro số 1 Bến Thành - Suối Tiên và tuyến Metro số 2.
  > 3. Cập nhật cốt nền xây dựng trong Quy hoạch chung TP.HCM tầm nhìn 2040 - 2060 thích ứng với hiện tượng đất lún nhanh hơn nước biển dâng."*

