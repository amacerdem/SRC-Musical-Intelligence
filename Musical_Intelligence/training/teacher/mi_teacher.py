"""MITeacher -- Wraps the deterministic MI Teacher pipeline for training.

Integrates the existing R3Extractor, H3Extractor, and BrainOrchestrator
into a single ``compute(mel) -> TeacherOutput`` interface that generates
ground truth labels at every intermediate layer of the MI pipeline.

The MI Teacher is fully deterministic with zero learnable parameters.
All outputs are scientifically traceable to formulas and citations.

Usage::

    teacher = MITeacher()
    output = teacher.compute(mel)
    # output.mel:      (B, T, 128)  -- mel spectrogram
    # output.r3:       (B, T, 128)  -- R3 spectral features
    # output.h3_dense: (B, T, N)    -- densified H3 temporal features
    # output.c3:       (B, T, 1006) -- C3 cognitive model outputs
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import torch
from torch import Tensor

from Musical_Intelligence.brain.orchestrator import BrainOrchestrator
from Musical_Intelligence.data.h3_densifier import H3Densifier
from Musical_Intelligence.ear.h3.extractor import H3Extractor
from Musical_Intelligence.ear.r3.extractor import R3Extractor
from Musical_Intelligence.training.teacher.h3_demand_collector import H3DemandCollector


# ======================================================================
# TeacherOutput
# ======================================================================

@dataclass(frozen=True)
class TeacherOutput:
    """Ground truth labels at every MI pipeline layer.

    All tensors share the same batch and time dimensions.

    Attributes:
        mel:      ``(B, T, 128)`` log-mel spectrogram (transposed from input).
        r3:       ``(B, T, 128)`` R3 spectral features in ``[0, 1]``.
        h3_dense: ``(B, T, N)`` densified H3 temporal features in ``[0, 1]``.
                  ``N`` is the number of unique demands (~5210).
        c3:       ``(B, T, 1006)`` C3 cognitive model outputs in ``[0, 1]``.
    """

    mel: Tensor
    r3: Tensor
    h3_dense: Tensor
    c3: Tensor


# ======================================================================
# MITeacher
# ======================================================================

class MITeacher:
    """Deterministic MI Teacher pipeline for training label generation.

    Reuses the existing Musical_Intelligence components:

    - ``R3Extractor``: mel (B, 128, T) -> R3Output (B, T, 128)
    - ``H3Extractor``: R3 + demand_set -> H3Output (sparse dict)
    - ``BrainOrchestrator``: H3 + R3 -> BrainOutput (B, T, 1006)

    The H3 output is converted to dense form via ``H3Densifier`` using
    the canonical ordering from ``H3DemandCollector``.

    All computation is performed with ``torch.no_grad()`` since the
    teacher has zero learnable parameters.
    """

    def __init__(self) -> None:
        # Collect all H3 demands from 96 models
        self._collector = H3DemandCollector()
        self._demand_set = set(self._collector.demand_list)

        # Build densifier for sparse -> dense H3 conversion
        self._densifier = H3Densifier(
            self._collector.demand_list,
            self._collector.index_map,
        )

        # Instantiate pipeline components
        self._r3_extractor = R3Extractor()
        self._h3_extractor = H3Extractor()
        self._brain = BrainOrchestrator()

    # ------------------------------------------------------------------
    # Properties
    # ------------------------------------------------------------------

    @property
    def n_h3_demands(self) -> int:
        """Number of unique H3 demands (~5210)."""
        return self._collector.n_demands

    @property
    def densifier(self) -> H3Densifier:
        """Access the H3 densifier for external use."""
        return self._densifier

    @property
    def collector(self) -> H3DemandCollector:
        """Access the demand collector for external use."""
        return self._collector

    # ------------------------------------------------------------------
    # Compute
    # ------------------------------------------------------------------

    @torch.no_grad()
    def compute(self, mel: Tensor) -> TeacherOutput:
        """Run the full MI Teacher pipeline on a mel spectrogram.

        Parameters
        ----------
        mel : Tensor
            Shape ``(B, 128, T)`` log-mel spectrogram, log1p normalised.
            Frame rate 172.27 Hz (sr=44100, hop_length=256).

        Returns
        -------
        TeacherOutput
            Frozen dataclass with labels at every pipeline layer.
        """
        B, N, T = mel.shape

        # Transpose mel for output: (B, 128, T) -> (B, T, 128)
        mel_transposed = mel.transpose(1, 2).contiguous()

        # Stage 1: R3 spectral extraction
        r3_output = self._r3_extractor.extract(mel)
        r3_features = r3_output.features  # (B, T, 128)

        # Stage 2: H3 temporal morphology (demand-driven, slow)
        h3_output = self._h3_extractor.extract(r3_features, self._demand_set)

        # Stage 3: C3 cognitive models
        brain_output = self._brain.forward(h3_output.features, r3_features)
        c3 = brain_output.tensor  # (B, T, 1006)

        # Convert sparse H3 to dense
        h3_dense = self._densifier.densify(h3_output.features)

        return TeacherOutput(
            mel=mel_transposed,
            r3=r3_features,
            h3_dense=h3_dense,
            c3=c3,
        )

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"MITeacher(h3_demands={self.n_h3_demands}, "
            f"r3_dim={self._r3_extractor.total_dim}, "
            f"c3_dim={self._brain.total_dim})"
        )
