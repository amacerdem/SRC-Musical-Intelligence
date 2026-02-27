"""Generate MIAA test stimuli — 17 MIDI audio files.

Targets MIAA's theoretical predictions (Kraemer 2005, Halpern 2004,
Di Liberto 2021) with:

  1. Tonal quality: single → cluster (4 files)
  2. Register/Timbre: C3 → C6 (3 files)
  3. Temporal/Phrase: sustained → alternating (4 files)
  4. Complexity/Density: single → dense cluster (4 files)
  5. Instrument contrast: piano vs organ (2 files)

All files rendered via FluidSynth + SoundFont, saved to
Tests/Functional-Test/F1/MIAA/stimuli/
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
    PIANO, ORGAN,
    SAMPLE_RATE,
    C3, E3, G3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, A4, B4,
    C5, E5, G5, C6,
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


# ======================================================================
# GROUP 1: Tonal Quality (4 files)
# Tests E0 imagery activation & E1 familiarity across tonal clarity
# References: Kraemer 2005 — AC active during imagery for tonal music
# ======================================================================

print("GROUP 1: Tonal quality")
DUR = 4.0

_save("g1_01_single", midi_note(C4, DUR), {
    "group": "tonal", "pattern": "single",
    "notes": "C4 alone",
    "expected": "high E0 — clear tonal input, high tonalness",
})

_save("g1_02_fifth", midi_chord([C4, G4], DUR), {
    "group": "tonal", "pattern": "fifth",
    "notes": "C4+G4 (3:2)",
    "expected": "high E0 — consonant, tonal",
})

_save("g1_03_triad", midi_chord([C4, E4, G4], DUR), {
    "group": "tonal", "pattern": "triad",
    "notes": "C4+E4+G4 major triad",
    "expected": "high E0 — familiar harmonic pattern",
})

_save("g1_04_cluster", midi_chord([C4, Db4, D4], DUR), {
    "group": "tonal", "pattern": "cluster",
    "notes": "C4+Db4+D4 semitone cluster",
    "expected": "moderate E0 — less tonal clarity",
})


# ======================================================================
# GROUP 2: Register/Timbre (3 files)
# Tests tristimulus balance variation across register
# References: Pollard & Jansson 1982 — tristimulus harmonic energy
# ======================================================================

print("GROUP 2: Register")

_save("g2_01_low_c3", midi_note(C3, DUR), {
    "group": "register", "pattern": "low",
    "notes": "C3 (130 Hz)",
    "expected": "strong fundamental, unbalanced tristimulus",
})

_save("g2_02_mid_c4", midi_note(C4, DUR), {
    "group": "register", "pattern": "mid",
    "notes": "C4 (262 Hz)",
    "expected": "balanced tristimulus, standard register",
})

_save("g2_03_high_c6", midi_note(C6, DUR), {
    "group": "register", "pattern": "high",
    "notes": "C6 (1047 Hz)",
    "expected": "less harmonic content, fundamental dominant",
})


# ======================================================================
# GROUP 3: Temporal/Phrase (4 files)
# Tests P2 phrase structure via spectral flux entropy
# References: Di Liberto 2021 — imagery pitch at sub-1Hz phrase rate
# ======================================================================

print("GROUP 3: Temporal/Phrase")

_save("g3_01_sustained", midi_chord([C4, E4, G4], 5.0), {
    "group": "temporal", "pattern": "sustained",
    "expected_P2_var": "low — stable spectrum, no transitions",
})

melody_notes = [C4, E4, G4, C5, G4, E4, C4, E4]
melody_durs = [0.5] * len(melody_notes)
_save("g3_02_melody", midi_melody(melody_notes, melody_durs), {
    "group": "temporal", "pattern": "melody",
    "expected_P2_var": "moderate — note onsets cause spectral flux",
})

prog_chords = [[C4, E4, G4], [F4, A4, C5], [G4, B4, D4+12], [C4, E4, G4]]
prog_durs = [1.25] * 4
_save("g3_03_chord_progression", midi_progression(prog_chords, prog_durs), {
    "group": "temporal", "pattern": "chord_progression",
    "expected_P2_var": "moderate — chord transitions",
})

arp_notes = [C4, E4, G4, C5, G4, E4] * 4
arp_durs = [0.2] * len(arp_notes)
_save("g3_04_arpeggio", midi_melody(arp_notes, arp_durs), {
    "group": "temporal", "pattern": "arpeggio",
    "expected_P2_var": "high — rapid note changes",
})


# ======================================================================
# GROUP 4: Density/Complexity (4 files)
# Tests imagery activation across note density
# References: Halpern 2004 — perception-imagery overlap r=0.84
# ======================================================================

print("GROUP 4: Density")

_save("g4_01_single", midi_note(C4, DUR), {
    "group": "density", "pattern": "single",
    "notes": "C4",
    "expected": "clear single tone baseline",
})

_save("g4_02_dyad", midi_chord([C4, E4], DUR), {
    "group": "density", "pattern": "dyad",
    "notes": "C4+E4 (major 3rd)",
    "expected": "consonant dyad",
})

_save("g4_03_triad", midi_chord([C4, E4, G4], DUR), {
    "group": "density", "pattern": "triad",
    "notes": "C4+E4+G4 (major triad)",
    "expected": "familiar harmonic pattern",
})

_save("g4_04_dense_cluster", midi_chord([C4, Db4, D4, Eb4], DUR), {
    "group": "density", "pattern": "dense_cluster",
    "notes": "C4+Db4+D4+Eb4 (4 adjacent semitones)",
    "expected": "maximal roughness, reduced tonal clarity",
})


# ======================================================================
# GROUP 5: Instrument Contrast (2 files)
# Tests E2 a1_modulation (instrumental > lyrics; different timbres)
# References: Kraemer 2005 — A1 modulation differs by instrument type
# ======================================================================

print("GROUP 5: Instrument contrast")

_save("g5_01_piano_c4", midi_note(C4, DUR, program=PIANO), {
    "group": "instrument", "pattern": "piano",
    "notes": "C4 piano",
    "expected": "baseline piano timbre",
})

_save("g5_02_organ_c4", midi_note(C4, DUR, program=ORGAN), {
    "group": "instrument", "pattern": "organ",
    "notes": "C4 organ",
    "expected": "sustained organ — different harmonic structure",
})


# ======================================================================
# Save metadata
# ======================================================================

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nMetadata saved: {meta_path}")
print(f"Total stimuli: {len(METADATA)}")
