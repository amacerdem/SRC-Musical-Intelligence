"""Tests for R³ spectral analysis."""

import torch
import pytest

from mi.ear.r3 import R3Extractor
from mi.core.constants import R3_DIM, SAMPLE_RATE
from mi.ear.cochlea import audio_to_mel


@pytest.fixture
def r3() -> R3Extractor:
    return R3Extractor()


def test_output_dim(r3, mel_spectrogram):
    output = r3.extract(mel_spectrogram)
    assert output.features.shape[-1] == R3_DIM


def test_output_shape(r3, mel_spectrogram):
    output = r3.extract(mel_spectrogram)
    B, T, D = output.features.shape
    assert B == 1
    assert D == 49
    assert T == mel_spectrogram.shape[-1]


def test_feature_names(r3, mel_spectrogram):
    output = r3.extract(mel_spectrogram)
    assert len(output.feature_names) == R3_DIM


def test_feature_range(r3, mel_spectrogram):
    output = r3.extract(mel_spectrogram)
    # R³ features should be in [-1, 1] range
    assert output.features.min() >= -1.1
    assert output.features.max() <= 1.1


def test_group_boundaries(r3):
    """Verify the 5 groups sum to 49D."""
    dims = sum(g.OUTPUT_DIM for g in r3.groups)
    assert dims == R3_DIM


def test_different_inputs_different_outputs(r3, sine_440, noise_1s):
    mel_sine = audio_to_mel(sine_440).mel
    mel_noise = audio_to_mel(noise_1s).mel
    out_sine = r3.extract(mel_sine)
    out_noise = r3.extract(mel_noise)
    # Should not be identical
    diff = (out_sine.features - out_noise.features).abs().mean()
    assert diff > 0.01, "Sine and noise should produce different R³ features"
