"""Generate PNH test stimuli — 18 MIDI audio files.

Targets PNH's predictions (Kim 2021, Bidelman 2013, Sarasso 2019):
  - Simple frequency ratios → less IFG/ACC activation (H0 low)
  - Complex ratios → more activation (H0 high)
  - Consonance preference higher for harmonic intervals

Groups:
  1. Ratio complexity (6 intervals) — Tests H0, M0
  2. Conflict response (4 files) — Tests H1, P1
  3. Consonance preference (4 files) — Tests P2
  4. Temporal context (4 files) — Tests F0, F1
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
    C5, E5, G5,
)
import torch

OUT_DIR = pathlib.Path(__file__).resolve().parent / "stimuli"
OUT_DIR.mkdir(exist_ok=True)
METADATA: Dict[str, dict] = {}
DUR = 4.0


def _save(name, audio, meta):
    a = audio.squeeze(0).numpy()
    sf.write(str(OUT_DIR / f"{name}.wav"), a, SAMPLE_RATE)
    METADATA[name] = meta
    print(f"  [{name}] ({len(a)/SAMPLE_RATE:.1f}s)")


print("GROUP 1: Ratio complexity intervals")
_save("g1_01_unison", midi_note(C4, DUR), {"group": "ratio", "ratio": "1:1"})
_save("g1_02_octave", midi_chord([C4, C5], DUR), {"group": "ratio", "ratio": "2:1"})
_save("g1_03_fifth", midi_chord([C4, G4], DUR), {"group": "ratio", "ratio": "3:2"})
_save("g1_04_fourth", midi_chord([C4, F4], DUR), {"group": "ratio", "ratio": "4:3"})
_save("g1_05_tritone", midi_chord([C4, Gb4], DUR), {"group": "ratio", "ratio": "sqrt2:1"})
_save("g1_06_minor2nd", midi_chord([C4, Db4], DUR), {"group": "ratio", "ratio": "16:15"})

print("GROUP 2: Conflict response")
_save("g2_01_consonant_chord", midi_chord([C4, E4, G4], DUR), {"group": "conflict"})
_save("g2_02_dissonant_cluster", midi_chord([C4, Db4, D4], DUR), {"group": "conflict"})
_save("g2_03_consonant_soft", midi_note(C4, DUR), {"group": "conflict"})
_save("g2_04_rapid_alternating",
      midi_progression([[C4, E4, G4], [C4, Db4, D4]] * 4, [0.5] * 8),
      {"group": "conflict"})

print("GROUP 3: Consonance preference")
_save("g3_01_major_triad", midi_chord([C4, E4, G4], DUR), {"group": "preference"})
_save("g3_02_minor_triad", midi_chord([C4, Eb4, G4], DUR), {"group": "preference"})
_save("g3_03_aug_triad", midi_chord([C4, E4, Ab4], DUR), {"group": "preference"})
_save("g3_04_cluster", midi_chord([C4, Db4, D4, Eb4], DUR), {"group": "preference"})

print("GROUP 4: Temporal context")
_save("g4_01_stable_consonant", midi_chord([C4, E4, G4], 5.0), {"group": "temporal"})
_save("g4_02_stable_dissonant", midi_chord([C4, Db4, D4], 5.0), {"group": "temporal"})
# Dissonance → resolution
diss = midi_chord([C4, Db4, D4], 2.5)
cons = midi_chord([C4, E4, G4], 2.5)
_save("g4_03_resolution", torch.cat([diss, cons], dim=-1), {"group": "temporal"})
_save("g4_04_progression",
      midi_progression(
          [[C4, E4, G4], [F4, A4, C5], [G4, B4, E5], [C4, E4, G4]],
          [1.5] * 4),
      {"group": "temporal"})

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nTotal stimuli: {len(METADATA)}")
