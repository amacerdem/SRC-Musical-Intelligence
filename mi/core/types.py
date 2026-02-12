"""
MI Output Types — Typed containers for pipeline outputs.

All tensors follow (B, T, D) convention unless noted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor


# ═══════════════════════════════════════════════════════════════════════
# EAR OUTPUTS
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class CochleaOutput:
    """Output of the Cochlea (mel spectrogram)."""
    mel: Tensor          # (B, N_MELS, T)
    sample_rate: int
    hop_length: int


@dataclass
class R3Output:
    """Output of R³ spectral analysis."""
    features: Tensor     # (B, T, 49)
    feature_names: Tuple[str, ...]


@dataclass
class H3Output:
    """Output of H³ temporal context — per-R³-feature tracking.

    Each key is a 4-tuple (r3_idx, horizon, morph, law) that tracks
    a SPECIFIC R³ feature through temporal morphological analysis.
    """
    features: Dict[Tuple[int, int, int, int], Tensor]  # {(r3,h,m,l): (B, T)}

    def get(self, r3_idx: int, h: int, m: int, l: int) -> Tensor:
        """Get a per-R³-feature H³ scalar time series."""
        return self.features[(r3_idx, h, m, l)]

    def __len__(self) -> int:
        return len(self.features)


@dataclass
class EarOutput:
    """Combined EAR output."""
    cochlea: CochleaOutput
    r3: R3Output
    h3: H3Output


# ═══════════════════════════════════════════════════════════════════════
# BRAIN OUTPUTS (legacy — kept for import compatibility)
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class MechanismOutput:
    """Deprecated: mechanisms removed. Kept for import compatibility."""
    name: str
    tensor: Tensor
    output_dim: int


@dataclass
class ModelOutput:
    """Deprecated: separate models replaced by MusicalBrain. Kept for import compatibility."""
    name: str
    tensor: Tensor
    output_dim: int
    layer_names: Tuple[str, ...]
    dimension_names: Tuple[str, ...]


# ═══════════════════════════════════════════════════════════════════════
# LANGUAGE OUTPUTS
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class SemanticGroupOutput:
    """Output of a single L³ semantic group."""
    group_name: str      # "alpha", "beta", "gamma", "delta"
    level: int           # 1-4
    tensor: Tensor       # (B, T, dim)
    dimension_names: Tuple[str, ...]


@dataclass
class L3Output:
    """Output of L³ semantic interpretation."""
    model_name: str
    groups: Dict[str, SemanticGroupOutput]  # {"alpha": ..., "beta": ...}
    tensor: Tensor       # (B, T, total_dim) — concatenated

    @property
    def total_dim(self) -> int:
        return self.tensor.shape[-1]


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE OUTPUT
# ═══════════════════════════════════════════════════════════════════════

@dataclass
class MIOutput:
    """Full MI pipeline output.

    brain: BrainOutput (26D unified output from MusicalBrain)
    semantics: L3Output (optional, from language layer)
    ear: EarOutput (optional, included if return_ear=True)
    """
    brain: object                       # BrainOutput (avoid circular import)
    semantics: Optional[L3Output] = None
    ear: Optional[EarOutput] = None
