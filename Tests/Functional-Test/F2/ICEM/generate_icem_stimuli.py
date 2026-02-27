"""Generate ICEM test stimuli — 18 MIDI audio files.

Targets ICEM's information content and emotional response with:

  1. Consonance hierarchy: single → minor 2nd (6 files)
  2. Register: C3 → C6 (3 files)
  3. Complexity: single → dense cluster (4 files)
  4. Temporal: sustained → arpeggio (3 files)
  5. Instrument contrast: piano/organ (2 files)

All files rendered via FluidSynth + SoundFont, saved to
Tests/Functional-Test/F2/ICEM/stimuli/
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
    midi_note, midi_chord, midi_melody,
    PIANO, ORGAN,
    SAMPLE_RATE,
    C3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, A4, B4,
    C5, C6,
)

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

# GROUP 1: Consonance Hierarchy
print("GROUP 1: Consonance hierarchy")
_save("g1_01_single", midi_note(C4, DUR), {"group": "consonance", "interval": "unison"})
_save("g1_02_octave", midi_chord([C4, C5], DUR), {"group": "consonance", "interval": "octave"})
_save("g1_03_fifth", midi_chord([C4, G4], DUR), {"group": "consonance", "interval": "fifth"})
_save("g1_04_tritone", midi_chord([C4, Gb4], DUR), {"group": "consonance", "interval": "tritone"})
_save("g1_05_minor_2nd", midi_chord([C4, Db4], DUR), {"group": "consonance", "interval": "minor_2nd"})
_save("g1_06_major_7th", midi_chord([C4, B4], DUR), {"group": "consonance", "interval": "major_7th"})

# GROUP 2: Register
print("GROUP 2: Register")
_save("g2_01_low", midi_note(C3, DUR), {"group": "register", "notes": "C3"})
_save("g2_02_mid", midi_note(C4, DUR), {"group": "register", "notes": "C4"})
_save("g2_03_high", midi_note(C6, DUR), {"group": "register", "notes": "C6"})

# GROUP 3: Complexity
print("GROUP 3: Complexity")
_save("g3_01_single", midi_note(C4, DUR), {"group": "complexity", "pattern": "single"})
_save("g3_02_dyad", midi_chord([C4, G4], DUR), {"group": "complexity", "pattern": "dyad"})
_save("g3_03_triad", midi_chord([C4, E4, G4], DUR), {"group": "complexity", "pattern": "triad"})
_save("g3_04_dense", midi_chord([C4, Db4, D4, Eb4], DUR), {"group": "complexity", "pattern": "dense"})

# GROUP 4: Temporal
print("GROUP 4: Temporal")
_save("g4_01_sustained", midi_chord([C4, E4, G4], 5.0), {"group": "temporal", "pattern": "sustained"})
melody_notes = [C4, E4, G4, C5, G4, E4, C4, E4]
_save("g4_02_melody", midi_melody(melody_notes, [0.5]*8), {"group": "temporal", "pattern": "melody"})
arp_notes = [C4, E4, G4, C5, G4, E4] * 4
_save("g4_03_arpeggio", midi_melody(arp_notes, [0.2]*24), {"group": "temporal", "pattern": "arpeggio"})

# GROUP 5: Instrument
print("GROUP 5: Instrument")
_save("g5_01_piano", midi_note(C4, DUR, program=PIANO), {"group": "instrument", "instrument": "piano"})
_save("g5_02_organ", midi_note(C4, DUR, program=ORGAN), {"group": "instrument", "instrument": "organ"})

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nMetadata saved: {meta_path}")
print(f"Total stimuli: {len(METADATA)}")
