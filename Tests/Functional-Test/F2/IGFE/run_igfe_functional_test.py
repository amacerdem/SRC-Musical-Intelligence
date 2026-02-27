"""IGFE Functional Test — v1.0

Tests IGFE 9D output: E0-E1, M0-M1, P0-P2, F0-F1.

IGFE models individual gamma frequency enhancement:
  E0: igf_match (periodicity + tonalness)
  E1: memory_enhancement (amplitude + onset_strength)
  M0: executive_enhancement (multi-scale gamma entrainment)
  M1: dose_response (sustained stimulation)
  P0: gamma_synchronization (chroma coupling, reads HTP[3])
  P1: dose_accumulation (chroma periodicity, M1)
  P2: memory_access (H_coupling, reads WMED[1])
  F0: memory_enhancement_post (P2 + coupling trend)
  F1: executive_improve_post (P0 + P1 + amplitude)

IGFE is an Integrator (depth 3), reads HTP and WMED.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F2/IGFE/run_igfe_functional_test.py
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

E0 = 0; E1 = 1; M0 = 2; M1 = 3; P0 = 4; P1 = 5; P2 = 6; F0 = 7; F1 = 8

DIM_NAMES = [
    "E0:igf_match", "E1:memory_enhancement",
    "M0:executive_enhance", "M1:dose_response",
    "P0:gamma_sync", "P1:dose_accumulation", "P2:memory_access",
    "F0:mem_enhance_post", "F1:exec_improve_post",
]
OUTPUT_DIM = 9


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class IGFETestRunner:
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
        relay = outputs.get("IGFE")
        if relay is None:
            raise RuntimeError(f"IGFE not found for '{name}'")
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
            self._test(G, f"T3_{DIM_NAMES[d]}", v > 0.001,
                       f"std={v:.4f}>0.001")

    def test_T4_igf_match(self):
        G = "T4_igf_match"
        for stim in ["g1_01_single", "g1_03_fifth", "g2_02_mid"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T4_E0_pos_{stim}", e0 > 0.10,
                       f"E0({e0:.4f})>0.10 (tonal→gamma match)")

    def test_T5_memory_enhancement(self):
        G = "T5_mem_enhance"
        for stim in ["g1_01_single", "g4_02_melody", "g4_03_arpeggio"]:
            e1 = self._mean(stim, E1)
            self._test(G, f"T5_E1_pos_{stim}", e1 > 0.0,
                       f"E1({e1:.4f})>0")

    def test_T6_executive_dose(self):
        G = "T6_exec_dose"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        e0s = np.array([self._mean(s, E0) for s in stims])
        m0s = np.array([self._mean(s, M0) for s in stims])
        r = float(np.corrcoef(e0s, m0s)[0, 1])
        self._test(G, "T6_M0_E0_corr", r > 0.30,
                   f"r(M0,E0)={r:.4f}>0.30 (E0 feeds M0 at 30%)")

        e1s = np.array([self._mean(s, E1) for s in stims])
        m1s = np.array([self._mean(s, M1) for s in stims])
        r2 = float(np.corrcoef(e1s, m1s)[0, 1])
        self._test(G, "T6_M1_E1_corr", r2 > 0.20,
                   f"r(M1,E1)={r2:.4f}>0.20 (E1 feeds M1 at 30%)")

    def test_T7_p_layer(self):
        G = "T7_p_layer"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        for stim in stims:
            for d, nm in [(P0, "P0"), (P1, "P1"), (P2, "P2")]:
                val = self._mean(stim, d)
                self._test(G, f"T7_{nm}_pos_{stim}", val > 0.0,
                           f"{nm}({val:.4f})>0")

    def test_T8_forecast(self):
        G = "T8_forecast"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        p2s = np.array([self._mean(s, P2) for s in stims])
        f0s = np.array([self._mean(s, F0) for s in stims])
        r = float(np.corrcoef(p2s, f0s)[0, 1])
        self._test(G, "T8_F0_P2_corr", r > 0.20,
                   f"r(F0,P2)={r:.4f}>0.20 (P2 feeds F0 at 35%)")

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
            (0, 2), (0, 4), (1, 3), (1, 5), (1, 8),
            (2, 6), (3, 5), (4, 6), (4, 8),
            (5, 8), (6, 7),
            (0, 6), (0, 7), (0, 8),
            (2, 4), (3, 7),
            (7, 8),
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
                  self.test_T3_nondegeneracy, self.test_T4_igf_match,
                  self.test_T5_memory_enhancement, self.test_T6_executive_dose,
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
        print(f"\n{'='*60}\n  IGFE FUNCTIONAL TEST RESULTS\n{'='*60}")
        print(f"  Total : {total}\n  Passed: {passed}\n  Failed: {failed}\n  Time  : {elapsed:.1f}s")
        print(f"{'='*60}")
        if failed:
            print(f"\n  FAILURES:")
            for r in self.results:
                if not r.passed:
                    print(f"    FAIL {r.name}: {r.message}")
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {"mechanism": "IGFE", "function": "F2", "timestamp": ts,
                  "total": total, "passed": passed, "failed": failed,
                  "elapsed_s": round(elapsed, 1),
                  "results": [{"name": r.name, "group": r.group, "passed": r.passed,
                               "message": r.message, "values": r.values} for r in self.results]}
        out = RESULTS_DIR / f"igfe_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")

if __name__ == "__main__":
    IGFETestRunner().run_all()
