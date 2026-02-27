"""CHPI Functional Test — v1.0

Tests CHPI 11D output: E0-E1, M0-M1, P0-P2, F0-F3.

CHPI models cross-modal harmonic predictive integration:
  E0: crossmodal_prediction_gain (harmonic_change multi-scale + onset)
  E1: voiceleading_parsimony (pleasantness + tristimulus + (1-roughness) + (1-spec_vel))
  M0: visual_motor_lead (E0 + onset_periodicity + tonalness + chroma_C)
  M1: harmonic_surprise_mod (E1 + pleasantness_1s + (1-roughness) + dist_conc_vel)
  P0: harmonic_context_strength (HTP[3] + tonalness + chroma_C + (1-PWUP[3]) + M1)
  P1: crossmodal_convergence (E0 + M0 + WMED[0] + HTP[3] + pleas_entropy)
  P2: voiceleading_smoothness (E1 + tristimulus + (1-spec_change) + (1-chroma_vel) + (1-ICEM[0]))
  F0: next_chord_prediction (P0 + tonalness + chroma_C + pleasantness)
  F1: crossmodal_anticipation (P1 + E0 + periodicity_trend + chroma_I)
  F2: harmonic_trajectory (P2 + spec_change_vel + chroma_I + E1)
  F3: integration_confidence (P0 + P1 + P2 + pleasantness — meta-layer)

CHPI is an Integrator (depth 3), reads HTP, ICEM, PWUP, WMED.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F2/CHPI/run_chpi_functional_test.py
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
F0 = 7; F1 = 8; F2 = 9; F3 = 10

DIM_NAMES = [
    "E0:crossmodal_pred_gain", "E1:voiceleading_parsimony",
    "M0:visual_motor_lead", "M1:harmonic_surprise_mod",
    "P0:harmonic_context", "P1:crossmodal_convergence", "P2:voiceleading_smooth",
    "F0:next_chord_pred", "F1:crossmodal_antic", "F2:harmonic_trajectory",
    "F3:integration_confidence",
]
OUTPUT_DIM = 11


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class CHPITestRunner:
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
        relay = outputs.get("CHPI")
        if relay is None:
            raise RuntimeError(f"CHPI not found for '{name}'")
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
            # F3 aggregates all P-layer + pleasantness — may have low variance
            thresh = 0.0003 if d == F3 else 0.001
            self._test(G, f"T3_{DIM_NAMES[d]}", v > thresh,
                       f"std={v:.4f}>{thresh}")

    def test_T4_voiceleading(self):
        """E1 = voiceleading_parsimony: consonant stimuli should score higher
        (pleasantness + low roughness + low spectral change)."""
        G = "T4_voiceleading"
        e1_single = self._mean("g1_01_single", E1)
        e1_fifth = self._mean("g1_03_fifth", E1)
        e1_dense = self._mean("g3_04_dense", E1)
        # Consonant ≥ dissonant (with tolerance)
        self._test(G, "T4_single>=dense",
                   e1_single >= e1_dense - 0.05,
                   f"single({e1_single:.4f})>=dense({e1_dense:.4f})-0.05")
        self._test(G, "T4_fifth>=dense",
                   e1_fifth >= e1_dense - 0.05,
                   f"fifth({e1_fifth:.4f})>=dense({e1_dense:.4f})-0.05")

        # E1 bounded
        for stim in ["g1_01_single", "g1_03_fifth", "g3_04_dense"]:
            e1 = self._mean(stim, E1)
            self._test(G, f"T4_E1_bounded_{stim}", 0.0 <= e1 <= 1.0,
                       f"E1({e1:.4f}) in [0,1]")

    def test_T5_crossmodal_gain(self):
        """E0 = crossmodal_prediction_gain: responds to harmonic change.
        Temporal stimuli (arpeggio/melody) should show higher E0 than sustained."""
        G = "T5_crossmodal"
        e0_sustained = self._mean("g4_01_sustained", E0)
        e0_arpeggio = self._mean("g4_03_arpeggio", E0)
        self._test(G, "T5_arpeggio>=sustained",
                   e0_arpeggio >= e0_sustained - 0.05,
                   f"arpeggio({e0_arpeggio:.4f})>=sustained({e0_sustained:.4f})-0.05")

        # E0 bounded
        for stim in ["g1_01_single", "g4_01_sustained", "g4_03_arpeggio"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T5_E0_bounded_{stim}", 0.0 <= e0 <= 1.0,
                       f"E0({e0:.4f}) in [0,1]")

    def test_T6_m_layer(self):
        """M0 integrates E0 (30%), M1 integrates E1 (30%). Both should correlate."""
        G = "T6_m_layer"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        e0s = np.array([self._mean(s, E0) for s in stims])
        m0s = np.array([self._mean(s, M0) for s in stims])
        r = float(np.corrcoef(e0s, m0s)[0, 1])
        self._test(G, "T6_M0_E0_corr", abs(r) > 0.20,
                   f"|r(M0,E0)|={abs(r):.4f}>0.20 (E0→M0 at 30%)")

        e1s = np.array([self._mean(s, E1) for s in stims])
        m1s = np.array([self._mean(s, M1) for s in stims])
        r2 = float(np.corrcoef(e1s, m1s)[0, 1])
        self._test(G, "T6_M1_E1_corr", abs(r2) > 0.20,
                   f"|r(M1,E1)|={abs(r2):.4f}>0.20 (E1→M1 at 30%)")

    def test_T7_p_layer(self):
        """P-layer reads upstream relays. All P dims should be positive and bounded."""
        G = "T7_p_layer"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        for stim in stims:
            for d, nm in [(P0, "P0"), (P1, "P1"), (P2, "P2")]:
                val = self._mean(stim, d)
                self._test(G, f"T7_{nm}_pos_{stim}", val > 0.0,
                           f"{nm}({val:.4f})>0")

    def test_T8_forecast(self):
        """F0↔P0, F1↔P1, F3 is meta (P0+P1+P2)."""
        G = "T8_forecast"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_01_low", "g2_03_high", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        p0s = np.array([self._mean(s, P0) for s in stims])
        f0s = np.array([self._mean(s, F0) for s in stims])
        r = float(np.corrcoef(p0s, f0s)[0, 1])
        self._test(G, "T8_F0_P0_corr", r > 0.20,
                   f"r(F0,P0)={r:.4f}>0.20 (P0 feeds F0 at 30%)")

        p1s = np.array([self._mean(s, P1) for s in stims])
        f1s = np.array([self._mean(s, F1) for s in stims])
        r2 = float(np.corrcoef(p1s, f1s)[0, 1])
        self._test(G, "T8_F1_P1_corr", r2 > 0.20,
                   f"r(F1,P1)={r2:.4f}>0.20 (P1 feeds F1 at 35%)")

        # F3 = meta-integration: should correlate with P0 (at 30%)
        f3s = np.array([self._mean(s, F3) for s in stims])
        r3 = float(np.corrcoef(p0s, f3s)[0, 1])
        self._test(G, "T8_F3_P0_corr", abs(r3) > 0.10,
                   f"|r(F3,P0)|={abs(r3):.4f}>0.10 (P0 feeds F3 at 30%)")

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
            # Direct E→M feeds
            (0, 2), (1, 3),
            # E→P feeds
            (0, 5), (1, 6),
            # E→F feeds
            (0, 8), (1, 9),
            # M→P feeds
            (2, 5), (3, 4),
            # P→F feeds
            (4, 7), (4, 10), (5, 8), (5, 10), (6, 9), (6, 10),
            # Transitive E→M→P→F
            (0, 10), (1, 10), (2, 8), (2, 10), (3, 7), (3, 10),
            # F-F shared P inputs
            (7, 10), (8, 10), (9, 10),
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
                  self.test_T3_nondegeneracy, self.test_T4_voiceleading,
                  self.test_T5_crossmodal_gain, self.test_T6_m_layer,
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
        print(f"\n{'='*60}\n  CHPI FUNCTIONAL TEST RESULTS\n{'='*60}")
        print(f"  Total : {total}\n  Passed: {passed}\n  Failed: {failed}\n  Time  : {elapsed:.1f}s")
        print(f"{'='*60}")
        if failed:
            print(f"\n  FAILURES:")
            for r in self.results:
                if not r.passed:
                    print(f"    FAIL {r.name}: {r.message}")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {"mechanism": "CHPI", "function": "F2", "timestamp": ts,
                  "total": total, "passed": passed, "failed": failed,
                  "elapsed_s": round(elapsed, 1),
                  "results": [{"name": r.name, "group": r.group, "passed": r.passed,
                               "message": r.message, "values": r.values} for r in self.results]}
        out = RESULTS_DIR / f"chpi_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")

if __name__ == "__main__":
    CHPITestRunner().run_all()
