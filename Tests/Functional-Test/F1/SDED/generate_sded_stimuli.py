"""Generate SDED test stimuli — 22 MIDI audio files.

Targets SDED's theoretical predictions (Crespo-Bojorque 2018, Fishman 2001,
Bidelman 2013, Trulla 2018) with:

  1. Consonance hierarchy: unison → minor 2nd (6 intervals)
  2. Roughness gradation: single tone → dense cluster (4 files)
  3. Context deviation: sustained vs switching consonance/dissonance (4 files)
  4. Spectral density: single → 4-note cluster (4 files)
  5. Temporal patterns: sustained vs alternating chords (4 files)

All files rendered via FluidSynth + SoundFont, saved to
Tests/Functional-Test/F1/SDED/stimuli/
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


# ======================================================================
# GROUP 1: Consonance Hierarchy (6 files)
# Tests E0 ordering: dissonant > consonant
# References: Bidelman 2013 brainstem consonance, Fishman 2001 A1
# ======================================================================

print("GROUP 1: Consonance hierarchy")

DUR_CHORD = 4.0  # seconds per chord

_save("g1_01_single_c4", midi_note(C4, DUR_CHORD), {
    "group": "consonance", "interval": "unison",
    "notes": "C4 alone",
    "expected_E0": "low — single tone, minimal dissonance",
})

_save("g1_02_octave", midi_chord([C4, C5], DUR_CHORD), {
    "group": "consonance", "interval": "octave",
    "notes": "C4+C5 (2:1)",
    "expected_E0": "low — most consonant interval",
})

_save("g1_03_fifth", midi_chord([C4, G4], DUR_CHORD), {
    "group": "consonance", "interval": "fifth",
    "notes": "C4+G4 (3:2)",
    "expected_E0": "low-moderate — consonant",
})

_save("g1_04_fourth", midi_chord([C4, F4], DUR_CHORD), {
    "group": "consonance", "interval": "fourth",
    "notes": "C4+F4 (4:3)",
    "expected_E0": "moderate — consonant but less than fifth",
})

_save("g1_05_tritone", midi_chord([C4, Gb4], DUR_CHORD), {
    "group": "consonance", "interval": "tritone",
    "notes": "C4+Gb4 (sqrt2:1)",
    "expected_E0": "high — dissonant interval",
})

_save("g1_06_minor_2nd", midi_chord([C4, Db4], DUR_CHORD), {
    "group": "consonance", "interval": "minor_2nd",
    "notes": "C4+Db4 (16:15)",
    "expected_E0": "very high — maximum roughness/beating",
})


# ======================================================================
# GROUP 2: Roughness Gradation (4 files)
# Tests P0 (roughness_detection) ordering
# ======================================================================

print("GROUP 2: Roughness gradation")

_save("g2_01_single", midi_note(C4, DUR_CHORD), {
    "group": "roughness", "pattern": "single",
    "expected_P0": "low — no inter-note roughness",
})

_save("g2_02_major_3rd", midi_chord([C4, E4], DUR_CHORD), {
    "group": "roughness", "pattern": "major_3rd",
    "expected_P0": "moderate — consonant dyad",
})

_save("g2_03_major_7th", midi_chord([C4, B4], DUR_CHORD), {
    "group": "roughness", "pattern": "major_7th",
    "expected_P0": "high — dissonant dyad with beating",
})

_save("g2_04_cluster", midi_chord([C4, Db4, D4], DUR_CHORD), {
    "group": "roughness", "pattern": "cluster",
    "expected_P0": "very high — three adjacent semitones",
})


# ======================================================================
# GROUP 3: Context Deviation (4 files)
# Tests P1 (deviation_detection = |roughness_h0 - roughness_mean|)
# ======================================================================

print("GROUP 3: Context deviation")

_save("g3_01_consonant_sustained",
      midi_chord([C4, E4, G4], 5.0), {
    "group": "context", "pattern": "consonant_sustained",
    "expected_P1": "low — stable context, no deviation",
})

_save("g3_02_dissonant_sustained",
      midi_chord([C4, Db4, D4], 5.0), {
    "group": "context", "pattern": "dissonant_sustained",
    "expected_P1": "low — dissonant but stable context",
})

# Consonant → Dissonant switch: C major chord then cluster
cons_audio = midi_chord([C4, E4, G4], 2.5)
diss_audio = midi_chord([C4, Db4, D4], 2.5)
_save("g3_03_consonant_to_dissonant",
      torch.cat([cons_audio, diss_audio], dim=-1), {
    "group": "context", "pattern": "consonant_to_dissonant",
    "expected_P1": "spike at transition — roughness deviation",
})

# Dissonant → Consonant switch
_save("g3_04_dissonant_to_consonant",
      torch.cat([diss_audio, cons_audio], dim=-1), {
    "group": "context", "pattern": "dissonant_to_consonant",
    "expected_P1": "spike at transition — roughness deviation",
})


# ======================================================================
# GROUP 4: Spectral Density (4 files)
# Tests E0 response to increasing note density
# ======================================================================

print("GROUP 4: Spectral density")

_save("g4_01_single", midi_note(C4, DUR_CHORD), {
    "group": "density", "pattern": "single",
    "notes": "C4",
    "expected_E0": "low — single tone baseline",
})

_save("g4_02_dyad", midi_chord([C4, G4], DUR_CHORD), {
    "group": "density", "pattern": "dyad",
    "notes": "C4+G4 (consonant dyad)",
    "expected_E0": "low-moderate",
})

_save("g4_03_triad", midi_chord([C4, E4, G4], DUR_CHORD), {
    "group": "density", "pattern": "triad",
    "notes": "C4+E4+G4 (major triad)",
    "expected_E0": "moderate — more harmonic interaction",
})

_save("g4_04_dense_cluster",
      midi_chord([C4, Db4, D4, Eb4], DUR_CHORD), {
    "group": "density", "pattern": "dense_cluster",
    "notes": "C4+Db4+D4+Eb4 (4 adjacent semitones)",
    "expected_E0": "very high — maximal roughness",
})


# ======================================================================
# GROUP 5: Temporal Patterns (4 files)
# Tests temporal integration: E0 variance, M0 tracking
# ======================================================================

print("GROUP 5: Temporal patterns")

# Consonant chord held
_save("g5_01_consonant_held", midi_chord([C4, E4, G4], 5.0), {
    "group": "temporal", "pattern": "consonant_held",
    "expected_E0_var": "low — stable",
})

# Repeated consonant chords (arpeggiated)
arp_notes = [C4, E4, G4, C5, G4, E4] * 3
_save("g5_02_consonant_arpeggio",
      midi_melody(arp_notes, [0.3] * len(arp_notes)), {
    "group": "temporal", "pattern": "consonant_arpeggio",
    "expected_E0_var": "moderate — note onsets",
})

# Dissonant chord held
_save("g5_03_dissonant_held", midi_chord([C4, Db4, D4], 5.0), {
    "group": "temporal", "pattern": "dissonant_held",
    "expected_E0_var": "low — stable (but higher mean than consonant)",
})

# Alternating consonant/dissonant chords
alt_chords = [[C4, E4, G4], [C4, Db4, D4]] * 4
alt_durs = [0.6] * len(alt_chords)
_save("g5_04_alternating", midi_progression(alt_chords, alt_durs), {
    "group": "temporal", "pattern": "alternating",
    "expected_E0_var": "high — switching between consonant/dissonant",
    "expected_P1": "high — frequent context deviation",
})


# ======================================================================
# Save metadata
# ======================================================================

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nMetadata saved: {meta_path}")
print(f"Total stimuli: {len(METADATA)}")
