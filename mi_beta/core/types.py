"""Pipeline output dataclasses. All tensors follow (B, T, D) unless noted."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor


# ── Ear Outputs ────────────────────────────────────────────────────────────────

@dataclass
class CochleaOutput:
    mel: Tensor           # (B, 128, T)
    sample_rate: int
    hop_length: int


@dataclass
class R3Output:
    features: Tensor              # (B, T, 49)
    feature_names: Tuple[str, ...]


@dataclass
class H3Output:
    features: Dict[Tuple[int, int, int, int], Tensor]  # {(r3_idx, h, m, l): (B, T)}


@dataclass
class EarOutput:
    cochlea: CochleaOutput
    r3: R3Output
    h3: H3Output


# ── Brain Outputs ──────────────────────────────────────────────────────────────

@dataclass
class ModelOutput:
    name: str
    unit: str
    tier: str
    tensor: Tensor                        # (B, T, output_dim)
    dimension_names: Tuple[str, ...]
    h3_demand: Tuple[Tuple[int, int, int, int], ...]


@dataclass
class UnitOutput:
    unit_name: str
    tensor: Tensor                        # (B, T, unit_dim)
    model_outputs: Dict[str, ModelOutput]
    model_ranges: Dict[str, Tuple[int, int]]
    dimension_names: Tuple[str, ...]


@dataclass
class BrainOutput:
    tensor: Tensor                        # (B, T, brain_dim)
    unit_outputs: Dict[str, UnitOutput]
    unit_ranges: Dict[str, Tuple[int, int]]
    dimension_names: Tuple[str, ...]

    def get_unit(self, unit_name: str) -> Tensor:
        """Extract unit slice from brain tensor."""
        start, end = self.unit_ranges[unit_name]
        return self.tensor[..., start:end]

    def get_model(self, unit_name: str, model_name: str) -> Tensor:
        """Extract model slice from brain tensor."""
        unit_start = self.unit_ranges[unit_name][0]
        model_start, model_end = self.unit_outputs[unit_name].model_ranges[model_name]
        global_start = unit_start + model_start
        global_end = unit_start + model_end
        return self.tensor[..., global_start:global_end]

    def get_dim(self, name: str) -> Tensor:
        """Extract single dimension by name."""
        idx = self.dimension_names.index(name)
        return self.tensor[..., idx]


# ── Language Outputs ───────────────────────────────────────────────────────────

@dataclass
class SemanticGroupOutput:
    group_name: str
    level: int
    tensor: Tensor                        # (B, T, dim)
    dimension_names: Tuple[str, ...]


@dataclass
class L3Output:
    model_name: str
    groups: Dict[str, SemanticGroupOutput]
    tensor: Tensor                        # (B, T, total_dim)


# ── Pipeline Output ────────────────────────────────────────────────────────────

@dataclass
class MIBetaOutput:
    mi_space: Tensor                              # (B, T, total_dim)
    cochlea_range: Tuple[int, int]                # always (0, 128)
    r3_range: Tuple[int, int]                     # (128, 128+r3_dim)
    brain_range: Tuple[int, int]                  # (r3_end, r3_end+brain_dim)
    l3_range: Optional[Tuple[int, int]] = None    # (brain_end, total) or None
    brain: Optional[BrainOutput] = None
    semantics: Optional[L3Output] = None
    ear: Optional[EarOutput] = None

    @property
    def cochlea(self) -> Tensor:
        s, e = self.cochlea_range
        return self.mi_space[..., s:e]

    @property
    def r3(self) -> Tensor:
        s, e = self.r3_range
        return self.mi_space[..., s:e]

    @property
    def brain_tensor(self) -> Tensor:
        s, e = self.brain_range
        return self.mi_space[..., s:e]

    @property
    def l3(self) -> Optional[Tensor]:
        if self.l3_range is None:
            return None
        s, e = self.l3_range
        return self.mi_space[..., s:e]

    @property
    def total_dim(self) -> int:
        return self.mi_space.shape[-1]
