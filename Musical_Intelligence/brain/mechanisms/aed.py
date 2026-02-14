"""AED -- Affective Entrainment Dynamics."""
from __future__ import annotations

from typing import Dict, List, Set, Tuple

import torch
from torch import Tensor

from ...contracts.bases.base_mechanism import BaseMechanism


class AED(BaseMechanism):
    """Affective Entrainment Dynamics.

    Processes affective entrainment features across two horizons (H6, H16).
    Primary R3 domain is Energy [7:12], secondary is Consonance [0:7],
    tertiary is Change [21:25].

    Because there are only 2 horizons, the third sub-section (dims 20-29) is
    a cross-horizon interaction that combines features from both H6 and H16.
    """

    NAME = "AED"
    FULL_NAME = "Affective Entrainment Dynamics"
    OUTPUT_DIM = 30
    HORIZONS = (6, 16)

    # R3 index domains
    _PRIMARY_R3 = tuple(range(7, 12))     # B domain: Energy
    _SECONDARY_R3 = tuple(range(0, 7))    # A domain: Consonance
    _TERTIARY_R3 = tuple(range(21, 25))   # D domain: Change

    # Per-horizon morph sets
    _MORPH_PROFILE: Dict[int, Tuple[int, ...]] = {
        6:  (0, 1, 2, 8, 19),
        16: (0, 1, 2, 8, 18, 19),
    }

    # Temporal laws
    _LAWS = (0, 1, 2)

    # Sub-section horizon mapping:
    #   H6 -> [0:10], H16 -> [10:20], combined H6+H16 -> [20:30]
    _SUBSECTIONS: Tuple[Tuple[int, ...], ...] = (
        (6,),       # dims 0-9
        (16,),      # dims 10-19
        (6, 16),    # dims 20-29  (cross-horizon interaction)
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
            return torch.nn.functional.adaptive_avg_pool1d(stacked, 10)
        else:
            pad = torch.zeros(B, T, 10 - K, device=device)
            return torch.cat([stacked, pad], dim=-1)
