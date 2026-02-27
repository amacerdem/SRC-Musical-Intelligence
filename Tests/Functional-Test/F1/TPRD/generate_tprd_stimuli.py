"""Generate TPRD test stimuli — 16 MIDI audio files.

Targets TPRD's theoretical predictions (Briley 2013, Norman-Haignere 2013,
Fishman 2001, Basinski 2025) with:

  1. Consonance hierarchy: single → minor 2nd (6 files)
  2. Complexity/Density: single → dense cluster (4 files)
  3. Register: C3 → C6 (3 files)
  4. Temporal: sustained → arpeggio (3 files)

All files rendered via FluidSynth + SoundFont, saved to
Tests/Functional-Test/F1/TPRD/stimuli/
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Dict

import numpy as np
import soundfile as sf

ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Tests" / "micro_beliefs"))

from real_audio_stimuli import (  # noqa: E402
    midi_note, midi_chord, midi_melody, midi_progression,
    PIANO,
    SAMPLE_RATE,
    C3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, A4, B4,
    C5, G5, C6,
)
import torch

OUT_DIR = pathlib.Path(__file__).resolve().parent / "stimuli"
OUT_DIR.mkdir(exist_ok=True)

METADATA: Dict[str, dict] = {}


def _save(name: str, audio_tensor, meta: dict):
    audio = audio_tensor.squeeze(0).numpy()
    path = OUT_DIR / f"{name}.wav"
    sf.write(str(path), audio, SAMPLE_RATE)
    METADATA[name] = meta
    print(f"  [{name}] {path.name} ({len(audio)/SAMPLE_RATE:.1f}s)")


DUR = 4.0

# ======================================================================
# GROUP 1: Consonance Hierarchy (6 files)
# Tests T0 (tonotopic) vs T1 (pitch) dissociation
# Briley 2013: medial HG = tonotopic, lateral HG = pitch
# ======================================================================

print("GROUP 1: Consonance hierarchy")

_save("g1_01_single", midi_note(C4, DUR), {
    "group": "consonance", "interval": "unison",
    "notes": "C4 alone",
    "expected": "T1 dominant — clear pitch, minimal roughness",
})

_save("g1_02_octave", midi_chord([C4, C5], DUR), {
    "group": "consonance", "interval": "octave",
    "notes": "C4+C5 (2:1)",
    "expected": "T1 dominant — most consonant interval",
})

_save("g1_03_fifth", midi_chord([C4, G4], DUR), {
    "group": "consonance", "interval": "fifth",
    "notes": "C4+G4 (3:2)",
    "expected": "T1 dominant — consonant",
})

_save("g1_04_tritone", midi_chord([C4, Gb4], DUR), {
    "group": "consonance", "interval": "tritone",
    "notes": "C4+Gb4 (sqrt2:1)",
    "expected": "more balanced T0/T1 — dissonant",
})

_save("g1_05_minor_2nd", midi_chord([C4, Db4], DUR), {
    "group": "consonance", "interval": "minor_2nd",
    "notes": "C4+Db4 (16:15)",
    "expected": "T0 increases — maximum roughness/beating",
})

_save("g1_06_major_7th", midi_chord([C4, B4], DUR), {
    "group": "consonance", "interval": "major_7th",
    "notes": "C4+B4 (15:8)",
    "expected": "T0 increases — dissonant with beating",
})


# ======================================================================
# GROUP 2: Complexity/Density (4 files)
# Tests dissociation index across note density
# ======================================================================

print("GROUP 2: Complexity")

_save("g2_01_single", midi_note(C4, DUR), {
    "group": "complexity", "pattern": "single",
    "notes": "C4",
})

_save("g2_02_dyad", midi_chord([C4, G4], DUR), {
    "group": "complexity", "pattern": "dyad",
    "notes": "C4+G4 (consonant)",
})

_save("g2_03_triad", midi_chord([C4, E4, G4], DUR), {
    "group": "complexity", "pattern": "triad",
    "notes": "C4+E4+G4 (major triad)",
})

_save("g2_04_dense", midi_chord([C4, Db4, D4, Eb4], DUR), {
    "group": "complexity", "pattern": "dense",
    "notes": "C4+Db4+D4+Eb4 (4 adjacent semitones)",
})


# ======================================================================
# GROUP 3: Register (3 files)
# Tests tonotopic encoding across frequency range
# ======================================================================

print("GROUP 3: Register")

_save("g3_01_low", midi_note(C3, DUR), {
    "group": "register", "notes": "C3 (130 Hz)",
})

_save("g3_02_mid", midi_note(C4, DUR), {
    "group": "register", "notes": "C4 (262 Hz)",
})

_save("g3_03_high", midi_note(C6, DUR), {
    "group": "register", "notes": "C6 (1047 Hz)",
})


# ======================================================================
# GROUP 4: Temporal (3 files)
# Tests dissociation stability over time
# ======================================================================

print("GROUP 4: Temporal")

_save("g4_01_sustained", midi_chord([C4, E4, G4], 5.0), {
    "group": "temporal", "pattern": "sustained",
})

melody_notes = [C4, E4, G4, C5, G4, E4, C4, E4]
_save("g4_02_melody", midi_melody(melody_notes, [0.5]*8), {
    "group": "temporal", "pattern": "melody",
})

arp_notes = [C4, E4, G4, C5, G4, E4] * 4
_save("g4_03_arpeggio", midi_melody(arp_notes, [0.2]*24), {
    "group": "temporal", "pattern": "arpeggio",
})


# ======================================================================
# Save metadata
# ======================================================================

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nMetadata saved: {meta_path}")
print(f"Total stimuli: {len(METADATA)}")
