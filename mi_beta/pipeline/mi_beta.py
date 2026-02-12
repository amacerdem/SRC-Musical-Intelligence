"""
MIBetaPipeline -- Main MI-Beta pipeline: audio -> MI-space.

Data flow:
    audio -> cochlea(128D) -> R3(49D+) -> H3(sparse) -> Brain(variable) -> L3(variable)
    -> MI-space = [cochlea | r3 | brain | l3]

The total MI-space dimensionality is dynamic, depending on which cognitive
units and models are active.  The pipeline tracks section ranges so that
downstream consumers can extract any component by name.

Usage::

    from mi_beta.pipeline import MIBetaPipeline

    pipeline = MIBetaPipeline()
    output = pipeline.process(waveform)

    print(output.total_dim)          # e.g. 177 + brain_dim
    print(output.cochlea_range)      # (0, 128)
    print(output.r3_range)           # (128, 177)
    print(output.brain_range)        # (177, 177 + brain_dim)
"""

from __future__ import annotations

import logging
from typing import Optional, Tuple

import torch
from torch import Tensor

from mi_beta.core.config import MIBetaConfig, MI_BETA_CONFIG
from mi_beta.core.types import (
    MIBetaOutput,
    CochleaOutput,
    R3Output,
    H3Output,
    BrainOutput,
    L3Output,
)
from mi_beta.ear.cochlea import audio_to_mel
from mi_beta.ear.r3 import R3Extractor
from mi_beta.ear.h3 import H3Extractor
from mi_beta.pipeline.brain_runner import BrainOrchestrator

logger = logging.getLogger(__name__)


class MIBetaPipeline:
    """Full audio -> MI-space orchestrator.

    Data flow:
        audio -> cochlea(128D) -> R3(49D+) -> H3(sparse) -> Brain(variable) -> L3(variable)
        -> MI-space = [cochlea | r3 | brain | l3]

    Args:
        config: MIBetaConfig for audio/pipeline settings.
        active_units: Tuple of unit names to activate in the brain.
            Defaults to all 9 units.
    """

    def __init__(
        self,
        config: Optional[MIBetaConfig] = None,
        active_units: Optional[Tuple[str, ...]] = None,
    ) -> None:
        self.config = config or MI_BETA_CONFIG

        # Ear
        self.r3_extractor = R3Extractor(self.config)
        self.h3_extractor = H3Extractor(self.config)

        # Brain
        self.brain = BrainOrchestrator(active_units=active_units)

        # TODO: L3 orchestrator

    def process(
        self,
        waveform: Tensor,
        return_ear: bool = False,
    ) -> MIBetaOutput:
        """Process audio waveform through the full MI-Beta pipeline.

        Args:
            waveform: (B, samples) or (samples,) audio tensor at the
                configured sample rate.
            return_ear: If True, include raw EarOutput in the result.

        Returns:
            MIBetaOutput with assembled MI-space tensor and per-section
            ranges for cochlea, R3, brain, and (future) L3.
        """
        # ── EAR ────────────────────────────────────────────────────────
        cochlea = audio_to_mel(waveform, self.config)
        r3 = self.r3_extractor.extract(cochlea.mel)

        # H3 demand: aggregate from all active models
        # Placeholder: empty demand set (models declare their own demands)
        demand: set[Tuple[int, int, int, int]] = set()
        h3 = self.h3_extractor.extract(r3.features, demand)

        # ── BRAIN ──────────────────────────────────────────────────────
        brain_output = self.brain.compute(h3.features, r3.features)

        # ── ASSEMBLE MI-SPACE ──────────────────────────────────────────
        # Cochlea mel: (B, N_MELS, T) -> (B, T, 128)
        mel_t = cochlea.mel.transpose(1, 2)
        # R3: already (B, T, 49)
        r3_t = r3.features
        # Brain: (B, T, brain_dim)
        brain_t = brain_output.tensor

        cochlea_end = self.config.n_mels  # 128
        r3_end = cochlea_end + r3_t.shape[-1]
        brain_end = r3_end + brain_t.shape[-1]

        mi_space = torch.cat([mel_t, r3_t, brain_t], dim=-1)

        # Build ear output if requested
        from mi_beta.core.types import EarOutput
        ear_output = None
        if return_ear:
            ear_output = EarOutput(cochlea=cochlea, r3=r3, h3=h3)

        return MIBetaOutput(
            mi_space=mi_space,
            cochlea_range=(0, cochlea_end),
            r3_range=(cochlea_end, r3_end),
            brain_range=(r3_end, brain_end),
            brain=brain_output,
            ear=ear_output,
        )

    # ── Properties ─────────────────────────────────────────────────────

    @property
    def total_dim(self) -> int:
        """Total MI-space dimensionality (cochlea + R3 + brain).

        Note: L3 is not yet included.
        """
        return (
            self.config.n_mels
            + self.r3_extractor.total_dim
            + self.brain.unit_runner.total_dim
        )

    @property
    def cochlea_dim(self) -> int:
        """Cochlea (mel spectrogram) dimensionality."""
        return self.config.n_mels

    @property
    def r3_dim(self) -> int:
        """R3 spectral feature dimensionality."""
        return self.r3_extractor.total_dim

    @property
    def brain_dim(self) -> int:
        """Brain output dimensionality (all active units)."""
        return self.brain.unit_runner.total_dim

    # ── Introspection ──────────────────────────────────────────────────

    def summary(self) -> dict:
        """Return a summary dict for debugging / logging."""
        return {
            "total_dim": self.total_dim,
            "cochlea_dim": self.cochlea_dim,
            "r3_dim": self.r3_dim,
            "brain_dim": self.brain_dim,
            "active_units": self.brain.active_unit_names,
            "config": repr(self.config),
        }

    def __repr__(self) -> str:
        return (
            f"MIBetaPipeline("
            f"dim={self.total_dim}, "
            f"cochlea={self.cochlea_dim}, "
            f"r3={self.r3_dim}, "
            f"brain={self.brain_dim})"
        )
