"""R3 Spectral Analysis: 49D feature extraction from mel spectrograms."""

from __future__ import annotations

import importlib
from typing import List, Tuple

from torch import Tensor
import torch

from ...core.config import MIBetaConfig, MI_BETA_CONFIG
from ...core.types import R3Output
from ...contracts.base_spectral_group import BaseSpectralGroup
from ._registry import R3FeatureRegistry, R3FeatureMap

# Subdirectories to scan in order
_SUBDIR_ORDER = ("psychoacoustic", "dsp", "cross_domain", "extensions")


class R3Extractor:
    """Orchestrates 5 spectral groups to produce 49D R3 features."""

    def __init__(self, config: MIBetaConfig = MI_BETA_CONFIG) -> None:
        self._config = config
        self._registry = R3FeatureRegistry()
        self._feature_map: R3FeatureMap | None = None

        # Auto-discover groups
        for subdir in _SUBDIR_ORDER:
            try:
                mod = importlib.import_module(f"mi_beta.ear.r3.{subdir}")
                for name in getattr(mod, "__all__", []):
                    cls = getattr(mod, name)
                    if isinstance(cls, type) and issubclass(cls, BaseSpectralGroup) and cls is not BaseSpectralGroup:
                        self._registry.register(cls())
            except ImportError:
                pass

        # Freeze registry and assign index ranges
        self._feature_map = self._registry.freeze()

    def extract(self, mel: Tensor) -> R3Output:
        """(B, 128, T) → R3Output with features (B, T, 49)."""
        outputs = []
        for group in self._registry.groups:
            out = group.compute(mel)  # (B, T, group.OUTPUT_DIM)
            outputs.append(out)

        features = torch.cat(outputs, dim=-1)  # (B, T, total_dim)
        return R3Output(
            features=features,
            feature_names=self.feature_names,
        )

    @property
    def feature_map(self) -> R3FeatureMap:
        assert self._feature_map is not None
        return self._feature_map

    @property
    def feature_names(self) -> Tuple[str, ...]:
        names: List[str] = []
        for group in self._registry.groups:
            names.extend(group.feature_names)
        return tuple(names)

    @property
    def total_dim(self) -> int:
        return self._feature_map.total_dim if self._feature_map else 0
