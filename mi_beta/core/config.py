"""
MI-Beta Configuration -- Runtime settings with sensible defaults.

Extends the mi/ config pattern with multi-model brain architecture
parameters: active units, active models, and device configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional, Tuple

from .constants import (
    SAMPLE_RATE,
    HOP_LENGTH,
    N_FFT,
    N_MELS,
    R3_DIM,
    UNIT_EXECUTION_ORDER,
    MECHANISM_DIM,
)


@dataclass
class MIBetaConfig:
    """Configuration for the MI-Beta pipeline.

    Immutable after creation. Override via keyword arguments::

        config = MIBetaConfig(device="cuda", active_units=("SPU", "ARU"))

    Active units/models filtering:
        - ``active_units = None`` means ALL units execute.
        - ``active_models = None`` means ALL models within active units execute.
        - Explicit tuples restrict to exactly those names.
    """

    # ── Audio settings (identical to mi/) ──────────────────────────────
    sample_rate: int = SAMPLE_RATE
    hop_length: int = HOP_LENGTH
    n_fft: int = N_FFT
    n_mels: int = N_MELS

    # ── R3 settings ────────────────────────────────────────────────────
    r3_groups: Tuple[str, ...] = (
        "consonance", "energy", "timbre", "change", "interactions"
    )

    # ── Brain: unit and model filtering ────────────────────────────────
    active_units: Optional[Tuple[str, ...]] = None    # None = all units
    active_models: Optional[Tuple[str, ...]] = None   # None = all models

    # ── Mechanism output size ──────────────────────────────────────────
    mechanism_dim: int = MECHANISM_DIM

    # ── Device ─────────────────────────────────────────────────────────
    device: str = "cpu"

    # ── Streaming ──────────────────────────────────────────────────────
    streaming: bool = False
    chunk_size: Optional[int] = None  # frames per chunk (streaming mode)

    def __post_init__(self) -> None:
        # Normalize mutable defaults to tuples
        if isinstance(self.r3_groups, list):
            object.__setattr__(self, "r3_groups", tuple(self.r3_groups))
        if isinstance(self.active_units, list):
            object.__setattr__(self, "active_units", tuple(self.active_units))
        if isinstance(self.active_models, list):
            object.__setattr__(self, "active_models", tuple(self.active_models))

        # Validate active_units against known unit names
        if self.active_units is not None:
            unknown = set(self.active_units) - set(UNIT_EXECUTION_ORDER)
            if unknown:
                raise ValueError(
                    f"Unknown unit(s) in active_units: {unknown}. "
                    f"Known units: {UNIT_EXECUTION_ORDER}"
                )

    # ── Computed properties ────────────────────────────────────────────

    @property
    def frame_rate(self) -> float:
        """Frame rate in Hz (sample_rate / hop_length)."""
        return self.sample_rate / self.hop_length

    @property
    def r3_dim(self) -> int:
        """Total R3 dimensionality."""
        return R3_DIM

    @property
    def cochlea_dim(self) -> int:
        """Cochlea (mel spectrogram) dimensionality."""
        return self.n_mels

    def is_unit_active(self, unit_name: str) -> bool:
        """Check if a given unit is active under this configuration."""
        if self.active_units is None:
            return True
        return unit_name in self.active_units

    def is_model_active(self, model_name: str) -> bool:
        """Check if a given model is active under this configuration."""
        if self.active_models is None:
            return True
        return model_name in self.active_models

    def __repr__(self) -> str:
        units = "all" if self.active_units is None else len(self.active_units)
        models = "all" if self.active_models is None else len(self.active_models)
        return (
            f"MIBetaConfig("
            f"sr={self.sample_rate}, hop={self.hop_length}, "
            f"units={units}, models={models}, "
            f"device={self.device!r})"
        )


# Singleton -- import and use directly
MI_BETA_CONFIG = MIBetaConfig()
