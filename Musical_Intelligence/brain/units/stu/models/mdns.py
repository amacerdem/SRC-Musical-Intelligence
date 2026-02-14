"""MDNS -- Melody Decoding from Neural Signals.

Unit: STU | Tier: alpha | Output: 11D
Mechanisms: BEP, TMH
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Optional, Tuple

import torch

from .....contracts.bases.base_model import BaseModel
from .....contracts.dataclasses import (
    BrainRegion,
    Citation,
    H3DemandSpec,
    LayerSpec,
    ModelMetadata,
)

if TYPE_CHECKING:
    from torch import Tensor


class MDNS(BaseModel):
    """Melody Decoding from Neural Signals.

    STU-alpha | 11D | Mechanisms: BEP, TMH
    """

    NAME = "MDNS"
    FULL_NAME = "Melody Decoding from Neural Signals"
    UNIT = "STU"
    TIER = "alpha"
    OUTPUT_DIM = 11
    MECHANISM_NAMES: Tuple[str, ...] = ("BEP", "TMH",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("mdns_e0", "mdns_e1", "mdns_e2",)),
        LayerSpec("M", "Mechanism", 3, 6, ("mdns_m0", "mdns_m1", "mdns_m2",)),
        LayerSpec("P", "Psychological", 6, 9, ("mdns_p0", "mdns_p1", "mdns_p2",)),
        LayerSpec("F", "Forecast", 9, 11, ("mdns_f0", "mdns_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(9, "rms_energy", 6, "200ms", 0, "value", 2, "integration", "MDNS temporal", "Melody Decoding from Neural Signals"),
            H3DemandSpec(9, "rms_energy", 9, "400ms", 0, "value", 2, "integration", "MDNS temporal", "Melody Decoding from Neural Signals"),
            H3DemandSpec(10, "onset_strength", 6, "200ms", 0, "value", 2, "integration", "MDNS temporal", "Melody Decoding from Neural Signals"),
            H3DemandSpec(10, "onset_strength", 9, "400ms", 0, "value", 2, "integration", "MDNS temporal", "Melody Decoding from Neural Signals"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("mdns_e0", "mdns_e1", "mdns_e2", "mdns_m0", "mdns_m1", "mdns_m2", "mdns_p0", "mdns_p1", "mdns_p2", "mdns_f0", "mdns_f1",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Supplementary Motor Area", "SMA", "bilateral", (0, -4, 56), 6, "Motor planning"),
            BrainRegion("Premotor Cortex", "PMC", "bilateral", (-44, -4, 48), 6, "Motor preparation"),
            BrainRegion("Cerebellum", "Cb", "bilateral", (0, -64, -28), None, "Timing coordination"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Melody Decoding from Neural Signals primary evidence", ""),
            ),
            evidence_tier="alpha",
            confidence_range=(0.9, 0.95),
            falsification_criteria=(
                "Melody Decoding from Neural Signals predictions must correlate with neural data",
            ),
            version="1.0.0",
        )

    def compute(
        self,
        mechanism_outputs: Dict[str, "Tensor"],
        h3_features: Dict[Tuple[int, int, int, int], "Tensor"],
        r3_features: "Tensor",
        cross_unit_inputs: Optional[Dict[str, "Tensor"]] = None,
    ) -> "Tensor":
        B, T, _ = r3_features.shape
        device = r3_features.device

        # Gather mechanism features
        parts = []
        for name in self.MECHANISM_NAMES:
            parts.append(
                mechanism_outputs.get(name, torch.zeros(B, T, 30, device=device))
            )
        mech = torch.cat(parts, dim=-1)
        total_m = mech.shape[-1]

        # Project mechanism + R3 to output dims
        out = torch.zeros(B, T, self.OUTPUT_DIM, device=device)
        for i in range(self.OUTPUT_DIM):
            ms = (i * total_m) // self.OUTPUT_DIM
            me = ((i + 1) * total_m) // self.OUTPUT_DIM
            m_val = mech[..., ms:me].mean(dim=-1)
            r3_val = r3_features[..., i % r3_features.shape[-1]]
            out[..., i] = torch.sigmoid(0.7 * m_val + 0.3 * r3_val)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
