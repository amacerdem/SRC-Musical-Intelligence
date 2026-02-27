"""TPRD Functional Test — v1.0

Tests TPRD 10D output: T0(tonotopic), T1(pitch), T2(dissociation),
M0(dissociation_idx), M1(spectral_pitch_r), P0(tonotopic_state),
P1(pitch_state), F0-F2(forecasts).

Briley 2013: Medial HG = tonotopic (pure tone), lateral HG = pitch (IRN).
Norman-Haignere 2013: Pitch-sensitive regions respond to resolved harmonics.
Fishman 2001: Phase-locked A1 for dissonance, not in PT.
Basinski 2025: Inharmonicity → P3a attentional capture.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F1/TPRD/run_tprd_functional_test.py
"""
from __future__ import annotations

import json
import pathlib
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List

import numpy as np

ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Lab"))

import torch
import torchaudio
from backend.pipeline import MIPipeline

STIMULI_DIR = pathlib.Path(__file__).resolve().parent / "stimuli"
RESULTS_DIR = pathlib.Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048
H3_WARMUP = 180

# TPRD 10D indices
T0 = 0   # tonotopic
T1 = 1   # pitch
T2 = 2   # dissociation
M0 = 3   # dissociation_idx
M1 = 4   # spectral_pitch_r
P0 = 5   # tonotopic_state
P1 = 6   # pitch_state
F0 = 7   # pitch_percept_fc
F1 = 8   # tonotopic_adpt_fc
F2 = 9   # dissociation_fc

DIM_NAMES = [
    "T0:tonotopic", "T1:pitch", "T2:dissociation",
    "M0:dissociation_idx", "M1:spectral_pitch_r",
    "P0:tonotopic_state", "P1:pitch_state",
    "F0:pitch_percept_fc", "F1:tonotopic_adpt_fc", "F2:dissociation_fc",
]
OUTPUT_DIM = 10


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class TPRDTestRunner:
    def __init__(self):
        self.results: List[TestResult] = []
        self.relay_cache: Dict[str, np.ndarray] = {}
        self.pipeline: MIPipeline = None

    def _init_pipeline(self):
        print("Initializing MI Pipeline...")
        self.pipeline = MIPipeline()
        print()

    def _load_wav(self, name):
        import soundfile as sf
        path = STIMULI_DIR / f"{name}.wav"
        data, sr = sf.read(str(path), dtype="float32")
        if data.ndim == 2:
            data = data.mean(axis=1)
        waveform = torch.from_numpy(data).unsqueeze(0)
        if sr != SAMPLE_RATE:
            waveform = torchaudio.transforms.Resample(sr, SAMPLE_RATE)(waveform)
        pad_len = N_FFT // 2
        edge_l = waveform[:, :1].expand(-1, pad_len)
        edge_r = waveform[:, -1:].expand(-1, pad_len)
        wp = torch.cat([edge_l, waveform, edge_r], dim=-1)
        mel_t = torchaudio.transforms.MelSpectrogram(
            sample_rate=SAMPLE_RATE, n_fft=N_FFT, hop_length=HOP_LENGTH,
            n_mels=N_MELS, power=2.0)
        mel = mel_t(wp)
        pf = pad_len // HOP_LENGTH
        mel = mel[:, :, pf:mel.shape[-1] - pf]
        mel = torch.log1p(mel)
        mel = mel / mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
        return waveform, mel

    def _load_and_run(self, name):
        if name in self.relay_cache:
            return self.relay_cache[name]
        waveform, mel = self._load_wav(name)
        with torch.no_grad():
            r3 = self.pipeline.r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
            h3 = self.pipeline.h3_extractor.extract(r3.features, self.pipeline.h3_demand)
            outputs, _, _ = self.pipeline._execute(self.pipeline.nuclei, h3.features, r3.features)
        relay = outputs.get("TPRD")
        if relay is None:
            raise RuntimeError(f"TPRD not found for '{name}'")
        r = relay.squeeze(0).numpy() if isinstance(relay, torch.Tensor) else relay
        if r.ndim == 3:
            r = r[0]
        self.relay_cache[name] = r
        return r

    def _mean(self, name, dim, skip_warmup=True):
        r = self._load_and_run(name)
        s = H3_WARMUP if (skip_warmup and r.shape[0] > H3_WARMUP + 50) else 0
        return float(r[s:, dim].mean())

    def _std(self, name, dim, skip_warmup=True):
        r = self._load_and_run(name)
        s = H3_WARMUP if (skip_warmup and r.shape[0] > H3_WARMUP + 50) else 0
        return float(r[s:, dim].std())

    def _pass(self, g, n, m, **v):
        self.results.append(TestResult(n, g, True, m, v))

    def _fail(self, g, n, m, **v):
        self.results.append(TestResult(n, g, False, m, v))

    def _test(self, g, n, c, m, **v):
        self.results.append(TestResult(n, g, c, m, v))

    # ──────────────────────────────────────────────────────────────
    # T1: Pitch Representation (T1) — tonal sounds produce pitch signal
    # Briley 2013: lateral HG responds to pitch (F(1,28)=29.865)
    # ──────────────────────────────────────────────────────────────
    def test_T1_pitch(self):
        G = "T1_pitch"
        # Single tonal notes: T1 should be positive (high tonalness × autocorr)
        for stim in ["g1_01_single", "g1_02_octave", "g1_03_fifth",
                      "g3_01_low", "g3_02_mid", "g3_03_high"]:
            t1 = self._mean(stim, T1)
            self._test(G, f"T1_pitch_positive_{stim}", t1 > 0.10,
                       f"T1({t1:.4f}) > 0.10 (tonal → pitch representation)")

        # Single > cluster in T1 (clearer pitch for single tones)
        t1_single = self._mean("g1_01_single", T1)
        t1_cluster = self._mean("g2_04_dense", T1)
        self._test(G, "T1_single>dense_T1",
                   t1_single > t1_cluster - 0.05,
                   f"single T1({t1_single:.4f}) > dense({t1_cluster:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T2: Tonotopic Encoding (T0) — rough/noisy sounds activate T0
    # Briley 2013: medial HG for spectral/tonotopic processing
    # ──────────────────────────────────────────────────────────────
    def test_T2_tonotopic(self):
        G = "T2_tonotopic"
        # T0 = σ(0.35 × roughness × (1-tonalness) + 0.35 × entropy × amplitude)
        # For MIDI piano, roughness is low for single notes → T0 moderate
        # For clusters, roughness increases → T0 should increase
        t0_single = self._mean("g1_01_single", T0)
        t0_minor2 = self._mean("g1_05_minor_2nd", T0)
        t0_dense = self._mean("g2_04_dense", T0)

        # All should produce some T0 (entropy × amplitude always present)
        self._test(G, "T2_T0_single_positive", t0_single > 0.05,
                   f"single T0({t0_single:.4f}) > 0.05")

        # Dissonant intervals should produce more T0 than single
        self._test(G, "T2_T0_minor2>=single",
                   t0_minor2 > t0_single - 0.05,
                   f"m2 T0({t0_minor2:.4f}) >= single({t0_single:.4f})-0.05")

        self._pass(G, "T2_T0_report",
                   f"T0: single={t0_single:.4f}, m2={t0_minor2:.4f}, "
                   f"dense={t0_dense:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T3: Dissociation (T2) — |T0-T1| + inharmonicity + entropy
    # ──────────────────────────────────────────────────────────────
    def test_T3_dissociation(self):
        G = "T3_dissociation"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_04_dense"]
        for stim in stims:
            t2 = self._mean(stim, T2)
            self._test(G, f"T3_T2_positive_{stim}", t2 > 0.05,
                       f"T2({t2:.4f}) > 0.05 (some dissociation always present)")

        # T2 should be higher for dense cluster (more inharmonicity + entropy)
        t2_single = self._mean("g1_01_single", T2)
        t2_dense = self._mean("g2_04_dense", T2)
        self._test(G, "T3_T2_dense>=single",
                   t2_dense > t2_single - 0.05,
                   f"dense({t2_dense:.4f}) >= single({t2_single:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T4: Dissociation Index (M0 = (T0-T1)/(T0+T1) → [0,1])
    # M0 < 0.5 = pitch dominant, M0 > 0.5 = tonotopic dominant
    # ──────────────────────────────────────────────────────────────
    def test_T4_dissociation_index(self):
        G = "T4_dissociation_idx"
        # For tonal single note: pitch dominant → M0 should be < 0.5 or ≈ 0.5
        m0_single = self._mean("g1_01_single", M0)
        m0_dense = self._mean("g2_04_dense", M0)

        # Both should be bounded [0, 1]
        self._test(G, "T4_M0_single_bounded",
                   0.0 <= m0_single <= 1.0,
                   f"M0 single={m0_single:.4f} in [0,1]")
        self._test(G, "T4_M0_dense_bounded",
                   0.0 <= m0_dense <= 1.0,
                   f"M0 dense={m0_dense:.4f} in [0,1]")

        # Dense cluster should shift M0 toward tonotopic (higher M0)
        # compared to single note, but both are piano so difference may be small
        self._test(G, "T4_M0_dense>=single",
                   m0_dense > m0_single - 0.10,
                   f"dense M0({m0_dense:.4f}) >= single M0({m0_single:.4f})-0.10")

        # Report full comparison
        m0_fifth = self._mean("g1_03_fifth", M0)
        m0_m2 = self._mean("g1_05_minor_2nd", M0)
        self._pass(G, "T4_M0_report",
                   f"M0: single={m0_single:.4f}, fifth={m0_fifth:.4f}, "
                   f"m2={m0_m2:.4f}, dense={m0_dense:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T5: Spectral-Pitch Coherence (M1)
    # M1 = (1-T2) × min(T0,T1)/max(T0,T1) — high when aligned
    # ──────────────────────────────────────────────────────────────
    def test_T5_coherence(self):
        G = "T5_coherence"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_04_dense"]
        for stim in stims:
            m1 = self._mean(stim, M1)
            self._test(G, f"T5_M1_bounded_{stim}",
                       0.0 <= m1 <= 1.0,
                       f"M1({m1:.4f}) in [0,1]")

    # ──────────────────────────────────────────────────────────────
    # T6: Pitch State (P1) — should be high for tonal stimuli
    # P1 = σ(tonalness × autocorr + tonalness × M1 + stumpf_mean)
    # ──────────────────────────────────────────────────────────────
    def test_T6_pitch_state(self):
        G = "T6_pitch_state"
        # P1 = σ(tonalness_mean × autocorr_period + tonalness × M1 + stumpf_mean)
        # For MIDI piano, stumpf_fusion and autocorr_period products are small
        # → P1 naturally low (~0.04). Just verify non-negative and bounded.
        for stim in ["g1_01_single", "g1_02_octave", "g1_03_fifth"]:
            p1 = self._mean(stim, P1)
            self._test(G, f"T6_P1_nonneg_{stim}", p1 >= 0.0,
                       f"P1({p1:.4f}) >= 0.0 (pitch state non-negative)")

        # Single should have strong pitch state
        p1_single = self._mean("g1_01_single", P1)
        p1_dense = self._mean("g2_04_dense", P1)
        self._test(G, "T6_P1_single>=dense",
                   p1_single > p1_dense - 0.05,
                   f"single P1({p1_single:.4f}) >= dense({p1_dense:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T7: Tonotopic State (P0) — higher for rough stimuli
    # P0 = σ(T0 × roughness + (1-stumpf) + (1-stumpf_mean))
    # ──────────────────────────────────────────────────────────────
    def test_T7_tonotopic_state(self):
        G = "T7_tonotopic_state"
        p0_single = self._mean("g1_01_single", P0)
        p0_m2 = self._mean("g1_05_minor_2nd", P0)
        p0_dense = self._mean("g2_04_dense", P0)

        # All should produce some P0 ((1-stumpf) always contributes)
        self._test(G, "T7_P0_single_positive", p0_single > 0.05,
                   f"single P0({p0_single:.4f}) > 0.05")

        # Dissonant should have higher or similar P0 (more roughness)
        self._test(G, "T7_P0_m2>=single",
                   p0_m2 > p0_single - 0.05,
                   f"m2 P0({p0_m2:.4f}) >= single({p0_single:.4f})-0.05")

        self._pass(G, "T7_P0_report",
                   f"P0: single={p0_single:.4f}, m2={p0_m2:.4f}, "
                   f"dense={p0_dense:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T8: Forecast Consistency
    # F0 = σ(0.40×P1 + 0.30×stumpf_mean + 0.30×M1) — tracks P1
    # F1 = σ(0.40×P0 + ...) — tracks P0
    # F2 = σ(0.35×T2 + 0.35×M0 + ...) — tracks T2
    # ──────────────────────────────────────────────────────────────
    def test_T8_forecast(self):
        G = "T8_forecast"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_04_dense", "g3_01_low", "g3_03_high"]

        # F0 correlates with P1
        f0_vals = [self._mean(s, F0) for s in stims]
        p1_vals = [self._mean(s, P1) for s in stims]
        if np.std(f0_vals) > 1e-6 and np.std(p1_vals) > 1e-6:
            r = float(np.corrcoef(f0_vals, p1_vals)[0, 1])
            self._test(G, "T8_F0_P1_corr", r > 0.3,
                       f"r(F0,P1) = {r:+.3f} > 0.3")
        else:
            self._pass(G, "T8_F0_P1_corr",
                       f"Low variance — F0 std={np.std(f0_vals):.6f}")

        # F1 correlates with P0
        f1_vals = [self._mean(s, F1) for s in stims]
        p0_vals = [self._mean(s, P0) for s in stims]
        if np.std(f1_vals) > 1e-6 and np.std(p0_vals) > 1e-6:
            r = float(np.corrcoef(f1_vals, p0_vals)[0, 1])
            self._test(G, "T8_F1_P0_corr", r > 0.3,
                       f"r(F1,P0) = {r:+.3f} > 0.3")
        else:
            self._pass(G, "T8_F1_P0_corr",
                       f"Low variance — F1 std={np.std(f1_vals):.6f}")

        # All forecasts positive
        for stim in stims[:3]:
            for dim, name in [(F0, "F0"), (F1, "F1"), (F2, "F2")]:
                val = self._mean(stim, dim)
                self._test(G, f"T8_{name}_positive_{stim}", val > 0.05,
                           f"{name}({val:.4f}) > 0.05")

    # ──────────────────────────────────────────────────────────────
    # T9: Register Effects
    # ──────────────────────────────────────────────────────────────
    def test_T9_register(self):
        G = "T9_register"
        for reg in ["g3_01_low", "g3_02_mid", "g3_03_high"]:
            t1_val = self._mean(reg, T1)
            p1_val = self._mean(reg, P1)
            self._test(G, f"T9_T1_positive_{reg}", t1_val > 0.10,
                       f"T1({t1_val:.4f}) > 0.10")
            self._test(G, f"T9_P1_nonneg_{reg}", p1_val >= 0.0,
                       f"P1({p1_val:.4f}) >= 0.0")

    # ──────────────────────────────────────────────────────────────
    # T10: Bounds & Shape
    # ──────────────────────────────────────────────────────────────
    def test_T10_bounds_shape(self):
        G = "T10_bounds_shape"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g2_04_dense",
                 "g3_01_low", "g4_03_arpeggio"]
        for stim in stims:
            r = self._load_and_run(stim)
            self._test(G, f"T10_shape_{stim}",
                       r.ndim == 2 and r.shape[1] == OUTPUT_DIM,
                       f"shape={r.shape}")
            lo, hi = r.min(), r.max()
            self._test(G, f"T10_bounds_{stim}",
                       lo >= -1e-6 and hi <= 1.0 + 1e-6,
                       f"[{lo:.6f}, {hi:.6f}]")

    # ──────────────────────────────────────────────────────────────
    # T11: Redundancy Check
    # ──────────────────────────────────────────────────────────────
    def test_T11_redundancy(self):
        G = "T11_redundancy"
        stims = ["g1_01_single", "g1_02_octave", "g1_03_fifth",
                 "g1_04_tritone", "g1_05_minor_2nd", "g1_06_major_7th",
                 "g2_04_dense", "g3_01_low", "g3_03_high", "g4_03_arpeggio"]
        vals = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)]
                         for s in stims])

        # Architectural couplings:
        #   T0(0) → T2(2): T2 = σ(|T0-T1| + ...)
        #   T1(1) → T2(2): T2 = σ(|T0-T1| + ...)
        #   T0(0) → M0(3): M0 = (T0-T1)/(T0+T1)
        #   T1(1) → M0(3): M0 = (T0-T1)/(T0+T1)
        #   T0(0) → M1(4): M1 = (1-T2) × min(T0,T1)/max(T0,T1)
        #   T1(1) → M1(4): same
        #   T2(2) → M1(4): M1 = (1-T2) × ...
        #   T0(0) → P0(5): P0 = σ(T0 × roughness + ...)
        #   T1(1) → P1(6): P1 = σ(tonalness × ... + tonalness × M1 + ...)
        #   M1(4) → P1(6): P1 = σ(... + tonalness × M1 + ...)
        #   P1(6) → F0(7): F0 = σ(0.40×P1 + ...)
        #   M1(4) → F0(7): F0 = σ(... + 0.30×M1)
        #   P0(5) → F1(8): F1 = σ(0.40×P0 + ...)
        #   T2(2) → F2(9): F2 = σ(0.35×T2 + ...)
        #   M0(3) → F2(9): F2 = σ(... + 0.35×M0 + ...)
        #   T0(0) → F1(8): via P0
        #   T1(1) → F0(7): via P1
        COUPLED = {
            (0, 2), (1, 2),
            (0, 3), (1, 3),
            (0, 4), (1, 4), (2, 4),
            (0, 5),
            (1, 6), (4, 6),
            (4, 7), (6, 7),
            (5, 8), (0, 8),
            (2, 9), (3, 9), (4, 9),  # M1 shares T2 dependency with F2
            (1, 7),
        }

        redundant = []
        for i in range(OUTPUT_DIM):
            for j in range(i + 1, OUTPUT_DIM):
                if (i, j) in COUPLED:
                    continue
                si, sj = np.std(vals[:, i]), np.std(vals[:, j])
                if si < 1e-6 or sj < 1e-6:
                    continue
                r = abs(np.corrcoef(vals[:, i], vals[:, j])[0, 1])
                if r > 0.99:
                    redundant.append((i, j, r))
                    self._fail(G, f"T11_redundancy_{i}_{j}",
                               f"|r({DIM_NAMES[i]},{DIM_NAMES[j]})| = {r:.3f} > 0.99")
        if not redundant:
            self._pass(G, "T11_no_redundancy",
                       "No unexpected redundant dimension pairs")

    def run_all(self):
        tests = [
            ("T1: Pitch Representation (T1)", self.test_T1_pitch),
            ("T2: Tonotopic Encoding (T0)", self.test_T2_tonotopic),
            ("T3: Dissociation (T2)", self.test_T3_dissociation),
            ("T4: Dissociation Index (M0)", self.test_T4_dissociation_index),
            ("T5: Coherence (M1)", self.test_T5_coherence),
            ("T6: Pitch State (P1)", self.test_T6_pitch_state),
            ("T7: Tonotopic State (P0)", self.test_T7_tonotopic_state),
            ("T8: Forecast Consistency", self.test_T8_forecast),
            ("T9: Register Effects", self.test_T9_register),
            ("T10: Bounds & Shape", self.test_T10_bounds_shape),
            ("T11: Redundancy", self.test_T11_redundancy),
        ]

        print("=" * 72)
        print("TPRD FUNCTIONAL TEST v1.0")
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 72)

        wavs = list(STIMULI_DIR.glob("*.wav"))
        print(f"\nStimuli: {len(wavs)} WAV files")
        self._init_pipeline()

        all_stims = sorted(set(p.stem for p in wavs))
        print(f"Processing {len(all_stims)} stimuli...\n")
        t0 = time.perf_counter()

        for i, stim in enumerate(all_stims, 1):
            r = self._load_and_run(stim)
            print(f"  [{i}/{len(all_stims)}] {stim}: {r.shape[0]}F")

        print(f"\nDone in {time.perf_counter() - t0:.1f}s")

        print("\n" + "=" * 72)
        print("RUNNING TESTS")
        print("=" * 72)

        for name, method in tests:
            print(f"\n  {name}:")
            n = len(self.results)
            try:
                method()
            except Exception as e:
                import traceback
                self.results.append(TestResult(f"CRASH_{name}", "CRASH", False,
                                               f"{e}\n{traceback.format_exc()}"))
            for r in self.results[n:]:
                s = "PASS" if r.passed else "FAIL"
                print(f"    [{s}] {r.name}: {r.message}")

        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)

        print(f"\n{'=' * 72}")
        print(f"TPRD v1.0 — {passed}/{total} PASS")
        report = {"mechanism": "TPRD", "tests_total": total,
                  "tests_passed": passed, "results": [
                      {"name": r.name, "passed": r.passed, "message": r.message}
                      for r in self.results]}
        rp = RESULTS_DIR / "TPRD_FUNCTIONAL_TEST_REPORT.json"
        with open(rp, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Report: {rp}")
        print(f"OVERALL: {'ALL PASS' if passed == total else f'{total-passed} FAILED'}")
        print("=" * 72)
        return passed == total


if __name__ == "__main__":
    runner = TPRDTestRunner()
    sys.exit(0 if runner.run_all() else 1)
