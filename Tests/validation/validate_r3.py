#!/usr/bin/env python3
"""R3 Spectral Feature Validation Report.

Validates the 97-D R3 spectral feature extractor against the Swan Lake
test audio. Checks value ranges, NaN/Inf absence, per-group statistics,
group boundary alignment, and warmup feature behavior.

Usage:
    python Tests/validation/validate_r3.py
"""
from __future__ import annotations

import os
import sys
import time

# ---------------------------------------------------------------------------
# Path setup -- make Musical_Intelligence importable from any working dir
# ---------------------------------------------------------------------------
_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import librosa
import numpy as np
import torch

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.r3.constants import (
    R3_DIM,
    R3_FEATURE_NAMES,
    R3_GROUP_BOUNDARIES,
)
from Musical_Intelligence.ear.r3.pipeline.warmup import (
    WARMUP_344_ZERO,
    WARMUP_344_RAMP,
    WARMUP_688_ZERO,
    WARMUP_ALL,
    WarmupManager,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SWAN_LAKE_PATH = os.path.join(
    _PROJECT_ROOT,
    "Test-Audio",
    "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
    " - Pyotr Ilyich Tchaikovsky.wav",
)
SR = 44100
HOP = 256
N_MELS = 128
FRAME_RATE = SR / HOP  # 172.27 Hz


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _sep(char: str = "=", width: int = 72) -> str:
    return char * width


def _section(title: str) -> str:
    return f"\n{'=' * 72}\n  {title}\n{'=' * 72}"


def _load_mel(path: str, duration: float = 30.0) -> torch.Tensor:
    """Load audio (first *duration* seconds) and compute normalised mel (1, 128, T)."""
    y, sr = librosa.load(path, sr=SR, mono=True, duration=duration)
    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, n_mels=N_MELS, hop_length=HOP, n_fft=1024,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    return torch.tensor(mel_norm, dtype=torch.float32).unsqueeze(0)


# ---------------------------------------------------------------------------
# Validation checks
# ---------------------------------------------------------------------------
def validate_shape(features: torch.Tensor) -> dict:
    """Check output shape is (B, T, 97)."""
    B, T, D = features.shape
    passed = D == R3_DIM
    return {
        "test": "Output shape",
        "passed": passed,
        "detail": f"Shape = ({B}, {T}, {D}), expected D={R3_DIM}",
    }


def validate_range(features: torch.Tensor) -> dict:
    """Check all values in [0, 1]."""
    fmin = features.min().item()
    fmax = features.max().item()
    passed = fmin >= 0.0 and fmax <= 1.0
    return {
        "test": "Value range [0, 1]",
        "passed": passed,
        "detail": f"min={fmin:.6f}, max={fmax:.6f}",
    }


def validate_no_nan_inf(features: torch.Tensor) -> dict:
    """Check no NaN or Inf values."""
    n_nan = torch.isnan(features).sum().item()
    n_inf = torch.isinf(features).sum().item()
    passed = n_nan == 0 and n_inf == 0
    return {
        "test": "No NaN/Inf",
        "passed": passed,
        "detail": f"NaN count={n_nan}, Inf count={n_inf}",
    }


def validate_group_boundaries(features: torch.Tensor) -> dict:
    """Check group boundaries cover [0, 97) without gaps/overlaps."""
    errors = []
    prev_end = 0
    total_dim = 0
    for g in R3_GROUP_BOUNDARIES:
        if g.start != prev_end:
            errors.append(f"Gap/overlap at {g.letter}: start={g.start}, prev_end={prev_end}")
        if g.end - g.start != g.dim:
            errors.append(f"Dim mismatch {g.letter}: end-start={g.end - g.start}, dim={g.dim}")
        total_dim += g.dim
        prev_end = g.end
    if prev_end != R3_DIM:
        errors.append(f"Final end={prev_end}, expected {R3_DIM}")
    if total_dim != R3_DIM:
        errors.append(f"Total dim={total_dim}, expected {R3_DIM}")
    passed = len(errors) == 0
    detail = "All 9 groups contiguous [0, 97)" if passed else "; ".join(errors)
    return {
        "test": "Group boundary alignment",
        "passed": passed,
        "detail": detail,
    }


def validate_feature_names() -> dict:
    """Check feature names count and uniqueness."""
    n = len(R3_FEATURE_NAMES)
    n_unique = len(set(R3_FEATURE_NAMES))
    passed = n == R3_DIM and n_unique == R3_DIM
    return {
        "test": "Feature names",
        "passed": passed,
        "detail": f"count={n}, unique={n_unique}, expected={R3_DIM}",
    }


# ---------------------------------------------------------------------------
# Per-group statistics
# ---------------------------------------------------------------------------
def compute_group_stats(features: torch.Tensor) -> list:
    """Compute per-group statistics."""
    stats = []
    for g in R3_GROUP_BOUNDARIES:
        group_data = features[:, :, g.start:g.end]  # (B, T, dim)
        flat = group_data.reshape(-1)
        zero_frac = (flat == 0.0).float().mean().item()
        stats.append({
            "letter": g.letter,
            "name": g.name,
            "range": f"[{g.start}:{g.end}]",
            "dim": g.dim,
            "stage": g.stage,
            "mean": flat.mean().item(),
            "std": flat.std().item(),
            "min": flat.min().item(),
            "max": flat.max().item(),
            "zero_frac": zero_frac,
        })
    return stats


# ---------------------------------------------------------------------------
# Warmup analysis
# ---------------------------------------------------------------------------
def analyze_warmup(features: torch.Tensor) -> dict:
    """Analyze warmup behavior of affected features."""
    B, T, D = features.shape
    wm = WarmupManager()

    # Check features at early frames vs late frames
    early_frames = min(50, T)
    late_start = max(T - 50, 688)

    warmup_report = {
        "total_warmup_features": len(WARMUP_ALL),
        "tier1_zero": len(WARMUP_344_ZERO),
        "tier1_ramp": len(WARMUP_344_RAMP),
        "tier2_zero": len(WARMUP_688_ZERO),
        "early_zero_features": [],
        "ramp_behavior": [],
    }

    # Check zero features at frame 0
    for idx in sorted(WARMUP_344_ZERO):
        val_early = features[0, 0, idx].item()
        val_late = features[0, -1, idx].item() if T > 688 else None
        warmup_report["early_zero_features"].append({
            "index": idx,
            "name": R3_FEATURE_NAMES[idx],
            "frame0_value": val_early,
            "late_value": val_late,
            "warmup_frames": 344,
        })

    for idx in sorted(WARMUP_688_ZERO):
        val_early = features[0, 0, idx].item()
        val_late = features[0, -1, idx].item() if T > 688 else None
        warmup_report["early_zero_features"].append({
            "index": idx,
            "name": R3_FEATURE_NAMES[idx],
            "frame0_value": val_early,
            "late_value": val_late,
            "warmup_frames": 688,
        })

    # Check ramp features
    for idx in sorted(WARMUP_344_RAMP):
        val_10 = features[0, min(10, T - 1), idx].item()
        val_172 = features[0, min(172, T - 1), idx].item()
        val_344 = features[0, min(344, T - 1), idx].item()
        warmup_report["ramp_behavior"].append({
            "index": idx,
            "name": R3_FEATURE_NAMES[idx],
            "frame10": val_10,
            "frame172": val_172,
            "frame344": val_344,
        })

    return warmup_report


# ---------------------------------------------------------------------------
# Main report
# ---------------------------------------------------------------------------
def main() -> None:
    print(_section("R3 SPECTRAL FEATURE VALIDATION REPORT"))
    print(f"  Audio: {os.path.basename(SWAN_LAKE_PATH)}")
    print(f"  Frame rate: {FRAME_RATE:.2f} Hz")
    print(f"  Expected dim: {R3_DIM}")
    print()

    # ------------------------------------------------------------------
    # 1. Load audio
    # ------------------------------------------------------------------
    print(_section("1. Loading Audio"))
    t0 = time.perf_counter()

    if not os.path.exists(SWAN_LAKE_PATH):
        print(f"  ERROR: Audio file not found: {SWAN_LAKE_PATH}")
        sys.exit(1)

    mel = _load_mel(SWAN_LAKE_PATH)
    B, N, T = mel.shape
    duration_s = T / FRAME_RATE
    load_time = time.perf_counter() - t0
    print(f"  Loaded mel spectrogram: ({B}, {N}, {T})")
    print(f"  Duration: {duration_s:.1f}s ({T} frames)")
    print(f"  Time: {load_time:.3f}s")

    # ------------------------------------------------------------------
    # 2. Extract R3 features
    # ------------------------------------------------------------------
    print(_section("2. R3 Feature Extraction"))
    t0 = time.perf_counter()
    extractor = R3Extractor()
    r3_output = extractor.extract(mel)
    extract_time = time.perf_counter() - t0
    features = r3_output.features  # (B, T, 97)
    print(f"  Extractor: {extractor}")
    print(f"  Output shape: {tuple(features.shape)}")
    print(f"  Feature names: {len(r3_output.feature_names)} entries")
    print(f"  Time: {extract_time:.3f}s")

    # ------------------------------------------------------------------
    # 3. Core validations
    # ------------------------------------------------------------------
    print(_section("3. Core Validations"))
    checks = [
        validate_shape(features),
        validate_range(features),
        validate_no_nan_inf(features),
        validate_group_boundaries(features),
        validate_feature_names(),
    ]
    all_passed = True
    for c in checks:
        status = "PASS" if c["passed"] else "FAIL"
        if not c["passed"]:
            all_passed = False
        print(f"  [{status}] {c['test']}: {c['detail']}")

    # ------------------------------------------------------------------
    # 4. Per-group statistics
    # ------------------------------------------------------------------
    print(_section("4. Per-Group Statistics"))
    group_stats = compute_group_stats(features)
    header = f"  {'Grp':<3} {'Name':<28} {'Range':<10} {'Dim':>4} {'Stg':>3}  {'Mean':>7} {'Std':>7} {'Min':>7} {'Max':>7} {'Zero%':>6}"
    print(header)
    print(f"  {'-' * (len(header) - 2)}")
    for s in group_stats:
        print(
            f"  {s['letter']:<3} {s['name']:<28} {s['range']:<10} "
            f"{s['dim']:>4} {s['stage']:>3}  "
            f"{s['mean']:>7.4f} {s['std']:>7.4f} {s['min']:>7.4f} "
            f"{s['max']:>7.4f} {s['zero_frac']*100:>5.1f}%"
        )

    # Summary
    full_flat = features.reshape(-1)
    print(f"\n  Overall: mean={full_flat.mean().item():.4f}, "
          f"std={full_flat.std().item():.4f}, "
          f"zero_frac={((full_flat == 0).float().mean().item()) * 100:.1f}%")

    # ------------------------------------------------------------------
    # 5. Warmup feature behavior
    # ------------------------------------------------------------------
    print(_section("5. Warmup Feature Behavior"))
    warmup = analyze_warmup(features)
    print(f"  Total warmup features: {warmup['total_warmup_features']}")
    print(f"    Tier 1 zero (344 frames):  {warmup['tier1_zero']} features")
    print(f"    Tier 1 ramp (344 frames):  {warmup['tier1_ramp']} features")
    print(f"    Tier 2 zero (688 frames):  {warmup['tier2_zero']} features")
    print()

    print("  Zero-output features at frame 0:")
    for f in warmup["early_zero_features"]:
        late = f"late={f['late_value']:.4f}" if f["late_value"] is not None else "late=N/A"
        print(f"    [{f['index']:>3}] {f['name']:<28} frame0={f['frame0_value']:.4f}  "
              f"{late}  warmup={f['warmup_frames']} frames")

    print()
    print("  Ramp features (confidence scaling):")
    for f in warmup["ramp_behavior"][:8]:  # Show first 8
        print(f"    [{f['index']:>3}] {f['name']:<28} f10={f['frame10']:.4f}  "
              f"f172={f['frame172']:.4f}  f344={f['frame344']:.4f}")
    if len(warmup["ramp_behavior"]) > 8:
        print(f"    ... and {len(warmup['ramp_behavior']) - 8} more ramp features")

    # ------------------------------------------------------------------
    # 6. Feature map structure
    # ------------------------------------------------------------------
    print(_section("6. Feature Map Structure"))
    fmap = r3_output.feature_map
    print(f"  {fmap}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print(_section("SUMMARY"))
    n_pass = sum(1 for c in checks if c["passed"])
    n_total = len(checks)
    print(f"  Checks: {n_pass}/{n_total} passed")
    print(f"  R3 extraction time: {extract_time:.3f}s")
    print(f"  Total time: {time.perf_counter() - t0 + load_time:.3f}s")
    if all_passed:
        print(f"  Status: ALL VALIDATIONS PASSED")
    else:
        print(f"  Status: SOME VALIDATIONS FAILED")
    print(_sep())


if __name__ == "__main__":
    main()
