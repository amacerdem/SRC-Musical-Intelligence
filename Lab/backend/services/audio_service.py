"""Audio loading, waveform extraction, and spectrogram computation."""

import numpy as np
import torch
import torchaudio
from pathlib import Path

from config import AUDIO_DIR, SAMPLE_RATE, HOP_LENGTH, N_MELS


def list_audio_files() -> list[dict]:
    """List all audio files in Test-Audio directory."""
    extensions = {".wav", ".mp3", ".flac"}
    files = []
    for f in sorted(AUDIO_DIR.iterdir()):
        if f.suffix.lower() in extensions and not f.name.startswith("."):
            info = torchaudio.info(str(f))
            duration = info.num_frames / info.sample_rate
            files.append({
                "name": f.stem,
                "filename": f.name,
                "duration": round(duration, 2),
                "sample_rate": info.sample_rate,
                "channels": info.num_channels,
            })
    return files


def load_audio(filename: str) -> tuple[np.ndarray, int]:
    """Load audio file, return (samples, sr). Mono, resampled to 44100."""
    path = AUDIO_DIR / filename
    waveform, sr = torchaudio.load(str(path))
    # Mono
    if waveform.shape[0] > 1:
        waveform = waveform.mean(dim=0, keepdim=True)
    # Resample
    if sr != SAMPLE_RATE:
        resampler = torchaudio.transforms.Resample(sr, SAMPLE_RATE)
        waveform = resampler(waveform)
    return waveform.squeeze(0).numpy(), SAMPLE_RATE


def compute_waveform_envelope(samples: np.ndarray, target_points: int = 4000) -> np.ndarray:
    """Downsample waveform to target_points for visualization (min/max envelope)."""
    n = len(samples)
    if n <= target_points * 2:
        return samples
    chunk_size = n // target_points
    trimmed = samples[:chunk_size * target_points]
    chunks = trimmed.reshape(target_points, chunk_size)
    mins = chunks.min(axis=1)
    maxs = chunks.max(axis=1)
    # Interleave min/max for envelope
    envelope = np.empty(target_points * 2, dtype=np.float32)
    envelope[0::2] = mins
    envelope[1::2] = maxs
    return envelope


def compute_mel_spectrogram(samples: np.ndarray) -> np.ndarray:
    """Compute log-mel spectrogram. Returns (n_mels, T) float32."""
    waveform = torch.from_numpy(samples).unsqueeze(0)
    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=2048,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
    )
    mel = mel_transform(waveform)  # (1, n_mels, T)
    mel_db = torchaudio.transforms.AmplitudeToDB()(mel)
    return mel_db.squeeze(0).numpy()  # (n_mels, T)
