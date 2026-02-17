#!/usr/bin/env python3
"""Emotion Transform Test — Frame-Level Audio Manipulation via MI-Space.

Proof-of-concept for the HYBRID mode:
  1. Load audio → mel spectrogram
  2. Analyze: mel → R³ (what the music IS)
  3. Apply emotion transform to mel (what we WANT it to be)
  4. Analyze modified mel → R³ (verify the shift)
  5. Reconstruct audio from modified mel (Griffin-Lim)
  6. Save A/B audio files for listening

This validates: "Can we control the emotional character of sound
by manipulating the MI-space representation?"

Available transforms:
  --transform warmer      : Boost low-mid, reduce highs
  --transform brighter    : Boost highs, reduce lows
  --transform darker      : Reduce highs, boost lows
  --transform intense     : Sharpen peaks, boost energy + highs
  --transform calm        : Smooth spectrum, reduce contrast
  --transform dissonant   : Add spectral roughness

Usage:
    python Tests/experiments/emotion_transform.py --transform warmer
    python Tests/experiments/emotion_transform.py --transform intense --strength 0.5
    python Tests/experiments/emotion_transform.py --transform darker --input "Duel of the Fates"
    python Tests/experiments/emotion_transform.py --all   # Run all transforms
"""
from __future__ import annotations

import os
import sys
import time
import argparse
from pathlib import Path

_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import librosa
import numpy as np
import soundfile as sf
import torch
from torch import Tensor

from Musical_Intelligence.ear.r3 import R3Extractor
from Musical_Intelligence.ear.r3.constants import R3_FEATURE_NAMES

# ─── Constants ────────────────────────────────────────────────────────────────
SR = 44100
HOP = 256
N_MELS = 128
N_FFT = 1024
FRAME_RATE = SR / HOP

AUDIO_DIR = os.path.join(_PROJECT_ROOT, "Test-Audio")
OUTPUT_DIR = os.path.join(_PROJECT_ROOT, "Tests", "reports", "emotion_transform")

AUDIO_FILES = {
    "swan_lake": "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky.wav",
    "cello": "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav",
    "duel": "Duel of the Fates - Epic Version.wav",
    "pathetique": "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
}

DEFAULT_AUDIO = "swan_lake"


# ─── Emotion Transforms ──────────────────────────────────────────────────────
# Each transform modifies the mel spectrogram (128 mel bins × T frames)
# to shift the emotional character in a specific direction.
#
# Mel bins: 0=lowest frequency (~20Hz) → 127=highest frequency (~11kHz)
# Low (0-30):   Bass, warmth, body
# Mid (30-70):  Fundamental, clarity, presence
# High (70-128): Brightness, air, sharpness

def _freq_envelope(n_mels: int, center: float, width: float) -> np.ndarray:
    """Create a Gaussian envelope over mel bins."""
    bins = np.arange(n_mels, dtype=np.float32)
    return np.exp(-0.5 * ((bins - center) / width) ** 2)


def transform_warmer(mel: np.ndarray, strength: float) -> np.ndarray:
    """Make the sound warmer: boost low-mid, reduce highs.

    Psychoacoustic basis: warmth correlates with low-frequency
    energy balance (R³.warmth, mel bins 20-60).
    """
    out = mel.copy()
    n_mels = mel.shape[0]

    # Boost low-mid (centered around bin 35, ~300-800Hz)
    boost = _freq_envelope(n_mels, center=35, width=20)
    out *= (1.0 + strength * 0.4 * boost[:, None])

    # Reduce highs (above bin 80, ~4kHz+)
    cut = 1.0 - strength * 0.3 * _freq_envelope(n_mels, center=110, width=25)[:, None]
    out *= cut

    return out


def transform_brighter(mel: np.ndarray, strength: float) -> np.ndarray:
    """Make the sound brighter: boost highs, slightly reduce lows.

    Psychoacoustic basis: brightness correlates with spectral
    centroid position (R³.clarity, R³.sharpness).
    """
    out = mel.copy()
    n_mels = mel.shape[0]

    # Boost highs (centered around bin 95, ~6-8kHz)
    boost = _freq_envelope(n_mels, center=95, width=20)
    out *= (1.0 + strength * 0.5 * boost[:, None])

    # Slightly reduce lows
    cut = 1.0 - strength * 0.15 * _freq_envelope(n_mels, center=15, width=15)[:, None]
    out *= cut

    return out


def transform_darker(mel: np.ndarray, strength: float) -> np.ndarray:
    """Make the sound darker: reduce highs, boost lows.

    Inverse of brighter. Reduces R³.clarity and R³.sharpness.
    """
    out = mel.copy()
    n_mels = mel.shape[0]

    # Cut highs
    cut = 1.0 - strength * 0.5 * _freq_envelope(n_mels, center=100, width=25)[:, None]
    out *= cut

    # Boost low
    boost = _freq_envelope(n_mels, center=25, width=20)
    out *= (1.0 + strength * 0.3 * boost[:, None])

    return out


def transform_intense(mel: np.ndarray, strength: float) -> np.ndarray:
    """Make the sound more intense: sharpen peaks, boost energy.

    Increases R³.energy, R³.onset_strength, R³.spectral_flux.
    Simulates adding more instruments / louder dynamics.
    """
    out = mel.copy()

    # Overall energy boost
    out *= (1.0 + strength * 0.3)

    # Sharpen spectral peaks (increase contrast)
    mean_per_frame = out.mean(axis=0, keepdims=True)
    deviation = out - mean_per_frame
    out = mean_per_frame + deviation * (1.0 + strength * 0.5)

    # Boost high-frequency energy (adds "edge")
    n_mels = mel.shape[0]
    high_boost = _freq_envelope(n_mels, center=90, width=30)
    out *= (1.0 + strength * 0.2 * high_boost[:, None])

    return np.maximum(out, 0.0)


def transform_calm(mel: np.ndarray, strength: float) -> np.ndarray:
    """Make the sound calmer: smooth spectrum, reduce contrast.

    Decreases R³.energy, R³.spectral_flux, R³.onset_strength.
    """
    out = mel.copy()

    # Reduce overall energy
    out *= (1.0 - strength * 0.2)

    # Smooth spectral peaks (reduce contrast)
    mean_per_frame = out.mean(axis=0, keepdims=True)
    deviation = out - mean_per_frame
    out = mean_per_frame + deviation * (1.0 - strength * 0.4)

    # Temporal smoothing (reduce transients)
    if out.shape[1] > 3:
        kernel = np.array([0.15, 0.7, 0.15])
        for i in range(out.shape[0]):
            out[i] = np.convolve(out[i], kernel, mode='same')

    return np.maximum(out, 0.0)


def transform_dissonant(mel: np.ndarray, strength: float) -> np.ndarray:
    """Add spectral roughness / dissonance.

    Adds inter-harmonic energy that increases R³.roughness
    and R³.sethares_dissonance. Simulates beating frequencies.
    """
    out = mel.copy()
    n_mels, T = mel.shape

    # Add frequency-shifted copies (creates beating)
    for shift in [1, 2, 3]:
        shifted = np.roll(out, shift, axis=0)
        out += strength * 0.15 * shifted

    # Add slight noise in mid-high range
    noise = np.random.RandomState(42).rand(n_mels, T).astype(np.float32)
    noise_mask = _freq_envelope(n_mels, center=70, width=30)[:, None]
    out += strength * 0.1 * noise * noise_mask * out.mean()

    return np.maximum(out, 0.0)


TRANSFORMS = {
    "warmer": (transform_warmer, "Boost low-mid, reduce highs → R³.warmth ↑"),
    "brighter": (transform_brighter, "Boost highs → R³.clarity ↑, R³.sharpness ↑"),
    "darker": (transform_darker, "Reduce highs, boost lows → R³.warmth ↑, R³.clarity ↓"),
    "intense": (transform_intense, "Sharpen peaks, boost energy → R³.energy ↑, R³.flux ↑"),
    "calm": (transform_calm, "Smooth spectrum, reduce contrast → R³.energy ↓"),
    "dissonant": (transform_dissonant, "Add spectral roughness → R³.roughness ↑"),
}


# ─── R³ Analysis ──────────────────────────────────────────────────────────────
def normalize_mel_for_r3(mel_power: np.ndarray) -> Tensor:
    """Convert raw power mel to normalized tensor for R³ extraction."""
    mel_db = librosa.power_to_db(mel_power, ref=np.max)
    mel_norm = (mel_db - mel_db.min()) / (mel_db.max() - mel_db.min() + 1e-8)
    return torch.tensor(mel_norm, dtype=torch.float32).unsqueeze(0)


def extract_r3_key_features(r3_ext: R3Extractor, mel_tensor: Tensor) -> dict:
    """Extract emotion-relevant R³ features."""
    r3_output = r3_ext.extract(mel_tensor)
    feat = r3_output.features[0]  # (T, 97)

    name_to_idx = {n: i for i, n in enumerate(R3_FEATURE_NAMES)}

    targets = [
        "roughness", "sethares_dissonance", "sensory_pleasantness",
        "amplitude", "onset_strength",
        "warmth", "sharpness", "tonalness", "clarity",
        "spectral_flux", "distribution_entropy",
    ]

    result = {}
    for name in targets:
        if name in name_to_idx:
            idx = name_to_idx[name]
            vals = feat[:, idx]
            result[name] = vals.mean().item()

    return result


# ─── Audio Reconstruction ────────────────────────────────────────────────────
def mel_to_audio(mel_power: np.ndarray) -> np.ndarray:
    """Reconstruct audio from power mel spectrogram using Griffin-Lim."""
    return librosa.feature.inverse.mel_to_audio(
        mel_power,
        sr=SR,
        n_fft=N_FFT,
        hop_length=HOP,
        power=2.0,
        n_iter=64,
    )


# ─── Main Logic ──────────────────────────────────────────────────────────────
def run_transform(
    audio_key: str,
    transform_name: str,
    strength: float,
    duration: float,
    offset: float,
) -> dict:
    """Run a single emotion transform and return results."""

    audio_file = AUDIO_FILES[audio_key]
    audio_path = os.path.join(AUDIO_DIR, audio_file)

    if not os.path.exists(audio_path):
        print(f"  ERROR: {audio_file} not found")
        return {}

    transform_fn, description = TRANSFORMS[transform_name]

    print(f"\n{'=' * 70}")
    print(f"  Transform: {transform_name.upper()} (strength={strength:.1f})")
    print(f"  Audio: {audio_key} ({duration}s from {offset}s)")
    print(f"  Effect: {description}")
    print(f"{'=' * 70}")

    # 1. Load audio and compute RAW mel (power spectrogram)
    t0 = time.time()
    y_orig, sr = librosa.load(audio_path, sr=SR, mono=True,
                               offset=offset, duration=duration)
    mel_power = librosa.feature.melspectrogram(
        y=y_orig, sr=sr, n_mels=N_MELS, hop_length=HOP, n_fft=N_FFT,
    )
    load_time = time.time() - t0
    print(f"\n  1. Loaded audio: {len(y_orig)/SR:.1f}s, mel shape: {mel_power.shape}")

    # 2. Extract R³ from ORIGINAL
    r3_ext = R3Extractor()
    mel_norm_orig = normalize_mel_for_r3(mel_power)
    t0 = time.time()
    r3_original = extract_r3_key_features(r3_ext, mel_norm_orig)
    r3_time = time.time() - t0
    print(f"  2. R³ original extracted ({r3_time:.2f}s)")

    # 3. Apply emotion transform to mel
    t0 = time.time()
    mel_modified = transform_fn(mel_power, strength)
    transform_time = time.time() - t0
    print(f"  3. Transform applied ({transform_time*1000:.1f}ms)")

    # 4. Extract R³ from MODIFIED
    mel_norm_mod = normalize_mel_for_r3(mel_modified)
    r3_modified = extract_r3_key_features(r3_ext, mel_norm_mod)
    print(f"  4. R³ modified extracted")

    # 5. Reconstruct audio
    t0 = time.time()
    y_original_recon = mel_to_audio(mel_power)
    y_modified_recon = mel_to_audio(mel_modified)
    recon_time = time.time() - t0
    print(f"  5. Audio reconstructed ({recon_time:.2f}s)")

    # 6. Save audio files
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    orig_path = os.path.join(OUTPUT_DIR, f"{audio_key}_original.wav")
    mod_path = os.path.join(OUTPUT_DIR, f"{audio_key}_{transform_name}_s{strength:.1f}.wav")
    direct_path = os.path.join(OUTPUT_DIR, f"{audio_key}_direct.wav")

    sf.write(orig_path, y_original_recon, SR)
    sf.write(mod_path, y_modified_recon, SR)
    sf.write(direct_path, y_orig, SR)  # original without Griffin-Lim

    print(f"  6. Saved audio:")
    print(f"     Original (direct):     {direct_path}")
    print(f"     Original (Griffin-Lim): {orig_path}")
    print(f"     Modified ({transform_name}):  {mod_path}")

    # 7. Compare R³
    print(f"\n  R³ COMPARISON (original → modified):")
    print(f"  {'Feature':<25s}  {'Original':>10s}  {'Modified':>10s}  {'Delta':>10s}  Direction")
    print(f"  {'─' * 25}  {'─' * 10}  {'─' * 10}  {'─' * 10}  {'─' * 12}")

    changes = {}
    for feat in sorted(r3_original.keys()):
        orig_val = r3_original[feat]
        mod_val = r3_modified[feat]
        delta = mod_val - orig_val
        direction = "↑" if delta > 0.005 else "↓" if delta < -0.005 else "="
        marker = " ***" if abs(delta) > 0.03 else " *" if abs(delta) > 0.01 else ""
        print(f"  {feat:<25s}  {orig_val:10.4f}  {mod_val:10.4f}  {delta:+10.4f}  {direction}{marker}")
        changes[feat] = delta

    return {
        "transform": transform_name,
        "strength": strength,
        "r3_original": r3_original,
        "r3_modified": r3_modified,
        "changes": changes,
        "audio_files": {
            "direct": direct_path,
            "original_recon": orig_path,
            "modified_recon": mod_path,
        },
    }


def run_all_transforms(audio_key: str, strength: float, duration: float, offset: float):
    """Run all transforms on the same audio for comparison."""
    print("\n" + "=" * 70)
    print("  ALL TRANSFORMS COMPARISON")
    print("=" * 70)

    results = {}
    for name in TRANSFORMS:
        result = run_transform(audio_key, name, strength, duration, offset)
        if result:
            results[name] = result

    if not results:
        return

    # Summary table
    print("\n" + "=" * 70)
    print("  SUMMARY: R³ changes across all transforms")
    print("=" * 70)

    features = sorted(list(results.values())[0]["changes"].keys())

    header = f"  {'Feature':<22s}"
    for name in TRANSFORMS:
        header += f"  {name:>10s}"
    print(header)
    print(f"  {'─' * 22}" + f"  {'─' * 10}" * len(TRANSFORMS))

    for feat in features:
        row = f"  {feat:<22s}"
        for name in TRANSFORMS:
            if name in results:
                delta = results[name]["changes"][feat]
                row += f"  {delta:+10.4f}"
            else:
                row += f"  {'N/A':>10s}"
        print(row)

    print(f"\n  Audio files saved to: {OUTPUT_DIR}/")
    print(f"  Listen to A/B comparisons to verify perceptual difference!")


def main():
    parser = argparse.ArgumentParser(description="Emotion Transform Test")
    parser.add_argument("--transform", choices=list(TRANSFORMS.keys()),
                       default="warmer", help="Which emotion transform")
    parser.add_argument("--all", action="store_true",
                       help="Run all transforms")
    parser.add_argument("--strength", type=float, default=0.7,
                       help="Transform strength 0.0-1.0 (default: 0.7)")
    parser.add_argument("--input", choices=list(AUDIO_FILES.keys()),
                       default=DEFAULT_AUDIO, help="Audio file to use")
    parser.add_argument("--duration", type=float, default=10.0,
                       help="Clip duration in seconds")
    parser.add_argument("--offset", type=float, default=15.0,
                       help="Start offset in seconds")
    args = parser.parse_args()

    print()
    print("=" * 70)
    print("  EMOTION TRANSFORM TEST")
    print("  Proof-of-concept: emotion control → audio change → R³ verification")
    print("=" * 70)

    if args.all:
        run_all_transforms(args.input, args.strength, args.duration, args.offset)
    else:
        run_transform(args.input, args.transform, args.strength,
                     args.duration, args.offset)

    print()


if __name__ == "__main__":
    main()
