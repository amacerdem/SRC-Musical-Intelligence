"""Pipeline API — run R³→H³→C³, get status & results."""

import threading

import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from schemas.pipeline import PipelineRunRequest, PipelineRunResponse, PipelineStatus
from services.pipeline_runner import run_pipeline, get_status
from services import experiment_store

router = APIRouter()


@router.post("/run")
async def pipeline_run(req: PipelineRunRequest) -> PipelineRunResponse:
    """Start pipeline execution in a background thread."""
    def _run():
        try:
            run_pipeline(req.audio_name, req.excerpt_start, req.excerpt_duration)
        except Exception as e:
            print(f"Pipeline error: {e}")

    # Generate experiment_id and start
    import uuid
    from datetime import datetime
    exp_id = datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + uuid.uuid4().hex[:6]

    # Actually run synchronously for now (async support later via WebSocket)
    try:
        exp_id = run_pipeline(req.audio_name, req.excerpt_start, req.excerpt_duration)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return PipelineRunResponse(
        experiment_id=exp_id,
        status="complete",
        audio_name=req.audio_name,
    )


@router.get("/status/{experiment_id}")
async def pipeline_status(experiment_id: str) -> PipelineStatus:
    """Get pipeline execution status."""
    status = get_status(experiment_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return PipelineStatus(experiment_id=experiment_id, **status)


@router.get("/results/{experiment_id}/summary")
async def results_summary(experiment_id: str):
    """Get experiment summary metadata."""
    meta = experiment_store.get_experiment_meta(experiment_id)
    if meta is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return meta


@router.get("/results/{experiment_id}/r3")
async def results_r3(experiment_id: str):
    """Get R³ features as binary float32 (T × 97)."""
    try:
        features, names = experiment_store.get_r3_features(experiment_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return Response(
        content=features.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={
            "X-N-Frames": str(features.shape[0]),
            "X-N-Features": str(features.shape[1]),
            "X-Feature-Names": ",".join(names),
        },
    )


@router.get("/results/{experiment_id}/h3")
async def results_h3(experiment_id: str):
    """Get H³ features as binary."""
    try:
        tuples, values = experiment_store.get_h3_features(experiment_id)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Experiment not found")
    # Pack: 4 bytes n_tuples, then tuples (N×4 int32), then values (N×T float32)
    n_tuples = tuples.shape[0]
    n_frames = values.shape[1] if values.ndim > 1 else 0
    content = (
        np.array([n_tuples, n_frames], dtype=np.int32).tobytes() +
        tuples.astype(np.int32).tobytes() +
        values.astype(np.float32).tobytes()
    )
    return Response(
        content=content,
        media_type="application/octet-stream",
        headers={"X-N-Tuples": str(n_tuples), "X-N-Frames": str(n_frames)},
    )


@router.get("/results/{experiment_id}/c3/relays/{relay_name}")
async def results_relay(experiment_id: str, relay_name: str):
    """Get relay output as binary float32 (T × D)."""
    data = experiment_store.get_relay_data(experiment_id, relay_name)
    if data is None:
        raise HTTPException(status_code=404, detail=f"Relay {relay_name} not found")
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={"X-N-Frames": str(data.shape[0]), "X-N-Dims": str(data.shape[1] if data.ndim > 1 else 1)},
    )


@router.get("/results/{experiment_id}/c3/ram")
async def results_ram(experiment_id: str):
    """Get RAM (T × 26) as binary float32."""
    data = experiment_store.get_ram(experiment_id)
    if data is None:
        raise HTTPException(status_code=404, detail="RAM not found")
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={"X-N-Frames": str(data.shape[0]), "X-N-Regions": str(data.shape[1] if data.ndim > 1 else 1)},
    )


@router.get("/results/{experiment_id}/c3/reward")
async def results_reward(experiment_id: str):
    """Get reward signal (T,) as binary float32."""
    data = experiment_store.get_reward(experiment_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Reward not found")
    return Response(
        content=data.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={"X-N-Frames": str(data.shape[0])},
    )


@router.get("/results/{experiment_id}/c3/beliefs")
async def results_beliefs(experiment_id: str):
    """Get beliefs observed (T × N) as binary float32."""
    result = experiment_store.get_beliefs(experiment_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Beliefs not found")
    observed, names = result
    return Response(
        content=observed.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={
            "X-N-Frames": str(observed.shape[0]),
            "X-N-Beliefs": str(observed.shape[1]),
            "X-Belief-Names": ",".join(names),
        },
    )
