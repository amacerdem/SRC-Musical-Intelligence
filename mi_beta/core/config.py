"""Runtime configuration for MI-Beta pipeline."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from .constants import (
    SAMPLE_RATE, HOP_LENGTH, N_FFT, N_MELS,
    MECHANISM_DIM, UNIT_EXECUTION_ORDER, R3_DIM,
)


@dataclass
class MIBetaConfig:
    # Audio
    sample_rate: int = SAMPLE_RATE
    hop_length: int = HOP_LENGTH
    n_fft: int = N_FFT
    n_mels: int = N_MELS

    # R3 groups
    r3_groups: Tuple[str, ...] = (
        "consonance", "energy", "timbre", "change", "interactions",
    )

    # Brain control
    active_units: Optional[Tuple[str, ...]] = None    # None = all 9 units
    active_models: Optional[Tuple[str, ...]] = None   # None = all models

    # Mechanism
    mechanism_dim: int = MECHANISM_DIM

    # Device
    device: str = "cpu"

    # Streaming
    streaming: bool = False
    chunk_size: Optional[int] = None

    def __post_init__(self) -> None:
        if self.active_units is not None:
            for u in self.active_units:
                if u not in UNIT_EXECUTION_ORDER:
                    raise ValueError(
                        f"Unknown unit '{u}'. Valid: {UNIT_EXECUTION_ORDER}"
                    )

    @property
    def frame_rate(self) -> float:
        return self.sample_rate / self.hop_length

    @property
    def r3_dim(self) -> int:
        return R3_DIM

    @property
    def cochlea_dim(self) -> int:
        return self.n_mels

    def is_unit_active(self, unit_name: str) -> bool:
        if self.active_units is None:
            return True
        return unit_name in self.active_units

    def is_model_active(self, model_name: str) -> bool:
        if self.active_models is None:
            return True
        return model_name in self.active_models


MI_BETA_CONFIG = MIBetaConfig()
