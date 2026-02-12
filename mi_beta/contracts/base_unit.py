"""
BaseCognitiveUnit -- Abstract base class for cognitive units.

A cognitive unit groups related models that share a neural circuit and
cognitive function.  The nine units from the C3 meta-analysis are:

    Core-4 VALIDATED (k >= 10 studies):
        SPU  -- Spectral Processing Unit      (d=0.84, Heschl's + Planum Polare)
        STU  -- Sensorimotor Timing Unit       (d=0.67, SMA + Heschl's)
        IMU  -- Integrative Memory Unit        (d=0.53, Hippocampus + mPFC)
        ARU  -- Affective Resonance Unit       (d=0.83, NAcc + VTA + Amygdala)

    Experimental-5 (k < 10):
        ASU  -- Auditory Salience Unit
        NDU  -- Novelty Detection Unit
        MPU  -- Motor Planning Unit
        PCU  -- Imagery / Emotion Unit
        RPU  -- Reward / Salience Unit

A unit contains one or more BaseModel subclasses.  The unit's compute()
method runs its models in the declared order and concatenates their outputs
into a single tensor.

Example:

    class ARUnit(BaseCognitiveUnit):
        UNIT_NAME = "ARU"
        FULL_NAME = "Affective Resonance Unit"
        CIRCUIT = "mesolimbic"
        POOLED_EFFECT = 0.83

        @property
        def models(self) -> List[BaseModel]:
            return [self._srp, self._aac, self._vmm]
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Tuple

from torch import Tensor

from .base_model import BaseModel


class BaseCognitiveUnit(ABC):
    """Abstract base class for cognitive units (ARU, SPU, STU, etc.).

    A unit is a container for related models that share a neural circuit.
    It manages model execution order and output concatenation.
    """

    # ═══════════════════════════════════════════════════════════════════
    # CLASS CONSTANTS — override in every subclass
    # ═══════════════════════════════════════════════════════════════════

    UNIT_NAME: str = ""
    """Short unit identifier (e.g. "ARU", "SPU")."""

    FULL_NAME: str = ""
    """Full descriptive name (e.g. "Affective Resonance Unit")."""

    CIRCUIT: str = ""
    """Primary neural circuit (e.g. "mesolimbic", "perceptual",
    "sensorimotor", "mnemonic", "salience", "imagery")."""

    POOLED_EFFECT: float = 0.0
    """Pooled effect size (Cohen's d) from C3 meta-analysis.
    0.0 for experimental units without meta-analytic estimates."""

    # ═══════════════════════════════════════════════════════════════════
    # ABSTRACT MEMBERS
    # ═══════════════════════════════════════════════════════════════════

    @property
    @abstractmethod
    def models(self) -> List[BaseModel]:
        """Ordered list of models in this unit.

        Models are executed in this order.  The output of each model
        is concatenated along the last dimension to form the unit output.
        """

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Compute the unit's concatenated output.

        Args:
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} temporal
                features covering the union of all model demands.
            r3_features: (B, T, 49) R3 spectral features.
            cross_unit_inputs: Optional dict of named tensors from other
                units' models, keyed by pathway_id.

        Returns:
            (B, T, total_dim) concatenated output of all models.
        """

    # ═══════════════════════════════════════════════════════════════════
    # COMPUTED PROPERTIES
    # ═══════════════════════════════════════════════════════════════════

    @property
    def active_models(self) -> List[BaseModel]:
        """Models that are currently active (non-empty output).

        By default, all models are active.  Subclasses can override this
        to support conditional model activation (e.g. disabling gamma-tier
        models during validation runs).
        """
        return self.models

    @property
    def total_dim(self) -> int:
        """Total output dimensionality (sum of all active model OUTPUT_DIMs)."""
        return sum(m.OUTPUT_DIM for m in self.active_models)

    @property
    def model_names(self) -> Tuple[str, ...]:
        """Names of all models in execution order."""
        return tuple(m.NAME for m in self.models)

    @property
    def mechanism_names(self) -> Tuple[str, ...]:
        """Flat tuple of all mechanism names across all models."""
        names: list[str] = []
        for model in self.models:
            names.extend(model.MECHANISM_NAMES)
        return tuple(names)

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """Union of all H3 demands across all active models."""
        demand: set[Tuple[int, int, int, int]] = set()
        for model in self.active_models:
            demand |= model.h3_demand_tuples()
        return demand

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        """Flat tuple of all dimension names across all active models."""
        names: list[str] = []
        for model in self.active_models:
            names.extend(model.dimension_names)
        return tuple(names)

    @property
    def is_validated(self) -> bool:
        """True if this unit has meta-analytic validation (pooled d > 0)."""
        return self.POOLED_EFFECT > 0.0

    @property
    def model_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Map from model name to (start, end) index range in the
        concatenated unit output tensor."""
        ranges: dict[str, Tuple[int, int]] = {}
        offset = 0
        for model in self.active_models:
            ranges[model.NAME] = (offset, offset + model.OUTPUT_DIM)
            offset += model.OUTPUT_DIM
        return ranges

    def validate(self) -> list[str]:
        """Check internal consistency.

        Returns:
            List of error messages (empty if valid).
        """
        errors: list[str] = []

        if not self.UNIT_NAME:
            errors.append("UNIT_NAME must be non-empty")
        if not self.FULL_NAME:
            errors.append("FULL_NAME must be non-empty")
        if not self.CIRCUIT:
            errors.append("CIRCUIT must be non-empty")

        # Validate all models claim this unit
        for model in self.models:
            if model.UNIT != self.UNIT_NAME:
                errors.append(
                    f"Model {model.NAME!r} declares UNIT={model.UNIT!r} "
                    f"but belongs to unit {self.UNIT_NAME!r}"
                )

        # Validate no duplicate model names
        names = [m.NAME for m in self.models]
        if len(names) != len(set(names)):
            errors.append(f"Duplicate model names: {names}")

        # Validate each model's internal consistency
        for model in self.models:
            model_errors = model.validate_constants()
            for err in model_errors:
                errors.append(f"  {model.NAME}: {err}")

        return errors

    def __repr__(self) -> str:
        model_str = ", ".join(m.NAME for m in self.models)
        return (
            f"{self.__class__.__name__}("
            f"unit={self.UNIT_NAME!r}, "
            f"circuit={self.CIRCUIT!r}, "
            f"d={self.POOLED_EFFECT:.2f}, "
            f"models=[{model_str}], "
            f"dim={self.total_dim})"
        )
