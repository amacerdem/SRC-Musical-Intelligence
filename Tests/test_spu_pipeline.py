"""Integration tests for SPU nuclei: BCH (Relay) + PSCL (Encoder).

Tests validate:
1. Nucleus contract compliance (validate_constants)
2. Compute shape correctness
3. Executor integration (depth-ordered BCH → PSCL)
4. Output ranges and NaN safety
"""
from __future__ import annotations

import torch

from Musical_Intelligence.brain.executor import execute
from Musical_Intelligence.brain.units.spu.encoders.pscl import PSCL
from Musical_Intelligence.brain.units.spu.relays.bch import BCH

B, T = 2, 100  # batch, time


def _mock_h3(nucleus) -> dict:
    """Create mock H³ features for all demands of a nucleus."""
    return {spec.as_tuple(): torch.rand(B, T) for spec in nucleus.h3_demand}


def _mock_r3() -> torch.Tensor:
    """Create mock R³ features: (B, T, 97)."""
    return torch.rand(B, T, 97)


# ── BCH Tests ─────────────────────────────────────────────────────────


class TestBCHRelay:
    """Tests for BCH Relay (depth 0, 16D)."""

    def test_validate_constants(self):
        """BCH passes Nucleus.validate_constants() with no errors."""
        bch = BCH()
        errors = bch.validate_constants()
        assert errors == [], f"BCH validation errors: {errors}"

    def test_role_and_depth(self):
        """BCH is a Relay at depth 0."""
        bch = BCH()
        assert bch.ROLE == "relay"
        assert bch.PROCESSING_DEPTH == 0
        assert bch.UNIT == "SPU"

    def test_output_dim(self):
        """BCH has 16D output (E4 + M4 + P4 + F4)."""
        bch = BCH()
        assert bch.OUTPUT_DIM == 16
        assert len(bch.dimension_names) == 16

    def test_h3_demand_count(self):
        """BCH demands exactly 50 H³ tuples."""
        bch = BCH()
        assert len(bch.h3_demand) == 50

    def test_h3_demand_unique(self):
        """All BCH H³ demands have unique 4-tuples."""
        bch = BCH()
        tuples = [spec.as_tuple() for spec in bch.h3_demand]
        assert len(tuples) == len(set(tuples)), "Duplicate H³ demands"

    def test_compute_shape(self):
        """BCH.compute() returns (B, T, 16)."""
        bch = BCH()
        h3 = _mock_h3(bch)
        r3 = _mock_r3()
        out = bch.compute(h3, r3)
        assert out.shape == (B, T, 16), f"Expected (2, 100, 16), got {out.shape}"

    def test_compute_no_nan(self):
        """BCH produces no NaN with valid inputs."""
        bch = BCH()
        h3 = _mock_h3(bch)
        r3 = _mock_r3()
        out = bch.compute(h3, r3)
        assert not torch.isnan(out).any(), "BCH output contains NaN"

    def test_compute_output_range(self):
        """All BCH outputs in [0, 1]."""
        bch = BCH()
        h3 = _mock_h3(bch)
        r3 = _mock_r3()
        out = bch.compute(h3, r3)
        assert out.min() >= 0.0, f"BCH min={out.min().item():.4f} < 0"
        assert out.max() <= 1.0, f"BCH max={out.max().item():.4f} > 1"

    def test_scope_partition(self):
        """BCH scope: E+M internal (0-7), P hybrid (8-11), F external (12-15)."""
        bch = BCH()
        assert bch.internal_dims == (0, 1, 2, 3, 4, 5, 6, 7)
        assert bch.hybrid_dims == (8, 9, 10, 11)
        assert bch.external_dims == (12, 13, 14, 15)
        # Routable = internal + hybrid = 0-11
        assert bch.routable_dims == tuple(range(12))
        # Exportable = hybrid + external = 8-15
        assert bch.exportable_dims == tuple(range(8, 16))

    def test_region_links_valid(self):
        """All BCH region_links reference valid dimension names."""
        bch = BCH()
        valid_dims = set(bch.dimension_names)
        for rl in bch.region_links:
            assert rl.dim_name in valid_dims, f"Invalid dim: {rl.dim_name}"

    def test_neuro_links_valid(self):
        """All BCH neuro_links reference valid dimension names."""
        bch = BCH()
        valid_dims = set(bch.dimension_names)
        for nl in bch.neuro_links:
            assert nl.dim_name in valid_dims, f"Invalid dim: {nl.dim_name}"


# ── PSCL Tests ────────────────────────────────────────────────────────


class TestPSCLEncoder:
    """Tests for PSCL Encoder (depth 1, 16D)."""

    def test_validate_constants(self):
        """PSCL passes Nucleus.validate_constants() with no errors."""
        pscl = PSCL()
        errors = pscl.validate_constants()
        assert errors == [], f"PSCL validation errors: {errors}"

    def test_role_and_depth(self):
        """PSCL is an Encoder at depth 1."""
        pscl = PSCL()
        assert pscl.ROLE == "encoder"
        assert pscl.PROCESSING_DEPTH == 1
        assert pscl.UNIT == "SPU"
        assert pscl.UPSTREAM_READS == ("BCH",)

    def test_output_dim(self):
        """PSCL has 16D output."""
        pscl = PSCL()
        assert pscl.OUTPUT_DIM == 16
        assert len(pscl.dimension_names) == 16

    def test_h3_demand_count(self):
        """PSCL demands exactly 20 H³ tuples."""
        pscl = PSCL()
        assert len(pscl.h3_demand) == 20

    def test_h3_demand_unique(self):
        """All PSCL H³ demands have unique 4-tuples."""
        pscl = PSCL()
        tuples = [spec.as_tuple() for spec in pscl.h3_demand]
        assert len(tuples) == len(set(tuples)), "Duplicate H³ demands"

    def test_compute_shape(self):
        """PSCL.compute() returns (B, T, 16)."""
        pscl = PSCL()
        h3 = _mock_h3(pscl)
        r3 = _mock_r3()
        bch_out = torch.rand(B, T, 16)
        out = pscl.compute(h3, r3, {"BCH": bch_out})
        assert out.shape == (B, T, 16), f"Expected (2, 100, 16), got {out.shape}"

    def test_compute_no_nan(self):
        """PSCL produces no NaN with valid inputs."""
        pscl = PSCL()
        h3 = _mock_h3(pscl)
        r3 = _mock_r3()
        bch_out = torch.rand(B, T, 16)
        out = pscl.compute(h3, r3, {"BCH": bch_out})
        assert not torch.isnan(out).any(), "PSCL output contains NaN"

    def test_compute_output_range(self):
        """PSCL outputs: [0,1] for all except F1 which is [-1,1]."""
        pscl = PSCL()
        h3 = _mock_h3(pscl)
        r3 = _mock_r3()
        bch_out = torch.rand(B, T, 16)
        out = pscl.compute(h3, r3, {"BCH": bch_out})
        # All except dim 13 (F1:salience_direction) in [0, 1]
        non_f1 = torch.cat([out[:, :, :13], out[:, :, 14:]], dim=-1)
        assert non_f1.min() >= 0.0, f"PSCL non-F1 min={non_f1.min().item():.4f} < 0"
        assert non_f1.max() <= 1.0, f"PSCL non-F1 max={non_f1.max().item():.4f} > 1"
        # F1 in [-1, 1]
        f1 = out[:, :, 13]
        assert f1.min() >= -1.0, f"PSCL F1 min={f1.min().item():.4f} < -1"
        assert f1.max() <= 1.0, f"PSCL F1 max={f1.max().item():.4f} > 1"

    def test_scope_partition(self):
        """PSCL scope: E+M internal, P hybrid, F external."""
        pscl = PSCL()
        assert pscl.internal_dims == (0, 1, 2, 3, 4, 5, 6, 7)
        assert pscl.hybrid_dims == (8, 9, 10, 11)
        assert pscl.external_dims == (12, 13, 14, 15)

    def test_region_links_valid(self):
        """All PSCL region_links reference valid dimension names."""
        pscl = PSCL()
        valid_dims = set(pscl.dimension_names)
        for rl in pscl.region_links:
            assert rl.dim_name in valid_dims, f"Invalid dim: {rl.dim_name}"

    def test_neuro_links_valid(self):
        """All PSCL neuro_links reference valid dimension names."""
        pscl = PSCL()
        valid_dims = set(pscl.dimension_names)
        for nl in pscl.neuro_links:
            assert nl.dim_name in valid_dims, f"Invalid dim: {nl.dim_name}"


# ── Executor Integration Tests ────────────────────────────────────────


class TestExecutorIntegration:
    """Tests for BCH + PSCL through the executor engine."""

    def test_executor_bch_alone(self):
        """Execute BCH alone through executor."""
        bch = BCH()
        h3 = _mock_h3(bch)
        r3 = _mock_r3()
        outputs, ram, neuro = execute([bch], h3, r3)
        assert "BCH" in outputs
        assert outputs["BCH"].shape == (B, T, 16)
        assert ram.shape == (B, T, 26)
        assert neuro.shape == (B, T, 4)

    def test_executor_bch_pscl_pipeline(self):
        """Execute BCH + PSCL through executor — depth ordering works."""
        bch = BCH()
        pscl = PSCL()
        # Merge all demands
        all_demands = bch.h3_demand_tuples() | pscl.h3_demand_tuples()
        h3 = {t: torch.rand(B, T) for t in all_demands}
        r3 = _mock_r3()
        # Pass in reverse order — executor should sort by depth
        outputs, ram, neuro = execute([pscl, bch], h3, r3)
        assert "BCH" in outputs
        assert "PSCL" in outputs
        assert outputs["BCH"].shape == (B, T, 16)
        assert outputs["PSCL"].shape == (B, T, 16)
        assert ram.shape == (B, T, 26)
        assert neuro.shape == (B, T, 4)

    def test_executor_no_nan(self):
        """Executor pipeline produces no NaN in outputs, RAM, neuro."""
        bch = BCH()
        pscl = PSCL()
        all_demands = bch.h3_demand_tuples() | pscl.h3_demand_tuples()
        h3 = {t: torch.rand(B, T) for t in all_demands}
        r3 = _mock_r3()
        outputs, ram, neuro = execute([bch, pscl], h3, r3)
        for name, tensor in outputs.items():
            assert not torch.isnan(tensor).any(), f"{name} contains NaN"
        assert not torch.isnan(ram).any(), "RAM contains NaN"
        assert not torch.isnan(neuro).any(), "Neuro contains NaN"

    def test_executor_ram_nonzero(self):
        """RAM should have some non-zero activations after BCH+PSCL."""
        bch = BCH()
        pscl = PSCL()
        all_demands = bch.h3_demand_tuples() | pscl.h3_demand_tuples()
        h3 = {t: torch.rand(B, T) for t in all_demands}
        r3 = _mock_r3()
        _, ram, _ = execute([bch, pscl], h3, r3)
        assert ram.abs().sum() > 0, "RAM is all zeros — region links not working"

    def test_h3_demands_disjoint_or_shared(self):
        """BCH and PSCL demands can overlap — executor handles merged set."""
        bch = BCH()
        pscl = PSCL()
        bch_tuples = bch.h3_demand_tuples()
        pscl_tuples = pscl.h3_demand_tuples()
        merged = bch_tuples | pscl_tuples
        # Total demands <= sum (some may overlap)
        assert len(merged) <= len(bch_tuples) + len(pscl_tuples)
        # Both should be non-empty subsets
        assert len(bch_tuples) == 50
        assert len(pscl_tuples) == 20
