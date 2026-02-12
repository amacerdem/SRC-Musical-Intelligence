#!/usr/bin/env python3
"""
export_mi_binary.py — MI Pipeline → .mi.bin binary export for web demo.

Binary format (MI01):
  HEADER       32 bytes
  DIM_INDEX    307 × 32 bytes  (~10 KB)
  FRAME_DATA   T × 307 × 2 bytes  (Float16, row-major)

Usage:
  python export_mi_binary.py                           # Swan Lake (default)
  python export_mi_binary.py --audio path/to/file.wav  # Custom audio
  python export_mi_binary.py --output data/out.mi.bin  # Custom output path
"""

from __future__ import annotations

import argparse
import json
import struct
import sys
from pathlib import Path

import numpy as np
import torch

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(PROJECT_ROOT))

from importlib import import_module


# ═══════════════════════════════════════════════════════════════════════
# BINARY FORMAT CONSTANTS
# ═══════════════════════════════════════════════════════════════════════

MAGIC = b"MI01"
VERSION = 1
TOTAL_DIM = 307  # 128 + 49 + 26 + 104
DIM_NAME_SIZE = 32  # bytes per dimension name (zero-padded ASCII)

HEADER_SIZE = 32
DIM_INDEX_SIZE = TOTAL_DIM * DIM_NAME_SIZE  # 9,824 bytes


# ═══════════════════════════════════════════════════════════════════════
# MI PIPELINE RUNNER
# ═══════════════════════════════════════════════════════════════════════

def run_pipeline(audio_path: str) -> dict:
    """Run MI pipeline on audio file. Returns dict with tensors + metadata."""
    import soundfile as sf
    import librosa

    # Load audio with soundfile/librosa (torchaudio 2.10 requires torchcodec)
    audio_np, sr = sf.read(audio_path)
    if audio_np.ndim > 1:
        audio_np = audio_np.mean(axis=1)
    if sr != 44100:
        audio_np = librosa.resample(audio_np, orig_sr=sr, target_sr=44100)
        sr = 44100
    waveform = torch.from_numpy(audio_np).float().unsqueeze(0)  # (1, samples)

    duration_ms = int(waveform.shape[-1] / sr * 1000)
    print(f"  Audio: {duration_ms / 1000:.1f}s, {sr}Hz, {waveform.shape[-1]} samples")

    # Import MI pipeline
    mi_pkg = import_module("Musical Intelligence.mi.pipeline.mi")
    MIPipeline = mi_pkg.MIPipeline

    pipeline = MIPipeline()
    output = pipeline.process(waveform, return_ear=True, return_semantics=True)

    # Extract tensors — all (B=1, T, D) or (B=1, D, T)
    cochlea_mel = output.ear.cochlea.mel  # (1, 128, T) — needs transpose
    r3_features = output.ear.r3.features  # (1, T, 49)
    brain_tensor = output.brain.tensor     # (1, T, 26)
    l3_tensor = output.semantics.tensor    # (1, T, 104)

    # Transpose cochlea to (1, T, 128)
    cochlea_t = cochlea_mel.permute(0, 2, 1)  # (1, T, 128)

    T = r3_features.shape[1]
    print(f"  Frames: {T} @ 172.27 Hz")

    # Verify cochlea T matches
    cochlea_T = cochlea_t.shape[1]
    if cochlea_T != T:
        # Trim or pad to match
        min_T = min(cochlea_T, T)
        cochlea_t = cochlea_t[:, :min_T, :]
        r3_features = r3_features[:, :min_T, :]
        brain_tensor = brain_tensor[:, :min_T, :]
        l3_tensor = l3_tensor[:, :min_T, :]
        T = min_T
        print(f"  Aligned to {T} frames")

    # Concatenate: (1, T, 307)
    mi_space = torch.cat([cochlea_t, r3_features, brain_tensor, l3_tensor], dim=-1)
    assert mi_space.shape == (1, T, TOTAL_DIM), f"Expected (1, {T}, {TOTAL_DIM}), got {mi_space.shape}"

    # Collect dimension names
    dim_names = []

    # Cochlea: mel_0 .. mel_127
    dim_names.extend([f"mel_{i}" for i in range(128)])

    # R³: from feature_names
    dim_names.extend(list(output.ear.r3.feature_names))

    # Brain: from DIMENSION_NAMES
    dim_names.extend(list(output.brain.dimension_names))

    # L³: from semantic groups
    for group_name in ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]:
        group = output.semantics.groups[group_name]
        dim_names.extend(list(group.dimension_names))

    assert len(dim_names) == TOTAL_DIM, f"Expected {TOTAL_DIM} names, got {len(dim_names)}"

    return {
        "mi_space": mi_space[0].detach().cpu(),  # (T, 307) float32
        "dim_names": dim_names,
        "n_frames": T,
        "sample_rate": 44100,
        "hop_length": 256,
        "duration_ms": duration_ms,
    }


# ═══════════════════════════════════════════════════════════════════════
# BINARY WRITER
# ═══════════════════════════════════════════════════════════════════════

def write_mi_bin(data: dict, output_path: str) -> None:
    """Write MI01 binary file."""
    mi_space = data["mi_space"]  # (T, 307) float32
    T, D = mi_space.shape
    assert D == TOTAL_DIM

    with open(output_path, "wb") as f:
        # ─── HEADER (32 bytes) ───────────────────────────────
        f.write(MAGIC)                                          # [0:4]
        f.write(struct.pack("<I", VERSION))                     # [4:8]
        f.write(struct.pack("<I", T))                           # [8:12]
        f.write(struct.pack("<I", D))                           # [12:16]
        f.write(struct.pack("<I", data["sample_rate"]))         # [16:20]
        f.write(struct.pack("<I", data["hop_length"]))          # [20:24]
        f.write(struct.pack("<I", data["duration_ms"]))         # [24:28]
        f.write(struct.pack("<I", 0))                           # [28:32] reserved

        # ─── DIMENSION INDEX (307 × 32 bytes) ────────────────
        for name in data["dim_names"]:
            encoded = name.encode("ascii")[:DIM_NAME_SIZE]
            padded = encoded.ljust(DIM_NAME_SIZE, b"\x00")
            f.write(padded)

        # ─── FRAME DATA (T × 307 × Float16) ──────────────────
        # Convert to float16 numpy array
        frames_f16 = mi_space.numpy().astype(np.float16)
        f.write(frames_f16.tobytes())

    file_size = Path(output_path).stat().st_size
    print(f"  Written: {output_path}")
    print(f"  Size: {file_size / 1024 / 1024:.1f} MB")
    print(f"  Header: {HEADER_SIZE} bytes")
    print(f"  DimIndex: {DIM_INDEX_SIZE} bytes")
    print(f"  FrameData: {T * D * 2} bytes ({T} frames × {D}D × Float16)")


# ═══════════════════════════════════════════════════════════════════════
# MOMENTS EXPORT
# ═══════════════════════════════════════════════════════════════════════

MOMENTS_DB = {
    "swan lake": [
        {"start": 0, "end": 5, "label": "Intro", "type": "section_start"},
        {"start": 5, "end": 30, "label": "Opening Tremolo", "type": "section"},
        {"start": 30, "end": 60, "label": "Swan Theme (Oboe)", "type": "consonance_peak"},
        {"start": 60, "end": 95, "label": "Development", "type": "section"},
        {"start": 95, "end": 130, "label": "Buildup", "type": "energy_buildup"},
        {"start": 130, "end": 160, "label": "Climax", "type": "pleasure_convergence"},
        {"start": 160, "end": 183, "label": "Resolution", "type": "tension_resolution"},
    ],
}


def export_moments(piece_key: str, output_path: str) -> None:
    """Export musical moments to JSON."""
    moments = MOMENTS_DB.get(piece_key, [])
    with open(output_path, "w") as f:
        json.dump({"piece": piece_key, "moments": moments}, f, indent=2)
    print(f"  Moments: {output_path} ({len(moments)} sections)")


# ═══════════════════════════════════════════════════════════════════════
# MANIFEST EXPORT
# ═══════════════════════════════════════════════════════════════════════

def export_manifest(piece_key: str, duration_ms: int, output_path: str) -> None:
    """Export piece manifest JSON."""
    manifest = {
        "pieces": [
            {
                "id": piece_key.replace(" ", "-"),
                "title": "Swan Lake Suite, Op. 20a: I. Scene",
                "composer": "Pyotr Ilyich Tchaikovsky",
                "genre": "Classical Orchestral",
                "genre_tr": "Klasik Orkestra",
                "duration_s": duration_ms / 1000,
                "data_file": "swan-lake.mi.bin",
                "audio_file": "swan-lake.mp3",
                "description": "Where the brain's reward system comes alive",
                "description_tr": "Beynin odül sisteminin canlandiği yer",
            }
        ],
        "format": {
            "magic": "MI01",
            "version": 1,
            "dims": 307,
            "layout": {
                "cochlea": [0, 128],
                "r3": [128, 177],
                "brain": [177, 203],
                "l3": [203, 307],
            },
            "brain_pathways": {
                "shared": [177, 181],
                "reward": [181, 190],
                "affect": [190, 196],
                "autonomic": [196, 201],
                "integration": [201, 203],
            },
            "l3_groups": {
                "alpha": [203, 209],
                "beta": [209, 223],
                "gamma": [223, 236],
                "delta": [236, 248],
                "epsilon": [248, 267],
                "zeta": [267, 279],
                "eta": [279, 291],
                "theta": [291, 307],
            },
        },
        "frame_rate": 172.265625,
        "sample_rate": 44100,
        "hop_length": 256,
    }
    with open(output_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  Manifest: {output_path}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════

DEFAULT_AUDIO = str(
    PROJECT_ROOT
    / "Musical Intelligence"
    / "Test-Audio"
    / "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky.wav"
)

DEFAULT_OUTPUT_DIR = str(Path(__file__).resolve().parent.parent / "data")


def main():
    parser = argparse.ArgumentParser(description="Export MI pipeline data to binary format")
    parser.add_argument("--audio", default=DEFAULT_AUDIO, help="Path to audio file")
    parser.add_argument("--output", default=None, help="Output .mi.bin path")
    parser.add_argument("--piece", default="swan lake", help="Piece key for moments lookup")
    args = parser.parse_args()

    output_dir = Path(DEFAULT_OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_bin = args.output or str(output_dir / "swan-lake.mi.bin")

    print("=" * 60)
    print("MI Binary Export — Musical Intelligence Demo")
    print("=" * 60)

    # 1. Run pipeline
    print(f"\n[1/3] Running MI pipeline on: {Path(args.audio).name}")
    data = run_pipeline(args.audio)

    # 2. Write binary
    print(f"\n[2/3] Writing MI01 binary")
    write_mi_bin(data, output_bin)

    # 3. Export metadata
    print(f"\n[3/3] Exporting metadata")
    export_moments(args.piece, str(output_dir / "moments.json"))
    export_manifest(args.piece, data["duration_ms"], str(output_dir / "manifest.json"))

    print(f"\n{'=' * 60}")
    print("Done! Files written to: " + str(output_dir))
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
