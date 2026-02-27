"""HDF5 experiment storage — save, load, list, delete experiments.

Each experiment is a single HDF5 file at ``experiments/{id}.h5``.

Layout::

    /{id}.h5
    ├── meta          (attrs: audio_name, duration_s, n_frames, fps, timestamp, kernel_version)
    ├── r3            dataset (T, 97) float32
    ├── h3/
    │   ├── tuples    dataset (N, 4) int32
    │   └── data      dataset (N, T) float32
    ├── c3/
    │   ├── beliefs   dataset (T, N_ext) float32
    │   ├── relays/
    │   │   ├── BCH   dataset (T, D) float32
    │   │   └── ...
    │   ├── ram       dataset (T, 26) float32
    │   ├── neuro     dataset (T, 4) float32
    │   ├── reward    dataset (T,) float32
    │   ├── psi/
    │   │   ├── affect    (T, 4)
    │   │   ├── emotion   (T, 7)
    │   │   └── ...
    │   └── dimensions/
    │       ├── dim_6d    (T, 6)   — psychology layer
    │       ├── dim_12d   (T, 12)  — cognition layer
    │       └── dim_24d   (T, 24)  — neuroscience layer
"""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import h5py
import numpy as np

from .config import EXPERIMENTS_DIR


def _ensure_dir() -> Path:
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    return EXPERIMENTS_DIR


def _h5_path(experiment_id: str) -> Path:
    return _ensure_dir() / f"{experiment_id}.h5"


# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------

def save(experiment_id: str, result) -> Path:
    """Save an ExperimentResult to HDF5.

    Args:
        experiment_id: Unique experiment identifier (e.g., ``20260224_143022``).
        result: ``ExperimentResult`` from pipeline.

    Returns:
        Path to the saved HDF5 file.
    """
    path = _h5_path(experiment_id)

    with h5py.File(path, "w") as f:
        # Metadata as root attrs
        f.attrs["audio_name"] = result.audio_name
        f.attrs["duration_s"] = result.duration_s
        f.attrs["n_frames"] = result.n_frames
        f.attrs["fps"] = result.fps
        f.attrs["timestamp"] = datetime.now().isoformat()
        f.attrs["kernel_version"] = "4.0"

        # R³
        f.create_dataset("r3", data=result.r3.astype(np.float32), compression="gzip")

        # H³
        h3g = f.create_group("h3")
        if result.h3_tuples:
            h3g.create_dataset(
                "tuples",
                data=np.array(result.h3_tuples, dtype=np.int32),
                compression="gzip",
            )
            h3g.create_dataset("data", data=result.h3_data.astype(np.float32), compression="gzip")
        else:
            h3g.create_dataset("tuples", data=np.empty((0, 4), dtype=np.int32))
            h3g.create_dataset("data", data=np.empty((0, 0), dtype=np.float32))

        # C³
        c3g = f.create_group("c3")
        c3g.create_dataset("beliefs", data=result.beliefs.astype(np.float32), compression="gzip")

        # Relays
        relays_g = c3g.create_group("relays")
        for name, arr in result.relays.items():
            relays_g.create_dataset(name, data=arr.astype(np.float32), compression="gzip")

        c3g.create_dataset("ram", data=result.ram.astype(np.float32), compression="gzip")
        c3g.create_dataset("neuro", data=result.neuro.astype(np.float32), compression="gzip")
        c3g.create_dataset("reward", data=result.reward.astype(np.float32), compression="gzip")

        # Ψ³
        psi_g = c3g.create_group("psi")
        for domain, arr in result.psi.items():
            psi_g.create_dataset(domain, data=arr.astype(np.float32), compression="gzip")

        # Belief horizon decomposition
        if hasattr(result, "belief_decomposition") and result.belief_decomposition:
            decomp_g = c3g.create_group("belief_decomposition")
            for belief_name, variants in result.belief_decomposition.items():
                bg = decomp_g.create_group(belief_name)
                for variant_name, trace in variants.items():
                    bg.create_dataset(
                        variant_name,
                        data=trace.astype(np.float32),
                        compression="gzip",
                    )

        # Hierarchical dimensions (6D/12D/24D)
        if hasattr(result, "dim_6d") and result.dim_6d.size > 0:
            dim_g = c3g.create_group("dimensions")
            dim_g.create_dataset("dim_6d", data=result.dim_6d.astype(np.float32), compression="gzip")
            dim_g.create_dataset("dim_12d", data=result.dim_12d.astype(np.float32), compression="gzip")
            dim_g.create_dataset("dim_24d", data=result.dim_24d.astype(np.float32), compression="gzip")

    return path


# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------

def load_dataset(experiment_id: str, dataset_path: str) -> np.ndarray:
    """Load a single dataset from an experiment HDF5 file.

    Args:
        experiment_id: Experiment ID.
        dataset_path: HDF5 internal path (e.g., ``"r3"``, ``"c3/beliefs"``,
            ``"c3/relays/BCH"``).

    Returns:
        numpy array with the dataset contents.

    Raises:
        FileNotFoundError: If experiment does not exist.
        KeyError: If dataset path does not exist in the file.
    """
    path = _h5_path(experiment_id)
    if not path.exists():
        raise FileNotFoundError(f"Experiment not found: {experiment_id}")

    with h5py.File(path, "r") as f:
        if dataset_path not in f:
            raise KeyError(f"Dataset '{dataset_path}' not found in {experiment_id}")
        return f[dataset_path][:]


def get_meta(experiment_id: str) -> Dict[str, Any]:
    """Load experiment metadata (root attrs).

    Returns:
        Dict with keys: audio_name, duration_s, n_frames, fps, timestamp,
        kernel_version, plus relay_names.
    """
    path = _h5_path(experiment_id)
    if not path.exists():
        raise FileNotFoundError(f"Experiment not found: {experiment_id}")

    with h5py.File(path, "r") as f:
        meta = dict(f.attrs)
        # Convert numpy types to Python native
        for k, v in meta.items():
            if isinstance(v, (np.integer,)):
                meta[k] = int(v)
            elif isinstance(v, (np.floating,)):
                meta[k] = float(v)

        # Add relay names
        if "c3/relays" in f:
            meta["relay_names"] = list(f["c3/relays"].keys())
        else:
            meta["relay_names"] = []

        # Add beliefs dim
        if "c3/beliefs" in f:
            meta["beliefs_shape"] = list(f["c3/beliefs"].shape)

    meta["experiment_id"] = experiment_id
    return meta


def get_relay_dim(experiment_id: str, relay_name: str) -> int:
    """Get the output dimension of a relay dataset."""
    path = _h5_path(experiment_id)
    if not path.exists():
        raise FileNotFoundError(f"Experiment not found: {experiment_id}")

    with h5py.File(path, "r") as f:
        ds_path = f"c3/relays/{relay_name}"
        if ds_path not in f:
            raise KeyError(f"Relay '{relay_name}' not found in {experiment_id}")
        shape = f[ds_path].shape
        return shape[1] if len(shape) > 1 else 1


# ---------------------------------------------------------------------------
# List & delete
# ---------------------------------------------------------------------------

def list_experiments() -> List[Dict[str, Any]]:
    """List all experiments with metadata."""
    _ensure_dir()
    experiments = []
    for h5_file in sorted(EXPERIMENTS_DIR.glob("*.h5")):
        eid = h5_file.stem
        try:
            meta = get_meta(eid)
            experiments.append(meta)
        except Exception:
            experiments.append({"experiment_id": eid, "error": "corrupt"})
    return experiments


def delete(experiment_id: str) -> bool:
    """Delete an experiment HDF5 file.

    Returns:
        True if deleted, False if not found.
    """
    path = _h5_path(experiment_id)
    if path.exists():
        path.unlink()
        return True
    return False


def exists(experiment_id: str) -> bool:
    """Check if an experiment exists."""
    return _h5_path(experiment_id).exists()
