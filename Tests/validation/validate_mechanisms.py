#!/usr/bin/env python3
"""C3 Mechanism Validation Report.

Validates all 10 brain mechanisms:
- Output shape (B, T, 30) for each mechanism
- _aggregate_to_10d behavior for K<10, K==10, K>10
- h3_demand per mechanism
- MechanismRunner compute-all and cache correctness
- Dimension transposition checks

Usage:
    python Tests/validation/validate_mechanisms.py
"""
from __future__ import annotations

import os
import sys
import time
from typing import Dict, Set, Tuple

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

import torch
from torch import Tensor

from Musical_Intelligence.brain.mechanisms import (
    PPC, TPC, BEP, ASA, TMH, MEM, SYN, AED, CPD, C0P,
    MechanismRunner,
)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
MECHANISM_NAMES = ("PPC", "TPC", "BEP", "ASA", "TMH", "MEM", "SYN", "AED", "CPD", "C0P")
MECHANISM_CLASSES = {
    "PPC": PPC, "TPC": TPC, "BEP": BEP, "ASA": ASA, "TMH": TMH,
    "MEM": MEM, "SYN": SYN, "AED": AED, "CPD": CPD, "C0P": C0P,
}
EXPECTED_OUTPUT_DIM = 30
B, T, R3_DIM = 1, 100, 128


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _section(title: str) -> str:
    return f"\n{'=' * 72}\n  {title}\n{'=' * 72}"


def _make_dummy_inputs(
    demand: Set[Tuple[int, int, int, int]],
) -> Tuple[Dict[Tuple[int, int, int, int], Tensor], Tensor]:
    """Create dummy H3 and R3 inputs for mechanism testing."""
    r3 = torch.rand(B, T, R3_DIM)
    h3: Dict[Tuple[int, int, int, int], Tensor] = {}
    for key in demand:
        h3[key] = torch.rand(B, T)
    return h3, r3


# ---------------------------------------------------------------------------
# Validation: individual mechanism output shapes
# ---------------------------------------------------------------------------
def validate_mechanism_outputs() -> list:
    """Test all 10 mechanisms produce (B, T, 30) output."""
    results = []

    for name in MECHANISM_NAMES:
        mech = MECHANISM_CLASSES[name]()
        t0 = time.perf_counter()

        try:
            # Collect demand and create inputs
            demand = mech.h3_demand
            h3, r3 = _make_dummy_inputs(demand)

            # Run compute
            output = mech.compute(h3, r3)
            compute_time = time.perf_counter() - t0

            # Validate shape
            expected_shape = (B, T, mech.OUTPUT_DIM)
            shape_ok = tuple(output.shape) == expected_shape

            # Validate no NaN/Inf
            no_nan = not torch.isnan(output).any().item()
            no_inf = not torch.isinf(output).any().item()

            # Validate range [0, 1]
            in_range = output.min().item() >= 0.0 and output.max().item() <= 1.0

            # Validate no dimension transposition
            # Output should be (B, T, D), not (B, D, T) or (D, B, T)
            dim_order_ok = (
                output.shape[0] == B
                and output.shape[1] == T
                and output.shape[2] == mech.OUTPUT_DIM
            )

            passed = shape_ok and no_nan and no_inf and in_range and dim_order_ok

            results.append({
                "name": name,
                "full_name": mech.FULL_NAME,
                "passed": passed,
                "shape": tuple(output.shape),
                "expected_shape": expected_shape,
                "shape_ok": shape_ok,
                "no_nan": no_nan,
                "no_inf": no_inf,
                "in_range": in_range,
                "dim_order_ok": dim_order_ok,
                "min_val": output.min().item(),
                "max_val": output.max().item(),
                "mean_val": output.mean().item(),
                "demand_count": len(demand),
                "horizons": sorted(mech.horizons_used) if demand else [],
                "compute_time": compute_time,
                "error": None,
            })

        except Exception as e:
            results.append({
                "name": name,
                "full_name": mech.FULL_NAME,
                "passed": False,
                "error": str(e),
                "compute_time": time.perf_counter() - t0,
                "demand_count": 0,
                "horizons": [],
            })

    return results


# ---------------------------------------------------------------------------
# Validation: _aggregate_to_10d
# ---------------------------------------------------------------------------
def validate_aggregate_to_10d() -> list:
    """Test _aggregate_to_10d for K<10, K==10, K>10."""
    results = []

    # Use BEP as the reference mechanism (has _aggregate_to_10d as static method)
    aggregate_fn = BEP._aggregate_to_10d
    device = torch.device("cpu")

    # Test K < 10 (zero padding)
    for K in [0, 1, 5, 9]:
        feats = [torch.rand(B, T) for _ in range(K)]
        output = aggregate_fn(feats, B, T, device)
        expected = (B, T, 10)
        shape_ok = tuple(output.shape) == expected

        # Check zero padding
        if K > 0 and K < 10:
            pad_zeros = output[:, :, K:].abs().sum().item() == 0.0
        else:
            pad_zeros = True

        results.append({
            "case": f"K={K} (< 10)",
            "passed": shape_ok and pad_zeros,
            "shape": tuple(output.shape),
            "expected": expected,
            "shape_ok": shape_ok,
            "pad_zeros": pad_zeros,
        })

    # Test K == 10 (direct pass-through)
    feats = [torch.rand(B, T) for _ in range(10)]
    output = aggregate_fn(feats, B, T, device)
    expected = (B, T, 10)
    shape_ok = tuple(output.shape) == expected
    results.append({
        "case": "K=10 (exact)",
        "passed": shape_ok,
        "shape": tuple(output.shape),
        "expected": expected,
        "shape_ok": shape_ok,
        "pad_zeros": True,
    })

    # Test K > 10 (adaptive avg pooling)
    for K in [11, 20, 50]:
        feats = [torch.rand(B, T) for _ in range(K)]
        output = aggregate_fn(feats, B, T, device)
        expected = (B, T, 10)
        shape_ok = tuple(output.shape) == expected
        results.append({
            "case": f"K={K} (> 10)",
            "passed": shape_ok,
            "shape": tuple(output.shape),
            "expected": expected,
            "shape_ok": shape_ok,
            "pad_zeros": True,
        })

    return results


# ---------------------------------------------------------------------------
# Validation: MechanismRunner
# ---------------------------------------------------------------------------
def validate_runner() -> dict:
    """Test MechanismRunner compute-all and cache behavior."""
    runner = MechanismRunner()

    # Collect union demand
    demand = runner.h3_demand
    h3, r3 = _make_dummy_inputs(demand)

    # Run all mechanisms
    t0 = time.perf_counter()
    runner.run(h3, r3)
    run_time = time.perf_counter() - t0

    # Verify all are cached
    cache_results = {}
    all_cached = True
    for name in MECHANISM_NAMES:
        try:
            output = runner.get(name)
            cached = True
            shape = tuple(output.shape)
            shape_ok = shape == (B, T, EXPECTED_OUTPUT_DIM)
        except RuntimeError:
            cached = False
            shape = None
            shape_ok = False
            all_cached = False

        cache_results[name] = {
            "cached": cached,
            "shape": shape,
            "shape_ok": shape_ok,
        }

    # Test cache retrieval consistency (get same tensor twice)
    consistency = True
    for name in MECHANISM_NAMES:
        try:
            t1 = runner.get(name)
            t2 = runner.get(name)
            if not torch.equal(t1, t2):
                consistency = False
        except RuntimeError:
            consistency = False

    # Test clear
    runner.clear()
    clear_works = True
    for name in MECHANISM_NAMES:
        try:
            runner.get(name)
            clear_works = False  # Should have raised
        except RuntimeError:
            pass

    return {
        "demand_count": len(demand),
        "run_time": run_time,
        "all_cached": all_cached,
        "cache_consistency": consistency,
        "clear_works": clear_works,
        "per_mechanism": cache_results,
    }


# ---------------------------------------------------------------------------
# Validation: dimension transposition
# ---------------------------------------------------------------------------
def validate_no_transposition() -> list:
    """Verify mechanisms don't accidentally transpose dimensions."""
    results = []

    # Use asymmetric B, T to detect transposition
    B_test, T_test = 2, 50

    for name in MECHANISM_NAMES:
        mech = MECHANISM_CLASSES[name]()
        demand = mech.h3_demand

        r3 = torch.rand(B_test, T_test, R3_DIM)
        h3: Dict[Tuple[int, int, int, int], Tensor] = {}
        for key in demand:
            h3[key] = torch.rand(B_test, T_test)

        try:
            output = mech.compute(h3, r3)
            # Expected: (2, 50, 30)
            shape = tuple(output.shape)
            ok = (
                shape[0] == B_test
                and shape[1] == T_test
                and shape[2] == mech.OUTPUT_DIM
            )
            results.append({
                "name": name,
                "passed": ok,
                "shape": shape,
                "expected": (B_test, T_test, mech.OUTPUT_DIM),
            })
        except Exception as e:
            results.append({
                "name": name,
                "passed": False,
                "error": str(e),
            })

    return results


# ---------------------------------------------------------------------------
# Main report
# ---------------------------------------------------------------------------
def main() -> None:
    t_start = time.perf_counter()
    print(_section("C3 MECHANISM VALIDATION REPORT"))
    print(f"  Mechanisms: {len(MECHANISM_NAMES)}")
    print(f"  Expected output: (B, T, {EXPECTED_OUTPUT_DIM}) per mechanism")
    print(f"  Test shapes: B={B}, T={T}")
    print()

    # ------------------------------------------------------------------
    # 1. Individual mechanism output validation
    # ------------------------------------------------------------------
    print(_section("1. Mechanism Output Validation"))
    mech_results = validate_mechanism_outputs()

    header = (f"  {'Name':<5} {'Full Name':<35} {'Shape':>14} "
              f"{'Range':>12} {'NaN':>4} {'Inf':>4} {'Demand':>6} {'Time':>8}")
    print(header)
    print(f"  {'-' * (len(header) - 2)}")

    all_passed = True
    for r in mech_results:
        if r.get("error"):
            print(f"  {r['name']:<5} ERROR: {r['error']}")
            all_passed = False
            continue

        status = "OK" if r["passed"] else "!!"
        shape_str = f"{r['shape']}"
        range_str = f"[{r['min_val']:.3f},{r['max_val']:.3f}]"
        nan_str = "OK" if r["no_nan"] else "FAIL"
        inf_str = "OK" if r["no_inf"] else "FAIL"
        if not r["passed"]:
            all_passed = False

        print(f"  {r['name']:<5} {r.get('full_name', ''):<35} {shape_str:>14} "
              f"{range_str:>12} {nan_str:>4} {inf_str:>4} "
              f"{r['demand_count']:>6} {r['compute_time']:.4f}s")

    n_pass = sum(1 for r in mech_results if r.get("passed", False))
    print(f"\n  [{n_pass}/{len(mech_results)}] mechanisms passed output validation")

    # ------------------------------------------------------------------
    # 2. h3_demand per mechanism
    # ------------------------------------------------------------------
    print(_section("2. H3 Demand Per Mechanism"))
    for r in mech_results:
        if r.get("error"):
            continue
        horizons_str = ", ".join(f"H{h}" for h in r["horizons"]) if r["horizons"] else "none"
        print(f"  {r['name']:<5}: {r['demand_count']:>5} tuples  "
              f"horizons=[{horizons_str}]")

    # Total demand via runner
    runner = MechanismRunner()
    total_mech_demand = runner.h3_demand
    print(f"\n  Total mechanism demand (union): {len(total_mech_demand)} tuples")

    # ------------------------------------------------------------------
    # 3. _aggregate_to_10d validation
    # ------------------------------------------------------------------
    print(_section("3. _aggregate_to_10d Validation"))
    agg_results = validate_aggregate_to_10d()

    for r in agg_results:
        status = "PASS" if r["passed"] else "FAIL"
        detail = f"shape={r['shape']}"
        if not r.get("pad_zeros", True):
            detail += " [pad not zero]"
        print(f"  [{status}] {r['case']:<20}: {detail}")

    n_agg_pass = sum(1 for r in agg_results if r["passed"])
    print(f"\n  [{n_agg_pass}/{len(agg_results)}] aggregate tests passed")

    # ------------------------------------------------------------------
    # 4. MechanismRunner validation
    # ------------------------------------------------------------------
    print(_section("4. MechanismRunner Validation"))
    runner_results = validate_runner()

    print(f"  Total demand (union):    {runner_results['demand_count']} tuples")
    print(f"  Run time:                {runner_results['run_time']:.4f}s")
    print(f"  [{'PASS' if runner_results['all_cached'] else 'FAIL'}] "
          f"All mechanisms cached after run()")
    print(f"  [{'PASS' if runner_results['cache_consistency'] else 'FAIL'}] "
          f"Cache retrieval consistency (get returns same tensor)")
    print(f"  [{'PASS' if runner_results['clear_works'] else 'FAIL'}] "
          f"clear() empties cache (get raises after clear)")

    print(f"\n  Per-mechanism cache status:")
    for name, info in runner_results["per_mechanism"].items():
        cached = "cached" if info["cached"] else "MISSING"
        shape = info["shape"] if info["shape"] else "N/A"
        shape_ok = "OK" if info.get("shape_ok") else "BAD"
        print(f"    {name:<5}: {cached:<8} shape={shape} [{shape_ok}]")

    # ------------------------------------------------------------------
    # 5. Dimension transposition checks
    # ------------------------------------------------------------------
    print(_section("5. Dimension Transposition Checks"))
    trans_results = validate_no_transposition()

    for r in trans_results:
        if r.get("error"):
            print(f"  [FAIL] {r['name']}: ERROR - {r['error']}")
            continue
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {r['name']}: output={r['shape']}, "
              f"expected={r.get('expected', 'N/A')}")

    n_trans_pass = sum(1 for r in trans_results if r.get("passed", False))
    print(f"\n  [{n_trans_pass}/{len(trans_results)}] transposition checks passed")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total_time = time.perf_counter() - t_start
    print(_section("SUMMARY"))
    print(f"  Mechanisms tested:      {len(MECHANISM_NAMES)}")
    print(f"  Output validation:      {n_pass}/{len(mech_results)} passed")
    print(f"  Aggregate tests:        {n_agg_pass}/{len(agg_results)} passed")
    print(f"  Runner cache:           {'PASS' if runner_results['all_cached'] else 'FAIL'}")
    print(f"  Transposition checks:   {n_trans_pass}/{len(trans_results)} passed")
    print(f"  Total demand tuples:    {runner_results['demand_count']}")
    print(f"  Total time:             {total_time:.3f}s")

    overall = (
        n_pass == len(mech_results)
        and n_agg_pass == len(agg_results)
        and runner_results["all_cached"]
        and runner_results["cache_consistency"]
        and runner_results["clear_works"]
        and n_trans_pass == len(trans_results)
    )
    if overall:
        print(f"  Status: ALL VALIDATIONS PASSED")
    else:
        print(f"  Status: SOME VALIDATIONS FAILED")
    print("=" * 72)


if __name__ == "__main__":
    main()
