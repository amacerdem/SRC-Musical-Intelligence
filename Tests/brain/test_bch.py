"""BCH (Brainstem Consonance Hierarchy) — scientific unit tests.

Tests the gold standard SPU Relay nucleus for:
1. Output shape and range
2. Contract validation
3. Consonance sensitivity (directional)
4. H³ demand completeness
5. RegionLink and NeuroLink correctness
6. Scope partitioning
"""
from __future__ import annotations

import math
import sys
from pathlib import Path
from typing import Dict, Set, Tuple

import pytest
import torch
from torch import Tensor

# Path setup
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from Musical_Intelligence.brain.units.spu.relays.bch import BCH
from Musical_Intelligence.brain.regions import REGION_REGISTRY

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
B = 2
T = 200
R3_DIM = 49
FRAME_RATE = 172.27


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def bch() -> BCH:
    return BCH()


@pytest.fixture
def random_r3() -> Tensor:
    torch.manual_seed(42)
    return torch.rand(B, T, R3_DIM)


@pytest.fixture
def h3_for_bch(bch: BCH) -> Dict[Tuple[int, int, int, int], Tensor]:
    """Random H³ features for all 16 BCH demands."""
    torch.manual_seed(42)
    return {spec.as_tuple(): torch.rand(B, T) for spec in bch.h3_demand}


@pytest.fixture
def bch_output(bch: BCH, h3_for_bch, random_r3) -> Tensor:
    return bch.compute(h3_for_bch, random_r3)


# ======================================================================
# 1. Output shape and range
# ======================================================================

class TestOutputShape:
    def test_shape(self, bch_output: Tensor):
        assert bch_output.shape == (B, T, 12)

    def test_no_nan(self, bch_output: Tensor):
        assert not torch.isnan(bch_output).any()

    def test_no_inf(self, bch_output: Tensor):
        assert not torch.isinf(bch_output).any()

    def test_range_0_1(self, bch_output: Tensor):
        assert bch_output.min() >= 0.0
        assert bch_output.max() <= 1.0


# ======================================================================
# 2. Contract validation
# ======================================================================

class TestContract:
    def test_validate_constants(self, bch: BCH):
        errors = bch.validate_constants()
        assert errors == [], f"Validation errors: {errors}"

    def test_name(self, bch: BCH):
        assert bch.NAME == "BCH"

    def test_full_name(self, bch: BCH):
        assert bch.FULL_NAME == "Brainstem Consonance Hierarchy"

    def test_unit(self, bch: BCH):
        assert bch.UNIT == "SPU"

    def test_role(self, bch: BCH):
        assert bch.ROLE == "relay"

    def test_depth(self, bch: BCH):
        assert bch.PROCESSING_DEPTH == 0

    def test_output_dim(self, bch: BCH):
        assert bch.OUTPUT_DIM == 12

    def test_dim_names_count(self, bch: BCH):
        assert len(bch.dimension_names) == 12

    def test_dim_names_unique(self, bch: BCH):
        names = bch.dimension_names
        assert len(set(names)) == len(names), "Duplicate dim names"

    def test_layers_cover_all_dims(self, bch: BCH):
        covered = set()
        for layer in bch.LAYERS:
            for i in range(layer.start, layer.end):
                covered.add(i)
        assert covered == set(range(12))

    def test_layer_dim_names_match(self, bch: BCH):
        assert bch.layer_dim_names == bch.dimension_names


# ======================================================================
# 3. Consonance sensitivity
# ======================================================================

class TestConsonanceSensitivity:
    """BCH should produce higher consonance_signal for consonant input."""

    def _make_r3(self, roughness: float, sethares: float, helmholtz: float,
                 tonalness: float = 0.8) -> Tensor:
        r3 = torch.full((1, 1, R3_DIM), 0.5)
        r3[:, :, 0] = roughness
        r3[:, :, 1] = sethares
        r3[:, :, 2] = helmholtz
        r3[:, :, 3] = 0.8  # stumpf
        r3[:, :, 14] = tonalness
        r3[:, :, 17] = tonalness  # autocorr
        r3[:, :, 18] = 0.6  # trist1
        r3[:, :, 19] = 0.2  # trist2
        r3[:, :, 20] = 0.1  # trist3
        return r3

    def _make_h3(self, bch: BCH) -> Dict[Tuple[int, int, int, int], Tensor]:
        return {spec.as_tuple(): torch.full((1, 1), 0.5) for spec in bch.h3_demand}

    def test_consonance_signal_higher_for_consonant(self, bch: BCH):
        h3 = self._make_h3(bch)
        # Consonant: low roughness, low sethares, high helmholtz
        consonant_r3 = self._make_r3(roughness=0.1, sethares=0.1, helmholtz=0.9)
        # Dissonant: high roughness, high sethares, low helmholtz
        dissonant_r3 = self._make_r3(roughness=0.9, sethares=0.9, helmholtz=0.1)

        consonant_out = bch.compute(h3, consonant_r3)
        dissonant_out = bch.compute(h3, dissonant_r3)

        # consonance_signal is dim 6
        assert consonant_out[0, 0, 6] > dissonant_out[0, 0, 6]

    def test_nps_higher_for_tonal(self, bch: BCH):
        h3 = self._make_h3(bch)
        # Tonal: high tonalness
        tonal_r3 = self._make_r3(0.5, 0.5, 0.5, tonalness=0.9)
        # Non-tonal: low tonalness
        noise_r3 = self._make_r3(0.5, 0.5, 0.5, tonalness=0.1)

        tonal_out = bch.compute(h3, tonal_r3)
        noise_out = bch.compute(h3, noise_r3)

        # f01_nps is dim 0
        assert tonal_out[0, 0, 0] > noise_out[0, 0, 0]

    def test_hierarchy_higher_for_consonant_interval(self, bch: BCH):
        h3 = self._make_h3(bch)
        # Perfect fifth (P5): high helmholtz, high stumpf
        r3_p5 = torch.full((1, 1, R3_DIM), 0.5)
        r3_p5[:, :, 2] = 0.9  # helmholtz
        r3_p5[:, :, 3] = 0.9  # stumpf

        # Tritone: low helmholtz, low stumpf
        r3_tt = torch.full((1, 1, R3_DIM), 0.5)
        r3_tt[:, :, 2] = 0.2  # helmholtz
        r3_tt[:, :, 3] = 0.2  # stumpf

        p5_out = bch.compute(h3, r3_p5)
        tt_out = bch.compute(h3, r3_tt)

        # f03_hierarchy is dim 2
        assert p5_out[0, 0, 2] > tt_out[0, 0, 2]


# ======================================================================
# 4. H³ demand completeness
# ======================================================================

class TestH3Demand:
    def test_count(self, bch: BCH):
        assert len(bch.h3_demand) == 16

    def test_all_tuples_are_4_element(self, bch: BCH):
        for spec in bch.h3_demand:
            t = spec.as_tuple()
            assert len(t) == 4

    def test_all_have_purpose(self, bch: BCH):
        for spec in bch.h3_demand:
            assert spec.purpose, f"H3 demand {spec.as_tuple()} has no purpose"

    def test_all_have_citation(self, bch: BCH):
        for spec in bch.h3_demand:
            assert spec.citation, f"H3 demand {spec.as_tuple()} has no citation"

    def test_r3_indices_in_range(self, bch: BCH):
        for spec in bch.h3_demand:
            assert 0 <= spec.r3_idx < R3_DIM


# ======================================================================
# 5. RegionLink and NeuroLink
# ======================================================================

class TestRegionLinks:
    def test_count(self, bch: BCH):
        assert len(bch.region_links) >= 6

    def test_all_reference_valid_regions(self, bch: BCH):
        for rl in bch.region_links:
            assert rl.region in REGION_REGISTRY, f"Unknown region: {rl.region}"

    def test_all_reference_valid_dims(self, bch: BCH):
        dim_names = set(bch.dimension_names)
        for rl in bch.region_links:
            assert rl.dim_name in dim_names, f"Unknown dim: {rl.dim_name}"

    def test_ic_is_primary(self, bch: BCH):
        """IC should have the highest total weight (primary site for BCH)."""
        ic_weight = sum(
            rl.weight for rl in bch.region_links if rl.region == "IC"
        )
        other_weights = {}
        for rl in bch.region_links:
            if rl.region != "IC":
                other_weights[rl.region] = (
                    other_weights.get(rl.region, 0) + rl.weight
                )
        for region, weight in other_weights.items():
            assert ic_weight >= weight, (
                f"IC weight ({ic_weight}) should be >= {region} ({weight})"
            )


class TestNeuroLinks:
    def test_count(self, bch: BCH):
        assert len(bch.neuro_links) >= 1

    def test_all_reference_valid_dims(self, bch: BCH):
        dim_names = set(bch.dimension_names)
        for nl in bch.neuro_links:
            assert nl.dim_name in dim_names, f"Unknown dim: {nl.dim_name}"

    def test_channel_range(self, bch: BCH):
        for nl in bch.neuro_links:
            assert 0 <= nl.channel < 4


# ======================================================================
# 6. Scope partitioning
# ======================================================================

class TestScope:
    def test_internal_count(self, bch: BCH):
        """E + M layers are internal = 6 dims."""
        assert len(bch.internal_dims) == 6

    def test_external_count(self, bch: BCH):
        """P layer is external = 3 dims."""
        assert len(bch.external_dims) == 3

    def test_hybrid_count(self, bch: BCH):
        """F layer is hybrid = 3 dims."""
        assert len(bch.hybrid_dims) == 3

    def test_routable_count(self, bch: BCH):
        """Internal + hybrid = 9 dims."""
        assert len(bch.routable_dims) == 9

    def test_exportable_count(self, bch: BCH):
        """External + hybrid = 6 dims."""
        assert len(bch.exportable_dims) == 6

    def test_no_overlap_internal_external(self, bch: BCH):
        assert not set(bch.internal_dims) & set(bch.external_dims)


# ======================================================================
# 7. Metadata
# ======================================================================

class TestMetadata:
    def test_tier(self, bch: BCH):
        assert bch.metadata.evidence_tier == "alpha"

    def test_paper_count(self, bch: BCH):
        assert bch.metadata.effective_paper_count == 13

    def test_falsification_count(self, bch: BCH):
        assert len(bch.metadata.falsification_criteria) == 5

    def test_confidence_range(self, bch: BCH):
        low, high = bch.metadata.confidence_range
        assert low >= 0.9
        assert high <= 1.0
