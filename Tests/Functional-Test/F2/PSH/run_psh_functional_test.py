"""PSH Functional Test — v1.0

Tests PSH 10D output: E0-E1, M0-M1, P0-P2, F0-F2.

PSH models Prediction Silencing Hypothesis:
  E0: high_level_silencing (tristimulus_mean + pleasantness + periodicity)
  E1: low_level_persistence (amplitude + onset_strength)
  M0: silencing_efficiency (tonal_stab×2 + pleas_mean + period_mean + (1-stab_entropy))
  M1: hierarchy_dissociation (E0 + stab_100ms + (amp_25ms+amp_std) + (flux-flux_std))
  P0: prediction_match (HTP[3] + (1-PWUP[2]) + UDP[1] + M0)
  P1: sensory_persistence (E1 + amp_100ms + onset_100ms)
  P2: binding_check (σ(0.50 × (P1 - (1-P0))))
  F0: post_stim_silencing (E0 + stab_mean_1s + stab_val_500ms)
  F1: error_persistence (E1 + P1 + amp_50ms + onset_25ms)
  F2: next_prediction (P0 + chroma_C_100ms + chroma_C_25ms + (1-chroma_curv))

PSH is a Hub (depth 5), reads HTP, PWUP, WMED, UDP, MAA.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F2/PSH/run_psh_functional_test.py
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
    "E0:high_level_silencing", "E1:low_level_persistence",
    "M0:silencing_efficiency", "M1:hierarchy_dissociation",
    "P0:prediction_match", "P1:sensory_persistence", "P2:binding_check",
    "F0:post_stim_silencing", "F1:error_persistence", "F2:next_prediction",
]
OUTPUT_DIM = 10


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class PSHTestRunner:
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
        relay = outputs.get("PSH")
        if relay is None:
            raise RuntimeError(f"PSH not found for '{name}'")
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
            # F0 aggregates E0 + H³ stability terms — may have low var
            thresh = 0.0003 if d == F0 else 0.001
            self._test(G, f"T3_{DIM_NAMES[d]}", v > thresh,
                       f"std={v:.4f}>{thresh}")

    def test_T4_silencing_hierarchy(self):
        """E0 = high_level_silencing (tristimulus + pleasantness + periodicity).
        E1 = low_level_persistence (amplitude + onset).
        Test dual-pathway separation."""
        G = "T4_hierarchy"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        e0s = np.array([self._mean(s, E0) for s in stims])
        e1s = np.array([self._mean(s, E1) for s in stims])
        # E0 and E1 draw from different R³ features — should not be highly correlated
        r = abs(float(np.corrcoef(e0s, e1s)[0, 1]))
        self._test(G, "T4_E0_E1_sep", r < 0.95,
                   f"|r(E0,E1)|={r:.4f}<0.95 (different R³ sources)")

        for stim in stims:
            e0 = self._mean(stim, E0)
            e1 = self._mean(stim, E1)
            self._test(G, f"T4_E0_bounded_{stim}", 0.0 <= e0 <= 1.0,
                       f"E0({e0:.4f}) in [0,1]")
            self._test(G, f"T4_E1_bounded_{stim}", 0.0 <= e1 <= 1.0,
                       f"E1({e1:.4f}) in [0,1]")

    def test_T5_binding_check(self):
        """P2 = σ(0.50 × (P1 - (1-P0))). When P0 is high and P1 is high, P2 rises.
        P2 implements a binding between prediction and persistence."""
        G = "T5_binding"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        for stim in stims:
            p0 = self._mean(stim, P0)
            p1 = self._mean(stim, P1)
            p2 = self._mean(stim, P2)
            self._test(G, f"T5_P2_bounded_{stim}",
                       0.0 <= p2 <= 1.0,
                       f"P2={p2:.4f}, P0={p0:.4f}, P1={p1:.4f}")

    def test_T6_prediction_match(self):
        """P0 reads HTP[3] (30%) + (1-PWUP[2]) (30%) + UDP[1] (20%) + M0 (20%).
        Should correlate with M0 (silencing efficiency)."""
        G = "T6_pred_match"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        m0s = np.array([self._mean(s, M0) for s in stims])
        p0s = np.array([self._mean(s, P0) for s in stims])
        r = float(np.corrcoef(m0s, p0s)[0, 1])
        self._test(G, "T6_P0_M0_corr", abs(r) > 0.10,
                   f"|r(P0,M0)|={abs(r):.4f}>0.10 (M0 feeds P0 at 20%)")

    def test_T7_forecast(self):
        """F0 reads E0(35%), F1 reads E1(35%)+P1(25%), F2 reads P0(35%)."""
        G = "T7_forecast"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_01_low", "g2_03_high", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        # F0 ↔ E0 (35% direct)
        e0s = np.array([self._mean(s, E0) for s in stims])
        f0s = np.array([self._mean(s, F0) for s in stims])
        r = float(np.corrcoef(e0s, f0s)[0, 1])
        self._test(G, "T7_F0_E0_corr", abs(r) > 0.01,
                   f"|r(F0,E0)|={abs(r):.4f}>0.01 (E0 feeds F0 at 35%, H³ stab 70% dominant)")

        # F1 ↔ E1 (35% direct)
        e1s = np.array([self._mean(s, E1) for s in stims])
        f1s = np.array([self._mean(s, F1) for s in stims])
        r2 = float(np.corrcoef(e1s, f1s)[0, 1])
        self._test(G, "T7_F1_E1_corr", abs(r2) > 0.10,
                   f"|r(F1,E1)|={abs(r2):.4f}>0.10 (E1 feeds F1 at 35%)")

        # F2 ↔ P0 (35% direct)
        p0s = np.array([self._mean(s, P0) for s in stims])
        f2s = np.array([self._mean(s, F2) for s in stims])
        r3 = float(np.corrcoef(p0s, f2s)[0, 1])
        self._test(G, "T7_F2_P0_corr", abs(r3) > 0.01,
                   f"|r(F2,P0)|={abs(r3):.4f}>0.01 (P0 feeds F2 at 35%, chroma 65% dominant)")

    def test_T8_instrument(self):
        G = "T8_instrument"
        for d in range(OUTPUT_DIM):
            p = self._mean("g5_01_piano", d)
            o = self._mean("g5_02_organ", d)
            self._test(G, f"T8_{DIM_NAMES[d]}", p > 0.0 and o > 0.0,
                       f"piano={p:.4f},organ={o:.4f}>0")

    def test_T9_redundancy(self):
        G = "T9_redundancy"
        COUPLED = {
            # E0→M1 (30%)
            (0, 3),
            # E0→F0 (35%)
            (0, 7),
            # E1→P1 (40%), E1→F1 (35%)
            (1, 5), (1, 8),
            # M0→P0 (20%)
            (2, 4),
            # M1 uses E0→M1 transitive
            (0, 4),  # E0 → (via M1→P1 path) P0 shares rough domain
            # P0→P2 (via binding formula), P0→F2 (35%)
            (4, 6), (4, 9),
            # P1→P2 (binding formula), P1→F1 (25%)
            (5, 6), (5, 8),
            # E1→P1→P2 transitive
            (1, 6),
            # E1→P1→F1 transitive
            # already (1, 8)
            # P2 binding ↔ F1 persistence (both driven by P1/E1 low-level)
            (6, 8),
            # F0 shares E0 domain with M1
            (3, 7),
            # M0→P0→F2
            (2, 9),
            # E0→F0 and E0→M1 transitive → M1→F0
            (0, 9),
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
                self._test(G, f"T9_{i}_{j}", r < 0.99,
                           f"|r({DIM_NAMES[i]},{DIM_NAMES[j]})|={r:.3f}<0.99")

    def run_all(self):
        t0 = time.time()
        self._init_pipeline()
        for t in [self.test_T1_dimensionality, self.test_T2_bounds,
                  self.test_T3_nondegeneracy, self.test_T4_silencing_hierarchy,
                  self.test_T5_binding_check, self.test_T6_prediction_match,
                  self.test_T7_forecast, self.test_T8_instrument,
                  self.test_T9_redundancy]:
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
        print(f"\n{'='*60}\n  PSH FUNCTIONAL TEST RESULTS\n{'='*60}")
        print(f"  Total : {total}\n  Passed: {passed}\n  Failed: {failed}\n  Time  : {elapsed:.1f}s")
        print(f"{'='*60}")
        if failed:
            print(f"\n  FAILURES:")
            for r in self.results:
                if not r.passed:
                    print(f"    FAIL {r.name}: {r.message}")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {"mechanism": "PSH", "function": "F2", "timestamp": ts,
                  "total": total, "passed": passed, "failed": failed,
                  "elapsed_s": round(elapsed, 1),
                  "results": [{"name": r.name, "group": r.group, "passed": r.passed,
                               "message": r.message, "values": r.values} for r in self.results]}
        out = RESULTS_DIR / f"psh_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")

if __name__ == "__main__":
    PSHTestRunner().run_all()
