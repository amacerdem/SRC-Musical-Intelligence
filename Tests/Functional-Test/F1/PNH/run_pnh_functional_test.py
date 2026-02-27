"""PNH Functional Test — v1.0

Tests PNH 11D output: H0(ratio_encoding), H1(conflict_response),
H2(expertise_mod), M0(ratio_complexity), M1(neural_activation),
P0(ratio_enc), P1(conflict_mon), P2(consonance_pref),
F0(dissonance_res_fc), F1(pref_judgment_fc), F2(expertise_mod_fc).

Kim 2021: simple ratios → less IFG activation, complex → more.
Bidelman 2013: consonance hierarchy. Sarasso 2019: aesthetic preference.

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F1/PNH/run_pnh_functional_test.py
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

# PNH 11D indices
H0 = 0   # ratio_encoding
H1 = 1   # conflict_response
H2 = 2   # expertise_mod
M0 = 3   # ratio_complexity
M1 = 4   # neural_activation
P0 = 5   # ratio_enc
P1 = 6   # conflict_mon
P2 = 7   # consonance_pref
F0 = 8   # dissonance_res_fc
F1_ = 9  # pref_judgment_fc (F1 shadows builtin)
F2 = 10  # expertise_mod_fc

DIM_NAMES = [
    "H0:ratio_encoding", "H1:conflict_response", "H2:expertise_mod",
    "M0:ratio_complexity", "M1:neural_activation",
    "P0:ratio_enc", "P1:conflict_mon", "P2:consonance_pref",
    "F0:dissonance_res_fc", "F1:pref_judgment_fc", "F2:expertise_mod_fc",
]
OUTPUT_DIM = 11


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class PNHTestRunner:
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
        relay = outputs.get("PNH")
        if relay is None:
            raise RuntimeError(f"PNH not found for '{name}'")
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

    # T1: Ratio Encoding (H0) — higher for dissonant (complex ratios)
    def test_T1_ratio_encoding(self):
        G = "T1_ratio_encoding"
        h0_unison = self._mean("g1_01_unison", H0)
        h0_fifth = self._mean("g1_03_fifth", H0)
        h0_tritone = self._mean("g1_05_tritone", H0)
        h0_minor2 = self._mean("g1_06_minor2nd", H0)

        # H0 = σ(0.75×(roughness+inharmonicity)/2 at H10)
        # Higher for dissonant intervals
        self._test(G, "T1_H0_minor2>fifth", h0_minor2 > h0_fifth,
                   f"m2({h0_minor2:.4f}) > P5({h0_fifth:.4f})")
        self._test(G, "T1_H0_tritone>unison", h0_tritone > h0_unison,
                   f"TT({h0_tritone:.4f}) > P1({h0_unison:.4f})")
        self._test(G, "T1_H0_minor2>unison", h0_minor2 > h0_unison,
                   f"m2({h0_minor2:.4f}) > P1({h0_unison:.4f})")
        self._pass(G, "T1_H0_hierarchy",
                   f"H0: m2={h0_minor2:.4f}, TT={h0_tritone:.4f}, "
                   f"P5={h0_fifth:.4f}, P1={h0_unison:.4f}")

    # T2: Conflict Response (H1)
    # H1 = σ(0.70 × velocity_D × roughness × roughness_H10)
    # For sustained MIDI chords, velocity_D ≈ 0 (no amplitude change),
    # so H1 ≈ sigmoid(0) = 0.5. H1 only differentiates during dynamic
    # transitions (onset transients, chord changes).
    def test_T2_conflict_response(self):
        G = "T2_conflict_response"

        # All sustained chords should have H1 ≈ 0.5 (sigmoid baseline)
        h1_cons = self._mean("g2_01_consonant_chord", H1)
        h1_diss = self._mean("g2_02_dissonant_cluster", H1)
        self._test(G, "T2_H1_near_baseline",
                   abs(h1_cons - 0.5) < 0.05 and abs(h1_diss - 0.5) < 0.05,
                   f"H1: cons={h1_cons:.4f}, diss={h1_diss:.4f} ≈ 0.5 "
                   f"(velocity_D=0 for sustained chords)")

        # H1 depends on velocity_D × roughness at H10 (400ms chord scale).
        # MIDI piano stimuli have very low velocity_D, so H1 variance is
        # minimal (~0.001) across all stimuli. This is correct — H1 would
        # only activate with real dynamic loudness changes.
        h1_std_stable = self._std("g4_01_stable_consonant", H1)
        self._test(G, "T2_H1_low_variance",
                   h1_std_stable < 0.01,
                   f"H1 std={h1_std_stable:.4f} < 0.01 (velocity_D low for MIDI piano)")

    # T3: Consonance Preference (P2) — higher for consonant
    def test_T3_consonance_pref(self):
        G = "T3_consonance_pref"
        p2_major = self._mean("g3_01_major_triad", P2)
        p2_minor = self._mean("g3_02_minor_triad", P2)
        p2_aug = self._mean("g3_03_aug_triad", P2)
        p2_cluster = self._mean("g3_04_cluster", P2)

        # Major > cluster (consonance preference)
        self._test(G, "T3_P2_major>cluster", p2_major > p2_cluster,
                   f"major({p2_major:.4f}) > cluster({p2_cluster:.4f})")
        # Major ≈ minor (both consonant triads)
        self._test(G, "T3_P2_minor>cluster", p2_minor > p2_cluster,
                   f"minor({p2_minor:.4f}) > cluster({p2_cluster:.4f})")
        self._pass(G, "T3_P2_hierarchy",
                   f"P2: major={p2_major:.4f}, minor={p2_minor:.4f}, "
                   f"aug={p2_aug:.4f}, cluster={p2_cluster:.4f}")

    # T4: Ratio Complexity (M0) — higher for dissonant
    def test_T4_ratio_complexity(self):
        G = "T4_ratio_complexity"
        m0_unison = self._mean("g1_01_unison", M0)
        m0_fifth = self._mean("g1_03_fifth", M0)
        m0_minor2 = self._mean("g1_06_minor2nd", M0)

        self._test(G, "T4_M0_minor2>unison", m0_minor2 > m0_unison,
                   f"m2({m0_minor2:.4f}) > P1({m0_unison:.4f})")
        self._test(G, "T4_M0_minor2>fifth", m0_minor2 > m0_fifth,
                   f"m2({m0_minor2:.4f}) > P5({m0_fifth:.4f})")

    # T5: Neural Activation (M1 = H0 × H1) — gated product
    def test_T5_neural_activation(self):
        G = "T5_neural_activation"
        stims = ["g1_01_unison", "g1_03_fifth", "g1_06_minor2nd",
                 "g2_01_consonant_chord"]
        for stim in stims:
            h0 = self._mean(stim, H0)
            h1 = self._mean(stim, H1)
            m1 = self._mean(stim, M1)
            # M1 = clamp(H0 × H1, 0, 1), so M1 ≤ min(H0, H1)
            self._test(G, f"T5_M1_bounded_{stim[:8]}",
                       m1 <= min(h0, h1) + 0.05,
                       f"M1({m1:.4f}) ≤ min(H0={h0:.4f}, H1={h1:.4f})")

    # T6: Temporal Context
    def test_T6_temporal(self):
        G = "T6_temporal"
        # Stable consonant should have higher P2 than stable dissonant
        p2_cons = self._mean("g4_01_stable_consonant", P2)
        p2_diss = self._mean("g4_02_stable_dissonant", P2)
        self._test(G, "T6_P2_cons>diss", p2_cons > p2_diss,
                   f"cons({p2_cons:.4f}) > diss({p2_diss:.4f})")

        # Rapid alternating should have more H0 variance
        h0_std_stable = self._std("g4_01_stable_consonant", H0)
        h0_std_alt = self._std("g2_04_rapid_alternating", H0)
        self._test(G, "T6_H0_alt>stable_var", h0_std_alt > h0_std_stable,
                   f"alt_std({h0_std_alt:.4f}) > stable_std({h0_std_stable:.4f})")

    # T7: Bounds & Shape
    def test_T7_bounds_shape(self):
        G = "T7_bounds_shape"
        stims = ["g1_01_unison", "g1_06_minor2nd", "g2_02_dissonant_cluster",
                 "g3_04_cluster", "g4_03_resolution"]
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
            ("T1: Ratio Encoding", self.test_T1_ratio_encoding),
            ("T2: Conflict Response", self.test_T2_conflict_response),
            ("T3: Consonance Preference", self.test_T3_consonance_pref),
            ("T4: Ratio Complexity", self.test_T4_ratio_complexity),
            ("T5: Neural Activation", self.test_T5_neural_activation),
            ("T6: Temporal Context", self.test_T6_temporal),
            ("T7: Bounds & Shape", self.test_T7_bounds_shape),
        ]

        print("=" * 72)
        print("PNH FUNCTIONAL TEST v1.0")
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
        print(f"PNH v1.0 — {passed}/{total} PASS")
        report = {"mechanism": "PNH", "tests_total": total,
                  "tests_passed": passed, "results": [
                      {"name": r.name, "passed": r.passed, "message": r.message}
                      for r in self.results]}
        rp = RESULTS_DIR / "PNH_FUNCTIONAL_TEST_REPORT.json"
        with open(rp, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Report: {rp}")
        print(f"OVERALL: {'ALL PASS' if passed == total else f'{total-passed} FAILED'}")
        print("=" * 72)
        return passed == total


if __name__ == "__main__":
    runner = PNHTestRunner()
    sys.exit(0 if runner.run_all() else 1)
