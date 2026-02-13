"""Template for custom R3 spectral groups.

To add a new group:
1. Copy this file to a new .py in any R3 subdirectory (or extensions/)
2. Subclass BaseSpectralGroup
3. Define GROUP_NAME, OUTPUT_DIM, feature_names, compute()
4. Export from subdirectory __init__.py via __all__
5. R3Extractor auto-discovers and registers at init time
6. INDEX_RANGE assigned automatically by freeze()
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ....contracts.base_spectral_group import BaseSpectralGroup


class _TemplateGroup(BaseSpectralGroup):
    GROUP_NAME = "_template"
    DOMAIN = "extensions"
    OUTPUT_DIM = 1

    @property
    def feature_names(self) -> List[str]:
        return ["template_feature"]

    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        return torch.zeros(B, T, self.OUTPUT_DIM, device=mel.device, dtype=mel.dtype)
