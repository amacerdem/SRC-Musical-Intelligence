"""MEM -- Memory Encoding / Retrieval."""
from __future__ import annotations

from typing import Dict, List, Set, Tuple

import torch
from torch import Tensor

from ...contracts.bases.base_mechanism import BaseMechanism


class MEM(BaseMechanism):
    """Memory Encoding / Retrieval.

    Processes memory encoding and retrieval features across four horizons
    (H18, H20, H22, H25). Primary R3 domain is Consonance [0:7], with
    secondary domains Energy [7:12], Timbre [12:21], Change [21:25], and
    Interactions [25:49].

    Because there are 4 horizons, the last sub-section groups H22 and H25
    together: H18 -> [0:10], H20 -> [10:20], H22+H25 -> [20:30].
    """

    NAME = "MEM"
    FULL_NAME = "Memory Encoding / Retrieval"
    OUTPUT_DIM = 30
    HORIZONS = (18, 20, 22, 25)

    # R3 index domains
    _PRIMARY_R3 = tuple(range(0, 7))       # A domain: Consonance
    _SECONDARY_R3 = tuple(range(7, 12))    # B domain: Energy
    _TERTIARY_R3 = tuple(range(12, 21))    # C domain: Timbre
    _QUATERNARY_R3 = tuple(range(21, 25))  # D domain: Change
    _QUINARY_R3 = tuple(range(25, 49))     # E domain: Interactions

    # Per-horizon morph sets
    _MORPH_PROFILE: Dict[int, Tuple[int, ...]] = {
        18: (0, 1, 2, 3, 4, 5, 18, 20),
        20: (0, 1, 2, 3, 5, 18, 20),
        22: (0, 1, 2, 18, 20),
        25: (0, 1, 18, 20),
    }

    # Temporal laws
    _LAWS = (0, 1, 2)

    # Sub-section horizon mapping: H18, H20, H22+H25
    _SUBSECTIONS: Tuple[Tuple[int, ...], ...] = (
        (18,),      # dims 0-9
        (20,),      # dims 10-19
        (22, 25),   # dims 20-29  (two horizons grouped)
    )

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        demand: Set[Tuple[int, int, int, int]] = set()
        all_r3 = (
            self._PRIMARY_R3
            + self._SECONDARY_R3
            + self._TERTIARY_R3
            + self._QUATERNARY_R3
            + self._QUINARY_R3
        )
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

            if len(feats) < 10:
                for key in sorted(h3_features.keys()):
                    r3_idx, h, m, law = key
                    if h in horizons and r3_idx in self._QUATERNARY_R3:
                        feats.append(h3_features[key])
                        if len(feats) >= 10:
                            break

            if len(feats) < 10:
                for key in sorted(h3_features.keys()):
                    r3_idx, h, m, law = key
                    if h in horizons and r3_idx in self._QUINARY_R3:
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
            return torch.nn.functional.adaptive_avg_pool1d(stacked, 10)
        else:
            pad = torch.zeros(B, T, 10 - K, device=device)
            return torch.cat([stacked, pad], dim=-1)
