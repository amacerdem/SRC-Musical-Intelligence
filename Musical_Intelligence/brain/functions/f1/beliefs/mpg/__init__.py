"""F1 Sensory Processing — MPG Beliefs.

2 beliefs from MPG mechanism:
    melodic_contour_tracking — Appraisal (observe-only)
    contour_continuation     — Anticipation (forward prediction)

Dependency chain:
    MPG (Depth 0, Relay) — reads R³/H³ directly.
    MPG beliefs require MPG mechanism only. No upstream dependency.
"""

from .contour_continuation import ContourContinuation
from .melodic_contour_tracking import MelodicContourTracking

__all__ = [
    "MelodicContourTracking",
    "ContourContinuation",
]
