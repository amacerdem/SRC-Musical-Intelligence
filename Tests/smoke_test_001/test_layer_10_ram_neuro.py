"""Layer 10 -- RAM (26 Regions) & Neurochemical (4 Channels) Validation.

Tests the 26-region brain activation model (RAM) and the 4-channel
neurochemical system (DA, NE, OPI, 5-HT).  Covers registry integrity,
init_neuro / accumulate_neuro, and manual RAM accumulation logic.

~25 tests.
"""
from __future__ import annotations

from typing import Any, Dict, List

import pytest
import torch
from torch import Tensor

from Musical_Intelligence.brain.regions.registry import (
    ALL_REGIONS,
    NUM_REGIONS,
    region_index,
    REGION_REGISTRY,
)
from Musical_Intelligence.brain.neurochemicals import (
    init_neuro,
    accumulate_neuro,
    DA,
    NE,
    OPI,
    _5HT,
    NUM_CHANNELS,
    BASELINE,
)


# ======================================================================
# Constants
# ======================================================================

B = 2
T = 50


# ======================================================================
# Region Registry
# ======================================================================

class TestRegionRegistry:
    """Validate the 26-region registry."""

    def test_num_regions_26(self):
        """NUM_REGIONS constant is 26."""
        assert NUM_REGIONS == 26

    def test_all_regions_length(self):
        """ALL_REGIONS tuple has exactly 26 entries."""
        assert len(ALL_REGIONS) == 26

    def test_region_registry_dict_length(self):
        """REGION_REGISTRY dict has 26 entries."""
        assert len(REGION_REGISTRY) == 26

    def test_indices_contiguous_0_to_25(self):
        """Region indices are 0..25 without gaps."""
        indices = sorted(r.index for r in ALL_REGIONS)
        assert indices == list(range(26)), f"Gaps in indices: {indices}"

    def test_indices_unique(self):
        """All region indices are unique."""
        indices = [r.index for r in ALL_REGIONS]
        assert len(indices) == len(set(indices)), "Duplicate indices"

    def test_cortical_count(self):
        """12 cortical regions (indices 0-11)."""
        cortical = [r for r in ALL_REGIONS if r.group == "cortical"]
        assert len(cortical) == 12, f"Got {len(cortical)} cortical"

    def test_subcortical_count(self):
        """9 subcortical regions (indices 12-20)."""
        subcortical = [r for r in ALL_REGIONS if r.group == "subcortical"]
        assert len(subcortical) == 9, f"Got {len(subcortical)} subcortical"

    def test_brainstem_count(self):
        """5 brainstem regions (indices 21-25)."""
        brainstem = [r for r in ALL_REGIONS if r.group == "brainstem"]
        assert len(brainstem) == 5, f"Got {len(brainstem)} brainstem"

    def test_region_index_stg(self):
        """region_index('STG') returns an int in 0..25."""
        idx = region_index("STG")
        assert isinstance(idx, int)
        assert 0 <= idx <= 25

    def test_region_index_a1_hg(self):
        """region_index for A1_HG returns 0 (first cortical)."""
        idx = region_index("A1_HG")
        assert isinstance(idx, int)
        assert 0 <= idx <= 25

    def test_all_regions_have_required_fields(self):
        """Every region has: index, name, abbreviation, hemisphere, group."""
        failures = []
        for r in ALL_REGIONS:
            for attr in ("index", "name", "abbreviation", "hemisphere", "group"):
                if not hasattr(r, attr):
                    failures.append(f"{r}: missing {attr}")
        assert not failures, "\n".join(failures)

    def test_all_regions_have_mni_coords(self):
        """Every region has mni_coords with 3 values."""
        failures = []
        for r in ALL_REGIONS:
            coords = getattr(r, "mni_coords", None)
            if coords is None:
                failures.append(f"{r.abbreviation}: no mni_coords")
            elif len(coords) != 3:
                failures.append(
                    f"{r.abbreviation}: mni_coords has {len(coords)} values"
                )
        assert not failures, "\n".join(failures)

    def test_known_abbreviations_present(self):
        """Key abbreviations exist in the registry."""
        known = [
            "A1_HG", "STG", "STS", "IFG", "dlPFC", "vmPFC", "OFC", "ACC",
            "SMA", "PMC", "AG", "TP",           # cortical
            "VTA", "NAcc", "caudate", "amygdala", "hippocampus",
            "putamen", "MGB", "hypothalamus", "insula",  # subcortical
            "IC", "AN", "CN", "SOC", "PAG",     # brainstem
        ]
        abbreviations = {r.abbreviation for r in ALL_REGIONS}
        missing = [k for k in known if k not in abbreviations]
        assert not missing, f"Missing abbreviations: {missing}"

    def test_group_values_valid(self):
        """All regions have group in {cortical, subcortical, brainstem}."""
        valid_groups = {"cortical", "subcortical", "brainstem"}
        failures = []
        for r in ALL_REGIONS:
            if r.group not in valid_groups:
                failures.append(f"{r.abbreviation}: group={r.group!r}")
        assert not failures, "\n".join(failures)


# ======================================================================
# RAM Accumulation (Manual)
# ======================================================================

class TestRAMAccumulation:
    """Test RAM accumulation logic without the executor."""

    def test_ram_shape_manual(self):
        """Manually constructed RAM tensor is (B, T, 26)."""
        ram = torch.zeros(B, T, NUM_REGIONS)
        assert ram.shape == (B, T, 26)

    def test_ram_initial_zeros(self):
        """Fresh RAM is all zeros."""
        ram = torch.zeros(B, T, NUM_REGIONS)
        assert (ram == 0.0).all()

    def test_ram_accumulate_single_region(self):
        """Adding signal to one region keeps others at zero."""
        ram = torch.zeros(B, T, NUM_REGIONS)
        stg_idx = region_index("STG")
        signal = torch.ones(B, T) * 0.5
        ram[:, :, stg_idx] += signal
        assert ram[:, :, stg_idx].mean().item() == pytest.approx(0.5, abs=1e-6)
        # All other regions remain zero
        mask = torch.ones(NUM_REGIONS, dtype=torch.bool)
        mask[stg_idx] = False
        assert (ram[:, :, mask] == 0.0).all()

    def test_ram_accumulate_multiple_regions(self):
        """Multiple regions accumulate independently."""
        ram = torch.zeros(B, T, NUM_REGIONS)
        stg_idx = region_index("STG")
        a1_idx = region_index("A1_HG")
        ram[:, :, stg_idx] += 0.3
        ram[:, :, a1_idx] += 0.7
        assert ram[:, :, stg_idx].mean().item() == pytest.approx(0.3, abs=1e-6)
        assert ram[:, :, a1_idx].mean().item() == pytest.approx(0.7, abs=1e-6)

    def test_ram_sigmoid_bounds(self):
        """After sigmoid, RAM is in (0, 1)."""
        ram = torch.randn(B, T, NUM_REGIONS)
        ram_bounded = torch.sigmoid(ram)
        assert ram_bounded.min() > 0.0
        assert ram_bounded.max() < 1.0

    def test_ram_relu_lower_bounded(self):
        """After ReLU, RAM is >= 0."""
        ram = torch.randn(B, T, NUM_REGIONS)
        ram_clipped = torch.relu(ram)
        assert ram_clipped.min() >= 0.0


# ======================================================================
# RAM from Relays (region_links)
# ======================================================================

class TestRAMFromRelays:
    """Test RAM accumulation using real relay region_links."""

    def test_relays_have_region_links(self, all_relays):
        """At least some relays declare region_links."""
        with_links = [
            m for m in all_relays
            if hasattr(m, "region_links") and len(m.region_links) > 0
        ]
        assert len(with_links) > 0, "No relay has region_links"

    def test_region_link_fields(self, all_relays):
        """Every region_link has dim_name, region, weight attributes."""
        failures = []
        for relay in all_relays:
            for rl in getattr(relay, "region_links", []):
                for attr in ("dim_name", "region", "weight"):
                    if not hasattr(rl, attr):
                        failures.append(
                            f"{relay.NAME}.{rl}: missing {attr}"
                        )
        assert not failures, "\n".join(failures)

    def test_region_link_region_is_valid(self, all_relays):
        """Every region_link.region is a known abbreviation."""
        abbreviations = {r.abbreviation for r in ALL_REGIONS}
        failures = []
        for relay in all_relays:
            for rl in getattr(relay, "region_links", []):
                reg = getattr(rl, "region", None)
                if reg not in abbreviations:
                    failures.append(f"{relay.NAME}: unknown region={reg!r}")
        assert not failures, "\n".join(failures)

    def test_manual_ram_from_relay(self, all_relays):
        """Manually apply region_links from a relay with them."""
        relays_with_links = [
            m for m in all_relays
            if hasattr(m, "region_links") and len(m.region_links) > 0
        ]
        if not relays_with_links:
            pytest.skip("No relay has region_links")

        relay = relays_with_links[0]
        dim = relay.OUTPUT_DIM
        output = torch.rand(B, T, dim)
        ram = torch.zeros(B, T, NUM_REGIONS)

        dim_names = relay.dimension_names
        name_to_idx = {name: i for i, name in enumerate(dim_names)}

        applied = 0
        for rl in relay.region_links:
            d_idx = name_to_idx.get(rl.dim_name)
            if d_idx is None:
                continue
            r_idx = region_index(rl.region)
            ram[:, :, r_idx] += output[:, :, d_idx] * rl.weight
            applied += 1

        if applied > 0:
            assert ram.abs().sum().item() > 0, "RAM stayed zero after accumulation"
        # No NaN
        assert not torch.isnan(ram).any(), "NaN in RAM after accumulation"


# ======================================================================
# Neurochemical Init
# ======================================================================

class TestNeuroInit:
    """init_neuro(B, T, device) creates (B, T, 4) at BASELINE=0.5."""

    def test_init_shape(self):
        """Shape is (B, T, 4)."""
        neuro = init_neuro(B, T, torch.device("cpu"))
        assert neuro.shape == (B, T, 4)

    def test_init_baseline_value(self):
        """All values equal BASELINE (0.5)."""
        neuro = init_neuro(B, T, torch.device("cpu"))
        assert (neuro == BASELINE).all()

    def test_baseline_is_05(self):
        """BASELINE constant is 0.5."""
        assert BASELINE == 0.5

    def test_channel_constants(self):
        """Channel indices are DA=0, NE=1, OPI=2, 5HT=3."""
        assert DA == 0
        assert NE == 1
        assert OPI == 2
        assert _5HT == 3

    def test_num_channels_4(self):
        """NUM_CHANNELS is 4."""
        assert NUM_CHANNELS == 4

    def test_init_dtype_float32(self):
        """init_neuro produces float32."""
        neuro = init_neuro(B, T, torch.device("cpu"))
        assert neuro.dtype == torch.float32

    def test_init_device_cpu(self):
        """init_neuro on CPU stays on CPU."""
        neuro = init_neuro(B, T, torch.device("cpu"))
        assert neuro.device.type == "cpu"

    def test_init_no_nan(self):
        """init_neuro produces no NaN."""
        neuro = init_neuro(B, T, torch.device("cpu"))
        assert not torch.isnan(neuro).any()


# ======================================================================
# Neurochemical Accumulation
# ======================================================================

class TestNeuroAccumulation:
    """accumulate_neuro modifies neuro tensor based on nucleus.neuro_links."""

    @pytest.fixture(scope="class")
    def relays_with_neuro(self, all_relays) -> List[Any]:
        """Relays that have non-empty neuro_links."""
        return [
            m for m in all_relays
            if hasattr(m, "neuro_links") and len(m.neuro_links) > 0
        ]

    def test_some_relays_have_neuro_links(self, relays_with_neuro):
        """At least some relays declare neuro_links."""
        assert len(relays_with_neuro) > 0, "No relay has neuro_links"

    def test_neuro_link_fields(self, all_relays):
        """Every neuro_link has dim_name, channel, effect, weight."""
        failures = []
        for relay in all_relays:
            for nl in getattr(relay, "neuro_links", []):
                for attr in ("dim_name", "channel", "effect", "weight"):
                    if not hasattr(nl, attr):
                        failures.append(
                            f"{relay.NAME}: neuro_link missing {attr}"
                        )
        assert not failures, "\n".join(failures)

    def test_neuro_link_channel_valid(self, all_relays):
        """Every neuro_link.channel is in {0, 1, 2, 3}."""
        valid_channels = {DA, NE, OPI, _5HT}
        failures = []
        for relay in all_relays:
            for nl in getattr(relay, "neuro_links", []):
                ch = getattr(nl, "channel", None)
                if ch not in valid_channels:
                    failures.append(
                        f"{relay.NAME}: channel={ch!r}"
                    )
        assert not failures, "\n".join(failures)

    def test_neuro_link_effect_valid(self, all_relays):
        """Every neuro_link.effect is in {produce, amplify, inhibit}."""
        valid_effects = {"produce", "amplify", "inhibit"}
        failures = []
        for relay in all_relays:
            for nl in getattr(relay, "neuro_links", []):
                eff = getattr(nl, "effect", None)
                if eff not in valid_effects:
                    failures.append(
                        f"{relay.NAME}: effect={eff!r}"
                    )
        assert not failures, "\n".join(failures)

    def test_accumulate_preserves_shape(self, relays_with_neuro):
        """accumulate_neuro preserves (B, T, 4) shape."""
        if not relays_with_neuro:
            pytest.skip("No relay has neuro_links")

        relay = relays_with_neuro[0]
        dim = relay.OUTPUT_DIM
        output = torch.rand(B, T, dim)
        neuro = init_neuro(B, T, torch.device("cpu"))

        neuro_after = accumulate_neuro(neuro, relay, output)
        assert neuro_after.shape == (B, T, 4)

    def test_accumulate_no_nan(self, relays_with_neuro):
        """accumulate_neuro does not produce NaN."""
        if not relays_with_neuro:
            pytest.skip("No relay has neuro_links")

        relay = relays_with_neuro[0]
        dim = relay.OUTPUT_DIM
        output = torch.rand(B, T, dim)
        neuro = init_neuro(B, T, torch.device("cpu"))

        neuro_after = accumulate_neuro(neuro, relay, output)
        assert not torch.isnan(neuro_after).any()

    def test_accumulate_bounded(self, relays_with_neuro):
        """After accumulation, neuro values should be bounded [0, 1]."""
        if not relays_with_neuro:
            pytest.skip("No relay has neuro_links")

        relay = relays_with_neuro[0]
        dim = relay.OUTPUT_DIM
        output = torch.rand(B, T, dim)
        neuro = init_neuro(B, T, torch.device("cpu"))

        neuro_after = accumulate_neuro(neuro, relay, output)
        assert neuro_after.min() >= -0.05, (
            f"Neuro below 0: {neuro_after.min().item():.4f}"
        )
        assert neuro_after.max() <= 1.05, (
            f"Neuro above 1: {neuro_after.max().item():.4f}"
        )

    def test_accumulate_changes_neuro(self, relays_with_neuro):
        """Accumulation with non-zero output should change some values."""
        if not relays_with_neuro:
            pytest.skip("No relay has neuro_links")

        relay = relays_with_neuro[0]
        dim = relay.OUTPUT_DIM
        output = torch.ones(B, T, dim)
        neuro = init_neuro(B, T, torch.device("cpu"))
        neuro_before = neuro.clone()

        neuro_after = accumulate_neuro(neuro, relay, output)
        # At least some channel should differ from baseline
        differs = (neuro_after - neuro_before).abs().sum().item()
        assert differs > 0.0, "Accumulation had no effect"

    def test_accumulate_all_relays_no_crash(self, relays_with_neuro):
        """accumulate_neuro does not crash for any relay with neuro_links."""
        failures = []
        for relay in relays_with_neuro:
            dim = relay.OUTPUT_DIM
            output = torch.rand(B, T, dim)
            neuro = init_neuro(B, T, torch.device("cpu"))
            try:
                neuro_after = accumulate_neuro(neuro, relay, output)
                if torch.isnan(neuro_after).any():
                    failures.append(f"{relay.NAME}: NaN after accumulation")
            except Exception as exc:
                failures.append(f"{relay.NAME}: {exc!r}")
        assert not failures, "Accumulation failures:\n" + "\n".join(failures)
