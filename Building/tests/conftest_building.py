"""Building-specific test fixtures.

Detects whether a model is still a skeleton or has been properly built.
Skeleton indicators:
  - dimension_names follow "{name}_e0, {name}_e1, ..." pattern
  - citations contain Citation("Author", 2020, ...)
  - compute() uses torch.linspace or torch.arange(...) % r3_dim
  - h3_demand has exactly 4 tuples (generic)
"""
from __future__ import annotations

import inspect
import re
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from Musical_Intelligence.contracts.bases.base_model import BaseModel


def is_skeleton(model: "BaseModel") -> bool:
    """Return True if the model appears to be an unbuilt skeleton."""
    checks = []

    # Check 1: Generic dimension names ({name}_e0 pattern)
    names = model.dimension_names
    name_lower = model.NAME.lower()
    generic_count = sum(
        1 for n in names
        if re.match(rf"^{name_lower}_[empf]\d+$", n)
    )
    checks.append(generic_count > len(names) // 2)

    # Check 2: Placeholder citations
    meta = model.metadata
    if meta.citations:
        checks.append(meta.citations[0].first_author == "Author")
    else:
        checks.append(True)

    # Check 3: Very few h3_demand tuples (skeleton has exactly 4)
    checks.append(len(model.h3_demand) <= 4)

    # Check 4: Generic compute() body (torch.linspace pattern)
    source = inspect.getsource(model.compute)
    checks.append("torch.linspace" in source or "torch.arange" in source)

    # Model is skeleton if ANY indicator is true
    return any(checks)


def skeleton_indicators(model: "BaseModel") -> list[str]:
    """Return list of skeleton indicators found in the model."""
    indicators = []
    name_lower = model.NAME.lower()

    # Dimension names
    names = model.dimension_names
    generic_count = sum(
        1 for n in names
        if re.match(rf"^{name_lower}_[empf]\d+$", n)
    )
    if generic_count > 0:
        indicators.append(
            f"Generic dimension names: {generic_count}/{len(names)} "
            f"follow '{name_lower}_X#' pattern"
        )

    # Citations
    meta = model.metadata
    if meta.citations and meta.citations[0].first_author == "Author":
        indicators.append("Placeholder citation: Citation('Author', 2020, ...)")

    # H3 demand count
    demand_count = len(model.h3_demand)
    if demand_count <= 4:
        indicators.append(
            f"Only {demand_count} h3_demand tuples (skeleton has 4, "
            f"built models have 8-20)"
        )

    # Compute source
    source = inspect.getsource(model.compute)
    if "torch.linspace" in source:
        indicators.append("compute() uses torch.linspace (skeleton pattern)")
    if "torch.arange" in source and "% r3_dim" in source:
        indicators.append("compute() uses torch.arange % r3_dim (skeleton cycling)")

    # Brain regions count
    regions = model.brain_regions
    if len(regions) <= 3:
        indicators.append(
            f"Only {len(regions)} brain regions (docs typically specify 4-6)"
        )

    # Version check
    if meta.version == "1.0.0":
        indicators.append("Version still at 1.0.0 (skeleton default)")

    return indicators
