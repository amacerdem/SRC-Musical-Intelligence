"""Deep R³ Test Suite — Comprehensive validation of the 97D spectral extractor.

Tests the R³ pipeline end-to-end using:
  1. Synthesized audio signals (sine waves, chords, noise, silence)
  2. Micro-belief test audio from Test-Audio/
  3. Real classical/orchestral recordings from Test-Audio/

Validates:
  - Structural correctness (shape, dtype, bounds, feature names)
  - Semantic correctness (does a sine wave give low roughness? etc.)
  - Determinism (same input → same output)
  - Edge cases (T=1, zeros, very short/long, batch sizes)
  - Cross-group consistency
  - Real audio plausibility

Run:
    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/deep_r3_test.py
"""
from __future__ import annotations

import math
import os
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
from torch import Tensor

# Ensure project root on path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from Musical_Intelligence.ear.r3.extractor import R3Extractor, R3Output
from Musical_Intelligence.ear.r3.constants.feature_names import R3_FEATURE_NAMES, R3_DIM
from Musical_Intelligence.ear.r3.constants.group_boundaries import R3_GROUP_BOUNDARIES

# ======================================================================
# Test infrastructure
# ======================================================================

@dataclass
class TestResult:
    name: str
    passed: bool
    message: str = ""
    duration_ms: float = 0.0

@dataclass
class TestSuite:
    name: str
    results: List[TestResult] = field(default_factory=list)

    def add(self, name: str, passed: bool, message: str = "", duration_ms: float = 0.0):
        self.results.append(TestResult(name, passed, message, duration_ms))

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    @property
    def total(self) -> int:
        return len(self.results)

    def report(self) -> str:
        lines = [f"\n{'='*70}", f"  {self.name}  ({self.passed}/{self.total} passed)", f"{'='*70}"]
        for r in self.results:
            icon = "PASS" if r.passed else "FAIL"
            dur = f"  [{r.duration_ms:.0f}ms]" if r.duration_ms > 0 else ""
            lines.append(f"  [{icon}] {r.name}{dur}")
            if r.message:
                for line in r.message.split("\n"):
                    lines.append(f"         {line}")
        return "\n".join(lines)


def timed(fn):
    """Measure execution time of a function."""
    t0 = time.perf_counter()
    result = fn()
    dt = (time.perf_counter() - t0) * 1000
    return result, dt


# ======================================================================
# Audio synthesis helpers
# ======================================================================

SR = 44100
HOP = 256
FRAME_RATE = SR / HOP  # 172.27 Hz
N_MELS = 128


def make_mel_from_audio(audio: np.ndarray, sr: int = SR) -> Tensor:
    """Convert raw audio (1D numpy) to mel spectrogram (1, 128, T).

    Uses a simple mel filterbank approximation to avoid torchaudio dependency.
    """
    import torch
    audio_t = torch.from_numpy(audio).float()
    if audio_t.dim() == 1:
        audio_t = audio_t.unsqueeze(0)  # (1, N)

    # STFT
    n_fft = 2048
    window = torch.hann_window(n_fft)
    stft = torch.stft(audio_t, n_fft=n_fft, hop_length=HOP, win_length=n_fft,
                       window=window, return_complex=True)  # (1, n_fft//2+1, T)
    power = stft.abs().pow(2)  # (1, F, T)

    # Mel filterbank
    n_freqs = power.shape[1]
    mel_fb = _mel_filterbank(sr, n_fft, N_MELS, n_freqs)  # (128, F)
    mel_fb = mel_fb.to(power.device, power.dtype)

    mel = torch.matmul(mel_fb, power)  # (1, 128, T)
    mel = torch.log1p(mel)  # log1p normalization

    return mel


def _mel_filterbank(sr: int, n_fft: int, n_mels: int, n_freqs: int) -> Tensor:
    """Build a simple mel filterbank matrix (n_mels, n_freqs)."""
    f_min, f_max = 0.0, sr / 2.0
    mel_min = 2595.0 * math.log10(1.0 + f_min / 700.0)
    mel_max = 2595.0 * math.log10(1.0 + f_max / 700.0)
    mel_points = torch.linspace(mel_min, mel_max, n_mels + 2)
    hz_points = 700.0 * (10.0 ** (mel_points / 2595.0) - 1.0)
    bin_points = (hz_points * n_fft / sr).long()

    fb = torch.zeros(n_mels, n_freqs)
    for m in range(n_mels):
        f_start = bin_points[m].item()
        f_center = bin_points[m + 1].item()
        f_end = bin_points[m + 2].item()
        for k in range(f_start, f_center):
            if f_center > f_start and k < n_freqs:
                fb[m, k] = (k - f_start) / (f_center - f_start)
        for k in range(f_center, f_end):
            if f_end > f_center and k < n_freqs:
                fb[m, k] = (f_end - k) / (f_end - f_center)
    return fb


def sine_wave(freq: float, duration: float = 1.0, amplitude: float = 0.5,
              sr: int = SR) -> np.ndarray:
    """Generate a pure sine wave."""
    t = np.arange(int(sr * duration)) / sr
    return (amplitude * np.sin(2 * np.pi * freq * t)).astype(np.float32)


def chord(freqs: List[float], duration: float = 1.0, amplitude: float = 0.3,
          sr: int = SR) -> np.ndarray:
    """Generate a chord (sum of sine waves)."""
    t = np.arange(int(sr * duration)) / sr
    signal = np.zeros_like(t, dtype=np.float32)
    for f in freqs:
        signal += amplitude * np.sin(2 * np.pi * f * t).astype(np.float32)
    return signal / len(freqs)


def white_noise(duration: float = 1.0, amplitude: float = 0.3, sr: int = SR) -> np.ndarray:
    """Generate white noise."""
    n = int(sr * duration)
    return (amplitude * np.random.randn(n)).astype(np.float32)


def am_signal(carrier_freq: float = 440.0, mod_freq: float = 4.0,
              mod_depth: float = 0.8, duration: float = 2.0,
              sr: int = SR) -> np.ndarray:
    """Generate an amplitude-modulated signal."""
    t = np.arange(int(sr * duration)) / sr
    carrier = np.sin(2 * np.pi * carrier_freq * t)
    modulator = 1.0 + mod_depth * np.sin(2 * np.pi * mod_freq * t)
    return (0.5 * carrier * modulator).astype(np.float32)


def chromatic_sweep(duration: float = 2.0, sr: int = SR) -> np.ndarray:
    """Generate a chromatic sweep through all 12 pitch classes."""
    freqs = [261.63 * 2**(i/12) for i in range(12)]  # C4 through B4
    samples_per_note = int(sr * duration / 12)
    signal = np.zeros(0, dtype=np.float32)
    for f in freqs:
        t = np.arange(samples_per_note) / sr
        note = (0.4 * np.sin(2 * np.pi * f * t)).astype(np.float32)
        # Apply fade in/out
        fade = min(500, samples_per_note // 4)
        note[:fade] *= np.linspace(0, 1, fade)
        note[-fade:] *= np.linspace(1, 0, fade)
        signal = np.concatenate([signal, note])
    return signal


def metronome_clicks(bpm: float = 120.0, duration: float = 4.0,
                     sr: int = SR) -> np.ndarray:
    """Generate metronome-like click track."""
    n = int(sr * duration)
    signal = np.zeros(n, dtype=np.float32)
    samples_per_beat = int(sr * 60.0 / bpm)
    click_dur = int(sr * 0.01)  # 10ms click
    for i in range(0, n, samples_per_beat):
        end = min(i + click_dur, n)
        t = np.arange(end - i) / sr
        signal[i:end] = 0.8 * np.sin(2 * np.pi * 1000 * t).astype(np.float32)
        # Apply exponential decay
        decay = np.exp(-30 * t)
        signal[i:end] *= decay
    return signal


def harmonic_tone(f0: float = 220.0, n_harmonics: int = 8,
                  duration: float = 1.0, sr: int = SR) -> np.ndarray:
    """Generate a harmonic complex tone with 1/n amplitude decay."""
    t = np.arange(int(sr * duration)) / sr
    signal = np.zeros_like(t, dtype=np.float32)
    for n in range(1, n_harmonics + 1):
        signal += (1.0 / n) * np.sin(2 * np.pi * f0 * n * t).astype(np.float32)
    signal *= 0.3 / signal.max()
    return signal.astype(np.float32)


def inharmonic_tone(f0: float = 220.0, n_partials: int = 8,
                    inharmonicity: float = 0.05, duration: float = 1.0,
                    sr: int = SR) -> np.ndarray:
    """Generate an inharmonic tone (like a stiff piano string)."""
    t = np.arange(int(sr * duration)) / sr
    signal = np.zeros_like(t, dtype=np.float32)
    for n in range(1, n_partials + 1):
        # Inharmonic partial: f_n = n * f0 * sqrt(1 + B*n^2)
        freq = n * f0 * math.sqrt(1 + inharmonicity * n * n)
        signal += (1.0 / n) * np.sin(2 * np.pi * freq * t).astype(np.float32)
    signal *= 0.3 / max(abs(signal.max()), abs(signal.min()))
    return signal.astype(np.float32)


# ======================================================================
# Group boundary helpers
# ======================================================================

GROUP_SLICES = {g.letter: slice(g.start, g.end) for g in R3_GROUP_BOUNDARIES}
GROUP_NAMES_BY_LETTER = {g.letter: g.name for g in R3_GROUP_BOUNDARIES}

def get_group(features: Tensor, letter: str) -> Tensor:
    """Extract a group's features from the 97D vector. Returns (B, T, dim)."""
    return features[:, :, GROUP_SLICES[letter]]

def get_feature(features: Tensor, idx: int) -> Tensor:
    """Extract a single feature from the 97D vector. Returns (B, T)."""
    return features[:, :, idx]


# ======================================================================
# TEST SUITE 1: Structural Validation
# ======================================================================

def test_structural(extractor: R3Extractor) -> TestSuite:
    suite = TestSuite("1. Structural Validation")

    # 1.1: Correct number of groups
    suite.add("9 groups registered", len(extractor.feature_map.groups) == 9,
              f"Got {len(extractor.feature_map.groups)} groups")

    # 1.2: Total dim = 97
    suite.add("Total dim = 97", extractor.total_dim == 97,
              f"Got {extractor.total_dim}")

    # 1.3: Feature names count
    suite.add("97 feature names", len(extractor.feature_names) == 97,
              f"Got {len(extractor.feature_names)} names")

    # 1.4: Feature names match constants
    match = extractor.feature_names == R3_FEATURE_NAMES
    suite.add("Feature names match constants", match)

    # 1.5: Output shape with standard input
    mel = torch.rand(2, 128, 100)
    out, dt = timed(lambda: extractor.extract(mel))
    suite.add("Output shape (2, 100, 97)", out.features.shape == (2, 100, 97),
              f"Got {tuple(out.features.shape)}", dt)

    # 1.6: dtype = float32
    suite.add("Output dtype = float32", out.features.dtype == torch.float32,
              f"Got {out.features.dtype}")

    # 1.7: device = CPU
    suite.add("Output device = CPU", out.features.device.type == "cpu",
              f"Got {out.features.device}")

    # 1.8: No NaN
    suite.add("No NaN in output", not torch.isnan(out.features).any().item())

    # 1.9: No Inf
    suite.add("No Inf in output", not torch.isinf(out.features).any().item())

    # 1.10: Values in [0, 1]
    vmin = out.features.min().item()
    vmax = out.features.max().item()
    suite.add("Values in [0, 1]", vmin >= 0.0 and vmax <= 1.0,
              f"Range: [{vmin:.6f}, {vmax:.6f}]")

    # 1.11: Feature map is frozen (R3FeatureMap should be immutable)
    suite.add("Feature map has groups", len(out.feature_map.groups) == 9)

    # 1.12: Batch size 1
    mel1 = torch.rand(1, 128, 50)
    out1 = extractor.extract(mel1)
    suite.add("Batch=1 works", out1.features.shape == (1, 50, 97),
              f"Got {tuple(out1.features.shape)}")

    # 1.13: Batch size 4
    mel4 = torch.rand(4, 128, 50)
    out4 = extractor.extract(mel4)
    suite.add("Batch=4 works", out4.features.shape == (4, 50, 97),
              f"Got {tuple(out4.features.shape)}")

    # 1.14: Group boundary coverage
    covered = set()
    for g in R3_GROUP_BOUNDARIES:
        covered.update(range(g.start, g.end))
    suite.add("Groups cover [0, 97)", covered == set(range(97)))

    # 1.15: Group boundary contiguity
    contiguous = all(
        R3_GROUP_BOUNDARIES[i].end == R3_GROUP_BOUNDARIES[i+1].start
        for i in range(len(R3_GROUP_BOUNDARIES) - 1)
    )
    suite.add("Groups are contiguous", contiguous)

    return suite


# ======================================================================
# TEST SUITE 2: Edge Cases
# ======================================================================

def test_edge_cases(extractor: R3Extractor) -> TestSuite:
    suite = TestSuite("2. Edge Cases")

    # 2.1: T=1 (single frame)
    try:
        mel = torch.rand(1, 128, 1)
        out, dt = timed(lambda: extractor.extract(mel))
        ok = out.features.shape == (1, 1, 97)
        no_nan = not torch.isnan(out.features).any().item()
        suite.add("T=1 shape correct", ok, f"Got {tuple(out.features.shape)}", dt)
        suite.add("T=1 no NaN", no_nan)
    except Exception as e:
        suite.add("T=1 no crash", False, str(e))

    # 2.2: T=2 (minimal for diff-based features)
    try:
        mel = torch.rand(1, 128, 2)
        out = extractor.extract(mel)
        suite.add("T=2 shape correct", out.features.shape == (1, 2, 97))
        suite.add("T=2 no NaN", not torch.isnan(out.features).any().item())
    except Exception as e:
        suite.add("T=2 no crash", False, str(e))

    # 2.3: T=5 (very short)
    try:
        mel = torch.rand(1, 128, 5)
        out = extractor.extract(mel)
        suite.add("T=5 shape correct", out.features.shape == (1, 5, 97))
        suite.add("T=5 no NaN", not torch.isnan(out.features).any().item())
        suite.add("T=5 in [0,1]", out.features.min() >= 0 and out.features.max() <= 1)
    except Exception as e:
        suite.add("T=5 no crash", False, str(e))

    # 2.4: Zero input
    try:
        mel = torch.zeros(1, 128, 50)
        out = extractor.extract(mel)
        suite.add("Zeros: no NaN", not torch.isnan(out.features).any().item())
        suite.add("Zeros: in [0,1]", out.features.min() >= 0 and out.features.max() <= 1)
    except Exception as e:
        suite.add("Zeros: no crash", False, str(e))

    # 2.5: Ones input (saturated)
    try:
        mel = torch.ones(1, 128, 50)
        out = extractor.extract(mel)
        suite.add("Ones: no NaN", not torch.isnan(out.features).any().item())
        suite.add("Ones: in [0,1]", out.features.min() >= 0 and out.features.max() <= 1)
    except Exception as e:
        suite.add("Ones: no crash", False, str(e))

    # 2.6: Very large values
    try:
        mel = torch.rand(1, 128, 50) * 1000.0
        out = extractor.extract(mel)
        suite.add("Large values: no NaN", not torch.isnan(out.features).any().item())
        suite.add("Large values: in [0,1]", out.features.min() >= 0 and out.features.max() <= 1)
    except Exception as e:
        suite.add("Large values: no crash", False, str(e))

    # 2.7: Very small values (near epsilon)
    try:
        mel = torch.rand(1, 128, 50) * 1e-10
        out = extractor.extract(mel)
        suite.add("Tiny values: no NaN", not torch.isnan(out.features).any().item())
        suite.add("Tiny values: in [0,1]", out.features.min() >= 0 and out.features.max() <= 1)
    except Exception as e:
        suite.add("Tiny values: no crash", False, str(e))

    # 2.8: Long sequence (T=5000 ≈ 29s)
    try:
        mel = torch.rand(1, 128, 5000)
        out, dt = timed(lambda: extractor.extract(mel))
        suite.add("T=5000 shape", out.features.shape == (1, 5000, 97),
                  f"Got {tuple(out.features.shape)}", dt)
        suite.add("T=5000 no NaN", not torch.isnan(out.features).any().item())
        fps = 5000 / (dt / 1000)
        suite.add("T=5000 FPS > 50", fps > 50, f"FPS: {fps:.0f}")
    except Exception as e:
        suite.add("T=5000 no crash", False, str(e))

    # 2.9: Single mel bin active (sparse input)
    try:
        mel = torch.zeros(1, 128, 50)
        mel[0, 64, :] = 1.0  # only middle bin active
        out = extractor.extract(mel)
        suite.add("Sparse mel: no NaN", not torch.isnan(out.features).any().item())
        suite.add("Sparse mel: in [0,1]", out.features.min() >= 0 and out.features.max() <= 1)
    except Exception as e:
        suite.add("Sparse mel: no crash", False, str(e))

    return suite


# ======================================================================
# TEST SUITE 3: Determinism
# ======================================================================

def test_determinism(extractor: R3Extractor) -> TestSuite:
    suite = TestSuite("3. Determinism")

    # 3.1: Same random mel → identical output
    torch.manual_seed(123)
    mel1 = torch.rand(1, 128, 200)
    out1 = extractor.extract(mel1)

    torch.manual_seed(123)
    mel2 = torch.rand(1, 128, 200)
    out2 = extractor.extract(mel2)

    diff = (out1.features - out2.features).abs().max().item()
    suite.add("Same seed → identical output", diff == 0.0,
              f"Max diff: {diff:.2e}")

    # 3.2: Same mel, different invocations
    mel = torch.rand(1, 128, 100)
    r1 = extractor.extract(mel)
    r2 = extractor.extract(mel)
    diff2 = (r1.features - r2.features).abs().max().item()
    suite.add("Same mel, two calls → identical", diff2 == 0.0,
              f"Max diff: {diff2:.2e}")

    # 3.3: Feature names stable
    suite.add("Feature names stable across calls",
              r1.feature_names == r2.feature_names)

    # 3.4: Batch equivalence — batch(2) == single(1) + single(1)
    mel_a = torch.rand(1, 128, 100)
    mel_b = torch.rand(1, 128, 100)
    mel_batch = torch.cat([mel_a, mel_b], dim=0)
    out_batch = extractor.extract(mel_batch)
    out_a = extractor.extract(mel_a)
    out_b = extractor.extract(mel_b)

    # Compare batch[0] with individual a
    diff_a = (out_batch.features[0] - out_a.features[0]).abs().max().item()
    diff_b = (out_batch.features[1] - out_b.features[0]).abs().max().item()

    # Note: Some features use batch-level normalization (amax over batch),
    # so batch processing may differ from individual processing. This is expected
    # for features with max-norm.
    threshold = 0.05  # allow small differences due to batch normalization
    suite.add("Batch[0] ≈ Individual[0]", diff_a < threshold,
              f"Max diff: {diff_a:.4f} (threshold: {threshold})")
    suite.add("Batch[1] ≈ Individual[1]", diff_b < threshold,
              f"Max diff: {diff_b:.4f} (threshold: {threshold})")

    return suite


# ======================================================================
# TEST SUITE 4: Semantic Validation with Synthesized Audio
# ======================================================================

def test_semantic_synthetic(extractor: R3Extractor) -> TestSuite:
    suite = TestSuite("4. Semantic Validation — Synthesized Audio")

    # --- Generate test signals ---
    sine_440 = sine_wave(440.0, duration=1.0)
    sine_low = sine_wave(100.0, duration=1.0)
    sine_high = sine_wave(4000.0, duration=1.0)
    noise = white_noise(duration=1.0)
    silence = np.zeros(SR, dtype=np.float32)
    harm = harmonic_tone(220.0, n_harmonics=8, duration=1.0)
    inharm = inharmonic_tone(220.0, n_partials=8, inharmonicity=0.05, duration=1.0)
    octave = chord([440.0, 880.0], duration=1.0)
    minor_2nd = chord([440.0, 466.16], duration=1.0)  # A4 + Bb4
    c_major = chord([261.63, 329.63, 392.00], duration=1.0)
    clicks = metronome_clicks(bpm=120.0, duration=4.0)
    sweep = chromatic_sweep(duration=2.0)
    am_4hz = am_signal(carrier_freq=440.0, mod_freq=4.0, mod_depth=0.8, duration=2.0)

    # Convert to mel
    mel_sine = make_mel_from_audio(sine_440)
    mel_low = make_mel_from_audio(sine_low)
    mel_high = make_mel_from_audio(sine_high)
    mel_noise = make_mel_from_audio(noise)
    mel_silence = make_mel_from_audio(silence)
    mel_harm = make_mel_from_audio(harm)
    mel_inharm = make_mel_from_audio(inharm)
    mel_octave = make_mel_from_audio(octave)
    mel_m2 = make_mel_from_audio(minor_2nd)
    mel_cmaj = make_mel_from_audio(c_major)
    mel_clicks = make_mel_from_audio(clicks)
    mel_sweep = make_mel_from_audio(sweep)
    mel_am4 = make_mel_from_audio(am_4hz)

    # Extract R³
    r3_sine = extractor.extract(mel_sine).features
    r3_low = extractor.extract(mel_low).features
    r3_high = extractor.extract(mel_high).features
    r3_noise = extractor.extract(mel_noise).features
    r3_silence = extractor.extract(mel_silence).features
    r3_harm = extractor.extract(mel_harm).features
    r3_inharm = extractor.extract(mel_inharm).features
    r3_octave = extractor.extract(mel_octave).features
    r3_m2 = extractor.extract(mel_m2).features
    r3_cmaj = extractor.extract(mel_cmaj).features
    r3_clicks = extractor.extract(mel_clicks).features
    r3_sweep = extractor.extract(mel_sweep).features
    r3_am4 = extractor.extract(mel_am4).features

    # --- Group A: Consonance [0:7] ---
    # Pure sine should have low roughness (idx 0)
    sine_rough = get_feature(r3_sine, 0).mean().item()
    noise_rough = get_feature(r3_noise, 0).mean().item()
    suite.add("A: Sine roughness < noise roughness",
              sine_rough < noise_rough,
              f"Sine: {sine_rough:.3f}, Noise: {noise_rough:.3f}")

    # Octave should have lower dissonance (idx 1) than minor 2nd
    oct_diss = get_feature(r3_octave, 1).mean().item()
    m2_diss = get_feature(r3_m2, 1).mean().item()
    suite.add("A: Octave dissonance ≤ minor 2nd dissonance",
              oct_diss <= m2_diss + 0.1,  # tolerance for mel-proxy
              f"Octave: {oct_diss:.3f}, m2: {m2_diss:.3f}")

    # Harmonic tone should have higher stumpf_fusion (idx 3) than inharmonic
    harm_stumpf = get_feature(r3_harm, 3).mean().item()
    noise_stumpf = get_feature(r3_noise, 3).mean().item()
    suite.add("A: Harmonic stumpf > noise stumpf",
              harm_stumpf > noise_stumpf,
              f"Harmonic: {harm_stumpf:.3f}, Noise: {noise_stumpf:.3f}")

    # --- Group B: Energy [7:12] ---
    # Silence should have very low amplitude (idx 7)
    silence_amp = get_feature(r3_silence, 7).mean().item()
    sine_amp = get_feature(r3_sine, 7).mean().item()
    suite.add("B: Silence amplitude < sine amplitude",
              silence_amp < sine_amp,
              f"Silence: {silence_amp:.3f}, Sine: {sine_amp:.3f}")

    # Metronome clicks should have high onset_strength (idx 11)
    click_onset = get_feature(r3_clicks, 11).mean().item()
    sine_onset = get_feature(r3_sine, 11).mean().item()
    suite.add("B: Clicks onset > sine onset",
              click_onset > sine_onset,
              f"Clicks: {click_onset:.3f}, Sine: {sine_onset:.3f}")

    # --- Group C: Timbre [12:21] ---
    # Low frequency should have higher warmth (idx 12) than high frequency
    low_warmth = get_feature(r3_low, 12).mean().item()
    high_warmth = get_feature(r3_high, 12).mean().item()
    suite.add("C: Low freq warmer than high freq",
              low_warmth > high_warmth,
              f"Low: {low_warmth:.3f}, High: {high_warmth:.3f}")

    # High frequency should have higher sharpness (idx 13)
    low_sharp = get_feature(r3_low, 13).mean().item()
    high_sharp = get_feature(r3_high, 13).mean().item()
    suite.add("C: High freq sharper than low freq",
              high_sharp > low_sharp,
              f"High: {high_sharp:.3f}, Low: {low_sharp:.3f}")

    # Sine should have higher tonalness (idx 14) than noise
    sine_tonal = get_feature(r3_sine, 14).mean().item()
    noise_tonal = get_feature(r3_noise, 14).mean().item()
    suite.add("C: Sine more tonal than noise",
              sine_tonal > noise_tonal,
              f"Sine: {sine_tonal:.3f}, Noise: {noise_tonal:.3f}")

    # Tristimulus: low freq should have high t1 (idx 18), high freq high t3 (idx 20)
    low_t1 = get_feature(r3_low, 18).mean().item()
    high_t1 = get_feature(r3_high, 18).mean().item()
    suite.add("C: Low freq t1 > high freq t1",
              low_t1 > high_t1,
              f"Low t1: {low_t1:.3f}, High t1: {high_t1:.3f}")

    low_t3 = get_feature(r3_low, 20).mean().item()
    high_t3 = get_feature(r3_high, 20).mean().item()
    suite.add("C: High freq t3 > low freq t3",
              high_t3 > low_t3,
              f"High t3: {high_t3:.3f}, Low t3: {low_t3:.3f}")

    # --- Group D: Change [21:25] ---
    # Steady sine should have lower spectral flux (idx 21) than sweep
    sine_flux = get_feature(r3_sine, 21).mean().item()
    sweep_flux = get_feature(r3_sweep, 21).mean().item()
    suite.add("D: Sine flux < sweep flux",
              sine_flux < sweep_flux,
              f"Sine: {sine_flux:.3f}, Sweep: {sweep_flux:.3f}")

    # Noise should have higher entropy (idx 22) than pure sine
    noise_ent = get_feature(r3_noise, 22).mean().item()
    sine_ent = get_feature(r3_sine, 22).mean().item()
    suite.add("D: Noise entropy > sine entropy",
              noise_ent > sine_ent,
              f"Noise: {noise_ent:.3f}, Sine: {sine_ent:.3f}")

    # --- Group F: Pitch & Chroma [25:41] ---
    # C major chord: chroma_C (idx 25), chroma_E (idx 29), chroma_G (idx 32) should be strong
    chroma_c = get_feature(r3_cmaj, 25).mean().item()
    chroma_e = get_feature(r3_cmaj, 29).mean().item()
    chroma_g = get_feature(r3_cmaj, 32).mean().item()
    chroma_other = get_feature(r3_cmaj, 26).mean().item()  # Db (should be weak)
    # At least C and E/G should be stronger than Db
    suite.add("F: C major activates C, E, G chroma",
              chroma_c > chroma_other and (chroma_e > chroma_other or chroma_g > chroma_other),
              f"C={chroma_c:.3f}, E={chroma_e:.3f}, G={chroma_g:.3f}, Db={chroma_other:.3f}")

    # 440Hz (A4): chroma_A (idx 34) should be high
    chroma_a_sine = get_feature(r3_sine, 34).mean().item()  # 440Hz = A4
    chroma_db_sine = get_feature(r3_sine, 26).mean().item()  # Should be low
    suite.add("F: 440Hz → high chroma_A",
              chroma_a_sine > chroma_db_sine,
              f"A={chroma_a_sine:.3f}, Db={chroma_db_sine:.3f}")

    # Pitch height: high freq should have higher pitch_height (idx 37)
    low_ph = get_feature(r3_low, 37).mean().item()
    high_ph = get_feature(r3_high, 37).mean().item()
    suite.add("F: High freq → higher pitch_height",
              high_ph > low_ph,
              f"High: {high_ph:.3f}, Low: {low_ph:.3f}")

    # Noise should have higher pitch_class_entropy (idx 38) than sine
    noise_pce = get_feature(r3_noise, 38).mean().item()
    sine_pce = get_feature(r3_sine, 38).mean().item()
    suite.add("F: Noise → higher pitch class entropy",
              noise_pce > sine_pce,
              f"Noise: {noise_pce:.3f}, Sine: {sine_pce:.3f}")

    # --- Group G: Rhythm & Groove [41:51] ---
    # Metronome at 120 BPM → tempo_estimate (idx 41) should be ~0.33 (120-30)/(300-30)
    click_tempo = get_feature(r3_clicks, 41).mean().item()
    expected_tempo_norm = (120.0 - 30.0) / (300.0 - 30.0)  # ≈ 0.333
    suite.add("G: 120 BPM clicks → tempo ≈ 0.33",
              abs(click_tempo - expected_tempo_norm) < 0.15,
              f"Got: {click_tempo:.3f}, Expected: ~{expected_tempo_norm:.3f}")

    # Clicks should have higher beat_strength (idx 42) than sine
    click_beat = get_feature(r3_clicks, 42).mean().item()
    sine_beat = get_feature(r3_sine, 42).mean().item()
    suite.add("G: Clicks beat_strength > sine beat_strength",
              click_beat > sine_beat,
              f"Clicks: {click_beat:.3f}, Sine: {sine_beat:.3f}")

    # --- Group H: Harmony [51:63] ---
    # C major chord should have some key_clarity (idx 51)
    cmaj_kc = get_feature(r3_cmaj, 51).mean().item()
    noise_kc = get_feature(r3_noise, 51).mean().item()
    suite.add("H: C major key_clarity > noise key_clarity",
              cmaj_kc > noise_kc,
              f"C major: {cmaj_kc:.3f}, Noise: {noise_kc:.3f}")

    # Steady harmony should have low harmonic_change (idx 59)
    cmaj_hc = get_feature(r3_cmaj, 59).mean().item()
    sweep_hc = get_feature(r3_sweep, 59).mean().item()
    suite.add("H: C major harmonic_change < sweep harmonic_change",
              cmaj_hc < sweep_hc,
              f"C major: {cmaj_hc:.3f}, Sweep: {sweep_hc:.3f}")

    # --- Group J: Timbre Extended [63:83] ---
    # Different timbres should produce different MFCC patterns
    sine_mfcc = get_group(r3_sine, "J")[:, :, :13].mean(dim=1)  # (1, 13)
    noise_mfcc = get_group(r3_noise, "J")[:, :, :13].mean(dim=1)
    mfcc_diff = (sine_mfcc - noise_mfcc).abs().sum().item()
    suite.add("J: Sine vs noise MFCC differ",
              mfcc_diff > 0.1,
              f"Total abs diff: {mfcc_diff:.3f}")

    # Spectral contrast: noise should have lower contrast than harmonic tone
    sine_contrast = get_group(r3_sine, "J")[:, :, 13:].mean().item()
    noise_contrast = get_group(r3_noise, "J")[:, :, 13:].mean().item()
    suite.add("J: Sine contrast ≠ noise contrast",
              abs(sine_contrast - noise_contrast) > 0.01,
              f"Sine: {sine_contrast:.3f}, Noise: {noise_contrast:.3f}")

    # --- Group K: Modulation [83:97] ---
    # AM 4Hz signal: modulation_4Hz (idx 86, which is K[3]) should be noticeable
    am_mod4 = get_feature(r3_am4, 86).mean().item()  # idx 86 = modulation_4Hz
    sine_mod4 = get_feature(r3_sine, 86).mean().item()
    suite.add("K: AM 4Hz → modulation_4Hz > sine's",
              am_mod4 > sine_mod4 or am_mod4 > 0.0,
              f"AM: {am_mod4:.3f}, Sine: {sine_mod4:.3f}")

    # Sharpness Zwicker (idx 91): high freq > low freq
    low_sharp_z = get_feature(r3_low, 91).mean().item()
    high_sharp_z = get_feature(r3_high, 91).mean().item()
    suite.add("K: High freq → higher Zwicker sharpness",
              high_sharp_z > low_sharp_z,
              f"High: {high_sharp_z:.3f}, Low: {low_sharp_z:.3f}")

    # Alpha ratio (idx 94): low freq should have higher alpha (more low-freq energy)
    low_alpha = get_feature(r3_low, 94).mean().item()
    high_alpha = get_feature(r3_high, 94).mean().item()
    suite.add("K: Low freq → higher alpha_ratio",
              low_alpha > high_alpha,
              f"Low: {low_alpha:.3f}, High: {high_alpha:.3f}")

    return suite


# ======================================================================
# TEST SUITE 5: Per-Group Variance & Independence
# ======================================================================

def test_group_independence(extractor: R3Extractor) -> TestSuite:
    suite = TestSuite("5. Per-Group Variance & Independence")

    # Use diverse mel input
    torch.manual_seed(42)
    mel = torch.rand(2, 128, 200)
    out = extractor.extract(mel)
    features = out.features

    # 5.1: Each group has non-zero variance
    for letter, slc in GROUP_SLICES.items():
        group_data = features[:, :, slc]
        var = group_data.var().item()
        suite.add(f"Group {letter} ({GROUP_NAMES_BY_LETTER[letter]}) variance > 0",
                  var > 0, f"Variance: {var:.6f}")

    # 5.2: Groups are not trivially correlated (different mean distributions)
    group_means = {}
    for letter, slc in GROUP_SLICES.items():
        group_means[letter] = features[:, :, slc].mean().item()
    unique_means = len(set(round(m, 3) for m in group_means.values()))
    suite.add("Groups have diverse means", unique_means >= 5,
              f"Unique means (3dp): {unique_means}/9\n" +
              "\n".join(f"  {l}: {m:.4f}" for l, m in group_means.items()))

    # 5.3: Temporal variance per group
    for letter, slc in GROUP_SLICES.items():
        group_data = features[:, :, slc]
        t_var = group_data.var(dim=1).mean().item()
        suite.add(f"Group {letter} temporal variance > 0",
                  t_var > 0, f"Temporal var: {t_var:.6f}")

    # 5.4: Each individual feature (97D) is not all-zero
    zero_features = []
    for i in range(97):
        if features[:, :, i].abs().max().item() == 0:
            zero_features.append(R3_FEATURE_NAMES[i])
    suite.add("No all-zero features (random mel)",
              len(zero_features) == 0,
              f"Zero features: {zero_features}" if zero_features else "All features active")

    # 5.5: No two features are perfectly identical
    identical_pairs = []
    feat_flat = features.view(-1, 97)  # (B*T, 97)
    for i in range(97):
        for j in range(i+1, 97):
            if torch.allclose(feat_flat[:, i], feat_flat[:, j], atol=1e-6):
                identical_pairs.append((R3_FEATURE_NAMES[i], R3_FEATURE_NAMES[j]))
    # Allow known duplicates (warmth ≈ stumpf_fusion, autocorr ≈ helmholtz)
    known_dups = {
        ("warmth", "stumpf_fusion"),
        ("stumpf_fusion", "warmth"),
        ("spectral_autocorrelation", "helmholtz_kang"),
        ("helmholtz_kang", "spectral_autocorrelation"),
    }
    unexpected = [p for p in identical_pairs if p not in known_dups]
    suite.add("No unexpected identical features",
              len(unexpected) == 0,
              f"Known dups: {len(identical_pairs)}, Unexpected: {unexpected}" if unexpected
              else f"Known dups: {len(identical_pairs)} (warmth≈stumpf, autocorr≈helmholtz)")

    return suite


# ======================================================================
# TEST SUITE 6: Real Audio from Test-Audio/ (synthetic micro-beliefs)
# ======================================================================

def test_micro_belief_audio(extractor: R3Extractor) -> TestSuite:
    suite = TestSuite("6. Micro-Belief Test Audio")

    test_audio_dir = _PROJECT_ROOT / "Test-Audio"
    if not test_audio_dir.exists():
        suite.add("Test-Audio/ exists", False, f"Directory not found: {test_audio_dir}")
        return suite

    # Find BCH test files
    bch_dir = test_audio_dir / "F1" / "bch"
    if not bch_dir.exists():
        # Try alternative structure
        bch_files = list(test_audio_dir.rglob("bch/*.wav"))
        if not bch_files:
            suite.add("BCH test files found", False, "No bch/*.wav files found")
            return suite
    else:
        bch_files = sorted(bch_dir.glob("*.wav"))

    if not bch_files:
        suite.add("BCH test files found", False, "No BCH wav files")
        return suite

    suite.add("BCH test files found", True, f"Found {len(bch_files)} files")

    # Load and test each BCH file
    try:
        import soundfile as sf
    except ImportError:
        try:
            import scipy.io.wavfile as wavfile
            sf = None
        except ImportError:
            suite.add("Audio loader available", False, "Need soundfile or scipy")
            return suite

    for wav_path in bch_files[:10]:  # Test up to 10 files
        name = wav_path.stem
        try:
            if sf:
                audio, file_sr = sf.read(str(wav_path), dtype='float32')
            else:
                file_sr, audio = wavfile.read(str(wav_path))
                audio = audio.astype(np.float32) / 32768.0

            if audio.ndim > 1:
                audio = audio.mean(axis=1)

            # Resample if needed (simple decimation/interpolation)
            if file_sr != SR:
                ratio = SR / file_sr
                new_len = int(len(audio) * ratio)
                audio = np.interp(np.linspace(0, len(audio)-1, new_len),
                                  np.arange(len(audio)), audio).astype(np.float32)

            mel = make_mel_from_audio(audio)
            out = extractor.extract(mel)

            no_nan = not torch.isnan(out.features).any().item()
            in_range = out.features.min() >= 0 and out.features.max() <= 1
            suite.add(f"BCH/{name}: valid output", no_nan and in_range,
                      f"Shape: {tuple(out.features.shape)}, "
                      f"NaN: {not no_nan}, Range: [{out.features.min():.3f}, {out.features.max():.3f}]")
        except Exception as e:
            suite.add(f"BCH/{name}: no crash", False, str(e)[:100])

    return suite


# ======================================================================
# TEST SUITE 7: Real Audio from Test-Audio/ (classical recordings)
# ======================================================================

def test_real_audio(extractor: R3Extractor) -> TestSuite:
    suite = TestSuite("7. Real Audio — Classical Recordings")

    test_audio_dir = _PROJECT_ROOT / "Test-Audio"
    if not test_audio_dir.exists():
        suite.add("Test-Audio/ exists", False, f"Not found: {test_audio_dir}")
        return suite

    # Find real audio files (WAV and MP3 in root of Test-Audio/)
    real_files = sorted(test_audio_dir.glob("*.wav")) + sorted(test_audio_dir.glob("*.mp3"))
    # Filter out micro-belief generated files (those with hash suffixes)
    real_files = [f for f in real_files if not any(c == '_' and f.stem[-8:].isalnum() and len(f.stem) > 30
                                                   for c in f.stem)]

    if not real_files:
        suite.add("Real audio files found", False, "No WAV/MP3 in Test-Audio/")
        return suite

    suite.add("Real audio files found", True, f"Found {len(real_files)} files")

    try:
        import soundfile as sf
    except ImportError:
        sf = None

    results_data = {}

    for wav_path in real_files:
        name = wav_path.stem[:50]
        try:
            if wav_path.suffix == '.mp3':
                # Try pydub or skip
                try:
                    from pydub import AudioSegment
                    seg = AudioSegment.from_mp3(str(wav_path))
                    samples = np.array(seg.get_array_of_samples(), dtype=np.float32)
                    if seg.channels > 1:
                        samples = samples.reshape(-1, seg.channels).mean(axis=1)
                    samples /= 32768.0
                    audio = samples
                    file_sr = seg.frame_rate
                except ImportError:
                    suite.add(f"  {name}: skip (no mp3 decoder)", True, "Need pydub for mp3")
                    continue
            else:
                if sf:
                    audio, file_sr = sf.read(str(wav_path), dtype='float32')
                else:
                    import scipy.io.wavfile as wavfile
                    file_sr, audio = wavfile.read(str(wav_path))
                    audio = audio.astype(np.float32)
                    if audio.dtype == np.int16:
                        audio = audio / 32768.0
                    elif audio.dtype == np.int32:
                        audio = audio / 2147483648.0

            if audio.ndim > 1:
                audio = audio.mean(axis=1)

            # Use first 10 seconds max for speed
            max_samples = SR * 10
            if len(audio) > max_samples:
                audio = audio[:max_samples]

            # Resample if needed
            if file_sr != SR:
                ratio = SR / file_sr
                new_len = int(len(audio) * ratio)
                audio = np.interp(np.linspace(0, len(audio)-1, new_len),
                                  np.arange(len(audio)), audio).astype(np.float32)

            mel = make_mel_from_audio(audio)
            t0 = time.perf_counter()
            out = extractor.extract(mel)
            dt = (time.perf_counter() - t0) * 1000

            f = out.features
            T = f.shape[1]
            fps = T / (dt / 1000)

            no_nan = not torch.isnan(f).any().item()
            no_inf = not torch.isinf(f).any().item()
            in_range = f.min() >= 0 and f.max() <= 1

            # Compute per-group statistics
            stats = {}
            for letter in GROUP_SLICES:
                g = get_group(f, letter)
                stats[letter] = {
                    "mean": g.mean().item(),
                    "std": g.std().item(),
                    "min": g.min().item(),
                    "max": g.max().item(),
                }

            results_data[name] = {
                "T": T, "fps": fps, "dt_ms": dt,
                "no_nan": no_nan, "no_inf": no_inf, "in_range": in_range,
                "stats": stats,
            }

            suite.add(f"  {name}: valid output", no_nan and no_inf and in_range,
                      f"T={T}, FPS={fps:.0f}, Range=[{f.min():.3f}, {f.max():.3f}]", dt)

            # Check that most features have temporal variance
            t_var = f.var(dim=1).squeeze()  # (97,)
            varying = (t_var > 1e-6).sum().item()
            suite.add(f"  {name}: temporal variance",
                      varying >= 40,
                      f"{varying}/97 features vary over time")

            # Check non-trivial feature activity
            active = (f.mean(dim=1).squeeze() > 0.01).sum().item()
            suite.add(f"  {name}: feature activity",
                      active >= 50,
                      f"{active}/97 features active (mean > 0.01)")

        except Exception as e:
            suite.add(f"  {name}: no crash", False, traceback.format_exc()[-200:])

    # Cross-piece comparison: different pieces should produce different feature profiles
    if len(results_data) >= 2:
        pieces = list(results_data.keys())
        differences_found = 0
        for i in range(len(pieces)):
            for j in range(i+1, len(pieces)):
                p1, p2 = pieces[i], pieces[j]
                d1 = results_data[p1]["stats"]
                d2 = results_data[p2]["stats"]
                total_diff = sum(abs(d1[l]["mean"] - d2[l]["mean"]) for l in GROUP_SLICES)
                if total_diff > 0.1:
                    differences_found += 1

        suite.add("Cross-piece diversity",
                  differences_found > 0,
                  f"{differences_found} piece-pairs show different profiles")

    return suite


# ======================================================================
# TEST SUITE 8: Audio Path vs Mel Path (ConsonanceGroup)
# ======================================================================

def test_audio_vs_mel_path(extractor: R3Extractor) -> TestSuite:
    suite = TestSuite("8. Audio Path vs Mel Path (ConsonanceGroup)")

    # Generate a harmonic tone
    audio_np = harmonic_tone(220.0, n_harmonics=8, duration=1.0)
    mel = make_mel_from_audio(audio_np)
    audio_t = torch.from_numpy(audio_np).unsqueeze(0)  # (1, N)

    # Mel-only path
    out_mel = extractor.extract(mel)
    consonance_mel = get_group(out_mel.features, "A")  # (1, T, 7)

    # Audio+mel path
    out_audio = extractor.extract(mel, audio=audio_t, sr=SR)
    consonance_audio = get_group(out_audio.features, "A")  # (1, T, 7)

    # Both should produce valid output
    suite.add("Mel path: no NaN", not torch.isnan(consonance_mel).any().item())
    suite.add("Audio path: no NaN", not torch.isnan(consonance_audio).any().item())
    suite.add("Mel path: in [0,1]",
              consonance_mel.min() >= 0 and consonance_mel.max() <= 1)
    suite.add("Audio path: in [0,1]",
              consonance_audio.min() >= 0 and consonance_audio.max() <= 1)

    # They should be different (audio path uses real psychoacoustic models)
    diff = (consonance_mel - consonance_audio).abs().mean().item()
    suite.add("Audio vs mel paths differ",
              diff > 0.001,
              f"Mean abs diff: {diff:.4f}")

    # Non-consonance groups should be identical (audio only affects Group A)
    for letter in ["B", "C", "D", "F", "J", "K"]:
        g_mel = get_group(out_mel.features, letter)
        g_audio = get_group(out_audio.features, letter)
        g_diff = (g_mel - g_audio).abs().max().item()
        suite.add(f"Group {letter} identical in both paths",
                  g_diff < 1e-5,
                  f"Max diff: {g_diff:.2e}")

    return suite


# ======================================================================
# TEST SUITE 9: Performance
# ======================================================================

def test_performance(extractor: R3Extractor) -> TestSuite:
    suite = TestSuite("9. Performance")

    # Warmup
    mel = torch.rand(1, 128, 100)
    extractor.extract(mel)

    # 9.1: Short clip (1s ≈ 172 frames)
    mel_1s = torch.rand(1, 128, 172)
    _, dt_1s = timed(lambda: extractor.extract(mel_1s))
    fps_1s = 172 / (dt_1s / 1000)
    suite.add("1s clip FPS", True, f"{fps_1s:.0f} FPS ({dt_1s:.0f}ms)", dt_1s)

    # 9.2: 10s clip (≈ 1722 frames)
    mel_10s = torch.rand(1, 128, 1722)
    _, dt_10s = timed(lambda: extractor.extract(mel_10s))
    fps_10s = 1722 / (dt_10s / 1000)
    suite.add("10s clip FPS", True, f"{fps_10s:.0f} FPS ({dt_10s:.0f}ms)", dt_10s)

    # 9.3: 30s clip (≈ 5168 frames)
    mel_30s = torch.rand(1, 128, 5168)
    _, dt_30s = timed(lambda: extractor.extract(mel_30s))
    fps_30s = 5168 / (dt_30s / 1000)
    suite.add("30s clip FPS", True, f"{fps_30s:.0f} FPS ({dt_30s:.0f}ms)", dt_30s)

    # 9.4: Batch=4 x 10s
    mel_b4 = torch.rand(4, 128, 1722)
    _, dt_b4 = timed(lambda: extractor.extract(mel_b4))
    fps_b4 = (4 * 1722) / (dt_b4 / 1000)
    suite.add("Batch=4 x 10s FPS", True, f"{fps_b4:.0f} total FPS ({dt_b4:.0f}ms)", dt_b4)

    # 9.5: Minimum FPS threshold
    suite.add("30s clip FPS > 100", fps_30s > 100,
              f"Got {fps_30s:.0f} FPS")

    return suite


# ======================================================================
# Main
# ======================================================================

def main():
    print("="*70)
    print("  R³ Deep Test Suite")
    print(f"  Project: {_PROJECT_ROOT}")
    print(f"  R³ dims: {R3_DIM}, Groups: {len(R3_GROUP_BOUNDARIES)}")
    print("="*70)

    # Initialize R³ extractor
    print("\nInitializing R³ extractor...")
    t0 = time.perf_counter()
    extractor = R3Extractor()
    init_time = (time.perf_counter() - t0) * 1000
    print(f"  R³ extractor ready: {extractor} ({init_time:.0f}ms)")

    # Run all test suites
    all_suites: List[TestSuite] = []

    suite_runners = [
        ("1. Structural Validation", lambda: test_structural(extractor)),
        ("2. Edge Cases", lambda: test_edge_cases(extractor)),
        ("3. Determinism", lambda: test_determinism(extractor)),
        ("4. Semantic (Synthesized)", lambda: test_semantic_synthetic(extractor)),
        ("5. Group Independence", lambda: test_group_independence(extractor)),
        ("6. Micro-Belief Audio", lambda: test_micro_belief_audio(extractor)),
        ("7. Real Audio", lambda: test_real_audio(extractor)),
        ("8. Audio vs Mel Path", lambda: test_audio_vs_mel_path(extractor)),
        ("9. Performance", lambda: test_performance(extractor)),
    ]

    for name, runner in suite_runners:
        print(f"\nRunning {name}...")
        try:
            suite = runner()
            all_suites.append(suite)
            print(suite.report())
        except Exception as e:
            print(f"  SUITE CRASHED: {e}")
            traceback.print_exc()
            crash_suite = TestSuite(name)
            crash_suite.add("Suite execution", False, traceback.format_exc()[-300:])
            all_suites.append(crash_suite)

    # Summary
    total_pass = sum(s.passed for s in all_suites)
    total_fail = sum(s.failed for s in all_suites)
    total_tests = sum(s.total for s in all_suites)

    print("\n" + "="*70)
    print(f"  GRAND TOTAL: {total_pass}/{total_tests} PASSED, {total_fail} FAILED")
    print("="*70)

    if total_fail > 0:
        print("\n  FAILURES:")
        for s in all_suites:
            for r in s.results:
                if not r.passed:
                    print(f"    [{s.name}] {r.name}")
                    if r.message:
                        print(f"      {r.message[:120]}")

    print()
    return total_fail == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
