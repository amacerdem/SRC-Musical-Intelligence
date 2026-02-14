"""MI-Core Training Script -- Main entry point.

Launches MI-Core bidirectional training with configuration from
YAML files or command-line overrides.

Usage::

    # Default config
    python -m Musical_Intelligence.training.scripts.train

    # Override parameters
    python -m Musical_Intelligence.training.scripts.train \\
        --data_dir /path/to/precomputed \\
        --epochs 600 \\
        --batch_size 8 \\
        --lr 3e-4 \\
        --checkpoint_dir checkpoints/run1

    # Resume from checkpoint
    python -m Musical_Intelligence.training.scripts.train \\
        --resume checkpoints/run1/mi_core_epoch_100.pt
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import numpy as np
import torch
from torch.utils.data import DataLoader

from Musical_Intelligence.data.collator import MICollator
from Musical_Intelligence.data.mi_dataset import MIDataset
from Musical_Intelligence.training.model.mi_core import MICore
from Musical_Intelligence.training.trainer.mi_trainer import MITrainer


def set_seed(seed: int) -> None:
    """Set random seed for reproducibility."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Train MI-Core bidirectional model."
    )
    parser.add_argument(
        "--data_dir", type=str, default="data/precomputed",
        help="Directory with pre-computed HDF5 labels.",
    )
    parser.add_argument(
        "--val_dir", type=str, default=None,
        help="Validation data directory (optional).",
    )
    parser.add_argument(
        "--epochs", type=int, default=600,
        help="Number of training epochs.",
    )
    parser.add_argument(
        "--batch_size", type=int, default=8,
        help="Training batch size.",
    )
    parser.add_argument(
        "--lr", type=float, default=3e-4,
        help="Learning rate.",
    )
    parser.add_argument(
        "--grad_accum", type=int, default=4,
        help="Gradient accumulation steps.",
    )
    parser.add_argument(
        "--checkpoint_dir", type=str, default="checkpoints",
        help="Checkpoint directory.",
    )
    parser.add_argument(
        "--resume", type=str, default=None,
        help="Path to checkpoint to resume from.",
    )
    parser.add_argument(
        "--seed", type=int, default=42,
        help="Random seed.",
    )
    parser.add_argument(
        "--segment_length", type=int, default=2048,
        help="Training segment length in frames.",
    )
    parser.add_argument(
        "--num_workers", type=int, default=4,
        help="DataLoader workers.",
    )
    parser.add_argument(
        "--no_amp", action="store_true",
        help="Disable BF16 mixed precision.",
    )
    parser.add_argument(
        "--log_every", type=int, default=50,
        help="Log metrics every N steps.",
    )
    args = parser.parse_args()

    # Seed
    set_seed(args.seed)

    # Device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Device: {device}")

    # Dataset
    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"ERROR: Data directory not found: {data_dir}")
        sys.exit(1)

    train_dataset = MIDataset(
        data_dir=str(data_dir),
        segment_length=args.segment_length,
    )
    print(f"Training dataset: {len(train_dataset)} tracks")

    collator = MICollator()
    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        num_workers=args.num_workers,
        collate_fn=collator,
        pin_memory=True,
        drop_last=True,
    )

    val_loader = None
    if args.val_dir:
        val_dataset = MIDataset(
            data_dir=args.val_dir,
            segment_length=args.segment_length,
        )
        val_loader = DataLoader(
            val_dataset,
            batch_size=args.batch_size * 2,
            shuffle=False,
            num_workers=args.num_workers,
            collate_fn=collator,
            pin_memory=True,
        )
        print(f"Validation dataset: {len(val_dataset)} tracks")

    # Model
    model = MICore()
    model = model.to(device)
    print(f"Model: {model}")

    # Trainer
    trainer = MITrainer(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        lr=args.lr,
        grad_accum_steps=args.grad_accum,
        use_amp=not args.no_amp,
        checkpoint_dir=args.checkpoint_dir,
        log_every=args.log_every,
    )

    # Resume
    if args.resume:
        trainer.load_checkpoint(args.resume)

    # Train
    trainer.train(n_epochs=args.epochs)

    # Save final
    trainer.save_checkpoint(args.epochs - 1)
    print("Training complete.")


if __name__ == "__main__":
    main()
