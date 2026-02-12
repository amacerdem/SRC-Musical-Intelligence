"""
MI Configuration — Runtime settings with sensible defaults.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from .constants import (
    SAMPLE_RATE,
    HOP_LENGTH,
    N_FFT,
    N_MELS,
    R3_DIM,
)


@dataclass
class MIConfig:
    """Configuration for the MI pipeline.

    Immutable after creation. Override via keyword arguments:
        config = MIConfig(device="cuda")
    """

    # Audio settings
    sample_rate: int = SAMPLE_RATE
    hop_length: int = HOP_LENGTH
    n_fft: int = N_FFT
    n_mels: int = N_MELS

    # R³ settings
    r3_dim: int = R3_DIM
    r3_groups: tuple[str, ...] = (
        "consonance", "energy", "timbre", "change", "interactions"
    )

    # Device
    device: str = "cpu"

    # Streaming
    streaming: bool = False
    chunk_size: Optional[int] = None  # frames per chunk (streaming mode)

    def __post_init__(self) -> None:
        if isinstance(self.r3_groups, list):
            object.__setattr__(self, "r3_groups", tuple(self.r3_groups))

    @property
    def frame_rate(self) -> float:
        return self.sample_rate / self.hop_length


# Singleton — import and use directly
MI_CONFIG = MIConfig()
