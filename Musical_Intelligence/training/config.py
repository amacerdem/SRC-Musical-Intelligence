"""Training configuration for BCH learned inverse heads POC.

Usage::

    config = BCHTrainingConfig()
    config = BCHTrainingConfig(epochs=200, batch_size=64)
    config = BCHTrainingConfig.from_cli()  # parse CLI args
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Tuple

from Musical_Intelligence.training.model.mi_space_layout import BCH_MANIFOLD_DIM


@dataclass
class BCHTrainingConfig:
    """All hyperparameters for the BCH inverse heads training run."""

    # ── Data ──────────────────────────────────────────────────
    data_dir: str = "./cache/bch"
    segment_frames: int = 2048          # ~12 seconds at 172 Hz
    batch_size: int = 32
    num_workers: int = 4

    # ── Model ─────────────────────────────────────────────────
    target_dim: int = BCH_MANIFOLD_DIM  # 112 = R³(16) + H³(50) + BCH(16) + RAM(26) + Neuro(4)
    hidden_dim: int = 256
    kernel_sizes: Tuple[int, ...] = (3, 5, 7, 11, 15)

    # ── Training ──────────────────────────────────────────────
    lr: float = 1e-3
    weight_decay: float = 1e-4
    epochs: int = 100
    cycle_loss_weight: float = 0.1
    cycle_loss_start_epoch: int = 50    # enable cycle loss after this epoch

    # ── Hardware ──────────────────────────────────────────────
    device: str = "cuda"
    mixed_precision: bool = True        # fp16 on H200
    compile_model: bool = True          # torch.compile for H200

    # ── Logging & checkpointing ───────────────────────────────
    log_every: int = 10                 # log every N steps
    save_every: int = 10                # save checkpoint every N epochs
    checkpoint_dir: str = "./checkpoints/bch"

    # ── CLI parser ────────────────────────────────────────────

    @classmethod
    def from_cli(cls) -> "BCHTrainingConfig":
        """Parse command-line arguments into a config."""
        parser = argparse.ArgumentParser(
            description="Train BCH learned inverse heads (POC)."
        )
        parser.add_argument("--data-dir", type=str, default=cls.data_dir)
        parser.add_argument("--segment-frames", type=int, default=cls.segment_frames)
        parser.add_argument("--batch-size", type=int, default=cls.batch_size)
        parser.add_argument("--num-workers", type=int, default=cls.num_workers)
        parser.add_argument("--hidden-dim", type=int, default=cls.hidden_dim)
        parser.add_argument("--lr", type=float, default=cls.lr)
        parser.add_argument("--weight-decay", type=float, default=cls.weight_decay)
        parser.add_argument("--epochs", type=int, default=cls.epochs)
        parser.add_argument("--cycle-loss-weight", type=float, default=cls.cycle_loss_weight)
        parser.add_argument("--cycle-loss-start-epoch", type=int, default=cls.cycle_loss_start_epoch)
        parser.add_argument("--device", type=str, default=cls.device)
        parser.add_argument("--no-mixed-precision", action="store_true")
        parser.add_argument("--no-compile", action="store_true")
        parser.add_argument("--log-every", type=int, default=cls.log_every)
        parser.add_argument("--save-every", type=int, default=cls.save_every)
        parser.add_argument("--checkpoint-dir", type=str, default=cls.checkpoint_dir)

        args = parser.parse_args()
        return cls(
            data_dir=args.data_dir,
            segment_frames=args.segment_frames,
            batch_size=args.batch_size,
            num_workers=args.num_workers,
            hidden_dim=args.hidden_dim,
            lr=args.lr,
            weight_decay=args.weight_decay,
            epochs=args.epochs,
            cycle_loss_weight=args.cycle_loss_weight,
            cycle_loss_start_epoch=args.cycle_loss_start_epoch,
            device=args.device,
            mixed_precision=not args.no_mixed_precision,
            compile_model=not args.no_compile,
            log_every=args.log_every,
            save_every=args.save_every,
            checkpoint_dir=args.checkpoint_dir,
        )
