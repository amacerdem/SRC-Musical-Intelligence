"""H3Densifier -- Converts between sparse H3 dict and dense tensor.

The H3Extractor produces a sparse dict: ``{(r3_idx, horizon, morph, law): (B, T)}``
The H3 auxiliary head needs a dense tensor: ``(B, T, N)`` where N ~ 5210.

This module provides bidirectional conversion using the canonical ordering
established by ``H3DemandCollector``.

Usage::

    from Musical_Intelligence.training.teacher.h3_demand_collector import H3DemandCollector
    from Musical_Intelligence.data.h3_densifier import H3Densifier

    collector = H3DemandCollector()
    densifier = H3Densifier(collector.demand_list, collector.index_map)

    dense = densifier.densify(h3_output)     # H3Output → (B, T, N)
    sparse = densifier.sparsify(dense)       # (B, T, N) → Dict
"""
from __future__ import annotations

from typing import Dict, List, Tuple

import torch
from torch import Tensor


class H3Densifier:
    """Bidirectional converter between sparse H3 and dense tensor.

    The canonical ordering is provided by ``H3DemandCollector``: each
    4-tuple ``(r3_idx, horizon, morph, law)`` maps to a fixed index in
    the dense dimension.

    Attributes:
        demand_list: Sorted list of 4-tuples (canonical order).
        index_map:   Maps each 4-tuple to its dense index.
        n_demands:   Total number of demands (dense dimension).
    """

    def __init__(
        self,
        demand_list: List[Tuple[int, int, int, int]],
        index_map: Dict[Tuple[int, int, int, int], int],
    ) -> None:
        self._demand_list = demand_list
        self._index_map = index_map
        self._n_demands = len(demand_list)

    @property
    def n_demands(self) -> int:
        """Dense dimension size."""
        return self._n_demands

    # ------------------------------------------------------------------
    # Sparse → Dense
    # ------------------------------------------------------------------

    def densify(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
    ) -> Tensor:
        """Convert sparse H3 dict to dense ``(B, T, N)`` tensor.

        Parameters
        ----------
        h3_features : dict
            Sparse H3 output: ``{(r3_idx, horizon, morph, law): (B, T)}``.

        Returns
        -------
        Tensor
            Dense tensor of shape ``(B, T, N)`` where ``N = n_demands``.
            Missing demands are filled with zeros.
        """
        # Determine B, T from any available tensor
        sample = next(iter(h3_features.values()))
        B, T = sample.shape
        device = sample.device
        dtype = sample.dtype

        dense = torch.zeros(B, T, self._n_demands, device=device, dtype=dtype)

        for key, tensor in h3_features.items():
            if key in self._index_map:
                idx = self._index_map[key]
                dense[:, :, idx] = tensor

        return dense

    # ------------------------------------------------------------------
    # Dense → Sparse
    # ------------------------------------------------------------------

    def sparsify(
        self,
        dense: Tensor,
    ) -> Dict[Tuple[int, int, int, int], Tensor]:
        """Convert dense ``(B, T, N)`` tensor back to sparse H3 dict.

        Parameters
        ----------
        dense : Tensor
            Dense tensor of shape ``(B, T, N)``.

        Returns
        -------
        dict
            Sparse dict: ``{(r3_idx, horizon, morph, law): (B, T)}``.
        """
        result: Dict[Tuple[int, int, int, int], Tensor] = {}
        for key, idx in self._index_map.items():
            result[key] = dense[:, :, idx]
        return result

    # ------------------------------------------------------------------
    # Repr
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return f"H3Densifier(n_demands={self._n_demands})"
