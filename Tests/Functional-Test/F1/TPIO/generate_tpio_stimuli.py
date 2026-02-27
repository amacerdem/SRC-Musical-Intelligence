"""Generate TPIO test stimuli — 18 MIDI audio files.

Targets TPIO's theoretical predictions (Halpern 2004, Zatorre 2005,
Crowder 1989, McAdams 1999) with:

  1. Tonal quality: single → cluster (4 files)
  2. Register: C3 → C6 (3 files)
  3. Instrument contrast: piano/organ/violin/flute (4 files)
  4. Temporal: sustained → arpeggio (4 files)
  5. Timbre change: static → rapid alternation (3 files)

All files rendered via FluidSynth + SoundFont, saved to
Tests/Functional-Test/F1/TPIO/stimuli/
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
    PIANO, ORGAN, VIOLIN, FLUTE,
    SAMPLE_RATE,
    C3, E3, G3,
    C4, Db4, D4, Eb4, E4, F4, G4, A4, B4,
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


DUR = 4.0

# ======================================================================
# GROUP 1: Tonal Quality (4 files)
# Tests f01 (perception substrate) and f03 (overlap)
# ======================================================================

print("GROUP 1: Tonal quality")

_save("g1_01_single", midi_note(C4, DUR), {
    "group": "tonal", "pattern": "single",
    "notes": "C4 alone",
})

_save("g1_02_fifth", midi_chord([C4, G4], DUR), {
    "group": "tonal", "pattern": "fifth",
    "notes": "C4+G4 (3:2)",
})

_save("g1_03_triad", midi_chord([C4, E4, G4], DUR), {
    "group": "tonal", "pattern": "triad",
    "notes": "C4+E4+G4 major triad",
})

_save("g1_04_cluster", midi_chord([C4, Db4, D4], DUR), {
    "group": "tonal", "pattern": "cluster",
    "notes": "C4+Db4+D4 semitone cluster",
})


# ======================================================================
# GROUP 2: Register (3 files)
# Tests warmth/sharpness variation across pitch range
# ======================================================================

print("GROUP 2: Register")

_save("g2_01_low_c3", midi_note(C3, DUR), {
    "group": "register", "pattern": "low",
    "notes": "C3 (130 Hz)",
})

_save("g2_02_mid_c4", midi_note(C4, DUR), {
    "group": "register", "pattern": "mid",
    "notes": "C4 (262 Hz)",
})

_save("g2_03_high_c6", midi_note(C6, DUR), {
    "group": "register", "pattern": "high",
    "notes": "C6 (1047 Hz)",
})


# ======================================================================
# GROUP 3: Instrument Contrast (4 files)
# Tests timbre perception substrate (f01) across different timbres
# References: Halpern 2004 — pSTG processes timbral quality
# ======================================================================

print("GROUP 3: Instrument contrast")

_save("g3_01_piano", midi_note(C4, DUR, program=PIANO), {
    "group": "instrument", "instrument": "piano",
})

_save("g3_02_organ", midi_note(C4, DUR, program=ORGAN), {
    "group": "instrument", "instrument": "organ",
})

_save("g3_03_violin", midi_note(C4, DUR, program=VIOLIN), {
    "group": "instrument", "instrument": "violin",
})

_save("g3_04_flute", midi_note(C4, DUR, program=FLUTE), {
    "group": "instrument", "instrument": "flute",
})


# ======================================================================
# GROUP 4: Temporal (4 files)
# Tests timbre change dynamics
# ======================================================================

print("GROUP 4: Temporal")

_save("g4_01_sustained", midi_chord([C4, E4, G4], 5.0), {
    "group": "temporal", "pattern": "sustained",
})

melody_notes = [C4, E4, G4, C5, G4, E4, C4, E4]
melody_durs = [0.5] * len(melody_notes)
_save("g4_02_melody", midi_melody(melody_notes, melody_durs), {
    "group": "temporal", "pattern": "melody",
})

arp_notes = [C4, E4, G4, C5, G4, E4] * 4
arp_durs = [0.2] * len(arp_notes)
_save("g4_03_arpeggio", midi_melody(arp_notes, arp_durs), {
    "group": "temporal", "pattern": "arpeggio",
})

prog_chords = [[C4, E4, G4], [F4, A4, C5], [G4, B4, D4+12], [C4, E4, G4]]
prog_durs = [1.25] * 4
_save("g4_04_chord_progression", midi_progression(prog_chords, prog_durs), {
    "group": "temporal", "pattern": "chord_progression",
})


# ======================================================================
# GROUP 5: Timbre Change (3 files)
# Tests P1 (SMA activation) — spectral change velocity
# ======================================================================

print("GROUP 5: Timbre change")

# Static single instrument
_save("g5_01_static", midi_chord([C4, E4, G4], 5.0), {
    "group": "timbre_change", "pattern": "static",
})

# Different register notes (timbre varies within instrument)
wide_melody = [C3, C4, C5, C6, C5, C4, C3, C4]
_save("g5_02_register_sweep", midi_melody(wide_melody, [0.5]*8), {
    "group": "timbre_change", "pattern": "register_sweep",
})

# Dense alternating (high spectral change)
alt_chords = [[C4, E4, G4], [C4, Db4, D4]] * 4
_save("g5_03_alternating", midi_progression(alt_chords, [0.5]*8), {
    "group": "timbre_change", "pattern": "alternating",
})


# ======================================================================
# Save metadata
# ======================================================================

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nMetadata saved: {meta_path}")
print(f"Total stimuli: {len(METADATA)}")
