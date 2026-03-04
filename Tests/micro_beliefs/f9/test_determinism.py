"""Determinism tests — F9 pipeline produces identical output on repeated runs.

Validates that the full R³→H³→C³ pipeline for all F9 beliefs is
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

F9_ALL_BELIEFS = [
    "neural_synchrony", "catchiness_pred",
    "synchrony_reward", "social_bonding", "group_flow",
    "entrainment_quality", "social_prediction_error",
    "collective_pleasure_pred",
    "social_coordination", "resource_allocation",
]


class TestDeterminism:
    """Same input → identical belief output on two runs."""

    def test_determinism_isochronous(self, runner):
        """Isochronous beats: two runs produce identical belief tensors."""
        audio = midi_isochronous(MC4, 120.0, 16, program=PIANO, velocity=80)
        run1 = runner.run(audio, F9_ALL_BELIEFS)
        run2 = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert torch.allclose(run1[b], run2[b], atol=1e-6), (
                f"Non-deterministic output for {b}"
            )

    def test_determinism_chord(self, runner):
        """Sustained chord: two runs produce identical belief tensors."""
        audio = midi_chord(major_triad(MC4), 5.0, program=PIANO, velocity=80)
        run1 = runner.run(audio, F9_ALL_BELIEFS)
        run2 = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert torch.allclose(run1[b], run2[b], atol=1e-6), (
                f"Non-deterministic output for {b}"
            )

    def test_determinism_melody(self, runner):
        """Diatonic melody: two runs produce identical belief tensors."""
        audio = midi_melody(
            diatonic_scale(MC4, 8), [0.5] * 8,
            program=PIANO, velocity=80,
        )
        run1 = runner.run(audio, F9_ALL_BELIEFS)
        run2 = runner.run(audio, F9_ALL_BELIEFS)
        for b in F9_ALL_BELIEFS:
            assert torch.allclose(run1[b], run2[b], atol=1e-6), (
                f"Non-deterministic output for {b}"
            )
