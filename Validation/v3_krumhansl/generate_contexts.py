"""Generate tonal context stimuli for Krumhansl profile extraction.

Two stimulus types:
1. Simultaneous: Tonic chord + probe tone sounding together (2s).
   BCH consonance directly measures how well each probe fits the key.
2. Sequential: I-IV-V-I cadence (3s) → silence (0.5s) → probe (1s).
   Traditional probe-tone paradigm for cognitive/predictive measures.

The simultaneous design is preferred because BCH consonance hierarchy
(Sethares 1993 + Plomp-Levelt) directly captures the acoustic basis of
tonal stability that underlies Krumhansl-Kessler profiles.
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Tuple

import numpy as np

from Validation.config.constants import SAMPLE_RATE
from Validation.config.paths import KRUMHANSL_DIR


# ── Frequency table (equal temperament, A4=440Hz) ──

def _midi_to_freq(midi_note: int) -> float:
    """Convert MIDI note number to frequency."""
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


# C4=60, C#4=61, ..., B4=71
PROBE_FREQUENCIES = {i: _midi_to_freq(60 + i) for i in range(12)}


def generate_tonal_context(
    key: str = "C",
    mode: str = "major",
    context_duration_s: float = 3.0,
    probe_duration_s: float = 2.0,
    sr: int = SAMPLE_RATE,
    output_dir: Path | None = None,
) -> List[Tuple[int, Path]]:
    """Generate 12 stimuli with probe tone over tonic chord.

    Each stimulus:
      [I-IV-V-I cadence (3s)]  → establishes tonal context
      [tonic chord + probe tone (2s)] → BCH measures consonance fit

    The probe tone is mixed with the sustained tonic chord so that BCH
    consonance directly captures how consonant each probe is within the key.

    Args:
        key: Root pitch class.
        mode: 'major' or 'minor'.
        context_duration_s: Duration of cadence context.
        probe_duration_s: Duration of chord+probe overlay.
        sr: Sample rate.
        output_dir: Directory for output WAV files.

    Returns:
        List of (pitch_class_index, wav_path) tuples.
    """
    import soundfile as sf

    if output_dir is None:
        output_dir = KRUMHANSL_DIR / f"{key}_{mode}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Key offset
    key_map = {
        "C": 0, "C#": 1, "Db": 1, "D": 2, "D#": 3, "Eb": 3,
        "E": 4, "F": 5, "F#": 6, "Gb": 6, "G": 7, "G#": 8,
        "Ab": 8, "A": 9, "A#": 10, "Bb": 10, "B": 11,
    }
    root_offset = key_map.get(key, 0)

    # Build cadence context
    context = _generate_cadence(root_offset, mode, context_duration_s, sr)

    # Tonic chord intervals
    if mode == "major":
        tonic_intervals = [0, 4, 7]   # I: root, M3, P5
    else:
        tonic_intervals = [0, 3, 7]   # i: root, m3, P5

    results = []
    for pc in range(12):
        # Tonic chord sustained during probe
        tonic_chord = np.zeros(int(probe_duration_s * sr), dtype=np.float32)
        for semitone in tonic_intervals:
            midi = 60 + root_offset + semitone
            freq = _midi_to_freq(midi)
            tonic_chord += _generate_tone(freq, probe_duration_s, sr, amplitude=0.25)

        # Probe tone (higher amplitude to be salient above chord)
        probe_freq = PROBE_FREQUENCIES[(pc + root_offset) % 12]
        probe = _generate_tone(probe_freq, probe_duration_s, sr, amplitude=0.4)

        # Mix: tonic chord + probe simultaneously
        probe_section = tonic_chord + probe

        # Small gap between cadence and probe section
        gap = np.zeros(int(0.2 * sr), dtype=np.float32)

        # Concatenate: cadence context + gap + simultaneous chord+probe
        stimulus = np.concatenate([context, gap, probe_section])

        # Normalize
        peak = np.abs(stimulus).max()
        if peak > 0:
            stimulus = stimulus / peak * 0.9

        # Save
        filename = f"probe_{pc:02d}.wav"
        path = output_dir / filename
        sf.write(str(path), stimulus, sr)
        results.append((pc, path))

    return results


def generate_all_contexts(
    keys: List[str] | None = None,
    modes: List[str] | None = None,
) -> dict[str, List[Tuple[int, Path]]]:
    """Generate probe stimuli for multiple keys.

    Args:
        keys: List of key names (default: ['C']).
        modes: List of modes (default: ['major', 'minor']).

    Returns:
        Dict mapping 'key_mode' to list of (pc, path) tuples.
    """
    if keys is None:
        keys = ["C"]
    if modes is None:
        modes = ["major", "minor"]

    all_results = {}
    for key in keys:
        for mode in modes:
            label = f"{key}_{mode}"
            all_results[label] = generate_tonal_context(key, mode)
    return all_results


def _generate_tone(
    freq: float,
    duration_s: float,
    sr: int,
    amplitude: float = 0.5,
) -> np.ndarray:
    """Generate a complex tone (fundamental + harmonics) for more natural timbre."""
    t = np.arange(int(duration_s * sr)) / sr

    # Fundamental + 3 harmonics with decreasing amplitude
    signal = amplitude * np.sin(2 * np.pi * freq * t)
    signal += amplitude * 0.5 * np.sin(2 * np.pi * 2 * freq * t)
    signal += amplitude * 0.25 * np.sin(2 * np.pi * 3 * freq * t)
    signal += amplitude * 0.125 * np.sin(2 * np.pi * 4 * freq * t)

    # Apply ADSR envelope
    attack = int(0.01 * sr)
    decay = int(0.05 * sr)
    release = int(0.1 * sr)
    env = np.ones(len(t), dtype=np.float32)
    env[:attack] = np.linspace(0, 1, attack)
    env[attack:attack + decay] = np.linspace(1, 0.7, decay)
    env[-release:] = np.linspace(0.7, 0, release)

    return (signal * env).astype(np.float32)


def _generate_cadence(
    root_offset: int,
    mode: str,
    duration_s: float,
    sr: int,
) -> np.ndarray:
    """Generate a I-IV-V-I cadence to establish tonal context."""
    chord_dur = duration_s / 4.0

    if mode == "major":
        # I (root, M3, P5), IV (P4, M6, root+8), V (P5, M7, root+9), I
        chord_intervals = [
            [0, 4, 7],      # I
            [5, 9, 12],     # IV
            [7, 11, 14],    # V
            [0, 4, 7],      # I
        ]
    else:
        # i (root, m3, P5), iv (P4, m6, root+8), V (P5, M7, root+9), i
        chord_intervals = [
            [0, 3, 7],      # i
            [5, 8, 12],     # iv
            [7, 11, 14],    # V (major V in minor)
            [0, 3, 7],      # i
        ]

    parts = []
    for intervals in chord_intervals:
        chord = np.zeros(int(chord_dur * sr), dtype=np.float32)
        for semitone in intervals:
            midi = 60 + root_offset + semitone
            freq = _midi_to_freq(midi)
            chord += _generate_tone(freq, chord_dur, sr, amplitude=0.3)
        parts.append(chord)

    return np.concatenate(parts)
