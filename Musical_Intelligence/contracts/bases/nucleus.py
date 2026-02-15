"""Nucleus -- Base class hierarchy for all 96 C³ brain components.

Replaces the flat ``BaseModel`` approach with a **role-based hierarchy**
that makes the 5-depth processing structure visible from the type alone:

    Relay (0) → Encoder (1) → Associator (2) → Integrator (3) → Hub (4-5)

Each role has a distinct ``compute()`` signature reflecting what it can read.
Scope-derived properties partition output dimensions into internal (downstream
nuclei), external (final output), and hybrid (both) based on ``LayerSpec.scope``.

``Nucleus`` coexists with ``BaseModel`` — new brain code uses ``Nucleus``,
existing skeletons remain on ``BaseModel`` until migrated.

See TERMINOLOGY.md Section 8 for the full specification.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, FrozenSet, List, Optional, Set, Tuple

from Musical_Intelligence.contracts.dataclasses import (
    Citation,
    CrossUnitPathway,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
    NeuroLink,
    RegionLink,
)

if TYPE_CHECKING:
    from torch import Tensor


_VALID_ROLES = frozenset({"relay", "encoder", "associator", "integrator", "hub"})


class Nucleus(ABC):
    """Abstract base class for all 96 C³ brain components.

    A Nucleus transforms H³ temporal features, R³ spectral features,
    and (role-dependent) upstream outputs into a fixed-dimensional
    output tensor structured by E/M/P/F layers with scope labels.

    Class Constants (must override in every subclass):
        NAME:              Short identifier (e.g. ``"BCH"``).
        FULL_NAME:         Full descriptive name.
        UNIT:              Parent cognitive unit (e.g. ``"SPU"``).
        ROLE:              Processing role (set by role subclass).
        PROCESSING_DEPTH:  Integer depth (set by role subclass).
        OUTPUT_DIM:        Total output dimensionality (all scopes).
        LAYERS:            E/M/P/F layer structure with scope labels.
        UPSTREAM_READS:    Same-unit dependencies (nucleus names).
        CROSS_UNIT_READS:  Cross-unit pathway dependencies.
    """

    # ------------------------------------------------------------------
    # Class constants — override in every concrete subclass
    # ------------------------------------------------------------------

    NAME: str = ""
    FULL_NAME: str = ""
    UNIT: str = ""
    ROLE: str = ""
    PROCESSING_DEPTH: int = -1
    OUTPUT_DIM: int = 0
    LAYERS: Tuple[LayerSpec, ...] = ()
    UPSTREAM_READS: Tuple[str, ...] = ()
    CROSS_UNIT_READS: Tuple[CrossUnitPathway, ...] = ()

    # ------------------------------------------------------------------
    # Abstract properties
    # ------------------------------------------------------------------

    @property
    @abstractmethod
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """H³ temporal demands needed by this nucleus."""

    @property
    @abstractmethod
    def dimension_names(self) -> Tuple[str, ...]:
        """Ordered names for every output dimension.

        ``len(dimension_names)`` MUST equal ``OUTPUT_DIM``.
        """

    @property
    @abstractmethod
    def region_links(self) -> Tuple[RegionLink, ...]:
        """Declarative mapping: output dims → brain regions (→ RAM)."""

    @property
    @abstractmethod
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        """Declarative mapping: output dims → neurochemical channels."""

    @property
    @abstractmethod
    def metadata(self) -> ModelMetadata:
        """Evidence provenance: citations, tier, confidence, falsification."""

    # ------------------------------------------------------------------
    # Scope-derived dimension indices
    # ------------------------------------------------------------------

    @property
    def internal_dims(self) -> Tuple[int, ...]:
        """Dimension indices routed to downstream nuclei only."""
        return self._dims_by_scope("internal")

    @property
    def external_dims(self) -> Tuple[int, ...]:
        """Dimension indices routed to final output only."""
        return self._dims_by_scope("external")

    @property
    def hybrid_dims(self) -> Tuple[int, ...]:
        """Dimension indices routed to both downstream and final output."""
        return self._dims_by_scope("hybrid")

    @property
    def routable_dims(self) -> Tuple[int, ...]:
        """Dimension indices visible to downstream nuclei (internal + hybrid)."""
        return tuple(sorted(set(self.internal_dims) | set(self.hybrid_dims)))

    @property
    def exportable_dims(self) -> Tuple[int, ...]:
        """Dimension indices in the final BrainOutput tensor (external + hybrid)."""
        return tuple(sorted(set(self.external_dims) | set(self.hybrid_dims)))

    def _dims_by_scope(self, scope: str) -> Tuple[int, ...]:
        """Return sorted dimension indices for layers matching ``scope``."""
        indices: List[int] = []
        for layer in self.LAYERS:
            if layer.scope == scope:
                indices.extend(range(layer.start, layer.end))
        return tuple(sorted(indices))

    # ------------------------------------------------------------------
    # Computed helpers
    # ------------------------------------------------------------------

    def h3_demand_tuples(self) -> Set[Tuple[int, int, int, int]]:
        """Set of raw 4-tuples for ``DemandTree.build()``."""
        return {spec.as_tuple() for spec in self.h3_demand}

    @property
    def layer_dim_names(self) -> Tuple[str, ...]:
        """Flat tuple of dimension names derived from ``LAYERS``."""
        names: List[str] = []
        for layer in self.LAYERS:
            names.extend(layer.dim_names)
        return tuple(names)

    @property
    def cross_unit_dependency_units(self) -> FrozenSet[str]:
        """Set of cognitive unit names this nucleus depends on."""
        return frozenset(p.source_unit for p in self.CROSS_UNIT_READS)

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    def validate_constants(self) -> list[str]:
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
        if self.ROLE not in _VALID_ROLES:
            errors.append(
                f"ROLE must be one of {sorted(_VALID_ROLES)}, "
                f"got {self.ROLE!r}"
            )
        if self.PROCESSING_DEPTH < 0:
            errors.append(
                f"PROCESSING_DEPTH must be >= 0, got {self.PROCESSING_DEPTH}"
            )
        if self.OUTPUT_DIM <= 0:
            errors.append(f"OUTPUT_DIM must be > 0, got {self.OUTPUT_DIM}")

        # LAYERS must cover [0, OUTPUT_DIM) without gaps or overlaps
        if self.LAYERS and self.OUTPUT_DIM > 0:
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
                errors.append(f"LAYERS: indices {uncovered} are not covered")
            overlapped = [i for i, c in enumerate(coverage) if c > 1]
            if overlapped:
                errors.append(f"LAYERS: indices {overlapped} have multiple coverage")

        # LAYERS dim_names must match dimension_names
        try:
            if self.layer_dim_names != self.dimension_names:
                errors.append(
                    f"LAYERS dim_names {self.layer_dim_names!r} does not "
                    f"match dimension_names {self.dimension_names!r}"
                )
        except NotImplementedError:
            pass

        # RegionLinks must reference valid dim_names
        try:
            dim_names = set(self.dimension_names)
            for rl in self.region_links:
                if rl.dim_name not in dim_names:
                    errors.append(
                        f"RegionLink references unknown dim {rl.dim_name!r}"
                    )
        except NotImplementedError:
            pass

        # NeuroLinks must reference valid dim_names
        try:
            dim_names = set(self.dimension_names)
            for nl in self.neuro_links:
                if nl.dim_name not in dim_names:
                    errors.append(
                        f"NeuroLink references unknown dim {nl.dim_name!r}"
                    )
        except NotImplementedError:
            pass

        return errors

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"name={self.NAME!r}, unit={self.UNIT!r}, "
            f"role={self.ROLE!r}, depth={self.PROCESSING_DEPTH}, "
            f"dim={self.OUTPUT_DIM})"
        )


# ======================================================================
# Role subclasses — each fixes ROLE, PROCESSING_DEPTH, and compute()
# ======================================================================


class Relay(Nucleus):
    """Depth 0 — foundation transformation from raw R³/H³.

    Relays are the ONLY role that touches raw R³/H³ directly. All other
    roles receive processed signals from upstream nuclei.
    """

    ROLE = "relay"
    PROCESSING_DEPTH = 0
    UPSTREAM_READS = ()  # Relays read nothing from same unit

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Transform raw R³/H³ into this unit's foundational representation.

        Args:
            h3_features: Per-demand H³ time series, keyed by 4-tuples.
            r3_features: ``(B, T, 49)`` R³ spectral features.

        Returns:
            ``(B, T, OUTPUT_DIM)`` output tensor.
        """


class Encoder(Nucleus):
    """Depth 1 — feature extraction from Relay output."""

    ROLE = "encoder"
    PROCESSING_DEPTH = 1

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        relay_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Extract features from the unit's Relay.

        Args:
            h3_features: Per-demand H³ time series.
            r3_features: ``(B, T, 49)`` R³ spectral features.
            relay_outputs: Dict mapping Relay NAME → ``(B, T, relay_dim)``
                           (routable dims only).

        Returns:
            ``(B, T, OUTPUT_DIM)`` output tensor.
        """


class Associator(Nucleus):
    """Depth 2 — combines Relay + Encoder outputs."""

    ROLE = "associator"
    PROCESSING_DEPTH = 2

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Combine Relay and Encoder outputs.

        Args:
            h3_features: Per-demand H³ time series.
            r3_features: ``(B, T, 49)`` R³ spectral features.
            upstream_outputs: Dict mapping nucleus NAME → routable output
                              tensor for all Relays and Encoders in this unit.

        Returns:
            ``(B, T, OUTPUT_DIM)`` output tensor.
        """


class Integrator(Nucleus):
    """Depth 3 — cross-stream integration within unit."""

    ROLE = "integrator"
    PROCESSING_DEPTH = 3

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Integrate across streams, optionally with cross-unit data.

        Args:
            h3_features: Per-demand H³ time series.
            r3_features: ``(B, T, 49)`` R³ spectral features.
            upstream_outputs: All upstream (R+E+A) routable outputs.
            cross_unit_inputs: Optional cross-unit pathway data.

        Returns:
            ``(B, T, OUTPUT_DIM)`` output tensor.
        """


class Hub(Nucleus):
    """Depth 4-5 — highest-level convergence within unit."""

    ROLE = "hub"
    PROCESSING_DEPTH = 4  # Override to 5 if needed

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Highest-level convergence computation.

        Args:
            h3_features: Per-demand H³ time series.
            r3_features: ``(B, T, 49)`` R³ spectral features.
            upstream_outputs: All upstream routable outputs.
            cross_unit_inputs: Optional cross-unit pathway data.

        Returns:
            ``(B, T, OUTPUT_DIM)`` output tensor.
        """
