"""Deterministic MIDI-based test-audio generator for F9 (Social Cognition).

Generates 52 stimuli across 5 categories for testing all 10 F9 beliefs:
  NSCP  — neural_synchrony (Core tau=0.65), catchiness_pred (Anticipation)
  SSRI  — synchrony_reward, social_bonding, group_flow,
           entrainment_quality, social_prediction_error (Appraisal),
           collective_pleasure_pred (Anticipation)
  DDSMI — social_coordination (Core tau=0.60), resource_allocation (Appraisal)

F9 Social Cognition has NO dedicated mechanisms (cross-function from F6/F7).
Beliefs observe relay fields populated by F6-Reward and F7-Motor mechanisms.

Science:
  Tarr Launay & Dunbar 2014 (N=264): synchronous dancing → endorphins
  Launay Tarr & Dunbar 2016 (N=94): synchrony → social bonding
  Bigand et al 2025 (EEG): mTRF social coordination in dancing brain
  Wohltjen et al 2023 (N=8): beat synchrony predicts social synchrony
  Ni et al 2024 (fNIRS N=528): social bonding → prefrontal synchrony
  Kohler et al 2025 (fMRI MVPA): self/other in joint piano
  Sabharwal et al 2024: leadership dynamics in musical groups
  Keller Novembre & Hove 2014: ensemble coordination framework (review)
  Williamson & Bonshor 2019 (N=346): wellbeing in brass bands
  Large et al 2023: dynamic models for rhythm perception (review)
  Koelsch 2014: neural substrates of music-evoked social emotions
  Chanda & Levitin 2013: neurochemistry of music (review)
  Novembre Ticini Schutz-Bosbach & Keller 2012 (N=20): motor simulation

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
C1 = 24
Db3, Eb3, Gb3, Ab3, Bb3 = 49, 51, 54, 56, 58
Db4, Eb4, Gb4, Ab4, Bb4 = 61, 63, 66, 68, 70
Db5, Eb5, Gb5, Ab5, Bb5 = 73, 75, 78, 80, 82
C7 = 96

# ── chord voicings ──────────────────────────────────────────────────
C_MAJ = [C4, E4, G4]
F_MAJ = [F3, A3, C4]
G_MAJ = [G3, B3, D4]
Am = [A3, C4, E4]
Dm = [D3, F3, A3]
G7 = [G3, B3, D4, F4]

# ── output ──────────────────────────────────────────────────────────
OUTPUT_DIR = _PROJECT_ROOT / "Test-Audio" / "micro_beliefs" / "f9"
ALL_METADATA: dict = {}

Note = pretty_midi.Note


# ═══════════════════════════════════════════════════════════════════
#  SAVE HELPER
# ═══════════════════════════════════════════════════════════════════

def save(pm: pretty_midi.PrettyMIDI, group: str, name: str,
         meta: dict, gain: float = 1.0) -> None:
    """Render MIDI -> WAV+MID, store metadata."""
    out = OUTPUT_DIR / group
    out.mkdir(parents=True, exist_ok=True)

    pm.write(str(out / f"{name}.mid"))

    audio = _render(pm)
    audio = audio * gain
    peak = audio.abs().max().item()
    if peak > 0:
        audio = audio * (0.95 / peak)
    audio = audio.clamp(-1.0, 1.0)

    pcm = (audio.squeeze(0).numpy() * 32767).astype(np.int16)
    wavfile.write(str(out / f"{name}.wav"), SAMPLE_RATE, pcm)

    ALL_METADATA[f"{group}/{name}"] = meta


# ═══════════════════════════════════════════════════════════════════
#  STANDARD MIDI BUILDER HELPERS
# ═══════════════════════════════════════════════════════════════════

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


# ═══════════════════════════════════════════════════════════════════
#  F9-SPECIFIC MIDI BUILDER HELPERS
# ═══════════════════════════════════════════════════════════════════

def _pm_duet_synchronized(melody1, melody2, durations,
                          prog1=PIANO, prog2=VIOLIN, vel=80):
    """Two instruments playing synchronized parallel melodies."""
    pm = pretty_midi.PrettyMIDI()
    inst1 = pretty_midi.Instrument(program=prog1)
    inst2 = pretty_midi.Instrument(program=prog2)
    t = 0.0
    for p1, p2, d in zip(melody1, melody2, durations):
        inst1.notes.append(Note(velocity=vel, pitch=p1,
                                start=t, end=t + d - 0.02))
        inst2.notes.append(Note(velocity=vel, pitch=p2,
                                start=t, end=t + d - 0.02))
        t += d
    pm.instruments.append(inst1)
    pm.instruments.append(inst2)
    return pm


def _pm_duet_offset(melody1, melody2, durations,
                    prog1=PIANO, prog2=VIOLIN, offset_s=0.05, vel=80):
    """Two instruments with timing offset (desynchronized)."""
    pm = pretty_midi.PrettyMIDI()
    inst1 = pretty_midi.Instrument(program=prog1)
    inst2 = pretty_midi.Instrument(program=prog2)
    t = 0.0
    for p1, p2, d in zip(melody1, melody2, durations):
        inst1.notes.append(Note(velocity=vel, pitch=p1,
                                start=t, end=t + d - 0.02))
        t2 = t + offset_s
        inst2.notes.append(Note(velocity=vel, pitch=p2,
                                start=t2, end=t2 + d - 0.02))
        t += d
    pm.instruments.append(inst1)
    pm.instruments.append(inst2)
    return pm


def _pm_call_response(call_notes, resp_notes, note_dur,
                      call_prog=PIANO, resp_prog=VIOLIN,
                      gap=0.05, vel=80):
    """Alternating call-response dialogue between two instruments."""
    pm = pretty_midi.PrettyMIDI()
    call_inst = pretty_midi.Instrument(program=call_prog)
    resp_inst = pretty_midi.Instrument(program=resp_prog)
    t = 0.0
    for cn, rn in zip(call_notes, resp_notes):
        call_inst.notes.append(Note(velocity=vel, pitch=cn,
                                    start=t, end=t + note_dur - 0.02))
        t += note_dur + gap
        resp_inst.notes.append(Note(velocity=vel, pitch=rn,
                                    start=t, end=t + note_dur - 0.02))
        t += note_dur + gap
    pm.instruments.append(call_inst)
    pm.instruments.append(resp_inst)
    return pm


def _pm_canon(melody, durations, prog1=PIANO, prog2=VIOLIN,
              delay_beats=2, vel=80):
    """Canon: second voice follows first by delay_beats notes."""
    pm = pretty_midi.PrettyMIDI()
    inst1 = pretty_midi.Instrument(program=prog1)
    inst2 = pretty_midi.Instrument(program=prog2)
    delay_time = sum(durations[:delay_beats])
    t = 0.0
    for p, d in zip(melody, durations):
        inst1.notes.append(Note(velocity=vel, pitch=p,
                                start=t, end=t + d - 0.02))
        t2 = t + delay_time
        if t2 + d < sum(durations) + delay_time + 2.0:
            inst2.notes.append(Note(velocity=vel, pitch=p,
                                    start=t2, end=t2 + d - 0.02))
        t += d
    pm.instruments.append(inst1)
    pm.instruments.append(inst2)
    return pm


def _pm_groove_bass_melody(bass_notes, bass_durs, melody_notes, melody_durs,
                           bass_prog=GUITAR_STEEL, melody_prog=PIANO,
                           bass_vel=90, melody_vel=80):
    """Groove with synchronized bass + melody layers."""
    pm = pretty_midi.PrettyMIDI()
    bass_inst = pretty_midi.Instrument(program=bass_prog)
    t = 0.0
    for p, d in zip(bass_notes, bass_durs):
        bass_inst.notes.append(Note(velocity=bass_vel, pitch=p,
                                    start=t, end=t + d - 0.02))
        t += d
    pm.instruments.append(bass_inst)

    melody_inst = pretty_midi.Instrument(program=melody_prog)
    t = 0.0
    for p, d in zip(melody_notes, melody_durs):
        melody_inst.notes.append(Note(velocity=melody_vel, pitch=p,
                                      start=t, end=t + d - 0.02))
        t += d
    pm.instruments.append(melody_inst)
    return pm


def _pm_interlocking(pattern1_pitches, pattern2_pitches, bpm, n_cycles,
                     prog1=PIANO, prog2=GUITAR_NYLON, vel=80):
    """Interlocking complementary rhythms — pattern1 on beats, pattern2 on offbeats."""
    ioi = 60.0 / bpm
    half_ioi = ioi / 2.0
    dur = half_ioi * 0.80
    pm = pretty_midi.PrettyMIDI()
    inst1 = pretty_midi.Instrument(program=prog1)
    inst2 = pretty_midi.Instrument(program=prog2)
    n1 = len(pattern1_pitches)
    n2 = len(pattern2_pitches)
    for cycle in range(n_cycles):
        for i, p in enumerate(pattern1_pitches):
            beat = cycle * n1 + i
            t = beat * ioi
            inst1.notes.append(Note(velocity=vel, pitch=p,
                                    start=t, end=t + dur))
        for i, p in enumerate(pattern2_pitches):
            beat = cycle * n2 + i
            t = beat * ioi + half_ioi
            inst2.notes.append(Note(velocity=vel, pitch=p,
                                    start=t, end=t + dur))
    pm.instruments.append(inst1)
    pm.instruments.append(inst2)
    return pm


# ═══════════════════════════════════════════════════════════════════
#  CATEGORY 1 — NSCP (Neural Synchrony Coupling Prediction)
# ═══════════════════════════════════════════════════════════════════

def generate_nscp_stimuli():
    """12 stimuli targeting neural_synchrony + catchiness_pred.

    Key R³ drivers: sensory_pleasantness[4], amplitude[7], loudness[8],
    onset_strength[10], tonalness[14], tristimulus[18:21].

    Wohltjen et al 2023 (N=8): beat synchrony predicts social synchrony.
    Ni et al 2024 (fNIRS N=528): social bonding → prefrontal synchrony.
    Leahy et al 2025 (review): music modulates inter-brain coupling.
    """
    stimuli = []

    # 01 — Synchronized ensemble groove: bass + piano + violin at 120 BPM
    ioi = 0.5  # 120 BPM quarters
    bass_notes = [C3, C3, G3, G3] * 4  # 16 beats
    bass_durs = [ioi] * 16
    melody_notes = [E5, G5, A5, G5, E5, D5, C5, D5] * 2
    melody_durs = [ioi] * 16
    pm = _pm_groove_bass_melody(bass_notes, bass_durs, melody_notes, melody_durs,
                                bass_prog=CELLO, melody_prog=VIOLIN,
                                bass_vel=85, melody_vel=80)
    # Add piano chords on beats 1 and 3
    piano = pretty_midi.Instrument(program=PIANO)
    for i in range(8):
        t = i * ioi * 2
        for p in C_MAJ:
            piano.notes.append(Note(velocity=75, pitch=p,
                                    start=t, end=t + ioi * 2 - 0.02))
    pm.instruments.append(piano)
    save(pm, "nscp", "01_ensemble_groove_synchronized", {
        "description": "Cello bass + violin melody + piano chords at 120 BPM. "
                       "Multi-voice synchronization with strong tonal structure.",
        "expected": {"neural_synchrony": "HIGH", "catchiness_pred": "MODERATE-HIGH"},
        "science": "Wohltjen et al 2023: beat synchrony predicts attentional synchrony."})
    stimuli.append("01_ensemble_groove_synchronized")

    # 02 — Solo piano rubato (no beat, single voice)
    rubato_notes = diatonic_scale(C4, 8) + list(reversed(diatonic_scale(C4, 8)))
    rubato_durs = [0.6, 0.4, 0.8, 0.3, 0.7, 0.5, 0.9, 0.4,
                   0.4, 0.9, 0.5, 0.7, 0.3, 0.8, 0.4, 0.6]
    pm = _pm_melody(rubato_notes, rubato_durs, program=PIANO, velocity=70)
    save(pm, "nscp", "02_solo_piano_rubato", {
        "description": "Single piano, ascending/descending scale with variable timing. "
                       "No clear beat, single voice — minimal synchrony affordance.",
        "expected": {"neural_synchrony": "LOW-MODERATE", "catchiness_pred": "LOW"},
        "science": "Wohltjen 2023: synchrony requires predictable temporal structure."})
    stimuli.append("02_solo_piano_rubato")

    # 03 — Choir unison sustained (maximum coherence)
    pm = _pm_ensemble_chord([
        ([C4], CHOIR, 80),
        ([C5], CHOIR, 75),
        ([G4], STRINGS, 70),
        ([E4], STRINGS, 70),
    ], 6.0)
    save(pm, "nscp", "03_choir_unison_sustained", {
        "description": "Choir + strings sustained on C major chord. "
                       "Maximum timbral coherence, tonal stability.",
        "expected": {"neural_synchrony": "MODERATE-HIGH"},
        "science": "Ni et al 2024: social bonding activates prefrontal synchrony (N=528)."})
    stimuli.append("03_choir_unison_sustained")

    # 04 — Dense independent polyphony (3 independent voices)
    voice1 = [C5, E5, G5, A5, G5, E5, D5, C5]
    voice2 = [E4, G4, B4, C5, A4, F4, G4, E4]
    voice3 = [C3, G3, E3, C3, D3, F3, G3, C3]
    pm = pretty_midi.PrettyMIDI()
    # Voice 1 — flute, slightly different durations
    flute = pretty_midi.Instrument(program=FLUTE)
    t = 0.0
    for p in voice1 * 2:
        d = 0.45
        flute.notes.append(Note(velocity=75, pitch=p, start=t, end=t + d))
        t += 0.5
    pm.instruments.append(flute)
    # Voice 2 — violin, offset rhythm
    vln = pretty_midi.Instrument(program=VIOLIN)
    t = 0.25
    for p in voice2 * 2:
        d = 0.35
        vln.notes.append(Note(velocity=70, pitch=p, start=t, end=t + d))
        t += 0.55
    pm.instruments.append(vln)
    # Voice 3 — cello, slow
    vcl = pretty_midi.Instrument(program=CELLO)
    t = 0.0
    for p in voice3:
        d = 0.9
        vcl.notes.append(Note(velocity=80, pitch=p, start=t, end=t + d))
        t += 1.0
    pm.instruments.append(vcl)
    save(pm, "nscp", "04_dense_independent_polyphony", {
        "description": "3 independent voices (flute, violin, cello) with different rhythms. "
                       "Rich texture but limited synchronization cues.",
        "expected": {"neural_synchrony": "MODERATE"},
        "science": "Keller et al 2014: independent voices reduce synchronization affordance."})
    stimuli.append("04_dense_independent_polyphony")

    # 05 — Strong beat emphasis (bass-heavy groove)
    pm = pretty_midi.PrettyMIDI()
    bass = pretty_midi.Instrument(program=GUITAR_STEEL)
    for i in range(16):
        t = i * 0.5
        vel = 100 if i % 4 == 0 else (85 if i % 2 == 0 else 65)
        bass.notes.append(Note(velocity=vel, pitch=C3,
                               start=t, end=t + 0.4))
    pm.instruments.append(bass)
    # Add melodic layer
    mel_inst = pretty_midi.Instrument(program=PIANO)
    mel = [E4, G4, C5, G4] * 4
    for i, p in enumerate(mel):
        t = i * 0.5
        mel_inst.notes.append(Note(velocity=75, pitch=p,
                                   start=t, end=t + 0.4))
    pm.instruments.append(mel_inst)
    save(pm, "nscp", "05_groove_strong_beat", {
        "description": "Bass-heavy groove with strong metric hierarchy (accented beats 1,3). "
                       "Piano melody layer synchronized. Strong entrainment cue.",
        "expected": {"neural_synchrony": "HIGH", "catchiness_pred": "HIGH"},
        "science": "Large et al 2023: beat perception enables prediction and coordination."})
    stimuli.append("05_groove_strong_beat")

    # 06 — Arrhythmic atonal (no beat, no tonal center)
    rng = np.random.RandomState(609)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for _ in range(20):
        p = int(rng.randint(48, 85))
        d = float(rng.uniform(0.15, 0.9))
        gap = float(rng.uniform(0.05, 0.6))
        inst.notes.append(Note(velocity=70, pitch=p,
                               start=t, end=t + d))
        t += d + gap
    pm.instruments.append(inst)
    save(pm, "nscp", "06_arrhythmic_atonal", {
        "description": "Random chromatic pitches with random timing. "
                       "No beat, no tonal center, no repetition — minimal social cues.",
        "expected": {"neural_synchrony": "LOW", "catchiness_pred": "LOW"},
        "science": "Wohltjen 2023: synchrony requires predictable temporal structure."})
    stimuli.append("06_arrhythmic_atonal")

    # 07 — Catchy repetitive hook (4-note loop, 8 repetitions)
    hook = [E4, G4, A4, G4]
    hook_durs = [0.25, 0.25, 0.5, 0.5]
    pm = _pm_melody(hook * 8, hook_durs * 8, program=BRIGHT_PIANO, velocity=85)
    save(pm, "nscp", "07_catchy_repetitive_hook", {
        "description": "4-note hook [E4-G4-A4-G4] repeated 8 times. "
                       "Maximum repetitiveness — high catchiness affordance.",
        "expected": {"catchiness_pred": "HIGH", "neural_synchrony": "MODERATE-HIGH"},
        "science": "Savage et al 2021: repetition is a cross-cultural music universal."})
    stimuli.append("07_catchy_repetitive_hook")

    # 08 — Complex non-repetitive melody (16 unique notes)
    complex_notes = [C4, Eb4, G4, Bb4, Db5, E5, Ab4, B4,
                     D5, F4, A4, Gb4, Bb4, D4, F5, Ab4]
    complex_durs = [0.35, 0.45, 0.3, 0.55, 0.4, 0.25, 0.6, 0.35,
                    0.5, 0.3, 0.4, 0.55, 0.3, 0.45, 0.35, 0.5]
    pm = _pm_melody(complex_notes, complex_durs, program=PIANO, velocity=75)
    save(pm, "nscp", "08_complex_non_repetitive", {
        "description": "16 unique chromatic notes with varied durations. "
                       "No repetition, no tonal center — low catchiness.",
        "expected": {"catchiness_pred": "LOW", "neural_synchrony": "LOW-MODERATE"},
        "science": "Savage 2021: non-repetitive structure reduces group synchrony."})
    stimuli.append("08_complex_non_repetitive")

    # 09 — Unison octaves multi-instrument (3 voices)
    pm = _pm_ensemble_isochronous([
        (C4, PIANO, 80),
        (C5, VIOLIN, 75),
        (C3, CELLO, 85),
    ], 120.0, 16)
    save(pm, "nscp", "09_unison_octaves_multi", {
        "description": "Piano C4 + violin C5 + cello C3 in perfect octave unison at 120 BPM. "
                       "Maximum inter-voice synchronization.",
        "expected": {"neural_synchrony": "HIGH"},
        "science": "Novembre & Keller 2014: synchronized voices enhance neural coupling."})
    stimuli.append("09_unison_octaves_multi")

    # 10 — Desynchronized random entries
    rng = np.random.RandomState(610)
    pm = pretty_midi.PrettyMIDI()
    for prog, pitch in [(PIANO, C4), (VIOLIN, E5), (FLUTE, G5)]:
        inst = pretty_midi.Instrument(program=prog)
        for _ in range(8):
            t = float(rng.uniform(0.0, 7.0))
            d = float(rng.uniform(0.2, 0.8))
            inst.notes.append(Note(velocity=75, pitch=pitch,
                                   start=t, end=t + d))
        pm.instruments.append(inst)
    save(pm, "nscp", "10_desynchronized_random_entries", {
        "description": "3 instruments entering at random times. Same pitches "
                       "but no temporal coordination — desynchronized texture.",
        "expected": {"neural_synchrony": "LOW"},
        "science": "Keller 2014: temporal alignment is prerequisite for coordination."})
    stimuli.append("10_desynchronized_random_entries")

    # 11 — Two voices parallel thirds
    voice_top = [E4, F4, G4, A4, B4, C5, D5, E5] * 2
    voice_bot = [C4, D4, E4, F4, G4, A4, B4, C5] * 2
    durs = [0.5] * 16
    pm = _pm_duet_synchronized(voice_bot, voice_top, durs,
                               prog1=PIANO, prog2=VIOLIN, vel=80)
    save(pm, "nscp", "11_two_voices_parallel_thirds", {
        "description": "Piano + violin ascending in parallel thirds, synchronized. "
                       "Two-voice coordination with harmonic consonance.",
        "expected": {"neural_synchrony": "MODERATE-HIGH"},
        "science": "Kohler et al 2025: parallel self/other representations in joint piano."})
    stimuli.append("11_two_voices_parallel_thirds")

    # 12 — Single note metronomic
    pm = _pm_isochronous(C4, 120.0, 16, program=PIANO, velocity=80)
    save(pm, "nscp", "12_single_note_metronomic", {
        "description": "Single C4 piano, isochronous at 120 BPM. "
                       "Perfect regularity but no timbral richness or multi-voice.",
        "expected": {"neural_synchrony": "MODERATE", "catchiness_pred": "LOW-MODERATE"},
        "science": "Large 2023: isochronous regularity entrains cortical oscillations."})
    stimuli.append("12_single_note_metronomic")

    return stimuli


# ═══════════════════════════════════════════════════════════════════
#  CATEGORY 2 — SSRI (Social Synchrony Reward Integration)
# ═══════════════════════════════════════════════════════════════════

def generate_ssri_stimuli():
    """14 stimuli targeting synchrony_reward, social_bonding, group_flow,
    entrainment_quality, social_prediction_error, collective_pleasure_pred.

    Key R³ drivers: sensory_pleasantness[4], amplitude[7], loudness[8],
    onset_strength[10], warmth[12], tonalness[14], x_l5l6[41:49].

    Tarr et al 2014 (N=264): synchronous dancing → endorphin release.
    Launay et al 2016 (N=94): synchrony → social bonding via endorphins.
    Williamson & Bonshor 2019 (N=346): wellbeing in brass bands.
    Chanda & Levitin 2013: neurochemistry of music (DA, oxytocin, endorphins).
    Koelsch 2014: neural substrates of music-evoked social emotions.
    """
    stimuli = []

    # 01 — Dance groove energetic (bass + melody + rhythm at 120 BPM)
    ioi = 0.5
    bass = [C3, C3, G3, G3, F3, F3, G3, G3] * 2
    mel = [C5, E5, G5, C5, A4, C5, G4, A4] * 2
    pm = _pm_groove_bass_melody(bass, [ioi]*16, mel, [ioi]*16,
                                bass_prog=GUITAR_STEEL, melody_prog=BRIGHT_PIANO,
                                bass_vel=95, melody_vel=85)
    # Add rhythm layer
    rhythm = pretty_midi.Instrument(program=HARPSICHORD)
    for i in range(32):
        t = i * 0.25
        vel = 80 if i % 4 == 0 else 55
        rhythm.notes.append(Note(velocity=vel, pitch=E4,
                                 start=t, end=t + 0.15))
    pm.instruments.append(rhythm)
    save(pm, "ssri", "01_dance_groove_energetic", {
        "description": "Energetic dance groove: steel guitar bass + bright piano melody + "
                       "harpsichord rhythm at 120 BPM. Strong entrainment.",
        "expected": {"synchrony_reward": "HIGH", "entrainment_quality": "HIGH",
                     "group_flow": "HIGH"},
        "science": "Tarr et al 2014: synchronous dancing → endorphin release (N=264)."})
    stimuli.append("01_dance_groove_energetic")

    # 02 — Warm ballad at 60 BPM (strings + piano)
    ioi_slow = 1.0
    chords = [C_MAJ, Am, F_MAJ, G_MAJ] * 2
    pm = _pm_progression(chords, [ioi_slow]*8, program=STRINGS, velocity=65)
    mel_inst = pretty_midi.Instrument(program=PIANO)
    mel_notes = [E5, D5, C5, D5, C5, A4, G4, A4]
    t = 0.0
    for p in mel_notes:
        mel_inst.notes.append(Note(velocity=70, pitch=p,
                                   start=t, end=t + ioi_slow - 0.02))
        t += ioi_slow
    pm.instruments.append(mel_inst)
    save(pm, "ssri", "02_ballad_warm_60bpm", {
        "description": "Slow warm ballad: strings harmony + piano melody at 60 BPM. "
                       "High sensory_pleasantness, warm timbral quality.",
        "expected": {"social_bonding": "HIGH", "collective_pleasure_pred": "MODERATE-HIGH"},
        "science": "Launay et al 2016: synchronous bonding via endorphin release (N=94)."})
    stimuli.append("02_ballad_warm_60bpm")

    # 03 — Full ensemble harmonic resolution
    pm = _pm_ensemble_chord([
        ([C3, G3], CELLO, 85),
        ([E4, G4, C5], STRINGS, 75),
        ([C5, E5], VIOLIN, 70),
        ([G4], FLUTE, 70),
        ([C4, E4, G4], PIANO, 65),
    ], 6.0)
    save(pm, "ssri", "03_full_ensemble_harmony", {
        "description": "Full ensemble sustained C major chord: cello + strings + violin + "
                       "flute + piano. Maximum timbral richness and consonance.",
        "expected": {"social_bonding": "HIGH", "collective_pleasure_pred": "HIGH",
                     "group_flow": "MODERATE-HIGH"},
        "science": "Williamson & Bonshor 2019: group music making → social cohesion (N=346)."})
    stimuli.append("03_full_ensemble_harmony")

    # 04 — Single cold isolated tone
    pm = _pm_note(C3, 6.0, program=ORGAN, velocity=50)
    save(pm, "ssri", "04_single_cold_isolated", {
        "description": "Single C3 organ tone, sustained 6s, low velocity. "
                       "Minimal timbral richness, cold quality.",
        "expected": {"social_bonding": "LOW", "synchrony_reward": "LOW",
                     "collective_pleasure_pred": "LOW"},
        "science": "Koelsch 2014: social reward requires multi-voice interaction."})
    stimuli.append("04_single_cold_isolated")

    # 05 — Strong beat percussion-like pattern (4/4 accented)
    pm = pretty_midi.PrettyMIDI()
    perc = pretty_midi.Instrument(program=PIANO)
    for i in range(24):
        t = i * (60.0 / 120.0 / 2)  # Eighth notes at 120 BPM
        vel = 100 if i % 8 == 0 else (90 if i % 4 == 0 else (70 if i % 2 == 0 else 50))
        perc.notes.append(Note(velocity=vel, pitch=C4,
                               start=t, end=t + 0.1))
    pm.instruments.append(perc)
    save(pm, "ssri", "05_strong_beat_percussion", {
        "description": "Percussion-like pattern with strong metric hierarchy: "
                       "beat 1 > beat 3 > offbeats. High onset_strength.",
        "expected": {"entrainment_quality": "HIGH", "synchrony_reward": "MODERATE"},
        "science": "Large et al 2023: metrical hierarchy entrains cortical oscillations."})
    stimuli.append("05_strong_beat_percussion")

    # 06 — Free tempo rubato (no beat)
    notes_rubato = [G4, A4, B4, C5, E5, D5, B4, G4]
    durs_rubato = [0.7, 0.3, 0.9, 0.4, 0.8, 0.5, 1.1, 0.6]
    pm = _pm_melody(notes_rubato, durs_rubato, program=FLUTE, velocity=65)
    save(pm, "ssri", "06_free_tempo_rubato", {
        "description": "Flute melody with highly variable timing. "
                       "No clear beat — minimal entrainment affordance.",
        "expected": {"entrainment_quality": "LOW", "synchrony_reward": "LOW"},
        "science": "Large 2023: entrainment requires temporal regularity."})
    stimuli.append("06_free_tempo_rubato")

    # 07 — Building crescendo (solo → ensemble)
    pm = pretty_midi.PrettyMIDI()
    # Phase 1: solo piano (0-3s)
    p_inst = pretty_midi.Instrument(program=PIANO)
    for i in range(6):
        t = i * 0.5
        p_inst.notes.append(Note(velocity=55, pitch=C4 + (i % 5) * 2,
                                 start=t, end=t + 0.45))
    pm.instruments.append(p_inst)
    # Phase 2: add strings (3-5s)
    s_inst = pretty_midi.Instrument(program=STRINGS)
    for i in range(4):
        t = 3.0 + i * 0.5
        for p in [C4, E4, G4]:
            s_inst.notes.append(Note(velocity=70, pitch=p,
                                     start=t, end=t + 0.45))
    pm.instruments.append(s_inst)
    # Phase 3: full ensemble (5-8s)
    for prog, pitch, vel in [(CELLO, C3, 85), (VIOLIN, E5, 80),
                              (FLUTE, G5, 75), (TRUMPET, C5, 80)]:
        inst = pretty_midi.Instrument(program=prog)
        for i in range(6):
            t = 5.0 + i * 0.5
            inst.notes.append(Note(velocity=vel, pitch=pitch,
                                   start=t, end=t + 0.45))
        pm.instruments.append(inst)
    save(pm, "ssri", "07_building_crescendo", {
        "description": "Gradual build from solo piano to full ensemble over 8s. "
                       "Increasing timbral richness and group cohesion.",
        "expected": {"group_flow": "MODERATE-HIGH", "social_bonding": "MODERATE-HIGH"},
        "science": "Chanda & Levitin 2013: orchestral crescendo engages reward circuitry."})
    stimuli.append("07_building_crescendo")

    # 08 — Sudden silence after groove (prediction error)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # 3 seconds of groove then stop
    for i in range(12):
        t = i * 0.25
        vel = 85 if i % 4 == 0 else 65
        inst.notes.append(Note(velocity=vel, pitch=C4 if i % 2 == 0 else E4,
                               start=t, end=t + 0.2))
    # 3 seconds silence (no notes)
    pm.instruments.append(inst)
    save(pm, "ssri", "08_sudden_silence_after_groove", {
        "description": "3s groove at 240 BPM then 3s abrupt silence. "
                       "Prediction error at the boundary.",
        "expected": {"social_prediction_error": "MODERATE-HIGH"},
        "science": "Koelsch 2014: unexpected silence generates social prediction error."})
    stimuli.append("08_sudden_silence_after_groove")

    # 09 — Tension to resolution (V7 → I)
    tension = dominant_seventh(G3)  # G7
    resolution = major_triad(C4)     # C major
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=STRINGS)
    # Tension: 3s
    for p in tension:
        inst.notes.append(Note(velocity=80, pitch=p, start=0.0, end=3.0))
    # Resolution: 3s
    for p in resolution:
        inst.notes.append(Note(velocity=85, pitch=p, start=3.0, end=6.0))
    pm.instruments.append(inst)
    save(pm, "ssri", "09_tension_resolution", {
        "description": "G7 tension (3s) → C major resolution (3s) in strings. "
                       "Classic tension-resolution arc.",
        "expected": {"collective_pleasure_pred": "MODERATE-HIGH",
                     "social_prediction_error": "MODERATE"},
        "science": "Koelsch 2014: harmonic resolution activates reward circuitry."})
    stimuli.append("09_tension_resolution")

    # 10 — Unresolved dissonance (sustained)
    cluster = chromatic_cluster(C4, 5)
    pm = _pm_chord(cluster, 6.0, program=ORGAN, velocity=75)
    save(pm, "ssri", "10_unresolved_dissonance", {
        "description": "5-note chromatic cluster on organ sustained 6s. "
                       "High dissonance, no resolution — minimal pleasure.",
        "expected": {"collective_pleasure_pred": "LOW",
                     "social_bonding": "LOW"},
        "science": "Koelsch 2014: unresolved dissonance reduces reward activation."})
    stimuli.append("10_unresolved_dissonance")

    # 11 — Repetitive catchy hook with harmony
    hook = [E4, G4, A4, G4]
    hook_durs = [0.25, 0.25, 0.5, 0.5]
    pm = _pm_melody(hook * 6, hook_durs * 6, program=BRIGHT_PIANO, velocity=85)
    # Add bass support
    bass_inst = pretty_midi.Instrument(program=GUITAR_STEEL)
    for i in range(6):
        t = i * 1.5
        bass_inst.notes.append(Note(velocity=80, pitch=C3,
                                    start=t, end=t + 1.45))
    pm.instruments.append(bass_inst)
    save(pm, "ssri", "11_repetitive_catchy_hook", {
        "description": "Catchy 4-note hook with bass support, repeated 6 times. "
                       "High repetitiveness + tonal grounding.",
        "expected": {"synchrony_reward": "HIGH", "catchiness_pred": "HIGH"},
        "science": "Savage 2021: repetition is universal music feature linked to group bonding."})
    stimuli.append("11_repetitive_catchy_hook")

    # 12 — Complex jazz harmony (ii-V-I with extensions)
    jazz_chords = [
        [D3, F3, A3, C4, E4],    # Dm9
        [G3, B3, D4, F4, Ab4],   # G7b9
        [C3, E3, G3, B3, D4],    # Cmaj9
        [F3, A3, C4, E4, G4],    # Fmaj9
    ]
    pm = _pm_progression(jazz_chords, [1.5]*4, program=PIANO, velocity=70)
    save(pm, "ssri", "12_complex_jazz_harmony", {
        "description": "Jazz ii-V-I-IV progression with 9th extensions. "
                       "Complex harmony, moderate predictability.",
        "expected": {"collective_pleasure_pred": "MODERATE",
                     "social_bonding": "MODERATE"},
        "science": "Koelsch 2014: complex harmony engages social cognition differently."})
    stimuli.append("12_complex_jazz_harmony")

    # 13 — Lullaby gentle rocking (6/8 feel)
    lullaby_notes = [C5, E5, G5, E5, C5, G4] * 3
    lullaby_durs = [0.33, 0.33, 0.34, 0.33, 0.33, 0.34] * 3
    pm = _pm_melody(lullaby_notes, lullaby_durs, program=FLUTE, velocity=55)
    # Add soft sustained strings
    strings = pretty_midi.Instrument(program=STRINGS)
    for p in [C4, E4, G4]:
        strings.notes.append(Note(velocity=45, pitch=p, start=0.0, end=6.0))
    pm.instruments.append(strings)
    save(pm, "ssri", "13_lullaby_gentle_rocking", {
        "description": "Gentle 6/8 lullaby: flute arpeggios over sustained string pad. "
                       "Calming, rhythmic, socially affiliative.",
        "expected": {"social_bonding": "MODERATE-HIGH", "entrainment_quality": "MODERATE"},
        "science": "Nguyen et al 2023: infant-directed music enables co-regulation and bonding."})
    stimuli.append("13_lullaby_gentle_rocking")

    # 14 — March energetic strong beat
    ioi_march = 60.0 / 120.0
    pm = pretty_midi.PrettyMIDI()
    # Brass melody
    brass = pretty_midi.Instrument(program=TRUMPET)
    march_mel = [C5, C5, E5, G5, E5, C5, G4, C5] * 2
    t = 0.0
    for p in march_mel:
        brass.notes.append(Note(velocity=90, pitch=p,
                                start=t, end=t + ioi_march * 0.85))
        t += ioi_march
    pm.instruments.append(brass)
    # Bass
    tuba = pretty_midi.Instrument(program=TROMBONE)
    bass_march = [C3, G3, C3, G3] * 4
    t = 0.0
    for p in bass_march:
        tuba.notes.append(Note(velocity=95, pitch=p,
                                start=t, end=t + ioi_march * 0.85))
        t += ioi_march
    pm.instruments.append(tuba)
    save(pm, "ssri", "14_march_energetic_strong", {
        "description": "March rhythm: trumpet melody + trombone bass at 120 BPM. "
                       "Strong beat, high energy, military-style coordination.",
        "expected": {"entrainment_quality": "HIGH", "synchrony_reward": "HIGH",
                     "group_flow": "MODERATE-HIGH"},
        "science": "Tarr 2014: synchronized movement → endorphin release and bonding."})
    stimuli.append("14_march_energetic_strong")

    return stimuli


# ═══════════════════════════════════════════════════════════════════
#  CATEGORY 3 — DDSMI (Dyadic Directional Social Movement Integration)
# ═══════════════════════════════════════════════════════════════════

def generate_ddsmi_stimuli():
    """10 stimuli targeting social_coordination + resource_allocation.

    Key R³ drivers: onset_strength[10], amplitude[7], spectral_flux[21],
    tristimulus[18:21], x_l4l5[33:41].

    Bigand et al 2025 (EEG): mTRF disentangles social coordination.
    Kohler et al 2025 (fMRI MVPA): self/other in joint piano.
    Keller et al 2014: ensemble coordination framework (review).
    Novembre et al 2012 (N=20): motor simulation in action observation.
    Sabharwal et al 2024: leadership dynamics in string quartets.
    """
    stimuli = []

    # 01 — Two instruments perfectly synchronized (duet in 3rds)
    mel1 = [C4, D4, E4, F4, G4, A4, B4, C5] * 2
    mel2 = [E4, F4, G4, A4, B4, C5, D5, E5] * 2
    durs = [0.5] * 16
    pm = _pm_duet_synchronized(mel1, mel2, durs,
                               prog1=PIANO, prog2=VIOLIN, vel=80)
    save(pm, "ddsmi", "01_duet_perfectly_synchronized", {
        "description": "Piano + violin ascending parallel thirds in perfect synchrony. "
                       "Two-voice coordination with harmonic consonance.",
        "expected": {"social_coordination": "HIGH", "resource_allocation": "MODERATE-HIGH"},
        "science": "Kohler et al 2025: parallel self/other representations in joint piano (fMRI MVPA)."})
    stimuli.append("01_duet_perfectly_synchronized")

    # 02 — Two instruments with timing offset (50ms desync)
    pm = _pm_duet_offset(mel1, mel2, durs,
                         prog1=PIANO, prog2=VIOLIN, offset_s=0.05, vel=80)
    save(pm, "ddsmi", "02_duet_timing_offset", {
        "description": "Same parallel thirds melody with 50ms timing offset. "
                       "Degraded synchronization quality.",
        "expected": {"social_coordination": "MODERATE"},
        "science": "Keller 2014: temporal precision critical for ensemble coordination."})
    stimuli.append("02_duet_timing_offset")

    # 03 — Canon (follower delayed by 2 beats)
    canon_mel = diatonic_scale(C4, 8) + list(reversed(diatonic_scale(C4, 8)))
    canon_durs = [0.5] * 16
    pm = _pm_canon(canon_mel, canon_durs,
                   prog1=PIANO, prog2=FLUTE, delay_beats=2, vel=80)
    save(pm, "ddsmi", "03_canon_leader_follower", {
        "description": "Canon: piano leads, flute follows 2 beats later. "
                       "Leader-follower imitation pattern.",
        "expected": {"social_coordination": "MODERATE-HIGH"},
        "science": "Sabharwal et al 2024: leadership dynamics modulate coordination in quartets."})
    stimuli.append("03_canon_leader_follower")

    # 04 — Call-response dialogue
    call = [C4, E4, G4, C5, G4, E4, C4, E4]
    resp = [G4, B4, D5, G5, D5, B4, G4, B4]
    pm = _pm_call_response(call, resp, note_dur=0.4,
                           call_prog=PIANO, resp_prog=VIOLIN, gap=0.05, vel=80)
    save(pm, "ddsmi", "04_call_response_dialogue", {
        "description": "Musical dialogue: piano calls, violin responds, alternating 8 exchanges. "
                       "Turn-taking coordination pattern.",
        "expected": {"social_coordination": "HIGH", "resource_allocation": "HIGH"},
        "science": "Novembre et al 2012: action-observation coupling in joint music (N=20)."})
    stimuli.append("04_call_response_dialogue")

    # 05 — Interlocking complementary rhythms (hemiola-like)
    pattern1 = [C4, E4, G4, C4]
    pattern2 = [G4, B4, D5, G4]
    pm = _pm_interlocking(pattern1, pattern2, 120.0, 4,
                          prog1=PIANO, prog2=GUITAR_NYLON, vel=80)
    save(pm, "ddsmi", "05_interlocking_rhythms", {
        "description": "Piano on beats + guitar on offbeats, interlocking pattern. "
                       "Complementary rhythmic coordination.",
        "expected": {"social_coordination": "HIGH", "resource_allocation": "HIGH"},
        "science": "Bigand et al 2025: interlocking movement patterns in dyadic dance."})
    stimuli.append("05_interlocking_rhythms")

    # 06 — Solo monologue (single voice, no partner)
    solo_notes = diatonic_scale(C4, 8) + list(reversed(diatonic_scale(C4, 8)))
    solo_durs = [0.5] * 16
    pm = _pm_melody(solo_notes, solo_durs, program=PIANO, velocity=80)
    save(pm, "ddsmi", "06_solo_monologue", {
        "description": "Single piano ascending/descending diatonic scale. "
                       "No second voice — minimal coordination demand.",
        "expected": {"social_coordination": "LOW-MODERATE", "resource_allocation": "LOW"},
        "science": "Keller 2014: coordination requires multiple agents."})
    stimuli.append("06_solo_monologue")

    # 07 — Three voices coordinated (trio)
    v1 = [C4, E4, G4, C5] * 4
    v2 = [E4, G4, B4, E5] * 4
    v3 = [G3, C4, D4, G4] * 4
    durs3 = [0.5] * 16
    pm = pretty_midi.PrettyMIDI()
    for notes, prog in [(v1, PIANO), (v2, VIOLIN), (v3, CELLO)]:
        inst = pretty_midi.Instrument(program=prog)
        t = 0.0
        for p, d in zip(notes, durs3):
            inst.notes.append(Note(velocity=80, pitch=p,
                                   start=t, end=t + d - 0.02))
            t += d
        pm.instruments.append(inst)
    save(pm, "ddsmi", "07_three_voice_coordinated", {
        "description": "Piano + violin + cello trio in synchronized chord arpeggiation. "
                       "Three-way coordination with rich texture.",
        "expected": {"social_coordination": "HIGH", "resource_allocation": "HIGH"},
        "science": "Keller 2014: ensemble size increases coordination demands."})
    stimuli.append("07_three_voice_coordinated")

    # 08 — Parallel motion in 6ths
    top = [A4, B4, C5, D5, E5, F5, G5, A5] * 2
    bot = [C4, D4, E4, F4, G4, A4, B4, C5] * 2
    pm = _pm_duet_synchronized(bot, top, [0.5]*16,
                               prog1=CELLO, prog2=FLUTE, vel=80)
    save(pm, "ddsmi", "08_parallel_sixths", {
        "description": "Cello + flute in parallel sixths ascending. "
                       "Coordinated parallel motion, consonant intervals.",
        "expected": {"social_coordination": "HIGH"},
        "science": "Kohler 2025: content-specific representations for self/other parts."})
    stimuli.append("08_parallel_sixths")

    # 09 — Contrary motion (voices moving apart)
    ascending = [C4, D4, E4, F4, G4, A4, B4, C5] * 2
    descending = [C5, B4, A4, G4, F4, E4, D4, C4] * 2
    pm = _pm_duet_synchronized(ascending, descending, [0.5]*16,
                               prog1=PIANO, prog2=VIOLIN, vel=80)
    save(pm, "ddsmi", "09_contrary_motion", {
        "description": "Piano ascends C4→C5 while violin descends C5→C4. "
                       "Contrary motion requires independent voice tracking.",
        "expected": {"social_coordination": "MODERATE-HIGH",
                     "resource_allocation": "MODERATE-HIGH"},
        "science": "Kohler 2025: distinct PMC representations for other-produced actions."})
    stimuli.append("09_contrary_motion")

    # 10 — Two instruments rhythmic unison (same rhythm, different pitch)
    pm = _pm_ensemble_isochronous([
        (C4, PIANO, 80),
        (G4, VIOLIN, 80),
    ], 120.0, 16)
    save(pm, "ddsmi", "10_rhythmic_unison", {
        "description": "Piano C4 + violin G4 in rhythmic unison at 120 BPM. "
                       "Same timing, different pitches — temporal coordination.",
        "expected": {"social_coordination": "MODERATE-HIGH"},
        "science": "Novembre & Keller 2014: temporal alignment core to joint action."})
    stimuli.append("10_rhythmic_unison")

    return stimuli


# ═══════════════════════════════════════════════════════════════════
#  CATEGORY 4 — CROSS-UNIT INTERACTIONS
# ═══════════════════════════════════════════════════════════════════

def generate_cross_stimuli():
    """8 stimuli testing cross-unit interactions.

    NSCP × SSRI: groove + harmony co-activation
    DDSMI × NSCP: coordination + synchrony co-activation
    DDSMI × SSRI: coordination + reward co-activation
    Dissociations: high sync / low reward, high reward / low sync
    Ceiling: all units maximal
    """
    stimuli = []

    # 01 — Full social scene (all units active)
    ioi = 0.5
    pm = pretty_midi.PrettyMIDI()
    # Bass groove
    bass = pretty_midi.Instrument(program=CELLO)
    for i in range(16):
        t = i * ioi
        p = C3 if i % 4 < 2 else G3
        bass.notes.append(Note(velocity=90, pitch=p, start=t, end=t + ioi * 0.85))
    pm.instruments.append(bass)
    # Harmony
    harm = pretty_midi.Instrument(program=STRINGS)
    for i in range(8):
        t = i * ioi * 2
        for p in (C_MAJ if i % 2 == 0 else G_MAJ):
            harm.notes.append(Note(velocity=70, pitch=p,
                                   start=t, end=t + ioi * 2 - 0.02))
    pm.instruments.append(harm)
    # Melody duet (call-response feel)
    mel1 = pretty_midi.Instrument(program=VIOLIN)
    mel2 = pretty_midi.Instrument(program=FLUTE)
    call_mel = [E5, G5, A5, G5]
    resp_mel = [C5, D5, E5, D5]
    for i in range(4):
        t1 = i * ioi * 4
        for j, p in enumerate(call_mel):
            mel1.notes.append(Note(velocity=80, pitch=p,
                                   start=t1 + j * ioi, end=t1 + (j + 1) * ioi - 0.02))
    for i in range(4):
        t2 = ioi * 2 + i * ioi * 4
        for j, p in enumerate(resp_mel):
            mel2.notes.append(Note(velocity=75, pitch=p,
                                   start=t2 + j * ioi, end=t2 + (j + 1) * ioi - 0.02))
    pm.instruments.append(mel1)
    pm.instruments.append(mel2)
    save(pm, "cross", "01_full_social_scene", {
        "description": "Full ensemble: cello bass + string harmony + violin/flute dialogue. "
                       "Multi-voice synchronization, groove, harmony, coordination.",
        "expected": {"neural_synchrony": "HIGH", "social_coordination": "HIGH",
                     "synchrony_reward": "HIGH", "social_bonding": "HIGH"},
        "science": "Williamson & Bonshor 2019: ensemble music engages all social mechanisms."})
    stimuli.append("01_full_social_scene")

    # 02 — Social minimum (single cold repeated note)
    pm = _pm_isochronous(C3, 60.0, 6, program=ORGAN, velocity=45)
    save(pm, "cross", "02_social_minimum", {
        "description": "Single C3 organ tone repeated slowly (60 BPM). "
                       "Minimal social affordance — single voice, cold timbre.",
        "expected": {"neural_synchrony": "LOW", "social_coordination": "LOW",
                     "synchrony_reward": "LOW"},
        "science": "Koelsch 2014: social functions require multi-voice interaction."})
    stimuli.append("02_social_minimum")

    # 03 — High sync, low reward (mechanical metronomic unison)
    pm = _pm_ensemble_isochronous([
        (C4, PIANO, 70),
        (C4, HARPSICHORD, 70),
        (C4, ORGAN, 70),
    ], 120.0, 16)
    save(pm, "cross", "03_high_sync_low_reward", {
        "description": "3 instruments in exact unison C4 at 120 BPM. "
                       "Perfect temporal sync but monotonous, no harmonic variety.",
        "expected": {"neural_synchrony": "HIGH", "social_bonding": "LOW-MODERATE"},
        "science": "Keller 2014: synchronization ≠ reward; reward needs variety."})
    stimuli.append("03_high_sync_low_reward")

    # 04 — High reward, low sync (beautiful solo)
    solo_notes = [C5, E5, G5, C6, G5, E5, C5, G4]
    solo_durs = [0.8, 0.4, 0.6, 1.0, 0.6, 0.4, 0.8, 0.6]
    pm = _pm_melody(solo_notes, solo_durs, program=VIOLIN, velocity=80)
    # Add soft harmony pad
    pad = pretty_midi.Instrument(program=STRINGS)
    for p in C_MAJ:
        pad.notes.append(Note(velocity=50, pitch=p, start=0.0, end=5.0))
    pm.instruments.append(pad)
    save(pm, "cross", "04_high_reward_low_sync", {
        "description": "Beautiful violin solo over soft string pad. "
                       "High reward/pleasure but rubato timing, no coordination partner.",
        "expected": {"collective_pleasure_pred": "MODERATE-HIGH",
                     "social_coordination": "LOW-MODERATE"},
        "science": "Koelsch 2014: solo performance engages reward but not coordination."})
    stimuli.append("04_high_reward_low_sync")

    # 05 — All-units ceiling (maximum complexity)
    pm = pretty_midi.PrettyMIDI()
    ioi_c = 0.5
    # Full orchestra groove
    for prog, pitch, vel in [(CELLO, C3, 90), (GUITAR_STEEL, G3, 85),
                              (PIANO, C4, 80), (STRINGS, E4, 75),
                              (VIOLIN, G5, 80), (FLUTE, C6, 70),
                              (TRUMPET, E5, 85), (FRENCH_HORN, C4, 75)]:
        inst = pretty_midi.Instrument(program=prog)
        for i in range(16):
            t = i * ioi_c
            inst.notes.append(Note(velocity=vel, pitch=pitch,
                                   start=t, end=t + ioi_c * 0.85))
        pm.instruments.append(inst)
    save(pm, "cross", "05_all_units_ceiling", {
        "description": "8-instrument full orchestra groove at 120 BPM. "
                       "Maximum timbral, harmonic, and rhythmic complexity.",
        "expected": {"neural_synchrony": "HIGH", "social_coordination": "HIGH",
                     "synchrony_reward": "HIGH", "social_bonding": "HIGH",
                     "entrainment_quality": "HIGH"},
        "science": "Williamson 2019: full ensemble activates all social cognition pathways."})
    stimuli.append("05_all_units_ceiling")

    # 06 — NSCP × SSRI co-activation (groove + harmony)
    pm = _pm_groove_bass_melody(
        [C3, E3, G3, C3] * 4, [0.5]*16,
        [C5, E5, G5, E5] * 4, [0.5]*16,
        bass_prog=CELLO, melody_prog=VIOLIN,
        bass_vel=85, melody_vel=80)
    # Add harmony
    pad = pretty_midi.Instrument(program=STRINGS)
    for p in [E4, G4, C5]:
        pad.notes.append(Note(velocity=65, pitch=p, start=0.0, end=8.0))
    pm.instruments.append(pad)
    save(pm, "cross", "06_nscp_ssri_groove_harmony", {
        "description": "Cello bass + violin melody groove with string harmony pad. "
                       "Synchrony + reward co-activation through groove + consonance.",
        "expected": {"neural_synchrony": "HIGH", "synchrony_reward": "HIGH",
                     "social_bonding": "MODERATE-HIGH"},
        "science": "Tarr 2014 + Launay 2016: synchrony + bonding co-activate."})
    stimuli.append("06_nscp_ssri_groove_harmony")

    # 07 — DDSMI × SSRI co-activation (coordinated dialogue + harmony)
    call_n = [C4, E4, G4, C5]
    resp_n = [E4, G4, B4, E5]
    pm = _pm_call_response(call_n * 2, resp_n * 2, note_dur=0.4,
                           call_prog=PIANO, resp_prog=VIOLIN, gap=0.05, vel=80)
    # Sustained harmony
    pad = pretty_midi.Instrument(program=STRINGS)
    for p in [C3, G3, E4]:
        pad.notes.append(Note(velocity=55, pitch=p, start=0.0, end=8.0))
    pm.instruments.append(pad)
    save(pm, "cross", "07_ddsmi_ssri_coordination_harmony", {
        "description": "Piano/violin call-response over sustained string harmony. "
                       "Coordination + social reward co-activation.",
        "expected": {"social_coordination": "HIGH", "synchrony_reward": "MODERATE-HIGH",
                     "social_bonding": "MODERATE-HIGH"},
        "science": "Novembre 2012 + Koelsch 2014: coordination + reward interact."})
    stimuli.append("07_ddsmi_ssri_coordination_harmony")

    # 08 — DDSMI × NSCP co-activation (coordination + strong beat)
    pm = _pm_interlocking(
        [C4, E4, G4, C5], [G4, B4, D5, G5],
        120.0, 4, prog1=PIANO, prog2=TRUMPET, vel=85)
    save(pm, "cross", "08_ddsmi_nscp_coordination_beat", {
        "description": "Piano/trumpet interlocking pattern at 120 BPM. "
                       "Coordination + beat synchrony co-activation.",
        "expected": {"social_coordination": "HIGH", "neural_synchrony": "HIGH"},
        "science": "Bigand 2025: interlocking patterns engage social coordination markers."})
    stimuli.append("08_ddsmi_nscp_coordination_beat")

    return stimuli


# ═══════════════════════════════════════════════════════════════════
#  CATEGORY 5 — BOUNDARY CONDITIONS
# ═══════════════════════════════════════════════════════════════════

def generate_boundary_stimuli():
    """8 boundary stimuli — same pattern as F7/F8."""
    stimuli = []

    # 01 — Near silence
    pm = _pm_near_silence(5.0)
    save(pm, "boundary", "01_near_silence", {
        "description": "Near-silence: single vel=1 tick. Floor condition.",
        "expected": {b: "FLOOR" for b in ["neural_synchrony", "social_coordination"]},
        "science": "Boundary condition — no published expectation."})
    stimuli.append("01_near_silence")

    # 02 — fff chromatic cluster
    cluster = chromatic_cluster(C4, 12)
    pm = _pm_chord(cluster, 5.0, program=PIANO, velocity=127)
    save(pm, "boundary", "02_fff_cluster", {
        "description": "12-note chromatic cluster fff sustained 5s. Ceiling amplitude.",
        "expected": {b: "CEILING" for b in ["neural_synchrony"]},
        "science": "Boundary condition — no published expectation."})
    stimuli.append("02_fff_cluster")

    # 03 — Single click
    pm = _pm_note(C4, 0.01, program=PIANO, velocity=127)
    save(pm, "boundary", "03_single_click", {
        "description": "Single loud click (1ms). Impulse response.",
        "expected": {},
        "science": "Boundary condition — impulse response."})
    stimuli.append("03_single_click")

    # 04 — Dense random noise
    pm = _pm_dense_random(5.0, seed=904, notes_per_sec=16)
    save(pm, "boundary", "04_dense_random_noise", {
        "description": "Dense random (16 notes/sec) — no structure.",
        "expected": {},
        "science": "Boundary condition — noise floor."})
    stimuli.append("04_dense_random_noise")

    # 05 — Very slow tempo (40 BPM)
    pm = _pm_isochronous(C4, 40.0, 4, program=PIANO, velocity=80)
    save(pm, "boundary", "05_very_slow_40bpm", {
        "description": "Isochronous C4 at 40 BPM — ultra-macro scale.",
        "expected": {},
        "science": "Boundary condition — slow tempo."})
    stimuli.append("05_very_slow_40bpm")

    # 06 — Very fast tempo (240 BPM)
    pm = _pm_isochronous(C4, 240.0, 32, program=PIANO, velocity=80)
    save(pm, "boundary", "06_very_fast_240bpm", {
        "description": "Isochronous C4 at 240 BPM — near motor limit.",
        "expected": {},
        "science": "Boundary condition — fast tempo."})
    stimuli.append("06_very_fast_240bpm")

    # 07 — Extreme register (C1 + C7)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(Note(velocity=80, pitch=C1, start=0.0, end=3.0))
    inst.notes.append(Note(velocity=80, pitch=C7, start=3.0, end=6.0))
    pm.instruments.append(inst)
    save(pm, "boundary", "07_extreme_register", {
        "description": "C1 (3s) then C7 (3s) — pitch extremes.",
        "expected": {},
        "science": "Boundary condition — extreme register."})
    stimuli.append("07_extreme_register")

    # 08 — Long duration (~32 bars at 120 BPM)
    pm = _pm_isochronous(C4, 120.0, 128, program=PIANO, velocity=80)
    save(pm, "boundary", "08_long_duration_32bar", {
        "description": "128 beats at 120 BPM (~64s). Long duration stability test.",
        "expected": {},
        "science": "Boundary condition — long duration."})
    stimuli.append("08_long_duration_32bar")

    return stimuli


# ═══════════════════════════════════════════════════════════════════
#  METADATA & CATALOG
# ═══════════════════════════════════════════════════════════════════

def write_metadata():
    """Write metadata.json."""
    path = OUTPUT_DIR / "metadata.json"
    with open(path, "w") as f:
        json.dump(ALL_METADATA, f, indent=2, ensure_ascii=False)
    print(f"  metadata.json  ({len(ALL_METADATA)} entries)")


def write_catalog():
    """Write STIMULUS-CATALOG.md with full ordinal comparison matrix."""
    lines = [
        "# F9 Social Cognition — Stimulus Catalog\n",
        f"**Total stimuli**: {len(ALL_METADATA)}\n",
        "## Target Beliefs (10)\n",
        "| # | Belief | Type | Unit | tau |",
        "|---|--------|------|------|-----|",
        "| 1 | neural_synchrony | Core | NSCP | 0.65 |",
        "| 2 | social_coordination | Core | DDSMI | 0.60 |",
        "| 3 | synchrony_reward | Appraisal | SSRI | — |",
        "| 4 | social_bonding | Appraisal | SSRI | — |",
        "| 5 | group_flow | Appraisal | SSRI | — |",
        "| 6 | entrainment_quality | Appraisal | SSRI | — |",
        "| 7 | social_prediction_error | Appraisal | SSRI | — |",
        "| 8 | resource_allocation | Appraisal | DDSMI | — |",
        "| 9 | catchiness_pred | Anticipation | NSCP | — |",
        "| 10 | collective_pleasure_pred | Anticipation | SSRI | — |",
        "",
        "## Ordinal Comparison Matrix\n",
        "| A | B | Belief | Dir | Science |",
        "|---|---|--------|-----|---------|",
    ]

    comparisons = [
        # ── NSCP: neural_synchrony ──────────────────────────────
        ("nscp/01_ensemble_groove_synchronized", "nscp/02_solo_piano_rubato",
         "neural_synchrony", "A>B",
         "Wohltjen 2023: multi-voice groove > solo rubato for synchrony"),
        ("nscp/01_ensemble_groove_synchronized", "nscp/06_arrhythmic_atonal",
         "neural_synchrony", "A>B",
         "Wohltjen 2023: structured groove > arrhythmic for synchrony"),
        ("nscp/05_groove_strong_beat", "nscp/06_arrhythmic_atonal",
         "neural_synchrony", "A>B",
         "Large 2023: strong beat > no beat for entrainment"),
        ("nscp/09_unison_octaves_multi", "nscp/10_desynchronized_random_entries",
         "neural_synchrony", "A>B",
         "Keller 2014: synchronized > desynchronized for neural coupling"),
        ("nscp/09_unison_octaves_multi", "nscp/12_single_note_metronomic",
         "neural_synchrony", "A>B",
         "Ni 2024: multi-voice > single voice for synchrony"),
        ("nscp/01_ensemble_groove_synchronized", "nscp/12_single_note_metronomic",
         "neural_synchrony", "A>B",
         "Ni 2024: ensemble groove > metronomic single for synchrony"),

        # ── NSCP: catchiness_pred ───────────────────────────────
        ("nscp/07_catchy_repetitive_hook", "nscp/08_complex_non_repetitive",
         "catchiness_pred", "A>B",
         "Savage 2021: repetitive > non-repetitive for catchiness"),

        # ── SSRI: synchrony_reward ──────────────────────────────
        ("ssri/01_dance_groove_energetic", "ssri/04_single_cold_isolated",
         "synchrony_reward", "A>B",
         "Tarr 2014: groove > isolated for synchrony reward (N=264)"),
        ("ssri/01_dance_groove_energetic", "ssri/06_free_tempo_rubato",
         "synchrony_reward", "A>B",
         "Tarr 2014: rhythmic groove > free tempo for reward"),
        ("ssri/14_march_energetic_strong", "ssri/04_single_cold_isolated",
         "synchrony_reward", "A>B",
         "Tarr 2014: march rhythm > cold tone for reward"),

        # ── SSRI: social_bonding ────────────────────────────────
        ("ssri/02_ballad_warm_60bpm", "ssri/04_single_cold_isolated",
         "social_bonding", "A>B",
         "Launay 2016: warm ensemble > cold isolated for bonding (N=94)"),
        ("ssri/03_full_ensemble_harmony", "ssri/04_single_cold_isolated",
         "social_bonding", "A>B",
         "Williamson 2019: full ensemble > isolated for bonding (N=346)"),
        ("ssri/13_lullaby_gentle_rocking", "ssri/04_single_cold_isolated",
         "social_bonding", "A>B",
         "Nguyen 2023: lullaby > cold tone for bonding"),

        # ── SSRI: entrainment_quality ───────────────────────────
        ("ssri/05_strong_beat_percussion", "ssri/06_free_tempo_rubato",
         "entrainment_quality", "A>B",
         "Large 2023: strong beat > rubato for entrainment"),
        ("ssri/01_dance_groove_energetic", "ssri/06_free_tempo_rubato",
         "entrainment_quality", "A>B",
         "Large 2023: groove > free tempo for entrainment"),

        # ── SSRI: collective_pleasure_pred ──────────────────────
        ("ssri/03_full_ensemble_harmony", "ssri/10_unresolved_dissonance",
         "collective_pleasure_pred", "A>B",
         "Koelsch 2014: consonant ensemble > dissonance for pleasure"),

        # ── DDSMI: social_coordination ──────────────────────────
        ("ddsmi/01_duet_perfectly_synchronized", "ddsmi/06_solo_monologue",
         "social_coordination", "A>B",
         "Kohler 2025: duet > solo for coordination activation"),
        ("ddsmi/04_call_response_dialogue", "ddsmi/06_solo_monologue",
         "social_coordination", "A>B",
         "Novembre 2012: call-response > solo for coordination (N=20)"),
        ("ddsmi/05_interlocking_rhythms", "ddsmi/06_solo_monologue",
         "social_coordination", "A>B",
         "Bigand 2025: interlocking > solo for social coordination"),
        ("ddsmi/07_three_voice_coordinated", "ddsmi/06_solo_monologue",
         "social_coordination", "A>B",
         "Keller 2014: trio > solo for coordination"),

        # ── DDSMI: resource_allocation ──────────────────────────
        ("ddsmi/04_call_response_dialogue", "ddsmi/06_solo_monologue",
         "resource_allocation", "A>B",
         "Bigand 2025: dialogue > monologue for resource allocation"),

        # ── CROSS: multi-unit ───────────────────────────────────
        ("cross/01_full_social_scene", "cross/02_social_minimum",
         "neural_synchrony", "A>B",
         "Williamson 2019: full ensemble > minimum for all beliefs"),
        ("cross/01_full_social_scene", "cross/02_social_minimum",
         "social_coordination", "A>B",
         "Keller 2014: full scene > minimum for coordination"),
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
    print("  STIMULUS-CATALOG.md")


# ═══════════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════════

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating F9 Social Cognition test audio...\n")

    s1 = generate_nscp_stimuli()
    print(f"  NSCP:      {len(s1)} stimuli")

    s2 = generate_ssri_stimuli()
    print(f"  SSRI:      {len(s2)} stimuli")

    s3 = generate_ddsmi_stimuli()
    print(f"  DDSMI:     {len(s3)} stimuli")

    s4 = generate_cross_stimuli()
    print(f"  Cross:     {len(s4)} stimuli")

    s5 = generate_boundary_stimuli()
    print(f"  Boundary:  {len(s5)} stimuli")

    total = len(s1) + len(s2) + len(s3) + len(s4) + len(s5)
    print(f"\n  Total: {total} stimuli\n")

    write_metadata()
    write_catalog()
    print("\nDone.")


if __name__ == "__main__":
    main()
