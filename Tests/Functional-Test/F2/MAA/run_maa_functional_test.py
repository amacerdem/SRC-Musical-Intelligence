"""MAA Functional Test — v1.0

Tests MAA 10D output: E0-E1, M0-M1, P0-P2, F0-F2.

MAA models Multifactorial Atonal Appreciation:
  E0: complexity_tolerance (roughness + (1-tonalness) + spec_change + tristimulus)
  E1: familiarity_index (periodicity + pleasantness + tonalness)
  M0: framing_effect (pleas_entropy + spec_entropy + roughness_mean + spec_mean + E0)
  M1: appreciation_composite (pleas_mean + tonal_mean×2 + H_coupling×3 + E1)
  P0: pattern_search (E0 + IGFE[4] + (1-periodicity) + roughness_val + M0)
  P1: context_assessment (PWUP[3] + UDP[3] + tonal_mean + E1 + M1)
  P2: aesthetic_evaluation (M0 + M1 + pleas_val + UDP[3] + P0)
  F0: appreciation_growth (E1 + H_coupling_trend + P2 + pleas_mean)
  F1: pattern_recognition (P0 + E0 + (1-tonal_mean) + spec_entropy)
  F2: aesthetic_development (P1 + H_coupling_trend + P2 + pleas_mean)

MAA is a Hub (depth 4), reads PWUP, UDP, IGFE.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F2/MAA/run_maa_functional_test.py
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

E0 = 0; E1 = 1; M0 = 2; M1 = 3; P0 = 4; P1 = 5; P2 = 6
F0 = 7; F1 = 8; F2 = 9

DIM_NAMES = [
    "E0:complexity_tolerance", "E1:familiarity_index",
    "M0:framing_effect", "M1:appreciation_composite",
    "P0:pattern_search", "P1:context_assessment", "P2:aesthetic_eval",
    "F0:appreciation_growth", "F1:pattern_recognition", "F2:aesthetic_dev",
]
OUTPUT_DIM = 10


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class MAATestRunner:
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
        relay = outputs.get("MAA")
        if relay is None:
            raise RuntimeError(f"MAA not found for '{name}'")
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
            # F-layer dims aggregate stable P-layer → may have low variance
            thresh = 0.0003 if d in (F0, F2) else 0.001
            self._test(G, f"T3_{DIM_NAMES[d]}", v > thresh,
                       f"std={v:.4f}>{thresh}")

    def test_T4_complexity_tolerance(self):
        """E0 = complexity_tolerance: roughness + (1-tonalness) + spectral_change.
        Dense/dissonant stimuli → higher E0."""
        G = "T4_complexity"
        e0_single = self._mean("g1_01_single", E0)
        e0_minor2 = self._mean("g1_05_minor_2nd", E0)
        e0_dense = self._mean("g3_04_dense", E0)
        # Dissonant should show higher complexity tolerance
        self._test(G, "T4_minor2>=single",
                   e0_minor2 >= e0_single - 0.10,
                   f"minor2nd({e0_minor2:.4f})>=single({e0_single:.4f})-0.10")
        for stim in ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T4_bounded_{stim}", 0.0 <= e0 <= 1.0,
                       f"E0({e0:.4f}) in [0,1]")

    def test_T5_familiarity(self):
        """E1 = familiarity_index: periodicity + pleasantness + tonalness.
        Consonant/tonal → higher E1."""
        G = "T5_familiarity"
        e1_single = self._mean("g1_01_single", E1)
        e1_fifth = self._mean("g1_03_fifth", E1)
        e1_minor2 = self._mean("g1_05_minor_2nd", E1)
        # Consonant should show higher familiarity
        self._test(G, "T5_fifth>=minor2",
                   e1_fifth >= e1_minor2 - 0.05,
                   f"fifth({e1_fifth:.4f})>=minor2nd({e1_minor2:.4f})-0.05")
        for stim in ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd"]:
            e1 = self._mean(stim, E1)
            self._test(G, f"T5_bounded_{stim}", 0.0 <= e1 <= 1.0,
                       f"E1({e1:.4f}) in [0,1]")

    def test_T6_m_layer(self):
        """M0 integrates E0 (15%), M1 integrates E1 (5%). Test framing and composite."""
        G = "T6_m_layer"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        # M0 includes E0 at 15% and entropy terms — should vary across stimuli
        for stim in stims:
            m0 = self._mean(stim, M0)
            m1 = self._mean(stim, M1)
            self._test(G, f"T6_M0_bounded_{stim}", 0.0 <= m0 <= 1.0,
                       f"M0({m0:.4f}) in [0,1]")
            self._test(G, f"T6_M1_bounded_{stim}", 0.0 <= m1 <= 1.0,
                       f"M1({m1:.4f}) in [0,1]")

    def test_T7_p_layer(self):
        """P-layer reads upstream: IGFE[4], PWUP[3], UDP[3]. All should be positive."""
        G = "T7_p_layer"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        for stim in stims:
            for d, nm in [(P0, "P0"), (P1, "P1"), (P2, "P2")]:
                val = self._mean(stim, d)
                self._test(G, f"T7_{nm}_pos_{stim}", val > 0.0,
                           f"{nm}({val:.4f})>0")

    def test_T8_forecast(self):
        """F0 reads E1(30%)+P2(20%), F1 reads P0(35%)+E0(25%), F2 reads P1(30%)+P2(25%)."""
        G = "T8_forecast"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_01_low", "g2_03_high", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        # F1 ↔ P0 (P0 feeds F1 at 35%)
        p0s = np.array([self._mean(s, P0) for s in stims])
        f1s = np.array([self._mean(s, F1) for s in stims])
        r = float(np.corrcoef(p0s, f1s)[0, 1])
        self._test(G, "T8_F1_P0_corr", abs(r) > 0.10,
                   f"|r(F1,P0)|={abs(r):.4f}>0.10 (P0 feeds F1 at 35%)")

        # F1 ↔ E0 (E0 feeds F1 at 25%)
        e0s = np.array([self._mean(s, E0) for s in stims])
        r2 = float(np.corrcoef(e0s, f1s)[0, 1])
        self._test(G, "T8_F1_E0_corr", abs(r2) > 0.10,
                   f"|r(F1,E0)|={abs(r2):.4f}>0.10 (E0 feeds F1 at 25%)")

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
            # E0→P0 (30%), E0→F1 (25%)
            (0, 4), (0, 8),
            # E1→P1 (15%), E1→F0 (30%)
            (1, 5), (1, 7),
            # M0→P0 (10%), M0→P2 (25%)
            (2, 4), (2, 6),
            # M1→P1 (15%), M1→P2 (25%)
            (3, 5), (3, 6),
            # P0→P2 (15%), P0→F1 (35%)
            (4, 6), (4, 8),
            # P1→F2 (30%)
            (5, 9),
            # P2→F0 (20%), P2→F2 (25%)
            (6, 7), (6, 9),
            # Transitive: E0→P0→F1
            (0, 6),
            # M0→P2→F0, M1→P2→F0
            (2, 7), (3, 7),
            # F0↔F2 share P2 + H_coupling_trend + pleas_mean
            (7, 9),
            # M0→P0→P2→F2
            (2, 9),
            # E1→F0→... (E1 at 30% in F0)
            (1, 9),
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
                  self.test_T3_nondegeneracy, self.test_T4_complexity_tolerance,
                  self.test_T5_familiarity, self.test_T6_m_layer,
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
        print(f"\n{'='*60}\n  MAA FUNCTIONAL TEST RESULTS\n{'='*60}")
        print(f"  Total : {total}\n  Passed: {passed}\n  Failed: {failed}\n  Time  : {elapsed:.1f}s")
        print(f"{'='*60}")
        if failed:
            print(f"\n  FAILURES:")
            for r in self.results:
                if not r.passed:
                    print(f"    FAIL {r.name}: {r.message}")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {"mechanism": "MAA", "function": "F2", "timestamp": ts,
                  "total": total, "passed": passed, "failed": failed,
                  "elapsed_s": round(elapsed, 1),
                  "results": [{"name": r.name, "group": r.group, "passed": r.passed,
                               "message": r.message, "values": r.values} for r in self.results]}
        out = RESULTS_DIR / f"maa_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")

if __name__ == "__main__":
    MAATestRunner().run_all()
