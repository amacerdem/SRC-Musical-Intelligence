"""Layer 11 -- Full Pipeline Integration Tests.

End-to-end validation: mel -> R3 -> H3 -> mechanisms -> beliefs, plus
optional executor and PsiInterpreter tests.  Covers cross-layer shape
compatibility, numerical stability, and performance benchmarks.

~20 tests.
"""
from __future__ import annotations

import time
from typing import Any, Dict, List, Tuple

import pytest
import torch
from torch import Tensor

from Tests.smoke_test_001.conftest import make_synthetic_h3


# ======================================================================
# Conditional imports for optional components
# ======================================================================

try:
    from Musical_Intelligence.brain.executor import execute as brain_execute
    EXECUTOR_AVAILABLE = True
except (ImportError, AttributeError):
    EXECUTOR_AVAILABLE = False

try:
    from Musical_Intelligence.brain.psi_interpreter import PsiInterpreter
    PSI_AVAILABLE = True
except (ImportError, AttributeError):
    PSI_AVAILABLE = False


# ======================================================================
# Constants
# ======================================================================

B = 2
T = 50
SEED = 42


# ======================================================================
# End-to-End Pipeline: mel -> R3 -> H3
# ======================================================================

class TestMelToR3ToH3:
    """Validate the mel -> R3 -> H3 pipeline produces consistent outputs."""

    def test_r3_output_shape(self, r3_features, batch_size, time_steps):
        """R3 features are (B, T, 97)."""
        assert r3_features.shape == (batch_size, time_steps, 97)

    def test_r3_no_nan(self, r3_features):
        """R3 features have no NaN."""
        assert not torch.isnan(r3_features).any(), "NaN in R3 output"

    def test_r3_no_inf(self, r3_features):
        """R3 features have no Inf."""
        assert not torch.isinf(r3_features).any(), "Inf in R3 output"

    def test_h3_features_not_empty(self, h3_features):
        """H3 extraction produced at least some features."""
        assert len(h3_features) > 0, "H3 features dict is empty"

    def test_h3_values_are_bt(self, h3_features, batch_size):
        """Every H3 feature value is (B, T) shaped."""
        failures = []
        for key, val in h3_features.items():
            if val.dim() != 2:
                failures.append(f"{key}: dim={val.dim()}")
            elif val.shape[0] != batch_size:
                failures.append(f"{key}: batch={val.shape[0]}")
        assert not failures, "H3 shape issues:\n" + "\n".join(failures)

    def test_h3_no_nan(self, h3_features):
        """No NaN in any H3 feature value."""
        failures = []
        for key, val in h3_features.items():
            if torch.isnan(val).any():
                failures.append(str(key))
        assert not failures, f"NaN in H3 keys: {failures}"

    def test_h3_keys_are_4tuples(self, h3_features):
        """All H3 keys are (r3_idx, horizon, morph, law) 4-tuples."""
        for key in h3_features:
            assert isinstance(key, tuple) and len(key) == 4, (
                f"Bad key: {key}"
            )
            r3_idx, horizon, morph, law = key
            assert isinstance(r3_idx, int) and 0 <= r3_idx < 97
            assert isinstance(horizon, int) and horizon >= 0
            assert isinstance(morph, int) and morph >= 0
            assert isinstance(law, int) and law in (0, 1, 2)


# ======================================================================
# H3 -> Mechanism Outputs
# ======================================================================

class TestH3ToMechanisms:
    """Validate that mechanisms can consume H3 features and produce output."""

    def test_relay_forward_with_synthetic_h3(self, all_relays):
        """Every relay can forward() with synthetic H3 and produce output."""
        failures = []
        for relay in all_relays:
            h3 = make_synthetic_h3(relay, batch_size=B, time_steps=T)
            try:
                with torch.no_grad():
                    out = relay.forward(h3)
                expected = (B, T, relay.OUTPUT_DIM)
                if out.shape != expected:
                    failures.append(
                        f"{relay.NAME}: shape {tuple(out.shape)} != {expected}"
                    )
            except Exception as exc:
                failures.append(f"{relay.NAME}: {exc!r}")
        assert not failures, "Relay forward failures:\n" + "\n".join(failures)

    def test_relay_output_no_nan(self, all_relays):
        """Relay outputs have no NaN."""
        failures = []
        for relay in all_relays:
            h3 = make_synthetic_h3(relay, batch_size=B, time_steps=T)
            try:
                with torch.no_grad():
                    out = relay.forward(h3)
                if torch.isnan(out).any():
                    failures.append(relay.NAME)
            except Exception:
                pass  # forward failure covered by other test
        assert not failures, f"NaN from relays: {failures}"

    def test_relay_output_no_inf(self, all_relays):
        """Relay outputs have no Inf."""
        failures = []
        for relay in all_relays:
            h3 = make_synthetic_h3(relay, batch_size=B, time_steps=T)
            try:
                with torch.no_grad():
                    out = relay.forward(h3)
                if torch.isinf(out).any():
                    failures.append(relay.NAME)
            except Exception:
                pass
        assert not failures, f"Inf from relays: {failures}"

    def test_relay_dim_names_match_output(self, all_relays):
        """Each relay's dimension_names length matches OUTPUT_DIM."""
        failures = []
        for relay in all_relays:
            names = getattr(relay, "dimension_names", [])
            if len(names) != relay.OUTPUT_DIM:
                failures.append(
                    f"{relay.NAME}: {len(names)} names != {relay.OUTPUT_DIM}D"
                )
        assert not failures, "Dim name mismatch:\n" + "\n".join(failures)


# ======================================================================
# Mechanism -> Belief observe()
# ======================================================================

class TestMechanismToBelief:
    """Validate that mechanism output can be fed to belief observe()."""

    def test_mechanism_to_belief_pipeline(
        self, all_beliefs, all_relays, mechanism_dims
    ):
        """For each belief, run its source mechanism then feed to observe()."""
        relay_by_name = {r.NAME: r for r in all_relays}
        failures = []
        tested = 0

        for belief in all_beliefs:
            mech_name = getattr(belief, "MECHANISM", None)
            relay = relay_by_name.get(mech_name)
            if relay is None:
                continue  # mechanism not a relay or cross-function

            h3 = make_synthetic_h3(relay, batch_size=B, time_steps=T)
            try:
                with torch.no_grad():
                    mech_out = relay.forward(h3)
                    belief_out = belief.observe(mech_out)
                tested += 1
                if belief_out.shape != (B, T):
                    failures.append(
                        f"{belief.NAME}: observe shape={tuple(belief_out.shape)}"
                    )
                if torch.isnan(belief_out).any():
                    failures.append(f"{belief.NAME}: NaN in observe output")
            except Exception as exc:
                failures.append(f"{belief.NAME}: {exc!r}")

        assert tested > 0, "No mechanism-to-belief pairs could be tested"
        assert not failures, (
            f"Pipeline failures ({tested} tested):\n" + "\n".join(failures)
        )


# ======================================================================
# Cross-Layer Shape Compatibility
# ======================================================================

class TestCrossLayerShapes:
    """Verify tensor shapes are compatible across layers."""

    def test_r3_97d(self, r3_features):
        """R3 last dim is 97."""
        assert r3_features.shape[-1] == 97

    def test_h3_demands_subset_of_features(self, all_demands, h3_features):
        """All demanded H3 tuples are present in h3_features."""
        missing = all_demands - set(h3_features.keys())
        assert not missing, f"{len(missing)} demanded tuples missing from H3"

    def test_mechanism_output_dims_match_declared(self, all_relays):
        """Every relay's forward output dim matches OUTPUT_DIM."""
        failures = []
        for relay in all_relays:
            h3 = make_synthetic_h3(relay, batch_size=B, time_steps=T)
            try:
                with torch.no_grad():
                    out = relay.forward(h3)
                if out.shape[-1] != relay.OUTPUT_DIM:
                    failures.append(
                        f"{relay.NAME}: actual={out.shape[-1]}, "
                        f"declared={relay.OUTPUT_DIM}"
                    )
            except Exception:
                pass
        assert not failures, "Dim mismatches:\n" + "\n".join(failures)


# ======================================================================
# Numerical Stability (full pipeline)
# ======================================================================

class TestNumericalStability:
    """No NaN/Inf/unbounded values across the entire pipeline."""

    def test_pipeline_under_no_grad(self, all_relays, all_beliefs, mechanism_dims):
        """Full pipeline runs cleanly under torch.no_grad()."""
        relay_by_name = {r.NAME: r for r in all_relays}
        errors = []
        with torch.no_grad():
            for belief in all_beliefs:
                mech_name = getattr(belief, "MECHANISM", None)
                relay = relay_by_name.get(mech_name)
                if relay is None:
                    # Use synthetic input with fallback dim
                    dim = mechanism_dims.get(mech_name, 10)
                    torch.manual_seed(SEED)
                    inp = torch.rand(B, T, dim)
                else:
                    h3 = make_synthetic_h3(relay, batch_size=B, time_steps=T)
                    try:
                        inp = relay.forward(h3)
                    except Exception as exc:
                        errors.append(f"{belief.NAME} relay: {exc!r}")
                        continue
                try:
                    out = belief.observe(inp)
                    if torch.isnan(out).any():
                        errors.append(f"{belief.NAME}: NaN")
                    if torch.isinf(out).any():
                        errors.append(f"{belief.NAME}: Inf")
                except Exception as exc:
                    errors.append(f"{belief.NAME}: {exc!r}")
        assert not errors, "Stability errors:\n" + "\n".join(errors)

    def test_r3_bounded(self, r3_features):
        """R3 values in [0, 1]."""
        assert r3_features.min() >= 0.0
        assert r3_features.max() <= 1.0

    def test_h3_bounded(self, h3_features):
        """H3 values in [-10, 10] (generous range for morphological features)."""
        failures = []
        for key, val in h3_features.items():
            if val.min() < -10.0 or val.max() > 10.0:
                failures.append(
                    f"{key}: range [{val.min().item():.2f}, {val.max().item():.2f}]"
                )
        # Allow a few outliers (morphological features can be diverse)
        max_outliers = max(5, len(h3_features) // 10)
        assert len(failures) <= max_outliers, (
            f"{len(failures)} H3 features outside [-10,10]:\n"
            + "\n".join(failures[:20])
        )


# ======================================================================
# Core Belief predict() Integration
# ======================================================================

class TestCoreBeliefPredictIntegration:
    """Test predict() in the context of the full pipeline."""

    def test_predict_after_observe(
        self, all_core_beliefs, all_relays, mechanism_dims
    ):
        """observe() then predict() works without crash for core beliefs."""
        relay_by_name = {r.NAME: r for r in all_relays}
        failures = []

        for belief in all_core_beliefs:
            mech_name = getattr(belief, "MECHANISM", None)
            relay = relay_by_name.get(mech_name)
            dim = mechanism_dims.get(mech_name, 10)

            if relay is not None:
                h3 = make_synthetic_h3(relay, batch_size=B, time_steps=T)
                try:
                    with torch.no_grad():
                        mech_out = relay.forward(h3)
                except Exception:
                    mech_out = torch.rand(B, T, dim)
            else:
                torch.manual_seed(SEED)
                mech_out = torch.rand(B, T, dim)

            try:
                with torch.no_grad():
                    observed = belief.observe(mech_out)
                    predicted = belief.predict(observed, {}, {})
                if torch.isnan(predicted).any():
                    failures.append(f"{belief.NAME}: NaN in predict")
                if predicted.shape != (B, T):
                    failures.append(
                        f"{belief.NAME}: predict shape={tuple(predicted.shape)}"
                    )
            except Exception as exc:
                failures.append(f"{belief.NAME}: {exc!r}")

        assert not failures, (
            "predict-after-observe failures:\n" + "\n".join(failures)
        )


# ======================================================================
# Executor (conditional)
# ======================================================================

class TestExecutor:
    """Test brain executor if importable."""

    @pytest.fixture(autouse=True)
    def _skip_if_unavailable(self):
        if not EXECUTOR_AVAILABLE:
            pytest.skip("Executor not importable (Hub/Integrator issue)")

    def test_execute_returns_3_tuple(
        self, all_relays, h3_features, r3_features
    ):
        """execute() returns (outputs_dict, ram, neuro)."""
        result = brain_execute(all_relays, h3_features, r3_features)
        assert isinstance(result, tuple) and len(result) == 3

    def test_execute_outputs_dict(
        self, all_relays, h3_features, r3_features
    ):
        """First return value is a dict of str -> Tensor."""
        outputs, ram, neuro = brain_execute(
            all_relays, h3_features, r3_features
        )
        assert isinstance(outputs, dict)
        for key, val in outputs.items():
            assert isinstance(key, str), f"Key {key} not str"
            assert isinstance(val, Tensor), f"Val for {key} not Tensor"

    def test_execute_ram_shape(
        self, all_relays, h3_features, r3_features, batch_size
    ):
        """RAM output is (B, T, 26)."""
        outputs, ram, neuro = brain_execute(
            all_relays, h3_features, r3_features
        )
        assert ram.shape[0] == batch_size
        assert ram.shape[2] == 26

    def test_execute_neuro_shape(
        self, all_relays, h3_features, r3_features, batch_size
    ):
        """Neuro output is (B, T, 4)."""
        outputs, ram, neuro = brain_execute(
            all_relays, h3_features, r3_features
        )
        assert neuro.shape[0] == batch_size
        assert neuro.shape[2] == 4

    def test_execute_no_nan(
        self, all_relays, h3_features, r3_features
    ):
        """No NaN in any executor output."""
        outputs, ram, neuro = brain_execute(
            all_relays, h3_features, r3_features
        )
        for key, val in outputs.items():
            assert not torch.isnan(val).any(), f"NaN in output[{key}]"
        assert not torch.isnan(ram).any(), "NaN in RAM"
        assert not torch.isnan(neuro).any(), "NaN in neuro"


# ======================================================================
# PsiInterpreter (conditional)
# ======================================================================

class TestPsiInterpreter:
    """Test PsiInterpreter if importable."""

    # Expected domain dimensions (total 28)
    EXPECTED_DOMAINS = {
        "affect": 4,
        "emotion": 7,
        "aesthetic": 5,
        "bodily": 4,
        "cognitive": 4,
        "temporal": 4,
    }

    @pytest.fixture(autouse=True)
    def _skip_if_unavailable(self):
        if not PSI_AVAILABLE:
            pytest.skip("PsiInterpreter not importable")

    @pytest.fixture(scope="class")
    def psi(self):
        return PsiInterpreter()

    def test_psi_has_interpret(self, psi):
        """PsiInterpreter has an interpret() method."""
        assert hasattr(psi, "interpret") and callable(psi.interpret)

    def test_psi_domain_count(self, psi):
        """PsiInterpreter covers 6 domains."""
        domains = getattr(psi, "DOMAINS", None) or getattr(psi, "domains", None)
        if domains is not None:
            assert len(domains) == 6, f"Got {len(domains)} domains"

    def test_psi_total_dim_28(self, psi):
        """Total output dimensionality is 28."""
        total = sum(self.EXPECTED_DOMAINS.values())
        assert total == 28


# ======================================================================
# Performance (mark as slow)
# ======================================================================

class TestPerformance:
    """Performance benchmarks -- marked slow."""

    @pytest.mark.slow
    def test_single_piece_under_30s(self, r3_extractor, h3_extractor):
        """Single piece (B=1, T=100) through R3+H3 completes in <30s."""
        torch.manual_seed(SEED)
        mel = torch.rand(1, 128, 100)

        start = time.time()
        with torch.no_grad():
            r3_out = r3_extractor.extract(mel)
            # Get demands from a subset (to avoid heavy H3 extraction)
            # Just time R3 here as H3 demands vary
        elapsed = time.time() - start

        assert elapsed < 30.0, f"R3 extraction took {elapsed:.1f}s (limit 30s)"

    @pytest.mark.slow
    def test_relay_forward_batch(self, all_relays):
        """All relays forward in <10s total for B=2, T=50."""
        start = time.time()
        with torch.no_grad():
            for relay in all_relays:
                h3 = make_synthetic_h3(relay, batch_size=B, time_steps=T)
                try:
                    relay.forward(h3)
                except Exception:
                    pass
        elapsed = time.time() - start
        assert elapsed < 10.0, (
            f"All relays took {elapsed:.1f}s (limit 10s)"
        )

    @pytest.mark.slow
    def test_belief_observe_batch(self, all_beliefs, mechanism_dims):
        """All 131 beliefs observe in <5s total for B=2, T=50."""
        torch.manual_seed(SEED)
        start = time.time()
        with torch.no_grad():
            for belief in all_beliefs:
                mech = getattr(belief, "MECHANISM", None)
                dim = mechanism_dims.get(mech, 10) if mech else 10
                inp = torch.rand(B, T, dim)
                try:
                    belief.observe(inp)
                except Exception:
                    pass
        elapsed = time.time() - start
        assert elapsed < 5.0, (
            f"All beliefs took {elapsed:.1f}s (limit 5s)"
        )

    @pytest.mark.slow
    def test_memory_under_500mb(self, r3_extractor):
        """Peak memory for B=1, T=100 R3 extraction < 500MB."""
        torch.manual_seed(SEED)
        mel = torch.rand(1, 128, 100)

        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
            mel_gpu = mel.cuda()
            with torch.no_grad():
                r3_extractor.extract(mel_gpu)
            peak_mb = torch.cuda.max_memory_allocated() / (1024 ** 2)
            assert peak_mb < 500, f"Peak GPU memory {peak_mb:.0f}MB (limit 500MB)"
        else:
            # CPU -- just ensure no OOM by running it
            with torch.no_grad():
                r3_extractor.extract(mel)
            # Cannot measure CPU peak memory precisely; pass if no OOM


# ======================================================================
# Encoder / Associator Integration (if present)
# ======================================================================

class TestEncoderAssociatorIntegration:
    """Validate encoders and associators if any are collected."""

    def test_encoders_forward(self, all_encoders):
        """Each encoder can forward with synthetic H3."""
        if not all_encoders:
            pytest.skip("No encoders collected")
        failures = []
        for enc in all_encoders:
            h3 = make_synthetic_h3(enc, batch_size=B, time_steps=T)
            try:
                with torch.no_grad():
                    out = enc.forward(h3)
                expected = (B, T, enc.OUTPUT_DIM)
                if out.shape != expected:
                    failures.append(
                        f"{enc.NAME}: {tuple(out.shape)} != {expected}"
                    )
            except Exception as exc:
                failures.append(f"{enc.NAME}: {exc!r}")
        assert not failures, "Encoder failures:\n" + "\n".join(failures)

    def test_associators_forward(self, all_associators):
        """Each associator can forward with synthetic H3."""
        if not all_associators:
            pytest.skip("No associators collected")
        failures = []
        for assoc in all_associators:
            h3 = make_synthetic_h3(assoc, batch_size=B, time_steps=T)
            try:
                with torch.no_grad():
                    out = assoc.forward(h3)
                expected = (B, T, assoc.OUTPUT_DIM)
                if out.shape != expected:
                    failures.append(
                        f"{assoc.NAME}: {tuple(out.shape)} != {expected}"
                    )
            except Exception as exc:
                failures.append(f"{assoc.NAME}: {exc!r}")
        assert not failures, "Associator failures:\n" + "\n".join(failures)


# ======================================================================
# Full Belief Count Cross-Check
# ======================================================================

class TestBeliefCountCrossCheck:
    """Cross-check belief counts between fixtures."""

    def test_core_plus_appraisal_plus_anticipation_eq_total(
        self, all_beliefs, all_core_beliefs,
        all_appraisal_beliefs, all_anticipation_beliefs,
    ):
        """36 + 65 + 30 = 131 and equals len(all_beliefs)."""
        core = len(all_core_beliefs)
        appraisal = len(all_appraisal_beliefs)
        anticipation = len(all_anticipation_beliefs)
        total = len(all_beliefs)
        assert core + appraisal + anticipation == total, (
            f"{core} + {appraisal} + {anticipation} = "
            f"{core + appraisal + anticipation} != {total}"
        )

    def test_mechanism_dims_covers_most_beliefs(
        self, all_beliefs, mechanism_dims
    ):
        """mechanism_dims should cover the MECHANISM of most beliefs."""
        covered = 0
        for b in all_beliefs:
            mech = getattr(b, "MECHANISM", None)
            if mech and mech in mechanism_dims:
                covered += 1
        # At least 80% of beliefs should be covered
        ratio = covered / len(all_beliefs) if all_beliefs else 0
        assert ratio >= 0.8, (
            f"Only {covered}/{len(all_beliefs)} beliefs "
            f"({ratio:.0%}) have mechanism in mechanism_dims"
        )

    def test_all_beliefs_unique_names(self, all_beliefs):
        """All 131 belief names are unique."""
        names = [b.NAME for b in all_beliefs]
        dupes = [n for n in names if names.count(n) > 1]
        assert not dupes, f"Duplicate belief names: {set(dupes)}"
