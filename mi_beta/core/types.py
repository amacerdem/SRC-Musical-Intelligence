"""
MI-Beta Output Types -- Typed containers for pipeline outputs.

All tensors follow (B, T, D) convention unless noted.

Extends mi/core/types.py with multi-model brain architecture outputs:
  - ModelOutput: single model's computation result with metadata
  - UnitOutput: aggregated output of all models within a cognitive unit
  - BrainOutput: all units combined, with per-unit dimension map
  - MIBetaOutput: full pipeline output including dynamic MI-space
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, FrozenSet, List, Optional, Tuple

import torch
from torch import Tensor


# =====================================================================
# EAR OUTPUTS (unchanged from mi/)
# =====================================================================

@dataclass
class CochleaOutput:
    """Output of the Cochlea (mel spectrogram)."""
    mel: Tensor          # (B, N_MELS, T)
    sample_rate: int
    hop_length: int


@dataclass
class R3Output:
    """Output of R3 spectral analysis."""
    features: Tensor     # (B, T, 49)
    feature_names: Tuple[str, ...]


@dataclass
class H3Output:
    """Output of H3 temporal context -- per-R3-feature tracking.

    Each key is a 4-tuple (r3_idx, horizon, morph, law) that tracks
    a SPECIFIC R3 feature through temporal morphological analysis.
    """
    features: Dict[Tuple[int, int, int, int], Tensor]  # {(r3,h,m,l): (B, T)}

    def get(self, r3_idx: int, h: int, m: int, l: int) -> Tensor:
        """Get a per-R3-feature H3 scalar time series."""
        return self.features[(r3_idx, h, m, l)]

    def __len__(self) -> int:
        return len(self.features)


@dataclass
class EarOutput:
    """Combined EAR output."""
    cochlea: CochleaOutput
    r3: R3Output
    h3: H3Output


# =====================================================================
# BRAIN OUTPUTS -- Multi-model architecture
# =====================================================================

@dataclass
class ModelOutput:
    """Output from a single Brain model (e.g., ARU-beta1-PUPF).

    Each model produces a fixed-size tensor and carries metadata
    about its provenance: which unit it belongs to, its confidence
    tier, its H3 demand set, and the names of each output dimension.
    """
    name: str                                          # e.g., "PUPF"
    unit: str                                          # e.g., "ARU"
    tier: str                                          # "alpha", "beta", "gamma"
    tensor: Tensor                                     # (B, T, output_dim)
    dimension_names: Tuple[str, ...]                   # one name per output dim
    h3_demand: FrozenSet[Tuple[int, int, int, int]]    # H3 4-tuples this model reads

    @property
    def output_dim(self) -> int:
        return self.tensor.shape[-1]

    def get_dim(self, name: str) -> Tensor:
        """Extract a single dimension by name."""
        idx = self.dimension_names.index(name)
        return self.tensor[..., idx]

    def __repr__(self) -> str:
        return (
            f"ModelOutput(name={self.name!r}, unit={self.unit!r}, "
            f"tier={self.tier!r}, dim={self.output_dim}, "
            f"h3_demand={len(self.h3_demand)})"
        )


@dataclass
class UnitOutput:
    """Aggregated output of all models within a single cognitive unit.

    The tensor is formed by concatenating all model outputs within the
    unit in a deterministic order (sorted by model name).
    """
    unit_name: str                                     # e.g., "ARU"
    tensor: Tensor                                     # (B, T, unit_dim)
    model_outputs: Dict[str, ModelOutput]               # model_name -> ModelOutput
    model_ranges: Dict[str, Tuple[int, int]]            # model_name -> (start, end) in tensor
    dimension_names: Tuple[str, ...]                    # flat list of all dim names

    @property
    def total_dim(self) -> int:
        return self.tensor.shape[-1]

    @property
    def n_models(self) -> int:
        return len(self.model_outputs)

    def get_model(self, model_name: str) -> Tensor:
        """Extract a model's slice from the unit tensor."""
        s, e = self.model_ranges[model_name]
        return self.tensor[..., s:e]

    def get_dim(self, name: str) -> Tensor:
        """Extract a single dimension by name from the unit tensor."""
        idx = self.dimension_names.index(name)
        return self.tensor[..., idx]

    def __repr__(self) -> str:
        return (
            f"UnitOutput(unit={self.unit_name!r}, "
            f"dim={self.total_dim}, "
            f"models={list(self.model_outputs.keys())})"
        )


@dataclass
class BrainOutput:
    """Output of the full Brain -- all cognitive units combined.

    The tensor is formed by concatenating all unit outputs in
    UNIT_EXECUTION_ORDER. Per-unit and per-model ranges enable
    surgical extraction of any slice.
    """
    tensor: Tensor                                     # (B, T, brain_dim)
    unit_outputs: Dict[str, UnitOutput]                # unit_name -> UnitOutput
    unit_ranges: Dict[str, Tuple[int, int]]            # unit_name -> (start, end) in tensor
    dimension_names: Tuple[str, ...]                   # flat list of all dim names

    @property
    def total_dim(self) -> int:
        return self.tensor.shape[-1]

    @property
    def n_units(self) -> int:
        return len(self.unit_outputs)

    def get_unit(self, unit_name: str) -> Tensor:
        """Extract a unit's slice from the brain tensor."""
        s, e = self.unit_ranges[unit_name]
        return self.tensor[..., s:e]

    def get_unit_output(self, unit_name: str) -> UnitOutput:
        """Get the full UnitOutput for a specific unit."""
        return self.unit_outputs[unit_name]

    def get_model(self, unit_name: str, model_name: str) -> Tensor:
        """Extract a specific model's tensor from the brain tensor.

        Computes the global offset by combining unit range and
        model range within the unit.
        """
        us, _ = self.unit_ranges[unit_name]
        ms, me = self.unit_outputs[unit_name].model_ranges[model_name]
        return self.tensor[..., us + ms:us + me]

    def get_dim(self, name: str) -> Tensor:
        """Extract a single dimension by name from the brain tensor."""
        idx = self.dimension_names.index(name)
        return self.tensor[..., idx]

    def __repr__(self) -> str:
        return (
            f"BrainOutput(dim={self.total_dim}, "
            f"units={list(self.unit_outputs.keys())})"
        )


# =====================================================================
# LANGUAGE OUTPUTS (unchanged from mi/)
# =====================================================================

@dataclass
class SemanticGroupOutput:
    """Output of a single L3 semantic group."""
    group_name: str      # "alpha", "beta", "gamma", "delta"
    level: int           # 1-8
    tensor: Tensor       # (B, T, dim)
    dimension_names: Tuple[str, ...]


@dataclass
class L3Output:
    """Output of L3 semantic interpretation."""
    model_name: str
    groups: Dict[str, SemanticGroupOutput]  # {"alpha": ..., "beta": ...}
    tensor: Tensor       # (B, T, total_dim) -- concatenated

    @property
    def total_dim(self) -> int:
        return self.tensor.shape[-1]


# =====================================================================
# PIPELINE OUTPUT
# =====================================================================

@dataclass
class MIBetaOutput:
    """Full MI-Beta pipeline output.

    The MI-space tensor is dynamically assembled from:
      [cochlea(128D) | r3(49D) | brain(variable) | l3(variable)]

    The total_dim depends on which units/models are active.

    Attributes:
        mi_space: The assembled MI-space vector, (B, T, total_dim)
        cochlea_range: (start, end) of cochlea in mi_space
        r3_range: (start, end) of R3 in mi_space
        brain_range: (start, end) of brain in mi_space
        l3_range: (start, end) of L3 in mi_space (if present)
        brain: Full BrainOutput with per-unit/per-model access
        semantics: Optional L3 output
        ear: Optional EarOutput (included if return_ear=True)
    """
    mi_space: Tensor                                    # (B, T, total_dim)

    # Section ranges within mi_space
    cochlea_range: Tuple[int, int]                      # always (0, 128)
    r3_range: Tuple[int, int]                           # (128, 128+r3_dim)
    brain_range: Tuple[int, int]                        # (r3_end, r3_end+brain_dim)
    l3_range: Optional[Tuple[int, int]] = None          # (brain_end, total) or None

    # Component outputs
    brain: Optional[BrainOutput] = None
    semantics: Optional[L3Output] = None
    ear: Optional[EarOutput] = None

    @property
    def total_dim(self) -> int:
        return self.mi_space.shape[-1]

    @property
    def cochlea(self) -> Tensor:
        """Extract cochlea slice from MI-space."""
        s, e = self.cochlea_range
        return self.mi_space[..., s:e]

    @property
    def r3(self) -> Tensor:
        """Extract R3 slice from MI-space."""
        s, e = self.r3_range
        return self.mi_space[..., s:e]

    @property
    def brain_tensor(self) -> Tensor:
        """Extract brain slice from MI-space."""
        s, e = self.brain_range
        return self.mi_space[..., s:e]

    @property
    def l3(self) -> Optional[Tensor]:
        """Extract L3 slice from MI-space, if present."""
        if self.l3_range is None:
            return None
        s, e = self.l3_range
        return self.mi_space[..., s:e]

    def __repr__(self) -> str:
        parts = [f"cochlea={self.cochlea_range}", f"r3={self.r3_range}"]
        parts.append(f"brain={self.brain_range}")
        if self.l3_range is not None:
            parts.append(f"l3={self.l3_range}")
        return f"MIBetaOutput(dim={self.total_dim}, {', '.join(parts)})"
