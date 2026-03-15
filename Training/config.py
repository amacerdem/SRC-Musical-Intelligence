"""Training configuration — all hyperparameters in one place.

Usage:
    from Training.config import TrainConfig
    cfg = TrainConfig()                    # defaults
    cfg = TrainConfig(batch_size=2048)     # override
    cfg = TrainConfig.from_json("path")    # load from file
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Dict, Optional


@dataclass
class TrainConfig:
    """All training hyperparameters."""

    # ── Data ──
    data_dir: str = ""
    chunk_size: int = 512
    val_fraction: float = 0.1
    seed: int = 42

    # ── Model ──
    n_h3: int = 637                    # H³ output dim (auto-detected from data if 0)
    r3_hidden: int = 256               # R³Head conv channels
    h3_d_model: int = 256              # H³Head transformer width
    h3_n_heads: int = 4                # H³Head attention heads
    h3_n_layers: int = 2               # H³Head transformer layers
    h3_max_len: int = 8192             # max sequence length
    belief_hidden: int = 512           # BeliefHead first conv channels

    # ── Optimization ──
    epochs: int = 50
    batch_size: int = 256
    lr: float = 1e-3
    weight_decay: float = 1e-4
    grad_clip: float = 1.0
    scheduler: str = "cosine"          # "cosine" | "plateau" | "none"
    warmup_epochs: int = 0

    # ── Loss weights (cascade) ──
    w_r3: float = 1.0
    w_h3: float = 1.5                  # H³ is critical bridge
    w_beliefs: float = 2.0             # beliefs are the hardest
    w_dims: float = 1.0                # 5+5 end target

    # ── Augmentation ──
    aug_time_mask: bool = False        # random time masking
    aug_time_mask_max: int = 50        # max frames to mask
    aug_freq_mask: bool = False        # random freq masking
    aug_freq_mask_max: int = 10        # max mel bins to mask
    aug_noise: float = 0.0             # additive gaussian noise std

    # ── Logging ──
    output_dir: str = ""
    log_every: int = 1                 # epochs between console logs
    detail_every: int = 5              # epochs between per-dim detail
    checkpoint_every: int = 10         # epochs between snapshots
    save_optimizer: bool = False       # save optimizer state in checkpoints

    # ── Early stopping ──
    patience: int = 0                  # 0 = disabled
    min_delta: float = 1e-5

    @property
    def loss_weights(self) -> Dict[str, float]:
        return {"r3": self.w_r3, "h3": self.w_h3, "beliefs": self.w_beliefs, "dims": self.w_dims}

    def to_json(self, path: str | Path) -> None:
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2)

    @classmethod
    def from_json(cls, path: str | Path) -> "TrainConfig":
        with open(path) as f:
            data = json.load(f)
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def __post_init__(self):
        if self.output_dir == "":
            self.output_dir = str(Path(__file__).resolve().parent / "runs" / "default")
