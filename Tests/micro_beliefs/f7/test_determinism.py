"""Determinism tests — F7 pipeline produces identical output on repeated runs.

Validates that the full R³→H³→C³ pipeline for all F7 beliefs is
deterministic: same waveform in → same belief time-series out.
"""
from __future__ import annotations

import torch

from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO,
    midi_isochronous, midi_chord, midi_melody,
    major_triad, diatonic_scale,
    C4 as MC4,
)

F7_ALL_BELIEFS = [
    "period_entrainment", "kinematic_efficiency",
    "timing_precision", "period_lock_strength", "next_beat_pred",
    "groove_quality", "beat_prominence", "meter_structure",
    "auditory_motor_coupling", "motor_preparation", "groove_trajectory",
    "context_depth", "short_context", "medium_context", "long_context",
    "phrase_boundary_pred", "structure_pred",
]


class TestDeterminism:
    """Same input → identical belief output on two runs."""

    def test_determinism_isochronous(self, runner):
        """Isochronous beats: two runs produce identical belief tensors."""
        audio = midi_isochronous(MC4, 120.0, 16, program=PIANO, velocity=80)
        run1 = runner.run(audio, F7_ALL_BELIEFS)
        run2 = runner.run(audio, F7_ALL_BELIEFS)
        for b in F7_ALL_BELIEFS:
            assert torch.allclose(run1[b], run2[b], atol=1e-6), (
                f"Non-deterministic output for {b}"
            )

    def test_determinism_chord(self, runner):
        """Sustained chord: two runs produce identical belief tensors."""
        audio = midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80)
        run1 = runner.run(audio, F7_ALL_BELIEFS)
        run2 = runner.run(audio, F7_ALL_BELIEFS)
        for b in F7_ALL_BELIEFS:
            assert torch.allclose(run1[b], run2[b], atol=1e-6), (
                f"Non-deterministic output for {b}"
            )

    def test_determinism_melody(self, runner):
        """Diatonic melody: two runs produce identical belief tensors."""
        audio = midi_melody(
            diatonic_scale(MC4, 8), [0.5] * 8,
            program=PIANO, velocity=80,
        )
        run1 = runner.run(audio, F7_ALL_BELIEFS)
        run2 = runner.run(audio, F7_ALL_BELIEFS)
        for b in F7_ALL_BELIEFS:
            assert torch.allclose(run1[b], run2[b], atol=1e-6), (
                f"Non-deterministic output for {b}"
            )
