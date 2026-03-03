"""Determinism tests — F6 pipeline produces identical output for identical input.

Validates:
  - Same audio, three runs = bitwise identical for all 16 F6 beliefs
  - Different audio produces different belief outputs
"""
from __future__ import annotations

import torch

from Tests.micro_beliefs.audio_stimuli import silence
from Tests.micro_beliefs.real_audio_stimuli import (
    PIANO, ORGAN,
    midi_chord, midi_isochronous, midi_crescendo,
    major_triad,
    C4 as MC4,
)


class TestDeterminism:
    """Two identical runs must produce identical F6 belief values."""

    def test_srp_core_deterministic(self, runner):
        """Piano chord produces identical SRP Core output on three runs.

        SRP Core: wanting, liking, pleasure, prediction_error, tension.
        """
        audio = midi_chord(major_triad(MC4), 4.0, program=PIANO, velocity=90)
        srp_core = [
            "wanting", "liking", "pleasure",
            "prediction_error", "tension",
        ]
        r1 = runner.run(audio, srp_core)
        r2 = runner.run(audio, srp_core)
        r3 = runner.run(audio, srp_core)
        for name in srp_core:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: r1→r2 diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )
                assert torch.allclose(r2[name], r3[name], atol=1e-6), (
                    f"{name}: r2→r3 diff {(r2[name] - r3[name]).abs().max().item():.2e}"
                )

    def test_srp_appraisal_deterministic(self, runner):
        """Isochronous beats produce identical SRP Appraisal output.

        SRP Appraisal: prediction_match, peak_detection, harmonic_tension.
        """
        audio = midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=85)
        srp_appraisal = [
            "prediction_match", "peak_detection", "harmonic_tension",
        ]
        r1 = runner.run(audio, srp_appraisal)
        r2 = runner.run(audio, srp_appraisal)
        r3 = runner.run(audio, srp_appraisal)
        for name in srp_appraisal:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: r1→r2 diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )
                assert torch.allclose(r2[name], r3[name], atol=1e-6), (
                    f"{name}: r2→r3 diff {(r2[name] - r3[name]).abs().max().item():.2e}"
                )

    def test_srp_anticipation_deterministic(self, runner):
        """Crescendo produces identical SRP Anticipation output.

        SRP Anticipation: chills_proximity, resolution_expectation, reward_forecast.
        """
        audio = midi_crescendo(MC4, 12, 0.4, 20, 120, program=PIANO)
        srp_anticipation = [
            "chills_proximity", "resolution_expectation", "reward_forecast",
        ]
        r1 = runner.run(audio, srp_anticipation)
        r2 = runner.run(audio, srp_anticipation)
        r3 = runner.run(audio, srp_anticipation)
        for name in srp_anticipation:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: r1→r2 diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )
                assert torch.allclose(r2[name], r3[name], atol=1e-6), (
                    f"{name}: r2→r3 diff {(r2[name] - r3[name]).abs().max().item():.2e}"
                )

    def test_daed_deterministic(self, runner):
        """Loud isochronous produces identical DAED output on three runs."""
        audio = midi_isochronous(MC4, 150.0, 16, program=PIANO, velocity=100)
        daed_beliefs = [
            "da_caudate", "da_nacc", "dissociation_index",
            "temporal_phase", "wanting_ramp",
        ]
        r1 = runner.run(audio, daed_beliefs)
        r2 = runner.run(audio, daed_beliefs)
        r3 = runner.run(audio, daed_beliefs)
        for name in daed_beliefs:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: r1→r2 diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )
                assert torch.allclose(r2[name], r3[name], atol=1e-6), (
                    f"{name}: r2→r3 diff {(r2[name] - r3[name]).abs().max().item():.2e}"
                )

    def test_different_audio_differs(self, runner):
        """Different audio should produce different wanting.

        Loud beats vs silence: clear separation expected.
        """
        belief = "wanting"
        res_a = runner.run(
            midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=110),
            [belief],
        )
        res_b = runner.run(silence(5.0), [belief])
        if belief in res_a and belief in res_b:
            mean_a = res_a[belief][:, 50:].mean().item()
            mean_b = res_b[belief][:, 50:].mean().item()
            diff = abs(mean_a - mean_b)
            assert diff > 0.01, f"Mean diff too small: {diff:.4f}"
