"""PCCR Functional Test — v1.0

Tests PCCR 11D output: E0(chroma_energy), E1(chroma_clarity),
E2(octave_coherence), E3(pitch_class_confidence), M0(chroma_stability),
P0(chroma_identity_signal), P1(octave_equivalence_index),
P2(chroma_salience), F0-F2(forecasts).

PCCR is an Associator (depth 2) reading both BCH and PSCL upstream.
E-layer uses linear weighted sums with scaling caps.
P-layer integrates BCH[1:harmonicity, 2:hierarchy] and PSCL[8:pitch_prominence, 10:periodicity].

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F1/PCCR/run_pccr_functional_test.py
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

# PCCR 11D indices
E0 = 0   # chroma_energy
E1 = 1   # chroma_clarity
E2 = 2   # octave_coherence
E3 = 3   # pitch_class_confidence
M0 = 4   # chroma_stability
P0 = 5   # chroma_identity_signal
P1 = 6   # octave_equivalence_index
P2 = 7   # chroma_salience
F0 = 8   # chroma_continuation_signal
F1 = 9   # chroma_transition_likelihood
F2 = 10  # chroma_resolution_direction

DIM_NAMES = [
    "E0:chroma_energy", "E1:chroma_clarity",
    "E2:octave_coherence", "E3:pitch_class_confidence",
    "M0:chroma_stability",
    "P0:chroma_identity_signal", "P1:octave_equivalence_index",
    "P2:chroma_salience",
    "F0:chroma_continuation", "F1:chroma_transition",
    "F2:chroma_resolution",
]
OUTPUT_DIM = 11


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class PCCRTestRunner:
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
        relay = outputs.get("PCCR")
        if relay is None:
            raise RuntimeError(f"PCCR not found for '{name}'")
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
    # T1: Chroma Energy (E0) — max(chroma) × pitch_salience
    # Higher for clear pitched sounds
    # ──────────────────────────────────────────────────────────────
    def test_T1_chroma_energy(self):
        G = "T1_chroma_energy"
        for stim in ["g1_01_single", "g1_02_octave", "g1_03_fifth",
                      "g3_01_low", "g3_02_mid", "g3_03_high"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T1_E0_positive_{stim}", e0 > 0.01,
                       f"E0({e0:.4f}) > 0.01 (pitched → chroma energy)")

        # Single note should have clear chroma
        e0_single = self._mean("g1_01_single", E0)
        e0_dense = self._mean("g2_04_dense", E0)
        self._test(G, "T1_E0_single>=dense",
                   e0_single > e0_dense - 0.10,
                   f"single({e0_single:.4f}) >= dense({e0_dense:.4f})-0.10")

    # ──────────────────────────────────────────────────────────────
    # T2: Chroma Clarity (E1) — (1-PCE) × tonalness
    # Higher when pitch class is unambiguous
    # ──────────────────────────────────────────────────────────────
    def test_T2_chroma_clarity(self):
        G = "T2_chroma_clarity"
        # Single note: clearest pitch class
        e1_single = self._mean("g1_01_single", E1)
        e1_dense = self._mean("g2_04_dense", E1)
        self._test(G, "T2_E1_single_positive", e1_single > 0.01,
                   f"E1({e1_single:.4f}) > 0.01 (single → clear chroma)")
        # Single >= dense (single has lower PCE)
        self._test(G, "T2_E1_single>=dense",
                   e1_single > e1_dense - 0.05,
                   f"single({e1_single:.4f}) >= dense({e1_dense:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T3: Octave Coherence (E2) — (1-inharmonicity) × spectral_autocorr
    # Higher for harmonic sounds
    # ──────────────────────────────────────────────────────────────
    def test_T3_octave_coherence(self):
        G = "T3_octave_coherence"
        for stim in ["g1_01_single", "g1_02_octave", "g1_03_fifth"]:
            e2 = self._mean(stim, E2)
            self._test(G, f"T3_E2_positive_{stim}", e2 > 0.01,
                       f"E2({e2:.4f}) > 0.01 (harmonic → octave coherence)")

    # ──────────────────────────────────────────────────────────────
    # T4: Chroma Stability (M0) — temporal integration of clarity
    # ──────────────────────────────────────────────────────────────
    def test_T4_chroma_stability(self):
        G = "T4_chroma_stability"
        stims = ["g1_01_single", "g1_03_fifth", "g2_04_dense",
                 "g4_01_sustained"]
        for stim in stims:
            m0 = self._mean(stim, M0)
            self._test(G, f"T4_M0_bounded_{stim}",
                       0.0 <= m0 <= 1.0,
                       f"M0({m0:.4f}) in [0,1]")

    # ──────────────────────────────────────────────────────────────
    # T5: Upstream Integration — P-layer reads BCH + PSCL
    # P0 reads PSCL[8,10], P1 reads BCH[1], P2 reads BCH[2]+PSCL[8]
    # ──────────────────────────────────────────────────────────────
    def test_T5_upstream_integration(self):
        G = "T5_upstream"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_04_dense"]
        for stim in stims:
            p0 = self._mean(stim, P0)
            p1 = self._mean(stim, P1)
            p2 = self._mean(stim, P2)
            # All P-layer should be bounded
            self._test(G, f"T5_P0_bounded_{stim}",
                       0.0 <= p0 <= 1.0,
                       f"P0({p0:.4f}) in [0,1]")
            self._test(G, f"T5_P1_bounded_{stim}",
                       0.0 <= p1 <= 1.0,
                       f"P1({p1:.4f}) in [0,1]")
            self._test(G, f"T5_P2_bounded_{stim}",
                       0.0 <= p2 <= 1.0,
                       f"P2({p2:.4f}) in [0,1]")

        # P1 (octave equivalence) uses BCH harmonicity —
        # higher for consonant intervals
        p1_single = self._mean("g1_01_single", P1)
        p1_dense = self._mean("g2_04_dense", P1)
        self._test(G, "T5_P1_single>=dense",
                   p1_single > p1_dense - 0.05,
                   f"single P1({p1_single:.4f}) >= dense({p1_dense:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T6: Register — Octave equivalence across C3/C4/C6
    # All Cs should have similar chroma identity (same pitch class)
    # ──────────────────────────────────────────────────────────────
    def test_T6_register(self):
        G = "T6_register"
        p0_low = self._mean("g3_01_low", P0)
        p0_mid = self._mean("g3_02_mid", P0)
        p0_high = self._mean("g3_03_high", P0)

        # All registers should produce chroma identity
        for reg, val in [("low", p0_low), ("mid", p0_mid), ("high", p0_high)]:
            self._test(G, f"T6_P0_{reg}_positive", val > 0.01,
                       f"P0({val:.4f}) > 0.01")

        # Report comparison
        self._pass(G, "T6_register_report",
                   f"P0: low={p0_low:.4f}, mid={p0_mid:.4f}, high={p0_high:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T7: Forecast (F0, F1, F2) — bounded and meaningful
    # ──────────────────────────────────────────────────────────────
    def test_T7_forecast(self):
        G = "T7_forecast"
        stims = ["g1_01_single", "g1_03_fifth", "g2_04_dense"]
        for stim in stims:
            f0 = self._mean(stim, F0)
            f1 = self._mean(stim, F1)
            f2 = self._mean(stim, F2)
            self._test(G, f"T7_F0_bounded_{stim}",
                       0.0 <= f0 <= 1.0, f"F0({f0:.4f}) in [0,1]")
            self._test(G, f"T7_F1_bounded_{stim}",
                       0.0 <= f1 <= 1.0, f"F1({f1:.4f}) in [0,1]")
            self._test(G, f"T7_F2_bounded_{stim}",
                       0.0 <= f2 <= 1.0, f"F2({f2:.4f}) in [0,1]")

    # ──────────────────────────────────────────────────────────────
    # T8: Consonance Hierarchy — dissonant → lower clarity/identity
    # ──────────────────────────────────────────────────────────────
    def test_T8_consonance(self):
        G = "T8_consonance"
        p0_single = self._mean("g1_01_single", P0)
        p0_octave = self._mean("g1_02_octave", P0)
        p0_fifth = self._mean("g1_03_fifth", P0)
        p0_m2 = self._mean("g1_05_minor_2nd", P0)

        # Consonant should have ≥ chroma identity than dissonant
        self._test(G, "T8_P0_single>=m2",
                   p0_single > p0_m2 - 0.05,
                   f"single({p0_single:.4f}) >= m2({p0_m2:.4f})-0.05")

        self._pass(G, "T8_consonance_report",
                   f"P0: single={p0_single:.4f}, octave={p0_octave:.4f}, "
                   f"fifth={p0_fifth:.4f}, m2={p0_m2:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T9: Bounds & Shape
    # ──────────────────────────────────────────────────────────────
    def test_T9_bounds_shape(self):
        G = "T9_bounds_shape"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g2_04_dense",
                 "g3_01_low", "g4_03_arpeggio"]
        for stim in stims:
            r = self._load_and_run(stim)
            self._test(G, f"T9_shape_{stim}",
                       r.ndim == 2 and r.shape[1] == OUTPUT_DIM,
                       f"shape={r.shape}")
            lo, hi = r.min(), r.max()
            self._test(G, f"T9_bounds_{stim}",
                       lo >= -1e-6 and hi <= 1.0 + 1e-6,
                       f"[{lo:.6f}, {hi:.6f}]")

    # ──────────────────────────────────────────────────────────────
    # T10: Redundancy Check
    # ──────────────────────────────────────────────────────────────
    def test_T10_redundancy(self):
        G = "T10_redundancy"
        stims = ["g1_01_single", "g1_02_octave", "g1_03_fifth",
                 "g1_04_tritone", "g1_05_minor_2nd", "g1_06_major_7th",
                 "g2_04_dense", "g3_01_low", "g3_03_high", "g4_03_arpeggio"]
        vals = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)]
                         for s in stims])

        # Architectural couplings in PCCR:
        #   E0(0) → P0(5): P0 = 0.25×E0 + ...
        #   E0(0) → P2(7): P2 = ... + 0.25×E0 + ...
        #   E1(1) → P0(5): P0 = ... + 0.20×E1 + ...
        #   E2(2) → P1(6): P1 = 0.40×E2 + ...
        #   E3(3) → P0(5): P0 = ... + 0.15×E3 + ...
        #   M0(4) → P0(5): P0 = ... + 0.15×M0 + ...
        #   M0(4) → F0(8): F0 = ... + 0.20×M0
        #   P0(5) → P2(7): P2 = 0.30×P0 + ...
        #   P0(5) → F2(10): F2 = ... + 0.25×P0 + ...
        #   E1(1) → P1(6): P1 = ... + 0.20×E1 + ...
        #   E3(3) → E0(0): both use pitch_salience
        COUPLED = {
            (0, 3),  # E0, E3 share pitch_salience
            (0, 5), (0, 7),
            (1, 5), (1, 6),
            (2, 6),
            (3, 5), (3, 10),  # E3, F2 share PCE + tonalness inputs
            (4, 5), (4, 8),
            (5, 7), (5, 10),
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
                    self._fail(G, f"T10_redundancy_{i}_{j}",
                               f"|r({DIM_NAMES[i]},{DIM_NAMES[j]})| = {r:.3f} > 0.99")
        if not redundant:
            self._pass(G, "T10_no_redundancy",
                       "No unexpected redundant dimension pairs")

    def run_all(self):
        tests = [
            ("T1: Chroma Energy (E0)", self.test_T1_chroma_energy),
            ("T2: Chroma Clarity (E1)", self.test_T2_chroma_clarity),
            ("T3: Octave Coherence (E2)", self.test_T3_octave_coherence),
            ("T4: Chroma Stability (M0)", self.test_T4_chroma_stability),
            ("T5: Upstream Integration (P0,P1,P2)", self.test_T5_upstream_integration),
            ("T6: Register/Octave Equivalence", self.test_T6_register),
            ("T7: Forecast (F0,F1,F2)", self.test_T7_forecast),
            ("T8: Consonance Hierarchy", self.test_T8_consonance),
            ("T9: Bounds & Shape", self.test_T9_bounds_shape),
            ("T10: Redundancy", self.test_T10_redundancy),
        ]

        print("=" * 72)
        print("PCCR FUNCTIONAL TEST v1.0")
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
        print(f"PCCR v1.0 — {passed}/{total} PASS")
        report = {"mechanism": "PCCR", "tests_total": total,
                  "tests_passed": passed, "results": [
                      {"name": r.name, "passed": r.passed, "message": r.message}
                      for r in self.results]}
        rp = RESULTS_DIR / "PCCR_FUNCTIONAL_TEST_REPORT.json"
        with open(rp, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Report: {rp}")
        print(f"OVERALL: {'ALL PASS' if passed == total else f'{total-passed} FAILED'}")
        print("=" * 72)
        return passed == total


if __name__ == "__main__":
    runner = PCCRTestRunner()
    sys.exit(0 if runner.run_all() else 1)
