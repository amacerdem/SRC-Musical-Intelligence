"""H3 morph constants -- 24 statistical descriptors for temporal morphology.

Defines morph names, category groupings, minimum window requirements, and the
set of signed morphs that require centered normalization.

Source of truth
---------------
- Docs/H3/H3-TEMPORAL-ARCHITECTURE.md  Section 5 (morph table, categories)
- Docs/H3/Registry/MorphCatalog.md     authoritative morph catalog
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Number of morphs
# ---------------------------------------------------------------------------
N_MORPHS: int = 24

# ---------------------------------------------------------------------------
# MORPH_NAMES -- canonical names for the 24 morphs (M0-M23)
# ---------------------------------------------------------------------------
MORPH_NAMES: tuple[str, ...] = (
    "value",                # M0   attention-weighted mean
    "mean",                 # M1   arithmetic mean
    "std",                  # M2   standard deviation
    "median",               # M3   median
    "max",                  # M4   maximum
    "range",                # M5   max - min
    "skewness",             # M6   third standardized moment
    "kurtosis",             # M7   fourth standardized moment (excess)
    "velocity",             # M8   first temporal derivative
    "velocity_mean",        # M9   mean of velocity
    "velocity_std",         # M10  std of velocity
    "acceleration",         # M11  second temporal derivative
    "acceleration_mean",    # M12  mean of acceleration
    "acceleration_std",     # M13  std of acceleration
    "periodicity",          # M14  autocorrelation peak
    "smoothness",           # M15  inverse jerk
    "curvature",            # M16  second derivative / arc length
    "shape_period",         # M17  zero-crossing interval
    "trend",                # M18  linear regression slope
    "stability",            # M19  inverse normalized variance
    "entropy",              # M20  Shannon entropy
    "zero_crossings",       # M21  mean-crossing count
    "peaks",                # M22  local-maxima count
    "symmetry",             # M23  forward/backward correlation
)

# ---------------------------------------------------------------------------
# MORPH_CATEGORIES -- 6 perceptual categories from H3-TEMPORAL-ARCHITECTURE
#   Section 5.2
# ---------------------------------------------------------------------------
MORPH_CATEGORIES: dict[str, frozenset[int]] = {
    "Level":       frozenset({0, 1, 3, 4}),
    "Dispersion":  frozenset({2, 5, 19}),
    "Shape":       frozenset({6, 7, 16, 23}),
    "Dynamics":    frozenset({8, 9, 10, 11, 12, 13, 15, 18, 21}),
    "Rhythm":      frozenset({14, 17, 22}),
    "Information": frozenset({20}),
}

# ---------------------------------------------------------------------------
# MORPH_MIN_WINDOW -- minimum frames required for each morph to produce a
#   valid result.  Values from H3-TEMPORAL-ARCHITECTURE Section 5.1 table.
# ---------------------------------------------------------------------------
MORPH_MIN_WINDOW: tuple[int, ...] = (
    1,   # M0  value
    1,   # M1  mean
    2,   # M2  std
    1,   # M3  median
    1,   # M4  max
    2,   # M5  range
    3,   # M6  skewness
    4,   # M7  kurtosis
    2,   # M8  velocity
    3,   # M9  velocity_mean
    3,   # M10 velocity_std
    3,   # M11 acceleration
    4,   # M12 acceleration_mean
    4,   # M13 acceleration_std
    8,   # M14 periodicity
    4,   # M15 smoothness
    3,   # M16 curvature
    8,   # M17 shape_period
    3,   # M18 trend
    3,   # M19 stability
    4,   # M20 entropy
    3,   # M21 zero_crossings
    3,   # M22 peaks
    4,   # M23 symmetry
)

# ---------------------------------------------------------------------------
# SIGNED_MORPHS -- morphs whose raw output spans a signed range centred at
#   zero.  These use the signed normalization formula:
#       output = clamp((raw / scale + 1) / 2, 0, 1)
#   Source: Docs/H3/Morphology/MorphScaling.md  Section 2.2
# ---------------------------------------------------------------------------
SIGNED_MORPHS: frozenset[int] = frozenset({
    6,   # M6  skewness
    8,   # M8  velocity
    9,   # M9  velocity_mean
    11,  # M11 acceleration
    12,  # M12 acceleration_mean
    16,  # M16 curvature
    18,  # M18 trend
    23,  # M23 symmetry
})
