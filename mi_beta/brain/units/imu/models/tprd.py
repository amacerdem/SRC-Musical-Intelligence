"""
TPRD -- Tonotopy-Pitch Representation Density.

Beta-8 model of the IMU.  Models how primary regions within Heschl's gyri
exhibit more tuning to spectral content (tonotopy), whereas surrounding areas
exhibit more tuning to pitch (fundamental frequency), revealing distinct
representations of tonotopy and pitch in auditory cortex.

Output: 10D per frame (172.27 Hz).
Mechanisms: PPC (Pitch Processing Circuit).
Evidence: Moerel 2012, Formisano 2003.
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


class TPRD(BaseModel):
    """Tonotopy-Pitch Representation Density -- dual pitch encoding."""

    NAME = "TPRD"
    FULL_NAME = "Tonotopy-Pitch Representation Density"
    UNIT = "IMU"
    TIER = "beta"
    OUTPUT_DIM = 10
    MECHANISM_NAMES = ("PPC",)
    CROSS_UNIT_READS = ()

    LAYERS = (
        LayerSpec("E", "Explicit Features", 0, 2, (
            "f01_tonotopic_tuning", "f02_pitch_tuning",
        )),
        LayerSpec("M", "Mathematical Model", 2, 4, (
            "tonotopy_pitch_dissociation", "representation_density",
        )),
        LayerSpec("P", "Present Processing", 4, 7, (
            "spectral_encoding", "f0_extraction", "harmonic_template",
        )),
        LayerSpec("F", "Future Predictions", 7, 10, (
            "pitch_stability_pred", "tonotopic_shift_pred", "octave_equiv_pred",
        )),
    )

    @property
    def h3_demand(self) -> Tuple:
        return ()

    @property
    def dimension_names(self) -> Tuple[str, ...]:
        return (
            "f01_tonotopic_tuning", "f02_pitch_tuning",
            "tonotopy_pitch_dissociation", "representation_density",
            "spectral_encoding", "f0_extraction", "harmonic_template",
            "pitch_stability_pred", "tonotopic_shift_pred", "octave_equiv_pred",
        )

    @property
    def brain_regions(self) -> Tuple[BrainRegion, ...]:
        return (
            BrainRegion(
                name="Heschl's Gyrus (medial)",
                abbreviation="mHG",
                hemisphere="bilateral",
                mni_coords=(44, -20, 6),
                function="Tonotopic spectral content encoding",
                evidence_count=3,
            ),
            BrainRegion(
                name="Heschl's Gyrus (lateral)",
                abbreviation="lHG",
                hemisphere="bilateral",
                mni_coords=(52, -14, 4),
                function="Pitch (fundamental frequency) representation",
                evidence_count=3,
            ),
        )

    @property
    def metadata(self) -> ModelMetadata:
        return ModelMetadata(
            citations=(
                Citation("Moerel", 2012,
                         "Tonotopy vs pitch maps in human auditory cortex", ""),
                Citation("Formisano", 2003,
                         "Tonotopic organization of human auditory cortex", ""),
            ),
            evidence_tier="beta",
            confidence_range=(0.70, 0.85),
            falsification_criteria=(
                "Medial HG must show tonotopy while lateral areas show pitch tuning",
                "Missing fundamental stimuli must dissociate the two maps",
            ),
            version="2.0.0",
            paper_count=4,
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
