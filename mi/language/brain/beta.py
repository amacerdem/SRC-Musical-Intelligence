"""
β (Beta) — Neuroscience Semantics (14D)

Level 2: WHERE in the brain.
Maps Brain dimensions to brain regions, neurotransmitter dynamics,
and circuit states.

Brain Regions (8D):
  β0-β1: Striatal (NAcc, Caudate)        [Salimpoor 2011]
  β2-β3: Midbrain (VTA, SN)              [Howe 2013]
  β4-β5: Cortical (STG, IFG)             [Kim 2021, Fong 2020]
  β6-β7: Limbic (Amygdala, Hippocampus)  [Koelsch 2006, Sachs 2025]

Neurotransmitter Dynamics (3D):
  β8:  Dopamine level                     [Salimpoor 2011]
  β9:  Opioid level                       [Blood & Zatorre 2001]
  β10: DA/Opioid interaction              [Berridge 2003]

Circuit States (3D):
  β11: Anticipation circuit (Caudate→DA ramp)  [Salimpoor 2011]
  β12: Consummation circuit (NAcc→DA burst)    [Salimpoor 2011]
  β13: Learning circuit (VTA→RPE)              [Fong 2020]
"""

from __future__ import annotations

from typing import List

import torch
from torch import Tensor

from ...core.base import BaseSemanticGroup
from ...core.types import SemanticGroupOutput


class BetaGroup(BaseSemanticGroup):
    LEVEL = 2
    GROUP_NAME = "beta"
    DISPLAY_NAME = "β"
    OUTPUT_DIM = 14

    @property
    def dimension_names(self) -> List[str]:
        return [
            "nacc_activation", "caudate_activation",
            "vta_activation", "sn_activation",
            "stg_activation", "ifg_activation",
            "amygdala_activation", "hippocampus_activation",
            "dopamine_level", "opioid_level", "da_opioid_interaction",
            "anticipation_circuit", "consummation_circuit", "learning_circuit",
        ]

    def compute(self, brain_output: object, **kwargs) -> SemanticGroupOutput:
        """Compute β group from BrainOutput (26D).

        Brain → region mapping uses direct dimension correspondence:
          da_nacc → NAcc, da_caudate → Caudate, reward_forecast → VTA,
          harmonic_context → STG, |prediction_error| → IFG.
        """
        # Brain regions — direct mapping from Brain dimensions
        nacc = brain_output.get_dim("da_nacc").unsqueeze(-1)
        caudate = brain_output.get_dim("da_caudate").unsqueeze(-1)
        vta = brain_output.get_dim("reward_forecast").unsqueeze(-1)  # VTA ramping DA
        sn = vta * 0.5  # shared midbrain proxy
        stg = brain_output.get_dim("harmonic_context").unsqueeze(-1)  # STG: harmony
        ifg = torch.sigmoid(
            brain_output.get_dim("prediction_error").abs().unsqueeze(-1)  # IFG: prediction
        )
        amygdala = torch.sigmoid(
            brain_output.get_dim("prediction_error").abs().unsqueeze(-1)
            * brain_output.get_dim("tension").unsqueeze(-1)
        )
        hippocampus = brain_output.get_dim("emotional_arc").unsqueeze(-1)  # memory encoding

        # Neurotransmitters
        dopamine = (nacc + caudate) * 0.5
        opioid = brain_output.get_dim("opioid_proxy").unsqueeze(-1)
        da_opioid = dopamine * opioid

        # Circuit states
        anticipation = caudate
        consummation = nacc
        learning = brain_output.get_dim("prediction_error").abs().unsqueeze(-1)

        tensor = torch.cat([
            nacc, caudate, vta, sn, stg, ifg, amygdala, hippocampus,
            dopamine, opioid, da_opioid,
            anticipation, consummation, learning,
        ], dim=-1)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor.clamp(0, 1),
            dimension_names=tuple(self.dimension_names),
        )
