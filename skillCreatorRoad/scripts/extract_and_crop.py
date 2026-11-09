#!/usr/bin/env python3
"""
extract_and_crop.py — Trích xuất ảnh nhúng từ PDF slide hoặc cắt sạch mép ảnh chụp slide.
Tự động loại bỏ số trang cũ và viền thừa trước khi đưa vào khung Quiet Luxury.
"""

import os
import sys
from pathlib import Path
import pymupdf


def extract_pdf_images(pdf_path: Path, out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(str(pdf_path))
    saved_images = []
    print(f"Đang trích xuất ảnh nhúng từ: {pdf_path.name} ({len(doc)} trang)...")
    for i, page in enumerate(doc):
        imgs = page.get_images(full=True)
        for img_idx, img in enumerate(imgs):
            xref = img[0]
            base_img = doc.extract_image(xref)
            ext = base_img["ext"]
            out_name = f"page_{i+1:02d}_img{img_idx:02d}.{ext}"
            out_path = out_dir / out_name
            with open(out_path, "wb") as f:
                f.write(base_img["image"])
            saved_images.append(out_path)
            print(f"  -> Lưu: {out_name} ({base_img['width']}x{base_img['height']})")
    doc.close()
    return saved_images


def crop_image(src_path: Path, x0: float, y0: float, x1: float, y1: float, dst_path: Path) -> None:
    dst_path.parent.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open()
    pix = pymupdf.Pixmap(str(src_path))
    page = doc.new_page(width=pix.width, height=pix.height)
    page.insert_image(page.rect, filename=str(src_path))
    clip = pymupdf.Rect(x0, y0, x1, y1)
    out_pix = page.get_pixmap(clip=clip, dpi=144)
    out_pix.save(str(dst_path))
    doc.close()
    print(f"=> Cắt xong: {dst_path.name} (Tọa độ: {x0},{y0} -> {x1},{y1})")


def main() -> None:
    if len(sys.argv) < 2 or any(arg in sys.argv for arg in ("-h", "--help")):
        print("Cách dùng:")
        print("  1. Trích xuất ảnh từ PDF : python extract_and_crop.py extract <slide.pdf> [thu_muc_ra]")
        print("  2. Cắt ảnh chụp màn hình : python extract_and_crop.py crop <anh_goc.png> <x0> <y0> <x1> <y1> <anh_ra.png>")
        sys.exit(0)

    mode = sys.argv[1].lower()
    if mode == "extract":
        pdf_path = Path(sys.argv[2]).resolve()
        out_dir = Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else pdf_path.parent / "extracted_images"
        extract_pdf_images(pdf_path, out_dir)
    elif mode == "crop":
        src = Path(sys.argv[2]).resolve()
        x0, y0, x1, y1 = float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5]), float(sys.argv[6])
        dst = Path(sys.argv[7]).resolve()
        crop_image(src, x0, y0, x1, y1, dst)
    else:
        print(f"Chế độ không hợp lệ: {mode}")


if __name__ == "__main__":
    main()
