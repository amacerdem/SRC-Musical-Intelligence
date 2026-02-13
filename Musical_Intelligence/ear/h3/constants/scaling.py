"""H3 morph scaling -- per-morph normalization to [0, 1].

Provides the MORPH_SCALE array and two normalization helpers that work with
both plain floats and ``torch.Tensor`` inputs.

Source of truth
---------------
- Docs/H3/Morphology/MorphScaling.md   MORPH_SCALE array, normalization formulas
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md  Section 5.3
"""

from __future__ import annotations

from typing import TypeVar, Union

from .morphs import SIGNED_MORPHS

# ---------------------------------------------------------------------------
# MORPH_SCALE -- per-morph normalization denominators
# ---------------------------------------------------------------------------
MORPH_SCALE: tuple[float, ...] = (
    1.0,    # M0  value              -- R3 input already [0,1]
    1.0,    # M1  mean               -- R3 input already [0,1]
    0.25,   # M2  std                -- typical max ~0.25
    1.0,    # M3  median             -- R3 input already [0,1]
    1.0,    # M4  max                -- R3 input already [0,1]
    1.0,    # M5  range              -- max possible 1.0
    2.0,    # M6  skewness           -- typical range [-2, 2]          (signed)
    5.0,    # M7  kurtosis           -- typical range [1, 5]
    0.1,    # M8  velocity           -- typical max ~0.1/frame         (signed)
    0.05,   # M9  velocity_mean      -- smoothed velocity              (signed)
    0.05,   # M10 velocity_std       -- velocity dispersion
    0.01,   # M11 acceleration       -- typical max ~0.01/frame^2      (signed)
    0.005,  # M12 acceleration_mean  -- smoothed acceleration          (signed)
    0.005,  # M13 acceleration_std   -- acceleration dispersion
    1.0,    # M14 periodicity        -- autocorrelation [0,1]
    1.0,    # M15 smoothness         -- [0,1] by construction
    0.1,    # M16 curvature          -- typical max ~0.1               (signed)
    100.0,  # M17 shape_period       -- frames; max ~100 frames
    0.01,   # M18 trend              -- slope per frame                (signed)
    1.0,    # M19 stability          -- [0,1] by construction
    3.0,    # M20 entropy            -- max ~log2(16) = 4.0 bits
    20.0,   # M21 zero_crossings     -- max ~20 crossings
    10.0,   # M22 peaks              -- max ~10 peaks
    1.0,    # M23 symmetry           -- correlation [-1,1]             (signed)
)

# ---------------------------------------------------------------------------
# Type alias for values that may be float or Tensor
# ---------------------------------------------------------------------------
_T = TypeVar("_T", float, "torch.Tensor")  # noqa: F821 -- torch is optional


def _clamp(x: _T, lo: float, hi: float) -> _T:
    """Clamp *x* to [lo, hi], supporting both float and torch.Tensor."""
    try:
        # torch.Tensor path
        return x.clamp(min=lo, max=hi)  # type: ignore[union-attr]
    except AttributeError:
        # plain float / int path
        if x < lo:
            return lo  # type: ignore[return-value]
        if x > hi:
            return hi  # type: ignore[return-value]
        return x


# ---------------------------------------------------------------------------
# Public normalization functions
# ---------------------------------------------------------------------------

def normalize_unsigned(raw: Union[float, "torch.Tensor"], scale: float) -> Union[float, "torch.Tensor"]:  # noqa: F821
    """Normalize an unsigned morph value to [0, 1].

    Formula::

        output = clamp(raw / scale, 0, 1)

    Parameters
    ----------
    raw : float or torch.Tensor
        Raw morph output (expected non-negative).
    scale : float
        ``MORPH_SCALE[morph_idx]`` for the morph being normalized.

    Returns
    -------
    float or torch.Tensor
        Value(s) in [0, 1].
    """
    return _clamp(raw / scale, 0.0, 1.0)


def normalize_signed(raw: Union[float, "torch.Tensor"], scale: float) -> Union[float, "torch.Tensor"]:  # noqa: F821
    """Normalize a signed morph value to [0, 1] with zero mapped to 0.5.

    Formula::

        output = clamp((raw / scale + 1) / 2, 0, 1)

    This maps:
    - ``raw =  0``       to ``0.5``
    - ``raw = +scale``   to ``1.0``
    - ``raw = -scale``   to ``0.0``

    Parameters
    ----------
    raw : float or torch.Tensor
        Raw morph output (may be positive or negative).
    scale : float
        ``MORPH_SCALE[morph_idx]`` for the morph being normalized.

    Returns
    -------
    float or torch.Tensor
        Value(s) in [0, 1], with zero centred at 0.5.
    """
    return _clamp((raw / scale + 1.0) / 2.0, 0.0, 1.0)
