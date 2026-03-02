"""Determinism tests — F1 pipeline produces identical output for identical input.

Validates:
  - Same audio, two runs = bitwise identical
  - Different audio produces different output
"""
from __future__ import annotations

import pytest
import torch

from Tests.micro_beliefs.audio_stimuli import (
    C4, G4,
    harmonic_complex, noise, rich_dyad,
)

ALL_F1 = [
    "harmonic_stability", "interval_quality", "harmonic_template_match",
    "consonance_trajectory", "pitch_prominence", "pitch_continuation",
    "pitch_identity", "octave_equivalence", "timbral_character",
    "imagery_recognition", "melodic_contour_tracking", "contour_continuation",
    "spectral_complexity", "consonance_salience_gradient", "aesthetic_quality",
    "spectral_temporal_synergy", "reward_response_pred",
]


class TestDeterminism:
    """Two identical runs must produce identical belief values."""

    def test_dyad_deterministic(self, runner):
        """rich_dyad C4+G4 produces identical output on two runs."""
        audio = rich_dyad(C4, G4, 6, 3.0)
        r1 = runner.run(audio, ALL_F1)
        r2 = runner.run(audio, ALL_F1)
        for name in ALL_F1:
            assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                f"{name}: max diff {(r1[name] - r2[name]).abs().max().item():.2e}"
            )

    def test_harmonic_deterministic(self, runner):
        """harmonic_complex C4 produces identical output on two runs."""
        audio = harmonic_complex(C4, 8, 3.0)
        r1 = runner.run(audio, ALL_F1)
        r2 = runner.run(audio, ALL_F1)
        for name in ALL_F1:
            assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                f"{name}: max diff {(r1[name] - r2[name]).abs().max().item():.2e}"
            )

    def test_different_audio_differs(self, runner):
        """Different audio should produce different harmonic_stability."""
        res_a = runner.run(rich_dyad(C4, G4, 6, 3.0), ["harmonic_stability"])
        res_b = runner.run(noise(3.0), ["harmonic_stability"])
        diff = (res_a["harmonic_stability"] - res_b["harmonic_stability"]).abs().mean().item()
        assert diff > 0.01, f"Mean diff too small: {diff:.4f}"
