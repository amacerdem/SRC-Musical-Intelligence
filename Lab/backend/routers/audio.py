"""Audio API routes — list, stream, waveform, spectrogram."""

import io
import struct

import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse, Response

from config import AUDIO_DIR
from services.audio_service import (
    list_audio_files,
    load_audio,
    compute_waveform_envelope,
    compute_mel_spectrogram,
)

router = APIRouter()

# In-memory cache for loaded audio (avoids reloading on every request)
_audio_cache: dict[str, tuple[np.ndarray, int]] = {}


def _get_audio(filename: str) -> tuple[np.ndarray, int]:
    """Load audio with caching."""
    if filename not in _audio_cache:
        _audio_cache[filename] = load_audio(filename)
    return _audio_cache[filename]


def _find_file(name: str) -> str:
    """Find actual filename from stem or full name."""
    for f in AUDIO_DIR.iterdir():
        if f.stem == name or f.name == name:
            return f.name
    raise HTTPException(status_code=404, detail=f"Audio file not found: {name}")


@router.get("/list")
async def audio_list():
    """List all available audio files."""
    return list_audio_files()


@router.get("/stream/{name:path}")
async def audio_stream(name: str):
    """Stream audio file as WAV."""
    filename = _find_file(name)
    path = AUDIO_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    def iterfile():
        with open(path, "rb") as f:
            while chunk := f.read(65536):
                yield chunk

    media_type = "audio/wav" if path.suffix == ".wav" else f"audio/{path.suffix[1:]}"
    return StreamingResponse(iterfile(), media_type=media_type)


@router.get("/waveform/{name:path}")
async def audio_waveform(name: str, points: int = 4000):
    """Get downsampled waveform envelope for visualization."""
    filename = _find_file(name)
    samples, sr = _get_audio(filename)
    envelope = compute_waveform_envelope(samples, target_points=points)
    # Return as binary float32
    return Response(
        content=envelope.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={
            "X-Sample-Rate": str(sr),
            "X-Total-Samples": str(len(samples)),
            "X-Envelope-Points": str(len(envelope)),
            "X-Duration": str(round(len(samples) / sr, 3)),
        },
    )


@router.get("/spectrogram/{name:path}")
async def audio_spectrogram(name: str):
    """Get mel spectrogram as binary float32 (n_mels × T)."""
    filename = _find_file(name)
    samples, sr = _get_audio(filename)
    mel = compute_mel_spectrogram(samples)
    n_mels, n_frames = mel.shape
    # Return as binary with shape header
    return Response(
        content=mel.astype(np.float32).tobytes(),
        media_type="application/octet-stream",
        headers={
            "X-N-Mels": str(n_mels),
            "X-N-Frames": str(n_frames),
            "X-Sample-Rate": str(sr),
            "X-Duration": str(round(len(samples) / sr, 3)),
        },
    )
