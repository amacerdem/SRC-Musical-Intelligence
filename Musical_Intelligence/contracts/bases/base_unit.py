"""BaseCognitiveUnit -- Abstract Base Class for cognitive unit groupings.

A cognitive unit groups related models that share a neural circuit and
cognitive function. The nine units from the C3 meta-analysis are:

Core-4 VALIDATED (k >= 10 studies):

    SPU  Spectral Processing Unit    perceptual     d=0.84
    STU  Sensorimotor Timing Unit    sensorimotor   d=0.67
    IMU  Integrative Memory Unit     mnemonic       d=0.53
    ARU  Affective Resonance Unit    mesolimbic     d=0.83

Experimental-5 (k < 10):

    ASU  Auditory Salience Unit      salience
    NDU  Novelty Detection Unit      --
    MPU  Motor Planning Unit         --
    PCU  Imagery / Emotion Unit      imagery
    RPU  Reward / Salience Unit      --

A unit contains one or more ``BaseModel`` subclasses. The unit's
``compute()`` method runs its models in declared order and concatenates
their outputs into a single tensor.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple

from Musical_Intelligence.contracts.bases.base_model import BaseModel

if TYPE_CHECKING:
    from torch import Tensor


class BaseCognitiveUnit(ABC):
    """Abstract base class for cognitive unit groupings.

    Groups related ``BaseModel`` instances that share a neural circuit and
    cognitive function. The unit's ``compute()`` runs models in declared
    order and concatenates outputs into a single tensor.

    Class Constants (must override in every subclass):
        UNIT_NAME:     Short unit identifier (e.g. ``"ARU"``, ``"SPU"``).
        FULL_NAME:     Full descriptive name (e.g. ``"Affective Resonance
                       Unit"``).
        CIRCUIT:       Primary neural circuit: ``"mesolimbic"``,
                       ``"perceptual"``, ``"sensorimotor"``, ``"mnemonic"``,
                       ``"salience"``, ``"imagery"``.
        POOLED_EFFECT: Pooled effect size (Cohen's d) from C3 meta-analysis.
                       ``0.0`` for experimental units without meta-analytic
                       estimates.
    """

    # ------------------------------------------------------------------
    # Class constants -- override in every subclass
    # ------------------------------------------------------------------

    UNIT_NAME: str = ""
    FULL_NAME: str = ""
    CIRCUIT: str = ""
    POOLED_EFFECT: float = 0.0

    # ------------------------------------------------------------------
    # Abstract members
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def models(self) -> List[BaseModel]:
        """Ordered list of models in this unit.

        Models are executed in this order. The output of each model is
        concatenated along the last dimension to form the unit output.

        Returns:
            List of ``BaseModel`` instances in execution order.
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
            h3_features: Temporal features covering the union of all model
                demands. Dict mapping H3 4-tuples to ``(B, T)`` tensors.
            r3_features: ``(B, T, 49)`` R3 spectral feature tensor.
            cross_unit_inputs: Named tensors from other units' models,
                keyed by ``pathway_id``. ``None`` if no cross-unit deps.

        Returns:
            ``(B, T, total_dim)`` concatenated output of all models.
        """

    # ------------------------------------------------------------------
    # Computed properties
    # ------------------------------------------------------------------

    @property
    def active_models(self) -> List[BaseModel]:
        """Models currently active (default: all).

        Subclasses can override for conditional activation (e.g. disabling
        gamma-tier during validation).

        Returns:
            List of currently active ``BaseModel`` instances.
        """
        return self.models

    @property
    def total_dim(self) -> int:
        """Sum of all active model ``OUTPUT_DIM`` values."""
        return sum(m.OUTPUT_DIM for m in self.active_models)

    @property
    def model_names(self) -> Tuple[str, ...]:
        """Names of all models in execution order.

        Returns:
            Tuple of model ``NAME`` strings.
        """
        return tuple(m.NAME for m in self.models)

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """Union of all H3 demands across all active models.

        Returns:
            Set of ``(r3_idx, horizon, morph, law)`` 4-tuples.
        """
        demand: Set[Tuple[int, int, int, int]] = set()
        for model in self.active_models:
            demand |= model.h3_demand_tuples()
        return demand

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        """Flat tuple of all dimension names across all active models.

        Returns:
            Concatenated ``dimension_names`` from all active models.
        """
        names: List[str] = []
        for model in self.active_models:
            names.extend(model.dimension_names)
        return tuple(names)

    @property
    def is_validated(self) -> bool:
        """``True`` if ``POOLED_EFFECT > 0.0`` (has meta-analytic validation)."""
        return self.POOLED_EFFECT > 0.0

    @property
    def model_ranges(self) -> Dict[str, Tuple[int, int]]:
        """Map from model name to ``(start, end)`` index range in the
        concatenated unit output.

        Returns:
            Dict mapping model ``NAME`` to ``(start, end)`` half-open
            interval.
        """
        ranges: Dict[str, Tuple[int, int]] = {}
        offset = 0
        for model in self.active_models:
            ranges[model.NAME] = (offset, offset + model.OUTPUT_DIM)
            offset += model.OUTPUT_DIM
        return ranges

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate(self) -> list[str]:
        """Check internal consistency.

        Returns:
            List of error messages (empty if valid).

        Checks:
            1. ``UNIT_NAME`` must be non-empty.
            2. ``FULL_NAME`` must be non-empty.
            3. ``CIRCUIT`` must be non-empty.
            4. Every model must declare ``UNIT == self.UNIT_NAME``
               (ownership check).
            5. No duplicate model names within the unit.
            6. Delegates to each model's ``validate_constants()`` for
               per-model consistency.
        """
        errors: list[str] = []

        # 1. UNIT_NAME non-empty
        if not self.UNIT_NAME:
            errors.append("UNIT_NAME must be non-empty")

        # 2. FULL_NAME non-empty
        if not self.FULL_NAME:
            errors.append("FULL_NAME must be non-empty")

        # 3. CIRCUIT non-empty
        if not self.CIRCUIT:
            errors.append("CIRCUIT must be non-empty")

        # 4. Every model must declare UNIT == self.UNIT_NAME
        for model in self.models:
            if model.UNIT != self.UNIT_NAME:
                errors.append(
                    f"Model {model.NAME!r} declares UNIT={model.UNIT!r} "
                    f"but belongs to unit {self.UNIT_NAME!r}"
                )

        # 5. No duplicate model names
        seen_names: set[str] = set()
        for model in self.models:
            if model.NAME in seen_names:
                errors.append(
                    f"Duplicate model name {model.NAME!r} in unit "
                    f"{self.UNIT_NAME!r}"
                )
            seen_names.add(model.NAME)

        # 6. Delegate to each model's validate_constants()
        for model in self.models:
            model_errors = model.validate_constants()
            for err in model_errors:
                errors.append(f"Model {model.NAME!r}: {err}")

        return errors

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"unit={self.UNIT_NAME!r}, "
            f"circuit={self.CIRCUIT!r}, "
            f"models={self.model_names}, "
            f"dim={self.total_dim})"
        )
