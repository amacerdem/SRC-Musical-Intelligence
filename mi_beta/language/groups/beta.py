"""
beta (Beta) -- Neuroscience Semantics (variable D)

Level 2: WHERE in the brain.
Maps Brain model outputs to brain region activations using the
BrainRegion declarations from each active model.

In mi_beta, each model declares brain_regions.  Beta collects all
unique regions from active models and produces one activation dimension
per unique region.

Total: N_unique_regions

Scientific basis:
    Each BrainRegion carries MNI152 coordinates and evidence_count
    from the C3 meta-analysis database.
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

import torch
from torch import Tensor

from ...contracts.base_semantic_group import BaseSemanticGroup, SemanticGroupOutput
from ...core.types import BrainOutput


class BetaGroup(BaseSemanticGroup):
    """Neuroscience semantics: per-region activation from active models."""

    LEVEL = 2
    GROUP_NAME = "beta"
    DISPLAY_NAME = "beta"

    def __init__(self, registry: Any = None) -> None:
        self._region_names: List[str] = []
        # Map: region_abbreviation -> list of (unit_name, model_name, model_output_dim)
        self._region_model_map: Dict[str, List[Tuple[str, str]]] = {}
        self._output_dim: int = 0
        if registry is not None:
            self._configure(registry)

    def _configure(self, registry: Any) -> None:
        """Configure from a scanned ModelRegistry."""
        region_set: Dict[str, List[Tuple[str, str]]] = {}
        for model in registry.active_models():
            brain_regions = getattr(model, "brain_regions", None)
            if brain_regions is None:
                continue
            for region in brain_regions:
                abbrev = region.abbreviation
                if abbrev not in region_set:
                    region_set[abbrev] = []
                region_set[abbrev].append((model.UNIT, model.NAME))

        self._region_names = sorted(region_set.keys())
        self._region_model_map = region_set
        self._output_dim = max(len(self._region_names), 1)

    @property
    def OUTPUT_DIM(self) -> int:  # type: ignore[override]
        return self._output_dim

    @property
    def dimension_names(self) -> List[str]:
        if not self._region_names:
            return ["no_region_placeholder"]
        return [f"region_{name.lower()}" for name in self._region_names]

    def compute(self, brain_output: Any, **kwargs: Any) -> SemanticGroupOutput:
        """Compute beta group -- per-region activation.

        For each unique brain region, averages the mean activation of all
        models that declare that region.
        """
        B, T, _ = brain_output.tensor.shape
        device = brain_output.tensor.device
        dtype = brain_output.tensor.dtype

        if not self._region_names:
            # Fallback: single placeholder dimension
            tensor = torch.full(
                (B, T, 1), 0.5, device=device, dtype=dtype
            )
            return SemanticGroupOutput(
                group_name=self.GROUP_NAME,
                level=self.LEVEL,
                tensor=tensor,
                dimension_names=("no_region_placeholder",),
            )

        parts: list[Tensor] = []
        for region_abbrev in self._region_names:
            model_refs = self._region_model_map.get(region_abbrev, [])
            if not model_refs:
                parts.append(torch.full((B, T, 1), 0.5, device=device, dtype=dtype))
                continue

            activations: list[Tensor] = []
            for unit_name, model_name in model_refs:
                try:
                    model_tensor = brain_output.get_model(unit_name, model_name)
                    activations.append(model_tensor.mean(dim=-1, keepdim=True))
                except (KeyError, ValueError):
                    pass

            if activations:
                region_act = torch.stack(activations, dim=-1).mean(dim=-1)  # (B, T, 1)
            else:
                region_act = torch.full((B, T, 1), 0.5, device=device, dtype=dtype)
            parts.append(region_act)

        tensor = torch.cat(parts, dim=-1)  # (B, T, N_regions)

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=tensor.clamp(0, 1),
            dimension_names=tuple(self.dimension_names),
        )
