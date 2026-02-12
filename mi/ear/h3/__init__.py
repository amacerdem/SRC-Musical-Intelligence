"""
H³ Temporal Context — Multi-scale windowed morphological features.

Computes temporal context at multiple horizons using:
  1. EventHorizon: defines window sizes
  2. Attention: exponential weighting A(dt) = exp(-3|dt|/H)
  3. MorphComputer: 24 morphological features per window
  4. DemandTree: sparse computation (only demanded tuples)

Demand format:
  4-tuple (r3_idx, h, m, l): per-R³ feature tracking
  Each tuple specifies WHICH R³ feature (0-48) to track through time.
"""

from __future__ import annotations

from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from ...core.config import MIConfig, MI_CONFIG
from ...core.constants import HORIZON_FRAMES, ATTENTION_DECAY
from ...core.types import H3Output
from .horizon import EventHorizon
from .morph import MorphComputer
from .attention import compute_attention_weights
from .demand import DemandTree


class H3Extractor:
    """Orchestrates H³ temporal context extraction.

    Computes per-R³-feature morphological statistics at demanded
    (r3_idx, horizon, morph, law) 4-tuples. Only computes what
    the MusicalBrain needs — sparse, not dense.
    """

    def __init__(self, config: MIConfig = MI_CONFIG) -> None:
        self.config = config
        self.morph_computer = MorphComputer()

    def extract(
        self,
        r3: Tensor,
        demand: Set[Tuple[int, int, int, int]],
    ) -> H3Output:
        """Extract demanded H³ temporal features.

        Args:
            r3: (B, T, 49) R³ spectral features
            demand: set of (r3_idx, horizon, morph, law) 4-tuples

        Returns:
            H3Output with features dict {(r3_idx, h, m, l): (B, T)}
        """
        B, T, D = r3.shape
        device = r3.device

        tree = DemandTree.build(demand)
        features: Dict[Tuple[int, int, int, int], Tensor] = {}

        for h_idx, rml_set in tree.items():
            horizon = EventHorizon(h_idx)
            n_frames = min(horizon.frames, T)
            weights = compute_attention_weights(n_frames, device=device)

            for r3_idx, m_idx, l_idx in rml_set:
                r3_scalar = r3[..., r3_idx]  # (B, T)

                result = self._compute_morph_series(
                    r3_scalar, B, T, n_frames, m_idx, l_idx, weights, device, r3.dtype
                )
                features[(r3_idx, h_idx, m_idx, l_idx)] = result

        return H3Output(features=features)

    def _compute_morph_series(
        self,
        r3_scalar: Tensor,
        B: int,
        T: int,
        n_frames: int,
        m_idx: int,
        l_idx: int,
        weights: Tensor,
        device,
        dtype,
    ) -> Tensor:
        """Compute a single morph across all time frames.

        Args:
            r3_scalar: (B, T) — the scalar time series to analyze
            B, T: batch and time dimensions
            n_frames: window size in frames
            m_idx: morph index (0-23)
            l_idx: law index (0=memory, 1=prediction, 2=integration)
            weights: (n_frames,) attention weights
            device, dtype: tensor properties

        Returns:
            (B, T) morph values
        """
        result = torch.zeros(B, T, device=device, dtype=dtype)

        for t in range(T):
            # Get window based on law
            if l_idx == 0:  # L0: Memory (past → now)
                start = max(0, t - n_frames + 1)
                end = t + 1
            elif l_idx == 1:  # L1: Prediction (now → future)
                start = t
                end = min(T, t + n_frames)
            else:  # L2: Integration (bidirectional)
                half = n_frames // 2
                start = max(0, t - half)
                end = min(T, t + n_frames - half)

            window = r3_scalar[:, start:end]  # (B, win_len)
            win_len = window.shape[1]

            if win_len == 0:
                continue

            # Apply attention weights (truncated to window length)
            w = weights[:win_len]
            w = w / w.sum().clamp(min=1e-8)

            # Compute morph
            result[:, t] = self.morph_computer.compute(
                window, w, m_idx
            )

        return result
