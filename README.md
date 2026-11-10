# BỘ CÔNG CỤ ĐÚC KẾT SÁCH, TÀI LIỆU, BUỔI HỌC & XUẤT SLIDE PDF 50 PHONG CÁCH
### The Creator Road & Distillation Studio (Tối ưu cho Google Antigravity & Gemini)

Bộ công cụ tự động hóa quy trình biến mọi tư liệu đầu vào (**Video Zoom/DJI**, **File ghi âm**, **Phụ đề `.srt`**, **Sách `.pdf`/`.epub`**, **Tài liệu/Báo cáo/SOP**) thành:
1. **Bản đúc kết chuyên sâu (`.md`):** Chuẩn hóa nội dung, loại bỏ lan man, tự động sửa lỗi chính tả giọng nói.
2. **Bộ Slide PDF Widescreen 16:9 (`.pdf`):** Hỗ trợ **50 phong cách chuyên nghiệp** (mặc định là **`01-quiet-luxury`** Obsidian & Champagne Gold, cùng *Apple Bento, McKinsey, Harvard Review, Bloomberg, SpaceX, Cyberpunk, v.v.*), font tiếng Việt không lỗi dấu, tự động crop ảnh gốc sạch mép.

---

## 1. HƯỚNG DẪN CÀI ĐẶT TỪ A–Z CHO NGƯỜI MỚI (5 BƯỚC CHUẨN)

```text
[Bước 1: Cài Git & Python] ➔ [Bước 2: Kéo dự án về máy] ➔ [Bước 3: Bấm cài thư viện] ➔ [Bước 4: Lấy Key & Antigravity] ➔ [Bước 5: Mở ra & Gõ lệnh chạy]
```

### Bước 1: Cài đặt 2 phần mềm nền tảng (Chỉ làm 1 lần duy nhất)
1. **Cài Git (để tải và cập nhật code):**
   - Tải bản 64-bit tại: [git-scm.com/downloads/win](https://git-scm.com/downloads/win) $\rightarrow$ Cứ bấm *Next* liên tục đến khi hoàn tất.
2. **Cài Python (để chạy các công cụ AI):**
   - Tải tại: [python.org/downloads](https://www.python.org/downloads/) (chọn bản 3.10 – 3.12).
   - ⚠️ **LƯU Ý QUAN TRỌNG:** Ở màn hình cài đặt đầu tiên, bắt buộc phải **TÍCH CHỌN** vào ô:
     `☑ Add python.exe to PATH` *(nếu quên tích ô này, máy sẽ không nhận diện được lệnh python).*

### Bước 2: Kéo bộ công cụ về máy tính
- Mở thư mục bạn muốn lưu dự án trên máy (ví dụ ổ `D:\Project` hoặc thư mục làm việc).
- Nhấp chuột phải chọn **Open in Terminal** (hoặc mở PowerShell) và gõ lệnh:
  ```bash
  git clone https://github.com/phongnhi247/the-creator-road-skill.git
  ```
- *(Nếu không dùng Git: Bấm nút xanh **`Code`** ở góc trên bên phải trang GitHub này $\rightarrow$ Chọn **`Download ZIP`** rồi giải nén ra).*

### Bước 3: Cài đặt thư viện tự động (1 chạm chuột)
- Mở thư mục `the-creator-road-skill` vừa tải về máy.
- Bấm đúp chuột vào file **`cai_dat_thu_vien.bat`** nằm ở thư mục gốc.
- Cửa sổ màu đen sẽ tự động cài toàn bộ thư viện. Khi thấy hiện chữ *"HOÀN TẤT CÀI ĐẶT!"* thì bấm phím bất kỳ để tắt đi.

### Bước 4: Lấy Gemini API Key & Cài Google Antigravity
1. **Lấy Key AI miễn phí:**
   - Vào [Google AI Studio (aistudio.google.com)](https://aistudio.google.com/) đăng nhập tài khoản Google (Gmail).
   - Bấm nút **"Get API key"** $\rightarrow$ Bấm **"Create API key"** $\rightarrow$ Copy mã Key vừa tạo.
2. **Lưu Key vào dự án:**
   - Trong thư mục `the-creator-road-skill`, tạo một file tên là `.env` và dán dòng sau vào:
     ```env
     GEMINI_API_KEY=mã_key_bạn_vừa_copy
     ```
3. **Cài đặt Google Antigravity:** Cài đặt và sử dụng Google Antigravity làm môi trường làm việc chính cho Gemini.

### Bước 5: Mở ra và Bắt đầu dùng
1. Mở **Google Antigravity** $\rightarrow$ Chọn **File $\rightarrow$ Open Folder** $\rightarrow$ Chọn thư mục `the-creator-road-skill`.
2. Thả tài liệu cần đúc kết vào thư mục bài học (ví dụ `Buoi-3/`).
3. Gõ câu lệnh mẫu ở **Mục 3** bên dưới vào khung chat để AI tự động xuất ra bản đúc kết `.md` và Slide PDF Quiet Luxury!

*(Tùy chọn nâng cao: Nếu muốn tự bóc băng video nặng 4–10 GB bằng GPU máy mình, cài thêm [FFmpeg](https://www.gyan.dev/ffmpeg/builds/) qua lệnh PowerShell `winget install Gyan.FFmpeg`).*
---

## 2. BA CHẾ ĐỘ ĐÚC KẾT & 50 PHONG CÁCH SLIDE

### 2.1. Ba Chế Độ Đúc Kết
1. **`workshop` (Mặc định):** Đúc kết buổi học, khóa đào tạo, coaching, họp chiến lược (Video/Audio/Sub) $\rightarrow$ Khung 5 phần chuẩn Kaizen.
2. **`book`:** Đúc kết sách giấy, ebook, sách nói $\rightarrow$ Trích xuất mô hình cốt lõi, case study đắt giá, giới hạn áp dụng và kế hoạch chuyển hóa 7–30–90 ngày.
3. **`document`:** Đúc kết tài liệu SOP, báo cáo nghiên cứu $\rightarrow$ Tóm tắt điều hành (Executive Summary), ma trận rủi ro và checklist thực thi.

### 2.2. Danh Mục 50 Phong Cách Slide PDF (Mặc định: 01-Quiet-Luxury)
- **Luxury & Editorial (10 phong cách):** `01-quiet-luxury` *(Mặc định)*, `02-warm-cashmere`, `03-kinfolk-editorial`, `04-dark-academia`, `21-haute-couture`, `22-old-money-yacht`, `23-wabi-sabi-clay`, `24-renaissance-vellum`, `25-art-deco-gatsby`, `26-botanical-herbarium`.
- **Executive & Consulting (10 phong cách):** `05-mckinsey-executive`, `06-harvard-review`, `07-private-wealth`, `08-swiss-grid`, `27-bloomberg-terminal`, `28-financial-times`, `29-supreme-court`, `30-bain-bridge`, `31-venture-capital`, `32-esg-sustainable`.
- **Tech & Modern Bento (10 phong cách):** `09-apple-bento`, `10-linear-dark-glass`, `11-vox-explainer`, `12-cyber-matrix`, `33-cyberpunk-neon`, `34-open-source-terminal`, `35-spacex-aerospace`, `36-quantum-prism`, `37-notion-minimalist`, `38-stripe-fintech`.
- **Creative & Storytelling (10 phong cách):** `13-journal-collage`, `14-ukiyo-zen`, `15-watercolor-healing`, `16-vintage-patent`, `39-film-noir-cinema`, `40-bauhaus-primary`, `41-retro-synthwave`, `42-pop-art-warhol`, `43-comic-manga-noir`, `44-claymorphism-3d`.
- **High-Impact & Action (10 phong cách):** `17-ted-spotlight`, `18-ironman-athletic`, `19-chalkboard-masterclass`, `20-monochrome-brutalist`, `45-clinical-medical`, `46-national-geographic`, `47-mind-palace-blueprint`, `48-montessori-playful`, `49-museum-archive`, `50-zen-monastery`.

*(Chi tiết thông số màu sắc, font chữ và catalog đầy đủ xem tại file `skillCreatorRoad/references/style_gallery_guide.md`).*

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
