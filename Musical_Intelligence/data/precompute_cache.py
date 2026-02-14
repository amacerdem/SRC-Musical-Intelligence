"""PrecomputeCache -- Manages cached pre-computed MI Teacher labels.

Provides save/load utilities for HDF5-based label caches, including
integrity checking and metadata tracking.

Usage::

    cache = PrecomputeCache("/path/to/cache")
    cache.save("track_001", mel, r3, h3_dense, c3)
    data = cache.load("track_001")
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Optional

import torch
from torch import Tensor


class PrecomputeCache:
    """Manages HDF5-based cache of pre-computed MI Teacher labels.

    Each audio track is stored as a separate HDF5 file with datasets:
    ``mel``, ``r3``, ``h3_dense``, ``c3``.

    A ``manifest.json`` file tracks metadata for all cached tracks.
    """

    def __init__(self, cache_dir: str) -> None:
        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._manifest_path = self._cache_dir / "manifest.json"
        self._manifest = self._load_manifest()

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    def save(
        self,
        track_id: str,
        mel: Tensor,
        r3: Tensor,
        h3_dense: Tensor,
        c3: Tensor,
        metadata: Optional[Dict] = None,
    ) -> Path:
        """Save pre-computed labels for a track.

        Parameters
        ----------
        track_id : str
            Unique identifier for the track.
        mel : Tensor
            Shape ``(T, 128)`` mel spectrogram.
        r3 : Tensor
            Shape ``(T, 128)`` R3 features.
        h3_dense : Tensor
            Shape ``(T, N)`` dense H3 features.
        c3 : Tensor
            Shape ``(T, 1006)`` C3 features.
        metadata : dict, optional
            Additional metadata (duration, source, etc.).

        Returns
        -------
        Path
            Path to the saved HDF5 file.
        """
        import h5py

        path = self._cache_dir / f"{track_id}.h5"

        with h5py.File(path, "w") as f:
            f.create_dataset("mel", data=mel.cpu().numpy(), compression="gzip")
            f.create_dataset("r3", data=r3.cpu().numpy(), compression="gzip")
            f.create_dataset(
                "h3_dense", data=h3_dense.cpu().numpy(), compression="gzip"
            )
            f.create_dataset("c3", data=c3.cpu().numpy(), compression="gzip")

        # Update manifest
        self._manifest[track_id] = {
            "n_frames": mel.shape[0],
            "mel_dim": mel.shape[1],
            "r3_dim": r3.shape[1],
            "h3_dim": h3_dense.shape[1],
            "c3_dim": c3.shape[1],
            **(metadata or {}),
        }
        self._save_manifest()

        return path

    # ------------------------------------------------------------------
    # Load
    # ------------------------------------------------------------------

    def load(self, track_id: str) -> Dict[str, Tensor]:
        """Load pre-computed labels for a track.

        Returns dict with keys: mel, r3, h3_dense, c3.
        """
        import h5py

        path = self._cache_dir / f"{track_id}.h5"
        if not path.exists():
            raise FileNotFoundError(f"No cached labels for {track_id!r}")

        with h5py.File(path, "r") as f:
            return {
                "mel": torch.from_numpy(f["mel"][...]),
                "r3": torch.from_numpy(f["r3"][...]),
                "h3_dense": torch.from_numpy(f["h3_dense"][...]),
                "c3": torch.from_numpy(f["c3"][...]),
            }

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def has(self, track_id: str) -> bool:
        """Check if a track has been pre-computed."""
        return (self._cache_dir / f"{track_id}.h5").exists()

    @property
    def track_ids(self):
        """List of all cached track IDs."""
        return list(self._manifest.keys())

    @property
    def n_tracks(self) -> int:
        """Number of cached tracks."""
        return len(self._manifest)

    # ------------------------------------------------------------------
    # Manifest I/O
    # ------------------------------------------------------------------

    def _load_manifest(self) -> Dict:
        if self._manifest_path.exists():
            return json.loads(self._manifest_path.read_text())
        return {}

    def _save_manifest(self) -> None:
        self._manifest_path.write_text(
            json.dumps(self._manifest, indent=2, sort_keys=True)
        )

    def __repr__(self) -> str:
        return f"PrecomputeCache(dir={self._cache_dir}, n_tracks={self.n_tracks})"
