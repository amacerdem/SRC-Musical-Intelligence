"""Experiment management API — list, get, delete experiments."""

from fastapi import APIRouter, HTTPException

from services import experiment_store

router = APIRouter()


@router.get("/list")
async def experiments_list():
    """List all saved experiments."""
    return experiment_store.list_experiments()


@router.get("/{experiment_id}")
async def experiment_detail(experiment_id: str):
    """Get experiment metadata."""
    meta = experiment_store.get_experiment_meta(experiment_id)
    if meta is None:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return meta


@router.delete("/{experiment_id}")
async def experiment_delete(experiment_id: str):
    """Delete an experiment."""
    deleted = experiment_store.delete_experiment(experiment_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return {"status": "deleted", "experiment_id": experiment_id}
