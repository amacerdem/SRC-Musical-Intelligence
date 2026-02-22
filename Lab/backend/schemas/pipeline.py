"""Pydantic schemas for pipeline execution."""

from pydantic import BaseModel
from typing import Optional


class PipelineRunRequest(BaseModel):
    audio_name: str
    excerpt_start: Optional[float] = None   # seconds
    excerpt_duration: Optional[float] = None  # seconds, None = full


class PipelineRunResponse(BaseModel):
    experiment_id: str
    status: str
    audio_name: str


class PipelineStatus(BaseModel):
    experiment_id: str
    status: str  # "running", "complete", "error"
    phase: Optional[str] = None
    progress: Optional[float] = None
    fps: Optional[float] = None
    error: Optional[str] = None


class ExperimentSummary(BaseModel):
    experiment_id: str
    audio_name: str
    duration: float
    n_frames: int
    fps: float
    reward_mean: float
    reward_positive_pct: float
    kernel_version: str
    timestamp: str
