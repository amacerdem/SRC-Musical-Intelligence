"""
δ (Delta) — Validation Semantics (12D)

Level 4: HOW to test empirically.
Maps Brain dimensions to measurable physiological, neural, and
behavioral signals.

Physiological (4D):
  δ0: skin_conductance — expected SCR signal     [de Fleurian & Pearce 2021, d=0.85]
  δ1: heart_rate — expected HR change             [Thayer 2009]
  δ2: pupil_diameter — expected pupil dilation    [Laeng 2012]
  δ3: piloerection — expected goosebump prob      [Sloboda 1991]

Neural (3D):
  δ4: fmri_nacc_bold — expected NAcc BOLD          [Salimpoor 2011, r=0.84]
  δ5: fmri_caudate_bold — expected Caudate BOLD    [Salimpoor 2011, r=0.71]
  δ6: eeg_frontal_alpha — expected alpha suppress  [Sammler 2007]

Behavioral (2D):
  δ7: willingness_to_pay — Salimpoor 2013 auction  [Salimpoor 2013]
  δ8: button_press_rating — continuous pleasure     [Schubert 2004]

Temporal (3D):
  δ9:  wanting_leads_liking — temporal ordering     [Salimpoor 2011]
  δ10: rpe_latency — prediction error magnitude     [Fong 2020]
  δ11: refractory_state — inter-chill cooldown      [Grewe 2009]
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ...core.base import BaseSemanticGroup
from ...core.types import SemanticGroupOutput


class DeltaGroup(BaseSemanticGroup):
    LEVEL = 4
    GROUP_NAME = "delta"
    DISPLAY_NAME = "δ"
    OUTPUT_DIM = 12

    @property
    def dimension_names(self) -> List[str]:
        return [
            "skin_conductance", "heart_rate", "pupil_diameter", "piloerection",
            "fmri_nacc_bold", "fmri_caudate_bold", "eeg_frontal_alpha",
            "willingness_to_pay", "button_press_rating",
            "wanting_leads_liking", "rpe_latency", "refractory_state",
        ]

    def compute(self, brain_output: object, **kwargs) -> SemanticGroupOutput:
        """Compute δ group from BrainOutput (26D).

        Brain provides DIRECT autonomic signals (scr, hr) that were
        previously estimated from AED mechanism.
        """
        # ─── Physiological (4D) — DIRECT from autonomic pathway
        scr = brain_output.get_dim("scr").unsqueeze(-1)           # D19
        hr = brain_output.get_dim("hr").unsqueeze(-1)             # D20
        # Pupil: arousal × |prediction_error| (Laeng 2012)
        arousal = brain_output.get_dim("arousal")
        pred_error = brain_output.get_dim("prediction_error")
        pupil = (arousal * pred_error.abs()).unsqueeze(-1)
        piloerection = brain_output.get_dim("chills_intensity").unsqueeze(-1)

        # ─── Neural (3D) — direct from reward pathway
        fmri_nacc = brain_output.get_dim("da_nacc").unsqueeze(-1)
        fmri_caudate = brain_output.get_dim("da_caudate").unsqueeze(-1)
        # Frontal alpha: high engagement (pleasure) = low alpha power
        pleasure = brain_output.get_dim("pleasure")
        eeg_alpha = (1.0 - pleasure).unsqueeze(-1)

        # ─── Behavioral (2D) — Salimpoor 2013
        wtp = pleasure.unsqueeze(-1)
        button_press = pleasure.unsqueeze(-1)

        # ─── Temporal (3D) — constraint checks
        da_caudate = brain_output.get_dim("da_caudate")
        da_nacc = brain_output.get_dim("da_nacc")
        wanting_leads = torch.sigmoid(da_caudate - da_nacc).unsqueeze(-1)
        rpe_latency = pred_error.abs().unsqueeze(-1)
        chills = brain_output.get_dim("chills_intensity")
        refractory = (1.0 - chills).unsqueeze(-1)

        tensor = torch.cat([
            scr, hr, pupil, piloerection,
            fmri_nacc, fmri_caudate, eeg_alpha,
            wtp, button_press,
            wanting_leads, rpe_latency, refractory,
        ], dim=-1)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor.clamp(0, 1),
            dimension_names=tuple(self.dimension_names),
        )
