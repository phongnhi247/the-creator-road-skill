#!/usr/bin/env python3
"""
read_document.py — Đọc và trích xuất nội dung văn bản từ các định dạng Sách & Tài liệu (.pdf, .docx, .epub, .txt).
Phục vụ chế độ đúc kết Book và Document.
"""

import sys
from pathlib import Path


def read_pdf(path: Path) -> str:
    import pymupdf
    doc = pymupdf.open(str(path))
    chunks = []
    print(f"Đang đọc file PDF: {path.name} ({len(doc)} trang)...")
    for i, page in enumerate(doc, 1):
        txt = page.get_text("text").strip()
        if txt:
            chunks.append(f"\n--- [Trang {i:03d}] ---\n{txt}")
    doc.close()
    return "\n".join(chunks)


def read_docx(path: Path) -> str:
    import zipfile
    import xml.etree.ElementTree as ET
    print(f"Đang đọc file DOCX: {path.name}...")
    with zipfile.ZipFile(path) as z:
        xml_content = z.read("word/document.xml")
    tree = ET.fromstring(xml_content)
    paragraphs = []
    for node in tree.iter():
        if node.tag.endswith("}p"):
            texts = [elem.text for elem in node.iter() if elem.text]
            if texts:
                paragraphs.append("".join(texts))
    return "\n\n".join(paragraphs)


def read_txt(path: Path) -> str:
    print(f"Đang đọc file text: {path.name}...")
    for enc in ("utf-8", "utf-16", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    raise RuntimeError(f"Không thể đọc mã hóa file {path.name}")


def read_document(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return read_pdf(path)
    elif suffix in (".docx", ".doc"):
        return read_docx(path)
    elif suffix in (".txt", ".md", ".json", ".srt", ".vtt"):
        return read_txt(path)
    else:
        # Fallback thử pymupdf (hỗ trợ cả epub, mobi, xps, cbz...)
        try:
            import pymupdf
            doc = pymupdf.open(str(path))
            chunks = [page.get_text("text").strip() for page in doc if page.get_text("text").strip()]
            doc.close()
            return "\n\n".join(chunks)
        except Exception:
            return read_txt(path)


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Cách dùng: python read_document.py <file_sach_hoac_tai_lieu> [file_xuat.txt]")
        return
    src = Path(sys.argv[1]).resolve()
    if not src.is_file():
        print(f"Không tìm thấy file: {src}")
        sys.exit(1)
    
    content = read_document(src)
    words = len(content.split())
    print(f"=> Đã trích xuất thành công: {len(content):,} ký tự (~{words:,} từ).")

    if len(sys.argv) > 2:
        out = Path(sys.argv[2]).resolve()
        out.write_text(content, encoding="utf-8")
        print(f"=> Đã lưu ra file: {out}")
    else:
        # In ra 500 ký tự đầu để xem trước
        print("\n--- XEM TRƯỚC 500 KÝ TỰ ĐẦU ---")
        print(content[:500])


if __name__ == "__main__":
    main()
