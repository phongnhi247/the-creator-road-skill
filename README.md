# HƯỚNG DẪN SỬ DỤNG TỪ A–Z: DISTILL STUDIO & THE CREATOR ROAD
### Bộ công cụ Đúc kết Sách, Tài liệu, Buổi học & Xuất Slide PDF 20 Phong Cách Chuyên Nghiệp

---

## 1. TỔNG QUAN BỘ CÔNG CỤ

Bộ công cụ này tự động hóa 100% quy trình biến tư liệu đầu vào (**Video Zoom / Máy ảnh DJI 4–10 GB**, **File ghi âm**, **Phụ đề `.srt`**, **Sách `.pdf`/`.docx`/`.epub`**, **Tài liệu/Báo cáo/SOP**) thành 2 sản phẩm chuẩn mực:

1. **Bản đúc kết nội dung chuyên sâu (`.md`):** Tự động áp dụng đúng khung theo 3 chế độ (*Workshop*, *Book*, *Document*), loại bỏ lan man, tự động sửa lỗi chính tả theo Từ điển nội bộ, có bảng chẩn đoán vấn đề và kế hoạch hành động.
2. **Bộ Slide PDF Widescreen 16:9 (`.pdf`):** Hỗ trợ **20 phong cách thiết kế chuyên nghiệp** (mặc định là **`01-quiet-luxury`** chuẩn mực, cùng các phong cách *Apple Bento, McKinsey, Harvard Review, Dark Academia, Watercolor...*), font tiếng Việt không lỗi dấu, tự động crop ảnh gốc sạch mép.

---

## 2. YÊU CẦU PHẦN MỀM CẦN CÀI ĐẶT TRÊN MÁY TÍNH

Để bộ công cụ chạy trơn tru, máy tính cần cài 4 thành phần cơ bản sau:

### 2.1. Cài đặt Git (Để tải và đồng bộ bộ công cụ về máy)
- Tải bản cài đặt cho Windows tại: [git-scm.com/downloads/win](https://git-scm.com/downloads/win)
- Hoặc cài nhanh qua cửa sổ dòng lệnh PowerShell:
  ```bash
  winget install Git.Git
  ```
- Lệnh tải trọn gói bộ công cụ về máy:
  ```bash
  git clone https://github.com/phongnhi247/the-creator-road-skill.git
  ```

### 2.2. Cài đặt Python (Phiên bản 3.10 – 3.12)
- Tải tại: [python.org/downloads](https://www.python.org/downloads/)
- **LƯU Ý QUAN TRỌNG:** Ở màn hình cài đặt đầu tiên, bắt buộc phải **TÍCH CHỌN** vào ô:
  `☑ Add python.exe to PATH` (nếu không tích, dòng lệnh sẽ báo lỗi không tìm thấy python).

### 2.3. Cài đặt FFmpeg (Dùng để rút âm thanh siêu tốc từ video)
- Cài nhanh nhất trên Windows 10/11 qua PowerShell:
  ```bash
  winget install Gyan.FFmpeg
  ```
- Hoặc tải bản `ffmpeg-release-essentials.zip` từ [gyan.dev/ffmpeg/builds](https://www.gyan.dev/ffmpeg/builds/), giải nén và thêm thư mục `bin` vào biến môi trường `PATH`.

### 2.4. Trình duyệt Google Chrome hoặc Microsoft Edge
- Công cụ sử dụng engine Chrome/Edge có sẵn trên máy để xuất PDF chuẩn 16:9 không lệch pixel.

### 2.5. Cài đặt các thư viện bổ trợ (Chỉ cần chạy 1 lần)
Mở cửa sổ dòng lệnh tại thư mục chứa bộ công cụ và chạy:
```bash
pip install -r requirements.txt
```
*(Thư viện gồm: `faster-whisper` bóc sub GPU, `pymupdf` đọc sách/pdf và crop ảnh, `numpy`).*

---

## 3. KẾT NỐI TÀI KHOẢN GEMINI / AI

Bộ skill này hoạt động hiệu quả nhất khi kết hợp với trợ lý AI (Gemini CLI, Claude Code, Cursor, Windsurf, Roo Code).

### 3.1. Cách lấy Gemini API Key (Hoàn toàn Miễn phí)
1. Truy cập: [Google AI Studio (aistudio.google.com)](https://aistudio.google.com/)
2. Đăng nhập bằng tài khoản Google (Gmail) của bạn.
3. Bấm nút **"Get API key"** $\rightarrow$ Chọn **"Create API key in new project"** $\rightarrow$ Sao chép (Copy) mã Key.

### 3.2. Cấu hình Key trên máy tính Windows
Mở cửa sổ Command Prompt (CMD) và gõ lệnh lưu vĩnh viễn (thay `MA_KEY_CUA_BAN` bằng key vừa copy):
```cmd
setx GEMINI_API_KEY "MA_KEY_CUA_BAN"
```
Hoặc tạo file `.env` đặt tại thư mục làm việc:
```env
GEMINI_API_KEY=MA_KEY_CUA_BAN
```

---

## 4. BA CHẾ ĐỘ ĐÚC KẾT & DANH MỤC 20 PHONG CÁCH SLIDE

### 4.1. Ba Chế Độ Đúc Kết Tự Động
1. **Chế độ `workshop` (Mặc định):** Đúc kết buổi học, khóa đào tạo, coaching, họp chiến lược (Video/Audio/Sub).
2. **Chế độ `book`:** Đúc kết sách giấy, ebook (`.pdf`, `.epub`, `.docx`), sách nói. Trích xuất mô hình cốt lõi, case study đắt giá, giới hạn áp dụng và kế hoạch chuyển hóa 7–30–90 ngày.
3. **Chế độ `document`:** Đúc kết tài liệu SOP, báo cáo nghiên cứu, phân tích thị trường. Trích xuất tóm tắt điều hành (Executive Summary), ma trận rủi ro và checklist thực thi.

### 4.2. Danh Mục 20 Phong Cách Slide PDF (Mặc định: 01-Quiet-Luxury)
- **Luxury & Editorial:** `01-quiet-luxury` *(Mặc định)*, `02-warm-cashmere`, `03-kinfolk-editorial`, `04-dark-academia`.
- **Executive & Consulting:** `05-mckinsey-executive`, `06-harvard-review`, `07-private-wealth`, `08-swiss-grid`.
- **Tech & Modern Bento:** `09-apple-bento`, `10-linear-dark-glass`, `11-vox-explainer`, `12-cyber-matrix`.
- **Creative & Storytelling:** `13-journal-collage`, `14-ukiyo-zen`, `15-watercolor-healing`, `16-vintage-patent`.
- **High-Impact & Action:** `17-ted-spotlight`, `18-ironman-athletic`, `19-chalkboard-masterclass`, `20-monochrome-brutalist`.

*(Chi tiết màu sắc và font chữ của từng phong cách xem tại file `skillCreatorRoad/references/style_gallery_guide.md`).*

---

## 5. MẪU CÂU LỆNH (PROMPTS) CHUẨN ĐỂ CHẠY

### Trường hợp 1: Đúc kết Buổi học (Mặc định phong cách Quiet Luxury)
> *"Áp dụng skill `creator-road`: Hãy xử lý toàn bộ tư liệu trong thư mục `Buoi-[X]`. Bước 1: Xuất bản text đúc kết (`.md`) theo chuẩn Kaizen để tôi duyệt trước. Bước 2: Test 1 ảnh slide Quiet Luxury kèm ảnh gốc để tôi duyệt rồi hãy xuất full PDF và gom gọn vào thư mục `Buoi-[X]` nhé."*

### Trường hợp 2: Đúc kết Sách
> *"Áp dụng skill `creator-road` chế độ `book`: Hãy phân tích cuốn sách `[ten_cuon_sach.pdf]`. Xuất bản đúc kết `.md` chuyên sâu cho sách và thiết kế bộ Slide PDF theo phong cách `04-dark-academia` (hoặc `02-warm-cashmere`)."*

### Trường hợp 3: Đúc kết Tài liệu / Báo cáo / SOP
> *"Áp dụng skill `creator-road` chế độ `document`: Hãy phân tích tài liệu `[ten_tai_lieu.docx]`. Xuất bản đúc kết tóm tắt điều hành và slide PDF theo phong cách `05-mckinsey-executive` (hoặc `08-swiss-grid`)."*

---

## 6. HƯỚNG DẪN CÁC SCRIPT KỸ THUẬT CHẠY RIÊNG

1. **Bóc sub video hàng loạt (GPU local):**
   ```bash
   python skillCreatorRoad/scripts/transcribe_batch.py "Buoi-X"
   ```
2. **Đọc và trích xuất text từ Sách & Tài liệu (.pdf, .docx, .epub, .txt):**
   ```bash
   python skillCreatorRoad/scripts/read_document.py "path/to/book.pdf" "output.txt"
   ```
3. **Trích xuất ảnh nhúng từ PDF slide hoặc cắt ảnh màn hình:**
   ```bash
   python skillCreatorRoad/scripts/extract_and_crop.py extract "slide.pdf" "images/"
   python skillCreatorRoad/scripts/extract_and_crop.py crop "screen.png" 0 0 1660 825 "clean.png"
   ```
4. **Xuất Slide PDF theo phong cách tùy chọn:**
   ```bash
   python skillCreatorRoad/scripts/build_luxury_pdf.py "slides.html" "output.pdf" --style 01-quiet-luxury
   ```
