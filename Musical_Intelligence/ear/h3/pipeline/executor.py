"""H3Executor -- 7-phase execution loop for sparse temporal morphology.

Orchestrates the complete H3 pipeline: given an R3 spectral tensor and a
demand tree grouped by horizon, computes all demanded temporal morph
features and returns them as a sparse dictionary.

Execution phases
----------------
1. Demand collection   -- input is the demand_tree (already built)
2. Tree ready          -- input is pre-grouped by horizon
3. Horizon loop        -- iterate sorted horizons
4. Window selection    -- law determines past / future / bidirectional
5. Attention weighting -- kernel weights, truncated and renormalized
6. Morph dispatch      -- batch morph computes all frames at once
7. Result packing      -- normalize and store as (B, T) tensors

For efficiency, tuples sharing (horizon, r3_idx, law) reuse the same
window slice.  Steady-state frames (full-size windows) are vectorized
via ``torch.Tensor.unfold``; boundary frames are left as zero.

Source of truth
---------------
- Docs/H3/Pipeline/ExecutionModel.md      7 phases, data flow
- Docs/H3/Contracts/H3Extractor.md        Sections 4-5
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md     Section 12.4: execution pseudocode
"""

from __future__ import annotations

from collections import defaultdict
from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from ..attention.kernel import AttentionKernel
from ..constants.horizons import HORIZON_FRAMES
from ..constants.laws import LAW_MEMORY, LAW_PREDICTION, LAW_INTEGRATION
from ..morphology.batch import batch_morph
from ..morphology.scaling import normalize_morph


class H3Executor:
    """Seven-phase execution loop for the H3 temporal morphology layer.

    The executor is stateless with respect to audio data -- all temporal
    context comes from the R3 tensor and the attention window.  Internal
    helper objects (kernel) are lightweight and carry no learnable
    parameters.

    This implementation uses vectorized batch computation: for each
    (horizon, r3_idx, law) group, all steady-state frames are extracted
    via ``unfold`` and all morphs are computed in a single tensor
    operation per morph index.

    Usage
    -----
    ::

        executor = H3Executor()
        results = executor.execute(r3_tensor, demand_tree)
        # results: Dict[(r3_idx, horizon, morph, law)] -> Tensor(B, T)
    """

    def __init__(self) -> None:
        self._kernel = AttentionKernel()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def execute(
        self,
        r3_tensor: Tensor,
        demand_tree: Dict[int, Set[Tuple[int, int, int]]],
    ) -> Dict[Tuple[int, int, int, int], Tensor]:
        """Execute the 7-phase H3 pipeline over all demanded tuples.

        Parameters
        ----------
        r3_tensor : Tensor
            Shape ``(B, T, 97)`` -- batch of R3 spectral feature sequences.
            Values are assumed to be in ``[0, 1]``.
        demand_tree : dict
            Pre-built demand tree mapping each horizon index to a set of
            ``(r3_idx, morph, law)`` 3-tuples.  Typically produced by
            ``DemandTree.build()``.

        Returns
        -------
        Dict[Tuple[int, int, int, int], Tensor]
            Sparse dictionary mapping each demanded 4-tuple
            ``(r3_idx, horizon, morph, law)`` to a ``(B, T)`` tensor
            with values in ``[0, 1]``.

        Notes
        -----
        - An empty *demand_tree* returns an empty dict immediately.
        - For each horizon, attention weights are computed once and reused
          across all tuples at that horizon.
        - Steady-state frames (full-size windows) are computed in batch
          via ``unfold``.  Boundary frames (truncated windows at sequence
          edges) are left as zero -- these correspond to warm-up regions
          where morph values have reduced reliability.
        """
        # Phase 1 & 2: demand collection / tree ready (inputs)
        if not demand_tree:
            return {}

        B, T, _D = r3_tensor.shape
        device = r3_tensor.device
        dtype = r3_tensor.dtype

        results: Dict[Tuple[int, int, int, int], Tensor] = {}

        # Phase 3: horizon loop -- iterate sorted horizons
        for h_idx in sorted(demand_tree.keys()):
            tuples_at_horizon = demand_tree[h_idx]

            # Clamp to sequence length so windows never exceed available data
            n_frames = min(HORIZON_FRAMES[h_idx], T)

            # Phase 5 (partial): compute kernel weights once per horizon.
            weights = self._kernel.compute_weights(n_frames, device=device)
            w_normed = weights / weights.sum().clamp(min=1e-8)  # (n_frames,)

            # Group tuples by (r3_idx, law) to reuse window slices.
            grouped = self._group_by_r3_law(tuples_at_horizon)

            # Number of steady-state frames: T - n_frames + 1
            n_steady = max(0, T - n_frames + 1)

            for (r3_idx, law_idx), morph_indices in grouped.items():
                # Extract the scalar R3 feature series for this r3_idx
                r3_series = r3_tensor[:, :, r3_idx]  # (B, T)

                # Allocate output tensors for each morph (initialized to 0)
                morph_results: Dict[int, Tensor] = {
                    m: torch.zeros(B, T, device=device, dtype=dtype)
                    for m in morph_indices
                }

                if n_steady <= 0:
                    # Horizon >= T: compute single value over full sequence
                    # and broadcast to all frames.
                    full_window = r3_series.unsqueeze(1)  # (B, 1, T)
                    full_w = self._kernel.compute_weights(T, device=device)
                    full_w_normed = full_w / full_w.sum().clamp(min=1e-8)

                    for morph_idx in morph_indices:
                        raw = batch_morph(
                            full_window, full_w_normed, morph_idx
                        )  # (B, 1)
                        normed = normalize_morph(raw, morph_idx)  # (B, 1)
                        morph_results[morph_idx][:, :] = normed.expand(B, T)

                    for morph_idx in morph_indices:
                        key = (r3_idx, h_idx, morph_idx, law_idx)
                        results[key] = morph_results[morph_idx]
                    continue

                # ── Vectorized steady-state computation ──────────────

                # Phase 4: extract all full-size windows via unfold.
                # unfold gives (B, n_steady, n_frames) where
                # windows[:, i, :] = r3_series[:, i:i+n_frames]
                windows = r3_series.unfold(1, n_frames, 1)

                # Compute the output offset based on law:
                # L0 Memory:      steady frames t = n-1 .. T-1, offset = n-1
                # L1 Prediction:  steady frames t = 0   .. T-n, offset = 0
                # L2 Integration: steady frames t = half .. T-n+half, offset=half
                if law_idx == LAW_MEMORY:
                    offset = n_frames - 1
                elif law_idx == LAW_PREDICTION:
                    offset = 0
                else:  # LAW_INTEGRATION
                    offset = n_frames // 2

                # Phase 6 & 7: batch morph dispatch + normalize
                for morph_idx in morph_indices:
                    raw = batch_morph(windows, w_normed, morph_idx)
                    # raw: (B, n_steady)
                    normed = normalize_morph(raw, morph_idx)
                    # Place into full output at the right offset
                    end = offset + n_steady
                    morph_results[morph_idx][:, offset:end] = normed

                # Pack into results dict
                for morph_idx in morph_indices:
                    key = (r3_idx, h_idx, morph_idx, law_idx)
                    results[key] = morph_results[morph_idx]

        return results

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _group_by_r3_law(
        tuples: Set[Tuple[int, int, int]],
    ) -> Dict[Tuple[int, int], set]:
        """Group (r3_idx, morph, law) 3-tuples by (r3_idx, law).

        Returns a dict mapping ``(r3_idx, law)`` to a set of morph indices.
        This enables reusing the same R3 feature slice and window selection
        across multiple morphs, which is the dominant cost reduction in the
        inner loop.
        """
        grouped: Dict[Tuple[int, int], set] = defaultdict(set)
        for r3_idx, morph_idx, law_idx in tuples:
            grouped[(r3_idx, law_idx)].add(morph_idx)
        return dict(grouped)
