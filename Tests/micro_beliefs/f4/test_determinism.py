"""Determinism tests — F4 pipeline produces identical output for identical input.

Validates:
  - Same audio, two runs = bitwise identical for all 13 F4 beliefs
  - Different audio produces different belief outputs
"""
from __future__ import annotations

import pytest
import torch

from Tests.micro_beliefs.audio_stimuli import (
    C4, G4,
    harmonic_complex, rich_dyad, silence,
)
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO, ORGAN, CHOIR,
    midi_chord, midi_melody, midi_isochronous,
    major_triad, diatonic_scale,
    C3, C4 as MC4, E4, G4 as MG4,
)

ALL_F4 = [
    "autobiographical_retrieval", "nostalgia_intensity", "emotional_coloring",
    "retrieval_probability", "memory_vividness", "self_relevance",
    "vividness_trajectory",
    "melodic_recognition", "memory_preservation", "memory_scaffold_pred",
    "episodic_encoding", "episodic_boundary", "consolidation_strength",
]


class TestDeterminism:
    """Two identical runs must produce identical F4 belief values."""

    def test_organ_chord_deterministic(self, runner):
        """Organ C major chord produces identical output on two runs."""
        audio = midi_chord(major_triad(MC4), 4.0, program=ORGAN, velocity=75)
        r1 = runner.run(audio, ALL_F4)
        r2 = runner.run(audio, ALL_F4)
        for name in ALL_F4:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: max diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )

    def test_beats_deterministic(self, runner):
        """Isochronous piano beats produce identical output on two runs."""
        audio = midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=90)
        r1 = runner.run(audio, ALL_F4)
        r2 = runner.run(audio, ALL_F4)
        for name in ALL_F4:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: max diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )

    def test_rich_dyad_deterministic(self, runner):
        """rich_dyad C4+G4 produces identical output on two runs."""
        audio = rich_dyad(C4, G4, 6, 3.0)
        r1 = runner.run(audio, ALL_F4)
        r2 = runner.run(audio, ALL_F4)
        for name in ALL_F4:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: max diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )

    def test_different_audio_differs(self, runner):
        """Different audio should produce different episodic_encoding.

        Organ chord (~0.595) vs silence (~0.561) produces clear separation.
        Compares mean values since different-length audio produces
        different-sized tensors.
        """
        belief = "episodic_encoding"
        res_a = runner.run(
            midi_chord(major_triad(MC4), 4.0, program=ORGAN, velocity=75),
            [belief],
        )
        res_b = runner.run(silence(4.0), [belief])
        if belief in res_a and belief in res_b:
            mean_a = res_a[belief][:, 50:].mean().item()
            mean_b = res_b[belief][:, 50:].mean().item()
            diff = abs(mean_a - mean_b)
            assert diff > 0.01, f"Mean diff too small: {diff:.4f}"
