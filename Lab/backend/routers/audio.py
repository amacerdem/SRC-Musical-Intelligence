"""Audio router — list, stream, waveform, spectrogram endpoints."""
from __future__ import annotations

from pathlib import Path

import numpy as np
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response

from ..config import AUDIO_CATALOG, AUDIO_DIR, HOP_LENGTH, N_FFT, N_MELS, SAMPLE_RATE

router = APIRouter(tags=["audio"])

# In-memory cache for waveforms (loaded on first request)
_waveform_cache: dict[str, np.ndarray] = {}


def _get_filepath(name: str) -> Path:
    if name not in AUDIO_CATALOG:
        raise HTTPException(status_code=404, detail=f"Unknown audio: {name}")
    filepath = AUDIO_DIR / AUDIO_CATALOG[name]
    if not filepath.exists():
        raise HTTPException(status_code=404, detail=f"File not found: {AUDIO_CATALOG[name]}")
    return filepath


def _load_waveform(name: str) -> np.ndarray:
    """Load mono waveform as float32 numpy array, cached."""
    if name in _waveform_cache:
        return _waveform_cache[name]

    import soundfile as sf
    import torchaudio
    import torch

    filepath = _get_filepath(name)
    try:
        data, sr = sf.read(str(filepath), dtype="float32")
        if data.ndim == 2:
            data = data.mean(axis=1)
        waveform = data
    except Exception:
        tensor, sr = torchaudio.load(str(filepath))
        if tensor.shape[0] > 1:
            tensor = tensor.mean(dim=0, keepdim=True)
        waveform = tensor[0].numpy()

    # Resample if needed
    if sr != SAMPLE_RATE:
        tensor = torch.from_numpy(waveform).unsqueeze(0)
        resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
        waveform = resampler(tensor)[0].numpy()

    _waveform_cache[name] = waveform
    return waveform


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/list")
async def list_audio():
    """List available audio files."""
    items = []
    for name, filename in AUDIO_CATALOG.items():
        filepath = AUDIO_DIR / filename
        ext = filepath.suffix.lstrip(".")
        duration_s = None
        if filepath.exists():
            try:
                import soundfile as sf
                info = sf.info(str(filepath))
                duration_s = info.duration
            except Exception:
                pass
        items.append({
            "name": name,
            "filename": filename,
            "format": ext,
            "duration_s": duration_s,
            "available": filepath.exists(),
        })
    return items


@router.get("/stream/{name}")
async def stream_audio(name: str):
    """Stream audio file as WAV/MP3."""
    filepath = _get_filepath(name)
    media_type = "audio/wav" if filepath.suffix == ".wav" else f"audio/{filepath.suffix.lstrip('.')}"
    return FileResponse(str(filepath), media_type=media_type, filename=filepath.name)


@router.get("/waveform/{name}")
async def get_waveform(name: str):
    """Return downsampled waveform envelope as binary Float32.

    Downsamples to ~4000 points for efficient visualization.
    Returns min/max interleaved: [min0, max0, min1, max1, ...] → 8000 floats.
    """
    waveform = _load_waveform(name)
    n_points = 4000
    chunk_size = max(1, len(waveform) // n_points)

    # Trim to exact multiple
    trimmed = waveform[:chunk_size * n_points]
    chunks = trimmed.reshape(n_points, chunk_size)

    mins = chunks.min(axis=1).astype(np.float32)
    maxs = chunks.max(axis=1).astype(np.float32)

    # Interleave min/max
    envelope = np.empty(n_points * 2, dtype=np.float32)
    envelope[0::2] = mins
    envelope[1::2] = maxs

    return Response(
        content=envelope.tobytes(),
        media_type="application/octet-stream",
    )


@router.get("/spectrogram/{name}")
async def get_spectrogram(name: str):
    """Return mel spectrogram as binary Float32 (128 × T).

    Row-major: 128 mel bins × T frames, flattened.
    """
    import torch
    import torchaudio

    waveform = _load_waveform(name)
    tensor = torch.from_numpy(waveform).unsqueeze(0)  # (1, N)

    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
        power=2.0,
    )
    mel = mel_transform(tensor)  # (1, 128, T)
    mel = torch.log1p(mel)
    mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
    mel = (mel / mel_max)[0]  # (128, T)

    data = mel.numpy().astype(np.float32)  # Row-major: (128, T)
    return Response(
        content=data.tobytes(),
        media_type="application/octet-stream",
        headers={"X-Mel-Bins": str(data.shape[0]), "X-Frames": str(data.shape[1])},
    )
