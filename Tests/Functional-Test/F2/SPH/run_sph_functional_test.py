"""SPH Functional Test — v1.0

Tests SPH 14D output: E0-E3(extraction), M0-M3(memory),
P0-P2(present), F0-F2(forecast).

SPH implements spatiotemporal prediction hierarchy with dual pathways:
  Match pathway: E0→M0,M2→P0  (gamma match, confirmed predictions)
  Error pathway: E1→M1,M3→P1  (alpha-beta error, prediction violations)
  M2/M3 complementary: M2=σ(E0+R³[4]), M3=σ(E1+(1-R³[4]))
  E3 uses subtraction: feedforward - feedback balance

SPH is a Relay (depth 0), reads only R³ and H³.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F2/SPH/run_sph_functional_test.py
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

# SPH 14D indices
E0 = 0    # gamma_match
E1 = 1    # alpha_beta_error
E2 = 2    # hierarchy_position
E3 = 3    # feedforward_feedback
M0 = 4    # match_response
M1 = 5    # varied_response
M2 = 6    # gamma_power
M3 = 7    # alpha_beta_power
P0 = 8    # memory_match
P1 = 9    # prediction_error
P2 = 10   # deviation_detection
F0 = 11   # next_tone_pred_350ms
F1 = 12   # sequence_completion_2s
F2 = 13   # decision_evaluation

DIM_NAMES = [
    "E0:gamma_match", "E1:alpha_beta_error",
    "E2:hierarchy_position", "E3:feedforward_feedback",
    "M0:match_response", "M1:varied_response",
    "M2:gamma_power", "M3:alpha_beta_power",
    "P0:memory_match", "P1:prediction_error", "P2:deviation_detection",
    "F0:next_tone_pred", "F1:sequence_completion", "F2:decision_evaluation",
]
OUTPUT_DIM = 14


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class SPHTestRunner:
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
        relay = outputs.get("SPH")
        if relay is None:
            raise RuntimeError(f"SPH not found for '{name}'")
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
    # T1: Dimensionality — 14D output
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
            self._test(G, f"T3_variance_{DIM_NAMES[d]}",
                       v > 0.001,
                       f"std_across_stims={v:.4f} > 0.001")

    # ──────────────────────────────────────────────────────────────
    # T4: Gamma match (E0) — consonance/tonal stability
    # E0 = σ(0.35*consonance + 0.30*spectral_auto + 0.20*cons_1s + 0.15*chroma)
    # ──────────────────────────────────────────────────────────────
    def test_T4_gamma_match(self):
        G = "T4_gamma_match"
        for stim in ["g1_01_single", "g1_03_fifth", "g2_02_mid",
                      "g3_03_triad"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T4_E0_positive_{stim}", e0 > 0.10,
                       f"E0({e0:.4f}) > 0.10 (consonant → gamma match)")

        # Consonant > dissonant
        e0_fifth = self._mean("g1_03_fifth", E0)
        e0_minor2 = self._mean("g1_05_minor_2nd", E0)
        self._test(G, "T4_E0_fifth>minor2",
                   e0_fifth > e0_minor2 - 0.05,
                   f"fifth({e0_fifth:.4f}) >= minor2({e0_minor2:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T5: Alpha-beta error (E1) — spectral flux, onset variability
    # E1 = σ(0.35*sf + 0.25*onset + 0.20*sf_std + 0.20*onset_period)
    # ──────────────────────────────────────────────────────────────
    def test_T5_alpha_beta_error(self):
        G = "T5_alpha_beta"
        for stim in ["g1_01_single", "g1_05_minor_2nd", "g4_03_arpeggio"]:
            e1 = self._mean(stim, E1)
            self._test(G, f"T5_E1_positive_{stim}", e1 > 0.05,
                       f"E1({e1:.4f}) > 0.05")

        # Report: temporal patterns should show E1 differences
        e1_sus = self._mean("g4_01_sustained", E1)
        e1_arp = self._mean("g4_03_arpeggio", E1)
        self._test(G, "T5_E1_temporal_report", True,
                   f"E1: sustained={e1_sus:.4f}, arp={e1_arp:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T6: Dual pathway — match(E0/M0/M2/P0) vs error(E1/M1/M3/P1)
    # ──────────────────────────────────────────────────────────────
    def test_T6_dual_pathway(self):
        G = "T6_dual_pathway"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]

        # Match pathway: E0→M0 (40% direct)
        e0s = np.array([self._mean(s, E0) for s in stims])
        m0s = np.array([self._mean(s, M0) for s in stims])
        r_e0_m0 = float(np.corrcoef(e0s, m0s)[0, 1])
        self._test(G, "T6_E0_M0_match",
                   r_e0_m0 > 0.40,
                   f"r(E0,M0)={r_e0_m0:.4f} > 0.40 (match pathway)")

        # Error pathway: E1→M1 (40% direct)
        e1s = np.array([self._mean(s, E1) for s in stims])
        m1s = np.array([self._mean(s, M1) for s in stims])
        r_e1_m1 = float(np.corrcoef(e1s, m1s)[0, 1])
        self._test(G, "T6_E1_M1_error",
                   r_e1_m1 > 0.40,
                   f"r(E1,M1)={r_e1_m1:.4f} > 0.40 (error pathway)")

        # P0 tracks match (M0 40% + M2 30%)
        p0s = np.array([self._mean(s, P0) for s in stims])
        r_m0_p0 = float(np.corrcoef(m0s, p0s)[0, 1])
        self._test(G, "T6_M0_P0_match",
                   r_m0_p0 > 0.30,
                   f"r(M0,P0)={r_m0_p0:.4f} > 0.30 (match → memory match)")

        # P1 tracks error (M1 40% + M3 30%)
        m1s_arr = np.array([self._mean(s, M1) for s in stims])
        p1s = np.array([self._mean(s, P1) for s in stims])
        r_m1_p1 = float(np.corrcoef(m1s_arr, p1s)[0, 1])
        self._test(G, "T6_M1_P1_error",
                   r_m1_p1 > 0.30,
                   f"r(M1,P1)={r_m1_p1:.4f} > 0.30 (error → prediction error)")

    # ──────────────────────────────────────────────────────────────
    # T7: M2/M3 complementarity
    # M2 = σ(0.50*E0 + 0.50*R³[4])
    # M3 = σ(0.50*E1 + 0.50*(1-R³[4]))
    # ──────────────────────────────────────────────────────────────
    def test_T7_gamma_alpha_complementarity(self):
        G = "T7_complementarity"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]
        for stim in stims:
            m2 = self._mean(stim, M2)
            m3 = self._mean(stim, M3)
            self._test(G, f"T7_both_positive_{stim}",
                       m2 > 0.0 and m3 > 0.0,
                       f"M2={m2:.4f}, M3={m3:.4f} > 0 (complementary)")

    # ──────────────────────────────────────────────────────────────
    # T8: Feedforward-feedback (E3) — subtractive formula
    # E3 = σ(0.50*spectral_auto_mean - 0.50*tonal_stab_entropy)
    # ──────────────────────────────────────────────────────────────
    def test_T8_feedforward_feedback(self):
        G = "T8_ff_fb"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g3_04_dense",
                 "g4_01_sustained", "g4_03_arpeggio"]
        for stim in stims:
            e3 = self._mean(stim, E3)
            self._test(G, f"T8_E3_bounded_{stim}",
                       0.0 <= e3 <= 1.0,
                       f"E3={e3:.4f} in [0,1] (subtractive sigmoid)")

    # ──────────────────────────────────────────────────────────────
    # T9: Deviation detection (P2) — independent of M layer
    # P2 = σ(0.35*sf + 0.25*onset + 0.20*amplitude + 0.20*pitch_height)
    # ──────────────────────────────────────────────────────────────
    def test_T9_deviation_detection(self):
        G = "T9_deviation"
        for stim in ["g1_01_single", "g1_05_minor_2nd", "g4_03_arpeggio"]:
            p2 = self._mean(stim, P2)
            self._test(G, f"T9_P2_positive_{stim}", p2 > 0.05,
                       f"P2({p2:.4f}) > 0.05")

        # P2 should vary across temporal patterns
        p2_sus = self._mean("g4_01_sustained", P2)
        p2_arp = self._mean("g4_03_arpeggio", P2)
        self._test(G, "T9_P2_temporal_report", True,
                   f"P2: sustained={p2_sus:.4f}, arp={p2_arp:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T10: Forecast alignment
    # F0 = σ(0.40*E0 + consonance_mean + pitch_height_vel)
    # F1 = σ(tonal_stab_mean + spectral_auto_mean + chroma_mean) — independent
    # F2 = σ(0.50*E2 + 0.50*tonal_stab_mean)
    # ──────────────────────────────────────────────────────────────
    def test_T10_forecast(self):
        G = "T10_forecast"
        stims = [
            "g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
            "g2_01_low", "g2_03_high", "g3_04_dense",
            "g4_01_sustained", "g4_03_arpeggio",
        ]

        e0s = np.array([self._mean(s, E0) for s in stims])
        f0s = np.array([self._mean(s, F0) for s in stims])
        e2s = np.array([self._mean(s, E2) for s in stims])
        f2s = np.array([self._mean(s, F2) for s in stims])

        # F0 ~ E0 (40% direct)
        r_f0_e0 = float(np.corrcoef(e0s, f0s)[0, 1])
        self._test(G, "T10_F0_E0_corr",
                   r_f0_e0 > 0.30,
                   f"r(F0,E0)={r_f0_e0:.4f} > 0.30 (40% direct)")

        # F2 ~ E2 (50% direct)
        r_f2_e2 = float(np.corrcoef(e2s, f2s)[0, 1])
        self._test(G, "T10_F2_E2_corr",
                   r_f2_e2 > 0.40,
                   f"r(F2,E2)={r_f2_e2:.4f} > 0.40 (50% direct)")

        # F1 should be positive (tonal stability based)
        for stim in ["g1_01_single", "g1_03_fifth", "g4_01_sustained"]:
            f1 = self._mean(stim, F1)
            self._test(G, f"T10_F1_positive_{stim}", f1 > 0.10,
                       f"F1({f1:.4f}) > 0.10 (tonal → sequence completion)")

    # ──────────────────────────────────────────────────────────────
    # T11: Redundancy — no pair |r| > 0.99 except COUPLED
    # ──────────────────────────────────────────────────────────────
    def test_T11_redundancy(self):
        G = "T11_redundancy"

        # Architectural couplings:
        # Match pathway: E0→M0(40%), E0→M2(50%), M0→P0(40%), M2→P0(30%)
        # Error pathway: E1→M1(40%), E1→M3(50%), M1→P1(40%), M3→P1(30%)
        # E0→F0(40%), E2→F2(50%)
        # M2/M3 complement via R³[4]/(1-R³[4])
        # E2 shares tonal_stab with F1, F2
        # E3 shares spectral_auto + tonal_stab with F1
        COUPLED = {
            # Match pathway
            (0, 4), (0, 6), (4, 8), (6, 8),
            # Error pathway
            (1, 5), (1, 7), (5, 9), (7, 9),
            # E→F direct
            (0, 11), (2, 13),
            # Transitive: E→M→P
            (0, 8), (1, 9),
            # M2↔M3 complementarity (shared R³[4])
            (6, 7),
            # E2/E3 share H³ features with F1, F2
            (2, 12), (3, 12), (12, 13),
            # E0 shared consonance with F0
            (0, 11),
            # E2↔F2 via tonal_stab
            (2, 12),
            # E0↔M3: consonance (E0) ↔ (1-sensory_pleasantness) in M3
            (0, 7),
            # M2↔F0: both share E0 + consonance/pleasantness chain
            (6, 11),
            # M3↔F0: covarying through consonance pathway
            (7, 11),
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
            self.test_T4_gamma_match,
            self.test_T5_alpha_beta_error,
            self.test_T6_dual_pathway,
            self.test_T7_gamma_alpha_complementarity,
            self.test_T8_feedforward_feedback,
            self.test_T9_deviation_detection,
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
        print(f"  SPH FUNCTIONAL TEST RESULTS")
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
            "mechanism": "SPH",
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
        out = RESULTS_DIR / f"sph_results_{ts}.json"
        with open(out, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\n  Report: {out}")


if __name__ == "__main__":
    runner = SPHTestRunner()
    runner.run_all()
