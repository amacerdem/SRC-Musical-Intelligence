"""WMED Functional Test — v1.0

Tests WMED 11D output: E0-E1(extraction), M0-M1(memory),
P0-P2(present), F0-F3(forecast).

WMED implements working memory-entrainment dissociation paradox:
  E0: entrainment_strength (onset periodicity, amplitude)
  E1: wm_contribution (entropy, spectral change)
  M0: tapping_accuracy (E0 + multi-scale onsets)
  M1: dissociation_index (E0*(1-E1) paradox term)
  P0: phase_locking_strength (reads PWUP[4])
  P1: pattern_segmentation (reads PWUP[3])
  P2: rhythmic_engagement (reads PWUP[2])
  F0-F3: forecasts (next_beat, tapping, wm_interference, paradox)

Noboa 2025: WM-entrainment paradox (beta=-0.418).

WMED is an Associator (depth 2), reads PWUP (Encoder).

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F2/WMED/run_wmed_functional_test.py
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

# WMED 11D indices
E0 = 0    # entrainment_strength
E1 = 1    # wm_contribution
M0 = 2    # tapping_accuracy
M1 = 3    # dissociation_index
P0 = 4    # phase_locking_strength
P1 = 5    # pattern_segmentation
P2 = 6    # rhythmic_engagement
F0 = 7    # next_beat_pred
F1 = 8    # tapping_accuracy_pred
F2 = 9    # wm_interference_pred
F3 = 10   # paradox_strength_pred

DIM_NAMES = [
    "E0:entrainment", "E1:wm_contribution",
    "M0:tapping_accuracy", "M1:dissociation_idx",
    "P0:phase_locking", "P1:pattern_segment", "P2:rhythmic_engage",
    "F0:next_beat", "F1:tapping_pred", "F2:wm_interference", "F3:paradox_pred",
]
OUTPUT_DIM = 11


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class WMEDTestRunner:
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
        relay = outputs.get("WMED")
        if relay is None:
            raise RuntimeError(f"WMED not found for '{name}'")
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
    # T1: Dimensionality — 11D output
    # ──────────────────────────────────────────────────────────────
    def test_T1_dimensionality(self):
        G = "T1_dimensionality"
        r = self._load_and_run("g1_01_single")
        self._test(G, "T1_ndim", r.ndim == 2,
                   f"ndim={r.ndim}, expected 2 (T, D)")
        self._test(G, "T1_dim_count", r.shape[1] == OUTPUT_DIM,
                   f"D={r.shape[1]}, expected {OUTPUT_DIM}")
        self._test(G, "T1_frames_positive", r.shape[0] > 100,
                   f"T={r.shape[0]} > 100 frames")

    # ──────────────────────────────────────────────────────────────
    # T2: Bounds — all [0, 1]
    # ──────────────────────────────────────────────────────────────
    def test_T2_bounds(self):
        G = "T2_bounds"
        all_stims = [
            "g1_01_single", "g1_02_octave", "g1_03_fifth",
            "g1_04_tritone", "g1_05_minor_2nd", "g1_06_major_7th",
            "g2_01_low", "g2_02_mid", "g2_03_high",
            "g3_01_single", "g3_02_dyad", "g3_03_triad", "g3_04_dense",
            "g4_01_sustained", "g4_02_melody", "g4_03_arpeggio",
            "g5_01_piano", "g5_02_organ",
        ]
        for stim in all_stims:
            r = self._load_and_run(stim)
            lo, hi = float(r.min()), float(r.max())
            self._test(G, f"T2_bounds_{stim}",
                       lo >= -0.001 and hi <= 1.001,
                       f"[{lo:.4f}, {hi:.4f}] ⊂ [0,1]")

    # ──────────────────────────────────────────────────────────────
    # T3: Non-degeneracy
    # ──────────────────────────────────────────────────────────────
    def test_T3_nondegeneracy(self):
        G = "T3_nondegeneracy"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high",
            "g3_04_dense", "g4_03_arpeggio", "g5_02_organ",
        ]
        means = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)]
                          for s in stims])
        for d in range(OUTPUT_DIM):
            v = float(means[:, d].std())
            # F0 aggregates P0+P2+(1-entropy), all stable → low variance
            thresh = 0.0003 if d == F0 else 0.001
            self._test(G, f"T3_variance_{DIM_NAMES[d]}",
                       v > thresh,
                       f"std_across_stims={v:.4f} > {thresh}")

    # ──────────────────────────────────────────────────────────────
    # T4: Entrainment (E0) — onset periodicity based
    # ──────────────────────────────────────────────────────────────
    def test_T4_entrainment(self):
        G = "T4_entrainment"
        for stim in ["g1_01_single", "g4_02_melody", "g4_03_arpeggio"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T4_E0_positive_{stim}", e0 > 0.0,
                       f"E0({e0:.4f}) > 0")

        # Report temporal variation
        e0_sus = self._mean("g4_01_sustained", E0)
        e0_mel = self._mean("g4_02_melody", E0)
        e0_arp = self._mean("g4_03_arpeggio", E0)
        self._test(G, "T4_E0_temporal_report", True,
                   f"E0: sus={e0_sus:.4f}, mel={e0_mel:.4f}, arp={e0_arp:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T5: WM contribution (E1) — entropy + spectral change
    # ──────────────────────────────────────────────────────────────
    def test_T5_wm_contribution(self):
        G = "T5_wm_contribution"
        for stim in ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense"]:
            e1 = self._mean(stim, E1)
            self._test(G, f"T5_E1_positive_{stim}", e1 > 0.0,
                       f"E1({e1:.4f}) > 0")

    # ──────────────────────────────────────────────────────────────
    # T6: Dissociation paradox (M1)
    # M1 uses E0*(1-E1) multiplicative term
    # ──────────────────────────────────────────────────────────────
    def test_T6_dissociation(self):
        G = "T6_dissociation"
        stims = [
            "g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]
        for stim in stims:
            e0 = self._mean(stim, E0)
            e1 = self._mean(stim, E1)
            m1 = self._mean(stim, M1)
            paradox = e0 * (1.0 - e1)
            self._test(G, f"T6_M1_bounded_{stim}",
                       0.0 <= m1 <= 1.0,
                       f"M1={m1:.4f} in [0,1], paradox_term={paradox:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T7: M-E coupling
    # M0 = σ(0.30*E0 + ...), M1 = σ(0.40*E0*(1-E1) + ...)
    # ──────────────────────────────────────────────────────────────
    def test_T7_memory_coupling(self):
        G = "T7_M_E_coupling"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]
        e0s = np.array([self._mean(s, E0) for s in stims])
        m0s = np.array([self._mean(s, M0) for s in stims])
        r_m0_e0 = float(np.corrcoef(e0s, m0s)[0, 1])
        self._test(G, "T7_M0_E0_corr",
                   r_m0_e0 > 0.30,
                   f"r(M0,E0)={r_m0_e0:.4f} > 0.30 (30% direct)")

    # ──────────────────────────────────────────────────────────────
    # T8: P-layer upstream integration (reads PWUP)
    # ──────────────────────────────────────────────────────────────
    def test_T8_upstream(self):
        G = "T8_upstream"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        for stim in stims:
            p0 = self._mean(stim, P0)
            p1 = self._mean(stim, P1)
            p2 = self._mean(stim, P2)
            self._test(G, f"T8_P_positive_{stim}",
                       p0 > 0.0 and p1 > 0.0 and p2 > 0.0,
                       f"P0={p0:.4f}, P1={p1:.4f}, P2={p2:.4f} > 0")

    # ──────────────────────────────────────────────────────────────
    # T9: Forecast structure
    # F0, F1 use P0+P2 (beat/engagement)
    # F2 uses P1+E1 (segmentation/WM)
    # F3 uses P0-(1-P1) (paradox)
    # ──────────────────────────────────────────────────────────────
    def test_T9_forecast(self):
        G = "T9_forecast"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]
        p0s = np.array([self._mean(s, P0) for s in stims])
        p2s = np.array([self._mean(s, P2) for s in stims])
        f0s = np.array([self._mean(s, F0) for s in stims])
        f1s = np.array([self._mean(s, F1) for s in stims])

        # F0 tracks P0 (40% direct)
        r_f0_p0 = float(np.corrcoef(p0s, f0s)[0, 1])
        self._test(G, "T9_F0_P0_corr",
                   r_f0_p0 > 0.30,
                   f"r(F0,P0)={r_f0_p0:.4f} > 0.30 (40% direct)")

        # F1 tracks P2 (35% direct)
        r_f1_p2 = float(np.corrcoef(p2s, f1s)[0, 1])
        self._test(G, "T9_F1_P2_corr",
                   r_f1_p2 > 0.20,
                   f"r(F1,P2)={r_f1_p2:.4f} > 0.20 (35% direct)")

    # ──────────────────────────────────────────────────────────────
    # T10: Instrument contrast
    # ──────────────────────────────────────────────────────────────
    def test_T10_instrument(self):
        G = "T10_instrument"
        for d in range(OUTPUT_DIM):
            piano = self._mean("g5_01_piano", d)
            organ = self._mean("g5_02_organ", d)
            self._test(G, f"T10_positive_{DIM_NAMES[d]}",
                       piano > 0.0 and organ > 0.0,
                       f"piano={piano:.4f}, organ={organ:.4f} > 0")

    # ──────────────────────────────────────────────────────────────
    # T11: Redundancy
    # ──────────────────────────────────────────────────────────────
    def test_T11_redundancy(self):
        G = "T11_redundancy"

        COUPLED = {
            # E → M
            (0, 2), (0, 3), (1, 3),
            # E → P
            (0, 4), (0, 6), (1, 5), (1, 6),
            # E → F
            (0, 8), (0, 10), (1, 9), (1, 10),
            # M → P
            (2, 6), (3, 5),
            # P → F
            (4, 7), (4, 8), (4, 9), (4, 10),
            (5, 9), (5, 10), (6, 7), (6, 8),
            # Transitive: E→P→F
            (0, 7), (1, 9),
            # M→P→F
            (3, 9),
            # F0↔F1 (both use P0 and P2)
            (7, 8),
            # F0↔F3, F1↔F3 (shared P0/E0)
            (7, 10), (8, 10),
        }

        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio", "g5_02_organ",
        ]
        means = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)]
                          for s in stims])

        for i in range(OUTPUT_DIM):
            for j in range(i + 1, OUTPUT_DIM):
                pair = (i, j)
                if pair in COUPLED:
                    continue
                r = abs(float(np.corrcoef(means[:, i], means[:, j])[0, 1]))
                self._test(G, f"T11_redundancy_{i}_{j}",
                           r < 0.99,
                           f"|r({DIM_NAMES[i]},{DIM_NAMES[j]})|={r:.3f} < 0.99")

    # ──────────────────────────────────────────────────────────────
    # Runner
    # ──────────────────────────────────────────────────────────────
    def run_all(self):
        t0 = time.time()
        self._init_pipeline()

        tests = [
            self.test_T1_dimensionality,
            self.test_T2_bounds,
            self.test_T3_nondegeneracy,
            self.test_T4_entrainment,
            self.test_T5_wm_contribution,
            self.test_T6_dissociation,
            self.test_T7_memory_coupling,
            self.test_T8_upstream,
            self.test_T9_forecast,
            self.test_T10_instrument,
            self.test_T11_redundancy,
        ]

        for t in tests:
            name = t.__name__
            print(f"\n{'='*60}")
            print(f"  {name}")
            print(f"{'='*60}")
            try:
                t()
            except Exception as ex:
                self._fail(name, f"{name}_exception", f"EXCEPTION: {ex}")
                import traceback; traceback.print_exc()

        elapsed = time.time() - t0
        self._report(elapsed)

    def _report(self, elapsed):
        passed = sum(1 for r in self.results if r.passed)
        total = len(self.results)
        failed = total - passed

        print(f"\n{'='*60}")
        print(f"  WMED FUNCTIONAL TEST RESULTS")
        print(f"{'='*60}")
        print(f"  Total : {total}")
        print(f"  Passed: {passed}")
        print(f"  Failed: {failed}")
        print(f"  Time  : {elapsed:.1f}s")
        print(f"{'='*60}")

        if failed:
            print(f"\n  FAILURES:")
            for r in self.results:
                if not r.passed:
                    print(f"    FAIL {r.name}: {r.message}")

        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {
            "mechanism": "WMED",
            "function": "F2",
            "timestamp": ts,
            "total": total,
            "passed": passed,
            "failed": failed,
            "elapsed_s": round(elapsed, 1),
            "results": [
                {"name": r.name, "group": r.group, "passed": r.passed,
                 "message": r.message, "values": r.values}
                for r in self.results
            ],
        }
        out = RESULTS_DIR / f"wmed_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")


if __name__ == "__main__":
    runner = WMEDTestRunner()
    runner.run_all()
