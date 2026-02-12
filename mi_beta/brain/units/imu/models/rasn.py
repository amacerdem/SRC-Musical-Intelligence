"""
RASN -- Rhythmic Auditory Stimulation Network.

Beta-1 model of the IMU.  Models how rhythmic auditory stimulation (RAS)
promotes neuroplasticity through entrainment of neural oscillations and
facilitation of sensorimotor integration.  Strong clinical evidence from
rehabilitation studies.

Output: 11D per frame (172.27 Hz).
Mechanisms: BEP (Beat Entrainment Processing),
            MEM (Memory Encoding & Retrieval).
Evidence: Thaut 2015, Schaefer 2014.
"""

from __future__ import annotations

from typing import Dict, Optional, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import (
    BaseModel,
    BrainRegion,
    Citation,
    LayerSpec,
    ModelMetadata,
)


class RASN(BaseModel):
    """Rhythmic Auditory Stimulation Network -- rhythm-driven neuroplasticity."""

    NAME = "RASN"
    FULL_NAME = "Rhythmic Auditory Stimulation Network"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 11
    MECHANISM_NAMES = ("BEP", "MEM")
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_entrainment_efficacy", "f02_neuroplasticity_index",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "ras_coupling", "plasticity_dose_response",
        )),
        LayerSpec("P", "Present Processing", 4, 8, (
            "oscillatory_entrainment", "sensorimotor_integration",
            "rehabilitation_state", "temporal_coherence",
        )),
        LayerSpec("F", "Future Predictions", 8, 11, (
            "plasticity_forecast", "motor_recovery_pred", "entrainment_stability",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_entrainment_efficacy", "f02_neuroplasticity_index",
            "ras_coupling", "plasticity_dose_response",
            "oscillatory_entrainment", "sensorimotor_integration",
            "rehabilitation_state", "temporal_coherence",
            "plasticity_forecast", "motor_recovery_pred", "entrainment_stability",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Supplementary Motor Area",
                abbreviation="SMA",
                hemisphere="bilateral",
                mni_coords=(0, -6, 62),
                function="Rhythmic entrainment driving motor rehabilitation",
                evidence_count=3,
            ),
            BrainRegion(
                name="Premotor Cortex",
                abbreviation="PMC",
                hemisphere="bilateral",
                mni_coords=(-46, 0, 50),
                function="Auditory-motor coupling for rhythm-based therapy",
                evidence_count=3,
            ),
            BrainRegion(
                name="Cerebellum",
                abbreviation="CB",
                hemisphere="bilateral",
                mni_coords=(20, -62, -26),
                function="Temporal prediction and sensorimotor plasticity",
                evidence_count=2,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Thaut", 2015,
                         "Rhythmic auditory stimulation in neurological rehabilitation",
                         ""),
                Citation("Schaefer", 2014,
                         "Music-driven brain plasticity in rehabilitation", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.75, 0.88),
            falsification_criteria=(
                "RAS must enhance motor recovery beyond passive listening",
                "Temporal entrainment must precede functional improvement",
            ),
            version="2.0.0",
            paper_count=5,
        )

    def compute(
        self,
        mechanism_outputs: Dict[str, Tensor],
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
        cross_unit_inputs: Optional[Dict[str, Tensor]] = None,
    ) -> Tensor:
        """Stub -- returns zeros of correct shape."""
        B, T = r3_features.shape[:2]
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
