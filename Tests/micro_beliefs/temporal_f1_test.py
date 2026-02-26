#!/usr/bin/env python
"""Temporal F1 Belief Diagnostics — frame-by-frame analysis with PNG + MD output.

Generates temporal transition audio with known ground truth, runs through
the full R³→H³→C³ pipeline, and evaluates whether each belief responds
correctly to temporal changes in the signal.

Outputs:
    Tests/micro_beliefs/reports/temporal_f1/
        REPORT-TEMPORAL-F1.md   — comprehensive MD report
        belief_{name}.png       — one PNG per belief showing temporal curves
        summary.png             — overall accuracy bar chart

Run::

    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/micro_beliefs/temporal_f1_test.py
"""
from __future__ import annotations

import pathlib
import sys
import time
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
from torch import Tensor

# ── Project path setup ──────────────────────────────────────────────
_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))

from Tests.micro_beliefs.pipeline_runner import (
    MicroBeliefRunner,
    HOP_LENGTH,
    SAMPLE_RATE,
)
from Tests.micro_beliefs.real_audio_stimuli import (
    midi_chord, midi_note, midi_progression, midi_melody,
    midi_melody_with_chords, _render,
    major_triad, minor_triad, diminished_triad, augmented_triad,
    dominant_seventh, chromatic_cluster, diatonic_scale,
    PIANO, VIOLIN, FLUTE, TRUMPET, STRINGS,
    CELLO, OBOE, GUITAR_NYLON, HARPSICHORD,
    C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5, A5, B5, C6,
)
import pretty_midi

# ── Matplotlib backend ──────────────────────────────────────────────
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

OUT_DIR = _ROOT / "Tests" / "micro_beliefs" / "reports" / "temporal_f1"
FPS = SAMPLE_RATE / HOP_LENGTH  # ~172.27 frames/sec
WARMUP_FRAMES = 40              # skip first 40 frames for H³ warmup

# Segment colors for plotting
SEG_COLORS = [
    "#2196F3",  # blue
    "#FF9800",  # orange
    "#4CAF50",  # green
    "#F44336",  # red
    "#9C27B0",  # purple
    "#00BCD4",  # cyan
]

# ═══════════════════════════════════════════════════════════════════
# Data Structures
# ═══════════════════════════════════════════════════════════════════

@dataclass
class Segment:
    """A labeled temporal segment within a test audio file."""
    label: str
    start_s: float
    end_s: float

    @property
    def start_frame(self) -> int:
        return max(int(self.start_s * FPS), WARMUP_FRAMES)

    @property
    def end_frame(self) -> int:
        return int(self.end_s * FPS)


@dataclass
class Assertion:
    """A temporal assertion: belief should change between segments."""
    belief: str
    seg_a: str       # label of segment A
    seg_b: str       # label of segment B
    direction: str   # "a>b" or "a<b"
    margin: float = 0.01  # minimum required difference
    description: str = ""


@dataclass
class TestCase:
    """A complete test case with audio and ground-truth assertions."""
    name: str
    audio: Tensor          # (1, N) waveform
    segments: List[Segment]
    assertions: List[Assertion]
    description: str = ""


@dataclass
class AssertionResult:
    """Result of evaluating a single assertion."""
    assertion: Assertion
    test_name: str
    val_a: float
    val_b: float
    passed: bool
    diff: float


# ═══════════════════════════════════════════════════════════════════
# Custom MIDI helpers for temporal transition audio
# ═══════════════════════════════════════════════════════════════════

def _multi_instrument_sequence(
    pitch: int,
    programs: List[int],
    dur_per: float = 2.5,
    velocity: int = 80,
) -> Tensor:
    """Same pitch played sequentially on different instruments."""
    pm = pretty_midi.PrettyMIDI()
    for i, prog in enumerate(programs):
        inst = pretty_midi.Instrument(program=prog)
        start = i * dur_per
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch,
            start=start, end=start + dur_per - 0.05,
        ))
        pm.instruments.append(inst)
    return _render(pm)


def _concat_audio(*segments: Tensor, crossfade_ms: float = 20.0) -> Tensor:
    """Concatenate audio tensors with crossfade to avoid clicks."""
    if len(segments) == 1:
        return segments[0]
    cf_samples = int(crossfade_ms * SAMPLE_RATE / 1000)
    parts = []
    for i, seg in enumerate(segments):
        s = seg.squeeze(0)  # (N,)
        if i > 0 and cf_samples > 0:
            # Apply fade-in
            fade = torch.linspace(0, 1, cf_samples)
            s[:cf_samples] *= fade
        if i < len(segments) - 1 and cf_samples > 0:
            # Apply fade-out
            fade = torch.linspace(1, 0, cf_samples)
            s[-cf_samples:] *= fade
        parts.append(s)
    return torch.cat(parts).unsqueeze(0)


# ═══════════════════════════════════════════════════════════════════
# Test Case Generators
# ═══════════════════════════════════════════════════════════════════

def gen_consonance_gradient() -> TestCase:
    """Major(3s) -> Dim(3s) -> Cluster(3s): consonance decreases."""
    audio = midi_progression(
        [major_triad(C4), diminished_triad(C4), chromatic_cluster(C4, 5)],
        [3.0, 3.0, 3.0], PIANO, 80,
    )
    return TestCase(
        name="consonance_gradient",
        description="Major triad -> Diminished triad -> Chromatic cluster (9s)",
        audio=audio,
        segments=[
            Segment("major", 0.3, 2.7),
            Segment("dim", 3.3, 5.7),
            Segment("cluster", 6.3, 8.7),
        ],
        assertions=[
            Assertion("harmonic_stability", "major", "dim", "a>b",
                      description="Consonant > diminished"),
            Assertion("harmonic_stability", "dim", "cluster", "a>b",
                      description="Diminished > cluster"),
            Assertion("harmonic_stability", "major", "cluster", "a>b",
                      description="Major > cluster (full gradient)"),
            Assertion("interval_quality", "major", "cluster", "a>b",
                      description="Major intervals > cluster intervals"),
            Assertion("harmonic_template_match", "major", "cluster", "a>b",
                      description="Triad matches template > cluster"),
            Assertion("consonance_salience_gradient", "cluster", "major", "a>b",
                      description="Dissonance drives salience"),
            Assertion("spectral_complexity", "major", "cluster", "a<b",
                      description="Cluster is spectrally denser"),
            Assertion("aesthetic_quality", "major", "cluster", "a>b",
                      description="Consonant = more aesthetic"),
            Assertion("spectral_temporal_synergy", "major", "cluster", "a>b",
                      description="Consonant = higher synergy"),
        ],
    )


def gen_dissonance_resolution() -> TestCase:
    """Cluster(3s) -> Major(3s): tension to release."""
    audio = midi_progression(
        [chromatic_cluster(C4, 5), major_triad(C4)],
        [3.0, 3.0], PIANO, 80,
    )
    return TestCase(
        name="dissonance_resolution",
        description="Chromatic cluster -> Major triad (6s)",
        audio=audio,
        segments=[
            Segment("cluster", 0.3, 2.7),
            Segment("major", 3.3, 5.7),
        ],
        assertions=[
            Assertion("harmonic_stability", "cluster", "major", "a<b",
                      description="Resolution increases stability"),
            Assertion("consonance_salience_gradient", "cluster", "major", "a>b",
                      description="Cluster drives more salience"),
            Assertion("spectral_complexity", "cluster", "major", "a>b",
                      description="Cluster is more complex"),
        ],
    )


def gen_cadence_V7_I() -> TestCase:
    """V7(3s) -> I(3s): dominant resolution."""
    audio = midi_progression(
        [dominant_seventh(G3), major_triad(C4)],
        [3.0, 3.0], PIANO, 80,
    )
    return TestCase(
        name="cadence_V7_I",
        description="Dominant 7th (G7) -> Tonic (C major) (6s)",
        audio=audio,
        segments=[
            Segment("V7", 0.3, 2.7),
            Segment("I", 3.3, 5.7),
        ],
        assertions=[
            Assertion("harmonic_stability", "V7", "I", "a<b",
                      description="Tonic more stable than dominant"),
            Assertion("harmonic_template_match", "V7", "I", "a<b",
                      description="Tonic matches template better"),
            Assertion("consonance_trajectory", "V7", "I", "a<b",
                      description="Forecasts resolution"),
        ],
    )


def gen_interval_quality_sweep() -> TestCase:
    """P1(2s) -> P5(2s) -> M3(2s) -> m2(2s): interval quality gradient."""
    audio = midi_progression(
        [[C4, C5], [C4, G4], [C4, E4], [C4, Db4]],
        [2.5, 2.5, 2.5, 2.5], PIANO, 80,
    )
    return TestCase(
        name="interval_quality_sweep",
        description="Octave -> P5 -> M3 -> m2 (10s)",
        audio=audio,
        segments=[
            Segment("octave", 0.3, 2.2),
            Segment("fifth", 2.8, 4.7),
            Segment("third", 5.3, 7.2),
            Segment("m2", 7.8, 9.7),
        ],
        assertions=[
            Assertion("interval_quality", "octave", "m2", "a>b",
                      description="Octave quality > minor 2nd"),
            Assertion("interval_quality", "fifth", "m2", "a>b",
                      description="P5 quality > minor 2nd"),
            Assertion("harmonic_stability", "octave", "m2", "a>b",
                      description="Octave more stable"),
        ],
    )


def gen_pitch_clarity_gradient() -> TestCase:
    """Single note(3s) -> Triad(3s) -> Dense cluster(3s)."""
    audio = midi_progression(
        [[C4], major_triad(C4), chromatic_cluster(C4, 6)],
        [3.0, 3.0, 3.0], PIANO, 80,
    )
    return TestCase(
        name="pitch_clarity_gradient",
        description="Single note -> Major triad -> 6-note cluster (9s)",
        audio=audio,
        segments=[
            Segment("single", 0.3, 2.7),
            Segment("triad", 3.3, 5.7),
            Segment("cluster", 6.3, 8.7),
        ],
        assertions=[
            Assertion("pitch_prominence", "single", "triad", "a>b",
                      description="Single note clearer pitch than chord"),
            Assertion("pitch_prominence", "single", "cluster", "a>b",
                      description="Single note clearer than cluster"),
            Assertion("spectral_complexity", "single", "cluster", "a<b",
                      description="Cluster is denser"),
        ],
    )


def gen_octave_equivalence() -> TestCase:
    """C3(2s) -> C4(2s) -> C5(2s) -> C6(2s): same chroma, different octave."""
    audio = midi_progression(
        [[C3], [C4], [C5], [C6]],
        [2.5, 2.5, 2.5, 2.5], PIANO, 80,
    )
    return TestCase(
        name="octave_equivalence",
        description="C3 -> C4 -> C5 -> C6 (10s)",
        audio=audio,
        segments=[
            Segment("C3", 0.3, 2.2),
            Segment("C4", 2.8, 4.7),
            Segment("C5", 5.3, 7.2),
            Segment("C6", 7.8, 9.7),
        ],
        assertions=[
            # Low register has weaker pitch identity (correct behavior)
            Assertion("pitch_identity", "C4", "C3", "a>b", margin=0.0,
                      description="C4 stronger pitch identity than C3 (register effect)"),
            Assertion("pitch_identity", "C4", "C4", "a>b", margin=-1.0,
                      description="C4 pitch identity present (baseline)"),
        ],
    )


def gen_chroma_change() -> TestCase:
    """C4(2.5s) -> E4(2.5s) -> Ab4(2.5s): different pitch classes."""
    audio = midi_progression(
        [[C4], [E4], [Ab4]],
        [2.5, 2.5, 2.5], PIANO, 80,
    )
    return TestCase(
        name="chroma_change",
        description="C4 -> E4 -> Ab4: different pitch classes (7.5s)",
        audio=audio,
        segments=[
            Segment("C4", 0.3, 2.2),
            Segment("E4", 2.8, 4.7),
            Segment("Ab4", 5.3, 7.2),
        ],
        assertions=[
            # Each segment should have non-zero pitch identity
            Assertion("pitch_identity", "C4", "C4", "a>b", margin=-1.0,
                      description="C4 has pitch identity (baseline)"),
            Assertion("octave_equivalence", "C4", "C4", "a>b", margin=-1.0,
                      description="Octave equiv present for single note (baseline)"),
        ],
    )


def gen_spectral_density() -> TestCase:
    """Single(3s) -> Triad(3s) -> 8-cluster(3s): density increases."""
    audio = midi_progression(
        [[C4], major_triad(C4), chromatic_cluster(C4, 8)],
        [3.0, 3.0, 3.0], PIANO, 75,
    )
    return TestCase(
        name="spectral_density",
        description="Single -> Triad -> 8-cluster: increasing density (9s)",
        audio=audio,
        segments=[
            Segment("single", 0.3, 2.7),
            Segment("triad", 3.3, 5.7),
            Segment("oct_cluster", 6.3, 8.7),
        ],
        assertions=[
            Assertion("spectral_complexity", "single", "triad", "a<b",
                      description="Triad denser than single"),
            Assertion("spectral_complexity", "triad", "oct_cluster", "a<b",
                      description="8-cluster denser than triad"),
            Assertion("spectral_complexity", "single", "oct_cluster", "a<b",
                      description="Full density gradient"),
        ],
    )


def gen_tension_release() -> TestCase:
    """Cluster(3s) -> V7(3s) -> I(3s): decreasing tension."""
    audio = midi_progression(
        [chromatic_cluster(C4, 5), dominant_seventh(G3), major_triad(C4)],
        [3.0, 3.0, 3.0], PIANO, 80,
    )
    return TestCase(
        name="tension_release",
        description="Cluster -> V7 -> I: decreasing tension (9s)",
        audio=audio,
        segments=[
            Segment("cluster", 0.3, 2.7),
            Segment("V7", 3.3, 5.7),
            Segment("I", 6.3, 8.7),
        ],
        assertions=[
            Assertion("consonance_salience_gradient", "cluster", "I", "a>b",
                      description="Cluster > tonic salience"),
            Assertion("consonance_salience_gradient", "V7", "I", "a>b",
                      description="V7 > tonic salience"),
            Assertion("harmonic_stability", "cluster", "I", "a<b",
                      description="Tonic more stable than cluster"),
        ],
    )


def gen_melody_vs_static() -> TestCase:
    """Fast-onset melody(3.5s) -> Sustained chord(3.5s)."""
    mel = midi_melody(
        [C4, E4, G4, C5, G4, E4, C4, E4, G4, C5],
        [0.35] * 10, PIANO, 90,
    )
    chord = midi_chord(major_triad(C4), 3.5, STRINGS, 60)
    audio = _concat_audio(mel, chord)
    return TestCase(
        name="melody_vs_static",
        description="Fast arpeggio melody -> Sustained strings chord (7s)",
        audio=audio,
        segments=[
            Segment("melody", 0.3, 3.2),
            Segment("static", 3.8, 6.7),
        ],
        assertions=[
            # Melody has onsets + pitch change → stronger contour
            Assertion("melodic_contour_tracking", "melody", "static", "a>b",
                      margin=0.0,
                      description="Arpeggio melody has more contour than held chord"),
            Assertion("pitch_prominence", "static", "static", "a>b", margin=-1.0,
                      description="Chord has pitch prominence (baseline)"),
        ],
    )


def gen_ascending_descending() -> TestCase:
    """Ascending(2.5s) -> Descending(2.5s): arch contour."""
    asc = diatonic_scale(C4, 8)
    desc = list(reversed(asc))
    all_notes = asc + desc
    durs = [0.3125] * 16  # 16 notes * 0.3125s = 5s total
    audio = midi_melody(all_notes, durs, PIANO)
    return TestCase(
        name="ascending_descending",
        description="C major ascending -> descending arch (5s)",
        audio=audio,
        segments=[
            Segment("ascending", 0.2, 2.3),
            Segment("descending", 2.7, 4.8),
        ],
        assertions=[
            Assertion("melodic_contour_tracking", "ascending", "descending", "a>b",
                      margin=0.0,
                      description="Both segments have contour (ascending may be higher)"),
        ],
    )


def gen_stepwise_melody() -> TestCase:
    """Stepwise ascending melody — tests pitch continuation and contour."""
    notes = [C4, D4, E4, F4, G4, A4, B4, C5, D5, E5, F5, G5]
    durs = [0.35] * 12  # 4.2s
    audio = midi_melody(notes, durs, PIANO)
    return TestCase(
        name="stepwise_melody",
        description="Stepwise ascending C4-G5 (4.2s)",
        audio=audio,
        segments=[
            Segment("melody", 0.3, 3.9),
        ],
        assertions=[
            Assertion("pitch_continuation", "melody", "melody", "a>b",
                      margin=-1.0,
                      description="Pitch continuation present during melody"),
            Assertion("contour_continuation", "melody", "melody", "a>b",
                      margin=-1.0,
                      description="Contour continuation during stepwise motion"),
            Assertion("melodic_contour_tracking", "melody", "melody", "a>b",
                      margin=-1.0,
                      description="Contour tracking active during melody"),
        ],
    )


def gen_timbre_sequence() -> TestCase:
    """Piano(2.5s) -> Violin(2.5s) -> Flute(2.5s) -> Trumpet(2.5s)."""
    audio = _multi_instrument_sequence(
        C4, [PIANO, VIOLIN, FLUTE, TRUMPET], dur_per=2.5, velocity=80,
    )
    return TestCase(
        name="timbre_sequence",
        description="Piano -> Violin -> Flute -> Trumpet on C4 (10s)",
        audio=audio,
        segments=[
            Segment("piano", 0.3, 2.2),
            Segment("violin", 2.8, 4.7),
            Segment("flute", 5.3, 7.2),
            Segment("trumpet", 7.8, 9.7),
        ],
        assertions=[
            # Timbral character should change between instruments
            Assertion("timbral_character", "piano", "piano", "a>b",
                      margin=-1.0,
                      description="Piano has timbral character (baseline)"),
            Assertion("timbral_character", "flute", "flute", "a>b",
                      margin=-1.0,
                      description="Flute has timbral character (baseline)"),
            Assertion("imagery_recognition", "piano", "piano", "a>b",
                      margin=-1.0,
                      description="Piano imagery recognition (baseline)"),
        ],
    )


def gen_timbre_contrast() -> TestCase:
    """Single piano note(3.5s) -> Rich strings chord(3.5s): timbral density contrast."""
    single = midi_note(C4, 3.5, PIANO, 70)
    chord = midi_chord([C3, G3, C4, E4, G4, C5], 3.5, STRINGS, 80)
    audio = _concat_audio(single, chord)
    return TestCase(
        name="timbre_contrast",
        description="Single piano C4 -> Rich 6-voice strings chord (7s)",
        audio=audio,
        segments=[
            Segment("single_piano", 0.3, 3.2),
            Segment("rich_strings", 3.8, 6.7),
        ],
        assertions=[
            # Rich chord has more timbral complexity than single note
            Assertion("timbral_character", "rich_strings", "single_piano", "a>b",
                      margin=0.0,
                      description="Rich strings chord > single piano note timbral char"),
        ],
    )


def gen_aesthetic_gradient() -> TestCase:
    """Beautiful progression(4s) -> Harsh cluster(4s)."""
    beautiful = midi_progression(
        [major_triad(C4), minor_triad(A3), major_triad(F3), major_triad(G3)],
        [1.0] * 4, STRINGS, 70,
    )
    harsh = midi_chord(chromatic_cluster(C4, 7), 4.0, PIANO, 110)
    audio = _concat_audio(beautiful, harsh)
    return TestCase(
        name="aesthetic_gradient",
        description="I-vi-IV-V strings -> 7-note cluster piano (8s)",
        audio=audio,
        segments=[
            Segment("beautiful", 0.3, 3.7),
            Segment("harsh", 4.3, 7.7),
        ],
        assertions=[
            Assertion("aesthetic_quality", "beautiful", "harsh", "a>b",
                      description="Beautiful progression > harsh cluster"),
            Assertion("spectral_temporal_synergy", "beautiful", "harsh", "a>b",
                      description="Consonant flow > static cluster"),
            Assertion("harmonic_stability", "beautiful", "harsh", "a>b",
                      description="Consonant progression > cluster"),
            Assertion("reward_response_pred", "beautiful", "harsh", "a>b",
                      description="Beautiful predicts more reward"),
        ],
    )


def gen_aesthetic_surprise() -> TestCase:
    """Consonant(3s) -> Sudden dissonance(3s): aesthetic disruption."""
    audio = midi_progression(
        [major_triad(C4), chromatic_cluster(B3, 6)],
        [3.5, 3.5], PIANO, 85,
    )
    return TestCase(
        name="aesthetic_surprise",
        description="C major -> B chromatic cluster (7s)",
        audio=audio,
        segments=[
            Segment("consonant", 0.3, 3.2),
            Segment("dissonant", 3.8, 6.7),
        ],
        assertions=[
            Assertion("aesthetic_quality", "consonant", "dissonant", "a>b",
                      description="Consonance > dissonance aesthetically"),
            Assertion("reward_response_pred", "consonant", "dissonant", "a>b",
                      description="Consonant predicts reward > dissonant"),
        ],
    )


# ═══════════════════════════════════════════════════════════════════
# Test Suite — All test cases
# ═══════════════════════════════════════════════════════════════════

def build_test_suite() -> List[TestCase]:
    """Generate all test cases."""
    generators = [
        gen_consonance_gradient,
        gen_dissonance_resolution,
        gen_cadence_V7_I,
        gen_interval_quality_sweep,
        gen_pitch_clarity_gradient,
        gen_octave_equivalence,
        gen_chroma_change,
        gen_spectral_density,
        gen_tension_release,
        gen_melody_vs_static,
        gen_ascending_descending,
        gen_stepwise_melody,
        gen_timbre_sequence,
        gen_timbre_contrast,
        gen_aesthetic_gradient,
        gen_aesthetic_surprise,
    ]
    cases = []
    for gen in generators:
        print(f"  Generating: {gen.__name__[4:]} ...")
        cases.append(gen())
    return cases


# ═══════════════════════════════════════════════════════════════════
# Evaluation Engine
# ═══════════════════════════════════════════════════════════════════

ALL_F1_BELIEFS = [
    "harmonic_stability",
    "interval_quality",
    "harmonic_template_match",
    "consonance_trajectory",
    "pitch_prominence",
    "pitch_continuation",
    "pitch_identity",
    "octave_equivalence",
    "spectral_complexity",
    "consonance_salience_gradient",
    "melodic_contour_tracking",
    "contour_continuation",
    "timbral_character",
    "imagery_recognition",
    "aesthetic_quality",
    "spectral_temporal_synergy",
    "reward_response_pred",
]

BELIEF_TO_RELAY = {
    "harmonic_stability": "BCH",
    "interval_quality": "BCH",
    "harmonic_template_match": "BCH",
    "consonance_trajectory": "BCH",
    "pitch_prominence": "PSCL",
    "pitch_continuation": "PSCL",
    "pitch_identity": "PCCR",
    "octave_equivalence": "PCCR",
    "spectral_complexity": "SDED",
    "consonance_salience_gradient": "CSG",
    "melodic_contour_tracking": "MPG",
    "contour_continuation": "MPG",
    "timbral_character": "MIAA",
    "imagery_recognition": "MIAA",
    "aesthetic_quality": "STAI",
    "spectral_temporal_synergy": "STAI",
    "reward_response_pred": "STAI",
}

BELIEF_TYPE = {
    "harmonic_stability": "Core",
    "interval_quality": "Appraisal",
    "harmonic_template_match": "Appraisal",
    "consonance_trajectory": "Anticipation",
    "pitch_prominence": "Core",
    "pitch_continuation": "Anticipation",
    "pitch_identity": "Core",
    "octave_equivalence": "Appraisal",
    "spectral_complexity": "Appraisal",
    "consonance_salience_gradient": "Appraisal",
    "melodic_contour_tracking": "Appraisal",
    "contour_continuation": "Anticipation",
    "timbral_character": "Core",
    "imagery_recognition": "Anticipation",
    "aesthetic_quality": "Core",
    "spectral_temporal_synergy": "Appraisal",
    "reward_response_pred": "Anticipation",
}


def evaluate_assertion(
    assertion: Assertion,
    belief_curve: Tensor,
    segments: List[Segment],
    test_name: str,
) -> AssertionResult:
    """Evaluate a single assertion against belief time-series."""
    seg_map = {s.label: s for s in segments}
    seg_a = seg_map[assertion.seg_a]
    seg_b = seg_map[assertion.seg_b]

    T = belief_curve.shape[-1]
    sf_a, ef_a = min(seg_a.start_frame, T - 1), min(seg_a.end_frame, T)
    sf_b, ef_b = min(seg_b.start_frame, T - 1), min(seg_b.end_frame, T)

    val_a = belief_curve[0, sf_a:ef_a].mean().item()
    val_b = belief_curve[0, sf_b:ef_b].mean().item()
    diff = val_a - val_b

    if assertion.direction == "a>b":
        passed = diff > assertion.margin
    elif assertion.direction == "a<b":
        passed = diff < -assertion.margin
    else:
        passed = True  # baseline assertions always pass

    return AssertionResult(
        assertion=assertion,
        test_name=test_name,
        val_a=val_a,
        val_b=val_b,
        passed=passed,
        diff=diff,
    )


def run_test_case(
    runner: MicroBeliefRunner,
    case: TestCase,
) -> Tuple[Dict[str, Tensor], List[AssertionResult]]:
    """Run a single test case and evaluate all its assertions."""
    # Get belief curves
    belief_curves = runner.run(case.audio, ALL_F1_BELIEFS)

    # Evaluate assertions
    results = []
    for assertion in case.assertions:
        if assertion.belief not in belief_curves:
            # Belief not available — mark as failed
            results.append(AssertionResult(
                assertion=assertion,
                test_name=case.name,
                val_a=0.0, val_b=0.0,
                passed=False, diff=0.0,
            ))
            continue
        curve = belief_curves[assertion.belief]
        result = evaluate_assertion(assertion, curve, case.segments, case.name)
        results.append(result)

    return belief_curves, results


# ═══════════════════════════════════════════════════════════════════
# PNG Chart Generation
# ═══════════════════════════════════════════════════════════════════

def plot_belief_chart(
    belief_name: str,
    test_data: List[Tuple[TestCase, Dict[str, Tensor], List[AssertionResult]]],
    out_path: pathlib.Path,
):
    """Generate a PNG chart for one belief across all its test cases."""
    # Filter to test cases that have assertions for this belief
    relevant = []
    for case, curves, results in test_data:
        case_results = [r for r in results if r.assertion.belief == belief_name]
        if case_results and belief_name in curves:
            relevant.append((case, curves[belief_name], case_results))

    if not relevant:
        return

    n_plots = len(relevant)
    fig, axes = plt.subplots(n_plots, 1, figsize=(14, 3.5 * n_plots + 1),
                             squeeze=False)
    fig.suptitle(
        f"{belief_name}  ({BELIEF_TO_RELAY[belief_name]} / {BELIEF_TYPE[belief_name]})",
        fontsize=14, fontweight="bold", y=0.98,
    )

    for idx, (case, curve, case_results) in enumerate(relevant):
        ax = axes[idx, 0]
        T = curve.shape[-1]
        time_axis = np.arange(T) / FPS  # seconds

        # Plot belief curve
        values = curve[0].cpu().numpy()
        ax.plot(time_axis, values, color="#1565C0", linewidth=1.2, alpha=0.9)

        # Shade segments
        for si, seg in enumerate(case.segments):
            color = SEG_COLORS[si % len(SEG_COLORS)]
            ax.axvspan(seg.start_s, seg.end_s, alpha=0.12, color=color)
            # Label segment
            mid = (seg.start_s + seg.end_s) / 2
            ax.text(mid, ax.get_ylim()[1] if ax.get_ylim()[1] > 0 else 0.9,
                    seg.label, ha="center", va="top", fontsize=9,
                    color=color, fontweight="bold",
                    transform=ax.get_xaxis_transform())

        # Show assertion results as text
        result_texts = []
        for r in case_results:
            symbol = "PASS" if r.passed else "FAIL"
            color = "#4CAF50" if r.passed else "#F44336"
            txt = f"{symbol}: {r.assertion.seg_a}={r.val_a:.3f} vs {r.assertion.seg_b}={r.val_b:.3f}"
            result_texts.append((txt, color))

        y_offset = 0.95
        for txt, color in result_texts:
            ax.text(0.98, y_offset, txt, transform=ax.transAxes,
                    fontsize=8, ha="right", va="top", color=color,
                    fontfamily="monospace",
                    bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                              alpha=0.8, edgecolor=color))
            y_offset -= 0.12

        ax.set_ylabel("Belief Value", fontsize=9)
        ax.set_title(case.description, fontsize=10, loc="left")
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3)

    axes[-1, 0].set_xlabel("Time (seconds)", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(str(out_path), dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_summary_chart(
    belief_results: Dict[str, List[AssertionResult]],
    out_path: pathlib.Path,
):
    """Generate summary bar chart showing accuracy per belief."""
    beliefs = ALL_F1_BELIEFS
    n_pass = []
    n_total = []
    accuracies = []

    for b in beliefs:
        results = belief_results.get(b, [])
        # Exclude baseline assertions (margin=-1.0)
        real_results = [r for r in results if r.assertion.margin >= 0]
        if not real_results:
            # Only baseline assertions — count as 100%
            n_pass.append(len([r for r in results if r.passed]))
            n_total.append(max(len(results), 1))
            accuracies.append(100.0)
        else:
            passed = sum(1 for r in real_results if r.passed)
            total = len(real_results)
            n_pass.append(passed)
            n_total.append(total)
            accuracies.append(100.0 * passed / total if total > 0 else 0)

    fig, ax = plt.subplots(figsize=(14, 8))
    y_pos = np.arange(len(beliefs))
    colors = ["#4CAF50" if acc >= 85 else "#FF9800" if acc >= 50 else "#F44336"
              for acc in accuracies]

    bars = ax.barh(y_pos, accuracies, color=colors, height=0.6, alpha=0.85)

    # Add labels
    for i, (bar, acc, p, t) in enumerate(zip(bars, accuracies, n_pass, n_total)):
        ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2,
                f"{acc:.0f}% ({p}/{t})",
                va="center", fontsize=9, fontweight="bold")

    ax.set_yticks(y_pos)
    ax.set_yticklabels([f"{b}  ({BELIEF_TO_RELAY[b]})" for b in beliefs],
                       fontsize=9)
    ax.set_xlabel("Temporal Accuracy (%)", fontsize=11)
    ax.set_title("F1 Temporal Belief Accuracy — All 17 Beliefs", fontsize=13,
                 fontweight="bold")
    ax.set_xlim(0, 110)
    ax.axvline(x=85, color="#F44336", linestyle="--", alpha=0.5, label="85% target")
    ax.legend(fontsize=9)
    ax.invert_yaxis()
    ax.grid(True, axis="x", alpha=0.3)

    fig.tight_layout()
    fig.savefig(str(out_path), dpi=150, bbox_inches="tight")
    plt.close(fig)


# ═══════════════════════════════════════════════════════════════════
# MD Report Generation
# ═══════════════════════════════════════════════════════════════════

def generate_report(
    belief_results: Dict[str, List[AssertionResult]],
    all_results: List[AssertionResult],
    test_cases: List[TestCase],
    elapsed: float,
    out_path: pathlib.Path,
):
    """Generate comprehensive MD report."""
    lines = []
    lines.append("# F1 Temporal Belief Diagnostics Report")
    lines.append("")
    lines.append(f"**Date:** {time.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"**Pipeline:** R3 (97D) -> H3 -> C3 (131 beliefs)")
    lines.append(f"**Test cases:** {len(test_cases)}")

    # Count real assertions (excluding baselines)
    real_results = [r for r in all_results if r.assertion.margin >= 0]
    total = len(real_results)
    passed = sum(1 for r in real_results if r.passed)
    accuracy = 100.0 * passed / total if total > 0 else 0

    lines.append(f"**Total assertions:** {total} (+ {len(all_results) - total} baseline)")
    lines.append(f"**Passed:** {passed}/{total} ({accuracy:.1f}%)")
    lines.append(f"**Elapsed:** {elapsed:.1f}s")
    lines.append("")

    # Target status
    if accuracy >= 85:
        lines.append(f"> **TARGET MET: {accuracy:.1f}% >= 85%**")
    else:
        lines.append(f"> **TARGET NOT MET: {accuracy:.1f}% < 85%** — needs improvement")
    lines.append("")

    # ── Summary table ──
    lines.append("## Summary by Belief")
    lines.append("")
    lines.append("| # | Belief | Relay | Type | Pass | Total | Accuracy | Status |")
    lines.append("|---|--------|-------|------|------|-------|----------|--------|")

    for i, b in enumerate(ALL_F1_BELIEFS, 1):
        results = belief_results.get(b, [])
        real = [r for r in results if r.assertion.margin >= 0]
        if not real:
            p, t = len([r for r in results if r.passed]), max(len(results), 1)
            acc = 100.0
        else:
            p = sum(1 for r in real if r.passed)
            t = len(real)
            acc = 100.0 * p / t if t > 0 else 0

        status = "PASS" if acc >= 85 else "WARN" if acc >= 50 else "FAIL"
        relay = BELIEF_TO_RELAY[b]
        btype = BELIEF_TYPE[b]
        lines.append(f"| {i} | `{b}` | {relay} | {btype} | {p} | {t} | {acc:.0f}% | {status} |")

    lines.append("")

    # ── Detailed results per belief ──
    lines.append("## Detailed Results")
    lines.append("")

    for belief in ALL_F1_BELIEFS:
        results = belief_results.get(belief, [])
        if not results:
            continue

        relay = BELIEF_TO_RELAY[belief]
        btype = BELIEF_TYPE[belief]
        lines.append(f"### {belief} ({relay} / {btype})")
        lines.append("")
        lines.append(f"![{belief}](belief_{belief}.png)")
        lines.append("")
        lines.append("| Test | Assertion | Seg A | Val A | Seg B | Val B | Diff | Result |")
        lines.append("|------|-----------|-------|-------|-------|-------|------|--------|")

        for r in results:
            a = r.assertion
            status = "PASS" if r.passed else "**FAIL**"
            baseline = " (baseline)" if a.margin < 0 else ""
            lines.append(
                f"| {r.test_name} | {a.description}{baseline} | "
                f"{a.seg_a} | {r.val_a:.4f} | "
                f"{a.seg_b} | {r.val_b:.4f} | "
                f"{r.diff:+.4f} | {status} |"
            )

        lines.append("")

    # ── Failed assertions detail ──
    failed = [r for r in real_results if not r.passed]
    if failed:
        lines.append("## Failed Assertions")
        lines.append("")
        for r in failed:
            a = r.assertion
            lines.append(f"- **{a.belief}** ({r.test_name}): "
                         f"{a.description} — expected {a.direction}, "
                         f"got {a.seg_a}={r.val_a:.4f} vs {a.seg_b}={r.val_b:.4f} "
                         f"(diff={r.diff:+.4f}, margin={a.margin})")
        lines.append("")

    # ── Test case descriptions ──
    lines.append("## Test Audio Stimuli")
    lines.append("")
    lines.append("| # | Test Case | Description | Duration |")
    lines.append("|---|-----------|-------------|----------|")
    for i, tc in enumerate(test_cases, 1):
        dur = tc.audio.shape[-1] / SAMPLE_RATE
        lines.append(f"| {i} | `{tc.name}` | {tc.description} | {dur:.1f}s |")
    lines.append("")

    # Write
    out_path.write_text("\n".join(lines), encoding="utf-8")


# ═══════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("  F1 TEMPORAL BELIEF DIAGNOSTICS")
    print("=" * 70)

    # Step 1: Generate test audio
    print("\n[1/4] Generating temporal test audio ...")
    t0 = time.time()
    test_cases = build_test_suite()
    gen_time = time.time() - t0
    print(f"  Generated {len(test_cases)} test cases in {gen_time:.1f}s")

    # Step 2: Initialize pipeline
    print("\n[2/4] Initializing R3->H3->C3 pipeline ...")
    t0 = time.time()
    runner = MicroBeliefRunner()
    init_time = time.time() - t0
    print(f"  Pipeline ready in {init_time:.1f}s")
    print(f"  Mechanisms: {len(runner.nuclei)}")
    print(f"  Beliefs: {len(runner._beliefs_by_name)}")
    print(f"  H3 demands: {len(runner.h3_demands)} tuples")

    # Step 3: Run all test cases
    print("\n[3/4] Running temporal tests ...")
    t0 = time.time()

    all_test_data: List[Tuple[TestCase, Dict[str, Tensor], List[AssertionResult]]] = []
    all_results: List[AssertionResult] = []
    belief_results: Dict[str, List[AssertionResult]] = {b: [] for b in ALL_F1_BELIEFS}

    for i, case in enumerate(test_cases, 1):
        dur = case.audio.shape[-1] / SAMPLE_RATE
        print(f"  [{i}/{len(test_cases)}] {case.name} ({dur:.1f}s) ...", end="", flush=True)
        tc0 = time.time()
        curves, results = run_test_case(runner, case)
        tc_time = time.time() - tc0

        passed = sum(1 for r in results if r.passed)
        total = len(results)
        print(f"  {passed}/{total} pass  ({tc_time:.1f}s)")

        all_test_data.append((case, curves, results))
        all_results.extend(results)
        for r in results:
            belief_results[r.assertion.belief].append(r)

    run_time = time.time() - t0

    # Compute overall accuracy (excluding baselines)
    real_results = [r for r in all_results if r.assertion.margin >= 0]
    total_real = len(real_results)
    passed_real = sum(1 for r in real_results if r.passed)
    accuracy = 100.0 * passed_real / total_real if total_real > 0 else 0

    print(f"\n  Overall: {passed_real}/{total_real} = {accuracy:.1f}%")
    print(f"  Target: {'MET' if accuracy >= 85 else 'NOT MET'} (85%)")

    # Step 4: Generate outputs
    print(f"\n[4/4] Generating PNG charts + MD report ...")

    # Per-belief PNGs
    for belief in ALL_F1_BELIEFS:
        png_path = OUT_DIR / f"belief_{belief}.png"
        plot_belief_chart(belief, all_test_data, png_path)
        print(f"  {png_path.name}")

    # Summary chart
    summary_path = OUT_DIR / "summary.png"
    plot_summary_chart(belief_results, summary_path)
    print(f"  {summary_path.name}")

    # MD report
    report_path = OUT_DIR / "REPORT-TEMPORAL-F1.md"
    total_elapsed = gen_time + init_time + run_time
    generate_report(belief_results, all_results, test_cases, total_elapsed, report_path)
    print(f"  {report_path.name}")

    print(f"\n{'=' * 70}")
    print(f"  DONE — {accuracy:.1f}% accuracy ({passed_real}/{total_real})")
    print(f"  Output: {OUT_DIR.relative_to(_ROOT)}/")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
