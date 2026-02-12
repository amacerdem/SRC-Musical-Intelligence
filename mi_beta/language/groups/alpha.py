"""
alpha (Alpha) -- Computation Semantics (variable D)

Level 1: HOW the value was computed.
Traces each Brain dimension back to its computational source unit.

In mi_beta, Brain output is variable-dimensional with N active units.
Alpha produces 1 attribution dimension per active unit plus 2 global
dimensions (computation_certainty and bipolar_activation).

Dimensions:
    {unit}_attribution  -- mean activation of that unit's output       [per unit]
    computation_certainty -- output stability (inverse variance)       [1D]
    bipolar_activation    -- net direction of signed dimensions        [1D]

Total: N_active_units + 2

Scientific basis:
    Pathway attribution enables computational transparency (white-box).
    Certainty derives from inverse output variance (Bayesian precision).
"""

from __future__ import annotations

from typing import Any, List

import torch
from torch import Tensor

from ...contracts.base_semantic_group import BaseSemanticGroup, SemanticGroupOutput
from ...core.types import BrainOutput


class AlphaGroup(BaseSemanticGroup):
    """Computation semantics: per-unit attribution + certainty + bipolar."""

    LEVEL = 1
    GROUP_NAME = "alpha"
    DISPLAY_NAME = "alpha"

    def __init__(self, brain_output_ref: BrainOutput | None = None) -> None:
        self._unit_names: list[str] = []
        self._output_dim: int = 2  # minimum: certainty + bipolar
        if brain_output_ref is not None:
            self._configure(brain_output_ref)

    def _configure(self, brain_output: BrainOutput) -> None:
        """Configure dimension layout from a BrainOutput sample."""
        self._unit_names = sorted(brain_output.unit_outputs.keys())
        self._output_dim = len(self._unit_names) + 2

    @property
    def OUTPUT_DIM(self) -> int:  # type: ignore[override]
        return self._output_dim

    @property
    def dimension_names(self) -> List[str]:
        names = [f"{u.lower()}_attribution" for u in self._unit_names]
        names.extend(["computation_certainty", "bipolar_activation"])
        return names

    def compute(self, brain_output: Any, **kwargs: Any) -> SemanticGroupOutput:
        """Compute alpha group from BrainOutput (variable D).

        Per-unit attribution: mean activation of each unit's tensor slice.
        """
        # Auto-configure on first call if not already configured
        if not self._unit_names:
            self._configure(brain_output)

        parts: list[Tensor] = []

        # Per-unit attribution: mean activation
        for unit_name in self._unit_names:
            unit_tensor = brain_output.get_unit(unit_name)  # (B, T, unit_dim)
            attr = unit_tensor.mean(dim=-1, keepdim=True)   # (B, T, 1)
            parts.append(attr)

        # Computation certainty: inverse of full output variance
        full = brain_output.tensor  # (B, T, brain_dim)
        certainty = 1.0 / (1.0 + full.var(dim=-1, keepdim=True))  # (B, T, 1)
        parts.append(certainty)

        # Bipolar activation: mean signed value across all brain dims
        # Values near 0.5 are "neutral" in [0,1] space; shift to center
        bipolar = (full.mean(dim=-1, keepdim=True) - 0.5) * 2.0  # (B, T, 1) in [-1,1]
        bipolar = bipolar * 0.5 + 0.5  # remap to [0,1]
        parts.append(bipolar)

        tensor = torch.cat(parts, dim=-1)  # (B, T, n_units+2)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor.clamp(0, 1),
            dimension_names=tuple(self.dimension_names),
        )
