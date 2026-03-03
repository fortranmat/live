#!/usr/bin/env python3
import argparse
import glob
import os
import shlex
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    process = subprocess.run(cmd)
    if process.returncode != 0:
        raise SystemExit(process.returncode)


def has_ffmpeg() -> bool:
    from shutil import which

    return which("ffmpeg") is not None


def find_single_mp3(audio_dir: Path) -> Path:
    mp3_files = sorted(audio_dir.glob("*.mp3"))
    if not mp3_files:
        raise FileNotFoundError(f"No MP3 found in {audio_dir}")
    if len(mp3_files) > 1:
        names = ", ".join(p.name for p in mp3_files)
        raise RuntimeError(f"Multiple MP3 files found in {audio_dir}: {names}. Keep exactly one.")
    return mp3_files[0]


def find_images(images_dir: Path) -> list[Path]:
    patterns = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]
    files: list[Path] = []
    for pattern in patterns:
        files.extend(images_dir.glob(pattern))
    uniq = sorted(set(files))
    if len(uniq) < 1:
        raise RuntimeError(f"Need at least 1 image in {images_dir}. Found {len(uniq)}.")
    return uniq


def build_filter_complex(image_count: int, hold_seconds: int) -> str:
    parts = []
    for idx in range(image_count):
        parts.append(
            f"[{idx}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            f"zoompan=z='min(zoom+0.0003,1.08)':d={hold_seconds*30}:s=1920x1080:fps=30,"
            f"setsar=1[v{idx}]"
        )

    concat_inputs = "".join(f"[v{i}]" for i in range(image_count))
    parts.append(f"{concat_inputs}concat=n={image_count}:v=1:a=0[vcat]")
    return ";".join(parts)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create long live-ready video from 1 MP3 + one or more images.")
    parser.add_argument("--project-root", default=".", help="Project root path")
    parser.add_argument("--hours", type=float, default=8.0, help="Target output duration in hours")
    parser.add_argument("--hold-seconds", type=int, default=12, help="Seconds each image stays before switching")
    parser.add_argument("--output-name", default="live_8h_1080p.mp4", help="Output filename")
    args = parser.parse_args()

    if args.hours <= 0:
        raise SystemExit("--hours must be > 0")
    if args.hold_seconds <= 0:
        raise SystemExit("--hold-seconds must be > 0")

    root = Path(args.project_root).resolve()
    input_root = root / "11_user_input"
    audio_dir = input_root / "audio"
    images_dir = input_root / "images"
    output_dir = input_root / "output"

    if not has_ffmpeg():
        raise SystemExit("ffmpeg is not installed. Install it first (sudo apt install ffmpeg).")

    output_dir.mkdir(parents=True, exist_ok=True)

    mp3 = find_single_mp3(audio_dir)
    images = find_images(images_dir)

    filter_complex = build_filter_complex(len(images), args.hold_seconds)
    out_path = output_dir / args.output_name
    duration_seconds = int(args.hours * 3600)

    cmd = ["ffmpeg", "-y"]

    for image in images:
        cmd += ["-loop", "1", "-t", str(args.hold_seconds), "-i", str(image)]

    cmd += [
        "-stream_loop",
        "-1",
        "-i",
        str(mp3),
        "-filter_complex",
        filter_complex,
        "-map",
        "[vcat]",
        "-map",
        f"{len(images)}:a",
        "-t",
        str(duration_seconds),
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-pix_fmt",
        "yuv420p",
        "-r",
        "30",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(out_path),
    ]

    print("Running FFmpeg command:\n")
    print(" ".join(shlex.quote(x) for x in cmd))
    run(cmd)

    print(f"\nDone. Output: {out_path}")


if __name__ == "__main__":
    main()
