"""Deterministic MIDI-based test audio generator for F6 (Reward & Motivation).

Generates ~75 stimuli across 6 categories for testing all 16 F6 beliefs:
  - SRP  (11): wanting, liking, pleasure, prediction_error, tension,
               prediction_match, peak_detection, harmonic_tension,
               chills_proximity, resolution_expectation, reward_forecast
  - DAED (5):  da_caudate, da_nacc, dissociation_index, temporal_phase,
               wanting_ramp

Scientific basis:
  - SRP:   Blood & Zatorre 2001 (PET, chills->DA), Huron 2006 (ITPRA),
           Steinbeis 2006 (tension-resolution), Koelsch 2013
  - DAED:  Salimpoor 2011 (PET [11C]raclopride, caudate r=0.71/NAcc r=0.84),
           Berridge 2007 (wanting vs liking), Mohebi 2024 (DA gradient)
  - SSRI:  Ni et al. 2024 (fNIRS N=528, rDLPFC sync d=0.85),
           Dunbar 2012 (endorphin 1.3-1.8x)
  - MORMR: Putkinen 2025 (PET [11C]carfentanil, d=4.8)
  - RPEM:  Gold 2023 (fMRI, VS crossover d=1.07)

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
    major_triad, minor_triad, dominant_seventh,
    chromatic_cluster, diatonic_scale,
    C2, D2, E2, F2, G2, A2, B2,
    C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5, A5, B5,
    C6,
)

OUTPUT_DIR = _PROJECT_ROOT / "Test-Audio" / "micro_beliefs" / "f6"
ALL_METADATA: dict = {}

# Extra pitch constants not exported by real_audio_stimuli
Bb2 = 46; Bb3 = 58; Db3 = 49; Eb3 = 51; Ab3 = 56
Db5 = 73; Eb5 = 75; Ab5 = 80; Bb5 = 82
C1 = 24; C7 = 96

# Chord voicings
C_MAJ = major_triad(C4)
C_MIN = minor_triad(C4)
G_DOM7 = dominant_seventh(G3)
F_MAJ = [F3, A3, C4]
A_MIN = [A3, C4, E4]
D_MIN = [D4, F4, A4]
C_MAJ_WIDE = [C3, G3, C4, E4, G4]
Eb_MAJ = [Eb4, G4, Bb4]


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


# ── MIDI builder helpers ─────────────────────────────────────────────

Note = pretty_midi.Note


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


def _pm_crescendo(pitch: int, n_beats: int, ioi: float,
                  v_start: int = 20, v_end: int = 120,
                  program: int = PIANO) -> pretty_midi.PrettyMIDI:
    note_dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_beats):
        v = int(v_start + (v_end - v_start) * i / max(n_beats - 1, 1))
        t = i * ioi
        inst.notes.append(Note(velocity=v, pitch=pitch,
                               start=t, end=t + note_dur))
    pm.instruments.append(inst)
    return pm


def _pm_near_silence(duration: float = 5.0) -> pretty_midi.PrettyMIDI:
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=1, pitch=60, start=0.0, end=0.01))
    pm.instruments.append(inst)
    return pm


def _pm_dense_random(duration: float = 5.0, seed: int = 60,
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
    """Chord progression with separate chords."""
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


def _pm_ensemble_crescendo(voices: list[tuple], n_beats: int, ioi: float,
                           v_start: int = 30,
                           v_end: int = 127) -> pretty_midi.PrettyMIDI:
    """Multi-instrument crescendo. voices: list of (pitches, program)."""
    note_dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    for pitches, prog in voices:
        inst = pretty_midi.Instrument(program=prog)
        for i in range(n_beats):
            v = int(v_start + (v_end - v_start) * i / max(n_beats - 1, 1))
            t = i * ioi
            for p in (pitches if isinstance(pitches, list) else [pitches]):
                inst.notes.append(Note(velocity=v, pitch=p,
                                       start=t, end=t + note_dur))
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


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 1: SRP — Striatal Reward Pathway (18 stimuli)
#
# Tests: wanting, liking, pleasure, prediction_error, tension,
#        prediction_match, peak_detection, harmonic_tension,
#        chills_proximity, resolution_expectation, reward_forecast
#
# Key R3: [7]amplitude, [21]spectral_flux, [4]pleasantness,
#          [0]roughness, [8]loudness
# Key H3: amplitude trend M18, spectral_flux trend M18 (500ms L0)
# ═══════════════════════════════════════════════════════════════════════

def generate_srp_stimuli() -> None:
    """18 stimuli targeting SRP relay and its 11 beliefs."""

    # ── 01: SATB major cadence I-IV-V-I — HIGH pleasure, tension arc ──
    # 4-voice polyphonic: Flute(S) + Strings(AT) + Cello(B)
    # Huron 2006: tension builds on V, resolves on final I
    pm = pretty_midi.PrettyMIDI()
    s = pretty_midi.Instrument(program=FLUTE)
    at = pretty_midi.Instrument(program=STRINGS)
    b = pretty_midi.Instrument(program=CELLO)
    voicings = [(E5, [C5, G4], C3), (F5, [C5, A4], F3),
                (D5, [B4, G4], G3), (E5, [C5, G4], C3)]
    for idx, (sp, atp, bp) in enumerate(voicings):
        t0, t1 = idx * 1.5, (idx + 1) * 1.5 - 0.02
        s.notes.append(Note(velocity=80, pitch=sp, start=t0, end=t1))
        for p in atp:
            at.notes.append(Note(velocity=70, pitch=p, start=t0, end=t1))
        b.notes.append(Note(velocity=75, pitch=bp, start=t0, end=t1))
    pm.instruments.extend([s, at, b])
    save(pm, "srp", "01_satb_major_cadence", {
        "description": "SATB I-IV-V-I in C major, Flute+Strings+Cello, 6s",
        "expected": {
            "pleasure": "HIGH — consonant polyphonic cadence",
            "tension": "LOW-HIGH-LOW — builds on V, resolves on I",
            "harmonic_tension": "LOW-HIGH-LOW — V=dominant tension",
            "resolution_expectation": "HIGH at chord 3 (V->I expected)",
        },
        "science": "Huron 2006 ITPRA: cadential tension-resolution cycle",
    })

    # ── 02: SATB minor lament — moderate pleasure, sustained tension ──
    pm = pretty_midi.PrettyMIDI()
    s = pretty_midi.Instrument(program=STRINGS)
    b = pretty_midi.Instrument(program=CELLO)
    # Lamento bass: D3->C3->Bb2->A2 with upper voices
    lament = [(F4, D3), (E4, C3), (D4, Bb2), (Db4, A2)]
    for idx, (sp, bp) in enumerate(lament):
        t0, t1 = idx * 1.5, (idx + 1) * 1.5 - 0.02
        s.notes.append(Note(velocity=70, pitch=sp, start=t0, end=t1))
        s.notes.append(Note(velocity=65, pitch=sp - 4, start=t0, end=t1))
        b.notes.append(Note(velocity=75, pitch=bp, start=t0, end=t1))
    pm.instruments.extend([s, b])
    save(pm, "srp", "02_satb_minor_lament", {
        "description": "SATB lamento bass D minor, Strings+Cello, 6s",
        "expected": {
            "pleasure": "LOW-MED — minor mode, chromatic descent",
            "tension": "HIGH — unresolved chromatic motion",
            "harmonic_tension": "HIGH — chromatic voice leading",
        },
        "science": "Huron 2006: minor mode sustains tension without resolution",
    })

    # ── 03: Orch consonant sustained — HIGH liking ────────────────────
    pm = _pm_ensemble_chord([
        ([C4, E4, G4], STRINGS, 70),
        ([C5, E5], PIANO, 60),
    ], 6.0)
    save(pm, "srp", "03_orch_consonant_sustained", {
        "description": "Strings+Piano C major 7th, legato mf, 6s",
        "expected": {
            "liking": "HIGH — sustained consonance",
            "pleasure": "HIGH — warm + consonant",
            "harmonic_tension": "LOW — tonic stability",
        },
        "science": "Salimpoor 2011: sustained consonance activates NAcc",
    })

    # ── 04: Orch dissonant cluster — LOW liking, HIGH tension ─────────
    pm = _pm_ensemble_chord([
        ([C4, Db4, D4], STRINGS, 100),
        ([Eb4, E4, F4], TRUMPET, 100),
    ], 6.0)
    save(pm, "srp", "04_orch_dissonant_cluster", {
        "description": "Strings+Trumpet 6-note chromatic cluster, ff, 6s",
        "expected": {
            "liking": "LOW — maximum roughness",
            "pleasure": "LOW — dissonant texture",
            "harmonic_tension": "HIGH — chromatic cluster",
        },
        "science": "Plomp-Levelt 1965: cluster within critical bandwidth = max roughness",
    })

    # ── 05: Piano deceptive cadence V7->vi — HIGH prediction_error ────
    # Bars: C->Am->Dm->G7->Am (deceptive instead of C)
    pm = _pm_progression(
        [C_MAJ, A_MIN, D_MIN, G_DOM7, A_MIN],
        [1.6, 1.6, 1.6, 1.6, 1.6], PIANO, 80)
    save(pm, "srp", "05_piano_deceptive_cadence", {
        "description": "Piano C-Am-Dm-G7-Am (deceptive V7->vi), 8s",
        "expected": {
            "prediction_error": "HIGH — V7->vi violates V7->I expectation",
            "prediction_match": "LOW — deceptive resolution",
            "tension": "HIGH->SUSTAINED — no true resolution",
        },
        "science": "Huron 2006: deceptive cadence = maximal prediction violation",
    })

    # ── 06: Piano perfect cadence V7->I — HIGH prediction_match ───────
    pm = _pm_progression(
        [C_MAJ, A_MIN, D_MIN, G_DOM7, C_MAJ],
        [1.6, 1.6, 1.6, 1.6, 1.6], PIANO, 80)
    save(pm, "srp", "06_piano_perfect_cadence", {
        "description": "Piano C-Am-Dm-G7-C (perfect V7->I), 8s",
        "expected": {
            "prediction_match": "HIGH — V7->I fulfilled",
            "prediction_error": "LOW — expected resolution",
            "tension": "HIGH->LOW — proper resolution",
            "resolution_expectation": "HIGH at G7, confirmed at C",
        },
        "science": "Meyer 1956: fulfilled harmonic expectation = satisfaction",
    })

    # ── 07: Orch crescendo climax — HIGH peak_detection ───────────────
    pm = _pm_ensemble_crescendo(
        [([C4, E4, G4], STRINGS), ([C5, E5, G5], PIANO)],
        n_beats=16, ioi=0.5, v_start=30, v_end=127)
    save(pm, "srp", "07_orch_crescendo_climax", {
        "description": "Strings+Piano C major crescendo pp->fff, 16 beats, 8s",
        "expected": {
            "peak_detection": "HIGH — fff climax at end",
            "wanting": "RISING — anticipatory buildup",
            "chills_proximity": "RISING — approaching peak",
            "reward_forecast": "RISING — increasing reward expectation",
        },
        "science": "Blood & Zatorre 2001: crescendo -> DA peak at climax",
    })

    # ── 08: Piano static pp — LOW everything (control) ────────────────
    pm = _pm_note(C4, 6.0, PIANO, 30)
    save(pm, "srp", "08_piano_static_pp", {
        "description": "Piano C4 sustained pp (v=30), 6s — control",
        "expected": {
            "peak_detection": "LOW — no dynamic peak",
            "wanting": "LOW — no anticipatory buildup",
            "pleasure": "LOW — minimal hedonic signal",
        },
        "science": "Control: minimal reward pathway activation",
    })

    # ── 09: Strings legato warm — HIGH liking (warmth) ────────────────
    pm = pretty_midi.PrettyMIDI()
    vln = pretty_midi.Instrument(program=VIOLIN)
    vcl = pretty_midi.Instrument(program=CELLO)
    mel = [C5, D5, E5, F5, G5, F5, E5, D5]
    t = 0.0
    for p in mel:
        vln.notes.append(Note(velocity=75, pitch=p, start=t, end=t + 0.73))
        t += 0.75
    vcl.notes.append(Note(velocity=70, pitch=C3, start=0.0, end=6.0))
    pm.instruments.extend([vln, vcl])
    save(pm, "srp", "09_strings_legato_warm", {
        "description": "Violin melody + Cello pedal C3, legato, 6s",
        "expected": {
            "liking": "HIGH — warm timbre + consonant",
            "pleasure": "HIGH — sustained warmth",
        },
        "science": "Putkinen 2025: warm timbres -> opioid-mediated pleasure",
    })

    # ── 10: Brass staccato harsh — LOW liking ─────────────────────────
    pm = pretty_midi.PrettyMIDI()
    trp = pretty_midi.Instrument(program=TRUMPET)
    trb = pretty_midi.Instrument(program=TROMBONE)
    for i in range(16):
        t = i * 0.375
        p_hi = C5 if i % 2 == 0 else Db5
        p_lo = C3 if i % 2 == 0 else Db3
        trp.notes.append(Note(velocity=110, pitch=p_hi, start=t, end=t + 0.15))
        trb.notes.append(Note(velocity=110, pitch=p_lo, start=t, end=t + 0.15))
    pm.instruments.extend([trp, trb])
    save(pm, "srp", "10_brass_staccato_harsh", {
        "description": "Trumpet+Trombone alternating minor 2nds, ff, 6s",
        "expected": {
            "liking": "LOW — harsh timbre + dissonance",
            "harmonic_tension": "HIGH — minor 2nd intervals",
            "prediction_error": "MED — alternating pattern partially predictable",
        },
        "science": "Sethares 1993: m2 interval high roughness -> tension",
    })

    # ── 11: Piano dom7 sustained — HIGH tension (unresolved) ──────────
    pm = _pm_chord(G_DOM7, 8.0, PIANO, 75)
    save(pm, "srp", "11_piano_dom7_sustained", {
        "description": "Piano G7 chord sustained, 8s — unresolved dominant",
        "expected": {
            "tension": "HIGH — dominant 7th = inherent instability",
            "harmonic_tension": "HIGH — tritone B-F within V7",
            "resolution_expectation": "HIGH — V7 strongly implies resolution",
        },
        "science": "Bigand 2006: unresolved dominants maintain tension",
    })

    # ── 12: Piano dom7 resolved — tension HIGH->LOW ───────────────────
    pm = _pm_progression([G_DOM7, C_MAJ_WIDE], [4.0, 4.0], PIANO, 75)
    save(pm, "srp", "12_piano_dom7_resolved", {
        "description": "Piano G7 (4s) -> C major (4s) — resolution",
        "expected": {
            "tension": "HIGH->LOW — dominant resolves to tonic",
            "harmonic_tension": "HIGH->LOW — tritone resolves",
            "resolution_expectation": "HIGH->FULFILLED",
            "liking": "RISING — resolution is pleasurable",
        },
        "science": "Steinbeis 2006: tension-resolution -> reward activation",
    })

    # ── 13: Orch double climax — two peaks, reward_forecast ───────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=STRINGS)
    # Peak 1 (0-3s): crescendo pp->mf
    for i in range(6):
        v = 30 + int(50 * i / 5)
        t = i * 0.5
        for p in [C4, E4, G4]:
            inst.notes.append(Note(velocity=v, pitch=p, start=t, end=t + 0.48))
    # Valley (3-5s): diminuendo mf->pp
    for i in range(4):
        v = 80 - int(50 * i / 3)
        t = 3.0 + i * 0.5
        for p in [C4, E4, G4]:
            inst.notes.append(Note(velocity=v, pitch=p, start=t, end=t + 0.48))
    # Peak 2 (5-8s): crescendo pp->fff
    for i in range(6):
        v = 30 + int(97 * i / 5)
        t = 5.0 + i * 0.5
        for p in [C4, E4, G4]:
            inst.notes.append(Note(velocity=v, pitch=p, start=t, end=t + 0.48))
    # Sustain fff (8-10s)
    for p in [C4, E4, G4]:
        inst.notes.append(Note(velocity=127, pitch=p, start=8.0, end=10.0))
    pm.instruments.append(inst)
    save(pm, "srp", "13_orch_double_climax", {
        "description": "Strings 2-peak crescendo (mf+fff), 10s",
        "expected": {
            "peak_detection": "TWO PEAKS — at 3s (mf) and 8s (fff)",
            "reward_forecast": "HIGHER at peak 2 — learned from peak 1",
            "wanting": "RISING before each peak",
        },
        "science": "Blood & Zatorre 2001: repeated peaks with sensitization",
    })

    # ── 14: Tritone to P5 resolution — harmonic_tension HIGH->LOW ─────
    pm = _pm_progression([[B3, F4], [C4, G4]], [3.0, 3.0], STRINGS, 75)
    save(pm, "srp", "14_tritone_to_p5", {
        "description": "Strings B3-F4 tritone (3s) -> C4-G4 P5 (3s)",
        "expected": {
            "harmonic_tension": "HIGH->LOW — TT resolves to P5",
            "tension": "HIGH->LOW — dissonance to consonance",
            "liking": "LOW->HIGH — pleasure at resolution",
        },
        "science": "Sethares 1993: TT=max dissonance, P5=high consonance",
    })

    # ── 15: Whole tone scale — ambiguous tonality ─────────────────────
    wt = [C4, D4, E4, Gb4, Ab4, Bb4, C5, Bb4, Ab4, Gb4, E4, D4]
    pm = _pm_melody(wt, [0.4] * 12, PIANO, 80)
    save(pm, "srp", "15_piano_whole_tone_scale", {
        "description": "Piano whole-tone scale up+down, 4.8s",
        "expected": {
            "prediction_error": "MED — ambiguous tonal center",
            "harmonic_tension": "MED — no clear tonic resolution",
        },
        "science": "Temperley 2007: whole-tone = maximally ambiguous tonality",
    })

    # ── 16: Orch unison to harmony — pleasure RISING ──────────────────
    pm = pretty_midi.PrettyMIDI()
    fl = pretty_midi.Instrument(program=FLUTE)
    st = pretty_midi.Instrument(program=STRINGS)
    vc = pretty_midi.Instrument(program=CELLO)
    # Phase 1 (0-2s): all on C4 unison
    for inst_obj in [fl, st, vc]:
        inst_obj.notes.append(Note(velocity=70, pitch=C4, start=0.0, end=1.98))
    # Phase 2 (2-6s): spread to C major voicing
    fl.notes.append(Note(velocity=75, pitch=G4, start=2.0, end=5.98))
    st.notes.append(Note(velocity=70, pitch=E4, start=2.0, end=5.98))
    vc.notes.append(Note(velocity=75, pitch=C3, start=2.0, end=5.98))
    pm.instruments.extend([fl, st, vc])
    save(pm, "srp", "16_orch_unison_to_harmony", {
        "description": "Flute+Strings+Cello unison C4 -> C major spread, 6s",
        "expected": {
            "pleasure": "RISING — unison to rich harmony",
            "harmonic_tension": "STABLE-LOW — P1 to consonant triad",
        },
        "science": "Consonance hierarchy: unison -> open voicing = stable pleasure",
    })

    # ── 17: Piano polyrhythm 3v4 — metric prediction_error ────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # Voice 1: triplets on C5 (3 per 2s cycle)
    cycle_dur = 2.0
    for cycle in range(3):
        for i in range(3):
            t = cycle * cycle_dur + i * (cycle_dur / 3)
            inst.notes.append(Note(velocity=80, pitch=C5,
                                   start=t, end=t + 0.4))
    # Voice 2: quarters on C3 (4 per 2s cycle)
    for cycle in range(3):
        for i in range(4):
            t = cycle * cycle_dur + i * (cycle_dur / 4)
            inst.notes.append(Note(velocity=70, pitch=C3,
                                   start=t, end=t + 0.35))
    pm.instruments.append(inst)
    save(pm, "srp", "17_piano_polyrhythm_3v4", {
        "description": "Piano 3-against-4 polyrhythm, C major, 6s",
        "expected": {
            "prediction_error": "MED — metric conflict creates surprise",
            "tension": "MED — rhythmic complexity",
        },
        "science": "Vuust 2009: polyrhythmic surprise activates prediction error",
    })

    # ── 18: Orch fortissimo resolution — peak + pleasure ──────────────
    pm = pretty_midi.PrettyMIDI()
    trp = pretty_midi.Instrument(program=TRUMPET)
    st = pretty_midi.Instrument(program=STRINGS)
    vc = pretty_midi.Instrument(program=CELLO)
    # V7 chord (0-2s) ff
    for p in [G4, B4]:
        trp.notes.append(Note(velocity=120, pitch=p, start=0.0, end=1.98))
    for p in [D4, F4]:
        st.notes.append(Note(velocity=110, pitch=p, start=0.0, end=1.98))
    vc.notes.append(Note(velocity=115, pitch=G2, start=0.0, end=1.98))
    # I chord (2-4s) fff
    for p in [C5, E5]:
        trp.notes.append(Note(velocity=127, pitch=p, start=2.0, end=3.98))
    for p in [C4, G4]:
        st.notes.append(Note(velocity=120, pitch=p, start=2.0, end=3.98))
    vc.notes.append(Note(velocity=120, pitch=C3, start=2.0, end=3.98))
    pm.instruments.extend([trp, st, vc])
    save(pm, "srp", "18_orch_fortissimo_resolution", {
        "description": "Trumpet+Strings+Cello ff V7->fff I cadence, 4s",
        "expected": {
            "peak_detection": "HIGH — fff climax at resolution",
            "pleasure": "HIGH — powerful consonant resolution",
            "tension": "HIGH->LOW — dominant to tonic",
            "liking": "HIGH — orchestral climax",
        },
        "science": "Blood & Zatorre 2001: orchestral climax = peak DA release",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 2: DAED — Dopamine Anticipation-Experience Dissociation
#              (15 stimuli)
#
# Tests: da_caudate, da_nacc, dissociation_index, temporal_phase,
#        wanting_ramp
#
# Key R3: [8]loudness velocity, [0]roughness velocity,
#          [4]pleasantness mean, [21]spectral entropy, [25]coupling
# Key H3: loudness_velocity_1s (8,16,8,0), pleas_mean_1s (4,16,1,2)
# ═══════════════════════════════════════════════════════════════════════

def generate_daed_stimuli() -> None:
    """15 stimuli targeting DAED relay and its 5 beliefs."""

    # ── 01: Strings crescendo 8s — HIGH da_caudate, wanting_ramp ──────
    pm = _pm_ensemble_crescendo(
        [([C4, E4, G4], STRINGS)],
        n_beats=16, ioi=0.5, v_start=25, v_end=120)
    save(pm, "daed", "01_strings_crescendo_8s", {
        "description": "Strings C major crescendo pp->ff, 16 beats, 8s",
        "expected": {
            "da_caudate": "HIGH — loudness velocity sustained positive",
            "wanting_ramp": "RISING — caudate DA ramp builds",
            "temporal_phase": "HIGH->1.0 — pure anticipation phase",
        },
        "science": "Salimpoor 2011: caudate DA ramps 15-30s before peak (r=0.71)",
    })

    # ── 02: Piano sudden major chord — HIGH da_nacc ───────────────────
    # 2s silence then sudden fff C major
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=1, pitch=60, start=0.0, end=0.01))
    for p in C_MAJ:
        inst.notes.append(Note(velocity=127, pitch=p, start=2.0, end=4.0))
    pm.instruments.append(inst)
    save(pm, "daed", "02_piano_sudden_major_chord", {
        "description": "Silence 2s -> Piano fff C major, 4s total",
        "expected": {
            "da_nacc": "HIGH — sudden consummatory DA burst",
            "temporal_phase": "LOW->0 — pure consummation at onset",
            "da_caudate": "LOW — no anticipatory buildup",
        },
        "science": "Salimpoor 2011: NAcc DA burst at peak moment (r=0.84)",
    })

    # ── 03: Orch buildup no resolution — wanting without liking ───────
    pm = _pm_ensemble_crescendo(
        [([G3, B3, D4, F4], STRINGS), ([G4], FRENCH_HORN)],
        n_beats=16, ioi=0.5, v_start=30, v_end=110)
    save(pm, "daed", "03_orch_buildup_no_resolution", {
        "description": "Strings+Horn V7 crescendo, NO resolution, 8s",
        "expected": {
            "da_caudate": "HIGH — sustained loudness velocity",
            "da_nacc": "LOW — no consummatory peak",
            "dissociation_index": "HIGH — |caudate - nacc| large",
            "wanting_ramp": "RISING — wanting without liking",
        },
        "science": "Berridge 2007: wanting (DA) without liking (opioid)",
    })

    # ── 04: Sudden pleasant surprise — liking without wanting ─────────
    pm = pretty_midi.PrettyMIDI()
    org = pretty_midi.Instrument(program=ORGAN)
    org.notes.append(Note(velocity=40, pitch=C4, start=0.0, end=2.98))
    st = pretty_midi.Instrument(program=STRINGS)
    for p in [C4, E4, G4, C5]:
        st.notes.append(Note(velocity=85, pitch=p, start=3.0, end=6.0))
    pm.instruments.extend([org, st])
    save(pm, "daed", "04_orch_sudden_pleasant_surprise", {
        "description": "Quiet organ 3s -> warm strings C major, 6s",
        "expected": {
            "da_nacc": "HIGH — sudden pleasant stimulus",
            "da_caudate": "LOW — no anticipatory buildup phase",
            "dissociation_index": "HIGH — reversed dissociation",
        },
        "science": "Berridge 2007: liking without prior wanting",
    })

    # ── 05: Piano steady mf — LOW dissociation (control) ─────────────
    pm = _pm_chord(C_MAJ, 6.0, PIANO, 75)
    save(pm, "daed", "05_piano_steady_mf", {
        "description": "Piano C major mf (v=75), 6s — no phase differentiation",
        "expected": {
            "dissociation_index": "LOW — no temporal differentiation",
            "temporal_phase": "~0.5 — neither anticipation nor consummation",
        },
        "science": "Control: steady-state stimulus for DAED baseline",
    })

    # ── 06: Strings slow crescendo 12s — slow wanting_ramp ────────────
    pm = _pm_ensemble_crescendo(
        [([C4, E4, G4], STRINGS)],
        n_beats=24, ioi=0.5, v_start=25, v_end=80)
    save(pm, "daed", "06_strings_slow_crescendo_12s", {
        "description": "Strings C major very gradual crescendo pp->mf, 12s",
        "expected": {
            "wanting_ramp": "SLOWLY RISING — gradual DA ramp",
            "da_caudate": "MED — moderate loudness velocity",
        },
        "science": "Mohebi 2024: slow DA ramp gradient in caudate",
    })

    # ── 07: Orch fast crescendo 4s — fast wanting_ramp ────────────────
    pm = _pm_ensemble_crescendo(
        [([C4, E4, G4], STRINGS), ([C5, E5], PIANO)],
        n_beats=8, ioi=0.5, v_start=30, v_end=127)
    save(pm, "daed", "07_orch_fast_crescendo_4s", {
        "description": "Strings+Piano fast crescendo pp->fff, 4s",
        "expected": {
            "wanting_ramp": "FAST RISING — steep DA ramp",
            "da_caudate": "HIGH — high loudness velocity",
            "da_nacc": "HIGH at end — consummation spike",
        },
        "science": "Salimpoor: faster ramp = stronger peak response",
    })

    # ── 08: SATB buildup resolve — temporal_phase 1.0->0.0 ───────────
    pm = pretty_midi.PrettyMIDI()
    st = pretty_midi.Instrument(program=STRINGS)
    vc = pretty_midi.Instrument(program=CELLO)
    # Buildup: iv->V7 crescendo (0-6s)
    buildup = [([F4, A4], F3), ([F4, Ab4], F3),
               ([G4, B4], G3), ([G4, B4, D5], G3)]
    for idx, (upper, bass) in enumerate(buildup):
        v = 40 + idx * 20
        t0, t1 = idx * 1.5, (idx + 1) * 1.5 - 0.02
        for p in upper:
            st.notes.append(Note(velocity=v, pitch=p, start=t0, end=t1))
        vc.notes.append(Note(velocity=v, pitch=bass, start=t0, end=t1))
    # Resolution: I chord (6-8s) forte
    for p in [C4, E4, G4, C5]:
        st.notes.append(Note(velocity=100, pitch=p, start=6.0, end=7.98))
    vc.notes.append(Note(velocity=100, pitch=C3, start=6.0, end=7.98))
    pm.instruments.extend([st, vc])
    save(pm, "daed", "08_satb_buildup_resolve", {
        "description": "Strings+Cello buildup iv-V7 (6s) -> I resolution (2s)",
        "expected": {
            "temporal_phase": "1.0->0.0 — anticipation to consummation",
            "da_caudate": "HIGH in buildup, LOW at resolution",
            "da_nacc": "LOW in buildup, HIGH at resolution",
            "dissociation_index": "HIGH then LOW",
        },
        "science": "Salimpoor 2011: temporal dissociation of caudate/NAcc DA",
    })

    # ── 09: Piano repetitive pattern — LOW wanting_ramp ───────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    pattern = [C4, E4, G4, E4]
    for rep in range(4):
        for i, p in enumerate(pattern):
            t = rep * 2.0 + i * 0.5
            inst.notes.append(Note(velocity=75, pitch=p,
                                   start=t, end=t + 0.48))
    pm.instruments.append(inst)
    save(pm, "daed", "09_piano_repetitive_pattern", {
        "description": "Piano C-E-G-E pattern repeated 4x, 8s",
        "expected": {
            "wanting_ramp": "LOW — no anticipatory buildup",
            "da_caudate": "LOW — no loudness velocity change",
            "prediction_error": "LOW after first cycle — pattern learned",
        },
        "science": "Control: repetitive pattern = no anticipatory ramp",
    })

    # ── 10: Strings descending diminuendo — post-climax decay ─────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=STRINGS)
    for i in range(12):
        v = 120 - int(90 * i / 11)
        t = i * 0.5
        p = G4 - i  # descending chromatic
        for note_p in [p, p + 4, p + 7]:
            if 36 <= note_p <= 96:
                inst.notes.append(Note(velocity=v, pitch=note_p,
                                       start=t, end=t + 0.48))
    pm.instruments.append(inst)
    save(pm, "daed", "10_strings_descending_dim", {
        "description": "Strings ff->pp descending chromatic triads, 6s",
        "expected": {
            "da_caudate": "LOW — negative loudness velocity (falling)",
            "temporal_phase": "LOW->0 — post-climax phase",
            "wanting_ramp": "FALLING — wanting decreasing",
        },
        "science": "Post-climax dopamine decay signature",
    })

    # ── 11: Tension-release cycle — dissociation oscillating ──────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=STRINGS)
    for cycle in range(2):
        offset = cycle * 4.0
        # Buildup (3s): crescendo on V7
        for i in range(6):
            v = 40 + int(70 * i / 5)
            t = offset + i * 0.5
            for p in G_DOM7:
                inst.notes.append(Note(velocity=v, pitch=p,
                                       start=t, end=t + 0.48))
        # Release (1s): I chord forte
        for p in C_MAJ:
            inst.notes.append(Note(velocity=100, pitch=p,
                                   start=offset + 3.0, end=offset + 3.98))
    pm.instruments.append(inst)
    save(pm, "daed", "11_orch_tension_release_cycle", {
        "description": "Strings 2x cycle: 3s V7 buildup + 1s I release, 8s",
        "expected": {
            "dissociation_index": "OSCILLATING — cycles of high/low",
            "temporal_phase": "CYCLING 1.0->0.0->1.0->0.0",
        },
        "science": "Vuust 2022: repeated tension-release cycles",
    })

    # ── 12: Piano arpeggiated buildup — wanting_ramp via harmony ──────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    prog = [C_MAJ, A_MIN, D_MIN, G_DOM7]
    t = 0.0
    for chord_idx, chord in enumerate(prog):
        v = 60 + chord_idx * 15
        for i, p in enumerate(chord):
            inst.notes.append(Note(velocity=v, pitch=p,
                                   start=t + i * 0.2, end=t + 1.98))
        t += 2.0
    pm.instruments.append(inst)
    save(pm, "daed", "12_piano_arpeggiated_buildup", {
        "description": "Piano C-Am-Dm-G7 arpeggios with crescendo, 8s",
        "expected": {
            "wanting_ramp": "RISING — harmonic departure + dynamic buildup",
            "da_caudate": "RISING — increasing energy velocity",
        },
        "science": "Steinbeis 2006: harmonic distance from tonic -> wanting",
    })

    # ── 13: Brass fanfare peak — HIGH da_nacc ─────────────────────────
    pm = pretty_midi.PrettyMIDI()
    trp = pretty_midi.Instrument(program=TRUMPET)
    hrn = pretty_midi.Instrument(program=FRENCH_HORN)
    for p in [C5, E5, G5]:
        trp.notes.append(Note(velocity=127, pitch=p, start=0.0, end=4.0))
    for p in [C4, G4]:
        hrn.notes.append(Note(velocity=120, pitch=p, start=0.0, end=4.0))
    pm.instruments.extend([trp, hrn])
    save(pm, "daed", "13_brass_fanfare_peak", {
        "description": "Trumpet+Horn C major fanfare fff, 4s",
        "expected": {
            "da_nacc": "HIGH — consummatory DA at peak loudness",
            "da_caudate": "MED — no buildup, immediate peak",
        },
        "science": "Blood & Zatorre: brass climax = peak DA activation",
    })

    # ── 14: Organ sustained warm — tonic pleasure, LOW ramp ───────────
    pm = _pm_chord([C4, E4, G4, B4], 8.0, ORGAN, 65)
    save(pm, "daed", "14_organ_sustained_warm", {
        "description": "Organ C major 7th, pp-p sustained, 8s",
        "expected": {
            "da_nacc": "MED — sustained tonic pleasure (not burst)",
            "wanting_ramp": "LOW — no dynamic buildup",
            "dissociation_index": "LOW — steady state",
        },
        "science": "Putkinen 2025: sustained opioid, not DA ramp",
    })

    # ── 15: Orch approach retreat — wanting frustrated ────────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=STRINGS)
    # Crescendo 0-4s
    for i in range(8):
        v = 30 + int(90 * i / 7)
        t = i * 0.5
        for p in [C4, E4, G4]:
            inst.notes.append(Note(velocity=v, pitch=p,
                                   start=t, end=t + 0.48))
    # Decrescendo 4-8s (no cadence, just fade)
    for i in range(8):
        v = 120 - int(90 * i / 7)
        t = 4.0 + i * 0.5
        for p in [C4, E4, G4]:
            inst.notes.append(Note(velocity=v, pitch=p,
                                   start=t, end=t + 0.48))
    pm.instruments.append(inst)
    save(pm, "daed", "15_orch_approach_retreat", {
        "description": "Strings crescendo 4s -> decrescendo 4s, no cadence",
        "expected": {
            "wanting_ramp": "RISE then FALL — approach then retreat",
            "da_caudate": "HIGH then LOW — anticipation frustrated",
            "dissociation_index": "TEMPORAL — rises then dissipates",
        },
        "science": "Anticipation frustrated: approach without arrival",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 3: SSRI — Social Synchrony Reward Integration (12 stimuli)
#
# Tests all F6 beliefs with ensemble textures designed for SSRI:
#   synchrony_reward, social_bonding, entrainment_quality,
#   group_flow, collective_pleasure, endorphin_proxy
#
# Key R3: [10]onset_strength, [4]pleasantness, [12]warmth,
#          [25]coupling, [8]loudness
# Key H3: onset periodicity (10,8,14,2), coupling trend (25,16,18,2)
# ═══════════════════════════════════════════════════════════════════════

def generate_ssri_stimuli() -> None:
    """12 stimuli targeting SSRI encoder with ensemble textures."""

    # ── 01: Ensemble isochronous 120BPM — HIGH entrainment ────────────
    pm = _pm_ensemble_isochronous([
        ([C4], PIANO, 80), ([E4], STRINGS, 75), ([G4], FLUTE, 80),
    ], bpm=120.0, n_beats=16)
    save(pm, "ssri", "01_ensemble_iso_120bpm", {
        "description": "Piano+Strings+Flute synchronized 120BPM, 8s",
        "expected": {
            "wanting": "MED — rhythmic engagement",
            "pleasure": "MED-HIGH — coordinated consonant onset",
        },
        "science": "Ni 2024: coordinated music = rDLPFC sync (d=0.85, N=528)",
    })

    # ── 02: Solo piano 120BPM — control (less coupling) ───────────────
    pm = _pm_isochronous(C4, 120.0, 16, PIANO, 80)
    save(pm, "ssri", "02_solo_piano_120bpm", {
        "description": "Piano only C4 @120BPM, 16 beats, 8s — solo control",
        "expected": {
            "wanting": "MED-LOW — solo, less coordination signal",
        },
        "science": "Control: solo vs ensemble comparison",
    })

    # ── 03: Ensemble polyrhythm — MED entrainment ─────────────────────
    pm = pretty_midi.PrettyMIDI()
    p_inst = pretty_midi.Instrument(program=PIANO)
    s_inst = pretty_midi.Instrument(program=STRINGS)
    fl_inst = pretty_midi.Instrument(program=FLUTE)
    # Piano: 3/4 pattern, Strings: 4/4 pattern, Flute: melody
    for cycle in range(2):
        off = cycle * 4.0
        for i in range(6):  # triplets in 4s
            t = off + i * (4.0 / 6)
            p_inst.notes.append(Note(velocity=80, pitch=C4,
                                     start=t, end=t + 0.5))
        for i in range(8):  # quarters in 4s
            t = off + i * 0.5
            s_inst.notes.append(Note(velocity=70, pitch=E4,
                                     start=t, end=t + 0.4))
        mel = [G4, A4, B4, C5, B4, A4, G4, A4]
        for i, p in enumerate(mel):
            t = off + i * 0.5
            fl_inst.notes.append(Note(velocity=75, pitch=p,
                                      start=t, end=t + 0.45))
    pm.instruments.extend([p_inst, s_inst, fl_inst])
    save(pm, "ssri", "03_ensemble_polyrhythm", {
        "description": "Piano 3/4 + Strings 4/4 + Flute melody, 8s",
        "expected": {
            "pleasure": "MED — complex but coordinated",
        },
        "science": "Vuust 2009: complex meter interaction",
    })

    # ── 04: Call response piano->strings ───────────────────────────────
    pm = pretty_midi.PrettyMIDI()
    p_inst = pretty_midi.Instrument(program=PIANO)
    s_inst = pretty_midi.Instrument(program=STRINGS)
    call = [C5, D5, E5, G5]
    resp = [G5, E5, D5, C5]
    for rep in range(2):
        off = rep * 4.0
        for i, p in enumerate(call):
            t = off + i * 0.5
            p_inst.notes.append(Note(velocity=80, pitch=p,
                                     start=t, end=t + 0.48))
        for i, p in enumerate(resp):
            t = off + 2.0 + i * 0.5
            s_inst.notes.append(Note(velocity=75, pitch=p,
                                     start=t, end=t + 0.48))
    pm.instruments.extend([p_inst, s_inst])
    save(pm, "ssri", "04_call_response", {
        "description": "Piano call (2s) -> Strings response (2s), 2x, 8s",
        "expected": {
            "pleasure": "MED-HIGH — dialogic coordination",
        },
        "science": "Dunbar 2012: call-response = social bonding pattern",
    })

    # ── 05: Unison all instruments — HIGH group flow ──────────────────
    pm = pretty_midi.PrettyMIDI()
    mel = diatonic_scale(C4, 8)
    for prog in [PIANO, STRINGS, FLUTE]:
        inst = pretty_midi.Instrument(program=prog)
        t = 0.0
        for p in mel:
            inst.notes.append(Note(velocity=80, pitch=p,
                                   start=t, end=t + 0.73))
            t += 0.75
        pm.instruments.append(inst)
    save(pm, "ssri", "05_unison_all_instruments", {
        "description": "Piano+Strings+Flute unison diatonic melody, 6s",
        "expected": {
            "pleasure": "HIGH — maximum synchrony + consonance",
        },
        "science": "Ni 2024: unison = maximum neural synchrony",
    })

    # ── 06: Solo flute melody — control (no ensemble) ─────────────────
    pm = _pm_melody(diatonic_scale(C4, 8), [0.75] * 8, FLUTE, 80)
    save(pm, "ssri", "06_solo_flute_melody", {
        "description": "Flute solo diatonic melody, 6s — solo control",
        "expected": {
            "pleasure": "MED — pleasant but solo",
        },
        "science": "Control: solo instrument for ensemble comparison",
    })

    # ── 07: Ensemble crescendo together — collective pleasure ─────────
    pm = _pm_ensemble_crescendo(
        [([C4], PIANO), ([E4], STRINGS), ([G4], FLUTE)],
        n_beats=16, ioi=0.5, v_start=25, v_end=120)
    save(pm, "ssri", "07_ensemble_crescendo_together", {
        "description": "Piano+Strings+Flute synchronized crescendo, 8s",
        "expected": {
            "pleasure": "RISING — shared crescendo amplifies reward",
            "wanting": "RISING — coordinated buildup",
        },
        "science": "Dunbar 2012: shared crescendo = 1.3-1.8x reward amplification",
    })

    # ── 08: Instruments asynchronous — LOW coordination ───────────────
    pm = pretty_midi.PrettyMIDI()
    rng = np.random.RandomState(42)
    for prog, base_p in [(PIANO, C4), (STRINGS, E4), (FLUTE, G4)]:
        inst = pretty_midi.Instrument(program=prog)
        for i in range(12):
            offset = rng.uniform(-0.15, 0.15)
            t = i * 0.5 + offset
            if t < 0:
                t = 0.0
            inst.notes.append(Note(velocity=80, pitch=base_p,
                                   start=t, end=t + 0.35))
        pm.instruments.append(inst)
    save(pm, "ssri", "08_instruments_asynchronous", {
        "description": "Piano+Strings+Flute with random onset offsets, 6s",
        "expected": {
            "pleasure": "LOW — poor coordination",
        },
        "science": "Control: asynchronous onset = no entrainment",
    })

    # ── 09: Ensemble warm sustained — endorphin proxy ─────────────────
    pm = _pm_ensemble_chord([
        ([C4, E4], STRINGS, 65), ([G3], CELLO, 65),
        ([C4, G4], ORGAN, 60),
    ], 8.0)
    save(pm, "ssri", "09_ensemble_warm_sustained", {
        "description": "Strings+Cello+Organ sustained C major, pp, 8s",
        "expected": {
            "pleasure": "HIGH — sustained warm ensemble",
            "liking": "HIGH — warmth + consonance",
        },
        "science": "Dunbar: sustained ensemble = endorphin release",
    })

    # ── 10: Solo organ sustained — control ────────────────────────────
    pm = _pm_chord([C4, E4, G4], 8.0, ORGAN, 65)
    save(pm, "ssri", "10_solo_organ_sustained", {
        "description": "Organ only C major sustained, pp, 8s — solo control",
        "expected": {
            "pleasure": "MED-HIGH — warm but solo",
        },
        "science": "Control: solo vs ensemble for social reward",
    })

    # ── 11: Ensemble accelerando — flow rising ────────────────────────
    pm = pretty_midi.PrettyMIDI()
    for prog, p in [(PIANO, C4), (STRINGS, E4), (FLUTE, G4)]:
        inst = pretty_midi.Instrument(program=prog)
        t = 0.0
        for i in range(20):
            frac = i / 19
            bpm = 80 + 80 * frac  # 80->160 BPM
            ioi = 60.0 / bpm
            inst.notes.append(Note(velocity=80, pitch=p,
                                   start=t, end=t + ioi * 0.8))
            t += ioi
        pm.instruments.append(inst)
    save(pm, "ssri", "11_ensemble_accelerando", {
        "description": "Piano+Strings+Flute accelerando 80->160BPM, ~8s",
        "expected": {
            "wanting": "RISING — increasing drive",
        },
        "science": "Wohltjen 2023: accelerating sync = increasing entrainment",
    })

    # ── 12: Ensemble ritardando — flow falling ────────────────────────
    pm = pretty_midi.PrettyMIDI()
    for prog, p in [(PIANO, C4), (STRINGS, E4), (FLUTE, G4)]:
        inst = pretty_midi.Instrument(program=prog)
        t = 0.0
        for i in range(20):
            frac = i / 19
            bpm = 160 - 80 * frac  # 160->80 BPM
            ioi = 60.0 / bpm
            inst.notes.append(Note(velocity=80, pitch=p,
                                   start=t, end=t + ioi * 0.8))
            t += ioi
        pm.instruments.append(inst)
    save(pm, "ssri", "12_ensemble_ritardando", {
        "description": "Piano+Strings+Flute ritardando 160->80BPM, ~8s",
        "expected": {
            "wanting": "FALLING — decreasing drive",
        },
        "science": "Decelerating = disengagement",
    })


# ═══════════════════════════════════════════════════════════════════════
# REMAINING CATEGORIES PLACEHOLDER
# ═══════════════════════════════════════════════════════════════════════


def generate_mormr_rpem_stimuli() -> None:
    """12 stimuli for opioid (MORMR) & prediction error (RPEM) pathways."""

    # ── 01: Strings warm consonant sustained — HIGH opioid ────────────
    pm = _pm_ensemble_chord([
        ([C4, E4, G4], STRINGS, 70),
        ([C3], CELLO, 65),
    ], 8.0)
    save(pm, "mormr_rpem", "01_strings_warm_consonant", {
        "description": "Strings+Cello C major legato, pp-mf, 8s",
        "expected": {
            "liking": "HIGH — sustained warm consonance",
            "pleasure": "HIGH — opioid pathway activation",
        },
        "science": "Putkinen 2025: sustained consonance -> MOR binding (d=4.8)",
    })

    # ── 02: Brass harsh dissonant sustained — LOW opioid ──────────────
    pm = _pm_ensemble_chord([
        ([C4, Db4, D4], TRUMPET, 100),
        ([C3, Db3], TROMBONE, 100),
    ], 8.0)
    save(pm, "mormr_rpem", "02_brass_harsh_dissonant", {
        "description": "Trumpet+Trombone cluster, ff, 8s",
        "expected": {
            "liking": "LOW — roughness blocks hedonic pathway",
            "pleasure": "LOW — dissonant texture",
        },
        "science": "Control: roughness inhibits opioid release",
    })

    # ── 03: Orch crescendo to chills — amplitude x beauty ─────────────
    pm = _pm_ensemble_crescendo(
        [([C4, E4, G4], STRINGS), ([C5], FLUTE), ([C3], CELLO)],
        n_beats=16, ioi=0.5, v_start=25, v_end=127)
    save(pm, "mormr_rpem", "03_orch_crescendo_chills", {
        "description": "Strings+Flute+Cello crescendo pp->fff, 8s",
        "expected": {
            "wanting": "RISING — crescendo builds anticipation",
            "chills_proximity": "RISING — approaching frisson threshold",
        },
        "science": "Putkinen 2025: amplitude x beauty -> chills",
    })

    # ── 04: Expected then pleasant surprise — positive RPE ────────────
    # 4 bars C major then unexpected Eb major 7th (pleasant surprise)
    pm = _pm_progression(
        [C_MAJ, C_MAJ, C_MAJ, C_MAJ, Eb_MAJ],
        [1.6, 1.6, 1.6, 1.6, 1.6], PIANO, 80)
    save(pm, "mormr_rpem", "04_pleasant_surprise", {
        "description": "Piano C major x4 -> unexpected Eb major, 8s",
        "expected": {
            "prediction_error": "HIGH at Eb — unexpected but consonant",
            "liking": "HIGH at Eb — pleasant chord",
        },
        "science": "Gold 2023: surprise x liked = VS activation (d=1.07)",
    })

    # ── 05: Expected then harsh surprise — negative RPE ───────────────
    cluster6 = chromatic_cluster(C4, 6)
    pm = _pm_progression(
        [C_MAJ, C_MAJ, C_MAJ, C_MAJ, cluster6],
        [1.6, 1.6, 1.6, 1.6, 1.6], PIANO, 80)
    save(pm, "mormr_rpem", "05_harsh_surprise", {
        "description": "Piano C major x4 -> chromatic cluster, 8s",
        "expected": {
            "prediction_error": "HIGH at cluster — unexpected + dissonant",
            "liking": "LOW at cluster — harsh",
        },
        "science": "Gold 2023: surprise x disliked = VS deactivation",
    })

    # ── 06: Fully predictable — LOW prediction error ──────────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    for rep in range(4):
        for i, p in enumerate([C4, E4, G4, E4]):
            t = rep * 2.0 + i * 0.5
            inst.notes.append(Note(velocity=75, pitch=p,
                                   start=t, end=t + 0.48))
    pm.instruments.append(inst)
    save(pm, "mormr_rpem", "06_fully_predictable", {
        "description": "Piano C-E-G-E arpeggio repeated 4x, 8s",
        "expected": {
            "prediction_error": "LOW — fully predictable after first cycle",
            "prediction_match": "HIGH — pattern confirmed",
        },
        "science": "Control: zero surprise baseline",
    })

    # ── 07: Medium complexity — optimal preference zone ───────────────
    pm = pretty_midi.PrettyMIDI()
    p_inst = pretty_midi.Instrument(program=PIANO)
    s_inst = pretty_midi.Instrument(program=STRINGS)
    mel = [C5, D5, E5, G5, F5, E5, D5, C5, D5, E5, G5, A5, G5, E5, D5, C5]
    t = 0.0
    for p in mel:
        p_inst.notes.append(Note(velocity=80, pitch=p,
                                  start=t, end=t + 0.48))
        t += 0.5
    # Strings: sustained harmony underneath
    chords = [C_MAJ, A_MIN, D_MIN, G_DOM7]
    for ci, ch in enumerate(chords):
        t0 = ci * 2.0
        for p in ch:
            s_inst.notes.append(Note(velocity=60, pitch=p,
                                      start=t0, end=t0 + 1.98))
    pm.instruments.extend([p_inst, s_inst])
    save(pm, "mormr_rpem", "07_medium_complexity", {
        "description": "Piano melody + Strings chords, moderate complexity, 8s",
        "expected": {
            "pleasure": "HIGH — optimal complexity zone (inverted-U peak)",
            "prediction_error": "MED — some surprise, not chaotic",
        },
        "science": "Gold 2019: inverted-U IC preference (R2=26.3%, N=70)",
    })

    # ── 08: Noise high entropy — chaos baseline ──────────────────────
    pm = _pm_dense_random(6.0, seed=60)
    save(pm, "mormr_rpem", "08_noise_high_entropy", {
        "description": "Dense random MIDI (noise-like, seed=60), 6s",
        "expected": {
            "pleasure": "LOW — chaotic = no reward",
            "prediction_error": "HIGH — unpredictable",
            "liking": "LOW — maximum incoherence",
        },
        "science": "Control: entropy ceiling for RPEM",
    })

    # ── 09: Strings rising pleasantness — opioid RISING ───────────────
    # Dissonant cluster -> consonant triad transition over 8s
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=STRINGS)
    # Phase 1 (0-4s): cluster [C4,Db4,D4] with decreasing roughness
    for p in [C4, Db4, D4]:
        inst.notes.append(Note(velocity=70, pitch=p, start=0.0, end=3.98))
    # Phase 2 (4-8s): consonant triad [C4,E4,G4]
    for p in [C4, E4, G4]:
        inst.notes.append(Note(velocity=70, pitch=p, start=4.0, end=7.98))
    pm.instruments.append(inst)
    save(pm, "mormr_rpem", "09_rising_pleasantness", {
        "description": "Strings cluster (4s) -> C major (4s), 8s",
        "expected": {
            "pleasure": "RISING — dissonant to consonant",
            "liking": "RISING — increasing hedonic quality",
        },
        "science": "Putkinen: rising hedonic trajectory -> MOR binding",
    })

    # ── 10: Piano falling pleasantness — opioid FALLING ───────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    for p in [C4, E4, G4]:
        inst.notes.append(Note(velocity=75, pitch=p, start=0.0, end=3.98))
    for p in chromatic_cluster(C4, 6):
        inst.notes.append(Note(velocity=75, pitch=p, start=4.0, end=7.98))
    pm.instruments.append(inst)
    save(pm, "mormr_rpem", "10_falling_pleasantness", {
        "description": "Piano C major (4s) -> chromatic cluster (4s), 8s",
        "expected": {
            "pleasure": "FALLING — consonant to dissonant",
            "liking": "FALLING — decreasing hedonic quality",
        },
        "science": "Inverse trajectory control",
    })

    # ── 11: Cello solo warm legato — warmth x pleasure ────────────────
    mel = [C4, D4, E4, F4, G4, F4, E4, D4, C4, E4]
    pm = _pm_melody(mel, [0.8] * 10, CELLO, 70)
    save(pm, "mormr_rpem", "11_cello_warm_legato", {
        "description": "Cello C major melody, legato, mf, 8s",
        "expected": {
            "liking": "HIGH — warm timbre + consonant melody",
            "pleasure": "HIGH — timbral warmth x pleasantness",
        },
        "science": "Putkinen 2025: timbral warmth -> MOR binding",
    })

    # ── 12: Organ warm with crescendo — opioid + arousal ──────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=ORGAN)
    for i in range(16):
        v = 40 + int(80 * i / 15)
        t = i * 0.5
        for p in [C4, E4, G4, B4]:
            inst.notes.append(Note(velocity=v, pitch=p,
                                   start=t, end=t + 0.48))
    pm.instruments.append(inst)
    save(pm, "mormr_rpem", "12_organ_warm_crescendo", {
        "description": "Organ C major 7th crescendo p->ff, 8s",
        "expected": {
            "wanting": "RISING — crescendo anticipation",
            "pleasure": "HIGH — warm timbre sustained",
            "chills_proximity": "RISING — opioid + arousal co-activation",
        },
        "science": "MOR + DA co-activation at warm crescendo",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 5: Cross-unit Integration (10 stimuli)
# ═══════════════════════════════════════════════════════════════════════

def generate_cross_stimuli() -> None:
    """10 stimuli testing SRP x DAED x SSRI cross-unit interactions."""

    # ── 01: Full arc: buildup->climax->resolution ─────────────────────
    pm = pretty_midi.PrettyMIDI()
    st = pretty_midi.Instrument(program=STRINGS)
    vc = pretty_midi.Instrument(program=CELLO)
    trp = pretty_midi.Instrument(program=TRUMPET)
    # Buildup (0-4s): strings crescendo on ii-V
    for i in range(8):
        v = 35 + int(55 * i / 7)
        t = i * 0.5
        chd = D_MIN if i < 4 else G_DOM7
        for p in chd:
            st.notes.append(Note(velocity=v, pitch=p, start=t, end=t + 0.48))
        vc.notes.append(Note(velocity=v, pitch=D3 if i < 4 else G3,
                             start=t, end=t + 0.48))
    # Climax (4-6s): trumpet + strings fff on I
    for p in [C5, E5, G5]:
        trp.notes.append(Note(velocity=127, pitch=p, start=4.0, end=5.98))
    for p in C_MAJ:
        st.notes.append(Note(velocity=120, pitch=p, start=4.0, end=5.98))
    vc.notes.append(Note(velocity=120, pitch=C3, start=4.0, end=5.98))
    # Resolution (6-10s): strings diminuendo
    for i in range(8):
        v = 100 - int(60 * i / 7)
        t = 6.0 + i * 0.5
        for p in C_MAJ:
            st.notes.append(Note(velocity=v, pitch=p, start=t, end=t + 0.48))
        vc.notes.append(Note(velocity=v, pitch=C3, start=t, end=t + 0.48))
    pm.instruments.extend([st, vc, trp])
    save(pm, "cross", "01_full_arc", {
        "description": "Strings+Cello+Trumpet: 4s buildup->2s climax->4s resolve, 10s",
        "expected": {
            "wanting": "RISING then FALLING — full reward arc",
            "liking": "LOW then HIGH then STABLE",
            "da_caudate": "HIGH in buildup, LOW at resolution",
            "da_nacc": "LOW then HIGH at climax",
            "peak_detection": "HIGH at 4s climax",
            "tension": "HIGH->LOW — full resolution",
        },
        "science": "Blood & Zatorre 2001: full musical arc = complete DA cycle",
    })

    # ── 02: Deceptive arc — wanting HIGH, liking LOW ──────────────────
    pm = pretty_midi.PrettyMIDI()
    st = pretty_midi.Instrument(program=STRINGS)
    vc = pretty_midi.Instrument(program=CELLO)
    # Buildup (0-6s) same as 01
    for i in range(12):
        v = 35 + int(75 * i / 11)
        t = i * 0.5
        chd = D_MIN if i < 6 else G_DOM7
        for p in chd:
            st.notes.append(Note(velocity=v, pitch=p, start=t, end=t + 0.48))
        vc.notes.append(Note(velocity=v, pitch=D3 if i < 6 else G3,
                             start=t, end=t + 0.48))
    # Deceptive: ff Am instead of C (6-8s)
    for p in A_MIN:
        st.notes.append(Note(velocity=110, pitch=p, start=6.0, end=7.98))
    vc.notes.append(Note(velocity=110, pitch=A2, start=6.0, end=7.98))
    pm.instruments.extend([st, vc])
    save(pm, "cross", "02_deceptive_arc", {
        "description": "Strings buildup 6s -> deceptive Am resolution, 8s",
        "expected": {
            "wanting": "HIGH — buildup creates strong wanting",
            "prediction_error": "HIGH — deceptive V->vi",
            "tension": "SUSTAINED — no true resolution",
            "dissociation_index": "HIGH — wanting without liking fulfillment",
        },
        "science": "Huron 2006: deceptive cadence = maximum expectation violation",
    })

    # ── 03: Double peak habituation — reward_forecast test ────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=STRINGS)
    # Peak 1 (0-4s): mf climax
    for i in range(8):
        v = 30 + int(50 * i / 7)
        t = i * 0.5
        for p in C_MAJ:
            inst.notes.append(Note(velocity=v, pitch=p, start=t, end=t + 0.48))
    # Valley (4-6s)
    for p in C_MAJ:
        inst.notes.append(Note(velocity=30, pitch=p, start=4.0, end=5.98))
    # Peak 2 (6-10s): fff climax
    for i in range(8):
        v = 30 + int(97 * i / 7)
        t = 6.0 + i * 0.5
        for p in C_MAJ:
            inst.notes.append(Note(velocity=v, pitch=p, start=t, end=t + 0.48))
    # Final sustain
    for p in C_MAJ:
        inst.notes.append(Note(velocity=127, pitch=p, start=10.0, end=11.98))
    pm.instruments.append(inst)
    save(pm, "cross", "03_double_peak_habituation", {
        "description": "Strings: peak1 mf -> valley -> peak2 fff, 12s",
        "expected": {
            "reward_forecast": "HIGHER at peak 2 — learned from peak 1",
            "peak_detection": "TWO PEAKS at 4s and 10s",
            "wanting": "STRONGER before peak 2",
        },
        "science": "Adaptation/sensitization: second peak amplifies forecast",
    })

    # ── 04: Monotonous loop — boredom/monotony ────────────────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    for rep in range(6):
        for i, p in enumerate([C4, E4, G4, E4]):
            t = rep * 2.0 + i * 0.5
            inst.notes.append(Note(velocity=70, pitch=p,
                                   start=t, end=t + 0.48))
    pm.instruments.append(inst)
    save(pm, "cross", "04_monotonous_loop", {
        "description": "Piano C-E-G-E pattern repeated 6x, 12s",
        "expected": {
            "wanting": "LOW — no buildup, pattern exhausted",
            "prediction_error": "NEAR ZERO after cycle 2",
            "pleasure": "DECREASING — monotony reduces hedonic value",
        },
        "science": "Berlyne 1971: repetition -> boredom, inverted-U violated",
    })

    # ── 05: Ensemble climax unison — group flow x peak ────────────────
    pm = pretty_midi.PrettyMIDI()
    for prog in [PIANO, STRINGS, FLUTE]:
        inst = pretty_midi.Instrument(program=prog)
        # Separate parts (0-4s)
        mel = diatonic_scale(C4 if prog == PIANO else
                             (E4 if prog == STRINGS else G4), 8)
        for i, p in enumerate(mel):
            inst.notes.append(Note(velocity=60, pitch=p,
                                   start=i * 0.5, end=i * 0.5 + 0.48))
        # Unison climax (4-6s): all on C major fff
        for p in [C5, E5, G5]:
            inst.notes.append(Note(velocity=127, pitch=p,
                                   start=4.0, end=5.98))
        # Resolution (6-8s): back to separate, pp
        for i, p in enumerate(mel[:4]):
            inst.notes.append(Note(velocity=40, pitch=p,
                                   start=6.0 + i * 0.5,
                                   end=6.0 + i * 0.5 + 0.48))
        pm.instruments.append(inst)
    save(pm, "cross", "05_ensemble_climax_unison", {
        "description": "3 instruments: separate -> unison fff -> separate pp, 8s",
        "expected": {
            "peak_detection": "HIGH at 4s unison moment",
            "pleasure": "PEAK at unison climax",
            "wanting": "RISING then FALLING",
        },
        "science": "Ni 2024 + Blood & Zatorre: group flow x peak = max reward",
    })

    # ── 06: Solo buildup -> ensemble resolution ───────────────────────
    pm = pretty_midi.PrettyMIDI()
    p_inst = pretty_midi.Instrument(program=PIANO)
    s_inst = pretty_midi.Instrument(program=STRINGS)
    fl_inst = pretty_midi.Instrument(program=FLUTE)
    # Solo piano buildup (0-5s)
    for i in range(10):
        v = 40 + int(50 * i / 9)
        t = i * 0.5
        chd = C_MAJ if i < 5 else G_DOM7
        for p in chd:
            p_inst.notes.append(Note(velocity=v, pitch=p,
                                     start=t, end=t + 0.48))
    # Full ensemble resolution (5-8s)
    for p in [C5, E5]:
        fl_inst.notes.append(Note(velocity=100, pitch=p, start=5.0, end=7.98))
    for p in C_MAJ:
        s_inst.notes.append(Note(velocity=100, pitch=p, start=5.0, end=7.98))
    for p in C_MAJ:
        p_inst.notes.append(Note(velocity=100, pitch=p, start=5.0, end=7.98))
    pm.instruments.extend([p_inst, s_inst, fl_inst])
    save(pm, "cross", "06_solo_to_ensemble", {
        "description": "Solo piano buildup 5s -> full ensemble resolution 3s",
        "expected": {
            "wanting": "RISING in solo buildup",
            "liking": "HIGH at ensemble entry",
            "da_nacc": "HIGH at ensemble resolution moment",
        },
        "science": "Dunbar 2012: social amplification of reward",
    })

    # ── 07: Complex fugue texture — medium IC ─────────────────────────
    pm = pretty_midi.PrettyMIDI()
    # 3-voice fugue-like texture: staggered entries of same subject
    subject = [C4, D4, E4, G4, F4, E4, D4, C4, E4, G4]
    durs = [0.5] * 10
    for idx, (prog, transpose) in enumerate([(PIANO, 0), (STRINGS, 7),
                                              (FLUTE, 12)]):
        inst = pretty_midi.Instrument(program=prog)
        entry_offset = idx * 1.5
        t = entry_offset
        for p, d in zip(subject, durs):
            if t + d < 10.0:
                inst.notes.append(Note(velocity=75, pitch=p + transpose,
                                       start=t, end=t + d - 0.02))
            t += d
        pm.instruments.append(inst)
    save(pm, "cross", "07_complex_fugue", {
        "description": "3-voice fugue (Piano+Strings+Flute), C major, ~10s",
        "expected": {
            "pleasure": "MED-HIGH — optimal complexity",
            "prediction_error": "MED — contrapuntal surprises",
        },
        "science": "Gold 2019: medium IC = peak preference",
    })

    # ── 08: Emotional peak with chills — DA + MOR synergy ─────────────
    pm = pretty_midi.PrettyMIDI()
    st = pretty_midi.Instrument(program=STRINGS)
    trp = pretty_midi.Instrument(program=TRUMPET)
    vc = pretty_midi.Instrument(program=CELLO)
    # Strings crescendo (0-7s)
    for i in range(14):
        v = 25 + int(85 * i / 13)
        t = i * 0.5
        for p in [C4, E4, G4]:
            st.notes.append(Note(velocity=v, pitch=p, start=t, end=t + 0.48))
        vc.notes.append(Note(velocity=v, pitch=C3, start=t, end=t + 0.48))
    # Brass entry at climax (7-10s) fff
    for p in [C5, E5, G5, C6]:
        trp.notes.append(Note(velocity=127, pitch=p, start=7.0, end=9.98))
    for p in [C4, E4, G4]:
        st.notes.append(Note(velocity=120, pitch=p, start=7.0, end=9.98))
    vc.notes.append(Note(velocity=120, pitch=C3, start=7.0, end=9.98))
    pm.instruments.extend([st, trp, vc])
    save(pm, "cross", "08_emotional_peak_chills", {
        "description": "Strings crescendo 7s + brass entry at fff climax, 10s",
        "expected": {
            "chills_proximity": "RISING through crescendo, PEAK at brass entry",
            "da_caudate": "HIGH during buildup",
            "da_nacc": "HIGH at brass climax",
            "peak_detection": "HIGH at 7s brass entry",
            "pleasure": "PEAK at climax",
        },
        "science": "Salimpoor + Putkinen: DA + MOR co-release at emotional peak",
    })

    # ── 09: Sparse to dense — texture accumulation ────────────────────
    pm = pretty_midi.PrettyMIDI()
    # Solo piano (0-3s)
    p_inst = pretty_midi.Instrument(program=PIANO)
    for i in range(6):
        p_inst.notes.append(Note(velocity=70, pitch=C4 + [0, 2, 4, 5, 7, 9][i],
                                 start=i * 0.5, end=i * 0.5 + 0.48))
    # Add strings (3-6s)
    s_inst = pretty_midi.Instrument(program=STRINGS)
    for i in range(6):
        t = 3.0 + i * 0.5
        p_inst.notes.append(Note(velocity=75, pitch=C4 + [0, 2, 4, 5, 7, 9][i],
                                 start=t, end=t + 0.48))
        s_inst.notes.append(Note(velocity=70, pitch=E4 + [0, 2, 4, 5, 7, 9][i],
                                 start=t, end=t + 0.48))
    # Add flute (6-10s)
    fl_inst = pretty_midi.Instrument(program=FLUTE)
    for i in range(8):
        t = 6.0 + i * 0.5
        p_inst.notes.append(Note(velocity=80, pitch=C4 + [0, 2, 4, 5, 7, 9, 11, 12][i],
                                 start=t, end=t + 0.48))
        s_inst.notes.append(Note(velocity=75, pitch=E4 + [0, 2, 4, 5, 7, 9, 11, 12][i],
                                 start=t, end=t + 0.48))
        fl_inst.notes.append(Note(velocity=80, pitch=G4 + [0, 2, 4, 5, 7, 9, 11, 12][i],
                                  start=t, end=t + 0.48))
    pm.instruments.extend([p_inst, s_inst, fl_inst])
    save(pm, "cross", "09_sparse_to_dense", {
        "description": "Solo piano -> duo -> trio accumulation, 10s",
        "expected": {
            "pleasure": "RISING — increasing textural richness",
            "wanting": "RISING — growing ensemble engagement",
        },
        "science": "Ni 2024: increasing coordination = rising reward",
    })

    # ── 10: Rich polyphonic resolution ────────────────────────────────
    pm = pretty_midi.PrettyMIDI()
    # 5-voice polyphonic texture -> unison cadence
    progs = [FLUTE, VIOLIN, STRINGS, CELLO, ORGAN]
    voices = [G5, E5, C5, G4, C4]
    for prog, pitch in zip(progs, voices):
        inst = pretty_midi.Instrument(program=prog)
        # Independent motion (0-5s)
        t = 0.0
        for i in range(10):
            p = pitch + [0, 2, -1, 3, 0, -2, 1, 4, 2, 0][i]
            inst.notes.append(Note(velocity=70, pitch=p,
                                   start=t, end=t + 0.48))
            t += 0.5
        # Unison cadence (5-8s): all converge on C major
        target = {FLUTE: G5, VIOLIN: E5, STRINGS: C5,
                  CELLO: G3, ORGAN: C3}
        inst.notes.append(Note(velocity=100, pitch=target[prog],
                               start=5.0, end=7.98))
        pm.instruments.append(inst)
    save(pm, "cross", "10_rich_polyphonic_resolution", {
        "description": "5-voice polyphonic texture -> unison C major cadence, 8s",
        "expected": {
            "pleasure": "RISING — convergence to consonance",
            "tension": "MED->LOW — independent motion resolves",
            "liking": "HIGH at cadential resolution",
        },
        "science": "Full reward system validation: polyphonic -> harmonic resolution",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 6: Boundary Conditions (8 stimuli)
# ═══════════════════════════════════════════════════════════════════════

def generate_boundary_stimuli() -> None:
    """8 edge-case stimuli to validate robustness for all 16 F6 beliefs."""

    # ── 01: Near-silence 2s ───────────────────────────────────────────
    pm = _pm_near_silence(2.0)
    save(pm, "boundary", "01_silence_2s", {
        "description": "Near-silence 2s — no NaN/Inf expected",
        "expected": "All 16 F6 beliefs valid, near baseline",
    })

    # ── 02: DC-like quiet note ────────────────────────────────────────
    pm = _pm_note(C4, 2.0, ORGAN, 5)
    save(pm, "boundary", "02_dc_like_quiet", {
        "description": "Organ C4 near-silence (v=5), 2s",
        "expected": "All beliefs valid, low activation",
    })

    # ── 03: Very short 0.1s ───────────────────────────────────────────
    pm = _pm_chord(C_MAJ, 0.1, PIANO, 80)
    save(pm, "boundary", "03_very_short", {
        "description": "Piano C major 0.1s — minimal duration",
        "expected": "All beliefs valid, pipeline handles short input",
    })

    # ── 04: Very long 10s ─────────────────────────────────────────────
    pm = _pm_chord(C_MAJ, 10.0, ORGAN, 70)
    save(pm, "boundary", "04_very_long", {
        "description": "Organ C major 10s — extended duration",
        "expected": "All beliefs valid, no memory overflow",
    })

    # ── 05: Maximum velocity ──────────────────────────────────────────
    pm = _pm_chord(C_MAJ, 4.0, PIANO, 127)
    save(pm, "boundary", "05_max_velocity", {
        "description": "Piano C major fff (v=127), 4s",
        "expected": "All beliefs valid, arousal near ceiling",
    })

    # ── 06: Minimum velocity ──────────────────────────────────────────
    pm = _pm_note(C4, 4.0, PIANO, 5)
    save(pm, "boundary", "06_min_velocity", {
        "description": "Piano C4 ppp (v=5), 4s",
        "expected": "All beliefs valid, near baseline",
    })

    # ── 07: Full 12-note chromatic cluster ─────────────────────────────
    pm = _pm_chord(chromatic_cluster(C4, 12), 5.0, PIANO, 100)
    save(pm, "boundary", "07_full_cluster_12note", {
        "description": "12-note chromatic cluster C4-B4, forte, 5s",
        "expected": "All beliefs valid, max inharmonicity",
    })

    # ── 08: Extreme register ──────────────────────────────────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=80, pitch=C1, start=0.0, end=4.0))
    inst.notes.append(Note(velocity=80, pitch=C7, start=0.0, end=4.0))
    pm.instruments.append(inst)
    save(pm, "boundary", "08_extreme_register", {
        "description": "Piano C1 + C7 simultaneously, 4s",
        "expected": "All beliefs valid, register extremes",
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
        # SRP — pleasure
        ("srp/03", "srp/04", "pleasure", "A>B",
         "Consonant ensemble > dissonant cluster for pleasure"),
        ("srp/01", "srp/02", "pleasure", "A>B",
         "Major cadence > minor lament for pleasure"),
        ("srp/18", "srp/08", "pleasure", "A>B",
         "Orch fff resolution > static pp for pleasure"),
        # SRP — liking
        ("srp/03", "srp/04", "liking", "A>B",
         "Consonant sustained > dissonant cluster for liking"),
        ("srp/09", "srp/10", "liking", "A>B",
         "Strings warm > brass harsh for liking"),
        ("srp/14", "srp/08", "liking", "A>B",
         "Tritone->P5 resolution second half > static pp for liking"),
        # SRP — tension
        ("srp/04", "srp/03", "tension", "A>B",
         "Dissonant cluster > consonant for tension"),
        ("srp/11", "srp/12", "tension", "A>B",
         "Unresolved V7 > resolved V7->I for sustained tension"),
        ("srp/10", "srp/09", "tension", "A>B",
         "Brass m2 > strings legato for tension"),
        ("srp/02", "srp/01", "tension", "A>B",
         "Minor lament > major cadence for tension"),
        # SRP — harmonic_tension
        ("srp/04", "srp/03", "harmonic_tension", "A>B",
         "Chromatic cluster > major chord for harmonic tension"),
        ("srp/11", "srp/03", "harmonic_tension", "A>B",
         "Dominant 7th > tonic triad for harmonic tension"),
        # SRP — prediction_error
        ("srp/05", "srp/06", "prediction_error", "A>B",
         "Huron 2006: deceptive V->vi > perfect V->I for PE"),
        ("srp/17", "srp/08", "prediction_error", "A>B",
         "Polyrhythm 3v4 > static note for PE"),
        # SRP — prediction_match
        ("srp/06", "srp/05", "prediction_match", "A>B",
         "Perfect cadence > deceptive cadence for prediction match"),
        # SRP — peak_detection
        ("srp/07", "srp/08", "peak_detection", "A>B",
         "Crescendo climax > static pp for peak detection"),
        ("srp/18", "srp/08", "peak_detection", "A>B",
         "Orch fff resolution > static pp for peak detection"),
        # SRP — wanting
        ("srp/07", "srp/08", "wanting", "A>B",
         "Crescendo > static for wanting (anticipatory buildup)"),
        # SRP — resolution_expectation
        ("srp/11", "srp/08", "resolution_expectation", "A>B",
         "V7 sustained > static note for resolution expectation"),
        # DAED — da_caudate
        ("daed/01", "daed/05", "da_caudate", "A>B",
         "Salimpoor 2011: crescendo > steady for caudate DA"),
        ("daed/03", "daed/05", "da_caudate", "A>B",
         "Buildup no resolution > steady for caudate DA"),
        ("daed/07", "daed/06", "da_caudate", "A>B",
         "Fast crescendo > slow crescendo for caudate DA"),
        # DAED — da_nacc
        ("daed/02", "daed/05", "da_nacc", "A>B",
         "Salimpoor 2011: sudden chord > steady for NAcc DA"),
        ("daed/13", "daed/14", "da_nacc", "A>B",
         "Brass fanfare fff > organ sustained for NAcc DA"),
        ("daed/04", "daed/05", "da_nacc", "A>B",
         "Pleasant surprise > steady for NAcc DA"),
        # DAED — dissociation_index
        ("daed/03", "daed/05", "dissociation_index", "A>B",
         "Berridge 2007: buildup-only > steady for dissociation"),
        ("daed/04", "daed/05", "dissociation_index", "A>B",
         "Surprise-only > steady for dissociation"),
        # DAED — wanting_ramp
        ("daed/01", "daed/09", "wanting_ramp", "A>B",
         "Crescendo > repetitive for wanting ramp"),
        ("daed/07", "daed/14", "wanting_ramp", "A>B",
         "Fast crescendo > organ sustained for wanting ramp"),
        ("daed/12", "daed/09", "wanting_ramp", "A>B",
         "Arpeggiated buildup > repetitive for wanting ramp"),
        # MORMR_RPEM — liking (opioid proxy)
        ("mormr_rpem/01", "mormr_rpem/02", "liking", "A>B",
         "Putkinen 2025: warm consonant > harsh dissonant for liking"),
        ("mormr_rpem/11", "mormr_rpem/08", "liking", "A>B",
         "Cello warm > noise for liking"),
        # MORMR_RPEM — pleasure
        ("mormr_rpem/07", "mormr_rpem/08", "pleasure", "A>B",
         "Gold 2019: medium complexity > noise for pleasure"),
        ("mormr_rpem/01", "mormr_rpem/02", "pleasure", "A>B",
         "Warm consonant > harsh dissonant for pleasure"),
        # MORMR_RPEM — prediction_error
        ("mormr_rpem/04", "mormr_rpem/06", "prediction_error", "A>B",
         "Gold 2023: pleasant surprise > predictable for PE"),
        ("mormr_rpem/05", "mormr_rpem/06", "prediction_error", "A>B",
         "Harsh surprise > predictable for PE"),
        ("mormr_rpem/08", "mormr_rpem/06", "prediction_error", "A>B",
         "Noise > predictable for PE"),
        # SSRI — wanting (ensemble vs solo proxy)
        ("ssri/01", "ssri/02", "wanting", "A>B",
         "Ni 2024: ensemble > solo for reward engagement"),
        ("ssri/05", "ssri/06", "pleasure", "A>B",
         "Unison ensemble > solo flute for pleasure"),
        ("ssri/07", "ssri/08", "wanting", "A>B",
         "Synchronized crescendo > asynchronous for wanting"),
        ("ssri/09", "ssri/10", "liking", "A>B",
         "Ensemble sustained > solo organ for liking"),
        ("ssri/11", "ssri/12", "wanting", "A>B",
         "Accelerando > ritardando for wanting"),
        # Cross-unit interactions
        ("cross/01", "cross/04", "pleasure", "A>B",
         "Full arc > monotonous loop for pleasure"),
        ("cross/01", "cross/02", "liking", "A>B",
         "Perfect resolution > deceptive for liking"),
        ("cross/05", "cross/04", "pleasure", "A>B",
         "Ensemble climax > monotonous for pleasure"),
        ("cross/08", "cross/04", "wanting", "A>B",
         "Emotional peak > monotonous for wanting"),
        ("cross/01", "cross/04", "da_nacc", "A>B",
         "Full arc climax > monotonous for NAcc DA"),
    ]

    lines = [
        "# F6 Reward & Motivation -- Stimulus Catalog",
        "",
        f"**Total stimuli:** {len(ALL_METADATA)}",
        f"**Ordinal comparisons:** {len(comparisons)}",
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
    print("Generating F6 Reward test audio...")
    print()

    print("[1/6] SRP -- Striatal Reward Pathway (18 stimuli)")
    generate_srp_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('srp/'))} files")

    print("[2/6] DAED -- Dopamine Anticipation-Experience Dissociation (15 stimuli)")
    generate_daed_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('daed/'))} files")

    print("[3/6] SSRI -- Social Synchrony Reward Integration (12 stimuli)")
    generate_ssri_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('ssri/'))} files")

    print("[4/6] MORMR+RPEM -- Opioid & Prediction Error (12 stimuli)")
    generate_mormr_rpem_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('mormr_rpem/'))} files")

    print("[5/6] Cross-unit Integration (10 stimuli)")
    generate_cross_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('cross/'))} files")

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
