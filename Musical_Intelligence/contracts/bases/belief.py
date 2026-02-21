"""Belief -- Base class hierarchy for all 131 C³ cognitive beliefs.

Three categories mirror distinct roles in the Bayesian prediction cycle:

    CoreBelief       — full predict → observe → PE → update cycle
    AppraisalBelief  — observe only, no prediction, no PE
    AnticipationBelief — forward prediction, no PE from this belief

Each belief is a *derived view* of mechanism output dimensions. Beliefs
live in the BeliefStore and flow into salience, reward, and precision
computations. They do NOT produce new tensor dimensions.

See BELIEF-CYCLE.md for the full specification.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Tuple

if TYPE_CHECKING:
    from torch import Tensor


class Belief(ABC):
    """Abstract base class for all 131 C³ cognitive beliefs.

    Class Constants (must override in every subclass):
        NAME:        Snake-case identifier (e.g. ``"harmonic_stability"``).
        FULL_NAME:   Human-readable name.
        CATEGORY:    ``"core"`` | ``"appraisal"`` | ``"anticipation"``.
        FUNCTION:    Primary cognitive function (e.g. ``"F1"``).
        MECHANISM:   Owning mechanism NAME (e.g. ``"BCH"``).
        SOURCE_DIMS: Tuple of ``(dim_name, weight)`` pairs from mechanism.
    """

    NAME: str = ""
    FULL_NAME: str = ""
    CATEGORY: str = ""
    FUNCTION: str = ""
    MECHANISM: str = ""
    SOURCE_DIMS: Tuple[Tuple[str, float], ...] = ()

    @abstractmethod
    def observe(self, mechanism_output: Tensor) -> Tensor:
        """Compute observed belief value from mechanism output.

        Args:
            mechanism_output: ``(B, T, mechanism_dim)`` full output tensor.

        Returns:
            ``(B, T)`` scalar belief value per frame.
        """

    def validate(self) -> List[str]:
        """Check internal consistency of class constants.

        Returns:
            List of error messages (empty if valid).
        """
        errors: List[str] = []
        if not self.NAME:
            errors.append("NAME must be non-empty")
        if not self.FULL_NAME:
            errors.append("FULL_NAME must be non-empty")
        if self.CATEGORY not in ("core", "appraisal", "anticipation"):
            errors.append(
                f"CATEGORY must be core/appraisal/anticipation, "
                f"got {self.CATEGORY!r}"
            )
        if not self.FUNCTION:
            errors.append("FUNCTION must be non-empty")
        if not self.MECHANISM:
            errors.append("MECHANISM must be non-empty")
        if not self.SOURCE_DIMS:
            errors.append("SOURCE_DIMS must be non-empty")
        # Weights should sum to ~1.0 (within tolerance)
        if self.SOURCE_DIMS:
            total = sum(w for _, w in self.SOURCE_DIMS)
            if abs(total - 1.0) > 0.01:
                errors.append(
                    f"SOURCE_DIMS weights sum to {total:.4f}, expected ~1.0"
                )
        return errors

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.NAME!r}, category={self.CATEGORY!r}, "
            f"function={self.FUNCTION!r}, mechanism={self.MECHANISM!r})"
        )


class CoreBelief(Belief):
    """Full Bayesian prediction error cycle: predict -> observe -> update.

    Core beliefs have inertia (TAU), generate prediction errors, and
    participate in the reward formula.
    """

    CATEGORY = "core"
    TAU: float = 0.0
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
            prev: ``(B, T)`` previous posterior value.
            context: Related belief values for contextual prediction.
            h3_features: H3 temporal features for trend/periodicity.

        Returns:
            ``(B, T)`` predicted belief value.
        """

    def update(
        self,
        predicted: Tensor,
        observed: Tensor,
        pi_obs: Tensor,
        pi_pred: Tensor,
    ) -> Tuple[Tensor, Tensor]:
        """Bayesian update: compute posterior and prediction error.

        Args:
            predicted: ``(B, T)`` predicted value.
            observed: ``(B, T)`` observed value.
            pi_obs: ``(B, T)`` observation precision.
            pi_pred: ``(B, T)`` prediction precision.

        Returns:
            Tuple of ``(posterior, prediction_error)``, each ``(B, T)``.
        """
        import torch

        pe = observed - predicted
        gain = pi_obs / (pi_obs + pi_pred + 1e-8)
        posterior = (1.0 - gain) * predicted + gain * observed
        return posterior, pe

    def validate(self) -> List[str]:
        errors = super().validate()
        if self.TAU <= 0.0 or self.TAU >= 1.0:
            errors.append(
                f"TAU must be in (0, 1), got {self.TAU}"
            )
        return errors


class AppraisalBelief(Belief):
    """Observe-only belief. No prediction, no PE generation.

    Appraisal beliefs are computed directly from mechanism outputs
    and tracked in the BeliefStore for downstream consumption.
    """

    CATEGORY = "appraisal"


class AnticipationBelief(Belief):
    """Forward prediction belief. No PE generated from this belief.

    Anticipation beliefs represent forward-looking signals from
    F-layer mechanism outputs. They feed into Core beliefs'
    predict() methods as context.
    """

    CATEGORY = "anticipation"
