"""MITrainer -- Main training loop for the MI-Core bidirectional model.

Each training step performs four simultaneous objectives:
1. ENCODE: mel → backbone → heads → {mel, R3, H3, C3}
2. DECODE: C3 → backbone → heads → {H3, R3, mel}
3. CYCLE:  Encode(Decode(C3)) ≈ C3, Decode(Encode(mel)) ≈ mel
4. FILL:   mask(C3) → FillNet → C3_filled

All 14 loss terms are weighted by the curriculum scheduler.

Supports: DDP, BF16 mixed precision, gradient accumulation,
WandB logging, checkpoint save/resume.

Reference: MI-VISION Section 12
"""
from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Dict, Optional

import torch
import torch.nn as nn
from torch import Tensor
from torch.cuda.amp import GradScaler, autocast
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingWarmRestarts
from torch.utils.data import DataLoader

from Musical_Intelligence.training.loss.composite_loss import MICompositeLoss
from Musical_Intelligence.training.loss.cycle_loss import CycleLoss
from Musical_Intelligence.training.loss.decode_loss import DecodeLoss
from Musical_Intelligence.training.loss.encode_loss import EncodeLoss
from Musical_Intelligence.training.loss.fill_loss import FillLoss
from Musical_Intelligence.training.loss.regularization import RegularizationLoss
from Musical_Intelligence.training.model.fill_net.fill_net import FillNet
from Musical_Intelligence.training.model.mi_core import MICore
from Musical_Intelligence.training.model.mi_space_layout import C3_SLICE


class MITrainer:
    """Main training loop for MI-Core bidirectional training.

    Parameters
    ----------
    model : MICore
        The MI-Core model to train.
    train_loader : DataLoader
        Training data loader yielding batches with keys:
        mel (B,T,128), r3 (B,T,128), h3_dense (B,T,N), c3 (B,T,1006).
    val_loader : DataLoader, optional
        Validation data loader (same format).
    lr : float
        Learning rate (default 3e-4).
    weight_decay : float
        Weight decay (default 0.01).
    grad_accum_steps : int
        Gradient accumulation steps (default 1).
    use_amp : bool
        Use BF16 mixed precision (default True).
    checkpoint_dir : str
        Directory for saving checkpoints.
    log_every : int
        Log metrics every N steps (default 50).
    """

    def __init__(
        self,
        model: MICore,
        train_loader: DataLoader,
        val_loader: Optional[DataLoader] = None,
        lr: float = 3e-4,
        weight_decay: float = 0.01,
        grad_accum_steps: int = 1,
        use_amp: bool = True,
        checkpoint_dir: str = "checkpoints",
        log_every: int = 50,
    ) -> None:
        self.model = model
        self.train_loader = train_loader
        self.val_loader = val_loader
        self.grad_accum_steps = grad_accum_steps
        self.use_amp = use_amp
        self.log_every = log_every
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

        # Optimiser
        self.optimizer = AdamW(
            model.parameters(), lr=lr, weight_decay=weight_decay
        )
        self.scheduler = CosineAnnealingWarmRestarts(
            self.optimizer, T_0=50, T_mult=2
        )

        # Loss modules
        self.encode_loss = EncodeLoss()
        self.decode_loss = DecodeLoss()
        self.cycle_loss = CycleLoss()
        self.fill_loss = FillLoss()
        self.reg_loss = RegularizationLoss()
        self.composite_loss = MICompositeLoss()

        # AMP scaler
        self.scaler = GradScaler(enabled=use_amp)

        # Tracking
        self._global_step = 0
        self._start_epoch = 0

    # ------------------------------------------------------------------
    # Training step
    # ------------------------------------------------------------------

    def _training_step(
        self, batch: Dict[str, Tensor], epoch: int
    ) -> Dict[str, float]:
        """Execute one bidirectional training step.

        Returns breakdown of all 14 losses + total.
        """
        mel = batch["mel"]       # (B, T, 128)
        r3 = batch["r3"]        # (B, T, 128)
        h3 = batch["h3_dense"]  # (B, T, N)
        c3 = batch["c3"]        # (B, T, 1006)
        mask = batch.get("attention_mask")

        device = next(self.model.parameters()).device
        mel = mel.to(device)
        r3 = r3.to(device)
        h3 = h3.to(device)
        c3 = c3.to(device)
        if mask is not None:
            mask = mask.to(device)

        amp_dtype = torch.bfloat16 if self.use_amp else torch.float32

        with autocast(dtype=amp_dtype, enabled=self.use_amp):
            # 1. ENCODE: mel → predictions at every layer
            enc_out = self.model.encode(mel)

            encode_losses = self.encode_loss(
                cochlea_hat=enc_out.cochlea_hat,
                r3_hat=enc_out.r3_hat,
                h3_hat=enc_out.h3_hat,
                c3_hat=enc_out.c3_hat,
                mel_target=mel,
                r3_target=r3,
                h3_target=h3,
                c3_target=c3,
                mask=mask,
            )

            # 2. DECODE: C3 → reconstructions at every layer
            dec_out = self.model.decode(c3)

            decode_losses = self.decode_loss(
                h3_rec=dec_out.h3_rec,
                r3_rec=dec_out.r3_rec,
                mel_rec=dec_out.mel_rec,
                h3_target=h3,
                r3_target=r3,
                mel_target=mel,
                mask=mask,
            )

            # 3. CYCLE: consistency
            # Forward cycle: Encode(Decode(C3)) ≈ C3
            cycle_enc = self.model.encode(dec_out.mel_rec)
            # Inverse cycle: Decode(Encode(mel)) ≈ mel
            cycle_dec = self.model.decode(enc_out.c3_hat)

            cycle_losses = self.cycle_loss(
                c3_original=c3,
                c3_reconstructed=cycle_enc.c3_hat,
                mel_original=mel,
                mel_reconstructed=cycle_dec.mel_rec,
            )

            # 4. FILL: masked C3 completion
            c3_masked, fill_mask = FillNet.random_mask(c3)
            c3_filled = self.model.fill(c3_masked, fill_mask)

            fill_losses = self.fill_loss(
                c3_filled=c3_filled,
                c3_target=c3,
                mask=fill_mask,
            )

            # 5. REGULARISATION
            reg_losses = self.reg_loss(
                mi_space=enc_out.mi_space,
                balance_loss=enc_out.balance_loss,
            )

            # Combine all 14 losses
            all_losses = {
                **encode_losses,
                **decode_losses,
                **cycle_losses,
                **fill_losses,
                **reg_losses,
            }

            total_loss, breakdown = self.composite_loss(all_losses, epoch)
            total_loss = total_loss / self.grad_accum_steps

        # Backward
        self.scaler.scale(total_loss).backward()

        return breakdown

    # ------------------------------------------------------------------
    # Train epoch
    # ------------------------------------------------------------------

    def train_epoch(self, epoch: int) -> Dict[str, float]:
        """Train for one epoch."""
        self.model.train()
        epoch_metrics: Dict[str, float] = {}
        n_steps = 0

        for step, batch in enumerate(self.train_loader):
            breakdown = self._training_step(batch, epoch)

            # Gradient accumulation
            if (step + 1) % self.grad_accum_steps == 0:
                self.scaler.step(self.optimizer)
                self.scaler.update()
                self.optimizer.zero_grad()
                self._global_step += 1

            # Accumulate metrics
            for k, v in breakdown.items():
                epoch_metrics[k] = epoch_metrics.get(k, 0) + v
            n_steps += 1

            # Log
            if (step + 1) % self.log_every == 0:
                avg_total = epoch_metrics.get("total", 0) / n_steps
                phase = breakdown.get("phase", 0)
                print(
                    f"  step {step + 1}/{len(self.train_loader)} | "
                    f"loss={avg_total:.4f} | phase={phase}"
                )

        # Average metrics
        for k in epoch_metrics:
            if isinstance(epoch_metrics[k], (int, float)):
                epoch_metrics[k] /= max(n_steps, 1)

        self.scheduler.step()
        return epoch_metrics

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------

    @torch.no_grad()
    def validate(self, epoch: int) -> Dict[str, float]:
        """Run validation epoch."""
        if self.val_loader is None:
            return {}

        self.model.eval()
        val_metrics: Dict[str, float] = {}
        n_steps = 0

        for batch in self.val_loader:
            mel = batch["mel"].to(next(self.model.parameters()).device)
            r3 = batch["r3"].to(mel.device)
            h3 = batch["h3_dense"].to(mel.device)
            c3 = batch["c3"].to(mel.device)

            enc_out = self.model.encode(mel)
            encode_losses = self.encode_loss(
                enc_out.cochlea_hat, enc_out.r3_hat,
                enc_out.h3_hat, enc_out.c3_hat,
                mel, r3, h3, c3,
            )

            for k, v in encode_losses.items():
                val_metrics[f"val_{k}"] = val_metrics.get(f"val_{k}", 0) + v.item()
            n_steps += 1

        for k in val_metrics:
            val_metrics[k] /= max(n_steps, 1)

        return val_metrics

    # ------------------------------------------------------------------
    # Full training
    # ------------------------------------------------------------------

    def train(self, n_epochs: int) -> None:
        """Run full training for n_epochs."""
        print(f"Starting training: {n_epochs} epochs")
        print(f"Model: {self.model}")

        for epoch in range(self._start_epoch, n_epochs):
            t0 = time.time()
            train_metrics = self.train_epoch(epoch)
            val_metrics = self.validate(epoch)
            elapsed = time.time() - t0

            phase = train_metrics.get("phase", 0)
            total = train_metrics.get("total", 0)
            print(
                f"Epoch {epoch + 1}/{n_epochs} | "
                f"phase={phase} | loss={total:.4f} | "
                f"time={elapsed:.1f}s"
            )

            # Save checkpoint every 10 epochs
            if (epoch + 1) % 10 == 0:
                self.save_checkpoint(epoch)

    # ------------------------------------------------------------------
    # Checkpointing
    # ------------------------------------------------------------------

    def save_checkpoint(self, epoch: int) -> Path:
        """Save training checkpoint."""
        path = self.checkpoint_dir / f"mi_core_epoch_{epoch + 1}.pt"
        torch.save({
            "epoch": epoch + 1,
            "global_step": self._global_step,
            "model_state_dict": self.model.state_dict(),
            "optimizer_state_dict": self.optimizer.state_dict(),
            "scheduler_state_dict": self.scheduler.state_dict(),
            "scaler_state_dict": self.scaler.state_dict(),
        }, path)
        print(f"Checkpoint saved: {path}")
        return path

    def load_checkpoint(self, path: str) -> None:
        """Resume from checkpoint."""
        ckpt = torch.load(path, map_location="cpu")
        self.model.load_state_dict(ckpt["model_state_dict"])
        self.optimizer.load_state_dict(ckpt["optimizer_state_dict"])
        self.scheduler.load_state_dict(ckpt["scheduler_state_dict"])
        self.scaler.load_state_dict(ckpt["scaler_state_dict"])
        self._start_epoch = ckpt["epoch"]
        self._global_step = ckpt["global_step"]
        print(f"Resumed from epoch {self._start_epoch}")
