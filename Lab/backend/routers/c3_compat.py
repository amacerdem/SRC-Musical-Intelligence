"""C³ compatibility router — serves the URLs that c3Store.ts expects.

The frontend's Zustand stores use:
    GET /api/c3/beliefs?experiment={id}
    GET /api/c3/relays/{name}?experiment={id}

This router translates these to the canonical HDF5 storage reads,
so the frontend works without URL changes.
"""
from __future__ import annotations

import numpy as np
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response

from .. import storage

router = APIRouter(tags=["c3-compat"])


@router.get("/beliefs")
async def get_beliefs(experiment: str = Query(..., description="Experiment ID")):
    """Return C³ beliefs as binary Float32 (T × N_ext).

    Matches c3Store.ts: ``fetch(`/api/c3/beliefs?experiment=${id}`)``
    """
    if not storage.exists(experiment):
        raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment}")

    data = storage.load_dataset(experiment, "c3/beliefs")
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
    )


@router.get("/relays/{relay_name}")
async def get_relay(
    relay_name: str,
    experiment: str = Query(..., description="Experiment ID"),
):
    """Return relay output as binary Float32 (T × D), with X-Relay-Dim header.

    Matches c3Store.ts: ``fetch(`/api/c3/relays/${relayName}?experiment=${id}`)``
    """
    if not storage.exists(experiment):
        raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment}")

    try:
        data = storage.load_dataset(experiment, f"c3/relays/{relay_name}")
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Relay '{relay_name}' not found")

    dim = data.shape[1] if data.ndim > 1 else 1
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={"X-Relay-Dim": str(dim)},
    )


@router.get("/beliefs/{belief_name}/decomposition")
async def get_belief_decomposition(
    belief_name: str,
    experiment: str = Query(..., description="Experiment ID"),
):
    """Return per-band and per-law decomposition traces for a belief.

    Response: Binary Float32Array (T × N_variants), column-major.
    Headers indicate variant names and frame count.
    """
    import h5py

    if not storage.exists(experiment):
        raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment}")

    h5_path = storage._h5_path(experiment)
    group_path = f"c3/belief_decomposition/{belief_name}"

    with h5py.File(h5_path, "r") as f:
        if group_path not in f:
            raise HTTPException(
                status_code=404,
                detail=f"Decomposition not found for '{belief_name}'",
            )

        group = f[group_path]
        variant_names = sorted(group.keys())
        arrays = [group[v][:].astype(np.float32) for v in variant_names]

    if not arrays:
        raise HTTPException(status_code=404, detail="No decomposition variants found")

    T = arrays[0].shape[0]
    # Stack as columns: (T, N_variants)
    stacked = np.column_stack(arrays)

    return Response(
        content=stacked.tobytes(),
        media_type="application/octet-stream",
        headers={
            "X-Decomposition-Variants": ",".join(variant_names),
            "X-Decomposition-Frames": str(T),
        },
    )
