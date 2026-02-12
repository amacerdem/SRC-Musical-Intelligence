"""
R3 Spectral Analysis — 49D per frame (default groups).

Five groups extract spectral features from mel spectrogram:
  A: Consonance (7D)  [0:7]   — harmonic quality       (psychoacoustic/)
  B: Energy (5D)      [7:12]  — loudness and dynamics   (dsp/)
  C: Timbre (9D)      [12:21] — tonal quality           (dsp/)
  D: Change (4D)      [21:25] — spectral surprise       (dsp/)
  E: Interactions (24D)[25:49] — cross-layer coupling   (cross_domain/)

Groups are auto-discovered from subdirectory __init__.py exports.
New groups can be added in extensions/ without modifying this file.
"""

from __future__ import annotations

import importlib
import pkgutil
from typing import List, Tuple

import torch
from torch import Tensor

from ...core.config import MIBetaConfig, MI_BETA_CONFIG
from ...core.types import R3Output
from ._registry import R3FeatureRegistry, R3FeatureMap
from ...contracts import BaseSpectralGroup

# ═══════════════════════════════════════════════════════════════════════
# AUTO-DISCOVERY
# ═══════════════════════════════════════════════════════════════════════

# Subdirectories to scan for BaseSpectralGroup exports.
# Order matters: groups are concatenated in this order.
_SUBDIRECTORY_NAMES = ("psychoacoustic", "dsp", "cross_domain", "extensions")


def _discover_groups() -> List[BaseSpectralGroup]:
    """Import subdirectory __init__.py modules and collect exported groups.

    Each subdirectory's __init__.py is expected to define an __all__ list
    of BaseSpectralGroup subclasses. They are instantiated and returned
    in the order: psychoacoustic -> dsp -> cross_domain -> extensions.
    """
    groups: List[BaseSpectralGroup] = []

    for subdir in _SUBDIRECTORY_NAMES:
        try:
            mod = importlib.import_module(f".{subdir}", package=__name__)
        except ImportError:
            continue

        # Collect all BaseSpectralGroup subclasses exported by the module
        for attr_name in getattr(mod, "__all__", []):
            cls = getattr(mod, attr_name, None)
            if cls is None:
                continue
            if isinstance(cls, type) and issubclass(cls, BaseSpectralGroup) and cls is not BaseSpectralGroup:
                groups.append(cls())

    return groups


# ═══════════════════════════════════════════════════════════════════════
# R3 EXTRACTOR
# ═══════════════════════════════════════════════════════════════════════

class R3Extractor:
    """Orchestrates all R3 spectral groups.

    Groups are discovered from psychoacoustic/, dsp/, cross_domain/,
    and extensions/ subdirectories using the _registry.
    """

    def __init__(self, config: MIBetaConfig = MI_BETA_CONFIG) -> None:
        self.config = config

        # Discover and register groups
        self._registry = R3FeatureRegistry()
        for group in _discover_groups():
            self._registry.register(group)

        # Freeze to assign index ranges
        self._feature_map = self._registry.freeze()
        self.groups = self._registry.groups

    @property
    def feature_map(self) -> R3FeatureMap:
        """Frozen feature map with index ranges."""
        return self._feature_map

    def extract(self, mel: Tensor) -> R3Output:
        """Extract R3 features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            R3Output with features (B, T, total_dim)
        """
        parts = []
        names: List[str] = []
        for group in self.groups:
            feat = group.compute(mel)  # (B, T, group_dim)
            parts.append(feat)
            names.extend(group.feature_names)

        features = torch.cat(parts, dim=-1)  # (B, T, total_dim)
        return R3Output(features=features, feature_names=tuple(names))

    @property
    def feature_names(self) -> List[str]:
        names: List[str] = []
        for group in self.groups:
            names.extend(group.feature_names)
        return names

    @property
    def total_dim(self) -> int:
        return self._feature_map.total_dim
