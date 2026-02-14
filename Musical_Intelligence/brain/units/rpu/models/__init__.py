"""Model implementations for the RPU cognitive unit.

10 models, 94D total output.
"""
from __future__ import annotations

from .daed import DAED  # alpha, 12D
from .mormr import MORMR  # alpha, 11D
from .rpem import RPEM  # alpha, 11D
from .iucp import IUCP  # beta, 10D
from .mccn import MCCN  # beta, 10D
from .meamr import MEAMR  # beta, 10D
from .ssri import SSRI  # beta, 11D
from .ldac import LDAC  # gamma, 9D
from .iotms import IOTMS  # gamma, 5D
from .ssps import SSPS  # gamma, 5D

MODEL_CLASSES: list = [
    DAED,
    MORMR,
    RPEM,
    IUCP,
    MCCN,
    MEAMR,
    SSRI,
    LDAC,
    IOTMS,
    SSPS,
]
