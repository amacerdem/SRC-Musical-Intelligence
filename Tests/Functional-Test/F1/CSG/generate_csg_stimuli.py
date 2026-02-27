"""Generate expanded CSG test stimuli — 30+ MIDI audio files.

Targets CSG's theoretical predictions (Bravo 2017, Sarasso 2019,
Koelsch 2006, Cheung 2019) with systematic edge cases:

  1. Consonance gradient: P1, P5, P8, M3, m3, m2, M7, TT, cluster
  2. Dynamic transitions: consonance→dissonance and reverse
  3. Inverted-U: augmented, diminished, whole-tone (ambiguous)
  4. Register: same interval at low / mid / high octaves
  5. Density: 1, 2, 3, 4, 6, 8 simultaneous notes
  6. Timbre: same chord on piano, strings, organ, brass

All files are rendered via FluidSynth + SoundFont and saved to
Tests/Functional-Test/F1/CSG/stimuli/
"""
from __future__ import annotations

import pathlib
import sys
import json
from typing import Dict, List, Optional

import numpy as np
import soundfile as sf

# -- Add project root to path --
ROOT = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "Tests" / "micro_beliefs"))

from real_audio_stimuli import (  # noqa: E402
    midi_note, midi_chord, midi_progression,
    PIANO, ORGAN, STRINGS, TRUMPET, VIOLIN, FLUTE,
    SAMPLE_RATE,
    C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5, A5, B5, C6,
)

OUT_DIR = pathlib.Path(__file__).resolve().parent / "stimuli"
OUT_DIR.mkdir(exist_ok=True)

METADATA: Dict[str, dict] = {}

DURATION = 5.0   # seconds per stimulus
VELOCITY = 80


def _save(name: str, audio_tensor, meta: dict):
    """Save WAV file + register metadata."""
    audio = audio_tensor.squeeze(0).numpy()
    path = OUT_DIR / f"{name}.wav"
    sf.write(str(path), audio, SAMPLE_RATE)
    METADATA[name] = meta
    print(f"  [{name}] {path.name} ({len(audio)/SAMPLE_RATE:.1f}s)")


# ══════════════════════════════════════════════════════════════════════
# GROUP 1: Consonance Gradient (10 files)
# Perfect interval hierarchy: P1 > P8 > P5 > P4 > M3 > m3 > m6 > M7 > m2
# ══════════════════════════════════════════════════════════════════════

print("GROUP 1: Consonance gradient intervals")

# P1 — Unison (most consonant possible)
_save("g1_01_unison", midi_chord([C4, C4], DURATION), {
    "group": "consonance_gradient",
    "interval": "P1", "semitones": 0,
    "expected_valence": "strongly_positive",
    "expected_salience": "very_low",
    "notes": "C4+C4 unison — acoustically identical, zero roughness",
})

# P8 — Octave
_save("g1_02_octave", midi_chord([C4, C5], DURATION), {
    "group": "consonance_gradient",
    "interval": "P8", "semitones": 12,
    "expected_valence": "strongly_positive",
    "expected_salience": "very_low",
    "notes": "C4+C5 octave — 2:1 ratio, minimal roughness",
})

# P5 — Perfect 5th
_save("g1_03_p5", midi_chord([C4, G4], DURATION), {
    "group": "consonance_gradient",
    "interval": "P5", "semitones": 7,
    "expected_valence": "positive",
    "expected_salience": "low",
    "notes": "C4+G4 — 3:2 ratio",
})

# P4 — Perfect 4th
_save("g1_04_p4", midi_chord([C4, F4], DURATION), {
    "group": "consonance_gradient",
    "interval": "P4", "semitones": 5,
    "expected_valence": "positive",
    "expected_salience": "low",
    "notes": "C4+F4 — 4:3 ratio",
})

# M3 — Major 3rd
_save("g1_05_m3rd", midi_chord([C4, E4], DURATION), {
    "group": "consonance_gradient",
    "interval": "M3", "semitones": 4,
    "expected_valence": "moderate_positive",
    "expected_salience": "moderate_low",
    "notes": "C4+E4 — 5:4 ratio",
})

# m3 — Minor 3rd
_save("g1_06_min3rd", midi_chord([C4, Eb4], DURATION), {
    "group": "consonance_gradient",
    "interval": "m3", "semitones": 3,
    "expected_valence": "moderate_positive",
    "expected_salience": "moderate_low",
    "notes": "C4+Eb4 — 6:5 ratio",
})

# m6 — Minor 6th
_save("g1_07_m6", midi_chord([C4, Ab4], DURATION), {
    "group": "consonance_gradient",
    "interval": "m6", "semitones": 8,
    "expected_valence": "neutral",
    "expected_salience": "moderate",
    "notes": "C4+Ab4 — 8:5 ratio",
})

# TT — Tritone (maximally ambiguous)
_save("g1_08_tritone", midi_chord([C4, Gb4], DURATION), {
    "group": "consonance_gradient",
    "interval": "TT", "semitones": 6,
    "expected_valence": "neutral_negative",
    "expected_salience": "high",
    "expected_m1": "peak (inverted-U)",
    "notes": "C4+Gb4 — sqrt(2):1 ratio, maximally ambiguous",
})

# M7 — Major 7th
_save("g1_09_M7", midi_chord([C4, B4], DURATION), {
    "group": "consonance_gradient",
    "interval": "M7", "semitones": 11,
    "expected_valence": "negative",
    "expected_salience": "high",
    "notes": "C4+B4 — highly dissonant interval",
})

# m2 — Minor 2nd (most dissonant dyad)
_save("g1_10_m2", midi_chord([C4, Db4], DURATION), {
    "group": "consonance_gradient",
    "interval": "m2", "semitones": 1,
    "expected_valence": "strongly_negative",
    "expected_salience": "very_high",
    "notes": "C4+Db4 — maximum beating/roughness",
})


# ══════════════════════════════════════════════════════════════════════
# GROUP 2: Chord Types (6 files)
# Major > Minor > Augmented ≈ Diminished > Chromatic cluster
# ══════════════════════════════════════════════════════════════════════

print("GROUP 2: Chord types")

_save("g2_01_major_triad", midi_chord([C4, E4, G4], DURATION), {
    "group": "chord_types",
    "chord": "C major", "type": "major_triad",
    "expected_valence": "positive",
})

_save("g2_02_minor_triad", midi_chord([C4, Eb4, G4], DURATION), {
    "group": "chord_types",
    "chord": "C minor", "type": "minor_triad",
    "expected_valence": "moderate_positive",
})

_save("g2_03_augmented", midi_chord([C4, E4, Ab4], DURATION), {
    "group": "chord_types",
    "chord": "C augmented", "type": "augmented_triad",
    "expected_valence": "ambiguous",
    "notes": "Equidistant intervals — high M1 expected (inverted-U)",
})

_save("g2_04_diminished", midi_chord([C4, Eb4, Gb4], DURATION), {
    "group": "chord_types",
    "chord": "C diminished", "type": "diminished_triad",
    "expected_valence": "moderate_negative",
})

_save("g2_05_dom7", midi_chord([G3, B3, D4, F4], DURATION), {
    "group": "chord_types",
    "chord": "G7", "type": "dominant_seventh",
    "expected_valence": "moderate_negative",
    "notes": "Contains tritone B-F, creates tension",
})

_save("g2_06_cluster_6note",
      midi_chord([C4, Db4, D4, Eb4, E4, F4], DURATION), {
    "group": "chord_types",
    "chord": "6-note cluster", "type": "chromatic_cluster",
    "expected_valence": "strongly_negative",
    "expected_salience": "very_high",
})


# ══════════════════════════════════════════════════════════════════════
# GROUP 3: Dynamic Transitions (4 files)
# Test CSG's temporal prediction (F-layer)
# ══════════════════════════════════════════════════════════════════════

print("GROUP 3: Dynamic transitions")

# Consonant → Dissonant
_save("g3_01_cons_to_diss",
      midi_progression(
          [[C4, E4, G4], [C4, Db4, D4, Eb4]],
          [3.0, 3.0],
      ), {
    "group": "dynamic_transitions",
    "progression": "C major → cluster",
    "expected": "E0 increase at transition, F0 drop to negative",
})

# Dissonant → Consonant
_save("g3_02_diss_to_cons",
      midi_progression(
          [[C4, Db4, D4, Eb4], [C4, E4, G4]],
          [3.0, 3.0],
      ), {
    "group": "dynamic_transitions",
    "progression": "cluster → C major",
    "expected": "E0 decrease at transition, F0 rise to positive",
})

# Gradual dissonance increase: major → minor → dim → cluster
_save("g3_03_gradual_increase",
      midi_progression(
          [[C4, E4, G4], [C4, Eb4, G4], [C4, Eb4, Gb4], [C4, Db4, D4, Eb4]],
          [2.0, 2.0, 2.0, 2.0],
      ), {
    "group": "dynamic_transitions",
    "progression": "C major → C minor → C dim → cluster",
    "expected": "Monotonic E2 decrease, E0 increase across transitions",
})

# V7 → I → V7 → I (tension-resolution cycle)
_save("g3_04_tension_resolution_cycle",
      midi_progression(
          [[G3, B3, D4, F4], [C4, E4, G4],
           [G3, B3, D4, F4], [C4, E4, G4]],
          [2.0, 2.0, 2.0, 2.0],
      ), {
    "group": "dynamic_transitions",
    "progression": "V7 → I → V7 → I",
    "expected": "Oscillating E0/E2, F-layer should predict cycle",
})


# ══════════════════════════════════════════════════════════════════════
# GROUP 4: Register Tests (6 files)
# Same interval at different octaves — roughness changes with register
# ══════════════════════════════════════════════════════════════════════

print("GROUP 4: Register tests")

# m2 in low register (C2-Db2) — wider critical band, less beating
_save("g4_01_m2_low", midi_chord([36, 37], DURATION), {
    "group": "register",
    "interval": "m2", "octave": 2,
    "notes": "C2+Db2 — low register, wider critical band",
    "expected": "Less roughness than mid-register m2",
})

# m2 in mid register (C4-Db4) — standard
_save("g4_02_m2_mid", midi_chord([C4, Db4], DURATION), {
    "group": "register",
    "interval": "m2", "octave": 4,
    "notes": "C4+Db4 — mid register, peak roughness",
})

# m2 in high register (C6-Db6) — wider critical band, less roughness
_save("g4_03_m2_high", midi_chord([84, 85], DURATION), {
    "group": "register",
    "interval": "m2", "octave": 6,
    "notes": "C6+Db6 — high register, less roughness",
})

# Major triad in low register
_save("g4_04_major_low", midi_chord([36, 40, 43], DURATION), {
    "group": "register",
    "interval": "major_triad", "octave": 2,
    "notes": "C2 major — low register, muddier",
})

# Major triad in mid register
_save("g4_05_major_mid", midi_chord([C4, E4, G4], DURATION), {
    "group": "register",
    "interval": "major_triad", "octave": 4,
    "notes": "C4 major — standard register",
})

# Major triad in high register
_save("g4_06_major_high", midi_chord([84, 88, 91], DURATION), {
    "group": "register",
    "interval": "major_triad", "octave": 6,
    "notes": "C6 major — high register, bright",
})


# ══════════════════════════════════════════════════════════════════════
# GROUP 5: Polyphonic Density (5 files)
# 1, 2, 3, 4, 6, 8 notes — increasing density
# ══════════════════════════════════════════════════════════════════════

print("GROUP 5: Polyphonic density")

_save("g5_01_single", midi_note(C4, DURATION), {
    "group": "density",
    "n_notes": 1,
    "notes": "Single C4 — baseline",
})

_save("g5_02_dyad", midi_chord([C4, G4], DURATION), {
    "group": "density",
    "n_notes": 2,
    "notes": "C4+G4 perfect 5th",
})

_save("g5_03_triad", midi_chord([C4, E4, G4], DURATION), {
    "group": "density",
    "n_notes": 3,
    "notes": "C4 major triad",
})

_save("g5_04_tetrad", midi_chord([C4, E4, G4, B4], DURATION), {
    "group": "density",
    "n_notes": 4,
    "notes": "Cmaj7 — consonant 4-voice",
})

_save("g5_05_hexad", midi_chord([C4, E4, G4, B4, D5, A4], DURATION), {
    "group": "density",
    "n_notes": 6,
    "notes": "Cmaj13 spread voicing — dense but consonant",
})

_save("g5_06_octad",
      midi_chord([C4, Db4, D4, Eb4, E4, F4, Gb4, G4], DURATION), {
    "group": "density",
    "n_notes": 8,
    "notes": "8-note chromatic cluster — extreme dissonance",
    "expected_valence": "strongly_negative",
})


# ══════════════════════════════════════════════════════════════════════
# GROUP 6: Timbre (4 files — same chord, different instruments)
# CSG should show similar consonance structure, different timbral features
# ══════════════════════════════════════════════════════════════════════

print("GROUP 6: Timbre variation")

for name, prog in [
    ("piano", PIANO), ("strings", STRINGS),
    ("organ", ORGAN), ("brass", TRUMPET),
]:
    _save(f"g6_{name}_major",
          midi_chord([C4, E4, G4], DURATION, program=prog), {
        "group": "timbre",
        "chord": "C major", "instrument": name,
        "expected": "Similar E2 valence, different M0/P0/P2 from timbral spectrum",
    })


# ══════════════════════════════════════════════════════════════════════
# Save metadata
# ══════════════════════════════════════════════════════════════════════

meta_path = OUT_DIR / "metadata.json"
with open(meta_path, "w") as f:
    json.dump(METADATA, f, indent=2)
print(f"\nMetadata saved: {meta_path}")
print(f"Total stimuli: {len(METADATA)}")
