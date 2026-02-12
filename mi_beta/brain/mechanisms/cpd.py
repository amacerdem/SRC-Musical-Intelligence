"""
CPD -- Chills & Peak Detection
===============================

Circuit:  mesolimbic (reward & pleasure)
Horizons: H9 (350 ms), H16 (1 s), H18 (2 s)
Output:   30-D

Overview
--------
Chills & Peak Detection identifies moments of intense autonomic arousal
during music listening -- the "goosebumps" or "frisson" response.  These
are brief, involuntary physiological events characterised by piloerection,
skin conductance spikes, and subjective reports of intense pleasure.

CPD operates across three timescales that span the autonomic nervous system's
response dynamics:

    H9  (350 ms) -- fast ANS detection:
        Captures the initial sympathetic response onset.  Skin conductance
        response (SCR) latency is ~1-3 s, but the triggering neural event
        occurs within hundreds of milliseconds.  H9 detects the acoustic
        trigger features (sudden dynamic change, harmonic shift, timbral
        novelty) that initiate the autonomic cascade.

    H16 (1 s) -- beat-level integration:
        Integrates over the timescale at which conscious awareness of the
        frisson event emerges.  This corresponds to the psychological
        present (Poppel 2009) and the typical duration of a musical beat.

    H18 (2 s) -- phrase-level context:
        Provides the broader musical context that determines whether an
        acoustic event is surprising enough to trigger chills.  Expectation
        violation (Huron 2006) requires a temporal window long enough to
        establish the prediction being violated.

Neuroscientific basis:
    - Blood & Zatorre (2001): PET study showing dopamine release during
      musical chills, with involvement of NAcc, VTA, and insula.
    - Salimpoor et al. (2009): Psychophysiological correlates of music-
      evoked chills including SCR, heart rate, and respiration changes.
    - Grewe et al. (2007): Acoustic features predicting chills include
      sudden dynamic increases, entry of new voices, and harmonic changes.
    - Huron (2006): Sweet Anticipation -- expectation violation as a
      driver of strong emotional responses in music.

Used by:
    - ARU models: SRP (Striatal Reward Pathway), AAC (Amygdala-Auditory
      Cortex)

Stub status:
    Returns zeros.  Full implementation will detect rapid loudness transients,
    harmonic surprise, and timbral novelty at H9; measure autonomic coupling
    strength at H16; and evaluate expectation violation magnitude at H18.
    The 30-D output will encode chill probability, SCR prediction, heart
    rate modulation, piloerection likelihood, and trigger-type classification.
"""

from __future__ import annotations

from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseMechanism


class CPD(BaseMechanism):
    """Chills & Peak Detection -- autonomic arousal and frisson moments.

    Detects goosebump/frisson events by monitoring fast ANS triggers (H9),
    conscious arousal emergence (H16), and expectation violation context
    (H18) across the mesolimbic circuit.
    """

    NAME = "CPD"
    FULL_NAME = "Chills & Peak Detection"
    OUTPUT_DIM = 30
    HORIZONS = (9, 16, 18)  # H9 = 350 ms, H16 = 1 s, H18 = 2 s

    # ── H3 demand ──────────────────────────────────────────────────────

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """Placeholder -- no H3 demands declared yet.

        The full implementation will declare demands for loudness velocity,
        harmonic change, and timbral novelty at H9/H16/H18 to detect
        autonomic trigger features and expectation violation.
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
