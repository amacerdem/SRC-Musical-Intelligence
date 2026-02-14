"""MIDataset -- Dataset of pre-computed MI Teacher labels.

Pre-computation is critical because H3 extraction is slow (~146s for 30s audio).
Labels are stored in HDF5 files with keys: mel, r3, h3_dense, c3.

Each sample returns a fixed-length segment with a random temporal offset
for data augmentation during training.

Usage::

    dataset = MIDataset(
        data_dir="/path/to/precomputed",
        segment_frames=2048,
        split="train",
    )
    sample = dataset[0]
    # sample["mel"]:      (T, 128)
    # sample["r3"]:       (T, 128)
    # sample["h3_dense"]: (T, N)
    # sample["c3"]:       (T, 1006)
"""
from __future__ import annotations

import random
from pathlib import Path
from typing import Dict, List, Optional

import torch
from torch import Tensor
from torch.utils.data import Dataset

from Musical_Intelligence.training.model.mi_space_layout import (
    C3_DIM,
    COCHLEA_DIM,
    R3_DIM,
)


class MIDataset(Dataset):
    """Dataset of pre-computed MI Teacher labels in HDF5 format.

    Each HDF5 file contains:
        - ``mel``:      ``(T, 128)`` float32
        - ``r3``:       ``(T, 128)`` float32
        - ``h3_dense``: ``(T, N)``   float32
        - ``c3``:       ``(T, 1006)`` float32

    At training time, returns fixed-length segments (default 2048 frames
    ~ 12 seconds) with a random temporal offset.
    """

    def __init__(
        self,
        data_dir: str,
        segment_frames: int = 2048,
        split: str = "train",
        file_extension: str = ".h5",
    ) -> None:
        self._data_dir = Path(data_dir)
        self._segment_frames = segment_frames
        self._split = split

        # Discover HDF5 files
        split_dir = self._data_dir / split
        if not split_dir.exists():
            split_dir = self._data_dir

        self._files: List[Path] = sorted(
            split_dir.glob(f"*{file_extension}")
        )

        if not self._files:
            raise FileNotFoundError(
                f"No {file_extension} files found in {split_dir}"
            )

    def __len__(self) -> int:
        return len(self._files)

    def __getitem__(self, idx: int) -> Dict[str, Tensor]:
        """Load a segment from the pre-computed labels.

        Returns a dict with keys: mel, r3, h3_dense, c3.
        Each value is a tensor of shape ``(segment_frames, dim)``.
        """
        import h5py

        path = self._files[idx]

        with h5py.File(path, "r") as f:
            total_frames = f["mel"].shape[0]

            # Random offset for augmentation (train), start for eval
            if self._split == "train" and total_frames > self._segment_frames:
                offset = random.randint(0, total_frames - self._segment_frames)
            else:
                offset = 0

            end = min(offset + self._segment_frames, total_frames)

            mel = torch.from_numpy(f["mel"][offset:end])
            r3 = torch.from_numpy(f["r3"][offset:end])
            h3_dense = torch.from_numpy(f["h3_dense"][offset:end])
            c3 = torch.from_numpy(f["c3"][offset:end])

        return {
            "mel": mel,
            "r3": r3,
            "h3_dense": h3_dense,
            "c3": c3,
        }

    # ------------------------------------------------------------------
    # Info
    # ------------------------------------------------------------------

    @property
    def n_files(self) -> int:
        """Number of pre-computed files."""
        return len(self._files)

    def __repr__(self) -> str:
        return (
            f"MIDataset(split={self._split!r}, "
            f"n_files={self.n_files}, "
            f"segment_frames={self._segment_frames})"
        )
