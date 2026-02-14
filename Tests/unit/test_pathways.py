"""Unit tests for pathway routing.

Tests pathway counts, definitions (P1-P5), PathwayRunner.route() with
real pathway definitions, and synthetic unit outputs.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

import pytest
import torch

from Musical_Intelligence.brain.pathways import (
    PathwayRunner,
    ALL_PATHWAYS,
    INTER_UNIT_PATHWAYS,
    INTRA_UNIT_PATHWAYS,
    P1_SPU_ARU,
    P2_STU_INTERNAL,
    P3_IMU_ARU,
    P4_STU_INTERNAL,
    P5_STU_ARU,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

B, T = 2, 30


@pytest.fixture(scope="module")
def runner() -> PathwayRunner:
    """Single PathwayRunner instance."""
    return PathwayRunner()


@pytest.fixture(scope="module")
def synthetic_unit_outputs() -> dict:
    """Synthetic outputs for all 9 cognitive units.

    Each unit's output is a random (B, T, dim) tensor matching the
    architecture specification.
    """
    torch.manual_seed(55)
    dims = {
        "SPU": 99,
        "STU": 148,
        "IMU": 159,
        "ASU": 94,
        "NDU": 94,
        "MPU": 104,
        "PCU": 94,
        "ARU": 120,
        "RPU": 94,
    }
    return {name: torch.rand(B, T, dim) for name, dim in dims.items()}


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestPathwayCount:
    """Verify pathway counts match the architecture spec."""

    def test_pathway_count(self):
        """Must have 5 total pathways: 3 inter + 2 intra."""
        assert len(ALL_PATHWAYS) == 5, (
            f"Expected 5 total pathways, got {len(ALL_PATHWAYS)}"
        )

    def test_inter_unit_pathway_count(self):
        """Must have exactly 3 inter-unit pathways."""
        assert len(INTER_UNIT_PATHWAYS) == 3, (
            f"Expected 3 inter-unit pathways, got {len(INTER_UNIT_PATHWAYS)}"
        )

    def test_intra_unit_pathway_count(self):
        """Must have exactly 2 intra-unit pathways."""
        assert len(INTRA_UNIT_PATHWAYS) == 2, (
            f"Expected 2 intra-unit pathways, got {len(INTRA_UNIT_PATHWAYS)}"
        )

    def test_all_equals_inter_plus_intra(self):
        """ALL_PATHWAYS must be the concatenation of inter + intra."""
        assert ALL_PATHWAYS == INTER_UNIT_PATHWAYS + INTRA_UNIT_PATHWAYS


class TestPathwayDefinitions:
    """Verify P1-P5 have correct source and target units."""

    @pytest.mark.parametrize(
        "pathway,expected_id,expected_source,expected_target",
        [
            (P1_SPU_ARU, "P1_SPU_ARU", "SPU", "ARU"),
            (P2_STU_INTERNAL, "P2_STU_INTERNAL", "STU", "STU"),
            (P3_IMU_ARU, "P3_IMU_ARU", "IMU", "ARU"),
            (P4_STU_INTERNAL, "P4_STU_INTERNAL", "STU", "STU"),
            (P5_STU_ARU, "P5_STU_ARU", "STU", "ARU"),
        ],
    )
    def test_pathway_definitions(
        self, pathway, expected_id, expected_source, expected_target
    ):
        """Each pathway must have the correct ID, source, and target."""
        assert pathway.pathway_id == expected_id, (
            f"Expected ID {expected_id!r}, got {pathway.pathway_id!r}"
        )
        assert pathway.source_unit == expected_source, (
            f"{expected_id}: expected source {expected_source!r}, "
            f"got {pathway.source_unit!r}"
        )
        assert pathway.target_unit == expected_target, (
            f"{expected_id}: expected target {expected_target!r}, "
            f"got {pathway.target_unit!r}"
        )

    def test_inter_pathways_cross_units(self):
        """All inter-unit pathways must have different source and target."""
        for pw in INTER_UNIT_PATHWAYS:
            assert pw.source_unit != pw.target_unit, (
                f"Inter-unit pathway {pw.pathway_id} has same "
                f"source and target: {pw.source_unit}"
            )

    def test_intra_pathways_same_unit(self):
        """All intra-unit pathways must have same source and target."""
        for pw in INTRA_UNIT_PATHWAYS:
            assert pw.source_unit == pw.target_unit, (
                f"Intra-unit pathway {pw.pathway_id} has different "
                f"source ({pw.source_unit}) and target ({pw.target_unit})"
            )

    def test_pathways_have_citations(self):
        """All pathways must have a non-empty citation."""
        for pw in ALL_PATHWAYS:
            assert pw.citation, (
                f"Pathway {pw.pathway_id} has no citation"
            )

    def test_pathways_have_names(self):
        """All pathways must have a non-empty name."""
        for pw in ALL_PATHWAYS:
            assert pw.name, (
                f"Pathway {pw.pathway_id} has no name"
            )


class TestPathwayRunnerRoute:
    """Verify PathwayRunner.route() returns correct dict."""

    def test_pathway_runner_route(self, runner, synthetic_unit_outputs):
        """route() must return a dict keyed by pathway_id."""
        result = runner.route(synthetic_unit_outputs)
        assert isinstance(result, dict)

    def test_pathway_runner_route_count(self, runner, synthetic_unit_outputs):
        """route() must return one entry per inter-unit pathway."""
        result = runner.route(synthetic_unit_outputs)
        assert len(result) == 3, (
            f"Expected 3 routed pathways, got {len(result)}"
        )

    def test_pathway_runner_route_keys(self, runner, synthetic_unit_outputs):
        """route() keys must be the inter-unit pathway IDs."""
        result = runner.route(synthetic_unit_outputs)
        expected_keys = {pw.pathway_id for pw in INTER_UNIT_PATHWAYS}
        assert set(result.keys()) == expected_keys, (
            f"Expected keys {expected_keys}, got {set(result.keys())}"
        )

    def test_pathway_runner_route_values_are_tensors(
        self, runner, synthetic_unit_outputs
    ):
        """route() values must be Tensors matching source unit output shape."""
        result = runner.route(synthetic_unit_outputs)
        for pw in INTER_UNIT_PATHWAYS:
            pid = pw.pathway_id
            assert pid in result
            routed = result[pid]
            source_output = synthetic_unit_outputs[pw.source_unit]
            assert routed.shape == source_output.shape, (
                f"{pid}: routed shape {routed.shape} != "
                f"source shape {source_output.shape}"
            )


class TestPathwayRunnerWithSynthetic:
    """End-to-end routing with random unit outputs."""

    def test_pathway_runner_with_synthetic(self, runner, synthetic_unit_outputs):
        """route() must correctly route SPU, IMU, and STU outputs."""
        result = runner.route(synthetic_unit_outputs)

        # P1: SPU -> ARU
        assert "P1_SPU_ARU" in result
        assert torch.equal(result["P1_SPU_ARU"], synthetic_unit_outputs["SPU"])

        # P3: IMU -> ARU
        assert "P3_IMU_ARU" in result
        assert torch.equal(result["P3_IMU_ARU"], synthetic_unit_outputs["IMU"])

        # P5: STU -> ARU
        assert "P5_STU_ARU" in result
        assert torch.equal(result["P5_STU_ARU"], synthetic_unit_outputs["STU"])

    def test_pathway_runner_missing_source(self, runner):
        """route() must handle missing source units gracefully."""
        partial_outputs = {"SPU": torch.rand(B, T, 99)}
        result = runner.route(partial_outputs)
        # Only P1_SPU_ARU should be present (IMU and STU are missing)
        assert "P1_SPU_ARU" in result
        assert "P3_IMU_ARU" not in result
        assert "P5_STU_ARU" not in result

    def test_pathway_runner_empty_outputs(self, runner):
        """route() with empty unit_outputs must return empty dict."""
        result = runner.route({})
        assert result == {}


class TestPathwayRunnerProperties:
    """Verify PathwayRunner metadata properties."""

    def test_pathway_runner_count(self, runner):
        """pathway_count must be 3 (inter-unit only)."""
        assert runner.pathway_count == 3

    def test_pathway_runner_ids(self, runner):
        """pathway_ids must list all 3 inter-unit pathway IDs."""
        ids = runner.pathway_ids
        assert len(ids) == 3
        assert set(ids) == {"P1_SPU_ARU", "P3_IMU_ARU", "P5_STU_ARU"}
