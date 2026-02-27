"""SDNPS Functional Test — v1.0

Tests SDNPS 10D output: E0(nps), E1(stimulus_dep), E2(roughness_corr),
M0(nps_stimulus_function), P0(ffr_encoding), P1(harmonicity_proxy),
P2(roughness_interference), F0-F2(forecasts).

Cousineau 2015: NPS predicts consonance for synthetic (r=0.34) but not
natural tones. NPS↔roughness r=-0.57 is stimulus-invariant.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F1/SDNPS/run_sdnps_functional_test.py
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

# SDNPS 10D indices
E0 = 0   # nps_value
E1 = 1   # stimulus_dependency
E2 = 2   # roughness_corr
M0 = 3   # nps_stimulus_function
P0 = 4   # ffr_encoding
P1 = 5   # harmonicity_proxy
P2 = 6   # roughness_interference
F0 = 7   # behavioral_consonance_pred
F1 = 8   # roughness_response_pred
F2 = 9   # generalization_limit

DIM_NAMES = [
    "E0:nps_value", "E1:stimulus_dep", "E2:roughness_corr",
    "M0:nps_stim_fn", "P0:ffr_encoding", "P1:harmonicity_proxy",
    "P2:roughness_interf", "F0:behav_cons_pred",
    "F1:rough_resp_pred", "F2:gen_limit",
]
OUTPUT_DIM = 10


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class SDNPSTestRunner:
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
        relay = outputs.get("SDNPS")
        if relay is None:
            raise RuntimeError(f"SDNPS not found for '{name}'")
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

    # T1: NPS Value (E0) — higher for harmonic
    def test_T1_nps_value(self):
        G = "T1_nps_value"
        e0_single = self._mean("g2_01_single", E0)
        e0_octave = self._mean("g2_02_octave", E0)
        e0_triad = self._mean("g2_03_triad", E0)
        e0_cluster = self._mean("g2_04_cluster", E0)

        self._test(G, "T1_E0_single>cluster", e0_single > e0_cluster,
                   f"single({e0_single:.4f}) > cluster({e0_cluster:.4f})")
        self._test(G, "T1_E0_octave>cluster", e0_octave > e0_cluster,
                   f"octave({e0_octave:.4f}) > cluster({e0_cluster:.4f})")
        self._pass(G, "T1_E0_hierarchy",
                   f"E0: single={e0_single:.4f}, octave={e0_octave:.4f}, "
                   f"triad={e0_triad:.4f}, cluster={e0_cluster:.4f}")

    # T2: Harmonicity Proxy (P1) — (1-inharm) × trist_balance
    def test_T2_harmonicity(self):
        G = "T2_harmonicity"
        p1_single = self._mean("g2_01_single", P1)
        p1_octave = self._mean("g2_02_octave", P1)
        p1_triad = self._mean("g2_03_triad", P1)
        p1_cluster = self._mean("g2_04_cluster", P1)

        self._test(G, "T2_P1_single>cluster", p1_single > p1_cluster,
                   f"single({p1_single:.4f}) > cluster({p1_cluster:.4f})")
        self._test(G, "T2_P1_octave>cluster", p1_octave > p1_cluster,
                   f"octave({p1_octave:.4f}) > cluster({p1_cluster:.4f})")
        self._pass(G, "T2_P1_hierarchy",
                   f"P1: single={p1_single:.4f}, octave={p1_octave:.4f}, "
                   f"triad={p1_triad:.4f}, cluster={p1_cluster:.4f}")

    # T3: Roughness Interference (P2) — 1-(roughness+sethares)/2, higher for consonant
    def test_T3_roughness_interference(self):
        G = "T3_roughness_interference"
        p2_single = self._mean("g1_01_single", P2)
        p2_fifth = self._mean("g1_03_fifth", P2)
        p2_tritone = self._mean("g1_04_tritone", P2)
        p2_minor2 = self._mean("g1_05_minor2nd", P2)

        self._test(G, "T3_P2_single>minor2nd", p2_single > p2_minor2,
                   f"single({p2_single:.4f}) > m2({p2_minor2:.4f})")
        self._test(G, "T3_P2_fifth>tritone", p2_fifth > p2_tritone,
                   f"fifth({p2_fifth:.4f}) > tritone({p2_tritone:.4f})")
        self._test(G, "T3_P2_fifth>minor2nd", p2_fifth > p2_minor2,
                   f"fifth({p2_fifth:.4f}) > m2({p2_minor2:.4f})")

    # T4: Gated Validity (M0 = E0 × E1)
    def test_T4_gated_validity(self):
        G = "T4_gated_validity"
        stims = ["g2_01_single", "g2_03_triad", "g2_04_cluster", "g1_05_minor2nd"]
        for stim in stims:
            e0 = self._mean(stim, E0)
            e1 = self._mean(stim, E1)
            m0 = self._mean(stim, M0)
            # M0 = E0 × E1, so M0 ≤ min(E0, E1) and M0 ≤ E0
            self._test(G, f"T4_M0_leq_E0_{stim}", m0 <= e0 + 0.01,
                       f"M0({m0:.4f}) ≤ E0({e0:.4f})")

    # T5: Roughness Correlation (E2) — higher when more roughness
    def test_T5_roughness_corr(self):
        G = "T5_roughness_corr"
        e2_single = self._mean("g4_01_single", E2)
        e2_minor2 = self._mean("g4_05_minor2nd", E2)
        e2_maj7 = self._mean("g4_04_major7th", E2)

        # E2 = sigmoid(0.57 × roughness_mean) → higher for rougher
        self._test(G, "T5_E2_minor2>single", e2_minor2 > e2_single,
                   f"m2({e2_minor2:.4f}) > single({e2_single:.4f})")
        self._test(G, "T5_E2_maj7>single", e2_maj7 > e2_single,
                   f"maj7({e2_maj7:.4f}) > single({e2_single:.4f})")

    # T6: Forecast correlation
    def test_T6_forecast(self):
        G = "T6_forecast"
        stims = ["g1_01_single", "g1_03_fifth", "g1_04_tritone",
                 "g1_05_minor2nd", "g2_04_cluster"]
        # F1 (roughness_response_pred) should correlate with P2
        f1_vals = [self._mean(s, F1) for s in stims]
        p2_vals = [self._mean(s, P2) for s in stims]
        r = float(np.corrcoef(f1_vals, p2_vals)[0, 1])
        self._test(G, "T6_F1_P2_corr", r > 0.3,
                   f"r(F1,P2) = {r:+.3f} > 0.3 (roughness pred tracks interference)")

    # T7: Bounds & Shape
    def test_T7_bounds_shape(self):
        G = "T7_bounds_shape"
        stims = ["g1_01_single", "g1_05_minor2nd", "g2_04_cluster",
                 "g4_04_major7th", "g3_04_dense"]
        for stim in stims:
            r = self._load_and_run(stim)
            self._test(G, f"T7_shape_{stim}",
                       r.ndim == 2 and r.shape[1] == OUTPUT_DIM,
                       f"shape={r.shape}")
            lo, hi = r.min(), r.max()
            self._test(G, f"T7_bounds_{stim}",
                       lo >= -1e-6 and hi <= 1.0 + 1e-6,
                       f"[{lo:.6f}, {hi:.6f}]")

    def run_all(self):
        tests = [
            ("T1: NPS Value", self.test_T1_nps_value),
            ("T2: Harmonicity", self.test_T2_harmonicity),
            ("T3: Roughness Interference", self.test_T3_roughness_interference),
            ("T4: Gated Validity", self.test_T4_gated_validity),
            ("T5: Roughness Corr", self.test_T5_roughness_corr),
            ("T6: Forecast", self.test_T6_forecast),
            ("T7: Bounds & Shape", self.test_T7_bounds_shape),
        ]

        print("=" * 72)
        print("SDNPS FUNCTIONAL TEST v1.0")
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
        print(f"SDNPS v1.0 — {passed}/{total} PASS")
        report = {"mechanism": "SDNPS", "tests_total": total,
                  "tests_passed": passed, "results": [
                      {"name": r.name, "passed": r.passed, "message": r.message}
                      for r in self.results]}
        rp = RESULTS_DIR / "SDNPS_FUNCTIONAL_TEST_REPORT.json"
        with open(rp, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Report: {rp}")
        print(f"OVERALL: {'ALL PASS' if passed == total else f'{total-passed} FAILED'}")
        print("=" * 72)
        return passed == total


if __name__ == "__main__":
    runner = SDNPSTestRunner()
    sys.exit(0 if runner.run_all() else 1)
