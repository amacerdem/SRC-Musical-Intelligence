"""Upload router — accept audio files for pipeline analysis."""
from __future__ import annotations

import re
import uuid
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from fastapi.responses import JSONResponse

from ..config import AUDIO_DIR, AUDIO_CATALOG

router = APIRouter(tags=["upload"])

ALLOWED_EXTENSIONS = {".wav", ".mp3", ".ogg", ".flac"}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB


def _sanitize_filename(name: str) -> str:
    """Remove unsafe characters, keep extension."""
    stem = Path(name).stem
    ext = Path(name).suffix.lower()
    safe = re.sub(r"[^\w\-.]", "_", stem)
    return f"{safe}_{uuid.uuid4().hex[:8]}{ext}"


@router.post("/upload")
async def upload_audio(request: Request, file: UploadFile = File(...)):
    """Upload an audio file, save to Test-Audio/, and start pipeline.

    Returns ``{ experiment_id, audio_name }`` — poll ``/status/{id}``
    for progress.
    """
    # Validate extension
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format: {ext}. Allowed: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Read and validate size
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="File too large (max 100 MB)")
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Empty file")

    # Save to Test-Audio/
    safe_name = _sanitize_filename(file.filename or "upload.wav")
    dest = AUDIO_DIR / safe_name
    dest.write_bytes(content)

    # Register in catalog (temporary — lives until server restart)
    catalog_key = f"upload_{Path(safe_name).stem}"
    AUDIO_CATALOG[catalog_key] = safe_name

    # Trigger pipeline run via the pipeline router's internal mechanism
    from .pipeline import _status
    from datetime import datetime
    import asyncio

    experiment_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    _status[experiment_id] = {
        "status": "running",
        "phase": "queued",
        "progress": 0.0,
        "fps": 0.0,
        "audio_name": catalog_key,
    }

    pipeline = request.app.state.pipeline

    def status_callback(phase: str, progress: float):
        _status[experiment_id]["phase"] = phase
        _status[experiment_id]["progress"] = progress

    async def _run():
        try:
            result = await asyncio.to_thread(
                pipeline.run, catalog_key, excerpt_s=0.0, callback=status_callback
            )
            from .. import storage
            storage.save(experiment_id, result)
            _status[experiment_id]["status"] = "done"
            _status[experiment_id]["progress"] = 100.0
        except Exception as exc:
            _status[experiment_id]["status"] = "error"
            _status[experiment_id]["error"] = str(exc)

    asyncio.create_task(_run())

    return JSONResponse({
        "experiment_id": experiment_id,
        "audio_name": catalog_key,
        "filename": safe_name,
    })
