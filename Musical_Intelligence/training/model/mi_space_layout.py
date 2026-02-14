"""MI-Space Layout -- Single source of truth for the 1366D manifold structure.

Defines slice boundaries, dimension constants, and the MISpaceLayout registry
that maps every region of the 1366D MI-space to its semantic meaning.

MI-Space structure::

    [0:128]       Cochlea   128D  Mel spectrogram (the sound itself)
    [128:256]     R3        128D  Spectral features (11 groups A-K)
    [256:1262]    C3       1006D  Cognitive models (9 units, 96 models)
    [1262:1366]   L3        104D  Semantic language (8 groups alpha-theta)
    ---------------------------------------------------------------
    Total                  1366D  @ 172.27 Hz frame rate
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

# ======================================================================
# Audio / Frame Constants
# ======================================================================

SAMPLE_RATE: int = 44100
HOP_LENGTH: int = 256
N_FFT: int = 2048
N_MELS: int = 128
FRAME_RATE_HZ: float = SAMPLE_RATE / HOP_LENGTH  # 172.265625 Hz
FRAME_DURATION_MS: float = 1000.0 / FRAME_RATE_HZ  # ~5.805 ms

# ======================================================================
# MI-Space Dimension Constants
# ======================================================================

COCHLEA_DIM: int = 128
R3_DIM: int = 128
C3_DIM: int = 1006
L3_DIM: int = 104
MI_SPACE_DIM: int = COCHLEA_DIM + R3_DIM + C3_DIM + L3_DIM  # 1366

# H3 auxiliary head (training only, pruned after)
H3_AUX_DIM: int = 5210

# ======================================================================
# MI-Space Slice Boundaries
# ======================================================================

COCHLEA_START: int = 0
COCHLEA_END: int = COCHLEA_START + COCHLEA_DIM          # 128
R3_START: int = COCHLEA_END                              # 128
R3_END: int = R3_START + R3_DIM                          # 256
C3_START: int = R3_END                                   # 256
C3_END: int = C3_START + C3_DIM                          # 1262
L3_START: int = C3_END                                   # 1262
L3_END: int = L3_START + L3_DIM                          # 1366

COCHLEA_SLICE = slice(COCHLEA_START, COCHLEA_END)
R3_SLICE = slice(R3_START, R3_END)
C3_SLICE = slice(C3_START, C3_END)
L3_SLICE = slice(L3_START, L3_END)

# ======================================================================
# MI-Core Hyperparameters
# ======================================================================

BACKBONE_HIDDEN_DIM: int = 2048
BACKBONE_N_LAYERS: int = 24
MAMBA_STATE_DIM: int = 64
MAMBA_CONV_KERNEL: int = 4
MAMBA_EXPAND: int = 2
SPARSE_ATTN_EVERY: int = 4       # Every 4th layer is sparse attention
SPARSE_ATTN_WINDOW: int = 256    # ~1.5s local window
SPARSE_ATTN_GLOBAL_TOKENS: int = 16
SPARSE_ATTN_N_HEADS: int = 16

N_EXPERTS: int = 4
EXPERT_CAPACITY: float = 1.25
TOP_K_EXPERTS: int = 3

PLANNING_HORIZON_FRAMES: int = 344   # ~2 seconds ahead
PLANNING_HORIZON_STEPS: int = 8

# Motor encoder
MOTOR_CHANNEL_DIMS = {
    "touch": 3,
    "mediapipe": 63,
    "midi_notes": 128,
    "midi_cc": 128,
    "gamepad": 8,
    "accelerometer": 3,
    "emotion": 4,
}
MOTOR_TOTAL_DIM: int = sum(MOTOR_CHANNEL_DIMS.values())  # 337
MOTOR_EMBED_DIM: int = 256


# ======================================================================
# MISpaceLayout -- Runtime registry
# ======================================================================

@dataclass(frozen=True)
class MISpaceLayout:
    """Registry of all MI-space slices with unit-level C3 sub-slices.

    Constructed once at system init from BrainOrchestrator.unit_slices,
    then frozen for the lifetime of the training run.

    Attributes:
        unit_slices: Maps unit name (e.g. ``"SPU"``) to ``(start, end)``
            within the 1006D C3 region, **relative to C3_START**.
        unit_order: Canonical unit ordering.
    """

    unit_slices: Dict[str, Tuple[int, int]] = field(default_factory=dict)
    unit_order: Tuple[str, ...] = (
        "SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU", "ARU", "RPU",
    )

    def c3_slice_absolute(self, unit_name: str) -> slice:
        """Return the absolute MI-space slice for a C3 unit."""
        start, end = self.unit_slices[unit_name]
        return slice(C3_START + start, C3_START + end)

    def validate(self) -> None:
        """Sanity-check that unit slices sum to C3_DIM."""
        total = sum(end - start for start, end in self.unit_slices.values())
        if total != C3_DIM:
            raise ValueError(
                f"Unit slices sum to {total}, expected {C3_DIM}"
            )


def build_layout_from_orchestrator() -> MISpaceLayout:
    """Build MISpaceLayout by instantiating BrainOrchestrator.

    This triggers all 96 model constructors to determine exact unit dims,
    then freezes the layout.
    """
    from Musical_Intelligence.brain.orchestrator import BrainOrchestrator

    orch = BrainOrchestrator()
    unit_slices = {}
    offset = 0
    for name in ("SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU", "ARU", "RPU"):
        dim = orch.unit_dims[name]
        unit_slices[name] = (offset, offset + dim)
        offset += dim

    layout = MISpaceLayout(unit_slices=unit_slices)
    layout.validate()
    return layout
