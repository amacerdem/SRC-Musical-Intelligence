"""
Shared test fixtures for MI test suite.

Provides reusable audio, mel, R³, and H³ fixtures
for unit, integration, and validation tests.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import torch
from torch import Tensor

# Ensure mi package is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from mi.core.config import MIConfig
from mi.core.constants import (
    SAMPLE_RATE,
    HOP_LENGTH,
    N_MELS,
    R3_DIM,
    N_MORPHS,
    N_LAWS,
)


@pytest.fixture
def config() -> MIConfig:
    """Standard test configuration."""
    return MIConfig(device="cpu")


@pytest.fixture
def sample_rate() -> int:
    return SAMPLE_RATE


@pytest.fixture
def hop_length() -> int:
    return HOP_LENGTH


# ── Audio Fixtures ──────────────────────────────────────────────────────

@pytest.fixture
def sine_440(sample_rate: int) -> Tensor:
    """1-second 440Hz sine wave. Shape: (1, 44100)."""
    t = torch.linspace(0, 1.0, sample_rate)
    waveform = torch.sin(2 * torch.pi * 440 * t).unsqueeze(0)
    return waveform


@pytest.fixture
def noise_1s(sample_rate: int) -> Tensor:
    """1-second white noise. Shape: (1, 44100)."""
    return torch.randn(1, sample_rate) * 0.1


@pytest.fixture
def silence_1s(sample_rate: int) -> Tensor:
    """1-second silence. Shape: (1, 44100)."""
    return torch.zeros(1, sample_rate)


@pytest.fixture
def chirp_1s(sample_rate: int) -> Tensor:
    """1-second chirp (200Hz to 4000Hz). Shape: (1, 44100)."""
    t = torch.linspace(0, 1.0, sample_rate)
    freq = 200 + (4000 - 200) * t
    phase = 2 * torch.pi * torch.cumsum(freq / sample_rate, dim=0)
    return torch.sin(phase).unsqueeze(0)


# ── Spectrogram Fixtures ────────────────────────────────────────────────

@pytest.fixture
def cochlea_output(sine_440: Tensor):
    """CochleaOutput from 440Hz sine."""
    from mi.ear.cochlea import audio_to_mel
    return audio_to_mel(sine_440)


@pytest.fixture
def mel_spectrogram(cochlea_output) -> Tensor:
    """Mel spectrogram tensor of 440Hz sine. Shape: (1, 128, T)."""
    return cochlea_output.mel


@pytest.fixture
def T_frames(mel_spectrogram: Tensor) -> int:
    """Number of frames from mel spectrogram."""
    return mel_spectrogram.shape[-1]


# ── R³ Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def random_r3() -> Tensor:
    """Random R³ features. Shape: (1, 100, 49)."""
    return torch.randn(1, 100, R3_DIM)


# ── H³ Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def random_h3_avg() -> Tensor:
    """Random H³ averaged 72D vector. Shape: (1, 100, 72)."""
    return torch.randn(1, 100, N_MORPHS * N_LAWS)
