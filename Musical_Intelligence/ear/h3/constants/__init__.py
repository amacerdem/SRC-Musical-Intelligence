"""H3 constants sub-package -- temporal morphology parameters.

Re-exports every public constant and helper from the four sub-modules so that
downstream code can simply write::

    from ear.h3.constants import HORIZON_MS, MORPH_NAMES, LAW_NAMES, ...
"""

from __future__ import annotations

# -- horizons ---------------------------------------------------------------
from .horizons import (
    BAND_ASSIGNMENTS,
    BAND_RANGES,
    FRAME_DURATION_MS,
    FRAME_RATE,
    HORIZON_FRAMES,
    HORIZON_MS,
    N_HORIZONS,
)

# -- morphs ----------------------------------------------------------------
from .morphs import (
    MORPH_CATEGORIES,
    MORPH_MIN_WINDOW,
    MORPH_NAMES,
    N_MORPHS,
    SIGNED_MORPHS,
)

# -- laws -------------------------------------------------------------------
from .laws import (
    ATTENTION_DECAY,
    LAW_INTEGRATION,
    LAW_MEMORY,
    LAW_NAMES,
    LAW_PREDICTION,
    N_LAWS,
)

# -- scaling ----------------------------------------------------------------
from .scaling import (
    MORPH_SCALE,
    normalize_signed,
    normalize_unsigned,
)

# ---------------------------------------------------------------------------
__all__ = [
    # horizons
    "HORIZON_MS",
    "HORIZON_FRAMES",
    "BAND_ASSIGNMENTS",
    "BAND_RANGES",
    "N_HORIZONS",
    "FRAME_RATE",
    "FRAME_DURATION_MS",
    # morphs
    "MORPH_NAMES",
    "MORPH_CATEGORIES",
    "MORPH_MIN_WINDOW",
    "SIGNED_MORPHS",
    "N_MORPHS",
    # laws
    "LAW_NAMES",
    "LAW_MEMORY",
    "LAW_PREDICTION",
    "LAW_INTEGRATION",
    "ATTENTION_DECAY",
    "N_LAWS",
    # scaling
    "MORPH_SCALE",
    "normalize_unsigned",
    "normalize_signed",
]
