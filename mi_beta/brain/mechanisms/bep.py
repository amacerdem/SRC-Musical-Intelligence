"""
BEP -- Beat Entrainment Processing
====================================

Circuit:  sensorimotor (rhythm & movement)
Horizons: H6 (200 ms), H9 (350 ms), H11 (450 ms)
Output:   30-D

Overview
--------
Beat Entrainment Processing models the sensorimotor coupling between
auditory beat perception and motor cortex entrainment.  When humans hear
rhythmic music, premotor and supplementary motor areas (SMA) synchronise
to the beat even in the absence of overt movement -- a phenomenon termed
"neural entrainment to the beat" (Grahn & Brett 2007).  BEP quantifies
the strength and precision of this coupling.

The mechanism targets three closely spaced horizons within the beat-level
temporal window, reflecting the fine temporal structure of sensorimotor
synchronisation:

    H6 (200 ms) -- sub-beat pulse:
        The fastest timescale of beat tracking, corresponding to sub-beat
        subdivisions in moderate-tempo music (120 BPM = 500 ms per beat,
        subdivisions at 250 ms).  At this horizon, BEP detects onset
        regularity and inter-onset-interval (IOI) periodicity that
        establish the metrical grid's finest level (Large & Palmer 2002).

    H9 (350 ms) -- beat period:
        The primary beat period for moderate-to-fast tempo music.  350 ms
        corresponds to ~171 BPM, near the upper end of comfortable tapping
        tempo.  At this timescale, BEP measures beat-period stability,
        phase consistency, and the strength of motor cortex entrainment.
        This aligns with the "preferred tempo" range identified by
        van Noorden & Moelants (1999).

    H11 (450 ms) -- beat-to-bar:
        Captures the transition from individual beats to metric grouping.
        At 450 ms (~133 BPM), this horizon spans a comfortable tactus
        tempo and detects whether beat events group into higher-level
        metric units.  SMA activation at this timescale reflects metric
        hierarchy processing (Chen et al. 2008).

Neuroscientific basis:
    - Grahn & Brett (2007): fMRI showing SMA, premotor, and basal ganglia
      activation during beat perception, even without movement.
    - Large & Palmer (2002): Neural oscillator model of beat tracking --
      entrainment as coupled oscillation.
    - Chen et al. (2008): Listening to musical rhythms recruits motor
      regions of the brain.
    - Zatorre et al. (2007): Motor-auditory interaction during rhythm
      perception and production.
    - van Noorden & Moelants (1999): Resonance theory of tempo perception;
      preferred tempo ~120 BPM, resonance range 80-160 BPM.

Used by:
    - STU models: HMCE (Hierarchical Motor-Cortical Entrainment), AMSC
      (Auditory-Motor Synchronisation Circuit), MDNS (Motor-Driven Neural
      Sequencing)

Stub status:
    Returns zeros.  Full implementation will read energy and onset-related
    R3 features at H6/H9/H11, compute IOI regularity, entrainment
    strength (phase coherence), beat-period estimate, metric salience,
    and sensorimotor coupling precision across the 30-D output space.
"""

from __future__ import annotations

from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseMechanism


class BEP(BaseMechanism):
    """Beat Entrainment Processing -- motor cortex synchronisation to beat.

    Quantifies sensorimotor entrainment at sub-beat (H6), beat (H9), and
    beat-to-bar (H11) timescales, modelling how motor areas lock onto
    rhythmic structure in music.
    """

    NAME = "BEP"
    FULL_NAME = "Beat Entrainment Processing"
    OUTPUT_DIM = 30
    HORIZONS = (6, 9, 11)  # H6 = 200 ms, H9 = 350 ms, H11 = 450 ms

    # ── H3 demand ──────────────────────────────────────────────────────

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """Placeholder -- no H3 demands declared yet.

        The full implementation will declare demands for energy, onset
        strength, and periodicity R3 features at H6, H9, and H11 to
        measure beat-level entrainment precision and motor coupling.
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
