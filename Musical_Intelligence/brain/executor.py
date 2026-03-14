"""Depth-ordered execution engine for C³ nuclei.

Executes nuclei in depth order (0→5).

Scope-aware routing: downstream nuclei see only routable dims
(internal + hybrid) from upstream nuclei.

See TERMINOLOGY.md Sections 6 and 13 for the full execution specification.

Note: Region activation (RAM) and neurochemical accumulation are disabled.
    RAM and neuro tensors are returned as zeros for backward compatibility.
"""
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Tuple

import torch

from Musical_Intelligence.contracts.bases.nucleus import (
    Associator,
    Encoder,
    Hub,
    Integrator,
    Nucleus,
    Relay,
)

if TYPE_CHECKING:
    from torch import Tensor

# RAM and neuro dimensions (kept for backward compatibility)
_NUM_REGIONS = 26
_NUM_NEURO = 4


def execute(
    nuclei: List[Nucleus],
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    cross_unit_inputs: Dict[str, Tensor] | None = None,
) -> Tuple[Dict[str, Tensor], Tensor, Tensor]:
    """Execute nuclei in depth order.

    Args:
        nuclei: All nuclei to execute (will be sorted by PROCESSING_DEPTH).
        h3_features: Per-demand H³ time series, keyed by 4-tuples.
        r3_features: ``(B, T, 97)`` R³ spectral features.
        cross_unit_inputs: Optional cross-unit pathway tensors.

    Returns:
        Tuple of:
            outputs: Dict mapping nucleus NAME → full ``(B, T, OUTPUT_DIM)``
            ram: ``(B, T, 26)`` zeros (region activation disabled)
            neuro: ``(B, T, 4)`` zeros (neurochemical accumulation disabled)
    """
    B, T = r3_features.shape[0], r3_features.shape[1]
    device = r3_features.device

    # RAM and neuro disabled — return zeros for backward compatibility
    ram = torch.zeros(B, T, _NUM_REGIONS, device=device)
    neuro = torch.zeros(B, T, _NUM_NEURO, device=device)

    # Sort by depth
    sorted_nuclei = sorted(nuclei, key=lambda n: n.PROCESSING_DEPTH)

    # Group by depth for processing
    depth_groups: Dict[int, List[Nucleus]] = defaultdict(list)
    for n in sorted_nuclei:
        depth_groups[n.PROCESSING_DEPTH].append(n)

    # All outputs stored (full tensor, not scope-filtered)
    outputs: Dict[str, Tensor] = {}

    cross = cross_unit_inputs or {}

    for depth in sorted(depth_groups.keys()):
        for nucleus in depth_groups[depth]:
            output = _compute_nucleus(
                nucleus, h3_features, r3_features, outputs, cross,
            )
            outputs[nucleus.NAME] = output

    return outputs, ram, neuro


def _compute_nucleus(
    nucleus: Nucleus,
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    outputs: Dict[str, Tensor],
    cross_unit_inputs: Dict[str, Tensor],
) -> Tensor:
    """Dispatch compute() based on nucleus role, with scope-filtered inputs."""

    if isinstance(nucleus, Relay):
        return nucleus.compute(h3_features, r3_features)

    elif isinstance(nucleus, Encoder):
        relay_outputs = _scope_filter_upstream(
            outputs, nucleus.UPSTREAM_READS, nucleus,
        )
        return nucleus.compute(h3_features, r3_features, relay_outputs)

    elif isinstance(nucleus, Associator):
        upstream = _scope_filter_upstream(
            outputs, nucleus.UPSTREAM_READS, nucleus,
        )
        return nucleus.compute(h3_features, r3_features, upstream)

    elif isinstance(nucleus, (Integrator, Hub)):
        upstream = _scope_filter_upstream(
            outputs, nucleus.UPSTREAM_READS, nucleus,
        )
        # Gather cross-unit inputs for this nucleus
        cross = {}
        for pathway in nucleus.CROSS_UNIT_READS:
            key = pathway.pathway_id if hasattr(pathway, 'pathway_id') else str(pathway)
            if key in cross_unit_inputs:
                cross[key] = cross_unit_inputs[key]
        return nucleus.compute(
            h3_features, r3_features, upstream,
            cross if cross else None,
        )

    else:
        raise TypeError(f"Unknown nucleus type: {type(nucleus).__name__}")


def _scope_filter_upstream(
    outputs: Dict[str, Tensor],
    upstream_reads: Tuple[str, ...],
    consumer: Nucleus,
) -> Dict[str, Tensor]:
    """Filter upstream outputs to only routable dims (internal + hybrid).

    For each upstream nucleus that the consumer declares as a dependency,
    select only the routable dimension indices from its full output tensor.
    """
    # For now, pass full tensors — scope filtering will be refined
    # when we have the full 96-nucleus registry. The key insight is that
    # downstream nuclei should only see routable_dims, but at this stage
    # BCH (a Relay) has no upstream dependencies, so this is a no-op.
    filtered: Dict[str, Tensor] = {}
    for name in upstream_reads:
        if name in outputs:
            filtered[name] = outputs[name]
    return filtered


