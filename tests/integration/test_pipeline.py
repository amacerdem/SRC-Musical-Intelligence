"""Integration test for the unified MI pipeline."""

import torch
import pytest

from mi.pipeline import MIPipeline
from mi.core.config import MIConfig
from mi.brain.musical_brain import BrainOutput


@pytest.fixture
def pipeline():
    return MIPipeline()


# ── Full pipeline ─────────────────────────────────────────────────────

def test_full_pipeline(pipeline, sine_440):
    output = pipeline.process(sine_440)
    assert isinstance(output.brain, BrainOutput)
    assert output.brain.tensor.shape[0] == 1  # batch
    assert output.brain.tensor.shape[2] == 26  # dims


def test_pipeline_chirp(pipeline, chirp_1s):
    output = pipeline.process(chirp_1s)
    assert output.brain.tensor.shape[2] == 26


def test_pipeline_output_range(pipeline, sine_440):
    output = pipeline.process(sine_440)
    t = output.brain.tensor
    assert t.min() >= -1.1
    assert t.max() <= 1.1


def test_pipeline_no_nan(pipeline, sine_440):
    output = pipeline.process(sine_440)
    assert not torch.isnan(output.brain.tensor).any()


def test_pipeline_deterministic(pipeline, sine_440):
    out1 = pipeline.process(sine_440)
    out2 = pipeline.process(sine_440)
    assert torch.allclose(out1.brain.tensor, out2.brain.tensor, atol=1e-6)


# ── Dimension access ─────────────────────────────────────────────────

def test_dimension_names(pipeline, sine_440):
    output = pipeline.process(sine_440)
    assert len(output.brain.dimension_names) == 26


def test_get_pathway(pipeline, sine_440):
    output = pipeline.process(sine_440)
    reward = output.brain.get_pathway("reward")
    assert reward.shape[2] == 9
    autonomic = output.brain.get_pathway("autonomic")
    assert autonomic.shape[2] == 5


def test_get_dim(pipeline, sine_440):
    output = pipeline.process(sine_440)
    pleasure = output.brain.get_dim("pleasure")
    assert pleasure.shape == (1, output.brain.tensor.shape[1])


# ── Key dimensions present ───────────────────────────────────────────

def test_reward_dimensions(pipeline, sine_440):
    output = pipeline.process(sine_440)
    names = output.brain.dimension_names
    assert "da_caudate" in names
    assert "da_nacc" in names
    assert "wanting" in names
    assert "liking" in names
    assert "pleasure" in names


def test_affect_dimensions(pipeline, sine_440):
    output = pipeline.process(sine_440)
    names = output.brain.dimension_names
    assert "f03_valence" in names
    assert "mode_signal" in names
    assert "happy_pathway" in names
    assert "sad_pathway" in names


def test_autonomic_dimensions(pipeline, sine_440):
    output = pipeline.process(sine_440)
    names = output.brain.dimension_names
    assert "scr" in names
    assert "hr" in names
    assert "chills_intensity" in names


# ── Valence formula ──────────────────────────────────────────────────

def test_valence_formula(pipeline, sine_440):
    """Verify f03_valence == tanh(0.5*happy - 0.5*sad) through full pipeline."""
    output = pipeline.process(sine_440)
    f03 = output.brain.get_dim("f03_valence")
    happy = output.brain.get_dim("happy_pathway")
    sad = output.brain.get_dim("sad_pathway")
    expected = torch.tanh(0.5 * happy - 0.5 * sad)
    assert torch.allclose(f03, expected, atol=1e-5)


# ── EAR output ───────────────────────────────────────────────────────

def test_ear_output(pipeline, sine_440):
    output = pipeline.process(sine_440, return_ear=True)
    assert output.ear is not None
    assert output.ear.cochlea is not None
    assert output.ear.r3 is not None
    assert output.ear.h3 is not None
    # H³ should have ~24 4-tuple features
    assert len(output.ear.h3.features) > 20


def test_no_ear_by_default(pipeline, sine_440):
    output = pipeline.process(sine_440)
    assert output.ear is None
