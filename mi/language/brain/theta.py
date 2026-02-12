"""
θ (Theta) — Narrative (16D)

Level 8: Sentence-level linguistic structure for generating natural
language descriptions of musical moments.

Subject (4D) — WHICH aspect dominates:
  θ0: reward_salience — reward/pleasure dominates     [Salimpoor 2011]
  θ1: tension_salience — tension/conflict dominates   [Huron 2006]
  θ2: motion_salience — movement/energy dominates     [Yang 2025]
  θ3: beauty_salience — beauty/harmony dominates      [Blood & Zatorre 2001]

Predicate (4D) — WHAT is happening:
  θ4: rising — the subject is increasing              [Schubert 2004]
  θ5: peaking — the subject is at climax              [Sloboda 1991]
  θ6: falling — the subject is decreasing             [Schubert 2004]
  θ7: stable — the subject is holding steady          [Meyer 1956]

Modifier (4D) — HOW it is happening:
  θ8: intensity — how strongly                        [Gabrielsson 2001]
  θ9: certainty — how confidently                     [Friston 2010]
  θ10: novelty — how surprisingly                     [Berlyne 1971]
  θ11: speed — how quickly                            [Fong 2020]

Connector (4D) — TEMPORAL relation:
  θ12: continuing — same thread continues             [Halliday & Hasan 1976]
  θ13: contrasting — opposing element introduced      [Almén 2008]
  θ14: resolving — tension/conflict resolves          [Huron 2006]
  θ15: transitioning — moving to new section          [Caplin 1998]
"""

from __future__ import annotations

from typing import List, Optional

import torch
from torch import Tensor

from ...core.base import BaseSemanticGroup
from ...core.types import SemanticGroupOutput


class ThetaGroup(BaseSemanticGroup):
    LEVEL = 8
    GROUP_NAME = "theta"
    DISPLAY_NAME = "θ"
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
        brain_output: object,
        *,
        epsilon_output: Optional[Tensor] = None,
        zeta_output: Optional[Tensor] = None,
        **kwargs,
    ) -> SemanticGroupOutput:
        """Compute θ group — narrative sentence structure.

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

        # ─── Subject (4D): WHICH aspect dominates ────────────
        pleasure = brain_output.get_dim("pleasure").unsqueeze(-1)
        tension = brain_output.get_dim("tension").unsqueeze(-1)
        arousal = brain_output.get_dim("arousal").unsqueeze(-1)
        beauty = brain_output.get_dim("beauty").unsqueeze(-1)

        subject_raw = torch.cat([pleasure, tension, arousal, beauty], dim=-1)
        subject = torch.softmax(subject_raw * 3.0, dim=-1)

        # ─── Predicate (4D): WHAT is happening ───────────────
        if epsilon_output is not None:
            pe_short = epsilon_output[..., 2:3]  # pe_short [0,1], center=0.5
        else:
            pe_short = half

        rising = (pe_short - 0.5).clamp(min=0) * 2.0
        falling = (0.5 - pe_short).clamp(min=0) * 2.0
        # Peaking: pleasure × arousal exceeds threshold
        peaking = (pleasure * arousal).clamp(0, 1)
        stable = (1.0 - (rising + falling + peaking)).clamp(min=0)

        predicate = torch.cat([rising, peaking, falling, stable], dim=-1)

        # ─── Modifier (4D): HOW it is happening ─────────────
        intensity = arousal

        if epsilon_output is not None:
            certainty = epsilon_output[..., 5:6]     # precision_short
            novelty_mod = epsilon_output[..., 0:1]   # surprise
        else:
            certainty = half
            novelty_mod = half

        pred_error = brain_output.get_dim("prediction_error")
        speed = torch.sigmoid(pred_error.abs() * 3.0).unsqueeze(-1)

        modifier = torch.cat([intensity, certainty, novelty_mod, speed], dim=-1)

        # ─── Connector (4D): TEMPORAL relation ───────────────
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
