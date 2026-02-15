#!/usr/bin/env python3
"""Assemble real piano dyads from University of Iowa MIS samples.

Uses mezzo-forte (mf) recordings of individual piano notes to create
6 consonance hierarchy dyads:
    1. Unison (P1)       — C4 + C4
    2. Perfect Fifth (P5) — C4 + G4
    3. Perfect Fourth (P4) — C4 + F4
    4. Major Third (M3)   — C4 + E4
    5. Minor Sixth (m6)   — C4 + Ab4
    6. Tritone (TT)       — C4 + Gb4

Source: University of Iowa Electronic Music Studios
        https://theremin.music.uiowa.edu/mis.html
        License: Public domain, unrestricted use.

Output: Lab/WebLab/experiments/BCH-R-Nucleus-Real/audio.wav
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import soundfile as sf

# ======================================================================
# Constants
# ======================================================================
SR = 44100
NOTE_DURATION = 8.0    # seconds per dyad
GAP_DURATION = 0.5     # silence between dyads
FADE_IN = 0.02         # short fade to avoid click
FADE_OUT = 0.15        # release fade
ONSET_SKIP = 0.0       # skip start silence (Iowa samples have clean onsets)

# Consonance hierarchy: P1 > P5 > P4 > M3 > m6 > TT
INTERVALS = [
    ("Unison (P1)",         0,  "C4",  "C4"),
    ("Perfect Fifth (P5)",  7,  "C4",  "G4"),
    ("Perfect Fourth (P4)", 5,  "C4",  "F4"),
    ("Major Third (M3)",    4,  "C4",  "E4"),
    ("Minor Sixth (m6)",    8,  "C4",  "Ab4"),
    ("Tritone (TT)",        6,  "C4",  "Gb4"),
]

BASE_AMP = 0.35


def load_note(path: Path) -> np.ndarray:
    """Load a piano note, convert to mono, extract NOTE_DURATION seconds."""
    data, sr = sf.read(str(path))
    assert sr == SR, f"Expected {SR}Hz, got {sr}Hz"

    # Stereo → mono
    if data.ndim == 2:
        data = data.mean(axis=1)

    # Skip onset, take NOTE_DURATION
    start = int(ONSET_SKIP * SR)
    end = start + int(NOTE_DURATION * SR)
    segment = data[start:end]

    # Pad if too short
    if len(segment) < int(NOTE_DURATION * SR):
        segment = np.pad(segment, (0, int(NOTE_DURATION * SR) - len(segment)))

    # Fade in
    fade_in_samples = int(FADE_IN * SR)
    if fade_in_samples > 0:
        segment[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)

    # Fade out
    fade_out_samples = int(FADE_OUT * SR)
    if fade_out_samples > 0:
        segment[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)

    return segment


def main():
    script_dir = Path(__file__).resolve().parent
    weblab_dir = script_dir.parent
    exp_dir = weblab_dir / "experiments" / "BCH-R-Nucleus-Real"
    raw_dir = exp_dir / "raw_notes"

    gap = np.zeros(int(GAP_DURATION * SR))
    segments = []

    # Frequency references for markers
    FREQS = {
        "C4": 261.63, "E4": 329.63, "F4": 349.23,
        "Gb4": 369.99, "G4": 392.00, "Ab4": 415.30,
    }

    print("Assembling real piano dyads (University of Iowa MIS, mf):")
    print(f"  Duration per dyad: {NOTE_DURATION}s")
    print(f"  Gap: {GAP_DURATION}s")
    print()

    for i, (name, semitones, note1, note2) in enumerate(INTERVALS):
        print(f"  [{i+1}] {name:<24} {note1} + {note2}")

        tone1 = load_note(raw_dir / f"{note1}.aiff")
        tone2 = load_note(raw_dir / f"{note2}.aiff")

        # Mix at equal level
        dyad = (tone1 + tone2) / 2.0
        segments.append(dyad)

        if i < len(INTERVALS) - 1:
            segments.append(gap)

    audio = np.concatenate(segments)

    # Normalize
    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio / peak * BASE_AMP

    total_duration = len(audio) / SR
    print(f"\n  Total duration: {total_duration:.2f}s")
    print(f"  Total samples: {len(audio)}")

    # Save audio
    audio_path = exp_dir / "audio.wav"
    sf.write(str(audio_path), audio, SR, subtype="PCM_16")
    print(f"  Saved: {audio_path}")

    # Save interval markers
    markers = []
    t = 0.0
    for i, (name, semitones, note1, note2) in enumerate(INTERVALS):
        markers.append({
            "name": name,
            "semitones": semitones,
            "start_s": round(t, 3),
            "end_s": round(t + NOTE_DURATION, 3),
            "freq1": FREQS[note1],
            "freq2": FREQS[note2],
        })
        t += NOTE_DURATION
        if i < len(INTERVALS) - 1:
            t += GAP_DURATION

    markers_path = exp_dir / "interval_markers.json"
    markers_path.write_text(json.dumps(markers, indent=2))
    print(f"  Saved: {markers_path}")


if __name__ == "__main__":
    main()
