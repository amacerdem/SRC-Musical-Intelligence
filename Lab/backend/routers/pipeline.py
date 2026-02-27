"""Pipeline router — run analysis, poll status, fetch results."""
from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any, Dict

import numpy as np
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from .. import storage

router = APIRouter(tags=["pipeline"])

# In-memory status tracker:  {experiment_id: {status, phase, progress, fps, error}}
_status: Dict[str, Dict[str, Any]] = {}


class RunRequest(BaseModel):
    audio_name: str
    excerpt_s: float = 0.0  # 0 = full file


# ---------------------------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------------------------

@router.post("/run")
async def run_pipeline(req: RunRequest, request: Request):
    """Start pipeline analysis in background.

    Returns the experiment_id immediately; poll ``/status/{id}`` for progress.
    """
    from ..config import AUDIO_CATALOG, MIDI_CATALOG

    if req.audio_name not in AUDIO_CATALOG and req.audio_name not in MIDI_CATALOG:
        raise HTTPException(status_code=400, detail=f"Unknown audio: {req.audio_name}")

    experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Avoid duplicate runs
    if experiment_id in _status and _status[experiment_id].get("status") == "running":
        raise HTTPException(status_code=409, detail="Pipeline already running")

    _status[experiment_id] = {
        "status": "running",
        "phase": "queued",
        "progress": 0.0,
        "fps": 0.0,
        "audio_name": req.audio_name,
    }

    pipeline = request.app.state.pipeline

    def status_callback(phase: str, progress: float):
        _status[experiment_id]["phase"] = phase
        _status[experiment_id]["progress"] = progress

    async def _run():
        try:
            result = await asyncio.to_thread(
                pipeline.run,
                req.audio_name,
                req.excerpt_s if req.excerpt_s > 0 else None,
                status_callback=status_callback,
            )
            storage.save(experiment_id, result)
            _status[experiment_id].update({
                "status": "done",
                "phase": "done",
                "progress": 1.0,
                "fps": result.fps,
            })
        except Exception as e:
            _status[experiment_id].update({
                "status": "error",
                "phase": "error",
                "error": str(e),
            })

    asyncio.create_task(_run())

    return {"experiment_id": experiment_id}


# ---------------------------------------------------------------------------
# Status
# ---------------------------------------------------------------------------

@router.get("/status/{experiment_id}")
async def get_status(experiment_id: str):
    """Poll pipeline progress."""
    if experiment_id in _status:
        return _status[experiment_id]

    # Check if experiment exists on disk (completed in a previous session)
    if storage.exists(experiment_id):
        meta = storage.get_meta(experiment_id)
        return {
            "status": "done",
            "phase": "done",
            "progress": 1.0,
            "fps": meta.get("fps", 0.0),
            "audio_name": meta.get("audio_name", ""),
        }

    raise HTTPException(status_code=404, detail=f"Unknown experiment: {experiment_id}")


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

def _require_experiment(experiment_id: str):
    if not storage.exists(experiment_id):
        raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment_id}")


@router.get("/results/{experiment_id}/summary")
async def get_summary(experiment_id: str):
    """Return experiment metadata as JSON."""
    _require_experiment(experiment_id)
    return storage.get_meta(experiment_id)


@router.get("/results/{experiment_id}/r3")
async def get_r3(experiment_id: str):
    """Return R³ features as binary Float32 (T × 97)."""
    _require_experiment(experiment_id)
    data = storage.load_dataset(experiment_id, "r3")
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
    )


@router.get("/results/{experiment_id}/h3")
async def get_h3(experiment_id: str):
    """Return H³ data as binary: Int32 header (N×4) + Float32 data (N×T).

    Frontend reads Int32 first (N×4 tuples), then Float32 (N×T values).
    Header ``X-H3-Count`` indicates N (number of tuples).
    """
    _require_experiment(experiment_id)
    tuples = storage.load_dataset(experiment_id, "h3/tuples")  # (N, 4) int32
    data = storage.load_dataset(experiment_id, "h3/data")      # (N, T) float32

    buf = tuples.astype(np.int32).tobytes() + data.astype(np.float32).tobytes()
    return Response(
        content=buf,
        media_type="application/octet-stream",
        headers={"X-H3-Count": str(tuples.shape[0])},
    )


@router.get("/results/{experiment_id}/h3/registry")
async def get_h3_registry(experiment_id: str):
    """Return just the H³ tuple addresses (N×4) as Int32 binary."""
    _require_experiment(experiment_id)
    tuples = storage.load_dataset(experiment_id, "h3/tuples")  # (N, 4) int32
    return Response(
        content=tuples.astype(np.int32).tobytes(),
        media_type="application/octet-stream",
        headers={"X-H3-Count": str(tuples.shape[0])},
    )


@router.get("/results/{experiment_id}/h3/select")
async def get_h3_select(
    experiment_id: str,
    indices: str = Query(..., description="Comma-separated row indices into h3/tuples"),
):
    """Return selected H³ tuple data rows as Float32 (K×T).

    Only fetches the requested rows, keeping wire size small.
    """
    _require_experiment(experiment_id)
    idx_list = [int(i) for i in indices.split(",") if i.strip()]
    if not idx_list:
        raise HTTPException(status_code=400, detail="No indices provided")

    data = storage.load_dataset(experiment_id, "h3/data")  # (N, T) float32
    n_tuples = data.shape[0]
    for idx in idx_list:
        if idx < 0 or idx >= n_tuples:
            raise HTTPException(status_code=400, detail=f"Index {idx} out of range [0, {n_tuples})")

    selected = data[idx_list, :]  # (K, T)
    return Response(
        content=selected.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={
            "X-H3-Count": str(len(idx_list)),
            "X-H3-Frames": str(data.shape[1]),
        },
    )


@router.get("/results/{experiment_id}/c3/beliefs")
async def get_beliefs(experiment_id: str):
    """Return C³ beliefs tensor as binary Float32 (T × N_ext)."""
    _require_experiment(experiment_id)
    data = storage.load_dataset(experiment_id, "c3/beliefs")
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
    )


@router.get("/results/{experiment_id}/c3/relays/{relay_name}")
async def get_relay(experiment_id: str, relay_name: str):
    """Return relay output as binary Float32 (T × D), with X-Relay-Dim header."""
    _require_experiment(experiment_id)
    try:
        data = storage.load_dataset(experiment_id, f"c3/relays/{relay_name}")
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Relay '{relay_name}' not found")

    dim = data.shape[1] if data.ndim > 1 else 1
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={"X-Relay-Dim": str(dim)},
    )


@router.get("/results/{experiment_id}/c3/ram")
async def get_ram(experiment_id: str):
    """Return RAM as binary Float32 (T × 26)."""
    _require_experiment(experiment_id)
    data = storage.load_dataset(experiment_id, "c3/ram")
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
    )


@router.get("/results/{experiment_id}/c3/reward")
async def get_reward(experiment_id: str):
    """Return reward signal as binary Float32 (T,)."""
    _require_experiment(experiment_id)
    data = storage.load_dataset(experiment_id, "c3/reward")
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
    )


@router.get("/results/{experiment_id}/c3/neuro")
async def get_neuro(experiment_id: str):
    """Return neurochemical state as binary Float32 (T × 4)."""
    _require_experiment(experiment_id)
    data = storage.load_dataset(experiment_id, "c3/neuro")
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
    )


@router.get("/results/{experiment_id}/c3/salience")
async def get_salience(experiment_id: str):
    """Return salience signal as binary Float32 (T,).

    Computed as mean of RAM across 26 regions.
    """
    _require_experiment(experiment_id)
    ram = storage.load_dataset(experiment_id, "c3/ram")  # (T, 26)
    salience = ram.mean(axis=1).astype(np.float32)
    return Response(
        content=salience.tobytes(),
        media_type="application/octet-stream",
    )


@router.get("/results/{experiment_id}/c3/psi")
async def get_psi(experiment_id: str):
    """Return Ψ³ cognitive state as JSON with 6 domains."""
    _require_experiment(experiment_id)

    domains = {}
    for domain in ("affect", "emotion", "aesthetic", "bodily", "cognitive", "temporal"):
        try:
            data = storage.load_dataset(experiment_id, f"c3/psi/{domain}")
            domains[domain] = {
                "shape": list(data.shape),
                "data": data.tolist(),
            }
        except KeyError:
            domains[domain] = None

    return domains
