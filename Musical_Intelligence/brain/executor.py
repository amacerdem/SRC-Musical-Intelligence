"""Depth-ordered execution engine for C³ nuclei.

Executes nuclei in depth order (0→5), applying RegionLinks (→ RAM) and
NeuroLinks (→ neuro) after each nucleus's compute().

Scope-aware routing: downstream nuclei see only routable dims
(internal + hybrid) from upstream nuclei.

See TERMINOLOGY.md Sections 6 and 13 for the full execution specification.
"""
from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Tuple

import torch

from Musical_Intelligence.brain.neurochemicals import accumulate_neuro, init_neuro
from Musical_Intelligence.brain.regions import NUM_REGIONS, region_index
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


def execute(
    nuclei: List[Nucleus],
    h3_features: Dict[Tuple[int, int, int, int], Tensor],
    r3_features: Tensor,
    cross_unit_inputs: Dict[str, Tensor] | None = None,
) -> Tuple[Dict[str, Tensor], Tensor, Tensor]:
    """Execute nuclei in depth order, building RAM and neuro tensors.

    Args:
        nuclei: All nuclei to execute (will be sorted by PROCESSING_DEPTH).
        h3_features: Per-demand H³ time series, keyed by 4-tuples.
        r3_features: ``(B, T, 97)`` R³ spectral features.
        cross_unit_inputs: Optional cross-unit pathway tensors.

    Returns:
        Tuple of:
            outputs: Dict mapping nucleus NAME → full ``(B, T, OUTPUT_DIM)``
            ram: ``(B, T, 26)`` Region Activation Map
            neuro: ``(B, T, 4)`` neurochemical state
    """
    B, T = r3_features.shape[0], r3_features.shape[1]
    device = r3_features.device

    # Initialize RAM and neuro
    ram = torch.zeros(B, T, NUM_REGIONS, device=device)
    neuro = init_neuro(B, T, device)

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

            # Apply RegionLinks → RAM
            _apply_region_links(ram, nucleus, output)

            # Apply NeuroLinks → neuro
            accumulate_neuro(neuro, nucleus, output)

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


def _apply_region_links(
    ram: Tensor,
    nucleus: Nucleus,
    output: Tensor,
) -> None:
    """Apply RegionLinks: accumulate nucleus output dims into RAM.

    For each RegionLink, the corresponding output dimension's value
    (weighted) is added to the appropriate RAM channel.
    """
    dim_names = nucleus.dimension_names
    name_to_idx = {name: i for i, name in enumerate(dim_names)}

    for rl in nucleus.region_links:
        dim_idx = name_to_idx.get(rl.dim_name)
        if dim_idx is None:
            continue
        try:
            reg_idx = region_index(rl.region)
        except KeyError:
            continue

        # Accumulate: RAM[region] += output[dim] * weight
        ram[:, :, reg_idx] = ram[:, :, reg_idx] + output[:, :, dim_idx] * rl.weight
