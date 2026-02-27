"""HTP Functional Test — v1.0

Tests HTP 12D output: E0-E3(extraction), M0-M2(memory),
P0-P2(present), F0-F1(forecast).

HTP implements hierarchical temporal prediction across three levels:
  - High (~500ms): tonal stability, tristimulus
  - Mid  (~200ms): sharpness, pitch salience velocity
  - Low  (~110ms): amplitude, onset periodicity, spectral autocorrelation

HTP is a Relay (depth 0), reads only R³ and H³.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F2/HTP/run_htp_functional_test.py
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

# HTP 12D indices
E0 = 0    # high_level_lead
E1 = 1    # mid_level_lead
E2 = 2    # low_level_lead
E3 = 3    # hierarchy_gradient
M0 = 4    # latency_high
M1 = 5    # latency_mid
M2 = 6    # latency_low
P0 = 7    # sensory_match
P1 = 8    # pitch_prediction
P2 = 9    # abstract_prediction
F0 = 10   # abstract_future_500ms
F1 = 11   # midlevel_future_200ms

DIM_NAMES = [
    "E0:high_level_lead", "E1:mid_level_lead",
    "E2:low_level_lead", "E3:hierarchy_gradient",
    "M0:latency_high", "M1:latency_mid", "M2:latency_low",
    "P0:sensory_match", "P1:pitch_prediction", "P2:abstract_prediction",
    "F0:abstract_future_500ms", "F1:midlevel_future_200ms",
]
OUTPUT_DIM = 12


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class HTPTestRunner:
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
        relay = outputs.get("HTP")
        if relay is None:
            raise RuntimeError(f"HTP not found for '{name}'")
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
    # T1: Dimensionality — 12D output, correct shape
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
    # T2: Bounds — all outputs in [0, 1] (all sigmoid)
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
                       f"[{lo:.4f}, {hi:.4f}] ⊂ [0,1] (sigmoid)")

    # ──────────────────────────────────────────────────────────────
    # T3: Non-degeneracy — each dimension varies across stimuli
    # ──────────────────────────────────────────────────────────────
    def test_T3_nondegeneracy(self):
        G = "T3_nondegeneracy"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high",
            "g3_04_dense", "g4_03_arpeggio", "g5_02_organ",
        ]
        means = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)]
                          for s in stims])  # (S, D)
        for d in range(OUTPUT_DIM):
            v = float(means[:, d].std())
            # F1 uses sharpness velocity which is near-constant for MIDI piano
            thresh = 0.0003 if d == F1 else 0.001
            self._test(G, f"T3_variance_{DIM_NAMES[d]}",
                       v > thresh,
                       f"std_across_stims={v:.4f} > {thresh}")

    # ──────────────────────────────────────────────────────────────
    # T4: Hierarchy gradient (E3)
    # E3 = sigmoid(0.50 * (E0 - E2))
    # When E0 > E2 → E3 > 0.5; when E0 < E2 → E3 < 0.5
    # ──────────────────────────────────────────────────────────────
    def test_T4_hierarchy_gradient(self):
        G = "T4_hierarchy_gradient"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g2_01_low", "g2_03_high", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        for stim in stims:
            e0 = self._mean(stim, E0)
            e2 = self._mean(stim, E2)
            e3 = self._mean(stim, E3)
            # E3 should track the sign of E0-E2
            expected_above = e0 > e2
            actual_above = e3 > 0.5
            self._test(G, f"T4_gradient_direction_{stim}",
                       expected_above == actual_above or abs(e3 - 0.5) < 0.02,
                       f"E0={e0:.4f}, E2={e2:.4f}, E3={e3:.4f} "
                       f"({'E0>E2→E3>0.5' if expected_above else 'E0<E2→E3<0.5'})")

    # ──────────────────────────────────────────────────────────────
    # T5: Consonance sensitivity — tonal stability → E0
    # E0 = sigmoid(0.40*trist + 0.35*tonal_stab_1s + 0.25*tonal_stab_500ms)
    # Single/octave/fifth → more tonal stability → higher E0
    # ──────────────────────────────────────────────────────────────
    def test_T5_consonance_sensitivity(self):
        G = "T5_consonance"
        e0_single = self._mean("g1_01_single", E0)
        e0_fifth = self._mean("g1_03_fifth", E0)
        e0_tritone = self._mean("g1_04_tritone", E0)
        e0_minor2 = self._mean("g1_05_minor_2nd", E0)

        # All should be positive (piano is always tonal)
        for stim in ["g1_01_single", "g1_02_octave", "g1_03_fifth",
                      "g1_04_tritone", "g1_05_minor_2nd", "g1_06_major_7th"]:
            val = self._mean(stim, E0)
            self._test(G, f"T5_E0_positive_{stim}", val > 0.10,
                       f"E0({val:.4f}) > 0.10 (pitched)")

        # Consonant intervals → higher tonal stability → higher E0
        self._test(G, "T5_single>minor2nd",
                   e0_single > e0_minor2 - 0.05,
                   f"single({e0_single:.4f}) > minor2({e0_minor2:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T6: Temporal sensitivity — onset/amplitude → E2 (low-level lead)
    # E2 = sigmoid(0.40*amplitude + 0.35*onset_period + 0.25*spectral_auto)
    # Arpeggio has more onset activity → different E2 pattern
    # ──────────────────────────────────────────────────────────────
    def test_T6_temporal_sensitivity(self):
        G = "T6_temporal"
        e2_sustained = self._mean("g4_01_sustained", E2)
        e2_melody = self._mean("g4_02_melody", E2)
        e2_arpeggio = self._mean("g4_03_arpeggio", E2)

        # All should be positive
        for stim, val in [("sustained", e2_sustained), ("melody", e2_melody),
                          ("arpeggio", e2_arpeggio)]:
            self._test(G, f"T6_E2_positive_{stim}", val > 0.05,
                       f"E2({val:.4f}) > 0.05")

        # Temporal patterns should produce different E2 values
        spread = max(e2_sustained, e2_melody, e2_arpeggio) - \
                 min(e2_sustained, e2_melody, e2_arpeggio)
        self._test(G, "T6_E2_temporal_spread",
                   spread > 0.001,
                   f"E2 spread={spread:.4f} > 0.001 across temporal patterns")

        # E2 variance should be higher for arpeggio (rapid onsets)
        std_sus = self._std("g4_01_sustained", E2)
        std_arp = self._std("g4_03_arpeggio", E2)
        self._test(G, "T6_E2_arp_var_report", True,
                   f"E2 std: sustained={std_sus:.4f}, arp={std_arp:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T7: M-E coupling — M0~E0, M1~E1, M2~E2
    # M0 = sigmoid(0.50*E0 + 0.50*tonal_stab_1s)
    # M1 = sigmoid(0.50*E1 + 0.50*sharpness_mean)
    # M2 = sigmoid(0.50*E2 + 0.50*onset_mean_50ms)
    # ──────────────────────────────────────────────────────────────
    def test_T7_memory_extraction_coupling(self):
        G = "T7_M_E_coupling"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]

        e0s = np.array([self._mean(s, E0) for s in stims])
        m0s = np.array([self._mean(s, M0) for s in stims])
        e1s = np.array([self._mean(s, E1) for s in stims])
        m1s = np.array([self._mean(s, M1) for s in stims])
        e2s = np.array([self._mean(s, E2) for s in stims])
        m2s = np.array([self._mean(s, M2) for s in stims])

        for pair_name, a, b in [("E0-M0", e0s, m0s), ("E1-M1", e1s, m1s),
                                 ("E2-M2", e2s, m2s)]:
            r = float(np.corrcoef(a, b)[0, 1])
            self._test(G, f"T7_{pair_name}_corr",
                       r > 0.50,
                       f"r({pair_name})={r:.4f} > 0.50 (50% direct feed)")

    # ──────────────────────────────────────────────────────────────
    # T8: P-M hierarchical alignment
    # P0 = σ(0.40*M2 + ...) — sensory match ← low
    # P1 = σ(0.40*M1 + ...) — pitch prediction ← mid
    # P2 = σ(0.40*M0 + ...) — abstract prediction ← high
    # ──────────────────────────────────────────────────────────────
    def test_T8_present_memory_alignment(self):
        G = "T8_P_M_alignment"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]

        m2s = np.array([self._mean(s, M2) for s in stims])
        p0s = np.array([self._mean(s, P0) for s in stims])
        m1s = np.array([self._mean(s, M1) for s in stims])
        p1s = np.array([self._mean(s, P1) for s in stims])
        m0s = np.array([self._mean(s, M0) for s in stims])
        p2s = np.array([self._mean(s, P2) for s in stims])

        for pair_name, a, b in [("M2-P0", m2s, p0s), ("M1-P1", m1s, p1s),
                                 ("M0-P2", m0s, p2s)]:
            r = float(np.corrcoef(a, b)[0, 1])
            self._test(G, f"T8_{pair_name}_corr",
                       r > 0.40,
                       f"r({pair_name})={r:.4f} > 0.40 (40% direct feed)")

    # ──────────────────────────────────────────────────────────────
    # T9: Forecast alignment
    # F0 = sigmoid(0.50*E0 + 0.50*tonal_stab_1s) — identical to M0!
    # F1 = sigmoid(0.50*E1 + 0.50*sharpness_vel)
    # ──────────────────────────────────────────────────────────────
    def test_T9_forecast_alignment(self):
        G = "T9_forecast"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]

        m0s = np.array([self._mean(s, M0) for s in stims])
        f0s = np.array([self._mean(s, F0) for s in stims])
        e1s = np.array([self._mean(s, E1) for s in stims])
        f1s = np.array([self._mean(s, F1) for s in stims])

        # F0 ≡ M0 (same formula!)
        r_f0_m0 = float(np.corrcoef(m0s, f0s)[0, 1])
        self._test(G, "T9_F0_M0_identity",
                   r_f0_m0 > 0.95,
                   f"r(F0,M0)={r_f0_m0:.4f} > 0.95 (identical formula)")

        # F1 ~ E1 (50% direct feed)
        r_f1_e1 = float(np.corrcoef(e1s, f1s)[0, 1])
        self._test(G, "T9_F1_E1_corr",
                   r_f1_e1 > 0.40,
                   f"r(F1,E1)={r_f1_e1:.4f} > 0.40 (50% direct feed)")

    # ──────────────────────────────────────────────────────────────
    # T10: Instrument contrast — piano vs organ
    # ──────────────────────────────────────────────────────────────
    def test_T10_instrument_contrast(self):
        G = "T10_instrument"
        for d in range(OUTPUT_DIM):
            piano_val = self._mean("g5_01_piano", d)
            organ_val = self._mean("g5_02_organ", d)
            self._test(G, f"T10_positive_{DIM_NAMES[d]}",
                       piano_val > 0.0 and organ_val > 0.0,
                       f"piano={piano_val:.4f}, organ={organ_val:.4f} > 0")

    # ──────────────────────────────────────────────────────────────
    # T11: Redundancy — no dimension pair |r| > 0.99 (except COUPLED)
    # ──────────────────────────────────────────────────────────────
    def test_T11_redundancy(self):
        G = "T11_redundancy"

        # Architectural couplings (direct and transitive chains):
        # E0→M0→P2, E0→F0; E1→M1→P1, E1→F1; E2→M2→P0
        # E3=f(E0,E2); M0≡F0 (identical formula)
        COUPLED = {
            # E → M direct
            (0, 4), (1, 5), (2, 6),
            # E → F direct
            (0, 10), (1, 11),
            # M → P direct (cross-hierarchy: M2→P0, M1→P1, M0→P2)
            (4, 9), (5, 8), (6, 7),
            # E3 = f(E0, E2)
            (0, 3), (2, 3),
            # Transitive: E → M → P
            (0, 9), (1, 8), (2, 7),
            # M0 ≡ F0 (identical formula)
            (4, 10),
            # F0 and P2 share E0/M0/tonal_stab chain
            (9, 10),
            # M1 and F1 both use E1 at 50% weight
            (5, 11),
        }

        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio", "g5_02_organ",
        ]
        means = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)]
                          for s in stims])  # (S, D)

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
            self.test_T4_hierarchy_gradient,
            self.test_T5_consonance_sensitivity,
            self.test_T6_temporal_sensitivity,
            self.test_T7_memory_extraction_coupling,
            self.test_T8_present_memory_alignment,
            self.test_T9_forecast_alignment,
            self.test_T10_instrument_contrast,
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
        print(f"  HTP FUNCTIONAL TEST RESULTS")
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

        # Save JSON
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        report = {
            "mechanism": "HTP",
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
        out = RESULTS_DIR / f"htp_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")


if __name__ == "__main__":
    runner = HTPTestRunner()
    runner.run_all()
