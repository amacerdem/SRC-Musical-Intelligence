"""
C0P -- Cognitive Projection
=============================

Circuit:  mesolimbic (reward & pleasure)
Horizons: H18 (2 s), H19 (3 s), H20 (5 s)
Output:   30-D

Overview
--------
Cognitive Projection models how top-down cognitive expectations are mapped
onto reward pathways in the mesolimbic dopaminergic system.  While AED
captures bottom-up entrainment and CPD detects autonomic peaks, C0P
encodes the *anticipatory* component -- the listener's prediction about
what will happen next and the reward signal generated when those
predictions are confirmed or violated.

This mechanism operates at longer timescales (2-5 s) where conscious
musical expectation unfolds:

    H18 (2 s) -- phrase-level anticipation:
        Encodes short-range predictions within a musical phrase.  At this
        timescale, listeners form expectations about melodic continuation,
        harmonic resolution, and rhythmic completion based on learned
        statistical regularities (Pearce & Wiggins 2012).  The prediction
        error between expected and actual musical events drives dopaminergic
        responses in the caudate nucleus (Salimpoor et al. 2011).

    H19 (3 s) -- inter-phrase anticipation:
        Captures predictions spanning phrase boundaries -- the "what comes
        next" expectation at section transitions.  This timescale aligns
        with the anticipatory dopamine release in caudate reported by
        Salimpoor et al. (2011), where peak caudate activity preceded
        peak NAcc activity by ~15 s.

    H20 (5 s) -- anticipation horizon:
        Integrates over the maximal window of conscious musical prediction.
        At this timescale, the mechanism tracks whether the music is
        approaching or retreating from a predicted goal state, modulating
        the "wanting" component of reward (Berridge 2003).

Neuroscientific basis:
    - Salimpoor et al. (2011): Temporal dissociation between caudate
      (anticipation) and NAcc (peak pleasure) during music listening.
    - Berridge (2003): Wanting vs. liking distinction in reward processing;
      C0P focuses on the "wanting" (anticipatory) component.
    - Pearce & Wiggins (2012): IDyOM model of melodic expectation based
      on statistical learning, generating surprise/information content.
    - Huron (2006): ITPRA theory -- Imagination, Tension, Prediction,
      Reaction, Appraisal as stages of anticipatory reward.

Used by:
    - ARU models: SRP (Striatal Reward Pathway), VMM (Ventral-Medial
      Mapping)

Stub status:
    Returns zeros.  Full implementation will compute prediction confidence,
    temporal distance to predicted goal, prediction error magnitude, and
    anticipatory reward signals by combining H3 trend, stability, and
    velocity features at H18-H20.  The 30-D output will encode wanting
    intensity, prediction precision, goal proximity, temporal urgency,
    and anticipatory valence dimensions.
"""

from __future__ import annotations

from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseMechanism


class C0P(BaseMechanism):
    """Cognitive Projection -- anticipatory reward and prediction mapping.

    Projects cognitive expectations onto mesolimbic reward pathways,
    encoding the "wanting" (anticipatory) component of musical reward
    at phrase-to-anticipation timescales (2-5 s).
    """

    NAME = "C0P"
    FULL_NAME = "Cognitive Projection"
    OUTPUT_DIM = 30
    HORIZONS = (18, 19, 20)  # H18 = 2 s, H19 = 3 s, H20 = 5 s

    # ── H3 demand ──────────────────────────────────────────────────────

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """Placeholder -- no H3 demands declared yet.

        The full implementation will declare demands for trend, stability,
        and velocity morphs on consonance and energy R3 features at
        H18/H19/H20 to track prediction confidence and goal proximity.
        """
        return set()

    # ── Compute ────────────────────────────────────────────────────────

    def compute(
        self,
        h3_features: Dict[Tuple[int, int, int, int], Tensor],
        r3_features: Tensor,
    ) -> Tensor:
        """Return zeros of shape (B, T, 30).

        Args:
            h3_features: H3 temporal features (unused in stub).
            r3_features: (B, T, 49) R3 spectral features.

        Returns:
            (B, T, 30) zero tensor on the same device as r3_features.
        """
        B, T, _ = r3_features.shape
        return torch.zeros(B, T, self.OUTPUT_DIM, device=r3_features.device)
