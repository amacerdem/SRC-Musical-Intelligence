"""BaseMechanism -- Abstract Base Class for model-internal sub-computations.

A mechanism is a sub-computation within a ``BaseModel``. It reads H3 temporal
features and R3 spectral features and produces a fixed-dimensional output
tensor that the parent model combines with other mechanism outputs to form
its final output.

Mechanisms are the atomic computational units of the MI brain. By convention,
each mechanism produces a 30-D output (configurable via ``OUTPUT_DIM``). The
30-D convention comes from the C3 meta-analysis framework where each mechanism
produces a standardised feature block.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, Set, Tuple

if TYPE_CHECKING:
    from torch import Tensor


class BaseMechanism(ABC):
    """Abstract base class for model-internal sub-computations.

    Each mechanism reads H3 temporal features and R3 spectral features and
    produces a fixed-dimensional output tensor. The parent model combines
    mechanism outputs to form its final output.

    Class Constants (must override in every subclass):
        NAME:       Short mechanism identifier (e.g. ``"AED"``, ``"CPD"``).
        FULL_NAME:  Full descriptive name (e.g. ``"Affective Evaluation of
                    Dynamics"``).
        OUTPUT_DIM: Output dimensionality. Default 30D per C3 convention;
                    override if different.
        HORIZONS:   Horizon indices this mechanism operates over. E.g.
                    ``(9, 16, 18)`` = H9 (350ms), H16 (1s), H18 (2s).
    """

    # ------------------------------------------------------------------
    # Class constants -- override in every subclass
    # ------------------------------------------------------------------

    NAME: str = ""
    FULL_NAME: str = ""
    OUTPUT_DIM: int = 30
    HORIZONS: Tuple[int, ...] = ()

    # ------------------------------------------------------------------
    # Abstract members
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """The set of H3 4-tuples ``(r3_idx, horizon, morph, law)`` this
        mechanism needs.

        The union of all mechanism demands within a model defines the model's
        total H3 demand. Each tuple maps to a single ``(B, T)`` scalar time
        series in the H3Output.

        Returns:
            Set of ``(r3_idx, horizon, morph, law)`` 4-tuples.
        """

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Compute the mechanism output.

        Args:
            h3_features: Temporal features. Dict mapping H3 4-tuples to
                ``(B, T)`` scalar time series. Only tuples declared in
                ``h3_demand`` are guaranteed present.
            r3_features: ``(B, T, 49)`` R3 spectral feature tensor.

        Returns:
            ``(B, T, OUTPUT_DIM)`` mechanism output tensor.
        """

    # ------------------------------------------------------------------
    # Computed helpers
    # ------------------------------------------------------------------

    @property
    def demand_count(self) -> int:
        """Number of unique H3 demands declared."""
        return len(self.h3_demand)

    @property
    def horizons_used(self) -> Set[int]:
        """Horizon indices actually referenced in ``h3_demand``.

        Should match ``HORIZONS`` for a correctly specified mechanism.
        """
        return {t[1] for t in self.h3_demand}

    @property
    def r3_indices_used(self) -> Set[int]:
        """R3 feature indices referenced in ``h3_demand``."""
        return {t[0] for t in self.h3_demand}

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> list[str]:
        """Check internal consistency.

        Returns:
            List of error messages (empty if valid).

        Checks:
            1. ``NAME`` must be non-empty.
            2. ``FULL_NAME`` must be non-empty.
            3. ``OUTPUT_DIM`` must be > 0.
            4. ``HORIZONS`` (if declared) must match the actual horizons
               extracted from ``h3_demand``; a mismatch is flagged as an
               inconsistency.
        """
        errors: list[str] = []

        if not self.NAME:
            errors.append("NAME must be non-empty")
        if not self.FULL_NAME:
            errors.append("FULL_NAME must be non-empty")
        if self.OUTPUT_DIM <= 0:
            errors.append(
                f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}"
            )

        # HORIZONS consistency check: only if HORIZONS is declared
        if self.HORIZONS:
            try:
                actual_horizons = self.horizons_used
                declared_horizons = set(self.HORIZONS)
                if actual_horizons != declared_horizons:
                    errors.append(
                        f"HORIZONS {sorted(declared_horizons)} does not match "
                        f"horizons in h3_demand {sorted(actual_horizons)}"
                    )
            except NotImplementedError:
                pass  # h3_demand not yet implemented in subclass

        return errors

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.NAME!r}, "
            f"dim={self.OUTPUT_DIM}, "
            f"horizons={self.HORIZONS})"
        )
