"""HDF5-based result caching — avoid re-running MI pipeline for same audio."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Dict, Optional

import h5py
import numpy as np

from Validation.config.paths import RESULTS


class ResultCache:
    """Cache MI pipeline results in HDF5 format.

    Keys are derived from audio file path + parameters (excerpt_s, neuro_gains).
    Stores numpy arrays and metadata efficiently.
    """

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or RESULTS / ".cache"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _make_key(
        self,
        audio_path: str,
        excerpt_s: float,
        neuro_gains: Optional[Dict[str, float]] = None,
    ) -> str:
        """Generate a deterministic cache key."""
        parts = [str(audio_path), str(excerpt_s)]
        if neuro_gains:
            parts.append(json.dumps(neuro_gains, sort_keys=True))
        raw = "|".join(parts)
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def _cache_path(self, key: str) -> Path:
        return self.cache_dir / f"{key}.h5"

    def has(
        self,
        audio_path: str,
        excerpt_s: float,
        neuro_gains: Optional[Dict[str, float]] = None,
    ) -> bool:
        """Check if a cached result exists."""
        key = self._make_key(audio_path, excerpt_s, neuro_gains)
        return self._cache_path(key).exists()

    def store(
        self,
        audio_path: str,
        excerpt_s: float,
        arrays: Dict[str, np.ndarray],
        metadata: Optional[Dict[str, str]] = None,
        neuro_gains: Optional[Dict[str, float]] = None,
    ) -> Path:
        """Store arrays in HDF5 cache.

        Args:
            audio_path: Source audio path (for key generation).
            excerpt_s: Duration parameter.
            arrays: Dict of name → numpy array to cache.
            metadata: Optional string metadata.
            neuro_gains: Optional neurochemical gains (for key generation).

        Returns:
            Path to cache file.
        """
        key = self._make_key(audio_path, excerpt_s, neuro_gains)
        path = self._cache_path(key)

        with h5py.File(path, "w") as f:
            for name, arr in arrays.items():
                f.create_dataset(name, data=arr, compression="gzip")
            # Store metadata
            f.attrs["audio_path"] = str(audio_path)
            f.attrs["excerpt_s"] = excerpt_s
            if metadata:
                for k, v in metadata.items():
                    f.attrs[k] = v
            if neuro_gains:
                f.attrs["neuro_gains"] = json.dumps(neuro_gains)

        return path

    def load(
        self,
        audio_path: str,
        excerpt_s: float,
        neuro_gains: Optional[Dict[str, float]] = None,
    ) -> Optional[Dict[str, np.ndarray]]:
        """Load cached arrays.

        Returns:
            Dict of name → numpy array, or None if not cached.
        """
        key = self._make_key(audio_path, excerpt_s, neuro_gains)
        path = self._cache_path(key)

        if not path.exists():
            return None

        arrays: Dict[str, np.ndarray] = {}
        with h5py.File(path, "r") as f:
            for name in f.keys():
                arrays[name] = f[name][:]

        return arrays

    def clear(self) -> int:
        """Delete all cached results. Returns number of files removed."""
        count = 0
        for f in self.cache_dir.glob("*.h5"):
            f.unlink()
            count += 1
        return count
