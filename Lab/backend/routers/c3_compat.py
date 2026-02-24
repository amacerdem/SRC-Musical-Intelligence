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
