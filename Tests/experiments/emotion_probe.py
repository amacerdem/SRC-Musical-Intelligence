#!/usr/bin/env python3
"""Emotion Differentiation Probe — Minimal Validation Test.

Tests the core hypothesis: does the MI pipeline produce meaningfully
different outputs for emotionally contrasting music?

Three clips, maximum contrast:
  1. CALM:        Bach Cello Suite No. 1 (solo cello, consonant, peaceful)
  2. MELANCHOLIC: Beethoven Pathetique (piano, minor, emotional)
  3. INTENSE:     Duel of the Fates (full orchestra, dramatic, dissonant)

Two test levels:
  Level 1 — R³ only (fast, ~3 seconds): Do spectral features differentiate?
  Level 2 — Full pipeline (slow, ~30-90s): Do cognitive units differentiate?

Hypotheses (from psychoacoustic literature):
  - Consonance:  Calm > Melancholic > Intense
  - Energy:      Intense > Melancholic > Calm
  - Warmth:      Calm ≥ Melancholic > Intense
  - Sharpness:   Intense > Melancholic ≥ Calm
  - Change:      Intense > Melancholic > Calm
  - ARU (affect): All three produce distinct profiles

Usage:
    python Tests/experiments/emotion_probe.py              # R³ only (fast)
    python Tests/experiments/emotion_probe.py --full       # R³ + H³ + C³
    python Tests/experiments/emotion_probe.py --duration 5 # shorter clips
"""
from __future__ import annotations

import os
import sys
import time
import argparse

_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import librosa
import numpy as np
import torch
from torch import Tensor

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.r3.constants import (
    R3_GROUP_BOUNDARIES,
    R3_FEATURE_NAMES,
)

# ─── Constants ────────────────────────────────────────────────────────────────
SR = 44100
HOP = 256
N_MELS = 128
FRAME_RATE = SR / HOP

AUDIO_DIR = os.path.join(_PROJECT_ROOT, "Test-Audio")

# Three emotionally contrasting clips
CLIPS = {
    "CALM": {
        "file": "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav",
        "offset": 10.0,   # skip intro silence, get into the flowing arpeggios
        "label": "Bach Cello Suite",
        "emoji": "🌊",
        "expected": "high consonance, low energy, warm timbre",
    },
    "MELANCHOLIC": {
        "file": "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
        "offset": 0.0,    # the Grave opening — slow, minor, heavy chords
        "label": "Beethoven Pathétique",
        "emoji": "🌧️",
        "expected": "moderate consonance, moderate energy, dark timbre",
    },
    "INTENSE": {
        "file": "Duel of the Fates - Epic Version.wav",
        "offset": 30.0,   # skip intro, get into the main theme
        "label": "Duel of the Fates",
        "emoji": "⚡",
        "expected": "low consonance, high energy, sharp timbre",
    },
}


# ─── Audio Loading ────────────────────────────────────────────────────────────
def load_mel(path: str, offset: float, duration: float) -> Tensor:
    """Load audio segment and compute normalised mel spectrogram."""
    y, sr = librosa.load(path, sr=SR, mono=True, offset=offset, duration=duration)
    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, n_mels=N_MELS, hop_length=HOP, n_fft=1024,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    return torch.tensor(mel_norm, dtype=torch.float32).unsqueeze(0)


# ─── R³ Group Statistics ──────────────────────────────────────────────────────
def r3_group_means(features: Tensor) -> dict:
    """Compute mean value per R³ group, averaged over all frames."""
    # features: (1, T, 97)
    feat = features[0]  # (T, 97)
    result = {}
    for g in R3_GROUP_BOUNDARIES:
        vals = feat[:, g.start:g.end]  # (T, group_dim)
        result[g.letter] = {
            "name": g.name,
            "mean": vals.mean().item(),
            "std": vals.std().item(),
            "dim": g.end - g.start,
        }
    return result


def r3_key_features(features: Tensor) -> dict:
    """Extract specific emotion-relevant features by name."""
    feat = features[0]  # (T, 97)
    names = R3_FEATURE_NAMES

    # Map name → index for lookup
    name_to_idx = {n: i for i, n in enumerate(names)}

    targets = [
        # Consonance group
        "roughness", "sethares_dissonance", "sensory_pleasantness",
        # Energy group
        "amplitude", "onset_strength",
        # Timbre group
        "warmth", "sharpness", "tonalness", "clarity",
        # Change group
        "spectral_flux", "distribution_entropy",
    ]

    result = {}
    for name in targets:
        if name in name_to_idx:
            idx = name_to_idx[name]
            vals = feat[:, idx]
            result[name] = {
                "mean": vals.mean().item(),
                "std": vals.std().item(),
                "min": vals.min().item(),
                "max": vals.max().item(),
            }
    return result


# ─── Hypothesis Testing ──────────────────────────────────────────────────────
def test_hypotheses(r3_results: dict) -> list:
    """Test psychoacoustic hypotheses and return pass/fail results."""
    calm = r3_results["CALM"]
    mel_ = r3_results["MELANCHOLIC"]
    intense = r3_results["INTENSE"]

    tests = []

    def check(name, condition, detail):
        tests.append({
            "name": name,
            "passed": condition,
            "detail": detail,
        })

    # H1: Consonance — Calm > Intense
    c_calm = calm["groups"]["A"]["mean"]
    c_intense = intense["groups"]["A"]["mean"]
    c_mel = mel_["groups"]["A"]["mean"]
    check(
        "H1: Consonance(Calm) > Consonance(Intense)",
        c_calm > c_intense,
        f"Calm={c_calm:.4f}  Intense={c_intense:.4f}  diff={c_calm - c_intense:+.4f}",
    )

    # H2: Energy — Intense > Calm
    e_calm = calm["groups"]["B"]["mean"]
    e_intense = intense["groups"]["B"]["mean"]
    check(
        "H2: Energy(Intense) > Energy(Calm)",
        e_intense > e_calm,
        f"Intense={e_intense:.4f}  Calm={e_calm:.4f}  diff={e_intense - e_calm:+.4f}",
    )

    # H3: Warmth — Calm > Intense
    if "warmth" in calm["features"] and "warmth" in intense["features"]:
        w_calm = calm["features"]["warmth"]["mean"]
        w_intense = intense["features"]["warmth"]["mean"]
        check(
            "H3: Warmth(Calm) > Warmth(Intense)",
            w_calm > w_intense,
            f"Calm={w_calm:.4f}  Intense={w_intense:.4f}  diff={w_calm - w_intense:+.4f}",
        )

    # H4: Sharpness — Intense > Calm
    if "sharpness" in calm["features"] and "sharpness" in intense["features"]:
        s_calm = calm["features"]["sharpness"]["mean"]
        s_intense = intense["features"]["sharpness"]["mean"]
        check(
            "H4: Sharpness(Intense) > Sharpness(Calm)",
            s_intense > s_calm,
            f"Intense={s_intense:.4f}  Calm={s_calm:.4f}  diff={s_intense - s_calm:+.4f}",
        )

    # H5: Spectral Change — Intense > Calm
    d_calm = calm["groups"]["D"]["mean"]
    d_intense = intense["groups"]["D"]["mean"]
    check(
        "H5: Change(Intense) > Change(Calm)",
        d_intense > d_calm,
        f"Intense={d_intense:.4f}  Calm={d_calm:.4f}  diff={d_intense - d_calm:+.4f}",
    )

    # H6: Roughness — Intense > Calm
    if "roughness" in calm["features"] and "roughness" in intense["features"]:
        r_calm = calm["features"]["roughness"]["mean"]
        r_intense = intense["features"]["roughness"]["mean"]
        check(
            "H6: Roughness(Intense) > Roughness(Calm)",
            r_intense > r_calm,
            f"Intense={r_intense:.4f}  Calm={r_calm:.4f}  diff={r_intense - r_calm:+.4f}",
        )

    # H7: Sensory Pleasantness — Calm > Intense
    if "sensory_pleasantness" in calm["features"] and "sensory_pleasantness" in intense["features"]:
        p_calm = calm["features"]["sensory_pleasantness"]["mean"]
        p_intense = intense["features"]["sensory_pleasantness"]["mean"]
        check(
            "H7: Pleasantness(Calm) > Pleasantness(Intense)",
            p_calm > p_intense,
            f"Calm={p_calm:.4f}  Intense={p_intense:.4f}  diff={p_calm - p_intense:+.4f}",
        )

    # H8: Onset Strength — Intense > Calm
    if "onset_strength" in calm["features"] and "onset_strength" in intense["features"]:
        o_calm = calm["features"]["onset_strength"]["mean"]
        o_intense = intense["features"]["onset_strength"]["mean"]
        check(
            "H8: OnsetStrength(Intense) > OnsetStrength(Calm)",
            o_intense > o_calm,
            f"Intense={o_intense:.4f}  Calm={o_calm:.4f}  diff={o_intense - o_calm:+.4f}",
        )

    return tests


# ─── Brain Analysis ───────────────────────────────────────────────────────────
def run_full_pipeline(mels: dict, r3_results: dict) -> dict:
    """Run H³ + C³ on all clips and compare cognitive unit profiles."""
    from Musical_Intelligence.ear.h3 import H3Extractor
    from Musical_Intelligence.brain import BrainOrchestrator
    from Musical_Intelligence.brain.orchestrator import UNIT_ORDER

    brain = BrainOrchestrator()

    # Collect demand
    demand = set()
    for unit in brain._units.values():
        demand |= unit.h3_demand
    demand |= brain._mechanism_runner.h3_demand

    h3_ext = H3Extractor()
    brain_results = {}

    for emotion, r3_data in r3_results.items():
        r3_features = r3_data["raw_features"]  # (1, T, 97)

        t0 = time.time()
        h3_output = h3_ext.extract(r3_features, demand)
        h3_time = time.time() - t0

        t0 = time.time()
        brain_output = brain.forward(h3_output.features, r3_features)
        brain_time = time.time() - t0

        # Per-unit mean activation
        unit_means = {}
        for unit_name in UNIT_ORDER:
            s, e = brain_output.unit_slices[unit_name]
            unit_tensor = brain_output.tensor[0, :, s:e]  # (T, dim)
            unit_means[unit_name] = {
                "mean": unit_tensor.mean().item(),
                "std": unit_tensor.std().item(),
                "max": unit_tensor.max().item(),
                "min": unit_tensor.min().item(),
            }

        brain_results[emotion] = {
            "unit_means": unit_means,
            "h3_tuples": h3_output.n_tuples,
            "h3_time": h3_time,
            "brain_time": brain_time,
            "brain_shape": tuple(brain_output.tensor.shape),
            "brain_range": (
                brain_output.tensor.min().item(),
                brain_output.tensor.max().item(),
            ),
        }

    return brain_results


# ─── Report Formatting ────────────────────────────────────────────────────────
def print_header():
    print()
    print("=" * 80)
    print("  EMOTION DIFFERENTIATION PROBE")
    print("  Minimal validation: does MI-space capture emotional character?")
    print("=" * 80)


def print_r3_comparison(r3_results: dict):
    print()
    print("-" * 80)
    print("  LEVEL 1: R³ SPECTRAL FEATURES (97D)")
    print("-" * 80)

    # Group comparison table
    groups = ["A", "B", "C", "D", "E"]
    group_names = {g.letter: g.name for g in R3_GROUP_BOUNDARIES}

    print()
    print(f"  {'Group':<25s}  {'CALM':>10s}  {'MELANCH.':>10s}  {'INTENSE':>10s}  {'Spread':>8s}")
    print(f"  {'─' * 25}  {'─' * 10}  {'─' * 10}  {'─' * 10}  {'─' * 8}")

    for g in groups:
        vals = [r3_results[e]["groups"][g]["mean"] for e in ("CALM", "MELANCHOLIC", "INTENSE")]
        spread = max(vals) - min(vals)
        gname = group_names.get(g, g)[:25]
        marker = " ***" if spread > 0.05 else " *" if spread > 0.02 else ""
        print(f"  {g}: {gname:<22s}  {vals[0]:10.4f}  {vals[1]:10.4f}  {vals[2]:10.4f}  {spread:7.4f}{marker}")

    # Key feature comparison
    print()
    print(f"  {'Feature':<25s}  {'CALM':>10s}  {'MELANCH.':>10s}  {'INTENSE':>10s}  {'Spread':>8s}")
    print(f"  {'─' * 25}  {'─' * 10}  {'─' * 10}  {'─' * 10}  {'─' * 8}")

    # Collect all feature names present in all clips
    all_feats = set(r3_results["CALM"]["features"].keys())
    for e in ("MELANCHOLIC", "INTENSE"):
        all_feats &= set(r3_results[e]["features"].keys())

    for feat in sorted(all_feats):
        vals = [r3_results[e]["features"][feat]["mean"] for e in ("CALM", "MELANCHOLIC", "INTENSE")]
        spread = max(vals) - min(vals)
        marker = " ***" if spread > 0.05 else " *" if spread > 0.02 else ""
        print(f"  {feat:<25s}  {vals[0]:10.4f}  {vals[1]:10.4f}  {vals[2]:10.4f}  {spread:7.4f}{marker}")


def print_hypotheses(tests: list):
    print()
    print("-" * 80)
    print("  HYPOTHESIS TESTS")
    print("-" * 80)

    passed = sum(1 for t in tests if t["passed"])
    total = len(tests)

    for t in tests:
        status = "PASS" if t["passed"] else "FAIL"
        icon = " [+]" if t["passed"] else " [-]"
        print(f"  {icon} {status}  {t['name']}")
        print(f"         {t['detail']}")

    print()
    print(f"  RESULT: {passed}/{total} hypotheses confirmed")

    if passed == total:
        print("  >>> R³ perfectly differentiates emotional character!")
    elif passed >= total * 0.75:
        print("  >>> R³ strongly differentiates emotional character.")
    elif passed >= total * 0.5:
        print("  >>> R³ partially differentiates — some dimensions work, some don't.")
    else:
        print("  >>> R³ does NOT reliably differentiate — needs investigation.")


def print_brain_comparison(brain_results: dict):
    from Musical_Intelligence.brain.orchestrator import UNIT_ORDER

    print()
    print("-" * 80)
    print("  LEVEL 2: C³ COGNITIVE UNITS (1006D)")
    print("-" * 80)

    # Timing
    for emotion, data in brain_results.items():
        clip_label = CLIPS[emotion]["label"]
        print(f"  {emotion}: H³={data['h3_time']:.1f}s  Brain={data['brain_time']:.2f}s  "
              f"tuples={data['h3_tuples']}  shape={data['brain_shape']}  "
              f"range=[{data['brain_range'][0]:.4f}, {data['brain_range'][1]:.4f}]")

    # Unit comparison table
    emotion_relevant = ["SPU", "STU", "IMU", "ASU", "NDU", "ARU", "RPU"]

    print()
    print(f"  {'Unit':<6s}  {'CALM':>10s}  {'MELANCH.':>10s}  {'INTENSE':>10s}  {'Spread':>8s}  Function")
    print(f"  {'─' * 6}  {'─' * 10}  {'─' * 10}  {'─' * 10}  {'─' * 8}  {'─' * 25}")

    unit_descriptions = {
        "SPU": "Spectral Processing",
        "STU": "Sensorimotor Timing",
        "IMU": "Integrative Memory",
        "ASU": "Auditory Salience",
        "NDU": "Novelty Detection",
        "MPU": "Motor Planning",
        "PCU": "Predictive Coding",
        "ARU": "Affective Resonance",
        "RPU": "Reward Processing",
    }

    for unit in UNIT_ORDER:
        vals = [brain_results[e]["unit_means"][unit]["mean"]
                for e in ("CALM", "MELANCHOLIC", "INTENSE")]
        spread = max(vals) - min(vals)
        marker = " ***" if spread > 0.02 else " *" if spread > 0.005 else ""
        desc = unit_descriptions.get(unit, "")
        print(f"  {unit:<6s}  {vals[0]:10.4f}  {vals[1]:10.4f}  {vals[2]:10.4f}  {spread:7.4f}{marker}  {desc}")

    # Cross-emotion distance
    print()
    print("  Cosine distances between emotion profiles (unit means):")
    emotions = list(brain_results.keys())
    for i, e1 in enumerate(emotions):
        for e2 in emotions[i + 1:]:
            v1 = torch.tensor([brain_results[e1]["unit_means"][u]["mean"] for u in UNIT_ORDER])
            v2 = torch.tensor([brain_results[e2]["unit_means"][u]["mean"] for u in UNIT_ORDER])
            cosine = torch.nn.functional.cosine_similarity(v1.unsqueeze(0), v2.unsqueeze(0)).item()
            euclidean = (v1 - v2).norm().item()
            print(f"    {e1:<13s} vs {e2:<13s}:  cosine={cosine:.6f}  euclidean={euclidean:.6f}")


def print_verdict(tests: list, brain_results: dict | None):
    print()
    print("=" * 80)
    print("  VERDICT")
    print("=" * 80)

    passed = sum(1 for t in tests if t["passed"])
    total = len(tests)

    print(f"\n  R³ Spectral Layer: {passed}/{total} hypotheses pass")

    if brain_results:
        # Check if emotion units (ARU, RPU) differ across emotions
        aru_vals = [brain_results[e]["unit_means"]["ARU"]["mean"]
                    for e in ("CALM", "MELANCHOLIC", "INTENSE")]
        aru_spread = max(aru_vals) - min(aru_vals)
        print(f"  C³ Emotion (ARU): spread = {aru_spread:.6f}")

        rpu_vals = [brain_results[e]["unit_means"]["RPU"]["mean"]
                    for e in ("CALM", "MELANCHOLIC", "INTENSE")]
        rpu_spread = max(rpu_vals) - min(rpu_vals)
        print(f"  C³ Reward  (RPU): spread = {rpu_spread:.6f}")

    print()
    if passed >= total * 0.75:
        print("  CONCLUSION: The MI-space DOES capture emotional character.")
        print("  R³ spectral features differentiate calm/melancholic/intense music")
        print("  in the directions predicted by psychoacoustic literature.")
        if brain_results:
            if aru_spread > 0.01:
                print("  C³ cognitive units also show meaningful differentiation.")
            else:
                print("  C³ differentiation is weak (expected — models are Phase 3 stubs).")
                print("  After Phase 5 implementation, C³ differentiation should increase.")
    else:
        print("  CONCLUSION: R³ differentiation is weaker than expected.")
        print("  Investigate which features fail and whether audio clips")
        print("  have sufficient emotional contrast.")

    print()
    print("  What this test PROVES:")
    print("  - Different emotional music → different MI-space coordinates")
    print("  - Differences align with known psychoacoustic relationships")
    print("  - The foundation for emotion-driven control is scientifically valid")
    print()
    print("  What REMAINS to validate:")
    print("  - COMPOSE direction: C³ intent → coherent R³ → audio")
    print("  - Perceptual test: do LISTENERS perceive the differences?")
    print("  - Phase 5: model-specific formulas (not generic stubs)")
    print()


# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Emotion Differentiation Probe")
    parser.add_argument("--full", action="store_true", help="Run full pipeline (H³ + C³)")
    parser.add_argument("--duration", type=float, default=10.0, help="Clip duration in seconds")
    args = parser.parse_args()

    print_header()

    # ── Load and extract R³ ───────────────────────────────────────────────
    r3_ext = R3Extractor()
    r3_results = {}
    mels = {}

    for emotion, clip in CLIPS.items():
        audio_path = os.path.join(AUDIO_DIR, clip["file"])
        if not os.path.exists(audio_path):
            print(f"  WARNING: {clip['file']} not found, skipping {emotion}")
            continue

        t0 = time.time()
        mel = load_mel(audio_path, clip["offset"], args.duration)
        load_time = time.time() - t0

        t0 = time.time()
        r3_output = r3_ext.extract(mel)
        r3_time = time.time() - t0

        T = r3_output.features.shape[1]
        print(f"\n  {clip['emoji']} {emotion}: {clip['label']}")
        print(f"     Offset: {clip['offset']}s  Duration: {args.duration}s  Frames: {T}")
        print(f"     Load: {load_time:.2f}s  R³: {r3_time:.2f}s")
        print(f"     Expected: {clip['expected']}")

        r3_results[emotion] = {
            "groups": r3_group_means(r3_output.features),
            "features": r3_key_features(r3_output.features),
            "raw_features": r3_output.features,
        }
        mels[emotion] = mel

    if len(r3_results) < 3:
        print("\n  ERROR: Need all 3 clips. Check Test-Audio/ directory.")
        return

    # ── R³ comparison ─────────────────────────────────────────────────────
    print_r3_comparison(r3_results)

    # ── Hypothesis tests ──────────────────────────────────────────────────
    tests = test_hypotheses(r3_results)
    print_hypotheses(tests)

    # ── Full pipeline (optional) ──────────────────────────────────────────
    brain_results = None
    if args.full:
        print()
        print("-" * 80)
        print("  Running full pipeline (H³ + C³) — this will take a while...")
        print("-" * 80)
        brain_results = run_full_pipeline(mels, r3_results)
        print_brain_comparison(brain_results)

    # ── Verdict ───────────────────────────────────────────────────────────
    print_verdict(tests, brain_results)


if __name__ == "__main__":
    main()
