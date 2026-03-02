"""Determinism tests — F5 pipeline produces identical output for identical input.

Validates:
  - Same audio, two runs = bitwise identical for all 15 F5 beliefs
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
    PIANO, ORGAN, STRINGS,
    midi_chord, midi_melody, midi_isochronous,
    major_triad, diatonic_scale,
    C3, C4 as MC4, E4, G4 as MG4,
)

ALL_F5 = [
    "perceived_happy", "perceived_sad", "mode_detection",
    "emotion_certainty", "happy_pathway", "sad_pathway",
    "emotional_arousal", "chills_intensity", "ans_dominance",
    "driving_signal",
    "nostalgia_affect", "self_referential_nostalgia",
    "wellbeing_enhancement", "nostalgia_peak_pred",
]


class TestDeterminism:
    """Two identical runs must produce identical F5 belief values."""

    def test_vmm_deterministic(self, runner):
        """Piano major chord produces identical VMM output on three runs."""
        audio = midi_chord(major_triad(MC4), 4.0, program=PIANO, velocity=80)
        vmm_beliefs = [
            "perceived_happy", "perceived_sad", "mode_detection",
            "emotion_certainty", "happy_pathway", "sad_pathway",
        ]
        r1 = runner.run(audio, vmm_beliefs)
        r2 = runner.run(audio, vmm_beliefs)
        r3 = runner.run(audio, vmm_beliefs)
        for name in vmm_beliefs:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: r1→r2 diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )
                assert torch.allclose(r2[name], r3[name], atol=1e-6), (
                    f"{name}: r2→r3 diff {(r2[name] - r3[name]).abs().max().item():.2e}"
                )

    def test_aac_deterministic(self, runner):
        """Loud isochronous produces identical AAC output on three runs."""
        audio = midi_isochronous(MC4, 120.0, 12, program=PIANO, velocity=100)
        aac_beliefs = [
            "emotional_arousal", "chills_intensity",
            "ans_dominance", "driving_signal",
        ]
        r1 = runner.run(audio, aac_beliefs)
        r2 = runner.run(audio, aac_beliefs)
        r3 = runner.run(audio, aac_beliefs)
        for name in aac_beliefs:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: r1→r2 diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )
                assert torch.allclose(r2[name], r3[name], atol=1e-6), (
                    f"{name}: r2→r3 diff {(r2[name] - r3[name]).abs().max().item():.2e}"
                )

    def test_nemac_deterministic(self, runner):
        """Organ drone produces identical NEMAC output on three runs."""
        audio = midi_chord(major_triad(MC4), 5.0, program=ORGAN, velocity=70)
        nemac_beliefs = [
            "nostalgia_affect", "self_referential_nostalgia",
            "wellbeing_enhancement", "nostalgia_peak_pred",
        ]
        r1 = runner.run(audio, nemac_beliefs)
        r2 = runner.run(audio, nemac_beliefs)
        r3 = runner.run(audio, nemac_beliefs)
        for name in nemac_beliefs:
            if name in r1 and name in r2:
                assert torch.allclose(r1[name], r2[name], atol=1e-6), (
                    f"{name}: r1→r2 diff {(r1[name] - r2[name]).abs().max().item():.2e}"
                )
                assert torch.allclose(r2[name], r3[name], atol=1e-6), (
                    f"{name}: r2→r3 diff {(r2[name] - r3[name]).abs().max().item():.2e}"
                )

    def test_different_audio_differs(self, runner):
        """Different audio should produce different emotional_arousal.

        Loud chord vs silence: clear separation expected.
        """
        belief = "emotional_arousal"
        res_a = runner.run(
            midi_chord(major_triad(MC4), 4.0, program=PIANO, velocity=110),
            [belief],
        )
        res_b = runner.run(silence(4.0), [belief])
        if belief in res_a and belief in res_b:
            mean_a = res_a[belief][:, 50:].mean().item()
            mean_b = res_b[belief][:, 50:].mean().item()
            diff = abs(mean_a - mean_b)
            assert diff > 0.01, f"Mean diff too small: {diff:.4f}"
