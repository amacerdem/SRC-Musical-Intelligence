"""
delta (Delta) -- Validation Semantics (12D)

Level 4: HOW to test empirically.
Maps Brain dimensions to measurable physiological, neural, and
behavioral signals.

Physiological (4D):
  delta0: skin_conductance -- expected SCR signal     [de Fleurian & Pearce 2021, d=0.85]
  delta1: heart_rate -- expected HR change             [Thayer 2009]
  delta2: pupil_diameter -- expected pupil dilation    [Laeng 2012]
  delta3: piloerection -- expected goosebump prob      [Sloboda 1991]

Neural (3D):
  delta4: fmri_nacc_bold -- expected NAcc BOLD          [Salimpoor 2011, r=0.84]
  delta5: fmri_caudate_bold -- expected Caudate BOLD    [Salimpoor 2011, r=0.71]
  delta6: eeg_frontal_alpha -- expected alpha suppress  [Sammler 2007]

Behavioral (2D):
  delta7: willingness_to_pay -- Salimpoor 2013 auction  [Salimpoor 2013]
  delta8: button_press_rating -- continuous pleasure     [Schubert 2004]

Temporal (3D):
  delta9:  wanting_leads_liking -- temporal ordering     [Salimpoor 2011]
  delta10: rpe_latency -- prediction error magnitude     [Fong 2020]
  delta11: refractory_state -- inter-chill cooldown      [Grewe 2009]
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


class DeltaGroup(BaseSemanticGroup):
    LEVEL = 4
    GROUP_NAME = "delta"
    DISPLAY_NAME = "delta"
    OUTPUT_DIM = 12

    @property
    def dimension_names(self) -> List[str]:
        return [
            "skin_conductance", "heart_rate", "pupil_diameter", "piloerection",
            "fmri_nacc_bold", "fmri_caudate_bold", "eeg_frontal_alpha",
            "willingness_to_pay", "button_press_rating",
            "wanting_leads_liking", "rpe_latency", "refractory_state",
        ]

    def compute(self, brain_output: Any, **kwargs: Any) -> SemanticGroupOutput:
        """Compute delta group from BrainOutput (variable D).

        Uses _safe_get_dim for graceful degradation when dimensions are missing.
        """
        # Physiological (4D)
        scr = _safe_get_dim(brain_output, "scr").unsqueeze(-1)
        hr = _safe_get_dim(brain_output, "hr").unsqueeze(-1)
        arousal = _safe_get_dim(brain_output, "arousal")
        pred_error = _safe_get_dim(brain_output, "prediction_error", default=0.0)
        pupil = (arousal * pred_error.abs()).unsqueeze(-1)
        piloerection = _safe_get_dim(brain_output, "chills_intensity").unsqueeze(-1)

        # Neural (3D)
        fmri_nacc = _safe_get_dim(brain_output, "da_nacc").unsqueeze(-1)
        fmri_caudate = _safe_get_dim(brain_output, "da_caudate").unsqueeze(-1)
        pleasure = _safe_get_dim(brain_output, "pleasure")
        eeg_alpha = (1.0 - pleasure).unsqueeze(-1)

        # Behavioral (2D)
        wtp = pleasure.unsqueeze(-1)
        button_press = pleasure.unsqueeze(-1)

        # Temporal (3D)
        da_caudate = _safe_get_dim(brain_output, "da_caudate")
        da_nacc = _safe_get_dim(brain_output, "da_nacc")
        wanting_leads = torch.sigmoid(da_caudate - da_nacc).unsqueeze(-1)
        rpe_latency = pred_error.abs().unsqueeze(-1)
        chills = _safe_get_dim(brain_output, "chills_intensity")
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
