"""
STU (Sensorimotor Timing Unit) -- All cognitive models.

14 models across three evidence tiers:

    Alpha (mechanistic, k >= 10):
        HMCE  -- Hierarchical Musical Context Encoding   (13D)
        AMSC  -- Auditory-Motor Stream Coupling           (12D)
        MDNS  -- Melody Decoding Neural Signals           (12D)

    Beta (correlational, 5 <= k < 10):
        AMSS  -- Attention-Modulated Stream Segregation   (11D)
        TPIO  -- Timbre Perception-Imagery Overlap        (10D)
        EDTA  -- Expertise-Dependent Tempo Adaptation     (10D)
        ETAM  -- Entrainment Tempo Attention Modulation   (11D)
        HGSIC -- Hierarchical Groove State Integration    (11D)
        OMS   -- Oscillatory Motor Synchronization        (10D)

    Gamma (exploratory, k < 5):
        TMRM  -- Tempo Memory Reproduction Matrix         (10D)
        NEWMD -- Neural Entrainment-Working Memory Diss.  (10D)
        MTNE  -- Music Training Neural Efficiency         (10D)
        PTGMP -- Piano Training Grey Matter Plasticity    (10D)
        MPFS  -- Musical Prodigy Flow State               (10D)

Total STU output: 148D per frame.
"""

from .amsc import AMSC
from .amss import AMSS
from .edta import EDTA
from .etam import ETAM
from .hgsic import HGSIC
from .hmce import HMCE
from .mdns import MDNS
from .mpfs import MPFS
from .mtne import MTNE
from .newmd import NEWMD
from .oms import OMS
from .ptgmp import PTGMP
from .tmrm import TMRM
from .tpio import TPIO

__all__ = [
    # Alpha
    "HMCE",
    "AMSC",
    "MDNS",
    # Beta
    "AMSS",
    "TPIO",
    "EDTA",
    "ETAM",
    "HGSIC",
    "OMS",
    # Gamma
    "TMRM",
    "NEWMD",
    "MTNE",
    "PTGMP",
    "MPFS",
]

ALL_STU_MODELS = (
    HMCE, AMSC, MDNS,
    AMSS, TPIO, EDTA, ETAM, HGSIC, OMS,
    TMRM, NEWMD, MTNE, PTGMP, MPFS,
)
"""Ordered tuple of all STU model classes for registry auto-discovery."""
