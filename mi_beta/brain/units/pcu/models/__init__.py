"""
PCU (Predictive Coding Unit) -- All cognitive models.

9 models across three evidence tiers:

    Alpha (mechanistic, k >= 10):
        HTP  -- Harmonic Tension Prediction          (12D)
        SPH  -- Spectral Pitch Height                 (11D)
        ICEM -- Imagery-Cognition Emotion Mapping     (11D)

    Beta (correlational, 5 <= k < 10):
        PWUP -- Pitch-Weight Uncertainty Processing   (10D)
        WMED -- Working Memory Emotion Dynamics       (10D)
        UDP  -- Uncertainty-Driven Prediction          (10D)

    Gamma (exploratory, k < 5):
        IGFE -- Imagery-Guided Feature Enhancement    (10D)
        MAA  -- Musical Agentic Attention             (10D)
        PSH  -- Perceptual Salience Hierarchy         (10D)

Total PCU output: 94D per frame.
"""

from .htp import HTP
from .sph import SPH
from .icem import ICEM
from .pwup import PWUP
from .wmed import WMED
from .udp import UDP
from .igfe import IGFE
from .maa import MAA
from .psh import PSH

__all__ = [
    # Alpha
    "HTP",
    "SPH",
    "ICEM",
    # Beta
    "PWUP",
    "WMED",
    "UDP",
    # Gamma
    "IGFE",
    "MAA",
    "PSH",
]

ALL_PCU_MODELS = (HTP, SPH, ICEM, PWUP, WMED, UDP, IGFE, MAA, PSH)
"""Ordered tuple of all PCU model classes for registry auto-discovery."""
