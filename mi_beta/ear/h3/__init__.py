"""H3 Temporal Context: sparse demand-driven temporal feature extraction."""

from __future__ import annotations

from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from ...core.config import MIBetaConfig, MI_BETA_CONFIG
from ...core.types import H3Output
from .morph import MorphComputer
from .horizon import EventHorizon
from .attention import compute_attention_weights
from .demand import DemandTree


class H3Extractor:
    """Computes H3 temporal features on-demand for requested 4-tuples."""

    def __init__(self, config: MIBetaConfig = MI_BETA_CONFIG) -> None:
        self._config = config
        self._morph = MorphComputer()

    def extract(
        self,
        r3: Tensor,                                     # (B, T, 49)
        demand: Set[Tuple[int, int, int, int]],          # {(r3_idx, h, m, l), ...}
    ) -> H3Output:
        """Compute H3 features for demanded 4-tuples.

        Args:
            r3: R3 feature tensor (B, T, 49)
            demand: Set of (r3_idx, horizon, morph, law) tuples

        Returns:
            H3Output with sparse {4-tuple: (B, T)} dict
        """
        if not demand:
            return H3Output(features={})

        B, T, _ = r3.shape
        device = r3.device
        dtype = r3.dtype
        result: Dict[Tuple[int, int, int, int], Tensor] = {}

        # Group demands by horizon for efficiency
        tree = DemandTree.build(demand)

        for h_idx, triples in tree.items():
            horizon = EventHorizon(h_idx)
            n_frames = horizon.frames
            weights = compute_attention_weights(n_frames, device=device)

            for r3_idx, m_idx, l_idx in triples:
                key = (r3_idx, h_idx, m_idx, l_idx)
                r3_scalar = r3[..., r3_idx]  # (B, T)
                val = self._compute_morph_series(
                    r3_scalar, B, T, n_frames, m_idx, l_idx, weights, device, dtype
                )
                result[key] = val

        return H3Output(features=result)

    def _compute_morph_series(
        self, r3_scalar: Tensor, B: int, T: int,
        n_frames: int, m_idx: int, l_idx: int,
        weights: Tensor, device: torch.device, dtype: torch.dtype,
    ) -> Tensor:
        """Compute windowed morph for each frame. Returns (B, T)."""
        out = torch.zeros(B, T, device=device, dtype=dtype)
        half = n_frames // 2

        for t in range(T):
            # Window selection by law
            if l_idx == 0:  # Memory: Past → Now
                start = max(0, t - n_frames + 1)
                end = t + 1
            elif l_idx == 1:  # Prediction: Now → Future
                start = t
                end = min(T, t + n_frames)
            else:  # Integration: Bidirectional
                start = max(0, t - half)
                end = min(T, t + n_frames - half)

            window = r3_scalar[:, start:end]  # (B, win_len)
            win_len = window.shape[1]

            if win_len == 0:
                continue

            # Truncate and normalize weights
            w = weights[:win_len]
            w = w / w.sum().clamp(min=1e-8)

            out[:, t] = self._morph.compute(window, w, m_idx)

        return out
