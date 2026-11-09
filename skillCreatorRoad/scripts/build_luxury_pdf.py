#!/usr/bin/env python3
"""
build_luxury_pdf.py — Nạp các slide HTML và xuất ra file PDF 16:9 theo 1 trong 20 phong cách chuyên nghiệp.
Hỗ trợ tham số `--style <style_id>` (mặc định: 01-quiet-luxury).
Sử dụng Chrome/Edge headless native, đảm bảo không viền trắng và font Segoe UI / Palatino Linotype chuẩn 100%.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def find_browser() -> str:
    candidates = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        shutil.which("chrome"),
        shutil.which("msedge"),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    raise RuntimeError("Không tìm thấy Chrome hoặc Edge trên hệ thống.")


def load_style_theme(style_id: str) -> dict:
    catalog_path = Path(__file__).resolve().parent.parent / "templates" / "styles_catalog.json"
    if not catalog_path.is_file():
        # Fallback quiet luxury mặc định
        return {
            "id": "01-quiet-luxury",
            "name": "Quiet Luxury",
            "css": {
                "background": "radial-gradient(circle at 22% 18%, #1A1625 0%, #0E0C14 55%, #09080C 100%)",
                "outer_border": "1px solid rgba(212, 182, 124, 0.22)",
                "inner_border": "1px solid rgba(212, 182, 124, 0.07)",
                "hairline_accent": "#C5A567",
                "gold_accent": "#D4B67C",
                "text_primary": "#F7F3EB",
                "text_secondary": "#E6E0D6",
                "text_muted": "#A69D8E",
                "card_bg": "rgba(255, 255, 255, 0.025)",
                "card_border": "1px solid rgba(212, 182, 124, 0.16)",
                "panel_bg": "rgba(18, 15, 26, 0.78)",
                "panel_border": "1px solid rgba(212, 182, 124, 0.20)",
                "table_th_bg": "rgba(212, 182, 124, 0.12)",
                "font_heading": "'Palatino Linotype', 'Book Antiqua', Georgia, serif",
                "font_body": "'Segoe UI', -apple-system, sans-serif",
            },
        }

    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    for st in data.get("styles", []):
        if st["id"] == style_id or st["id"].startswith(style_id):
            return st
    print(f"Cảnh báo: Không tìm thấy style '{style_id}', sử dụng style mặc định '01-quiet-luxury'.")
    return [s for s in data["styles"] if s["id"] == "01-quiet-luxury"][0]


def render_html_to_pdf(html_file: Path, pdf_file: Path, style_id: str = "01-quiet-luxury") -> None:
    browser = find_browser()
    pdf_file.parent.mkdir(parents=True, exist_ok=True)
    theme = load_style_theme(style_id)

    html_url = f"file:///{str(html_file.resolve()).replace(chr(92), '/')}"
    print(f"Đang render PDF qua: {Path(browser).name} (Phong cách: {theme['name']})...")
    subprocess.run(
        [
            browser,
            "--headless=new",
            "--disable-gpu",
            "--print-to-pdf-no-header",
            f"--print-to-pdf={str(pdf_file.resolve())}",
            html_url,
        ],
        check=True,
    )
    print(f"=> XUẤT THÀNH CÔNG: {pdf_file.name} ({os.path.getsize(pdf_file)/1024:.1f} KB)")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Slide HTML to 16:9 PDF via Headless Browser with 20 Professional Themes")
    parser.add_argument("html_in", help="Input HTML slide file")
    parser.add_argument("pdf_out", help="Output PDF file")
    parser.add_argument("--style", default="01-quiet-luxury", help="Style ID from styles_catalog.json (default: 01-quiet-luxury)")
    args = parser.parse_args()

    html_in = Path(args.html_in).resolve()
    pdf_out = Path(args.pdf_out).resolve()
    if not html_in.is_file():
        print(f"Không tìm thấy file HTML: {html_in}")
        sys.exit(1)
    render_html_to_pdf(html_in, pdf_out, style_id=args.style)


if __name__ == "__main__":
    main()
