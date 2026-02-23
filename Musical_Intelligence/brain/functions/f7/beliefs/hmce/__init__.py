"""F7 Beliefs — HMCE (Hierarchical Music Context Encoding).

6 beliefs derived from HMCE mechanism output:
    1 Core:         context_depth (tau=0.70)
    3 Appraisal:    short_context, medium_context, long_context
    2 Anticipation: phrase_boundary_pred, structure_pred
"""

from .context_depth import ContextDepth
from .long_context import LongContext
from .medium_context import MediumContext
from .phrase_boundary_pred import PhraseBoundaryPred
from .short_context import ShortContext
from .structure_pred import StructurePred

__all__ = [
    "ContextDepth",
    "ShortContext",
    "MediumContext",
    "LongContext",
    "PhraseBoundaryPred",
    "StructurePred",
]
