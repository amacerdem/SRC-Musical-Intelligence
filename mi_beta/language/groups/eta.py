"""
eta (Eta) -- Vocabulary (12D)

Level 7: 64-gradation quantization of polarity axes into human-readable
semantic terms.

Each dimension corresponds to one zeta polarity axis, quantized to one of
64 discrete levels.  The tensor output is the normalized gradation index
(continuous [0, 1]), while the ``get_terms()`` method returns human-readable
labels.

64-Gradation System:
  - 8 intensity bands x 8 gradations per band = 64 levels
  - Step size: 1/64 ~= 1.56% -- matches human JND (~3%) threshold
  - 6 bits per axis -- total 72 bits for 12 axes

Scientific basis:
  - Prototype Theory (Rosch 1975)
  - Semantic Field Theory (Trier 1931, Lyons 1977)
  - JND Psychophysics (Weber 1834, Stevens 1957)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import torch
from torch import Tensor

from ...contracts.base_semantic_group import BaseSemanticGroup, SemanticGroupOutput


AXIS_NAMES: Tuple[str, ...] = (
    "valence", "arousal", "tension", "power",
    "wanting", "liking", "novelty", "complexity",
    "beauty", "groove", "stability", "engagement",
)

AXIS_TERMS: Dict[str, Tuple[str, ...]] = {
    "valence": (
        "devastating", "melancholic", "wistful", "subdued",
        "neutral", "content", "happy", "euphoric",
    ),
    "arousal": (
        "comatose", "lethargic", "drowsy", "calm",
        "neutral", "alert", "energized", "explosive",
    ),
    "tension": (
        "dissolved", "slack", "easy", "mild",
        "neutral", "taut", "strained", "crushing",
    ),
    "power": (
        "whisper", "fragile", "gentle", "moderate",
        "neutral", "strong", "forceful", "overwhelming",
    ),
    "wanting": (
        "fulfilled", "content", "settled", "mild",
        "neutral", "interested", "eager", "desperate",
    ),
    "liking": (
        "aversive", "unpleasant", "bland", "indifferent",
        "neutral", "pleasant", "delightful", "ecstatic",
    ),
    "novelty": (
        "habitual", "routine", "known", "expected",
        "neutral", "fresh", "surprising", "shocking",
    ),
    "complexity": (
        "trivial", "basic", "clear", "moderate",
        "neutral", "elaborate", "intricate", "labyrinthine",
    ),
    "beauty": (
        "harsh", "grating", "rough", "plain",
        "neutral", "pleasing", "beautiful", "sublime",
    ),
    "groove": (
        "mechanical", "stiff", "stilted", "measured",
        "neutral", "swinging", "grooving", "transcendent",
    ),
    "stability": (
        "turbulent", "erratic", "unsteady", "wavering",
        "neutral", "steady", "anchored", "immovable",
    ),
    "engagement": (
        "oblivious", "indifferent", "distracted", "aware",
        "neutral", "attentive", "immersed", "entranced",
    ),
}

N_GRADATIONS: int = 64
N_BANDS: int = 8
GRADATIONS_PER_BAND: int = N_GRADATIONS // N_BANDS  # 8


def polarity_to_gradation(value: Tensor) -> Tensor:
    """Convert polarity [-1, +1] to gradation index [0, 63]."""
    normalized = (value + 1.0) * 0.5
    return (normalized * (N_GRADATIONS - 1)).round().long().clamp(0, N_GRADATIONS - 1)


def gradation_to_band(grad_idx: Tensor) -> Tensor:
    """Convert gradation index [0, 63] to band index [0, 7]."""
    return (grad_idx // GRADATIONS_PER_BAND).clamp(0, N_BANDS - 1)


class EtaGroup(BaseSemanticGroup):
    LEVEL = 7
    GROUP_NAME = "eta"
    DISPLAY_NAME = "eta"
    OUTPUT_DIM = 12

    @property
    def dimension_names(self) -> List[str]:
        return [f"{name}_vocab" for name in AXIS_NAMES]

    def compute(
        self,
        brain_output: Any,
        *,
        zeta_output: Optional[Tensor] = None,
        **kwargs: Any,
    ) -> SemanticGroupOutput:
        """Compute eta group -- 64-gradation vocabulary quantization.

        Quantizes zeta polarity axes [-1,+1] -> 64 discrete levels -> [0,1].
        """
        if zeta_output is not None:
            normalized = (zeta_output + 1.0) * 0.5
            quantized = (normalized * (N_GRADATIONS - 1)).round().clamp(
                0, N_GRADATIONS - 1
            ) / (N_GRADATIONS - 1)
            tensor = quantized
        else:
            B, T, _ = brain_output.tensor.shape
            tensor = torch.full(
                (B, T, self.OUTPUT_DIM), 0.5,
                device=brain_output.tensor.device,
                dtype=brain_output.tensor.dtype,
            )

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor,
            dimension_names=tuple(self.dimension_names),
        )

    def get_terms(self, zeta_output: Tensor) -> List[List[Dict[str, object]]]:
        """Return human-readable vocabulary terms for each axis.

        Args:
            zeta_output: (B, T, 12) polarity values in [-1, +1]

        Returns:
            List of 12 lists (one per axis) of dicts with axis/band/term.
        """
        grad_indices = polarity_to_gradation(zeta_output)
        band_indices = gradation_to_band(grad_indices)
        B, T, _ = zeta_output.shape

        results: List[List[Dict[str, object]]] = []
        for ax_idx, ax_name in enumerate(AXIS_NAMES):
            terms = AXIS_TERMS[ax_name]
            ax_bands = band_indices[..., ax_idx]
            ax_results: List[Dict[str, object]] = []
            for b in range(B):
                for t_idx in range(T):
                    band_i = ax_bands[b, t_idx].item()
                    ax_results.append({
                        "axis": ax_name,
                        "band_index": band_i,
                        "term": terms[band_i],
                    })
            results.append(ax_results)
        return results
