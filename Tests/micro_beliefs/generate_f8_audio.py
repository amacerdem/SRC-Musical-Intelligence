"""Deterministic MIDI-based test-audio generator for F8 (Learning & Plasticity).

Generates ~80 stimuli across 7 categories for testing all 14 F8 beliefs:

  TSCP (Timbre-Specific Cortical Plasticity):
    trained_timbre_recognition (Core, tau=0.90)
    plasticity_magnitude       (Appraisal)

  ESME (Expertise-Specific MMN Enhancement):
    expertise_enhancement  (Core, tau=0.92)
    pitch_mmn              (Appraisal)
    rhythm_mmn             (Appraisal)
    timbre_mmn             (Appraisal)
    expertise_trajectory   (Anticipation)

  EDNR (Expertise-Dependent Network Reorganization):
    network_specialization (Core, tau=0.95 — highest in C³)
    within_connectivity    (Appraisal)

  SLEE (Statistical Learning Expertise Enhancement):
    statistical_model      (Core, tau=0.88)
    detection_accuracy     (Appraisal)
    multisensory_binding   (Appraisal)

  ECT (Expertise Compartmentalization Trade-off):
    compartmentalization_cost (Appraisal)
    transfer_limitation       (Anticipation)

Science:
  Pantev et al 2001 (MEG N=17): timbre-specific N1m double dissociation
  Koelsch Schroger & Tervaniemi 1999 (EEG N~20/grp): violinist MMN 0.75%
  Vuust et al 2012 (EEG N~40-60): genre-specific MMN gradient
  Criscuolo et al 2022 (ALE k=84 N=3005): musician > NM bilateral STG
  Paraskevopoulos et al 2022 (MEG/PTE N=25): 106 within vs 192 between
  Bridwell 2017 (EEG N=13): 45% amplitude reduction patterned vs random
  Moller et al 2021 (DTI+CT N=45): musicians local-only CT correlations
  Papadaki et al 2023 (fMRI N=41): professional > amateur network strength

Output: .wav (44100 Hz 16-bit) + .mid + metadata.json + STIMULUS-CATALOG.md
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
import pretty_midi
import torch
from scipy.io import wavfile

# ── project root & shared infrastructure ────────────────────────────
_HERE = pathlib.Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from Tests.micro_beliefs.real_audio_stimuli import (   # noqa: E402
    SAMPLE_RATE, _render,
    PIANO, BRIGHT_PIANO, HARPSICHORD, ORGAN,
    GUITAR_NYLON, GUITAR_STEEL,
    VIOLIN, VIOLA, CELLO, STRINGS, CHOIR,
    TRUMPET, TROMBONE, FRENCH_HORN,
    FLUTE, OBOE, CLARINET,
    major_triad, minor_triad, dominant_seventh,
    chromatic_cluster, diatonic_scale,
    C2, C3, D3, E3, F3, G3, A3, B3,
    C4, D4, E4, F4, G4, A4, B4,
    C5, D5, E5, F5, G5, A5, B5, C6,
)

# ── extra pitch constants ───────────────────────────────────────────
Db4, Eb4, Gb4, Ab4, Bb4 = 61, 63, 66, 68, 70
Db3, Eb3, Ab3, Bb3 = 49, 51, 56, 58
D2, E2, G2, A2, B2 = 38, 40, 43, 45, 47
C1 = 24; C7 = 96

# ── chord voicings ──────────────────────────────────────────────────
C_MAJ = [C4, E4, G4]
C_MIN = [C4, Eb4, G4]
G_DOM7 = [G3, B3, D4, F4]
F_MAJ = [F3, A3, C4]
A_MIN = [A3, C4, E4]
D_MIN = [D4, F4, A4]
G_MAJ = [G3, B3, D4]
Eb_MAJ = [Eb3, G3, Bb3]
Ab_MAJ = [Ab3, C4, Eb4]

# ── output ──────────────────────────────────────────────────────────
OUTPUT_DIR = _PROJECT_ROOT / "Test-Audio" / "micro_beliefs" / "f8"
ALL_METADATA: dict = {}

Note = pretty_midi.Note


# =====================================================================
# Save helper
# =====================================================================
def save(pm: pretty_midi.PrettyMIDI, group: str, name: str,
         meta: dict, gain: float = 1.0) -> None:
    """Render MIDI → WAV+MID, store metadata."""
    out = OUTPUT_DIR / group
    out.mkdir(parents=True, exist_ok=True)

    pm.write(str(out / f"{name}.mid"))

    audio = _render(pm)                         # (1, N) float32
    audio = audio * gain
    peak = audio.abs().max().item()
    if peak > 0:
        audio = audio * (0.95 / peak)
    audio = audio.clamp(-1.0, 1.0)

    pcm = (audio.squeeze(0).numpy() * 32767).astype(np.int16)
    wavfile.write(str(out / f"{name}.wav"), SAMPLE_RATE, pcm)

    ALL_METADATA[f"{group}/{name}"] = meta


# =====================================================================
# Standard MIDI builder helpers (reused from F7 pattern)
# =====================================================================
def _pm_note(pitch, duration, program=PIANO, velocity=80):
    """Single note PrettyMIDI."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    inst.notes.append(Note(velocity=velocity, pitch=pitch,
                           start=0.0, end=duration))
    pm.instruments.append(inst)
    return pm


def _pm_chord(pitches, duration, program=PIANO, velocity=80):
    """Chord PrettyMIDI."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for p in pitches:
        inst.notes.append(Note(velocity=velocity, pitch=p,
                               start=0.0, end=duration))
    pm.instruments.append(inst)
    return pm


def _pm_melody(notes, durations, program=PIANO, velocity=80):
    """Sequential melody with 20ms gaps."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for p, d in zip(notes, durations):
        inst.notes.append(Note(velocity=velocity, pitch=p,
                               start=t, end=t + d - 0.02))
        t += d
    pm.instruments.append(inst)
    return pm


def _pm_isochronous(pitch, bpm, n_beats, program=PIANO, velocity=80):
    """Isochronous repeating note at exact BPM."""
    ioi = 60.0 / bpm
    dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_beats):
        t = i * ioi
        inst.notes.append(Note(velocity=velocity, pitch=pitch,
                               start=t, end=t + dur))
    pm.instruments.append(inst)
    return pm


def _pm_near_silence(duration=5.0):
    """Near-silence baseline: single vel=1 tick."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=1, pitch=C4, start=0.0, end=0.01))
    pm.instruments.append(inst)
    return pm


def _pm_dense_random(duration, seed, notes_per_sec=8):
    """Random pitches/velocities — maximally unpredictable."""
    rng = np.random.RandomState(seed)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    n = int(duration * notes_per_sec)
    for i in range(n):
        t = i / notes_per_sec
        p = int(rng.randint(36, 85))
        v = int(rng.randint(40, 121))
        inst.notes.append(Note(velocity=v, pitch=p,
                               start=t, end=t + 0.04))
    pm.instruments.append(inst)
    return pm


def _pm_progression(chords, durations, program=PIANO, velocity=80):
    """Chord progression with 20ms gaps."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for ch, d in zip(chords, durations):
        for p in ch:
            inst.notes.append(Note(velocity=velocity, pitch=p,
                                   start=t, end=t + d - 0.02))
        t += d
    pm.instruments.append(inst)
    return pm


def _pm_ensemble_chord(voices, duration):
    """Multi-instrument sustained chord. voices=[(pitches, program, vel)]."""
    pm = pretty_midi.PrettyMIDI()
    for pitches, prog, vel in voices:
        inst = pretty_midi.Instrument(program=prog)
        for p in pitches:
            inst.notes.append(Note(velocity=vel, pitch=p,
                                   start=0.0, end=duration))
        pm.instruments.append(inst)
    return pm


def _pm_ensemble_isochronous(voices, bpm, n_beats):
    """Multi-instrument synchronized isochronous. voices=[(pitch, prog, vel)]."""
    ioi = 60.0 / bpm
    dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    for pitch, prog, vel in voices:
        inst = pretty_midi.Instrument(program=prog)
        for i in range(n_beats):
            t = i * ioi
            inst.notes.append(Note(velocity=vel, pitch=pitch,
                                   start=t, end=t + dur))
        pm.instruments.append(inst)
    return pm


# =====================================================================
# F8-specific MIDI builder helpers
# =====================================================================
def _pm_oddball_sequence(standard_pitch, deviant_pitch, n_total,
                         deviant_positions, ioi, program=PIANO,
                         standard_vel=80, deviant_vel=80):
    """Oddball paradigm: standard notes with deviants at specified positions.

    Classic MMN elicitation paradigm (Naatanen 1978).
    """
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    dur = ioi * 0.85
    for i in range(n_total):
        t = i * ioi
        if i in deviant_positions:
            inst.notes.append(Note(velocity=deviant_vel, pitch=deviant_pitch,
                                   start=t, end=t + dur))
        else:
            inst.notes.append(Note(velocity=standard_vel, pitch=standard_pitch,
                                   start=t, end=t + dur))
    pm.instruments.append(inst)
    return pm


def _pm_timbre_oddball(standard_program, deviant_program, pitch,
                       n_total, deviant_positions, ioi, velocity=80):
    """Timbre oddball: same pitch, instrument changes at deviant positions.

    Pantev et al 2001: instrument-specific MMN.
    """
    pm = pretty_midi.PrettyMIDI()
    std_inst = pretty_midi.Instrument(program=standard_program)
    dev_inst = pretty_midi.Instrument(program=deviant_program)
    dur = ioi * 0.85
    for i in range(n_total):
        t = i * ioi
        if i in deviant_positions:
            dev_inst.notes.append(Note(velocity=velocity, pitch=pitch,
                                       start=t, end=t + dur))
        else:
            std_inst.notes.append(Note(velocity=velocity, pitch=pitch,
                                       start=t, end=t + dur))
    pm.instruments.append(std_inst)
    pm.instruments.append(dev_inst)
    return pm


def _pm_rhythm_oddball(pitch, bpm, n_bars, deviant_bars,
                       program=PIANO, velocity=80):
    """Rhythm oddball: regular beat with timing violations in deviant bars.

    Vuust et al 2012: rhythmic expectation violation.
    """
    ioi = 60.0 / bpm
    dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    beat = 0
    for bar in range(n_bars):
        for pos in range(4):  # 4 beats per bar
            t = beat * ioi
            if bar in deviant_bars and pos == 2:
                # Shift beat 3 by +30% IOI (early accent)
                t += ioi * 0.3
            inst.notes.append(Note(velocity=velocity, pitch=pitch,
                                   start=t, end=t + dur))
            beat += 1
    pm.instruments.append(inst)
    return pm


def _pm_pattern_repeat(notes, durations, n_repeats, program=PIANO,
                       velocity=80):
    """Repeat a melodic pattern n times — statistical learning stimulus.

    Bridwell 2017: cortical sensitivity to patterned vs random sequences.
    """
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for _ in range(n_repeats):
        for p, d in zip(notes, durations):
            inst.notes.append(Note(velocity=velocity, pitch=p,
                                   start=t, end=t + d - 0.02))
            t += d
    pm.instruments.append(inst)
    return pm


def _pm_alternating_instruments(pitch, programs, notes_per_inst, ioi,
                                velocity=80):
    """Alternate between instruments — rapid timbre switching.

    High timbre_change[24], tests flexibility/reconfiguration.
    """
    pm = pretty_midi.PrettyMIDI()
    instruments = {p: pretty_midi.Instrument(program=p) for p in programs}
    dur = ioi * 0.85
    total = len(programs) * notes_per_inst
    for i in range(total):
        prog = programs[i % len(programs)]
        t = i * ioi
        instruments[prog].notes.append(Note(velocity=velocity, pitch=pitch,
                                            start=t, end=t + dur))
    for inst in instruments.values():
        pm.instruments.append(inst)
    return pm


# =====================================================================
# Category 1: TSCP — Timbre-Specific Cortical Plasticity
# =====================================================================
def generate_tscp_stimuli():
    """14 stimuli targeting trained_timbre_recognition + plasticity_magnitude.

    Key R³ drivers: tristimulus[18:21], inharmonicity[5], tonalness[14],
    warmth[12], sharpness[13], timbre_change[24], x_l5l7[41:47].

    Pantev et al 2001: timbre-specific N1m enhancement, double dissociation
    violinists > trumpeters for violin timbre, trumpeters > violinists for
    trumpet timbre (MEG N=17, F(1,15)=28.55, p=.00008).
    """
    stimuli = []

    # 01 — Piano C4 sustained (reference timbre)
    pm = _pm_note(C4, 6.0, PIANO, 80)
    save(pm, "tscp", "01_piano_c4_sustained", {
        "description": "Piano C4 sustained 6s — balanced tristimulus, moderate "
                       "inharmonicity, standard reference timbre.",
        "expected": {"trained_timbre_recognition": "MODERATE",
                     "plasticity_magnitude": "MODERATE"},
        "science": "Pantev 2001: piano has intermediate harmonic complexity."})
    stimuli.append("01_piano_c4_sustained")

    # 02 — Violin C4 sustained (rich harmonics)
    pm = _pm_note(C4, 6.0, VIOLIN, 80)
    save(pm, "tscp", "02_violin_c4_sustained", {
        "description": "Violin C4 sustained 6s — high trist1 (fundamental "
                       "dominant), low inharmonicity, high tonalness.",
        "expected": {"trained_timbre_recognition": "HIGH",
                     "plasticity_magnitude": "HIGH"},
        "science": "Pantev 2001: violinists show enhanced N1m for violin "
                   "timbre specifically."})
    stimuli.append("02_violin_c4_sustained")

    # 03 — Trumpet C4 sustained (bright)
    pm = _pm_note(C4, 6.0, TRUMPET, 85)
    save(pm, "tscp", "03_trumpet_c4_sustained", {
        "description": "Trumpet C4 sustained 6s — high trist2/trist3 "
                       "(high-harmonic energy), high sharpness.",
        "expected": {"trained_timbre_recognition": "HIGH",
                     "plasticity_magnitude": "HIGH"},
        "science": "Pantev 2001: trumpeters show enhanced N1m for trumpet "
                   "timbre specifically."})
    stimuli.append("03_trumpet_c4_sustained")

    # 04 — Flute C5 sustained (simple breathy)
    pm = _pm_note(C5, 6.0, FLUTE, 75)
    save(pm, "tscp", "04_flute_c5_sustained", {
        "description": "Flute C5 sustained 6s — very high trist1, near-zero "
                       "trist2/trist3, minimal inharmonicity.",
        "expected": {"trained_timbre_recognition": "LOW-MODERATE",
                     "plasticity_magnitude": "LOW"},
        "science": "Alluri et al 2012: timbral brightness activates bilateral "
                   "STG (fMRI N=11, Z=8.13)."})
    stimuli.append("04_flute_c5_sustained")

    # 05 — Organ C4 sustained (sustained complex)
    pm = _pm_note(C4, 6.0, ORGAN, 80)
    save(pm, "tscp", "05_organ_c4_sustained", {
        "description": "Organ C4 sustained 6s — high all three tristimulus "
                       "components, very low inharmonicity, rich timbre.",
        "expected": {"trained_timbre_recognition": "MODERATE-HIGH",
                     "plasticity_magnitude": "MODERATE"},
        "science": "Sturm et al 2014: spectral centroid has distinct STG "
                   "activation spots (ECoG high-gamma)."})
    stimuli.append("05_organ_c4_sustained")

    # 06 — Guitar nylon C4 sustained (plucked, decaying)
    pm = _pm_note(C4, 6.0, GUITAR_NYLON, 80)
    save(pm, "tscp", "06_guitar_nylon_c4_sustained", {
        "description": "Nylon guitar C4 sustained 6s — percussive attack, "
                       "rapid decay, moderate inharmonicity.",
        "expected": {"trained_timbre_recognition": "MODERATE",
                     "plasticity_magnitude": "LOW-MODERATE"},
        "science": "Bellmann & Asano 2024: ALE meta-analysis k=18 N=338 — "
                   "4 clusters bilateral pSTG/HG/SMG (4640 mm³)."})
    stimuli.append("06_guitar_nylon_c4_sustained")

    # 07 — Cello C3 sustained (warm, low register)
    pm = _pm_note(C3, 6.0, CELLO, 80)
    save(pm, "tscp", "07_cello_c3_sustained", {
        "description": "Cello C3 sustained 6s — high warmth, low sharpness, "
                       "rich low-frequency harmonic content.",
        "expected": {"trained_timbre_recognition": "HIGH",
                     "plasticity_magnitude": "MODERATE-HIGH"},
        "science": "Halpern et al 2004: timbre imagery activates posterior "
                   "PT overlapping with perception (R STG t=4.66)."})
    stimuli.append("07_cello_c3_sustained")

    # 08 — Piano C major phrase (melodic context)
    notes = [C4, D4, E4, F4, G4, A4, B4, C5]
    durs = [0.5] * 8
    pm = _pm_melody(notes, durs, PIANO, 80)
    save(pm, "tscp", "08_piano_phrase_c_major", {
        "description": "Piano C major ascending scale 4s — consistent timbre "
                       "across pitch range, low timbre_change.",
        "expected": {"trained_timbre_recognition": "MODERATE-HIGH",
                     "plasticity_magnitude": "MODERATE"},
        "science": "Santoyo et al 2023: enhanced theta phase-locking for "
                   "timbre-based streams in musicians (EEG N=23)."})
    stimuli.append("08_piano_phrase_c_major")

    # 09 — Violin C major phrase (same melody, different timbre)
    pm = _pm_melody(notes, durs, VIOLIN, 80)
    save(pm, "tscp", "09_violin_phrase_c_major", {
        "description": "Violin C major ascending scale 4s — rich sustained "
                       "timbre, continuous bowing character.",
        "expected": {"trained_timbre_recognition": "HIGH",
                     "plasticity_magnitude": "MODERATE-HIGH"},
        "science": "Pantev 2001: trained timbre > untrained timbre for N1m."})
    stimuli.append("09_violin_phrase_c_major")

    # 10 — Piano repeated C4 (timbre consistency)
    pm = _pm_isochronous(C4, 120, 24, PIANO, 80)
    save(pm, "tscp", "10_piano_repeated_c4", {
        "description": "Piano C4 repeated 24 beats at 120bpm — maximal "
                       "timbre consistency, minimal timbre_change[24].",
        "expected": {"trained_timbre_recognition": "MODERATE-HIGH",
                     "plasticity_magnitude": "MODERATE"},
        "science": "Whiteford et al 2025: plasticity must be cortical NOT "
                   "subcortical (N>260, d=-0.064, BF=0.13 for null)."})
    stimuli.append("10_piano_repeated_c4")

    # 11 — Multi-instrument ensemble (timbre richness)
    pm = _pm_ensemble_chord(
        [([C4, E4, G4], PIANO, 75),
         ([C4], VIOLIN, 80),
         ([G3], CELLO, 75),
         ([C5], FLUTE, 70)],
        duration=6.0,
    )
    save(pm, "tscp", "11_multi_instrument_ensemble", {
        "description": "Piano+Violin+Cello+Flute C major 6s — maximal "
                       "timbral diversity, high x_l5l7 coupling.",
        "expected": {"trained_timbre_recognition": "HIGH",
                     "plasticity_magnitude": "HIGH"},
        "science": "Bellmann & Asano 2024: bilateral pSTG/HG responds to "
                   "timbral richness."})
    stimuli.append("11_multi_instrument_ensemble")

    # 12 — Rapid timbre alternation (high timbre_change)
    pm = _pm_alternating_instruments(
        C4, [PIANO, VIOLIN, FLUTE, TRUMPET], notes_per_inst=6,
        ioi=0.4, velocity=80,
    )
    save(pm, "tscp", "12_rapid_timbre_alternation", {
        "description": "C4 alternating Piano→Violin→Flute→Trumpet 24 notes — "
                       "maximal timbre_change[24], high spectral flux.",
        "expected": {"trained_timbre_recognition": "MODERATE",
                     "plasticity_magnitude": "HIGH"},
        "science": "Pantev 2001: timbre specificity requires consistent "
                   "exposure; rapid switching tests flexibility."})
    stimuli.append("12_rapid_timbre_alternation")

    # 13 — Harpsichord C4 sustained (distinct from piano)
    pm = _pm_note(C4, 6.0, HARPSICHORD, 80)
    save(pm, "tscp", "13_harpsichord_c4_sustained", {
        "description": "Harpsichord C4 sustained 6s — plucked mechanism, "
                       "acoustically similar to piano but distinct timbre.",
        "expected": {"trained_timbre_recognition": "MODERATE",
                     "plasticity_magnitude": "MODERATE"},
        "science": "Pantev 2001: generalization gradient — acoustically "
                   "similar instruments show partial transfer."})
    stimuli.append("13_harpsichord_c4_sustained")

    # 14 — Near silence (floor)
    pm = _pm_near_silence(5.0)
    save(pm, "tscp", "14_near_silence", {
        "description": "Near silence 5s — vel=1 tick, floor for all beliefs.",
        "expected": {"trained_timbre_recognition": "FLOOR",
                     "plasticity_magnitude": "FLOOR"},
        "science": "Control condition."})
    stimuli.append("14_near_silence")

    return stimuli


# =====================================================================
# Category 2: ESME — Expertise-Specific MMN Enhancement
# =====================================================================
def generate_esme_stimuli():
    """15 stimuli targeting expertise_enhancement, pitch_mmn, rhythm_mmn,
    timbre_mmn, expertise_trajectory.

    Key R³ drivers: helmholtz_kang[2], onset_strength[11],
    spectral_change[21], pitch_change[23], tristimulus[18:21],
    timbre_change[24], x_l4l5[33:41].

    Koelsch Schroger & Tervaniemi 1999 (EEG N~20/grp): violinists MMN
    to 0.75% pitch deviants absent in non-musicians.
    Vuust et al 2012 (EEG N~40-60): genre-specific gradient
    jazz > rock > pop > non-musicians.
    """
    stimuli = []
    ioi = 0.5  # 120 bpm equivalent

    # Deviant positions: ~15% deviance rate, pseudo-random
    deviant_pos = {4, 9, 14, 19, 25, 30, 36, 41}

    # 01 — Standard repeated (no deviants, baseline)
    pm = _pm_isochronous(C4, 120, 48, PIANO, 80)
    save(pm, "esme", "01_piano_standard_repeated", {
        "description": "Piano C4 repeated 48 beats at 120bpm — all standard, "
                       "no deviants. Baseline for MMN comparison.",
        "expected": {"pitch_mmn": "LOW", "rhythm_mmn": "LOW",
                     "timbre_mmn": "LOW", "expertise_enhancement": "LOW"},
        "science": "Control: pure standard stream has no prediction error."})
    stimuli.append("01_piano_standard_repeated")

    # 02 — Pitch deviant small (1 semitone = C#4)
    pm = _pm_oddball_sequence(C4, Db4, 48, deviant_pos, ioi, PIANO)
    save(pm, "esme", "02_piano_pitch_deviant_small", {
        "description": "Piano oddball: C4 standard, C#4 deviant (1 semitone), "
                       "15% rate. Small pitch_change[23] at deviants.",
        "expected": {"pitch_mmn": "MODERATE", "expertise_enhancement": "MODERATE"},
        "science": "Koelsch et al 1999: musicians detect 0.75% pitch deviants; "
                   "1 semitone = ~6% difference, well above threshold."})
    stimuli.append("02_piano_pitch_deviant_small")

    # 03 — Pitch deviant large (4 semitones = E4)
    pm = _pm_oddball_sequence(C4, E4, 48, deviant_pos, ioi, PIANO)
    save(pm, "esme", "03_piano_pitch_deviant_large", {
        "description": "Piano oddball: C4 standard, E4 deviant (4 semitones), "
                       "15% rate. Large pitch_change[23] at deviants.",
        "expected": {"pitch_mmn": "HIGH", "expertise_enhancement": "HIGH"},
        "science": "Wagner et al 2018: pre-attentive harmonic interval MMN "
                   "(-0.34 uV, p=0.003, N=15)."})
    stimuli.append("03_piano_pitch_deviant_large")

    # 04 — Pitch deviant tritone (6 semitones = Gb4)
    pm = _pm_oddball_sequence(C4, Gb4, 48, deviant_pos, ioi, PIANO)
    save(pm, "esme", "04_piano_pitch_deviant_tritone", {
        "description": "Piano oddball: C4 standard, Gb4 deviant (tritone), "
                       "15% rate. Maximally dissonant deviant.",
        "expected": {"pitch_mmn": "HIGH", "expertise_enhancement": "HIGH"},
        "science": "Crespo-Bojorque et al 2018: dissonance latency >> "
                   "consonance latency (F(1,15)=155.03, p<.001)."})
    stimuli.append("04_piano_pitch_deviant_tritone")

    # 05 — Rhythm regular (no deviants, baseline for rhythm)
    pm = _pm_isochronous(C4, 120, 48, PIANO, 80)
    save(pm, "esme", "05_piano_rhythm_regular", {
        "description": "Piano C4 at 120bpm perfectly isochronous — baseline "
                       "for rhythm MMN comparison.",
        "expected": {"rhythm_mmn": "LOW", "expertise_enhancement": "LOW"},
        "science": "Control: perfect regularity has no timing prediction error."})
    stimuli.append("05_piano_rhythm_regular")

    # 06 — Rhythm deviant (timing violation)
    pm = _pm_rhythm_oddball(C4, 120, 12, deviant_bars={2, 5, 8, 11},
                            program=PIANO, velocity=80)
    save(pm, "esme", "06_piano_rhythm_deviant", {
        "description": "Piano C4 at 120bpm with beat-3 shifted +30% IOI in "
                       "bars 3,6,9,12. Onset_strength[11] disrupted.",
        "expected": {"rhythm_mmn": "HIGH", "expertise_enhancement": "MODERATE"},
        "science": "Vuust et al 2012: rhythmic expectation violation produces "
                   "enhanced MMN in musicians."})
    stimuli.append("06_piano_rhythm_deviant")

    # 07 — Timbre oddball (piano standard, violin deviant)
    pm = _pm_timbre_oddball(PIANO, VIOLIN, C4, 48, deviant_pos, ioi)
    save(pm, "esme", "07_piano_timbre_deviant_violin", {
        "description": "Piano standard, violin deviant at C4, 15% rate. "
                       "Timbre_change[24] spikes at deviants.",
        "expected": {"timbre_mmn": "HIGH", "expertise_enhancement": "MODERATE"},
        "science": "Pantev 2001: timbre-specific N1m enhancement for trained "
                   "instrument (F(1,15)=28.55, p=.00008)."})
    stimuli.append("07_piano_timbre_deviant_violin")

    # 08 — Timbre oddball (piano standard, trumpet deviant)
    pm = _pm_timbre_oddball(PIANO, TRUMPET, C4, 48, deviant_pos, ioi)
    save(pm, "esme", "08_piano_timbre_deviant_trumpet", {
        "description": "Piano standard, trumpet deviant at C4, 15% rate. "
                       "Contrasting timbral family (brass vs keyboard).",
        "expected": {"timbre_mmn": "HIGH", "expertise_enhancement": "MODERATE"},
        "science": "Pantev 2001: double dissociation — instrument-specific "
                   "cortical enhancement."})
    stimuli.append("08_piano_timbre_deviant_trumpet")

    # 09 — Combined deviants (pitch + timbre)
    pm = pretty_midi.PrettyMIDI()
    std_inst = pretty_midi.Instrument(program=PIANO)
    dev_inst = pretty_midi.Instrument(program=VIOLIN)
    dur = ioi * 0.85
    for i in range(48):
        t = i * ioi
        if i in deviant_pos:
            dev_inst.notes.append(Note(velocity=80, pitch=E4,
                                       start=t, end=t + dur))
        else:
            std_inst.notes.append(Note(velocity=80, pitch=C4,
                                       start=t, end=t + dur))
    pm.instruments.append(std_inst)
    pm.instruments.append(dev_inst)
    save(pm, "esme", "09_combined_pitch_timbre_deviant", {
        "description": "Piano-C4 standard, Violin-E4 deviant — simultaneous "
                       "pitch (M3) + timbre change at 15% rate.",
        "expected": {"pitch_mmn": "HIGH", "timbre_mmn": "HIGH",
                     "expertise_enhancement": "HIGH"},
        "science": "Fong et al 2020: MMN as prediction error under Bayesian "
                   "framework; combined deviants test subadditivity."})
    stimuli.append("09_combined_pitch_timbre_deviant")

    # 10 — Jazz-complexity melody (complex intervals, syncopation)
    jazz_notes = [C4, Eb4, G4, Bb4, Ab4, F4, D4, Gb4,
                  E4, A4, Db4, G4, C5, Bb4, Ab4, E4]
    jazz_durs = [0.35, 0.25, 0.4, 0.3, 0.35, 0.25, 0.4, 0.3,
                 0.35, 0.25, 0.4, 0.3, 0.35, 0.25, 0.4, 0.3]
    pm = _pm_melody(jazz_notes, jazz_durs, PIANO, 85)
    save(pm, "esme", "10_jazz_complex_melody", {
        "description": "Jazz-like melody with chromatic intervals, syncopated "
                       "rhythm — high pitch_change[23], variable onset spacing.",
        "expected": {"pitch_mmn": "HIGH", "rhythm_mmn": "MODERATE-HIGH",
                     "expertise_enhancement": "HIGH"},
        "science": "Vuust et al 2012: jazz musicians show strongest rhythm "
                   "MMN — genre-specific gradient."})
    stimuli.append("10_jazz_complex_melody")

    # 11 — Simple repeated riff (rock-like)
    rock_notes = [E4, E4, G4, A4] * 6
    rock_durs = [0.3, 0.3, 0.3, 0.3] * 6
    pm = _pm_melody(rock_notes, rock_durs, GUITAR_STEEL, 90)
    save(pm, "esme", "11_rock_simple_riff", {
        "description": "Simple 4-note rock riff repeated 6x on steel guitar — "
                       "moderate predictability, low pitch_change.",
        "expected": {"pitch_mmn": "LOW", "rhythm_mmn": "LOW",
                     "expertise_enhancement": "MODERATE"},
        "science": "Vuust 2012: rock < jazz for MMN amplitude."})
    stimuli.append("11_rock_simple_riff")

    # 12 — Highly predictable pop melody
    pop_notes = [C4, C4, G4, G4, A4, A4, G4] * 4
    pop_durs = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0] * 4
    pm = _pm_melody(pop_notes, pop_durs, PIANO, 75)
    save(pm, "esme", "12_pop_predictable_melody", {
        "description": "Highly predictable 'Twinkle'-like melody repeated 4x — "
                       "minimal pitch_change, very regular rhythm.",
        "expected": {"pitch_mmn": "LOW", "rhythm_mmn": "LOW",
                     "expertise_enhancement": "LOW"},
        "science": "Vuust 2012: pop < rock < jazz for MMN."})
    stimuli.append("12_pop_predictable_melody")

    # 13 — Melodic context deviant (tonal violation in phrase)
    context_notes = [C4, D4, E4, F4, G4, A4, B4, C5,
                     C5, B4, A4, G4, F4, E4, D4, C4,
                     C4, D4, E4, F4, G4, A4, Gb4, C5]  # Gb4 = deviant
    context_durs = [0.35] * 24
    pm = _pm_melody(context_notes, context_durs, PIANO, 80)
    save(pm, "esme", "13_melodic_context_deviant", {
        "description": "C major scale up-down-up with Gb4 replacing B4 in "
                       "third pass — melodic context violation.",
        "expected": {"pitch_mmn": "MODERATE-HIGH",
                     "expertise_enhancement": "MODERATE"},
        "science": "Rupp & Hansen 2022: context-dependent MMR — musicians > "
                   "NM in melodic paradigm but = NM in oddball (MEG)."})
    stimuli.append("13_melodic_context_deviant")

    # 14 — Dense random (noise floor for MMN)
    pm = _pm_dense_random(8.0, seed=200, notes_per_sec=6)
    save(pm, "esme", "14_dense_random_notes", {
        "description": "Random pitches + velocities 6/s for 8s — no statistical "
                       "regularity, maximal prediction error at every note.",
        "expected": {"pitch_mmn": "MODERATE", "rhythm_mmn": "MODERATE",
                     "expertise_enhancement": "LOW"},
        "science": "Carbajal & Malmierca 2018: SSA (stimulus-specific "
                   "adaptation) requires regularity to generate prediction."})
    stimuli.append("14_dense_random_notes")

    # 15 — Near silence (floor)
    pm = _pm_near_silence(5.0)
    save(pm, "esme", "15_near_silence", {
        "description": "Near silence 5s — floor for all ESME beliefs.",
        "expected": {"pitch_mmn": "FLOOR", "rhythm_mmn": "FLOOR",
                     "timbre_mmn": "FLOOR", "expertise_enhancement": "FLOOR"},
        "science": "Control condition."})
    stimuli.append("15_near_silence")

    return stimuli


# =====================================================================
# Category 3: EDNR — Expertise-Dependent Network Reorganization
# =====================================================================
def generate_ednr_stimuli():
    """12 stimuli targeting network_specialization + within_connectivity.

    Key R³ drivers: x_l0l5[25:33], x_l4l5[33:41], tonalness[14],
    sensory_pleasantness[4], spectral_flatness[16], loudness[8].

    Paraskevopoulos et al 2022 (MEG/PTE N=25): musicians 106 within vs
    192 between network edges; IFG area 47m hub (Hedges' g=-1.09).
    Moller et al 2021 (DTI+CT N=45): musicians local-only CT correlations.
    """
    stimuli = []

    # 01 — Consonant tonal chord (high pleasantness + tonalness)
    pm = _pm_chord(C_MAJ, 6.0, PIANO, 80)
    save(pm, "ednr", "01_piano_consonant_chord", {
        "description": "C major triad 6s — high sensory_pleasantness[4], "
                       "high tonalness[14], low spectral_flatness[16].",
        "expected": {"network_specialization": "MODERATE-HIGH",
                     "within_connectivity": "HIGH"},
        "science": "Papadaki et al 2023: network strength correlates with "
                   "interval recognition (N=41, d=0.70, rho=0.36)."})
    stimuli.append("01_piano_consonant_chord")

    # 02 — Dissonant chromatic cluster (low pleasantness)
    pm = _pm_chord(chromatic_cluster(C4, 6), 6.0, PIANO, 80)
    save(pm, "ednr", "02_piano_chromatic_cluster", {
        "description": "6-note chromatic cluster C4-F4 for 6s — low "
                       "sensory_pleasantness[4], high spectral_flatness[16].",
        "expected": {"network_specialization": "LOW",
                     "within_connectivity": "LOW"},
        "science": "Paraskevopoulos 2022: tonal processing drives within-"
                   "network specialization."})
    stimuli.append("02_piano_chromatic_cluster")

    # 03 — Harmonic progression (I-IV-V-I repeated)
    prog = [C_MAJ, F_MAJ, G_MAJ, C_MAJ] * 3
    durs = [1.5] * 12
    pm = _pm_progression(prog, durs, PIANO, 75)
    save(pm, "ednr", "03_piano_harmonic_progression", {
        "description": "I-IV-V-I x3 in C major on piano — sustained tonal "
                       "context, high tonalness over time.",
        "expected": {"network_specialization": "HIGH",
                     "within_connectivity": "HIGH"},
        "science": "Leipold et al 2021: musicianship effects on FC replicable "
                   "across AP/non-AP (N=153, pFWE<0.05)."})
    stimuli.append("03_piano_harmonic_progression")

    # 04 — Multi-instrument tonal ensemble
    pm = _pm_ensemble_chord(
        [([C4, E4, G4], PIANO, 75),
         ([C4, G4], STRINGS, 70),
         ([E4], VIOLIN, 80),
         ([C3], CELLO, 75)],
        duration=6.0,
    )
    save(pm, "ednr", "04_multi_instrument_tonal", {
        "description": "Piano+Strings+Violin+Cello C major ensemble — maximal "
                       "x_l0l5 (within-network) and x_l4l5 (cross-network).",
        "expected": {"network_specialization": "HIGH",
                     "within_connectivity": "HIGH"},
        "science": "Paraskevopoulos 2022: IFG area 47m supramodal hub; "
                   "multi-instrument activates broader network."})
    stimuli.append("04_multi_instrument_tonal")

    # 05 — Single note simple (minimal complexity)
    pm = _pm_note(C4, 6.0, PIANO, 70)
    save(pm, "ednr", "05_single_note_simple", {
        "description": "Single piano C4 sustained 6s — minimal network "
                       "demand, low x_l0l5 and x_l4l5.",
        "expected": {"network_specialization": "LOW-MODERATE",
                     "within_connectivity": "LOW-MODERATE"},
        "science": "Moller 2021: musicians show only local CT correlations; "
                   "single source = minimal network engagement."})
    stimuli.append("05_single_note_simple")

    # 06 — Dense atonal random (high flatness, low tonalness)
    pm = _pm_dense_random(6.0, seed=300, notes_per_sec=10)
    save(pm, "ednr", "06_dense_atonal_random", {
        "description": "Random pitches 10/s for 6s — high spectral_flatness, "
                       "low tonalness, no musical structure.",
        "expected": {"network_specialization": "LOW",
                     "within_connectivity": "LOW"},
        "science": "Paraskevopoulos 2022: within-network edges driven by "
                   "tonal processing expertise."})
    stimuli.append("06_dense_atonal_random")

    # 07 — String quartet tonal (rich within-family coupling)
    pm = _pm_ensemble_chord(
        [([G4], VIOLIN, 80),
         ([E4], VIOLIN, 75),
         ([C4], VIOLA, 75),
         ([C3], CELLO, 80)],
        duration=6.0,
    )
    save(pm, "ednr", "07_string_quartet_tonal", {
        "description": "String quartet (2 Vln + Vla + Vc) C major — same "
                       "instrument family, high within-network coupling.",
        "expected": {"network_specialization": "HIGH",
                     "within_connectivity": "HIGH"},
        "science": "Leipold 2021: intrahemispheric FC enhanced in musicians."})
    stimuli.append("07_string_quartet_tonal")

    # 08 — Brass trio (different timbre family, tonal)
    pm = _pm_ensemble_chord(
        [([C4], TRUMPET, 80),
         ([E4], FRENCH_HORN, 75),
         ([G3], TROMBONE, 75)],
        duration=6.0,
    )
    save(pm, "ednr", "08_brass_trio_tonal", {
        "description": "Trumpet+Horn+Trombone C major — brass family, tonal "
                       "but different timbral coupling pattern.",
        "expected": {"network_specialization": "MODERATE-HIGH",
                     "within_connectivity": "MODERATE-HIGH"},
        "science": "Papadaki 2023: professionals > amateurs for network "
                   "strength and global efficiency."})
    stimuli.append("08_brass_trio_tonal")

    # 09 — Full orchestra tonal (maximum network engagement)
    pm = _pm_ensemble_chord(
        [([C4, E4, G4], PIANO, 70),
         ([C4, G4], STRINGS, 65),
         ([E4], VIOLIN, 75),
         ([C3], CELLO, 70),
         ([C4], TRUMPET, 70),
         ([E4], FLUTE, 70),
         ([G3], TROMBONE, 65)],
        duration=6.0,
    )
    save(pm, "ednr", "09_full_orchestra_tonal", {
        "description": "7-instrument orchestra C major — maximal network "
                       "activation across all coupling dimensions.",
        "expected": {"network_specialization": "HIGH",
                     "within_connectivity": "HIGH"},
        "science": "Criscuolo et al 2022: ALE meta-analysis k=84 N=3005 — "
                   "musicians > NM bilateral STG + L IFG (BA44)."})
    stimuli.append("09_full_orchestra_tonal")

    # 10 — Sustained noise-like (chromatic cluster rapid)
    rng = np.random.RandomState(301)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    for i in range(100):
        t = i * 0.06
        p = int(rng.randint(48, 73))  # cluster range C3-C5
        inst.notes.append(Note(velocity=60, pitch=p,
                               start=t, end=t + 0.04))
    pm.instruments.append(inst)
    save(pm, "ednr", "10_rapid_chromatic_noise", {
        "description": "Rapid chromatic notes ~16/s across C3-C5 range — "
                       "noise-like, high spectral_flatness, low tonalness.",
        "expected": {"network_specialization": "LOW",
                     "within_connectivity": "LOW"},
        "science": "Cui et al 2025: 1-year training does NOT change WM — "
                   "structural change requires sustained tonal exposure."})
    stimuli.append("10_rapid_chromatic_noise")

    # 11 — Modulating progression (network reconfiguration)
    mod_prog = [C_MAJ, F_MAJ, G_MAJ, C_MAJ,
                Eb_MAJ, Ab_MAJ, [Bb3, D4, F4], Eb_MAJ]
    mod_durs = [1.5] * 8
    pm = _pm_progression(mod_prog, mod_durs, PIANO, 75)
    save(pm, "ednr", "11_modulating_progression", {
        "description": "C major → Eb major modulation via I-IV-V-I in each — "
                       "tests network reconfiguration at key change.",
        "expected": {"network_specialization": "MODERATE-HIGH",
                     "within_connectivity": "MODERATE-HIGH"},
        "science": "Olszewska et al 2021: training-induced brain "
                   "reorganization via dynamic reconfiguration."})
    stimuli.append("11_modulating_progression")

    # 12 — Near silence (floor)
    pm = _pm_near_silence(5.0)
    save(pm, "ednr", "12_near_silence", {
        "description": "Near silence 5s — floor for all EDNR beliefs.",
        "expected": {"network_specialization": "FLOOR",
                     "within_connectivity": "FLOOR"},
        "science": "Control condition."})
    stimuli.append("12_near_silence")

    return stimuli


# =====================================================================
# Category 4: SLEE — Statistical Learning Expertise Enhancement
# =====================================================================
def generate_slee_stimuli():
    """13 stimuli targeting statistical_model, detection_accuracy,
    multisensory_binding.

    Key R³ drivers: amplitude[7], loudness[8], spectral_flux[10],
    x_l5l6[41:49], pitch_stability[24], x_l4l5[33:41].

    Bridwell 2017 (EEG N=13): 45% amplitude reduction for patterned vs
    random — cortical sensitivity at 4 Hz (r=0.65, p=0.015).
    Paraskevopoulos et al 2022 (MEG N=25): statistical learning accuracy
    (Hedges' g=-1.09, t(23)=-2.815, p<.05).
    """
    stimuli = []

    # 01 — Highly regular pattern (ABAB repeated)
    pattern_notes = [C4, E4, G4, E4] * 8    # 32 notes
    pattern_durs = [0.3] * 32
    pm = _pm_melody(pattern_notes, pattern_durs, PIANO, 80)
    save(pm, "slee", "01_pattern_abab_regular", {
        "description": "C-E-G-E repeated 8x — perfectly predictable 4-note "
                       "pattern. Maximal statistical regularity.",
        "expected": {"statistical_model": "HIGH",
                     "detection_accuracy": "HIGH"},
        "science": "Bridwell 2017: 45% amplitude reduction for patterned vs "
                   "random sequences (N=13, r=0.65)."})
    stimuli.append("01_pattern_abab_regular")

    # 02 — Completely random (no pattern)
    rng = np.random.RandomState(400)
    random_notes = [int(rng.choice(diatonic_scale(C4, 8))) for _ in range(32)]
    random_durs = [0.3] * 32
    pm = _pm_melody(random_notes, random_durs, PIANO, 80)
    save(pm, "slee", "02_random_no_pattern", {
        "description": "32 random diatonic notes in C major — no repeating "
                       "pattern. Statistical learning baseline.",
        "expected": {"statistical_model": "LOW",
                     "detection_accuracy": "LOW"},
        "science": "Bridwell 2017: random sequences produce no cortical "
                   "amplitude reduction (maximal unpredictability)."})
    stimuli.append("02_random_no_pattern")

    # 03 — Ascending sequence repeated (high regularity)
    asc_notes = diatonic_scale(C4, 8)
    asc_durs = [0.4] * 8
    pm = _pm_pattern_repeat(asc_notes, asc_durs, n_repeats=4, program=PIANO)
    save(pm, "slee", "03_ascending_scale_repeated", {
        "description": "C major ascending scale repeated 4x — predictable "
                       "contour, high pitch_stability[24].",
        "expected": {"statistical_model": "HIGH",
                     "detection_accuracy": "HIGH"},
        "science": "Doelling & Poeppel 2015: cortical entrainment 1-8Hz "
                   "enhanced in musicians (MEG N=34)."})
    stimuli.append("03_ascending_scale_repeated")

    # 04 — Irregular timing (moderate regularity)
    rng = np.random.RandomState(401)
    irr_notes = [C4, D4, E4, F4, G4, A4, B4, C5] * 3
    irr_durs = [float(rng.uniform(0.2, 0.5)) for _ in range(24)]
    pm = _pm_melody(irr_notes, irr_durs, PIANO, 80)
    save(pm, "slee", "04_regular_pitch_irregular_timing", {
        "description": "C major scale (regular pitch) with irregular timing — "
                       "pitch regularity present but onset pattern disrupted.",
        "expected": {"statistical_model": "MODERATE",
                     "detection_accuracy": "MODERATE"},
        "science": "Fong et al 2020: MMN as prediction error — temporal "
                   "irregularity reduces statistical model accuracy."})
    stimuli.append("04_regular_pitch_irregular_timing")

    # 05 — Multi-instrument patterned (binding test)
    pm = _pm_ensemble_isochronous(
        [(C4, PIANO, 80), (E4, VIOLIN, 75), (G4, FLUTE, 70)],
        bpm=120, n_beats=24,
    )
    save(pm, "slee", "05_multi_instrument_patterned", {
        "description": "Piano C4 + Violin E4 + Flute G4 at 120bpm isochronous "
                       "— high x_l5l6 cross-modal binding + high regularity.",
        "expected": {"statistical_model": "HIGH",
                     "multisensory_binding": "HIGH"},
        "science": "Paraskevopoulos 2022: IFG area 47m supramodal hub for "
                   "multisensory statistical learning (g=-1.09)."})
    stimuli.append("05_multi_instrument_patterned")

    # 06 — Single instrument random (low binding)
    pm = _pm_dense_random(8.0, seed=402, notes_per_sec=6)
    save(pm, "slee", "06_single_random_no_binding", {
        "description": "Single piano random pitches 6/s — no pattern, no "
                       "multi-instrument binding, low x_l5l6.",
        "expected": {"statistical_model": "LOW",
                     "multisensory_binding": "LOW"},
        "science": "Porfyri et al 2025: unisensory affects only auditory; "
                   "no cross-modal advantage (N=30)."})
    stimuli.append("06_single_random_no_binding")

    # 07 — Medium regularity (3-note pattern with variation)
    med_notes = [C4, E4, G4, C4, E4, A4, C4, E4, G4, C4, E4, B4,
                 C4, E4, G4, C4, E4, G4, C4, E4, A4, C4, E4, G4]
    med_durs = [0.3] * 24
    pm = _pm_melody(med_notes, med_durs, PIANO, 80)
    save(pm, "slee", "07_medium_regularity_pattern", {
        "description": "C-E-G base pattern with occasional substitutions — "
                       "moderate statistical regularity.",
        "expected": {"statistical_model": "MODERATE",
                     "detection_accuracy": "MODERATE-HIGH"},
        "science": "Carbajal & Malmierca 2018: predictive coding hierarchy — "
                   "SSA to MMN to deviance detection."})
    stimuli.append("07_medium_regularity_pattern")

    # 08 — Pattern boundary (pattern → silence → new pattern)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # First pattern: C-E-G-E x4
    t = 0.0
    for _ in range(4):
        for p in [C4, E4, G4, E4]:
            inst.notes.append(Note(velocity=80, pitch=p,
                                   start=t, end=t + 0.28))
            t += 0.3
    # 1s silence gap
    t += 1.0
    # Second pattern: D-F-A-F x4 (different pattern)
    for _ in range(4):
        for p in [D4, F4, A4, F4]:
            inst.notes.append(Note(velocity=80, pitch=p,
                                   start=t, end=t + 0.28))
            t += 0.3
    pm.instruments.append(inst)
    save(pm, "slee", "08_pattern_boundary_switch", {
        "description": "C-E-G-E x4 → 1s silence → D-F-A-F x4 — statistical "
                       "boundary at pattern switch tests detection_accuracy.",
        "expected": {"statistical_model": "MODERATE-HIGH",
                     "detection_accuracy": "HIGH"},
        "science": "Billig 2022: hippocampus supports sequence binding and "
                   "statistical learning at segment boundaries."})
    stimuli.append("08_pattern_boundary_switch")

    # 09 — Very long pattern (16-note repeated)
    long_notes = [C4, D4, E4, G4, A4, G4, E4, D4,
                  C4, E4, G4, C5, G4, E4, D4, C4] * 3  # 48 notes
    long_durs = [0.3] * 48
    pm = _pm_melody(long_notes, long_durs, PIANO, 80)
    save(pm, "slee", "09_long_pattern_repeated", {
        "description": "16-note pattern repeated 3x — complex pattern memory, "
                       "higher exposure needed for statistical model.",
        "expected": {"statistical_model": "MODERATE-HIGH",
                     "detection_accuracy": "MODERATE"},
        "science": "Doelling & Poeppel 2015: longer patterns require more "
                   "exposure but build stronger cortical entrainment."})
    stimuli.append("09_long_pattern_repeated")

    # 10 — Ensemble patterned with variation
    pm = pretty_midi.PrettyMIDI()
    piano_inst = pretty_midi.Instrument(program=PIANO)
    vln_inst = pretty_midi.Instrument(program=VIOLIN)
    t = 0.0
    for rep in range(6):
        for p in [C4, E4, G4, E4]:
            piano_inst.notes.append(Note(velocity=80, pitch=p,
                                         start=t, end=t + 0.28))
            vln_inst.notes.append(Note(velocity=70, pitch=p + 12,
                                       start=t, end=t + 0.28))
            t += 0.3
    pm.instruments.append(piano_inst)
    pm.instruments.append(vln_inst)
    save(pm, "slee", "10_ensemble_pattern_octaves", {
        "description": "Piano + Violin in octaves C-E-G-E x6 — high pattern "
                       "regularity + multi-timbre cross-modal binding.",
        "expected": {"statistical_model": "HIGH",
                     "multisensory_binding": "HIGH"},
        "science": "Porfyri 2025: multisensory training improves audiovisual "
                   "incongruency detection (F(1,28)=4.635, eta-sq=0.168)."})
    stimuli.append("10_ensemble_pattern_octaves")

    # 11 — Gradual pattern emergence (random → pattern)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    rng = np.random.RandomState(403)
    t = 0.0
    # First half: random
    for i in range(16):
        p = int(rng.choice(diatonic_scale(C4, 8)))
        inst.notes.append(Note(velocity=80, pitch=p,
                               start=t, end=t + 0.28))
        t += 0.3
    # Second half: pattern
    for _ in range(4):
        for p in [C4, E4, G4, E4]:
            inst.notes.append(Note(velocity=80, pitch=p,
                                   start=t, end=t + 0.28))
            t += 0.3
    pm.instruments.append(inst)
    save(pm, "slee", "11_random_to_pattern_emergence", {
        "description": "16 random notes → C-E-G-E x4 pattern — statistical "
                       "model builds in second half.",
        "expected": {"statistical_model": "MODERATE",
                     "detection_accuracy": "MODERATE"},
        "science": "Bridwell 2017: cortical sensitivity builds with pattern "
                   "exposure; amplitude reduction emerges over time."})
    stimuli.append("11_random_to_pattern_emergence")

    # 12 — Isochronous rhythm only (no pitch variation)
    pm = _pm_isochronous(C4, 120, 32, PIANO, 80)
    save(pm, "slee", "12_isochronous_single_pitch", {
        "description": "Single pitch C4 at 120bpm 32 beats — maximal temporal "
                       "regularity, minimal pitch information.",
        "expected": {"statistical_model": "MODERATE-HIGH",
                     "detection_accuracy": "MODERATE"},
        "science": "Doelling & Poeppel 2015: isochronous stimuli produce "
                   "strongest temporal entrainment."})
    stimuli.append("12_isochronous_single_pitch")

    # 13 — Near silence (floor)
    pm = _pm_near_silence(5.0)
    save(pm, "slee", "13_near_silence", {
        "description": "Near silence 5s — floor for all SLEE beliefs.",
        "expected": {"statistical_model": "FLOOR",
                     "detection_accuracy": "FLOOR",
                     "multisensory_binding": "FLOOR"},
        "science": "Control condition."})
    stimuli.append("13_near_silence")

    return stimuli


# =====================================================================
# Category 5: ECT — Expertise Compartmentalization Trade-off
# =====================================================================
def generate_ect_stimuli():
    """10 stimuli targeting compartmentalization_cost + transfer_limitation.

    Key R³ drivers: x_l0l5[25:33], x_l4l5[33:41], x_l5l6[41:49],
    spectral_change[21], amplitude[7], loudness[8].

    Paraskevopoulos et al 2022 (MEG N=25): 106 within vs 192 between
    edges; compartmentalization = within/between ratio.
    Moller et al 2021 (DTI+CT N=45): musicians reduced cross-modal
    connectivity (t(42.3)=3.06, p=0.004).
    """
    stimuli = []

    # 01 — Single piano tonal (low compartmentalization demand)
    pm = _pm_chord(C_MAJ, 6.0, PIANO, 80)
    save(pm, "ect", "01_single_piano_tonal", {
        "description": "Piano C major chord 6s — single instrument, low "
                       "cross-network demand, low compartmentalization cost.",
        "expected": {"compartmentalization_cost": "LOW",
                     "transfer_limitation": "LOW"},
        "science": "Paraskevopoulos 2022: within/between ratio low for simple "
                   "single-source tonal stimuli."})
    stimuli.append("01_single_piano_tonal")

    # 02 — Diverse multi-instrument (high compartmentalization demand)
    pm = _pm_ensemble_chord(
        [([C4, E4, G4], PIANO, 75),
         ([C4], TRUMPET, 80),
         ([G3], TROMBONE, 70),
         ([E4], VIOLIN, 75),
         ([C3], CELLO, 70),
         ([G4], FLUTE, 70)],
        duration=6.0,
    )
    save(pm, "ect", "02_diverse_multi_instrument", {
        "description": "6 diverse instruments (keyboard+brass+strings+wind) — "
                       "maximal cross-network demand, high comp. cost.",
        "expected": {"compartmentalization_cost": "HIGH",
                     "transfer_limitation": "MODERATE-HIGH"},
        "science": "Moller 2021: musicians show reduced cross-modal "
                   "connectivity (IFOB FA p<0.001); more instruments = more "
                   "compartmentalization demand."})
    stimuli.append("02_diverse_multi_instrument")

    # 03 — Slow spectral change (low reconfiguration demand)
    notes = [C4, D4, E4, F4, G4, A4, B4, C5]
    durs = [1.0] * 8
    pm = _pm_melody(notes, durs, PIANO, 75)
    save(pm, "ect", "03_slow_spectral_change", {
        "description": "Piano C major scale, 1s per note — slow "
                       "spectral_change[21], low reconfiguration demand.",
        "expected": {"compartmentalization_cost": "LOW",
                     "transfer_limitation": "LOW"},
        "science": "Wu-Chung et al 2025: baseline flexibility moderates "
                   "training benefit (fMRI N=52)."})
    stimuli.append("03_slow_spectral_change")

    # 04 — Rapid spectral change (high reconfiguration demand)
    pm = _pm_dense_random(6.0, seed=500, notes_per_sec=12)
    save(pm, "ect", "04_rapid_spectral_change", {
        "description": "Dense random notes 12/s — rapid spectral_change[21], "
                       "high reconfiguration speed demand.",
        "expected": {"compartmentalization_cost": "HIGH",
                     "transfer_limitation": "HIGH"},
        "science": "Moller 2021: NM benefit more from visual cues — musicians' "
                   "compartmentalization limits cross-modal flexibility."})
    stimuli.append("04_rapid_spectral_change")

    # 05 — Same-family ensemble (strings — low cross-network cost)
    pm = _pm_ensemble_chord(
        [([G4], VIOLIN, 80),
         ([E4], VIOLIN, 75),
         ([C4], VIOLA, 75),
         ([C3], CELLO, 80)],
        duration=6.0,
    )
    save(pm, "ect", "05_same_family_strings", {
        "description": "String quartet (same family) — high within-network "
                       "coupling, low between-network cost.",
        "expected": {"compartmentalization_cost": "LOW-MODERATE",
                     "transfer_limitation": "LOW"},
        "science": "Leipold 2021: intrahemispheric FC enhanced in musicians; "
                   "same-family instruments share processing pathways."})
    stimuli.append("05_same_family_strings")

    # 06 — Mixed-family ensemble (high cross-network cost)
    pm = _pm_ensemble_chord(
        [([C4], PIANO, 75),
         ([E4], TRUMPET, 80),
         ([G3], CELLO, 75),
         ([C5], FLUTE, 70)],
        duration=6.0,
    )
    save(pm, "ect", "06_mixed_family_ensemble", {
        "description": "Piano+Trumpet+Cello+Flute — 4 different instrument "
                       "families, high between-network demand.",
        "expected": {"compartmentalization_cost": "MODERATE-HIGH",
                     "transfer_limitation": "MODERATE"},
        "science": "Paraskevopoulos 2022: 47 vs 15 multilinks between "
                   "networks (p<0.001 FDR)."})
    stimuli.append("06_mixed_family_ensemble")

    # 07 — Rapid instrument alternation (flexibility stress test)
    pm = _pm_alternating_instruments(
        C4, [PIANO, TRUMPET, VIOLIN, FLUTE, ORGAN, CELLO],
        notes_per_inst=5, ioi=0.3, velocity=80,
    )
    save(pm, "ect", "07_rapid_instrument_alternation", {
        "description": "6 instruments alternating rapidly every 300ms — "
                       "maximal flexibility demand, high reconfiguration speed.",
        "expected": {"compartmentalization_cost": "HIGH",
                     "transfer_limitation": "HIGH"},
        "science": "Blasi et al 2025: music training produces neuroplasticity "
                   "but rapid switching stresses network flexibility."})
    stimuli.append("07_rapid_instrument_alternation")

    # 08 — Acoustically similar pair (piano + harpsichord)
    pm = _pm_ensemble_chord(
        [([C4, E4, G4], PIANO, 75),
         ([C4, E4, G4], HARPSICHORD, 75)],
        duration=6.0,
    )
    save(pm, "ect", "08_acoustically_similar_pair", {
        "description": "Piano + Harpsichord C major — acoustically similar "
                       "instruments share processing (low transfer cost).",
        "expected": {"compartmentalization_cost": "LOW",
                     "transfer_limitation": "LOW"},
        "science": "Pantev 2001: generalization gradient — similar instruments "
                   "share cortical representations."})
    stimuli.append("08_acoustically_similar_pair")

    # 09 — Acoustically dissimilar pair (trumpet + cello)
    pm = _pm_ensemble_chord(
        [([C4], TRUMPET, 80),
         ([C3], CELLO, 80)],
        duration=6.0,
    )
    save(pm, "ect", "09_acoustically_dissimilar_pair", {
        "description": "Trumpet + Cello — maximally dissimilar timbres in "
                       "different registers, high cross-domain cost.",
        "expected": {"compartmentalization_cost": "MODERATE",
                     "transfer_limitation": "MODERATE"},
        "science": "Moller 2021: reduced cross-modal connectivity reflects "
                   "compartmentalization cost of specialization."})
    stimuli.append("09_acoustically_dissimilar_pair")

    # 10 — Near silence (floor)
    pm = _pm_near_silence(5.0)
    save(pm, "ect", "10_near_silence", {
        "description": "Near silence 5s — floor for all ECT beliefs.",
        "expected": {"compartmentalization_cost": "FLOOR",
                     "transfer_limitation": "FLOOR"},
        "science": "Control condition."})
    stimuli.append("10_near_silence")

    return stimuli


# =====================================================================
# Category 6: Cross-unit integration (TSCP × ESME × EDNR × SLEE × ECT)
# =====================================================================
def generate_cross_stimuli():
    """10 stimuli testing cross-unit interactions.

    Validates co-activation patterns, dissociations, and integration
    across all five F8 belief units.
    """
    stimuli = []

    # 01 — Rich tonal ensemble (all units active)
    pm = _pm_ensemble_chord(
        [([C4, E4, G4], PIANO, 75),
         ([C4], VIOLIN, 80),
         ([G3], CELLO, 75),
         ([E4], FLUTE, 70)],
        duration=6.0,
    )
    save(pm, "cross", "01_rich_tonal_ensemble", {
        "description": "Piano+Violin+Cello+Flute C major 6s — activates "
                       "TSCP (timbre), EDNR (network), SLEE (binding), "
                       "ECT (multi-instrument cost).",
        "expected": {"trained_timbre_recognition": "HIGH",
                     "network_specialization": "HIGH",
                     "multisensory_binding": "HIGH",
                     "compartmentalization_cost": "MODERATE-HIGH"},
        "science": "Criscuolo 2022: multi-instrument activates bilateral "
                   "STG + L IFG."})
    stimuli.append("01_rich_tonal_ensemble")

    # 02 — Oddball in tonal context (ESME + EDNR co-activation)
    pm = _pm_oddball_sequence(C4, Gb4, 48, {4, 9, 14, 19, 25, 30, 36, 41},
                              0.5, PIANO)
    save(pm, "cross", "02_oddball_tonal_context", {
        "description": "Piano C4 standard with Gb4 (tritone) deviants in "
                       "tonal context — ESME deviance + EDNR tonal network.",
        "expected": {"pitch_mmn": "HIGH",
                     "network_specialization": "MODERATE-HIGH",
                     "expertise_enhancement": "HIGH"},
        "science": "Rupp & Hansen 2022: context-dependent MMR enhanced in "
                   "musicians for melodic paradigm."})
    stimuli.append("02_oddball_tonal_context")

    # 03 — Random atonal solo (all units low)
    pm = _pm_dense_random(6.0, seed=600, notes_per_sec=8)
    save(pm, "cross", "03_random_atonal_solo", {
        "description": "Random atonal notes 8/s — low on all F8 beliefs: "
                       "no trained timbre, no network, no pattern.",
        "expected": {"trained_timbre_recognition": "LOW",
                     "network_specialization": "LOW",
                     "statistical_model": "LOW",
                     "compartmentalization_cost": "LOW"},
        "science": "Bridwell 2017: random = no statistical learning."})
    stimuli.append("03_random_atonal_solo")

    # 04 — Near silence (all units floor)
    pm = _pm_near_silence(5.0)
    save(pm, "cross", "04_near_silence", {
        "description": "Near silence 5s — floor baseline for all units.",
        "expected": {"trained_timbre_recognition": "FLOOR",
                     "network_specialization": "FLOOR",
                     "statistical_model": "FLOOR"},
        "science": "Control condition."})
    stimuli.append("04_near_silence")

    # 05 — Patterned single instrument (SLEE high, ECT low)
    pm = _pm_pattern_repeat([C4, E4, G4, E4], [0.3]*4, 8, PIANO)
    save(pm, "cross", "05_patterned_single_instrument", {
        "description": "Piano C-E-G-E x8 — high SLEE (pattern) but low ECT "
                       "(single instrument, no cross-network demand).",
        "expected": {"statistical_model": "HIGH",
                     "compartmentalization_cost": "LOW",
                     "trained_timbre_recognition": "MODERATE"},
        "science": "Bridwell 2017: pattern learning doesn't require "
                   "multi-instrument complexity."})
    stimuli.append("05_patterned_single_instrument")

    # 06 — Diverse ensemble no pattern (ECT high, SLEE low)
    rng = np.random.RandomState(601)
    pm = pretty_midi.PrettyMIDI()
    for prog in [PIANO, TRUMPET, VIOLIN, FLUTE]:
        inst = pretty_midi.Instrument(program=prog)
        for i in range(12):
            t = i * 0.5
            p = int(rng.randint(48, 73))
            inst.notes.append(Note(velocity=75, pitch=p,
                                   start=t, end=t + 0.4))
        pm.instruments.append(inst)
    save(pm, "cross", "06_diverse_ensemble_no_pattern", {
        "description": "4 instruments playing random notes — high ECT "
                       "(cross-network demand) but low SLEE (no pattern).",
        "expected": {"compartmentalization_cost": "HIGH",
                     "statistical_model": "LOW",
                     "transfer_limitation": "MODERATE-HIGH"},
        "science": "Paraskevopoulos 2022: multi-instrument random = high "
                   "between-network demand without pattern benefit."})
    stimuli.append("06_diverse_ensemble_no_pattern")

    # 07 — Timbre deviant in pattern (TSCP + ESME + SLEE)
    pm = pretty_midi.PrettyMIDI()
    std_inst = pretty_midi.Instrument(program=PIANO)
    dev_inst = pretty_midi.Instrument(program=VIOLIN)
    t = 0.0
    notes_seq = [C4, E4, G4, E4] * 8
    for i, p in enumerate(notes_seq):
        dur = 0.28
        if i in {7, 15, 23, 31}:  # deviant at pattern end
            dev_inst.notes.append(Note(velocity=80, pitch=p,
                                       start=t, end=t + dur))
        else:
            std_inst.notes.append(Note(velocity=80, pitch=p,
                                       start=t, end=t + dur))
        t += 0.3
    pm.instruments.append(std_inst)
    pm.instruments.append(dev_inst)
    save(pm, "cross", "07_timbre_deviant_in_pattern", {
        "description": "C-E-G-E pattern (piano) with violin deviant at every "
                       "4th position — TSCP timbre + ESME MMN + SLEE pattern.",
        "expected": {"timbre_mmn": "HIGH",
                     "statistical_model": "MODERATE-HIGH",
                     "trained_timbre_recognition": "MODERATE"},
        "science": "Tervaniemi 2022: parameters most important in performance "
                   "evoke largest MMN."})
    stimuli.append("07_timbre_deviant_in_pattern")

    # 08 — Expertise ceiling (full complexity)
    pm = _pm_ensemble_chord(
        [([C4, E4, G4], PIANO, 70),
         ([C4, G4], STRINGS, 65),
         ([C4], TRUMPET, 70),
         ([E4], VIOLIN, 75),
         ([C3], CELLO, 70),
         ([G4], FLUTE, 70),
         ([E4], OBOE, 65)],
        duration=6.0,
    )
    save(pm, "cross", "08_expertise_ceiling", {
        "description": "7-instrument orchestra C major — ceiling test for all "
                       "F8 units simultaneously.",
        "expected": {"trained_timbre_recognition": "HIGH",
                     "network_specialization": "HIGH",
                     "compartmentalization_cost": "HIGH"},
        "science": "Bucher et al 2023: Heschl's Gyrus 130% larger in "
                   "professionals; OFC co-activation 25-40ms faster."})
    stimuli.append("08_expertise_ceiling")

    # 09 — Simple familiar melody (TSCP + SLEE, low ECT)
    melody_notes = [C4, C4, G4, G4, A4, A4, G4,
                    F4, F4, E4, E4, D4, D4, C4]
    melody_durs = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0,
                   0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0]
    pm = _pm_melody(melody_notes, melody_durs, PIANO, 80)
    save(pm, "cross", "09_simple_familiar_melody", {
        "description": "Twinkle Twinkle melody on piano — familiar pattern "
                       "(high SLEE) + consistent timbre (TSCP) + low ECT.",
        "expected": {"statistical_model": "HIGH",
                     "trained_timbre_recognition": "MODERATE-HIGH",
                     "compartmentalization_cost": "LOW"},
        "science": "Bonetti et al 2024: hierarchical auditory memory develops "
                   "with expertise; familiar melodies = strong pattern memory."})
    stimuli.append("09_simple_familiar_melody")

    # 10 — Atonal multi-instrument chaos (stress test)
    rng = np.random.RandomState(602)
    pm = pretty_midi.PrettyMIDI()
    for prog in [PIANO, TRUMPET, VIOLIN, FLUTE, ORGAN, CELLO]:
        inst = pretty_midi.Instrument(program=prog)
        for i in range(10):
            t = float(rng.uniform(0, 5.5))
            p = int(rng.randint(36, 85))
            v = int(rng.randint(50, 120))
            inst.notes.append(Note(velocity=v, pitch=p,
                                   start=t, end=t + 0.3))
        pm.instruments.append(inst)
    save(pm, "cross", "10_atonal_multi_chaos", {
        "description": "6 instruments playing random notes at random times — "
                       "maximal chaos, high ECT cost, low SLEE/EDNR.",
        "expected": {"compartmentalization_cost": "HIGH",
                     "statistical_model": "LOW",
                     "network_specialization": "LOW"},
        "science": "Moller 2021: maximal cross-network demand with no "
                   "musical structure."})
    stimuli.append("10_atonal_multi_chaos")

    return stimuli


# =====================================================================
# Category 7: Boundary conditions
# =====================================================================
def generate_boundary_stimuli():
    """8 stimuli testing extreme and edge conditions.

    Standard boundary tests ensuring all F8 beliefs produce valid
    output in the [0, 1] range under any input condition.
    """
    stimuli = []

    # 01 — Near silence
    pm = _pm_near_silence(5.0)
    save(pm, "boundary", "01_near_silence", {
        "description": "Near silence 5s — absolute floor.",
        "expected": {"all": "FLOOR [0, 1]"},
        "science": "Boundary: output must be valid at minimum energy."})
    stimuli.append("01_near_silence")

    # 02 — fff chromatic cluster (maximum amplitude)
    pm = _pm_chord(chromatic_cluster(C4, 8), 4.0, PIANO, 127)
    save(pm, "boundary", "02_fff_cluster", {
        "description": "8-note chromatic cluster at fff (vel=127) — maximum "
                       "amplitude, extreme dissonance.",
        "expected": {"all": "VALID [0, 1]"},
        "science": "Boundary: output must be valid at maximum energy."})
    stimuli.append("02_fff_cluster")

    # 03 — Single click (impulse)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=100, pitch=C4, start=0.0, end=0.02))
    pm.instruments.append(inst)
    save(pm, "boundary", "03_single_click", {
        "description": "Single 20ms click — minimal temporal information.",
        "expected": {"all": "VALID [0, 1]"},
        "science": "Boundary: output must be valid for impulse stimuli."})
    stimuli.append("03_single_click")

    # 04 — Dense random noise (16 notes/sec)
    pm = _pm_dense_random(6.0, seed=700, notes_per_sec=16)
    save(pm, "boundary", "04_dense_random_noise", {
        "description": "16 random notes/s for 6s — noise-like stimulus.",
        "expected": {"all": "VALID [0, 1]"},
        "science": "Boundary: output must handle noise-like input."})
    stimuli.append("04_dense_random_noise")

    # 05 — Very slow (40 bpm)
    pm = _pm_isochronous(C4, 40, 6, PIANO, 80)
    save(pm, "boundary", "05_very_slow_40bpm", {
        "description": "Piano C4 at 40bpm (1.5s IOI) — ultra-macro timescale.",
        "expected": {"all": "VALID [0, 1]"},
        "science": "Boundary: F8 beliefs must handle slow stimuli."})
    stimuli.append("05_very_slow_40bpm")

    # 06 — Very fast (240 bpm)
    pm = _pm_isochronous(C4, 240, 48, PIANO, 80)
    save(pm, "boundary", "06_very_fast_240bpm", {
        "description": "Piano C4 at 240bpm (0.25s IOI) — near upper tempo.",
        "expected": {"all": "VALID [0, 1]"},
        "science": "Boundary: F8 beliefs must handle fast stimuli."})
    stimuli.append("06_very_fast_240bpm")

    # 07 — Extreme register (C1 + C7)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=80, pitch=C1, start=0.0, end=5.0))
    inst.notes.append(Note(velocity=80, pitch=C7, start=0.0, end=5.0))
    pm.instruments.append(inst)
    save(pm, "boundary", "07_extreme_register", {
        "description": "C1 + C7 simultaneously — extreme frequency range.",
        "expected": {"all": "VALID [0, 1]"},
        "science": "Boundary: extreme register must not cause numerical issues."})
    stimuli.append("07_extreme_register")

    # 08 — Long duration (32 bars ~44s)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    ioi = 0.5  # 120bpm
    dur = 0.42
    # AABA form repeated
    A_notes = diatonic_scale(C4, 8)
    B_notes = diatonic_scale(G4, 8)
    for section in [A_notes, A_notes, B_notes, A_notes] * 2:
        for p in section:
            inst.notes.append(Note(velocity=75, pitch=p,
                                   start=t, end=t + dur))
            t += ioi
    pm.instruments.append(inst)
    save(pm, "boundary", "08_long_duration_32bar", {
        "description": "AABA form x2 ~32s — extended duration test.",
        "expected": {"all": "VALID [0, 1]"},
        "science": "Boundary: F8 beliefs must handle long durations."})
    stimuli.append("08_long_duration_32bar")

    return stimuli


# =====================================================================
# Metadata & Catalog
# =====================================================================
def write_metadata():
    """Write metadata.json."""
    path = OUTPUT_DIR / "metadata.json"
    with open(path, "w") as f:
        json.dump(ALL_METADATA, f, indent=2, ensure_ascii=False)
    print(f"  metadata.json  ({len(ALL_METADATA)} entries)")


def write_catalog():
    """Write STIMULUS-CATALOG.md with full ordinal comparison matrix."""
    lines = [
        "# F8 Learning & Plasticity — Stimulus Catalog\n",
        f"**Total stimuli**: {len(ALL_METADATA)}\n",
        "## Target Beliefs (14)\n",
        "| # | Belief | Type | Unit | tau |",
        "|---|--------|------|------|-----|",
        "| 1 | trained_timbre_recognition | Core | TSCP | 0.90 |",
        "| 2 | plasticity_magnitude | Appraisal | TSCP | — |",
        "| 3 | expertise_enhancement | Core | ESME | 0.92 |",
        "| 4 | pitch_mmn | Appraisal | ESME | — |",
        "| 5 | rhythm_mmn | Appraisal | ESME | — |",
        "| 6 | timbre_mmn | Appraisal | ESME | — |",
        "| 7 | expertise_trajectory | Anticipation | ESME | — |",
        "| 8 | network_specialization | Core | EDNR | 0.95 |",
        "| 9 | within_connectivity | Appraisal | EDNR | — |",
        "| 10 | statistical_model | Core | SLEE | 0.88 |",
        "| 11 | detection_accuracy | Appraisal | SLEE | — |",
        "| 12 | multisensory_binding | Appraisal | SLEE | — |",
        "| 13 | compartmentalization_cost | Appraisal | ECT | — |",
        "| 14 | transfer_limitation | Anticipation | ECT | — |",
        "",
        "## Ordinal Comparison Matrix\n",
        "| A | B | Belief | Dir | Science |",
        "|---|---|--------|-----|---------|",
    ]

    comparisons = [
        # TSCP
        ("tscp/02_violin_c4_sustained", "tscp/14_near_silence",
         "trained_timbre_recognition", "A>B",
         "Pantev 2001: instrument timbre > silence"),
        ("tscp/03_trumpet_c4_sustained", "tscp/14_near_silence",
         "trained_timbre_recognition", "A>B",
         "Pantev 2001: instrument timbre > silence"),
        ("tscp/11_multi_instrument_ensemble", "tscp/05_organ_c4_sustained",
         "plasticity_magnitude", "A>B",
         "Bellmann & Asano 2024: timbral richness > single timbre"),
        ("tscp/01_piano_c4_sustained", "tscp/14_near_silence",
         "trained_timbre_recognition", "A>B",
         "Any instrument > silence for timbre recognition"),
        ("tscp/11_multi_instrument_ensemble", "tscp/14_near_silence",
         "trained_timbre_recognition", "A>B",
         "Multi-instrument > silence"),
        # ESME
        ("esme/03_piano_pitch_deviant_large", "esme/01_piano_standard_repeated",
         "pitch_mmn", "A>B",
         "Wagner 2018: large deviant produces MMN (-0.34uV p=0.003)"),
        ("esme/03_piano_pitch_deviant_large", "esme/02_piano_pitch_deviant_small",
         "pitch_mmn", "A>B",
         "Koelsch 1999: larger deviant = larger MMN amplitude"),
        ("esme/06_piano_rhythm_deviant", "esme/05_piano_rhythm_regular",
         "rhythm_mmn", "A>B",
         "Vuust 2012: timing violation > regular rhythm for MMN"),
        ("esme/07_piano_timbre_deviant_violin", "esme/01_piano_standard_repeated",
         "timbre_mmn", "A>B",
         "Pantev 2001: timbre deviant activates timbre-specific MMN"),
        ("esme/10_jazz_complex_melody", "esme/12_pop_predictable_melody",
         "expertise_enhancement", "A>B",
         "Vuust 2012: jazz complexity > pop for expertise MMN"),
        ("esme/09_combined_pitch_timbre_deviant", "esme/03_piano_pitch_deviant_large",
         "expertise_enhancement", "A>B",
         "Fong 2020: combined deviants > single deviant for PE"),
        ("esme/03_piano_pitch_deviant_large", "esme/15_near_silence",
         "pitch_mmn", "A>B",
         "Any deviant > silence for pitch MMN"),
        # EDNR
        ("ednr/01_piano_consonant_chord", "ednr/02_piano_chromatic_cluster",
         "within_connectivity", "A>B",
         "Paraskevopoulos 2022: tonal > atonal for within-network"),
        ("ednr/04_multi_instrument_tonal", "ednr/05_single_note_simple",
         "network_specialization", "A>B",
         "Papadaki 2023: richer activation > simple for network d=0.70"),
        ("ednr/09_full_orchestra_tonal", "ednr/12_near_silence",
         "network_specialization", "A>B",
         "Orchestra > silence for network specialization"),
        ("ednr/03_piano_harmonic_progression", "ednr/06_dense_atonal_random",
         "within_connectivity", "A>B",
         "Leipold 2021: harmonic > atonal for FC (pFWE<0.05)"),
        ("ednr/07_string_quartet_tonal", "ednr/06_dense_atonal_random",
         "network_specialization", "A>B",
         "Moller 2021: tonal ensemble > noise for network"),
        # SLEE
        ("slee/01_pattern_abab_regular", "slee/02_random_no_pattern",
         "statistical_model", "A>B",
         "Bridwell 2017: patterned > random (45% amplitude reduction)"),
        ("slee/01_pattern_abab_regular", "slee/13_near_silence",
         "statistical_model", "A>B",
         "Any pattern > silence for statistical model"),
        ("slee/03_ascending_scale_repeated", "slee/02_random_no_pattern",
         "detection_accuracy", "A>B",
         "Doelling & Poeppel 2015: regular > random for cortical entrainment"),
        ("slee/05_multi_instrument_patterned", "slee/06_single_random_no_binding",
         "multisensory_binding", "A>B",
         "Paraskevopoulos 2022: multi-instrument > single for binding g=-1.09"),
        ("slee/10_ensemble_pattern_octaves", "slee/06_single_random_no_binding",
         "multisensory_binding", "A>B",
         "Porfyri 2025: multisensory > unisensory (eta-sq=0.168)"),
        # ECT
        ("ect/02_diverse_multi_instrument", "ect/01_single_piano_tonal",
         "compartmentalization_cost", "A>B",
         "Paraskevopoulos 2022: 106 within vs 192 between edges"),
        ("ect/07_rapid_instrument_alternation", "ect/03_slow_spectral_change",
         "compartmentalization_cost", "A>B",
         "Moller 2021: rapid switching > slow change for cost"),
        ("ect/06_mixed_family_ensemble", "ect/05_same_family_strings",
         "compartmentalization_cost", "A>B",
         "Leipold 2021: cross-family > same-family for between-network"),
        ("ect/04_rapid_spectral_change", "ect/10_near_silence",
         "transfer_limitation", "A>B",
         "Rapid change > silence for transfer limitation"),
        # Cross-unit
        ("cross/01_rich_tonal_ensemble", "cross/04_near_silence",
         "trained_timbre_recognition", "A>B",
         "Multi-instrument > silence for all F8 beliefs"),
        ("cross/01_rich_tonal_ensemble", "cross/04_near_silence",
         "network_specialization", "A>B",
         "Multi-instrument > silence for all F8 beliefs"),
        ("cross/05_patterned_single_instrument", "cross/04_near_silence",
         "statistical_model", "A>B",
         "Patterned > silence for statistical learning"),
        ("cross/08_expertise_ceiling", "cross/04_near_silence",
         "network_specialization", "A>B",
         "Full orchestra > silence (ceiling test)"),
    ]

    for a, b, belief, direction, science in comparisons:
        lines.append(f"| {a} | {b} | {belief} | {direction} | {science} |")

    lines.append("")
    lines.append("## Stimulus Index\n")
    for key, meta in sorted(ALL_METADATA.items()):
        lines.append(f"### {key}")
        lines.append(f"- {meta['description']}")
        lines.append(f"- Science: {meta['science']}")
        lines.append("")

    path = OUTPUT_DIR / "STIMULUS-CATALOG.md"
    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  STIMULUS-CATALOG.md")


# =====================================================================
# Main
# =====================================================================
def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating F8 Learning & Plasticity test audio...\n")

    s1 = generate_tscp_stimuli()
    print(f"  TSCP:      {len(s1)} stimuli")

    s2 = generate_esme_stimuli()
    print(f"  ESME:      {len(s2)} stimuli")

    s3 = generate_ednr_stimuli()
    print(f"  EDNR:      {len(s3)} stimuli")

    s4 = generate_slee_stimuli()
    print(f"  SLEE:      {len(s4)} stimuli")

    s5 = generate_ect_stimuli()
    print(f"  ECT:       {len(s5)} stimuli")

    s6 = generate_cross_stimuli()
    print(f"  Cross:     {len(s6)} stimuli")

    s7 = generate_boundary_stimuli()
    print(f"  Boundary:  {len(s7)} stimuli")

    total = len(s1) + len(s2) + len(s3) + len(s4) + len(s5) + len(s6) + len(s7)
    print(f"\n  Total: {total} stimuli\n")

    write_metadata()
    write_catalog()
    print("\nDone.")


if __name__ == "__main__":
    main()
