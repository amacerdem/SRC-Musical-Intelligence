"""Brain module smoke test — full pipeline from R³/H³ to BrainOutput.

Tests the orchestrator with BCH as the only nucleus, verifying that
all four output channels (tensor, ram, neuro, psi) are produced with
correct shapes and no numerical errors.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Dict, Tuple

import pytest
import torch
from torch import Tensor

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from Musical_Intelligence.brain.orchestrator import BrainOrchestrator
from Musical_Intelligence.brain.units.spu.relays.bch import BCH
from Musical_Intelligence.contracts.dataclasses.brain_output import BrainOutput

B = 2
T = 100
R3_DIM = 97


@pytest.fixture(scope="module")
def bch() -> BCH:
    return BCH()


@pytest.fixture(scope="module")
def orchestrator(bch: BCH) -> BrainOrchestrator:
    return BrainOrchestrator(nuclei=[bch])


@pytest.fixture
def brain_output(orchestrator, bch) -> BrainOutput:
    torch.manual_seed(123)
    r3 = torch.rand(B, T, R3_DIM)
    h3 = {spec.as_tuple(): torch.rand(B, T) for spec in bch.h3_demand}
    return orchestrator.process(r3, h3)


# ======================================================================
# Shape tests
# ======================================================================

class TestShapes:
    def test_tensor_shape(self, brain_output: BrainOutput):
        # BCH exportable dims: external(4) + hybrid(4) = 8
        assert brain_output.tensor.shape == (B, T, 8)

    def test_ram_shape(self, brain_output: BrainOutput):
        assert brain_output.ram.shape == (B, T, 26)

    def test_neuro_shape(self, brain_output: BrainOutput):
        assert brain_output.neuro.shape == (B, T, 4)

    def test_psi_flat_shape(self, brain_output: BrainOutput):
        # 4 affect + 7 emotion + 5 aesthetic + 4 bodily + 4 cognitive + 4 temporal = 28
        assert brain_output.psi.flat.shape == (B, T, 28)

    def test_psi_domains(self, brain_output: BrainOutput):
        assert brain_output.psi.affect.shape[-1] == 4
        assert brain_output.psi.emotion.shape[-1] == 7
        assert brain_output.psi.aesthetic.shape[-1] == 5
        assert brain_output.psi.bodily.shape[-1] == 4
        assert brain_output.psi.cognitive.shape[-1] == 4
        assert brain_output.psi.temporal.shape[-1] == 4


# ======================================================================
# Numerical stability
# ======================================================================

class TestNumerical:
    def test_no_nan_tensor(self, brain_output: BrainOutput):
        assert not torch.isnan(brain_output.tensor).any()

    def test_no_nan_ram(self, brain_output: BrainOutput):
        assert not torch.isnan(brain_output.ram).any()

    def test_no_nan_neuro(self, brain_output: BrainOutput):
        assert not torch.isnan(brain_output.neuro).any()

    def test_no_nan_psi(self, brain_output: BrainOutput):
        assert not torch.isnan(brain_output.psi.flat).any()

    def test_no_inf(self, brain_output: BrainOutput):
        for t in [brain_output.tensor, brain_output.ram,
                  brain_output.neuro, brain_output.psi.flat]:
            assert not torch.isinf(t).any()


# ======================================================================
# Range tests
# ======================================================================

class TestRanges:
    def test_tensor_range(self, brain_output: BrainOutput):
        assert brain_output.tensor.min() >= 0.0
        assert brain_output.tensor.max() <= 1.0

    def test_neuro_range(self, brain_output: BrainOutput):
        assert brain_output.neuro.min() >= 0.0
        assert brain_output.neuro.max() <= 1.0

    def test_psi_range(self, brain_output: BrainOutput):
        assert brain_output.psi.flat.min() >= 0.0
        assert brain_output.psi.flat.max() <= 1.0

    def test_ram_non_negative(self, brain_output: BrainOutput):
        assert brain_output.ram.min() >= 0.0


# ======================================================================
# Neuro state correctness
# ======================================================================

class TestNeuroState:
    def test_da_above_zero(self, brain_output: BrainOutput):
        """BCH produces DA via consonance_signal → DA produce."""
        da = brain_output.neuro[:, :, 0]
        assert da.mean() > 0.0

    def test_serotonin_around_baseline(self, brain_output: BrainOutput):
        """BCH amplifies 5HT via pitch_forecast — should be near or above baseline."""
        serotonin = brain_output.neuro[:, :, 3]
        assert serotonin.mean() >= 0.4  # at least close to baseline 0.5

    def test_ne_at_baseline(self, brain_output: BrainOutput):
        """BCH has no NE links — NE should stay at baseline 0.5."""
        ne = brain_output.neuro[:, :, 1]
        assert abs(ne.mean().item() - 0.5) < 0.01

    def test_opi_at_baseline(self, brain_output: BrainOutput):
        """BCH has no OPI links — OPI should stay at baseline 0.5."""
        opi = brain_output.neuro[:, :, 2]
        assert abs(opi.mean().item() - 0.5) < 0.01


# ======================================================================
# RAM correctness
# ======================================================================

class TestRAM:
    def test_ic_activated(self, brain_output: BrainOutput):
        """IC is BCH's primary region — should have non-zero activation."""
        from Musical_Intelligence.brain.regions import region_index
        ic_idx = region_index("IC")
        assert brain_output.ram[:, :, ic_idx].mean() > 0.0

    def test_an_activated(self, brain_output: BrainOutput):
        """AN is in BCH's pathway — should be activated."""
        from Musical_Intelligence.brain.regions import region_index
        an_idx = region_index("AN")
        assert brain_output.ram[:, :, an_idx].mean() > 0.0

    def test_unlinked_regions_zero(self, brain_output: BrainOutput):
        """Regions not in BCH's links should have zero activation."""
        from Musical_Intelligence.brain.regions import region_index
        # NAcc is subcortical reward — BCH doesn't link to it
        nacc_idx = region_index("NAcc")
        assert brain_output.ram[:, :, nacc_idx].sum() == 0.0
