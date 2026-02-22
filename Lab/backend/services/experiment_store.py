"""Experiment storage — read HDF5 results and metadata."""

import json
from pathlib import Path

import h5py
import numpy as np

from config import EXPERIMENTS_DIR


def list_experiments() -> list[dict]:
    """List all saved experiments."""
    experiments = []
    for json_file in sorted(EXPERIMENTS_DIR.glob("*.json"), reverse=True):
        try:
            meta = json.loads(json_file.read_text())
            experiments.append(meta)
        except Exception:
            pass
    return experiments


def get_experiment_meta(experiment_id: str) -> dict | None:
    """Get metadata for a specific experiment."""
    path = EXPERIMENTS_DIR / f"{experiment_id}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())


def get_r3_features(experiment_id: str) -> tuple[np.ndarray, list[str]]:
    """Load R³ features. Returns (T × 97 float32, feature_names)."""
    path = EXPERIMENTS_DIR / f"{experiment_id}.h5"
    with h5py.File(path, "r") as f:
        features = f["r3/features"][:]
        names = [n.decode() if isinstance(n, bytes) else n for n in f["r3/feature_names"][:]]
    return features, names


def get_h3_features(experiment_id: str) -> tuple[np.ndarray, np.ndarray]:
    """Load H³ features. Returns (tuples: N×4 int32, values: N×T float32)."""
    path = EXPERIMENTS_DIR / f"{experiment_id}.h5"
    with h5py.File(path, "r") as f:
        if "h3/tuples" not in f:
            return np.zeros((0, 4), dtype=np.int32), np.zeros((0, 0), dtype=np.float32)
        tuples = f["h3/tuples"][:]
        values = f["h3/values"][:]
    return tuples, values


def get_relay_data(experiment_id: str, relay_name: str) -> np.ndarray | None:
    """Load relay output. Returns (T × D float32) or None."""
    path = EXPERIMENTS_DIR / f"{experiment_id}.h5"
    with h5py.File(path, "r") as f:
        key = f"c3/relays/{relay_name.lower()}"
        if key not in f:
            return None
        return f[key][:]


def get_ram(experiment_id: str) -> np.ndarray | None:
    """Load RAM. Returns (T × 26 float32) or None."""
    path = EXPERIMENTS_DIR / f"{experiment_id}.h5"
    with h5py.File(path, "r") as f:
        if "c3/ram" not in f:
            return None
        return f["c3/ram"][:]


def get_neuro(experiment_id: str) -> np.ndarray | None:
    """Load neuro. Returns (T × 4 float32) or None."""
    path = EXPERIMENTS_DIR / f"{experiment_id}.h5"
    with h5py.File(path, "r") as f:
        if "c3/neuro" not in f:
            return None
        return f["c3/neuro"][:]


def get_reward(experiment_id: str) -> np.ndarray | None:
    """Load reward. Returns (T,) float32 or None."""
    path = EXPERIMENTS_DIR / f"{experiment_id}.h5"
    with h5py.File(path, "r") as f:
        if "c3/reward" not in f:
            return None
        return f["c3/reward"][:]


def get_beliefs(experiment_id: str) -> tuple[np.ndarray, list[str]] | None:
    """Load beliefs observed. Returns (T × N float32, names) or None."""
    path = EXPERIMENTS_DIR / f"{experiment_id}.h5"
    with h5py.File(path, "r") as f:
        if "c3/beliefs/observed" not in f:
            return None
        observed = f["c3/beliefs/observed"][:]
        names = [n.decode() if isinstance(n, bytes) else n for n in f["c3/beliefs/names"][:]]
    return observed, names


def delete_experiment(experiment_id: str) -> bool:
    """Delete experiment files."""
    h5_path = EXPERIMENTS_DIR / f"{experiment_id}.h5"
    json_path = EXPERIMENTS_DIR / f"{experiment_id}.json"
    deleted = False
    for p in [h5_path, json_path]:
        if p.exists():
            p.unlink()
            deleted = True
    return deleted
