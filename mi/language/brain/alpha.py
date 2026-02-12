"""
α (Alpha) — Computation Semantics (6D)

Level 1: HOW the value was computed.
Traces each Brain dimension back to its computational source pathway.

α0: shared_attribution — shared state pathway contribution
α1: reward_attribution — reward pathway contribution
α2: affect_attribution — affect pathway contribution
α3: autonomic_attribution — autonomic pathway contribution
α4: computation_certainty — output stability (inverse variance)
α5: bipolar_activation — net direction of signed dimensions

Scientific basis:
  Pathway attribution enables computational transparency (white-box).
  Certainty derives from inverse output variance (Bayesian precision).
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ...core.base import BaseSemanticGroup
from ...core.types import SemanticGroupOutput


class AlphaGroup(BaseSemanticGroup):
    LEVEL = 1
    GROUP_NAME = "alpha"
    DISPLAY_NAME = "α"
    OUTPUT_DIM = 6

    @property
    def dimension_names(self) -> List[str]:
        return [
            "shared_attribution",
            "reward_attribution",
            "affect_attribution",
            "autonomic_attribution",
            "computation_certainty",
            "bipolar_activation",
        ]

    def compute(self, brain_output: object, **kwargs) -> SemanticGroupOutput:
        """Compute α group from BrainOutput (26D).

        Pathway attribution: mean activation of each pathway slice.
        """
        # Pathway slices
        shared = brain_output.get_pathway("shared")       # (B, T, 4)
        reward = brain_output.get_pathway("reward")        # (B, T, 9)
        affect = brain_output.get_pathway("affect")        # (B, T, 6)
        autonomic = brain_output.get_pathway("autonomic")  # (B, T, 5)

        # Attribution: mean activation per pathway
        shared_attr = shared.mean(dim=-1, keepdim=True)       # (B, T, 1)
        reward_attr = reward.mean(dim=-1, keepdim=True)
        affect_attr = affect.mean(dim=-1, keepdim=True)
        autonomic_attr = autonomic.mean(dim=-1, keepdim=True)

        # Computation certainty: inverse of full output variance
        full = brain_output.tensor  # (B, T, 26)
        certainty = 1.0 / (1.0 + full.var(dim=-1, keepdim=True))

        # Bipolar activation: net direction of tanh dimensions
        # prediction_error (D1) and f03_valence (D13) are [-1,1]
        pe = brain_output.get_dim("prediction_error").unsqueeze(-1)
        val = brain_output.get_dim("f03_valence").unsqueeze(-1)
        bipolar = (pe + val) * 0.5

        tensor = torch.cat([
            shared_attr, reward_attr, affect_attr,
            autonomic_attr, certainty, bipolar,
        ], dim=-1)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor,
            dimension_names=tuple(self.dimension_names),
        )
