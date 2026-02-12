"""
Brain Semantic Interpretation (104D)

Eight semantic groups interpret the unified 26D MusicalBrain output
across 8 epistemological levels:

  Phase 1 — Independent:
    α (6D):  Computation — HOW values were computed (pathway attribution)
    β (14D): Neuroscience — WHERE in the brain (region activation)
    γ (13D): Psychology — WHAT it means subjectively (reward, emotion, chills)
    δ (12D): Validation — HOW to test empirically (physio, neural, behavioral)
    ε (19D): Learning — HOW the listener learns (STATEFUL: Markov, EMA, Welford)

  Phase 2 — Dependent (ε→ζ→η, ε+ζ→θ):
    ζ (12D): Polarity — bipolar semantic axes [-1, +1]
    η (12D): Vocabulary — 64-gradation human-readable terms
    θ (16D): Narrative — sentence structure (subject/predicate/modifier/connector)

Total: 104D per frame. Zero learned parameters. Every dimension has a citation.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Dict

import torch
from torch import Tensor

from ...core.types import L3Output, SemanticGroupOutput
from .alpha import AlphaGroup
from .beta import BetaGroup
from .gamma import GammaGroup
from .delta import DeltaGroup
from .epsilon import EpsilonGroup
from .zeta import ZetaGroup
from .eta import EtaGroup
from .theta import ThetaGroup


class BrainSemantics:
    """Orchestrates all 8 semantic groups for the unified MusicalBrain."""

    TOTAL_DIM = 6 + 14 + 13 + 12 + 19 + 12 + 12 + 16  # = 104

    def __init__(self) -> None:
        self.groups: OrderedDict[str, object] = OrderedDict([
            ("alpha", AlphaGroup()),
            ("beta", BetaGroup()),
            ("gamma", GammaGroup()),
            ("delta", DeltaGroup()),
            ("epsilon", EpsilonGroup()),
            ("zeta", ZetaGroup()),
            ("eta", EtaGroup()),
            ("theta", ThetaGroup()),
        ])

    def compute(self, brain_output: object) -> L3Output:
        """Compute 104D semantic interpretation of Brain output.

        Dependency-ordered computation:
          Phase 1: α, β, γ, δ, ε (independent, read only brain_output)
          Phase 2: ζ(ε) → η(ζ) → θ(ε, ζ)

        Args:
            brain_output: BrainOutput (26D) from MusicalBrain

        Returns:
            L3Output with (B, T, 104)
        """
        group_outputs: Dict[str, SemanticGroupOutput] = {}
        tensors = []

        # ─── Phase 1: Independent groups ─────────────────────
        for name in ("alpha", "beta", "gamma", "delta"):
            out = self.groups[name].compute(brain_output)
            group_outputs[name] = out
            tensors.append(out.tensor)

        # ─── Phase 1b: Epsilon (stateful, but only reads brain)
        eps_out = self.groups["epsilon"].compute(brain_output)
        group_outputs["epsilon"] = eps_out
        tensors.append(eps_out.tensor)

        # ─── Phase 2: Zeta (needs epsilon) ───────────────────
        zeta_out = self.groups["zeta"].compute(
            brain_output,
            epsilon_output=eps_out.tensor,
        )
        group_outputs["zeta"] = zeta_out
        tensors.append(zeta_out.tensor)

        # ─── Phase 3: Eta (needs zeta) ───────────────────────
        eta_out = self.groups["eta"].compute(
            brain_output,
            zeta_output=zeta_out.tensor,
        )
        group_outputs["eta"] = eta_out
        tensors.append(eta_out.tensor)

        # ─── Phase 4: Theta (needs epsilon + zeta) ───────────
        theta_out = self.groups["theta"].compute(
            brain_output,
            epsilon_output=eps_out.tensor,
            zeta_output=zeta_out.tensor,
        )
        group_outputs["theta"] = theta_out
        tensors.append(theta_out.tensor)

        combined = torch.cat(tensors, dim=-1)  # (B, T, 104)

        return L3Output(
            model_name="Brain",
            groups=group_outputs,
            tensor=combined,
        )

    def reset(self) -> None:
        """Reset stateful groups. Call between audio files."""
        self.groups["epsilon"].reset()

    @property
    def total_dim(self) -> int:
        return sum(g.OUTPUT_DIM for g in self.groups.values())


__all__ = ["BrainSemantics"]
