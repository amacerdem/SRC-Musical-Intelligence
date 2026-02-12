"""
zeta (Zeta) -- Polarity (12D)

Level 6: Bipolar semantic axes mapping Brain output to interpretable
poles.  Each axis spans [-1, +1] with named negative and positive poles.

Reward Axes (6D):
  zeta0: valence -- sad <-> joyful                    [Russell 1980]
  zeta1: arousal -- calm <-> excited                   [Yang 2025]
  zeta2: tension -- relaxed <-> tense                  [Huron 2006]
  zeta3: power -- delicate <-> powerful                [Osgood 1957]
  zeta4: wanting -- satiated <-> craving               [Berridge 2003]
  zeta5: liking -- displeasure <-> satisfaction        [Berridge 2003]

Learning Axes (3D) -- from epsilon:
  zeta6: novelty -- familiar <-> novel                 [Berlyne 1971]
  zeta7: complexity -- simple <-> complex              [Berlyne 1971]
  zeta10: stability -- chaotic <-> stable              [Friston 2010]

Aesthetic Axes (3D):
  zeta8: beauty -- discordant <-> harmonious           [Blood & Zatorre 2001]
  zeta9: groove -- rigid <-> flowing                   [Janata 2012]
  zeta11: engagement -- detached <-> absorbed          [Csikszentmihalyi 1990]

Scientific basis:
  - Semantic Differential Theory (Osgood et al. 1957)
  - Circumplex Model of Affect (Russell 1980)
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

import torch
from torch import Tensor

from ...contracts.base_semantic_group import BaseSemanticGroup, SemanticGroupOutput
from ...core.types import BrainOutput


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


class ZetaGroup(BaseSemanticGroup):
    LEVEL = 6
    GROUP_NAME = "zeta"
    DISPLAY_NAME = "zeta"
    OUTPUT_DIM = 12

    @property
    def dimension_names(self) -> List[str]:
        return [ax["name"] for ax in POLARITY_AXES]

    def compute(
        self,
        brain_output: Any,
        *,
        epsilon_output: Optional[Tensor] = None,
        **kwargs: Any,
    ) -> SemanticGroupOutput:
        """Compute zeta group -- 12 bipolar polarity axes.

        Maps Brain dimensions to [-1, +1] bipolar semantic space.
        Sigmoid outputs get 2x-1 transform; already-bipolar values pass through.
        """
        zero = torch.zeros_like(brain_output.tensor[..., :1])

        # Reward axes (Brain [0,1] -> [-1,+1])
        valence = _safe_get_dim(brain_output, "valence")
        valence_pol = (2 * valence - 1).unsqueeze(-1)

        arousal = 2 * _safe_get_dim(brain_output, "arousal").unsqueeze(-1) - 1
        tension = 2 * _safe_get_dim(brain_output, "tension").unsqueeze(-1) - 1

        # Power: use mean brain activation as proxy when ans_composite unavailable
        power_val = _safe_get_dim(brain_output, "arousal")
        power = (2 * power_val - 1).unsqueeze(-1)

        wanting = 2 * _safe_get_dim(brain_output, "wanting").unsqueeze(-1) - 1
        liking = 2 * _safe_get_dim(brain_output, "liking").unsqueeze(-1) - 1

        # Learning axes (from epsilon)
        if epsilon_output is not None:
            novelty = 2 * epsilon_output[..., 0:1] - 1     # surprise
            complexity = 2 * epsilon_output[..., 1:2] - 1   # entropy
            stability = 2 * epsilon_output[..., 6:7] - 1    # precision_long
        else:
            novelty = zero
            complexity = zero
            stability = zero

        # Aesthetic axes
        beauty_val = _safe_get_dim(brain_output, "beauty")
        beauty = (2 * beauty_val - 1).unsqueeze(-1)

        groove_val = (
            _safe_get_dim(brain_output, "arousal")
            * _safe_get_dim(brain_output, "harmonic_context")
        )
        groove = (2 * groove_val - 1).unsqueeze(-1)

        engagement_val = (
            _safe_get_dim(brain_output, "pleasure")
            * _safe_get_dim(brain_output, "arousal")
        )
        engagement = (2 * engagement_val - 1).unsqueeze(-1)

        tensor = torch.cat([
            valence_pol, arousal, tension, power, wanting, liking,
            novelty, complexity, beauty, groove, stability, engagement,
        ], dim=-1)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor.clamp(-1, 1),
            dimension_names=tuple(self.dimension_names),
        )
