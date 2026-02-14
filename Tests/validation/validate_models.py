#!/usr/bin/env python3
"""C3 Model Contract Validation Report.

Validates all 96 cognitive models across 9 units against their contracts:
- validate_constants() on every model
- LAYERS coverage of OUTPUT_DIM range
- h3_demand spec validity
- Mechanism usage distribution
- Brain region coverage
- Per-unit model counts and dimensions

Usage:
    python Tests/validation/validate_models.py
"""
from __future__ import annotations

import os
import sys
import time
from collections import defaultdict
from typing import Dict, List, Set, Tuple

# ---------------------------------------------------------------------------
# Path setup
# ---------------------------------------------------------------------------
_PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir, os.pardir)
)
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)

from Musical_Intelligence.contracts.bases.base_model import BaseModel
from Musical_Intelligence.contracts.bases.base_unit import BaseCognitiveUnit
from Musical_Intelligence.brain.units import (
    SPUUnit, STUUnit, IMUUnit, ASUUnit, NDUUnit, MPUUnit, PCUUnit,
    ARUUnit, RPUUnit,
)
from Musical_Intelligence.ear.h3.constants.horizons import N_HORIZONS
from Musical_Intelligence.ear.h3.constants.morphs import N_MORPHS
from Musical_Intelligence.ear.h3.constants.laws import N_LAWS
from Musical_Intelligence.ear.r3.constants import R3_DIM


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
UNIT_ORDER = ("SPU", "STU", "IMU", "ASU", "NDU", "MPU", "PCU", "ARU", "RPU")
UNIT_CLASSES = {
    "SPU": SPUUnit, "STU": STUUnit, "IMU": IMUUnit,
    "ASU": ASUUnit, "NDU": NDUUnit, "MPU": MPUUnit,
    "PCU": PCUUnit, "ARU": ARUUnit, "RPU": RPUUnit,
}
EXPECTED_TOTAL_DIM = 1006
EXPECTED_TOTAL_MODELS = 96

VALID_TIERS = frozenset({"alpha", "beta", "gamma"})
VALID_LAYER_CODES = frozenset({"E", "M", "P", "F"})
ALL_MECHANISMS = frozenset({
    "PPC", "TPC", "BEP", "ASA", "TMH", "MEM", "SYN", "AED", "CPD", "C0P",
})


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _section(title: str) -> str:
    return f"\n{'=' * 72}\n  {title}\n{'=' * 72}"


# ---------------------------------------------------------------------------
# Validation functions
# ---------------------------------------------------------------------------
def validate_all_models() -> dict:
    """Run validate_constants() on all 96 models and collect results."""
    results = {
        "per_unit": {},
        "all_errors": [],
        "total_models": 0,
        "total_passed": 0,
        "total_failed": 0,
    }

    for unit_name in UNIT_ORDER:
        unit = UNIT_CLASSES[unit_name]()
        unit_results = {
            "n_models": len(unit.models),
            "total_dim": unit.total_dim,
            "circuit": unit.CIRCUIT,
            "effect": unit.POOLED_EFFECT,
            "models": [],
            "unit_errors": [],
        }

        # Validate unit-level
        unit_errs = unit.validate()
        unit_results["unit_errors"] = unit_errs

        for model in unit.models:
            results["total_models"] += 1
            errors = model.validate_constants()
            model_info = {
                "name": model.NAME,
                "full_name": model.FULL_NAME,
                "tier": model.TIER,
                "output_dim": model.OUTPUT_DIM,
                "n_mechanisms": len(model.MECHANISM_NAMES),
                "mechanism_names": model.MECHANISM_NAMES,
                "n_layers": len(model.LAYERS),
                "n_cross_unit": len(model.CROSS_UNIT_READS),
                "errors": errors,
                "passed": len(errors) == 0,
            }
            unit_results["models"].append(model_info)
            if model_info["passed"]:
                results["total_passed"] += 1
            else:
                results["total_failed"] += 1
                for err in errors:
                    results["all_errors"].append(
                        f"{unit_name}/{model.NAME}: {err}"
                    )

        results["per_unit"][unit_name] = unit_results

    return results


def analyze_layers(units: dict) -> dict:
    """Analyze LAYERS coverage across all models."""
    layer_analysis = {
        "total_models": 0,
        "full_coverage": 0,
        "partial_coverage": 0,
        "layer_code_counts": defaultdict(int),
        "layer_code_dims": defaultdict(int),
        "issues": [],
    }

    for unit_name in UNIT_ORDER:
        unit = UNIT_CLASSES[unit_name]()
        for model in unit.models:
            layer_analysis["total_models"] += 1

            if not model.LAYERS:
                layer_analysis["issues"].append(
                    f"{unit_name}/{model.NAME}: No LAYERS defined"
                )
                continue

            # Check full coverage
            coverage = [0] * model.OUTPUT_DIM
            for layer in model.LAYERS:
                for i in range(layer.start, layer.end):
                    if 0 <= i < model.OUTPUT_DIM:
                        coverage[i] += 1
                layer_analysis["layer_code_counts"][layer.code] += 1
                layer_analysis["layer_code_dims"][layer.code] += layer.dim

            uncovered = [i for i, c in enumerate(coverage) if c == 0]
            if uncovered:
                layer_analysis["partial_coverage"] += 1
                layer_analysis["issues"].append(
                    f"{unit_name}/{model.NAME}: Uncovered dims {uncovered}"
                )
            else:
                layer_analysis["full_coverage"] += 1

    return layer_analysis


def analyze_h3_demands() -> dict:
    """Analyze h3_demand specs across all models."""
    analysis = {
        "total_models_with_demand": 0,
        "total_models_without_demand": 0,
        "total_demand_specs": 0,
        "total_unique_tuples": 0,
        "range_violations": [],
    }

    all_tuples: Set[Tuple[int, int, int, int]] = set()

    for unit_name in UNIT_ORDER:
        unit = UNIT_CLASSES[unit_name]()
        for model in unit.models:
            try:
                demands = model.h3_demand
                if demands:
                    analysis["total_models_with_demand"] += 1
                    analysis["total_demand_specs"] += len(demands)
                    for spec in demands:
                        t = spec.as_tuple()
                        all_tuples.add(t)
                        r3_idx, horizon, morph, law = t
                        # Validate ranges
                        if not (0 <= r3_idx < R3_DIM):
                            analysis["range_violations"].append(
                                f"{unit_name}/{model.NAME}: "
                                f"r3_idx={r3_idx} out of [0, {R3_DIM})"
                            )
                        if not (0 <= horizon < N_HORIZONS):
                            analysis["range_violations"].append(
                                f"{unit_name}/{model.NAME}: "
                                f"horizon={horizon} out of [0, {N_HORIZONS})"
                            )
                        if not (0 <= morph < N_MORPHS):
                            analysis["range_violations"].append(
                                f"{unit_name}/{model.NAME}: "
                                f"morph={morph} out of [0, {N_MORPHS})"
                            )
                        if not (0 <= law < N_LAWS):
                            analysis["range_violations"].append(
                                f"{unit_name}/{model.NAME}: "
                                f"law={law} out of [0, {N_LAWS})"
                            )
                else:
                    analysis["total_models_without_demand"] += 1
            except Exception as e:
                analysis["total_models_without_demand"] += 1

    analysis["total_unique_tuples"] = len(all_tuples)
    return analysis


def analyze_mechanisms() -> dict:
    """Analyze mechanism usage distribution across models."""
    mech_usage: Dict[str, List[str]] = defaultdict(list)
    models_with_mech = 0
    models_without_mech = 0

    for unit_name in UNIT_ORDER:
        unit = UNIT_CLASSES[unit_name]()
        for model in unit.models:
            if model.MECHANISM_NAMES:
                models_with_mech += 1
                for mech in model.MECHANISM_NAMES:
                    mech_usage[mech].append(f"{unit_name}/{model.NAME}")
            else:
                models_without_mech += 1

    return {
        "models_with_mechanisms": models_with_mech,
        "models_without_mechanisms": models_without_mech,
        "per_mechanism": {k: len(v) for k, v in sorted(mech_usage.items())},
        "mechanism_models": dict(mech_usage),
    }


def analyze_brain_regions() -> dict:
    """Analyze brain region coverage across models."""
    all_regions: Dict[str, int] = defaultdict(int)
    cortical = 0
    subcortical = 0
    hemispheres: Dict[str, int] = defaultdict(int)

    for unit_name in UNIT_ORDER:
        unit = UNIT_CLASSES[unit_name]()
        for model in unit.models:
            try:
                regions = model.brain_regions
                for region in regions:
                    all_regions[region.name] += 1
                    if region.is_cortical:
                        cortical += 1
                    else:
                        subcortical += 1
                    hemispheres[region.hemisphere] += 1
            except Exception:
                pass

    return {
        "unique_regions": len(all_regions),
        "total_region_references": sum(all_regions.values()),
        "cortical": cortical,
        "subcortical": subcortical,
        "hemispheres": dict(hemispheres),
        "top_regions": sorted(all_regions.items(), key=lambda x: -x[1])[:15],
    }


# ---------------------------------------------------------------------------
# Main report
# ---------------------------------------------------------------------------
def main() -> None:
    t_start = time.perf_counter()
    print(_section("C3 MODEL CONTRACT VALIDATION REPORT"))
    print(f"  Expected: {EXPECTED_TOTAL_MODELS} models, "
          f"{len(UNIT_ORDER)} units, {EXPECTED_TOTAL_DIM}D total output")
    print()

    # ------------------------------------------------------------------
    # 1. Run validate_constants() on all models
    # ------------------------------------------------------------------
    print(_section("1. Model Contract Validation (validate_constants)"))
    t0 = time.perf_counter()
    results = validate_all_models()
    val_time = time.perf_counter() - t0

    print(f"  Total models: {results['total_models']}")
    print(f"  Passed: {results['total_passed']}")
    print(f"  Failed: {results['total_failed']}")
    print(f"  Time: {val_time:.3f}s")

    if results["all_errors"]:
        print(f"\n  Errors ({len(results['all_errors'])}):")
        for err in results["all_errors"][:20]:
            print(f"    - {err}")
        if len(results["all_errors"]) > 20:
            print(f"    ... and {len(results['all_errors']) - 20} more errors")

    # ------------------------------------------------------------------
    # 2. Per-unit model counts and dimensions
    # ------------------------------------------------------------------
    print(_section("2. Per-Unit Model Counts & Dimensions"))
    header = (f"  {'Unit':<5} {'Circuit':<14} {'d':>5} {'Models':>6} "
              f"{'Dim':>5} {'alpha':>5} {'beta':>5} {'gamma':>5}")
    print(header)
    print(f"  {'-' * (len(header) - 2)}")

    total_dim = 0
    total_alpha = 0
    total_beta = 0
    total_gamma = 0

    for unit_name in UNIT_ORDER:
        info = results["per_unit"][unit_name]
        n_alpha = sum(1 for m in info["models"] if m["tier"] == "alpha")
        n_beta = sum(1 for m in info["models"] if m["tier"] == "beta")
        n_gamma = sum(1 for m in info["models"] if m["tier"] == "gamma")
        total_dim += info["total_dim"]
        total_alpha += n_alpha
        total_beta += n_beta
        total_gamma += n_gamma
        print(f"  {unit_name:<5} {info['circuit']:<14} {info['effect']:>5.2f} "
              f"{info['n_models']:>6} {info['total_dim']:>5} "
              f"{n_alpha:>5} {n_beta:>5} {n_gamma:>5}")

    print(f"  {'-' * (len(header) - 2)}")
    print(f"  {'TOTAL':<5} {'':<14} {'':<5} {results['total_models']:>6} "
          f"{total_dim:>5} {total_alpha:>5} {total_beta:>5} {total_gamma:>5}")
    print(f"\n  [{'PASS' if total_dim == EXPECTED_TOTAL_DIM else 'FAIL'}] "
          f"Total dim: {total_dim} (expected {EXPECTED_TOTAL_DIM})")
    print(f"  [{'PASS' if results['total_models'] == EXPECTED_TOTAL_MODELS else 'FAIL'}] "
          f"Total models: {results['total_models']} (expected {EXPECTED_TOTAL_MODELS})")

    # ------------------------------------------------------------------
    # 3. LAYERS coverage analysis
    # ------------------------------------------------------------------
    print(_section("3. LAYERS Coverage Analysis"))
    layer_info = analyze_layers(results)
    print(f"  Models with full coverage:    {layer_info['full_coverage']}")
    print(f"  Models with partial coverage: {layer_info['partial_coverage']}")

    print(f"\n  Layer code distribution:")
    for code in sorted(layer_info["layer_code_counts"]):
        n = layer_info["layer_code_counts"][code]
        d = layer_info["layer_code_dims"][code]
        label = {"E": "Extraction", "M": "Mechanism",
                 "P": "Psychological", "F": "Forecast"}.get(code, code)
        print(f"    {code} ({label:<14}): {n:>4} layers, {d:>5} total dims")

    if layer_info["issues"]:
        print(f"\n  Coverage issues ({len(layer_info['issues'])}):")
        for issue in layer_info["issues"][:10]:
            print(f"    - {issue}")

    # ------------------------------------------------------------------
    # 4. H3 demand spec validation
    # ------------------------------------------------------------------
    print(_section("4. H3 Demand Spec Validation"))
    h3_info = analyze_h3_demands()
    print(f"  Models with h3_demand:    {h3_info['total_models_with_demand']}")
    print(f"  Models without h3_demand: {h3_info['total_models_without_demand']}")
    print(f"  Total demand specs:       {h3_info['total_demand_specs']}")
    print(f"  Unique 4-tuples:          {h3_info['total_unique_tuples']}")

    n_violations = len(h3_info["range_violations"])
    print(f"\n  [{'PASS' if n_violations == 0 else 'FAIL'}] "
          f"Range violations: {n_violations}")
    if h3_info["range_violations"]:
        for v in h3_info["range_violations"][:10]:
            print(f"    - {v}")

    # ------------------------------------------------------------------
    # 5. Mechanism usage distribution
    # ------------------------------------------------------------------
    print(_section("5. Mechanism Usage Distribution"))
    mech_info = analyze_mechanisms()
    print(f"  Models using mechanisms:     {mech_info['models_with_mechanisms']}")
    print(f"  Models without mechanisms:   {mech_info['models_without_mechanisms']}")

    print(f"\n  Per-mechanism usage:")
    for mech, count in sorted(mech_info["per_mechanism"].items()):
        in_all = mech in ALL_MECHANISMS
        marker = " " if in_all else " [UNKNOWN]"
        print(f"    {mech:<5}: {count:>3} models{marker}")

    unused = ALL_MECHANISMS - set(mech_info["per_mechanism"].keys())
    if unused:
        print(f"\n  Unused mechanisms: {sorted(unused)}")

    # ------------------------------------------------------------------
    # 6. Brain region coverage
    # ------------------------------------------------------------------
    print(_section("6. Brain Region Coverage"))
    region_info = analyze_brain_regions()
    print(f"  Unique brain regions:     {region_info['unique_regions']}")
    print(f"  Total region references:  {region_info['total_region_references']}")
    print(f"  Cortical references:      {region_info['cortical']}")
    print(f"  Subcortical references:   {region_info['subcortical']}")

    print(f"\n  Hemisphere distribution:")
    for hemi, count in sorted(region_info["hemispheres"].items()):
        print(f"    {hemi:<10}: {count}")

    print(f"\n  Top 15 referenced regions:")
    for name, count in region_info["top_regions"]:
        print(f"    {name:<40}: {count}")

    # ------------------------------------------------------------------
    # 7. Detailed model listing
    # ------------------------------------------------------------------
    print(_section("7. Model Listing (by unit and tier)"))
    for unit_name in UNIT_ORDER:
        info = results["per_unit"][unit_name]
        print(f"\n  {unit_name} ({info['circuit']}, {info['total_dim']}D):")
        for m in info["models"]:
            status = "OK" if m["passed"] else "ERR"
            mechs = ",".join(m["mechanism_names"]) if m["mechanism_names"] else "-"
            print(f"    [{status}] {m['name']:<8} {m['tier']:<6} "
                  f"{m['output_dim']:>3}D  "
                  f"layers={m['n_layers']}  "
                  f"mechs={mechs}")

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    total_time = time.perf_counter() - t_start
    print(_section("SUMMARY"))
    print(f"  Models validated:     {results['total_models']}")
    print(f"  Contracts passed:     {results['total_passed']}")
    print(f"  Contracts failed:     {results['total_failed']}")
    print(f"  Total output dim:     {total_dim}")
    print(f"  Layer coverage:       {layer_info['full_coverage']}/{layer_info['total_models']}")
    print(f"  Demand range valid:   {n_violations == 0}")
    print(f"  Unique brain regions: {region_info['unique_regions']}")
    print(f"  Total time:           {total_time:.3f}s")

    all_ok = (
        results["total_failed"] == 0
        and total_dim == EXPECTED_TOTAL_DIM
        and results["total_models"] == EXPECTED_TOTAL_MODELS
        and n_violations == 0
    )
    if all_ok:
        print(f"  Status: ALL VALIDATIONS PASSED")
    else:
        print(f"  Status: SOME VALIDATIONS FAILED")
    print("=" * 72)


if __name__ == "__main__":
    main()
