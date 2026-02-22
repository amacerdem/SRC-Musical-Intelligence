"""Abstract base classes for C3 beliefs (Core, Appraisal, Anticipation)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Tuple

from torch import Tensor


class _BeliefBase(ABC):
    """Shared base for all belief types."""

    NAME: str
    FULL_NAME: str
    FUNCTION: str
    MECHANISM: str
    SOURCE_DIMS: Tuple[Tuple[str, float], ...]

    @abstractmethod
    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Observe belief value from mechanism output.

        Args:
            mechanism_output: ``(B, T, D)`` mechanism output tensor.

        Returns:
            ``(B, T)`` observed belief value.
        """


class CoreBelief(_BeliefBase):
    """Full Bayesian belief with predict/observe/update cycle.

    Subclass must set TAU, BASELINE and implement observe() and predict().
    """

    TAU: float
    BASELINE: float = 0.5

    @abstractmethod
    def predict(
        self,
        prev: Tensor,
        context: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Predict next belief value.

        Args:
            prev: ``(B, T)`` previous posterior.
            context: Related belief values.
            h3_features: H3 temporal features.

        Returns:
            ``(B, T)`` predicted value.
        """


class AppraisalBelief(_BeliefBase):
    """Observe-only belief — no predict/update cycle."""


class AnticipationBelief(_BeliefBase):
    """Forward prediction belief — observe-only."""
