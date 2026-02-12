"""
SYN -- Syntactic Processing
=============================

Circuit:  mnemonic (memory consolidation & familiarity)
Horizons: H12 (525 ms), H16 (1 s), H18 (2 s)
Output:   30-D

Overview
--------
Syntactic Processing models how the brain parses musical structure according
to implicit grammatical rules -- the "syntax" of music.  Musical syntax
encompasses harmonic progressions, phrase structure, voice-leading
conventions, and hierarchical grouping rules that listeners internalise
through exposure.  Violations of these rules produce distinctive neural
signatures (ERAN, P600) analogous to those observed in language processing.

The primary neural substrate is the inferior frontal gyrus (IFG, Broca's
area homologue), which is recruited for both linguistic and musical syntactic
processing (Patel 2003).  The mechanism also involves interaction with
posterior superior temporal gyrus (pSTG) for hierarchical structure building.

The three horizons capture different levels of musical syntactic processing:

    H12 (525 ms) -- beat-level harmonic syntax:
        At this timescale, the mechanism processes chord-to-chord transitions
        and detects local harmonic violations.  This corresponds to the
        timescale of individual chords in most music (~250-700 ms per
        chord).  Syntactic violations at this level produce the early right
        anterior negativity (ERAN) response peaking at ~200 ms after an
        unexpected chord (Koelsch et al. 2000).

    H16 (1 s) -- phrase-level syntax:
        Integrates over multiple chords to evaluate phrase-level harmonic
        trajectories.  This includes detection of cadential progressions,
        tonal closure, and phrase-internal syntactic coherence.  At this
        timescale, the mechanism tracks whether harmonic progressions follow
        expected patterns (e.g., ii-V-I cadence) or deviate from them.

    H18 (2 s) -- hierarchical grouping:
        Captures higher-order syntactic structure -- how phrases group into
        periods and how hierarchical tonal relationships span multiple
        phrases.  This corresponds to the timescale of Lerdahl &
        Jackendoff's (1983) GTTM grouping rules, where musical events
        are recursively grouped into hierarchical structures.

Neuroscientific basis:
    - Patel (2003): Shared Syntactic Integration Resource Hypothesis (SSIRH)
      -- music and language share syntactic processing resources in IFG.
    - Koelsch et al. (2000): ERAN response to unexpected chords, localised
      to IFG and anterior STG.
    - Lerdahl & Jackendoff (1983): A Generative Theory of Tonal Music (GTTM)
      -- hierarchical grouping and prolongational reduction rules.
    - Maess et al. (2001): MEG evidence for early musical syntax processing
      in Broca's area (BA44/45).
    - Tillmann et al. (2003): Musical structure processing activates a
      bilateral network including IFG, STG, and premotor cortex.

Used by:
    - IMU models: MSPBA (Musical Syntax Processing -- Broca's Area)

Stub status:
    Returns zeros.  Full implementation will read consonance, harmonic,
    and energy R3 features at H12/H16/H18, compute chord-transition
    surprise, cadential probability, syntactic violation magnitude,
    hierarchical depth estimate, and tonal closure strength across
    the 30-D output space.
"""

from __future__ import annotations

from typing import Dict, Set, Tuple

import torch
from torch import Tensor

from mi_beta.contracts import BaseMechanism


class SYN(BaseMechanism):
    """Syntactic Processing -- musical grammar parsing via IFG/Broca's area.

    Parses musical syntax at chord (H12), phrase (H16), and hierarchical
    grouping (H18) timescales, detecting violations of harmonic expectation
    and evaluating syntactic coherence in the mnemonic circuit.
    """

    NAME = "SYN"
    FULL_NAME = "Syntactic Processing"
    OUTPUT_DIM = 30
    HORIZONS = (12, 16, 18)  # H12 = 525 ms, H16 = 1 s, H18 = 2 s

    # ── H3 demand ──────────────────────────────────────────────────────

    @property
    def h3_demand(self) -> Set[Tuple[int, int, int, int]]:
        """Placeholder -- no H3 demands declared yet.

        The full implementation will declare demands for consonance group
        R3 features (stumpf_fusion, harmonicity, roughness) at H12/H16/H18
        to measure harmonic transition surprise and syntactic coherence.
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
