"""BaseModel -- THE Central Contract for All Cognitive Models.

``BaseModel`` is THE central contract for the MI architecture. A cognitive
model is a deterministic, zero-parameter function that transforms H3 temporal
features, R3 spectral features, and optional cross-unit inputs into a
fixed-dimensional output tensor.

Every output dimension must have a human-readable name, a scientific citation,
a defined value range, and assignment to one of the E/M/P/F output layers.

Models are grouped into cognitive units (ARU, SPU, STU, IMU, etc.). Each
model belongs to exactly one unit and one evidence tier (alpha/beta/gamma).
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, FrozenSet, List, Optional, Set, Tuple

from Musical_Intelligence.contracts.dataclasses import (
    BrainRegion,
    CrossUnitPathway,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
)

if TYPE_CHECKING:
    from torch import Tensor


_VALID_TIERS = frozenset({"alpha", "beta", "gamma"})


class BaseModel(ABC):
    """Abstract base class for all 96 cognitive models.

    A cognitive model transforms H3 temporal features, R3 spectral features,
    and optional cross-unit inputs into a fixed-dimensional output tensor
    structured according to E/M/P/F output layers.

    Class Constants (must override in every subclass):
        NAME:             Short model identifier (e.g. ``"SRP"``).
        FULL_NAME:        Full descriptive name (e.g. ``"Striatal Reward
                          Pathway"``).
        UNIT:             Parent cognitive unit (e.g. ``"ARU"``).
        TIER:             Evidence tier: ``"alpha"``, ``"beta"``, or
                          ``"gamma"``.
        OUTPUT_DIM:       Total output dimensionality; must equal the sum of
                          all LAYERS dims.
        CROSS_UNIT_READS: Declared cross-unit data dependencies. Empty if the
                          model only reads H3/R3.
        LAYERS:           Output layer structure; each ``LayerSpec`` defines a
                          semantic slice of the output tensor.
    """

    # ------------------------------------------------------------------
    # Class constants -- override in every subclass
    # ------------------------------------------------------------------

    NAME: str = ""
    FULL_NAME: str = ""
    UNIT: str = ""
    TIER: str = ""
    OUTPUT_DIM: int = 0
    CROSS_UNIT_READS: Tuple[CrossUnitPathway, ...] = ()
    LAYERS: Tuple[LayerSpec, ...] = ()

    # ------------------------------------------------------------------
    # Abstract properties
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """All H3 temporal demands needed by this model.

        Each ``H3DemandSpec`` maps to a single scalar time series. The set of
        ``as_tuple()`` values is passed to the DemandTree for efficient H3
        computation. May be empty for models that only read R3 features
        directly.

        Returns:
            Tuple of ``H3DemandSpec`` instances.
        """

    @property
    @abstractmethod
    def dimension_names(self) -> Tuple[str, ...]:
        """Ordered names for every output dimension.

        ``len(dimension_names)`` MUST equal ``OUTPUT_DIM``. Names must be
        unique within the model and follow ``snake_case`` convention.

        Returns:
            Tuple of dimension name strings.
        """

    @property
    @abstractmethod
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        """Brain regions associated with this model's computation.

        Used for MNI152 visualisation and anatomical grounding.

        Returns:
            Tuple of ``BrainRegion`` instances.
        """

    @property
    @abstractmethod
    def metadata(self) -> ModelMetadata:
        """Evidence provenance: citations, tier, confidence range,
        falsification criteria.

        Returns:
            ``ModelMetadata`` instance.
        """

    # ------------------------------------------------------------------
    # Abstract method
    # ------------------------------------------------------------------

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """The core computation.

        Transforms inputs into the model's output tensor.

        Args:
            h3_features: Per-demand H3 scalar time series, keyed by
                ``(r3_idx, horizon, morph, law)`` 4-tuples.
                Shape per value: ``(B, T)``.
            r3_features: ``(B, T, 49)`` R3 spectral feature tensor.
            cross_unit_inputs: Named tensors from other models, keyed by
                ``pathway_id``. ``None`` if no cross-unit dependencies.

        Returns:
            ``(B, T, OUTPUT_DIM)`` output tensor with dimensions ordered
            as declared in ``dimension_names`` and structured according to
            ``LAYERS``.
        """

    # ------------------------------------------------------------------
    # Computed helpers
    # ------------------------------------------------------------------

    def h3_demand_tuples(self) -> Set[Tuple[int, int, int, int]]:
        """Set of raw 4-tuples consumed by ``DemandTree.build()`` and
        ``H3Output``.

        Deduplicates via set semantics.

        Returns:
            Set of ``(r3_idx, horizon, morph, law)`` tuples.
        """
        return {spec.as_tuple() for spec in self.h3_demand}

    @property
    def layer_dim_names(self) -> Tuple[str, ...]:
        """Flat tuple of dimension names derived from ``LAYERS``.

        Must match ``dimension_names`` (cross-check validated by
        ``validate_constants()``).

        Returns:
            Concatenated dim_names from all layers in order.
        """
        names: List[str] = []
        for layer in self.LAYERS:
            names.extend(layer.dim_names)
        return tuple(names)

    @property
    def cross_unit_dependency_units(self) -> FrozenSet[str]:
        """Set of cognitive unit names this model depends on.

        Derived from ``CROSS_UNIT_READS``.

        Returns:
            Frozen set of source unit names.
        """
        return frozenset(p.source_unit for p in self.CROSS_UNIT_READS)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_constants(self) -> list[str]:
        """Check internal consistency of class constants.

        Returns:
            List of error messages (empty if valid).

        Checks:
            1. ``NAME`` must be non-empty.
            2. ``FULL_NAME`` must be non-empty.
            3. ``UNIT`` must be non-empty.
            4. ``TIER`` must be one of ``"alpha"``, ``"beta"``, ``"gamma"``.
            5. ``OUTPUT_DIM`` must be > 0.
            6. ``LAYERS`` must cover ``[0, OUTPUT_DIM)`` without gaps or
               overlaps -- each index in range must be covered exactly once.
            7. ``LAYERS`` ``dim_names`` concatenated must match
               ``dimension_names`` (if implemented).
        """
        errors: list[str] = []

        # 1. NAME non-empty
        if not self.NAME:
            errors.append("NAME must be non-empty")

        # 2. FULL_NAME non-empty
        if not self.FULL_NAME:
            errors.append("FULL_NAME must be non-empty")

        # 3. UNIT non-empty
        if not self.UNIT:
            errors.append("UNIT must be non-empty")

        # 4. TIER valid
        if self.TIER not in _VALID_TIERS:
            errors.append(
                f"TIER must be one of {sorted(_VALID_TIERS)}, "
                f"got {self.TIER!r}"
            )

        # 5. OUTPUT_DIM > 0
        if self.OUTPUT_DIM <= 0:
            errors.append(
                f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}"
            )

        # 6. LAYERS must cover [0, OUTPUT_DIM) without gaps or overlaps
        if self.LAYERS and self.OUTPUT_DIM > 0:
            # Build a coverage array: each index should be covered exactly once
            coverage = [0] * self.OUTPUT_DIM
            for layer in self.LAYERS:
                for i in range(layer.start, layer.end):
                    if 0 <= i < self.OUTPUT_DIM:
                        coverage[i] += 1
                    else:
                        errors.append(
                            f"LAYERS: LayerSpec {layer.code!r} index {i} "
                            f"is out of range [0, {self.OUTPUT_DIM})"
                        )

            uncovered = [i for i, c in enumerate(coverage) if c == 0]
            if uncovered:
                errors.append(
                    f"LAYERS: indices {uncovered} are not covered by any layer"
                )

            overlapped = [i for i, c in enumerate(coverage) if c > 1]
            if overlapped:
                errors.append(
                    f"LAYERS: indices {overlapped} are covered by multiple layers"
                )

        # 7. LAYERS dim_names must match dimension_names
        try:
            dim_names = self.dimension_names
            layer_names = self.layer_dim_names
            if layer_names != dim_names:
                errors.append(
                    f"LAYERS dim_names concatenated {layer_names!r} does not "
                    f"match dimension_names {dim_names!r}"
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
            f"name={self.NAME!r}, "
            f"unit={self.UNIT!r}, "
            f"tier={self.TIER!r}, "
            f"dim={self.OUTPUT_DIM})"
        )
