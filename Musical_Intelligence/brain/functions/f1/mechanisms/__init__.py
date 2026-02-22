"""F1 mechanisms — sensory processing computational models.

Depth-ordered pipeline (executor runs in this order):
    BCH   (Relay,      depth 0, 16D, SPU) — reads R³/H³ directly
    CSG   (Relay,      depth 0, 12D, ASU) — reads R³/H³ directly
    MIAA  (Relay,      depth 0, 11D, SPU) — reads R³/H³ directly
    MPG   (Relay,      depth 0, 10D, NDU) — reads R³/H³ directly
    PNH   (Relay,      depth 0, 11D, IMU) — reads R³/H³ directly
    SDNPS (Relay,      depth 0, 10D, SPU) — reads R³/H³ directly
    SDED  (Relay,      depth 0, 10D, SPU) — reads R³/H³ directly
    TPRD  (Relay,      depth 0, 10D, IMU) — reads R³/H³ directly
    PSCL  (Encoder,    depth 1, 16D, SPU) — reads BCH output + R³/H³
    PCCR  (Associator, depth 2, 11D, SPU) — reads BCH + PSCL output + R³/H³

Dependency chain:
    BCH   (Depth 0) ──→ PSCL (Depth 1) ──→ PCCR (Depth 2)
    CSG   (Depth 0) ──→ (no downstream in F1, feeds AACM + IACM cross-unit)
    MIAA  (Depth 0) ──→ (no downstream in F1, feeds MEAMN + TPIO cross-unit)
    MPG   (Depth 0) ──→ (no downstream in F1, feeds NDU + STU cross-unit)
    PNH   (Depth 0) ──→ (no downstream in F1, ratio templates → BCH/PSCL/TPRD)
    SDNPS (Depth 0) ──→ (no downstream in F1, constrains BCH universality)
    SDED  (Depth 0) ──→ (no downstream in F1, feeds STAI + ARU cross-unit)
    TPRD  (Depth 0) ──→ (no downstream in F1, tonotopy-pitch → PNH/PMIM)
"""
from .bch import BCH
from .csg import CSG
from .miaa import MIAA
from .mpg import MPG
from .pccr import PCCR
from .pnh import PNH
from .pscl import PSCL
from .sdnps import SDNPS
from .sded import SDED
from .tprd import TPRD

__all__ = [
    "BCH", "CSG", "MIAA", "MPG", "PCCR", "PNH",
    "PSCL", "SDNPS", "SDED", "TPRD",
]
