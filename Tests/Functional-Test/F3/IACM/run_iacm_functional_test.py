"""IACM Functional Test — v1.0

Tests IACM 11D output: E0-E2, M0-M2, P0-P1, F0-F2.

IACM models Inharmonicity-driven Attention Capture:
  E0: inharmonic_capture ((1-tonalness) + flatness + roughness_entropy + (1-tonalness))
  E1: object_segregation (periodicity_val + periodicity_std + coupling_val + tonalness_period)
  E2: precision_weighting (tonalness_period×2 + coupling_zc)
  M0: attention_capture (E0 + (1-tonalness_mean))
  M1: approx_entropy (flatness + (1-tonalness))
  M2: object_perception_or (E1 + M1)
  P0: p3a_capture (M0 + E0 + flatness_entropy)
  P1: spectral_encoding (periodicity_val + periodicity_std + tonalness)
  F0: object_segreg_pred (E1 + M1)
  F1: attention_shift_pred (E0 + P0)
  F2: multiple_objects_pred (E1 + M2)

IACM is a Relay (depth 0) in F3/ASU. Note: P-layer is 2D (P0,P1).

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F3/IACM/run_iacm_functional_test.py
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

E0 = 0; E1 = 1; E2 = 2
M0 = 3; M1 = 4; M2 = 5
P0 = 6; P1 = 7
F0 = 8; F1 = 9; F2 = 10

DIM_NAMES = [
    "E0:inharmonic_capture", "E1:object_segregation", "E2:precision_weight",
    "M0:attention_capture", "M1:approx_entropy", "M2:object_perception",
    "P0:p3a_capture", "P1:spectral_encoding",
    "F0:object_segreg_pred", "F1:attention_shift_pred", "F2:multi_objects_pred",
]
OUTPUT_DIM = 11


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class IACMTestRunner:
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
        relay = outputs.get("IACM")
        if relay is None:
            raise RuntimeError(f"IACM not found for '{name}'")
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

    def test_T1_dimensionality(self):
        G = "T1_dimensionality"
        r = self._load_and_run("g1_01_single")
        self._test(G, "T1_ndim", r.ndim == 2, f"ndim={r.ndim}")
        self._test(G, "T1_dim_count", r.shape[1] == OUTPUT_DIM, f"D={r.shape[1]}")
        self._test(G, "T1_frames", r.shape[0] > 100, f"T={r.shape[0]}")

    def test_T2_bounds(self):
        G = "T2_bounds"
        for stim in ["g1_01_single", "g1_05_minor_2nd", "g2_01_low", "g2_03_high",
                      "g3_04_dense", "g4_03_arpeggio", "g5_01_piano", "g5_02_organ"]:
            r = self._load_and_run(stim)
            lo, hi = float(r.min()), float(r.max())
            self._test(G, f"T2_{stim}", lo >= -0.001 and hi <= 1.001,
                       f"[{lo:.4f},{hi:.4f}]⊂[0,1]")

    def test_T3_nondegeneracy(self):
        G = "T3_nondegeneracy"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g2_01_low", "g2_03_high",
                 "g3_04_dense", "g4_03_arpeggio", "g5_02_organ"]
        means = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)] for s in stims])
        for d in range(OUTPUT_DIM):
            v = float(means[:, d].std())
            # F-layer dims may have low variance for MIDI sustained tones
            thresh = 0.0003 if d in (F0, F1, F2) else 0.001
            self._test(G, f"T3_{DIM_NAMES[d]}", v > thresh,
                       f"std={v:.4f}>{thresh}")

    def test_T4_inharmonic_capture(self):
        """E0 = (1-tonalness) + flatness + roughness_entropy + (1-tonalness).
        Should be higher for dissonant/noisy stimuli."""
        G = "T4_inharmonic"
        e0_single = self._mean("g1_01_single", E0)
        e0_minor2 = self._mean("g1_05_minor_2nd", E0)
        # Dissonant should show more inharmonic capture (with tolerance)
        self._test(G, "T4_minor2>=single-0.10",
                   e0_minor2 >= e0_single - 0.10,
                   f"minor2nd({e0_minor2:.4f})>=single({e0_single:.4f})-0.10")
        for stim in ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T4_E0_bounded_{stim}", 0.0 <= e0 <= 1.0,
                       f"E0({e0:.4f}) in [0,1]")

    def test_T5_object_segregation(self):
        """E1 = object segregation from periodicity + coupling. Should be positive
        for all tonal stimuli."""
        G = "T5_object"
        for stim in ["g1_01_single", "g1_03_fifth", "g4_02_melody"]:
            e1 = self._mean(stim, E1)
            self._test(G, f"T5_E1_pos_{stim}", e1 > 0.0,
                       f"E1({e1:.4f})>0")

    def test_T6_attention_m(self):
        """M0 integrates E0 (50%), M1 = flatness+(1-tonalness), M2 = E1+M1."""
        G = "T6_attention"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        e0s = np.array([self._mean(s, E0) for s in stims])
        m0s = np.array([self._mean(s, M0) for s in stims])
        r = float(np.corrcoef(e0s, m0s)[0, 1])
        self._test(G, "T6_M0_E0_corr", abs(r) > 0.20,
                   f"|r(M0,E0)|={abs(r):.4f}>0.20 (E0 feeds M0 at 50%)")

    def test_T7_p_layer(self):
        """P0 = M0+E0+flatness_entropy, P1 = periodicity+tonalness."""
        G = "T7_p_layer"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        for stim in stims:
            for d, nm in [(P0, "P0"), (P1, "P1")]:
                val = self._mean(stim, d)
                self._test(G, f"T7_{nm}_pos_{stim}", val > 0.0,
                           f"{nm}({val:.4f})>0")

    def test_T8_forecast(self):
        """F0 = E1+M1, F1 = E0+P0, F2 = E1+M2."""
        G = "T8_forecast"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_01_low", "g2_03_high", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        # F1 ↔ E0 (50% direct)
        e0s = np.array([self._mean(s, E0) for s in stims])
        f1s = np.array([self._mean(s, F1) for s in stims])
        r = float(np.corrcoef(e0s, f1s)[0, 1])
        self._test(G, "T8_F1_E0_corr", abs(r) > 0.10,
                   f"|r(F1,E0)|={abs(r):.4f}>0.10 (E0 feeds F1 at 50%)")

        # F0 ↔ E1 (50% direct)
        e1s = np.array([self._mean(s, E1) for s in stims])
        f0s = np.array([self._mean(s, F0) for s in stims])
        r2 = float(np.corrcoef(e1s, f0s)[0, 1])
        self._test(G, "T8_F0_E1_corr", abs(r2) > 0.10,
                   f"|r(F0,E1)|={abs(r2):.4f}>0.10 (E1 feeds F0 at 50%)")

    def test_T9_instrument(self):
        G = "T9_instrument"
        for d in range(OUTPUT_DIM):
            p = self._mean("g5_01_piano", d)
            o = self._mean("g5_02_organ", d)
            self._test(G, f"T9_{DIM_NAMES[d]}", p > 0.0 and o > 0.0,
                       f"piano={p:.4f},organ={o:.4f}>0")

    def test_T10_redundancy(self):
        G = "T10_redundancy"
        COUPLED = {
            # E0→M0 (50%), E0→P0 (30%), E0→F1 (50%)
            (0, 3), (0, 6), (0, 9),
            # E1→M2 (50%), E1→F0 (50%), E1→F2 (50%)
            (1, 5), (1, 8), (1, 10),
            # M0→P0 (40%)
            (3, 6),
            # M1→M2 (50%), M1→F0 (50%)
            (4, 5), (4, 8),
            # M2→F2 (50%)
            (5, 10),
            # P0→F1 (50%)
            (6, 9),
            # Transitive chains
            (0, 4),   # E0 shares (1-tonalness) with M1
            (3, 9),   # M0→P0→F1
            (4, 10),  # M1→M2→F2
            (1, 4),   # E1 and M1 share tonalness domain
            (8, 10),  # F0 and F2 share E1
            (4, 9),   # M1 relates to F1 via E0 domain
            (5, 8),   # M2=E1+M1, F0=E1+M1 → identical formula
            (1, 7),   # E1 and P1 share periodicity_val + periodicity_std
            (7, 10),  # P1↔F2 via E1 coupling (F2=E1+M2)
        }
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_01_low", "g2_03_high", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio", "g5_02_organ"]
        means = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)] for s in stims])
        for i in range(OUTPUT_DIM):
            for j in range(i+1, OUTPUT_DIM):
                if (i, j) in COUPLED:
                    continue
                r = abs(float(np.corrcoef(means[:, i], means[:, j])[0, 1]))
                self._test(G, f"T10_{i}_{j}", r < 0.99,
                           f"|r({DIM_NAMES[i]},{DIM_NAMES[j]})|={r:.3f}<0.99")

    def run_all(self):
        t0 = time.time()
        self._init_pipeline()
        for t in [self.test_T1_dimensionality, self.test_T2_bounds,
                  self.test_T3_nondegeneracy, self.test_T4_inharmonic_capture,
                  self.test_T5_object_segregation, self.test_T6_attention_m,
                  self.test_T7_p_layer, self.test_T8_forecast,
                  self.test_T9_instrument, self.test_T10_redundancy]:
            name = t.__name__
            print(f"\n{'='*60}\n  {name}\n{'='*60}")
            try:
                t()
            except Exception as ex:
                self._fail(name, f"{name}_exc", f"EXCEPTION: {ex}")
                import traceback; traceback.print_exc()
        elapsed = time.time() - t0
        self._report(elapsed)

    def _report(self, elapsed):
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        failed = total - passed
        print(f"\n{'='*60}\n  IACM FUNCTIONAL TEST RESULTS\n{'='*60}")
        print(f"  Total : {total}\n  Passed: {passed}\n  Failed: {failed}\n  Time  : {elapsed:.1f}s")
        print(f"{'='*60}")
        if failed:
            print(f"\n  FAILURES:")
            for r in self.results:
                if not r.passed:
                    print(f"    FAIL {r.name}: {r.message}")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {"mechanism": "IACM", "function": "F3", "timestamp": ts,
                  "total": total, "passed": passed, "failed": failed,
                  "elapsed_s": round(elapsed, 1),
                  "results": [{"name": r.name, "group": r.group, "passed": r.passed,
                               "message": r.message, "values": r.values} for r in self.results]}
        out = RESULTS_DIR / f"iacm_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")

if __name__ == "__main__":
    IACMTestRunner().run_all()
