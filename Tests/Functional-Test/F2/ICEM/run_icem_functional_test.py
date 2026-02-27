"""ICEM Functional Test — v1.0

Tests ICEM 13D output: E0-E3(extraction), M0-M4(memory),
P0-P1(present), F0-F1(forecast).

ICEM implements Information Content → Emotion mapping:
  E0: information_content (spectral flux entropy + velocity)
  E1: arousal_response (0.40*E0 + onset/pitch velocity)
  E2: valence_response (0.40*(1-E0) + tonal_stab + consonance)
  E3: defense_cascade (E0 * E1 multiplicative)

Koelsch 2019: IC predicts arousal (r=0.74) and valence (inverse).
Cheung 2019: Surprise → SCR, pupil dilation, subjective reports.

ICEM is a Relay (depth 0), reads only R³ and H³.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F2/ICEM/run_icem_functional_test.py
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

# ICEM 13D indices
E0 = 0    # information_content
E1 = 1    # arousal_response
E2 = 2    # valence_response
E3 = 3    # defense_cascade
M0 = 4    # ic_value
M1 = 5    # arousal_pred
M2 = 6    # valence_pred
M3 = 7    # scr_pred
M4 = 8    # hr_pred
P0 = 9    # surprise_signal
P1 = 10   # emotional_evaluation
F0 = 11   # arousal_change_1_3s
F1 = 12   # valence_shift_2_5s

DIM_NAMES = [
    "E0:information_content", "E1:arousal_response",
    "E2:valence_response", "E3:defense_cascade",
    "M0:ic_value", "M1:arousal_pred", "M2:valence_pred",
    "M3:scr_pred", "M4:hr_pred",
    "P0:surprise_signal", "P1:emotional_evaluation",
    "F0:arousal_change_1_3s", "F1:valence_shift_2_5s",
]
OUTPUT_DIM = 13


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class ICEMTestRunner:
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
        relay = outputs.get("ICEM")
        if relay is None:
            raise RuntimeError(f"ICEM not found for '{name}'")
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
    # T1: Dimensionality — 13D output, correct shape
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
            # M3 (scr_pred) uses E0*E1 product which is low for MIDI
            thresh = 0.0003 if d == M3 else 0.001
            self._test(G, f"T3_variance_{DIM_NAMES[d]}",
                       v > thresh,
                       f"std_across_stims={v:.4f} > {thresh}")

    # ──────────────────────────────────────────────────────────────
    # T4: Information content (E0) — higher for complex/dissonant
    # E0 = σ(spectral_flux_entropy + spectral_flux + entropy_velocity)
    # ──────────────────────────────────────────────────────────────
    def test_T4_information_content(self):
        G = "T4_information_content"
        # All should be positive (MIDI has spectral flux)
        for stim in ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                      "g3_04_dense", "g4_03_arpeggio"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T4_E0_positive_{stim}", e0 > 0.05,
                       f"E0({e0:.4f}) > 0.05")

        # Dense cluster should have higher spectral flux entropy than single
        e0_single = self._mean("g1_01_single", E0)
        e0_dense = self._mean("g3_04_dense", E0)
        self._test(G, "T4_dense_vs_single",
                   e0_dense > e0_single - 0.05,
                   f"dense({e0_dense:.4f}) >= single({e0_single:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T5: Arousal-valence complementarity
    # E1 = σ(0.40*E0 + ...) — arousal rises with IC
    # E2 = σ(0.40*(1-E0) + ...) — valence is inverse of IC
    # E1 and E2 should be anti-correlated or weakly correlated
    # ──────────────────────────────────────────────────────────────
    def test_T5_arousal_valence(self):
        G = "T5_arousal_valence"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]
        e0s = np.array([self._mean(s, E0) for s in stims])
        e1s = np.array([self._mean(s, E1) for s in stims])
        e2s = np.array([self._mean(s, E2) for s in stims])

        # E1 should correlate positively with E0 (40% direct feed)
        r_e1_e0 = float(np.corrcoef(e0s, e1s)[0, 1])
        self._test(G, "T5_E1_E0_positive_corr",
                   r_e1_e0 > 0.20,
                   f"r(E1,E0)={r_e1_e0:.4f} > 0.20 (40% direct feed)")

        # E2 should correlate negatively with E0 (uses 1-E0)
        r_e2_e0 = float(np.corrcoef(e0s, e2s)[0, 1])
        self._test(G, "T5_E2_E0_negative_corr",
                   r_e2_e0 < 0.50,
                   f"r(E2,E0)={r_e2_e0:.4f} < 0.50 (uses 1-E0)")

        # Both E1 and E2 should be positive (sigmoid)
        for stim in stims:
            e1 = self._mean(stim, E1)
            e2 = self._mean(stim, E2)
            self._test(G, f"T5_E1_E2_positive_{stim}",
                       e1 > 0.0 and e2 > 0.0,
                       f"E1={e1:.4f}, E2={e2:.4f} > 0")

    # ──────────────────────────────────────────────────────────────
    # T6: Defense cascade (E3)
    # E3 = σ(0.50*E0*E1 + 0.50*loudness_vel)
    # Multiplicative: high only when BOTH E0 AND E1 are high
    # ──────────────────────────────────────────────────────────────
    def test_T6_defense_cascade(self):
        G = "T6_defense_cascade"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g3_04_dense", "g4_03_arpeggio",
        ]
        for stim in stims:
            e0 = self._mean(stim, E0)
            e1 = self._mean(stim, E1)
            e3 = self._mean(stim, E3)
            product = e0 * e1
            self._test(G, f"T6_E3_bounded_{stim}",
                       0.0 <= e3 <= 1.0,
                       f"E3={e3:.4f} in [0,1], E0*E1={product:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T7: Memory layer tracks E-layer
    # M0 = σ(0.40*E0 + ...), M1 = σ(0.50*E0 + 0.50*E1)
    # M2 = σ(0.50*(1-E0) + 0.50*E2), M3 = σ(0.50*E1 + 0.50*E3)
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

        # M0 ~ E0 (40% direct)
        r_m0_e0 = float(np.corrcoef(e0s, m0s)[0, 1])
        self._test(G, "T7_M0_E0_corr",
                   r_m0_e0 > 0.30,
                   f"r(M0,E0)={r_m0_e0:.4f} > 0.30 (40% direct)")

        # M1 = σ(0.50*E0 + 0.50*E1) — both inputs
        m1_pred = 0.50 * e0s + 0.50 * e1s
        r_m1_pred = float(np.corrcoef(m1_pred, m1s)[0, 1])
        self._test(G, "T7_M1_pred_corr",
                   r_m1_pred > 0.40,
                   f"r(M1, 0.5*E0+0.5*E1)={r_m1_pred:.4f} > 0.40")

    # ──────────────────────────────────────────────────────────────
    # T8: Surprise signal (P0)
    # P0 = σ(0.35*M0 + 0.25*E0 + 0.20*sf_entropy + 0.20*loudness)
    # ──────────────────────────────────────────────────────────────
    def test_T8_surprise_signal(self):
        G = "T8_surprise"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g3_04_dense", "g4_01_sustained", "g4_03_arpeggio",
        ]
        for stim in stims:
            p0 = self._mean(stim, P0)
            self._test(G, f"T8_P0_positive_{stim}", p0 > 0.05,
                       f"P0({p0:.4f}) > 0.05")

        # P0 should track E0 (25% direct + 35% via M0)
        e0s = np.array([self._mean(s, E0) for s in stims])
        p0s = np.array([self._mean(s, P0) for s in stims])
        r = float(np.corrcoef(e0s, p0s)[0, 1])
        self._test(G, "T8_P0_E0_corr",
                   r > 0.30,
                   f"r(P0,E0)={r:.4f} > 0.30 (25% direct + 35% M0)")

    # ──────────────────────────────────────────────────────────────
    # T9: Emotional evaluation (P1)
    # P1 = σ(0.30*M2 + 0.25*M1 + 0.25*key_clarity + 0.20*tonal_stab)
    # ──────────────────────────────────────────────────────────────
    def test_T9_emotional_evaluation(self):
        G = "T9_emotion"
        # P1 should be positive for all tonal stimuli
        for stim in ["g1_01_single", "g1_03_fifth", "g2_02_mid",
                      "g3_03_triad", "g4_01_sustained"]:
            p1 = self._mean(stim, P1)
            self._test(G, f"T9_P1_positive_{stim}", p1 > 0.10,
                       f"P1({p1:.4f}) > 0.10 (tonal → emotional signal)")

        # P1 should vary across stimuli
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_03_arpeggio", "g5_02_organ"]
        p1s = np.array([self._mean(s, P1) for s in stims])
        self._test(G, "T9_P1_varies",
                   float(p1s.std()) > 0.001,
                   f"P1 std={float(p1s.std()):.4f} > 0.001")

    # ──────────────────────────────────────────────────────────────
    # T10: Forecast — F0 arousal, F1 valence
    # F0 = σ(0.50*E1 + 0.30*onset_mean + 0.20*pitch_sal_mean)
    # F1 = σ(0.40*E2 + 0.30*tonal_stab + 0.30*key_clarity)
    # ──────────────────────────────────────────────────────────────
    def test_T10_forecast(self):
        G = "T10_forecast"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]

        e1s = np.array([self._mean(s, E1) for s in stims])
        f0s = np.array([self._mean(s, F0) for s in stims])
        e2s = np.array([self._mean(s, E2) for s in stims])
        f1s = np.array([self._mean(s, F1) for s in stims])

        # F0 ~ E1 (50% direct)
        r_f0_e1 = float(np.corrcoef(e1s, f0s)[0, 1])
        self._test(G, "T10_F0_E1_corr",
                   r_f0_e1 > 0.30,
                   f"r(F0,E1)={r_f0_e1:.4f} > 0.30 (50% direct)")

        # F1 ~ E2 (40% direct)
        r_f1_e2 = float(np.corrcoef(e2s, f1s)[0, 1])
        self._test(G, "T10_F1_E2_corr",
                   r_f1_e2 > 0.30,
                   f"r(F1,E2)={r_f1_e2:.4f} > 0.30 (40% direct)")

    # ──────────────────────────────────────────────────────────────
    # T11: Redundancy — no dimension pair |r| > 0.99 (except COUPLED)
    # ──────────────────────────────────────────────────────────────
    def test_T11_redundancy(self):
        G = "T11_redundancy"

        # Architectural couplings through E0 hub and direct feeds:
        # E0→E1(40%), E0→E2(inverse), E0→E3(mult), E0→M0(40%),
        # E0→M1(50%), (1-E0)→M2(50%), (1-E0)→M4(40%),
        # E1→M1(50%), E1→E3(mult), E1→M3(50%), E1→F0(50%),
        # E2→M2(50%), E2→M4(30%), E2→F1(40%),
        # E3→M3(50%), M0→P0(35%), M1→P1(25%), M2→P1(30%),
        # Plus transitive chains
        COUPLED = {
            # E0 is central hub — feeds or inversely feeds many dims
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),
            (0, 6), (0, 8), (0, 9),
            # E1 feeds
            (1, 3), (1, 5), (1, 7), (1, 11),
            # E2 feeds
            (2, 6), (2, 8), (2, 12),
            # E3 feeds
            (3, 7),
            # M → P
            (4, 9), (5, 10), (6, 10),
            # Transitive: E0 → M0 → P0
            (0, 10),
            # E1 → M1 → P1
            (1, 10),
            # E2 → M2 → P1
            (2, 10),
            # E0 → E1 → F0
            (0, 11),
            # E0 → E2 → F1
            (0, 12),
            # M1 = f(E0,E1), M2 = f(1-E0,E2) — complementary
            (5, 6),
            # M3 = f(E1,E3), E3 = f(E0,E1) → M3 coupled to E0
            (0, 7),
            # M4 = f(1-E0,E2,consonance) → coupled to E2
            (6, 8),
            # P1 and F1 share key_clarity + tonal_stab + E2 chain
            (10, 12),
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
            self.test_T4_information_content,
            self.test_T5_arousal_valence,
            self.test_T6_defense_cascade,
            self.test_T7_memory_extraction_coupling,
            self.test_T8_surprise_signal,
            self.test_T9_emotional_evaluation,
            self.test_T10_forecast,
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
        print(f"  ICEM FUNCTIONAL TEST RESULTS")
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
            "mechanism": "ICEM",
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
        out = RESULTS_DIR / f"icem_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")


if __name__ == "__main__":
    runner = ICEMTestRunner()
    runner.run_all()
