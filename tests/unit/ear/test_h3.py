"""Tests for H³ temporal context extraction."""

import torch
import pytest

from mi.ear.h3 import H3Extractor
from mi.ear.h3.horizon import EventHorizon
from mi.ear.h3.morph import MorphComputer
from mi.ear.h3.attention import compute_attention_weights
from mi.core.constants import N_HORIZONS, HORIZON_FRAMES, HORIZON_MS


# ── Horizon Tests ───────────────────────────────────────────────────────

def test_horizon_count():
    assert N_HORIZONS == 32
    assert len(HORIZON_FRAMES) == 32
    assert len(HORIZON_MS) == 32


def test_horizon_object():
    h = EventHorizon(index=6)
    assert h.index == 6
    assert h.frames == HORIZON_FRAMES[6]
    assert h.ms == HORIZON_MS[6]
    assert abs(h.seconds - HORIZON_MS[6] / 1000.0) < 0.001


def test_horizons_monotonic():
    for i in range(1, len(HORIZON_MS)):
        assert HORIZON_MS[i] >= HORIZON_MS[i - 1], \
            f"Horizon {i} should be >= {i-1}"


# ── Attention Tests ─────────────────────────────────────────────────────

def test_attention_weights_shape():
    weights = compute_attention_weights(10)
    assert weights.shape == (10,)


def test_attention_weights_positive():
    weights = compute_attention_weights(10)
    assert (weights > 0).all()


def test_attention_end_highest():
    weights = compute_attention_weights(10)
    # End (most recent) should have highest weight with exponential decay
    assert weights[-1] >= weights[0]


# ── Morph Tests ─────────────────────────────────────────────────────────

def test_morph_compute():
    mc = MorphComputer()
    window = torch.randn(1, 20)  # (B, win_len)
    weights = compute_attention_weights(20)
    val = mc.compute(window, weights, morph_idx=0)  # value
    assert val.shape == (1,)  # (B,)


def test_all_morphs_compute():
    mc = MorphComputer()
    window = torch.randn(1, 50)
    weights = compute_attention_weights(50)
    for m in range(24):
        val = mc.compute(window, weights, morph_idx=m)
        assert val is not None, f"Morph {m} returned None"
        assert val.shape == (1,), f"Morph {m} wrong shape: {val.shape}"


# ── H3Extractor Tests (4-tuple demand) ───────────────────────────────

def test_h3_extractor_sparse(random_r3):
    """4-tuple demand: (r3_idx, horizon, morph, law)."""
    demand = {
        (0, 6, 0, 0),   # R³ feature 0, H6, value, memory
        (10, 6, 4, 2),   # R³ feature 10, H6, max, integration
        (3, 16, 0, 0),   # R³ feature 3, H16, value, memory
        (8, 16, 4, 2),   # R³ feature 8, H16, max, integration
    }
    h3 = H3Extractor()
    output = h3.extract(random_r3, demand)
    for key in demand:
        assert key in output.features


def test_h3_empty_demand(random_r3):
    h3 = H3Extractor()
    output = h3.extract(random_r3, set())
    assert len(output) == 0


def test_h3_output_shape(random_r3):
    """Each H³ feature should have (B, T) shape."""
    demand = {(3, 18, 0, 2), (10, 18, 4, 2)}
    h3 = H3Extractor()
    output = h3.extract(random_r3, demand)
    B, T, _ = random_r3.shape
    for key, val in output.features.items():
        assert val.shape == (B, T), f"Key {key} has wrong shape {val.shape}"
