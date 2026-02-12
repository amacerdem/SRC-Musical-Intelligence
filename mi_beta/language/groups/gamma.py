"""
gamma (Gamma) -- Psychology Semantics (13D)

Level 3: WHAT it means subjectively.
Maps Brain outputs to psychological constructs.

Reward (3D):
  gamma0: reward_intensity -- overall reward signal strength     [Salimpoor 2011]
  gamma1: reward_type -- wanting-dominant vs liking-dominant     [Berridge 2003]
  gamma2: reward_phase -- anticipation vs consummation           [Salimpoor 2011]

ITPRA (2D):
  gamma3: itpra_tension_resolution -- tension -> resolution arc  [Huron 2006]
  gamma4: itpra_surprise_evaluation -- surprise -> appraisal     [Huron 2006]

Aesthetics (3D):
  gamma5: beauty -- opioid-mediated hedonic pleasure             [Blood & Zatorre 2001]
  gamma6: sublime -- awe, overwhelm, transcendence               [Konecni 2005]
  gamma7: groove -- motor-harmonic coupling pleasure              [Janata 2012]

Emotion (2D):
  gamma8: valence -- positive/negative affective state            [Russell 1980]
  gamma9: arousal -- activation level                             [Yang 2025]

Chills (3D):
  gamma10: chill_probability -- ANS chill signature              [de Fleurian & Pearce 2021]
  gamma11: chill_intensity -- integrated chill strength          [Sloboda 1991, Guhn 2007]
  gamma12: chill_phase -- buildup/peak/afterglow                 [Grewe 2009]

In mi_beta, these dimensions are computed from whatever models are active.
Missing signals default to 0.5 (neutral).
"""

from __future__ import annotations

from typing import Any, List

import torch
from torch import Tensor

from ...contracts.base_semantic_group import BaseSemanticGroup, SemanticGroupOutput
from ...core.types import BrainOutput


def _safe_get_dim(brain_output: BrainOutput, name: str, default: float = 0.5) -> Tensor:
    """Safely extract a named dimension, returning default if not found."""
    try:
        return brain_output.get_dim(name)
    except (ValueError, KeyError):
        B, T, _ = brain_output.tensor.shape
        return torch.full(
            (B, T), default,
            device=brain_output.tensor.device,
            dtype=brain_output.tensor.dtype,
        )


class GammaGroup(BaseSemanticGroup):
    LEVEL = 3
    GROUP_NAME = "gamma"
    DISPLAY_NAME = "gamma"
    OUTPUT_DIM = 13

    @property
    def dimension_names(self) -> List[str]:
        return [
            "reward_intensity", "reward_type", "reward_phase",
            "itpra_tension_resolution", "itpra_surprise_evaluation",
            "beauty", "sublime", "groove",
            "valence", "arousal",
            "chill_probability", "chill_intensity", "chill_phase",
        ]

    def compute(self, brain_output: Any, **kwargs: Any) -> SemanticGroupOutput:
        """Compute gamma group from BrainOutput (variable D).

        Uses _safe_get_dim to gracefully handle missing dimensions.
        """
        # Reward (3D)
        pleasure = _safe_get_dim(brain_output, "pleasure")
        wanting = _safe_get_dim(brain_output, "wanting")
        liking = _safe_get_dim(brain_output, "liking")
        da_caudate = _safe_get_dim(brain_output, "da_caudate")
        da_nacc = _safe_get_dim(brain_output, "da_nacc")

        reward_intensity = pleasure.unsqueeze(-1)
        reward_type = ((liking - wanting) * 0.5 + 0.5).unsqueeze(-1)
        reward_phase = ((da_nacc - da_caudate) * 0.5 + 0.5).unsqueeze(-1)

        # ITPRA (2D)
        tension = _safe_get_dim(brain_output, "tension")
        harmonic_ctx = _safe_get_dim(brain_output, "harmonic_context")
        pred_error = _safe_get_dim(brain_output, "prediction_error", default=0.0)
        emotional_arc = _safe_get_dim(brain_output, "emotional_arc")

        itpra_tr = ((1.0 - tension) * harmonic_ctx).unsqueeze(-1)
        itpra_se = (pred_error.abs() * emotional_arc).unsqueeze(-1)

        # Aesthetics (3D)
        beauty_val = _safe_get_dim(brain_output, "beauty")
        arousal = _safe_get_dim(brain_output, "arousal")
        beauty_dim = beauty_val.unsqueeze(-1)
        sublime = (pleasure * arousal).unsqueeze(-1)
        groove = (arousal * harmonic_ctx).unsqueeze(-1)

        # Emotion (2D)
        valence = _safe_get_dim(brain_output, "valence")
        valence_dim = valence.unsqueeze(-1)
        arousal_dim = arousal.unsqueeze(-1)

        # Chills (3D)
        scr = _safe_get_dim(brain_output, "scr")
        hr = _safe_get_dim(brain_output, "hr")
        chills = _safe_get_dim(brain_output, "chills_intensity")

        chill_prob = (scr * (1.0 - hr)).unsqueeze(-1)
        chill_intensity = chills.unsqueeze(-1)
        chill_phase = torch.sigmoid(chills - tension).unsqueeze(-1)

        tensor = torch.cat([
            reward_intensity, reward_type, reward_phase,
            itpra_tr, itpra_se,
            beauty_dim, sublime, groove,
            valence_dim, arousal_dim,
            chill_prob, chill_intensity, chill_phase,
        ], dim=-1)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor.clamp(0, 1),
            dimension_names=tuple(self.dimension_names),
        )
