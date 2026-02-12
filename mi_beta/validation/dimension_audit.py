"""Audit all models for metadata completeness."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class AuditResult:
    total: int = 0
    complete: int = 0
    incomplete: List[str] = field(default_factory=list)
    details: Dict[str, List[str]] = field(default_factory=dict)


def audit_all_models(package: str = "mi_beta.brain") -> AuditResult:
    from mi_beta.core.registry import ModelRegistry
    registry = ModelRegistry()
    registry.scan(package)
    result = AuditResult()
    for model in registry.all_models():
        result.total += 1
        issues = []
        if len(model.dimension_names) != model.OUTPUT_DIM:
            issues.append(
                f"dimension_names ({len(model.dimension_names)}) "
                f"!= OUTPUT_DIM ({model.OUTPUT_DIM})"
            )
        if not model.brain_regions:
            issues.append("no brain_regions defined")
        if not model.metadata.citations:
            issues.append("no citations in metadata")
        if issues:
            result.incomplete.append(model.NAME)
            result.details[model.NAME] = issues
        else:
            result.complete += 1
    return result
