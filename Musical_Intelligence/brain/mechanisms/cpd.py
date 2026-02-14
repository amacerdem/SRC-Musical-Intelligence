"""CPD -- Chills and Peak Detection."""
from __future__ import annotations

from typing import Dict, List, Set, Tuple

import torch
from torch import Tensor

from ...contracts.bases.base_mechanism import BaseMechanism


class CPD(BaseMechanism):
    """Chills and Peak Detection.

    Processes chills and peak-related features across three temporal horizons
    (H9, H16, H18). Primary R3 domain is Energy [7:12], secondary is
    Consonance [0:7], tertiary is Interactions [25:49].
    """

    NAME = "CPD"
    FULL_NAME = "Chills and Peak Detection"
    OUTPUT_DIM = 30
    HORIZONS = (9, 16, 18)

    # R3 index domains
    _PRIMARY_R3 = tuple(range(7, 12))     # B domain: Energy
    _SECONDARY_R3 = tuple(range(0, 7))    # A domain: Consonance
    _TERTIARY_R3 = tuple(range(25, 49))   # E domain: Interactions

    # Per-horizon morph sets
    _MORPH_PROFILE: Dict[int, Tuple[int, ...]] = {
        9:  (0, 1, 2, 8, 11),
        16: (0, 1, 2, 8, 11, 14),
        18: (0, 1, 2, 8, 14, 18),
    }

    # Temporal laws
    _LAWS = (0, 1, 2)

    # Sub-section horizon mapping
    _SUBSECTIONS: Tuple[Tuple[int, ...], ...] = (
        (9,),    # dims 0-9
        (16,),   # dims 10-19
        (18,),   # dims 20-29
    )

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        demand: Set[Tuple[int, int, int, int]] = set()
        all_r3 = self._PRIMARY_R3 + self._SECONDARY_R3 + self._TERTIARY_R3
        for r3_idx in all_r3:
            for horizon, morphs in self._MORPH_PROFILE.items():
                for morph in morphs:
                    for law in self._LAWS:
                        demand.add((r3_idx, horizon, morph, law))
        return demand

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        B, T, _ = r3_features.shape
        device = r3_features.device
        sections: List[Tensor] = []

        for horizons in self._SUBSECTIONS:
            feats: List[Tensor] = []
            for key in sorted(h3_features.keys()):
                r3_idx, h, m, law = key
                if h in horizons and r3_idx in self._PRIMARY_R3:
                    feats.append(h3_features[key])

            if len(feats) < 10:
                for key in sorted(h3_features.keys()):
                    r3_idx, h, m, law = key
                    if h in horizons and r3_idx in self._SECONDARY_R3:
                        feats.append(h3_features[key])
                        if len(feats) >= 10:
                            break

            if len(feats) < 10:
                for key in sorted(h3_features.keys()):
                    r3_idx, h, m, law = key
                    if h in horizons and r3_idx in self._TERTIARY_R3:
                        feats.append(h3_features[key])
                        if len(feats) >= 10:
                            break

            section = self._aggregate_to_10d(feats, B, T, device)
            sections.append(section)

        output = torch.cat(sections, dim=-1)  # (B, T, 30)
        return output.clamp(0.0, 1.0)

    @staticmethod
    def _aggregate_to_10d(
        feats: List[Tensor], B: int, T: int, device: torch.device,
    ) -> Tensor:
        if not feats:
            return torch.zeros(B, T, 10, device=device)
        stacked = torch.stack(feats, dim=-1)  # (B, T, K)
        K = stacked.shape[-1]
        if K == 10:
            return stacked
        elif K > 10:
            return torch.nn.functional.adaptive_avg_pool1d(
                stacked.transpose(1, 2), 10,
            ).transpose(1, 2)
        else:
            pad = torch.zeros(B, T, 10 - K, device=device)
            return torch.cat([stacked, pad], dim=-1)
