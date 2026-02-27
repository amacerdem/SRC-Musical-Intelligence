"""Generate SDNPS test stimuli — 18 MIDI audio files.

Targets SDNPS's predictions (Cousineau 2015, Bidelman 2009/2013):
  - NPS predicts consonance for synthetic (r=0.34) but not natural tones
  - NPS↔roughness r=-0.57 is stimulus-invariant
  - Spectral complexity degrades NPS validity

Groups:
  1. Consonance intervals (5 files) — Tests P2 (roughness interference)
  2. Harmonicity (4 files) — Tests E0 (nps_value), P1 (harmonicity_proxy)
  3. Spectral complexity (4 files) — Tests E1 (stimulus_dependency)
  4. Roughness levels (5 files) — Tests E2 (roughness_corr)
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
    SAMPLE_RATE,
    C3, E3, G3, C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, B4,
    C5, E5, G5, C6,
)

OUT_DIR = pathlib.Path(__file__).resolve().parent / "stimuli"
OUT_DIR.mkdir(exist_ok=True)
METADATA: Dict[str, dict] = {}
DUR = 4.0


def _save(name, audio, meta):
    a = audio.squeeze(0).numpy()
    sf.write(str(OUT_DIR / f"{name}.wav"), a, SAMPLE_RATE)
    METADATA[name] = meta
    print(f"  [{name}] ({len(a)/SAMPLE_RATE:.1f}s)")


print("GROUP 1: Consonance intervals")
_save("g1_01_single", midi_note(C4, DUR), {"group": "consonance"})
_save("g1_02_octave", midi_chord([C4, C5], DUR), {"group": "consonance"})
_save("g1_03_fifth", midi_chord([C4, G4], DUR), {"group": "consonance"})
_save("g1_04_tritone", midi_chord([C4, Gb4], DUR), {"group": "consonance"})
_save("g1_05_minor2nd", midi_chord([C4, Db4], DUR), {"group": "consonance"})

print("GROUP 2: Harmonicity")
_save("g2_01_single", midi_note(C4, DUR), {"group": "harmonicity"})
_save("g2_02_octave", midi_chord([C4, C5], DUR), {"group": "harmonicity"})
_save("g2_03_triad", midi_chord([C4, E4, G4], DUR), {"group": "harmonicity"})
_save("g2_04_cluster", midi_chord([C4, Db4, D4, Eb4], DUR), {"group": "harmonicity"})

print("GROUP 3: Spectral complexity")
_save("g3_01_single", midi_note(C4, DUR), {"group": "complexity", "notes": "simple"})
_save("g3_02_dyad", midi_chord([C4, G4], DUR), {"group": "complexity"})
_save("g3_03_triad", midi_chord([C4, E4, G4], DUR), {"group": "complexity"})
_save("g3_04_dense", midi_chord([C4, Db4, D4, Eb4, E4], DUR), {"group": "complexity"})

print("GROUP 4: Roughness levels")
_save("g4_01_single", midi_note(C4, DUR), {"group": "roughness", "level": "none"})
_save("g4_02_maj3rd", midi_chord([C4, E4], DUR), {"group": "roughness", "level": "low"})
_save("g4_03_minor3rd", midi_chord([C4, Eb4], DUR), {"group": "roughness", "level": "moderate"})
_save("g4_04_major7th", midi_chord([C4, B4], DUR), {"group": "roughness", "level": "high"})
_save("g4_05_minor2nd", midi_chord([C4, Db4], DUR), {"group": "roughness", "level": "very_high"})

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nTotal stimuli: {len(METADATA)}")
