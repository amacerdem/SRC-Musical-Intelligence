"""F1 mechanisms — sensory processing computational models.

BCH (Relay, depth 0, 16D) → PSCL (Encoder, depth 1, 16D) → ...
"""
from .bch import BCH
from .pscl import PSCL

__all__ = ["BCH", "PSCL"]
