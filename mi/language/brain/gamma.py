"""
γ (Gamma) — Psychology Semantics (13D)

Level 3: WHAT it means subjectively.
Maps Brain dimensions to psychological constructs.

Reward (3D):
  γ0: reward_intensity — overall reward signal strength     [Salimpoor 2011]
  γ1: reward_type — wanting-dominant vs liking-dominant     [Berridge 2003]
  γ2: reward_phase — anticipation vs consummation           [Salimpoor 2011]

ITPRA (2D):
  γ3: itpra_tension_resolution — tension→resolution arc     [Huron 2006]
  γ4: itpra_surprise_evaluation — surprise→appraisal arc    [Huron 2006]

Aesthetics (3D):
  γ5: beauty — opioid-mediated hedonic pleasure             [Blood & Zatorre 2001]
  γ6: sublime — awe, overwhelm, transcendence               [Konečni 2005]
  γ7: groove — motor-harmonic coupling pleasure              [Janata 2012]

Emotion (2D):
  γ8: valence — positive/negative affective state            [Russell 1980]
  γ9: arousal — activation level                             [Yang 2025]

Chills (3D):
  γ10: chill_probability — ANS chill signature               [de Fleurian & Pearce 2021]
  γ11: chill_intensity — integrated chill strength           [Sloboda 1991, Guhn 2007]
  γ12: chill_phase — buildup/peak/afterglow                  [Grewe 2009]
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ...core.base import BaseSemanticGroup
from ...core.types import SemanticGroupOutput


class GammaGroup(BaseSemanticGroup):
    LEVEL = 3
    GROUP_NAME = "gamma"
    DISPLAY_NAME = "γ"
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

    def compute(self, brain_output: object, **kwargs) -> SemanticGroupOutput:
        """Compute γ group from BrainOutput (26D).

        Brain provides DIRECT access to reward, affect, and autonomic signals
        that were previously scattered across SRP + mechanisms.
        """
        # ─── Reward (3D) ────────────────────────────────────
        pleasure = brain_output.get_dim("pleasure")
        wanting = brain_output.get_dim("wanting")
        liking = brain_output.get_dim("liking")
        da_caudate = brain_output.get_dim("da_caudate")
        da_nacc = brain_output.get_dim("da_nacc")

        reward_intensity = pleasure.unsqueeze(-1)
        reward_type = ((liking - wanting) * 0.5 + 0.5).unsqueeze(-1)
        reward_phase = ((da_nacc - da_caudate) * 0.5 + 0.5).unsqueeze(-1)

        # ─── ITPRA (2D) — Huron 2006 ────────────────────────
        tension = brain_output.get_dim("tension")
        harmonic_ctx = brain_output.get_dim("harmonic_context")
        pred_error = brain_output.get_dim("prediction_error")
        emotional_arc = brain_output.get_dim("emotional_arc")

        itpra_tr = ((1.0 - tension) * harmonic_ctx).unsqueeze(-1)
        itpra_se = (pred_error.abs() * emotional_arc).unsqueeze(-1)

        # ─── Aesthetics (3D) ────────────────────────────────
        beauty = brain_output.get_dim("beauty").unsqueeze(-1)  # DIRECT
        arousal = brain_output.get_dim("arousal")
        sublime = (pleasure * arousal).unsqueeze(-1)
        groove = (arousal * harmonic_ctx).unsqueeze(-1)

        # ─── Emotion (2D) ───────────────────────────────────
        f03_valence = brain_output.get_dim("f03_valence")
        valence = ((f03_valence + 1.0) * 0.5).unsqueeze(-1)  # [-1,1] → [0,1]
        arousal_dim = arousal.unsqueeze(-1)

        # ─── Chills (3D) ────────────────────────────────────
        scr = brain_output.get_dim("scr")
        hr = brain_output.get_dim("hr")
        chills = brain_output.get_dim("chills_intensity")

        chill_prob = (scr * (1.0 - hr)).unsqueeze(-1)  # ANS chill signature
        chill_intensity = chills.unsqueeze(-1)
        chill_phase = torch.sigmoid(chills - tension).unsqueeze(-1)

        tensor = torch.cat([
            reward_intensity, reward_type, reward_phase,
            itpra_tr, itpra_se,
            beauty, sublime, groove,
            valence, arousal_dim,
            chill_prob, chill_intensity, chill_phase,
        ], dim=-1)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor.clamp(0, 1),
            dimension_names=tuple(self.dimension_names),
        )
