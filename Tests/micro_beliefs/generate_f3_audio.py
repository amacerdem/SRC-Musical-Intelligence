#!/usr/bin/env python
"""Generate F3 (Attention & Salience) micro-belief test audio via MIDI + FluidSynth.

Every stimulus is fully deterministic — we know exactly which notes,
intervals, velocity and instrument program were used, giving us
ground truth for every F3 belief (15 beliefs across 4 mechanism groups:
SNEM, IACM, CSG, AACM).

Saves to Test-Audio/micro_beliefs/f3/{mechanism}/*.wav + *.mid

Total: ~63 stimuli across 6 groups:
  snem/      (18 stimuli) — Beat entrainment + Meter hierarchy
  iacm/      (14 stimuli) — Attention capture + Object segregation + Precision
  csg/       (8 stimuli)  — Salience network + Valence + Load
  aacm/      (7 stimuli)  — Aesthetic engagement + Savoring
  cross/     (8 stimuli)  — Cross-Mechanism Integration
  boundary/  (5 stimuli)  — Boundary Conditions

Run::
    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/micro_beliefs/generate_f3_audio.py
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Dict, List

import numpy as np
import pretty_midi
import torch
from scipy.io import wavfile

# -- Project root ----------------------------------------------------------------
_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))

from Tests.micro_beliefs.real_audio_stimuli import (
    SAMPLE_RATE, _render,
    PIANO, ORGAN, VIOLIN, STRINGS, TRUMPET, FLUTE, CELLO,
    major_triad, minor_triad, diminished_triad, dominant_seventh,
    chromatic_cluster, diatonic_scale, chromatic_scale,
    C2, C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5, A5, B5, C6,
)

OUT_DIR = _ROOT / "Test-Audio" / "micro_beliefs" / "f3"
ALL_METADATA: Dict[str, dict] = {}
_count = 0


# =====================================================================
# Save helper
# =====================================================================

def save(
    pm: pretty_midi.PrettyMIDI,
    group: str,
    name: str,
    meta: dict,
    gain: float = 1.0,
) -> pathlib.Path:
    """Save PrettyMIDI as .mid + rendered .wav, collect metadata."""
    global _count
    _count += 1

    d = OUT_DIR / group
    d.mkdir(parents=True, exist_ok=True)

    # Save MIDI
    mid_path = d / f"{name}.mid"
    pm.write(str(mid_path))

    # Render and save WAV
    has_notes = any(len(inst.notes) > 0 for inst in pm.instruments)
    if has_notes:
        waveform = _render(pm)
    else:
        n_samples = 5 * SAMPLE_RATE
        waveform = torch.zeros(1, n_samples)
    wav_path = d / f"{name}.wav"
    w = (waveform * gain).clamp(-1.0, 1.0).squeeze(0).numpy()
    int16 = (w * 32767).astype(np.int16)
    wavfile.write(str(wav_path), SAMPLE_RATE, int16)

    dur = len(w) / SAMPLE_RATE
    meta["duration_s"] = round(dur, 2)
    meta["filename"] = f"{group}/{name}"
    ALL_METADATA[f"{group}/{name}"] = meta
    print(f"  [{_count:02d}] {wav_path.relative_to(_ROOT)}  ({dur:.1f}s)")
    return wav_path


# =====================================================================
# PrettyMIDI builder helpers
# =====================================================================

def _pm_melody(
    notes: List[int],
    durs: List[float],
    program: int = PIANO,
    velocity: int = 80,
    gap: float = 0.02,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI from monophonic note list."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for p, d in zip(notes, durs):
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=p, start=t, end=t + d - gap,
        ))
        t += d
    pm.instruments.append(inst)
    return pm


def _pm_progression(
    chords: List[List[int]],
    durs: List[float],
    program: int = PIANO,
    velocity: int = 70,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI from chord list."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for chord, d in zip(chords, durs):
        for p in chord:
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=p, start=t, end=t + d,
            ))
        t += d
    pm.instruments.append(inst)
    return pm


def _pm_isochronous(
    pitch: int, bpm: float, n_beats: int,
    program: int = PIANO, velocity: int = 80,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI for isochronous (equally spaced) notes."""
    ioi = 60.0 / bpm
    dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_beats):
        t = i * ioi
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch, start=t, end=t + dur,
        ))
    pm.instruments.append(inst)
    return pm


def _pm_note(
    pitch: int, duration_s: float,
    program: int = PIANO, velocity: int = 80,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI for single sustained note."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    inst.notes.append(pretty_midi.Note(
        velocity=velocity, pitch=pitch, start=0.0, end=duration_s,
    ))
    pm.instruments.append(inst)
    return pm


def _pm_chord(
    notes: List[int], duration_s: float,
    program: int = PIANO, velocity: int = 80,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI for sustained chord."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for p in notes:
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=p, start=0.0, end=duration_s,
        ))
    pm.instruments.append(inst)
    return pm


def _pm_melody_with_chords(
    mel_notes, mel_durs, chd_notes, chd_durs,
    mel_prog=FLUTE, chd_prog=PIANO,
    mel_vel=90, chd_vel=60,
) -> pretty_midi.PrettyMIDI:
    """Melody over chord accompaniment."""
    pm = pretty_midi.PrettyMIDI()
    mi = pretty_midi.Instrument(program=mel_prog)
    t = 0.0
    for p, d in zip(mel_notes, mel_durs):
        mi.notes.append(pretty_midi.Note(
            velocity=mel_vel, pitch=p, start=t, end=t + d - 0.02,
        ))
        t += d
    pm.instruments.append(mi)
    ci = pretty_midi.Instrument(program=chd_prog)
    t = 0.0
    for chord, d in zip(chd_notes, chd_durs):
        for p in chord:
            ci.notes.append(pretty_midi.Note(
                velocity=chd_vel, pitch=p, start=t, end=t + d,
            ))
        t += d
    pm.instruments.append(ci)
    return pm


# =====================================================================
# Chord shorthands
# =====================================================================
Cmaj = major_triad(C3)
Fmaj = major_triad(F3)
Gmaj = major_triad(G3)
Am = minor_triad(A3)
G7 = dominant_seventh(G3)


# =====================================================================
# Category 1: Beat Entrainment (SNEM, 10 stimuli)
# Key: flux_period_H16, onset_period_H16, amp_mean_H16
# =====================================================================

def generate_snem_beat():
    """Category 1 — Beat entrainment (10 stimuli)."""
    print("\n=== CATEGORY 1: BEAT ENTRAINMENT (SNEM) ===")
    g = "snem"

    # 1.1  Isochronous @120BPM — perfect periodicity
    pm = _pm_isochronous(C4, 120, 20, PIANO, 80)
    save(pm, g, "01_isochronous_120bpm", {
        "description": "C4 piano @120BPM, 20 beats (10s). Perfect onset periodicity at 500ms IOI.",
        "tests": ["beat_entrainment", "beat_onset_pred"],
        "expected": {"beat_entrainment": "HIGH", "beat_onset_pred": "HIGH"},
        "science": "Nozaradan 2012: SS-EP at beat frequency (p<0.0001, N=9)",
    })

    # 1.2  Isochronous @60BPM — slower but regular
    pm = _pm_isochronous(C4, 60, 10, PIANO, 80)
    save(pm, g, "02_isochronous_60bpm", {
        "description": "C4 piano @60BPM, 10 beats (10s). Regular at H16 (1s) timescale.",
        "tests": ["beat_entrainment"],
        "expected": {"beat_entrainment": "HIGH"},
        "science": "Large & Palmer 2002: oscillator entrainment at 0.5-2s range",
    })

    # 1.3  Isochronous @180BPM — fast regular
    pm = _pm_isochronous(C4, 180, 30, PIANO, 80)
    save(pm, g, "03_isochronous_180bpm", {
        "description": "C4 piano @180BPM, 30 beats (10s). Fast regular at 333ms IOI.",
        "tests": ["beat_entrainment"],
        "expected": {"beat_entrainment": "HIGH"},
        "science": "Grahn & Brett 2007: beat perception valid 60-180 BPM",
    })

    # 1.4  Random timing — no periodicity
    rng = np.random.RandomState(42)
    n_notes = 20
    iois = rng.uniform(0.2, 1.0, size=n_notes).tolist()
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for ioi in iois:
        inst.notes.append(pretty_midi.Note(80, C4, t, t + ioi * 0.85))
        t += ioi
    pm.instruments.append(inst)
    save(pm, g, "04_random_timing", {
        "description": "C4 piano, random IOI 0.2-1.0s (seed=42), 20 notes. No periodicity.",
        "tests": ["beat_entrainment", "beat_onset_pred"],
        "expected": {"beat_entrainment": "LOW", "beat_onset_pred": "LOW"},
        "science": "No periodic structure destroys H16 periodicity morphology",
    })

    # 1.5  Syncopated @120BPM — offbeat accents
    # Standard offbeat pattern: beats on the AND (between main beats)
    ioi = 60.0 / 120.0  # 500ms
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for i in range(40):
        # Alternate: offbeat (weak) then main beat (strong accent)
        if i % 2 == 0:
            # Offbeat: soft
            inst.notes.append(pretty_midi.Note(50, C4, t, t + ioi * 0.4))
        else:
            # Main beat: normal
            inst.notes.append(pretty_midi.Note(90, C4, t, t + ioi * 0.4))
        t += ioi * 0.5
    pm.instruments.append(inst)
    save(pm, g, "05_syncopated_120bpm", {
        "description": "Syncopated C4 @120BPM: offbeat soft (v=50) + main strong (v=90). "
                       "10s. Disrupts clean periodicity.",
        "tests": ["beat_entrainment"],
        "expected": {"beat_entrainment": "MODERATE"},
        "science": "Syncopation partially disrupts onset periodicity at beat rate",
    })

    # 1.6  Polyrhythm 3:4 — competing periodicities
    dur_s = 10.0
    pm = pretty_midi.PrettyMIDI()
    # Voice 1: 3 beats per 2s (IOI=667ms)
    inst1 = pretty_midi.Instrument(program=PIANO)
    ioi_3 = 2.0 / 3.0
    t = 0.0
    while t < dur_s:
        inst1.notes.append(pretty_midi.Note(80, C4, t, t + 0.15))
        t += ioi_3
    pm.instruments.append(inst1)
    # Voice 2: 4 beats per 2s (IOI=500ms)
    inst2 = pretty_midi.Instrument(program=PIANO)
    ioi_4 = 2.0 / 4.0
    t = 0.0
    while t < dur_s:
        inst2.notes.append(pretty_midi.Note(80, E4, t, t + 0.15))
        t += ioi_4
    pm.instruments.append(inst2)
    save(pm, g, "06_polyrhythm_3v4", {
        "description": "Polyrhythm 3:4 (C4+E4), 10s. Two competing beat rates.",
        "tests": ["beat_entrainment"],
        "expected": {"beat_entrainment": "MODERATE"},
        "science": "Competing periodicities reduce single-rate entrainment strength",
    })

    # 1.7  Accented downbeats — clear metric accent pattern
    # 4/4 meter: accent every 4th beat (v=110 vs v=60)
    ioi = 60.0 / 120.0  # 500ms
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    for i in range(20):
        t = i * ioi
        v = 110 if i % 4 == 0 else 60
        inst.notes.append(pretty_midi.Note(v, C4, t, t + ioi * 0.85))
    pm.instruments.append(inst)
    save(pm, g, "07_accented_downbeat", {
        "description": "C4 @120BPM, accent every 4th beat (v=110 vs 60), 10s. "
                       "Clear beat + metric pattern.",
        "tests": ["beat_entrainment", "selective_gain"],
        "expected": {"beat_entrainment": "HIGH", "selective_gain": "HIGH"},
        "science": "Nozaradan 2012: metric accent enhances SS-EP at beat frequency",
    })

    # 1.8  Crescendo beat — growing salience
    ioi = 60.0 / 120.0
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    n = 20
    for i in range(n):
        t = i * ioi
        v = int(40 + (120 - 40) * i / (n - 1))
        inst.notes.append(pretty_midi.Note(v, C4, t, t + ioi * 0.85))
    pm.instruments.append(inst)
    save(pm, g, "08_crescendo_beat", {
        "description": "C4 @120BPM, velocity 40->120 over 10s. Beat with growing amplitude.",
        "tests": ["beat_entrainment"],
        "expected": {"beat_entrainment": "INCREASING"},
        "science": "Growing amplitude strengthens H16 amp_mean → stronger entrainment",
    })

    # 1.9  Sustained note — no onsets after initial
    pm = _pm_note(C4, 10.0, PIANO, 80)
    save(pm, g, "09_sustained_note", {
        "description": "C4 piano sustained 10s. Single onset, no repeated events.",
        "tests": ["beat_entrainment"],
        "expected": {"beat_entrainment": "VERY LOW"},
        "science": "No periodic onsets = zero flux/onset periodicity at H16",
    })

    # 1.10  Beat then random — transition
    ioi = 60.0 / 120.0
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # First 5s: regular @120BPM
    for i in range(10):
        t = i * ioi
        inst.notes.append(pretty_midi.Note(80, C4, t, t + ioi * 0.85))
    # Next 5s: random timing
    rng2 = np.random.RandomState(99)
    t = 5.0
    for _ in range(10):
        rand_ioi = rng2.uniform(0.2, 1.0)
        inst.notes.append(pretty_midi.Note(80, C4, t, t + rand_ioi * 0.85))
        t += rand_ioi
    pm.instruments.append(inst)
    save(pm, g, "10_beat_to_random", {
        "description": "C4 @120BPM for 5s, then random timing 5s. Transition stimulus.",
        "tests": ["beat_entrainment"],
        "expected": {"beat_entrainment": "HIGH first half, LOW second half"},
        "science": "Transition tests temporal tracking of entrainment dissolution",
    })


# =====================================================================
# Category 2: Meter Hierarchy (SNEM, 8 stimuli)
# Key: coupling_period_H16, coupling_period_H3, coupling_zc_H16
# =====================================================================

def generate_snem_meter():
    """Category 2 — Meter hierarchy (8 stimuli)."""
    print("\n=== CATEGORY 2: METER HIERARCHY (SNEM) ===")
    g = "snem"

    ioi = 60.0 / 120.0  # 500ms

    # 2.1  Strong 4/4 meter — accented downbeats
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    velocities_4_4 = [110, 60, 80, 60]
    for i in range(20):
        t = i * ioi
        v = velocities_4_4[i % 4]
        inst.notes.append(pretty_midi.Note(v, C4, t, t + ioi * 0.85))
    pm.instruments.append(inst)
    save(pm, g, "11_strong_4_4", {
        "description": "C4 @120BPM, 4/4 accents [110,60,80,60] x5, 10s. Strong metric hierarchy.",
        "tests": ["meter_hierarchy", "meter_position_pred"],
        "expected": {"meter_hierarchy": "HIGH", "meter_position_pred": "HIGH"},
        "science": "Grahn & Brett 2007: metric accent recruits SMA/BG (fMRI, N=27)",
    })

    # 2.2  Waltz 3/4 — ternary meter
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    velocities_3_4 = [110, 60, 60]
    for i in range(21):
        t = i * ioi
        v = velocities_3_4[i % 3]
        inst.notes.append(pretty_midi.Note(v, C4, t, t + ioi * 0.85))
    pm.instruments.append(inst)
    save(pm, g, "12_waltz_3_4", {
        "description": "C4 @120BPM, 3/4 accents [110,60,60] x7, ~10.5s. Waltz meter.",
        "tests": ["meter_hierarchy"],
        "expected": {"meter_hierarchy": "HIGH"},
        "science": "Ternary meter creates periodic coupling at 3-beat cycle",
    })

    # 2.3  Uniform beats — NO accent hierarchy
    pm = _pm_isochronous(C4, 120, 20, PIANO, 80)
    save(pm, g, "13_uniform_beats", {
        "description": "C4 @120BPM, all v=80, 10s. Beats but no metric accent hierarchy.",
        "tests": ["meter_hierarchy"],
        "expected": {"meter_hierarchy": "LOW (beats present but no hierarchy)"},
        "science": "Uniform velocity = no coupling periodicity at bar level",
    })

    # 2.4  Random accents — no periodic accent
    rng = np.random.RandomState(43)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    for i in range(20):
        t = i * ioi
        v = int(rng.randint(40, 121))
        inst.notes.append(pretty_midi.Note(v, C4, t, t + ioi * 0.85))
    pm.instruments.append(inst)
    save(pm, g, "14_random_accents", {
        "description": "C4 @120BPM, random velocity 40-120 per beat (seed=43), 10s.",
        "tests": ["meter_hierarchy"],
        "expected": {"meter_hierarchy": "LOW (random accents = no periodic hierarchy)"},
        "science": "Random velocity destroys coupling periodicity at any timescale",
    })

    # 2.5  Full musical 4/4 — melody + chords + accented downbeats
    mel = [C5, D5, E5, G5, E5, D5, C5, G4, C5, E5, G5, C6]
    mel_durs = [1.0] * 12
    chords = [Cmaj, Fmaj, Gmaj, Cmaj] * 3
    chd_durs = [1.0] * 12
    pm = _pm_melody_with_chords(mel, mel_durs, chords, chd_durs,
                                 mel_prog=FLUTE, chd_prog=PIANO,
                                 mel_vel=90, chd_vel=60)
    save(pm, g, "15_melody_chords_4_4", {
        "description": "Flute melody + piano I-IV-V-I chords, 12s. Rich metric context.",
        "tests": ["meter_hierarchy"],
        "expected": {"meter_hierarchy": "HIGH"},
        "science": "Melody+harmony provides multi-level metric cues",
    })

    # 2.6  Rapid uniform @480BPM — too fast for meter
    pm = _pm_isochronous(C4, 480, 40, PIANO, 80)
    save(pm, g, "16_rapid_uniform_480bpm", {
        "description": "C4 @480BPM, 40 beats (~5s). Too fast for metric grouping.",
        "tests": ["meter_hierarchy"],
        "expected": {"meter_hierarchy": "LOW (sub-beat rate, no grouping)"},
        "science": "125ms IOI is below beat-perception threshold (~200ms minimum)",
    })

    # 2.7  March 2/4 — strong binary meter
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    velocities_2_4 = [110, 60]
    for i in range(20):
        t = i * ioi
        v = velocities_2_4[i % 2]
        inst.notes.append(pretty_midi.Note(v, C4, t, t + ioi * 0.85))
    pm.instruments.append(inst)
    save(pm, g, "17_march_2_4", {
        "description": "C4 @120BPM, 2/4 accents [110,60] x10, 10s. Strong binary meter.",
        "tests": ["meter_hierarchy", "meter_position_pred"],
        "expected": {"meter_hierarchy": "HIGH", "meter_position_pred": "HIGH"},
        "science": "Binary accent = simplest periodic coupling pattern",
    })

    # 2.8  Irregular 7/8 — asymmetric grouping
    # 7/8 = 3+2+2 eighth-note groups at 120BPM eighth = 250ms
    eighth = 60.0 / 240.0  # 250ms per eighth
    groups_7_8 = [3, 2, 2]  # group sizes in eighths
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    beat_idx = 0
    while t < 10.0:
        for group_size in groups_7_8:
            for j in range(group_size):
                if t >= 10.0:
                    break
                v = 110 if j == 0 else 60  # accent on group start
                inst.notes.append(pretty_midi.Note(v, C4, t, t + eighth * 0.85))
                t += eighth
                beat_idx += 1
    pm.instruments.append(inst)
    save(pm, g, "18_irregular_7_8", {
        "description": "C4 in 7/8 (3+2+2), accent on group start, ~10s. Asymmetric meter.",
        "tests": ["meter_hierarchy"],
        "expected": {"meter_hierarchy": "MODERATE (asymmetric but still periodic)"},
        "science": "Irregular meter creates weaker coupling periodicity than binary/ternary",
    })


# =====================================================================
# Category 3: Attention Capture (IACM, 8 stimuli)
# Key: (1-tonalness), spectral_flatness, roughness_entropy
# =====================================================================

def generate_iacm_capture():
    """Category 3 — Attention capture (8 stimuli)."""
    print("\n=== CATEGORY 3: ATTENTION CAPTURE (IACM) ===")
    g = "iacm"

    # 3.1  Perfect fifth — highly tonal, consonant
    pm = _pm_chord([C4, G4], 8.0, PIANO, 80)
    save(pm, g, "01_pure_fifth", {
        "description": "C4+G4 (P5) piano sustained, 8s. High tonalness, high consonance.",
        "tests": ["attention_capture"],
        "expected": {"attention_capture": "LOW (high tonalness = low capture)"},
        "science": "Basinski 2025: harmonic stimuli produce minimal P3a (baseline)",
    })

    # 3.2  12-note chromatic cluster — dense, inharmonic
    pm = _pm_chord(chromatic_cluster(C4, 12), 8.0, PIANO, 80)
    save(pm, g, "02_chromatic_cluster_12", {
        "description": "12-note cluster C4-B4 sustained, 8s. Low tonalness, max roughness.",
        "tests": ["attention_capture"],
        "expected": {"attention_capture": "HIGH (low tonalness, high flatness)"},
        "science": "Basinski 2025: P3a d=-1.37 inharmonic vs harmonic; ORN OR=16.44",
    })

    # 3.3  Minor second — rough, dissonant
    pm = _pm_chord([C4, Db4], 8.0, PIANO, 80)
    save(pm, g, "03_minor_second", {
        "description": "C4+Db4 (m2) piano sustained, 8s. Strong beating, low tonalness.",
        "tests": ["attention_capture"],
        "expected": {"attention_capture": "MODERATE-HIGH"},
        "science": "Minor second produces strong roughness and reduced tonalness",
    })

    # 3.4  Tritone — dissonant but simpler than cluster
    pm = _pm_chord([C4, Gb4], 8.0, PIANO, 80)
    save(pm, g, "04_tritone", {
        "description": "C4+Gb4 (TT) piano sustained, 8s. Dissonant dyad.",
        "tests": ["attention_capture"],
        "expected": {"attention_capture": "MODERATE"},
        "science": "Tritone is dissonant but fewer partials than cluster",
    })

    # 3.5  Tonal to cluster transition
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # First 4s: C major chord
    for p in major_triad(C4):
        inst.notes.append(pretty_midi.Note(80, p, 0.0, 4.0))
    # Next 4s: 12-note cluster
    for p in chromatic_cluster(C4, 12):
        inst.notes.append(pretty_midi.Note(80, p, 4.0, 8.0))
    pm.instruments.append(inst)
    save(pm, g, "05_tonal_to_cluster", {
        "description": "C major chord 4s -> 12-note cluster 4s. Capture increases at transition.",
        "tests": ["attention_capture"],
        "expected": {"attention_capture": "LOW first half, HIGH second half"},
        "science": "Inharmonic onset within tonal context = maximal deviance capture",
    })

    # 3.6  Cluster to tonal resolution
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # First 4s: 12-note cluster
    for p in chromatic_cluster(C4, 12):
        inst.notes.append(pretty_midi.Note(80, p, 0.0, 4.0))
    # Next 4s: C major chord
    for p in major_triad(C4):
        inst.notes.append(pretty_midi.Note(80, p, 4.0, 8.0))
    pm.instruments.append(inst)
    save(pm, g, "06_cluster_to_tonal", {
        "description": "12-note cluster 4s -> C major chord 4s. Capture decreases at resolution.",
        "tests": ["attention_capture"],
        "expected": {"attention_capture": "HIGH first half, LOW second half"},
        "science": "Resolution from inharmonic to tonal reduces capture",
    })

    # 3.7  Single C4 — maximally tonal baseline
    pm = _pm_note(C4, 8.0, PIANO, 80)
    save(pm, g, "07_single_piano_c4", {
        "description": "C4 piano sustained, 8s. Single pure tone, maximum tonalness.",
        "tests": ["attention_capture", "attention_shift_pred"],
        "expected": {"attention_capture": "VERY LOW", "attention_shift_pred": "VERY LOW"},
        "science": "Single harmonic tone = baseline tonalness, zero inharmonic capture",
    })

    # 3.8  Wide cluster in low register
    pm = _pm_chord(chromatic_cluster(C3, 12), 8.0, PIANO, 80)
    save(pm, g, "08_wide_cluster_c3", {
        "description": "12-note cluster C3-B3 sustained, 8s. Dense low register.",
        "tests": ["attention_capture"],
        "expected": {"attention_capture": "HIGH"},
        "science": "Low-register clusters have even lower tonalness (dense harmonics)",
    })


# =====================================================================
# Category 4: Object Segregation & Precision (IACM, 6 stimuli)
# Segregation: inharmonicity val/std, coupling, tonalness_period
# Precision: tonalness_period_H3, tonalness_period_H16, coupling_zc
# =====================================================================

def generate_iacm_segregation():
    """Category 4 — Object segregation & precision weighting (6 stimuli)."""
    print("\n=== CATEGORY 4: OBJECT SEGREGATION & PRECISION (IACM) ===")
    g = "iacm"

    # 4.1  Single piano melody — one stream
    mel = [C4, D4, E4, F4, G4, A4, B4, C5, B4, A4, G4, F4, E4, D4, C4]
    durs = [0.67] * 15  # ~10s total
    pm = _pm_melody(mel, durs, PIANO, 80)
    save(pm, g, "09_single_piano_melody", {
        "description": "C major scale up-down, piano only, 10s. Single auditory stream.",
        "tests": ["object_segregation"],
        "expected": {"object_segregation": "LOW (single stream)"},
        "science": "Single instrument = no stream segregation cues",
    })

    # 4.2  Piano + flute duet — two alternating streams
    pm = pretty_midi.PrettyMIDI()
    mel_notes = [C4, D4, E4, F4, G4, A4, B4, C5, B4, A4, G4, F4, E4, D4, C4]
    ioi = 0.67
    # Piano plays odd notes
    inst_p = pretty_midi.Instrument(program=PIANO)
    # Flute plays even notes
    inst_f = pretty_midi.Instrument(program=FLUTE)
    for i, p in enumerate(mel_notes):
        t = i * ioi
        if i % 2 == 0:
            inst_p.notes.append(pretty_midi.Note(80, p, t, t + ioi - 0.02))
        else:
            inst_f.notes.append(pretty_midi.Note(80, p, t, t + ioi - 0.02))
    pm.instruments.append(inst_p)
    pm.instruments.append(inst_f)
    save(pm, g, "10_piano_flute_duet", {
        "description": "Piano + flute alternating notes of C major scale, 10s. Two timbral streams.",
        "tests": ["object_segregation"],
        "expected": {"object_segregation": "HIGH (two timbres alternate)"},
        "science": "Alain 2007: ORN indexes concurrent sound segregation",
    })

    # 4.3  Three instruments interleaved
    pm = pretty_midi.PrettyMIDI()
    mel_notes = [C4, D4, E4, F4, G4, A4, B4, C5, B4, A4, G4, F4, E4, D4, C4]
    ioi = 0.67
    inst_p = pretty_midi.Instrument(program=PIANO)
    inst_f = pretty_midi.Instrument(program=FLUTE)
    inst_t = pretty_midi.Instrument(program=TRUMPET)
    instruments = [inst_p, inst_f, inst_t]
    for i, p in enumerate(mel_notes):
        t = i * ioi
        instruments[i % 3].notes.append(pretty_midi.Note(80, p, t, t + ioi - 0.02))
    pm.instruments.append(inst_p)
    pm.instruments.append(inst_f)
    pm.instruments.append(inst_t)
    save(pm, g, "11_three_instrument", {
        "description": "Piano+flute+trumpet interleaved notes, C major scale, 10s. Three streams.",
        "tests": ["object_segregation"],
        "expected": {"object_segregation": "VERY HIGH (three timbres)"},
        "science": "More streams = higher inharmonicity variability + tonalness periodicity",
    })

    # 4.4  Stable diatonic melody — high precision context
    mel = [C4, D4, E4, F4, G4, F4, E4, D4, C4, D4, E4, F4, G4, F4, E4, D4, C4, C4, C4, C4]
    durs = [0.5] * 20  # 10s
    pm = _pm_melody(mel, durs, PIANO, 80)
    save(pm, g, "12_stable_diatonic", {
        "description": "Diatonic C major melody, steady 0.5s IOI, piano, 10s. Stable tonal context.",
        "tests": ["precision_weighting"],
        "expected": {"precision_weighting": "HIGH (stable tonalness periodicity)"},
        "science": "Friston 2005: stable context = high precision weighting",
    })

    # 4.5  Chromatic wandering — unstable context
    rng = np.random.RandomState(44)
    pitches = [int(rng.randint(48, 84)) for _ in range(20)]
    iois_rand = rng.uniform(0.3, 0.7, size=20).tolist()
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for p, ioi_r in zip(pitches, iois_rand):
        inst.notes.append(pretty_midi.Note(80, p, t, t + ioi_r * 0.85))
        t += ioi_r
    pm.instruments.append(inst)
    save(pm, g, "13_chromatic_wandering", {
        "description": "Random chromatic pitches C3-B5, varied IOI 0.3-0.7s (seed=44), 10s.",
        "tests": ["precision_weighting"],
        "expected": {"precision_weighting": "LOW (unstable tonalness)"},
        "science": "Unpredictable context destroys tonalness periodicity",
    })

    # 4.6  Stable to unstable transition
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # First 5s: stable diatonic (C major ascending/descending)
    mel_stable = [C4, D4, E4, F4, G4, F4, E4, D4, C4, D4]
    t = 0.0
    for p in mel_stable:
        inst.notes.append(pretty_midi.Note(80, p, t, t + 0.48))
        t += 0.5
    # Next 5s: chromatic wandering
    rng2 = np.random.RandomState(45)
    for _ in range(10):
        p = int(rng2.randint(48, 84))
        ioi_r = rng2.uniform(0.3, 0.7)
        inst.notes.append(pretty_midi.Note(80, p, t, t + ioi_r * 0.85))
        t += ioi_r
    pm.instruments.append(inst)
    save(pm, g, "14_stable_to_unstable", {
        "description": "Diatonic C major 5s -> random chromatic 5s. Precision transition.",
        "tests": ["precision_weighting"],
        "expected": {"precision_weighting": "HIGH first half -> LOW second half"},
        "science": "Context stability directly drives precision weighting",
    })


# =====================================================================
# Category 5: Salience Network (CSG, 8 stimuli)
# E0: wsig(0.40*(1-pleas) + 0.35*roughness + 0.25*loud_entropy)
# P1: tanh(0.50*E2 + 0.30*(pleas-roughness) + 0.20*flux_vel)
# P2: wsig(0.30*ambiguity + ...)
# =====================================================================

def generate_csg_salience():
    """Category 5 — Salience network, valence, load (8 stimuli)."""
    print("\n=== CATEGORY 5: SALIENCE NETWORK (CSG) ===")
    g = "csg"

    # 5.1  Harsh cluster — max dissonance → high salience
    pm = _pm_chord(chromatic_cluster(C4, 12), 8.0, PIANO, 100)
    save(pm, g, "01_harsh_cluster", {
        "description": "12-note cluster C4-B4, f (v=100), 8s. Maximum dissonance.",
        "tests": ["salience_network_activation"],
        "expected": {"salience_network_activation": "HIGH (max dissonance drives ACC/AI)"},
        "science": "Bravo 2017: salience from dissonance d=5.16",
    })

    # 5.2  Pure major chord — consonant → low salience
    pm = _pm_chord(major_triad(C4), 8.0, PIANO, 70)
    save(pm, g, "02_pure_major_chord", {
        "description": "C major triad, mf (v=70), 8s. Consonant, low roughness.",
        "tests": ["salience_network_activation"],
        "expected": {"salience_network_activation": "LOW (consonant = low salience)"},
        "science": "Consonant intervals produce minimal ACC/AI activation",
    })

    # 5.3  Consonant interval sequence → positive valence
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    intervals = [
        [C4, G4],       # P5
        [C4, F4],       # P4
        [C4, E4],       # M3
        [C4, A4],       # M6
    ]
    for i, chord in enumerate(intervals):
        t = i * 2.0
        for p in chord:
            inst.notes.append(pretty_midi.Note(70, p, t, t + 2.0))
    pm.instruments.append(inst)
    save(pm, g, "03_consonant_intervals", {
        "description": "P5->P4->M3->M6 sequence, 2s each, 8s. All consonant intervals.",
        "tests": ["consonance_valence_mapping"],
        "expected": {"consonance_valence_mapping": "POSITIVE (>0, consonant=pleasant)"},
        "science": "Bravo 2017: consonance-valence linear relationship d=3.31",
    })

    # 5.4  Dissonant interval sequence → negative valence
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    intervals = [
        [C4, Db4],      # m2
        [C4, Gb4],      # TT
        [C4, Bb4],      # m7
        [C4, Db4],      # m2
    ]
    for i, chord in enumerate(intervals):
        t = i * 2.0
        for p in chord:
            inst.notes.append(pretty_midi.Note(70, p, t, t + 2.0))
    pm.instruments.append(inst)
    save(pm, g, "04_dissonant_intervals", {
        "description": "m2->TT->m7->m2 sequence, 2s each, 8s. All dissonant intervals.",
        "tests": ["consonance_valence_mapping"],
        "expected": {"consonance_valence_mapping": "NEGATIVE (<0, dissonant=unpleasant)"},
        "science": "Bravo 2017: dissonance maps to negative valence",
    })

    # 5.5  Tritone — ambiguous consonance → peak load
    # Tritone is maximally ambiguous (consonance ≈ 0.5)
    pm = _pm_chord([C4, Gb4], 8.0, PIANO, 70)
    save(pm, g, "05_ambiguous_tritone", {
        "description": "C4+Gb4 tritone sustained, 8s. Ambiguous consonance (≈0.5).",
        "tests": ["sensory_load"],
        "expected": {"sensory_load": "HIGH (inverted-U peak at ambiguity)"},
        "science": "Bravo 2017: intermediate dissonance -> max HG load d=1.9",
    })

    # 5.6  Clear consonance — P5 → low load
    pm = _pm_chord([C4, G4], 8.0, PIANO, 70)
    save(pm, g, "06_clear_consonance", {
        "description": "C4+G4 P5 sustained, 8s. Clear consonance.",
        "tests": ["sensory_load"],
        "expected": {"sensory_load": "LOW (consonance ≈ 0.85, no ambiguity)"},
        "science": "Clear categorization = minimal processing demand",
    })

    # 5.7  Clear dissonance — m2 → low load
    pm = _pm_chord([C4, Db4], 8.0, PIANO, 70)
    save(pm, g, "07_clear_dissonance", {
        "description": "C4+Db4 m2 sustained, 8s. Clear dissonance.",
        "tests": ["sensory_load"],
        "expected": {"sensory_load": "LOW (consonance ≈ 0.15, clearly dissonant)"},
        "science": "Clear dissonance also has low ambiguity = low load",
    })

    # 5.8  Dissonant to consonant trajectory
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # First 5s: 12-note cluster
    for p in chromatic_cluster(C4, 12):
        inst.notes.append(pretty_midi.Note(80, p, 0.0, 5.0))
    # Next 5s: C major chord
    for p in major_triad(C4):
        inst.notes.append(pretty_midi.Note(80, p, 5.0, 10.0))
    pm.instruments.append(inst)
    save(pm, g, "08_dissonant_to_consonant", {
        "description": "12-note cluster 5s -> C major chord 5s. Salience trajectory HIGH->LOW.",
        "tests": ["salience_network_activation"],
        "expected": {"salience_network_activation": "HIGH first half, LOW second half"},
        "science": "Dissonance resolution reduces salience network activation",
    })


# =====================================================================
# Category 6: Aesthetic Engagement (AACM, 7 stimuli)
# E0: sigma(0.35*stumpf + 0.30*(1-roughness) + 0.20*loudness + 0.15*coupling)
# E2: sigma(0.35*stumpf_vel + 0.35*coupling_mean + 0.30*stumpf_period)
# =====================================================================

def generate_aacm_aesthetic():
    """Category 6 — Aesthetic engagement & savoring (7 stimuli)."""
    print("\n=== CATEGORY 6: AESTHETIC ENGAGEMENT (AACM) ===")
    g = "aacm"

    # 6.1  Beautiful melody with chords — high engagement + savoring
    mel = [E5, G5, C6, B5, A5, G5, F5, E5, D5, C5, D5, E5]
    mel_durs = [0.75, 0.75, 1.0, 0.5, 0.5, 0.75, 0.75, 0.5, 0.75, 0.75, 1.0, 1.0]
    chords = [Cmaj, Am, Fmaj, Gmaj, Cmaj, Fmaj, Gmaj, Cmaj]
    chd_durs = [1.25, 1.25, 1.0, 1.0, 1.25, 1.25, 1.0, 1.0]
    pm = _pm_melody_with_chords(mel, mel_durs, chords, chd_durs,
                                 mel_prog=FLUTE, chd_prog=PIANO,
                                 mel_vel=85, chd_vel=55)
    save(pm, g, "01_beautiful_melody", {
        "description": "Flute melody + piano I-vi-IV-V-I chords, ~10s. Consonant, dynamic.",
        "tests": ["aesthetic_engagement", "savoring_effect"],
        "expected": {"aesthetic_engagement": "HIGH", "savoring_effect": "HIGH"},
        "science": "Sarasso 2019: consonance engagement d=2.008; Brattico 2013: vmPFC liked",
    })

    # 6.2  Harsh repeated cluster — low engagement
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    cluster = chromatic_cluster(C4, 8)
    for i in range(6):
        t = i * 1.0
        for p in cluster:
            inst.notes.append(pretty_midi.Note(100, p, t, t + 0.3))
    pm.instruments.append(inst)
    save(pm, g, "02_harsh_repeated_cluster", {
        "description": "8-note cluster sfz x6 at 1s intervals, 6s. Harsh, dissonant.",
        "tests": ["aesthetic_engagement"],
        "expected": {"aesthetic_engagement": "LOW (dissonant, high roughness)"},
        "science": "Sarasso 2019: dissonant intervals reduce N1/P2 engagement",
    })

    # 6.3  Consonant P5 sustained — high engagement
    pm = _pm_chord([C4, G4], 8.0, PIANO, 70)
    save(pm, g, "03_consonant_p5_sustained", {
        "description": "C4+G4 P5 piano sustained, mf, 8s. Maximally consonant interval.",
        "tests": ["aesthetic_engagement"],
        "expected": {"aesthetic_engagement": "HIGH (high stumpf_fusion, low roughness)"},
        "science": "Sarasso 2019: consonant intervals enhance aesthetic attention",
    })

    # 6.4  Dissonant m2 sustained — low engagement
    pm = _pm_chord([C4, Db4], 8.0, PIANO, 70)
    save(pm, g, "04_dissonant_m2_sustained", {
        "description": "C4+Db4 m2 piano sustained, mf, 8s. Maximally dissonant dyad.",
        "tests": ["aesthetic_engagement"],
        "expected": {"aesthetic_engagement": "LOW (low stumpf_fusion, high roughness)"},
        "science": "Sarasso 2019: dissonant intervals reduce aesthetic engagement",
    })

    # 6.5  Gentle cadence — high savoring
    pm = _pm_progression([Cmaj, Fmaj, Gmaj, Cmaj] * 3, [1.0] * 12, ORGAN, 65)
    save(pm, g, "05_gentle_cadence", {
        "description": "Slow I-IV-V-I x3, organ mf, 12s. Sustained pleasant dynamics.",
        "tests": ["savoring_effect"],
        "expected": {"savoring_effect": "HIGH (pleasant dynamics + coupling)"},
        "science": "Brattico 2013: sustained vmPFC activation during liked passages",
    })

    # 6.6  Rapid chromatic — low savoring
    rng = np.random.RandomState(46)
    pitches = [int(rng.randint(48, 84)) for _ in range(32)]
    pm = _pm_melody(pitches, [0.25] * 32, PIANO, 90)
    save(pm, g, "06_rapid_chromatic", {
        "description": "Random chromatic pitches, 4/s staccato, 8s. No pleasant dynamics.",
        "tests": ["savoring_effect"],
        "expected": {"savoring_effect": "LOW (no sustained pleasantness)"},
        "science": "Rapid chromatic = no sustained stumpf_fusion or coupling",
    })

    # 6.7  Crescendo consonant chord — increasing engagement
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # C major chord with increasing velocity: 8 segments of 1.25s
    for i in range(8):
        v = int(30 + (100 - 30) * i / 7)
        t = i * 1.25
        for p in major_triad(C4):
            inst.notes.append(pretty_midi.Note(v, p, t, t + 1.25))
    pm.instruments.append(inst)
    save(pm, g, "07_crescendo_consonant", {
        "description": "C major chord, velocity 30->100 in 8 steps over 10s. Growing engagement.",
        "tests": ["aesthetic_engagement"],
        "expected": {"aesthetic_engagement": "INCREASING (growing loudness + consonance)"},
        "science": "Louder consonant = stronger E0 (loudness term in AACM extraction)",
    })


# =====================================================================
# Category 7: Cross-Mechanism Integration (8 stimuli)
# =====================================================================

def generate_cross():
    """Category 7 — Cross-mechanism integration (8 stimuli)."""
    print("\n=== CATEGORY 7: CROSS-MECHANISM INTEGRATION ===")
    g = "cross"

    # 7.1  Full musical piece — all beliefs reference
    mel = [C5, E5, G5, C6, G5, E5, D5, F5, A5, G5, F5, E5, D5, C5]
    mel_durs = [0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 1.0, 0.5, 0.5, 0.5, 1.0]
    chords = [Cmaj, Am, Fmaj, Gmaj, Am, Fmaj, Gmaj, Cmaj]
    chd_durs = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.5, 1.5]
    pm = _pm_melody_with_chords(mel, mel_durs, chords, chd_durs,
                                 mel_prog=FLUTE, chd_prog=PIANO,
                                 mel_vel=85, chd_vel=55)
    save(pm, g, "01_full_musical", {
        "description": "Flute melody + piano chords, diatonic I-vi-IV-V, ~10s. Full reference.",
        "tests": ["all 15 beliefs"],
        "expected": "All mechanisms engaged: beat, meter, consonance salience, aesthetic",
        "science": "Comprehensive: beat+meter+consonance+aesthetic all present",
    })

    # 7.2  Beat + consonant — synergy
    chords_beat = [Cmaj, Fmaj, Gmaj, Cmaj] * 3
    durs_beat = [1.0] * 12
    pm = _pm_progression(chords_beat, durs_beat, PIANO, 70)
    save(pm, g, "02_beat_consonant", {
        "description": "I-IV-V-I chords at 1s intervals (=@60BPM), 12s. Beat + consonance.",
        "tests": ["beat_entrainment", "aesthetic_engagement"],
        "expected": {"beat_entrainment": "HIGH", "aesthetic_engagement": "HIGH"},
        "science": "Regular consonant events produce both entrainment and aesthetic engagement",
    })

    # 7.3  Beat + dissonant — beat with capture
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # Chromatic clusters at regular 1s intervals
    for i in range(12):
        t = i * 1.0
        for p in chromatic_cluster(C4, 6):
            inst.notes.append(pretty_midi.Note(80, p, t, t + 0.8))
    pm.instruments.append(inst)
    save(pm, g, "03_beat_dissonant", {
        "description": "6-note clusters at 1s intervals, 12s. Regular beat but dissonant content.",
        "tests": ["beat_entrainment", "attention_capture"],
        "expected": {"beat_entrainment": "HIGH", "attention_capture": "HIGH"},
        "science": "Beat periodicity maintained despite dissonant content",
    })

    # 7.4  No beat + consonant — sustained chord
    pm = _pm_chord(major_triad(C4), 10.0, PIANO, 70)
    save(pm, g, "04_no_beat_consonant", {
        "description": "C major chord sustained, no onsets, 10s. Consonant but no beat.",
        "tests": ["beat_entrainment", "aesthetic_engagement"],
        "expected": {"beat_entrainment": "LOW", "aesthetic_engagement": "HIGH"},
        "science": "Dissociation: consonance without temporal structure",
    })

    # 7.5  No beat + dissonant — sustained cluster
    pm = _pm_chord(chromatic_cluster(C4, 12), 8.0, PIANO, 80)
    save(pm, g, "05_no_beat_dissonant", {
        "description": "12-note cluster C4 sustained, no onsets, 8s. Dissonant, no beat.",
        "tests": ["beat_entrainment", "attention_capture"],
        "expected": {"beat_entrainment": "LOW", "attention_capture": "HIGH"},
        "science": "Dissociation: inharmonic capture without temporal structure",
    })

    # 7.6  Multi-instrument rhythm — segregation + beat
    ioi = 60.0 / 120.0  # 500ms
    pm = pretty_midi.PrettyMIDI()
    inst_p = pretty_midi.Instrument(program=PIANO)
    inst_f = pretty_midi.Instrument(program=FLUTE)
    inst_t = pretty_midi.Instrument(program=TRUMPET)
    instruments = [inst_p, inst_f, inst_t]
    for i in range(24):
        t = i * ioi
        instruments[i % 3].notes.append(
            pretty_midi.Note(80, C4, t, t + ioi * 0.85)
        )
    pm.instruments.append(inst_p)
    pm.instruments.append(inst_f)
    pm.instruments.append(inst_t)
    save(pm, g, "06_multi_instr_rhythm", {
        "description": "Piano+flute+trumpet alternating C4 @120BPM, 12s. 3 streams + beat.",
        "tests": ["object_segregation", "beat_entrainment"],
        "expected": {"object_segregation": "HIGH", "beat_entrainment": "HIGH"},
        "science": "Three timbres with regular timing: dual test of segregation + entrainment",
    })

    # 7.7  Stable → deviant → stable
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # Phase 1 (0-6s): P5 sustained
    inst.notes.append(pretty_midi.Note(70, C4, 0.0, 6.0))
    inst.notes.append(pretty_midi.Note(70, G4, 0.0, 6.0))
    # Phase 2 (6-9s): sudden 12-note cluster
    for p in chromatic_cluster(C4, 12):
        inst.notes.append(pretty_midi.Note(100, p, 6.0, 9.0))
    # Phase 3 (9-12s): back to P5
    inst.notes.append(pretty_midi.Note(70, C4, 9.0, 12.0))
    inst.notes.append(pretty_midi.Note(70, G4, 9.0, 12.0))
    pm.instruments.append(inst)
    save(pm, g, "07_stable_then_deviant", {
        "description": "P5 (6s) -> cluster (3s) -> P5 (3s), 12s. Precision drop + capture spike.",
        "tests": ["precision_weighting", "attention_capture"],
        "expected": {
            "precision_weighting": "HIGH -> DROP at cluster -> partial recovery",
            "attention_capture": "LOW -> SPIKE at cluster -> LOW",
        },
        "science": "Contextual deviance maximizes precision error and attention capture",
    })

    # 7.8  All-stressed orchestral — stress test
    pm = pretty_midi.PrettyMIDI()
    # Flute melody (accented)
    inst_f = pretty_midi.Instrument(program=FLUTE)
    mel = [C5, D5, E5, G5, A5, G5, E5, D5, C5, E5, G5, C6]
    t = 0.0
    for i, p in enumerate(mel):
        d = 1.0 if i < 8 else 1.5
        inst_f.notes.append(pretty_midi.Note(90, p, t, t + d - 0.02))
        t += d
    pm.instruments.append(inst_f)
    # Piano chords with accented downbeats (modulating C -> G)
    prog_chords = [
        Cmaj, Fmaj, Gmaj, Am,
        major_triad(G3), major_triad(C4), major_triad(D3), major_triad(G3),
    ]
    inst_p = pretty_midi.Instrument(program=PIANO)
    for i, chord in enumerate(prog_chords):
        s = i * 1.5
        v = 80 if i % 4 == 0 else 55
        for p in chord:
            inst_p.notes.append(pretty_midi.Note(v, p, s, s + 1.5))
    pm.instruments.append(inst_p)
    # Trumpet interjections (ff)
    inst_t = pretty_midi.Instrument(program=TRUMPET)
    for bar in [4, 6]:
        s = bar * 1.5
        inst_t.notes.append(pretty_midi.Note(120, G5, s, s + 0.3))
        inst_t.notes.append(pretty_midi.Note(120, C6, s + 0.4, s + 0.7))
    pm.instruments.append(inst_t)
    save(pm, g, "08_all_stressed", {
        "description": "Orchestral: flute + piano (C->G modulation) + trumpet ff, ~15s.",
        "tests": ["all 15 beliefs"],
        "expected": "All mechanisms engaged: multiple instruments, metric accents, modulation.",
        "science": "Stress test: beat+meter+segregation+salience+aesthetic simultaneously",
    })


# =====================================================================
# Category 8: Boundary Conditions (5 stimuli)
# =====================================================================

def generate_boundary():
    """Category 8 — Boundary conditions (5 stimuli)."""
    print("\n=== CATEGORY 8: BOUNDARY CONDITIONS ===")
    g = "boundary"

    # 8.1  Silence
    pm = pretty_midi.PrettyMIDI()
    pm.instruments.append(pretty_midi.Instrument(program=PIANO))
    save(pm, g, "01_silence", {
        "description": "Pure silence (empty MIDI). All beliefs should return near baseline.",
        "tests": ["all"],
        "expected": "All Core beliefs converge toward baseline (~0.5). No NaN/Inf.",
        "science": "Boundary: zero input must produce valid output",
    })

    # 8.2  Single note sustained
    pm = _pm_note(C4, 5.0, PIANO, 80)
    save(pm, g, "02_single_note", {
        "description": "Single C4 piano note, 5s sustained.",
        "tests": ["beat_entrainment", "attention_capture"],
        "expected": {
            "beat_entrainment": "LOW (single onset, no periodicity)",
            "attention_capture": "LOW (high tonalness, single tone)",
        },
        "science": "Boundary: minimal input, single onset event",
    })

    # 8.3  Extreme fast tempo (600 BPM = 10 notes/s)
    pm = _pm_isochronous(C4, 600, 50, PIANO, 80)
    save(pm, g, "03_extreme_fast", {
        "description": "C4 at 600 BPM (10 notes/sec), 50 beats (~5s). Near temporal fusion.",
        "tests": ["beat_entrainment"],
        "expected": {"beat_entrainment": "LOW (100ms IOI below beat perception threshold)"},
        "science": "Boundary: too fast for beat entrainment (H16 periodicity absent)",
    })

    # 8.4  Extreme slow tempo (20 BPM = 1 note every 3s)
    pm = _pm_isochronous(C4, 20, 5, PIANO, 80)
    save(pm, g, "04_extreme_slow", {
        "description": "C4 at 20 BPM, 5 notes over 15s. Very sparse events.",
        "tests": ["beat_entrainment"],
        "expected": {"beat_entrainment": "LOW (3s IOI exceeds entrainment range)"},
        "science": "Boundary: too slow for beat tracking (~2s upper limit)",
    })

    # 8.5  Full chromatic cluster sustained
    pm = _pm_chord(chromatic_scale(C4, 12), 5.0, PIANO, 60)
    save(pm, g, "05_full_cluster", {
        "description": "All 12 notes C4-B4 sustained, 5s. Maximum spectral complexity.",
        "tests": ["attention_capture", "beat_entrainment"],
        "expected": {
            "attention_capture": "HIGH (max inharmonicity)",
            "beat_entrainment": "LOW (no periodic onsets)",
        },
        "science": "Boundary: maximum spectral complexity, zero temporal structure",
    })


# =====================================================================
# Metadata & Catalog Writers
# =====================================================================

def write_metadata():
    """Write metadata.json with ground truth for all stimuli."""
    path = OUT_DIR / "metadata.json"
    with open(path, "w") as f:
        json.dump(ALL_METADATA, f, indent=2, ensure_ascii=False)
    print(f"\n  metadata.json -> {path.relative_to(_ROOT)}")


def write_catalog():
    """Write STIMULUS-CATALOG.md summarizing all stimuli."""
    path = OUT_DIR / "STIMULUS-CATALOG.md"
    lines = [
        "# F3 Test Audio Stimulus Catalog",
        "",
        f"**Total stimuli**: {_count}",
        "**Mechanisms tested**: SNEM, IACM, CSG, AACM (15 beliefs)",
        "",
        "## Ordinal Comparisons (Ground Truth)",
        "",
        "| # | A | B | Belief | Expected | Rationale |",
        "|---|---|---|--------|----------|-----------|",
        "| 1 | snem/01 iso_120 | snem/04 random | beat_entrainment | A>B | Nozaradan 2012: regular>irregular |",
        "| 2 | snem/01 iso_120 | snem/09 sustained | beat_entrainment | A>B | Repeated onsets > no onsets |",
        "| 3 | snem/08 crescendo | snem/04 random | beat_entrainment | A>B | Regular tempo + dynamics > aperiodic |",
        "| 4 | snem/07 accented | snem/04 random | selective_gain | A>B | Metric accent x beat > no structure |",
        "| 5 | snem/01 iso_120 | snem/04 random | beat_onset_pred | A>B | Periodicity enables prediction |",
        "| 6 | snem/11 strong_4_4 | snem/13 uniform | meter_hierarchy | A>B | Grahn 2007: accent > uniform |",
        "| 7 | snem/12 waltz_3_4 | snem/13 uniform | meter_hierarchy | A>B | Ternary accent > uniform |",
        "| 8 | snem/11 strong_4_4 | snem/14 random_acc | meter_hierarchy | A>B | Periodic > random accent |",
        "| 9 | snem/15 melody_chords | snem/09 sustained | meter_hierarchy | A>B | Metric music > no onsets |",
        "| 10 | snem/17 march | snem/14 random_acc | meter_position_pred | A>B | Binary pattern > random |",
        "| 11 | iacm/02 cluster | iacm/01 P5 | attention_capture | A>B | Basinski 2025 P3a |",
        "| 12 | iacm/02 cluster | iacm/07 single | attention_capture | A>B | Inharmonic > tonal |",
        "| 13 | iacm/03 m2 | iacm/01 P5 | attention_capture | A>B | Dissonant > consonant |",
        "| 14 | iacm/08 low_cluster | iacm/07 single | attention_capture | A>B | Cluster > pure tone |",
        "| 15 | iacm/02 cluster | iacm/07 single | attention_shift_pred | A>B | E0+P0 driven |",
        "| 16 | iacm/10 duet | iacm/09 solo | object_segregation | A>B | Alain 2007 ORN |",
        "| 17 | iacm/11 trio | iacm/09 solo | object_segregation | A>B | More streams > single |",
        "| 18 | iacm/07 single_c4 | iacm/13 chromatic | precision_weighting | A>B | Friston 2005: max stable > unstable |",
        "| 19 | csg/01 cluster | csg/02 major | salience_network_activation | A>B | Bravo 2017 d=5.16 |",
        "| 20 | csg/03 consonant | csg/04 dissonant | consonance_valence_mapping | A>B | Bravo 2017 d=3.31 |",
        "| 21 | csg/05 tritone | csg/06 P5 | sensory_load | A>B | Inverted-U: ambiguous > clear consonance |",
        "| 22 | csg/01 harsh_cluster | boundary/02 single | sensory_load | A>B | Dense cluster > single tone load |",
        "| 23 | aacm/01 beautiful | aacm/02 harsh | aesthetic_engagement | A>B | Sarasso 2019 d=2.008 |",
        "| 24 | aacm/03 P5 | aacm/04 m2 | aesthetic_engagement | A>B | Sarasso 2019: consonant > dissonant |",
        "| 25 | aacm/05 cadence | aacm/06 chromatic | savoring_effect | A>B | Brattico 2013: pleasant > random |",
        "| 26 | aacm/01 beautiful | aacm/06 chromatic | savoring_effect | A>B | Pleasant dynamics > random |",
        "| 27 | cross/01 full | boundary/01 silence | beat_entrainment | A>B | Music > silence |",
        "| 28 | cross/01 full | boundary/01 silence | meter_hierarchy | A>B | Music > silence |",
        "| 29 | cross/02 beat_cons | cross/04 no_beat_cons | beat_entrainment | A>B | Beat present > no beat (consonance held) |",
        "| 30 | cross/03 beat_diss | cross/04 no_beat_cons | beat_entrainment | A>B | Beat > no-beat |",
        "| 31 | cross/04 no_beat_cons | cross/05 no_beat_diss | aesthetic_engagement | A>B | Consonant > dissonant |",
        "| 32 | cross/05 no_beat_diss | cross/04 no_beat_cons | attention_capture | A>B | Cluster > chord |",
        "| 33 | cross/06 multi_instr | iacm/09 solo | object_segregation | A>B | 3 instruments > 1 |",
        "| 34 | snem/01 iso_120 | snem/06 polyrhythm | beat_entrainment | A>B | Single beat > competing beats |",
        "| 35 | snem/01 iso_120 | boundary/04 extreme_slow | beat_entrainment | A>B | 120 BPM > 20 BPM |",
        "| 36 | boundary/05 cluster | boundary/02 single | attention_capture | A>B | 12 notes > 1 note |",
        "| 37 | csg/03 cons_intervals | csg/04 diss_intervals | aesthetic_engagement | A>B | Consonant > dissonant (Sarasso 2019) |",
        "| 38 | snem/11 strong_4_4 | snem/09 sustained | meter_hierarchy | A>B | Clear meter > no onsets |",
        "| 39 | aacm/03 P5 | iacm/02 cluster | consonance_valence_mapping | A>B | Consonant > cluster |",
        "| 40 | cross/02 beat_cons | cross/03 beat_diss | consonance_valence_mapping | A>B | Consonant > dissonant |",
        "",
        "## Stimulus Index",
        "",
    ]

    # Group by directory
    groups = {}
    for key, meta in sorted(ALL_METADATA.items()):
        grp = key.split("/")[0]
        if grp not in groups:
            groups[grp] = []
        groups[grp].append((key, meta))

    for grp_name, items in groups.items():
        lines.append(f"### {grp_name}/")
        lines.append("")
        lines.append("| File | Duration | Description |")
        lines.append("|------|----------|-------------|")
        for key, meta in items:
            fname = key.split("/", 1)[1]
            dur = meta.get("duration_s", "?")
            desc = meta.get("description", "")[:80]
            lines.append(f"| {fname} | {dur}s | {desc} |")
        lines.append("")

    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  STIMULUS-CATALOG.md -> {path.relative_to(_ROOT)}")


# =====================================================================
# Main
# =====================================================================

def main():
    """Generate all F3 test stimuli."""
    print("=" * 70)
    print("  F3 (Attention & Salience) Test Audio Generator")
    print("  Output: Test-Audio/micro_beliefs/f3/")
    print("=" * 70)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Category 1: Beat Entrainment (SNEM, 10 stimuli)
    generate_snem_beat()

    # Category 2: Meter Hierarchy (SNEM, 8 stimuli)
    generate_snem_meter()

    # Category 3: Attention Capture (IACM, 8 stimuli)
    generate_iacm_capture()

    # Category 4: Object Segregation & Precision (IACM, 6 stimuli)
    generate_iacm_segregation()

    # Category 5: Salience Network (CSG, 8 stimuli)
    generate_csg_salience()

    # Category 6: Aesthetic Engagement (AACM, 7 stimuli)
    generate_aacm_aesthetic()

    # Category 7: Cross-Mechanism Integration (8 stimuli)
    generate_cross()

    # Category 8: Boundary Conditions (5 stimuli)
    generate_boundary()

    # Write metadata and catalog
    write_metadata()
    write_catalog()

    print(f"\n{'=' * 70}")
    print(f"  DONE — {_count} stimuli generated")
    print(f"  Output: {OUT_DIR.relative_to(_ROOT)}/")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
