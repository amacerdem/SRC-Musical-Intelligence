"""
NDU (Novelty Detection Unit) -- All cognitive models.

9 models across three evidence tiers:

    Alpha (mechanistic, k >= 10):
        MPG  -- Mismatch Prediction Gate                 (12D)
        SDD  -- Spectral Deviance Detection              (11D)
        EDNR -- Expectation-Dependent Novelty Response   (11D)

    Beta (correlational, 5 <= k < 10):
        DSP_ -- Deviance Salience Processing             (10D)
        CDMR -- Context-Dependent Mismatch Response      (10D)
        SLEE -- Statistical Learning Expectation Engine   (10D)

    Gamma (exploratory, k < 5):
        SDDP -- Sensory-Driven Deviance Processing       (10D)
        ONI  -- Oddball Novelty Index                    (10D)
        ECT  -- Error Correction Trace                   (10D)

Total NDU output: 94D per frame.
"""

from .cdmr import CDMR
from .dsp_ import DSP_
from .ect import ECT
from .ednr import EDNR
from .mpg import MPG
from .oni import ONI
from .sdd import SDD
from .sddp import SDDP
from .slee import SLEE

__all__ = [
    # Alpha
    "MPG",
    "SDD",
    "EDNR",
    # Beta
    "DSP_",
    "CDMR",
    "SLEE",
    # Gamma
    "SDDP",
    "ONI",
    "ECT",
]

ALL_NDU_MODELS = (MPG, SDD, EDNR, DSP_, CDMR, SLEE, SDDP, ONI, ECT)
"""Ordered tuple of all NDU model classes for registry auto-discovery."""
