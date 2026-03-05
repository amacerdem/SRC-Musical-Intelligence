"""Extract MI features resampled to fMRI TR resolution."""
from __future__ import annotations

import gc
from pathlib import Path
from typing import Dict

import numpy as np

from Validation.infrastructure.alignment import apply_hrf, resample_to_tr
from Validation.infrastructure.mi_bridge import MIBridge

# Max seconds per MI chunk — 300s preserves H³ temporal state across long spans
_MAX_CHUNK_S = 300.0


def _clear_gpu_cache() -> None:
    """Release GPU memory (CUDA or MPS)."""
    try:
        import torch
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        if hasattr(torch, "mps") and torch.backends.mps.is_available():
            torch.mps.empty_cache()
    except Exception:
        pass


def extract_features_for_fmri(
    bridge: MIBridge,
    audio_path: Path,
    tr: float = 2.0,
    excerpt_s: float = 300.0,
) -> Dict[str, np.ndarray]:
    """Run MI and resample features to fMRI TR, with HRF convolution.

    Processes audio in chunks of _MAX_CHUNK_S seconds to avoid GPU OOM
    on long fMRI scans, then concatenates before resampling.

    Args:
        bridge: MI pipeline bridge.
        audio_path: Stimulus audio path.
        tr: fMRI repetition time.
        excerpt_s: Max duration.

    Returns:
        Dict with HRF-convolved features at TR resolution:
        - 'r3': (T, 97)
        - 'beliefs': (T, 131)
        - 'ram': (T, 26)
        - 'neuro': (T, 4)
        - 'full': (T, 258)
    """
    # Process in chunks to avoid GPU OOM on long audio
    if excerpt_s > _MAX_CHUNK_S:
        return _extract_chunked(bridge, audio_path, tr, excerpt_s)

    _clear_gpu_cache()
    result = bridge.run(audio_path, excerpt_s=excerpt_s)

    features = {}

    # Resample to TR, then convolve with HRF
    for name, data in [
        ("r3", result.r3),
        ("beliefs", result.beliefs),
        ("ram", result.ram),
        ("neuro", result.neuro),
    ]:
        resampled = resample_to_tr(data, tr_seconds=tr)
        features[name] = apply_hrf(resampled, tr=tr)

    # Full concatenated
    full = np.concatenate([result.r3, result.beliefs, result.ram, result.neuro], axis=1)
    full_resampled = resample_to_tr(full, tr_seconds=tr)
    features["full"] = apply_hrf(full_resampled, tr=tr)

    return features


def _extract_chunked(
    bridge: MIBridge,
    audio_path: Path,
    tr: float,
    total_s: float,
) -> Dict[str, np.ndarray]:
    """Process long audio in chunks, concatenate, then resample+HRF."""
    import soundfile as sf
    import tempfile

    data, sr = sf.read(str(audio_path), dtype="float32")
    if data.ndim == 2:
        data = data.mean(axis=1)

    chunk_samples = int(_MAX_CHUNK_S * sr)
    total_samples = min(len(data), int(total_s * sr))
    data = data[:total_samples]

    accum = {"r3": [], "beliefs": [], "ram": [], "neuro": []}
    tmp_dir = Path(tempfile.mkdtemp())

    for start in range(0, total_samples, chunk_samples):
        end = min(start + chunk_samples, total_samples)
        chunk = data[start:end]
        chunk_path = tmp_dir / f"chunk_{start}.wav"
        sf.write(str(chunk_path), chunk, sr)

        _clear_gpu_cache()
        gc.collect()

        result = bridge.run(chunk_path, excerpt_s=_MAX_CHUNK_S)
        accum["r3"].append(result.r3)
        accum["beliefs"].append(result.beliefs)
        accum["ram"].append(result.ram)
        accum["neuro"].append(result.neuro)

        chunk_path.unlink(missing_ok=True)

    # Concatenate chunks along time axis
    features = {}
    concat = {}
    for name in ("r3", "beliefs", "ram", "neuro"):
        concat[name] = np.concatenate(accum[name], axis=0)
        resampled = resample_to_tr(concat[name], tr_seconds=tr)
        features[name] = apply_hrf(resampled, tr=tr)

    full = np.concatenate(
        [concat["r3"], concat["beliefs"], concat["ram"], concat["neuro"]], axis=1
    )
    full_resampled = resample_to_tr(full, tr_seconds=tr)
    features["full"] = apply_hrf(full_resampled, tr=tr)

    # Cleanup
    try:
        tmp_dir.rmdir()
    except OSError:
        pass

    return features
