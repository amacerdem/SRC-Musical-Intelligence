"""
ARU (Affective Resonance Unit) -- All cognitive models.

10 models across three evidence tiers:

    Alpha (mechanistic, k >= 10):
        SRP  -- Striatal Reward Pathway          (19D)
        AAC  -- Autonomic-Affective Coupling     (14D)
        VMM  -- Valence-Mode Mapping             (12D)

    Beta (correlational, 5 <= k < 10):
        PUPF -- Pleasure-Uncertainty-Prediction  (12D)
        CLAM -- Cognitive-Load-Arousal Modulation(11D)
        MAD  -- Musical Anhedonia Disconnection   (11D)
        NEMAC-- Nostalgia-Enhanced Memory-Affect  (11D)

    Gamma (exploratory, k < 5):
        DAP  -- Developmental Affective Plasticity(10D)
        CMAT -- Cross-Modal Affective Transfer    (10D)
        TAR  -- Therapeutic Affective Resonance   (10D)

Total ARU output: 120D per frame.
"""

from .aac import AAC
from .clam import CLAM
from .cmat import CMAT
from .dap import DAP
from .mad import MAD
from .nemac import NEMAC
from .pupf import PUPF
from .srp import SRP
from .tar import TAR
from .vmm import VMM

__all__ = [
    # Alpha
    "SRP",
    "AAC",
    "VMM",
    # Beta
    "PUPF",
    "CLAM",
    "MAD",
    "NEMAC",
    # Gamma
    "DAP",
    "CMAT",
    "TAR",
]

ALL_ARU_MODELS = (SRP, AAC, VMM, PUPF, CLAM, MAD, NEMAC, DAP, CMAT, TAR)
"""Ordered tuple of all ARU model classes for registry auto-discovery."""
