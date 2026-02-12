"""Tests for the unified Brain language layer (L³ = 104D).

Tests each semantic group independently, the orchestrator, and
integration with the full pipeline.
"""

import torch
import pytest

from mi.brain.musical_brain import MusicalBrain, BrainOutput
from mi.language.brain import BrainSemantics
from mi.language.brain.alpha import AlphaGroup
from mi.language.brain.beta import BetaGroup
from mi.language.brain.gamma import GammaGroup
from mi.language.brain.delta import DeltaGroup
from mi.language.brain.epsilon import EpsilonGroup
from mi.language.brain.zeta import ZetaGroup
from mi.language.brain.eta import EtaGroup, polarity_to_gradation, gradation_to_band
from mi.language.brain.theta import ThetaGroup


# ── Fixtures ─────────────────────────────────────────────────────────

@pytest.fixture
def brain_output():
    """Create a synthetic BrainOutput for testing."""
    B, T = 2, 50
    brain = MusicalBrain()
    # Create synthetic H³ features and R³ features
    h3_features = {}
    for demand in brain.h3_demand:
        h3_features[demand] = torch.rand(B, T)
    r3 = torch.rand(B, T, 49)
    return brain.compute(h3_features, r3)


@pytest.fixture
def semantics():
    return BrainSemantics()


# ═══════════════════════════════════════════════════════════════════════
# INDIVIDUAL GROUP TESTS
# ═══════════════════════════════════════════════════════════════════════

class TestAlphaGroup:
    def test_output_shape(self, brain_output):
        group = AlphaGroup()
        out = group.compute(brain_output)
        assert out.tensor.shape == (2, 50, 6)

    def test_dimension_names(self):
        group = AlphaGroup()
        assert len(group.dimension_names) == 6
        assert "shared_attribution" in group.dimension_names
        assert "computation_certainty" in group.dimension_names

    def test_class_attributes(self):
        group = AlphaGroup()
        assert group.LEVEL == 1
        assert group.GROUP_NAME == "alpha"
        assert group.DISPLAY_NAME == "α"
        assert group.OUTPUT_DIM == 6


class TestBetaGroup:
    def test_output_shape(self, brain_output):
        group = BetaGroup()
        out = group.compute(brain_output)
        assert out.tensor.shape == (2, 50, 14)

    def test_in_01_range(self, brain_output):
        group = BetaGroup()
        out = group.compute(brain_output)
        assert out.tensor.min() >= 0.0
        assert out.tensor.max() <= 1.0

    def test_dimension_names(self):
        group = BetaGroup()
        assert len(group.dimension_names) == 14
        assert "nacc_activation" in group.dimension_names
        assert "dopamine_level" in group.dimension_names


class TestGammaGroup:
    def test_output_shape(self, brain_output):
        group = GammaGroup()
        out = group.compute(brain_output)
        assert out.tensor.shape == (2, 50, 13)

    def test_in_01_range(self, brain_output):
        group = GammaGroup()
        out = group.compute(brain_output)
        assert out.tensor.min() >= -0.01  # clamp tolerance
        assert out.tensor.max() <= 1.01

    def test_key_dimensions(self):
        group = GammaGroup()
        names = group.dimension_names
        assert "beauty" in names
        assert "chill_intensity" in names
        assert "valence" in names


class TestDeltaGroup:
    def test_output_shape(self, brain_output):
        group = DeltaGroup()
        out = group.compute(brain_output)
        assert out.tensor.shape == (2, 50, 12)

    def test_in_01_range(self, brain_output):
        group = DeltaGroup()
        out = group.compute(brain_output)
        assert out.tensor.min() >= 0.0
        assert out.tensor.max() <= 1.0

    def test_physiological_signals(self):
        group = DeltaGroup()
        names = group.dimension_names
        assert "skin_conductance" in names
        assert "heart_rate" in names
        assert "piloerection" in names


class TestEpsilonGroup:
    def test_output_shape(self, brain_output):
        group = EpsilonGroup()
        out = group.compute(brain_output)
        assert out.tensor.shape == (2, 50, 19)

    def test_in_01_range(self, brain_output):
        group = EpsilonGroup()
        out = group.compute(brain_output)
        assert out.tensor.min() >= 0.0
        assert out.tensor.max() <= 1.0

    def test_stateful(self, brain_output):
        """Running twice should produce different outputs (state accumulates)."""
        group = EpsilonGroup()
        out1 = group.compute(brain_output)
        out2 = group.compute(brain_output)
        # Epsilon is stateful — second run should differ
        assert not torch.allclose(out1.tensor, out2.tensor, atol=1e-6)

    def test_reset(self, brain_output):
        """Reset should restore initial state."""
        group = EpsilonGroup()
        out1 = group.compute(brain_output)
        group.reset()
        out1b = group.compute(brain_output)
        # After reset, should match first run
        assert torch.allclose(out1.tensor, out1b.tensor, atol=1e-6)

    def test_wundt_inverted_u(self, brain_output):
        """Wundt position should be highest at medium surprise (inverted-U)."""
        group = EpsilonGroup()
        out = group.compute(brain_output)
        wundt = out.tensor[..., 17]  # wundt_position
        assert wundt.min() >= 0.0
        assert wundt.max() <= 1.0


class TestZetaGroup:
    def test_output_shape(self, brain_output):
        group = ZetaGroup()
        out = group.compute(brain_output)
        assert out.tensor.shape == (2, 50, 12)

    def test_bipolar_range(self, brain_output):
        group = ZetaGroup()
        out = group.compute(brain_output)
        assert out.tensor.min() >= -1.0
        assert out.tensor.max() <= 1.0

    def test_with_epsilon(self, brain_output):
        eps_group = EpsilonGroup()
        eps_out = eps_group.compute(brain_output)
        zeta_group = ZetaGroup()
        out = zeta_group.compute(brain_output, epsilon_output=eps_out.tensor)
        assert out.tensor.shape == (2, 50, 12)
        # Novelty should be non-zero when epsilon provides surprise
        novelty = out.tensor[..., 6]  # ζ6: novelty
        assert not torch.allclose(novelty, torch.zeros_like(novelty))


class TestEtaGroup:
    def test_output_shape(self, brain_output):
        group = EtaGroup()
        out = group.compute(brain_output)
        # Without zeta, should produce default 0.5
        assert out.tensor.shape == (2, 50, 12)
        assert torch.allclose(out.tensor, torch.full_like(out.tensor, 0.5))

    def test_with_zeta(self, brain_output):
        zeta_group = ZetaGroup()
        zeta_out = zeta_group.compute(brain_output)
        eta_group = EtaGroup()
        out = eta_group.compute(brain_output, zeta_output=zeta_out.tensor)
        assert out.tensor.shape == (2, 50, 12)
        assert out.tensor.min() >= 0.0
        assert out.tensor.max() <= 1.0

    def test_gradation_quantization(self):
        val = torch.tensor([[-1.0, 0.0, 1.0]])
        grad = polarity_to_gradation(val)
        assert grad[0, 0].item() == 0    # extreme negative
        assert grad[0, 1].item() == 32   # center
        assert grad[0, 2].item() == 63   # extreme positive

    def test_band_mapping(self):
        grad = torch.tensor([[0, 8, 31, 32, 63]])
        bands = gradation_to_band(grad)
        assert bands[0, 0].item() == 0   # band 0
        assert bands[0, 1].item() == 1   # band 1
        assert bands[0, 4].item() == 7   # band 7

    def test_get_terms(self, brain_output):
        zeta_group = ZetaGroup()
        zeta_out = zeta_group.compute(brain_output)
        eta_group = EtaGroup()
        terms = eta_group.get_terms(zeta_out.tensor)
        assert len(terms) == 12  # 12 axes
        assert terms[0][0]["axis"] == "valence"
        assert "term" in terms[0][0]


class TestThetaGroup:
    def test_output_shape(self, brain_output):
        group = ThetaGroup()
        out = group.compute(brain_output)
        assert out.tensor.shape == (2, 50, 16)

    def test_in_01_range(self, brain_output):
        group = ThetaGroup()
        out = group.compute(brain_output)
        assert out.tensor.min() >= 0.0
        assert out.tensor.max() <= 1.0

    def test_subject_softmax(self, brain_output):
        """Subject dimensions should sum to ~1 (softmax)."""
        group = ThetaGroup()
        out = group.compute(brain_output)
        subject = out.tensor[..., :4]  # first 4 dims
        sums = subject.sum(dim=-1)
        assert torch.allclose(sums, torch.ones_like(sums), atol=1e-5)

    def test_with_dependencies(self, brain_output):
        eps = EpsilonGroup()
        eps_out = eps.compute(brain_output)
        zeta = ZetaGroup()
        zeta_out = zeta.compute(brain_output, epsilon_output=eps_out.tensor)
        theta = ThetaGroup()
        out = theta.compute(
            brain_output,
            epsilon_output=eps_out.tensor,
            zeta_output=zeta_out.tensor,
        )
        assert out.tensor.shape == (2, 50, 16)


# ═══════════════════════════════════════════════════════════════════════
# ORCHESTRATOR TESTS
# ═══════════════════════════════════════════════════════════════════════

class TestBrainSemantics:
    def test_total_dim(self, semantics):
        assert semantics.total_dim == 104

    def test_output_shape(self, brain_output, semantics):
        l3 = semantics.compute(brain_output)
        assert l3.tensor.shape == (2, 50, 104)

    def test_model_name(self, brain_output, semantics):
        l3 = semantics.compute(brain_output)
        assert l3.model_name == "Brain"

    def test_all_groups_present(self, brain_output, semantics):
        l3 = semantics.compute(brain_output)
        expected = {"alpha", "beta", "gamma", "delta",
                    "epsilon", "zeta", "eta", "theta"}
        assert set(l3.groups.keys()) == expected

    def test_group_dims_sum_to_total(self, brain_output, semantics):
        l3 = semantics.compute(brain_output)
        dim_sum = sum(g.tensor.shape[-1] for g in l3.groups.values())
        assert dim_sum == 104

    def test_concatenation_order(self, brain_output, semantics):
        """Verify groups are concatenated in α→β→γ→δ→ε→ζ→η→θ order."""
        l3 = semantics.compute(brain_output)
        offset = 0
        for name in ("alpha", "beta", "gamma", "delta",
                      "epsilon", "zeta", "eta", "theta"):
            group = l3.groups[name]
            dim = group.tensor.shape[-1]
            expected_slice = group.tensor
            actual_slice = l3.tensor[..., offset:offset + dim]
            assert torch.allclose(expected_slice, actual_slice, atol=1e-6), (
                f"Group {name} mismatch at offset {offset}"
            )
            offset += dim

    def test_no_nan(self, brain_output, semantics):
        l3 = semantics.compute(brain_output)
        assert not torch.isnan(l3.tensor).any()

    def test_reset(self, brain_output, semantics):
        l3_1 = semantics.compute(brain_output)
        semantics.reset()
        l3_2 = semantics.compute(brain_output)
        # After reset, epsilon should produce same output
        eps1 = l3_1.groups["epsilon"].tensor
        eps2 = l3_2.groups["epsilon"].tensor
        assert torch.allclose(eps1, eps2, atol=1e-6)

    def test_l3_total_dim_property(self, brain_output, semantics):
        l3 = semantics.compute(brain_output)
        assert l3.total_dim == 104


# ═══════════════════════════════════════════════════════════════════════
# PIPELINE INTEGRATION
# ═══════════════════════════════════════════════════════════════════════

class TestPipelineSemantics:
    def test_semantics_by_default(self):
        """Pipeline should compute semantics by default."""
        from mi.pipeline import MIPipeline
        pipeline = MIPipeline()
        waveform = torch.randn(1, 44100)
        output = pipeline.process(waveform)
        assert output.semantics is not None
        assert output.semantics.tensor.shape[2] == 104

    def test_semantics_off(self):
        """return_semantics=False should skip L³."""
        from mi.pipeline import MIPipeline
        pipeline = MIPipeline()
        waveform = torch.randn(1, 44100)
        output = pipeline.process(waveform, return_semantics=False)
        assert output.semantics is None

    def test_semantics_groups(self):
        """All 8 groups should be present in pipeline output."""
        from mi.pipeline import MIPipeline
        pipeline = MIPipeline()
        waveform = torch.randn(1, 44100)
        output = pipeline.process(waveform)
        assert len(output.semantics.groups) == 8

    def test_pipeline_reset(self):
        """Pipeline reset should clear epsilon state."""
        from mi.pipeline import MIPipeline
        pipeline = MIPipeline()
        waveform = torch.randn(1, 44100)
        out1 = pipeline.process(waveform)
        pipeline.reset()
        out2 = pipeline.process(waveform)
        eps1 = out1.semantics.groups["epsilon"].tensor
        eps2 = out2.semantics.groups["epsilon"].tensor
        assert torch.allclose(eps1, eps2, atol=1e-6)
