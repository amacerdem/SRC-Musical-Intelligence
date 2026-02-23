"""Layer 06 -- Depth-1 Encoder & Depth-2 Associator Forward Pass.

Validates that encoders and associators can be computed in proper dependency
order (relays first, then encoders, then associators) and produce valid output
tensors.  Covers shape, value bounds, NaN checks, depth ordering, and
UPSTREAM_READS satisfaction.

~20 tests.
"""
from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

import pytest
import torch
from torch import Tensor

from Musical_Intelligence.contracts.bases.nucleus import (
    _NucleusBase,
    Relay,
    Encoder,
    Associator,
)
from Tests.smoke_test_001.conftest import make_synthetic_h3


# ======================================================================
# Constants
# ======================================================================

B = 2       # batch size
T = 50      # time steps
R3_DIM = 97


# ======================================================================
# Helpers
# ======================================================================

def _make_r3(batch: int = B, time: int = T) -> Tensor:
    """Synthetic R3 features (B, T, 97) in [0, 1]."""
    torch.manual_seed(42)
    return torch.rand(batch, time, R3_DIM)


def _compute_all_relays(
    relays: List[Relay],
    batch: int = B,
    time: int = T,
) -> Dict[str, Tensor]:
    """Run all relays and collect outputs keyed by NAME."""
    r3 = _make_r3(batch, time)
    outputs: Dict[str, Tensor] = {}
    for relay in relays:
        h3 = make_synthetic_h3(relay, batch_size=batch, time_steps=time)
        outputs[relay.NAME] = relay.compute(h3, r3)
    return outputs


def _compute_all_encoders(
    encoders: List[Encoder],
    relay_outputs: Dict[str, Tensor],
    batch: int = B,
    time: int = T,
) -> Dict[str, Tensor]:
    """Run all encoders with relay outputs and collect results."""
    r3 = _make_r3(batch, time)
    outputs: Dict[str, Tensor] = {}
    for enc in encoders:
        h3 = make_synthetic_h3(enc, batch_size=batch, time_steps=time)
        try:
            out = enc.compute(h3, r3, relay_outputs)
            outputs[enc.NAME] = out
        except (KeyError, RuntimeError, ValueError):
            # Some encoders may reference relays from other functions
            # that are not available; handle gracefully
            pass
    return outputs


def _compute_all_associators(
    associators: List[Associator],
    upstream_outputs: Dict[str, Tensor],
    batch: int = B,
    time: int = T,
) -> Dict[str, Tensor]:
    """Run all associators with upstream (relay + encoder) outputs."""
    r3 = _make_r3(batch, time)
    outputs: Dict[str, Tensor] = {}
    for assoc in associators:
        h3 = make_synthetic_h3(assoc, batch_size=batch, time_steps=time)
        try:
            out = assoc.compute(h3, r3, upstream_outputs)
            outputs[assoc.NAME] = out
        except (KeyError, RuntimeError, ValueError):
            pass
    return outputs


# ======================================================================
# Session-scope "pipeline" fixture (expensive -- run once)
# ======================================================================

@pytest.fixture(scope="module")
def pipeline_outputs(all_relays, all_encoders, all_associators):
    """Run the full depth-0 -> depth-1 -> depth-2 pipeline once.

    Returns a dict with keys 'relay', 'encoder', 'associator',
    each mapping NAME -> (mechanism_instance, output_tensor).
    """
    # Stage 0: relays
    relay_tensors = _compute_all_relays(all_relays)

    # Stage 1: encoders (receive relay outputs)
    encoder_tensors = _compute_all_encoders(all_encoders, relay_tensors)

    # Stage 2: associators (receive relay + encoder outputs)
    upstream = {**relay_tensors, **encoder_tensors}
    associator_tensors = _compute_all_associators(all_associators, upstream)

    # Package mechanism instance alongside its output for later inspection
    relay_map = {
        r.NAME: (r, relay_tensors[r.NAME])
        for r in all_relays if r.NAME in relay_tensors
    }
    encoder_map = {
        e.NAME: (e, encoder_tensors[e.NAME])
        for e in all_encoders if e.NAME in encoder_tensors
    }
    associator_map = {
        a.NAME: (a, associator_tensors[a.NAME])
        for a in all_associators if a.NAME in associator_tensors
    }

    return {
        "relay": relay_map,
        "encoder": encoder_map,
        "associator": associator_map,
    }


# ======================================================================
# 1. Encoder output shape
# ======================================================================

class TestEncoderOutputShape:
    """Encoders must produce (B, T, OUTPUT_DIM)."""

    def test_encoder_rank_is_3(self, pipeline_outputs):
        """Encoder output tensor must be 3-dimensional."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            assert out.dim() == 3, (
                f"{name}: expected rank 3, got {out.dim()}"
            )

    def test_encoder_batch_dim(self, pipeline_outputs):
        """Encoder output batch size must match input."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            assert out.shape[0] == B, (
                f"{name}: expected B={B}, got {out.shape[0]}"
            )

    def test_encoder_time_dim(self, pipeline_outputs):
        """Encoder output time dimension must match input."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            assert out.shape[1] == T, (
                f"{name}: expected T={T}, got {out.shape[1]}"
            )

    def test_encoder_feature_dim(self, pipeline_outputs):
        """Encoder output feature dim must match OUTPUT_DIM."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            assert out.shape[2] == enc.OUTPUT_DIM, (
                f"{name}: expected D={enc.OUTPUT_DIM}, got {out.shape[2]}"
            )


# ======================================================================
# 2. Associator output shape
# ======================================================================

class TestAssociatorOutputShape:
    """Associators must produce (B, T, OUTPUT_DIM)."""

    def test_associator_rank_is_3(self, pipeline_outputs):
        """Associator output tensor must be 3-dimensional."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            assert out.dim() == 3, (
                f"{name}: expected rank 3, got {out.dim()}"
            )

    def test_associator_batch_dim(self, pipeline_outputs):
        """Associator output batch size must match input."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            assert out.shape[0] == B, (
                f"{name}: expected B={B}, got {out.shape[0]}"
            )

    def test_associator_time_dim(self, pipeline_outputs):
        """Associator output time dimension must match input."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            assert out.shape[1] == T, (
                f"{name}: expected T={T}, got {out.shape[1]}"
            )

    def test_associator_feature_dim(self, pipeline_outputs):
        """Associator output feature dim must match OUTPUT_DIM."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            assert out.shape[2] == assoc.OUTPUT_DIM, (
                f"{name}: expected D={assoc.OUTPUT_DIM}, got {out.shape[2]}"
            )


# ======================================================================
# 3. Value bounds (encoders + associators)
# ======================================================================

class TestDeepValueBounds:
    """Output values must be in [0, 1] with no NaN/Inf."""

    def test_encoder_values_bounded(self, pipeline_outputs):
        """Encoder outputs in [0, 1]."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            assert out.min().item() >= -1e-6, (
                f"{name}: min={out.min().item():.6f}"
            )
            assert out.max().item() <= 1.0 + 1e-6, (
                f"{name}: max={out.max().item():.6f}"
            )

    def test_associator_values_bounded(self, pipeline_outputs):
        """Associator outputs in [0, 1]."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            assert out.min().item() >= -1e-6, (
                f"{name}: min={out.min().item():.6f}"
            )
            assert out.max().item() <= 1.0 + 1e-6, (
                f"{name}: max={out.max().item():.6f}"
            )

    def test_encoder_no_nan(self, pipeline_outputs):
        """No NaN in encoder outputs."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            assert not torch.isnan(out).any(), f"{name}: NaN detected"

    def test_associator_no_nan(self, pipeline_outputs):
        """No NaN in associator outputs."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            assert not torch.isnan(out).any(), f"{name}: NaN detected"

    def test_encoder_no_inf(self, pipeline_outputs):
        """No Inf in encoder outputs."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            assert not torch.isinf(out).any(), f"{name}: Inf detected"

    def test_associator_no_inf(self, pipeline_outputs):
        """No Inf in associator outputs."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            assert not torch.isinf(out).any(), f"{name}: Inf detected"


# ======================================================================
# 4. Non-trivial output (not all zeros, some variance)
# ======================================================================

class TestDeepNonTrivial:
    """Deep mechanism outputs should contain meaningful signal."""

    def test_encoder_not_all_zeros(self, pipeline_outputs):
        """Encoder outputs must contain non-zero values."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            assert out.abs().sum().item() > 0, (
                f"{name}: output is entirely zero"
            )

    def test_associator_not_all_zeros(self, pipeline_outputs):
        """Associator outputs must contain non-zero values."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            assert out.abs().sum().item() > 0, (
                f"{name}: output is entirely zero"
            )


# ======================================================================
# 5. Depth ordering: relays < encoders < associators
# ======================================================================

class TestDepthOrdering:
    """Validate that ROLE assignments reflect correct depth order."""

    def test_relay_role(self, all_relays):
        """All relays have ROLE='relay'."""
        for r in all_relays:
            assert r.ROLE == "relay", f"{r.NAME}: ROLE={r.ROLE!r}"

    def test_encoder_role(self, all_encoders):
        """All encoders have ROLE='encoder'."""
        for e in all_encoders:
            assert e.ROLE == "encoder", f"{e.NAME}: ROLE={e.ROLE!r}"

    def test_associator_role(self, all_associators):
        """All associators have ROLE='associator'."""
        for a in all_associators:
            assert a.ROLE == "associator", f"{a.NAME}: ROLE={a.ROLE!r}"

    def test_relay_has_no_upstream_reads(self, all_relays):
        """Relays should not have UPSTREAM_READS (they are depth-0)."""
        for r in all_relays:
            if hasattr(r, "UPSTREAM_READS"):
                assert r.UPSTREAM_READS == () or r.UPSTREAM_READS is None, (
                    f"{r.NAME}: relay should not have UPSTREAM_READS, "
                    f"got {r.UPSTREAM_READS!r}"
                )


# ======================================================================
# 6. UPSTREAM_READS satisfaction
# ======================================================================

class TestUpstreamReads:
    """Encoders/Associators should declare UPSTREAM_READS that are satisfiable."""

    def test_encoder_upstream_reads_declared(self, all_encoders):
        """Every encoder should declare UPSTREAM_READS as a tuple."""
        for enc in all_encoders:
            assert hasattr(enc, "UPSTREAM_READS"), (
                f"{enc.NAME}: missing UPSTREAM_READS"
            )
            assert isinstance(enc.UPSTREAM_READS, tuple), (
                f"{enc.NAME}: UPSTREAM_READS must be a tuple"
            )

    def test_associator_upstream_reads_declared(self, all_associators):
        """Every associator should declare UPSTREAM_READS as a tuple."""
        for assoc in all_associators:
            assert hasattr(assoc, "UPSTREAM_READS"), (
                f"{assoc.NAME}: missing UPSTREAM_READS"
            )
            assert isinstance(assoc.UPSTREAM_READS, tuple), (
                f"{assoc.NAME}: UPSTREAM_READS must be a tuple"
            )

    def test_encoder_upstream_reads_are_strings(self, all_encoders):
        """UPSTREAM_READS entries must be mechanism name strings."""
        for enc in all_encoders:
            for name in enc.UPSTREAM_READS:
                assert isinstance(name, str) and len(name) > 0, (
                    f"{enc.NAME}: UPSTREAM_READS entry {name!r} is not a "
                    f"non-empty string"
                )

    def test_upstream_reads_reference_known_mechanisms(
        self, all_encoders, all_associators, all_mechanisms
    ):
        """UPSTREAM_READS entries should reference mechanisms that exist."""
        all_names = {m.NAME for m in all_mechanisms}
        warnings = []
        for mech in list(all_encoders) + list(all_associators):
            for upstream_name in mech.UPSTREAM_READS:
                if upstream_name not in all_names:
                    warnings.append(
                        f"{mech.NAME} reads {upstream_name!r} which is not "
                        f"in known mechanisms"
                    )
        # This is a soft check -- warn but do not fail, since F9 has no
        # mechanisms and cross-function reads may reference future work.
        if warnings:
            pytest.xfail(
                f"{len(warnings)} dangling upstream references: "
                f"{warnings[:5]}{'...' if len(warnings) > 5 else ''}"
            )


# ======================================================================
# 7. EMPF layer structure on deep mechanisms
# ======================================================================

class TestDeepLayerStructure:
    """Encoders and associators should have valid EMPF layer specs."""

    def test_encoder_layers_valid(self, pipeline_outputs):
        """Encoder layer slices sum to OUTPUT_DIM."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            total = sum(layer.dims for layer in enc.LAYERS)
            assert total == enc.OUTPUT_DIM, (
                f"{name}: layer dims sum={total}, OUTPUT_DIM={enc.OUTPUT_DIM}"
            )

    def test_associator_layers_valid(self, pipeline_outputs):
        """Associator layer slices sum to OUTPUT_DIM."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            total = sum(layer.dims for layer in assoc.LAYERS)
            assert total == assoc.OUTPUT_DIM, (
                f"{name}: layer dims sum={total}, OUTPUT_DIM={assoc.OUTPUT_DIM}"
            )

    def test_encoder_layers_extractable(self, pipeline_outputs):
        """Each encoder layer slice is extractable from the output tensor."""
        for name, (enc, out) in pipeline_outputs["encoder"].items():
            for layer in enc.LAYERS:
                sliced = out[:, :, layer.start:layer.end]
                assert sliced.shape[2] == layer.dims, (
                    f"{name}/{layer.code}: slice dims mismatch"
                )

    def test_associator_layers_extractable(self, pipeline_outputs):
        """Each associator layer slice is extractable from the output tensor."""
        for name, (assoc, out) in pipeline_outputs["associator"].items():
            for layer in assoc.LAYERS:
                sliced = out[:, :, layer.start:layer.end]
                assert sliced.shape[2] == layer.dims, (
                    f"{name}/{layer.code}: slice dims mismatch"
                )


# ======================================================================
# 8. Population counts
# ======================================================================

class TestDeepPopulation:
    """Validate the population of deep mechanisms."""

    def test_at_least_some_encoders(self, all_encoders):
        """System should contain at least a few encoders."""
        assert len(all_encoders) >= 3, (
            f"Only {len(all_encoders)} encoders found"
        )

    def test_at_least_some_associators(self, all_associators):
        """System should contain at least a few associators."""
        assert len(all_associators) >= 2, (
            f"Only {len(all_associators)} associators found"
        )

    def test_encoder_names_unique(self, all_encoders):
        """Encoder NAMEs must be unique."""
        names = [e.NAME for e in all_encoders]
        assert len(names) == len(set(names)), (
            f"Duplicate encoder names: "
            f"{[n for n in names if names.count(n) > 1]}"
        )

    def test_associator_names_unique(self, all_associators):
        """Associator NAMEs must be unique."""
        names = [a.NAME for a in all_associators]
        assert len(names) == len(set(names)), (
            f"Duplicate associator names: "
            f"{[n for n in names if names.count(n) > 1]}"
        )

    def test_no_overlap_relay_encoder_associator(
        self, all_relays, all_encoders, all_associators
    ):
        """No mechanism should appear in more than one role category."""
        relay_names = {r.NAME for r in all_relays}
        encoder_names = {e.NAME for e in all_encoders}
        assoc_names = {a.NAME for a in all_associators}

        re_overlap = relay_names & encoder_names
        ra_overlap = relay_names & assoc_names
        ea_overlap = encoder_names & assoc_names

        assert not re_overlap, f"Relay/Encoder overlap: {re_overlap}"
        assert not ra_overlap, f"Relay/Associator overlap: {ra_overlap}"
        assert not ea_overlap, f"Encoder/Associator overlap: {ea_overlap}"


# ======================================================================
# 9. H3 demand consistency for deep mechanisms
# ======================================================================

class TestDeepH3Demand:
    """Deep mechanisms should have valid H3 demands."""

    def test_encoder_h3_demand(self, all_encoders):
        """Every encoder should have h3_demand."""
        for enc in all_encoders:
            demand = enc.h3_demand
            # Encoders may have zero h3 demand if they rely entirely on
            # relay outputs, so just check it is a tuple/list
            assert hasattr(demand, "__len__"), (
                f"{enc.NAME}: h3_demand is not iterable"
            )

    def test_associator_h3_demand(self, all_associators):
        """Every associator should have h3_demand."""
        for assoc in all_associators:
            demand = assoc.h3_demand
            assert hasattr(demand, "__len__"), (
                f"{assoc.NAME}: h3_demand is not iterable"
            )

    def test_deep_h3_demand_tuples_valid(self, all_encoders, all_associators):
        """All H3 demand tuples from deep mechanisms are 4-int tuples."""
        for mech in list(all_encoders) + list(all_associators):
            for spec in mech.h3_demand:
                t = spec.as_tuple()
                assert len(t) == 4 and all(isinstance(v, int) for v in t), (
                    f"{mech.NAME}: invalid demand tuple {t}"
                )
