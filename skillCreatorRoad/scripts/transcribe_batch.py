#!/usr/bin/env python3
"""
transcribe_batch.py — Tách phụ đề (.srt) và transcript từ file Video/Audio bằng GPU Local.
Lõi: faster-whisper (large-v3-turbo) trên CUDA với BatchedInferencePipeline + ffmpeg audio filter.
Tự động gộp nhiều clip lẻ (như DJI 0001..0008) thành Full_Merged.srt và Full_Transcript.txt.
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


def transcribe_one(batched_model, video_path: Path, lang: str = "vi") -> tuple[Path, list[tuple[float, float, str]], float]:
    t0 = time.time()
    srt_path = video_path.with_suffix(".srt")
    print(f"\n[1/2] Đang rút âm thanh: {video_path.name}...")
    audio = decode_audio_16k(video_path)
    duration_sec = len(audio) / 16000.0
    print(f"      Thời lượng: {duration_sec/60:.2f} phút ({duration_sec:.1f}s)")

    print(f"[2/2] Đang nhận diện giọng nói GPU Batched Inference...")
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
        "Hãy subscribe cho kênh La La School",
        "Cảm ơn các bạn đã theo dõi",
        "Hẹn gặp lại các bạn trong những video tiếp theo",
        "Các bạn hãy đăng ký kênh để ủng hộ",
    )

    items = []
    with open(srt_path, "w", encoding="utf-8") as f:
        for seg in segments:
            text = seg.text.strip()
            if not text:
                continue
            if any(h.lower() in text.lower() for h in hallucination_phrases) and (seg.end - seg.start) > 8:
                continue
            items.append((seg.start, seg.end, text))
            idx = len(items)
            f.write(f"{idx}\n{format_srt_time(seg.start)} --> {format_srt_time(seg.end)}\n{text}\n\n")

    elapsed = time.time() - t0
    print(f"=> Xuất xong: {srt_path.name} ({len(items)} đoạn | {elapsed:.1f}s)")
    return srt_path, items, duration_sec


def main() -> None:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print("Cách dùng: python transcribe_batch.py <thu_muc_buoi_hoc | file_video.mp4> [--model large-v3-turbo] [--lang vi]")
        return

    register_windows_cuda_dlls()
    import ctranslate2
    from faster_whisper import WhisperModel, BatchedInferencePipeline

    target = Path(sys.argv[1]).resolve()
    model_name = "large-v3-turbo"
    lang = "vi"

    video_files = []
    if target.is_dir():
        for ext in ("*.mp4", "*.MP4", "*.mkv", "*.mov", "*.m4a", "*.mp3", "*.wav"):
            video_files.extend(sorted(target.glob(ext)))
        seen = set()
        dedup = []
        for vf in sorted(video_files, key=lambda x: x.name.lower()):
            if vf.name.lower() not in seen:
                seen.add(vf.name.lower())
                dedup.append(vf)
        video_files = dedup
    elif target.is_file():
        video_files = [target]

    if not video_files:
        print(f"Không tìm thấy file media tại: {target}")
        sys.exit(1)

    has_cuda = ctranslate2.get_cuda_device_count() > 0
    device = "cuda" if has_cuda else "cpu"
    compute_type = "int8_float16" if device == "cuda" else "int8"

    print("=" * 60)
    print(f"BÓC BĂNG MEDIA THE CREATOR ROAD ({len(video_files)} files)")
    print(f"Thiết bị: {device.upper()} ({compute_type}) | Model: {model_name}")
    print("=" * 60)

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
        print("=" * 60)
        print("HOÀN TẤT GỘP FILE:")
        print(f"1. SRT tổng : {merged_srt.name}")
        print(f"2. Text tổng: {merged_txt.name}")
        print("=" * 60)


if __name__ == "__main__":
    main()
