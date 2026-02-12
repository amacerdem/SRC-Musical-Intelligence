"""
R³ Spectral Analysis — 49D per frame.

Five groups extract spectral features from mel spectrogram:
  A: Consonance (7D)  [0:7]   — harmonic quality
  B: Energy (5D)      [7:12]  — loudness and dynamics
  C: Timbre (9D)      [12:21] — tonal quality
  D: Change (4D)      [21:25] — spectral surprise
  E: Interactions (24D)[25:49] — cross-layer coupling
"""

from __future__ import annotations

from typing import List, Tuple

import torch
from torch import Tensor

from ...core.config import MIConfig, MI_CONFIG
from ...core.types import R3Output
from .consonance import ConsonanceGroup
from .energy import EnergyGroup
from .timbre import TimbreGroup
from .change import ChangeGroup
from .interactions import InteractionsGroup


class R3Extractor:
    """Orchestrates all R³ spectral groups."""

    def __init__(self, config: MIConfig = MI_CONFIG) -> None:
        self.config = config
        self.groups = [
            ConsonanceGroup(),
            EnergyGroup(),
            TimbreGroup(),
            ChangeGroup(),
            InteractionsGroup(),
        ]

    def extract(self, mel: Tensor) -> R3Output:
        """Extract 49D R³ features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            R3Output with features (B, T, 49)
        """
        parts = []
        names: List[str] = []
        for group in self.groups:
            feat = group.compute(mel)  # (B, T, group_dim)
            parts.append(feat)
            names.extend(group.feature_names)

        features = torch.cat(parts, dim=-1)  # (B, T, 49)
        return R3Output(features=features, feature_names=tuple(names))

    @property
    def feature_names(self) -> List[str]:
        names: List[str] = []
        for group in self.groups:
            names.extend(group.feature_names)
        return names
