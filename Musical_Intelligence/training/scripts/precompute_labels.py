"""Pre-compute MI Teacher labels for an entire audio corpus.

For each audio file:
1. Load audio -> mel spectrogram
2. R3Extractor(mel) -> R3 features (128D)
3. H3Extractor(r3, demand) -> H3 features (sparse, SLOW: ~146s/30s)
4. BrainOrchestrator(h3, r3) -> C3 output (1006D)
5. H3Densifier(h3) -> dense tensor (~5210D)
6. Save all to HDF5 via PrecomputeCache

Usage::

    python -m Musical_Intelligence.training.scripts.precompute_labels \\
        --input_dir /path/to/audio \\
        --output_dir /path/to/cache \\
        --max_duration 60 \\
        --workers 4
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path
from typing import List

import torch


def find_audio_files(input_dir: Path) -> List[Path]:
    """Find all supported audio files recursively."""
    extensions = {".wav", ".flac", ".mp3", ".ogg", ".m4a", ".aac"}
    files = []
    for ext in extensions:
        files.extend(input_dir.rglob(f"*{ext}"))
    return sorted(files)


def precompute_single(
    audio_path: Path,
    output_dir: Path,
    max_duration_s: float | None = None,
) -> bool:
    """Pre-compute labels for a single audio file.

    Returns True if successful, False if skipped or failed.
    """
    from Musical_Intelligence.data.preprocessing import (
        compute_mel,
        load_audio,
    )
    from Musical_Intelligence.data.precompute_cache import PrecomputeCache
    from Musical_Intelligence.training.teacher.mi_teacher import MITeacher

    cache = PrecomputeCache(str(output_dir))
    track_id = audio_path.stem

    # Skip if already cached
    if cache.has(track_id):
        print(f"  SKIP {track_id} (already cached)")
        return False

    t0 = time.time()

    # Load and preprocess
    waveform, sr = load_audio(audio_path)
    if max_duration_s is not None:
        max_samples = int(max_duration_s * sr)
        if waveform.shape[-1] > max_samples:
            waveform = waveform[:, :max_samples]

    duration_s = waveform.shape[-1] / sr
    mel = compute_mel(waveform, sr=sr)  # (1, 128, T)

    # Run MI Teacher pipeline
    teacher = MITeacher()
    output = teacher.compute(mel)

    # Save to cache (squeeze batch dim for storage)
    cache.save(
        track_id=track_id,
        mel=output.mel.squeeze(0),           # (T, 128)
        r3=output.r3.squeeze(0),             # (T, 128)
        h3_dense=output.h3_dense.squeeze(0), # (T, N)
        c3=output.c3.squeeze(0),             # (T, 1006)
        metadata={
            "source": str(audio_path),
            "duration_s": round(duration_s, 2),
            "n_frames": output.mel.shape[1],
        },
    )

    elapsed = time.time() - t0
    print(
        f"  DONE {track_id}: {duration_s:.1f}s audio -> "
        f"{output.mel.shape[1]} frames in {elapsed:.1f}s"
    )
    return True


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pre-compute MI Teacher labels for audio corpus."
    )
    parser.add_argument(
        "--input_dir", type=str, required=True,
        help="Directory containing audio files.",
    )
    parser.add_argument(
        "--output_dir", type=str, required=True,
        help="Directory to store HDF5 label cache.",
    )
    parser.add_argument(
        "--max_duration", type=float, default=None,
        help="Maximum audio duration in seconds (truncate longer files).",
    )
    parser.add_argument(
        "--workers", type=int, default=1,
        help="Number of parallel workers (default 1, sequential).",
    )
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)

    if not input_dir.exists():
        print(f"ERROR: Input directory not found: {input_dir}")
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)

    audio_files = find_audio_files(input_dir)
    print(f"Found {len(audio_files)} audio files in {input_dir}")

    if not audio_files:
        print("No audio files found. Exiting.")
        sys.exit(0)

    processed = 0
    skipped = 0

    for i, path in enumerate(audio_files):
        print(f"[{i + 1}/{len(audio_files)}] {path.name}")
        try:
            did_process = precompute_single(
                path, output_dir, max_duration_s=args.max_duration
            )
            if did_process:
                processed += 1
            else:
                skipped += 1
        except Exception as e:
            print(f"  ERROR: {e}")
            skipped += 1

    print(f"\nDone: {processed} processed, {skipped} skipped.")


if __name__ == "__main__":
    main()
