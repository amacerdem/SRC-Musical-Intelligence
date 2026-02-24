"""Experiments router — list and delete experiments."""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from .. import storage

router = APIRouter(tags=["experiments"])


@router.get("/list")
async def list_experiments():
    """List all stored experiments with metadata."""
    return storage.list_experiments()


@router.delete("/{experiment_id}")
async def delete_experiment(experiment_id: str):
    """Delete an experiment and its HDF5 file."""
    if not storage.delete(experiment_id):
        raise HTTPException(status_code=404, detail=f"Experiment not found: {experiment_id}")
    return {"status": "deleted", "experiment_id": experiment_id}
