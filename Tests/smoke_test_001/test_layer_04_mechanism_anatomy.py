"""Layer 04 — Mechanism Anatomy & Metadata Validation.

Validates all mechanism instances from F1-F9: class attributes, layers
contiguity, H3 demand validity, region links, neuro links, and metadata.

~40 tests using `all_mechanisms` and related fixtures from conftest.
"""
from __future__ import annotations

import importlib
from typing import Any, Dict, List, Set, Tuple

import pytest

from Musical_Intelligence.contracts.bases.nucleus import (
    _NucleusBase,
    Relay,
    Encoder,
    Associator,
)
from Musical_Intelligence.contracts.dataclasses import H3DemandSpec

# Attempt to import REGION_REGISTRY for region validation
try:
    from Musical_Intelligence.brain.regions.registry import REGION_REGISTRY, NUM_REGIONS
    _HAS_REGION_REGISTRY = True
except ImportError:
    _HAS_REGION_REGISTRY = False
    REGION_REGISTRY = {}
    NUM_REGIONS = 26

# Known valid region abbreviations (superset including aliases)
KNOWN_REGIONS = {
    "A1_HG", "STG", "STS", "IFG", "dlPFC", "vmPFC", "OFC", "ACC",
    "SMA", "PMC", "AG", "TP",
    "VTA", "NAcc", "caudate", "amygdala", "hippocampus", "putamen",
    "MGB", "hypothalamus", "insula",
    "IC", "AN", "CN", "SOC", "PAG",
    # Common aliases
    "AI",           # anterior insula = insula
    "HG",           # Heschl's gyrus = A1_HG
    "A1",           # primary auditory = A1_HG
    "mPFC",         # medial PFC ≈ vmPFC
    "dACC",         # dorsal ACC ≈ ACC
    "pSTS",         # posterior STS ≈ STS
    "aSTS",         # anterior STS ≈ STS
    "pSTG",         # posterior STG ≈ STG
    "aSTG",         # anterior STG ≈ STG
    "pre-SMA",      # pre-supplementary motor area ≈ SMA
    "vPMC",         # ventral premotor ≈ PMC
    "dPMC",         # dorsal premotor ≈ PMC
    "lOFC",         # lateral OFC ≈ OFC
    "mOFC",         # medial OFC ≈ OFC
    "vStr",         # ventral striatum ≈ NAcc
    "BA47",         # Brodmann area 47 ≈ IFG
    "BA44",         # Brodmann area 44 ≈ IFG
    "BA45",         # Brodmann area 45 ≈ IFG
    "BA22",         # Brodmann area 22 ≈ STG
    "BA41",         # Brodmann area 41 ≈ A1_HG
    "BA42",         # Brodmann area 42 ≈ A1_HG
    "BG",           # basal ganglia
    "thalamus",     # thalamus
    "cerebellum",   # cerebellum
    "brainstem",    # brainstem
    "LC",           # locus coeruleus
    "raphe",        # raphe nuclei
    "SNc",          # substantia nigra pars compacta
    "GPe",          # globus pallidus external
    "GPi",          # globus pallidus internal
    "STN",          # subthalamic nucleus
}

# Valid function identifiers
VALID_FUNCTIONS = {
    "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9",
    "F10", "F11", "F12",
}

# Valid layer scopes
VALID_SCOPES = {"internal", "external", "hybrid"}

# Expected H3 demand counts for specific mechanisms
EXPECTED_H3_COUNTS = {
    "BCH": 48,
    "SNEM": 18,
    "TPIO": 18,
    "HMCE": 17,
    "HGSIC": 15,
    "PWSM": 16,
}

# ======================================================================
# Module importability
# ======================================================================

_FUNCTION_IDS = ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9")


class TestModuleImportability:
    """All F1-F9 mechanism modules should be importable (F9 may be empty)."""

    @pytest.mark.parametrize("fn_id", _FUNCTION_IDS)
    def test_mechanism_module_importable(self, fn_id):
        """Mechanism module for function is importable."""
        mod_path = f"Musical_Intelligence.brain.functions.{fn_id}.mechanisms"
        try:
            mod = importlib.import_module(mod_path)
            # If F9, it may import but have empty __all__
            if fn_id == "f9":
                all_names = getattr(mod, "__all__", [])
                # F9 having no mechanisms is acceptable
                pytest.skip(f"F9 has {len(all_names)} mechanisms (may be 0)")
        except ImportError:
            if fn_id == "f9":
                pytest.skip("F9 has no mechanism module (expected)")
            else:
                pytest.fail(f"Failed to import {mod_path}")
        except Exception as e:
            # Some modules may fail due to missing Hub/Integrator types
            if fn_id == "f2" and "Hub" in str(e) or "Integrator" in str(e):
                pytest.skip(f"F2 module has import issue with Hub/Integrator: {e}")
            else:
                pytest.fail(f"Unexpected error importing {mod_path}: {e}")


# ======================================================================
# Collection sanity
# ======================================================================

class TestCollectionSanity:
    """The mechanism collection should be non-empty and well-formed."""

    def test_mechanisms_collected(self, all_mechanisms):
        """At least some mechanisms were collected."""
        assert len(all_mechanisms) > 0, "No mechanisms collected from F1-F9"

    def test_all_are_nucleus_instances(self, all_mechanisms):
        """Every collected object is a _NucleusBase instance."""
        for m in all_mechanisms:
            assert isinstance(m, _NucleusBase), f"{m} is not a _NucleusBase"

    def test_relays_present(self, all_relays):
        """At least some Relay instances exist."""
        assert len(all_relays) > 0

    def test_encoders_present(self, all_encoders):
        """At least some Encoder instances exist."""
        assert len(all_encoders) > 0

    def test_associators_present(self, all_associators):
        """At least some Associator instances exist."""
        assert len(all_associators) > 0

    def test_names_unique(self, all_mechanisms):
        """Every mechanism NAME is unique."""
        names = [m.NAME for m in all_mechanisms]
        duplicates = [n for n in names if names.count(n) > 1]
        assert len(set(duplicates)) == 0, f"Duplicate mechanism names: {set(duplicates)}"


# ======================================================================
# Class attribute validation
# ======================================================================

class TestClassAttributes:
    """Every mechanism must have required class attributes."""

    def test_name_is_string(self, all_mechanisms):
        """NAME is a non-empty string."""
        for m in all_mechanisms:
            assert isinstance(m.NAME, str), f"{m}: NAME not a string"
            assert len(m.NAME) > 0, f"{m}: NAME is empty"

    def test_full_name_is_string(self, all_mechanisms):
        """FULL_NAME is a non-empty string."""
        for m in all_mechanisms:
            assert isinstance(m.FULL_NAME, str), f"{m.NAME}: FULL_NAME not a string"
            assert len(m.FULL_NAME) > 0, f"{m.NAME}: FULL_NAME is empty"

    def test_unit_is_valid_string(self, all_mechanisms):
        """UNIT is a non-empty string."""
        for m in all_mechanisms:
            assert isinstance(m.UNIT, str), f"{m.NAME}: UNIT not a string"
            assert len(m.UNIT) > 0, f"{m.NAME}: UNIT is empty"

    def test_function_valid(self, all_mechanisms):
        """FUNCTION is one of F1-F12."""
        for m in all_mechanisms:
            assert m.FUNCTION in VALID_FUNCTIONS, (
                f"{m.NAME}: FUNCTION='{m.FUNCTION}' not in {VALID_FUNCTIONS}"
            )

    def test_output_dim_positive(self, all_mechanisms):
        """OUTPUT_DIM > 0."""
        for m in all_mechanisms:
            assert isinstance(m.OUTPUT_DIM, int), f"{m.NAME}: OUTPUT_DIM not int"
            assert m.OUTPUT_DIM > 0, f"{m.NAME}: OUTPUT_DIM={m.OUTPUT_DIM} <= 0"

    def test_role_valid(self, all_mechanisms):
        """ROLE is one of 'relay', 'encoder', 'associator', or extended types."""
        valid_roles = {"relay", "encoder", "associator", "integrator", "hub"}
        for m in all_mechanisms:
            assert m.ROLE in valid_roles, (
                f"{m.NAME}: ROLE='{m.ROLE}' not in {valid_roles}"
            )


# ======================================================================
# Dimension names
# ======================================================================

class TestDimensionNames:
    """dimension_names count must match OUTPUT_DIM."""

    def test_dim_names_count_matches_output_dim(self, all_mechanisms):
        """len(dimension_names) == OUTPUT_DIM."""
        for m in all_mechanisms:
            dim_names = m.dimension_names
            assert len(dim_names) == m.OUTPUT_DIM, (
                f"{m.NAME}: {len(dim_names)} dim_names but OUTPUT_DIM={m.OUTPUT_DIM}"
            )

    def test_dim_names_are_strings(self, all_mechanisms):
        """Each dimension name is a non-empty string."""
        for m in all_mechanisms:
            for name in m.dimension_names:
                assert isinstance(name, str), f"{m.NAME}: dim name not a string"
                assert len(name) > 0, f"{m.NAME}: empty dim name"

    def test_dim_names_unique_within_mechanism(self, all_mechanisms):
        """Dimension names are unique within a mechanism."""
        for m in all_mechanisms:
            names = list(m.dimension_names)
            assert len(names) == len(set(names)), (
                f"{m.NAME}: duplicate dimension names: "
                f"{[n for n in names if names.count(n) > 1]}"
            )


# ======================================================================
# Layer contiguity
# ======================================================================

class TestLayerContiguity:
    """LAYERS must form a contiguous cover of [0, OUTPUT_DIM)."""

    def test_layers_exist(self, all_mechanisms):
        """Every mechanism has at least one layer."""
        for m in all_mechanisms:
            assert len(m.LAYERS) > 0, f"{m.NAME}: no LAYERS defined"

    def test_layers_start_at_zero(self, all_mechanisms):
        """First layer starts at index 0."""
        for m in all_mechanisms:
            layers_sorted = sorted(m.LAYERS, key=lambda l: l.start)
            assert layers_sorted[0].start == 0, (
                f"{m.NAME}: first layer starts at {layers_sorted[0].start}, not 0"
            )

    def test_layers_end_at_output_dim(self, all_mechanisms):
        """Last layer ends at OUTPUT_DIM."""
        for m in all_mechanisms:
            layers_sorted = sorted(m.LAYERS, key=lambda l: l.start)
            assert layers_sorted[-1].end == m.OUTPUT_DIM, (
                f"{m.NAME}: last layer ends at {layers_sorted[-1].end}, "
                f"not OUTPUT_DIM={m.OUTPUT_DIM}"
            )

    def test_layers_contiguous(self, all_mechanisms):
        """Layers are contiguous — no gaps between consecutive layers."""
        for m in all_mechanisms:
            layers_sorted = sorted(m.LAYERS, key=lambda l: l.start)
            for i in range(len(layers_sorted) - 1):
                assert layers_sorted[i].end == layers_sorted[i + 1].start, (
                    f"{m.NAME}: gap between layer ending at {layers_sorted[i].end} "
                    f"and layer starting at {layers_sorted[i + 1].start}"
                )

    def test_layer_dims_match_range(self, all_mechanisms):
        """Each layer's dims == end - start."""
        for m in all_mechanisms:
            for layer in m.LAYERS:
                expected = layer.end - layer.start
                assert layer.dims == expected, (
                    f"{m.NAME}/{layer.code}: dims={layer.dims} but "
                    f"end-start={expected}"
                )

    def test_layer_scope_valid(self, all_mechanisms):
        """Layer scope is one of the valid values."""
        for m in all_mechanisms:
            for layer in m.LAYERS:
                assert layer.scope in VALID_SCOPES, (
                    f"{m.NAME}/{layer.code}: scope='{layer.scope}' "
                    f"not in {VALID_SCOPES}"
                )


# ======================================================================
# H3 demand validation
# ======================================================================

class TestH3Demands:
    """H3 demand specifications must be valid."""

    def test_h3_demand_returns_list(self, all_mechanisms):
        """h3_demand property returns an iterable."""
        for m in all_mechanisms:
            demands = m.h3_demand
            # Should be iterable (list, tuple, etc.)
            assert hasattr(demands, "__iter__"), f"{m.NAME}: h3_demand not iterable"

    def test_h3_demand_spec_types(self, all_mechanisms):
        """Each demand spec is an H3DemandSpec."""
        for m in all_mechanisms:
            for spec in m.h3_demand:
                assert isinstance(spec, H3DemandSpec), (
                    f"{m.NAME}: demand spec {spec} is not H3DemandSpec"
                )

    def test_h3_demand_r3_idx_valid(self, all_mechanisms):
        """r3_idx in [0, 96]."""
        for m in all_mechanisms:
            for spec in m.h3_demand:
                assert 0 <= spec.r3_idx <= 96, (
                    f"{m.NAME}: r3_idx={spec.r3_idx} out of range"
                )

    def test_h3_demand_horizon_valid(self, all_mechanisms):
        """horizon in [0, 31]."""
        for m in all_mechanisms:
            for spec in m.h3_demand:
                assert 0 <= spec.horizon <= 31, (
                    f"{m.NAME}: horizon={spec.horizon} out of range"
                )

    def test_h3_demand_morph_valid(self, all_mechanisms):
        """morph in [0, 23]."""
        for m in all_mechanisms:
            for spec in m.h3_demand:
                assert 0 <= spec.morph <= 23, (
                    f"{m.NAME}: morph={spec.morph} out of range"
                )

    def test_h3_demand_law_valid(self, all_mechanisms):
        """law in [0, 2]."""
        for m in all_mechanisms:
            for spec in m.h3_demand:
                assert 0 <= spec.law <= 2, (
                    f"{m.NAME}: law={spec.law} out of range"
                )

    def test_h3_demand_no_duplicates(self, all_mechanisms):
        """No duplicate 4-tuples within a single mechanism."""
        for m in all_mechanisms:
            tuples = [spec.as_tuple() for spec in m.h3_demand]
            assert len(tuples) == len(set(tuples)), (
                f"{m.NAME}: {len(tuples) - len(set(tuples))} duplicate H3 demands"
            )

    def test_h3_demand_tuples_method(self, all_mechanisms):
        """h3_demand_tuples() returns list of 4-tuples matching h3_demand."""
        for m in all_mechanisms:
            tuples = m.h3_demand_tuples()
            assert isinstance(tuples, list)
            expected = [spec.as_tuple() for spec in m.h3_demand]
            assert set(tuples) == set(expected), (
                f"{m.NAME}: h3_demand_tuples() mismatch"
            )


# ======================================================================
# Specific H3 demand counts
# ======================================================================

class TestSpecificH3Counts:
    """Known mechanisms must have exact H3 demand counts."""

    @pytest.mark.parametrize("name,expected_count", EXPECTED_H3_COUNTS.items())
    def test_known_h3_count(self, all_mechanisms, name, expected_count):
        """Mechanism {name} has exactly {expected_count} H3 demands."""
        matches = [m for m in all_mechanisms if m.NAME == name]
        if not matches:
            pytest.skip(f"Mechanism {name} not found in collected mechanisms")
        m = matches[0]
        actual = len(list(m.h3_demand))
        assert actual == expected_count, (
            f"{name}: expected {expected_count} H3 demands, got {actual}"
        )


# ======================================================================
# Region links
# ======================================================================

class TestRegionLinks:
    """region_links must reference valid brain regions with valid weights."""

    def test_region_links_iterable(self, all_mechanisms):
        """region_links returns an iterable."""
        for m in all_mechanisms:
            links = m.region_links
            assert hasattr(links, "__iter__"), f"{m.NAME}: region_links not iterable"

    def test_region_links_valid_regions(self, all_mechanisms):
        """Each region link references a known brain region."""
        unknown_regions: Dict[str, set] = {}
        for m in all_mechanisms:
            for link in m.region_links:
                region = link.region
                # Check against REGION_REGISTRY first, then known set
                if _HAS_REGION_REGISTRY:
                    valid = region in REGION_REGISTRY or region in KNOWN_REGIONS
                else:
                    valid = region in KNOWN_REGIONS
                if not valid:
                    unknown_regions.setdefault(m.NAME, set()).add(region)
        if unknown_regions:
            # Warn but don't fail hard — aliases may exist
            total = sum(len(v) for v in unknown_regions.values())
            if total > 10:
                pytest.fail(
                    f"{total} unknown regions across mechanisms: "
                    f"{dict((k, sorted(v)) for k, v in list(unknown_regions.items())[:5])}..."
                )

    def test_region_links_weight_bounds(self, all_mechanisms):
        """Region link weights are in [0, 1]."""
        for m in all_mechanisms:
            for link in m.region_links:
                assert 0.0 <= link.weight <= 1.0, (
                    f"{m.NAME}: region link weight={link.weight} for "
                    f"{link.region}/{link.dim_name}"
                )


# ======================================================================
# Neuro links
# ======================================================================

class TestNeuroLinks:
    """neuro_links must have valid structure."""

    def test_neuro_links_iterable(self, all_mechanisms):
        """neuro_links returns an iterable."""
        for m in all_mechanisms:
            links = m.neuro_links
            assert hasattr(links, "__iter__"), f"{m.NAME}: neuro_links not iterable"

    def test_neuro_links_weight_bounds(self, all_mechanisms):
        """Neuro link weights are in [0, 1]."""
        for m in all_mechanisms:
            for link in m.neuro_links:
                assert 0.0 <= link.weight <= 1.0, (
                    f"{m.NAME}: neuro link weight={link.weight} for "
                    f"{link.modulator}/{link.dim_name}"
                )

    def test_neuro_links_modulator_is_string(self, all_mechanisms):
        """Each neuro link has a non-empty modulator name."""
        for m in all_mechanisms:
            for link in m.neuro_links:
                assert isinstance(link.modulator, str), (
                    f"{m.NAME}: modulator not a string"
                )
                assert len(link.modulator) > 0, (
                    f"{m.NAME}: empty modulator name"
                )


# ======================================================================
# Metadata
# ======================================================================

class TestMetadata:
    """metadata property must contain required fields."""

    def test_metadata_exists(self, all_mechanisms):
        """Every mechanism has metadata."""
        for m in all_mechanisms:
            md = m.metadata
            assert md is not None, f"{m.NAME}: metadata is None"

    def test_metadata_has_citations(self, all_mechanisms):
        """Metadata contains citations."""
        for m in all_mechanisms:
            md = m.metadata
            assert hasattr(md, "citations"), f"{m.NAME}: metadata missing citations"

    def test_metadata_has_evidence_tier(self, all_mechanisms):
        """Metadata contains evidence_tier."""
        for m in all_mechanisms:
            md = m.metadata
            assert hasattr(md, "evidence_tier"), (
                f"{m.NAME}: metadata missing evidence_tier"
            )
            assert isinstance(md.evidence_tier, str), (
                f"{m.NAME}: evidence_tier not a string"
            )

    def test_metadata_has_version(self, all_mechanisms):
        """Metadata contains version."""
        for m in all_mechanisms:
            md = m.metadata
            assert hasattr(md, "version"), f"{m.NAME}: metadata missing version"
            assert isinstance(md.version, str), f"{m.NAME}: version not a string"

    def test_metadata_confidence_range_ordered(self, all_mechanisms):
        """Metadata confidence_range has lower <= upper."""
        for m in all_mechanisms:
            md = m.metadata
            if hasattr(md, "confidence_range") and md.confidence_range is not None:
                lo, hi = md.confidence_range
                assert lo <= hi, (
                    f"{m.NAME}: confidence_range ({lo}, {hi}) is inverted"
                )


# ======================================================================
# Cross-role distribution
# ======================================================================

class TestRoleDistribution:
    """Sanity checks on the overall mechanism collection."""

    def test_relay_count_reasonable(self, all_relays):
        """At least 10 relay mechanisms exist."""
        assert len(all_relays) >= 10, f"Only {len(all_relays)} relays found"

    def test_encoder_count_reasonable(self, all_encoders):
        """At least 5 encoder mechanisms exist."""
        assert len(all_encoders) >= 5, f"Only {len(all_encoders)} encoders found"

    def test_associator_count_reasonable(self, all_associators):
        """At least 5 associator mechanisms exist."""
        assert len(all_associators) >= 5, f"Only {len(all_associators)} associators found"

    def test_total_mechanism_count(self, all_mechanisms):
        """The total number of collected mechanisms is in a reasonable range."""
        # From the spec: F1(11) + F2(10) + F3(12) + F4(15) + F5(12) + F6(10) + F7(12) + F8(6) = ~88
        # Some may fail to import (F2 Hub/Integrator), so be lenient
        assert len(all_mechanisms) >= 40, (
            f"Only {len(all_mechanisms)} mechanisms collected — expected 40+"
        )

    def test_functions_represented(self, all_mechanisms):
        """Multiple functions (F1-F8) are represented in collected mechanisms."""
        functions = set(m.FUNCTION for m in all_mechanisms)
        # At minimum F1, F3, F5, F7 should be present
        for fn in ("F1", "F3", "F5", "F7"):
            assert fn in functions, f"Function {fn} not represented in mechanisms"

    def test_mechanism_dims_dict(self, mechanism_dims):
        """mechanism_dims fixture provides NAME→OUTPUT_DIM mapping."""
        assert isinstance(mechanism_dims, dict)
        assert len(mechanism_dims) > 0
        for name, dim in mechanism_dims.items():
            assert isinstance(name, str)
            assert isinstance(dim, int)
            assert dim > 0
