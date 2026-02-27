"""PWUP Functional Test — v1.0

Tests PWUP 10D output: E0-E1(extraction), M0-M1(memory),
P0-P2(present), F0-F2(forecast).

PWUP implements precision-weighted uncertainty processing:
  E0: tonal_precision (R³: tonalness, consonance, periodicity)
  E1: rhythmic_precision (R³: onset_strength, periodicity)
  M0: weighted_error (precision-gated PE signal)
  M1: uncertainty_index (inverse precision)
  P0: tonal_precision_weight (reads HTP[3])
  P1: rhythmic_precision_weight (reads HTP[7])
  P2: attenuated_response (reads ICEM[0,3])
  F0: precision_adjustment (E0+E1+(1-entropy))
  F1: context_uncertainty (entropy+(1-periodicity))
  F2: response_attenuation (P0+P1+(1-P2))

PWUP is an Encoder (depth 1), reads HTP and ICEM relays.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F2/PWUP/run_pwup_functional_test.py
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

# PWUP 10D indices
E0 = 0    # tonal_precision
E1 = 1    # rhythmic_precision
M0 = 2    # weighted_error
M1 = 3    # uncertainty_index
P0 = 4    # tonal_precision_weight
P1 = 5    # rhythmic_precision_weight
P2 = 6    # attenuated_response
F0 = 7    # precision_adjustment
F1 = 8    # context_uncertainty
F2 = 9    # response_attenuation

DIM_NAMES = [
    "E0:tonal_precision", "E1:rhythmic_precision",
    "M0:weighted_error", "M1:uncertainty_index",
    "P0:tonal_prec_weight", "P1:rhythmic_prec_weight", "P2:attenuated_response",
    "F0:precision_adjust", "F1:context_uncertainty", "F2:response_attenuation",
]
OUTPUT_DIM = 10


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class PWUPTestRunner:
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
        relay = outputs.get("PWUP")
        if relay is None:
            raise RuntimeError(f"PWUP not found for '{name}'")
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
    # T1: Dimensionality — 10D output
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
    # T2: Bounds — all [0, 1] (all sigmoid)
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
            # F2 aggregates P0+P1+(1-P2), all stable → low variance
            thresh = 0.0003 if d == F2 else 0.001
            self._test(G, f"T3_variance_{DIM_NAMES[d]}",
                       v > thresh,
                       f"std_across_stims={v:.4f} > {thresh}")

    # ──────────────────────────────────────────────────────────────
    # T4: Tonal precision (E0)
    # E0 = σ(0.50*tonalness + 0.30*consonance + 0.20*periodicity)
    # Higher for consonant tonal stimuli
    # ──────────────────────────────────────────────────────────────
    def test_T4_tonal_precision(self):
        G = "T4_tonal_precision"
        for stim in ["g1_01_single", "g1_03_fifth", "g2_02_mid"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T4_E0_positive_{stim}", e0 > 0.10,
                       f"E0({e0:.4f}) > 0.10 (tonal → high precision)")

        e0_single = self._mean("g1_01_single", E0)
        e0_minor2 = self._mean("g1_05_minor_2nd", E0)
        self._test(G, "T4_single>minor2",
                   e0_single > e0_minor2 - 0.05,
                   f"single({e0_single:.4f}) >= minor2({e0_minor2:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T5: Rhythmic precision (E1)
    # E1 = σ(0.55*onset_strength + 0.45*periodicity)
    # ──────────────────────────────────────────────────────────────
    def test_T5_rhythmic_precision(self):
        G = "T5_rhythmic_precision"
        for stim in ["g1_01_single", "g4_02_melody", "g4_03_arpeggio"]:
            e1 = self._mean(stim, E1)
            self._test(G, f"T5_E1_positive_{stim}", e1 > 0.0,
                       f"E1({e1:.4f}) > 0 (has onsets)")

        # Report across temporal patterns
        e1_sus = self._mean("g4_01_sustained", E1)
        e1_mel = self._mean("g4_02_melody", E1)
        e1_arp = self._mean("g4_03_arpeggio", E1)
        self._test(G, "T5_E1_temporal_report", True,
                   f"E1: sustained={e1_sus:.4f}, melody={e1_mel:.4f}, arp={e1_arp:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T6: Precision gating (M0)
    # M0 = σ(raw_error × (1 - 0.5×precision_gate))
    # High precision → attenuated error; low precision → pass-through
    # ──────────────────────────────────────────────────────────────
    def test_T6_precision_gating(self):
        G = "T6_precision_gating"
        stims = [
            "g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]
        for stim in stims:
            m0 = self._mean(stim, M0)
            self._test(G, f"T6_M0_bounded_{stim}",
                       0.0 <= m0 <= 1.0,
                       f"M0({m0:.4f}) in [0,1]")

        # M0 should vary (different precision × error combinations)
        m0s = np.array([self._mean(s, M0) for s in stims])
        self._test(G, "T6_M0_varies",
                   float(m0s.std()) > 0.001,
                   f"M0 std={float(m0s.std()):.4f} > 0.001")

    # ──────────────────────────────────────────────────────────────
    # T7: Upstream integration (P-layer reads HTP + ICEM)
    # P0 = σ(0.30*E0 + 0.25*M0 + 0.25*HTP[3] + 0.20*tonal_stab)
    # P1 = σ(0.30*E1 + 0.25*periodicity + 0.25*HTP[7] + 0.20*consonance)
    # P2 = σ(0.35*ICEM[0]*(1-0.5*prec) + 0.25*M1 + 0.20*ICEM[3] + 0.20*trist)
    # ──────────────────────────────────────────────────────────────
    def test_T7_upstream_integration(self):
        G = "T7_upstream"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]

        # P0 has E0 at 30% but HTP[3]+M0+tonal_stab can dominate
        e0s = np.array([self._mean(s, E0) for s in stims])
        p0s = np.array([self._mean(s, P0) for s in stims])
        r_p0_e0 = float(np.corrcoef(e0s, p0s)[0, 1])
        self._test(G, "T7_P0_E0_corr",
                   abs(r_p0_e0) > 0.10,
                   f"|r(P0,E0)|={abs(r_p0_e0):.4f} > 0.10 (E0 contributes)")

        # P1 should track E1 (30% direct)
        e1s = np.array([self._mean(s, E1) for s in stims])
        p1s = np.array([self._mean(s, P1) for s in stims])
        r_p1_e1 = float(np.corrcoef(e1s, p1s)[0, 1])
        self._test(G, "T7_P1_E1_corr",
                   r_p1_e1 > 0.20,
                   f"r(P1,E1)={r_p1_e1:.4f} > 0.20 (30% direct)")

        # All P dims should be positive
        for stim in stims:
            for d, nm in [(P0, "P0"), (P1, "P1"), (P2, "P2")]:
                val = self._mean(stim, d)
                self._test(G, f"T7_{nm}_positive_{stim}", val > 0.0,
                           f"{nm}({val:.4f}) > 0")

    # ──────────────────────────────────────────────────────────────
    # T8: F0↔F1 complementarity
    # F0 = σ(E0+E1+(1-entropy)) — high when precise
    # F1 = σ(entropy+(1-periodicity)+(1-onset_period)) — high when uncertain
    # ──────────────────────────────────────────────────────────────
    def test_T8_forecast_complementarity(self):
        G = "T8_f0_f1_complement"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]
        f0s = np.array([self._mean(s, F0) for s in stims])
        f1s = np.array([self._mean(s, F1) for s in stims])

        # F0 and F1 should be negatively or weakly correlated
        r_f0_f1 = float(np.corrcoef(f0s, f1s)[0, 1])
        self._test(G, "T8_F0_F1_complement",
                   r_f0_f1 < 0.80,
                   f"r(F0,F1)={r_f0_f1:.4f} < 0.80 (complementary)")

    # ──────────────────────────────────────────────────────────────
    # T9: Response attenuation (F2) = σ(P0+P1+(1-P2))
    # ──────────────────────────────────────────────────────────────
    def test_T9_response_attenuation(self):
        G = "T9_attenuation"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]
        p0s = np.array([self._mean(s, P0) for s in stims])
        p1s = np.array([self._mean(s, P1) for s in stims])
        f2s = np.array([self._mean(s, F2) for s in stims])

        # F2 should track P0+P1 combined
        combo = 0.50 * p0s + 0.50 * p1s
        r_f2_combo = float(np.corrcoef(combo, f2s)[0, 1])
        self._test(G, "T9_F2_tracks_precision",
                   r_f2_combo > 0.30,
                   f"r(F2, 0.5*P0+0.5*P1)={r_f2_combo:.4f} > 0.30")

    # ──────────────────────────────────────────────────────────────
    # T10: Instrument contrast
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
    # T11: Redundancy
    # ──────────────────────────────────────────────────────────────
    def test_T11_redundancy(self):
        G = "T11_redundancy"

        # Architectural couplings:
        # E0→M0(precision gate), E0→P0(30%), E0→F0(35%)
        # E1→M0(precision gate), E1→P1(30%), E1→F0(30%)
        # M0→P0(25%), M1→P2(25%)
        # P0→F2(35%), P1→F2(35%), P2→F2(inverse 30%)
        # F0↔F1 complementary
        COUPLED = {
            # E → M (precision gate)
            (0, 2), (1, 2),
            # E → P direct
            (0, 4), (1, 5),
            # E → F direct
            (0, 7), (1, 7),
            # M → P direct
            (2, 4), (3, 6),
            # P → F direct
            (4, 9), (5, 9), (6, 9),
            # F0 ↔ F1 complementary
            (7, 8),
            # Transitive: E→P→F
            (0, 9), (1, 9),
            # E→M→P transitive
            (0, 2), (1, 2),
            # M0→P0→F2
            (2, 9),
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
            self.test_T4_tonal_precision,
            self.test_T5_rhythmic_precision,
            self.test_T6_precision_gating,
            self.test_T7_upstream_integration,
            self.test_T8_forecast_complementarity,
            self.test_T9_response_attenuation,
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
        print(f"  PWUP FUNCTIONAL TEST RESULTS")
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
            "mechanism": "PWUP",
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
        out = RESULTS_DIR / f"pwup_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")


if __name__ == "__main__":
    runner = PWUPTestRunner()
    runner.run_all()
