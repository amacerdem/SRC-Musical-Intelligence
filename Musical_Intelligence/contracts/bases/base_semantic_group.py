"""BaseSemanticGroup -- Abstract Base Class for L3 semantic groups.

The foundational contract for all 8 L3 semantic groups. Each group transforms
brain output into a semantic interpretation at a specific epistemological
level.

The 8 groups (alpha through theta) form a layered interpretation stack:

    Level 1  alpha    Variable DIM   Phase 1    Stateless
    Level 2  beta     Variable DIM   Phase 1    Stateless
    Level 3  gamma    13D            Phase 1    Stateless
    Level 4  delta    12D            Phase 1    Stateless
    Level 5  epsilon  19D            Phase 1b   Stateful
    Level 6  zeta     12D            Phase 2a   Stateless
    Level 7  eta      12D            Phase 2b   Stateless
    Level 8  theta    16D            Phase 2c   Stateless

Range convention:

    alpha, beta, gamma, delta, epsilon, eta, theta  [0, 1]
    zeta                                             [-1, +1]
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List, Tuple

from Musical_Intelligence.contracts.dataclasses import SemanticGroupOutput

if TYPE_CHECKING:
    pass


class BaseSemanticGroup(ABC):
    """Abstract base class for L3 semantic groups (alpha through theta).

    Each group computes a semantic interpretation from the Brain output at
    a specific epistemological level. Groups may optionally receive outputs
    from earlier groups via ``**kwargs``.

    Class Constants (must override in every subclass):
        LEVEL:        Epistemological level (1-8).
        GROUP_NAME:   Canonical name: ``"alpha"`` .. ``"theta"``.
        DISPLAY_NAME: Greek letter display name.
        OUTPUT_DIM:   Number of output dimensions. Must be > 0.
    """

    # ------------------------------------------------------------------
    # Class constants -- override in every subclass
    # ------------------------------------------------------------------

    LEVEL: int = 0
    GROUP_NAME: str = ""
    DISPLAY_NAME: str = ""
    OUTPUT_DIM: int = 0

    # ------------------------------------------------------------------
    # Abstract members
    # ------------------------------------------------------------------

    @abstractmethod
    def compute(self, brain_output: Any, **kwargs: Any) -> SemanticGroupOutput:
        """Compute semantic interpretation from the Brain output.

        Args:
            brain_output: ``BrainOutput`` tensor (26D in mi v2, variable in
                mi_beta). The concatenated output from all cognitive units.
            **kwargs: Optional outputs from earlier groups (e.g.
                ``epsilon_output``, ``zeta_output``). Used for dependency
                injection between groups.

        Returns:
            ``SemanticGroupOutput`` with tensor shape ``(B, T, OUTPUT_DIM)``.
        """

    @property
    @abstractmethod
    def dimension_names(self) -> Tuple[str, ...]:
        """Ordered names for each output dimension.

        ``len(dimension_names)`` MUST equal ``OUTPUT_DIM``.

        Returns:
            Tuple of dimension name strings.
        """

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> list[str]:
        """Check internal consistency.

        Returns:
            List of error messages (empty if valid).

        Checks:
            1. ``LEVEL`` in ``[1, 8]``.
            2. ``GROUP_NAME`` is non-empty.
            3. ``DISPLAY_NAME`` is non-empty.
            4. ``OUTPUT_DIM > 0``.
            5. ``len(dimension_names) == OUTPUT_DIM``.
        """
        errors: list[str] = []

        # 1. LEVEL in [1, 8]
        if not (1 <= self.LEVEL <= 8):
            errors.append(
                f"LEVEL must be in [1, 8], got {self.LEVEL}"
            )

        # 2. GROUP_NAME non-empty
        if not self.GROUP_NAME:
            errors.append("GROUP_NAME must be non-empty")

        # 3. DISPLAY_NAME non-empty
        if not self.DISPLAY_NAME:
            errors.append("DISPLAY_NAME must be non-empty")

        # 4. OUTPUT_DIM > 0
        if self.OUTPUT_DIM <= 0:
            errors.append(
                f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}"
            )

        # 5. dimension_names length matches OUTPUT_DIM
        try:
            names = self.dimension_names
            if len(names) != self.OUTPUT_DIM:
                errors.append(
                    f"len(dimension_names) is {len(names)}, "
                    f"expected OUTPUT_DIM={self.OUTPUT_DIM}"
                )
        except NotImplementedError:
            pass  # dimension_names not yet implemented in subclass

        return errors

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"level={self.LEVEL}, "
            f"group={self.GROUP_NAME!r}, "
            f"display={self.DISPLAY_NAME!r}, "
            f"dim={self.OUTPUT_DIM})"
        )
