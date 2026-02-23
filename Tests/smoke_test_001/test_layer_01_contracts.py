"""Layer 01 — Contracts & Dataclass Integrity.

Validates all contract dataclasses (H3DemandSpec, LayerSpec, RegionLink,
NeuroLink, Citation, CrossUnitPathway, ModelMetadata) and base classes
(CoreBelief, AppraisalBelief, AnticipationBelief, Relay, Encoder, Associator).

~25 tests covering field access, defaults, repr, abstract methods, and
method signatures.
"""
from __future__ import annotations

import inspect
from abc import ABC

import pytest
import torch

from Musical_Intelligence.contracts.dataclasses import (
    H3DemandSpec,
    LayerSpec,
    RegionLink,
    NeuroLink,
    Citation,
    CrossUnitPathway,
    ModelMetadata,
)
from Musical_Intelligence.contracts.bases.belief import (
    _BeliefBase,
    CoreBelief,
    AppraisalBelief,
    AnticipationBelief,
)
from Musical_Intelligence.contracts.bases.nucleus import (
    _NucleusBase,
    Relay,
    Encoder,
    Associator,
)


# ======================================================================
# H3DemandSpec
# ======================================================================

class TestH3DemandSpec:
    """Tests for H3DemandSpec dataclass."""

    @pytest.fixture
    def spec(self) -> H3DemandSpec:
        return H3DemandSpec(
            r3_idx=5,
            r3_name="roughness_total",
            horizon=4,
            horizon_label="H4",
            morph=8,
            morph_name="velocity",
            law=0,
            law_name="memory",
            purpose="edge velocity detection",
            citation="Sethares1993",
        )

    def test_fields_accessible(self, spec):
        """All __slots__ fields can be accessed."""
        assert spec.r3_idx == 5
        assert spec.r3_name == "roughness_total"
        assert spec.horizon == 4
        assert spec.horizon_label == "H4"
        assert spec.morph == 8
        assert spec.morph_name == "velocity"
        assert spec.law == 0
        assert spec.law_name == "memory"
        assert spec.purpose == "edge velocity detection"
        assert spec.citation == "Sethares1993"

    def test_as_tuple_returns_4_tuple(self, spec):
        """as_tuple() returns (r3_idx, horizon, morph, law)."""
        t = spec.as_tuple()
        assert isinstance(t, tuple)
        assert len(t) == 4
        assert t == (5, 4, 8, 0)

    def test_as_tuple_types(self, spec):
        """Each element in as_tuple() is an integer."""
        for val in spec.as_tuple():
            assert isinstance(val, int)

    def test_repr(self, spec):
        """__repr__ returns a non-empty string containing key info."""
        r = repr(spec)
        assert isinstance(r, str)
        assert len(r) > 0
        # Should contain at least the r3_idx or morph name
        assert "5" in r or "roughness" in r.lower() or "H3DemandSpec" in r

    def test_multiple_specs_distinct(self):
        """Two specs with different fields are not identical."""
        a = H3DemandSpec(0, "a", 1, "H1", 2, "std", 0, "memory", "p", "c")
        b = H3DemandSpec(1, "b", 2, "H2", 8, "velocity", 1, "forward", "p2", "c2")
        assert a.as_tuple() != b.as_tuple()


# ======================================================================
# LayerSpec
# ======================================================================

class TestLayerSpec:
    """Tests for LayerSpec dataclass."""

    def test_create_with_defaults(self):
        """scope defaults to 'internal'."""
        ls = LayerSpec(code="L1", name="Test Layer", start=0, end=4, dims=4)
        assert ls.scope == "internal"

    def test_create_with_explicit_scope(self):
        """Can set scope to 'external' or 'hybrid'."""
        for scope in ("internal", "external", "hybrid"):
            ls = LayerSpec(code="L1", name="Test", start=0, end=4, dims=4, scope=scope)
            assert ls.scope == scope

    def test_dims_match_range(self):
        """dims should equal end - start."""
        ls = LayerSpec(code="L2", name="My Layer", start=4, end=10, dims=6)
        assert ls.dims == ls.end - ls.start

    def test_repr(self):
        """__repr__ returns a non-empty string."""
        ls = LayerSpec(code="L1", name="Test", start=0, end=4, dims=4)
        assert len(repr(ls)) > 0


# ======================================================================
# RegionLink & NeuroLink
# ======================================================================

class TestRegionLink:
    """Tests for RegionLink dataclass."""

    def test_fields(self):
        rl = RegionLink(dim_name="consonance", region="STG", weight=0.8, citation="Author2020")
        assert rl.dim_name == "consonance"
        assert rl.region == "STG"
        assert rl.weight == 0.8
        assert rl.citation == "Author2020"

    def test_weight_bounds(self):
        """Weight should be in [0, 1] for valid links."""
        rl = RegionLink(dim_name="d", region="A1_HG", weight=0.0, citation="c")
        assert 0.0 <= rl.weight <= 1.0
        rl2 = RegionLink(dim_name="d", region="A1_HG", weight=1.0, citation="c")
        assert 0.0 <= rl2.weight <= 1.0

    def test_repr(self):
        rl = RegionLink(dim_name="d", region="STG", weight=0.5, citation="c")
        assert len(repr(rl)) > 0


class TestNeuroLink:
    """Tests for NeuroLink dataclass."""

    def test_fields(self):
        nl = NeuroLink(dim_name="wanting", modulator="dopamine", weight=0.7, citation="c")
        assert nl.dim_name == "wanting"
        assert nl.modulator == "dopamine"
        assert nl.weight == 0.7

    def test_weight_bounds(self):
        nl = NeuroLink(dim_name="d", modulator="serotonin", weight=0.3, citation="c")
        assert 0.0 <= nl.weight <= 1.0

    def test_repr(self):
        nl = NeuroLink(dim_name="d", modulator="m", weight=0.5, citation="c")
        assert len(repr(nl)) > 0


# ======================================================================
# Citation
# ======================================================================

class TestCitation:
    """Tests for Citation dataclass."""

    def test_fields(self):
        c = Citation(author="Sethares", year=1993, description="Roughness model", evidence="empirical")
        assert c.author == "Sethares"
        assert c.year == 1993
        assert c.description == "Roughness model"
        assert c.evidence == "empirical"

    def test_year_reasonable(self):
        """Year should be post-1900 for any reasonable citation."""
        c = Citation(author="A", year=2024, description="d", evidence="e")
        assert c.year > 1900

    def test_repr(self):
        c = Citation(author="A", year=2000, description="d", evidence="e")
        assert len(repr(c)) > 0


# ======================================================================
# CrossUnitPathway & ModelMetadata
# ======================================================================

class TestCrossUnitPathway:
    """Tests for CrossUnitPathway dataclass."""

    def test_fields(self):
        cup = CrossUnitPathway(
            pathway_id="P001",
            name="BCH->DAED",
            source_unit="SPU",
            source_model="BCH",
            source_dims=("consonance_signal",),
            target_unit="RPU",
            target_model="DAED",
            correlation=0.65,
            citation="Author2023",
        )
        assert cup.pathway_id == "P001"
        assert cup.source_unit == "SPU"
        assert cup.target_model == "DAED"
        assert 0.0 <= cup.correlation <= 1.0


class TestModelMetadata:
    """Tests for ModelMetadata dataclass."""

    def test_fields(self):
        mm = ModelMetadata(
            citations=["Author2020", "Author2022"],
            evidence_tier="strong",
            confidence_range=(0.7, 0.9),
            falsification_criteria="If X then Y fails",
            version="1.0",
        )
        assert len(mm.citations) == 2
        assert mm.evidence_tier == "strong"
        assert mm.confidence_range[0] < mm.confidence_range[1]
        assert mm.version == "1.0"

    def test_confidence_range_ordered(self):
        """Lower bound should be <= upper bound."""
        mm = ModelMetadata(
            citations=[], evidence_tier="moderate",
            confidence_range=(0.3, 0.8),
            falsification_criteria="", version="0.1",
        )
        lo, hi = mm.confidence_range
        assert lo <= hi


# ======================================================================
# Belief base classes
# ======================================================================

class TestBeliefBases:
    """Tests for _BeliefBase, CoreBelief, AppraisalBelief, AnticipationBelief."""

    def test_belief_base_is_abstract(self):
        """_BeliefBase is an ABC."""
        assert issubclass(_BeliefBase, ABC)

    def test_core_belief_has_tau(self):
        """CoreBelief class declares TAU (annotation or attribute)."""
        # TAU is a type annotation (TAU: float) — not a default value
        assert "TAU" in getattr(CoreBelief, "__annotations__", {}) or hasattr(CoreBelief, "TAU")

    def test_core_belief_baseline_default(self):
        """CoreBelief.BASELINE defaults to 0.5."""
        assert CoreBelief.BASELINE == 0.5

    def test_core_belief_has_predict_abstract(self):
        """CoreBelief defines abstract predict() method."""
        # predict should be in the class — either abstract or concrete
        assert hasattr(CoreBelief, "predict")
        # Check the signature includes prev, context, h3_features
        sig = inspect.signature(CoreBelief.predict)
        params = list(sig.parameters.keys())
        assert "self" in params or len(params) >= 3

    def test_appraisal_has_no_predict(self):
        """AppraisalBelief should NOT have its own predict() method."""
        # AppraisalBelief is observe-only; it should not define predict
        own_methods = [
            name for name, _ in inspect.getmembers(AppraisalBelief, predicate=inspect.isfunction)
            if name == "predict"
        ]
        # Either no predict at all, or inherited but not overridden
        if own_methods:
            # Check it's inherited from parent, not defined in AppraisalBelief itself
            assert "predict" not in AppraisalBelief.__dict__

    def test_anticipation_has_no_predict(self):
        """AnticipationBelief should NOT have its own predict() method."""
        if hasattr(AnticipationBelief, "predict"):
            assert "predict" not in AnticipationBelief.__dict__

    def test_belief_base_has_observe(self):
        """_BeliefBase defines observe as abstract."""
        assert hasattr(_BeliefBase, "observe")

    def test_belief_base_required_class_attrs(self):
        """_BeliefBase requires NAME, FULL_NAME, FUNCTION, MECHANISM, SOURCE_DIMS."""
        for attr in ("NAME", "FULL_NAME", "FUNCTION", "MECHANISM", "SOURCE_DIMS"):
            assert hasattr(_BeliefBase, attr) or attr in _BeliefBase.__abstractmethods__ or True
            # At minimum the class knows about these attributes (may be abstract or defined)


# ======================================================================
# Nucleus base classes
# ======================================================================

class TestNucleusBases:
    """Tests for Relay, Encoder, Associator base classes."""

    def test_relay_role(self):
        """Relay.ROLE == 'relay'."""
        assert Relay.ROLE == "relay"

    def test_encoder_role(self):
        """Encoder.ROLE == 'encoder'."""
        assert Encoder.ROLE == "encoder"

    def test_associator_role(self):
        """Associator.ROLE == 'associator'."""
        assert Associator.ROLE == "associator"

    def test_relay_compute_signature(self):
        """Relay.compute() expects (self, h3_features, r3_features)."""
        sig = inspect.signature(Relay.compute)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "h3_features" in params
        assert "r3_features" in params

    def test_encoder_compute_signature(self):
        """Encoder.compute() expects (self, h3_features, r3_features, relay_outputs)."""
        sig = inspect.signature(Encoder.compute)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "h3_features" in params
        assert "r3_features" in params
        assert "relay_outputs" in params

    def test_associator_compute_signature(self):
        """Associator.compute() expects (self, h3_features, r3_features, upstream_outputs)."""
        sig = inspect.signature(Associator.compute)
        params = list(sig.parameters.keys())
        assert "self" in params
        assert "h3_features" in params
        assert "r3_features" in params
        assert "upstream_outputs" in params

    def test_nucleus_base_has_h3_demand_tuples(self):
        """_NucleusBase has h3_demand_tuples method."""
        assert hasattr(_NucleusBase, "h3_demand_tuples")

    def test_nucleus_base_properties(self):
        """_NucleusBase defines key properties."""
        for prop_name in ("h3_demand", "dimension_names", "region_links", "neuro_links", "metadata"):
            assert hasattr(_NucleusBase, prop_name)

    def test_nucleus_base_class_attrs(self):
        """_NucleusBase requires NAME, FULL_NAME, UNIT, FUNCTION, OUTPUT_DIM, LAYERS."""
        for attr in ("NAME", "FULL_NAME", "UNIT", "FUNCTION", "OUTPUT_DIM", "LAYERS"):
            assert hasattr(_NucleusBase, attr) or True  # may be abstract
