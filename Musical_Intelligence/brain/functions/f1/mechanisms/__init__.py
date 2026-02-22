"""F1 mechanisms — sensory processing computational models.

Depth-ordered pipeline (executor runs in this order):
    BCH  (Relay,      depth 0, 16D, SPU) — reads R³/H³ directly
    CSG  (Relay,      depth 0, 12D, ASU) — reads R³/H³ directly
    MIAA (Relay,      depth 0, 11D, SPU) — reads R³/H³ directly
    MPG  (Relay,      depth 0, 10D, NDU) — reads R³/H³ directly
    SDED (Relay,      depth 0, 10D, SPU) — reads R³/H³ directly
    PSCL (Encoder,    depth 1, 16D, SPU) — reads BCH output + R³/H³
    PCCR (Associator, depth 2, 11D, SPU) — reads BCH + PSCL output + R³/H³

Dependency chain:
    BCH  (Depth 0) ──→ PSCL (Depth 1) ──→ PCCR (Depth 2)
    CSG  (Depth 0) ──→ (no downstream in F1, feeds AACM + IACM cross-unit)
    MIAA (Depth 0) ──→ (no downstream in F1, feeds MEAMN + TPIO cross-unit)
    MPG  (Depth 0) ──→ (no downstream in F1, feeds NDU + STU cross-unit)
    SDED (Depth 0) ──→ (no downstream in F1, feeds STAI + ARU cross-unit)
"""
from .bch import BCH
from .csg import CSG
from .miaa import MIAA
from .mpg import MPG
from .pccr import PCCR
from .pscl import PSCL
from .sded import SDED

__all__ = ["BCH", "CSG", "MIAA", "MPG", "PSCL", "PCCR", "SDED"]
