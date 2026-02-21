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
R3_DIM: int = 97         # R³ spectral features (9 groups, A-K excl. E,I)
R3_BRAIN_DIM: int = 97   # R³ features visible to brain (9 groups A-K excl. E,I)
C3_DIM: int = 1006       # full C³ (all 96 nuclei exportable dims)

# ── Brain regions and neurochemicals ─────────────────────────
RAM_DIM: int = 26         # Region Activation Map (26 brain regions)
NEURO_DIM: int = 4        # Neurochemicals: DA, NE, OPI, 5HT
PSI_DIM: int = 27         # Ψ³ psychological interpretation

# ── BCH nucleus (POC) ────────────────────────────────────────
BCH_DIM: int = 16        # BCH total output: E(4) + M(4) + P(4) + F(4)
BCH_EXPORTABLE_DIM: int = 8  # BCH external+hybrid dims (P4 + F4 = [8:16])

# ── BCH Computational Manifold ──────────────────────────────
# The full information state that BCH reads and produces:
#   R³ active dims  → 16D (indices BCH reads from r3_features in compute())
#   H³ active dims  → 50D (BCH's 50 temporal demand tuples: 21 L2 + 17 L0 + 12 L1)
#   BCH output      → 16D (E4 + Memory4 + Present4 + Future4)
#   RAM             → 26D (Region Activation Map — spatial brain state)
#   Neuro           → 4D  (Neurochemical state — DA, NE, OPI, 5HT)
# Total = 112D — a single manifold for training inverse heads.
BCH_R3_ACTIVE_INDICES: tuple = (
    # Consonance group A [0:7]
    0, 1, 2, 3, 4, 5, 6,
    # Timbre group C [12:21]
    14, 17, 18, 19, 20,
    # Pitch & Chroma group F [25:41] (post-freeze, was [49:65])
    38, 39,
    # Harmony group H [51:63] (post-freeze, was [75:87])
    51, 60,
)
BCH_R3_ACTIVE_DIM: int = len(BCH_R3_ACTIVE_INDICES)   # 16
BCH_H3_DEMAND_COUNT: int = 50                          # 50 H³ tuples
BCH_MANIFOLD_DIM: int = (
    BCH_R3_ACTIVE_DIM + BCH_H3_DEMAND_COUNT + BCH_DIM + RAM_DIM + NEURO_DIM
)  # 112

# Manifold segment offsets (for per-layer reporting)
MANIFOLD_R3_START: int = 0
MANIFOLD_R3_END: int = BCH_R3_ACTIVE_DIM                          # 0:16
MANIFOLD_H3_START: int = BCH_R3_ACTIVE_DIM                        # 16
MANIFOLD_H3_END: int = BCH_R3_ACTIVE_DIM + BCH_H3_DEMAND_COUNT    # 66
MANIFOLD_BCH_START: int = MANIFOLD_H3_END                         # 66
MANIFOLD_BCH_END: int = MANIFOLD_BCH_START + BCH_DIM              # 82
MANIFOLD_RAM_START: int = MANIFOLD_BCH_END                        # 82
MANIFOLD_RAM_END: int = MANIFOLD_RAM_START + RAM_DIM              # 108
MANIFOLD_NEURO_START: int = MANIFOLD_RAM_END                      # 108
MANIFOLD_NEURO_END: int = MANIFOLD_NEURO_START + NEURO_DIM        # 112

# Semantic names for each manifold dimension (for reports)
BCH_R3_ACTIVE_NAMES: tuple = (
    # A: Consonance [0:7]
    "roughness", "sethares", "helmholtz", "stumpf", "sens_pleasant",
    "inharmonicity", "harmonic_dev",
    # C: Timbre
    "tonalness", "spectral_autocorr",
    "trist1", "trist2", "trist3",
    # F: Pitch & Chroma
    "pitch_class_entropy", "pitch_salience",
    # H: Harmony
    "key_clarity", "tonal_stability",
)
BCH_H3_DEMAND_NAMES: tuple = (
    # Present demands (L2 = Integration, 21 tuples)
    "h3:rough_H0_val_integ",       # (0, 0, 0, 2)
    "h3:rough_H3_mean_integ",      # (0, 3, 1, 2)
    "h3:helm_H0_val_integ",        # (2, 0, 0, 2)
    "h3:helm_H3_mean_integ",       # (2, 3, 1, 2)
    "h3:stumpf_H0_val_integ",      # (3, 0, 0, 2)
    "h3:inharm_H0_val_integ",      # (5, 0, 0, 2)
    "h3:hdev_H0_val_integ",        # (6, 0, 0, 2)
    "h3:trist1_H0_val_integ",      # (18, 0, 0, 2)
    "h3:trist2_H0_val_integ",      # (19, 0, 0, 2)
    "h3:trist3_H0_val_integ",      # (20, 0, 0, 2)
    "h3:coupling_H3_val_integ",    # (41, 3, 0, 2)
    "h3:coupling_H6_period_integ", # (41, 6, 14, 2)
    "h3:pce_H0_val_integ",         # (38, 0, 0, 2)
    "h3:pce_H3_mean_integ",        # (38, 3, 1, 2)
    "h3:pitchsal_H0_val_integ",    # (39, 0, 0, 2)
    "h3:pitchsal_H3_val_integ",    # (39, 3, 0, 2)
    "h3:pitchsal_H6_val_integ",    # (39, 6, 0, 2)
    "h3:keyclarity_H3_val_integ",  # (51, 3, 0, 2)
    "h3:keyclarity_H3_mean_integ", # (51, 3, 1, 2)
    "h3:keyclarity_H6_val_integ",  # (51, 6, 0, 2)
    "h3:tonalstab_H3_val_integ",   # (60, 3, 0, 2)
    # Past demands (L0 = Memory, 17 tuples)
    "h3:rough_H6_trend_mem",       # (0, 6, 18, 0)
    "h3:rough_H12_mean_mem",       # (0, 12, 1, 0)
    "h3:rough_H16_mean_mem",       # (0, 16, 1, 0)
    "h3:helm_H12_mean_mem",        # (2, 12, 1, 0)
    "h3:helm_H18_mean_mem",        # (2, 18, 1, 0)
    "h3:stumpf_H6_mean_mem",       # (3, 6, 1, 0)
    "h3:stumpf_H16_mean_mem",      # (3, 16, 1, 0)
    "h3:inharm_H3_trend_mem",      # (5, 3, 18, 0)
    "h3:inharm_H12_mean_mem",      # (5, 12, 1, 0)
    "h3:hdev_H3_mean_mem",         # (6, 3, 1, 0)
    "h3:hdev_H12_mean_mem",        # (6, 12, 1, 0)
    "h3:pitchsal_H12_mean_mem",    # (39, 12, 1, 0)
    "h3:pitchsal_H18_mean_mem",    # (39, 18, 1, 0)
    "h3:keyclarity_H12_mean_mem",  # (51, 12, 1, 0)
    "h3:keyclarity_H18_mean_mem",  # (51, 18, 1, 0)
    "h3:tonalstab_H6_mean_mem",    # (60, 6, 1, 0)
    "h3:tonalstab_H18_mean_mem",   # (60, 18, 1, 0)
    # Future demands (L1 = Prediction, 12 tuples)
    "h3:rough_H6_mean_pred",       # (0, 6, 1, 1)
    "h3:rough_H12_trend_pred",     # (0, 12, 18, 1)
    "h3:helm_H6_mean_pred",        # (2, 6, 1, 1)
    "h3:helm_H12_mean_pred",       # (2, 12, 1, 1)
    "h3:stumpf_H6_mean_pred",      # (3, 6, 1, 1)
    "h3:inharm_H6_trend_pred",     # (5, 6, 18, 1)
    "h3:pitchsal_H6_mean_pred",    # (39, 6, 1, 1)
    "h3:pitchsal_H12_mean_pred",   # (39, 12, 1, 1)
    "h3:keyclarity_H6_mean_pred",  # (51, 6, 1, 1)
    "h3:keyclarity_H16_mean_pred", # (51, 16, 1, 1)
    "h3:tonalstab_H6_mean_pred",   # (60, 6, 1, 1)
    "h3:tonalstab_H12_mean_pred",  # (60, 12, 1, 1)
)
BCH_OUTPUT_NAMES: tuple = (
    # E-layer (4D): Extraction
    "E0:nps", "E1:harmonicity", "E2:hierarchy", "E3:ffr_behavior",
    # M-layer (4D): Memory (Past)
    "M0:consonance_memory", "M1:pitch_memory", "M2:tonal_memory", "M3:spectral_memory",
    # P-layer (4D): Present
    "P0:consonance_signal", "P1:template_match", "P2:neural_pitch", "P3:tonal_context",
    # F-layer (4D): Future
    "F0:consonance_forecast", "F1:pitch_forecast", "F2:tonal_forecast", "F3:interval_forecast",
)
BCH_RAM_NAMES: tuple = (
    # Cortical (0-11)
    "ram:A1_HG", "ram:STG", "ram:STS", "ram:IFG", "ram:dlPFC", "ram:vmPFC",
    "ram:OFC", "ram:ACC", "ram:SMA", "ram:PMC", "ram:AG", "ram:TP",
    # Subcortical (12-20)
    "ram:VTA", "ram:NAcc", "ram:caudate", "ram:amygdala", "ram:hippocampus",
    "ram:putamen", "ram:MGB", "ram:hypothalamus", "ram:insula",
    # Brainstem (21-25)
    "ram:IC", "ram:AN", "ram:CN", "ram:SOC", "ram:PAG",
)
BCH_NEURO_NAMES: tuple = (
    "neuro:DA", "neuro:NE", "neuro:OPI", "neuro:5HT",
)

# ── PSCL nucleus (Encoder, depth 1) ──────────────────────────────
PSCL_DIM: int = 16       # PSCL total output: E(4) + M(4) + P(4) + F(4)
PSCL_EXPORTABLE_DIM: int = 8   # PSCL external+hybrid dims (P4 + F4 = [8:16])

PSCL_R3_ACTIVE_INDICES: tuple = (
    # Consonance group A [0:7]
    4, 5,
    # Timbre group C [12:21]
    14, 15, 16, 17, 18,
    # Dynamics group D [21:25]
    22, 23, 24,
    # Pitch & Chroma group F [25:41]
    25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36,  # chroma [25:37]
    37, 39,                                             # pitch_height, pitch_salience
)
PSCL_R3_ACTIVE_DIM: int = len(PSCL_R3_ACTIVE_INDICES)  # 24
PSCL_H3_DEMAND_COUNT: int = 20                           # 20 H³ tuples (7 L2 + 9 L0 + 4 L1)

# PSCL Computational Manifold (for future inverse heads):
#   R³ active dims  → 24D
#   H³ active dims  → 20D
#   BCH output      → 16D (upstream relay)
#   PSCL output     → 16D
#   RAM             → 26D
#   Neuro           → 4D
# Total = 106D
PSCL_MANIFOLD_DIM: int = (
    PSCL_R3_ACTIVE_DIM + PSCL_H3_DEMAND_COUNT + BCH_DIM + PSCL_DIM
    + RAM_DIM + NEURO_DIM
)  # 106
