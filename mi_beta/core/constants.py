"""Single source of truth for all MI-Beta numerical constants."""

from __future__ import annotations

import torch
from torch import Tensor

# ── Audio ──────────────────────────────────────────────────────────────────────
SAMPLE_RATE: int = 44_100
HOP_LENGTH: int = 256
FRAME_RATE: float = SAMPLE_RATE / HOP_LENGTH  # 172.265625 Hz
FRAME_DURATION_MS: float = 1000.0 / FRAME_RATE  # ~5.805 ms
N_FFT: int = 2048
N_MELS: int = 128

# ── R3 Spectral ───────────────────────────────────────────────────────────────
R3_DIM: int = 49
R3_CONSONANCE: tuple[int, int] = (0, 7)    # Group A: 7D
R3_ENERGY: tuple[int, int] = (7, 12)       # Group B: 5D
R3_TIMBRE: tuple[int, int] = (12, 21)      # Group C: 9D
R3_CHANGE: tuple[int, int] = (21, 25)      # Group D: 4D
R3_INTERACTIONS: tuple[int, int] = (25, 49) # Group E: 24D

# ── H3 Temporal ───────────────────────────────────────────────────────────────
N_HORIZONS: int = 32
N_MORPHS: int = 24
N_LAWS: int = 3
H3_TOTAL_DIM: int = N_HORIZONS * N_MORPHS * N_LAWS  # 2304
ATTENTION_DECAY: float = 3.0

HORIZON_MS: tuple[float, ...] = (
    5.8, 11.6, 17.4, 23.2, 34.8, 46.4,           # H0-H5:   sub-beat
    200, 250, 300, 350, 400, 450,                   # H6-H11:  beat
    525, 600, 700, 800, 1000, 1500,                 # H12-H17: beat-phrase
    2000, 3000, 5000, 8000, 15000, 25000,           # H18-H23: phrase-section
    36000, 60000, 120000, 200000, 414000,           # H24-H28: section-form
    600000, 800000, 981000,                          # H29-H31: piece
)

HORIZON_FRAMES: tuple[int, ...] = tuple(
    max(1, round(ms / 1000.0 * FRAME_RATE)) for ms in HORIZON_MS
)

MORPH_NAMES: tuple[str, ...] = (
    "value", "mean", "std", "median", "max", "range",
    "skewness", "kurtosis",
    "velocity", "velocity_mean", "velocity_std",
    "acceleration", "acceleration_mean", "acceleration_std",
    "periodicity", "smoothness", "curvature", "shape_period",
    "trend", "stability", "entropy", "zero_crossings", "peaks", "symmetry",
)

LAW_NAMES: tuple[str, ...] = ("memory", "prediction", "integration")

MORPH_SCALE: tuple[tuple[float, float], ...] = (
    (6.0, 0.5),      # M0  value         [0,1] level
    (6.0, 0.5),      # M1  mean           [0,1] level
    (40.0, 0.0),     # M2  std            small positive
    (6.0, 0.5),      # M3  median         [0,1] level
    (6.0, 0.5),      # M4  max            [0,1] level
    (10.0, 0.25),    # M5  range          [0, ~0.5]
    (3.0, 0.0),      # M6  skewness       centered ~0
    (1.5, 0.0),      # M7  kurtosis       centered ~0
    (300.0, 0.0),    # M8  velocity       ~±0.003 std
    (300.0, 0.0),    # M9  velocity_mean  ~±0.003 std
    (200.0, 0.0),    # M10 velocity_std   small positive
    (500.0, 0.0),    # M11 acceleration   ~±0.001 std
    (500.0, 0.0),    # M12 accel_mean     near-zero
    (400.0, 0.0),    # M13 accel_std      near-zero positive
    (6.0, 0.5),      # M14 periodicity    [0,1] level
    (6.0, 0.5),      # M15 smoothness     (0,1]
    (200.0, 0.0),    # M16 curvature      small positive
    (6.0, 0.5),      # M17 shape_period   sigmoid-mapped
    (1000.0, 0.0),   # M18 trend          ~±0.0005 std slope
    (6.0, 0.5),      # M19 stability      (0,1]
    (6.0, 0.5),      # M20 entropy        [0,1]
    (6.0, 0.5),      # M21 zero_crossings [0,1]
    (6.0, 0.5),      # M22 peaks          [0,1]
    (6.0, 0.5),      # M23 symmetry       (0,1]
)

# ── Brain Architecture ─────────────────────────────────────────────────────────
MECHANISM_DIM: int = 30
UNIT_EXECUTION_ORDER: tuple[str, ...] = (
    "SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU", "ARU", "RPU",
)
ALL_UNIT_NAMES: tuple[str, ...] = UNIT_EXECUTION_ORDER
INDEPENDENT_UNITS: tuple[str, ...] = (
    "SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU",
)
DEPENDENT_UNITS: tuple[str, ...] = ("ARU", "RPU")
MODEL_TIERS: tuple[str, ...] = ("alpha", "beta", "gamma")

# ── Circuits ───────────────────────────────────────────────────────────────────
CIRCUIT_NAMES: tuple[str, ...] = (
    "mesolimbic", "perceptual", "sensorimotor", "mnemonic", "salience", "imagery",
)
CIRCUITS: tuple[str, ...] = (
    "perceptual", "sensorimotor", "mnemonic", "mesolimbic", "salience",
)
N_CIRCUITS: int = len(CIRCUITS)

# ── Neuroscience Coefficients ──────────────────────────────────────────────────
BETA_NACC: float = 0.84    # NAcc binding potential ↔ pleasure (Salimpoor 2011)
BETA_CAUDATE: float = 0.71  # Caudate binding potential ↔ chills (Salimpoor 2011)


# ── Helper Functions ───────────────────────────────────────────────────────────

def h3_flat_index(horizon: int, morph: int, law: int) -> int:
    """Flat index into 2304D H3 space: h*72 + m*3 + l."""
    return horizon * (N_MORPHS * N_LAWS) + morph * N_LAWS + law


def scale_h3_value(value: Tensor, morph: int) -> Tensor:
    """Scale H3 value by morph's gain and bias. (B, T) → (B, T)."""
    gain, bias = MORPH_SCALE[morph]
    return gain * (value - bias)
