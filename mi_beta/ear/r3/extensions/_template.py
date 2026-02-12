"""
_template.py — Template for creating a new R3 spectral group.

To add a new group to the R3 feature vector:

1. Copy this file to a new .py file in this directory (or any R3 subdirectory).
2. Rename the class and fill in GROUP_NAME, OUTPUT_DIM, feature_names, compute().
3. Export the class from the subdirectory's __init__.py via __all__.

The R3FeatureRegistry will auto-discover it and assign index ranges.
INDEX_RANGE is set automatically at freeze() time — you can leave it as (0, 0).

Example:
    # In extensions/__init__.py:
    from .my_new_group import MyNewGroup
    __all__ = ["MyNewGroup"]
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts import BaseSpectralGroup


class _TemplateGroup(BaseSpectralGroup):
    """Template — do NOT use directly. Copy and rename."""

    GROUP_NAME = "template"   # Unique name for this group
    OUTPUT_DIM = 3            # Number of features this group produces
    INDEX_RANGE = (0, 0)      # Auto-assigned by registry.freeze()

    @property
    def feature_names(self) -> List[str]:
        return [
            "feature_1",
            "feature_2",
            "feature_3",
        ]

    def compute(self, mel: Tensor) -> Tensor:
        """Compute features from mel spectrogram.

        Args:
            mel: (B, N_MELS, T) log-mel spectrogram

        Returns:
            (B, T, OUTPUT_DIM) features, ideally in [0, 1]
        """
        B, N, T = mel.shape
        # Your computation here. Example:
        mel_t = mel.transpose(1, 2)  # (B, T, N)
        f1 = mel_t.mean(dim=-1, keepdim=True)
        f2 = mel_t.std(dim=-1, keepdim=True)
        f3 = mel_t.max(dim=-1, keepdim=True).values

        features = torch.cat([f1, f2, f3], dim=-1)  # (B, T, 3)
        return features.clamp(0, 1)
