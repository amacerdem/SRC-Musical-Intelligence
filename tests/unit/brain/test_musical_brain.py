"""Tests for MusicalBrain — unified 26D musical cognition."""

import torch
import pytest

from mi.brain.musical_brain import MusicalBrain, BrainOutput
from mi.core.constants import R3_DIM


B, T = 2, 100


@pytest.fixture
def brain():
    return MusicalBrain()


@pytest.fixture
def h3(brain):
    """4-tuple H³ features for all brain demands."""
    return {key: torch.randn(B, T) for key in brain.h3_demand}


@pytest.fixture
def r3():
    """R³ spectral features (B, T, 49)."""
    return torch.rand(B, T, R3_DIM)


# ── Output shape and type ─────────────────────────────────────────────


def test_output_shape(brain, h3, r3):
    out = brain.compute(h3, r3)
    assert out.tensor.shape == (B, T, 26)


def test_output_type(brain, h3, r3):
    out = brain.compute(h3, r3)
    assert isinstance(out, BrainOutput)


def test_output_dim_constant(brain):
    assert brain.OUTPUT_DIM == 26


def test_dimension_names_count(brain):
    assert len(brain.DIMENSION_NAMES) == 26


# ── Pathway ranges ────────────────────────────────────────────────────


def test_pathway_ranges_cover_all(brain):
    """Pathway ranges must cover [0, 26) with no gaps."""
    ranges = brain.PATHWAY_RANGES
    assert ranges["shared"] == (0, 4)
    assert ranges["reward"] == (4, 13)
    assert ranges["affect"] == (13, 19)
    assert ranges["autonomic"] == (19, 24)
    assert ranges["integration"] == (24, 26)
    # Total
    total = sum(e - s for s, e in ranges.values())
    assert total == 26


def test_get_pathway(brain, h3, r3):
    out = brain.compute(h3, r3)
    shared = out.get_pathway("shared")
    assert shared.shape == (B, T, 4)
    reward = out.get_pathway("reward")
    assert reward.shape == (B, T, 9)
    affect = out.get_pathway("affect")
    assert affect.shape == (B, T, 6)
    autonomic = out.get_pathway("autonomic")
    assert autonomic.shape == (B, T, 5)
    integration = out.get_pathway("integration")
    assert integration.shape == (B, T, 2)


def test_get_dim(brain, h3, r3):
    out = brain.compute(h3, r3)
    arousal = out.get_dim("arousal")
    assert arousal.shape == (B, T)
    pleasure = out.get_dim("pleasure")
    assert pleasure.shape == (B, T)


# ── Value ranges ──────────────────────────────────────────────────────


def test_sigmoid_dims_in_01(brain, h3, r3):
    """Dimensions that use sigmoid should be in [0, 1]."""
    out = brain.compute(h3, r3)
    sigmoid_dims = [
        "arousal", "harmonic_context",
        "da_caudate", "da_nacc", "opioid_proxy",
        "wanting", "liking", "pleasure",
        "tension", "reward_forecast",
        "mode_signal", "consonance_valence",
        "happy_pathway", "sad_pathway", "emotion_certainty",
        "scr", "hr", "respr",
        "beauty", "emotional_arc",
    ]
    for name in sigmoid_dims:
        val = out.get_dim(name)
        assert val.min() >= -0.01, f"{name} below 0: {val.min()}"
        assert val.max() <= 1.01, f"{name} above 1: {val.max()}"


def test_tanh_dims_in_neg1_1(brain, h3, r3):
    """Dimensions that use tanh should be in [-1, 1]."""
    out = brain.compute(h3, r3)
    tanh_dims = ["prediction_error", "emotional_momentum", "prediction_match",
                 "f03_valence", "ans_composite"]
    for name in tanh_dims:
        val = out.get_dim(name)
        assert val.min() >= -1.01, f"{name} below -1: {val.min()}"
        assert val.max() <= 1.01, f"{name} above 1: {val.max()}"


def test_chills_intensity_range(brain, h3, r3):
    """Chills = 0.35*scr + 0.40*(1-hr) + 0.25*respr — all in [0,1]."""
    out = brain.compute(h3, r3)
    ci = out.get_dim("chills_intensity")
    assert ci.min() >= -0.01
    assert ci.max() <= 1.01


# ── H³ demand ─────────────────────────────────────────────────────────


def test_h3_demand_all_4_tuples(brain):
    for tup in brain.h3_demand:
        assert len(tup) == 4, f"Expected 4-tuple, got {tup}"


def test_h3_demand_count(brain):
    demand = brain.h3_demand
    assert 20 <= len(demand) <= 30, f"Expected ~24 unique tuples, got {len(demand)}"


def test_h3_demand_sorted(brain):
    demand = brain.h3_demand
    assert demand == sorted(demand)


def test_h3_demand_no_duplicates(brain):
    demand = brain.h3_demand
    assert len(demand) == len(set(demand))


def test_h3_demand_horizons(brain):
    """Brain uses H9, H16, H18, H19, H20, H22."""
    horizons = {h for _, h, _, _ in brain.h3_demand}
    assert horizons == {9, 16, 18, 19, 20, 22}


def test_h3_demand_r3_features(brain):
    """Brain must track consonance, energy, timbre features."""
    r3_indices = {r for r, _, _, _ in brain.h3_demand}
    assert 3 in r3_indices    # stumpf_fusion (consonance)
    assert 10 in r3_indices   # loudness (energy)
    assert 8 in r3_indices    # velocity_A (energy)
    assert 14 in r3_indices   # tonalness (timbre)
    assert 12 in r3_indices   # warmth (timbre)


# ── Determinism ───────────────────────────────────────────────────────


def test_deterministic(brain, h3, r3):
    """Same input → same output."""
    out1 = brain.compute(h3, r3)
    out2 = brain.compute(h3, r3)
    assert torch.allclose(out1.tensor, out2.tensor, atol=1e-6)


def test_no_nan(brain, h3, r3):
    out = brain.compute(h3, r3)
    assert not torch.isnan(out.tensor).any()


def test_no_inf(brain, h3, r3):
    out = brain.compute(h3, r3)
    assert not torch.isinf(out.tensor).any()


# ── Cross-pathway dependencies ────────────────────────────────────────


def test_autonomic_depends_on_shared(brain, r3):
    """Changing arousal (shared) should change SCR (autonomic)."""
    h3_low = {key: torch.zeros(B, T) for key in brain.h3_demand}
    h3_high = {key: torch.zeros(B, T) for key in brain.h3_demand}
    # Pump up arousal inputs (loud_max_h9 = (10,9,4,2))
    h3_high[(10, 9, 4, 2)] = torch.ones(B, T) * 2.0

    out_low = brain.compute(h3_low, r3)
    out_high = brain.compute(h3_high, r3)

    scr_low = out_low.get_dim("scr").mean()
    scr_high = out_high.get_dim("scr").mean()
    assert scr_high > scr_low, "SCR should increase with arousal"


def test_reward_affect_integrated(brain, r3):
    """Beauty = opioid_proxy * liking — changes in reward affect integration."""
    h3_low = {key: torch.zeros(B, T) for key in brain.h3_demand}
    h3_high = {key: torch.zeros(B, T) for key in brain.h3_demand}
    # Pump consonance mean (3,18,0,2) → increases da_nacc → liking → beauty
    h3_high[(3, 18, 0, 2)] = torch.ones(B, T) * 2.0

    out_low = brain.compute(h3_low, r3)
    out_high = brain.compute(h3_high, r3)

    beauty_low = out_low.get_dim("beauty").mean()
    beauty_high = out_high.get_dim("beauty").mean()
    assert beauty_high > beauty_low, "Beauty should increase with consonance"


# ── Batch and single-frame ────────────────────────────────────────────


def test_single_frame(brain):
    """Works with T=1."""
    h3 = {key: torch.randn(1, 1) for key in brain.h3_demand}
    r3 = torch.rand(1, 1, R3_DIM)
    out = brain.compute(h3, r3)
    assert out.tensor.shape == (1, 1, 26)


def test_large_batch(brain):
    """Works with large batch."""
    h3 = {key: torch.randn(8, 500) for key in brain.h3_demand}
    r3 = torch.rand(8, 500, R3_DIM)
    out = brain.compute(h3, r3)
    assert out.tensor.shape == (8, 500, 26)


# ── Missing H³ features ──────────────────────────────────────────────


def test_missing_h3_features(brain, r3):
    """Brain should handle missing H³ features gracefully (zero fallback)."""
    # Provide only half the demands
    all_demands = brain.h3_demand
    partial = {key: torch.randn(B, T) for key in all_demands[:len(all_demands)//2]}
    out = brain.compute(partial, r3)
    assert out.tensor.shape == (B, T, 26)
    assert not torch.isnan(out.tensor).any()
