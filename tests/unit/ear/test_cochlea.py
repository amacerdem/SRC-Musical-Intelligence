"""Tests for cochlea (mel spectrogram extraction)."""

import torch
import pytest

from mi.ear.cochlea import audio_to_mel
from mi.core.constants import SAMPLE_RATE, N_MELS


def test_output_shape(sine_440):
    out = audio_to_mel(sine_440)
    B, M, T = out.mel.shape
    assert B == 1
    assert M == N_MELS
    assert T > 0


def test_output_range(sine_440):
    out = audio_to_mel(sine_440)
    assert out.mel.min() >= 0, "Mel should be non-negative after log1p"
    assert out.mel.max() <= 1.0 + 1e-5, "Mel should be normalized to [0, 1]"


def test_silence_is_quiet(silence_1s):
    out = audio_to_mel(silence_1s)
    assert out.mel.max() < 0.01, "Silence should produce near-zero mel"


def test_batch_dim():
    waveform = torch.randn(2, SAMPLE_RATE)
    out = audio_to_mel(waveform)
    assert out.mel.shape[0] == 2


def test_cochlea_output_fields(sine_440):
    out = audio_to_mel(sine_440)
    assert out.sample_rate == SAMPLE_RATE
    assert out.hop_length == 256
