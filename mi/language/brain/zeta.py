"""
ζ (Zeta) — Polarity (12D)

Level 6: Bipolar semantic axes mapping Brain output to interpretable
poles. Each axis spans [-1, +1] with named negative and positive poles.

Reward Axes (6D):
  ζ0: valence — sad ↔ joyful                    [Russell 1980]
  ζ1: arousal — calm ↔ excited                   [Yang 2025]
  ζ2: tension — relaxed ↔ tense                  [Huron 2006]
  ζ3: power — delicate ↔ powerful                [Osgood 1957]
  ζ4: wanting — satiated ↔ craving               [Berridge 2003]
  ζ5: liking — displeasure ↔ satisfaction        [Berridge 2003]

Learning Axes (3D) — from ε:
  ζ6: novelty — familiar ↔ novel                 [Berlyne 1971]
  ζ7: complexity — simple ↔ complex              [Berlyne 1971]
  ζ10: stability — chaotic ↔ stable              [Friston 2010]

Aesthetic Axes (3D):
  ζ8: beauty — discordant ↔ harmonious           [Blood & Zatorre 2001]
  ζ9: groove — rigid ↔ flowing                   [Janata 2012]
  ζ11: engagement — detached ↔ absorbed          [Csikszentmihalyi 1990]

Scientific basis:
  - Semantic Differential Theory (Osgood et al. 1957)
  - Circumplex Model of Affect (Russell 1980)
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor

from ...core.base import BaseSemanticGroup
from ...core.types import SemanticGroupOutput


POLARITY_AXES: Tuple[Dict[str, str], ...] = (
    {"name": "valence",    "neg": "sad",         "pos": "joyful"},
    {"name": "arousal",    "neg": "calm",        "pos": "excited"},
    {"name": "tension",    "neg": "relaxed",     "pos": "tense"},
    {"name": "power",      "neg": "delicate",    "pos": "powerful"},
    {"name": "wanting",    "neg": "satiated",    "pos": "craving"},
    {"name": "liking",     "neg": "displeasure", "pos": "satisfaction"},
    {"name": "novelty",    "neg": "familiar",    "pos": "novel"},
    {"name": "complexity", "neg": "simple",      "pos": "complex"},
    {"name": "beauty",     "neg": "discordant",  "pos": "harmonious"},
    {"name": "groove",     "neg": "rigid",       "pos": "flowing"},
    {"name": "stability",  "neg": "chaotic",     "pos": "stable"},
    {"name": "engagement", "neg": "detached",    "pos": "absorbed"},
)


class ZetaGroup(BaseSemanticGroup):
    LEVEL = 6
    GROUP_NAME = "zeta"
    DISPLAY_NAME = "ζ"
    OUTPUT_DIM = 12

    @property
    def dimension_names(self) -> List[str]:
        return [ax["name"] for ax in POLARITY_AXES]

    def compute(
        self,
        brain_output: object,
        *,
        epsilon_output: Optional[Tensor] = None,
        **kwargs,
    ) -> SemanticGroupOutput:
        """Compute ζ group — 12 bipolar polarity axes.

        Maps Brain dimensions to [-1, +1] bipolar semantic space.
        f03_valence is already [-1,1]; sigmoid outputs get 2x-1 transform.
        """
        zero = torch.zeros_like(brain_output.tensor[..., :1])

        # ─── Reward axes (Brain [0,1] → [-1,+1]) ────────────
        valence = brain_output.get_dim("f03_valence").unsqueeze(-1)  # already [-1,1]
        arousal = 2 * brain_output.get_dim("arousal").unsqueeze(-1) - 1
        tension = 2 * brain_output.get_dim("tension").unsqueeze(-1) - 1
        power = 2 * brain_output.get_dim("ans_composite").unsqueeze(-1) - 1
        wanting = 2 * brain_output.get_dim("wanting").unsqueeze(-1) - 1
        liking = 2 * brain_output.get_dim("liking").unsqueeze(-1) - 1

        # ─── Learning axes (from epsilon) ────────────────────
        if epsilon_output is not None:
            novelty = 2 * epsilon_output[..., 0:1] - 1     # surprise
            complexity = 2 * epsilon_output[..., 1:2] - 1   # entropy
            stability = 2 * epsilon_output[..., 6:7] - 1    # precision_long
        else:
            novelty = zero
            complexity = zero
            stability = zero

        # ─── Aesthetic axes ──────────────────────────────────
        beauty = 2 * brain_output.get_dim("beauty").unsqueeze(-1) - 1
        groove_val = (
            brain_output.get_dim("harmonic_context")
            * brain_output.get_dim("arousal")
        )
        groove = (2 * groove_val - 1).unsqueeze(-1)
        engagement_val = (
            brain_output.get_dim("pleasure")
            * brain_output.get_dim("arousal")
        )
        engagement = (2 * engagement_val - 1).unsqueeze(-1)

        tensor = torch.cat([
            valence, arousal, tension, power, wanting, liking,
            novelty, complexity, beauty, groove, stability, engagement,
        ], dim=-1)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor.clamp(-1, 1),
            dimension_names=tuple(self.dimension_names),
        )
