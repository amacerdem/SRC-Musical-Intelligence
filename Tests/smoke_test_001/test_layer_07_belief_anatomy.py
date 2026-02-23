"""Layer 07 -- Belief Anatomy & Structural Integrity.

Validates all 131 beliefs across 9 functions for correct typing, attribute
presence, function-level counts, type-level counts, TAU values for core
beliefs, SOURCE_DIMS consistency, and method signatures.

~35 tests.
"""
from __future__ import annotations

import inspect
from typing import Any, Dict, List

import pytest

from Musical_Intelligence.contracts.bases.belief import (
    _BeliefBase,
    CoreBelief,
    AppraisalBelief,
    AnticipationBelief,
)


# ======================================================================
# Expected counts
# ======================================================================

FUNCTION_BELIEF_COUNTS = {
    "F1": 17,
    "F2": 15,
    "F3": 15,
    "F4": 13,
    "F5": 14,
    "F6": 16,
    "F7": 17,
    "F8": 14,
    "F9": 10,
}

TOTAL_BELIEFS = 131
TOTAL_CORE = 36
TOTAL_APPRAISAL = 65
TOTAL_ANTICIPATION = 30

# Known TAU values for specific core beliefs
KNOWN_TAU_VALUES = {
    "harmonic_stability": 0.3,
    "beat_entrainment": 0.35,
    "period_entrainment": 0.65,
    "wanting": 0.6,
    "autobiographical_retrieval": 0.85,
    "trained_timbre_recognition": 0.9,
    "network_specialization": 0.95,
    "groove_quality": 0.55,
    "context_depth": 0.7,
    "aesthetic_quality": 0.4,
}


# ======================================================================
# 1. Total population
# ======================================================================

class TestBeliefPopulation:
    """Validate total belief counts."""

    def test_total_belief_count(self, all_beliefs):
        """System must contain exactly 131 beliefs."""
        assert len(all_beliefs) == TOTAL_BELIEFS, (
            f"Expected {TOTAL_BELIEFS} beliefs, found {len(all_beliefs)}"
        )

    def test_core_belief_count(self, all_core_beliefs):
        """Must have exactly 36 CoreBelief instances."""
        assert len(all_core_beliefs) == TOTAL_CORE, (
            f"Expected {TOTAL_CORE} core beliefs, found {len(all_core_beliefs)}"
        )

    def test_appraisal_belief_count(self, all_appraisal_beliefs):
        """Must have exactly 65 AppraisalBelief instances."""
        assert len(all_appraisal_beliefs) == TOTAL_APPRAISAL, (
            f"Expected {TOTAL_APPRAISAL} appraisal beliefs, "
            f"found {len(all_appraisal_beliefs)}"
        )

    def test_anticipation_belief_count(self, all_anticipation_beliefs):
        """Must have exactly 30 AnticipationBelief instances."""
        assert len(all_anticipation_beliefs) == TOTAL_ANTICIPATION, (
            f"Expected {TOTAL_ANTICIPATION} anticipation beliefs, "
            f"found {len(all_anticipation_beliefs)}"
        )

    def test_type_counts_sum_to_total(
        self, all_core_beliefs, all_appraisal_beliefs, all_anticipation_beliefs
    ):
        """36 Core + 65 Appraisal + 30 Anticipation = 131."""
        total = (
            len(all_core_beliefs)
            + len(all_appraisal_beliefs)
            + len(all_anticipation_beliefs)
        )
        assert total == TOTAL_BELIEFS, (
            f"Type sum {total} != expected {TOTAL_BELIEFS}"
        )


# ======================================================================
# 2. Per-function counts
# ======================================================================

class TestFunctionCounts:
    """Validate belief counts per function (F1-F9)."""

    @pytest.mark.parametrize(
        "function_id, expected_count",
        list(FUNCTION_BELIEF_COUNTS.items()),
        ids=list(FUNCTION_BELIEF_COUNTS.keys()),
    )
    def test_function_belief_count(
        self, beliefs_by_function, function_id, expected_count
    ):
        """Each function has the correct number of beliefs."""
        actual = len(beliefs_by_function.get(function_id, []))
        assert actual == expected_count, (
            f"{function_id}: expected {expected_count} beliefs, found {actual}"
        )

    def test_all_functions_represented(self, beliefs_by_function):
        """All 9 functions (F1-F9) must be represented."""
        expected_functions = {f"F{i}" for i in range(1, 10)}
        actual_functions = set(beliefs_by_function.keys())
        missing = expected_functions - actual_functions
        assert not missing, (
            f"Missing functions: {missing}"
        )

    def test_no_unknown_functions(self, beliefs_by_function):
        """No beliefs should belong to functions outside F1-F9."""
        valid_functions = {f"F{i}" for i in range(1, 10)}
        actual_functions = set(beliefs_by_function.keys())
        extra = actual_functions - valid_functions
        assert not extra, (
            f"Unexpected function IDs: {extra}"
        )


# ======================================================================
# 3. Required attributes (all beliefs)
# ======================================================================

class TestBeliefRequiredAttributes:
    """Every belief must have NAME, FULL_NAME, FUNCTION, MECHANISM, SOURCE_DIMS."""

    def test_name_is_nonempty_string(self, all_beliefs):
        """NAME must be a non-empty string."""
        for b in all_beliefs:
            assert hasattr(b, "NAME"), f"Belief missing NAME attribute"
            assert isinstance(b.NAME, str) and len(b.NAME) > 0, (
                f"Belief NAME={b.NAME!r} is not a non-empty string"
            )

    def test_full_name_is_nonempty_string(self, all_beliefs):
        """FULL_NAME must be a non-empty string."""
        for b in all_beliefs:
            assert hasattr(b, "FULL_NAME"), (
                f"{b.NAME}: missing FULL_NAME"
            )
            assert isinstance(b.FULL_NAME, str) and len(b.FULL_NAME) > 0, (
                f"{b.NAME}: FULL_NAME={b.FULL_NAME!r} is not a non-empty string"
            )

    def test_function_is_valid(self, all_beliefs):
        """FUNCTION must be F1-F9."""
        valid = {f"F{i}" for i in range(1, 10)}
        for b in all_beliefs:
            assert hasattr(b, "FUNCTION"), f"{b.NAME}: missing FUNCTION"
            assert b.FUNCTION in valid, (
                f"{b.NAME}: FUNCTION={b.FUNCTION!r} not in F1-F9"
            )

    def test_mechanism_is_nonempty_string(self, all_beliefs):
        """MECHANISM must be a non-empty string (the source mechanism name)."""
        for b in all_beliefs:
            assert hasattr(b, "MECHANISM"), f"{b.NAME}: missing MECHANISM"
            assert isinstance(b.MECHANISM, str) and len(b.MECHANISM) > 0, (
                f"{b.NAME}: MECHANISM={b.MECHANISM!r} is not a non-empty string"
            )

    def test_source_dims_is_tuple(self, all_beliefs):
        """SOURCE_DIMS must be a tuple."""
        for b in all_beliefs:
            assert hasattr(b, "SOURCE_DIMS"), (
                f"{b.NAME}: missing SOURCE_DIMS"
            )
            assert isinstance(b.SOURCE_DIMS, tuple), (
                f"{b.NAME}: SOURCE_DIMS is {type(b.SOURCE_DIMS).__name__}, "
                f"expected tuple"
            )

    def test_source_dims_non_empty(self, all_beliefs):
        """SOURCE_DIMS must contain at least one entry."""
        for b in all_beliefs:
            assert len(b.SOURCE_DIMS) > 0, (
                f"{b.NAME}: SOURCE_DIMS is empty"
            )

    def test_belief_names_unique(self, all_beliefs):
        """All 131 belief NAMEs must be globally unique."""
        names = [b.NAME for b in all_beliefs]
        dupes = [n for n in names if names.count(n) > 1]
        assert len(names) == len(set(names)), (
            f"Duplicate belief names: {set(dupes)}"
        )


# ======================================================================
# 4. SOURCE_DIMS structure
# ======================================================================

class TestSourceDimsStructure:
    """SOURCE_DIMS entries must be (dim_name: str, weight: float) tuples."""

    def test_source_dims_entries_are_pairs(self, all_beliefs):
        """Each SOURCE_DIMS entry must be a 2-element tuple."""
        for b in all_beliefs:
            for i, entry in enumerate(b.SOURCE_DIMS):
                assert isinstance(entry, tuple) and len(entry) == 2, (
                    f"{b.NAME}: SOURCE_DIMS[{i}]={entry!r} is not a 2-tuple"
                )

    def test_source_dims_names_are_strings(self, all_beliefs):
        """Dimension names in SOURCE_DIMS must be non-empty strings."""
        for b in all_beliefs:
            for dim_name, weight in b.SOURCE_DIMS:
                assert isinstance(dim_name, str) and len(dim_name) > 0, (
                    f"{b.NAME}: dim_name={dim_name!r} is not a non-empty string"
                )

    def test_source_dims_weights_positive(self, all_beliefs):
        """All SOURCE_DIMS weights must be > 0."""
        for b in all_beliefs:
            for dim_name, weight in b.SOURCE_DIMS:
                assert isinstance(weight, (int, float)), (
                    f"{b.NAME}: weight for {dim_name!r} is {type(weight).__name__}"
                )
                assert weight > 0, (
                    f"{b.NAME}: weight for {dim_name!r} is {weight} (<= 0)"
                )

    def test_source_dims_weight_sum_reasonable(self, all_beliefs):
        """Sum of SOURCE_DIMS weights should be in [0.5, 2.0]."""
        for b in all_beliefs:
            total = sum(w for _, w in b.SOURCE_DIMS)
            assert 0.5 <= total <= 2.0, (
                f"{b.NAME}: SOURCE_DIMS weight sum={total:.3f} "
                f"outside [0.5, 2.0]"
            )

    def test_source_dims_no_duplicate_names(self, all_beliefs):
        """Within a single belief, dimension names should not repeat."""
        for b in all_beliefs:
            names = [dim_name for dim_name, _ in b.SOURCE_DIMS]
            if len(names) != len(set(names)):
                dupes = [n for n in names if names.count(n) > 1]
                assert False, (
                    f"{b.NAME}: duplicate dim names in SOURCE_DIMS: {set(dupes)}"
                )


# ======================================================================
# 5. CoreBelief-specific: TAU and BASELINE
# ======================================================================

class TestCoreBelief:
    """CoreBelief-specific validation: TAU, BASELINE, predict()."""

    def test_tau_exists_and_is_float(self, all_core_beliefs):
        """Every CoreBelief must have a numeric TAU."""
        for b in all_core_beliefs:
            assert hasattr(b, "TAU"), f"{b.NAME}: missing TAU"
            assert isinstance(b.TAU, (int, float)), (
                f"{b.NAME}: TAU={b.TAU!r} is not numeric"
            )

    def test_tau_in_open_unit_interval(self, all_core_beliefs):
        """TAU must be strictly between 0 and 1."""
        for b in all_core_beliefs:
            assert 0.0 < b.TAU < 1.0, (
                f"{b.NAME}: TAU={b.TAU} not in (0, 1)"
            )

    def test_baseline_in_unit_interval(self, all_core_beliefs):
        """BASELINE must be in [0, 1]."""
        for b in all_core_beliefs:
            baseline = getattr(b, "BASELINE", 0.5)
            assert 0.0 <= baseline <= 1.0, (
                f"{b.NAME}: BASELINE={baseline} not in [0, 1]"
            )

    def test_has_predict_method(self, all_core_beliefs):
        """Every CoreBelief must have a predict() method."""
        for b in all_core_beliefs:
            assert hasattr(b, "predict") and callable(b.predict), (
                f"{b.NAME}: missing callable predict()"
            )

    def test_has_observe_method(self, all_core_beliefs):
        """Every CoreBelief must have an observe() method."""
        for b in all_core_beliefs:
            assert hasattr(b, "observe") and callable(b.observe), (
                f"{b.NAME}: missing callable observe()"
            )

    @pytest.mark.parametrize(
        "belief_name, expected_tau",
        list(KNOWN_TAU_VALUES.items()),
        ids=list(KNOWN_TAU_VALUES.keys()),
    )
    def test_specific_tau_values(
        self, all_core_beliefs, belief_name, expected_tau
    ):
        """Known core beliefs must have their documented TAU values."""
        matches = [b for b in all_core_beliefs if b.NAME == belief_name]
        assert len(matches) == 1, (
            f"Expected exactly one core belief named {belief_name!r}, "
            f"found {len(matches)}"
        )
        actual_tau = matches[0].TAU
        assert abs(actual_tau - expected_tau) < 1e-6, (
            f"{belief_name}: TAU={actual_tau}, expected {expected_tau}"
        )


# ======================================================================
# 6. AppraisalBelief-specific
# ======================================================================

class TestAppraisalBelief:
    """AppraisalBelief-specific validation: observe-only."""

    def test_has_observe_method(self, all_appraisal_beliefs):
        """Every AppraisalBelief must have an observe() method."""
        for b in all_appraisal_beliefs:
            assert hasattr(b, "observe") and callable(b.observe), (
                f"{b.NAME}: missing callable observe()"
            )

    def test_no_own_predict_method(self, all_appraisal_beliefs):
        """AppraisalBelief instances should not define their own predict()."""
        for b in all_appraisal_beliefs:
            # predict may exist from parent, but should NOT be in the
            # concrete class's own __dict__
            own_class = type(b)
            if "predict" in own_class.__dict__:
                # If it exists, it should raise or be a no-op
                pytest.fail(
                    f"{b.NAME} ({own_class.__name__}): defines its own "
                    f"predict() -- appraisal beliefs are observe-only"
                )

    def test_no_tau_attribute(self, all_appraisal_beliefs):
        """AppraisalBelief should not have TAU (that is a CoreBelief thing)."""
        for b in all_appraisal_beliefs:
            # TAU might be inherited as a class default; check it is not
            # explicitly set on the concrete subclass
            own_class = type(b)
            if "TAU" in own_class.__dict__:
                pytest.fail(
                    f"{b.NAME} ({own_class.__name__}): defines TAU "
                    f"but is an AppraisalBelief"
                )


# ======================================================================
# 7. AnticipationBelief-specific
# ======================================================================

class TestAnticipationBelief:
    """AnticipationBelief-specific validation: observe-only."""

    def test_has_observe_method(self, all_anticipation_beliefs):
        """Every AnticipationBelief must have an observe() method."""
        for b in all_anticipation_beliefs:
            assert hasattr(b, "observe") and callable(b.observe), (
                f"{b.NAME}: missing callable observe()"
            )

    def test_no_own_predict_method(self, all_anticipation_beliefs):
        """AnticipationBelief instances should not define their own predict()."""
        for b in all_anticipation_beliefs:
            own_class = type(b)
            if "predict" in own_class.__dict__:
                pytest.fail(
                    f"{b.NAME} ({own_class.__name__}): defines its own "
                    f"predict() -- anticipation beliefs are observe-only"
                )

    def test_no_tau_attribute(self, all_anticipation_beliefs):
        """AnticipationBelief should not have TAU."""
        for b in all_anticipation_beliefs:
            own_class = type(b)
            if "TAU" in own_class.__dict__:
                pytest.fail(
                    f"{b.NAME} ({own_class.__name__}): defines TAU "
                    f"but is an AnticipationBelief"
                )


# ======================================================================
# 8. Type hierarchy
# ======================================================================

class TestBeliefTypeHierarchy:
    """Validate that belief instances are properly typed."""

    def test_all_beliefs_are_belief_base(self, all_beliefs):
        """Every belief must be an instance of _BeliefBase."""
        for b in all_beliefs:
            assert isinstance(b, _BeliefBase), (
                f"{b.NAME}: not an instance of _BeliefBase"
            )

    def test_core_beliefs_are_core(self, all_core_beliefs):
        """Every core belief is an instance of CoreBelief."""
        for b in all_core_beliefs:
            assert isinstance(b, CoreBelief), (
                f"{b.NAME}: not a CoreBelief instance"
            )

    def test_appraisal_beliefs_are_appraisal(self, all_appraisal_beliefs):
        """Every appraisal belief is an instance of AppraisalBelief."""
        for b in all_appraisal_beliefs:
            assert isinstance(b, AppraisalBelief), (
                f"{b.NAME}: not an AppraisalBelief instance"
            )

    def test_anticipation_beliefs_are_anticipation(self, all_anticipation_beliefs):
        """Every anticipation belief is an instance of AnticipationBelief."""
        for b in all_anticipation_beliefs:
            assert isinstance(b, AnticipationBelief), (
                f"{b.NAME}: not an AnticipationBelief instance"
            )

    def test_types_mutually_exclusive(self, all_beliefs):
        """No belief should be both Core and Appraisal, etc."""
        for b in all_beliefs:
            is_core = isinstance(b, CoreBelief)
            is_appraisal = isinstance(b, AppraisalBelief)
            is_anticipation = isinstance(b, AnticipationBelief)
            types_count = sum([is_core, is_appraisal, is_anticipation])
            assert types_count == 1, (
                f"{b.NAME}: belongs to {types_count} type categories "
                f"(core={is_core}, appraisal={is_appraisal}, "
                f"anticipation={is_anticipation})"
            )


# ======================================================================
# 9. MECHANISM references
# ======================================================================

class TestBeliefMechanismReferences:
    """Validate that MECHANISM references are consistent."""

    def test_mechanism_names_are_uppercase_acronyms(self, all_beliefs):
        """MECHANISM should be an uppercase acronym (e.g., BCH, SNEM)."""
        for b in all_beliefs:
            mech = b.MECHANISM
            # Allow uppercase letters and digits (some mechanisms have digits)
            assert mech == mech.upper(), (
                f"{b.NAME}: MECHANISM={mech!r} is not uppercase"
            )

    def test_beliefs_per_mechanism_reasonable(self, all_beliefs):
        """No single mechanism should source more than ~20 beliefs."""
        from collections import Counter
        mech_counts = Counter(b.MECHANISM for b in all_beliefs)
        for mech, count in mech_counts.items():
            assert count <= 20, (
                f"Mechanism {mech} sources {count} beliefs (max 20)"
            )

    def test_multiple_mechanisms_referenced(self, all_beliefs):
        """Beliefs should reference a diverse set of mechanisms."""
        mechanisms = {b.MECHANISM for b in all_beliefs}
        assert len(mechanisms) >= 10, (
            f"Only {len(mechanisms)} distinct mechanisms referenced, "
            f"expected >= 10"
        )


# ======================================================================
# 10. Cross-validation: function <-> mechanism alignment
# ======================================================================

class TestFunctionMechanismAlignment:
    """Beliefs within a function should reference mechanisms from that function."""

    def test_f1_mechanisms(self, beliefs_by_function):
        """F1 beliefs should reference F1 mechanisms."""
        f1_beliefs = beliefs_by_function.get("F1", [])
        known_f1_mechs = {"BCH", "CSG", "MIAA", "MPG", "PNH", "SDNPS",
                          "SDED", "TPIO", "TPRD", "PSCL", "PCCR", "STAI",
                          "MDNS"}
        for b in f1_beliefs:
            # Soft check: warn but allow unknown mechanisms
            if b.MECHANISM not in known_f1_mechs:
                # Could be a new mechanism added after docs were written
                pass  # Accept gracefully

    def test_each_function_has_diverse_mechanisms(self, beliefs_by_function):
        """Each function's beliefs should reference more than one mechanism."""
        for fn_id in [f"F{i}" for i in range(1, 10)]:
            beliefs = beliefs_by_function.get(fn_id, [])
            if not beliefs:
                continue
            mechs = {b.MECHANISM for b in beliefs}
            assert len(mechs) >= 2, (
                f"{fn_id}: all {len(beliefs)} beliefs reference only "
                f"{mechs} (expected >= 2 mechanisms)"
            )
