#!/usr/bin/env python3
"""
MI Dataset Segmenter
====================
Splits downloaded WAV files into 24-second segments.
Runs alongside the downloader — processes new files as they arrive.

Naming: {idx:03d}_{artist}_{title}_seg{seg:03d}.wav
Example: 001_Ryo_Fukui_Early_Summer_seg001.wav

Usage:
    python segment_dataset.py [--input /workspace/dataset] [--output /workspace/segments]
    python segment_dataset.py --watch   # keep watching for new files
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time

SEGMENT_DURATION = 24  # seconds
SAMPLE_RATE = 44100
CHANNELS = 1  # mono for MI pipeline
MAX_FILE_SIZE = 250 * 1024 * 1024  # 250 MB — skip likely full-album downloads


def sanitize_name(name):
    """Convert to filesystem-safe name."""
    # Replace special chars with underscore
    name = re.sub(r'[<>:"/\\|?*\'\.,()&\[\]!]+', '', name)
    # Replace spaces and multiple underscores
    name = re.sub(r'[\s\-]+', '_', name)
    name = re.sub(r'_+', '_', name)
    return name.strip('_')[:80]


def get_duration(filepath):
    """Get audio duration in seconds using ffprobe."""
    try:
        result = subprocess.run(
            [
                "ffprobe", "-v", "quiet",
                "-show_entries", "format=duration",
                "-of", "csv=p=0",
                filepath,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return float(result.stdout.strip())
    except (ValueError, subprocess.TimeoutExpired):
        return 0


def segment_file(input_path, output_dir, idx, track_info):
    """Split a single WAV file into 24-second segments."""
    duration = get_duration(input_path)
    if duration < 5:  # skip very short files
        print(f"    SKIP (too short: {duration:.1f}s)")
        return 0

    # Build base name
    artist = sanitize_name(track_info.get("artist", "Unknown"))
    title = sanitize_name(track_info.get("title", "Unknown"))
    base_name = f"{idx:03d}_{artist}_{title}"

    n_segments = int(duration // SEGMENT_DURATION)
    # Include last segment if it's at least 12 seconds (half)
    remainder = duration - (n_segments * SEGMENT_DURATION)
    if remainder >= 12:
        n_segments += 1

    if n_segments == 0:
        # File shorter than 12s, already filtered above but just in case
        return 0

    created = 0
    for seg in range(n_segments):
        start = seg * SEGMENT_DURATION
        seg_name = f"{base_name}_seg{seg + 1:03d}.wav"
        output_path = os.path.join(output_dir, seg_name)

        if os.path.exists(output_path):
            continue

        try:
            result = subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-i", input_path,
                    "-ss", str(start),
                    "-t", str(SEGMENT_DURATION),
                    "-ar", str(SAMPLE_RATE),
                    "-ac", str(CHANNELS),
                    "-acodec", "pcm_s16le",
                    output_path,
                ],
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode == 0:
                created += 1
            else:
                print(f"    ffmpeg error on seg {seg + 1}: {result.stderr[:100]}")
        except subprocess.TimeoutExpired:
            print(f"    TIMEOUT on seg {seg + 1}")

    return created


def load_track_info(dataset_dir):
    """Load track metadata from download_log.json."""
    log_path = os.path.join(dataset_dir, "download_log.json")
    if os.path.exists(log_path):
        with open(log_path) as f:
            return json.load(f)
    return {}


def parse_filename(filename):
    """Extract artist and title from downloaded filename."""
    # Format: "Artist - Title.wav"
    name = os.path.splitext(filename)[0]
    if " - " in name:
        parts = name.split(" - ", 1)
        return {"artist": parts[0].strip(), "title": parts[1].strip()}
    return {"artist": "Unknown", "title": name}


def process_dataset(input_dir, output_dir, watch=False):
    """Process all WAV files in input directory."""
    os.makedirs(output_dir, exist_ok=True)

    # Track what's already been processed
    processed_log = os.path.join(output_dir, "segment_log.json")
    processed = {}
    if os.path.exists(processed_log):
        with open(processed_log) as f:
            processed = json.load(f)

    # Build manifest for the dataset
    manifest_path = os.path.join(output_dir, "manifest.json")

    while True:
        # Find all WAV files in input
        wav_files = sorted([
            f for f in os.listdir(input_dir)
            if f.endswith(".wav") and not f.startswith(".")
        ])

        # Load download log for metadata
        dl_log = load_track_info(input_dir)

        new_count = 0
        total_segments = 0

        for i, wav_file in enumerate(wav_files, 1):
            if wav_file in processed:
                total_segments += processed[wav_file]["segments"]
                continue

            input_path = os.path.join(input_dir, wav_file)

            # Skip if file was deleted (by cleanup running in parallel)
            if not os.path.exists(input_path):
                continue

            # Check file size — skip full-album downloads
            try:
                size1 = os.path.getsize(input_path)
            except OSError:
                continue
            if size1 > MAX_FILE_SIZE:
                print(f"  [{i:3d}/{len(wav_files)}] SKIP (too large {size1//(1024*1024)}MB): {wav_file}")
                continue

            # Check if file is still being written (size changing)
            time.sleep(0.5)
            try:
                size2 = os.path.getsize(input_path)
            except OSError:
                continue
            if size1 != size2:
                continue  # still downloading

            # Get track info
            track_info = parse_filename(wav_file)

            print(f"  [{i:3d}/{len(wav_files)}] Segmenting: {wav_file}")
            duration = get_duration(input_path)
            n_created = segment_file(input_path, output_dir, i, track_info)

            if n_created > 0:
                processed[wav_file] = {
                    "idx": i,
                    "artist": track_info["artist"],
                    "title": track_info["title"],
                    "duration": round(duration, 1),
                    "segments": n_created,
                }
                total_segments += n_created
                new_count += 1

                # Save progress
                with open(processed_log, "w") as f:
                    json.dump(processed, f, indent=2, ensure_ascii=False)

                print(f"    -> {n_created} segments ({duration:.0f}s total)")

        # Build manifest
        manifest = {
            "segment_duration": SEGMENT_DURATION,
            "sample_rate": SAMPLE_RATE,
            "channels": CHANNELS,
            "total_tracks": len(processed),
            "total_segments": total_segments,
            "tracks": processed,
        }
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)

        if new_count > 0:
            print(f"\n  Processed {new_count} new tracks -> {total_segments} total segments")
            print(f"  Manifest: {manifest_path}")

        if not watch:
            break

        # Wait and check again
        print(f"\n  Watching for new files... (Ctrl+C to stop)")
        time.sleep(30)

    # Final summary
    print(f"\n=== Segmentation Complete ===")
    print(f"  Tracks:   {len(processed)}")
    print(f"  Segments: {total_segments}")
    print(f"  Output:   {output_dir}")
    seg_files = [f for f in os.listdir(output_dir) if f.endswith(".wav")]
    if seg_files:
        total_size = sum(os.path.getsize(os.path.join(output_dir, f)) for f in seg_files)
        print(f"  Size:     {total_size / (1024**3):.2f} GB")


def main():
    parser = argparse.ArgumentParser(description="MI Dataset Segmenter")
    parser.add_argument("--input", default="/workspace/dataset", help="Input directory with downloaded WAVs")
    parser.add_argument("--output", default="/workspace/segments", help="Output directory for segments")
    parser.add_argument("--watch", action="store_true", help="Keep watching for new files")
    args = parser.parse_args()

    print(f"=== MI Dataset Segmenter ===")
    print(f"  Input:    {args.input}")
    print(f"  Output:   {args.output}")
    print(f"  Segment:  {SEGMENT_DURATION}s @ {SAMPLE_RATE}Hz mono\n")

    process_dataset(args.input, args.output, args.watch)


if __name__ == "__main__":
    main()
