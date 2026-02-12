"""
MI-Beta Core Constants -- SINGLE SOURCE OF TRUTH

All numerical constants for the Musical Intelligence Beta system.
Changing a value here propagates everywhere.

Extends mi/core/constants.py with multi-model brain architecture constants.
"""

from __future__ import annotations

# =====================================================================
# AUDIO
# =====================================================================

SAMPLE_RATE: int = 44_100
HOP_LENGTH: int = 256
FRAME_RATE: float = SAMPLE_RATE / HOP_LENGTH  # 172.265625 Hz
FRAME_DURATION_MS: float = 1000.0 * HOP_LENGTH / SAMPLE_RATE  # ~5.805 ms
N_FFT: int = 2048
N_MELS: int = 128

# =====================================================================
# R3 SPECTRAL
# =====================================================================

R3_DIM: int = 49  # Total R3 features per frame

# Group boundaries [start, end)
R3_CONSONANCE: tuple[int, int] = (0, 7)      # Group A: 7D
R3_ENERGY: tuple[int, int] = (7, 12)          # Group B: 5D
R3_TIMBRE: tuple[int, int] = (12, 21)         # Group C: 9D
R3_CHANGE: tuple[int, int] = (21, 25)         # Group D: 4D
R3_INTERACTIONS: tuple[int, int] = (25, 49)   # Group E: 24D

# =====================================================================
# H3 TEMPORAL
# =====================================================================

N_HORIZONS: int = 32
N_MORPHS: int = 24
N_LAWS: int = 3
H3_TOTAL_DIM: int = N_HORIZONS * N_MORPHS * N_LAWS  # 2304

# All 32 horizon durations in milliseconds
HORIZON_MS: tuple[float, ...] = (
    5.8, 11.6, 17.4, 23.2, 34.8, 46.4,      # H0-H5: sub-beat
    200, 250, 300, 350, 400, 450,              # H6-H11: beat
    525, 600, 700, 800, 1000, 1500,            # H12-H17: beat-phrase
    2000, 3000, 5000, 8000, 15000, 25000,      # H18-H23: phrase-section
    36000, 60000, 120000, 200000, 414000,      # H24-H28: section-form
    600000, 800000, 981000,                     # H29-H31: piece
)

# Frame counts for each horizon (at 172.27 Hz)
HORIZON_FRAMES: tuple[int, ...] = tuple(
    max(1, round(ms / 1000.0 * FRAME_RATE)) for ms in HORIZON_MS
)

# Attention decay constant: A(dt) = exp(-3|dt|/H)
ATTENTION_DECAY: float = 3.0

# =====================================================================
# MORPH NAMES (24 morphological features)
# =====================================================================

MORPH_NAMES: tuple[str, ...] = (
    "value",             # M0:  Attention-weighted mean
    "mean",              # M1:  Unweighted mean
    "std",               # M2:  Standard deviation
    "median",            # M3:  Median
    "max",               # M4:  Maximum
    "range",             # M5:  Max - Min
    "skewness",          # M6:  Distribution skew
    "kurtosis",          # M7:  Distribution peakedness
    "velocity",          # M8:  First derivative (dR3/dt)
    "velocity_mean",     # M9:  Mean of velocity
    "velocity_std",      # M10: Velocity variance (jerk proxy)
    "acceleration",      # M11: Second derivative
    "acceleration_mean", # M12: Mean acceleration
    "acceleration_std",  # M13: Acceleration variance
    "periodicity",       # M14: Autocorrelation peak
    "smoothness",        # M15: 1/(1+|jerk|/sigma) -- scale-invariant
    "curvature",         # M16: Spectral curvature
    "shape_period",      # M17: Oscillation period
    "trend",             # M18: Linear regression slope
    "stability",         # M19: 1/(1+var/sigma^2)
    "entropy",           # M20: Shannon entropy
    "zero_crossings",    # M21: Sign change count
    "peaks",             # M22: Local maxima count
    "symmetry",          # M23: Forward/backward symmetry
)

# Law names (3 temporal perspectives)
LAW_NAMES: tuple[str, ...] = (
    "memory",       # L0: Forward/causal (past -> now)
    "prediction",   # L1: Backward (now -> future)
    "integration",  # L2: Bidirectional (past <-> future)
)

# =====================================================================
# NEUROSCIENCE COEFFICIENTS (from Salimpoor 2011)
# =====================================================================

BETA_NACC: float = 0.84     # NAcc binding potential <-> pleasure (r=0.84)
BETA_CAUDATE: float = 0.71  # Caudate binding potential <-> chills (r=0.71)

# =====================================================================
# CIRCUIT DEFINITIONS
# =====================================================================

CIRCUIT_NAMES: tuple[str, ...] = (
    "mesolimbic",    # Reward & Pleasure
    "perceptual",    # Hearing & Pattern
    "sensorimotor",  # Rhythm & Movement
    "mnemonic",      # Memory & Familiarity
    "salience",      # Attention & Novelty
    "imagery",       # Simulation & Prediction
)

# =====================================================================
# MORPH SCALING -- gain and bias for activation inputs
# =====================================================================

# (gain, bias) per morph index. Applied as: gain * (h3_value - bias)
# Level morphs in [0,1] -> center at bias, scale to fill sigmoid range.
# Derivative morphs near 0 -> large gain to amplify real signal.
# Calibrated against Swan Lake H3 signal ranges (Feb 2026).
MORPH_SCALE: tuple[tuple[float, float], ...] = (
    (6.0, 0.5),       # M0  value: att-weighted mean [0,1]
    (6.0, 0.5),       # M1  mean [0,1]
    (40.0, 0.0),      # M2  std: small positive
    (6.0, 0.5),       # M3  median [0,1]
    (6.0, 0.5),       # M4  max [0,1]
    (10.0, 0.25),     # M5  range [0, ~0.5]
    (3.0, 0.0),       # M6  skewness: centered ~0
    (1.5, 0.0),       # M7  kurtosis: centered ~0
    (300.0, 0.0),     # M8  velocity: ~+/-0.003 std
    (300.0, 0.0),     # M9  velocity_mean: ~+/-0.003 std
    (200.0, 0.0),     # M10 velocity_std: small positive
    (500.0, 0.0),     # M11 acceleration: ~+/-0.001 std
    (500.0, 0.0),     # M12 acceleration_mean: near-zero
    (400.0, 0.0),     # M13 acceleration_std: near-zero positive
    (6.0, 0.5),       # M14 periodicity [0,1]
    (6.0, 0.5),       # M15 smoothness (0,1]
    (200.0, 0.0),     # M16 curvature: small positive
    (6.0, 0.5),       # M17 shape_period: sigmoid-mapped
    (1000.0, 0.0),    # M18 trend: ~+/-0.0005 std slope
    (6.0, 0.5),       # M19 stability (0,1]
    (6.0, 0.5),       # M20 entropy [0,1]
    (6.0, 0.5),       # M21 zero_crossings [0,1]
    (6.0, 0.5),       # M22 peaks [0,1]
    (6.0, 0.5),       # M23 symmetry (0,1]
)


# =====================================================================
# HELPERS
# =====================================================================

def h3_flat_index(horizon: int, morph: int, law: int) -> int:
    """Flat index into 2304D H3 space: h*72 + m*3 + l."""
    return horizon * (N_MORPHS * N_LAWS) + morph * N_LAWS + law


def scale_h3_value(value: "Tensor", morph: int) -> "Tensor":
    """Scale a single H3 value by its morph's gain and bias.

    Args:
        value: (B, T) raw H3 morph value
        morph: morph index (0-23)

    Returns:
        (B, T) scaled value
    """
    g, b = MORPH_SCALE[morph]
    return g * (value - b)


# =====================================================================
# mi_beta EXTENSIONS
# =====================================================================

# Mechanism standard size -- each mechanism within a model produces
# a fixed-size output vector for uniform stacking and interpretation.
MECHANISM_DIM: int = 30

# Unit execution order (dependency-resolved).
# Phase 2 units are independent -- they read only from R3/H3.
# Phase 4 units (ARU, RPU) depend on pathway outputs from other units,
# so they must execute AFTER the independent units and pathway merging.
UNIT_EXECUTION_ORDER: tuple[str, ...] = (
    # Phase 2: Independent units
    "SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU",
    # Phase 4: Dependent units (after pathways)
    "ARU", "RPU",
)

# All cognitive unit names
ALL_UNIT_NAMES: tuple[str, ...] = UNIT_EXECUTION_ORDER

# Model tier names -- evidence confidence levels from C3 meta-analysis.
# alpha: foundational, >90% confidence, k>=10 studies
# beta: integrative, 70-90% confidence, k>=5 studies
# gamma: theoretical, <70% confidence, k<5 studies
MODEL_TIERS: tuple[str, ...] = ("alpha", "beta", "gamma")

# Circuit names -- neural circuits that multiple units participate in.
# Used for cross-unit pathway routing and integration.
CIRCUITS: tuple[str, ...] = (
    "perceptual",     # Hearing & pattern recognition
    "sensorimotor",   # Rhythm & movement entrainment
    "mnemonic",       # Memory consolidation & familiarity
    "mesolimbic",     # Reward & dopaminergic pleasure
    "salience",       # Attention, novelty, & arousal gating
)

# Number of circuits
N_CIRCUITS: int = len(CIRCUITS)
