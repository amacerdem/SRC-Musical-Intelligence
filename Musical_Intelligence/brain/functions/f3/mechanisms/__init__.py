"""F3 mechanisms — attention and salience computational models.

Depth-ordered pipeline (executor runs in this order):
    SNEM  (Relay,      depth 0, 12D, ASU) — reads R³/H³ directly
    IACM  (Relay,      depth 0, 11D, ASU) — reads R³/H³ directly
    BARM  (Encoder,    depth 1, 10D, ASU) — reads SNEM
    STANM (Encoder,    depth 1, 11D, ASU) — reads R³/H³ + context
    AACM  (Encoder,    depth 1, 10D, ASU) — reads CSG [F1 cross-function]
    AMSS  (Encoder,    depth 1, 11D, STU) — reads HMCE [STU cross-unit]
    ETAM  (Encoder,    depth 1, 11D, STU) — reads HMCE + context
    DGTP  (Associator, depth 2,  9D, ASU) — reads BARM, SNEM
    SDL   (Associator, depth 2,  9D, ASU) — reads STANM, PWSM* [F2]
    NEWMD (Associator, depth 2, 10D, STU) — reads AMSC, HMCE [STU]
    IGFE  (Associator, depth 2,  9D, PCU) — reads WMED [F2]

Dependency chain:
    SNEM (Depth 0) ─┬─→ BARM (Depth 1) ──→ DGTP (Depth 2)
                     └─→ DGTP (Depth 2)
    IACM (Depth 0) ── (no downstream in F3)
    CSG* (Depth 0, F1) ──→ AACM (Depth 1)
    STANM (Depth 1) ──→ SDL (Depth 2)
    AMSS/ETAM (Depth 1) ──→ NEWMD (Depth 2)
    WMED* (F2) ──→ IGFE (Depth 2)
"""
from .snem import SNEM
from .iacm import IACM
from .barm import BARM
from .stanm import STANM
from .aacm import AACM
from .amss import AMSS
from .etam import ETAM
from .dgtp import DGTP
from .sdl import SDL
from .newmd import NEWMD
from .igfe import IGFE

__all__ = [
    "SNEM", "IACM",
    "BARM", "STANM", "AACM", "AMSS", "ETAM",
    "DGTP", "SDL", "NEWMD", "IGFE",
]
