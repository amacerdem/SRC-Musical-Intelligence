#!/usr/bin/env python3
"""H3 Temporal Morphology Validation Report.

Validates the H3 sparse temporal extractor by collecting all demand sets
from 96 cognitive models and 10 mechanisms, analyzing demand distribution,
computing sparsity metrics, and validating H3 output values.

Usage:
    python Tests/validation/validate_h3.py
"""
from __future__ import annotations

import os
import sys
import time
from collections import defaultdict
from typing import Dict, Set, Tuple

# ---------------------------------------------------------------------------
# Path setup
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
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.ear.h3.constants.horizons import (
    N_HORIZONS,
    HORIZON_MS,
    BAND_ASSIGNMENTS,
    BAND_RANGES,
)
from Musical_Intelligence.ear.h3.constants.morphs import (
    N_MORPHS,
    MORPH_NAMES,
    MORPH_CATEGORIES,
)
from Musical_Intelligence.ear.h3.constants.laws import N_LAWS, LAW_NAMES
from Musical_Intelligence.ear.r3.constants import R3_DIM, R3_FEATURE_NAMES
from Musical_Intelligence.brain.mechanisms import MechanismRunner
from Musical_Intelligence.brain.units import (
    SPUUnit, STUUnit, IMUUnit, ASUUnit, NDUUnit, MPUUnit, PCUUnit,
    ARUUnit, RPUUnit,
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
FRAME_RATE = SR / HOP

THEORETICAL_SPACE = R3_DIM * N_HORIZONS * N_MORPHS * N_LAWS  # 97*32*24*3 = 223,488

UNIT_NAMES = ("SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU", "ARU", "RPU")
UNIT_CLASSES = {
    "SPU": SPUUnit, "STU": STUUnit, "IMU": IMUUnit,
    "ASU": ASUUnit, "NDU": NDUUnit, "MPU": MPUUnit,
    "PCU": PCUUnit, "ARU": ARUUnit, "RPU": RPUUnit,
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
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
# Demand collection
# ---------------------------------------------------------------------------
def collect_all_demands() -> dict:
    """Collect H3 demands from all 96 models + 10 mechanisms."""
    results = {
        "per_unit": {},
        "per_mechanism": {},
        "all_model_demand": set(),
        "all_mechanism_demand": set(),
    }

    # Collect per-unit model demands
    for name in UNIT_NAMES:
        unit = UNIT_CLASSES[name]()
        unit_demand: Set[Tuple[int, int, int, int]] = set()
        per_model = {}
        for model in unit.models:
            model_demand = model.h3_demand_tuples()
            per_model[model.NAME] = model_demand
            unit_demand |= model_demand
        results["per_unit"][name] = {
            "total": len(unit_demand),
            "models": per_model,
            "demand": unit_demand,
            "n_models": len(unit.models),
        }
        results["all_model_demand"] |= unit_demand

    # Collect mechanism demands
    runner = MechanismRunner()
    for mech_name, mech in runner._mechanisms.items():
        mech_demand = mech.h3_demand
        results["per_mechanism"][mech_name] = {
            "total": len(mech_demand),
            "demand": mech_demand,
        }
        results["all_mechanism_demand"] |= mech_demand

    return results


def analyze_demand_distribution(
    demand: Set[Tuple[int, int, int, int]],
) -> dict:
    """Analyze distribution of demands across axes."""
    horizon_counts: Dict[int, int] = defaultdict(int)
    morph_counts: Dict[int, int] = defaultdict(int)
    law_counts: Dict[int, int] = defaultdict(int)
    r3_counts: Dict[int, int] = defaultdict(int)
    band_counts: Dict[str, int] = defaultdict(int)

    for r3_idx, horizon, morph, law in demand:
        horizon_counts[horizon] += 1
        morph_counts[morph] += 1
        law_counts[law] += 1
        r3_counts[r3_idx] += 1
        band_counts[BAND_ASSIGNMENTS[horizon]] += 1

    return {
        "horizon_counts": dict(sorted(horizon_counts.items())),
        "morph_counts": dict(sorted(morph_counts.items())),
        "law_counts": dict(sorted(law_counts.items())),
        "r3_counts": dict(sorted(r3_counts.items())),
        "band_counts": dict(sorted(band_counts.items())),
        "n_unique_horizons": len(horizon_counts),
        "n_unique_morphs": len(morph_counts),
        "n_unique_laws": len(law_counts),
        "n_unique_r3": len(r3_counts),
    }


def compute_unit_overlap(demand_info: dict) -> dict:
    """Compute pairwise demand overlap between units."""
    overlap = {}
    unit_demands = {
        name: info["demand"] for name, info in demand_info["per_unit"].items()
    }
    for u1 in UNIT_NAMES:
        for u2 in UNIT_NAMES:
            if u1 < u2:
                shared = unit_demands[u1] & unit_demands[u2]
                if shared:
                    overlap[f"{u1}-{u2}"] = len(shared)
    return overlap


# ---------------------------------------------------------------------------
# Main report
# ---------------------------------------------------------------------------
def main() -> None:
    t_start = time.perf_counter()
    print(_section("H3 TEMPORAL MORPHOLOGY VALIDATION REPORT"))
    print(f"  Theoretical space: {R3_DIM} x {N_HORIZONS} x {N_MORPHS} x {N_LAWS} "
          f"= {THEORETICAL_SPACE:,}")
    print()

    # ------------------------------------------------------------------
    # 1. Collect all demands
    # ------------------------------------------------------------------
    print(_section("1. Demand Collection"))
    t0 = time.perf_counter()
    demand_info = collect_all_demands()
    collect_time = time.perf_counter() - t0

    all_model = demand_info["all_model_demand"]
    all_mech = demand_info["all_mechanism_demand"]
    all_demand = all_model | all_mech

    print(f"  Total model demand tuples:     {len(all_model):>6}")
    print(f"  Total mechanism demand tuples:  {len(all_mech):>6}")
    print(f"  Combined (union):              {len(all_demand):>6}")
    print(f"  Overlap (model & mechanism):   {len(all_model & all_mech):>6}")
    print(f"  Sparsity: {len(all_demand):,} / {THEORETICAL_SPACE:,} "
          f"= {len(all_demand) / THEORETICAL_SPACE * 100:.3f}%")
    print(f"  Collection time: {collect_time:.3f}s")

    # ------------------------------------------------------------------
    # 2. Per-unit demand summary
    # ------------------------------------------------------------------
    print(_section("2. Per-Unit Demand Summary"))
    header = f"  {'Unit':<5} {'Models':>6} {'Demands':>8} {'Avg/Model':>10}"
    print(header)
    print(f"  {'-' * (len(header) - 2)}")
    total_models = 0
    for name in UNIT_NAMES:
        info = demand_info["per_unit"][name]
        n_models = info["n_models"]
        total_models += n_models
        avg = info["total"] / n_models if n_models > 0 else 0
        print(f"  {name:<5} {n_models:>6} {info['total']:>8} {avg:>10.1f}")
    print(f"  {'TOTAL':<5} {total_models:>6} {len(all_model):>8}")

    # ------------------------------------------------------------------
    # 3. Per-mechanism demand summary
    # ------------------------------------------------------------------
    print(_section("3. Per-Mechanism Demand Summary"))
    header = f"  {'Mechanism':<10} {'Demands':>8}"
    print(header)
    print(f"  {'-' * (len(header) - 2)}")
    for mech_name in sorted(demand_info["per_mechanism"]):
        info = demand_info["per_mechanism"][mech_name]
        print(f"  {mech_name:<10} {info['total']:>8}")
    print(f"  {'TOTAL':<10} {len(all_mech):>8}")

    # ------------------------------------------------------------------
    # 4. Demand distribution analysis
    # ------------------------------------------------------------------
    print(_section("4. Demand Distribution Analysis"))
    dist = analyze_demand_distribution(all_demand)

    print(f"  Unique R3 indices used:  {dist['n_unique_r3']:>4} / {R3_DIM}")
    print(f"  Unique horizons used:    {dist['n_unique_horizons']:>4} / {N_HORIZONS}")
    print(f"  Unique morphs used:      {dist['n_unique_morphs']:>4} / {N_MORPHS}")
    print(f"  Unique laws used:        {dist['n_unique_laws']:>4} / {N_LAWS}")

    # Per-band counts
    print(f"\n  Per-band demand counts:")
    for band in ("micro", "meso", "macro", "ultra"):
        count = dist["band_counts"].get(band, 0)
        brange = BAND_RANGES[band]
        print(f"    {band:<6} (H{brange[0]:>2}-H{brange[1]:>2}): {count:>6} tuples")

    # Per-horizon top 10
    print(f"\n  Top 10 horizons by demand count:")
    sorted_h = sorted(dist["horizon_counts"].items(), key=lambda x: -x[1])
    for h_idx, count in sorted_h[:10]:
        ms = HORIZON_MS[h_idx]
        band = BAND_ASSIGNMENTS[h_idx]
        print(f"    H{h_idx:>2} ({ms:>9.1f}ms, {band:<5}): {count:>5} tuples")

    # Per-morph counts
    print(f"\n  Per-morph demand counts:")
    for m_idx in range(N_MORPHS):
        count = dist["morph_counts"].get(m_idx, 0)
        if count > 0:
            print(f"    M{m_idx:>2} {MORPH_NAMES[m_idx]:<22}: {count:>5} tuples")

    # Per-law counts
    print(f"\n  Per-law demand counts:")
    for law_idx in range(N_LAWS):
        count = dist["law_counts"].get(law_idx, 0)
        print(f"    L{law_idx} {LAW_NAMES[law_idx]:<14}: {count:>5} tuples")

    # ------------------------------------------------------------------
    # 5. Unit demand overlap
    # ------------------------------------------------------------------
    print(_section("5. Inter-Unit Demand Overlap"))
    overlap = compute_unit_overlap(demand_info)
    if overlap:
        sorted_overlap = sorted(overlap.items(), key=lambda x: -x[1])
        for pair, count in sorted_overlap:
            print(f"  {pair:<10}: {count:>5} shared tuples")
    else:
        print("  No demand overlap between units")

    # ------------------------------------------------------------------
    # 6. H3 extraction and value validation
    # ------------------------------------------------------------------
    print(_section("6. H3 Extraction & Value Validation"))

    if not os.path.exists(SWAN_LAKE_PATH):
        print(f"  WARNING: Audio file not found: {SWAN_LAKE_PATH}")
        print(f"  Skipping H3 extraction validation.")
    else:
        t0 = time.perf_counter()
        mel = _load_mel(SWAN_LAKE_PATH)
        r3_ext = R3Extractor()
        r3_out = r3_ext.extract(mel)
        r3_features = r3_out.features  # (B, T, 97)
        r3_time = time.perf_counter() - t0
        print(f"  R3 extraction: {tuple(r3_features.shape)}, time={r3_time:.3f}s")

        # Use a subset of demand for validation (full demand may be large)
        subset_size = min(len(all_demand), 500)
        demand_list = sorted(all_demand)
        subset_demand = set(demand_list[:subset_size])

        t0 = time.perf_counter()
        h3_ext = H3Extractor()
        h3_out = h3_ext.extract(r3_features, subset_demand)
        h3_time = time.perf_counter() - t0

        print(f"  H3 extraction: {h3_out.n_tuples} tuples computed "
              f"(of {subset_size} demanded)")
        print(f"  Time: {h3_time:.3f}s")

        # Validate output values
        n_valid = 0
        n_out_of_range = 0
        n_nan = 0
        n_inf = 0
        morph_stats: Dict[int, list] = defaultdict(list)

        for key, tensor in h3_out.features.items():
            r3_idx, horizon, morph, law = key
            flat = tensor.reshape(-1)
            if torch.isnan(flat).any():
                n_nan += 1
            elif torch.isinf(flat).any():
                n_inf += 1
            elif flat.min().item() < 0.0 or flat.max().item() > 1.0:
                n_out_of_range += 1
            else:
                n_valid += 1
            morph_stats[morph].append(flat.mean().item())

        total_checked = n_valid + n_out_of_range + n_nan + n_inf
        print(f"\n  Value validation ({total_checked} features checked):")
        print(f"    [{'PASS' if n_valid == total_checked else 'FAIL'}] "
              f"In range [0, 1]: {n_valid}/{total_checked}")
        print(f"    [{'PASS' if n_out_of_range == 0 else 'FAIL'}] "
              f"Out of range: {n_out_of_range}")
        print(f"    [{'PASS' if n_nan == 0 else 'FAIL'}] NaN values: {n_nan}")
        print(f"    [{'PASS' if n_inf == 0 else 'FAIL'}] Inf values: {n_inf}")

        # Per-morph statistics
        if morph_stats:
            print(f"\n  Per-morph mean statistics (from validated subset):")
            for m_idx in sorted(morph_stats.keys()):
                vals = morph_stats[m_idx]
                avg = sum(vals) / len(vals) if vals else 0.0
                print(f"    M{m_idx:>2} {MORPH_NAMES[m_idx]:<22}: "
                      f"mean={avg:.4f}, n={len(vals)}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total_time = time.perf_counter() - t_start
    print(_section("SUMMARY"))
    print(f"  Total demand: {len(all_demand):,} tuples")
    print(f"  Sparsity: {len(all_demand) / THEORETICAL_SPACE * 100:.3f}% "
          f"of theoretical space")
    print(f"  Models contributing: {total_models}")
    print(f"  Mechanisms contributing: {len(demand_info['per_mechanism'])}")
    print(f"  Total time: {total_time:.3f}s")
    print("=" * 72)


if __name__ == "__main__":
    main()
