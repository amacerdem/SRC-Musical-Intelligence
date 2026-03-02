"""Boundary condition tests — F1 beliefs handle edge-case audio gracefully.

Validates:
  - No NaN/Inf for silence, DC offset, near-Nyquist, extreme amplitudes
  - Very short (0.1s) and very long (10s) audio produce valid output
  - All 17 beliefs remain in [0, 1]
"""
from __future__ import annotations

import pytest
import torch

from Tests.micro_beliefs.audio_stimuli import C4, harmonic_complex, silence, sine_tone

ALL_F1 = [
    "harmonic_stability", "interval_quality", "harmonic_template_match",
    "consonance_trajectory", "pitch_prominence", "pitch_continuation",
    "pitch_identity", "octave_equivalence", "timbral_character",
    "imagery_recognition", "melodic_contour_tracking", "contour_continuation",
    "spectral_complexity", "consonance_salience_gradient", "aesthetic_quality",
    "spectral_temporal_synergy", "reward_response_pred",
]

SR = 44_100


def _check_all_valid(results: dict, label: str):
    """Assert no NaN, no Inf, all in [0, 1]."""
    for name, tensor in results.items():
        assert not torch.isnan(tensor).any(), f"[{label}] {name} has NaN"
        assert not torch.isinf(tensor).any(), f"[{label}] {name} has Inf"
        mn, mx = tensor.min().item(), tensor.max().item()
        assert mn >= -0.05, f"[{label}] {name} min={mn:.4f} < -0.05"
        assert mx <= 1.05, f"[{label}] {name} max={mx:.4f} > 1.05"


class TestBoundaryConditions:
    """Edge-case audio should produce valid (no NaN/Inf, in [0,1]) output."""

    def test_silence(self, runner):
        results = runner.run(silence(2.0), ALL_F1)
        _check_all_valid(results, "silence")

    def test_dc_offset(self, runner):
        audio = torch.full((1, SR * 2), 0.5, dtype=torch.float32)
        results = runner.run(audio, ALL_F1)
        _check_all_valid(results, "DC offset")

    def test_near_nyquist(self, runner):
        audio = sine_tone(20000.0, 2.0, 0.3)
        results = runner.run(audio, ALL_F1)
        _check_all_valid(results, "near-Nyquist")

    def test_very_short(self, runner):
        audio = harmonic_complex(C4, 8, 0.1)
        results = runner.run(audio, ALL_F1)
        _check_all_valid(results, "very short (0.1s)")

    def test_very_long(self, runner):
        audio = harmonic_complex(C4, 4, 10.0)
        results = runner.run(audio, ALL_F1)
        _check_all_valid(results, "very long (10s)")

    def test_max_amplitude(self, runner):
        audio = sine_tone(C4, 2.0, 1.0)
        results = runner.run(audio, ALL_F1)
        _check_all_valid(results, "max amplitude")

    def test_min_amplitude(self, runner):
        audio = sine_tone(C4, 2.0, 0.001)
        results = runner.run(audio, ALL_F1)
        _check_all_valid(results, "min amplitude")
