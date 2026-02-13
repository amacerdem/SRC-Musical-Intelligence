"""BaseModel: central ABC for all 94 cognitive models."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, FrozenSet, List, Optional, Set, Tuple

import torch
from torch import Tensor

from .layer_spec import LayerSpec
from .demand_spec import H3DemandSpec
from .pathway_spec import CrossUnitPathway
from .brain_region import BrainRegion
from .model_metadata import ModelMetadata


class BaseModel(ABC):
    # ── CLASS CONSTANTS ──
    NAME: str = ""                              # "BCH", "SRP", etc.
    FULL_NAME: str = ""                         # "Brainstem Consonance Hierarchy"
    UNIT: str = ""                              # "SPU", "ARU", etc.
    TIER: str = ""                              # "alpha", "beta", "gamma"
    OUTPUT_DIM: int = 0                         # sum of LAYERS dims
    MECHANISM_NAMES: Tuple[str, ...] = ()       # ("PPC",), ("AED", "CPD"), etc.
    CROSS_UNIT_READS: Tuple[CrossUnitPathway, ...] = ()
    LAYERS: Tuple[LayerSpec, ...] = ()          # E/M/P/F output structure

    # ── ABSTRACT PROPERTIES ──
    @property
    @abstractmethod
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        """All H3 temporal demands needed by this model."""

    @property
    @abstractmethod
    def dimension_names(self) -> Tuple[str, ...]:
        """Ordered names for every output dimension. len == OUTPUT_DIM"""

    @property
    @abstractmethod
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        """Brain regions associated with this model's computation."""

    @property
    @abstractmethod
    def metadata(self) -> ModelMetadata:
        """Evidence provenance: citations, tier, confidence, falsification."""

    # ── ABSTRACT METHOD — THE CORE COMPUTATION ──
    @abstractmethod
    def compute(
        self,
        mechanism_outputs: Dict[str, Tensor],              # {mech_name: (B,T,30)}
        h3_features: Dict[Tuple[int, int, int, int], Tensor],  # {4-tuple: (B,T)}
        r3_features: Tensor,                                # (B, T, 49)
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:                                            # (B, T, OUTPUT_DIM)
        ...

    # ── COMPUTED HELPERS ──
    def h3_demand_tuples(self) -> Set[Tuple[int, int, int, int]]:
        return {d.as_tuple() for d in self.h3_demand}

    @property
    def layer_dim_names(self) -> Tuple[str, ...]:
        names: List[str] = []
        for layer in self.LAYERS:
            names.extend(layer.dim_names)
        return tuple(names)

    @property
    def cross_unit_dependency_units(self) -> FrozenSet[str]:
        return frozenset(p.source_unit for p in self.CROSS_UNIT_READS)

    def validate_constants(self) -> List[str]:
        errors = []
        layer_dim = sum(l.dim for l in self.LAYERS)
        if layer_dim != self.OUTPUT_DIM:
            errors.append(
                f"{self.NAME}: LAYERS sum {layer_dim} != OUTPUT_DIM {self.OUTPUT_DIM}"
            )
        if len(self.dimension_names) != self.OUTPUT_DIM:
            errors.append(
                f"{self.NAME}: dimension_names len {len(self.dimension_names)} "
                f"!= OUTPUT_DIM {self.OUTPUT_DIM}"
            )
        return errors
