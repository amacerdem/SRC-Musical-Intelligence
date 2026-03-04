"""Deterministic MIDI-based test audio generator for F7 (Motor & Timing).

Generates ~85 stimuli across 6 categories for testing all 17 F7 beliefs:
  - PEOM  (5): period_entrainment, kinematic_efficiency, timing_precision,
               period_lock_strength, next_beat_pred
  - HGSIC (6): groove_quality, beat_prominence, meter_structure,
               auditory_motor_coupling, motor_preparation, groove_trajectory
  - HMCE  (6): context_depth, short_context, medium_context, long_context,
               phrase_boundary_pred, structure_pred

Scientific basis:
  - PEOM:  Thaut 2015 (CTR period entrainment), Grahn & Brett 2007
           (putamen Z=5.67, SMA Z=5.03), Repp 2005 (period correction),
           Fujioka 2012 (beta oscillations), Yamashita 2025 (CV reduction d=-1.10)
  - HGSIC: Janata 2012 (fMRI motor->groove r=0.84), Madison 2011 (inverted-U),
           Witek 2014 (N=66 syncopation-groove), Grahn & Brett 2007
  - HMCE:  Koelsch 2009 (CPS at boundaries), Pearce 2018 (IDyOM),
           Tillmann 2003 (implicit structure fMRI N=20)

Output: .wav + .mid + metadata.json + STIMULUS-CATALOG.md
All files at 44,100 Hz, 16-bit PCM WAV.
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
import pretty_midi
import torch
from scipy.io import wavfile

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from Tests.micro_beliefs.real_audio_stimuli import (
    SAMPLE_RATE,
    _render,
    PIANO, ORGAN, STRINGS, FLUTE, CELLO, CHOIR,
    TRUMPET, TROMBONE, FRENCH_HORN, VIOLIN,
    GUITAR_NYLON, GUITAR_STEEL,
    major_triad, minor_triad, dominant_seventh,
    chromatic_cluster, diatonic_scale,
    C2, D2, E2, F2, G2, A2, B2,
    C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5, A5, B5,
    C6,
)

OUTPUT_DIR = _PROJECT_ROOT / "Test-Audio" / "micro_beliefs" / "f7"
ALL_METADATA: dict = {}

# Extra pitch constants
Bb2 = 46; Bb3 = 58; Db3 = 49; Eb3 = 51; Ab3 = 56
Db5 = 73; Eb5 = 75; Ab5 = 80; Bb5 = 82
C1 = 24; C7 = 96; D6 = 86

# Chord voicings
C_MAJ = major_triad(C4)
C_MIN = minor_triad(C4)
G_DOM7 = dominant_seventh(G3)
F_MAJ = [F3, A3, C4]
A_MIN = [A3, C4, E4]
D_MIN = [D4, F4, A4]
G_MAJ = [G3, B3, D4]
C_MAJ_WIDE = [C3, G3, C4, E4, G4]
Eb_MAJ = [Eb4, G4, Bb4]
D_MAJ = [D4, Gb4, A4]

# GM Drum note numbers (channel 10)
KICK = 36
SNARE = 38
CLOSED_HH = 42
OPEN_HH = 46
RIDE = 51
CRASH = 49
TOM_LOW = 45
TOM_MID = 47
TOM_HI = 48
CLAP = 39
RIMSHOT = 37
SIDESTICK = 37

Note = pretty_midi.Note


# ── Save helper ──────────────────────────────────────────────────────

def save(pm: pretty_midi.PrettyMIDI, group: str, name: str,
         meta: dict, gain: float = 1.0) -> None:
    """Render MIDI -> WAV + save .mid + collect metadata."""
    out_dir = OUTPUT_DIR / group
    out_dir.mkdir(parents=True, exist_ok=True)
    mid_path = out_dir / f"{name}.mid"
    pm.write(str(mid_path))

    audio = _render(pm)
    wav = audio.squeeze(0).numpy()
    if gain != 1.0:
        wav = wav * gain
    peak = np.abs(wav).max()
    if peak > 0:
        wav = wav * (0.95 / peak)
    wav = np.clip(wav, -1.0, 1.0)
    wav_int16 = (wav * 32767).astype(np.int16)

    wav_path = out_dir / f"{name}.wav"
    wavfile.write(str(wav_path), SAMPLE_RATE, wav_int16)

    meta["file"] = f"{group}/{name}.wav"
    meta["duration_s"] = round(len(wav) / SAMPLE_RATE, 2)
    ALL_METADATA[f"{group}/{name}"] = meta


# ── Standard MIDI builder helpers ────────────────────────────────────

def _pm_note(pitch: int, duration: float, program: int = PIANO,
             velocity: int = 80) -> pretty_midi.PrettyMIDI:
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    inst.notes.append(Note(velocity=velocity, pitch=pitch,
                           start=0.0, end=duration))
    pm.instruments.append(inst)
    return pm


def _pm_chord(pitches: list[int], duration: float, program: int = PIANO,
              velocity: int = 80) -> pretty_midi.PrettyMIDI:
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for p in pitches:
        inst.notes.append(Note(velocity=velocity, pitch=p,
                               start=0.0, end=duration))
    pm.instruments.append(inst)
    return pm


def _pm_melody(notes: list[int], durations: list[float],
               program: int = PIANO, velocity: int = 80) -> pretty_midi.PrettyMIDI:
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for pitch, dur in zip(notes, durations):
        inst.notes.append(Note(velocity=velocity, pitch=pitch,
                               start=t, end=t + dur - 0.02))
        t += dur
    pm.instruments.append(inst)
    return pm


def _pm_isochronous(pitch: int, bpm: float, n_beats: int,
                    program: int = PIANO,
                    velocity: int = 80) -> pretty_midi.PrettyMIDI:
    ioi = 60.0 / bpm
    note_dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_beats):
        t = i * ioi
        inst.notes.append(Note(velocity=velocity, pitch=pitch,
                               start=t, end=t + note_dur))
    pm.instruments.append(inst)
    return pm


def _pm_near_silence(duration: float = 5.0) -> pretty_midi.PrettyMIDI:
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=1, pitch=60, start=0.0, end=0.01))
    pm.instruments.append(inst)
    return pm


def _pm_dense_random(duration: float = 5.0, seed: int = 70,
                     notes_per_sec: int = 16) -> pretty_midi.PrettyMIDI:
    rng = np.random.RandomState(seed)
    n_notes = int(duration * notes_per_sec)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    for i in range(n_notes):
        p = int(rng.randint(36, 84))
        t = i * (duration / n_notes)
        inst.notes.append(Note(velocity=int(rng.randint(40, 120)),
                               pitch=p, start=t, end=t + 0.04))
    pm.instruments.append(inst)
    return pm


def _pm_progression(chords: list[list[int]], durations: list[float],
                    program: int = PIANO,
                    velocity: int = 80) -> pretty_midi.PrettyMIDI:
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for pitches, dur in zip(chords, durations):
        for p in pitches:
            inst.notes.append(Note(velocity=velocity, pitch=p,
                                   start=t, end=t + dur - 0.02))
        t += dur
    pm.instruments.append(inst)
    return pm


def _pm_ensemble_chord(voices: list[tuple], duration: float) -> pretty_midi.PrettyMIDI:
    """Multi-instrument chord. voices: list of (pitches, program, velocity)."""
    pm = pretty_midi.PrettyMIDI()
    for pitches, prog, vel in voices:
        inst = pretty_midi.Instrument(program=prog)
        for p in (pitches if isinstance(pitches, list) else [pitches]):
            inst.notes.append(Note(velocity=vel, pitch=p,
                                   start=0.0, end=duration))
        pm.instruments.append(inst)
    return pm


def _pm_ensemble_isochronous(voices: list[tuple], bpm: float,
                             n_beats: int) -> pretty_midi.PrettyMIDI:
    """Multi-instrument synchronized isochronous. voices: (pitches, prog, vel)."""
    ioi = 60.0 / bpm
    note_dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    for pitches, prog, vel in voices:
        inst = pretty_midi.Instrument(program=prog)
        for i in range(n_beats):
            t = i * ioi
            for p in (pitches if isinstance(pitches, list) else [pitches]):
                inst.notes.append(Note(velocity=vel, pitch=p,
                                       start=t, end=t + note_dur))
        pm.instruments.append(inst)
    return pm


# ── F7-Specific MIDI builder helpers ────────────────────────────────


def _pm_drum_pattern(pattern: dict[int, list[int]], bpm: float,
                     n_bars: int = 4, steps_per_bar: int = 16,
                     velocity_map: dict[int, int] | None = None) -> pretty_midi.PrettyMIDI:
    """Create drum pattern from grid notation.

    pattern: {drum_note: [step_indices_within_bar]} e.g. {KICK: [0,8], SNARE: [4,12]}
    steps_per_bar: subdivision (16 = 16th notes)
    velocity_map: optional per-drum velocity override
    """
    step_dur = (60.0 / bpm) * (4.0 / steps_per_bar)
    note_dur = step_dur * 0.5
    vel_map = velocity_map or {}
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    for bar in range(n_bars):
        bar_offset = bar * steps_per_bar * step_dur
        for drum_note, steps in pattern.items():
            vel = vel_map.get(drum_note, 100)
            for step in steps:
                t = bar_offset + step * step_dur
                drums.notes.append(Note(velocity=vel, pitch=drum_note,
                                        start=t, end=t + note_dur))
    pm.instruments.append(drums)
    return pm


def _pm_drum_with_velocity(pattern: dict[int, list[tuple[int, int]]],
                           bpm: float,
                           n_bars: int = 4,
                           steps_per_bar: int = 16) -> pretty_midi.PrettyMIDI:
    """Drum pattern with per-hit velocity. pattern: {note: [(step, vel), ...]}."""
    step_dur = (60.0 / bpm) * (4.0 / steps_per_bar)
    note_dur = step_dur * 0.5
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    for bar in range(n_bars):
        bar_offset = bar * steps_per_bar * step_dur
        for drum_note, hits in pattern.items():
            for step, vel in hits:
                t = bar_offset + step * step_dur
                drums.notes.append(Note(velocity=vel, pitch=drum_note,
                                        start=t, end=t + note_dur))
    pm.instruments.append(drums)
    return pm


def _pm_tempo_shift(pitch: int, bpm_start: float, bpm_end: float,
                    n_beats: int, program: int = PIANO,
                    velocity: int = 80) -> pretty_midi.PrettyMIDI:
    """Gradual tempo change from bpm_start to bpm_end over n_beats."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for i in range(n_beats):
        frac = i / max(n_beats - 1, 1)
        bpm = bpm_start + (bpm_end - bpm_start) * frac
        ioi = 60.0 / bpm
        note_dur = ioi * 0.85
        inst.notes.append(Note(velocity=velocity, pitch=pitch,
                               start=t, end=t + note_dur))
        t += ioi
    pm.instruments.append(inst)
    return pm


def _add_bass_line(pm: pretty_midi.PrettyMIDI, notes: list[int],
                   durations: list[float], program: int = 33,
                   velocity: int = 80) -> None:
    """Add a bass instrument track to existing PrettyMIDI."""
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for pitch, dur in zip(notes, durations):
        inst.notes.append(Note(velocity=velocity, pitch=pitch,
                               start=t, end=t + dur - 0.02))
        t += dur
    pm.instruments.append(inst)


def _add_drum_track(pm: pretty_midi.PrettyMIDI, pattern: dict[int, list[int]],
                    bpm: float, n_bars: int = 4, steps_per_bar: int = 16,
                    velocity_map: dict[int, int] | None = None) -> None:
    """Add a drum track to an existing PrettyMIDI object.

    pattern: {drum_note: [step_indices_within_bar]}
    Same format as _pm_drum_pattern but mutates pm in-place.
    """
    step_dur = (60.0 / bpm) * (4.0 / steps_per_bar)
    note_dur = step_dur * 0.5
    vel_map = velocity_map or {}
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    for bar in range(n_bars):
        bar_offset = bar * steps_per_bar * step_dur
        for drum_note, steps in pattern.items():
            vel = vel_map.get(drum_note, 100)
            for step in steps:
                t = bar_offset + step * step_dur
                drums.notes.append(Note(velocity=vel, pitch=drum_note,
                                        start=t, end=t + note_dur))
    pm.instruments.append(drums)


def _add_chord_track(pm: pretty_midi.PrettyMIDI, chords: list[list[int]],
                     durations: list[float], program: int = PIANO,
                     velocity: int = 65) -> None:
    """Add chord comping track to existing PrettyMIDI."""
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for pitches, dur in zip(chords, durations):
        for p in pitches:
            inst.notes.append(Note(velocity=velocity, pitch=p,
                                   start=t, end=t + dur - 0.02))
        t += dur
    pm.instruments.append(inst)


def _add_melody_track(pm: pretty_midi.PrettyMIDI, notes: list[int],
                      durations: list[float], program: int = FLUTE,
                      velocity: int = 85) -> None:
    """Add melody track to existing PrettyMIDI."""
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for pitch, dur in zip(notes, durations):
        inst.notes.append(Note(velocity=velocity, pitch=pitch,
                               start=t, end=t + dur - 0.02))
        t += dur
    pm.instruments.append(inst)


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 1: PEOM — Period Entrainment Optimization Model (15 stimuli)
#
# Tests: period_entrainment, kinematic_efficiency, timing_precision,
#        period_lock_strength, next_beat_pred
#
# Key R3: [7]amplitude, [10]spectral_flux, [11]onset_strength, [25:33]coupling
# Key H3: beat_periodicity@H16(1s), onset_periodicity@H16(1s),
#          coupling@H3(100ms)/H16(1s)
# ═══════════════════════════════════════════════════════════════════════

def generate_peom_stimuli() -> None:
    """15 stimuli targeting PEOM relay and its 5 beliefs."""

    # ── 01: Piano isochronous 120bpm — HIGH period_entrainment ─────────
    # Perfect isochrony at canonical motor tempo: maximum periodicity.
    # Thaut 2015: CTR produces entrainment at 100-140bpm optimally.
    pm = _pm_isochronous(C4, 120.0, 16, PIANO, 80)
    save(pm, "peom", "01_piano_iso_120bpm", {
        "description": "Piano C4 isochronous 120bpm, 16 beats, 8s",
        "expected": {
            "period_entrainment": "HIGH — perfect isochrony at optimal tempo",
            "timing_precision": "HIGH — zero CV, max periodicity",
            "period_lock_strength": "HIGH — stable phase lock",
            "next_beat_pred": "HIGH — perfectly predictable",
        },
        "science": "Thaut 2015: CTR entrainment optimal 100-140bpm",
    })

    # ── 02: Piano isochronous 80bpm — HIGH entrainment at slow rate ───
    # Slower but still in entrainable range.
    # Repp 2005: period correction operates at 60-180bpm.
    pm = _pm_isochronous(C4, 80.0, 14, PIANO, 80)
    save(pm, "peom", "02_piano_iso_80bpm", {
        "description": "Piano C4 isochronous 80bpm, 14 beats, 10.5s",
        "expected": {
            "period_entrainment": "HIGH — within entrainable range",
            "timing_precision": "HIGH — isochronous",
        },
        "science": "Repp 2005: period correction at 60-180bpm range",
    })

    # ── 03: Piano isochronous 160bpm — HIGH entrainment, fast ─────────
    # Fast rate near upper motor limit.
    pm = _pm_isochronous(C4, 160.0, 24, PIANO, 85)
    save(pm, "peom", "03_piano_iso_160bpm", {
        "description": "Piano C4 isochronous 160bpm, 24 beats, 9s",
        "expected": {
            "period_entrainment": "HIGH — fast but entrainable",
            "kinematic_efficiency": "MODERATE — fast rate taxes motor system",
        },
        "science": "Repp 2005: upper limit of comfortable tapping ~200bpm",
    })

    # ── 04: Piano accelerando 100→140bpm — TRACKING entrainment ───────
    # Gradual tempo increase tests adaptive period tracking.
    # Thaut 2015: CTR adjusts to 2-5% tempo changes within 2-3 cycles.
    pm = _pm_tempo_shift(C4, 100.0, 140.0, 20, PIANO, 80)
    save(pm, "peom", "04_piano_accel_100_140", {
        "description": "Piano C4 gradual accelerando 100→140bpm, 20 beats",
        "expected": {
            "period_entrainment": "TRACKING — adapts to tempo change",
            "kinematic_efficiency": "HIGH — smooth acceleration",
            "next_beat_pred": "ADAPTING — predictions adjust",
        },
        "science": "Thaut 2015: CTR tracks 2-5% tempo shifts within 2-3 cycles",
    })

    # ── 05: Piano ritardando 140→100bpm — smooth deceleration ─────────
    pm = _pm_tempo_shift(C4, 140.0, 100.0, 20, PIANO, 80)
    save(pm, "peom", "05_piano_rit_140_100", {
        "description": "Piano C4 gradual ritardando 140→100bpm, 20 beats",
        "expected": {
            "period_entrainment": "TRACKING — adapts to deceleration",
            "kinematic_efficiency": "HIGH — smooth deceleration",
        },
        "science": "Repp 2005: deceleration equally trackable as acceleration",
    })

    # ── 06: Piano sudden tempo shift 120→80bpm — lock BREAKS ──────────
    # Abrupt change tests phase-lock disruption and recovery.
    # Fujioka 2012: beta oscillations reset after tempo perturbation.
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # Phase 1: 8 beats at 120bpm
    ioi_1 = 60.0 / 120.0
    for i in range(8):
        t = i * ioi_1
        inst.notes.append(Note(velocity=80, pitch=C4,
                               start=t, end=t + ioi_1 * 0.85))
    # Phase 2: 8 beats at 80bpm (sudden change)
    t_offset = 8 * ioi_1
    ioi_2 = 60.0 / 80.0
    for i in range(8):
        t = t_offset + i * ioi_2
        inst.notes.append(Note(velocity=80, pitch=C4,
                               start=t, end=t + ioi_2 * 0.85))
    pm.instruments.append(inst)
    save(pm, "peom", "06_piano_sudden_tempo_shift", {
        "description": "Piano C4 sudden 120→80bpm at beat 9, 10s total",
        "expected": {
            "period_lock_strength": "HIGH→LOW→HIGH — lock breaks at shift, re-entrains",
            "period_entrainment": "DISRUPTED then RECOVERING",
            "next_beat_pred": "ERROR at shift, then re-calibrates",
        },
        "science": "Fujioka 2012: beta reset after tempo perturbation (MEG N=12)",
    })

    # ── 07: Piano light syncopation — MODERATE lock disruption ─────────
    # Offbeat accents on beat 2.5 and 4.5, main beats still present.
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    ioi = 60.0 / 120.0
    for bar in range(4):
        bar_t = bar * 4 * ioi
        # Main beats 1, 2, 3, 4
        for beat in range(4):
            t = bar_t + beat * ioi
            inst.notes.append(Note(velocity=70, pitch=C4,
                                   start=t, end=t + ioi * 0.4))
        # Syncopated accents on 2.5 and 4.5 (louder)
        for off in [1.5, 3.5]:
            t = bar_t + off * ioi
            inst.notes.append(Note(velocity=100, pitch=E4,
                                   start=t, end=t + ioi * 0.3))
    pm.instruments.append(inst)
    save(pm, "peom", "07_piano_light_syncopation", {
        "description": "Piano C4 120bpm with offbeat E4 accents, 8s",
        "expected": {
            "period_lock_strength": "MODERATE — syncopation disrupts but beat present",
            "period_entrainment": "MODERATE — competing periodicities",
        },
        "science": "Nozaradan 2011: syncopation modulates neural entrainment (EEG N=11)",
    })

    # ── 08: Piano heavy syncopation — LOW lock ────────────────────────
    # Only offbeats, no downbeats — maximum disruption.
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    ioi = 60.0 / 120.0
    for bar in range(4):
        bar_t = bar * 4 * ioi
        # Only offbeats: 0.5, 1.5, 2.5, 3.5
        for off in [0.5, 1.5, 2.5, 3.5]:
            t = bar_t + off * ioi
            inst.notes.append(Note(velocity=95, pitch=C4,
                                   start=t, end=t + ioi * 0.35))
    pm.instruments.append(inst)
    save(pm, "peom", "08_piano_heavy_syncopation", {
        "description": "Piano C4 120bpm offbeats only, 8s",
        "expected": {
            "period_lock_strength": "LOW — no downbeat support",
            "period_entrainment": "LOW — shifted from expected phase",
        },
        "science": "Nozaradan 2011: removed downbeats collapse entrainment",
    })

    # ── 09: Strings+Piano isochronous unison — HIGH coupling ──────────
    # Multi-timbre reinforcement strengthens entrainment.
    pm = _pm_ensemble_isochronous(
        [([C4, E4, G4], STRINGS, 70), (C4, PIANO, 80)],
        120.0, 16)
    save(pm, "peom", "09_ensemble_iso_120bpm", {
        "description": "Strings chord + Piano C4 isochronous unison 120bpm, 8s",
        "expected": {
            "period_entrainment": "HIGH — multi-timbre reinforcement",
            "kinematic_efficiency": "HIGH — rich harmonic + rhythmic",
            "period_lock_strength": "HIGH — redundant onset cues",
        },
        "science": "Grahn & Brett 2007: richer timbres enhance beat processing",
    })

    # ── 10: Piano+Cello isochronous octaves — HIGH efficiency ─────────
    pm = _pm_ensemble_isochronous(
        [(C4, PIANO, 80), (C3, CELLO, 75)],
        120.0, 16)
    save(pm, "peom", "10_piano_cello_octaves_120", {
        "description": "Piano C4 + Cello C3 octave isochronous 120bpm, 8s",
        "expected": {
            "kinematic_efficiency": "HIGH — warm timbre + rhythmic",
            "period_entrainment": "HIGH — doubled onset energy",
        },
        "science": "Thaut 2015: acoustic complexity enhances motor coupling",
    })

    # ── 11: Piano rubato phrase — LOW timing_precision ─────────────────
    # Expressive timing: irregular IOIs imitating rubato playing.
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # Rubato IOIs: alternating long-short-medium with drift
    iois = [0.55, 0.35, 0.50, 0.65, 0.30, 0.45, 0.70, 0.40,
            0.60, 0.35, 0.55, 0.45, 0.65, 0.30, 0.50, 0.55]
    scale = diatonic_scale(C4, 8)
    t = 0.0
    for i, ioi_val in enumerate(iois):
        p = scale[i % len(scale)]
        inst.notes.append(Note(velocity=75, pitch=p,
                               start=t, end=t + ioi_val * 0.85))
        t += ioi_val
    pm.instruments.append(inst)
    save(pm, "peom", "11_piano_rubato_phrase", {
        "description": "Piano C major rubato melody, irregular IOIs, ~8s",
        "expected": {
            "timing_precision": "LOW — high IOI variability",
            "period_entrainment": "LOW — no stable period",
            "period_lock_strength": "LOW — no consistent phase",
        },
        "science": "Repp 2005: expressive timing disrupts period locking",
    })

    # ── 12: Piano random IOI — LOWEST entrainment ─────────────────────
    # Poisson-like random onsets: no detectable periodicity.
    rng = np.random.RandomState(42)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for i in range(20):
        ioi_val = float(rng.uniform(0.15, 0.85))
        p = int(rng.randint(55, 72))
        inst.notes.append(Note(velocity=int(rng.randint(60, 100)),
                               pitch=p, start=t, end=t + 0.12))
        t += ioi_val
    pm.instruments.append(inst)
    save(pm, "peom", "12_piano_random_ioi", {
        "description": "Piano random pitches with random IOIs 150-850ms, ~8s",
        "expected": {
            "period_entrainment": "LOWEST — no detectable periodicity",
            "timing_precision": "LOWEST — maximum CV",
            "period_lock_strength": "LOWEST — no phase to lock",
            "next_beat_pred": "LOWEST — unpredictable",
        },
        "science": "Grahn & Brett 2007: non-metric sequences fail to activate putamen",
    })

    # ── 13: Near-silence control — LOW everything ─────────────────────
    pm = _pm_near_silence(5.0)
    save(pm, "peom", "13_near_silence", {
        "description": "Near-silence, single v=1 tick, 5s",
        "expected": {
            "period_entrainment": "FLOOR — no auditory input",
            "timing_precision": "FLOOR",
            "period_lock_strength": "FLOOR",
        },
        "science": "Control: no auditory stimulus baseline",
    })

    # ── 14: Piano swing feel (2:1 ratio) — MODERATE entrainment ───────
    # Swing eighths: long-short alternation at ~120bpm.
    # Still periodic at the quarter-note level.
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    quarter = 60.0 / 120.0
    long_8th = quarter * 0.67
    short_8th = quarter * 0.33
    t = 0.0
    for bar in range(4):
        for beat in range(4):
            # Long eighth
            inst.notes.append(Note(velocity=80, pitch=C4,
                                   start=t, end=t + long_8th * 0.85))
            t += long_8th
            # Short eighth
            inst.notes.append(Note(velocity=65, pitch=E4,
                                   start=t, end=t + short_8th * 0.85))
            t += short_8th
    pm.instruments.append(inst)
    save(pm, "peom", "14_piano_swing_feel", {
        "description": "Piano swing 8ths (2:1) at 120bpm, C4+E4, 8s",
        "expected": {
            "period_entrainment": "MODERATE — quarter-note period present",
            "timing_precision": "MODERATE — asymmetric but periodic",
            "period_lock_strength": "MODERATE — 8th-note asymmetry",
        },
        "science": "Repp 2005: swing timing still supports period extraction at higher level",
    })

    # ── 15: Piano polyrhythm 3-against-2 — competing predictions ──────
    # Two competing periodicities challenge beat prediction.
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    cycle_dur = 2.0
    for cycle in range(4):
        # Voice 1: triplets on C5
        for i in range(3):
            t = cycle * cycle_dur + i * (cycle_dur / 3)
            inst.notes.append(Note(velocity=85, pitch=C5,
                                   start=t, end=t + 0.3))
        # Voice 2: duplets on C3
        for i in range(2):
            t = cycle * cycle_dur + i * (cycle_dur / 2)
            inst.notes.append(Note(velocity=75, pitch=C3,
                                   start=t, end=t + 0.45))
    pm.instruments.append(inst)
    save(pm, "peom", "15_piano_polyrhythm_3v2", {
        "description": "Piano 3-against-2 polyrhythm, C5+C3, 8s",
        "expected": {
            "next_beat_pred": "COMPLEX — two competing periodicities",
            "period_entrainment": "MODERATE — ambiguous period",
            "period_lock_strength": "LOW — competing phase references",
        },
        "science": "Vuust 2009: polyrhythmic conflict = motor prediction challenge",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 2: HGSIC — Hierarchical Groove State Integration (15 stimuli)
#
# Tests: groove_quality, beat_prominence, meter_structure,
#        auditory_motor_coupling, motor_preparation, groove_trajectory
#
# Key R3: [7]amplitude, [8]loudness, [10]spectral_flux, [11]onset_strength,
#          [22]entropy, [23]flatness, [24]timbre_change
# Key H3: amp/onset@H6(200ms beat), entropy/loudness@H11(450ms measure),
#          roughness/flatness@H16(1s phrase)
# ═══════════════════════════════════════════════════════════════════════

def generate_hgsic_stimuli() -> None:
    """15 stimuli targeting HGSIC encoder and its 6 beliefs."""

    # ── 01: Drums straight 4/4 rock — MODERATE groove ──────────────────
    # Standard rock: kick on 1,3; snare on 2,4; closed HH on every 8th.
    # Regular but not syncopated — moderate groove (inverted-U).
    # Madison 2011: zero syncopation = below inverted-U peak.
    pm = _pm_drum_pattern({
        KICK: [0, 8],
        SNARE: [4, 12],
        CLOSED_HH: [0, 2, 4, 6, 8, 10, 12, 14],
    }, bpm=120.0, n_bars=5)
    save(pm, "hgsic", "01_drums_straight_4_4", {
        "description": "Drums straight 4/4 rock: K(1,3) S(2,4) HH(8ths), 120bpm, 10s",
        "expected": {
            "groove_quality": "MODERATE — regular but low syncopation",
            "beat_prominence": "HIGH — clear kick+snare on beats",
            "meter_structure": "HIGH — clear 4/4 metric grid",
        },
        "science": "Madison 2011: straight beat = below inverted-U peak",
    })

    # ── 02: Drums funk groove (medium syncopation) — HIGH groove ───────
    # Classic funk: kick syncopated, snare on 2,4, open HH on offbeats.
    # Medium syncopation = inverted-U peak for groove.
    # Witek 2014: medium syncopation maximizes groove (N=66).
    pm = _pm_drum_with_velocity({
        KICK: [(0, 110), (3, 80), (6, 70), (10, 90), (13, 75)],
        SNARE: [(4, 110), (12, 110)],
        CLOSED_HH: [(0, 70), (2, 60), (4, 70), (6, 60), (8, 70),
                     (10, 60), (12, 70), (14, 60)],
        OPEN_HH: [(3, 50), (11, 50)],
    }, bpm=100.0, n_bars=5)
    save(pm, "hgsic", "02_drums_funk_groove", {
        "description": "Drums funk groove: syncopated kick, 100bpm, 10s",
        "expected": {
            "groove_quality": "HIGH — medium syncopation = inverted-U peak",
            "beat_prominence": "HIGH — snare on 2,4 anchors beat",
            "auditory_motor_coupling": "HIGH — groove drives coupling",
            "motor_preparation": "HIGH — strong desire-to-move",
        },
        "science": "Witek 2014: medium syncopation maximizes groove (N=66)",
    })

    # ── 03: Drums heavy syncopation — MODERATE groove (past peak) ──────
    # Displaced kick, ghost notes everywhere, weak downbeats.
    # Heavy syncopation goes past inverted-U peak.
    pm = _pm_drum_with_velocity({
        KICK: [(1, 90), (5, 70), (9, 80), (14, 85)],
        SNARE: [(4, 100), (7, 50), (11, 50), (12, 100), (15, 45)],
        CLOSED_HH: [(0, 50), (2, 40), (4, 50), (6, 40), (8, 50),
                     (10, 40), (12, 50), (14, 40)],
        RIMSHOT: [(3, 60), (13, 55)],
    }, bpm=100.0, n_bars=5)
    save(pm, "hgsic", "03_drums_heavy_syncopation", {
        "description": "Drums heavy syncopation: displaced kicks, ghost snares, 100bpm, 10s",
        "expected": {
            "groove_quality": "MODERATE — past inverted-U peak",
            "beat_prominence": "LOW — weak downbeats",
            "meter_structure": "LOW — ambiguous metric grid",
        },
        "science": "Madison 2011: heavy syncopation reduces groove (past peak)",
    })

    # ── 04: Piano isochronous (zero syncopation) — LOW groove ──────────
    # No syncopation, no timbral variety: below inverted-U.
    pm = _pm_isochronous(C4, 120.0, 16, PIANO, 75)
    save(pm, "hgsic", "04_piano_iso_zero_sync", {
        "description": "Piano C4 isochronous 120bpm, zero syncopation, 8s",
        "expected": {
            "groove_quality": "LOW — zero syncopation = below inverted-U",
            "beat_prominence": "MODERATE — regular onsets but no hierarchy",
        },
        "science": "Madison 2011: zero syncopation = minimum groove",
    })

    # ── 05: Drums+Bass funk — HIGH motor coupling ─────────────────────
    # Full rhythm section reinforces groove through multi-instrument coupling.
    pm = _pm_drum_with_velocity({
        KICK: [(0, 110), (3, 80), (6, 70), (10, 90)],
        SNARE: [(4, 110), (12, 110)],
        CLOSED_HH: [(0, 70), (2, 60), (4, 70), (6, 60),
                     (8, 70), (10, 60), (12, 70), (14, 60)],
    }, bpm=100.0, n_bars=5)
    # Add funk bass line
    bass = pretty_midi.Instrument(program=33)  # Fingered Bass
    bar_dur = 4 * (60.0 / 100.0)
    for bar in range(5):
        bt = bar * bar_dur
        step = 60.0 / 100.0 / 4  # 16th note
        bass_hits = [(0, C2, 100), (3, C2, 70), (6, Eb3, 80),
                     (8, G2, 90), (10, C2, 60), (13, Bb2, 75)]
        for s, p, v in bass_hits:
            t = bt + s * step
            bass.notes.append(Note(velocity=v, pitch=p,
                                   start=t, end=t + step * 1.5))
    pm.instruments.append(bass)
    save(pm, "hgsic", "05_drums_bass_funk", {
        "description": "Drums+Bass funk groove, 100bpm, 10s",
        "expected": {
            "auditory_motor_coupling": "HIGH — multi-instrument reinforcement",
            "groove_quality": "HIGH — full rhythm section groove",
            "motor_preparation": "HIGH — bass+drums drive movement",
        },
        "science": "Janata 2012: motor cortex activation scales with groove richness",
    })

    # ── 06: Drums jazz shuffle — HIGH groove ───────────────────────────
    # Swing feel with ride cymbal: classic jazz groove.
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    triplet_8th = (60.0 / 140.0) * 2 / 3
    quarter = 60.0 / 140.0
    for bar in range(6):
        bt = bar * 4 * quarter
        for beat in range(4):
            beat_t = bt + beat * quarter
            # Ride: swing pattern (1 and 3 of triplet)
            drums.notes.append(Note(velocity=80, pitch=RIDE,
                                    start=beat_t, end=beat_t + 0.05))
            drums.notes.append(Note(velocity=60, pitch=RIDE,
                                    start=beat_t + 2 * triplet_8th,
                                    end=beat_t + 2 * triplet_8th + 0.05))
        # Snare: beats 2 and 4
        drums.notes.append(Note(velocity=90, pitch=SNARE,
                                start=bt + quarter, end=bt + quarter + 0.05))
        drums.notes.append(Note(velocity=90, pitch=SNARE,
                                start=bt + 3 * quarter, end=bt + 3 * quarter + 0.05))
        # Kick: beats 1 and 3
        drums.notes.append(Note(velocity=85, pitch=KICK,
                                start=bt, end=bt + 0.05))
        drums.notes.append(Note(velocity=75, pitch=KICK,
                                start=bt + 2 * quarter, end=bt + 2 * quarter + 0.05))
    pm.instruments.append(drums)
    save(pm, "hgsic", "06_drums_jazz_shuffle", {
        "description": "Jazz shuffle: ride swing + snare 2,4 + kick 1,3, 140bpm, 10s",
        "expected": {
            "groove_quality": "HIGH — swing = strong groove sensation",
            "meter_structure": "HIGH — clear 4/4 with swing subdivision",
        },
        "science": "Witek 2014: moderate swing syncopation = high groove",
    })

    # ── 07: Drums+Bass reggae offbeat — HIGH groove, offbeat emphasis ──
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    quarter = 60.0 / 80.0
    for bar in range(5):
        bt = bar * 4 * quarter
        # Kick on 1, 3; Rimshot on offbeats (reggae skank)
        drums.notes.append(Note(velocity=100, pitch=KICK,
                                start=bt, end=bt + 0.08))
        drums.notes.append(Note(velocity=80, pitch=KICK,
                                start=bt + 2 * quarter, end=bt + 2 * quarter + 0.08))
        for beat in range(4):
            # Offbeat hi-hat
            t = bt + beat * quarter + quarter * 0.5
            drums.notes.append(Note(velocity=85, pitch=CLOSED_HH,
                                    start=t, end=t + 0.05))
    pm.instruments.append(drums)
    # Reggae bass: root on 1, octave up on 3
    bass = pretty_midi.Instrument(program=33)
    for bar in range(5):
        bt = bar * 4 * quarter
        bass.notes.append(Note(velocity=90, pitch=C2,
                               start=bt, end=bt + quarter * 0.9))
        bass.notes.append(Note(velocity=80, pitch=C3,
                               start=bt + 2 * quarter,
                               end=bt + 2 * quarter + quarter * 0.9))
    pm.instruments.append(bass)
    save(pm, "hgsic", "07_drums_bass_reggae", {
        "description": "Drums+Bass reggae: offbeat HH, kick 1,3, 80bpm, 10s",
        "expected": {
            "groove_quality": "HIGH — offbeat groove pattern",
            "meter_structure": "HIGH — clear 4/4 with offbeat emphasis",
            "beat_prominence": "HIGH — kick anchors downbeats",
        },
        "science": "Witek 2014: offbeat patterns produce strong groove sensation",
    })

    # ── 08: Piano+Strings waltz 3/4 — different meter ─────────────────
    pm = pretty_midi.PrettyMIDI()
    pno = pretty_midi.Instrument(program=PIANO)
    str_inst = pretty_midi.Instrument(program=STRINGS)
    quarter = 60.0 / 120.0
    for bar in range(8):
        bt = bar * 3 * quarter
        # Piano: bass on 1, chord on 2,3
        pno.notes.append(Note(velocity=85, pitch=C3,
                              start=bt, end=bt + quarter * 0.9))
        for beat in [1, 2]:
            t = bt + beat * quarter
            for p in [E4, G4]:
                pno.notes.append(Note(velocity=65, pitch=p,
                                      start=t, end=t + quarter * 0.8))
        # Strings: sustained harmony
        for p in [C4, E4, G4]:
            str_inst.notes.append(Note(velocity=55, pitch=p,
                                       start=bt, end=bt + 3 * quarter - 0.02))
    pm.instruments.extend([pno, str_inst])
    save(pm, "hgsic", "08_waltz_3_4", {
        "description": "Piano+Strings waltz 3/4, C major, 120bpm, 12s",
        "expected": {
            "meter_structure": "CLEAR 3/4 — oom-pah-pah pattern",
            "groove_quality": "MODERATE — triple meter less groove than 4/4",
            "beat_prominence": "HIGH — strong downbeat + chord pattern",
        },
        "science": "Grahn & Brett 2007: metrical structure activates putamen/SMA",
    })

    # ── 09: Drums 7/8 complex meter — irregular grouping ──────────────
    # 7/8 = 2+2+3 or 3+2+2: asymmetric meter.
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    eighth = 60.0 / 140.0 / 2
    bar_dur = 7 * eighth
    for bar in range(7):
        bt = bar * bar_dur
        # Grouping: 2+2+3 (accents on 1, 3, 5)
        accents = [0, 2, 4]
        for a in accents:
            t = bt + a * eighth
            drums.notes.append(Note(velocity=110, pitch=KICK,
                                    start=t, end=t + 0.05))
        # Hi-hat on every 8th
        for i in range(7):
            t = bt + i * eighth
            drums.notes.append(Note(velocity=70, pitch=CLOSED_HH,
                                    start=t, end=t + 0.03))
        # Snare on beat 3 (eighth 4)
        drums.notes.append(Note(velocity=100, pitch=SNARE,
                                start=bt + 4 * eighth, end=bt + 4 * eighth + 0.05))
    pm.instruments.append(drums)
    save(pm, "hgsic", "09_drums_7_8_complex", {
        "description": "Drums 7/8 (2+2+3), 140bpm, 7 bars, ~10s",
        "expected": {
            "meter_structure": "LOW — irregular grouping, hard to entrain",
            "groove_quality": "LOW — asymmetric meter disrupts groove",
            "beat_prominence": "MODERATE — accents present but irregular",
        },
        "science": "Grahn & Brett 2007: irregular meters weaker putamen activation",
    })

    # ── 10: Full ensemble funk — MAXIMUM motor preparation ─────────────
    # Drums + bass + piano comping + flute melody.
    pm = _pm_drum_with_velocity({
        KICK: [(0, 110), (3, 80), (6, 70), (10, 90)],
        SNARE: [(4, 110), (12, 110)],
        CLOSED_HH: [(0, 70), (2, 60), (4, 70), (6, 60),
                     (8, 70), (10, 60), (12, 70), (14, 60)],
    }, bpm=100.0, n_bars=6)
    bar_dur = 4 * (60.0 / 100.0)
    step = 60.0 / 100.0 / 4
    # Bass
    bass = pretty_midi.Instrument(program=33)
    for bar in range(6):
        bt = bar * bar_dur
        for s, p, v in [(0, C2, 100), (6, Eb3, 80), (8, G2, 90), (13, Bb2, 70)]:
            t = bt + s * step
            bass.notes.append(Note(velocity=v, pitch=p, start=t, end=t + step * 1.5))
    pm.instruments.append(bass)
    # Piano comping
    pno = pretty_midi.Instrument(program=PIANO)
    quarter = 60.0 / 100.0
    for bar in range(6):
        bt = bar * bar_dur
        for beat in [0.5, 1.5, 2.5, 3.5]:
            t = bt + beat * quarter
            for p in [Eb4, G4, Bb4]:
                pno.notes.append(Note(velocity=55, pitch=p,
                                      start=t, end=t + quarter * 0.4))
    pm.instruments.append(pno)
    # Flute melody
    fl = pretty_midi.Instrument(program=FLUTE)
    mel_notes = [G5, Bb5, C6, Bb5, G5, Eb5, G5, Bb5] * 3
    mel_durs = [quarter] * 24
    t = 0.0
    for p, d in zip(mel_notes, mel_durs):
        fl.notes.append(Note(velocity=85, pitch=p, start=t, end=t + d * 0.9))
        t += d
    pm.instruments.append(fl)
    save(pm, "hgsic", "10_full_ensemble_funk", {
        "description": "Full funk: drums+bass+piano+flute, Eb major, 100bpm, 12s",
        "expected": {
            "motor_preparation": "HIGH — maximum motor drive from full ensemble",
            "groove_quality": "HIGH — multi-layer groove reinforcement",
            "auditory_motor_coupling": "HIGH — 4-instrument synchrony",
            "beat_prominence": "HIGH — redundant beat markers",
        },
        "science": "Janata 2012: motor cortex PMC activation scales with ensemble complexity",
    })

    # ── 11: Solo hi-hat pattern — LOW beat prominence ──────────────────
    # Hi-hat only: weak transients, no kick/snare contrast.
    pm = _pm_drum_pattern({
        CLOSED_HH: [0, 2, 4, 6, 8, 10, 12, 14],
    }, bpm=120.0, n_bars=4, velocity_map={CLOSED_HH: 60})
    save(pm, "hgsic", "11_solo_hihat", {
        "description": "Solo closed hi-hat 8ths, 120bpm, 4 bars, 8s",
        "expected": {
            "beat_prominence": "LOW — no kick/snare accent hierarchy",
            "groove_quality": "LOW — no dynamic contrast",
            "meter_structure": "LOW — flat dynamic = ambiguous meter",
        },
        "science": "Grahn & Brett 2007: metric clarity requires accent hierarchy",
    })

    # ── 12: Drums crescendo groove buildup — RISING trajectory ─────────
    # Groove intensifies as velocity increases.
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    step = 60.0 / 110.0 / 4
    total_bars = 5
    for bar in range(total_bars):
        bt = bar * 16 * step
        v_scale = 0.4 + 0.6 * (bar / max(total_bars - 1, 1))
        pattern = {
            KICK: [(0, int(110 * v_scale)), (6, int(80 * v_scale)),
                   (10, int(90 * v_scale))],
            SNARE: [(4, int(110 * v_scale)), (12, int(110 * v_scale))],
            CLOSED_HH: [(i, int(70 * v_scale)) for i in range(0, 16, 2)],
        }
        for drum_note, hits in pattern.items():
            for s, v in hits:
                t = bt + s * step
                drums.notes.append(Note(velocity=v, pitch=drum_note,
                                        start=t, end=t + step * 0.5))
    pm.instruments.append(drums)
    save(pm, "hgsic", "12_drums_crescendo_groove", {
        "description": "Drums groove with crescendo pp→f, 110bpm, 5 bars, 10s",
        "expected": {
            "groove_trajectory": "RISING — groove intensity increases",
            "beat_prominence": "RISING — crescendo increases salience",
            "motor_preparation": "RISING — increasing motor drive",
        },
        "science": "Janata 2012: groove intensity scales with dynamic level",
    })

    # ── 13: Drums decrescendo groove fade — FALLING trajectory ─────────
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    step = 60.0 / 110.0 / 4
    total_bars = 5
    for bar in range(total_bars):
        bt = bar * 16 * step
        v_scale = 1.0 - 0.7 * (bar / max(total_bars - 1, 1))
        pattern = {
            KICK: [(0, int(110 * v_scale)), (6, int(80 * v_scale)),
                   (10, int(90 * v_scale))],
            SNARE: [(4, int(110 * v_scale)), (12, int(110 * v_scale))],
            CLOSED_HH: [(i, int(70 * v_scale)) for i in range(0, 16, 2)],
        }
        for drum_note, hits in pattern.items():
            for s, v in hits:
                t = bt + s * step
                drums.notes.append(Note(velocity=max(v, 10), pitch=drum_note,
                                        start=t, end=t + step * 0.5))
    pm.instruments.append(drums)
    save(pm, "hgsic", "13_drums_decrescendo_groove", {
        "description": "Drums groove with decrescendo f→pp, 110bpm, 5 bars, 10s",
        "expected": {
            "groove_trajectory": "FALLING — groove dissolves",
            "beat_prominence": "FALLING — decreasing salience",
        },
        "science": "Inverse of crescendo: groove intensity decreases with dynamic level",
    })

    # ── 14: Drums random velocities — LOW groove ──────────────────────
    rng = np.random.RandomState(99)
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    step = 60.0 / 120.0 / 4
    for bar in range(4):
        bt = bar * 16 * step
        for i in range(16):
            t = bt + i * step
            drum_note = [KICK, SNARE, CLOSED_HH][int(rng.randint(0, 3))]
            v = int(rng.randint(30, 127))
            drums.notes.append(Note(velocity=v, pitch=drum_note,
                                    start=t, end=t + step * 0.4))
    pm.instruments.append(drums)
    save(pm, "hgsic", "14_drums_random_velocity", {
        "description": "Drums random instrument+velocity on 16ths, 120bpm, 8s",
        "expected": {
            "groove_quality": "LOW — no systematic dynamic pattern",
            "beat_prominence": "LOW — no accent hierarchy",
            "meter_structure": "LOW — random accents destroy meter",
        },
        "science": "Madison 2011: random dynamics eliminate groove sensation",
    })

    # ── 15: Drums+Bass marching — LOW groove (too rigid) ───────────────
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    quarter = 60.0 / 120.0
    for bar in range(4):
        bt = bar * 4 * quarter
        for beat in range(4):
            t = bt + beat * quarter
            drums.notes.append(Note(velocity=100, pitch=SNARE,
                                    start=t, end=t + 0.05))
            drums.notes.append(Note(velocity=100, pitch=KICK,
                                    start=t, end=t + 0.05))
    pm.instruments.append(drums)
    bass = pretty_midi.Instrument(program=33)
    for bar in range(4):
        bt = bar * 4 * quarter
        for beat in range(4):
            t = bt + beat * quarter
            bass.notes.append(Note(velocity=100, pitch=C2,
                                   start=t, end=t + quarter * 0.9))
    pm.instruments.append(bass)
    save(pm, "hgsic", "15_drums_bass_march", {
        "description": "Drums+Bass strict march: all beats equal, 120bpm, 8s",
        "expected": {
            "groove_quality": "LOW — zero syncopation, mechanical",
            "meter_structure": "HIGH — perfectly regular but flat",
            "beat_prominence": "HIGH — every beat equally strong",
        },
        "science": "Madison 2011: zero syncopation + flat dynamics = min groove",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 3: HMCE — Hierarchical Musical Context Encoding (15 stimuli)
#
# Tests: context_depth, short_context, medium_context, long_context,
#        phrase_boundary_pred, structure_pred
#
# Key R3: [17]spectral_autocorr, [21]spectral_change, [51]x_l5l7,
#          [60]x_l0l2l5
# Key H3: spectral_auto/onset@H3(100ms), hier_mean@H8/H16
# ═══════════════════════════════════════════════════════════════════════

def generate_hmce_stimuli() -> None:
    """15 stimuli targeting HMCE relay and its 6 beliefs."""

    # ── 01: Piano 2-bar ostinato ×4 — HIGH short_context ───────────────
    # Repetitive 2-bar pattern: strong local structure.
    # Tillmann 2003: repetition establishes implicit structure.
    quarter = 60.0 / 120.0
    pattern = [C4, E4, G4, E4, F4, A4, G4, E4]
    durs = [quarter] * 8
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for rep in range(4):
        for p, d in zip(pattern, durs):
            inst.notes.append(Note(velocity=75, pitch=p,
                                   start=t, end=t + d - 0.02))
            t += d
    pm.instruments.append(inst)
    save(pm, "hmce", "01_piano_2bar_ostinato", {
        "description": "Piano 2-bar C major ostinato ×4, 120bpm, 8s",
        "expected": {
            "short_context": "HIGH — local repetition clear after 1st cycle",
            "structure_pred": "HIGH — pattern becomes predictable",
            "context_depth": "MODERATE — limited to 2-bar scale",
        },
        "science": "Tillmann 2003: repetition establishes implicit structure (fMRI N=20)",
    })

    # ── 02: Piano 8-bar phrase with PAC — HIGH medium_context ──────────
    # Complete 8-bar period with tonic-dominant-tonic arc.
    # Koelsch 2009: phrase-level processing at theta timescale.
    quarter = 60.0 / 100.0
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # 8-bar chord progression: I-vi-IV-V | I-vi-ii-V-I
    chords = [C_MAJ, A_MIN, F_MAJ, G_MAJ,
              C_MAJ, A_MIN, D_MIN, G_DOM7]
    dur_per_chord = 4 * quarter
    t = 0.0
    for ch in chords:
        for p in ch:
            inst.notes.append(Note(velocity=70, pitch=p,
                                   start=t, end=t + dur_per_chord - 0.02))
        t += dur_per_chord
    # Final resolution
    for p in C_MAJ_WIDE:
        inst.notes.append(Note(velocity=80, pitch=p,
                               start=t, end=t + dur_per_chord - 0.02))
    pm.instruments.append(inst)
    save(pm, "hmce", "02_piano_8bar_phrase", {
        "description": "Piano 8-bar phrase I-vi-IV-V-I-vi-ii-V-I, 100bpm, 21.6s",
        "expected": {
            "medium_context": "HIGH — phrase-level harmonic arc complete",
            "context_depth": "HIGH — 8-bar structure clear",
            "phrase_boundary_pred": "HIGH at cadence (bar 8→9 transition)",
        },
        "science": "Koelsch 2009: phrase boundary = CPS ERP component",
    })

    # ── 03: Piano 16-bar AABB — HIGH long_context ─────────────────────
    quarter = 60.0 / 120.0
    bar_dur = 4 * quarter
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # Section A (4 bars): I-IV-V-I
    section_a = [C_MAJ, F_MAJ, G_MAJ, C_MAJ]
    # Section B (4 bars): vi-ii-V-I
    section_b = [A_MIN, D_MIN, G_DOM7, C_MAJ]
    t = 0.0
    for section in [section_a, section_a, section_b, section_b]:
        for ch in section:
            for p in ch:
                inst.notes.append(Note(velocity=72, pitch=p,
                                       start=t, end=t + bar_dur - 0.02))
            t += bar_dur
    pm.instruments.append(inst)
    save(pm, "hmce", "03_piano_16bar_aabb", {
        "description": "Piano 16-bar AABB form (C major), 120bpm, 32s",
        "expected": {
            "long_context": "HIGH — 16-bar form = long-range organization",
            "context_depth": "HIGH — multi-level hierarchy (bar, phrase, section)",
            "structure_pred": "HIGH — repetition enables prediction",
            "phrase_boundary_pred": "HIGH at section transitions (bars 4,8,12)",
        },
        "science": "Pearce 2018: IDyOM information content drops with structural regularity",
    })

    # ── 04: Piano 32-bar AABA — HIGHEST context_depth ──────────────────
    quarter = 60.0 / 130.0
    bar_dur = 4 * quarter
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # A section (8 bars): C major standard
    a_chords = [C_MAJ, A_MIN, F_MAJ, G_MAJ, C_MAJ, D_MIN, G_DOM7, C_MAJ]
    # B section (8 bars): modulation to G major
    b_chords = [[G3, B3, D4], [E4, G4, B4], [C4, E4, G4], [D4, Gb4, A4],
                [G3, B3, D4], [A3, C4, E4], [D4, Gb4, A4], [G3, B3, D4]]
    t = 0.0
    for section_chords in [a_chords, a_chords, b_chords, a_chords]:
        for ch in section_chords:
            for p in ch:
                inst.notes.append(Note(velocity=70, pitch=p,
                                       start=t, end=t + bar_dur - 0.02))
            t += bar_dur
    pm.instruments.append(inst)
    save(pm, "hmce", "04_piano_32bar_aaba", {
        "description": "Piano 32-bar AABA form (C→G→C), 130bpm, 29.5s",
        "expected": {
            "context_depth": "HIGHEST — full formal organization AABA",
            "long_context": "HIGH — 30s duration, key change in B",
            "medium_context": "HIGH — 8-bar phrases clear",
            "structure_pred": "HIGH — return of A after B = strong prediction",
            "phrase_boundary_pred": "HIGH at A→A, A→B, B→A transitions",
        },
        "science": "Pearce 2018: AABA = standard song form, high predictability at return",
    })

    # ── 05: Piano key change C→G at bar 8 — boundary detection ────────
    quarter = 60.0 / 110.0
    bar_dur = 4 * quarter
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # Bars 1-8: C major
    c_prog = [C_MAJ, F_MAJ, G_MAJ, C_MAJ, A_MIN, D_MIN, G_DOM7, C_MAJ]
    # Bars 9-16: G major
    g_prog = [[G3, B3, D4], [C4, E4, G4], [D4, Gb4, A4], [G3, B3, D4],
              [E4, G4, B4], [A3, C4, E4], [D4, Gb4, A4], [G3, B3, D4]]
    t = 0.0
    for ch in c_prog + g_prog:
        for p in ch:
            inst.notes.append(Note(velocity=72, pitch=p,
                                   start=t, end=t + bar_dur - 0.02))
        t += bar_dur
    pm.instruments.append(inst)
    save(pm, "hmce", "05_piano_key_change_c_to_g", {
        "description": "Piano C major (8 bars) → G major (8 bars), 110bpm, 17.5s",
        "expected": {
            "phrase_boundary_pred": "HIGH at bar 8-9 — key change boundary",
            "context_depth": "RISING — two key areas accumulate context",
            "medium_context": "HIGH — phrase-level structure in each key",
        },
        "science": "Koelsch 2009: key changes generate CPS (Closure Positive Shift)",
    })

    # ── 06: Piano continuous chromatic melody — LOW boundary ───────────
    # Wandering chromatic line: no clear phrase boundaries.
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    quarter = 60.0 / 100.0
    rng = np.random.RandomState(55)
    t, pitch = 0.0, 60
    for i in range(20):
        dur = quarter * float(rng.choice([1, 1, 2]))
        inst.notes.append(Note(velocity=70, pitch=pitch,
                               start=t, end=t + dur - 0.02))
        t += dur
        pitch = max(48, min(84, pitch + int(rng.choice([-2, -1, 1, 2]))))
    pm.instruments.append(inst)
    save(pm, "hmce", "06_piano_chromatic_wandering", {
        "description": "Piano chromatic wandering melody, no phrases, ~10s",
        "expected": {
            "phrase_boundary_pred": "LOW — no clear boundaries",
            "structure_pred": "LOW — unpredictable continuation",
            "context_depth": "LOW — no tonal center established",
        },
        "science": "Pearce 2018: chromatic sequences have high information content",
    })

    # ── 07: Piano phrase with silence gap — HIGH boundary detection ────
    quarter = 60.0 / 120.0
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    phrase = [C4, D4, E4, F4, G4, F4, E4, D4]
    t = 0.0
    for rep in range(2):
        for p in phrase:
            inst.notes.append(Note(velocity=75, pitch=p,
                                   start=t, end=t + quarter - 0.02))
            t += quarter
        t += 1.0  # 1-second silence gap
    pm.instruments.append(inst)
    save(pm, "hmce", "07_piano_phrase_with_gap", {
        "description": "Piano 8-note phrase × 2 with 1s silence gap, 120bpm",
        "expected": {
            "phrase_boundary_pred": "HIGH — silence = unambiguous boundary",
            "short_context": "HIGH — repetition within phrase",
            "structure_pred": "HIGH — same phrase repeats after gap",
        },
        "science": "Koelsch 2009: silence gaps are strongest phrase boundary cues",
    })

    # ── 08: Piano sequence (transposed repetition) — HIGH structure ────
    # 4-note motif transposed up stepwise.
    quarter = 60.0 / 120.0
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    motif = [0, 2, 4, 2]  # intervals from root: root, 2nd, 3rd, 2nd
    roots = [C4, D4, E4, F4, G4, A4, B4, C5]
    t = 0.0
    for root in roots:
        for interval in motif:
            p = root + interval
            inst.notes.append(Note(velocity=75, pitch=p,
                                   start=t, end=t + quarter - 0.02))
            t += quarter
    pm.instruments.append(inst)
    save(pm, "hmce", "08_piano_sequence_ascending", {
        "description": "Piano ascending sequence: 4-note motif transposed ×8, 120bpm, 16s",
        "expected": {
            "structure_pred": "HIGH — sequential pattern = high predictability",
            "medium_context": "HIGH — phrase-level repetition",
            "context_depth": "RISING — accumulating structural model",
        },
        "science": "Pearce 2018: sequences reduce information content progressively",
    })

    # ── 09: Piano ABA form — return recognition ───────────────────────
    quarter = 60.0 / 120.0
    bar_dur = 4 * quarter
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # Section A: C major melody
    a_notes = [C4, E4, G4, E4, F4, E4, D4, C4]
    # Section B: A minor melody
    b_notes = [A3, C4, E4, C4, D4, C4, B3, A3]
    t = 0.0
    for section in [a_notes, a_notes, b_notes, b_notes, a_notes, a_notes]:
        for p in section:
            inst.notes.append(Note(velocity=75, pitch=p,
                                   start=t, end=t + quarter - 0.02))
            t += quarter
    pm.instruments.append(inst)
    save(pm, "hmce", "09_piano_aba_form", {
        "description": "Piano ABA form: A=C major, B=A minor, 120bpm, 24s",
        "expected": {
            "structure_pred": "HIGH — return of A after B = confirmed prediction",
            "long_context": "HIGH — ABA recognized as form",
            "phrase_boundary_pred": "HIGH at A→B and B→A transitions",
        },
        "science": "Koelsch 2009: ABA return generates recognition + CPS",
    })

    # ── 10: Piano through-composed (no repetition) — LOW structure ────
    quarter = 60.0 / 110.0
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    rng = np.random.RandomState(77)
    scale = [C4, D4, E4, F4, G4, A4, B4, C5]
    t = 0.0
    for i in range(24):
        p = scale[int(rng.randint(0, len(scale)))]
        d = quarter * float(rng.choice([1, 1, 2, 0.5]))
        v = int(rng.randint(55, 90))
        inst.notes.append(Note(velocity=v, pitch=p,
                               start=t, end=t + d - 0.02))
        t += d
    pm.instruments.append(inst)
    save(pm, "hmce", "10_piano_through_composed", {
        "description": "Piano random diatonic melody, no repetition, ~12s",
        "expected": {
            "structure_pred": "LOW — no repeated patterns to learn",
            "context_depth": "LOW — no hierarchical organization",
        },
        "science": "Pearce 2018: novel sequences = high information content throughout",
    })

    # ── 11: Piano atonal random pitch — LOWEST context ─────────────────
    pm = _pm_dense_random(8.0, seed=88, notes_per_sec=4)
    save(pm, "hmce", "11_piano_atonal_random", {
        "description": "Piano random pitches, 4 notes/sec, 8s",
        "expected": {
            "context_depth": "LOWEST — no tonal/structural organization",
            "short_context": "LOW — no local repetition",
            "medium_context": "LOW — no phrase structure",
            "long_context": "LOW — no formal organization",
        },
        "science": "Tillmann 2003: atonal sequences fail to build implicit models",
    })

    # ── 12: Strings I-IV-V-I repeated — HIGH harmonic pattern ─────────
    quarter = 60.0 / 100.0
    bar_dur = 4 * quarter
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=STRINGS)
    prog = [C_MAJ, F_MAJ, G_MAJ, C_MAJ]
    t = 0.0
    for rep in range(3):
        for ch in prog:
            for p in ch:
                inst.notes.append(Note(velocity=70, pitch=p,
                                       start=t, end=t + bar_dur - 0.02))
            t += bar_dur
    pm.instruments.append(inst)
    save(pm, "hmce", "12_strings_I_IV_V_I_x3", {
        "description": "Strings I-IV-V-I progression ×3, 100bpm, 14.4s",
        "expected": {
            "short_context": "HIGH — 4-bar harmonic cycle clear",
            "medium_context": "HIGH — phrase structure from repetition",
            "structure_pred": "HIGH — harmonic pattern learned by 2nd cycle",
        },
        "science": "Tillmann 2003: repeated chord progressions build implicit priming",
    })

    # ── 13: Piano modulating progression — RISING context_depth ────────
    quarter = 60.0 / 100.0
    bar_dur = 4 * quarter
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # C major → A minor → F major → D minor → G major → C major
    prog = [C_MAJ, A_MIN, F_MAJ, D_MIN, G_MAJ, [E4, G4, B4],
            [D4, Gb4, A4], C_MAJ_WIDE]
    t = 0.0
    for ch in prog:
        for p in ch:
            inst.notes.append(Note(velocity=72, pitch=p,
                                   start=t, end=t + bar_dur - 0.02))
        t += bar_dur
    pm.instruments.append(inst)
    save(pm, "hmce", "13_piano_modulating_prog", {
        "description": "Piano modulating progression C→Am→F→Dm→G→Em→D→C, 100bpm, 19.2s",
        "expected": {
            "context_depth": "RISING — increasing harmonic complexity builds context",
            "medium_context": "RISING — phrase structure emerges from harmonic journey",
        },
        "science": "Pearce 2018: tonal modulation increases contextual processing demand",
    })

    # ── 14: Piano single sustained note — MINIMAL context ─────────────
    pm = _pm_note(C4, 8.0, PIANO, 70)
    save(pm, "hmce", "14_piano_sustained_c4", {
        "description": "Piano single C4 sustained, 8s",
        "expected": {
            "short_context": "MINIMAL — no sequential structure",
            "medium_context": "LOW — single event, no phrases",
            "context_depth": "LOW — nothing to accumulate",
        },
        "science": "Control: single note = minimum structural information",
    })

    # ── 15: Piano+Cello call-response — alternation pattern ───────────
    quarter = 60.0 / 110.0
    pm = pretty_midi.PrettyMIDI()
    pno = pretty_midi.Instrument(program=PIANO)
    vcl = pretty_midi.Instrument(program=CELLO)
    t = 0.0
    for rep in range(4):
        # Piano call (1 bar)
        for i, p in enumerate([C5, D5, E5, G5]):
            pno.notes.append(Note(velocity=80, pitch=p,
                                  start=t + i * quarter,
                                  end=t + i * quarter + quarter - 0.02))
        t += 4 * quarter
        # Cello response (1 bar)
        for i, p in enumerate([G3, A3, B3, C4]):
            vcl.notes.append(Note(velocity=75, pitch=p,
                                  start=t + i * quarter,
                                  end=t + i * quarter + quarter - 0.02))
        t += 4 * quarter
    pm.instruments.extend([pno, vcl])
    save(pm, "hmce", "15_piano_cello_call_response", {
        "description": "Piano+Cello call-response: 1-bar alternation ×4, 110bpm, 17.5s",
        "expected": {
            "structure_pred": "HIGH — alternation pattern = predictable structure",
            "short_context": "HIGH — call-response cycle clear",
            "medium_context": "HIGH — dialogue pattern emerges",
        },
        "science": "Koelsch 2009: antiphonal structure builds hierarchical expectations",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 4: Cross-unit Integration (10 stimuli)
# ═══════════════════════════════════════════════════════════════════════

def generate_cross_stimuli() -> None:
    """10 stimuli testing cross-unit interactions (PEOM×HGSIC×HMCE)."""

    # ── 01: Full groove + phrases — ALL HIGH ───────────────────────────
    pm = _pm_drum_with_velocity({
        KICK: [(0, 110), (6, 80), (10, 90)],
        SNARE: [(4, 110), (12, 110)],
        CLOSED_HH: [(i, 70) for i in range(0, 16, 2)],
    }, bpm=110.0, n_bars=5)
    quarter = 60.0 / 110.0
    bar_dur = 4 * quarter
    bass = pretty_midi.Instrument(program=33)
    chords_cycle = [C_MAJ, F_MAJ, G_MAJ, C_MAJ]
    t = 0.0
    for bar in range(5):
        ch = chords_cycle[bar % 4]
        bass.notes.append(Note(velocity=85, pitch=ch[0] - 12,
                               start=t, end=t + bar_dur - 0.02))
        t += bar_dur
    pm.instruments.append(bass)
    _add_chord_track(pm, chords_cycle + [C_MAJ], [bar_dur] * 5, PIANO, 60)
    save(pm, "cross", "01_groove_with_phrases", {
        "description": "Drums+Bass+Piano groove with I-IV-V-I phrases, 110bpm, 10.9s",
        "expected": {
            "period_entrainment": "HIGH — isochronous drum grid",
            "groove_quality": "HIGH — medium syncopation groove",
            "context_depth": "HIGH — harmonic progression provides structure",
        },
        "science": "Full integration: motor + groove + context co-activated",
    })

    # ── 02: Piano melody alone — HMCE HIGH, motor LOW ─────────────────
    quarter = 60.0 / 100.0
    mel = [C5, D5, E5, G5, A5, G5, E5, D5, C5, E5, G5, C6,
           B5, G5, E5, D5, C5, D5, E5, G5]
    durs = [quarter * float(np.random.RandomState(33).choice([1, 1, 2, 0.5]))
            for _ in mel]
    pm = _pm_melody(mel, durs, PIANO, 80)
    save(pm, "cross", "02_piano_melody_no_rhythm", {
        "description": "Piano melody alone (no drums/bass), irregular rhythm, ~12s",
        "expected": {
            "context_depth": "HIGH — pitch contour + tonal structure",
            "groove_quality": "LOW — no rhythmic grid, no groove",
            "period_entrainment": "LOW — irregular IOIs",
        },
        "science": "Dissociation: context without motor entrainment",
    })

    # ── 03: Drums only — motor HIGH, context LOW ──────────────────────
    pm = _pm_drum_with_velocity({
        KICK: [(0, 110), (3, 80), (6, 70), (10, 90)],
        SNARE: [(4, 110), (12, 110)],
        CLOSED_HH: [(i, 70) for i in range(0, 16, 2)],
    }, bpm=100.0, n_bars=5)
    save(pm, "cross", "03_drums_only_no_harmony", {
        "description": "Drums only: funk pattern, no melody/harmony, 100bpm, 10s",
        "expected": {
            "period_entrainment": "HIGH — clear beat grid",
            "groove_quality": "HIGH — rhythmic groove present",
            "context_depth": "LOW — no pitch/harmonic structure",
        },
        "science": "Dissociation: motor without hierarchical context",
    })

    # ── 04: Near-silence — ALL LOW ────────────────────────────────────
    pm = _pm_near_silence(5.0)
    save(pm, "cross", "04_near_silence", {
        "description": "Near-silence control, 5s",
        "expected": "ALL LOW — baseline for all F7 beliefs",
        "science": "Control: no auditory stimulus",
    })

    # ── 05: Orch crescendo with cadence — ALL RISING ──────────────────
    pm = pretty_midi.PrettyMIDI()
    str_inst = pretty_midi.Instrument(program=STRINGS)
    fl = pretty_midi.Instrument(program=FLUTE)
    vcl = pretty_midi.Instrument(program=CELLO)
    quarter = 60.0 / 100.0
    bar_dur = 4 * quarter
    chords = [C_MAJ, F_MAJ, D_MIN, G_DOM7, C_MAJ_WIDE]
    for idx, ch in enumerate(chords):
        v = 40 + int(80 * idx / (len(chords) - 1))
        t_start = idx * bar_dur
        for p in ch:
            str_inst.notes.append(Note(velocity=v, pitch=p,
                                       start=t_start, end=t_start + bar_dur - 0.02))
        vcl.notes.append(Note(velocity=v, pitch=ch[0] - 12,
                              start=t_start, end=t_start + bar_dur - 0.02))
    mel = [E5, F5, G5, A5, G5, F5, E5, D5, C5, E5, G5, C6,
           B5, A5, G5, F5, E5, D5, C5, C5]
    t = 0.0
    for p in mel:
        v_mel = 50 + int(70 * t / (5 * bar_dur))
        fl.notes.append(Note(velocity=min(v_mel, 120), pitch=p,
                             start=t, end=t + quarter - 0.02))
        t += quarter
    pm.instruments.extend([str_inst, fl, vcl])
    save(pm, "cross", "05_orch_crescendo_cadence", {
        "description": "Strings+Flute+Cello crescendo with I-IV-ii-V-I cadence, 100bpm, 12s",
        "expected": {
            "period_entrainment": "MODERATE — not strongly metric, but regular",
            "groove_quality": "LOW-MODERATE — no groove rhythm, but dynamic arc",
            "context_depth": "RISING — harmonic cadence builds context",
            "phrase_boundary_pred": "HIGH at V→I cadence (bar 4→5)",
        },
        "science": "Co-activation: crescendo + cadence drives context + motor",
    })

    # ── 06: Groove breakdown (groove→chaos→groove) — trajectory test ──
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    step = 60.0 / 110.0 / 4
    # Phase 1 (bars 1-3): clean groove
    for bar in range(3):
        bt = bar * 16 * step
        for s, v in [(0, 110), (6, 80), (10, 90)]:
            drums.notes.append(Note(velocity=v, pitch=KICK,
                                    start=bt + s * step, end=bt + s * step + step * 0.5))
        for s in [4, 12]:
            drums.notes.append(Note(velocity=110, pitch=SNARE,
                                    start=bt + s * step, end=bt + s * step + step * 0.5))
        for s in range(0, 16, 2):
            drums.notes.append(Note(velocity=70, pitch=CLOSED_HH,
                                    start=bt + s * step, end=bt + s * step + step * 0.3))
    # Phase 2 (bars 4-5): chaos — random hits
    rng = np.random.RandomState(44)
    for bar in range(3, 5):
        bt = bar * 16 * step
        for i in range(16):
            t = bt + i * step
            dn = [KICK, SNARE, CLOSED_HH, TOM_MID][int(rng.randint(0, 4))]
            drums.notes.append(Note(velocity=int(rng.randint(40, 120)),
                                    pitch=dn, start=t, end=t + step * 0.3))
    # Phase 3 (bars 6-8): groove returns
    for bar in range(5, 8):
        bt = bar * 16 * step
        for s, v in [(0, 110), (6, 80), (10, 90)]:
            drums.notes.append(Note(velocity=v, pitch=KICK,
                                    start=bt + s * step, end=bt + s * step + step * 0.5))
        for s in [4, 12]:
            drums.notes.append(Note(velocity=110, pitch=SNARE,
                                    start=bt + s * step, end=bt + s * step + step * 0.5))
        for s in range(0, 16, 2):
            drums.notes.append(Note(velocity=70, pitch=CLOSED_HH,
                                    start=bt + s * step, end=bt + s * step + step * 0.3))
    pm.instruments.append(drums)
    save(pm, "cross", "06_groove_breakdown_recovery", {
        "description": "Drums groove→chaos→groove: 3+2+3 bars, 110bpm, ~17s",
        "expected": {
            "groove_quality": "HIGH→LOW→HIGH — breakdown and recovery",
            "groove_trajectory": "FALLING then RISING — trajectory tracks breakdown",
            "period_lock_strength": "HIGH→LOW→HIGH — lock disrupted during chaos",
        },
        "science": "HGSIC trajectory test: groove recovery after disruption",
    })

    # ── 07: Metric modulation 4/4→3/4 — PEOM re-entrainment ──────────
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    quarter = 60.0 / 120.0
    # Phase 1: 4/4 (4 bars)
    for bar in range(4):
        bt = bar * 4 * quarter
        drums.notes.append(Note(velocity=100, pitch=KICK, start=bt, end=bt + 0.05))
        drums.notes.append(Note(velocity=90, pitch=SNARE,
                                start=bt + 2 * quarter, end=bt + 2 * quarter + 0.05))
        for beat in range(4):
            t = bt + beat * quarter
            drums.notes.append(Note(velocity=70, pitch=CLOSED_HH,
                                    start=t, end=t + 0.03))
    # Phase 2: 3/4 (5 bars)
    t_offset = 4 * 4 * quarter
    for bar in range(5):
        bt = t_offset + bar * 3 * quarter
        drums.notes.append(Note(velocity=100, pitch=KICK, start=bt, end=bt + 0.05))
        for beat in range(3):
            t = bt + beat * quarter
            drums.notes.append(Note(velocity=70, pitch=CLOSED_HH,
                                    start=t, end=t + 0.03))
    pm.instruments.append(drums)
    save(pm, "cross", "07_metric_modulation_4_to_3", {
        "description": "Drums 4/4 (4 bars) → 3/4 (5 bars), 120bpm, ~11.5s",
        "expected": {
            "period_entrainment": "RE-ENTRAINING — period adapts to new meter",
            "meter_structure": "SHIFT — 4/4 clear then 3/4 clear",
            "phrase_boundary_pred": "HIGH at meter change point",
        },
        "science": "Grahn & Brett 2007: meter change requires putamen/SMA re-calibration",
    })

    # ── 08: Multi-section intro-verse-chorus — progressive context ────
    pm = pretty_midi.PrettyMIDI()
    pno = pretty_midi.Instrument(program=PIANO)
    quarter = 60.0 / 120.0
    bar_dur = 4 * quarter
    # Intro (2 bars): just C major
    t = 0.0
    for _ in range(2):
        for p in C_MAJ:
            pno.notes.append(Note(velocity=60, pitch=p,
                                  start=t, end=t + bar_dur - 0.02))
        t += bar_dur
    # Verse (4 bars): I-vi-IV-V
    verse = [C_MAJ, A_MIN, F_MAJ, G_MAJ]
    for ch in verse:
        for p in ch:
            pno.notes.append(Note(velocity=72, pitch=p,
                                  start=t, end=t + bar_dur - 0.02))
        t += bar_dur
    # Chorus (4 bars): I-IV-V-I with higher energy
    chorus = [C_MAJ_WIDE, F_MAJ + [C5], G_MAJ + [B4], C_MAJ_WIDE]
    for ch in chorus:
        for p in ch:
            pno.notes.append(Note(velocity=90, pitch=p,
                                  start=t, end=t + bar_dur - 0.02))
        t += bar_dur
    pm.instruments.append(pno)
    save(pm, "cross", "08_intro_verse_chorus", {
        "description": "Piano intro(2)-verse(4)-chorus(4), C major, 120bpm, 20s",
        "expected": {
            "context_depth": "RISING — sections accumulate context progressively",
            "medium_context": "HIGH — verse and chorus = clear phrases",
            "long_context": "EMERGING — multi-section form",
            "phrase_boundary_pred": "HIGH at intro→verse and verse→chorus",
        },
        "science": "Pearce 2018: multi-section forms build hierarchical expectations",
    })

    # ── 09: Groove with tempo rubato — PEOM compromised, HGSIC partly ─
    pm = pretty_midi.PrettyMIDI()
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    rng = np.random.RandomState(66)
    base_ioi = 60.0 / 110.0
    step_base = base_ioi / 4
    t = 0.0
    for bar in range(5):
        # Add tempo wobble: ±10% random per 16th
        for s in range(16):
            wobble = 1.0 + float(rng.uniform(-0.10, 0.10))
            step = step_base * wobble
            if s in [0, 6, 10]:
                drums.notes.append(Note(velocity=100, pitch=KICK,
                                        start=t, end=t + step * 0.5))
            if s in [4, 12]:
                drums.notes.append(Note(velocity=105, pitch=SNARE,
                                        start=t, end=t + step * 0.5))
            if s % 2 == 0:
                drums.notes.append(Note(velocity=65, pitch=CLOSED_HH,
                                        start=t, end=t + step * 0.3))
            t += step
    pm.instruments.append(drums)
    save(pm, "cross", "09_groove_with_rubato", {
        "description": "Drums groove with ±10% tempo rubato, ~110bpm, ~10s",
        "expected": {
            "period_entrainment": "MODERATE — tempo wobble disrupts period lock",
            "groove_quality": "MODERATE — groove pattern present but unstable",
            "timing_precision": "LOW — high IOI variability",
        },
        "science": "Dissociation: groove survives mild tempo jitter but PEOM suffers",
    })

    # ── 10: Dense polyphony dissolving to unison — FALLING context ────
    pm = pretty_midi.PrettyMIDI()
    fl = pretty_midi.Instrument(program=FLUTE)
    st = pretty_midi.Instrument(program=STRINGS)
    vcl = pretty_midi.Instrument(program=CELLO)
    quarter = 60.0 / 100.0
    # Phase 1 (0-4s): rich 3-part counterpoint
    voices = [(fl, [G5, A5, B5, C6, D6, C6, B5, A5]),
              (st, [E4, F4, G4, A4, B4, A4, G4, F4]),
              (vcl, [C3, D3, E3, F3, G3, F3, E3, D3])]
    for inst_obj, notes in voices:
        t = 0.0
        for p in notes:
            inst_obj.notes.append(Note(velocity=75, pitch=p,
                                       start=t, end=t + quarter - 0.02))
            t += quarter
    # Phase 2 (4-8s): converge to unison C4
    for inst_obj in [fl, st, vcl]:
        for i in range(8):
            t = 4.0 + i * quarter
            inst_obj.notes.append(Note(velocity=65, pitch=C4,
                                       start=t, end=t + quarter - 0.02))
    pm.instruments.extend([fl, st, vcl])
    save(pm, "cross", "10_polyphony_to_unison", {
        "description": "Flute+Strings+Cello: 3-part counterpoint → unison C4, 100bpm, 8s",
        "expected": {
            "context_depth": "FALLING — from rich polyphony to minimal unison",
            "short_context": "HIGH→LOW — decreasing local complexity",
        },
        "science": "Context simplification: polyphony→unison reduces structural information",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 5: Multi-voice Polyphonic (10 stimuli)
# ═══════════════════════════════════════════════════════════════════════

def generate_polyphonic_stimuli() -> None:
    """10 stimuli testing multi-voice and polyphonic textures."""

    # ── 01: SATB chorale 4-bar phrases (Flute+Strings+Cello) ────────
    pm = pretty_midi.PrettyMIDI()
    soprano = pretty_midi.Instrument(program=FLUTE)
    alto = pretty_midi.Instrument(program=STRINGS)
    tenor = pretty_midi.Instrument(program=STRINGS)
    bass = pretty_midi.Instrument(program=CELLO)
    voicings = [
        (E5, C5, G4, C3), (C5, A4, E4, A2), (F5, C5, A4, F3),
        (D5, B4, G4, G3), (E5, C5, G4, C3), (C5, A4, E4, A2),
        (F5, C5, A4, F3), (E5, C5, G4, C3),
    ]
    for idx, (s, a, te, b) in enumerate(voicings):
        t0, t1 = idx * 1.5, (idx + 1) * 1.5 - 0.02
        soprano.notes.append(Note(velocity=75, pitch=s, start=t0, end=t1))
        alto.notes.append(Note(velocity=65, pitch=a, start=t0, end=t1))
        tenor.notes.append(Note(velocity=65, pitch=te, start=t0, end=t1))
        bass.notes.append(Note(velocity=70, pitch=b, start=t0, end=t1))
    pm.instruments.extend([soprano, alto, tenor, bass])
    save(pm, "polyphonic", "01_satb_chorale", {
        "description": "SATB chorale 8 chords (Flute+Strings+Cello), 12s",
        "expected": {
            "context_depth": "HIGH — rich 4-part harmonic context",
            "short_context": "HIGH — harmonic progression clear",
        },
        "science": "Tillmann 2003: implicit harmonic structure from chorale texture",
    })

    # ── 02: Piano + percussion (beat + harmony) ─────────────────────
    pm = _pm_progression(
        [C_MAJ, F_MAJ, G_MAJ, C_MAJ] * 2,
        [1.0] * 8, program=PIANO, velocity=75)
    rock_pat = {
        KICK:      [0, 4, 8, 12],
        SNARE:     [4, 12],
        CLOSED_HH: [0, 2, 4, 6, 8, 10, 12, 14],
    }
    _add_drum_track(pm, rock_pat, bpm=120.0, n_bars=2)
    save(pm, "polyphonic", "02_piano_plus_drums", {
        "description": "Piano chords I-IV-V-I + rock drums 120bpm, 8s",
        "expected": {
            "period_entrainment": "HIGH — beat from drums",
            "groove_quality": "MODERATE — simple beat+harmony",
            "context_depth": "MODERATE — harmonic + rhythmic",
        },
        "science": "Grahn & Brett 2007: combined rhythm+harmony activates motor+auditory",
    })

    # ── 03: String quartet with phrase structure ─────────────────────
    pm = pretty_midi.PrettyMIDI()
    v1 = pretty_midi.Instrument(program=VIOLIN)
    v2 = pretty_midi.Instrument(program=VIOLIN)
    va = pretty_midi.Instrument(program=STRINGS)
    vc = pretty_midi.Instrument(program=CELLO)
    phrase1 = [(E5, C5, G4, C3), (D5, B4, G4, G2), (C5, A4, E4, A2), (D5, B4, F4, G2)]
    phrase2 = [(F5, C5, A4, F3), (E5, Db5, Ab4, Ab3), (D5, B4, G4, G3), (E5, C5, G4, C3)]
    for idx, (s, a, te, b) in enumerate(phrase1 + phrase2):
        t0, t1 = idx * 2.0, (idx + 1) * 2.0 - 0.02
        v1.notes.append(Note(velocity=70, pitch=s, start=t0, end=t1))
        v2.notes.append(Note(velocity=60, pitch=a, start=t0, end=t1))
        va.notes.append(Note(velocity=60, pitch=te, start=t0, end=t1))
        vc.notes.append(Note(velocity=65, pitch=b, start=t0, end=t1))
    pm.instruments.extend([v1, v2, va, vc])
    save(pm, "polyphonic", "03_string_quartet_phrases", {
        "description": "String quartet 2 contrasting 4-bar phrases, 16s",
        "expected": {
            "context_depth": "HIGH — extended context, phrase contrast",
            "medium_context": "HIGH — phrase-level structure",
            "phrase_boundary_pred": "HIGH — contrast between phrases",
        },
        "science": "Pearce 2018: phrase-level statistical learning in polyphonic texture",
    })

    # ── 04: Piano + walking bass ─────────────────────────────────────
    pm = _pm_progression(
        [C_MAJ, A_MIN, D_MIN, G_DOM7] * 2,
        [1.5] * 8, program=PIANO, velocity=70)
    bass_notes = [C3, E3, A2, C3, D3, F3, G2, B2,
                  C3, E3, A2, C3, D3, F3, G2, B2]
    bass_durs = [0.75] * 16
    _add_bass_line(pm, bass_notes, bass_durs, program=33, velocity=85)
    save(pm, "polyphonic", "04_piano_walking_bass", {
        "description": "Piano chords + walking bass line, 12s",
        "expected": {
            "groove_quality": "MODERATE — walking bass provides steady pulse",
            "context_depth": "MODERATE — harmonic + bass line context",
        },
        "science": "Janata 2012: bass+harmony coupling supports groove perception",
    })

    # ── 05: Full band: drums+bass+piano+melody, 12s ─────────────────
    pm = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=PIANO)
    chords = [C_MAJ, F_MAJ, A_MIN, G_MAJ] * 3
    t = 0.0
    for chord in chords:
        for p in chord:
            piano.notes.append(Note(velocity=65, pitch=p,
                                     start=t, end=t + 0.98))
        t += 1.0
    pm.instruments.append(piano)
    melody_inst = pretty_midi.Instrument(program=FLUTE)
    melody_notes = [E5, D5, C5, D5, F5, E5, D5, C5,
                    E5, D5, C5, B4, C5, D5, E5, C5,
                    E5, F5, G5, E5, D5, C5, B4, C5]
    for i, p in enumerate(melody_notes):
        melody_inst.notes.append(Note(velocity=75, pitch=p,
                                       start=i * 0.5, end=i * 0.5 + 0.45))
    pm.instruments.append(melody_inst)
    _add_bass_line(pm, [C3, C3, F3, F3, A2, A2, G2, G2] * 2,
                   [0.75] * 16, program=33, velocity=85)
    funk_pat = {
        KICK:      [0, 6, 8, 14],
        SNARE:     [4, 12],
        CLOSED_HH: [0, 2, 4, 6, 8, 10, 12, 14],
    }
    _add_drum_track(pm, funk_pat, bpm=120.0, n_bars=6)
    save(pm, "polyphonic", "05_full_band", {
        "description": "Full band: drums+bass+piano+flute melody, 120bpm, 12s",
        "expected": {
            "groove_quality": "HIGH — ceiling test, full ensemble",
            "motor_preparation": "HIGH — maximum motor drive",
            "context_depth": "HIGH — melody+harmony+rhythm",
        },
        "science": "Janata 2012: full ensemble r=0.84 motor area activation",
    })

    # ── 06: Ensemble unison -> polyphonic spread ─────────────────────
    pm = pretty_midi.PrettyMIDI()
    fl = pretty_midi.Instrument(program=FLUTE)
    st = pretty_midi.Instrument(program=STRINGS)
    ce = pretty_midi.Instrument(program=CELLO)
    for i in range(8):
        t0, t1 = i * 0.5, i * 0.5 + 0.45
        fl.notes.append(Note(velocity=70, pitch=C4, start=t0, end=t1))
        st.notes.append(Note(velocity=65, pitch=C4, start=t0, end=t1))
        ce.notes.append(Note(velocity=65, pitch=C4, start=t0, end=t1))
    poly_fl = [E5, D5, C5, E5, F5, E5, D5, C5]
    poly_st = [G4, F4, E4, G4, A4, G4, F4, E4]
    poly_ce = [C3, D3, E3, C3, F3, E3, D3, C3]
    for i in range(8):
        t0, t1 = 4.0 + i * 0.5, 4.0 + i * 0.5 + 0.45
        fl.notes.append(Note(velocity=75, pitch=poly_fl[i], start=t0, end=t1))
        st.notes.append(Note(velocity=65, pitch=poly_st[i], start=t0, end=t1))
        ce.notes.append(Note(velocity=70, pitch=poly_ce[i], start=t0, end=t1))
    pm.instruments.extend([fl, st, ce])
    save(pm, "polyphonic", "06_unison_to_polyphony", {
        "description": "Flute+Strings+Cello: unison -> 3-part polyphony, 8s",
        "expected": {
            "context_depth": "RISING — from minimal to rich polyphonic texture",
        },
        "science": "Pearce 2018: increasing voice count raises information content",
    })

    # ── 07: Drum pattern + sustained organ ───────────────────────────
    pm = _pm_chord(C_MAJ_WIDE, duration=8.0, program=ORGAN, velocity=60)
    rock_d = {
        KICK:      [0, 4, 8, 12],
        SNARE:     [4, 12],
        CLOSED_HH: [0, 2, 4, 6, 8, 10, 12, 14],
    }
    _add_drum_track(pm, rock_d, bpm=120.0, n_bars=4)
    save(pm, "polyphonic", "07_drums_plus_organ", {
        "description": "Sustained organ C major + rock drums 120bpm, 8s",
        "expected": {
            "groove_quality": "MODERATE — groove from drums, no harmonic change",
            "period_entrainment": "HIGH — clear beat",
            "context_depth": "LOW — static harmony",
        },
        "science": "Grahn 2007: rhythm dominates motor response over static harmony",
    })

    # ── 08: Trumpet melody over string pad ───────────────────────────
    pm = pretty_midi.PrettyMIDI()
    pad = pretty_midi.Instrument(program=STRINGS)
    for p in C_MAJ_WIDE:
        pad.notes.append(Note(velocity=50, pitch=p, start=0.0, end=4.0))
    for p in [F3, A3, C4, F4]:
        pad.notes.append(Note(velocity=50, pitch=p, start=4.0, end=8.0))
    pm.instruments.append(pad)
    trpt = pretty_midi.Instrument(program=TRUMPET)
    mel = [G5, E5, C5, D5, E5, F5, G5, A5,
           A5, G5, F5, E5, D5, C5, D5, E5]
    for i, p in enumerate(mel):
        trpt.notes.append(Note(velocity=80, pitch=p,
                                start=i * 0.5, end=i * 0.5 + 0.45))
    pm.instruments.append(trpt)
    save(pm, "polyphonic", "08_trumpet_over_strings", {
        "description": "Trumpet melody over string pad, 8s",
        "expected": {
            "medium_context": "HIGH — melody phrase structure",
            "phrase_boundary_pred": "MODERATE — melodic phrase at midpoint",
        },
        "science": "Koelsch 2009: melodic stream drives phrase boundary detection",
    })

    # ── 09: Piano stride (bass+chord alternation) ───────────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    ioi = 60.0 / 120.0 / 2
    stride = [
        (C3, None), (None, C_MAJ), (G2, None), (None, C_MAJ),
        (F3, None), (None, F_MAJ), (C3, None), (None, F_MAJ),
        (A2, None), (None, A_MIN), (E3, None), (None, A_MIN),
        (G2, None), (None, G_MAJ), (D3, None), (None, G_MAJ),
    ] * 2
    t = 0.0
    for bass_p, chord in stride:
        if bass_p is not None:
            inst.notes.append(Note(velocity=85, pitch=bass_p,
                                    start=t, end=t + ioi * 0.8))
        if chord is not None:
            for p in chord:
                inst.notes.append(Note(velocity=70, pitch=p,
                                        start=t, end=t + ioi * 0.8))
        t += ioi
    pm.instruments.append(inst)
    save(pm, "polyphonic", "09_piano_stride", {
        "description": "Piano stride (bass-chord alternation), 120bpm, 8s",
        "expected": {
            "groove_quality": "MODERATE — stride has groove character",
            "period_entrainment": "HIGH — regular alternation",
            "context_depth": "MODERATE — harmonic progression",
        },
        "science": "Janata 2012: stride patterns activate motor+auditory cortex",
    })

    # ── 10: Brass fanfare with drum cadence ──────────────────────────
    pm = pretty_midi.PrettyMIDI()
    trpt = pretty_midi.Instrument(program=TRUMPET)
    trmb = pretty_midi.Instrument(program=TROMBONE)
    horn = pretty_midi.Instrument(program=FRENCH_HORN)
    fanfare = [
        (0.0, 0.75, [G5, D5, G4]),
        (0.75, 0.25, [A5, E5, A4]),
        (1.0, 1.0, [G5, D5, G4]),
        (2.0, 0.75, [A5, F5, A4]),
        (2.75, 0.25, [B5, G5, B4]),
        (3.0, 1.0, [C6, E5, C5]),
        (4.0, 2.0, [G5, D5, G4]),
    ]
    for t0, dur, pitches in fanfare:
        trpt.notes.append(Note(velocity=100, pitch=pitches[0],
                                start=t0, end=t0 + dur - 0.02))
        trmb.notes.append(Note(velocity=90, pitch=pitches[1],
                                start=t0, end=t0 + dur - 0.02))
        horn.notes.append(Note(velocity=85, pitch=pitches[2],
                                start=t0, end=t0 + dur - 0.02))
    pm.instruments.extend([trpt, trmb, horn])
    drums = pretty_midi.Instrument(program=0, is_drum=True)
    for i in range(24):
        drums.notes.append(Note(velocity=60 + i * 2, pitch=SNARE,
                                 start=i * 0.125, end=i * 0.125 + 0.1))
    drums.notes.append(Note(velocity=127, pitch=CRASH, start=4.0, end=4.5))
    drums.notes.append(Note(velocity=100, pitch=KICK, start=4.0, end=4.3))
    pm.instruments.append(drums)
    save(pm, "polyphonic", "10_brass_fanfare_drums", {
        "description": "Brass fanfare (trumpet+trombone+horn) + drum cadence, 6s",
        "expected": {
            "beat_prominence": "HIGH — strong rhythmic accents",
            "motor_preparation": "HIGH — fanfare drives motor activation",
            "context_depth": "MODERATE — short formal structure",
        },
        "science": "Grahn & Brett 2007: brass+percussion maximizes putamen activation",
    })

# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 6: Boundary Conditions (8 stimuli)
# ═══════════════════════════════════════════════════════════════════════

def generate_boundary_stimuli() -> None:
    """8 stimuli testing extreme / boundary conditions."""

    # ── 01: Near-silence ──────────────────────────────────────────────
    pm = _pm_near_silence(5.0)
    save(pm, "boundary", "01_near_silence", {
        "description": "Near-silence, single v=1 tick, 5s",
        "expected": "All beliefs near floor/baseline",
    })

    # ── 02: fff sustained cluster — maximum amplitude ─────────────────
    pm = _pm_chord(chromatic_cluster(C4, 6), 5.0, PIANO, 127)
    save(pm, "boundary", "02_fff_cluster", {
        "description": "Piano fff 6-note chromatic cluster, 5s",
        "expected": "Maximum amplitude, minimal period/groove/context",
    })

    # ── 03: Single loud click — impulse ───────────────────────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=127, pitch=C4, start=0.5, end=0.52))
    pm.instruments.append(inst)
    save(pm, "boundary", "03_single_click", {
        "description": "Piano single fff C4 click at 0.5s, <1s duration",
        "expected": "Transient impulse: no period, no groove, no context",
    })

    # ── 04: Dense random noise — noise floor ──────────────────────────
    pm = _pm_dense_random(6.0, seed=77, notes_per_sec=16)
    save(pm, "boundary", "04_dense_random_noise", {
        "description": "Dense random MIDI (16 notes/sec), 6s",
        "expected": "No periodicity, no structure, no groove",
    })

    # ── 05: Very slow tempo 40bpm — ultra-macro entrainment ───────────
    pm = _pm_isochronous(C4, 40.0, 10, PIANO, 80)
    save(pm, "boundary", "05_very_slow_40bpm", {
        "description": "Piano isochronous 40bpm, 10 beats, 15s",
        "expected": "period_entrainment: ultra-macro scale, near lower motor limit",
    })

    # ── 06: Very fast tempo 240bpm — near motor limit ─────────────────
    pm = _pm_isochronous(C4, 240.0, 32, PIANO, 90)
    save(pm, "boundary", "06_very_fast_240bpm", {
        "description": "Piano isochronous 240bpm, 32 beats, 8s",
        "expected": "period_entrainment: near upper motor limit, rapid periodicity",
    })

    # ── 07: Extreme register C1 + C7 ─────────────────────────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=80, pitch=C1, start=0.0, end=4.0))
    inst.notes.append(Note(velocity=80, pitch=C7, start=0.0, end=4.0))
    pm.instruments.append(inst)
    save(pm, "boundary", "07_extreme_register", {
        "description": "Piano C1 + C7 simultaneously, 4s",
        "expected": "All beliefs valid, register extremes",
    })

    # ── 08: Maximum duration 45s piece — long context accumulation ────
    quarter = 60.0 / 130.0
    bar_dur = 4 * quarter
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # 24-bar piece: AABA×2 with simple chords
    a_chords = [C_MAJ, F_MAJ, G_MAJ, C_MAJ]
    b_chords = [A_MIN, D_MIN, G_DOM7, C_MAJ]
    form = a_chords + a_chords + b_chords + a_chords
    form = form + form  # Double it for ~45s
    t = 0.0
    for ch in form[:32]:
        for p in ch:
            inst.notes.append(Note(velocity=70, pitch=p,
                                   start=t, end=t + bar_dur - 0.02))
        t += bar_dur
    pm.instruments.append(inst)
    save(pm, "boundary", "08_long_duration_45s", {
        "description": "Piano 32-bar AABA×2, 130bpm, ~44s",
        "expected": "context_depth: maximum accumulation over extended duration",
    })


# ═══════════════════════════════════════════════════════════════════════
# Metadata & Catalog Writers
# ═══════════════════════════════════════════════════════════════════════

def write_metadata() -> None:
    meta_path = OUTPUT_DIR / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(ALL_METADATA, f, indent=2, ensure_ascii=False)
    print(f"  Metadata -> {meta_path}")


def write_catalog() -> None:
    """Write STIMULUS-CATALOG.md with ordinal comparisons."""
    cat_path = OUTPUT_DIR / "STIMULUS-CATALOG.md"

    comparisons = [
        # ── PEOM — period_entrainment ──
        ("peom/01", "peom/12", "period_entrainment", "A>B",
         "Thaut 2015: isochronous > random IOI for period entrainment"),
        ("peom/01", "peom/11", "period_entrainment", "A>B",
         "Isochronous > rubato for period entrainment"),
        ("peom/01", "peom/08", "period_entrainment", "A>B",
         "Isochronous > heavy syncopation for entrainment"),
        ("peom/09", "peom/01", "period_entrainment", "A>B",
         "Ensemble unison > solo piano for entrainment strength"),
        ("peom/02", "peom/13", "period_entrainment", "A>B",
         "Slow iso > silence for period entrainment"),
        # ── PEOM — timing_precision ──
        ("peom/01", "peom/11", "timing_precision", "A>B",
         "Isochronous > rubato for timing precision (CV)"),
        ("peom/01", "peom/12", "timing_precision", "A>B",
         "Isochronous > random IOI for timing precision"),
        ("peom/02", "peom/14", "timing_precision", "A>B",
         "Slow iso > swing for timing precision"),
        # ── PEOM — period_lock_strength ──
        ("peom/01", "peom/07", "period_lock_strength", "A>B",
         "Isochronous > light syncopation for phase lock"),
        ("peom/07", "peom/08", "period_lock_strength", "A>B",
         "Nozaradan 2011: light > heavy syncopation for lock"),
        ("peom/01", "peom/15", "period_lock_strength", "A>B",
         "Isochronous > polyrhythm for lock strength"),
        # ── PEOM — kinematic_efficiency ──
        ("peom/09", "peom/12", "kinematic_efficiency", "A>B",
         "Ensemble iso > random for kinematic efficiency"),
        ("peom/10", "peom/11", "kinematic_efficiency", "A>B",
         "Piano+Cello iso > rubato for kinematic efficiency"),
        # ── PEOM — next_beat_pred ──
        ("peom/01", "peom/12", "next_beat_pred", "A>B",
         "Isochronous > random for beat prediction"),
        ("peom/04", "peom/12", "next_beat_pred", "A>B",
         "Accelerando (trackable) > random for prediction"),
        # ── HGSIC — groove_quality (inverted-U critical!) ──
        ("hgsic/02", "hgsic/04", "groove_quality", "A>B",
         "Witek 2014: medium syncopation > zero for groove"),
        ("hgsic/02", "hgsic/01", "groove_quality", "A>B",
         "Madison 2011: funk groove > straight beat for groove"),
        ("hgsic/02", "hgsic/03", "groove_quality", "A>B",
         "Madison 2011: medium > heavy syncopation (inverted-U)"),
        ("hgsic/06", "hgsic/04", "groove_quality", "A>B",
         "Jazz shuffle > isochronous for groove"),
        ("hgsic/05", "hgsic/11", "groove_quality", "A>B",
         "Drums+Bass funk > solo hi-hat for groove"),
        ("hgsic/07", "hgsic/15", "groove_quality", "A>B",
         "Reggae > marching for groove"),
        ("hgsic/10", "hgsic/14", "groove_quality", "A>B",
         "Full ensemble > random velocity for groove"),
        # ── HGSIC — beat_prominence ──
        ("hgsic/01", "hgsic/11", "beat_prominence", "A>B",
         "Grahn 2007: kick+snare > solo hi-hat for beat prominence"),
        ("hgsic/10", "hgsic/11", "beat_prominence", "A>B",
         "Full ensemble > solo hi-hat for beat prominence"),
        ("hgsic/02", "hgsic/14", "beat_prominence", "A>B",
         "Funk groove > random velocity for beat prominence"),
        # ── HGSIC — meter_structure ──
        ("hgsic/01", "hgsic/09", "meter_structure", "A>B",
         "Grahn 2007: regular 4/4 > complex 7/8 for meter clarity"),
        ("hgsic/08", "hgsic/09", "meter_structure", "A>B",
         "Waltz 3/4 > complex 7/8 for meter clarity"),
        ("hgsic/01", "hgsic/14", "meter_structure", "A>B",
         "Straight beat > random velocity for meter structure"),
        # ── HGSIC — groove_trajectory ──
        ("hgsic/12", "hgsic/13", "groove_trajectory", "A>B",
         "Crescendo groove > decrescendo groove for trajectory"),
        ("hgsic/12", "hgsic/04", "groove_trajectory", "A>B",
         "Crescendo groove > static isochronous for trajectory"),
        # ── HGSIC — motor_preparation ──
        ("hgsic/10", "hgsic/11", "motor_preparation", "A>B",
         "Janata 2012: full ensemble > solo for motor preparation"),
        ("hgsic/05", "hgsic/04", "motor_preparation", "A>B",
         "Drums+Bass > isochronous for motor preparation"),
        # ── HMCE — context_depth ──
        ("hmce/04", "hmce/01", "context_depth", "A>B",
         "Pearce 2018: 32-bar AABA > 2-bar ostinato for context depth"),
        ("hmce/03", "hmce/11", "context_depth", "A>B",
         "16-bar AABB > atonal random for context depth"),
        ("hmce/02", "hmce/14", "context_depth", "A>B",
         "8-bar phrase > single note for context depth"),
        # ── HMCE — short_context ──
        ("hmce/01", "hmce/14", "short_context", "A>B",
         "2-bar ostinato > single note for short context"),
        ("hmce/07", "hmce/11", "short_context", "A>B",
         "Phrase with gap > atonal for short context"),
        # ── HMCE — medium_context ──
        ("hmce/02", "hmce/11", "medium_context", "A>B",
         "8-bar phrase > atonal for medium context"),
        ("hmce/12", "hmce/14", "medium_context", "A>B",
         "I-IV-V-I ×3 > single note for medium context"),
        # ── HMCE — long_context ──
        ("hmce/03", "hmce/01", "long_context", "A>B",
         "16-bar AABB > 2-bar ostinato for long context"),
        ("hmce/04", "hmce/11", "long_context", "A>B",
         "32-bar AABA > atonal for long context"),
        # ── HMCE — phrase_boundary_pred ──
        ("hmce/07", "hmce/06", "phrase_boundary_pred", "A>B",
         "Koelsch 2009: silence gap > continuous for boundary detection"),
        ("hmce/05", "hmce/06", "phrase_boundary_pred", "A>B",
         "Key change > chromatic for boundary detection"),
        ("hmce/09", "hmce/10", "phrase_boundary_pred", "A>B",
         "ABA form > through-composed for boundary detection"),
        # ── HMCE — structure_pred ──
        ("hmce/08", "hmce/10", "structure_pred", "A>B",
         "Ascending sequence > through-composed for structure prediction"),
        ("hmce/09", "hmce/10", "structure_pred", "A>B",
         "ABA form > through-composed for structure prediction"),
        ("hmce/12", "hmce/11", "structure_pred", "A>B",
         "I-IV-V-I repeated > atonal for structure prediction"),
        # ── Cross-unit ──
        ("cross/01", "cross/04", "groove_quality", "A>B",
         "Full groove+phrases > silence for groove"),
        ("cross/01", "cross/02", "period_entrainment", "A>B",
         "Groove+phrases > melody alone for entrainment"),
        ("cross/03", "cross/02", "groove_quality", "A>B",
         "Drums only > melody alone for groove"),
        ("cross/02", "cross/03", "context_depth", "A>B",
         "Melody alone > drums only for context depth"),
        ("cross/01", "cross/04", "context_depth", "A>B",
         "Groove+phrases > silence for context depth"),
        # ── Polyphonic ──
        ("polyphonic/05", "polyphonic/07", "groove_quality", "A>B",
         "Full band > drums+organ for groove quality"),
        ("polyphonic/05", "polyphonic/04", "groove_quality", "A>B",
         "Full band > piano+walking bass for groove"),
        ("polyphonic/01", "polyphonic/07", "context_depth", "A>B",
         "SATB chorale > drums+organ for context depth"),
        ("polyphonic/03", "polyphonic/07", "context_depth", "A>B",
         "String quartet > drums+organ for context depth"),
        ("polyphonic/05", "polyphonic/09", "motor_preparation", "A>B",
         "Full band > piano stride for motor preparation"),
        ("polyphonic/10", "polyphonic/08", "beat_prominence", "A>B",
         "Brass fanfare > trumpet melody for beat prominence"),
        ("polyphonic/02", "polyphonic/08", "period_entrainment", "A>B",
         "Piano+drums > trumpet+strings for period entrainment"),
        ("polyphonic/06", "polyphonic/07", "context_depth", "A>B",
         "Unison->polyphony (rising) > drums+organ (static) for context"),
        ("polyphonic/03", "polyphonic/06", "phrase_boundary_pred", "A>B",
         "String quartet phrases > unison->polyphony for boundary pred"),
        ("polyphonic/05", "boundary/01", "groove_quality", "A>B",
         "Full band > near-silence for groove (ceiling vs floor)"),
    ]

    lines = [
        "# F7 Motor & Timing — Stimulus Catalog",
        "",
        f"**Total stimuli:** {len(ALL_METADATA)}",
        f"**Ordinal comparisons:** {len(comparisons)}",
        "",
        "## Target Beliefs (17)",
        "",
        "| Unit | Beliefs | Type |",
        "|------|---------|------|",
        "| PEOM (5) | period_entrainment, kinematic_efficiency | Core |",
        "| | timing_precision, period_lock_strength | Appraisal |",
        "| | next_beat_pred | Anticipation |",
        "| HGSIC (6) | groove_quality | Core |",
        "| | beat_prominence, meter_structure, auditory_motor_coupling, motor_preparation | Appraisal |",
        "| | groove_trajectory | Anticipation |",
        "| HMCE (6) | context_depth | Core |",
        "| | short_context, medium_context, long_context | Appraisal |",
        "| | phrase_boundary_pred, structure_pred | Anticipation |",
        "",
        "## Ordinal Comparison Matrix",
        "",
        "| # | Stimulus A | Stimulus B | Belief | Direction | Science |",
        "|---|-----------|-----------|--------|-----------|---------|",
    ]
    for i, (a, b, belief, direction, science) in enumerate(comparisons, 1):
        lines.append(f"| {i} | {a} | {b} | {belief} | {direction} | {science} |")

    lines.extend(["", "## Stimulus Index", ""])
    for key, meta in sorted(ALL_METADATA.items()):
        desc = meta.get("description", "")
        dur = meta.get("duration_s", "?")
        lines.append(f"- **{key}** ({dur}s): {desc}")

    with open(cat_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Catalog -> {cat_path}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating F7 Motor & Timing test audio...")
    print()

    print("[1/6] PEOM — Period Entrainment Optimization Model (15 stimuli)")
    generate_peom_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('peom/'))} files")

    print("[2/6] HGSIC — Hierarchical Groove State Integration (15 stimuli)")
    generate_hgsic_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('hgsic/'))} files")

    print("[3/6] HMCE — Hierarchical Musical Context Encoding (15 stimuli)")
    generate_hmce_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('hmce/'))} files")

    print("[4/6] Cross-unit Integration (10 stimuli)")
    generate_cross_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('cross/'))} files")

    print("[5/6] Multi-voice Polyphonic (10 stimuli)")
    generate_polyphonic_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('polyphonic/'))} files")

    print("[6/6] Boundary Conditions (8 stimuli)")
    generate_boundary_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('boundary/'))} files")

    print()
    print(f"Total: {len(ALL_METADATA)} stimuli")
    write_metadata()
    write_catalog()
    print()
    print("Done.")


if __name__ == "__main__":
    main()
