"""Verify all model H3 demands can be satisfied."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Set, Tuple


@dataclass
class DemandReport:
    total_tuples: int = 0
    models_with_demands: int = 0
    models_without_demands: int = 0
    unique_horizons: Set[int] = field(default_factory=set)


def check_demand_coverage(package: str = "mi_beta.brain") -> DemandReport:
    from mi_beta.core.registry import ModelRegistry
    registry = ModelRegistry()
    registry.scan(package)
    report = DemandReport()
    all_demands = set()
    for model in registry.all_models():
        demands = model.h3_demand_tuples()
        if demands:
            report.models_with_demands += 1
            all_demands |= demands
        else:
            report.models_without_demands += 1
    report.total_tuples = len(all_demands)
    report.unique_horizons = {d[1] for d in all_demands}
    return report
