"""MI Space Layout — canonical dimension constants for the training pipeline.

These constants define the shape of every tensor in the MI system.
Imported by ``Musical_Intelligence.data`` modules and training scripts.
"""
from __future__ import annotations

# ── Audio ─────────────────────────────────────────────────────
SAMPLE_RATE: int = 44100
N_FFT: int = 2048
HOP_LENGTH: int = 256
N_MELS: int = 128
FRAME_RATE: float = SAMPLE_RATE / HOP_LENGTH  # 172.27 Hz

# ── Pipeline dimensions ──────────────────────────────────────
COCHLEA_DIM: int = 128   # mel spectrogram bins
R3_DIM: int = 128        # R³ spectral features (11 groups, A-K)
R3_BRAIN_DIM: int = 49   # R³ features visible to brain (groups A-E)
C3_DIM: int = 1006       # full C³ (all 96 nuclei exportable dims)

# ── BCH nucleus (POC) ────────────────────────────────────────
BCH_DIM: int = 12        # BCH total output (E4 + M2 + P3 + F3)
BCH_EXPORTABLE_DIM: int = 6  # BCH external+hybrid dims (P3 + F3 = [6:12])

# ── BCH Computational Manifold ──────────────────────────────
# The full information state that BCH reads and produces:
#   R³ active dims  → 12D (indices BCH reads from r3_features in compute())
#   H³ active dims  → 16D (BCH's 16 temporal demand tuples)
#   BCH output      → 12D (the computed consonance features)
# Total = 40D — a single manifold for training inverse heads.
BCH_R3_ACTIVE_INDICES: tuple = (0, 1, 2, 3, 4, 5, 6, 14, 17, 18, 19, 20)
BCH_R3_ACTIVE_DIM: int = len(BCH_R3_ACTIVE_INDICES)   # 12
BCH_H3_DEMAND_COUNT: int = 16                          # 16 H³ tuples
BCH_MANIFOLD_DIM: int = BCH_R3_ACTIVE_DIM + BCH_H3_DEMAND_COUNT + BCH_DIM  # 40

# Manifold segment offsets (for per-layer reporting)
MANIFOLD_R3_START: int = 0
MANIFOLD_R3_END: int = BCH_R3_ACTIVE_DIM                          # 0:12
MANIFOLD_H3_START: int = BCH_R3_ACTIVE_DIM                        # 12
MANIFOLD_H3_END: int = BCH_R3_ACTIVE_DIM + BCH_H3_DEMAND_COUNT    # 28
MANIFOLD_BCH_START: int = MANIFOLD_H3_END                         # 28
MANIFOLD_BCH_END: int = BCH_MANIFOLD_DIM                          # 40

# Semantic names for each manifold dimension (for reports)
BCH_R3_ACTIVE_NAMES: tuple = (
    "roughness", "sethares", "helmholtz", "stumpf", "sens_pleasant",
    "inharmonicity", "harmonic_dev", "tonalness", "spectral_autocorr",
    "trist1", "trist2", "trist3",
)
BCH_H3_DEMAND_NAMES: tuple = (
    "h3:rough_H0_val_integ",       # (0, 0, 0, 2)
    "h3:rough_H3_mean_integ",      # (0, 3, 1, 2)
    "h3:rough_H6_trend_mem",       # (0, 6, 18, 0)
    "h3:helm_H0_val_integ",        # (2, 0, 0, 2)
    "h3:helm_H3_mean_integ",       # (2, 3, 1, 2)
    "h3:stumpf_H0_val_integ",      # (3, 0, 0, 2)
    "h3:stumpf_H6_mean_mem",       # (3, 6, 1, 0)
    "h3:inharm_H0_val_integ",      # (5, 0, 0, 2)
    "h3:inharm_H3_trend_mem",      # (5, 3, 18, 0)
    "h3:hdev_H0_val_integ",        # (6, 0, 0, 2)
    "h3:hdev_H3_mean_mem",         # (6, 3, 1, 0)
    "h3:trist1_H0_val_integ",      # (18, 0, 0, 2)
    "h3:trist2_H0_val_integ",      # (19, 0, 0, 2)
    "h3:trist3_H0_val_integ",      # (20, 0, 0, 2)
    "h3:coupling_H3_val_integ",    # (41, 3, 0, 2)
    "h3:coupling_H6_period_integ", # (41, 6, 14, 2)
)
BCH_OUTPUT_NAMES: tuple = (
    "E0:f01_nps", "E1:f02_harmonicity", "E2:f03_hierarchy", "E3:f04_ffr_behavior",
    "M0:nps_t", "M1:harm_interval",
    "P0:consonance_signal", "P1:template_match", "P2:neural_pitch",
    "F0:consonance_pred", "F1:pitch_propagation", "F2:interval_expect",
)

# ── Brain regions and neurochemicals ─────────────────────────
RAM_DIM: int = 26         # Region Activation Map (26 brain regions)
NEURO_DIM: int = 4        # Neurochemicals: DA, NE, OPI, 5HT
PSI_DIM: int = 27         # Ψ³ psychological interpretation
