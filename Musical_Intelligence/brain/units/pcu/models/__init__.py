"""Model implementations for the PCU cognitive unit.

10 models, 94D total output.
"""
from __future__ import annotations

from .htp import HTP  # alpha, 12D
from .sph import SPH  # alpha, 11D
from .icem import ICEM  # alpha, 11D
from .pwup import PWUP  # beta, 10D
from .wmed import WMED  # beta, 10D
from .udp import UDP  # beta, 10D
from .chpi import CHPI  # beta, 11D
from .igfe import IGFE  # gamma, 9D
from .maa import MAA  # gamma, 5D
from .psh import PSH  # gamma, 5D

MODEL_CLASSES: list = [
    HTP,
    SPH,
    ICEM,
    PWUP,
    WMED,
    UDP,
    CHPI,
    IGFE,
    MAA,
    PSH,
]
