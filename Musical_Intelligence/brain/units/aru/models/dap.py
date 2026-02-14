"""DAP -- Developmental Affective Plasticity.

Unit: ARU | Tier: gamma | Output: 10D
Mechanisms: AED, CPD
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


class DAP(BaseModel):
    """Developmental Affective Plasticity.

    ARU-gamma | 10D | Mechanisms: AED, CPD
    """

    NAME = "DAP"
    FULL_NAME = "Developmental Affective Plasticity"
    UNIT = "ARU"
    TIER = "gamma"
    OUTPUT_DIM = 10
    MECHANISM_NAMES: Tuple[str, ...] = ("AED", "CPD",)
    CROSS_UNIT_READS: Tuple = ()
    LAYERS: Tuple[LayerSpec, ...] = (
        LayerSpec("E", "Extraction", 0, 3, ("dap_e0", "dap_e1", "dap_e2",)),
        LayerSpec("M", "Mechanism", 3, 5, ("dap_m0", "dap_m1",)),
        LayerSpec("P", "Psychological", 5, 8, ("dap_p0", "dap_p1", "dap_p2",)),
        LayerSpec("F", "Forecast", 8, 10, ("dap_f0", "dap_f1",)),
    )

    @property
    def h3_demand(self) -> Tuple[H3DemandSpec, ...]:
        return (
            H3DemandSpec(30, "x_30", 6, "200ms", 0, "value", 2, "integration", "DAP temporal", "Developmental Affective Plasticity"),
            H3DemandSpec(30, "x_30", 9, "400ms", 0, "value", 2, "integration", "DAP temporal", "Developmental Affective Plasticity"),
            H3DemandSpec(35, "x_35", 6, "200ms", 0, "value", 2, "integration", "DAP temporal", "Developmental Affective Plasticity"),
            H3DemandSpec(35, "x_35", 9, "400ms", 0, "value", 2, "integration", "DAP temporal", "Developmental Affective Plasticity"),
        )

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return ("dap_e0", "dap_e1", "dap_e2", "dap_m0", "dap_m1", "dap_p0", "dap_p1", "dap_p2", "dap_f0", "dap_f1",)

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion("Nucleus Accumbens", "NAcc", "bilateral", (10, 12, -8), None, "Reward processing"),
            BrainRegion("Ventral Tegmental Area", "VTA", "bilateral", (0, -16, -8), None, "Dopamine signaling"),
            BrainRegion("Ventromedial Prefrontal Cortex", "vmPFC", "bilateral", (0, 44, -12), 11, "Value computation"),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Author", 2020, "Developmental Affective Plasticity primary evidence", ""),
            ),
            evidence_tier="gamma",
            confidence_range=(0.5, 0.7),
            falsification_criteria=(
                "Developmental Affective Plasticity predictions must correlate with neural data",
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
            out[..., i] = torch.sigmoid(0.5 * m_val + 0.5 * r3_val)

        # H3 temporal modulation
        h3_mod = torch.ones(B, T, device=device)
        for spec in self.h3_demand:
            key = spec.as_tuple()
            if key in h3_features:
                h3_mod = h3_mod * (0.5 + 0.5 * h3_features[key])
        out = out * h3_mod.unsqueeze(-1)

        return out.clamp(0.0, 1.0)
