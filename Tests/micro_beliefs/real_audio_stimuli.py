"""MIDI-based audio synthesis for micro-belief tests.

Generates musically realistic but fully deterministic stimuli using
FluidSynth + SoundFont rendering.  Every parameter (notes, velocity,
program, duration) is explicitly controlled so we know the exact
ground truth for each test.

All functions return ``(1, N)`` float32 tensors at 44 100 Hz.
"""
from __future__ import annotations

import pathlib
from typing import List, Optional, Tuple

import numpy as np
import pretty_midi
import torch
from torch import Tensor

SAMPLE_RATE = 44_100

# ── SoundFont path ────────────────────────────────────────────────────
_SF2_CANDIDATES = [
    pathlib.Path.home() / "miniconda3" / "lib" / "python3.13"
    / "site-packages" / "pretty_midi" / "TimGM6mb.sf2",
    pathlib.Path("/usr/share/sounds/sf2/FluidR3_GM.sf2"),
    pathlib.Path("/usr/local/share/fluidsynth/default.sf2"),
]

_SF2_PATH: Optional[str] = None
for _p in _SF2_CANDIDATES:
    if _p.exists():
        _SF2_PATH = str(_p)
        break

# ── GM Program Numbers ────────────────────────────────────────────────
PIANO = 0
BRIGHT_PIANO = 1
HARPSICHORD = 6
ORGAN = 19
GUITAR_NYLON = 24
GUITAR_STEEL = 25
VIOLIN = 40
VIOLA = 41
CELLO = 42
STRINGS = 48       # String Ensemble 1
CHOIR = 52         # Choir Aahs
TRUMPET = 56
TROMBONE = 57
FRENCH_HORN = 60
FLUTE = 73
OBOE = 68
CLARINET = 71


# ── Core rendering ────────────────────────────────────────────────────

def _render(pm: pretty_midi.PrettyMIDI) -> Tensor:
    """Render a PrettyMIDI object to ``(1, N)`` float32 tensor.

    Uses FluidSynth with SoundFont if available, otherwise falls
    back to simple sine-wave synthesis.
    """
    try:
        import fluidsynth as _  # noqa: F401
        audio = pm.fluidsynth(fs=SAMPLE_RATE, sf2_path=_SF2_PATH)
    except Exception:
        audio = pm.synthesize(fs=SAMPLE_RATE)

    # Convert to float32, normalize to [-0.95, 0.95]
    audio = audio.astype(np.float32)
    peak = np.abs(audio).max()
    if peak > 0:
        audio = audio * (0.95 / peak)
    return torch.from_numpy(audio).unsqueeze(0)  # (1, N)


# ── MIDI Primitives ───────────────────────────────────────────────────

def midi_note(
    pitch: int = 60,
    duration_s: float = 4.0,
    program: int = PIANO,
    velocity: int = 80,
) -> Tensor:
    """Single sustained MIDI note.

    Ground truth: single f0 at ``midi_to_hz(pitch)`` Hz,
    with timbral character determined by ``program``.
    """
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    inst.notes.append(pretty_midi.Note(
        velocity=velocity, pitch=pitch,
        start=0.0, end=duration_s,
    ))
    pm.instruments.append(inst)
    return _render(pm)


def midi_chord(
    notes: List[int],
    duration_s: float = 4.0,
    program: int = PIANO,
    velocity: int = 80,
) -> Tensor:
    """Sustained MIDI chord (multiple simultaneous notes).

    Ground truth: simultaneous pitches with known intervallic relationships.
    """
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for pitch in notes:
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch,
            start=0.0, end=duration_s,
        ))
    pm.instruments.append(inst)
    return _render(pm)


def midi_progression(
    chords: List[List[int]],
    durations: Optional[List[float]] = None,
    program: int = PIANO,
    velocity: int = 80,
) -> Tensor:
    """Chord progression — sequence of chords.

    Ground truth: each chord's consonance/dissonance is known from
    its interval content.
    """
    if durations is None:
        durations = [1.5] * len(chords)

    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for chord_pitches, dur in zip(chords, durations):
        for pitch in chord_pitches:
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=pitch,
                start=t, end=t + dur,
            ))
        t += dur
    pm.instruments.append(inst)
    return _render(pm)


def midi_melody(
    notes: List[int],
    durations: Optional[List[float]] = None,
    program: int = PIANO,
    velocity: int = 80,
) -> Tensor:
    """Monophonic melody — sequence of single notes.

    Ground truth: pitch sequence, interval sizes, contour direction.
    """
    if durations is None:
        durations = [0.4] * len(notes)

    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for pitch, dur in zip(notes, durations):
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch,
            start=t, end=t + dur - 0.02,  # 20ms gap for note separation
        ))
        t += dur
    pm.instruments.append(inst)
    return _render(pm)


def midi_melody_with_chords(
    melody_notes: List[int],
    melody_durs: List[float],
    chord_notes: List[List[int]],
    chord_durs: List[float],
    melody_program: int = FLUTE,
    chord_program: int = PIANO,
    melody_velocity: int = 90,
    chord_velocity: int = 60,
) -> Tensor:
    """Melody over chord accompaniment — polyphonic texture.

    Ground truth: melody pitch + harmonic context from chords.
    """
    pm = pretty_midi.PrettyMIDI()

    # Melody instrument
    mel_inst = pretty_midi.Instrument(program=melody_program)
    t = 0.0
    for pitch, dur in zip(melody_notes, melody_durs):
        mel_inst.notes.append(pretty_midi.Note(
            velocity=melody_velocity, pitch=pitch,
            start=t, end=t + dur - 0.02,
        ))
        t += dur
    pm.instruments.append(mel_inst)

    # Chord instrument
    chd_inst = pretty_midi.Instrument(program=chord_program)
    t = 0.0
    for chord_pitches, dur in zip(chord_notes, chord_durs):
        for pitch in chord_pitches:
            chd_inst.notes.append(pretty_midi.Note(
                velocity=chord_velocity, pitch=pitch,
                start=t, end=t + dur,
            ))
        t += dur
    pm.instruments.append(chd_inst)

    return _render(pm)


def midi_multi_instrument(
    pitch: int = 60,
    duration_s: float = 5.0,
    programs: Optional[List[int]] = None,
    velocity: int = 80,
) -> dict[int, Tensor]:
    """Same pitch rendered on multiple instruments.

    Ground truth: identical pitch, different timbral spectrum per program.
    Returns dict mapping program number to ``(1, N)`` tensor.
    """
    if programs is None:
        programs = [PIANO, VIOLIN, FLUTE, TRUMPET, ORGAN, GUITAR_NYLON]

    results = {}
    for prog in programs:
        results[prog] = midi_note(pitch, duration_s, prog, velocity)
    return results


# ── Musical Pattern Constructors ──────────────────────────────────────

# MIDI note numbers
C3, D3, E3, F3, G3, A3, B3 = 48, 50, 52, 53, 55, 57, 59
C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4 = range(60, 72)
C5, D5, E5, F5, G5, A5, B5 = 72, 74, 76, 77, 79, 81, 83
C6 = 84


def major_triad(root: int = C4) -> List[int]:
    """Major triad: root + M3 + P5."""
    return [root, root + 4, root + 7]


def minor_triad(root: int = C4) -> List[int]:
    """Minor triad: root + m3 + P5."""
    return [root, root + 3, root + 7]


def diminished_triad(root: int = C4) -> List[int]:
    """Diminished triad: root + m3 + TT."""
    return [root, root + 3, root + 6]


def augmented_triad(root: int = C4) -> List[int]:
    """Augmented triad: root + M3 + Aug5."""
    return [root, root + 4, root + 8]


def dominant_seventh(root: int = G3) -> List[int]:
    """Dominant 7th: root + M3 + P5 + m7."""
    return [root, root + 4, root + 7, root + 10]


def chromatic_cluster(base: int = C4, n: int = 4) -> List[int]:
    """Chromatic cluster: n adjacent semitones."""
    return list(range(base, base + n))


def diatonic_scale(start: int = C4, n: int = 8) -> List[int]:
    """C major diatonic scale (W-W-H-W-W-W-H)."""
    intervals = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24]
    return [start + intervals[i] for i in range(min(n, len(intervals)))]


def chromatic_scale(start: int = C4, n: int = 13) -> List[int]:
    """Chromatic ascending scale."""
    return [start + i for i in range(n)]


# ── Extended Primitives (R³ verification) ────────────────────────────

C2 = 36
D2, E2, F2, G2, A2, B2 = 38, 40, 41, 43, 45, 47

def midi_isochronous(
    pitch: int = 60,
    bpm: float = 120.0,
    n_beats: int = 16,
    program: int = PIANO,
    velocity: int = 80,
) -> Tensor:
    """Isochronous (equally spaced) note sequence at exact BPM.

    Ground truth: tempo = bpm, isochrony_nPVI ≈ 1.0 (perfect regularity).
    """
    ioi = 60.0 / bpm
    note_dur = ioi * 0.85

    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_beats):
        t = i * ioi
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch,
            start=t, end=t + note_dur,
        ))
    pm.instruments.append(inst)
    return _render(pm)


def midi_crescendo(
    pitch: int = 60,
    n_steps: int = 12,
    step_dur: float = 0.4,
    v_start: int = 20,
    v_end: int = 120,
    program: int = PIANO,
) -> Tensor:
    """Notes with linearly increasing velocity (crescendo).

    Ground truth: amplitude ramps up, velocity_A positive.
    """
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_steps):
        v = int(v_start + (v_end - v_start) * i / max(n_steps - 1, 1))
        t = i * step_dur
        inst.notes.append(pretty_midi.Note(
            velocity=v, pitch=pitch,
            start=t, end=t + step_dur - 0.02,
        ))
    pm.instruments.append(inst)
    return _render(pm)


def midi_decrescendo(
    pitch: int = 60,
    n_steps: int = 12,
    step_dur: float = 0.4,
    v_start: int = 120,
    v_end: int = 20,
    program: int = PIANO,
) -> Tensor:
    """Notes with linearly decreasing velocity (decrescendo).

    Ground truth: amplitude ramps down, velocity_A negative.
    """
    return midi_crescendo(pitch, n_steps, step_dur, v_start, v_end, program)


def midi_tremolo(
    pitch: int = 60,
    rate_hz: float = 4.0,
    duration_s: float = 4.0,
    program: int = PIANO,
    velocity: int = 80,
) -> Tensor:
    """Rapid repeated notes at a specific Hz rate.

    Ground truth: modulation energy peaks at rate_hz.
    """
    ioi = 1.0 / rate_hz
    note_dur = ioi * 0.7
    n_notes = int(duration_s * rate_hz)

    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_notes):
        t = i * ioi
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch,
            start=t, end=t + note_dur,
        ))
    pm.instruments.append(inst)
    return _render(pm)


def midi_syncopated(
    pitch: int = 60,
    bpm: float = 120.0,
    n_bars: int = 4,
    program: int = PIANO,
    velocity: int = 80,
) -> Tensor:
    """Syncopated pattern — accents on offbeats.

    Pattern per bar (in 8th notes): rest-HIT-rest-HIT-rest-HIT-rest-rest
    Ground truth: high syncopation_index, lower metricality.
    """
    eighth = 60.0 / bpm / 2.0
    note_dur = eighth * 0.8

    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    offbeats = [1, 3, 5]
    for bar in range(n_bars):
        bar_start = bar * 8 * eighth
        for pos in offbeats:
            t = bar_start + pos * eighth
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=pitch,
                start=t, end=t + note_dur,
            ))
    pm.instruments.append(inst)
    return _render(pm)


def midi_polyrhythm(
    pitch1: int = 60,
    pitch2: int = 67,
    beats1: int = 3,
    beats2: int = 4,
    duration_s: float = 6.0,
    program: int = PIANO,
    velocity: int = 80,
) -> Tensor:
    """Polyrhythm: two voices with different beat subdivisions.

    Ground truth: complex rhythm, lower metricality, lower rhythmic_regularity.
    """
    cycle_dur = duration_s / 2.0
    ioi1 = cycle_dur / beats1
    ioi2 = cycle_dur / beats2

    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)

    for cycle in range(2):
        offset = cycle * cycle_dur
        for i in range(beats1):
            t = offset + i * ioi1
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=pitch1,
                start=t, end=t + ioi1 * 0.7,
            ))
        for i in range(beats2):
            t = offset + i * ioi2
            inst.notes.append(pretty_midi.Note(
                velocity=velocity - 15, pitch=pitch2,
                start=t, end=t + ioi2 * 0.7,
            ))
    pm.instruments.append(inst)
    return _render(pm)


def midi_irregular_rhythm(
    pitch: int = 60,
    n_notes: int = 12,
    program: int = PIANO,
    velocity: int = 80,
    seed: int = 42,
) -> Tensor:
    """Notes with irregular (non-isochronous) timing.

    Ground truth: low isochrony_nPVI, low rhythmic_regularity.
    """
    rng = np.random.RandomState(seed)
    iois = rng.uniform(0.15, 0.8, size=n_notes).tolist()

    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for ioi in iois:
        note_dur = min(ioi * 0.8, 0.5)
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch,
            start=t, end=t + note_dur,
        ))
        t += ioi
    pm.instruments.append(inst)
    return _render(pm)


def midi_key_progression(
    keys: List[int],
    dur_per_key: float = 3.0,
    program: int = PIANO,
    velocity: int = 70,
) -> Tensor:
    """Chord progression through different keys (modulation).

    Each key plays a I-IV-V-I cadence.
    Ground truth: harmonic_change spikes at key boundaries, tonal_stability dips.
    """
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    chord_dur = dur_per_key / 4.0

    for root in keys:
        for p in [root, root + 4, root + 7]:
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=p, start=t, end=t + chord_dur,
            ))
        t += chord_dur
        iv = root + 5
        for p in [iv, iv + 4, iv + 7]:
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=p, start=t, end=t + chord_dur,
            ))
        t += chord_dur
        v = root + 7
        for p in [v, v + 4, v + 7]:
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=p, start=t, end=t + chord_dur,
            ))
        t += chord_dur
        for p in [root, root + 4, root + 7]:
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=p, start=t, end=t + chord_dur,
            ))
        t += chord_dur

    pm.instruments.append(inst)
    return _render(pm)
