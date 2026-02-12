"""
BaseSemanticGroup — Abstract base for L³ interpretation groups.

A SemanticGroup interprets MusicalBrain output at a specific epistemological level:
  Level 1 (α): Computation — HOW the value was computed
  Level 2 (β): Neuroscience — WHERE in the brain
  Level 3 (γ): Psychology — WHAT it means subjectively
  Level 4 (δ): Validation — HOW to test it empirically
  Level 5 (ε): Learning — HOW the listener learns over time
  Level 6 (ζ): Polarity — bipolar semantic axes
  Level 7 (η): Vocabulary — 64-gradation human-readable terms
  Level 8 (θ): Narrative — sentence-level linguistic structure
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from torch import Tensor

from ..types import SemanticGroupOutput


class BaseSemanticGroup(ABC):
    """Abstract base class for L³ semantic interpretation groups."""

    # ─── Class attributes (override in subclass) ────────────────────
    LEVEL: int           # 1-8
    GROUP_NAME: str      # "alpha", "beta", "gamma", etc.
    DISPLAY_NAME: str    # "α", "β", "γ", etc.
    OUTPUT_DIM: int      # e.g., 6

    @abstractmethod
    def compute(
        self,
        brain_output: object,
        **kwargs,
    ) -> SemanticGroupOutput:
        """Compute semantic interpretation.

        Args:
            brain_output: BrainOutput (26D) from MusicalBrain
            **kwargs: optional outputs from earlier groups (e.g. epsilon_output)

        Returns:
            SemanticGroupOutput with (B, T, OUTPUT_DIM) tensor
        """

    @property
    @abstractmethod
    def dimension_names(self) -> List[str]:
        """Names of each output dimension."""

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"level={self.LEVEL}, "
            f"group={self.DISPLAY_NAME}, "
            f"dim={self.OUTPUT_DIM})"
        )
