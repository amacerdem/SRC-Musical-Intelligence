"""Unit tests for all 10 brain mechanisms.

Tests mechanism names, output dimensions, value ranges, h3_demand, the
MechanismRunner, and the _aggregate_to_10d helper shared by all mechanisms.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

import pytest
import torch
from torch import Tensor

from Musical_Intelligence.brain.mechanisms.runner import MechanismRunner
from Musical_Intelligence.brain.mechanisms.ppc import PPC
from Musical_Intelligence.brain.mechanisms.tpc import TPC
from Musical_Intelligence.brain.mechanisms.bep import BEP
from Musical_Intelligence.brain.mechanisms.asa import ASA
from Musical_Intelligence.brain.mechanisms.tmh import TMH
from Musical_Intelligence.brain.mechanisms.mem import MEM
from Musical_Intelligence.brain.mechanisms.syn import SYN
from Musical_Intelligence.brain.mechanisms.aed import AED
from Musical_Intelligence.brain.mechanisms.cpd import CPD
from Musical_Intelligence.brain.mechanisms.c0p import C0P


# ---------------------------------------------------------------------------
# The 10 mechanism classes in canonical order
# ---------------------------------------------------------------------------

ALL_MECHANISM_CLASSES = [PPC, TPC, BEP, ASA, TMH, MEM, SYN, AED, CPD, C0P]

EXPECTED_NAMES = {"PPC", "TPC", "BEP", "ASA", "TMH", "MEM", "SYN", "AED", "CPD", "C0P"}

B, T = 2, 50  # batch size, time steps


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(scope="module")
def all_mechanisms():
    """Instantiate all 10 mechanisms."""
    return [cls() for cls in ALL_MECHANISM_CLASSES]


@pytest.fixture(scope="module")
def synthetic_r3() -> Tensor:
    """Synthetic R3 features: (B, T, 97) in [0, 1]."""
    torch.manual_seed(99)
    return torch.rand(B, T, 97)


@pytest.fixture(scope="module")
def synthetic_h3(all_mechanisms) -> dict:
    """Build synthetic H3 features covering all mechanism demands.

    Creates a (B, T) tensor for every 4-tuple demanded by any mechanism.
    """
    torch.manual_seed(99)
    h3: dict = {}
    for mech in all_mechanisms:
        for key in mech.h3_demand:
            if key not in h3:
                h3[key] = torch.rand(B, T)
    return h3


@pytest.fixture(scope="module")
def runner_with_results(synthetic_h3, synthetic_r3):
    """MechanismRunner with all 10 mechanisms computed."""
    runner = MechanismRunner()
    runner.run(synthetic_h3, synthetic_r3)
    return runner


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

class TestMechanismNames:
    """Verify all 10 mechanisms have correct NAME constants."""

    def test_mechanism_names(self, all_mechanisms):
        """All 10 mechanisms must have unique NAME values matching the
        expected set.
        """
        names = {m.NAME for m in all_mechanisms}
        assert names == EXPECTED_NAMES, (
            f"Expected names {EXPECTED_NAMES}, got {names}"
        )

    @pytest.mark.parametrize("cls", ALL_MECHANISM_CLASSES)
    def test_mechanism_has_nonempty_name(self, cls):
        """Each mechanism class must have a non-empty NAME."""
        mech = cls()
        assert mech.NAME, f"{cls.__name__} has empty NAME"

    @pytest.mark.parametrize("cls", ALL_MECHANISM_CLASSES)
    def test_mechanism_has_nonempty_fullname(self, cls):
        """Each mechanism class must have a non-empty FULL_NAME."""
        mech = cls()
        assert mech.FULL_NAME, f"{cls.__name__} has empty FULL_NAME"


class TestMechanismOutputDim:
    """Verify all mechanisms produce (B, T, 30) output."""

    @pytest.mark.parametrize("cls", ALL_MECHANISM_CLASSES)
    def test_mechanism_output_dim(self, cls, synthetic_h3, synthetic_r3):
        """Each mechanism compute() must return (B, T, 30)."""
        mech = cls()
        out = mech.compute(synthetic_h3, synthetic_r3)
        assert out.shape == (B, T, 30), (
            f"{cls.__name__}: expected ({B}, {T}, 30), got {out.shape}"
        )


class TestMechanismOutputRange:
    """Verify all mechanism outputs are in [0, 1]."""

    @pytest.mark.parametrize("cls", ALL_MECHANISM_CLASSES)
    def test_mechanism_output_range(self, cls, synthetic_h3, synthetic_r3):
        """Each mechanism output tensor must have values in [0, 1]."""
        mech = cls()
        out = mech.compute(synthetic_h3, synthetic_r3)
        assert out.min().item() >= 0.0, (
            f"{cls.__name__}: min {out.min().item()} < 0"
        )
        assert out.max().item() <= 1.0, (
            f"{cls.__name__}: max {out.max().item()} > 1"
        )


class TestMechanismH3Demand:
    """Verify all mechanisms declare non-empty h3_demand."""

    @pytest.mark.parametrize("cls", ALL_MECHANISM_CLASSES)
    def test_mechanism_h3_demand_nonempty(self, cls):
        """Each mechanism must declare at least one H3 demand tuple."""
        mech = cls()
        demand = mech.h3_demand
        assert isinstance(demand, set), (
            f"{cls.__name__}: h3_demand is {type(demand)}, expected set"
        )
        assert len(demand) > 0, (
            f"{cls.__name__}: h3_demand is empty"
        )

    @pytest.mark.parametrize("cls", ALL_MECHANISM_CLASSES)
    def test_mechanism_h3_demand_valid_tuples(self, cls):
        """Each H3 demand tuple must be a 4-tuple of non-negative ints."""
        mech = cls()
        for t in mech.h3_demand:
            assert isinstance(t, tuple) and len(t) == 4, (
                f"{cls.__name__}: demand entry {t} is not a 4-tuple"
            )
            r3_idx, horizon, morph, law = t
            assert 0 <= r3_idx <= 96, (
                f"{cls.__name__}: r3_idx {r3_idx} out of range"
            )
            assert 0 <= horizon <= 31, (
                f"{cls.__name__}: horizon {horizon} out of range"
            )
            assert 0 <= morph <= 23, (
                f"{cls.__name__}: morph {morph} out of range"
            )
            assert 0 <= law <= 2, (
                f"{cls.__name__}: law {law} out of range"
            )


class TestMechanismRunnerComputesAll:
    """Verify MechanismRunner.run() populates all 10 mechanisms."""

    def test_mechanism_runner_computes_all(self, runner_with_results):
        """After run(), get() must succeed for all 10 mechanism names."""
        for name in EXPECTED_NAMES:
            out = runner_with_results.get(name)
            assert isinstance(out, Tensor), (
                f"MechanismRunner.get({name!r}) did not return a Tensor"
            )
            assert out.shape == (B, T, 30), (
                f"MechanismRunner.get({name!r}): "
                f"expected ({B}, {T}, 30), got {out.shape}"
            )

    def test_mechanism_runner_h3_demand_union(self):
        """MechanismRunner.h3_demand must be the union of all mechanism demands."""
        runner = MechanismRunner()
        union_demand = runner.h3_demand
        assert isinstance(union_demand, set)
        assert len(union_demand) > 0

        # Verify it is the union of individual demands
        individual_union = set()
        for cls in ALL_MECHANISM_CLASSES:
            individual_union |= cls().h3_demand
        assert union_demand == individual_union

    def test_mechanism_runner_get_before_run_raises(self):
        """get() before run() must raise RuntimeError."""
        runner = MechanismRunner()
        with pytest.raises(RuntimeError, match="not cached"):
            runner.get("PPC")


class TestAggregateTo10D:
    """Verify the _aggregate_to_10d helper handles all K sizes."""

    @pytest.mark.parametrize("K", [5, 10, 15])
    def test_aggregate_to_10d_shapes(self, K):
        """_aggregate_to_10d must produce (B, T, 10) for K<10, K==10, K>10."""
        feats = [torch.rand(B, T) for _ in range(K)]
        result = PPC._aggregate_to_10d(feats, B, T, torch.device("cpu"))
        assert result.shape == (B, T, 10), (
            f"K={K}: expected ({B}, {T}, 10), got {result.shape}"
        )

    def test_aggregate_to_10d_empty(self):
        """_aggregate_to_10d with empty feats must return zeros (B, T, 10)."""
        result = PPC._aggregate_to_10d([], B, T, torch.device("cpu"))
        assert result.shape == (B, T, 10)
        assert result.sum().item() == 0.0

    def test_aggregate_to_10d_padding(self):
        """K < 10: trailing dimensions must be zero-padded."""
        K = 3
        feats = [torch.ones(B, T) for _ in range(K)]
        result = PPC._aggregate_to_10d(feats, B, T, torch.device("cpu"))
        # First K dims should be 1.0, remaining should be 0.0
        assert (result[..., :K] == 1.0).all()
        assert (result[..., K:] == 0.0).all()
