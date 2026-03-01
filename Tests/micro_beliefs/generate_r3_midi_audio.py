#!/usr/bin/env python
"""Generate R³ verification test audio via MIDI + FluidSynth.

Every stimulus is fully deterministic — we know exactly which notes,
intervals, velocity and instrument program were used, giving us
ground truth for every R³ feature (97 dimensions across 9 groups).

Organisation:
    Test-Audio/micro_beliefs/r3_midi/{group_letter}_{group_name}/*.wav

Groups:
    A [0:7]   — Consonance           (7D)
    B [7:12]  — Energy               (5D)
    C [12:21] — Timbre               (9D)
    D [21:25] — Change               (4D)
    F [25:41] — Pitch & Chroma       (16D)
    G [41:51] — Rhythm & Groove      (10D)
    H [51:63] — Harmony & Tonality   (12D)
    J [63:83] — Timbre Extended      (20D)
    K [83:97] — Modulation & Psych.  (14D)

Run::

    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/micro_beliefs/generate_r3_midi_audio.py
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
    _render,
    # Programs
    PIANO, BRIGHT_PIANO, ORGAN, GUITAR_NYLON, GUITAR_STEEL,
    VIOLIN, VIOLA, CELLO, STRINGS, CHOIR,
    TRUMPET, TROMBONE, FRENCH_HORN, FLUTE, OBOE, CLARINET,
    HARPSICHORD,
    # Core generators
    midi_note, midi_chord, midi_progression, midi_melody,
    midi_melody_with_chords,
    # Extended generators
    midi_isochronous, midi_crescendo, midi_decrescendo,
    midi_tremolo, midi_syncopated, midi_polyrhythm,
    midi_irregular_rhythm, midi_key_progression,
    # Constructors
    major_triad, minor_triad, diminished_triad, augmented_triad,
    dominant_seventh, chromatic_cluster, diatonic_scale, chromatic_scale,
    # MIDI note numbers
    C2, D2, E2, F2, G2, A2, B2,
    C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5, A5, B5, C6,
)

import pretty_midi

OUT_DIR = _ROOT / "Test-Audio" / "micro_beliefs" / "r3_midi"


def save(waveform: torch.Tensor, group: str, name: str, gain: float = 1.0) -> pathlib.Path:
    """Save (1, N) waveform as 16-bit WAV.

    Args:
        gain: Scale factor applied AFTER _render() peak-normalization.
              Use velocity/127 to preserve dynamics across files.
    """
    path = OUT_DIR / group / f"{name}.wav"
    path.parent.mkdir(parents=True, exist_ok=True)
    w = (waveform * gain).clamp(-1.0, 1.0).squeeze(0).numpy()
    int16 = (w * 32767).astype(np.int16)
    wavfile.write(str(path), SAMPLE_RATE, int16)
    dur = len(w) / SAMPLE_RATE
    print(f"  {path.relative_to(_ROOT)}  ({dur:.2f}s)")
    return path


# =====================================================================
# GROUP A: CONSONANCE [0:7] — 7 dimensions
# Features: roughness, sethares_dissonance, helmholtz_kang,
#           stumpf_fusion, sensory_pleasantness, inharmonicity,
#           harmonic_deviation
#
# Ground truth ordering (consonance):
#   unison > octave > P5 > P4 > M3 > m3 > M6 > m6 > TT > m2
#   major triad > minor > diminished > augmented > cluster
# =====================================================================

def generate_a_consonance():
    """Group A — consonance/dissonance spectrum."""
    g = "a_consonance"
    print(f"\n=== GROUP A: CONSONANCE [0:7] ===")

    # --- Single intervals (ascending dissonance) ---
    # 01: Unison — maximum consonance (single pitch)
    save(midi_note(C4, 4.0, PIANO), g, "01_unison_C4")
    # 02: Octave — most consonant interval (2:1)
    save(midi_chord([C4, C5], 4.0, PIANO), g, "02_octave_C4C5")
    # 03: Perfect 5th (3:2)
    save(midi_chord([C4, G4], 4.0, PIANO), g, "03_p5_C4G4")
    # 04: Perfect 4th (4:3)
    save(midi_chord([C4, F4], 4.0, PIANO), g, "04_p4_C4F4")
    # 05: Major 3rd (5:4)
    save(midi_chord([C4, E4], 4.0, PIANO), g, "05_M3_C4E4")
    # 06: Minor 3rd (6:5)
    save(midi_chord([C4, Eb4], 4.0, PIANO), g, "06_m3_C4Eb4")
    # 07: Major 6th (5:3)
    save(midi_chord([C4, A4], 4.0, PIANO), g, "07_M6_C4A4")
    # 08: Minor 2nd — maximum roughness (critical bandwidth beating)
    save(midi_chord([C4, Db4], 4.0, PIANO), g, "08_m2_C4Db4")
    # 09: Tritone — maximum dissonance (45:32)
    save(midi_chord([C4, Gb4], 4.0, PIANO), g, "09_tritone_C4Gb4")

    # --- Chords (ascending dissonance) ---
    # 10: Major triad — consonant
    save(midi_chord(major_triad(C4), 4.0, PIANO), g, "10_major_triad")
    # 11: Minor triad — slightly less consonant
    save(midi_chord(minor_triad(C4), 4.0, PIANO), g, "11_minor_triad")
    # 12: Diminished triad — dissonant (contains tritone)
    save(midi_chord(diminished_triad(C4), 4.0, PIANO), g, "12_dim_triad")
    # 13: Augmented triad — dissonant (symmetric)
    save(midi_chord(augmented_triad(C4), 4.0, PIANO), g, "13_aug_triad")
    # 14: Dominant 7th — moderate dissonance
    save(midi_chord(dominant_seventh(G3), 4.0, PIANO), g, "14_dom7_G")
    # 15: 4-note chromatic cluster — high dissonance
    save(midi_chord(chromatic_cluster(C4, 4), 4.0, PIANO), g, "15_cluster_4")
    # 16: 6-note chromatic cluster — very high dissonance
    save(midi_chord(chromatic_cluster(C4, 6), 4.0, PIANO), g, "16_cluster_6")

    # --- Timbre invariance (same harmony, different instruments) ---
    # 17-19: Major triad on different instruments (consonance should be similar)
    save(midi_chord(major_triad(C4), 4.0, ORGAN), g, "17_major_triad_organ")
    save(midi_chord(major_triad(C4), 4.0, STRINGS), g, "18_major_triad_strings")
    save(midi_chord(major_triad(C4), 4.0, GUITAR_NYLON), g, "19_major_triad_guitar")
    # 20-21: Cluster on different instruments
    save(midi_chord(chromatic_cluster(C4, 4), 4.0, ORGAN), g, "20_cluster_4_organ")
    save(midi_chord(chromatic_cluster(C4, 4), 4.0, STRINGS), g, "21_cluster_4_strings")

    # --- Temporal transitions ---
    # 22: Consonant → dissonant progression
    save(midi_progression(
        [major_triad(C4), minor_triad(C4), diminished_triad(C4),
         chromatic_cluster(C4, 4)],
        [2.0, 2.0, 2.0, 2.0], PIANO,
    ), g, "22_consonant_to_dissonant")
    # 23: Dissonant → consonant progression
    save(midi_progression(
        [chromatic_cluster(C4, 4), diminished_triad(C4),
         minor_triad(C4), major_triad(C4)],
        [2.0, 2.0, 2.0, 2.0], PIANO,
    ), g, "23_dissonant_to_consonant")


# =====================================================================
# GROUP B: ENERGY [7:12] — 5 dimensions
# Features: amplitude, velocity_A, acceleration_A, loudness,
#           onset_strength
# =====================================================================

def generate_b_energy():
    """Group B — energy/dynamics spectrum."""
    g = "b_energy"
    print(f"\n=== GROUP B: ENERGY [7:12] ===")

    # --- Amplitude / Loudness (static levels) ---
    # _render() peak-normalizes to 0.95 — apply gain to restore dynamics
    # 01: Pianissimo (v=25) — minimum amplitude
    save(midi_note(C4, 4.0, PIANO, 25), g, "01_pp_v25", gain=25 / 127)
    # 02: Piano (v=50)
    save(midi_note(C4, 4.0, PIANO, 50), g, "02_p_v50", gain=50 / 127)
    # 03: Mezzo-forte (v=80)
    save(midi_note(C4, 4.0, PIANO, 80), g, "03_mf_v80", gain=80 / 127)
    # 04: Forte (v=100)
    save(midi_note(C4, 4.0, PIANO, 100), g, "04_f_v100", gain=100 / 127)
    # 05: Fortissimo (v=127) — maximum amplitude
    save(midi_note(C4, 4.0, PIANO, 127), g, "05_ff_v127", gain=1.0)

    # --- Velocity_A (amplitude derivative) ---
    # 06: Crescendo — positive velocity_A
    save(midi_crescendo(C4, 16, 0.35, 20, 120, PIANO), g, "06_crescendo")
    # 07: Decrescendo — negative velocity_A
    save(midi_decrescendo(C4, 16, 0.35, 120, 20, PIANO), g, "07_decrescendo")
    # 08: Steady forte (constant velocity) — near-zero velocity_A
    save(midi_isochronous(C4, 120.0, 16, PIANO, 90), g, "08_steady_f")

    # --- Onset strength ---
    # 09: Staccato attacks (short notes, sharp onsets) — high onset_strength
    save(midi_melody([C4]*16, [0.15]*16, PIANO, 100), g, "09_staccato_onsets")
    # 10: Legato pad (sustained organ, very stable) — low onset_strength
    save(midi_note(C4, 6.0, ORGAN, 80), g, "10_legato_pad")
    # 11: Dense onsets (rapid notes) — high event density + onset
    save(midi_melody([C4]*32, [0.1]*32, PIANO, 80), g, "11_dense_onsets")
    # 12: Single onset then silence — single spike
    save(midi_note(C4, 0.3, PIANO, 110), g, "12_single_attack")
    # 13: Chord onset (thick texture) — strong onset
    save(midi_chord(chromatic_scale(C3, 12), 0.5, PIANO, 100), g, "13_chord_onset")
    # 14: Repeated chords (multiple strong onsets)
    save(midi_progression(
        [major_triad(C4)] * 8,
        [0.5] * 8, PIANO, 90,
    ), g, "14_repeated_chord_onsets")


# =====================================================================
# GROUP C: TIMBRE [12:21] — 9 dimensions
# Features: warmth, sharpness, tonalness, clarity (centroid),
#           spectral_smoothness, spectral_autocorrelation,
#           tristimulus1, tristimulus2, tristimulus3
# =====================================================================

def generate_c_timbre():
    """Group C — timbral characteristics."""
    g = "c_timbre"
    print(f"\n=== GROUP C: TIMBRE [12:21] ===")

    # --- Warmth vs Sharpness (spectral balance) ---
    # 01: Cello C3 — very warm (strong low frequencies)
    save(midi_note(C3, 5.0, CELLO, 80), g, "01_cello_C3_warm")
    # 02: Flute C4 — moderate warmth (near-sinusoidal)
    save(midi_note(C4, 5.0, FLUTE, 80), g, "02_flute_C4_moderate")
    # 03: Trumpet C5 — bright/sharp (many upper harmonics)
    save(midi_note(C5, 5.0, TRUMPET, 100), g, "03_trumpet_C5_bright")
    # 04: Piano C2 — very warm (low register)
    save(midi_note(C2, 5.0, PIANO, 80), g, "04_piano_C2_very_warm")
    # 05: Piano C6 — very sharp (high register)
    save(midi_note(C6, 5.0, PIANO, 80), g, "05_piano_C6_very_sharp")

    # --- Tonalness (peak vs spread) ---
    # 06: Piano C4 — peaked spectrum, high tonalness
    save(midi_note(C4, 5.0, PIANO, 80), g, "06_flute_C4_tonal")
    # 07: Organ C4 — rich harmonics but periodic, high tonalness
    save(midi_note(C4, 5.0, ORGAN, 80), g, "07_organ_C4_rich")
    # 08: Wide chromatic cluster (same instrument, same velocity) — spread, low tonalness
    save(midi_chord(chromatic_cluster(C3, 12), 5.0, PIANO, 80), g, "08_cluster_low_tonal")

    # --- Spectral smoothness & autocorrelation ---
    # 09: Organ (many harmonics, smooth spectrum) — high spectral_autocorr
    save(midi_note(C4, 5.0, ORGAN, 80), g, "09_organ_smooth_spectrum")
    # 10: Piano ff (percussive, rich) — moderate smoothness
    save(midi_note(C4, 5.0, PIANO, 127), g, "10_piano_ff_percussive")
    # 11: Harpsichord (plucked, spiky spectrum) — low smoothness
    save(midi_note(C4, 5.0, HARPSICHORD, 80), g, "11_harpsichord_spiky")

    # --- Tristimulus (low/mid/high energy distribution) ---
    # 12: Bass note (C2) — tristimulus1 dominant (low band)
    save(midi_note(C2, 5.0, PIANO, 80), g, "12_bass_C2_trist1")
    # 13: Mid note (C4) — tristimulus2 dominant (mid band)
    save(midi_note(C4, 5.0, PIANO, 80), g, "13_mid_C4_trist2")
    # 14: High note (C6) — tristimulus3 dominant (high band)
    save(midi_note(C6, 5.0, PIANO, 80), g, "14_high_C6_trist3")
    # 15: Full chord spanning registers — balanced tristimulus
    save(midi_chord([C2, C3, C4, C5, C6], 5.0, PIANO, 70), g, "15_full_range_balanced")

    # --- Timbre comparison (same pitch, different instruments) ---
    # 16: Violin (bowed, warm overtones)
    save(midi_note(C4, 5.0, VIOLIN, 80), g, "16_violin_C4")
    # 17: Oboe (nasal, strong odd harmonics)
    save(midi_note(C4, 5.0, OBOE, 80), g, "17_oboe_C4")
    # 18: Guitar (plucked, fast decay)
    save(midi_note(C4, 5.0, GUITAR_NYLON, 80), g, "18_guitar_C4")


# =====================================================================
# GROUP D: CHANGE [21:25] — 4 dimensions
# Features: spectral_flux, distribution_entropy,
#           distribution_flatness, distribution_concentration
# =====================================================================

def generate_d_change():
    """Group D — spectral change and distribution features."""
    g = "d_change"
    print(f"\n=== GROUP D: CHANGE [21:25] ===")

    # --- Spectral flux (frame-to-frame change) ---
    # 01: Sustained note — minimal spectral flux
    save(midi_note(C4, 6.0, STRINGS, 70), g, "01_sustained_no_flux")
    # 02: Fast melody — high spectral flux (changing pitch = changing spectrum)
    save(midi_melody(
        [C4, E4, G4, B4, C5, B4, G4, E4, C4, E4, G4, B4, C5, B4, G4, E4],
        [0.2] * 16, PIANO, 80,
    ), g, "02_fast_melody_high_flux")
    # 03: Chord progression (moderate flux at chord changes)
    save(midi_progression(
        [major_triad(C4), major_triad(F3), major_triad(G3), major_triad(C4),
         minor_triad(A3), major_triad(F3), dominant_seventh(G3), major_triad(C4)],
        [0.75] * 8, PIANO, 80,
    ), g, "03_chord_progression_moderate_flux")
    # 04: Sudden timbre change — spike in flux
    pm = pretty_midi.PrettyMIDI()
    for prog, start in [(STRINGS, 0.0), (TRUMPET, 3.0), (FLUTE, 6.0)]:
        inst = pretty_midi.Instrument(program=prog)
        inst.notes.append(pretty_midi.Note(
            velocity=80, pitch=C4, start=start, end=start + 3.0,
        ))
        pm.instruments.append(inst)
    save(_render(pm), g, "04_timbre_change_flux_spikes")
    # 05: Repeated same note (minimal pitch change but onset flux)
    save(midi_melody([C4] * 16, [0.3] * 16, PIANO, 80), g, "05_repeated_note_onset_flux")

    # --- Distribution entropy / flatness / concentration ---
    # 06: High note C6 — few harmonics (within Nyquist), concentrated mel, low entropy
    save(midi_note(C6, 5.0, PIANO, 80), g, "06_pure_tone_low_entropy")
    # 07: Bass note C2 — many harmonics spread across mel spectrum, high entropy
    save(midi_note(C2, 5.0, PIANO, 80), g, "07_all_12_notes_high_entropy")
    # 08: Single note different register (high) — different concentration
    save(midi_note(C6, 5.0, PIANO, 80), g, "08_high_note_different_dist")
    # 09: Open voicing chord — moderate entropy
    save(midi_chord([C3, G3, E4, B4], 5.0, PIANO, 70), g, "09_open_voicing_moderate")
    # 10: Single bass note — energy concentrated in low bins
    save(midi_note(C2, 5.0, PIANO, 80), g, "10_bass_concentrated_low")
    # 11: Melody with constant timbre — varying concentration over time
    save(midi_melody(
        diatonic_scale(C4, 8) + list(reversed(diatonic_scale(C4, 8))),
        [0.3] * 16, FLUTE, 80,
    ), g, "11_melody_varying_concentration")


# =====================================================================
# GROUP F: PITCH & CHROMA [25:41] — 16 dimensions
# Features: chroma_C..chroma_B (12D), pitch_height,
#           pitch_class_entropy, pitch_salience, inharmonicity_index
# =====================================================================

def generate_f_pitch_chroma():
    """Group F — pitch class, chroma, height, salience."""
    g = "f_pitch_chroma"
    print(f"\n=== GROUP F: PITCH & CHROMA [25:41] ===")

    # --- Individual chroma identity (12 pitch classes) ---
    # 01-12: Single notes for each pitch class (all in octave 4)
    note_names = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]
    for i, (midi_num, name) in enumerate(zip(range(60, 72), note_names)):
        save(midi_note(midi_num, 4.0, PIANO, 80), g, f"{i+1:02d}_single_{name}4")

    # --- Pitch height ---
    # 13: C2 — very low pitch_height
    save(midi_note(C2, 4.0, PIANO, 80), g, "13_C2_low_height")
    # 14: C3
    save(midi_note(C3, 4.0, PIANO, 80), g, "14_C3_mid_low_height")
    # 15: C4 — middle
    save(midi_note(C4, 4.0, PIANO, 80), g, "15_C4_mid_height")
    # 16: C5
    save(midi_note(C5, 4.0, PIANO, 80), g, "16_C5_mid_high_height")
    # 17: C6 — very high pitch_height
    save(midi_note(C6, 4.0, PIANO, 80), g, "17_C6_high_height")

    # --- Pitch class entropy ---
    # 18: Single note — minimum entropy (1 chroma class active)
    save(midi_note(C4, 4.0, PIANO, 80), g, "18_single_note_min_entropy")
    # 19: Octave C4+C5 — still low entropy (same chroma class)
    save(midi_chord([C4, C5], 4.0, PIANO, 80), g, "19_octave_low_entropy")
    # 20: Major triad — 3 chroma classes
    save(midi_chord(major_triad(C4), 4.0, PIANO, 80), g, "20_triad_3_chroma")
    # 21: Pentatonic chord (C-D-E-G-A) — 5 chroma classes
    save(midi_chord([C4, D4, E4, G4, A4], 4.0, PIANO, 70), g, "21_pentatonic_5_chroma")
    # 22: Diatonic chord (7 notes) — 7 chroma classes
    save(midi_chord(diatonic_scale(C4, 7), 4.0, PIANO, 60), g, "22_diatonic_7_chroma")
    # 23: All 12 notes — maximum entropy
    save(midi_chord(chromatic_scale(C4, 12), 4.0, PIANO, 50), g, "23_chromatic_12_max_entropy")

    # --- Pitch salience ---
    # 24: Strong single note — max pitch salience
    save(midi_note(A4, 4.0, PIANO, 100), g, "24_strong_A4_max_salience")
    # 25: Dense full-range cluster — low pitch salience (energy across all mel bins)
    save(midi_chord([C2, E2, A2, C3, F3, A3, C4, E4, Ab4, C5, E5, C6],
                    4.0, PIANO, 60), g, "25_cluster_low_salience")
    # 26: Octave-doubled note — high salience (reinforced pitch)
    save(midi_chord([C3, C4, C5], 4.0, PIANO, 80), g, "26_octave_doubled_high_salience")

    # --- Chroma in different keys ---
    # 27: C major scale — dominant C major chroma
    save(midi_melody(diatonic_scale(C4, 8), [0.4]*8, PIANO, 80), g, "27_C_major_scale")
    # 28: G major scale — dominant G major chroma (F# instead of F)
    g_major = [G4, A4, B4, C5, D5, E5, G4+11, G5]  # G A B C D E F# G
    save(midi_melody(g_major, [0.4]*8, PIANO, 80), g, "28_G_major_scale")
    # 29: Eb major scale
    eb_major = [Eb4, F4, G4, Ab4, Bb4, C5, D5, Eb4+12]
    save(midi_melody(eb_major, [0.4]*8, PIANO, 80), g, "29_Eb_major_scale")


# =====================================================================
# GROUP G: RHYTHM & GROOVE [41:51] — 10 dimensions
# Features: tempo_estimate, beat_strength, pulse_clarity,
#           syncopation_index, metricality_index, isochrony_nPVI,
#           groove_index, event_density, tempo_stability,
#           rhythmic_regularity
# =====================================================================

def generate_g_rhythm():
    """Group G — rhythm, tempo, groove, beat structure."""
    g = "g_rhythm"
    print(f"\n=== GROUP G: RHYTHM & GROOVE [41:51] ===")

    # --- Tempo estimation (different BPMs) ---
    # 01: 60 BPM — slow (1 beat/s)
    save(midi_isochronous(C4, 60.0, 12, PIANO, 90), g, "01_60bpm_slow")
    # 02: 90 BPM — moderate
    save(midi_isochronous(C4, 90.0, 16, PIANO, 90), g, "02_90bpm_moderate")
    # 03: 120 BPM — standard (2 beats/s)
    save(midi_isochronous(C4, 120.0, 20, PIANO, 90), g, "03_120bpm_standard")
    # 04: 150 BPM — fast
    save(midi_isochronous(C4, 150.0, 24, PIANO, 90), g, "04_150bpm_fast")
    # 05: 180 BPM — very fast (3 beats/s)
    save(midi_isochronous(C4, 180.0, 28, PIANO, 90), g, "05_180bpm_very_fast")

    # --- Beat strength & pulse clarity ---
    # 06: Strong downbeats (loud, clear pulse) — max beat_strength
    save(midi_isochronous(C4, 120.0, 20, PIANO, 110), g, "06_strong_beats_120bpm")
    # 07: Weak beats (soft) — lower beat_strength
    save(midi_isochronous(C4, 120.0, 20, PIANO, 40), g, "07_weak_beats_120bpm")
    # 08: Sustained chord (no beats) — near-zero beat_strength
    save(midi_note(C4, 8.0, STRINGS, 70), g, "08_sustained_no_beats")

    # --- Syncopation ---
    # 09: On-beat only (downbeats at 120 BPM) — zero syncopation
    save(midi_isochronous(C4, 120.0, 16, PIANO, 90), g, "09_on_beat_no_syncopation")
    # 10: Offbeat syncopated pattern — high syncopation
    save(midi_syncopated(C4, 120.0, 4, PIANO, 90), g, "10_offbeat_syncopated")

    # --- Isochrony & regularity ---
    # 11: Perfect isochrony at 120 BPM — max isochrony_nPVI, max regularity
    save(midi_isochronous(C4, 120.0, 20, PIANO, 80), g, "11_perfect_isochrony")
    # 12: Irregular timing — low isochrony, low regularity
    save(midi_irregular_rhythm(C4, 16, PIANO, 80, seed=42), g, "12_irregular_timing")

    # --- Metricality ---
    # 13: Metrical pattern (strong-weak-medium-weak in 4/4)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    beat_dur = 0.5  # 120 BPM
    pattern_vel = [110, 50, 80, 50]  # strong-weak-medium-weak
    for bar in range(4):
        for beat, vel in enumerate(pattern_vel):
            t = (bar * 4 + beat) * beat_dur
            inst.notes.append(pretty_midi.Note(
                velocity=vel, pitch=C4, start=t, end=t + beat_dur * 0.8,
            ))
    pm.instruments.append(inst)
    save(_render(pm), g, "13_metrical_4_4_pattern")

    # --- Event density ---
    # 14: Sparse events (whole notes = 1 per 2s at 120 BPM)
    save(midi_isochronous(C4, 30.0, 4, PIANO, 80), g, "14_sparse_events")
    # 15: Dense events (16th notes at 120 BPM = 8 per second)
    save(midi_isochronous(C4, 480.0, 48, PIANO, 70), g, "15_dense_16th_notes")

    # --- Groove (syncopation × bass × clarity) ---
    # 16: Groove pattern (bass on downbeat, syncopation on offbeat)
    pm = pretty_midi.PrettyMIDI()
    bass = pretty_midi.Instrument(program=PIANO)
    hi = pretty_midi.Instrument(program=PIANO)
    beat = 0.5  # 120 BPM
    for bar in range(4):
        offset = bar * 4 * beat
        # Bass on beats 1, 3
        for b in [0, 2]:
            t = offset + b * beat
            bass.notes.append(pretty_midi.Note(
                velocity=100, pitch=C3, start=t, end=t + beat * 0.9,
            ))
        # Hi-hat on offbeats (8th note grid)
        for eighth in range(8):
            t = offset + eighth * (beat / 2)
            vel = 60 if eighth % 2 == 0 else 90  # offbeats louder
            hi.notes.append(pretty_midi.Note(
                velocity=vel, pitch=G5, start=t, end=t + 0.05,
            ))
    pm.instruments.append(bass)
    pm.instruments.append(hi)
    save(_render(pm), g, "16_groove_pattern")

    # --- Polyrhythm (complex rhythm) ---
    # 17: 3 against 4 — complex, lower metricality
    save(midi_polyrhythm(C4, G4, 3, 4, 6.0, PIANO, 80), g, "17_polyrhythm_3v4")


# =====================================================================
# GROUP H: HARMONY & TONALITY [51:63] — 12 dimensions
# Features: key_clarity, tonnetz (6D: fifth_xy, minor_xy, major_xy),
#           voice_leading_distance, harmonic_change,
#           tonal_stability, diatonicity, syntactic_irregularity
# =====================================================================

def generate_h_harmony():
    """Group H — key, tonality, voice leading, harmonic analysis."""
    g = "h_harmony"
    print(f"\n=== GROUP H: HARMONY & TONALITY [51:63] ===")

    # --- Key clarity ---
    # 01: C major scale — strong C major key clarity
    save(midi_melody(diatonic_scale(C4, 8), [0.4]*8, PIANO, 80), g, "01_C_major_scale")
    # 02: A natural minor scale — strong A minor key clarity
    a_minor = [A3, B3, C4, D4, E4, F4, G4, A4]
    save(midi_melody(a_minor, [0.4]*8, PIANO, 80), g, "02_A_minor_scale")
    # 03: Chromatic scale — ambiguous key (low key_clarity)
    save(midi_melody(chromatic_scale(C4, 13), [0.3]*13, PIANO, 80), g, "03_chromatic_low_clarity")
    # 04: Whole-tone scale — no clear key
    whole_tone = [C4, D4, E4, Gb4, Ab4, Bb4, C5]
    save(midi_melody(whole_tone, [0.4]*7, PIANO, 80), g, "04_whole_tone_no_key")

    # --- Diatonicity ---
    # 05: Pure diatonic (only white keys) — max diatonicity
    save(midi_chord(diatonic_scale(C4, 7), 5.0, PIANO, 60), g, "05_diatonic_max")
    # 06: Full chromatic — min diatonicity
    save(midi_chord(chromatic_scale(C4, 12), 5.0, PIANO, 50), g, "06_chromatic_min_diatonic")
    # 07: Pentatonic (5 of 7 diatonic notes) — high diatonicity
    save(midi_chord([C4, D4, E4, G4, A4], 5.0, PIANO, 70), g, "07_pentatonic_high_diatonic")

    # --- Harmonic change & voice leading distance ---
    # 08: Sustained single chord — zero harmonic_change
    save(midi_chord(major_triad(C4), 6.0, PIANO, 70), g, "08_sustained_chord_no_change")
    # 09: Smooth voice leading (I→vi→IV→V) — low voice_leading_distance
    save(midi_progression(
        [major_triad(C4), minor_triad(A3), major_triad(F3), major_triad(G3)],
        [1.5]*4, PIANO, 70,
    ), g, "09_smooth_voice_leading")
    # 10: Large jumps (distant keys) — high voice_leading_distance
    save(midi_progression(
        [major_triad(C4), major_triad(Gb4), major_triad(C4), major_triad(Gb4)],
        [1.5]*4, PIANO, 70,
    ), g, "10_distant_jumps_high_vl_dist")
    # 11: Rapid chord changes — high harmonic_change frequency
    save(midi_progression(
        [major_triad(C4), minor_triad(D4), major_triad(Eb4), minor_triad(F4),
         major_triad(G4), minor_triad(A4), major_triad(B3), major_triad(C4)],
        [0.5]*8, PIANO, 70,
    ), g, "11_rapid_chord_changes")

    # --- Tonal stability ---
    # 12: Stable C major cadence (I-IV-V-I) — high tonal_stability
    save(midi_progression(
        [major_triad(C4), major_triad(F3), major_triad(G3), major_triad(C4)],
        [2.0]*4, PIANO, 70,
    ), g, "12_stable_I_IV_V_I")
    # 13: Modulating progression (C→G→D) — lower tonal_stability
    save(midi_key_progression([C4, G3, D4], 3.0, PIANO, 70), g, "13_modulating_C_G_D")
    # 14: Chromatic modulation (all keys) — minimum tonal_stability
    save(midi_key_progression([C4, Db4, D4, Eb4], 2.0, PIANO, 70), g, "14_chromatic_modulation")

    # --- Syntactic irregularity ---
    # 15: Standard cadence (expected) — low syntactic_irregularity
    save(midi_progression(
        [major_triad(C4), major_triad(F3), dominant_seventh(G3), major_triad(C4)],
        [2.0]*4, PIANO, 70,
    ), g, "15_standard_cadence_regular")
    # 16: Deceptive cadence (V→vi instead of V→I) — irregularity spike
    save(midi_progression(
        [major_triad(C4), major_triad(F3), dominant_seventh(G3), minor_triad(A3)],
        [2.0]*4, PIANO, 70,
    ), g, "16_deceptive_cadence_irregular")
    # 17: Bitonal passage — high syntactic_irregularity
    save(midi_chord([C4, E4, G4, Gb4, Bb4, C5 + 1], 5.0, PIANO, 70), g, "17_bitonal_irregular")

    # --- Tonnetz position ---
    # 18: C major triad (C-E-G) — specific tonnetz position
    save(midi_chord(major_triad(C4), 5.0, PIANO, 70), g, "18_C_major_tonnetz")
    # 19: F# major triad — opposite tonnetz position (tritone away)
    save(midi_chord(major_triad(Gb4), 5.0, PIANO, 70), g, "19_Fsharp_major_tonnetz")
    # 20: G major triad — adjacent on fifths cycle
    save(midi_chord(major_triad(G3), 5.0, PIANO, 70), g, "20_G_major_tonnetz")
    # 21: C minor triad — same root, different tonnetz (minor third cycle)
    save(midi_chord(minor_triad(C4), 5.0, PIANO, 70), g, "21_C_minor_tonnetz")


# =====================================================================
# GROUP J: TIMBRE EXTENDED [63:83] — 20 dimensions
# Features: mfcc_1..mfcc_13, spectral_contrast_1..spectral_contrast_7
# =====================================================================

def generate_j_timbre_ext():
    """Group J — MFCC profiles & spectral contrast."""
    g = "j_timbre_ext"
    print(f"\n=== GROUP J: TIMBRE EXTENDED [63:83] ===")

    # --- MFCC profiles (different instruments = different MFCC patterns) ---
    # 01-08: Same pitch C4 on 8 instruments — each has unique MFCC fingerprint
    instruments = [
        (PIANO, "piano"), (VIOLIN, "violin"), (CELLO, "cello"),
        (FLUTE, "flute"), (OBOE, "oboe"), (TRUMPET, "trumpet"),
        (ORGAN, "organ"), (GUITAR_NYLON, "guitar"),
    ]
    for i, (prog, name) in enumerate(instruments, 1):
        save(midi_note(C4, 5.0, prog, 80), g, f"{i:02d}_C4_{name}")

    # --- Register effect on MFCCs ---
    # 09: C2 — low register MFCC shift
    save(midi_note(C2, 5.0, PIANO, 80), g, "09_C2_piano_low")
    # 10: C4 — mid register
    save(midi_note(C4, 5.0, PIANO, 80), g, "10_C4_piano_mid")
    # 11: C6 — high register MFCC shift
    save(midi_note(C6, 5.0, PIANO, 80), g, "11_C6_piano_high")

    # --- Dynamics effect on MFCCs ---
    # 12: pp — softer timbre (fewer harmonics) — scale to preserve dynamics
    save(midi_note(C4, 5.0, PIANO, 25), g, "12_C4_piano_pp", gain=25 / 127)
    # 13: ff — brighter timbre (more harmonics)
    save(midi_note(C4, 5.0, PIANO, 127), g, "13_C4_piano_ff", gain=1.0)

    # --- Spectral contrast (peak vs valley in octave sub-bands) ---
    # 14: Major chord — moderate spectral contrast
    save(midi_chord(major_triad(C4), 5.0, PIANO, 80), g, "14_major_chord")
    # 15: Dense cluster — low spectral contrast (flat spectrum)
    save(midi_chord(chromatic_cluster(C4, 8), 5.0, PIANO, 60), g, "15_dense_cluster_flat")
    # 16: Single note — high spectral contrast (clear peaks)
    save(midi_note(C4, 5.0, PIANO, 80), g, "16_single_note_peaked")
    # 17: Full range chord — broad spectral contrast
    save(midi_chord([C2, C3, G3, C4, E4, G4, C5], 5.0, PIANO, 70), g, "17_full_range_chord")

    # --- Timbre sequence (MFCC change over time) ---
    # 18: Piano → Violin → Trumpet → Flute sequence
    pm = pretty_midi.PrettyMIDI()
    for prog, start in [(PIANO, 0.0), (VIOLIN, 2.0), (TRUMPET, 4.0), (FLUTE, 6.0)]:
        inst = pretty_midi.Instrument(program=prog)
        inst.notes.append(pretty_midi.Note(
            velocity=80, pitch=C4, start=start, end=start + 2.0,
        ))
        pm.instruments.append(inst)
    save(_render(pm), g, "18_timbre_sequence_4inst")


# =====================================================================
# GROUP K: MODULATION & PSYCHOACOUSTIC [83:97] — 14 dimensions
# Features: modulation_0_5Hz..modulation_16Hz (6D),
#           modulation_centroid, modulation_bandwidth,
#           sharpness_zwicker, fluctuation_strength,
#           loudness_a_weighted, alpha_ratio,
#           hammarberg_index, spectral_slope_0_500
# =====================================================================

def generate_k_modulation():
    """Group K — modulation spectrum, psychoacoustic loudness, sharpness."""
    g = "k_modulation"
    print(f"\n=== GROUP K: MODULATION & PSYCHOACOUSTIC [83:97] ===")

    # --- Modulation spectrum at specific rates ---
    # 01: Sustained note (no modulation) — flat modulation spectrum
    save(midi_note(C4, 6.0, STRINGS, 70), g, "01_sustained_no_modulation")
    # 02: Tremolo at ~0.5 Hz (slow swell) — peak at 0.5 Hz
    save(midi_tremolo(C4, 0.5, 6.0, PIANO, 80), g, "02_tremolo_0_5Hz")
    # 03: Tremolo at ~1 Hz — peak at 1 Hz
    save(midi_tremolo(C4, 1.0, 6.0, PIANO, 80), g, "03_tremolo_1Hz")
    # 04: Tremolo at ~2 Hz (120 BPM) — peak at 2 Hz
    save(midi_tremolo(C4, 2.0, 6.0, PIANO, 80), g, "04_tremolo_2Hz")
    # 05: Tremolo at ~4 Hz (vibrato-like) — peak at 4 Hz, max fluctuation_strength
    save(midi_tremolo(C4, 4.0, 6.0, PIANO, 80), g, "05_tremolo_4Hz")
    # 06: Tremolo at ~8 Hz (fast) — peak at 8 Hz
    save(midi_tremolo(C4, 8.0, 6.0, PIANO, 80), g, "06_tremolo_8Hz")
    # 07: Tremolo at ~16 Hz (very fast, approaching roughness) — peak at 16 Hz
    save(midi_tremolo(C4, 16.0, 4.0, PIANO, 80), g, "07_tremolo_16Hz")

    # --- Modulation centroid & bandwidth ---
    # 08: Isochronous 120 BPM (2 Hz dominant) — low centroid
    save(midi_isochronous(C4, 120.0, 20, PIANO, 80), g, "08_120bpm_low_centroid")
    # 09: Isochronous 480 BPM (8 Hz dominant) — high centroid
    save(midi_isochronous(C4, 480.0, 48, PIANO, 70), g, "09_480bpm_high_centroid")

    # --- Sharpness (Zwicker) ---
    # 10: Dark timbre (cello low register) — low sharpness_zwicker
    save(midi_note(C2, 5.0, CELLO, 80), g, "10_cello_C2_dark")
    # 11: Bright timbre (trumpet high register) — high sharpness_zwicker
    save(midi_note(C5, 5.0, TRUMPET, 100), g, "11_trumpet_C5_bright")
    # 12: Mid timbre (piano C4) — moderate sharpness
    save(midi_note(C4, 5.0, PIANO, 80), g, "12_piano_C4_moderate")

    # --- Loudness (A-weighted) ---
    # 13: Soft (v=25) — low loudness_a_weighted — scale to preserve dynamics
    save(midi_note(C4, 5.0, PIANO, 25), g, "13_soft_v25", gain=25 / 127)
    # 14: Loud (v=127) — high loudness_a_weighted
    save(midi_note(C4, 5.0, PIANO, 127), g, "14_loud_v127", gain=1.0)
    # 15: Low note loud — lower A-weighted (A-weighting de-emphasizes bass)
    save(midi_note(C2, 5.0, PIANO, 110), g, "15_bass_loud_low_Aweight")
    # 16: Mid note loud — higher A-weighted (A-weighting peaks at 2-4 kHz)
    save(midi_note(A4, 5.0, PIANO, 110), g, "16_mid_loud_high_Aweight")

    # --- Alpha ratio (low / total energy) ---
    # 17: Bass note — high alpha_ratio (most energy below 1 kHz)
    save(midi_note(C2, 5.0, PIANO, 80), g, "17_bass_high_alpha")
    # 18: High note — low alpha_ratio (most energy above 1 kHz)
    save(midi_note(C6, 5.0, PIANO, 80), g, "18_high_low_alpha")

    # --- Hammarberg index (0-2 kHz peak / 2-5 kHz peak) ---
    # 19: Dark sustained (organ low) — high hammarberg (strong low peak)
    save(midi_note(C3, 5.0, ORGAN, 80), g, "19_organ_C3_high_hammarberg")
    # 20: Bright staccato (trumpet) — low hammarberg (strong high peak)
    save(midi_note(C5, 5.0, TRUMPET, 100), g, "20_trumpet_C5_low_hammarberg")

    # --- Spectral slope (0-500 Hz regression) ---
    # 21: Strong fundamental (organ) — positive/flat slope
    save(midi_note(C4, 5.0, ORGAN, 80), g, "21_organ_strong_fundamental")
    # 22: High note (no content in 0-500 Hz) — different slope
    save(midi_note(C6, 5.0, PIANO, 80), g, "22_high_note_no_low_content")
    # 23: Full chord (rich low content) — specific slope
    save(midi_chord([C2, C3, G3, C4, E4, G4], 5.0, PIANO, 70), g, "23_full_chord_rich_low")


# =====================================================================
# Main
# =====================================================================

def main():
    print(f"Generating R³ verification audio → {OUT_DIR.relative_to(_ROOT)}/")

    generate_a_consonance()
    generate_b_energy()
    generate_c_timbre()
    generate_d_change()
    generate_f_pitch_chroma()
    generate_g_rhythm()
    generate_h_harmony()
    generate_j_timbre_ext()
    generate_k_modulation()

    count = sum(1 for _ in OUT_DIR.rglob("*.wav"))
    print(f"\nDone — {count} WAV files generated across 9 R³ groups.")


if __name__ == "__main__":
    main()
