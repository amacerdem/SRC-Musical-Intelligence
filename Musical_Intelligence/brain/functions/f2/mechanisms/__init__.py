"""F2 mechanisms — pattern recognition and prediction computational models.

Depth-ordered pipeline (executor runs in this order):
    HTP  (Relay,  depth 0, 12D, PCU) — reads R³/H³ directly
    SPH  (Relay,  depth 0, 14D, PCU) — reads R³/H³ directly
    ICEM (Relay,  depth 0, 13D, PCU) — reads R³/H³ directly

Dependency chain:
    HTP  (Depth 0) ──→ downstream F5/F6
    SPH  (Depth 0) ──→ downstream F5/F6
    ICEM (Depth 0) ──→ downstream F5/F6
"""
from .htp import HTP
from .icem import ICEM
from .sph import SPH

__all__ = ["HTP", "ICEM", "SPH"]
