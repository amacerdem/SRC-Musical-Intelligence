"""
BaseMechanism -- Abstract base class for model-internal mechanisms.

A mechanism is a sub-computation within a BaseModel.  It reads H3 temporal
features and R3 spectral features and produces a fixed-dimensional output
tensor that the parent model combines with other mechanism outputs to form
its final output.

Mechanisms are the atomic computational units of the mi_beta brain.  Each
mechanism has:
    - A fixed 30-D output (by convention, configurable via OUTPUT_DIM).
    - A declared set of H3 demands (which temporal features it needs).
    - A declared set of horizons it operates over.
    - A deterministic compute() function.

The 30-D convention comes from the C3 meta-analysis framework where each
mechanism produces a standardised feature block.  Models that need a
different output size can override OUTPUT_DIM.

Example subclass:

    class AED(BaseMechanism):
        NAME = "AED"
        FULL_NAME = "Affective Evaluation of Dynamics"
        OUTPUT_DIM = 30
        HORIZONS = (9, 16, 18)  # 350ms, 1s, 2s

        @property
        def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
            return {(10, 9, 4, 2), (8, 9, 8, 2), ...}

        def compute(self, h3_features, r3_features) -> Tensor:
            ...
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, Set, Tuple

from torch import Tensor


class BaseMechanism(ABC):
    """Abstract base class for model-internal mechanisms.

    A mechanism is a deterministic sub-computation that transforms
    H3/R3 features into a fixed-dimensional output tensor.
    """

    # ═══════════════════════════════════════════════════════════════════
    # CLASS CONSTANTS — override in every subclass
    # ═══════════════════════════════════════════════════════════════════

    NAME: str = ""
    """Short mechanism identifier (e.g. "AED", "CPD", "C0P")."""

    FULL_NAME: str = ""
    """Full descriptive name (e.g. "Affective Evaluation of Dynamics")."""

    OUTPUT_DIM: int = 30
    """Output dimensionality.  Default 30D per C3 convention.
    Override if the mechanism needs a different output size."""

    HORIZONS: Tuple[int, ...] = ()
    """Tuple of horizon indices this mechanism operates over.
    E.g. (9, 16, 18) means it reads H3 features at H9 (350ms),
    H16 (1s), and H18 (2s).  Used for documentation and validation."""

    # ═══════════════════════════════════════════════════════════════════
    # ABSTRACT MEMBERS
    # ═══════════════════════════════════════════════════════════════════

    @property
    @abstractmethod
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """The set of H3 4-tuples (r3_idx, horizon, morph, law) this
        mechanism needs.

        The union of all mechanism demands within a model defines the
        model's total H3 demand.  Each tuple maps to a single (B, T)
        scalar time series in the H3Output.

        Returns:
            Set of (r3_idx, horizon, morph, law) 4-tuples.
        """

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Compute the mechanism output.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features.  Only the tuples declared in h3_demand are
                guaranteed to be present.
            r3_features: (B, T, 49) R3 spectral features.

        Returns:
            (B, T, OUTPUT_DIM) mechanism output tensor.
        """

    # ═══════════════════════════════════════════════════════════════════
    # COMPUTED HELPERS
    # ═══════════════════════════════════════════════════════════════════

    @property
    def demand_count(self) -> int:
        """Number of unique H3 demands declared by this mechanism."""
        return len(self.h3_demand)

    @property
    def horizons_used(self) -> Set[int]:
        """Set of horizon indices actually referenced in h3_demand.

        This should match HORIZONS; a mismatch is a code smell.
        """
        return {h for _, h, _, _ in self.h3_demand}

    @property
    def r3_indices_used(self) -> Set[int]:
        """Set of R3 feature indices referenced in h3_demand."""
        return {r for r, _, _, _ in self.h3_demand}

    def validate(self) -> list[str]:
        """Check internal consistency.

        Returns:
            List of error messages (empty if valid).
        """
        errors: list[str] = []

        if not self.NAME:
            errors.append("NAME must be non-empty")
        if not self.FULL_NAME:
            errors.append("FULL_NAME must be non-empty")
        if self.OUTPUT_DIM <= 0:
            errors.append(f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}")

        # HORIZONS should match what h3_demand actually uses
        declared = set(self.HORIZONS)
        actual = self.horizons_used
        if declared and declared != actual:
            errors.append(
                f"HORIZONS {sorted(declared)} != "
                f"horizons in h3_demand {sorted(actual)}"
            )

        return errors

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.NAME!r}, "
            f"dim={self.OUTPUT_DIM}, "
            f"demands={self.demand_count}, "
            f"horizons={self.HORIZONS})"
        )
