"""
IMU (Integrative Memory Unit) -- All cognitive models.

15 models across three evidence tiers:

    Alpha (mechanistic, k >= 10):
        MEAMN -- Music-Evoked Autobiographical Memory    (12D)
        PNH   -- Pythagorean Neural Hierarchy            (11D)
        MMP   -- Musical Mnemonic Preservation           (12D)

    Beta (correlational, 5 <= k < 10):
        RASN   -- Rhythmic Auditory Stimulation Network  (11D)
        PMIM   -- Predictive Memory Integration Matrix   (11D)
        OII    -- Oscillatory Intelligence Integration   (10D)
        HCMC   -- Hippocampal-Cortical Memory Consolid.  (11D)
        RIRI   -- Recognition-Recall Integration Recency (10D)
        MSPBA  -- Musical Syntax Processing Broca's Area (11D)
        VRIAP  -- VR-Induced Analgesia Paradigm          (10D)
        TPRD   -- Tonotopy-Pitch Representation Density  (10D)
        CMAPCC -- Cross-Modal Action-Perception Coupling (10D)

    Gamma (exploratory, k < 5):
        DMMS  -- Developmental Music Memory Schema       (10D)
        CSSL  -- Cross-Species Song Learning             (10D)
        CDEM  -- Context-Dependent Emotional Memory      (10D)

Total IMU output: 159D per frame.
"""

from .cdem import CDEM
from .cmapcc import CMAPCC
from .cssl import CSSL
from .dmms import DMMS
from .hcmc import HCMC
from .meamn import MEAMN
from .mmp import MMP
from .mspba import MSPBA
from .oii import OII
from .pmim import PMIM
from .pnh import PNH
from .rasn import RASN
from .riri import RIRI
from .tprd import TPRD
from .vriap import VRIAP

__all__ = [
    # Alpha
    "MEAMN",
    "PNH",
    "MMP",
    # Beta
    "RASN",
    "PMIM",
    "OII",
    "HCMC",
    "RIRI",
    "MSPBA",
    "VRIAP",
    "TPRD",
    "CMAPCC",
    # Gamma
    "DMMS",
    "CSSL",
    "CDEM",
]

ALL_IMU_MODELS = (
    MEAMN, PNH, MMP,
    RASN, PMIM, OII, HCMC, RIRI, MSPBA, VRIAP, TPRD, CMAPCC,
    DMMS, CSSL, CDEM,
)
"""Ordered tuple of all IMU model classes for registry auto-discovery."""
