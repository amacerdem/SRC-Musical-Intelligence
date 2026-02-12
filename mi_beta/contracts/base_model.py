"""
BaseModel -- THE central contract for all mi_beta cognitive models.

A cognitive model is a deterministic, zero-parameter function that transforms
H3 temporal features, R3 spectral features, and optional cross-unit inputs
into a fixed-dimensional output tensor.  Every output dimension has:

    - A human-readable name.
    - A scientific citation justifying its existence.
    - A defined value range (e.g. [0,1], [-1,1]).
    - Assignment to one of the E/M/P/F output layers.

Models are grouped into cognitive units (ARU, SPU, STU, IMU, etc.).  Each
model belongs to exactly one unit and one evidence tier (alpha/beta/gamma).

The BaseModel ABC enforces:
    1. Declarative metadata (NAME, UNIT, TIER, OUTPUT_DIM, etc.)
    2. H3 demand declaration (which temporal features are needed)
    3. Structured output with named dimensions and layers
    4. Cross-unit read declarations (CROSS_UNIT_READS)
    5. Consistent compute() signature

Example subclass (abbreviated):

    class SRP(BaseModel):
        NAME = "SRP"
        FULL_NAME = "Striatal Reward Pathway"
        UNIT = "ARU"
        TIER = "alpha"
        OUTPUT_DIM = 19
        MECHANISM_NAMES = ("AED", "CPD", "C0P")
        CROSS_UNIT_READS = ()
        LAYERS = (
            LayerSpec("E", "Neurochemical", 0, 3, ("da_caudate", "da_nacc", "opioid_proxy")),
            LayerSpec("M", "Circuit", 3, 6, ("vta_drive", "stg_nacc_coupling", "prediction_error")),
            ...
        )
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

from torch import Tensor

from .brain_region import BrainRegion
from .demand_spec import H3DemandSpec
from .layer_spec import LayerSpec
from .model_metadata import ModelMetadata
from .pathway_spec import CrossUnitPathway


class BaseModel(ABC):
    """Abstract base class for all mi_beta cognitive models.

    Subclasses MUST override all class constants and abstract members.
    The class is designed for zero-parameter deterministic models, but the
    contract is compatible with future learnable extensions.
    """

    # ═══════════════════════════════════════════════════════════════════
    # CLASS CONSTANTS — override in every subclass
    # ═══════════════════════════════════════════════════════════════════

    NAME: str = ""
    """Short model identifier (e.g. "SRP", "AAC", "VMM")."""

    FULL_NAME: str = ""
    """Full descriptive name (e.g. "Striatal Reward Pathway")."""

    UNIT: str = ""
    """Parent cognitive unit (e.g. "ARU", "SPU", "STU", "IMU")."""

    TIER: str = ""
    """Evidence tier: "alpha" (>=10 studies), "beta" (5-9), "gamma" (<5)."""

    OUTPUT_DIM: int = 0
    """Total output dimensionality.  Must equal sum of LAYERS dims."""

    MECHANISM_NAMES: Tuple[str, ...] = ()
    """Names of internal mechanisms (e.g. ("AED", "CPD")).
    Mechanisms are sub-computations; their outputs are combined into
    the model output.  Empty tuple if the model has no sub-mechanisms."""

    CROSS_UNIT_READS: Tuple[CrossUnitPathway, ...] = ()
    """Declared cross-unit data dependencies.  Empty if the model only
    reads H3/R3 features and does not depend on other models' outputs."""

    LAYERS: Tuple[LayerSpec, ...] = ()
    """Output layer structure.  Each LayerSpec defines a slice of the
    output tensor with semantic meaning.  The union of all layer ranges
    must cover [0, OUTPUT_DIM) without gaps or overlaps."""

    # ═══════════════════════════════════════════════════════════════════
    # ABSTRACT PROPERTIES
    # ═══════════════════════════════════════════════════════════════════

    @property
    @abstractmethod
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """All H3 temporal demands needed by this model.

        Each H3DemandSpec maps to a single scalar time series.  The set of
        as_tuple() values is passed to the DemandTree for efficient H3
        computation.

        Returns:
            Tuple of H3DemandSpec instances (may be empty for models that
            only read R3 features directly).
        """

    @property
    @abstractmethod
    def dimension_names(self) -> Tuple[str, ...]:
        """Ordered names for every output dimension.

        len(dimension_names) MUST equal OUTPUT_DIM.  Names must be unique
        within the model and follow snake_case convention.
        """

    @property
    @abstractmethod
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        """Brain regions associated with this model's computation.

        Used for MNI152 visualisation and anatomical grounding.
        """

    @property
    @abstractmethod
    def metadata(self) -> ModelMetadata:
        """Evidence provenance: citations, tier, confidence, falsification."""

    # ═══════════════════════════════════════════════════════════════════
    # ABSTRACT METHOD — the core computation
    # ═══════════════════════════════════════════════════════════════════

    @abstractmethod
    def compute(
        self,
        mechanism_outputs: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Compute the model output tensor.

        Args:
            mechanism_outputs: {mechanism_name: (B, T, mechanism_dim)} tensors
                from this model's internal mechanisms.  Empty dict if the model
                has no mechanisms (MECHANISM_NAMES is empty).
            h3_features: {(r3_idx, horizon, morph, law): (B, T)} per-demand
                H3 scalar time series.  Keyed by the 4-tuple from h3_demand.
            r3_features: (B, T, 49) R3 spectral feature tensor.
            cross_unit_inputs: Optional dict of named tensors from other models,
                keyed by pathway_id from CROSS_UNIT_READS.  None if the model
                has no cross-unit dependencies.

        Returns:
            (B, T, OUTPUT_DIM) output tensor with dimensions ordered as
            declared in dimension_names and structured according to LAYERS.
        """

    # ═══════════════════════════════════════════════════════════════════
    # COMPUTED HELPERS
    # ═══════════════════════════════════════════════════════════════════

    def h3_demand_tuples(self) -> Set[Tuple[int, int, int, int]]:
        """Return the set of raw (r3_idx, horizon, morph, law) 4-tuples.

        This is the format consumed by DemandTree.build() and H3Output.
        Deduplicates automatically via set semantics.
        """
        return {spec.as_tuple() for spec in self.h3_demand}

    @property
    def layer_dim_names(self) -> Tuple[str, ...]:
        """Flat tuple of dimension names derived from LAYERS.

        This MUST match dimension_names.  Provided as a cross-check.
        """
        names: list[str] = []
        for layer in self.LAYERS:
            names.extend(layer.dim_names)
        return tuple(names)

    @property
    def cross_unit_dependency_units(self) -> FrozenSet[str]:
        """Set of cognitive unit names this model depends on."""
        return frozenset(p.source_unit for p in self.CROSS_UNIT_READS)

    def validate_constants(self) -> List[str]:
        """Check internal consistency of class constants.

        Returns:
            List of error messages (empty if valid).
        """
        errors: list[str] = []

        if not self.NAME:
            errors.append("NAME must be non-empty")
        if not self.FULL_NAME:
            errors.append("FULL_NAME must be non-empty")
        if not self.UNIT:
            errors.append("UNIT must be non-empty")
        if self.TIER not in ("alpha", "beta", "gamma"):
            errors.append(f"TIER must be alpha/beta/gamma, got {self.TIER!r}")
        if self.OUTPUT_DIM <= 0:
            errors.append(f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}")

        # Validate LAYERS cover [0, OUTPUT_DIM) without gaps or overlaps
        if self.LAYERS:
            covered = set()
            for layer in self.LAYERS:
                for i in range(layer.start, layer.end):
                    if i in covered:
                        errors.append(
                            f"LAYERS overlap at index {i} "
                            f"(layer {layer.code!r})"
                        )
                    covered.add(i)
            expected = set(range(self.OUTPUT_DIM))
            missing = expected - covered
            extra = covered - expected
            if missing:
                errors.append(f"LAYERS missing indices: {sorted(missing)}")
            if extra:
                errors.append(f"LAYERS extra indices: {sorted(extra)}")

            # Check layer dim_names match dimension_names
            layer_names = self.layer_dim_names
            try:
                dim_names = self.dimension_names
                if layer_names != dim_names:
                    errors.append(
                        f"LAYERS dim_names {layer_names} != "
                        f"dimension_names {dim_names}"
                    )
            except NotImplementedError:
                pass  # dimension_names not yet implemented in subclass

        return errors

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.NAME!r}, unit={self.UNIT}, "
            f"tier={self.TIER}, dim={self.OUTPUT_DIM})"
        )
