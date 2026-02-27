"""Generate MPG test stimuli — 24 MIDI audio files.

Targets MPG's theoretical predictions (Rupp 2022, Patterson 2002,
Norman-Haignere 2013, Briley 2013, Cheung 2019) with:

  1. Contour patterns: sustained, scale, chromatic, arpeggio, random
  2. Onset patterns: single, regular, fast, irregular
  3. Phrase boundaries: rest gaps, direction changes
  4. Gradient balance: onset-dominant vs contour-dominant
  5. Register: low, mid, high melodies
  6. Complexity: simple to complex melodic material

All files rendered via FluidSynth + SoundFont, saved to
Tests/Functional-Test/F1/MPG/stimuli/
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Dict, List

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


# ======================================================================
# GROUP 1: Contour Patterns (8 files)
# Tests E1 (sequence_anterior), E2 (contour_complexity)
# ======================================================================

print("GROUP 1: Contour patterns")

# Sustained C4 — no contour at all
_save("g1_01_sustained_c4", midi_note(C4, 6.0), {
    "group": "contour",
    "pattern": "sustained", "notes": "C4 held 6s",
    "expected_E1": "low — no pitch change",
    "expected_E2": "low — no contour complexity",
    "expected_E3": "high — onset dominant (no anterior activity)",
})

# Ascending C major scale C4→C5
_save("g1_02_ascending_scale",
      midi_melody([C4, D4, E4, F4, G4, A4, B4, C5], [0.5]*8), {
    "group": "contour",
    "pattern": "ascending_scale", "notes": "C4-D4-E4-F4-G4-A4-B4-C5",
    "expected_E1": "high — continuous pitch change",
    "expected_E2": "moderate — regular steps",
})

# Descending C major scale C5→C4
_save("g1_03_descending_scale",
      midi_melody([C5, B4, A4, G4, F4, E4, D4, C4], [0.5]*8), {
    "group": "contour",
    "pattern": "descending_scale",
    "expected_E1": "high — continuous pitch change (direction reversed)",
})

# Repeated C4 — onset but no pitch change
_save("g1_04_repeated_c4",
      midi_melody([C4]*12, [0.4]*12), {
    "group": "contour",
    "pattern": "repeated", "notes": "C4 x 12",
    "expected_E1": "low — no pitch change despite onsets",
    "expected_E3": "very high — onset dominant (E0 >> E1)",
})

# Large leaps — C4→C6→C4→C6→C4→C6
_save("g1_05_large_leaps",
      midi_melody([C4, C6, C4, C6, C4, C6], [0.6]*6), {
    "group": "contour",
    "pattern": "large_leaps", "notes": "C4-C6-C4-C6-C4-C6",
    "expected_E1": "very high — dramatic pitch change",
    "expected_E2": "high — large interval complexity",
})

# Chromatic ascending — C4→Db4→D4→Eb4→...→C5
_save("g1_06_chromatic_asc",
      midi_melody(list(range(C4, C5 + 1)), [0.3]*13), {
    "group": "contour",
    "pattern": "chromatic_ascending",
    "expected_E2": "high — many small, regular steps",
})

# Arpeggio — C4-E4-G4-C5-G4-E4-C4 repeated
arp_notes = [C4, E4, G4, C5, G4, E4, C4, C4, E4, G4, C5, G4, E4, C4]
_save("g1_07_arpeggio",
      midi_melody(arp_notes, [0.35]*len(arp_notes)), {
    "group": "contour",
    "pattern": "arpeggio", "notes": "C4-E4-G4-C5 up and down, repeated",
    "expected_E1": "high — continuous pitch change",
})

# Pseudo-random melody — unpredictable pitch pattern
rng = np.random.RandomState(42)
random_pitches = [int(p) for p in rng.choice(range(C4, C6), size=16)]
_save("g1_08_random_melody",
      midi_melody(random_pitches, [0.3]*16), {
    "group": "contour",
    "pattern": "random",
    "expected_E2": "very high — maximal unpredictability",
})


# ======================================================================
# GROUP 2: Onset Patterns (4 files)
# Tests E0 (onset_posterior), M1 (posterior_activity)
# ======================================================================

print("GROUP 2: Onset patterns")

# Single onset — one note held
_save("g2_01_single_onset", midi_note(C4, 6.0), {
    "group": "onset",
    "pattern": "single_onset",
    "expected_E0": "spike at start then low",
    "expected_M1": "spike at start then low",
})

# Regular quarter-note onsets (~2 Hz)
_save("g2_02_regular_onsets",
      midi_melody([C4, E4, G4, C5, E5]*3, [0.5]*15), {
    "group": "onset",
    "pattern": "regular",
    "expected_E0": "regular spikes every 0.5s",
})

# Fast 16th-note onsets (~4 Hz)
fast_notes = [C4, D4, E4, F4, G4, A4, B4, C5]*3
_save("g2_03_fast_onsets",
      midi_melody(fast_notes, [0.2]*len(fast_notes)), {
    "group": "onset",
    "pattern": "fast",
    "expected_E0": "dense onset activity",
})

# Irregular onsets — mixed durations
irreg_durs = [0.8, 0.2, 0.5, 0.3, 1.0, 0.15, 0.6, 0.4, 0.2, 0.7]
irreg_notes = [C4, E4, D4, G4, F4, A4, G4, B4, C5, E4]
_save("g2_04_irregular_onsets",
      midi_melody(irreg_notes, irreg_durs), {
    "group": "onset",
    "pattern": "irregular",
    "expected_E0": "irregular onset pattern",
    "expected_F0": "higher — periodicity breaks",
})


# ======================================================================
# GROUP 3: Phrase Boundaries (4 files)
# Tests F0 (phrase_boundary_pred)
# ======================================================================

print("GROUP 3: Phrase boundaries")

# Phrase with rest — melody, 1s rest, melody
phrase1 = midi_melody([C4, D4, E4, F4, G4], [0.4]*5)
# Create audio with gap in the middle
import torch
gap = torch.zeros(1, int(1.0 * SAMPLE_RATE))  # 1s silence
phrase2 = midi_melody([A4, G4, F4, E4, D4, C4], [0.4]*6)
combined = torch.cat([phrase1, gap, phrase2], dim=-1)
_save("g3_01_phrase_with_rest", combined, {
    "group": "phrase_boundary",
    "pattern": "phrase_rest_phrase",
    "expected_F0": "peak during rest gap (phrase boundary)",
})

# Continuous melody — no gaps
cont_notes = [C4, D4, E4, F4, G4, A4, B4, C5, B4, A4, G4, F4, E4, D4, C4]
_save("g3_02_continuous_melody",
      midi_melody(cont_notes, [0.35]*len(cont_notes)), {
    "group": "phrase_boundary",
    "pattern": "continuous",
    "expected_F0": "low — no boundary within continuous melody",
})

# Direction change — ascending then descending
dir_notes = [C4, D4, E4, F4, G4, A4, B4, C5, B4, A4, G4, F4, E4, D4, C4]
_save("g3_03_direction_change",
      midi_melody(dir_notes, [0.35]*len(dir_notes)), {
    "group": "phrase_boundary",
    "pattern": "direction_change",
    "expected_F0": "moderate peak at contour apex (C5)",
})

# Two distinct phrases with long rest
p1 = midi_melody([C4, E4, G4, C5], [0.4]*4)
gap2 = torch.zeros(1, int(1.5 * SAMPLE_RATE))
p2 = midi_melody([A4, F4, D4, G3], [0.4]*4)
_save("g3_04_two_phrases", torch.cat([p1, gap2, p2], dim=-1), {
    "group": "phrase_boundary",
    "pattern": "two_phrases",
    "expected_F0": "strong peak during 1.5s rest",
})


# ======================================================================
# GROUP 4: Gradient Balance (4 files)
# Tests E3 (gradient_ratio = E0/(E0+E1))
# ======================================================================

print("GROUP 4: Gradient balance")

# Onset dominant — repeated same pitch (high E0, low E1)
_save("g4_01_onset_dominant",
      midi_melody([E4]*16, [0.25]*16), {
    "group": "gradient_balance",
    "pattern": "repeated_fast",
    "expected_E3": "high — E0 >> E1 (onsets without pitch change)",
})

# Contour dominant — slow large pitch changes (low onset rate, high pitch change)
_save("g4_02_contour_dominant",
      midi_melody([C3, C5, C3, C5], [1.2]*4), {
    "group": "gradient_balance",
    "pattern": "slow_leaps",
    "expected_E3": "lower — E1 relatively higher from large pitch changes",
})

# Balanced — regular scale with regular onsets
_save("g4_03_balanced",
      midi_melody([C4, D4, E4, F4, G4, A4, B4, C5]*2, [0.35]*16), {
    "group": "gradient_balance",
    "pattern": "scale",
    "expected_E3": "moderate — both onset and contour active",
})

# Static chord — minimal both onset and contour
_save("g4_04_static_chord", midi_chord([C4, E4, G4], 5.0), {
    "group": "gradient_balance",
    "pattern": "static_chord",
    "expected_E0": "low after onset — no ongoing onsets",
    "expected_E1": "low — no pitch change",
})


# ======================================================================
# GROUP 5: Register (4 files)
# Tests pitch height influence on E1, E2
# ======================================================================

print("GROUP 5: Register")

_save("g5_01_melody_low",
      midi_melody([C3, D3, E3, F3, G3, A3, B3, 60], [0.5]*8), {
    "group": "register",
    "pattern": "scale_low",
    "notes": "C3-C4 ascending",
})

_save("g5_02_melody_mid",
      midi_melody([C4, D4, E4, F4, G4, A4, B4, C5], [0.5]*8), {
    "group": "register",
    "pattern": "scale_mid",
    "notes": "C4-C5 ascending",
})

_save("g5_03_melody_high",
      midi_melody([C5, D5, E5, F5, G5, A5, B5, C6], [0.5]*8), {
    "group": "register",
    "pattern": "scale_high",
    "notes": "C5-C6 ascending",
})

# Same contour, different register — tests invariance
_save("g5_04_contour_invariant",
      midi_melody([C3, E3, G3, C3, E3, G3, C3, E3, G3], [0.4]*9), {
    "group": "register",
    "pattern": "arpeggio_low",
    "expected": "E1/E2 similar to mid register arpeggio",
})


# ======================================================================
# Save metadata
# ======================================================================

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nMetadata saved: {meta_path}")
print(f"Total stimuli: {len(METADATA)}")
