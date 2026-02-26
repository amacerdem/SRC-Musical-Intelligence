#!/usr/bin/env python
"""Generate F1 micro-belief test audio via MIDI + FluidSynth.

Every stimulus is fully deterministic — we know exactly which notes,
intervals, velocity and instrument program were used, giving us
ground truth for every belief.

Saves to Test-Audio/micro_beliefs/f1_midi/{relay}/*.wav

Run::

    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/micro_beliefs/generate_f1_midi_audio.py
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import torch
from scipy.io import wavfile

# Ensure project root on path
_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))

from Tests.micro_beliefs.real_audio_stimuli import (
    SAMPLE_RATE,
    # Programs
    PIANO, ORGAN, GUITAR_NYLON, VIOLIN, CELLO, STRINGS,
    CHOIR, TRUMPET, FLUTE, OBOE, HARPSICHORD,
    # Generators
    midi_note, midi_chord, midi_progression, midi_melody,
    midi_melody_with_chords,
    # Constructors
    major_triad, minor_triad, diminished_triad, augmented_triad,
    dominant_seventh, chromatic_cluster, diatonic_scale, chromatic_scale,
    # MIDI note numbers
    C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5, A5, B5, C6,
)

OUT_DIR = _ROOT / "Test-Audio" / "micro_beliefs" / "f1_midi"


def save(waveform: torch.Tensor, relay: str, name: str) -> pathlib.Path:
    """Save (1, N) waveform as 16-bit WAV."""
    path = OUT_DIR / relay / f"{name}.wav"
    path.parent.mkdir(parents=True, exist_ok=True)
    w = waveform.clamp(-1.0, 1.0).squeeze(0).numpy()
    int16 = (w * 32767).astype(np.int16)
    wavfile.write(str(path), SAMPLE_RATE, int16)
    dur = len(w) / SAMPLE_RATE
    print(f"  {path.relative_to(_ROOT)}  ({dur:.2f}s)")
    return path


# =====================================================================
# BCH — Consonance Hierarchy
# Ground truth: We know exact intervallic content of each chord.
# Expected ordering: unison > octave > P5 > major > minor > dim > cluster
# =====================================================================

def generate_bch():
    """BCH relay — chord types with known consonance."""
    print("\n=== BCH (Consonance Hierarchy — MIDI) ===")

    # Single note — maximum consonance (no beating partials)
    save(midi_note(C4, 4.0, PIANO), "bch", "01_single_C4_piano")

    # Octave — most consonant interval (2:1 ratio)
    save(midi_chord([C4, C5], 4.0, PIANO), "bch", "02_octave_C4C5_piano")

    # Perfect 5th — second most consonant (3:2 ratio)
    save(midi_chord([C4, G4], 4.0, PIANO), "bch", "03_p5_C4G4_piano")

    # Perfect 4th — consonant (4:3 ratio)
    save(midi_chord([C4, F4], 4.0, PIANO), "bch", "04_p4_C4F4_piano")

    # Major triad — consonant chord (C-E-G)
    save(midi_chord(major_triad(C4), 4.0, PIANO), "bch", "05_major_triad_piano")

    # Minor triad — slightly less consonant (C-Eb-G)
    save(midi_chord(minor_triad(C4), 4.0, PIANO), "bch", "06_minor_triad_piano")

    # Diminished triad — dissonant (C-Eb-Gb, contains tritone)
    save(midi_chord(diminished_triad(C4), 4.0, PIANO), "bch", "07_dim_triad_piano")

    # Augmented triad — dissonant (C-E-G#)
    save(midi_chord(augmented_triad(C4), 4.0, PIANO), "bch", "08_aug_triad_piano")

    # Dominant 7th — moderate dissonance (G-B-D-F, contains tritone B-F)
    save(midi_chord(dominant_seventh(G3), 4.0, PIANO), "bch", "09_dom7_G_piano")

    # Chromatic cluster — maximum dissonance (4 adjacent semitones)
    save(midi_chord(chromatic_cluster(C4, 4), 4.0, PIANO), "bch", "10_cluster_4note_piano")

    # Dense cluster — even more dissonance (6 adjacent semitones)
    save(midi_chord(chromatic_cluster(C4, 6), 4.0, PIANO), "bch", "11_cluster_6note_piano")

    # I-IV-V-I cadence — consonant progression
    save(midi_progression(
        [major_triad(C4), major_triad(F3), major_triad(G3), major_triad(C4)],
        [1.5, 1.5, 1.5, 1.5], PIANO,
    ), "bch", "12_I_IV_V_I_piano")

    # Same chords on organ — different timbre, same harmony
    save(midi_chord(major_triad(C4), 4.0, ORGAN), "bch", "13_major_triad_organ")
    save(midi_chord(chromatic_cluster(C4, 4), 4.0, ORGAN), "bch", "14_cluster_4note_organ")

    # Same chords on strings — yet another timbre
    save(midi_chord(major_triad(C4), 4.0, STRINGS), "bch", "15_major_triad_strings")

    # Consonant to dissonant progression
    save(midi_progression(
        [major_triad(C4), minor_triad(C4), diminished_triad(C4),
         chromatic_cluster(C4, 4)],
        [2.0, 2.0, 2.0, 2.0], PIANO,
    ), "bch", "16_consonant_to_dissonant_8s")

    # Dissonant to consonant (reverse)
    save(midi_progression(
        [chromatic_cluster(C4, 4), diminished_triad(C4),
         minor_triad(C4), major_triad(C4)],
        [2.0, 2.0, 2.0, 2.0], PIANO,
    ), "bch", "17_dissonant_to_consonant_8s")


# =====================================================================
# PSCL — Pitch Salience
# Ground truth: Clear pitched notes vs chords vs clusters.
# All use known f0 values.
# =====================================================================

def generate_pscl():
    """PSCL encoder — pitch salience with different instruments."""
    print("\n=== PSCL (Pitch Salience — MIDI) ===")

    # Single notes on different instruments — all A4 (440 Hz)
    save(midi_note(A4, 4.0, PIANO, 80), "pscl", "01_A4_piano")
    save(midi_note(A4, 4.0, VIOLIN, 80), "pscl", "02_A4_violin")
    save(midi_note(A4, 4.0, FLUTE, 80), "pscl", "03_A4_flute")
    save(midi_note(A4, 4.0, OBOE, 80), "pscl", "04_A4_oboe")
    save(midi_note(A4, 4.0, TRUMPET, 80), "pscl", "05_A4_trumpet")

    # Same instrument, different pitches — pitch should be clear for all
    save(midi_note(C3, 4.0, PIANO, 80), "pscl", "06_C3_piano")
    save(midi_note(C4, 4.0, PIANO, 80), "pscl", "07_C4_piano")
    save(midi_note(C5, 4.0, PIANO, 80), "pscl", "08_C5_piano")
    save(midi_note(C6, 4.0, PIANO, 80), "pscl", "09_C6_piano")

    # Chord — pitch more ambiguous
    save(midi_chord(major_triad(C4), 4.0, PIANO), "pscl", "10_chord_C_major")

    # Dense chord — pitch very ambiguous
    save(midi_chord(chromatic_cluster(C4, 6), 4.0, PIANO), "pscl", "11_cluster_6note")

    # Melody — sequential pitch clarity
    save(midi_melody(diatonic_scale(C4, 8), [0.5] * 8, PIANO), "pscl", "12_melody_diatonic")


# =====================================================================
# PCCR — Pitch Chroma & Octave Equivalence
# Ground truth: Same chroma class at different octaves should produce
# similar octave_equivalence. Different chroma should differ.
# =====================================================================

def generate_pccr():
    """PCCR associator — chroma identity tests."""
    print("\n=== PCCR (Pitch Chroma — MIDI) ===")

    # Same melody in 3 octaves — should show octave equivalence
    mel_notes = [0, 2, 4, 5, 7]  # C-D-E-F-G relative
    save(midi_melody([C3 + n for n in mel_notes], [0.5] * 5, PIANO),
         "pccr", "01_melody_C_oct3")
    save(midi_melody([C4 + n for n in mel_notes], [0.5] * 5, PIANO),
         "pccr", "02_melody_C_oct4")
    save(midi_melody([C5 + n for n in mel_notes], [0.5] * 5, PIANO),
         "pccr", "03_melody_C_oct5")

    # Different key — different chroma
    save(midi_melody([G4, A4, B4, C5, D5], [0.5] * 5, PIANO),
         "pccr", "04_melody_G_oct4")
    save(midi_melody([Eb4, F4, G4, Ab4, Bb4], [0.5] * 5, PIANO),
         "pccr", "05_melody_Eb_oct4")

    # Octave dyad vs tritone dyad (octave = maximum chroma equivalence)
    save(midi_chord([C4, C5], 4.0, PIANO), "pccr", "06_octave_dyad")
    save(midi_chord([C4, Gb4], 4.0, PIANO), "pccr", "07_tritone_dyad")
    save(midi_chord([C4, G4], 4.0, PIANO), "pccr", "08_fifth_dyad")

    # Single notes — strong chroma identity
    save(midi_note(C4, 4.0, PIANO), "pccr", "09_single_C4")
    save(midi_note(A4, 4.0, PIANO), "pccr", "10_single_A4")

    # Chromatic cluster — weak chroma identity (all classes present)
    save(midi_chord(chromatic_scale(C4, 12), 4.0, PIANO, 50),
         "pccr", "11_all_12_notes")


# =====================================================================
# SDED — Spectral Dissonance / Complexity
# Ground truth: We know exact spectral content from note choices.
# Cluster > inharmonic > triad > single note
# =====================================================================

def generate_sded():
    """SDED relay — spectral complexity via chord density."""
    print("\n=== SDED (Spectral Complexity — MIDI) ===")

    # Single note — minimal spectral complexity
    save(midi_note(C4, 4.0, PIANO), "sded", "01_single_C4")

    # Octave — very low spectral interaction
    save(midi_chord([C4, C5], 4.0, PIANO), "sded", "02_octave")

    # Major triad — low complexity (consonant partials)
    save(midi_chord(major_triad(C4), 4.0, PIANO), "sded", "03_major_triad")

    # m2 dyad — high roughness from close partials
    save(midi_chord([C4, Db4], 4.0, PIANO), "sded", "04_m2_dyad")

    # 4-note chromatic cluster
    save(midi_chord(chromatic_cluster(C4, 4), 4.0, PIANO), "sded", "05_cluster_4note")

    # 6-note chromatic cluster — maximum spectral density
    save(midi_chord(chromatic_cluster(C4, 6), 4.0, PIANO), "sded", "06_cluster_6note")

    # Bitonal: C major + F# major simultaneously
    save(midi_chord([C4, E4, G4, Gb4, Bb4, C5 + 1], 4.0, PIANO),
         "sded", "07_bitonal_C_Fsharp")

    # Full chromatic — all 12 notes
    save(midi_chord(chromatic_scale(C4, 12), 4.0, PIANO, 50),
         "sded", "08_full_chromatic")


# =====================================================================
# CSG — Consonance-Salience Gradient
# Ground truth: Dissonance creates high salience (perceptual attention).
# Resolution reduces salience.
# =====================================================================

def generate_csg():
    """CSG relay — consonance-salience gradient tests."""
    print("\n=== CSG (Consonance-Salience Gradient — MIDI) ===")

    # Consonant chord — low salience
    save(midi_chord(major_triad(C4), 4.0, PIANO), "csg", "01_major_triad")

    # m2 dyad — high roughness → high salience
    save(midi_chord([C4, Db4], 4.0, PIANO), "csg", "02_m2_dyad")

    # Chromatic cluster — maximum salience
    save(midi_chord(chromatic_cluster(C4, 4), 4.0, PIANO), "csg", "03_cluster")

    # V7 → I resolution: tension (high salience) → release (low salience)
    save(midi_progression(
        [dominant_seventh(G3), major_triad(C4)],
        [3.0, 3.0], PIANO,
    ), "csg", "04_V7_I_resolution")

    # Reverse: I → V7 (consonance → dissonance → rising salience)
    save(midi_progression(
        [major_triad(C4), dominant_seventh(G3)],
        [3.0, 3.0], PIANO,
    ), "csg", "05_I_V7_tension")

    # Single note — baseline salience
    save(midi_note(C4, 4.0, PIANO), "csg", "06_single_note")


# =====================================================================
# MPG — Melodic Contour
# Ground truth: We know exact pitch sequence, contour direction,
# interval sizes, and temporal pattern.
# =====================================================================

def generate_mpg():
    """MPG relay — melodic contour tests."""
    print("\n=== MPG (Melodic Contour — MIDI) ===")

    # Ascending diatonic scale (C4→C5)
    save(midi_melody(diatonic_scale(C4, 8), [0.4] * 8, PIANO),
         "mpg", "01_ascending_diatonic")

    # Descending diatonic scale (C5→C4)
    save(midi_melody(list(reversed(diatonic_scale(C4, 8))), [0.4] * 8, PIANO),
         "mpg", "02_descending_diatonic")

    # Ascending chromatic scale (semitones)
    save(midi_melody(chromatic_scale(C4, 13), [0.3] * 13, PIANO),
         "mpg", "03_ascending_chromatic")

    # Arpeggio: C-E-G-C-G-E-C (arch contour)
    save(midi_melody([C4, E4, G4, C5, G4, E4, C4], [0.5] * 7, PIANO),
         "mpg", "04_arpeggio_arch")

    # Repeated note (no contour)
    save(midi_melody([C4] * 8, [0.4] * 8, PIANO),
         "mpg", "05_repeated_C4")

    # Large leaps: C4-C5-C4-C5-C4 (octave jumps)
    save(midi_melody([C4, C5, C4, C5, C4], [0.6] * 5, PIANO),
         "mpg", "06_octave_leaps")

    # Melody with mixed contour (up-down-up pattern)
    save(midi_melody(
        [C4, E4, G4, F4, D4, F4, A4, G4, E4, C5],
        [0.35] * 10, PIANO,
    ), "mpg", "07_mixed_contour")

    # Sustained note — no melodic motion
    save(midi_note(C4, 4.0, PIANO), "mpg", "08_sustained_C4")

    # Same melody on violin
    save(midi_melody(diatonic_scale(C4, 8), [0.4] * 8, VIOLIN),
         "mpg", "09_ascending_diatonic_violin")

    # Same melody on flute
    save(midi_melody(diatonic_scale(C4, 8), [0.4] * 8, FLUTE),
         "mpg", "10_ascending_diatonic_flute")


# =====================================================================
# MIAA — Timbral Character
# Ground truth: Same pitch (C4), different GM programs.
# Only timbre differs — frequency content determined by SoundFont.
# =====================================================================

def generate_miaa():
    """MIAA relay — timbral character tests (same pitch, diff instrument)."""
    print("\n=== MIAA (Timbral Character — MIDI) ===")

    # Same note on 8 different instruments
    instruments = [
        (PIANO, "piano"),
        (VIOLIN, "violin"),
        (CELLO, "cello"),
        (FLUTE, "flute"),
        (OBOE, "oboe"),
        (TRUMPET, "trumpet"),
        (ORGAN, "organ"),
        (GUITAR_NYLON, "guitar"),
    ]
    for i, (prog, name) in enumerate(instruments, 1):
        save(midi_note(C4, 5.0, prog, 80),
             "miaa", f"{i:02d}_C4_{name}")

    # Same instrument, different dynamics → affects timbral character
    save(midi_note(C4, 5.0, PIANO, 30), "miaa", "09_C4_piano_pp")
    save(midi_note(C4, 5.0, PIANO, 127), "miaa", "10_C4_piano_ff")

    # Different pitch on same instrument → timbre changes with register
    save(midi_note(C3, 5.0, PIANO, 80), "miaa", "11_C3_piano")
    save(midi_note(C5, 5.0, PIANO, 80), "miaa", "12_C5_piano")

    # Chord vs single note — timbral complexity difference
    save(midi_chord(major_triad(C4), 5.0, PIANO), "miaa", "13_chord_C_major_piano")

    # Multi-timbre sequence: piano→violin→flute→trumpet (1.5s each)
    from Tests.micro_beliefs.real_audio_stimuli import _render
    import pretty_midi
    pm = pretty_midi.PrettyMIDI()
    for prog, start_t in [(PIANO, 0.0), (VIOLIN, 1.5), (FLUTE, 3.0), (TRUMPET, 4.5)]:
        inst = pretty_midi.Instrument(program=prog)
        inst.notes.append(pretty_midi.Note(
            velocity=80, pitch=C4,
            start=start_t, end=start_t + 1.5,
        ))
        pm.instruments.append(inst)
    save(_render(pm), "miaa", "14_timbre_sequence_4inst")


# =====================================================================
# STAI — Aesthetic Quality
# Ground truth: Beautiful = consonant + coherent + resolved.
# Harsh = dissonant + dense + unresolved.
# =====================================================================

def generate_stai():
    """STAI encoder — aesthetic quality tests."""
    print("\n=== STAI (Aesthetic Quality — MIDI) ===")

    # Beautiful: I-vi-IV-V progression on strings
    save(midi_progression(
        [major_triad(C4), minor_triad(A3), major_triad(F3), major_triad(G3)],
        [2.0] * 4, STRINGS, 70,
    ), "stai", "01_beautiful_I_vi_IV_V_strings")

    # Beautiful: Bach-style chorale on choir
    save(midi_progression(
        [[C4, E4, G4, C5], [F4, A4, C5, F5],
         [G4, B4, D5, G5], [C4, E4, G4, C5]],
        [2.0] * 4, CHOIR, 70,
    ), "stai", "02_chorale_SATB_choir")

    # Harsh: chromatic cluster sequence
    save(midi_progression(
        [chromatic_cluster(C4, 4), chromatic_cluster(Db4, 4),
         chromatic_cluster(D4, 4), chromatic_cluster(Eb4, 4)],
        [1.5] * 4, PIANO, 100,
    ), "stai", "03_harsh_chromatic_clusters")

    # Moderate: minor-key progression (more tension than major)
    save(midi_progression(
        [minor_triad(A3), diminished_triad(B3),
         major_triad(C4), dominant_seventh(E3)],
        [2.0] * 4, PIANO, 75,
    ), "stai", "04_minor_key_progression")

    # Beautiful: melody with consonant accompaniment
    save(midi_melody_with_chords(
        melody_notes=[E5, D5, C5, D5, E5, E5, E5],
        melody_durs=[0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0],
        chord_notes=[major_triad(C4), major_triad(G3),
                     major_triad(C4), major_triad(G3)],
        chord_durs=[1.0, 1.0, 1.0, 1.0],
        melody_program=FLUTE,
        chord_program=STRINGS,
    ), "stai", "05_melody_with_chords_beautiful")

    # Harsh: dense cluster with harsh dynamics
    save(midi_chord(chromatic_cluster(C4, 8), 4.0, PIANO, 127),
         "stai", "06_dense_cluster_ff")

    # Single consonant chord — pleasant baseline
    save(midi_chord(major_triad(C4), 4.0, STRINGS, 60),
         "stai", "07_major_triad_strings_p")

    # Dissonant → consonant resolution (aesthetic improvement)
    save(midi_progression(
        [chromatic_cluster(B3, 4), dominant_seventh(G3), major_triad(C4)],
        [2.0, 2.0, 3.0], PIANO, 75,
    ), "stai", "08_dissonant_to_resolved")

    # Consonant → dissonant (aesthetic decline)
    save(midi_progression(
        [major_triad(C4), dominant_seventh(G3), chromatic_cluster(B3, 4)],
        [3.0, 2.0, 2.0], PIANO, 75,
    ), "stai", "09_resolved_to_dissonant")


# =====================================================================
# Main
# =====================================================================

def main():
    print(f"Generating F1 MIDI test audio → {OUT_DIR.relative_to(_ROOT)}/")
    generate_bch()
    generate_pscl()
    generate_pccr()
    generate_sded()
    generate_csg()
    generate_mpg()
    generate_miaa()
    generate_stai()

    count = sum(1 for _ in OUT_DIR.rglob("*.wav"))
    print(f"\nDone — {count} WAV files generated.")


if __name__ == "__main__":
    main()
