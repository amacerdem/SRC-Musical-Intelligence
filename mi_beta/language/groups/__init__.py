"""
L3 Orchestrator -- Coordinates 8 semantic groups for mi_beta.

Adapted from mi/language/brain/__init__.py for the multi-model brain
architecture.  In mi_beta, Brain output is variable-dimensional
(depending on which units/models are active), so Alpha and Beta groups
auto-configure their output size from the BrainOutput structure.

Computation phases:
  Phase 1 — Independent (read only BrainOutput):
    alpha, beta, gamma, delta
  Phase 1b — Stateful (read only BrainOutput, maintains state):
    epsilon
  Phase 2 — Dependent (epsilon -> zeta -> eta, epsilon+zeta -> theta):
    zeta, eta, theta
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any, Dict, Optional

import torch
from torch import Tensor

from ...core.types import BrainOutput, L3Output, SemanticGroupOutput
from .alpha import AlphaGroup
from .beta import BetaGroup
from .gamma import GammaGroup
from .delta import DeltaGroup
from .epsilon import EpsilonGroup
from .zeta import ZetaGroup
from .eta import EtaGroup
from .theta import ThetaGroup


class L3Orchestrator:
    """Orchestrates all 8 semantic groups for the mi_beta multi-model Brain.

    Unlike the mi/ BrainSemantics (fixed 104D), mi_beta's L3Orchestrator
    produces variable-dimensional output because Alpha (per-unit attribution)
    and Beta (per-region activation) adapt to the active model set.

    Usage::

        orchestrator = L3Orchestrator()
        l3_output = orchestrator.compute(brain_output)
        print(l3_output.total_dim)  # variable, depends on active units/regions

    With a registry (enables Beta group to know about brain regions)::

        orchestrator = L3Orchestrator(registry=registry)
    """

    def __init__(self, registry: Any = None) -> None:
        self.groups: OrderedDict[str, Any] = OrderedDict([
            ("alpha", AlphaGroup()),
            ("beta", BetaGroup(registry=registry)),
            ("gamma", GammaGroup()),
            ("delta", DeltaGroup()),
            ("epsilon", EpsilonGroup()),
            ("zeta", ZetaGroup()),
            ("eta", EtaGroup()),
            ("theta", ThetaGroup()),
        ])

    def compute(self, brain_output: BrainOutput) -> L3Output:
        """Compute semantic interpretation of Brain output.

        Dependency-ordered computation:
          Phase 1:  alpha, beta, gamma, delta (independent, read only brain_output)
          Phase 1b: epsilon (stateful, reads only brain_output)
          Phase 2:  zeta(epsilon) -> eta(zeta) -> theta(epsilon, zeta)

        Args:
            brain_output: BrainOutput from the mi_beta brain pipeline.

        Returns:
            L3Output with (B, T, total_dim) where total_dim is variable.
        """
        group_outputs: Dict[str, SemanticGroupOutput] = {}
        tensors = []

        # --- Phase 1: Independent groups ---
        for name in ("alpha", "beta", "gamma", "delta"):
            out = self.groups[name].compute(brain_output)
            group_outputs[name] = out
            tensors.append(out.tensor)

        # --- Phase 1b: Epsilon (stateful, but only reads brain) ---
        eps_out = self.groups["epsilon"].compute(brain_output)
        group_outputs["epsilon"] = eps_out
        tensors.append(eps_out.tensor)

        # --- Phase 2: Zeta (needs epsilon) ---
        zeta_out = self.groups["zeta"].compute(
            brain_output,
            epsilon_output=eps_out.tensor,
        )
        group_outputs["zeta"] = zeta_out
        tensors.append(zeta_out.tensor)

        # --- Phase 3: Eta (needs zeta) ---
        eta_out = self.groups["eta"].compute(
            brain_output,
            zeta_output=zeta_out.tensor,
        )
        group_outputs["eta"] = eta_out
        tensors.append(eta_out.tensor)

        # --- Phase 4: Theta (needs epsilon + zeta) ---
        theta_out = self.groups["theta"].compute(
            brain_output,
            epsilon_output=eps_out.tensor,
            zeta_output=zeta_out.tensor,
        )
        group_outputs["theta"] = theta_out
        tensors.append(theta_out.tensor)

        combined = torch.cat(tensors, dim=-1)  # (B, T, total_dim)

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
        """Total output dimensionality (variable, depends on active models)."""
        return sum(
            g.OUTPUT_DIM for g in self.groups.values()
        )


__all__ = ["L3Orchestrator"]
