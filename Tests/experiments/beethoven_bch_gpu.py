#!/usr/bin/env python3
"""Beethoven Pathétique — Single-Nucleus GPU Test (BCH on MPS).

Runs the first 60 seconds of Beethoven's Pathétique Sonata Op.13 I.
through the full MI pipeline with a single nucleus (BCH — Brainstem
Consonance Hierarchy), entirely on Apple MPS GPU.

Pipeline stages:
    1. Audio → mel spectrogram (CPU, then → MPS)
    2. R³ spectral feature extraction (97D) on MPS
    3. H³ temporal morphology extraction (BCH's 16 demands) on MPS
    4. Brain forward pass (BCH only, 12D output) on MPS

Output: Tests/reports/beethoven_bch_gpu_report.txt

Usage:
    python Tests/experiments/beethoven_bch_gpu.py
"""
from __future__ import annotations

import os
import sys
import time
from typing import Dict, List, Tuple

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
from torch import Tensor

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.h3 import H3Extractor
from Musical_Intelligence.brain.orchestrator import BrainOrchestrator
from Musical_Intelligence.brain.units.spu.relays.bch import BCH
from Musical_Intelligence.brain.psi_interpreter import PsiInterpreter
from Musical_Intelligence.ear.r3.constants import (
    R3_GROUP_BOUNDARIES,
    R3_FEATURE_NAMES,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
AUDIO_PATH = os.path.join(
    _PROJECT_ROOT,
    "Test-Audio",
    "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
)
REPORT_DIR = os.path.join(_PROJECT_ROOT, "Tests", "reports")
REPORT_PATH = os.path.join(REPORT_DIR, "beethoven_bch_gpu_report.txt")

SR = 44100
HOP = 256
N_MELS = 128
FRAME_RATE = SR / HOP  # 172.27 Hz
DURATION_S = 60.0  # First 60 seconds


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _sep(char: str = "=", width: int = 80) -> str:
    return char * width


def _section(title: str) -> str:
    return f"\n{'=' * 80}\n  {title}\n{'=' * 80}"


def frame_to_time(frame: int) -> float:
    return frame / FRAME_RATE


def time_to_frame(seconds: float) -> int:
    return int(round(seconds * FRAME_RATE))


def _load_mel(path: str, duration: float, device: torch.device) -> Tensor:
    """Load audio and compute normalised mel spectrogram on target device."""
    y, sr = librosa.load(path, sr=SR, mono=True, duration=duration)
    mel = librosa.feature.melspectrogram(
        y=y, sr=sr, n_mels=N_MELS, hop_length=HOP, n_fft=1024,
    )
    mel_db = librosa.power_to_db(mel, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    return torch.tensor(mel_norm, dtype=torch.float32, device=device).unsqueeze(0)


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------
class ReportWriter:
    def __init__(self, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self._file = open(filepath, "w", encoding="utf-8")

    def print(self, text: str = "") -> None:
        print(text, flush=True)
        self._file.write(text + "\n")
        self._file.flush()

    def close(self) -> None:
        self._file.close()


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------
def main() -> None:
    # ------------------------------------------------------------------
    # Device selection
    # ------------------------------------------------------------------
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    elif torch.cuda.is_available():
        device = torch.device("cuda")
    else:
        device = torch.device("cpu")

    rw = ReportWriter(REPORT_PATH)
    timings: Dict[str, float] = {}
    t_experiment = time.perf_counter()

    rw.print(_section("BEETHOVEN PATHÉTIQUE — BCH SINGLE-NUCLEUS GPU TEST"))
    rw.print(f"  Audio : {os.path.basename(AUDIO_PATH)}")
    rw.print(f"  Device: {device}")
    rw.print(f"  Duration: {DURATION_S:.0f}s")
    rw.print(f"  Frame rate: {FRAME_RATE:.2f} Hz")
    rw.print(f"  Nucleus: BCH (Brainstem Consonance Hierarchy, 12D)")
    rw.print()

    # ==================================================================
    # Stage 1: Load audio → mel on GPU
    # ==================================================================
    rw.print(_section("STAGE 1: Audio Loading → MPS"))
    if not os.path.exists(AUDIO_PATH):
        rw.print(f"  ERROR: Audio file not found: {AUDIO_PATH}")
        rw.close()
        sys.exit(1)

    t0 = time.perf_counter()
    mel = _load_mel(AUDIO_PATH, DURATION_S, device)
    timings["audio_load"] = time.perf_counter() - t0
    B, N, T = mel.shape
    duration_actual = T / FRAME_RATE

    rw.print(f"  Mel spectrogram: ({B}, {N}, {T})")
    rw.print(f"  Duration: {duration_actual:.1f}s ({T} frames)")
    rw.print(f"  Device: {mel.device}")
    rw.print(f"  Time: {timings['audio_load']:.3f}s")

    # ==================================================================
    # Stage 2: R³ extraction on GPU
    # ==================================================================
    rw.print(_section("STAGE 2: R³ Spectral Feature Extraction"))
    t0 = time.perf_counter()
    r3_ext = R3Extractor()
    r3_output = r3_ext.extract(mel)
    timings["r3_extraction"] = time.perf_counter() - t0
    r3_features = r3_output.features  # (B, T, 97)

    rw.print(f"  R³ output: {tuple(r3_features.shape)}")
    rw.print(f"  Device: {r3_features.device}")
    rw.print(f"  Value range: [{r3_features.min().item():.4f}, "
             f"{r3_features.max().item():.4f}]")
    rw.print(f"  Mean: {r3_features.mean().item():.4f}")
    rw.print(f"  Time: {timings['r3_extraction']:.3f}s")

    # R³ group summary
    rw.print(f"\n  R³ group means:")
    for g in R3_GROUP_BOUNDARIES:
        g_mean = r3_features[0, :, g.start:g.end].mean().item()
        g_std = r3_features[0, :, g.start:g.end].std().item()
        rw.print(f"    {g.letter} [{g.start:>3}:{g.end:>3}] "
                 f"mean={g_mean:.4f}  std={g_std:.4f}")

    # ==================================================================
    # Stage 3: H³ extraction (BCH demand only)
    # ==================================================================
    rw.print(_section("STAGE 3: H³ Temporal Morphology (BCH Demand)"))
    t0 = time.perf_counter()

    bch = BCH()
    bch_demand = bch.h3_demand_tuples()
    rw.print(f"  BCH demands: {len(bch_demand)} tuples")
    for tup in sorted(bch_demand):
        rw.print(f"    {tup}")

    h3_ext = H3Extractor()
    h3_output = h3_ext.extract(r3_features, bch_demand)
    timings["h3_extraction"] = time.perf_counter() - t0

    rw.print(f"\n  Computed tuples: {h3_output.n_tuples}")
    rw.print(f"  Time: {timings['h3_extraction']:.3f}s")

    # Sample H³ values
    rw.print(f"\n  H³ feature sample (t=0s, t=30s, t=55s):")
    for t_sec in [0.0, 30.0, 55.0]:
        frame = min(time_to_frame(t_sec), T - 1)
        rw.print(f"    t={t_sec:.0f}s (frame {frame}):")
        for key in sorted(h3_output.features.keys()):
            val = h3_output.features[key][0, frame].item()
            rw.print(f"      {key} = {val:.4f}")

    # Ensure H³ features are on GPU
    h3_features_gpu: Dict[Tuple[int, int, int, int], Tensor] = {}
    for key, tensor in h3_output.features.items():
        h3_features_gpu[key] = tensor.to(device)

    # ==================================================================
    # Stage 4: Brain forward pass (BCH only) on GPU
    # ==================================================================
    rw.print(_section("STAGE 4: Brain Forward Pass (BCH Only)"))
    t0 = time.perf_counter()

    # Ensure R³ on GPU
    r3_gpu = r3_features.to(device)

    brain = BrainOrchestrator(nuclei=[bch])
    brain_output = brain.process(r3_gpu, h3_features_gpu)
    timings["brain_forward"] = time.perf_counter() - t0

    brain_tensor = brain_output.tensor   # (B, T, N_ext)
    ram = brain_output.ram               # (B, T, 26)
    neuro = brain_output.neuro           # (B, T, 4)
    psi = brain_output.psi

    rw.print(f"  Brain tensor: {tuple(brain_tensor.shape)}")
    rw.print(f"  Device: {brain_tensor.device}")
    rw.print(f"  Value range: [{brain_tensor.min().item():.4f}, "
             f"{brain_tensor.max().item():.4f}]")
    rw.print(f"  Mean: {brain_tensor.mean().item():.4f}")
    rw.print(f"  Time: {timings['brain_forward']:.3f}s")

    # BCH exportable dimensions (external + hybrid = P + F = 6D)
    export_dims = bch.exportable_dims
    export_names = [bch.dimension_names[d] for d in export_dims]
    rw.print(f"\n  BCH exported dimensions ({len(export_dims)}D, external+hybrid):")
    for i, (dim_idx, name) in enumerate(zip(export_dims, export_names)):
        vals = brain_tensor[0, :, i]
        rw.print(f"    [{dim_idx:>2}] {name:<24} "
                 f"mean={vals.mean().item():.4f}  "
                 f"std={vals.std().item():.4f}  "
                 f"range=[{vals.min().item():.4f}, {vals.max().item():.4f}]")

    # ==================================================================
    # Analysis 1: RAM (Region Activation Map)
    # ==================================================================
    rw.print(_section("ANALYSIS 1: Region Activation Map (RAM)"))
    rw.print(f"  RAM shape: {tuple(ram.shape)}")
    rw.print(f"  Device: {ram.device}")

    from Musical_Intelligence.brain.regions import ALL_REGIONS
    ram_means = ram[0].mean(dim=0)  # (26,)
    for region in ALL_REGIONS:
        m = ram_means[region.index].item()
        if abs(m) > 1e-6:  # Only print active regions
            rw.print(f"    [{region.index:>2}] {region.abbreviation:<12} mean={m:.4f}")

    # ==================================================================
    # Analysis 2: Neurochemical state
    # ==================================================================
    rw.print(_section("ANALYSIS 2: Neurochemical State"))
    rw.print(f"  Neuro shape: {tuple(neuro.shape)}")
    neuro_names = ["DA (Dopamine)", "NE (Norepinephrine)",
                   "OPI (Opioid)", "5HT (Serotonin)"]
    for i, nname in enumerate(neuro_names):
        vals = neuro[0, :, i]
        rw.print(f"    {nname:<24} mean={vals.mean().item():.4f}  "
                 f"std={vals.std().item():.4f}  "
                 f"range=[{vals.min().item():.4f}, {vals.max().item():.4f}]")

    # ==================================================================
    # Analysis 3: Ψ³ cognitive interpretation
    # ==================================================================
    rw.print(_section("ANALYSIS 3: Ψ³ Cognitive Interpretation"))
    rw.print(f"  Affect:    {tuple(psi.affect.shape)}")
    rw.print(f"  Emotion:   {tuple(psi.emotion.shape)}")
    rw.print(f"  Aesthetic:  {tuple(psi.aesthetic.shape)}")
    rw.print(f"  Bodily:    {tuple(psi.bodily.shape)}")
    rw.print(f"  Cognitive: {tuple(psi.cognitive.shape)}")
    rw.print(f"  Temporal:  {tuple(psi.temporal.shape)}")
    rw.print(f"  Total Ψ³ dims: {psi.n_psi}")

    # Affect means
    affect_names = ["valence", "arousal", "tension", "dominance"]
    for i in range(min(psi.affect.shape[-1], len(affect_names))):
        vals = psi.affect[0, :, i]
        rw.print(f"    {affect_names[i]:<12} mean={vals.mean().item():.4f}  "
                 f"std={vals.std().item():.4f}")

    # ==================================================================
    # Analysis 4: Temporal dynamics — consonance over time
    # ==================================================================
    rw.print(_section("ANALYSIS 4: Consonance Dynamics Over Time"))
    # BCH exportable dims are P-layer (external) + F-layer (hybrid)
    # P: consonance_signal (idx 6), template_match (7), neural_pitch (8)
    # F: consonance_pred (9), pitch_propagation (10), interval_expect (11)
    # But after _assemble_tensor, only external+hybrid dims are kept.
    # Let's compute from the full 12D BCH output directly.

    rw.print(f"  5-second interval summary (from BCH full compute):")
    # Re-run BCH compute to get the full 12D (including internal E/M layers)
    bch_full = bch.compute(h3_features_gpu, r3_gpu)  # (B, T, 12)
    interval_frames = time_to_frame(5.0)

    header = f"  {'Time':>10} {'NPS':>8} {'Harm':>8} {'Hier':>8} " \
             f"{'Cons':>8} {'Tmpl':>8} {'Pitch':>8} {'Pred':>8}"
    rw.print(header)
    rw.print(f"  {'-' * 70}")

    for t_start in range(0, T, interval_frames):
        t_end = min(t_start + interval_frames, T)
        seg = bch_full[0, t_start:t_end, :]  # (frames, 12)
        seg_mean = seg.mean(dim=0)
        time_str = f"{frame_to_time(t_start):>4.0f}-{frame_to_time(t_end):>4.0f}s"
        rw.print(f"  {time_str:>10} "
                 f"{seg_mean[0].item():>8.4f} "  # f01_nps
                 f"{seg_mean[1].item():>8.4f} "  # f02_harmonicity
                 f"{seg_mean[2].item():>8.4f} "  # f03_hierarchy
                 f"{seg_mean[6].item():>8.4f} "  # consonance_signal
                 f"{seg_mean[7].item():>8.4f} "  # template_match
                 f"{seg_mean[8].item():>8.4f} "  # neural_pitch
                 f"{seg_mean[9].item():>8.4f}")   # consonance_pred

    # ==================================================================
    # Analysis 5: Peak consonance moments
    # ==================================================================
    rw.print(_section("ANALYSIS 5: Peak Consonance Moments"))
    cons_signal = bch_full[0, :, 6]  # consonance_signal (P-layer)
    top_vals, top_idx = torch.topk(cons_signal, min(10, T))
    rw.print(f"  Top 10 consonance peaks:")
    for i, (val, idx) in enumerate(zip(top_vals.tolist(), top_idx.tolist())):
        t_s = frame_to_time(idx)
        nps = bch_full[0, idx, 0].item()
        harm = bch_full[0, idx, 1].item()
        rw.print(f"    #{i+1}: t={t_s:>6.2f}s  consonance={val:.4f}  "
                 f"NPS={nps:.4f}  harmonicity={harm:.4f}")

    # Lowest consonance (most dissonant)
    bot_vals, bot_idx = torch.topk(cons_signal, min(10, T), largest=False)
    rw.print(f"\n  Top 10 dissonance troughs:")
    for i, (val, idx) in enumerate(zip(bot_vals.tolist(), bot_idx.tolist())):
        t_s = frame_to_time(idx)
        nps = bch_full[0, idx, 0].item()
        harm = bch_full[0, idx, 1].item()
        rw.print(f"    #{i+1}: t={t_s:>6.2f}s  consonance={val:.4f}  "
                 f"NPS={nps:.4f}  harmonicity={harm:.4f}")

    # ==================================================================
    # Timing summary
    # ==================================================================
    total_time = time.perf_counter() - t_experiment
    rw.print(_section("TIMING SUMMARY"))
    rw.print(f"  Device:              {device}")
    rw.print(f"  Audio loading:       {timings['audio_load']:>8.3f}s")
    rw.print(f"  R³ extraction:       {timings['r3_extraction']:>8.3f}s")
    rw.print(f"  H³ extraction:       {timings['h3_extraction']:>8.3f}s")
    rw.print(f"  Brain forward:       {timings['brain_forward']:>8.3f}s")
    pipeline_time = sum(timings.values())
    rw.print(f"  Pipeline total:      {pipeline_time:>8.3f}s")
    rw.print(f"  Analysis overhead:   {total_time - pipeline_time:>8.3f}s")
    rw.print(f"  Experiment total:    {total_time:>8.3f}s")

    # ==================================================================
    # Validation checks
    # ==================================================================
    rw.print(_section("VALIDATION"))
    checks_passed = 0
    checks_total = 0

    def check(name: str, condition: bool) -> None:
        nonlocal checks_passed, checks_total
        checks_total += 1
        status = "PASS" if condition else "FAIL"
        if condition:
            checks_passed += 1
        rw.print(f"  [{status}] {name}")

    # Shape checks
    check("R³ shape is (1, T, 97)", r3_features.shape == (1, T, 97))
    check("BCH full output is (1, T, 12)", bch_full.shape == (1, T, 12))
    check("RAM shape is (1, T, 26)", ram.shape == (1, T, 26))
    check("Neuro shape is (1, T, 4)", neuro.shape == (1, T, 4))

    # Value range checks
    check("R³ in [0, 1]",
          r3_features.min().item() >= -0.01 and r3_features.max().item() <= 1.01)
    check("BCH output has no NaN", not torch.isnan(bch_full).any().item())
    check("BCH output has no Inf", not torch.isinf(bch_full).any().item())
    check("RAM has no NaN", not torch.isnan(ram).any().item())
    check("Neuro has no NaN", not torch.isnan(neuro).any().item())

    # Device checks
    check(f"Brain tensor on {device}", str(brain_tensor.device).startswith(str(device)))
    check(f"RAM on {device}", str(ram.device).startswith(str(device)))
    check(f"Neuro on {device}", str(neuro.device).startswith(str(device)))

    # Semantic checks
    check("Consonance signal in [0, 1]",
          bch_full[:, :, 6].min().item() >= -0.01
          and bch_full[:, :, 6].max().item() <= 1.01)
    check("NPS (sigmoid) in [0, 1]",
          bch_full[:, :, 0].min().item() >= 0.0
          and bch_full[:, :, 0].max().item() <= 1.0)
    check("Consonance varies over time (std > 0.001)",
          bch_full[:, :, 6].std().item() > 0.001)
    check("NPS varies over time (std > 0.001)",
          bch_full[:, :, 0].std().item() > 0.001)

    rw.print(f"\n  {checks_passed}/{checks_total} checks passed")

    # ==================================================================
    # Final summary
    # ==================================================================
    rw.print(_section("EXPERIMENT SUMMARY"))
    rw.print(f"  Audio: Beethoven — Pathétique Sonata Op.13 I. Grave–Allegro")
    rw.print(f"  Duration: {duration_actual:.1f}s ({T} frames)")
    rw.print(f"  Device: {device}")
    rw.print(f"  Nucleus: BCH (12D)")
    rw.print(f"  Brain output: {tuple(brain_tensor.shape)}")
    rw.print(f"  R³ features: {tuple(r3_features.shape)}")
    rw.print(f"  H³ tuples: {h3_output.n_tuples}")
    rw.print(f"  Validation: {checks_passed}/{checks_total} passed")
    rw.print(f"  Total time: {total_time:.3f}s")
    rw.print(f"  Report: {REPORT_PATH}")
    rw.print(_sep())

    rw.close()
    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
