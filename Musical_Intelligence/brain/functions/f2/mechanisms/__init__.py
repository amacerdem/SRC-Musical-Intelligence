"""F2 mechanisms — pattern recognition and prediction computational models.

Depth-ordered pipeline (executor runs in this order):
    HTP  (Relay,       depth 0, 12D, PCU) — reads R³/H³ directly
    SPH  (Relay,       depth 0, 14D, PCU) — reads R³/H³ directly
    ICEM (Relay,       depth 0, 13D, PCU) — reads R³/H³ directly
    PWUP (Encoder,     depth 1, 10D, PCU) — reads HTP, ICEM
    WMED (Associator,  depth 2, 11D, PCU) — reads PWUP
    UDP  (Integrator,  depth 3, 10D, PCU) — reads PWUP, WMED
    CHPI (Integrator,  depth 3, 11D, PCU) — reads HTP, ICEM, PWUP, WMED
    IGFE (Integrator,  depth 3,  9D, PCU) — reads HTP, WMED
    MAA  (Hub,         depth 4, 10D, PCU) — reads PWUP, UDP, IGFE
    PSH  (Hub,         depth 5, 10D, PCU) — reads HTP, PWUP, WMED, UDP, MAA

Dependency chain:
    HTP  (Depth 0) ─┬─→ PWUP (Depth 1) ─┬─→ WMED (Depth 2) ─┬─→ UDP  (Depth 3)
    ICEM (Depth 0) ─┘                    │                    ├─→ CHPI (Depth 3)
    SPH  (Depth 0)                       │                    ├─→ IGFE (Depth 3)
                                         │                    │
                                         └────────────────────┼─→ MAA  (Depth 4)
                                                              └─→ PSH  (Depth 5)
"""
from .chpi import CHPI
from .htp import HTP
from .icem import ICEM
from .igfe import IGFE
from .maa import MAA
from .psh import PSH
from .pwup import PWUP
from .sph import SPH
from .udp import UDP
from .wmed import WMED

__all__ = [
    "HTP", "SPH", "ICEM",
    "PWUP", "WMED", "UDP", "CHPI", "IGFE",
    "MAA", "PSH",
]
