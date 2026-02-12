"""
BaseSemanticGroup -- Abstract base class for L3 semantic interpretation groups.

L3 (Language Layer) interprets the Brain output at 8 epistemological levels,
each answering a different question about the same neural signal:

    Level 1  (alpha)    -- Computation:   HOW was the value computed?
    Level 2  (beta)     -- Neuroscience:  WHERE in the brain?
    Level 3  (gamma)    -- Psychology:    WHAT does it mean subjectively?
    Level 4  (delta)    -- Validation:    HOW to test it empirically?
    Level 5  (epsilon)  -- Learning:      HOW does the listener learn over time?
    Level 6  (zeta)     -- Polarity:      Bipolar semantic axes (e.g. tense/relaxed).
    Level 7  (eta)      -- Vocabulary:    64-gradation human-readable terms.
    Level 8  (theta)    -- Narrative:     Sentence-level linguistic structure.

Each level is implemented as a BaseSemanticGroup subclass.  The group reads
the Brain output (26D in mi v2, variable in mi_beta) and optionally reads
outputs from earlier semantic groups (e.g. theta may reference zeta's polarity
axes).

The compute() method returns a SemanticGroupOutput dataclass containing the
group name, level, tensor, and dimension names.

This ABC is structurally compatible with the mi (v2) BaseSemanticGroup but
adds validation helpers for the mi_beta architecture.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, List, Tuple

from torch import Tensor


# ═══════════════════════════════════════════════════════════════════════
# OUTPUT TYPE
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class SemanticGroupOutput:
    """Output container for a single L3 semantic group.

    Attributes:
        group_name:      Canonical name (e.g. "alpha", "beta", "gamma").
        level:           Epistemological level (1-8).
        tensor:          (B, T, dim) semantic interpretation tensor.
        dimension_names: Ordered names for each output dimension.
    """

    group_name: str
    level: int
    tensor: Tensor
    dimension_names: Tuple[str, ...]

    def __post_init__(self) -> None:
        dim = self.tensor.shape[-1]
        if len(self.dimension_names) != dim:
            raise ValueError(
                f"SemanticGroupOutput {self.group_name!r}: "
                f"dimension_names has {len(self.dimension_names)} entries "
                f"but tensor has {dim} dimensions"
            )


# ═══════════════════════════════════════════════════════════════════════
# ABC
# ═══════════════════════════════════════════════════════════════════════

class BaseSemanticGroup(ABC):
    """Abstract base class for L3 semantic interpretation groups.

    Each subclass interprets the Brain output at a specific epistemological
    level and produces a fixed-dimensional semantic tensor.
    """

    # ═══════════════════════════════════════════════════════════════════
    # CLASS CONSTANTS — override in every subclass
    # ═══════════════════════════════════════════════════════════════════

    LEVEL: int = 0
    """Epistemological level (1-8).  See module docstring for definitions."""

    GROUP_NAME: str = ""
    """Canonical group name: "alpha", "beta", "gamma", "delta",
    "epsilon", "zeta", "eta", "theta"."""

    DISPLAY_NAME: str = ""
    """Greek letter display name: "a", "b", "g", "d", "e", "z", "h", "th"."""

    OUTPUT_DIM: int = 0
    """Number of semantic dimensions this group produces."""

    # ═══════════════════════════════════════════════════════════════════
    # ABSTRACT MEMBERS
    # ═══════════════════════════════════════════════════════════════════

    @abstractmethod
    def compute(
        self,
        brain_output: Any,
        **kwargs: Any,
    ) -> SemanticGroupOutput:
        """Compute semantic interpretation from the Brain output.

        Args:
            brain_output: The Brain's output object.  In mi v2 this is
                BrainOutput (26D).  In mi_beta this is the concatenated
                unit outputs.  The type is Any to avoid circular imports.
            **kwargs: Optional outputs from earlier semantic groups.
                Keys are group names (e.g. "zeta_output", "epsilon_output").
                This enables cross-level dependencies (e.g. theta reading
                zeta polarity axes).

        Returns:
            SemanticGroupOutput with (B, T, OUTPUT_DIM) tensor.
        """

    @property
    @abstractmethod
    def dimension_names(self) -> List[str]:
        """Ordered names of each output dimension.

        len(dimension_names) MUST equal OUTPUT_DIM.
        Names follow snake_case convention.
        """

    # ═══════════════════════════════════════════════════════════════════
    # COMPUTED HELPERS
    # ═══════════════════════════════════════════════════════════════════

    def validate(self) -> list[str]:
        """Check internal consistency.

        Returns:
            List of error messages (empty if valid).
        """
        errors: list[str] = []

        if not (1 <= self.LEVEL <= 8):
            errors.append(f"LEVEL must be in [1, 8], got {self.LEVEL}")
        if not self.GROUP_NAME:
            errors.append("GROUP_NAME must be non-empty")
        if not self.DISPLAY_NAME:
            errors.append("DISPLAY_NAME must be non-empty")
        if self.OUTPUT_DIM <= 0:
            errors.append(f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}")

        try:
            names = self.dimension_names
            if len(names) != self.OUTPUT_DIM:
                errors.append(
                    f"dimension_names has {len(names)} entries, "
                    f"expected {self.OUTPUT_DIM}"
                )
        except NotImplementedError:
            pass

        return errors

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"level={self.LEVEL}, "
            f"group={self.DISPLAY_NAME}, "
            f"dim={self.OUTPUT_DIM})"
        )
