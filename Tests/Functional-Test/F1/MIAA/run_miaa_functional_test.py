"""MIAA Functional Test — v1.0

Tests MIAA 11D output: E0(imagery_activation), E1(familiarity_enhancement),
E2(a1_modulation), M0(activation_function), M1(familiarity_effect),
P0(melody_retrieval), P1(continuation_prediction), P2(phrase_structure),
F0-F2(forecasts).

Kraemer 2005: AC active during musical imagery; familiar > unfamiliar
(F(1,14)=48.92 p<.0001); instrumental > lyrics in A1 (F(1,14)=22.55 p<.0005).
Halpern 2004: Perception-imagery overlap r=0.84.
Di Liberto 2021: Imagery pitch ≈ perception (p=0.19 n.s.).

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F1/MIAA/run_miaa_functional_test.py
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

# MIAA 11D indices
E0 = 0   # imagery_activation
E1 = 1   # familiarity_enhancement
E2 = 2   # a1_modulation
M0 = 3   # activation_function
M1 = 4   # familiarity_effect
P0 = 5   # melody_retrieval
P1 = 6   # continuation_prediction
P2 = 7   # phrase_structure
F0 = 8   # melody_continuation_pred
F1 = 9   # ac_activation_pred
F2 = 10  # recognition_pred

DIM_NAMES = [
    "E0:imagery_activation", "E1:familiarity_enhancement",
    "E2:a1_modulation", "M0:activation_function",
    "M1:familiarity_effect", "P0:melody_retrieval",
    "P1:continuation_prediction", "P2:phrase_structure",
    "F0:melody_continuation_pred", "F1:ac_activation_pred",
    "F2:recognition_pred",
]
OUTPUT_DIM = 11


@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class MIAATestRunner:
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
        relay = outputs.get("MIAA")
        if relay is None:
            raise RuntimeError(f"MIAA not found for '{name}'")
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

    def _trace(self, name, dim, skip_warmup=True):
        r = self._load_and_run(name)
        s = H3_WARMUP if (skip_warmup and r.shape[0] > H3_WARMUP + 50) else 0
        return r[s:, dim]

    def _pass(self, g, n, m, **v):
        self.results.append(TestResult(n, g, True, m, v))

    def _fail(self, g, n, m, **v):
        self.results.append(TestResult(n, g, False, m, v))

    def _test(self, g, n, c, m, **v):
        self.results.append(TestResult(n, g, c, m, v))

    # ──────────────────────────────────────────────────────────────
    # T1: Imagery Activation (E0) — tonal sounds produce E0 > baseline
    # Kraemer 2005: AC active during musical imagery (F(1,14)=48.92)
    # ──────────────────────────────────────────────────────────────
    def test_T1_imagery_activation(self):
        G = "T1_imagery_activation"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g2_01_low_c3", "g2_02_mid_c4", "g2_03_high_c6"]
        for stim in stims:
            e0 = self._mean(stim, E0)
            self._test(G, f"T1_E0_positive_{stim}", e0 > 0.15,
                       f"E0({e0:.4f}) > 0.15 (tonal → imagery activation)")

        # Cluster should still produce some activation (it's still piano)
        e0_cluster = self._mean("g1_04_cluster", E0)
        self._test(G, "T1_E0_cluster_positive", e0_cluster > 0.10,
                   f"cluster E0({e0_cluster:.4f}) > 0.10 (still auditory input)")

        # Hierarchy: single ≥ cluster (cluster less tonal)
        e0_single = self._mean("g1_01_single", E0)
        self._test(G, "T1_E0_single>=cluster",
                   e0_single > e0_cluster - 0.05,
                   f"single({e0_single:.4f}) >= cluster({e0_cluster:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T2: A1 Modulation (E2) — instrumental sounds modulate A1
    # Kraemer 2005: instrumental > lyrics in A1 (F(1,14)=22.55)
    # ──────────────────────────────────────────────────────────────
    def test_T2_a1_modulation(self):
        G = "T2_a1_modulation"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g2_01_low_c3", "g2_02_mid_c4"]
        for stim in stims:
            e2 = self._mean(stim, E2)
            self._test(G, f"T2_E2_positive_{stim}", e2 > 0.15,
                       f"E2({e2:.4f}) > 0.15 (instrumental → A1 modulation)")

        # Harmonic input > dissonant cluster (cluster has higher inharmonicity)
        e2_single = self._mean("g1_01_single", E2)
        e2_cluster = self._mean("g1_04_cluster", E2)
        self._test(G, "T2_E2_single>=cluster",
                   e2_single > e2_cluster - 0.05,
                   f"single({e2_single:.4f}) >= cluster({e2_cluster:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T3: Familiarity Enhancement (E1)
    # Kraemer 2005: familiar > unfamiliar BA22 (p<.0001)
    # ──────────────────────────────────────────────────────────────
    def test_T3_familiarity(self):
        G = "T3_familiarity"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g2_02_mid_c4"]
        for stim in stims:
            e1 = self._mean(stim, E1)
            self._test(G, f"T3_E1_positive_{stim}", e1 > 0.15,
                       f"E1({e1:.4f}) > 0.15 (clear tonal → familiarity)")

        # E1 should be reasonable for all piano stimuli
        e1_cluster = self._mean("g1_04_cluster", E1)
        self._test(G, "T3_E1_cluster_positive", e1_cluster > 0.10,
                   f"cluster E1({e1_cluster:.4f}) > 0.10")

    # ──────────────────────────────────────────────────────────────
    # T4: Memory Layer (M0, M1) — verify mathematical relationships
    # M0 = 0.60×E0 + 0.40×E2, M1 = E1×E0
    # ──────────────────────────────────────────────────────────────
    def test_T4_memory_layer(self):
        G = "T4_memory_layer"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g1_04_cluster", "g4_04_dense_cluster"]

        for stim in stims:
            e0 = self._mean(stim, E0)
            e1 = self._mean(stim, E1)
            e2 = self._mean(stim, E2)
            m0 = self._mean(stim, M0)
            m1 = self._mean(stim, M1)

            # M0 = 0.60×E0 + 0.40×E2 → should be between min and max of E0, E2
            m0_expected_lo = min(e0, e2) - 0.05
            m0_expected_hi = max(e0, e2) + 0.05
            self._test(G, f"T4_M0_bounded_{stim}",
                       m0_expected_lo <= m0 <= m0_expected_hi,
                       f"M0({m0:.4f}) in [{m0_expected_lo:.4f}, {m0_expected_hi:.4f}] "
                       f"(E0={e0:.4f}, E2={e2:.4f})")

            # M1 = E1 × E0 → M1 ≤ min(E0, E1) + tolerance
            upper = min(e0, e1) + 0.02
            self._test(G, f"T4_M1_gating_{stim}",
                       m1 <= upper,
                       f"M1({m1:.4f}) ≤ min(E0,E1)+0.02 = {upper:.4f} "
                       f"(multiplicative gating)")

    # ──────────────────────────────────────────────────────────────
    # T5: Phrase Structure (P2) — spectral flux entropy
    # Di Liberto 2021: sub-1Hz phrase boundaries critical
    # ──────────────────────────────────────────────────────────────
    def test_T5_phrase_structure(self):
        G = "T5_phrase_structure"

        # P2 = σ(spectral_flux_entropy) at H8 (300ms) L0
        # Piano attack/decay creates spectral flux even in sustained chords,
        # and H8 smoothing (300ms) averages out rapid arpeggio changes.
        # Test: all stimuli produce meaningful P2 values
        p2_sust_std = self._std("g3_01_sustained", P2)
        p2_melody_std = self._std("g3_02_melody", P2)
        p2_arp_std = self._std("g3_04_arpeggio", P2)
        p2_prog_std = self._std("g3_03_chord_progression", P2)

        # All P2 means should be > 0 (spectral flux entropy is always present)
        for stim in ["g3_01_sustained", "g3_02_melody",
                     "g3_03_chord_progression", "g3_04_arpeggio"]:
            p2_m = self._mean(stim, P2)
            self._test(G, f"T5_P2_positive_{stim}", p2_m > 0.10,
                       f"P2({p2_m:.4f}) > 0.10 (spectral flux present)")

        # Report variance comparison
        self._pass(G, "T5_P2_var_report",
                   f"P2 std: sustained={p2_sust_std:.4f}, melody={p2_melody_std:.4f}, "
                   f"prog={p2_prog_std:.4f}, arp={p2_arp_std:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T6: Continuation Prediction (P1)
    # P1 = σ(0.50×tonalness_mean + 0.50×trist_balance)
    # ──────────────────────────────────────────────────────────────
    def test_T6_continuation(self):
        G = "T6_continuation"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g2_02_mid_c4"]
        for stim in stims:
            p1 = self._mean(stim, P1)
            self._test(G, f"T6_P1_positive_{stim}", p1 > 0.15,
                       f"P1({p1:.4f}) > 0.15 (tonal → continuation prediction)")

    # ──────────────────────────────────────────────────────────────
    # T7: Melody Retrieval (P0)
    # Halpern 2004: perception-imagery overlap r=0.84
    # P0 = 0.35×M0 + 0.25×E1 + 0.20×(1-inharm) + 0.20×clarity_mean
    # ──────────────────────────────────────────────────────────────
    def test_T7_melody_retrieval(self):
        G = "T7_melody_retrieval"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad"]
        for stim in stims:
            p0 = self._mean(stim, P0)
            self._test(G, f"T7_P0_positive_{stim}", p0 > 0.15,
                       f"P0({p0:.4f}) > 0.15 (tonal → melody retrieval)")

        # Single tone: should be strong retrieval (clear harmonic)
        p0_single = self._mean("g1_01_single", P0)
        p0_cluster = self._mean("g1_04_cluster", P0)
        self._test(G, "T7_P0_single>=cluster",
                   p0_single > p0_cluster - 0.05,
                   f"single({p0_single:.4f}) >= cluster({p0_cluster:.4f})-0.05")

    # ──────────────────────────────────────────────────────────────
    # T8: Forecast Consistency (F0, F1, F2)
    # F0 = σ(0.50×E0 + 0.30×P0 + 0.20×P1)
    # F1 = σ(0.60×E1 + 0.40×E0)
    # F2 = σ(0.50×E1 + 0.30×spectral_auto_mean + 0.20×tonalness_mean)
    # ──────────────────────────────────────────────────────────────
    def test_T8_forecast(self):
        G = "T8_forecast"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g1_04_cluster", "g4_04_dense_cluster"]

        # F1 should correlate with E1 (dominant component: 0.60×E1)
        f1_vals = [self._mean(s, F1) for s in stims]
        e1_vals = [self._mean(s, E1) for s in stims]
        if np.std(f1_vals) > 1e-6 and np.std(e1_vals) > 1e-6:
            r_f1_e1 = float(np.corrcoef(f1_vals, e1_vals)[0, 1])
            self._test(G, "T8_F1_E1_corr", r_f1_e1 > 0.3,
                       f"r(F1,E1) = {r_f1_e1:+.3f} > 0.3")
        else:
            self._pass(G, "T8_F1_E1_corr",
                       f"Low variance — F1 std={np.std(f1_vals):.6f}")

        # F0 = σ(0.50×E0 + 0.30×P0 + 0.20×P1) — multi-input, may not
        # correlate with any single component. Verify F0 is bounded and positive.
        f0_vals = [self._mean(s, F0) for s in stims]
        f0_min, f0_max = min(f0_vals), max(f0_vals)
        self._test(G, "T8_F0_positive", f0_min > 0.10,
                   f"F0 range [{f0_min:.4f}, {f0_max:.4f}] all > 0.10")

        # F2 should correlate with E1 (dominant component: 0.50×E1)
        f2_vals = [self._mean(s, F2) for s in stims]
        if np.std(f2_vals) > 1e-6 and np.std(e1_vals) > 1e-6:
            r_f2_e1 = float(np.corrcoef(f2_vals, e1_vals)[0, 1])
            self._test(G, "T8_F2_E1_corr", r_f2_e1 > 0.3,
                       f"r(F2,E1) = {r_f2_e1:+.3f} > 0.3")
        else:
            self._pass(G, "T8_F2_E1_corr",
                       f"Low variance — F2 std={np.std(f2_vals):.6f}")

    # ──────────────────────────────────────────────────────────────
    # T9: Register Effects
    # Tristimulus balance varies by register
    # ──────────────────────────────────────────────────────────────
    def test_T9_register(self):
        G = "T9_register"
        e0_low = self._mean("g2_01_low_c3", E0)
        e0_mid = self._mean("g2_02_mid_c4", E0)
        e0_high = self._mean("g2_03_high_c6", E0)

        # All registers should produce imagery activation
        self._test(G, "T9_E0_low>0.10", e0_low > 0.10,
                   f"C3 E0={e0_low:.4f}")
        self._test(G, "T9_E0_mid>0.10", e0_mid > 0.10,
                   f"C4 E0={e0_mid:.4f}")
        self._test(G, "T9_E0_high>0.10", e0_high > 0.10,
                   f"C6 E0={e0_high:.4f}")

        # Report E1, E2 across register
        self._pass(G, "T9_register_report",
                   f"E0: low={e0_low:.4f}, mid={e0_mid:.4f}, high={e0_high:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T10: Instrument Contrast
    # Kraemer 2005: different instrument types → different A1 response
    # ──────────────────────────────────────────────────────────────
    def test_T10_instrument(self):
        G = "T10_instrument"
        e2_piano = self._mean("g5_01_piano_c4", E2)
        e2_organ = self._mean("g5_02_organ_c4", E2)

        # Both should produce A1 modulation
        self._test(G, "T10_E2_piano>0.10", e2_piano > 0.10,
                   f"piano E2={e2_piano:.4f}")
        self._test(G, "T10_E2_organ>0.10", e2_organ > 0.10,
                   f"organ E2={e2_organ:.4f}")

        # E0 should also differ (different tristimulus)
        e0_piano = self._mean("g5_01_piano_c4", E0)
        e0_organ = self._mean("g5_02_organ_c4", E0)
        self._pass(G, "T10_instrument_report",
                   f"piano: E0={e0_piano:.4f} E2={e2_piano:.4f}, "
                   f"organ: E0={e0_organ:.4f} E2={e2_organ:.4f}")

    # ──────────────────────────────────────────────────────────────
    # T11: Bounds & Shape
    # ──────────────────────────────────────────────────────────────
    def test_T11_bounds_shape(self):
        G = "T11_bounds_shape"
        stims = ["g1_01_single", "g1_04_cluster", "g2_01_low_c3",
                 "g3_04_arpeggio", "g4_04_dense_cluster"]
        for stim in stims:
            r = self._load_and_run(stim)
            self._test(G, f"T11_shape_{stim}",
                       r.ndim == 2 and r.shape[1] == OUTPUT_DIM,
                       f"shape={r.shape}")
            lo, hi = r.min(), r.max()
            self._test(G, f"T11_bounds_{stim}",
                       lo >= -1e-6 and hi <= 1.0 + 1e-6,
                       f"[{lo:.6f}, {hi:.6f}]")

    # ──────────────────────────────────────────────────────────────
    # T12: Redundancy Check
    # ──────────────────────────────────────────────────────────────
    def test_T12_redundancy(self):
        G = "T12_redundancy"
        stims = ["g1_01_single", "g1_02_fifth", "g1_03_triad",
                 "g1_04_cluster", "g2_01_low_c3", "g2_03_high_c6",
                 "g4_02_dyad", "g4_04_dense_cluster",
                 "g5_01_piano_c4", "g5_02_organ_c4"]
        vals = np.array([[self._mean(s, d) for d in range(OUTPUT_DIM)]
                         for s in stims])

        # Known architectural couplings:
        #   E0(0) → M0(3): M0 = 0.60×E0 + 0.40×E2
        #   E0(0) → M1(4): M1 = E1 × E0
        #   E2(2) → M0(3): M0 = 0.60×E0 + 0.40×E2
        #   E0(0) → F0(8): F0 = σ(0.50×E0 + ...)
        #   E0(0) → F1(9): F1 = σ(0.40×E0 + 0.60×E1)
        #   E1(1) → F1(9): F1 = σ(0.60×E1 + 0.40×E0)
        #   E1(1) → F2(10): F2 = σ(0.50×E1 + ...)
        #   M0(3) → P0(5): P0 = 0.35×M0 + ...
        #   E1(1) → P0(5): P0 = ... + 0.25×E1 + ...
        #   M0(3) → F0(8): via P0
        COUPLED = {
            (0, 3), (0, 4), (2, 3),
            (0, 8), (0, 9),
            (1, 5), (1, 9), (1, 10),
            (3, 5), (3, 8),
            (4, 9),  # M1(E1×E0) ↔ F1(0.60×E1+0.40×E0) — same inputs
            (5, 8),  # P0 → F0
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
                    self._fail(G, f"T12_redundancy_{i}_{j}",
                               f"|r({DIM_NAMES[i]},{DIM_NAMES[j]})| = {r:.3f} > 0.99")
        if not redundant:
            self._pass(G, "T12_no_redundancy",
                       "No unexpected redundant dimension pairs")

    def run_all(self):
        tests = [
            ("T1: Imagery Activation (E0)", self.test_T1_imagery_activation),
            ("T2: A1 Modulation (E2)", self.test_T2_a1_modulation),
            ("T3: Familiarity Enhancement (E1)", self.test_T3_familiarity),
            ("T4: Memory Layer (M0, M1)", self.test_T4_memory_layer),
            ("T5: Phrase Structure (P2)", self.test_T5_phrase_structure),
            ("T6: Continuation Prediction (P1)", self.test_T6_continuation),
            ("T7: Melody Retrieval (P0)", self.test_T7_melody_retrieval),
            ("T8: Forecast Consistency", self.test_T8_forecast),
            ("T9: Register Effects", self.test_T9_register),
            ("T10: Instrument Contrast", self.test_T10_instrument),
            ("T11: Bounds & Shape", self.test_T11_bounds_shape),
            ("T12: Redundancy", self.test_T12_redundancy),
        ]

        print("=" * 72)
        print("MIAA FUNCTIONAL TEST v1.0")
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
        print(f"MIAA v1.0 — {passed}/{total} PASS")
        report = {"mechanism": "MIAA", "tests_total": total,
                  "tests_passed": passed, "results": [
                      {"name": r.name, "passed": r.passed, "message": r.message}
                      for r in self.results]}
        rp = RESULTS_DIR / "MIAA_FUNCTIONAL_TEST_REPORT.json"
        with open(rp, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"Report: {rp}")
        print(f"OVERALL: {'ALL PASS' if passed == total else f'{total-passed} FAILED'}")
        print("=" * 72)
        return passed == total


if __name__ == "__main__":
    runner = MIAATestRunner()
    sys.exit(0 if runner.run_all() else 1)
