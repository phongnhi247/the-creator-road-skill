---
name: creator-road
description: "Quy trình trọn gói tự động đúc kết Buổi học (Workshop), Sách (Book) và Tài liệu (Document) thành Bản đúc kết chuyên sâu (.md) sạch và Bộ Slide PDF Widescreen 16:9 với 20 phong cách chuyên nghiệp (Mặc định: 01-quiet-luxury; cùng 19 phong cách McKinsey, Apple Bento, Harvard, Dark Academia, v.v.). Không lỗi font tiếng Việt, không tràn khung, tự động crop ảnh gốc."
category: content-distillation
keywords: [creator-road, book-summary, document-distillation, quiet-luxury, mckinsey-slides, bento-grid, star-method, presentation-pdf]
metadata:
  author: creator-road-core
  version: "2.0.0"
---

# Skill: `creator-road` — Đúc Kết Sách, Tài Liệu & Slide PDF 20 Phong Cách

Skill này chuẩn hóa toàn bộ quy trình tiếp nhận nguyên liệu đa định dạng (**Workshop**, **Sách**, **Tài liệu/Báo cáo/SOP**), bóc tách tri thức lõi và xuất bản tài liệu kép:
1. **Bản đúc kết chuyên sâu (`.md`):** Tự động điều chỉnh theo 3 chế độ (*Workshop*, *Book*, *Document*), loại bỏ lan man, tự động sửa lỗi chính tả giọng nói theo Từ điển nội bộ.
2. **Bộ Slide PDF Widescreen 16:9 (`.pdf`):** Hỗ trợ **20 phong cách thiết kế chuyên nghiệp** (mặc định là **`01-quiet-luxury`** chuẩn mực, không bao giờ thay đổi), không lỗi font, không tràn chữ, tự động ghép ảnh minh họa sạch mép.

---

## 1. Ba Chế Độ Đúc Kết (3 Distillation Modes)

Skill tự động nhận diện hoặc nhận chỉ định chế độ qua câu lệnh:

| Chế độ | Đầu vào nhận diện | Khung đúc kết chuẩn mực (.md & Slide) |
| :--- | :--- | :--- |
| **1. `workshop` (Mặc định)** | Video (`.mp4`), Audio (`.m4a`/`.mp3`), Phụ đề (`.srt`) + Slide gốc | **Chuẩn 6 Tầng (1 Trụ cột cốt lõi = 1 Slide):** Tổng quan & 6 Thông điệp cốt lõi $\rightarrow$ 3–5 Slide Trụ cột 6 tầng (Chân lý, Cơ chế, Bẫy học viên hay mắc, Kỹ thuật bài tập, Tiêu chuẩn đạt DoD, Tự vấn) $\rightarrow$ Bảng khó khăn STAR $\rightarrow$ Checklist 7-30-90 ngày. |
| **2. `book` (Đúc kết Sách)** | Sách `.pdf`, `.epub`, `.docx`, `.txt` hoặc audio sách nói | **Chuẩn 6 Tầng (1 Bài học/Chương = 1 Slide):** Bối cảnh & 6 Luận điểm gốc $\rightarrow$ Giải phẫu chi tiết toàn bộ các bài học theo Khung 6 Tầng (Axiom, Mechanism, Pitfall, Drill, DoD, Reflection) $\rightarrow$ Case study $\rightarrow$ Checklist hành động & Tóm tắt 1 trang. |
| **3. `document` (Tài liệu / SOP)** | File `.pdf`, `.docx`, `.md`, báo cáo thị trường, quy trình nội bộ | **5 Phần:** Tóm tắt điều hành (Executive Summary) $\rightarrow$ Hệ thống Khái niệm, Số liệu & Quy trình lõi $\rightarrow$ Ma trận phân tích rủi ro & điểm nghẽn $\rightarrow$ Giải pháp theo nguyên nhân gốc $\rightarrow$ Checklist thực thi & KPIs. |
---

## 2. Danh Mục 20 Phong Cách Slide PDF (Mặc định: 01-Quiet-Luxury)

Chi tiết thông số màu sắc, font chữ và câu lệnh tạo ảnh xem tại `references/style_gallery_guide.md`:

- **Nhóm Luxury & Editorial:** `01-quiet-luxury` *(Mặc định)*, `02-warm-cashmere`, `03-kinfolk-editorial`, `04-dark-academia`.
- **Nhóm Executive & Consulting:** `05-mckinsey-executive`, `06-harvard-review`, `07-private-wealth`, `08-swiss-grid`.
- **Nhóm Tech & Modern Bento:** `09-apple-bento`, `10-linear-dark-glass`, `11-vox-explainer`, `12-cyber-matrix`.
- **Nhóm Creative & Storytelling:** `13-journal-collage`, `14-ukiyo-zen`, `15-watercolor-healing`, `16-vintage-patent`.
- **Nhóm High-Impact & Action:** `17-ted-spotlight`, `18-ironman-athletic`, `19-chalkboard-masterclass`, `20-monochrome-brutalist`.

---

## 3. Quy Trình Vận Hành Chuẩn 5 Bước

<critical>
### NGUYÊN TẮC CỐT LÕI (MANDATORY GATEKEEPER):
**BẮT BUỘC TRẢ VĂN BẢN .MD TRƯỚC KHI TẠO SLIDE:**
- Ở mọi chế độ (*Workshop*, *Book*, *Document*), AI BẮT BUỘC phải biên soạn hoàn thiện, chuyên sâu và gửi bản đúc kết (`.md`) cho người dùng duyệt, góp ý trước khi tiến hành bất kỳ bước tạo slide nào.
- Tuyệt đối KHÔNG nhảy cóc sang thiết kế, tạo mã nguồn HTML hay xuất file Slide PDF khi người dùng chưa đọc và duyệt nội dung đúc kết `.md`.
</critical>

```text
[Bước 1: Tiếp nhận & Phân loại Đầu vào]
  ├── Workshop: transcribe_batch.py (Bóc sub GPU local) + extract_and_crop.py
  ├── Sách / Tài liệu: read_document.py (Trích xuất văn bản từ PDF, DOCX, TXT)
        ↓
[Bước 2: Soạn thảo Bản Đúc Kết (.md) theo đúng Mode (Workshop/Book/Document)]
  └── Tự động chuẩn hóa Từ điển tên riêng -> Xuất bản Text sạch -> GỬI DUYỆT BẮT BUỘC
        ↓ (CHỈ TIẾP TỤC SAU KHI USER DUYỆT NỘI DUNG .MD)
[Bước 3: Chọn Phong Cách Slide (Mặc định: 01-quiet-luxury hoặc 1 trong 20 styles)]
  └── Render 1 trang tiêu biểu kiểm tra bố cục & màu sắc -> Gửi duyệt phong cách
        ↓
[Bước 4: Xuất Full Slide PDF (16:9 qua build_luxury_pdf.py)]
  └── Kiểm tra nghiêm ngặt không trùng lặp, không tràn khung -> In PDF qua Chrome
        ↓
[Bước 5: Đóng gói & Gom Thư Mục Hoàn Chỉnh]
  └── Gom toàn bộ file vào thư mục buổi học / sách tương ứng
```
---

## 4. Hướng Dẫn Sử Dụng Bộ Scripts Kỹ Thuật

Sử dụng môi trường Python venv của dự án (`D:\Project\VIDEO\herk-edit-kit\.venv\Scripts\python.exe`):

1. **Bóc băng Video/Audio hàng loạt (GPU local):**
   ```bash
   python skillCreatorRoad/scripts/transcribe_batch.py "Buoi-X"
   ```
2. **Đọc văn bản từ Sách & Tài liệu (.pdf, .docx, .epub, .txt):**
   ```bash
   python skillCreatorRoad/scripts/read_document.py "path/to/cuon-sach.pdf" "output.txt"
   ```
3. **Trích xuất ảnh nhúng từ PDF slide hoặc cắt ảnh chụp màn hình:**
   ```bash
   python skillCreatorRoad/scripts/extract_and_crop.py extract "slide.pdf" "images/"
   python skillCreatorRoad/scripts/extract_and_crop.py crop "screen.png" 0 0 1660 825 "clean.png"
   ```
4. **Xuất Slide PDF 16:9 theo phong cách chỉ định:**
   ```bash
   # Mặc định Quiet Luxury
   python skillCreatorRoad/scripts/build_luxury_pdf.py "slides.html" "output.pdf"

   # Hoặc chọn phong cách khác (ví dụ: mckinsey, apple-bento, dark-academia...)
   python skillCreatorRoad/scripts/build_luxury_pdf.py "slides.html" "output.pdf" --style 05-mckinsey-executive
   ```

---

## 5. Mẫu Câu Lệnh (Prompt) Nhanh Khi Ra Lệnh Cho AI

- **Đúc kết Buổi học (Mặc định Quiet Luxury):**
  > *"Áp dụng skill `creator-road`: Hãy xử lý thư mục `Buoi-[X]`. Bước 1: Xuất bản text đúc kết (`.md`) sạch, chuẩn Kaizen để tôi duyệt. Bước 2: Test 1 ảnh slide Quiet Luxury kèm ảnh gốc để tôi duyệt rồi hãy xuất full PDF nhé."*
- **Đúc kết Sách:**
  > *"Áp dụng skill `creator-road` chế độ `book`: Hãy phân tích cuốn sách `[ten_sach.pdf]`. Xuất bản đúc kết `.md` chuyên sâu cho sách và thiết kế slide PDF theo phong cách `04-dark-academia` (hoặc `02-warm-cashmere`)."*
- **Đúc kết Tài liệu / Báo cáo:**
  > *"Áp dụng skill `creator-road` chế độ `document`: Hãy phân tích tài liệu `[file.docx]`. Xuất bản đúc kết tóm tắt điều hành và slide PDF theo phong cách `05-mckinsey-executive`."*
