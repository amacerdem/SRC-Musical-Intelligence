"""Abstract base classes for C3 nucleus models.

Roles (depth-ordered):
    Relay       (depth 0) — reads R3/H3 directly
    Encoder     (depth 1) — reads relay outputs
    Associator  (depth 2) — reads relay + encoder outputs
    Integrator  (depth 3) — reads relay + encoder + associator outputs
    Hub         (depth 4+) — reads all upstream + cross-unit pathways

``Nucleus`` is an alias for ``_NucleusBase`` used by the executor.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from torch import Tensor

from Musical_Intelligence.contracts.dataclasses import (
    H3DemandSpec,
    ModelMetadata,
    NeuroLink,
    RegionLink,
)


class _NucleusBase(ABC):
    """Shared base for all nucleus roles."""

    # -- Subclass must set these class attributes --
    NAME: str
    FULL_NAME: str
    UNIT: str
    FUNCTION: str
    OUTPUT_DIM: int
    LAYERS: tuple  # Tuple[LayerSpec, ...]

    # -- Abstract properties (mechanism-specific) --

    @property
    @abstractmethod
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """H3 feature demand specifications."""

    @property
    @abstractmethod
    def dimension_names(self) -> Tuple[str, ...]:
        """Names for each output dimension."""

    @property
    @abstractmethod
    def region_links(self) -> Tuple[RegionLink, ...]:
        """Brain region links."""

    @property
    @abstractmethod
    def neuro_links(self) -> Tuple[NeuroLink, ...]:
        """Neuromodulator links."""

    @property
    @abstractmethod
    def metadata(self) -> ModelMetadata:
        """Model metadata with citations."""

    # -- Derived helpers --

    # Processing depth — used by executor for ordering
    PROCESSING_DEPTH: int = 0

    def h3_demand_tuples(self) -> List[Tuple[int, int, int, int]]:
        """Return list of ``(r3_idx, horizon, morph, law)`` 4-tuples."""
        return [spec.as_tuple() for spec in self.h3_demand]


# Alias used by executor.py
Nucleus = _NucleusBase


class Relay(_NucleusBase):
    """Depth-0 nucleus — reads R3/H3 directly, no upstream dependencies."""

    ROLE = "relay"
    CROSS_UNIT_READS: Tuple[str, ...] = ()

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Compute relay output from raw features.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``

        Returns:
            ``(B, T, OUTPUT_DIM)``
        """


class Encoder(_NucleusBase):
    """Depth-1 nucleus — reads relay outputs."""

    ROLE = "encoder"
    UPSTREAM_READS: Tuple[str, ...] = ()
    CROSS_UNIT_READS: Tuple[str, ...] = ()

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        relay_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Compute encoder output from features + relay outputs.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            relay_outputs: ``{"NAME": (B, T, D)}`` from depth-0 relays.

        Returns:
            ``(B, T, OUTPUT_DIM)``
        """


class Associator(_NucleusBase):
    """Depth-2 nucleus — reads relay + encoder outputs."""

    ROLE = "associator"
    UPSTREAM_READS: Tuple[str, ...] = ()
    CROSS_UNIT_READS: Tuple[str, ...] = ()

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
    ) -> Tensor:
        """Compute associator output from features + all upstream outputs.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"NAME": (B, T, D)}`` from depth-0/1.

        Returns:
            ``(B, T, OUTPUT_DIM)``
        """


class Integrator(_NucleusBase):
    """Depth-3 nucleus — reads relay + encoder + associator outputs."""

    ROLE = "integrator"
    PROCESSING_DEPTH = 3
    UPSTREAM_READS: Tuple[str, ...] = ()
    CROSS_UNIT_READS: Tuple[str, ...] = ()

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
        cross_unit_inputs: Dict[str, Tensor] | None = None,
    ) -> Tensor:
        """Compute integrator output.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"NAME": (B, T, D)}`` from depth 0-2.
            cross_unit_inputs: Optional cross-unit pathway tensors.

        Returns:
            ``(B, T, OUTPUT_DIM)``
        """


class Hub(_NucleusBase):
    """Depth-4+ nucleus — reads all upstream + cross-unit pathways."""

    ROLE = "hub"
    PROCESSING_DEPTH = 4
    UPSTREAM_READS: Tuple[str, ...] = ()
    CROSS_UNIT_READS: Tuple[str, ...] = ()

    @abstractmethod
    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        upstream_outputs: Dict[str, Tensor],
        cross_unit_inputs: Dict[str, Tensor] | None = None,
    ) -> Tensor:
        """Compute hub output.

        Args:
            h3_features: ``{(r3_idx, horizon, morph, law): (B, T)}``
            r3_features: ``(B, T, 97)``
            upstream_outputs: ``{"NAME": (B, T, D)}`` from all depths.
            cross_unit_inputs: Optional cross-unit pathway tensors.

        Returns:
            ``(B, T, OUTPUT_DIM)``
        """
