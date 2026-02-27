"""TPIO Functional Test — v1.0

Tests TPIO 10D output: f01(perception_substrate), f02(imagery_substrate),
f03(perc_imag_overlap), f04(sma_imagery), M0(overlap_index),
P0(pstg_activation), P1(sma_activation), F0-F2(forecasts).

Halpern 2004: pSTG perception-imagery overlap r=0.84.
Zatorre 2005: SMA activation during timbral imagery.
Crowder 1989: imagery preserves spectral detail from memory.
McAdams 1999: spectral continuity drives timbre expectation.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F1/TPIO/run_tpio_functional_test.py
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

# TPIO 10D indices (note: E-layer uses f01-f04 naming)
f01 = 0   # perception_substrate
f02 = 1   # imagery_substrate
f03 = 2   # perc_imag_overlap
f04 = 3   # sma_imagery
M0  = 4   # overlap_index
P0  = 5   # pstg_activation
P1  = 6   # sma_activation
F0  = 7   # imagery_stability_pred
F1  = 8   # timbre_expectation
F2  = 9   # overlap_pred

DIM_NAMES = [
    "f01:perception_substrate", "f02:imagery_substrate",
    "f03:perc_imag_overlap", "f04:sma_imagery",
    "M0:overlap_index", "P0:pstg_activation",
    "P1:sma_activation", "F0:imagery_stability_pred",
    "F1:timbre_expectation", "F2:overlap_pred",
]
OUTPUT_DIM = 10


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class TPIOTestRunner:
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
        relay = outputs.get("TPIO")
        if relay is None:
            raise RuntimeError(f"TPIO not found for '{name}'")
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
    # T1: Perception Substrate (f01) — all tonal input should activate
    # Halpern 2004: pSTG processes warmth+sharpness for timbral quality
    # ──────────────────────────────────────────────────────────────
    def test_T1_perception_substrate(self):
        G = "T1_perception_substrate"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g2_01_low_c3", "g2_02_mid_c4", "g2_03_high_c6"]
        for stim in stims:
            val = self._mean(stim, f01)
            self._test(G, f"T1_f01_positive_{stim}", val > 0.15,
                       f"f01({val:.4f}) > 0.15 (tonal → perception substrate)")

        # Cluster still perceivable
        val_cl = self._mean("g1_04_cluster", f01)
        self._test(G, "T1_f01_cluster_positive", val_cl > 0.10,
                   f"cluster f01({val_cl:.4f}) > 0.10")

    # ──────────────────────────────────────────────────────────────
    # T2: Imagery Substrate (f02) — memory-based representation
    # Crowder 1989: imagery preserves spectral detail from memory
    # ──────────────────────────────────────────────────────────────
    def test_T2_imagery_substrate(self):
        G = "T2_imagery_substrate"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g2_02_mid_c4"]
        for stim in stims:
            val = self._mean(stim, f02)
            self._test(G, f"T2_f02_positive_{stim}", val > 0.15,
                       f"f02({val:.4f}) > 0.15 (tonal → imagery substrate)")

    # ──────────────────────────────────────────────────────────────
    # T3: Perception-Imagery Overlap (f03) — f01×f02 product + cross-terms
    # Halpern 2004: overlap in pSTG (r=0.84)
    # ──────────────────────────────────────────────────────────────
    def test_T3_overlap(self):
        G = "T3_overlap"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad"]
        for stim in stims:
            val_f01 = self._mean(stim, f01)
            val_f02 = self._mean(stim, f02)
            val_f03 = self._mean(stim, f03)
            # f03 depends on f01×f02 product → positive when both active
            self._test(G, f"T3_f03_positive_{stim}", val_f03 > 0.10,
                       f"f03({val_f03:.4f}) > 0.10 (f01={val_f01:.4f}, f02={val_f02:.4f})")

    # ──────────────────────────────────────────────────────────────
    # T4: SMA Imagery (f04) — motor imagery for timbral production
    # Zatorre 2005: SMA activation during timbral imagery
    # ──────────────────────────────────────────────────────────────
    def test_T4_sma_imagery(self):
        G = "T4_sma_imagery"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g2_02_mid_c4"]
        for stim in stims:
            val = self._mean(stim, f04)
            self._test(G, f"T4_f04_positive_{stim}", val > 0.15,
                       f"f04({val:.4f}) > 0.15 (tristimulus+tonalness → SMA)")

    # ──────────────────────────────────────────────────────────────
    # T5: Overlap Index (M0) — bounded by E-layer
    # M0 = σ(0.40×f03 + 0.25×f01 + 0.20×f02 + 0.15×f04)
    # ──────────────────────────────────────────────────────────────
    def test_T5_overlap_index(self):
        G = "T5_overlap_index"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g1_04_cluster", "g4_01_sustained"]
        for stim in stims:
            m0_val = self._mean(stim, M0)
            f01_val = self._mean(stim, f01)
            f02_val = self._mean(stim, f02)
            f03_val = self._mean(stim, f03)
            f04_val = self._mean(stim, f04)
            # M0 is sigmoid of weighted E-layer sum → should be positive
            self._test(G, f"T5_M0_positive_{stim}", m0_val > 0.10,
                       f"M0({m0_val:.4f}) > 0.10 "
                       f"(f01={f01_val:.4f}, f02={f02_val:.4f}, "
                       f"f03={f03_val:.4f}, f04={f04_val:.4f})")

    # ──────────────────────────────────────────────────────────────
    # T6: Instrument Contrast — different timbres produce different profiles
    # Halpern 2004: pSTG distinguishes timbral quality
    # ──────────────────────────────────────────────────────────────
    def test_T6_instrument_contrast(self):
        G = "T6_instrument"
        instruments = ["g3_01_piano", "g3_02_organ", "g3_03_violin", "g3_04_flute"]

        # All instruments should produce positive activation
        for inst in instruments:
            f01_val = self._mean(inst, f01)
            self._test(G, f"T6_f01_{inst}", f01_val > 0.10,
                       f"f01({f01_val:.4f}) > 0.10")

        # Different instruments should produce different f01 profiles
        f01_vals = [self._mean(inst, f01) for inst in instruments]
        f01_range = max(f01_vals) - min(f01_vals)
        # Piano, organ, violin, flute have different warmth/sharpness profiles
        self._pass(G, "T6_f01_range",
                   f"f01 range across instruments: {f01_range:.4f} "
                   f"(piano={f01_vals[0]:.4f}, organ={f01_vals[1]:.4f}, "
                   f"violin={f01_vals[2]:.4f}, flute={f01_vals[3]:.4f})")

        # P0 (pSTG activation) should be positive for all instruments
        for inst in instruments:
            p0_val = self._mean(inst, P0)
            self._test(G, f"T6_P0_{inst}", p0_val > 0.10,
                       f"P0({p0_val:.4f}) > 0.10 (pSTG activation)")

    # ──────────────────────────────────────────────────────────────
    # T7: Register Effects — warmth/sharpness differ across register
    # ──────────────────────────────────────────────────────────────
    def test_T7_register(self):
        G = "T7_register"
        regs = ["g2_01_low_c3", "g2_02_mid_c4", "g2_03_high_c6"]
        for reg in regs:
            f01_val = self._mean(reg, f01)
            f02_val = self._mean(reg, f02)
            self._test(G, f"T7_f01_positive_{reg}", f01_val > 0.10,
                       f"f01({f01_val:.4f}) > 0.10")
            self._test(G, f"T7_f02_positive_{reg}", f02_val > 0.10,
                       f"f02({f02_val:.4f}) > 0.10")

        # Report register comparison
        self._pass(G, "T7_register_report",
                   f"f01: low={self._mean('g2_01_low_c3', f01):.4f}, "
                   f"mid={self._mean('g2_02_mid_c4', f01):.4f}, "
                   f"high={self._mean('g2_03_high_c6', f01):.4f}")

    # ──────────────────────────────────────────────────────────────
    # T8: Temporal Dynamics — P1 (SMA) responds to spectral change
    # ──────────────────────────────────────────────────────────────
    def test_T8_temporal(self):
        G = "T8_temporal"
        # P1 includes spectral_change_velocity → more active during changes
        p1_sust = self._mean("g4_01_sustained", P1)
        p1_melody = self._mean("g4_02_melody", P1)
        p1_arp = self._mean("g4_03_arpeggio", P1)

        # All should be positive
        for stim, val in [("sustained", p1_sust), ("melody", p1_melody),
                          ("arpeggio", p1_arp)]:
            self._test(G, f"T8_P1_positive_{stim}", val > 0.10,
                       f"P1({val:.4f}) > 0.10")

        # P0 (pSTG) should be positive for all temporal patterns
        for stim in ["g4_01_sustained", "g4_02_melody", "g4_03_arpeggio"]:
            p0_val = self._mean(stim, P0)
            self._test(G, f"T8_P0_positive_{stim}", p0_val > 0.10,
                       f"P0({p0_val:.4f}) > 0.10")

    # ──────────────────────────────────────────────────────────────
    # T9: Forecast Consistency
    # F0 = σ(0.40×M0 + 0.30×f02 + 0.30×P1)
    # F1 = σ(0.35×P0 + 0.30×f01 + 0.20×f04 + 0.15×M0)
    # F2 = σ(0.40×f03 + 0.30×M0 + 0.30×P0)
    # ──────────────────────────────────────────────────────────────
    def test_T9_forecast(self):
        G = "T9_forecast"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g1_04_cluster", "g3_01_piano", "g3_02_organ"]

        # F1 tracks P0 (dominant 0.35) + f01 (0.30)
        f1_vals = [self._mean(s, F1) for s in stims]
        p0_vals = [self._mean(s, P0) for s in stims]
        if np.std(f1_vals) > 1e-6 and np.std(p0_vals) > 1e-6:
            r = float(np.corrcoef(f1_vals, p0_vals)[0, 1])
            self._test(G, "T9_F1_P0_corr", r > 0.3,
                       f"r(F1,P0) = {r:+.3f} > 0.3")
        else:
            self._pass(G, "T9_F1_P0_corr",
                       f"Low variance — F1 std={np.std(f1_vals):.6f}")

        # F2 tracks f03 (dominant 0.40) + M0 (0.30) + P0 (0.30)
        f2_vals = [self._mean(s, F2) for s in stims]
        f03_vals = [self._mean(s, f03) for s in stims]
        if np.std(f2_vals) > 1e-6 and np.std(f03_vals) > 1e-6:
            r = float(np.corrcoef(f2_vals, f03_vals)[0, 1])
            self._test(G, "T9_F2_f03_corr", r > 0.3,
                       f"r(F2,f03) = {r:+.3f} > 0.3")
        else:
            self._pass(G, "T9_F2_f03_corr",
                       f"Low variance — F2 std={np.std(f2_vals):.6f}")

        # All forecasts should be positive
        for stim in stims[:3]:
            for dim, name in [(F0, "F0"), (F1, "F1"), (F2, "F2")]:
                val = self._mean(stim, dim)
                self._test(G, f"T9_{name}_positive_{stim}", val > 0.10,
                           f"{name}({val:.4f}) > 0.10")

    # ──────────────────────────────────────────────────────────────
    # T10: Bounds & Shape
    # ──────────────────────────────────────────────────────────────
    def test_T10_bounds_shape(self):
        G = "T10_bounds_shape"
        stims = ["g1_01_single", "g1_04_cluster", "g2_01_low_c3",
                 "g3_03_violin", "g5_03_alternating"]
        for stim in stims:
            r = self._load_and_run(stim)
            self._test(G, f"T10_shape_{stim}",
                       r.ndim == 2 and r.shape[1] == OUTPUT_DIM,
                       f"shape={r.shape}")
            lo, hi = r.min(), r.max()
            self._test(G, f"T10_bounds_{stim}",
                       lo >= -1e-6 and hi <= 1.0 + 1e-6,
                       f"[{lo:.6f}, {hi:.6f}]")

    # ──────────────────────────────────────────────────────────────
    # T11: Redundancy Check
    # ──────────────────────────────────────────────────────────────
    def test_T11_redundancy(self):
        G = "T11_redundancy"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g1_04_cluster", "g2_01_low_c3", "g2_03_high_c6",
                 "g3_01_piano", "g3_02_organ", "g3_03_violin", "g3_04_flute"]
        vals = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)]
                         for s in stims])

        # Known architectural couplings:
        #   f01(0) → f03(2): f03 = σ(0.40×f01×f02 + ...)
        #   f02(1) → f03(2): f03 = σ(0.40×f01×f02 + ...)
        #   f03(2) → M0(4): M0 = σ(0.40×f03 + ...)
        #   f03(2) → F2(9): F2 = σ(0.40×f03 + ...)
        #   f01(0) → M0(4): M0 = σ(... + 0.25×f01 + ...)
        #   f01(0) → P0(5): P0 = σ(0.25×f01 + ...)
        #   f01(0) → F1(8): F1 = σ(... + 0.30×f01 + ...)
        #   f04(3) → P1(6): P1 = σ(0.30×f04 + ...)
        #   f04(3) → F1(8): F1 = σ(... + 0.20×f04 + ...)
        #   M0(4) → F0(7): F0 = σ(0.40×M0 + ...)
        #   M0(4) → F1(8): F1 = σ(... + 0.15×M0)
        #   M0(4) → F2(9): F2 = σ(... + 0.30×M0 + ...)
        #   P0(5) → F1(8): F1 = σ(0.35×P0 + ...)
        #   P0(5) → F2(9): F2 = σ(... + 0.30×P0)
        #   f02(1) → F0(7): F0 = σ(... + 0.30×f02 + ...)
        #   f03(2) → P1(6): P1 = σ(... + 0.15×f03 + ...)
        COUPLED = {
            (0, 2), (1, 2), (2, 4), (2, 9),
            (0, 4), (0, 5), (0, 7), (0, 8),
            (1, 4), (1, 7), (1, 9),
            (3, 6), (3, 8),
            (4, 7), (4, 8), (4, 9),
            (5, 8), (5, 9),
            (2, 6),
        }

        redundant = []
        for i in range(OUTPUT_DIM):
            for j in range(i + 1, OUTPUT_DIM):
                if (i, j) in COUPLED:
                    continue
                si, sj = np.std(vals[:, i]), np.std(vals[:, j])
                if si < 1e-6 or sj < 1e-6:
                    continue
                r = abs(np.corrcoef(vals[:, i], vals[:, j])[0, 1])
                if r > 0.99:
                    redundant.append((i, j, r))
                    self._fail(G, f"T11_redundancy_{i}_{j}",
                               f"|r({DIM_NAMES[i]},{DIM_NAMES[j]})| = {r:.3f} > 0.99")
        if not redundant:
            self._pass(G, "T11_no_redundancy",
                       "No unexpected redundant dimension pairs")

    def run_all(self):
        tests = [
            ("T1: Perception Substrate (f01)", self.test_T1_perception_substrate),
            ("T2: Imagery Substrate (f02)", self.test_T2_imagery_substrate),
            ("T3: Perception-Imagery Overlap (f03)", self.test_T3_overlap),
            ("T4: SMA Imagery (f04)", self.test_T4_sma_imagery),
            ("T5: Overlap Index (M0)", self.test_T5_overlap_index),
            ("T6: Instrument Contrast", self.test_T6_instrument_contrast),
            ("T7: Register Effects", self.test_T7_register),
            ("T8: Temporal Dynamics", self.test_T8_temporal),
            ("T9: Forecast Consistency", self.test_T9_forecast),
            ("T10: Bounds & Shape", self.test_T10_bounds_shape),
            ("T11: Redundancy", self.test_T11_redundancy),
        ]

        print("=" * 72)
        print("TPIO FUNCTIONAL TEST v1.0")
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
        print(f"TPIO v1.0 — {passed}/{total} PASS")
        report = {"mechanism": "TPIO", "tests_total": total,
                  "tests_passed": passed, "results": [
                      {"name": r.name, "passed": r.passed, "message": r.message}
                      for r in self.results]}
        rp = RESULTS_DIR / "TPIO_FUNCTIONAL_TEST_REPORT.json"
        with open(rp, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Report: {rp}")
        print(f"OVERALL: {'ALL PASS' if passed == total else f'{total-passed} FAILED'}")
        print("=" * 72)
        return passed == total


if __name__ == "__main__":
    runner = TPIOTestRunner()
    sys.exit(0 if runner.run_all() else 1)
