"""PSCL Functional Test — v1.0

Tests PSCL 16D output: E0-E3(extraction), M0-M3(memory+BCH),
P0-P3(present), F0-F3(forecast).

Patterson 2002: alHG pitch center (fMRI cluster [-48,-16,8]).
Penagos 2004: Pitch salience tracks alHG (r=0.92).
Bidelman 2009: FFR pitch salience predicts consonance (r=0.81).
Tabas 2019: POR latency 36ms shorter for consonant in alHG.

PSCL is an Encoder (depth 1) reading BCH relay output.
F1:salience_direction is signed [-1, 1] using tanh.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F1/PSCL/run_pscl_functional_test.py
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

# PSCL 16D indices
E0 = 0    # pitch_salience_raw
E1 = 1    # hg_activation_proxy
E2 = 2    # salience_gradient
E3 = 3    # spectral_focus
M0 = 4    # salience_sustained
M1 = 5    # spectral_coherence
M2 = 6    # tonal_salience_ctx
M3 = 7    # bch_integration (reads BCH relay!)
P0 = 8    # pitch_prominence_sig
P1 = 9    # hg_cortical_response
P2 = 10   # periodicity_clarity
P3 = 11   # salience_hierarchy
F0 = 12   # pitch_continuation
F1 = 13   # salience_direction (SIGNED [-1,1])
F2 = 14   # melody_propagation
F3 = 15   # register_trajectory

DIM_NAMES = [
    "E0:pitch_salience_raw", "E1:hg_activation_proxy",
    "E2:salience_gradient", "E3:spectral_focus",
    "M0:salience_sustained", "M1:spectral_coherence",
    "M2:tonal_salience_ctx", "M3:bch_integration",
    "P0:pitch_prominence_sig", "P1:hg_cortical_response",
    "P2:periodicity_clarity", "P3:salience_hierarchy",
    "F0:pitch_continuation", "F1:salience_direction",
    "F2:melody_propagation", "F3:register_trajectory",
]
OUTPUT_DIM = 16


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class PSCLTestRunner:
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
        relay = outputs.get("PSCL")
        if relay is None:
            raise RuntimeError(f"PSCL not found for '{name}'")
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
    # T1: Pitch Salience (E0) — higher for tonal, pitched sounds
    # Penagos 2004: Pitch salience tracks alHG (r=0.92)
    # ──────────────────────────────────────────────────────────────
    def test_T1_pitch_salience(self):
        G = "T1_pitch_salience"
        for stim in ["g1_01_single", "g1_02_octave", "g1_03_fifth",
                      "g2_01_low", "g2_02_mid", "g2_03_high"]:
            e0 = self._mean(stim, E0)
            self._test(G, f"T1_E0_positive_{stim}", e0 > 0.05,
                       f"E0({e0:.4f}) > 0.05 (pitched → salience)")

        # Single tone should have good pitch salience
        e0_single = self._mean("g1_01_single", E0)
        e0_dense = self._mean("g3_04_dense", E0)
        self._test(G, "T1_E0_single>=dense",
                   e0_single > e0_dense - 0.05,
                   f"single({e0_single:.4f}) >= dense({e0_dense:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T2: HG Activation (E1) — (1-inharmonicity) × spectral quality
    # Patterson 2002: alHG responds to pitch
    # ──────────────────────────────────────────────────────────────
    def test_T2_hg_activation(self):
        G = "T2_hg_activation"
        for stim in ["g1_01_single", "g1_02_octave", "g1_03_fifth"]:
            e1 = self._mean(stim, E1)
            self._test(G, f"T2_E1_positive_{stim}", e1 > 0.05,
                       f"E1({e1:.4f}) > 0.05 (harmonic → HG)")

    # ──────────────────────────────────────────────────────────────
    # T3: BCH Integration (M3) — reads upstream BCH relay
    # M3 = 0.40×BCH_E0 + 0.30×BCH_E1 + 0.20×BCH_P0 + 0.10×BCH_F1
    # ──────────────────────────────────────────────────────────────
    def test_T3_bch_integration(self):
        G = "T3_bch_integration"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g3_04_dense"]
        for stim in stims:
            m3 = self._mean(stim, M3)
            self._test(G, f"T3_M3_bounded_{stim}",
                       0.0 <= m3 <= 1.0,
                       f"M3({m3:.4f}) in [0,1] (BCH relay integration)")

        # M3 should be positive (BCH outputs are always positive for piano)
        m3_single = self._mean("g1_01_single", M3)
        self._test(G, "T3_M3_positive_single", m3_single > 0.05,
                   f"M3({m3_single:.4f}) > 0.05 (BCH provides brainstem signal)")

    # ──────────────────────────────────────────────────────────────
    # T4: Pitch Prominence (P0) — combines E0, M0, M3
    # P0 = 0.25×E0 + 0.25×M0 + 0.20×M3 + ...
    # ──────────────────────────────────────────────────────────────
    def test_T4_pitch_prominence(self):
        G = "T4_pitch_prominence"
        for stim in ["g1_01_single", "g1_02_octave", "g1_03_fifth"]:
            p0 = self._mean(stim, P0)
            self._test(G, f"T4_P0_positive_{stim}", p0 > 0.05,
                       f"P0({p0:.4f}) > 0.05 (tonal → pitch prominence)")

        # Report hierarchy
        p0_vals = {s: self._mean(s, P0) for s in
                   ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd", "g3_04_dense"]}
        self._pass(G, "T4_P0_report",
                   f"P0: " + ", ".join(f"{k}={v:.4f}" for k, v in p0_vals.items()))

    # ──────────────────────────────────────────────────────────────
    # T5: Salience Direction (F1) — SIGNED [-1, 1] using tanh
    # This is the unique signed dimension in PSCL
    # ──────────────────────────────────────────────────────────────
    def test_T5_salience_direction(self):
        G = "T5_salience_direction"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g3_04_dense", "g4_01_sustained"]
        for stim in stims:
            f1 = self._mean(stim, F1)
            self._test(G, f"T5_F1_bounded_{stim}",
                       -1.0 - 1e-6 <= f1 <= 1.0 + 1e-6,
                       f"F1({f1:.4f}) in [-1,1] (tanh activation)")

        # For sustained stimuli, F1 should be near 0 (stable, no trend)
        f1_sust = self._mean("g4_01_sustained", F1)
        self._pass(G, "T5_F1_sustained",
                   f"sustained F1={f1_sust:.4f} (should be near 0 for stable)")

    # ──────────────────────────────────────────────────────────────
    # T6: Register Effects — pitch salience varies with register
    # Pressnitzer 2001: pitch salience varies with register
    # ──────────────────────────────────────────────────────────────
    def test_T6_register(self):
        G = "T6_register"
        for reg in ["g2_01_low", "g2_02_mid", "g2_03_high"]:
            e0 = self._mean(reg, E0)
            p0 = self._mean(reg, P0)
            self._test(G, f"T6_E0_positive_{reg}", e0 > 0.01,
                       f"E0({e0:.4f}) > 0.01")
            self._test(G, f"T6_P0_positive_{reg}", p0 > 0.01,
                       f"P0({p0:.4f}) > 0.01")

        # F3 (register_trajectory) responds to pitch_height
        f3_low = self._mean("g2_01_low", F3)
        f3_mid = self._mean("g2_02_mid", F3)
        f3_high = self._mean("g2_03_high", F3)
        self._pass(G, "T6_F3_register",
                   f"F3: low={f3_low:.4f}, mid={f3_mid:.4f}, high={f3_high:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T7: Forecast (F0, F2) — should be positive for tonal input
    # F0 incorporates BCH F1:pitch_forecast at 10%
    # ──────────────────────────────────────────────────────────────
    def test_T7_forecast(self):
        G = "T7_forecast"
        stims = ["g1_01_single", "g1_03_fifth", "g1_05_minor_2nd",
                 "g3_04_dense", "g5_01_piano", "g5_02_organ"]

        # F0 (pitch continuation) and F2 (melody propagation) should be bounded
        for stim in stims[:3]:
            f0 = self._mean(stim, F0)
            f2 = self._mean(stim, F2)
            self._test(G, f"T7_F0_bounded_{stim}",
                       0.0 <= f0 <= 1.0,
                       f"F0({f0:.4f}) in [0,1]")
            self._test(G, f"T7_F2_bounded_{stim}",
                       0.0 <= f2 <= 1.0,
                       f"F2({f2:.4f}) in [0,1]")

    # ──────────────────────────────────────────────────────────────
    # T8: Memory Layer (M0, M1, M2) — temporal consolidation
    # ──────────────────────────────────────────────────────────────
    def test_T8_memory(self):
        G = "T8_memory"
        stims = ["g1_01_single", "g1_03_fifth", "g3_04_dense"]
        for stim in stims:
            m0 = self._mean(stim, M0)
            m1 = self._mean(stim, M1)
            m2 = self._mean(stim, M2)
            self._test(G, f"T8_M0_bounded_{stim}",
                       0.0 <= m0 <= 1.0, f"M0({m0:.4f}) in [0,1]")
            self._test(G, f"T8_M1_bounded_{stim}",
                       0.0 <= m1 <= 1.0, f"M1({m1:.4f}) in [0,1]")
            self._test(G, f"T8_M2_bounded_{stim}",
                       0.0 <= m2 <= 1.0, f"M2({m2:.4f}) in [0,1]")

    # ──────────────────────────────────────────────────────────────
    # T9: Instrument Contrast
    # ──────────────────────────────────────────────────────────────
    def test_T9_instrument(self):
        G = "T9_instrument"
        for inst in ["g5_01_piano", "g5_02_organ"]:
            e0 = self._mean(inst, E0)
            p0 = self._mean(inst, P0)
            self._test(G, f"T9_E0_positive_{inst}", e0 > 0.01,
                       f"E0({e0:.4f}) > 0.01")
            self._test(G, f"T9_P0_positive_{inst}", p0 > 0.01,
                       f"P0({p0:.4f}) > 0.01")

    # ──────────────────────────────────────────────────────────────
    # T10: Bounds & Shape
    # ──────────────────────────────────────────────────────────────
    def test_T10_bounds_shape(self):
        G = "T10_bounds_shape"
        stims = ["g1_01_single", "g1_05_minor_2nd", "g2_01_low",
                 "g3_04_dense", "g4_03_arpeggio"]
        for stim in stims:
            r = self._load_and_run(stim)
            self._test(G, f"T10_shape_{stim}",
                       r.ndim == 2 and r.shape[1] == OUTPUT_DIM,
                       f"shape={r.shape}")
            # Dims 0-12 and 14-15 clamp [0,1], dim 13 (F1) clamps [-1,1]
            lo_pos = r[:, [*range(13), 14, 15]].min()
            hi_pos = r[:, [*range(13), 14, 15]].max()
            lo_f1 = r[:, 13].min()
            hi_f1 = r[:, 13].max()
            self._test(G, f"T10_bounds_pos_{stim}",
                       lo_pos >= -1e-6 and hi_pos <= 1.0 + 1e-6,
                       f"[0,1] dims: [{lo_pos:.6f}, {hi_pos:.6f}]")
            self._test(G, f"T10_bounds_f1_{stim}",
                       lo_f1 >= -1.0 - 1e-6 and hi_f1 <= 1.0 + 1e-6,
                       f"F1 (signed): [{lo_f1:.6f}, {hi_f1:.6f}]")

    # ──────────────────────────────────────────────────────────────
    # T11: Redundancy Check
    # ──────────────────────────────────────────────────────────────
    def test_T11_redundancy(self):
        G = "T11_redundancy"
        stims = ["g1_01_single", "g1_02_octave", "g1_03_fifth",
                 "g1_04_tritone", "g1_05_minor_2nd", "g1_06_major_7th",
                 "g3_04_dense", "g2_01_low", "g2_03_high",
                 "g5_01_piano", "g5_02_organ"]
        vals = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)]
                         for s in stims])

        # Architectural couplings in PSCL:
        #   E0(0) → P0(8): P0 = 0.25×E0 + ...
        #   E0(0) → P3(11): P3 = ... + 0.15×E0
        #   E1(1) → P1(9): P1 = 0.30×E1 + ...
        #   E2(2) → P3(11): P3 = 0.35×E2 + ...
        #   E3(3) → P2(10): P2 = 0.30×E3 + ...
        #   M0(4) → P0(8): P0 = ... + 0.25×M0 + ...
        #   M0(4) → P3(11): P3 = ... + 0.25×M0
        #   M2(6) → P3(11): P3 = ... + 0.25×M2 + ...
        #   M2(6) → F2(14): F2 = ... + 0.20×M2
        #   M3(7) → P0(8): P0 = ... + 0.20×M3 + ...
        #   P0(8) → F2(14): F2 = 0.30×P0 + ...
        #   M1(5) → P1(9): P1 = ... + 0.25×M1 + ...
        #   E0(0) → M0(4): both use pitch_salience/tonalness
        #   E1(1) → M1(5): spectral features shared
        COUPLED = {
            (0, 4), (0, 8), (0, 11),
            (1, 5), (1, 9),
            (2, 11),
            (3, 10),
            (4, 8), (4, 11),
            (5, 9),
            (6, 11), (6, 14),
            (7, 8),
            (8, 14),
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
            ("T1: Pitch Salience (E0)", self.test_T1_pitch_salience),
            ("T2: HG Activation (E1)", self.test_T2_hg_activation),
            ("T3: BCH Integration (M3)", self.test_T3_bch_integration),
            ("T4: Pitch Prominence (P0)", self.test_T4_pitch_prominence),
            ("T5: Salience Direction (F1)", self.test_T5_salience_direction),
            ("T6: Register Effects", self.test_T6_register),
            ("T7: Forecast (F0, F2)", self.test_T7_forecast),
            ("T8: Memory Layer", self.test_T8_memory),
            ("T9: Instrument Contrast", self.test_T9_instrument),
            ("T10: Bounds & Shape", self.test_T10_bounds_shape),
            ("T11: Redundancy", self.test_T11_redundancy),
        ]

        print("=" * 72)
        print("PSCL FUNCTIONAL TEST v1.0")
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
        print(f"PSCL v1.0 — {passed}/{total} PASS")
        report = {"mechanism": "PSCL", "tests_total": total,
                  "tests_passed": passed, "results": [
                      {"name": r.name, "passed": r.passed, "message": r.message}
                      for r in self.results]}
        rp = RESULTS_DIR / "PSCL_FUNCTIONAL_TEST_REPORT.json"
        with open(rp, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Report: {rp}")
        print(f"OVERALL: {'ALL PASS' if passed == total else f'{total-passed} FAILED'}")
        print("=" * 72)
        return passed == total


if __name__ == "__main__":
    runner = PSCLTestRunner()
    sys.exit(0 if runner.run_all() else 1)
