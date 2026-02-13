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
6. Morph dispatch      -- MorphComputer produces raw scalar per frame
7. Result packing      -- normalize and store as (B, T) tensors

For efficiency, tuples sharing (horizon, r3_idx, law) reuse the same
window slice.  This avoids redundant R3 indexing and window selection.

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
from ..attention.memory import MemoryWindow
from ..attention.prediction import PredictionWindow
from ..attention.integration import IntegrationWindow
from ..constants.horizons import HORIZON_FRAMES
from ..constants.laws import LAW_MEMORY, LAW_PREDICTION, LAW_INTEGRATION
from ..morphology.computer import MorphComputer
from ..morphology.scaling import normalize_morph


class H3Executor:
    """Seven-phase execution loop for the H3 temporal morphology layer.

    The executor is stateless with respect to audio data -- all temporal
    context comes from the R3 tensor and the attention window.  Internal
    helper objects (kernel, windows, morph computer) are lightweight and
    carry no learnable parameters.

    Usage
    -----
    ::

        executor = H3Executor()
        results = executor.execute(r3_tensor, demand_tree)
        # results: Dict[(r3_idx, horizon, morph, law)] -> Tensor(B, T)
    """

    def __init__(self) -> None:
        self._kernel = AttentionKernel()
        self._morph_computer = MorphComputer()

        # Law-to-window dispatcher
        self._windows = {
            LAW_MEMORY: MemoryWindow(),
            LAW_PREDICTION: PredictionWindow(),
            LAW_INTEGRATION: IntegrationWindow(),
        }

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
            Shape ``(B, T, 128)`` -- batch of R3 spectral feature sequences.
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
        - Windows that extend beyond sequence boundaries are truncated and
          attention weights are renormalized to sum to 1.
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
            # These are unnormalized; truncation + renorm happens per frame.
            weights = self._kernel.compute_weights(n_frames, device=device)

            # Group tuples by (r3_idx, law) to reuse window slices.
            # Within a group we iterate only over morph indices.
            grouped = self._group_by_r3_law(tuples_at_horizon)

            for (r3_idx, law_idx), morph_indices in grouped.items():
                # Extract the scalar R3 feature series for this r3_idx
                r3_series = r3_tensor[:, :, r3_idx]  # (B, T)

                # Select the window selector for this law
                window_selector = self._windows[law_idx]

                # Allocate output tensors for each morph in this group
                morph_results: Dict[int, Tensor] = {
                    m: torch.zeros(B, T, device=device, dtype=dtype)
                    for m in morph_indices
                }

                # Frame-by-frame loop (correctness first)
                for t in range(T):
                    # Phase 4: window selection by law
                    start, end = window_selector.select(t, n_frames, T)
                    win_len = end - start

                    if win_len <= 0:
                        # Degenerate: no frames in window -> leave as zero
                        continue

                    # Slice the R3 series for the window
                    window_slice = r3_series[:, start:end]  # (B, win_len)

                    # Phase 5: truncate attention weights and renormalize
                    w = weights[:win_len]
                    w_sum = w.sum().clamp(min=1e-8)
                    w_normed = w / w_sum  # (win_len,)

                    # Phase 6: morph dispatch for each morph in the group
                    for morph_idx in morph_indices:
                        raw = self._morph_computer.compute(
                            window_slice, w_normed, morph_idx
                        )  # (B,)

                        # Phase 7 (partial): apply normalize_morph -> [0, 1]
                        normed = normalize_morph(raw, morph_idx)  # (B,)

                        morph_results[morph_idx][:, t] = normed

                # Phase 7: pack into results dict
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
