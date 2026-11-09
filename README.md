# BỘ CÔNG CỤ ĐÚC KẾT SÁCH, TÀI LIỆU, BUỔI HỌC & XUẤT SLIDE PDF 20 PHONG CÁCH
### The Creator Road & Distillation Studio (Tối ưu cho Google Antigravity & Gemini)

Bộ công cụ tự động hóa quy trình biến mọi tư liệu đầu vào (**Video Zoom/DJI**, **File ghi âm**, **Phụ đề `.srt`**, **Sách `.pdf`/`.epub`**, **Tài liệu/Báo cáo/SOP**) thành:
1. **Bản đúc kết chuyên sâu (`.md`):** Chuẩn hóa nội dung, loại bỏ lan man, tự động sửa lỗi chính tả giọng nói.
2. **Bộ Slide PDF Widescreen 16:9 (`.pdf`):** Hỗ trợ **20 phong cách chuyên nghiệp** (mặc định là **`01-quiet-luxury`** Obsidian & Champagne Gold, cùng *Apple Bento, McKinsey, Harvard Review, Dark Academia, v.v.*), font tiếng Việt không lỗi dấu, tự động crop ảnh gốc sạch mép.

---

## 1. CÀI ĐẶT NHANH (CHỈ 3 BƯỚC ĐƠN GIẢN)

Đã loại bỏ toàn bộ các bước cài đặt phần mềm phức tạp không cần thiết (không cần cài Git, không cần cài Chrome vì máy tính đã có sẵn Edge).

### Bước 1: Tải bộ công cụ về máy
- Bấm vào nút xanh **`Code`** ở góc trên bên phải trang GitHub này $\rightarrow$ Chọn **`Download ZIP`**.
- Giải nén file ZIP ra thư mục bất kỳ trên máy tính của bạn.

### Bước 2: Cài đặt thư viện tự động (1 chạm)
- Đảm bảo máy đã cài **Python** (tải tại [python.org](https://www.python.org/downloads/), nhớ tích chọn `☑ Add python.exe to PATH`).
- Bấm đúp chuột vào file **`cai_dat_thu_vien.bat`** nằm ở thư mục gốc $\rightarrow$ máy sẽ tự động cài toàn bộ thư viện cần thiết.

### Bước 3: Cài đặt Google Antigravity & Kết nối Trợ lý AI
- **Phần mềm AI khuyến nghị:** Cài đặt và sử dụng **Google Antigravity** (môi trường lập trình & trợ lý AI Agent tối ưu nhất cho Gemini) để mở thư mục dự án và điều phối toàn bộ bộ skill này.
- **Lấy Gemini API Key miễn phí:**
  1. Vào [Google AI Studio (aistudio.google.com)](https://aistudio.google.com/) đăng nhập Gmail.
  2. Bấm **"Get API key"** $\rightarrow$ Tạo Key và copy mã.
  3. Tạo 1 file tên `.env` trong thư mục dự án và dán vào:
     ```env
     GEMINI_API_KEY=ma_key_cua_ban
     ```

*(Lưu ý tùy chọn: Nếu bạn muốn tự bóc băng video nặng 4–10 GB trực tiếp trên máy bằng card đồ họa GPU, hãy cài thêm [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) qua lệnh PowerShell `winget install Gyan.FFmpeg`).*

---

## 2. BA CHẾ ĐỘ ĐÚC KẾT & 20 PHONG CÁCH SLIDE

### 2.1. Ba Chế Độ Đúc Kết
1. **`workshop` (Mặc định):** Đúc kết buổi học, khóa đào tạo, coaching, họp chiến lược (Video/Audio/Sub) $\rightarrow$ Khung 5 phần chuẩn Kaizen.
2. **`book`:** Đúc kết sách giấy, ebook, sách nói $\rightarrow$ Trích xuất mô hình cốt lõi, case study đắt giá, giới hạn áp dụng và kế hoạch chuyển hóa 7–30–90 ngày.
3. **`document`:** Đúc kết tài liệu SOP, báo cáo nghiên cứu $\rightarrow$ Tóm tắt điều hành (Executive Summary), ma trận rủi ro và checklist thực thi.

### 2.2. Danh Mục 20 Phong Cách Slide PDF (Mặc định: 01-Quiet-Luxury)
- **Luxury & Editorial:** `01-quiet-luxury` *(Mặc định)*, `02-warm-cashmere`, `03-kinfolk-editorial`, `04-dark-academia`.
- **Executive & Consulting:** `05-mckinsey-executive`, `06-harvard-review`, `07-private-wealth`, `08-swiss-grid`.
- **Tech & Modern Bento:** `09-apple-bento`, `10-linear-dark-glass`, `11-vox-explainer`, `12-cyber-matrix`.
- **Creative & Storytelling:** `13-journal-collage`, `14-ukiyo-zen`, `15-watercolor-healing`, `16-vintage-patent`.
- **High-Impact & Action:** `17-ted-spotlight`, `18-ironman-athletic`, `19-chalkboard-masterclass`, `20-monochrome-brutalist`.

*(Chi tiết thông số màu sắc và font chữ xem tại file `skillCreatorRoad/references/style_gallery_guide.md`).*

---

## 3. MẪU CÂU LỆNH (PROMPT) CHUẨN ĐỂ CHẠY TRÊN AI

Chỉ cần mở **Google Antigravity** (hoặc trợ lý AI), mở thư mục dự án và copy các mẫu lệnh sau:

### Trường hợp 1: Đúc kết Buổi học (Mặc định phong cách Quiet Luxury)
> *"Áp dụng skill `creator-road`: Hãy xử lý toàn bộ tư liệu trong thư mục `Buoi-[X]`. Bước 1: Xuất bản text đúc kết (`.md`) theo chuẩn Kaizen để tôi duyệt trước. Bước 2: Test 1 ảnh slide Quiet Luxury kèm ảnh gốc để tôi duyệt rồi hãy xuất full PDF và gom gọn vào thư mục `Buoi-[X]` nhé."*

### Trường hợp 2: Đúc kết Sách
> *"Áp dụng skill `creator-road` chế độ `book`: Hãy phân tích cuốn sách `[ten_cuon_sach.pdf]`. Xuất bản đúc kết `.md` chuyên sâu cho sách và thiết kế bộ Slide PDF theo phong cách `04-dark-academia` (hoặc `02-warm-cashmere`)."*

### Trường hợp 3: Đúc kết Tài liệu / Báo cáo / SOP
> *"Áp dụng skill `creator-road` chế độ `document`: Hãy phân tích tài liệu `[ten_tai_lieu.docx]`. Xuất bản đúc kết tóm tắt điều hành và slide PDF theo phong cách `05-mckinsey-executive`."*

---

## 4. CÔNG CỤ TÁCH PHỤ ĐỀ NHANH (NẰM TRONG THƯ MỤC `tools/`)

Nếu bạn có file video quay riêng và chỉ muốn tách ra file `.srt` để lấy chữ:
- Mở thư mục **`tools/`** $\rightarrow$ Bấm đúp vào file **`Tach_Sub_Video.bat`** (hoặc kéo thả video đè lên file này).
- Công cụ sẽ tự động dùng GPU trên máy để trích xuất ra file `.srt` nằm ngay cạnh video gốc trong vài giây.
