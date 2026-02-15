#!/usr/bin/env python3
"""Generate synthetic piano dyads for BCH consonance hierarchy testing.

Produces 6 intervals (8 seconds each, with 0.5s silence gaps):
    1. Unison (P1)      — C4 + C4   (0 semitones, ratio 1:1)
    2. Perfect Fifth (P5) — C4 + G4   (7 semitones, ratio 3:2)
    3. Perfect Fourth (P4) — C4 + F4   (5 semitones, ratio 4:3)
    4. Major Third (M3)   — C4 + E4   (4 semitones, ratio 5:4)
    5. Minor Sixth (m6)   — C4 + Ab4  (8 semitones, ratio 8:5)
    6. Tritone (TT)       — C4 + F#4  (6 semitones, ratio √2:1)

This ordering matches the Bidelman & Krishnan (2009) consonance hierarchy:
    P1 > P5 > P4 > M3 > m6 > TT

Piano synthesis: additive harmonics (12 partials) with exponential decay
envelope simulating a sustained piano tone.

Output: Lab/WebLab/experiments/BCH-R-Nucleus/audio.wav

Usage:
    python Lab/WebLab/scripts/generate_bch_consonance.py
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

# ======================================================================
# Constants
# ======================================================================
SR = 44100
NOTE_DURATION = 8.0    # seconds per dyad
GAP_DURATION = 0.5     # silence between dyads
FADE_IN = 0.05         # attack in seconds
FADE_OUT = 0.3         # release in seconds

C4 = 261.6256          # Hz

# Consonance hierarchy: P1 > P5 > P4 > M3 > m6 > TT
INTERVALS = [
    ("Unison (P1)",         0),   # C4 + C4
    ("Perfect Fifth (P5)",  7),   # C4 + G4
    ("Perfect Fourth (P4)", 5),   # C4 + F4
    ("Major Third (M3)",    4),   # C4 + E4
    ("Minor Sixth (m6)",    8),   # C4 + Ab4
    ("Tritone (TT)",        6),   # C4 + F#4
]

N_HARMONICS = 12
BASE_AMP = 0.35  # overall amplitude


# ======================================================================
# Synthesis
# ======================================================================
def piano_tone(freq: float, duration: float, sr: int = SR) -> np.ndarray:
    """Synthesize a piano-like tone using additive harmonics.

    12 partials with amplitudes following 1/n^0.7 decay (brighter than
    pure 1/n to match piano spectral profile). Exponential decay envelope
    with 4-second time constant.
    """
    t = np.arange(int(duration * sr)) / sr
    signal = np.zeros_like(t)

    for n in range(1, N_HARMONICS + 1):
        partial_freq = freq * n
        if partial_freq > sr / 2:
            break
        # Amplitude: 1/n^0.7 (brighter than pure harmonic)
        amp = 1.0 / (n ** 0.7)
        # Slight inharmonicity for realism (piano strings aren't perfect)
        inharmonicity = 1.0 + 0.0001 * n * n
        actual_freq = freq * n * inharmonicity
        if actual_freq > sr / 2:
            break
        signal += amp * np.sin(2.0 * np.pi * actual_freq * t)

    # Exponential decay envelope (piano-like sustain)
    envelope = np.exp(-t / 4.0)

    # Fade in (attack)
    attack_samples = int(FADE_IN * sr)
    if attack_samples > 0:
        envelope[:attack_samples] *= np.linspace(0, 1, attack_samples)

    # Fade out (release)
    release_samples = int(FADE_OUT * sr)
    if release_samples > 0:
        envelope[-release_samples:] *= np.linspace(1, 0, release_samples)

    return signal * envelope


def make_dyad(semitones: int, duration: float = NOTE_DURATION) -> np.ndarray:
    """Create a two-note dyad at given interval above C4."""
    freq1 = C4
    freq2 = C4 * (2.0 ** (semitones / 12.0))

    tone1 = piano_tone(freq1, duration)
    tone2 = piano_tone(freq2, duration)

    # Mix at equal level
    dyad = (tone1 + tone2) / 2.0
    return dyad


def main():
    _script_dir = Path(__file__).resolve().parent
    _weblab_dir = _script_dir.parent
    exp_dir = _weblab_dir / "experiments" / "BCH-R-Nucleus"
    exp_dir.mkdir(parents=True, exist_ok=True)

    gap = np.zeros(int(GAP_DURATION * SR))
    segments = []

    print("Generating consonance hierarchy dyads:")
    print(f"  Base note: C4 = {C4:.2f} Hz")
    print(f"  Duration per dyad: {NOTE_DURATION}s")
    print(f"  Gap between dyads: {GAP_DURATION}s")
    print()

    for i, (name, semitones) in enumerate(INTERVALS):
        freq2 = C4 * (2.0 ** (semitones / 12.0))
        ratio = freq2 / C4
        print(f"  [{i+1}] {name:<24} C4({C4:.1f}Hz) + "
              f"{freq2:.1f}Hz  (ratio {ratio:.4f})")

        dyad = make_dyad(semitones)
        segments.append(dyad)
        if i < len(INTERVALS) - 1:
            segments.append(gap)

    # Concatenate all segments
    audio = np.concatenate(segments)

    # Normalize to prevent clipping
    audio = audio / np.abs(audio).max() * BASE_AMP

    total_duration = len(audio) / SR
    print(f"\n  Total duration: {total_duration:.2f}s")
    print(f"  Total samples: {len(audio)}")

    # Save
    audio_path = exp_dir / "audio.wav"
    sf.write(str(audio_path), audio, SR, subtype="PCM_16")
    print(f"  Saved: {audio_path}")

    # Also save interval markers for visualization
    markers = []
    t = 0.0
    for i, (name, semitones) in enumerate(INTERVALS):
        markers.append({
            "name": name,
            "semitones": semitones,
            "start_s": round(t, 3),
            "end_s": round(t + NOTE_DURATION, 3),
            "freq1": round(C4, 2),
            "freq2": round(C4 * (2.0 ** (semitones / 12.0)), 2),
        })
        t += NOTE_DURATION
        if i < len(INTERVALS) - 1:
            t += GAP_DURATION

    import json
    markers_path = exp_dir / "interval_markers.json"
    markers_path.write_text(json.dumps(markers, indent=2))
    print(f"  Saved: {markers_path}")

    return str(audio_path)


if __name__ == "__main__":
    main()
