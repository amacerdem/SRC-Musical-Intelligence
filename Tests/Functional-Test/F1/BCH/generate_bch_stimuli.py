"""Generate BCH test stimuli — 23 MIDI audio files.

Targets BCH's theoretical predictions (Bidelman 2009/2013, Sethares 1993,
Plomp-Levelt 1965, Krumhansl 1990, Parncutt 1989) with:

  1. Consonance hierarchy: P1/P8/P5/P4/M3/m6/TT/m2 (8 intervals)
  2. Harmonicity: single tone, chord, cluster, octave (4 files)
  3. Tonal context: scale, chromatic, random, held chord (4 files)
  4. Spectral balance: low/mid/high register, wide spread (4 files)
  5. Temporal stability: held, progression, rapid changes (3 files)

All files rendered via FluidSynth + SoundFont, saved to
Tests/Functional-Test/F1/BCH/stimuli/
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Dict

import numpy as np
import soundfile as sf

# -- Add project root to path --
ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Tests" / "micro_beliefs"))

from real_audio_stimuli import (  # noqa: E402
    midi_note, midi_chord, midi_melody, midi_progression,
    PIANO,
    SAMPLE_RATE,
    C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5, A5, B5, C6,
)
import torch

OUT_DIR = pathlib.Path(__file__).resolve().parent / "stimuli"
OUT_DIR.mkdir(exist_ok=True)

METADATA: Dict[str, dict] = {}


def _save(name: str, audio_tensor, meta: dict):
    """Save WAV file + register metadata."""
    audio = audio_tensor.squeeze(0).numpy()
    path = OUT_DIR / f"{name}.wav"
    sf.write(str(path), audio, SAMPLE_RATE)
    METADATA[name] = meta
    print(f"  [{name}] {path.name} ({len(audio)/SAMPLE_RATE:.1f}s)")


DUR = 4.0  # seconds per stimulus

# ======================================================================
# GROUP 1: Consonance Hierarchy (8 intervals)
# Tests E2 (hierarchy = helmholtz × stumpf), P0, P1
# Hierarchy: P1 > P8 > P5 > P4 > M3 > m6 > TT > m2
# ======================================================================

print("GROUP 1: Consonance hierarchy intervals")

_save("g1_01_unison", midi_note(C4, DUR), {
    "group": "consonance", "interval": "P1_unison",
    "ratio": "1:1", "expected_E2": "highest — perfect consonance",
})

_save("g1_02_octave", midi_chord([C4, C5], DUR), {
    "group": "consonance", "interval": "P8_octave",
    "ratio": "2:1", "expected_E2": "very high — nearly perfect consonance",
})

_save("g1_03_fifth", midi_chord([C4, G4], DUR), {
    "group": "consonance", "interval": "P5_fifth",
    "ratio": "3:2", "expected_E2": "high",
})

_save("g1_04_fourth", midi_chord([C4, F4], DUR), {
    "group": "consonance", "interval": "P4_fourth",
    "ratio": "4:3", "expected_E2": "moderate-high",
})

_save("g1_05_major_3rd", midi_chord([C4, E4], DUR), {
    "group": "consonance", "interval": "M3_major_third",
    "ratio": "5:4", "expected_E2": "moderate",
})

_save("g1_06_minor_6th", midi_chord([C4, Ab4], DUR), {
    "group": "consonance", "interval": "m6_minor_sixth",
    "ratio": "8:5", "expected_E2": "moderate (inverted M3)",
})

_save("g1_07_tritone", midi_chord([C4, Gb4], DUR), {
    "group": "consonance", "interval": "TT_tritone",
    "ratio": "sqrt2:1", "expected_E2": "low — dissonant",
})

_save("g1_08_minor_2nd", midi_chord([C4, Db4], DUR), {
    "group": "consonance", "interval": "m2_minor_second",
    "ratio": "16:15", "expected_E2": "lowest — maximum dissonance",
})


# ======================================================================
# GROUP 2: Harmonicity (4 files)
# Tests E0 (nps), E1 (harmonicity)
# ======================================================================

print("GROUP 2: Harmonicity")

_save("g2_01_single_c4", midi_note(C4, DUR), {
    "group": "harmonicity", "pattern": "single",
    "expected_E1": "high — single harmonic series",
})

_save("g2_02_major_chord", midi_chord([C4, E4, G4], DUR), {
    "group": "harmonicity", "pattern": "major_chord",
    "expected_E1": "moderate — three aligned harmonic series",
})

_save("g2_03_cluster", midi_chord([C4, Db4, D4], DUR), {
    "group": "harmonicity", "pattern": "cluster",
    "expected_E1": "low — inharmonic interaction",
})

_save("g2_04_octave_dyad", midi_chord([C4, C5], DUR), {
    "group": "harmonicity", "pattern": "octave_dyad",
    "expected_E1": "high — perfectly harmonic relationship",
})


# ======================================================================
# GROUP 3: Tonal Context (4 files)
# Tests P3 (tonal_context), M2 (tonal_memory)
# ======================================================================

print("GROUP 3: Tonal context")

_save("g3_01_c_major_scale",
      midi_melody([C4, D4, E4, F4, G4, A4, B4, C5], [0.5] * 8), {
    "group": "tonal_context", "pattern": "c_major_scale",
    "expected_P3": "high — strong C major key context",
})

_save("g3_02_chromatic",
      midi_melody(list(range(C4, C5 + 1)), [0.3] * 13), {
    "group": "tonal_context", "pattern": "chromatic",
    "expected_P3": "low — ambiguous key",
})

rng = np.random.RandomState(42)
random_pitches = [int(p) for p in rng.choice(range(C4, C6), size=16)]
_save("g3_03_random",
      midi_melody(random_pitches, [0.3] * 16), {
    "group": "tonal_context", "pattern": "random",
    "expected_P3": "low — no key context",
})

_save("g3_04_c_major_held", midi_chord([C4, E4, G4], 5.0), {
    "group": "tonal_context", "pattern": "c_major_held",
    "expected_P3": "high — strong stable tonal context",
})


# ======================================================================
# GROUP 4: Spectral Balance (4 files)
# Tests M3 (spectral_memory), E1 tristimulus balance
# ======================================================================

print("GROUP 4: Spectral balance / register")

_save("g4_01_low_chord", midi_chord([C3, E3, G3], DUR), {
    "group": "spectral", "pattern": "low_register",
    "expected_M3": "warm, F0-heavy",
})

_save("g4_02_mid_chord", midi_chord([C4, E4, G4], DUR), {
    "group": "spectral", "pattern": "mid_register",
    "expected_M3": "balanced tristimulus",
})

_save("g4_03_high_chord", midi_chord([C5, E5, G5], DUR), {
    "group": "spectral", "pattern": "high_register",
    "expected_M3": "bright, high-partial heavy",
})

_save("g4_04_wide_spread", midi_chord([C3, G4, E5], DUR), {
    "group": "spectral", "pattern": "wide_spread",
    "expected_M3": "dispersed spectral energy",
})


# ======================================================================
# GROUP 5: Temporal Stability (3 files)
# Tests M0-M3 temporal integration stability
# ======================================================================

print("GROUP 5: Temporal stability")

_save("g5_01_stable_chord", midi_chord([C4, E4, G4], 5.0), {
    "group": "temporal", "pattern": "stable",
    "expected_M0": "high, stable — no harmonic change",
})

# I-IV-V-I progression
_save("g5_02_progression",
      midi_progression(
          [[C4, E4, G4], [F4, A4, C5], [G4, B4, D5], [C4, E4, G4]],
          [1.5, 1.5, 1.5, 1.5],
      ), {
    "group": "temporal", "pattern": "progression",
    "expected_M0": "moderate — changing but related chords",
})

# Rapid chord changes (consonant → dissonant → consonant ...)
rapid_chords = [[C4, E4, G4], [C4, Db4, D4]] * 6
_save("g5_03_rapid_changes",
      midi_progression(rapid_chords, [0.4] * len(rapid_chords)), {
    "group": "temporal", "pattern": "rapid_changes",
    "expected_M0": "variable — frequent consonance shifts",
})


# ======================================================================
# Save metadata
# ======================================================================

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nMetadata saved: {meta_path}")
print(f"Total stimuli: {len(METADATA)}")
