"""
RPU (Reward Processing Unit) -- All cognitive models.

9 models across three evidence tiers:

    Alpha (mechanistic, k >= 10):
        DAED  -- DA-Expectation Dynamics               (12D)
        MORMR -- Model-Optimal Reward Modulation Relay  (11D)
        RPEM  -- Reward Prediction Error Model          (11D)

    Beta (correlational, 5 <= k < 10):
        IUCP  -- Information-Uncertainty Coupling Process (10D)
        MCCN  -- Musical Context Coupling Network        (10D)
        MEAMR -- Memory-Affect Modulated Reward          (10D)

    Gamma (exploratory, k < 5):
        LDAC  -- Listener-Dependent Aesthetic Computation (10D)
        IOTMS -- Individual Optimal Tempo Matching System (10D)
        SSPS  -- Social Signal Processing System          (10D)

Total RPU output: 94D per frame.
"""

from .daed import DAED
from .mormr import MORMR
from .rpem import RPEM
from .iucp import IUCP
from .mccn import MCCN
from .meamr import MEAMR
from .ldac import LDAC
from .iotms import IOTMS
from .ssps import SSPS

__all__ = [
    # Alpha
    "DAED",
    "MORMR",
    "RPEM",
    # Beta
    "IUCP",
    "MCCN",
    "MEAMR",
    # Gamma
    "LDAC",
    "IOTMS",
    "SSPS",
]

ALL_RPU_MODELS = (DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, LDAC, IOTMS, SSPS)
"""Ordered tuple of all RPU model classes for registry auto-discovery."""
