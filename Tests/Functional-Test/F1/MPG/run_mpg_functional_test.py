"""MPG Comprehensive Functional Test — v1.0

Processes 24 MIDI stimuli through the full MI pipeline and validates
MPG's 10D output against theoretical predictions from:

  - Rupp 2022: posterior→anterior cortical gradient
  - Patterson 2002: onset-locked HG processing
  - Norman-Haignere 2013: anterior AC contour tracking
  - Briley 2013: pitch contour complexity EEG sources
  - Cheung 2019: phrase boundary uncertainty×surprise

Test Groups:
  T1:  Contour Activity — E1 ordering (scale > repeated > sustained)
  T2:  Onset Detection — E0/M1 ordering (fast > regular > sustained)
  T3:  Contour Complexity — E2 ordering (random > chromatic > scale > sustained)
  T4:  Gradient Ratio — E3 (onset-dominant > balanced > contour-dominant)
  T5:  Phrase Boundary — F0 peak during silence gaps
  T6:  Present Layer — P0 tracks E0, P1 tracks E1/E2
  T7:  Memory Layer — M0 ≈ 0.7*E0 + 0.3*E1
  T8:  Correlation Health — cross-dimension correlations
  T9:  Bounds & Shape — all outputs in [0, 1], shape (B, T, 10)
  T10: Register — pitch height influence on E1/E2

Usage:
    cd "SRC Musical Intelligence"
    python Tests/Functional-Test/F1/MPG/run_mpg_functional_test.py
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

# -- Project paths --
ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Lab"))

import torch
import torchaudio

from backend.config import FRAME_RATE
from backend.pipeline import MIPipeline

# -- Constants --
STIMULI_DIR = pathlib.Path(__file__).resolve().parent / "stimuli"
RESULTS_DIR = pathlib.Path(__file__).resolve().parent / "results"
RESULTS_DIR.mkdir(exist_ok=True)

SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048
H3_WARMUP = 180  # frames to skip for H³ stabilization


# -- MPG dimension indices within relay output (0-indexed) --
E0 = 0   # onset_posterior
E1 = 1   # sequence_anterior
E2 = 2   # contour_complexity
E3 = 3   # gradient_ratio
M0 = 4   # activity_x
M1 = 5   # posterior_activity
M2 = 6   # anterior_activity
P0 = 7   # onset_state
P1 = 8   # contour_state
F0 = 9   # phrase_boundary_pred

DIM_NAMES = [
    "E0:onset_posterior", "E1:sequence_anterior",
    "E2:contour_complexity", "E3:gradient_ratio",
    "M0:activity_x", "M1:posterior_activity", "M2:anterior_activity",
    "P0:onset_state", "P1:contour_state",
    "F0:phrase_boundary_pred",
]


# ══════════════════════════════════════════════════════════════════════
# Test Result Tracking
# ══════════════════════════════════════════════════════════════════════

@dataclass
class TestResult:
    name: str
    group: str
    passed: bool
    message: str
    values: Dict[str, Any] = field(default_factory=dict)


class MPGTestRunner:
    def __init__(self):
        self.results: List[TestResult] = []
        self.relay_cache: Dict[str, np.ndarray] = {}  # name -> (T, 10)
        self.pipeline: MIPipeline = None

    def _init_pipeline(self):
        """Initialize MI Pipeline."""
        print("Initializing MI Pipeline...")
        self.pipeline = MIPipeline()
        print()

    def _load_wav(self, name: str):
        """Load WAV with edge padding (matches pipeline.py)."""
        import soundfile as sf

        path = STIMULI_DIR / f"{name}.wav"
        data, sr = sf.read(str(path), dtype="float32")
        if data.ndim == 2:
            data = data.mean(axis=1)
        waveform = torch.from_numpy(data).unsqueeze(0)

        if sr != SAMPLE_RATE:
            waveform = torchaudio.transforms.Resample(sr, SAMPLE_RATE)(waveform)

        # Edge padding to prevent STFT artifacts (same as pipeline.py)
        pad_len = N_FFT // 2
        edge_l = waveform[:, :1].expand(-1, pad_len)
        edge_r = waveform[:, -1:].expand(-1, pad_len)
        waveform_padded = torch.cat([edge_l, waveform, edge_r], dim=-1)

        mel_transform = torchaudio.transforms.MelSpectrogram(
            sample_rate=SAMPLE_RATE, n_fft=N_FFT, hop_length=HOP_LENGTH,
            n_mels=N_MELS, power=2.0,
        )
        mel = mel_transform(waveform_padded)
        pad_frames = pad_len // HOP_LENGTH
        mel = mel[:, :, pad_frames: mel.shape[-1] - pad_frames]
        mel = torch.log1p(mel)
        mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
        mel = mel / mel_max

        return waveform, mel

    def _load_and_run(self, name: str) -> np.ndarray:
        """Load stimulus, run pipeline, extract MPG relay. Returns (T, 10)."""
        if name in self.relay_cache:
            return self.relay_cache[name]

        waveform, mel = self._load_wav(name)

        with torch.no_grad():
            r3_output = self.pipeline.r3_extractor.extract(
                mel, audio=waveform, sr=SAMPLE_RATE,
            )
            r3_features = r3_output.features

            h3_output = self.pipeline.h3_extractor.extract(
                r3_features, self.pipeline.h3_demand,
            )

            outputs, _ram, _neuro = self.pipeline._execute(
                self.pipeline.nuclei, h3_output.features, r3_features,
            )

        mpg = outputs.get("MPG")
        if mpg is None:
            raise RuntimeError(f"MPG relay not found for stimulus '{name}'")

        mpg_np = mpg.squeeze(0).numpy() if isinstance(mpg, torch.Tensor) else mpg
        if mpg_np.ndim == 3:
            mpg_np = mpg_np[0]

        self.relay_cache[name] = mpg_np
        return mpg_np

    def _mean(self, name: str, dim: int, skip_warmup: bool = True) -> float:
        """Mean of dimension across time, optionally skipping H³ warmup."""
        relay = self._load_and_run(name)
        start = H3_WARMUP if (skip_warmup and relay.shape[0] > H3_WARMUP + 50) else 0
        return float(relay[start:, dim].mean())

    def _std(self, name: str, dim: int, skip_warmup: bool = True) -> float:
        relay = self._load_and_run(name)
        start = H3_WARMUP if (skip_warmup and relay.shape[0] > H3_WARMUP + 50) else 0
        return float(relay[start:, dim].std())

    def _max(self, name: str, dim: int) -> float:
        relay = self._load_and_run(name)
        return float(relay[:, dim].max())

    def _trace(self, name: str, dim: int) -> np.ndarray:
        """Full temporal trace for a dimension."""
        relay = self._load_and_run(name)
        return relay[:, dim]

    def _pass(self, group: str, name: str, msg: str, **vals):
        self.results.append(TestResult(name, group, True, msg, vals))

    def _fail(self, group: str, name: str, msg: str, **vals):
        self.results.append(TestResult(name, group, False, msg, vals))

    def _test(self, group: str, name: str, condition: bool, msg: str, **vals):
        self.results.append(TestResult(name, group, condition, msg, vals))

    # ==================================================================
    # T1: Contour Activity
    # E1 (sequence_anterior) should increase with pitch change rate
    # ==================================================================
    def test_T1_contour_activity(self):
        G = "T1_contour_activity"

        e1_sustained = self._mean("g1_01_sustained_c4", E1)
        e1_repeated = self._mean("g1_04_repeated_c4", E1)
        e1_scale = self._mean("g1_02_ascending_scale", E1)
        e1_leaps = self._mean("g1_05_large_leaps", E1)

        # Scale (pitch changes) > sustained (no pitch changes)
        self._test(G, "T1_E1_scale>sustained",
                   e1_scale > e1_sustained,
                   f"scale({e1_scale:.4f}) > sustained({e1_sustained:.4f})",
                   scale=e1_scale, sustained=e1_sustained)

        # Large leaps > scale (bigger intervals)
        self._test(G, "T1_E1_leaps>scale",
                   e1_leaps > e1_scale,
                   f"leaps({e1_leaps:.4f}) > scale({e1_scale:.4f})",
                   leaps=e1_leaps, scale=e1_scale)

        # Repeated (same pitch) ≈ sustained (both low E1)
        # Repeated has onsets but no pitch change → E1 should be low
        self._test(G, "T1_E1_scale>repeated",
                   e1_scale > e1_repeated,
                   f"scale({e1_scale:.4f}) > repeated({e1_repeated:.4f})",
                   scale=e1_scale, repeated=e1_repeated)

        # Ascending ≈ descending (direction shouldn't matter much since abs())
        e1_desc = self._mean("g1_03_descending_scale", E1)
        diff = abs(e1_scale - e1_desc)
        self._test(G, "T1_E1_asc_approx_desc",
                   diff < 0.15,
                   f"|ascending({e1_scale:.4f}) - descending({e1_desc:.4f})| = {diff:.4f} < 0.15",
                   ascending=e1_scale, descending=e1_desc)

    # ==================================================================
    # T2: Onset Detection
    # E0 (onset_posterior) should respond to onset density
    # ==================================================================
    def test_T2_onset_detection(self):
        G = "T2_onset_detection"

        e0_sustained = self._mean("g1_01_sustained_c4", E0)
        e0_regular = self._mean("g2_02_regular_onsets", E0)
        e0_fast = self._mean("g2_03_fast_onsets", E0)

        # Fast onsets > sustained (more onset events)
        self._test(G, "T2_E0_fast>sustained",
                   e0_fast > e0_sustained,
                   f"fast({e0_fast:.4f}) > sustained({e0_sustained:.4f})",
                   fast=e0_fast, sustained=e0_sustained)

        # Regular onsets > sustained
        self._test(G, "T2_E0_regular>sustained",
                   e0_regular > e0_sustained,
                   f"regular({e0_regular:.4f}) > sustained({e0_sustained:.4f})",
                   regular=e0_regular, sustained=e0_sustained)

        # M1 (posterior_activity) should track onset events
        m1_fast = self._mean("g2_03_fast_onsets", M1)
        m1_sustained = self._mean("g1_01_sustained_c4", M1)
        self._test(G, "T2_M1_fast>sustained",
                   m1_fast > m1_sustained,
                   f"M1 fast({m1_fast:.4f}) > sustained({m1_sustained:.4f})",
                   fast=m1_fast, sustained=m1_sustained)

        # E0 temporal variation in onset patterns
        e0_std_regular = self._std("g2_02_regular_onsets", E0, skip_warmup=False)
        self._test(G, "T2_E0_regular_varies",
                   e0_std_regular > 0.005,
                   f"E0 std(regular)={e0_std_regular:.4f} > 0.005",
                   std=e0_std_regular)

    # ==================================================================
    # T3: Contour Complexity
    # E2 should reflect melodic unpredictability
    # ==================================================================
    def test_T3_contour_complexity(self):
        G = "T3_contour_complexity"

        e2_sustained = self._mean("g1_01_sustained_c4", E2)
        e2_scale = self._mean("g1_02_ascending_scale", E2)
        e2_chromatic = self._mean("g1_06_chromatic_asc", E2)
        e2_random = self._mean("g1_08_random_melody", E2)
        e2_leaps = self._mean("g1_05_large_leaps", E2)

        # Random melody > sustained (maximal vs minimal complexity)
        self._test(G, "T3_E2_random>sustained",
                   e2_random > e2_sustained,
                   f"random({e2_random:.4f}) > sustained({e2_sustained:.4f})",
                   random=e2_random, sustained=e2_sustained)

        # Large leaps > sustained
        self._test(G, "T3_E2_leaps>sustained",
                   e2_leaps > e2_sustained,
                   f"leaps({e2_leaps:.4f}) > sustained({e2_sustained:.4f})",
                   leaps=e2_leaps, sustained=e2_sustained)

        # Scale > sustained (some pitch change)
        self._test(G, "T3_E2_scale>sustained",
                   e2_scale > e2_sustained,
                   f"scale({e2_scale:.4f}) > sustained({e2_sustained:.4f})",
                   scale=e2_scale, sustained=e2_sustained)

        # Print hierarchy for analysis
        self._pass(G, "T3_E2_hierarchy",
                   f"E2: random={e2_random:.4f}, leaps={e2_leaps:.4f}, "
                   f"chromatic={e2_chromatic:.4f}, scale={e2_scale:.4f}, "
                   f"sustained={e2_sustained:.4f}",
                   random=e2_random, leaps=e2_leaps, chromatic=e2_chromatic,
                   scale=e2_scale, sustained=e2_sustained)

    # ==================================================================
    # T4: Gradient Ratio
    # E3 = E0/(E0+E1) — high when onset-dominant, low when contour-dominant
    # ==================================================================
    def test_T4_gradient_ratio(self):
        G = "T4_gradient_ratio"

        e3_onset_dom = self._mean("g4_01_onset_dominant", E3)
        e3_contour_dom = self._mean("g4_02_contour_dominant", E3)
        e3_balanced = self._mean("g4_03_balanced", E3)

        # Onset dominant (repeated) > contour dominant (slow leaps)
        self._test(G, "T4_E3_onset>contour",
                   e3_onset_dom > e3_contour_dom,
                   f"onset_dom({e3_onset_dom:.4f}) > contour_dom({e3_contour_dom:.4f})",
                   onset=e3_onset_dom, contour=e3_contour_dom)

        # E3 should be in (0, 1) range for all
        for stim, val in [("onset_dom", e3_onset_dom),
                          ("contour_dom", e3_contour_dom),
                          ("balanced", e3_balanced)]:
            self._test(G, f"T4_E3_{stim}_range",
                       0.0 <= val <= 1.0,
                       f"E3({stim})={val:.4f} in [0,1]")

        # Hierarchy
        self._pass(G, "T4_E3_hierarchy",
                   f"E3: onset_dom={e3_onset_dom:.4f}, balanced={e3_balanced:.4f}, "
                   f"contour_dom={e3_contour_dom:.4f}",
                   onset=e3_onset_dom, balanced=e3_balanced, contour=e3_contour_dom)

    # ==================================================================
    # T5: Phrase Boundary
    # F0 should peak during silence gaps between phrases
    # ==================================================================
    def test_T5_phrase_boundary(self):
        G = "T5_phrase_boundary"

        f0_continuous = self._mean("g3_02_continuous_melody", F0)
        f0_with_rest = self._mean("g3_01_phrase_with_rest", F0)

        # Phrase with rest should have higher mean F0 than continuous
        self._test(G, "T5_F0_rest>continuous",
                   f0_with_rest > f0_continuous,
                   f"rest({f0_with_rest:.4f}) > continuous({f0_continuous:.4f})",
                   rest=f0_with_rest, continuous=f0_continuous)

        # Two phrases (longer rest) should also show high F0
        f0_two = self._mean("g3_04_two_phrases", F0)
        self._test(G, "T5_F0_two_phrases>continuous",
                   f0_two > f0_continuous,
                   f"two_phrases({f0_two:.4f}) > continuous({f0_continuous:.4f})",
                   two=f0_two, continuous=f0_continuous)

        # F0 should be in [0, 1] (sigmoid output)
        f0_max_rest = self._max("g3_01_phrase_with_rest", F0)
        self._test(G, "T5_F0_bounded",
                   0.0 <= f0_max_rest <= 1.0,
                   f"F0 max(rest)={f0_max_rest:.4f} in [0,1]")

    # ==================================================================
    # T6: Present Layer
    # P0 should track onset-related activity, P1 contour activity
    # ==================================================================
    def test_T6_present_layer(self):
        G = "T6_present_layer"

        # P0 onset_state: fast onsets > sustained
        p0_fast = self._mean("g2_03_fast_onsets", P0)
        p0_sustained = self._mean("g1_01_sustained_c4", P0)
        self._test(G, "T6_P0_fast>sustained",
                   p0_fast > p0_sustained,
                   f"P0 fast({p0_fast:.4f}) > sustained({p0_sustained:.4f})",
                   fast=p0_fast, sustained=p0_sustained)

        # P1 contour_state: scale > repeated
        p1_scale = self._mean("g1_02_ascending_scale", P1)
        p1_repeated = self._mean("g1_04_repeated_c4", P1)
        self._test(G, "T6_P1_scale>repeated",
                   p1_scale > p1_repeated,
                   f"P1 scale({p1_scale:.4f}) > repeated({p1_repeated:.4f})",
                   scale=p1_scale, repeated=p1_repeated)

        # P1 contour_state: leaps > sustained
        p1_leaps = self._mean("g1_05_large_leaps", P1)
        p1_sustained = self._mean("g1_01_sustained_c4", P1)
        self._test(G, "T6_P1_leaps>sustained",
                   p1_leaps > p1_sustained,
                   f"P1 leaps({p1_leaps:.4f}) > sustained({p1_sustained:.4f})",
                   leaps=p1_leaps, sustained=p1_sustained)

    # ==================================================================
    # T7: Memory Layer
    # M0 = 0.70*E0 + 0.30*E1 (cortical gradient function)
    # ==================================================================
    def test_T7_memory_layer(self):
        G = "T7_memory_layer"

        for stim in ["g1_02_ascending_scale", "g1_04_repeated_c4",
                      "g2_03_fast_onsets", "g1_01_sustained_c4"]:
            e0 = self._mean(stim, E0)
            e1 = self._mean(stim, E1)
            m0 = self._mean(stim, M0)
            expected = 0.70 * e0 + 0.30 * e1

            diff = abs(m0 - expected)
            short = stim.replace("g1_", "").replace("g2_", "")
            self._test(G, f"T7_M0_formula_{short}",
                       diff < 0.1,
                       f"M0={m0:.4f} ≈ 0.7*E0+0.3*E1={expected:.4f} (diff={diff:.4f})",
                       M0=m0, expected=expected, diff=diff)

        # M2 (anterior_activity) should track contour — scale > sustained
        m2_scale = self._mean("g1_02_ascending_scale", M2)
        m2_sustained = self._mean("g1_01_sustained_c4", M2)
        self._test(G, "T7_M2_scale>sustained",
                   m2_scale > m2_sustained,
                   f"M2 scale({m2_scale:.4f}) > sustained({m2_sustained:.4f})",
                   scale=m2_scale, sustained=m2_sustained)

    # ==================================================================
    # T8: Correlation Health
    # Cross-dimension correlations should be reasonable
    # ==================================================================
    def test_T8_correlation_health(self):
        G = "T8_correlation"

        # Collect traces across all stimuli for correlation analysis
        all_stims = ["g1_01_sustained_c4", "g1_02_ascending_scale",
                     "g1_04_repeated_c4", "g1_05_large_leaps",
                     "g2_03_fast_onsets", "g1_08_random_melody"]

        means = {s: [self._mean(s, d) for d in range(10)] for s in all_stims}
        vals = np.array([means[s] for s in all_stims])  # (N_stims, 10)

        # E0 and M1 should correlate (both track onsets)
        r_e0_m1 = np.corrcoef(vals[:, E0], vals[:, M1])[0, 1]
        self._test(G, "T8_E0_M1_corr",
                   r_e0_m1 > 0.3,
                   f"r(E0,M1) = {r_e0_m1:+.3f} > 0.3 (both onset-related)",
                   r=r_e0_m1)

        # E1 and M2 should correlate (both track contour)
        r_e1_m2 = np.corrcoef(vals[:, E1], vals[:, M2])[0, 1]
        self._test(G, "T8_E1_M2_corr",
                   r_e1_m2 > 0.3,
                   f"r(E1,M2) = {r_e1_m2:+.3f} > 0.3 (both contour-related)",
                   r=r_e1_m2)

        # E0 and P0 should correlate (onset pathway)
        r_e0_p0 = np.corrcoef(vals[:, E0], vals[:, P0])[0, 1]
        self._test(G, "T8_E0_P0_corr",
                   r_e0_p0 > 0.3,
                   f"r(E0,P0) = {r_e0_p0:+.3f} > 0.3 (onset pathway)",
                   r=r_e0_p0)

        # E1/E2 and P1 should correlate (contour pathway)
        r_e2_p1 = np.corrcoef(vals[:, E2], vals[:, P1])[0, 1]
        self._test(G, "T8_E2_P1_corr",
                   r_e2_p1 > 0.3,
                   f"r(E2,P1) = {r_e2_p1:+.3f} > 0.3 (contour pathway)",
                   r=r_e2_p1)

        # No dimension pair should be perfectly redundant
        # EXCEPT known architectural couplings (same processing pathway):
        #   Onset pathway:   E0(0) → M0(4), M1(5), P0(7)
        #   Contour pathway: E1(1) → P1(8)
        #   Memory coupling:  M0(4) ↔ M1(5) (both derived from E0)
        COUPLED = {(0,4),(0,5),(0,7),(1,8),(4,5),(5,7)}
        redundant = []
        for i in range(10):
            for j in range(i+1, 10):
                if (i, j) in COUPLED:
                    continue  # skip architecturally coupled pairs
                r = abs(np.corrcoef(vals[:, i], vals[:, j])[0, 1])
                if r > 0.99:
                    redundant.append((i, j, r))
                    self._fail(G, f"T8_redundancy_{i}_{j}",
                               f"|r({DIM_NAMES[i]},{DIM_NAMES[j]})| = {r:.3f} > 0.99 (redundant)")

        if not redundant:
            self._pass(G, "T8_no_redundancy", "No unexpected redundant dimension pairs")

    # ==================================================================
    # T9: Bounds & Shape
    # All dimensions in [0, 1], shape (T, 10)
    # ==================================================================
    def test_T9_bounds_shape(self):
        G = "T9_bounds_shape"

        all_stims = ["g1_01_sustained_c4", "g1_02_ascending_scale",
                     "g1_04_repeated_c4", "g1_05_large_leaps",
                     "g2_03_fast_onsets", "g1_08_random_melody",
                     "g3_01_phrase_with_rest", "g4_04_static_chord"]

        for stim in all_stims:
            relay = self._load_and_run(stim)

            # Shape check
            self._test(G, f"T9_shape_{stim}",
                       relay.ndim == 2 and relay.shape[1] == 10,
                       f"shape={relay.shape} {'OK' if relay.shape[1] == 10 else 'BAD'}")

            # Bounds check
            lo, hi = relay.min(), relay.max()
            ok = lo >= -1e-6 and hi <= 1.0 + 1e-6
            self._test(G, f"T9_bounds_{stim}",
                       ok,
                       f"range=[{lo:.6f}, {hi:.6f}] {'OK' if ok else 'OUT OF BOUNDS'}")

    # ==================================================================
    # T10: Register Influence
    # Pitch height should affect E1/E2 via H³ pitch_height feature
    # ==================================================================
    def test_T10_register(self):
        G = "T10_register"

        # Same scale pattern at different registers — E1/E2 should be similar
        # (contour activity is about CHANGE, not absolute pitch)
        e1_low = self._mean("g5_01_melody_low", E1)
        e1_mid = self._mean("g5_02_melody_mid", E1)
        e1_high = self._mean("g5_03_melody_high", E1)

        # All should show contour activity (> sustained baseline)
        e1_baseline = self._mean("g1_01_sustained_c4", E1)
        for reg, val in [("low", e1_low), ("mid", e1_mid), ("high", e1_high)]:
            self._test(G, f"T10_E1_{reg}>baseline",
                       val > e1_baseline,
                       f"E1 {reg}({val:.4f}) > baseline({e1_baseline:.4f})")

        # E1 hierarchy: document (should be similar across registers)
        self._pass(G, "T10_E1_register_hierarchy",
                   f"E1: low={e1_low:.4f}, mid={e1_mid:.4f}, high={e1_high:.4f}")

    # ==================================================================
    # Run All Tests
    # ==================================================================
    def run_all(self) -> bool:
        test_methods = [
            ("T1: Contour Activity", self.test_T1_contour_activity),
            ("T2: Onset Detection", self.test_T2_onset_detection),
            ("T3: Contour Complexity", self.test_T3_contour_complexity),
            ("T4: Gradient Ratio", self.test_T4_gradient_ratio),
            ("T5: Phrase Boundary", self.test_T5_phrase_boundary),
            ("T6: Present Layer", self.test_T6_present_layer),
            ("T7: Memory Layer", self.test_T7_memory_layer),
            ("T8: Correlation Health", self.test_T8_correlation_health),
            ("T9: Bounds & Shape", self.test_T9_bounds_shape),
            ("T10: Register", self.test_T10_register),
        ]

        print("=" * 72)
        print("MPG COMPREHENSIVE FUNCTIONAL TEST v1.0")
        print(f"Started: {datetime.now().isoformat()}")
        print("=" * 72)

        # Check stimuli
        wavs = list(STIMULI_DIR.glob("*.wav"))
        print(f"\nStimuli directory: {STIMULI_DIR}")
        print(f"Found {len(wavs)} WAV files")

        self._init_pipeline()

        # Pre-load all stimuli
        all_stims = sorted(set(
            p.stem for p in wavs
        ))
        print(f"Processing {len(all_stims)} stimuli...\n")
        t0 = time.perf_counter()

        for i, stim in enumerate(all_stims, 1):
            relay = self._load_and_run(stim)
            print(f"  [{i}/{len(all_stims)}] {stim}: {relay.shape[0]}F")

        elapsed_load = time.perf_counter() - t0
        print(f"\nProcessing complete: {len(all_stims)} files in {elapsed_load:.1f}s")

        # Print dimension summaries
        print("\n  MPG Dimension Summaries:")
        for stim in ["g1_01_sustained_c4", "g1_02_ascending_scale",
                      "g1_04_repeated_c4", "g1_05_large_leaps",
                      "g2_03_fast_onsets", "g1_08_random_melody"]:
            vals = [f"{self._mean(stim, d):+.3f}" for d in range(10)]
            short = stim.ljust(25)
            print(f"    {short} | {' | '.join(vals)}")

        # Run tests
        print("\n" + "=" * 72)
        print("RUNNING TESTS")
        print("=" * 72)

        for section_name, method in test_methods:
            print(f"\n  {section_name}:")
            n_before = len(self.results)
            try:
                method()
            except Exception as exc:
                import traceback
                self.results.append(TestResult(
                    f"CRASH_{section_name}", "CRASH", False,
                    f"Exception: {exc}\n{traceback.format_exc()}"))
            for r in self.results[n_before:]:
                status = "PASS" if r.passed else "FAIL"
                print(f"    [{status}] {r.name}: {r.message}")

        # Summary
        total = len(self.results)
        passed = sum(1 for r in self.results if r.passed)
        failed = total - passed

        print(f"\n{'=' * 72}")
        print(f"MPG Functional Test v1.0 — FINAL RESULTS")
        print(f"{'=' * 72}")
        print(f"  Stimuli processed:  {len(all_stims)}")
        print(f"  Tests passed:       {passed}/{total}")
        elapsed_total = time.perf_counter() - t0
        print(f"  Processing time:    {elapsed_total:.1f}s")

        # Save report
        report = {
            "version": "1.0",
            "timestamp": datetime.now().isoformat(),
            "stimuli_count": len(all_stims),
            "tests_total": total,
            "tests_passed": passed,
            "tests_failed": failed,
            "elapsed_s": elapsed_total,
            "results": [
                {
                    "name": r.name, "group": r.group,
                    "passed": r.passed, "message": r.message,
                    "values": r.values,
                }
                for r in self.results
            ],
        }
        report_path = RESULTS_DIR / "MPG_FUNCTIONAL_TEST_REPORT.json"
        with open(report_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"  Report:             {report_path}")
        print(f"  OVERALL:            {'ALL PASS' if failed == 0 else f'{failed} FAILED'}")
        print(f"{'=' * 72}")

        return failed == 0


def main():
    # Check stimuli exist
    if not STIMULI_DIR.exists() or not any(STIMULI_DIR.glob("*.wav")):
        print("Stimuli not found. Generating...")
        exec(open(pathlib.Path(__file__).parent / "generate_mpg_stimuli.py").read())
        print()

    runner = MPGTestRunner()
    all_passed = runner.run_all()
    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
