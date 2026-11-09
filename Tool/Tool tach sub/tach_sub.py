#!/usr/bin/env python3
"""
Công cụ tách phụ đề (.srt) trực tiếp từ file Video/Audio bằng GPU Local (faster-whisper large-v3-turbo).
Sử dụng BatchedInferencePipeline + lọc âm highpass/dynaudnorm giúp tốc độ nhanh gấp 5 lần và chống lặp chữ.
"""

import os
import site
import subprocess
import sys
import time
from pathlib import Path
import numpy as np

os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")


def register_windows_cuda_dlls() -> None:
    if os.name != "nt" or not hasattr(os, "add_dll_directory"):
        return
    for base in site.getsitepackages() + [site.getusersitepackages()]:
        if not base:
            continue
        nvidia_root = Path(base) / "nvidia"
        if nvidia_root.is_dir():
            for bin_dir in nvidia_root.glob("*/bin"):
                if bin_dir.is_dir():
                    try:
                        os.add_dll_directory(str(bin_dir))
                        os.environ["PATH"] = str(bin_dir) + os.pathsep + os.environ.get("PATH", "")
                    except OSError:
                        pass


def format_srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h = ms // 3_600_000
    ms %= 3_600_000
    m = ms // 60_000
    ms %= 60_000
    s = ms // 1000
    ms %= 1000
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def decode_audio_16k(path: Path) -> np.ndarray:
    res = subprocess.run(
        [
            "ffmpeg",
            "-v",
            "error",
            "-i",
            str(path),
            "-vn",
            "-af",
            "highpass=f=80,dynaudnorm=p=0.9:s=5",
            "-ac",
            "1",
            "-ar",
            "16000",
            "-f",
            "s16le",
            "-",
        ],
        capture_output=True,
        check=True,
    )
    return np.frombuffer(res.stdout, dtype=np.int16).astype(np.float32) / 32768.0


def pick_file_gui() -> list[str]:
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        file_paths = filedialog.askopenfilenames(
            title="Chọn 1 hoặc nhiều file Video/Audio cần tách phụ đề (.srt)",
            filetypes=[
                ("Video / Audio files", "*.mp4 *.MP4 *.mkv *.mov *.avi *.webm *.mp3 *.m4a *.wav"),
                ("All files", "*.*"),
            ],
        )
        root.destroy()
        return list(file_paths) if file_paths else []
    except Exception:
        return []


def transcribe_one(batched_model, video_path: Path, lang: str = "vi") -> tuple[Path, list[tuple[float, float, str]], float]:
    t0 = time.time()
    srt_path = video_path.with_suffix(".srt")
    print(f"\n------------------------------------------------------------")
    print(f"[1/2] Đang trích xuất âm thanh: {video_path.name} ...")
    audio = decode_audio_16k(video_path)
    duration_sec = len(audio) / 16000.0
    print(f"      Thời lượng: {duration_sec/60:.2f} phút ({duration_sec:.1f}s)")

    print(f"[2/2] Đang nhận diện giọng nói bằng GPU (Batched Inference)...")
    segments, _ = batched_model.transcribe(
        audio,
        language=lang,
        batch_size=16,
        chunk_length=15,
        condition_on_previous_text=False,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 300, "max_speech_duration_s": 15},
    )

    hallucination_phrases = (
        "Hãy subscribe cho kênh Ghiền Mì Gõ",
        "Cảm ơn các bạn đã theo dõi",
        "Hẹn gặp lại các bạn trong những video tiếp theo",
    )

    items = []
    with open(srt_path, "w", encoding="utf-8") as f:
        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue
            if any(h.lower() in text.lower() for h in hallucination_phrases) and (seg.end - seg.start) > 10:
                continue
            items.append((seg.start, seg.end, text))
            idx = len(items)
            f.write(f"{idx}\n{format_srt_time(seg.start)} --> {format_srt_time(seg.end)}\n{text}\n\n")

    elapsed = time.time() - t0
    print(f"=> Đã lưu: {srt_path.name} ({len(items)} đoạn | xử lý trong {elapsed:.1f}s)")
    return srt_path, items, duration_sec


def main() -> None:
    if "--help" in sys.argv or "-h" in sys.argv:
        print("Cách dùng: python tach_sub.py [video1.mp4 video2.mp4 | thu_muc] [--model large-v3-turbo] [--lang vi]")
        return

    register_windows_cuda_dlls()
    import ctranslate2
    from faster_whisper import WhisperModel, BatchedInferencePipeline

    input_args = []
    model_name = "large-v3-turbo"
    lang = "vi"

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--model" and i + 1 < len(args):
            model_name = args[i + 1]
            i += 2
        elif args[i] == "--lang" and i + 1 < len(args):
            lang = args[i + 1]
            i += 2
        else:
            input_args.append(args[i])
            i += 1

    if not input_args:
        print("Đang mở cửa sổ chọn file video/audio...")
        input_args = pick_file_gui()
        if not input_args:
            print("Đã hủy chọn file.")
            return

    video_files: list[Path] = []
    for arg in input_args:
        p = Path(arg).resolve()
        if p.is_dir():
            for ext in ("*.mp4", "*.MP4", "*.mkv", "*.mov", "*.m4a", "*.mp3", "*.wav"):
                video_files.extend(sorted(p.glob(ext)))
            # Deduplicate case-insensitive on Windows
            seen = set()
            dedup = []
            for vf in sorted(video_files, key=lambda x: x.name.lower()):
                if vf.name.lower() not in seen:
                    seen.add(vf.name.lower())
                    dedup.append(vf)
            video_files = dedup
        elif p.is_file():
            video_files.append(p)

    if not video_files:
        print("Không tìm thấy file video/audio hợp lệ.")
        sys.exit(1)

    try:
        has_cuda = ctranslate2.get_cuda_device_count() > 0
    except Exception:
        has_cuda = False
    device = "cuda" if has_cuda else "cpu"
    compute_type = "int8_float16" if device == "cuda" else "int8"

    print("============================================================")
    print(f"Tổng số file cần tách sub: {len(video_files)}")
    print(f"Thiết bị chạy: {device.upper()} ({compute_type}) | Model: {model_name}")
    print("============================================================")

    model = WhisperModel(model_name, device=device, compute_type=compute_type)
    batched = BatchedInferencePipeline(model=model)

    combined_items = []
    time_offset = 0.0
    for vf in video_files:
        _, items, dur = transcribe_one(batched, vf, lang=lang)
        for st, et, txt in items:
            combined_items.append((time_offset + st, time_offset + et, f"[{vf.stem}] {txt}", txt))
        time_offset += dur

    if len(video_files) > 1:
        parent_dir = video_files[0].parent
        merged_srt = parent_dir / f"{parent_dir.name}_Full_Merged.srt"
        merged_txt = parent_dir / f"{parent_dir.name}_Full_Transcript.txt"
        with open(merged_srt, "w", encoding="utf-8") as fsrt, open(merged_txt, "w", encoding="utf-8") as ftxt:
            cur_clip = None
            for idx, (st, et, tagged_txt, raw_txt) in enumerate(combined_items, 1):
                fsrt.write(f"{idx}\n{format_srt_time(st)} --> {format_srt_time(et)}\n{raw_txt}\n\n")
                clip_tag = tagged_txt.split("]")[0] + "]"
                if clip_tag != cur_clip:
                    cur_clip = clip_tag
                    ftxt.write(f"\n\n=== {cur_clip} (Mốc {format_srt_time(st)}) ===\n")
                ftxt.write(f"[{format_srt_time(st)}] {raw_txt}\n")
        print("\n============================================================")
        print(f"ĐÃ GỘP TOÀN BỘ {len(video_files)} FILE THÀNH:")
        print(f"1. File SRT tổng : {merged_srt}")
        print(f"2. File Text tổng: {merged_txt}")
        print("============================================================")


if __name__ == "__main__":
    main()
