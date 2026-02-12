"""Tests for MI core constants."""

from mi.core.constants import (
    SAMPLE_RATE,
    HOP_LENGTH,
    FRAME_RATE,
    N_MELS,
    R3_DIM,
    N_HORIZONS,
    N_MORPHS,
    N_LAWS,
    H3_TOTAL_DIM,
    HORIZON_MS,
    HORIZON_FRAMES,
    MORPH_NAMES,
    LAW_NAMES,
    BETA_NACC,
    BETA_CAUDATE,
    CIRCUIT_NAMES,
    h3_flat_index,
    scale_h3_value,
)


def test_audio_constants():
    assert SAMPLE_RATE == 44_100
    assert HOP_LENGTH == 256
    assert abs(FRAME_RATE - 172.265625) < 0.001


def test_r3_dim():
    assert R3_DIM == 49


def test_h3_dimensions():
    assert N_HORIZONS == 32
    assert N_MORPHS == 24
    assert N_LAWS == 3
    assert H3_TOTAL_DIM == 32 * 24 * 3


def test_horizon_counts():
    assert len(HORIZON_MS) == N_HORIZONS
    assert len(HORIZON_FRAMES) == N_HORIZONS
    # All frame counts > 0
    assert all(f >= 1 for f in HORIZON_FRAMES)


def test_morph_law_counts():
    assert len(MORPH_NAMES) == N_MORPHS
    assert len(LAW_NAMES) == N_LAWS


def test_neuroscience_coefficients():
    assert BETA_NACC == 0.84
    assert BETA_CAUDATE == 0.71


def test_circuit_names():
    assert len(CIRCUIT_NAMES) == 6
    assert "mesolimbic" in CIRCUIT_NAMES


def test_h3_flat_index():
    # H0, M0, L0 → 0
    assert h3_flat_index(0, 0, 0) == 0
    # H0, M0, L2 → 2
    assert h3_flat_index(0, 0, 2) == 2
    # H1, M0, L0 → 72
    assert h3_flat_index(1, 0, 0) == 72
    # Last index
    assert h3_flat_index(31, 23, 2) == H3_TOTAL_DIM - 1


def test_scale_h3_value():
    import torch
    val = torch.tensor([[0.5]])
    # M0 has gain=6.0, bias=0.5 → 6.0*(0.5-0.5) = 0.0
    scaled = scale_h3_value(val, morph=0)
    assert abs(scaled.item()) < 1e-6
