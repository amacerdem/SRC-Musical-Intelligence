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
