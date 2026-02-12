"""
theta (Theta) -- Narrative (16D)

Level 8: Sentence-level linguistic structure for generating natural
language descriptions of musical moments.

Subject (4D) -- WHICH aspect dominates:
  theta0: reward_salience -- reward/pleasure dominates     [Salimpoor 2011]
  theta1: tension_salience -- tension/conflict dominates   [Huron 2006]
  theta2: motion_salience -- movement/energy dominates     [Yang 2025]
  theta3: beauty_salience -- beauty/harmony dominates      [Blood & Zatorre 2001]

Predicate (4D) -- WHAT is happening:
  theta4: rising -- the subject is increasing              [Schubert 2004]
  theta5: peaking -- the subject is at climax              [Sloboda 1991]
  theta6: falling -- the subject is decreasing             [Schubert 2004]
  theta7: stable -- the subject is holding steady          [Meyer 1956]

Modifier (4D) -- HOW it is happening:
  theta8: intensity -- how strongly                        [Gabrielsson 2001]
  theta9: certainty -- how confidently                     [Friston 2010]
  theta10: novelty -- how surprisingly                     [Berlyne 1971]
  theta11: speed -- how quickly                            [Fong 2020]

Connector (4D) -- TEMPORAL relation:
  theta12: continuing -- same thread continues             [Halliday & Hasan 1976]
  theta13: contrasting -- opposing element introduced      [Almen 2008]
  theta14: resolving -- tension/conflict resolves          [Huron 2006]
  theta15: transitioning -- moving to new section          [Caplin 1998]
"""

from __future__ import annotations

from typing import Any, List, Optional

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


class ThetaGroup(BaseSemanticGroup):
    LEVEL = 8
    GROUP_NAME = "theta"
    DISPLAY_NAME = "theta"
    OUTPUT_DIM = 16

    @property
    def dimension_names(self) -> List[str]:
        return [
            "reward_salience", "tension_salience",
            "motion_salience", "beauty_salience",
            "rising", "peaking", "falling", "stable",
            "intensity", "certainty", "novelty", "speed",
            "continuing", "contrasting", "resolving", "transitioning",
        ]

    def compute(
        self,
        brain_output: Any,
        *,
        epsilon_output: Optional[Tensor] = None,
        zeta_output: Optional[Tensor] = None,
        **kwargs: Any,
    ) -> SemanticGroupOutput:
        """Compute theta group -- narrative sentence structure.

        Subject: softmax competition between Brain pathways.
        Predicate: from epsilon prediction errors (temporal dynamics).
        Modifier: from Brain + epsilon signals.
        Connector: from zeta polarity (temporal relations).
        """
        B, T, _ = brain_output.tensor.shape
        device = brain_output.tensor.device
        dtype = brain_output.tensor.dtype
        one = torch.ones(B, T, 1, device=device, dtype=dtype)
        half = one * 0.5

        # Subject (4D): WHICH aspect dominates
        pleasure = _safe_get_dim(brain_output, "pleasure").unsqueeze(-1)
        tension = _safe_get_dim(brain_output, "tension").unsqueeze(-1)
        arousal = _safe_get_dim(brain_output, "arousal").unsqueeze(-1)
        beauty = _safe_get_dim(brain_output, "beauty").unsqueeze(-1)

        subject_raw = torch.cat([pleasure, tension, arousal, beauty], dim=-1)
        subject = torch.softmax(subject_raw * 3.0, dim=-1)

        # Predicate (4D): WHAT is happening
        if epsilon_output is not None:
            pe_short = epsilon_output[..., 2:3]  # pe_short [0,1], center=0.5
        else:
            pe_short = half

        rising = (pe_short - 0.5).clamp(min=0) * 2.0
        falling = (0.5 - pe_short).clamp(min=0) * 2.0
        peaking = (pleasure * arousal).clamp(0, 1)
        stable = (1.0 - (rising + falling + peaking)).clamp(min=0)

        predicate = torch.cat([rising, peaking, falling, stable], dim=-1)

        # Modifier (4D): HOW it is happening
        intensity = arousal

        if epsilon_output is not None:
            certainty = epsilon_output[..., 5:6]     # precision_short
            novelty_mod = epsilon_output[..., 0:1]   # surprise
        else:
            certainty = half
            novelty_mod = half

        pred_error = _safe_get_dim(brain_output, "prediction_error", default=0.0)
        speed = torch.sigmoid(pred_error.abs() * 3.0).unsqueeze(-1)

        modifier = torch.cat([intensity, certainty, novelty_mod, speed], dim=-1)

        # Connector (4D): TEMPORAL relation
        if zeta_output is not None:
            val_pol = zeta_output[..., 0:1]    # valence polarity [-1,+1]
            ten_pol = zeta_output[..., 2:3]    # tension polarity [-1,+1]
        else:
            val_pol = torch.zeros(B, T, 1, device=device, dtype=dtype)
            ten_pol = torch.zeros(B, T, 1, device=device, dtype=dtype)

        continuing = 1.0 / (1.0 + val_pol.abs() + ten_pol.abs())
        contrasting = (val_pol.abs() + ten_pol.abs()) * 0.5
        resolving = (-ten_pol).clamp(min=0)
        transitioning = (1.0 - (continuing + contrasting + resolving)).clamp(min=0)

        connector = torch.cat([
            continuing, contrasting, resolving, transitioning,
        ], dim=-1)

        tensor = torch.cat([subject, predicate, modifier, connector], dim=-1)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor.clamp(0, 1),
            dimension_names=tuple(self.dimension_names),
        )
