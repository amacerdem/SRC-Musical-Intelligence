"""Train BCH learned inverse heads — proof of concept.

Trains Head1 (mel → 112D manifold) and Head2 (112D manifold → mel) using
(mel, manifold) pairs pre-computed by the deterministic forward pipeline.

The 112D manifold = R³ active (16D) + H³ active (50D) + BCH output (16D)
+ RAM (26D) + Neuro (4D).
This captures the full computational state of the BCH nucleus plus its
downstream effects on brain regions and neurochemistry.

Usage::

    # Pre-compute first (local machine):
    python -m Musical_Intelligence.training.precompute_bch \\
        --audio-dir Test-Audio/ --output-dir ./cache/bch

    # Then train (RunPod H200):
    python -m Musical_Intelligence.training.train_bch \\
        --data-dir ./cache/bch \\
        --epochs 100 --batch-size 32

    # Smaller local test:
    python -m Musical_Intelligence.training.train_bch \\
        --data-dir ./cache/bch \\
        --epochs 10 --batch-size 4 --device cpu --no-compile --no-mixed-precision

Reference: MI-PLASTICITY.md §13.13 (Learned Inverse Heads).
"""
from __future__ import annotations

import json
import random
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

import torch
from torch import Tensor
from torch.utils.data import DataLoader, Dataset

from Musical_Intelligence.training.config import BCHTrainingConfig
from Musical_Intelligence.training.model.head import InverseHeadPair
from Musical_Intelligence.training.model.mi_space_layout import (
    BCH_H3_DEMAND_NAMES,
    BCH_NEURO_NAMES,
    BCH_OUTPUT_NAMES,
    BCH_R3_ACTIVE_NAMES,
    BCH_RAM_NAMES,
    COCHLEA_DIM,
    MANIFOLD_BCH_END,
    MANIFOLD_BCH_START,
    MANIFOLD_H3_END,
    MANIFOLD_H3_START,
    MANIFOLD_NEURO_END,
    MANIFOLD_NEURO_START,
    MANIFOLD_R3_END,
    MANIFOLD_R3_START,
    MANIFOLD_RAM_END,
    MANIFOLD_RAM_START,
)


# ======================================================================
# Manifold dimension names (112D = R³ 16 + H³ 50 + BCH 16 + RAM 26 + Neuro 4)
# ======================================================================

# Full 112D manifold names
MANIFOLD_DIM_NAMES: tuple = (
    BCH_R3_ACTIVE_NAMES + BCH_H3_DEMAND_NAMES + BCH_OUTPUT_NAMES
    + BCH_RAM_NAMES + BCH_NEURO_NAMES
)

# Layer boundaries for grouped reporting
MANIFOLD_LAYERS = {
    "r3_active": {"start": MANIFOLD_R3_START, "end": MANIFOLD_R3_END, "label": "R³ Active (16D)"},
    "h3_active": {"start": MANIFOLD_H3_START, "end": MANIFOLD_H3_END, "label": "H³ Active (50D)"},
    "bch_output": {"start": MANIFOLD_BCH_START, "end": MANIFOLD_BCH_END, "label": "BCH Output (16D)"},
    "ram": {"start": MANIFOLD_RAM_START, "end": MANIFOLD_RAM_END, "label": "RAM (26D)"},
    "neuro": {"start": MANIFOLD_NEURO_START, "end": MANIFOLD_NEURO_END, "label": "Neuro (4D)"},
}


# ======================================================================
# Training Report — deep JSON logging
# ======================================================================


class TrainingReport:
    """Accumulates deep training metrics and saves as JSON.

    Produces a comprehensive report including:
    - Full configuration snapshot
    - Model architecture (layers, params per head)
    - Per-epoch aggregate losses + learning rate + timing
    - Per-dimension MSE for Head1 (112D manifold breakdown by layer)
    - Per-step fine-grained loss trace
    - Gradient norm statistics per epoch
    - Final evaluation metrics
    """

    def __init__(self, config: BCHTrainingConfig, model: torch.nn.Module) -> None:
        self._start_time = time.time()
        self._start_datetime = datetime.now(timezone.utc).isoformat()
        self._target_dim = config.target_dim

        # Snapshot configuration
        self._config = {
            "data_dir": config.data_dir,
            "segment_frames": config.segment_frames,
            "batch_size": config.batch_size,
            "num_workers": config.num_workers,
            "target_dim": config.target_dim,
            "hidden_dim": config.hidden_dim,
            "kernel_sizes": list(config.kernel_sizes),
            "lr": config.lr,
            "weight_decay": config.weight_decay,
            "epochs": config.epochs,
            "cycle_loss_weight": config.cycle_loss_weight,
            "cycle_loss_start_epoch": config.cycle_loss_start_epoch,
            "device": config.device,
            "mixed_precision": config.mixed_precision,
            "compile_model": config.compile_model,
            "manifold_layout": {
                "r3_active": f"[{MANIFOLD_R3_START}:{MANIFOLD_R3_END}] (16D)",
                "h3_active": f"[{MANIFOLD_H3_START}:{MANIFOLD_H3_END}] (50D)",
                "bch_output": f"[{MANIFOLD_BCH_START}:{MANIFOLD_BCH_END}] (16D)",
                "ram": f"[{MANIFOLD_RAM_START}:{MANIFOLD_RAM_END}] (26D)",
                "neuro": f"[{MANIFOLD_NEURO_START}:{MANIFOLD_NEURO_END}] (4D)",
            },
        }

        # Model architecture snapshot
        raw_model = model._orig_mod if hasattr(model, "_orig_mod") else model
        self._model_info = {
            "total_params": sum(p.numel() for p in raw_model.parameters()),
            "perception_params": sum(
                p.numel() for p in raw_model.perception.parameters()
            ),
            "expression_params": sum(
                p.numel() for p in raw_model.expression.parameters()
            ),
            "perception_layers": _describe_module(raw_model.perception),
            "expression_layers": _describe_module(raw_model.expression),
        }

        # Accumulation buffers
        self._epochs: List[Dict[str, Any]] = []
        self._steps: List[Dict[str, Any]] = []
        self._current_epoch_steps: List[Dict[str, Any]] = []
        self._current_epoch_grad_norms: List[float] = []
        self._current_epoch_per_dim_mse: List[List[float]] = []

    def log_step(
        self,
        epoch: int,
        global_step: int,
        head1_loss: float,
        head2_loss: float,
        cycle_loss: float,
        lr: float,
        per_dim_mse: Optional[List[float]] = None,
        grad_norm: Optional[float] = None,
    ) -> None:
        """Record a single training step."""
        step_record = {
            "epoch": epoch,
            "global_step": global_step,
            "head1_loss": round(head1_loss, 6),
            "head2_loss": round(head2_loss, 6),
            "cycle_loss": round(cycle_loss, 6),
            "lr": lr,
        }
        self._steps.append(step_record)
        self._current_epoch_steps.append(step_record)

        if per_dim_mse is not None:
            self._current_epoch_per_dim_mse.append(per_dim_mse)
        if grad_norm is not None:
            self._current_epoch_grad_norms.append(grad_norm)

    def log_epoch(
        self,
        epoch: int,
        avg_head1: float,
        avg_head2: float,
        avg_cycle: float,
        avg_total: float,
        lr: float,
        elapsed_s: float,
        is_best: bool,
    ) -> None:
        """Record epoch-level aggregate metrics."""
        # Per-dimension breakdown grouped by layer
        per_dim_avg = None
        per_layer_avg = None
        if self._current_epoch_per_dim_mse:
            n = len(self._current_epoch_per_dim_mse)
            per_dim_avg = {}
            for d in range(self._target_dim):
                vals = [s[d] for s in self._current_epoch_per_dim_mse]
                name = MANIFOLD_DIM_NAMES[d] if d < len(MANIFOLD_DIM_NAMES) else f"dim_{d}"
                per_dim_avg[name] = round(sum(vals) / n, 6)

            # Per-layer aggregate
            per_layer_avg = {}
            for layer_name, info in MANIFOLD_LAYERS.items():
                layer_dims = range(info["start"], info["end"])
                layer_vals = []
                for d in layer_dims:
                    if d < self._target_dim:
                        vals = [s[d] for s in self._current_epoch_per_dim_mse]
                        layer_vals.append(sum(vals) / n)
                if layer_vals:
                    per_layer_avg[layer_name] = round(sum(layer_vals) / len(layer_vals), 6)

        # Gradient norm stats
        grad_stats = None
        if self._current_epoch_grad_norms:
            norms = self._current_epoch_grad_norms
            grad_stats = {
                "mean": round(sum(norms) / len(norms), 6),
                "max": round(max(norms), 6),
                "min": round(min(norms), 6),
            }

        epoch_record = {
            "epoch": epoch,
            "avg_losses": {
                "head1": round(avg_head1, 6),
                "head2": round(avg_head2, 6),
                "cycle": round(avg_cycle, 6),
                "total": round(avg_total, 6),
            },
            "lr": lr,
            "elapsed_s": round(elapsed_s, 3),
            "is_best": is_best,
            "n_steps": len(self._current_epoch_steps),
            "per_layer_mse_head1": per_layer_avg,
            "per_dim_mse_head1": per_dim_avg,
            "grad_norm_stats": grad_stats,
        }
        self._epochs.append(epoch_record)

        # Reset per-epoch buffers
        self._current_epoch_steps = []
        self._current_epoch_grad_norms = []
        self._current_epoch_per_dim_mse = []

    def finalize(
        self,
        best_loss: float,
        dataset_info: Dict[str, Any],
        eval_results: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Build the complete report dict."""
        total_time = time.time() - self._start_time
        return {
            "meta": {
                "task": "BCH Learned Inverse Heads — Training POC (112D Manifold)",
                "reference": "MI-PLASTICITY.md §13.13",
                "manifold": "R³ active (16D) + H³ active (50D) + BCH output (16D) + RAM (26D) + Neuro (4D) = 112D",
                "started_at": self._start_datetime,
                "finished_at": datetime.now(timezone.utc).isoformat(),
                "total_time_s": round(total_time, 2),
                "torch_version": torch.__version__,
                "cuda_available": torch.cuda.is_available(),
                "gpu_name": (
                    torch.cuda.get_device_name(0)
                    if torch.cuda.is_available()
                    else None
                ),
            },
            "config": self._config,
            "model": self._model_info,
            "dataset": dataset_info,
            "training": {
                "total_epochs": len(self._epochs),
                "total_steps": len(self._steps),
                "best_total_loss": round(best_loss, 6),
                "final_losses": (
                    self._epochs[-1]["avg_losses"] if self._epochs else None
                ),
            },
            "epoch_history": self._epochs,
            "step_trace": self._steps,
            "evaluation": eval_results,
        }

    def save(self, path: Path, **kwargs) -> None:
        """Serialize report to JSON."""
        report = self.finalize(**kwargs)
        path.write_text(json.dumps(report, indent=2, ensure_ascii=False))
        print(f"Report saved: {path} ({path.stat().st_size / 1024:.1f} KB)")


def _describe_module(module: torch.nn.Module) -> List[Dict[str, Any]]:
    """Produce a human-readable layer-by-layer description."""
    layers = []
    for name, child in module.named_modules():
        if isinstance(child, torch.nn.Conv1d):
            layers.append({
                "name": name,
                "type": "Conv1d",
                "in_channels": child.in_channels,
                "out_channels": child.out_channels,
                "kernel_size": child.kernel_size[0],
                "padding": child.padding[0],
                "params": sum(p.numel() for p in child.parameters()),
            })
        elif isinstance(child, torch.nn.LayerNorm):
            layers.append({
                "name": name,
                "type": "LayerNorm",
                "normalized_shape": list(child.normalized_shape),
            })
    return layers


def _compute_per_dim_mse(
    pred: Tensor, target: Tensor, mask: Tensor,
) -> List[float]:
    """Per-dimension MSE for manifold (Head1 diagnostic).

    Parameters
    ----------
    pred, target : (B, D, T)
    mask : (B, T)

    Returns list of D floats.
    """
    mask_f = mask.unsqueeze(1).float()  # (B, 1, T)
    n_valid = mask_f.sum()
    if n_valid == 0:
        return [0.0] * pred.shape[1]

    diff_sq = (pred - target) ** 2  # (B, D, T)
    masked = diff_sq * mask_f       # (B, D, T)
    per_dim = masked.sum(dim=(0, 2)) / n_valid  # (D,)
    return [round(v.item(), 6) for v in per_dim]


def _compute_grad_norm(model: torch.nn.Module) -> float:
    """Compute total gradient L2 norm across all parameters."""
    total = 0.0
    for p in model.parameters():
        if p.grad is not None:
            total += p.grad.data.norm(2).item() ** 2
    return total ** 0.5


# ======================================================================
# BCH Dataset — reads pre-computed (mel, manifold) HDF5 pairs
# ======================================================================


class BCHDataset(Dataset):
    """Dataset of pre-computed (mel, manifold) pairs in HDF5 format.

    Each HDF5 file contains:
        - ``mel``: ``(T, 128)`` float32
        - ``manifold``: ``(T, 82)`` float32

    Returns fixed-length segments with random temporal offset.
    """

    def __init__(
        self,
        data_dir: str,
        segment_frames: int = 2048,
        split: str = "train",
    ) -> None:
        self._segment_frames = segment_frames
        self._split = split

        # Discover HDF5 files
        data_path = Path(data_dir) / split
        if not data_path.exists():
            data_path = Path(data_dir)

        self._files: List[Path] = sorted(data_path.glob("*.h5"))
        if not self._files:
            raise FileNotFoundError(f"No .h5 files found in {data_path}")

    def __len__(self) -> int:
        return len(self._files)

    def __getitem__(self, idx: int) -> Dict[str, Tensor]:
        import h5py

        path = self._files[idx]

        with h5py.File(path, "r") as f:
            total_frames = f["mel"].shape[0]

            # Random offset for training, start for eval
            if self._split == "train" and total_frames > self._segment_frames:
                offset = random.randint(0, total_frames - self._segment_frames)
            else:
                offset = 0

            end = min(offset + self._segment_frames, total_frames)

            mel = torch.from_numpy(f["mel"][offset:end])           # (T, 128)
            manifold = torch.from_numpy(f["manifold"][offset:end]) # (T, 112)

        return {"mel": mel, "manifold": manifold}


class BCHCollator:
    """Collates variable-length (mel, manifold) samples into padded batches."""

    def __call__(self, samples: List[Dict[str, Tensor]]) -> Dict[str, Tensor]:
        batch_size = len(samples)
        max_t = max(s["mel"].shape[0] for s in samples)
        manifold_dim = samples[0]["manifold"].shape[1]

        mel_padded = torch.zeros(batch_size, max_t, COCHLEA_DIM)
        manifold_padded = torch.zeros(batch_size, max_t, manifold_dim)
        mask = torch.zeros(batch_size, max_t, dtype=torch.bool)

        for i, s in enumerate(samples):
            t = s["mel"].shape[0]
            mel_padded[i, :t] = s["mel"]
            manifold_padded[i, :t] = s["manifold"]
            mask[i, :t] = True

        return {
            "mel": mel_padded,           # (B, T, 128)
            "manifold": manifold_padded, # (B, T, 112)
            "mask": mask,                # (B, T)
        }


# ======================================================================
# Masked MSE loss — ignores padding
# ======================================================================


def masked_mse(pred: Tensor, target: Tensor, mask: Tensor) -> Tensor:
    """MSE loss computed only over valid (non-padded) frames.

    Parameters
    ----------
    pred : Tensor
        Shape ``(B, C, T)`` — predicted values.
    target : Tensor
        Shape ``(B, C, T)`` — target values.
    mask : Tensor
        Shape ``(B, T)`` — True for valid frames.

    Returns
    -------
    Tensor
        Scalar MSE loss over valid frames.
    """
    mask_expanded = mask.unsqueeze(1).float()  # (B, 1, T)
    diff = (pred - target) ** 2  # (B, C, T)
    masked_diff = diff * mask_expanded
    n_valid = mask_expanded.sum() * pred.shape[1]  # total valid elements
    if n_valid > 0:
        return masked_diff.sum() / n_valid
    return masked_diff.sum()


# ======================================================================
# Training loop
# ======================================================================


def train(config: BCHTrainingConfig) -> None:
    """Run the full training loop for BCH inverse heads."""
    device = torch.device(config.device)

    # ── Dataset & loader ──────────────────────────────────────
    dataset = BCHDataset(
        data_dir=config.data_dir,
        segment_frames=config.segment_frames,
        split="train",
    )
    loader = DataLoader(
        dataset,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=config.num_workers,
        collate_fn=BCHCollator(),
        pin_memory=(config.device == "cuda"),
        drop_last=False,
    )

    dataset_info = {
        "n_tracks": len(dataset),
        "segment_frames": config.segment_frames,
        "segment_seconds": round(config.segment_frames * 256 / 44100, 2),
        "steps_per_epoch": len(loader),
        "track_files": [p.name for p in dataset._files],
        "manifold_dim": config.target_dim,
    }
    print(f"Dataset: {len(dataset)} tracks, segment={config.segment_frames} frames")
    print(f"Manifold: {config.target_dim}D = R³(16) + H³(50) + BCH(16) + RAM(26) + Neuro(4)")
    print(f"Loader: batch_size={config.batch_size}, steps/epoch={len(loader)}")

    # ── Model ─────────────────────────────────────────────────
    model = InverseHeadPair(
        target_dim=config.target_dim,
        hidden_dim=config.hidden_dim,
        kernel_sizes=config.kernel_sizes,
    ).to(device)

    n_params = sum(p.numel() for p in model.parameters())
    n_h1 = sum(p.numel() for p in model.perception.parameters())
    n_h2 = sum(p.numel() for p in model.expression.parameters())
    print(f"Model: InverseHeadPair, {n_params:,} parameters")
    print(f"  Head1 (mel→manifold): {n_h1:,}")
    print(f"  Head2 (manifold→mel): {n_h2:,}")

    # ── Report ─────────────────────────────────────────────────
    report = TrainingReport(config, model)

    if config.compile_model and hasattr(torch, "compile"):
        try:
            model = torch.compile(model)
            print("  torch.compile: enabled")
        except Exception as e:
            print(f"  torch.compile: failed ({e}), continuing without")

    # ── Optimizer & scheduler ─────────────────────────────────
    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=config.lr,
        weight_decay=config.weight_decay,
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=config.epochs,
    )

    # ── Mixed precision ───────────────────────────────────────
    use_amp = config.mixed_precision and device.type == "cuda"
    scaler = torch.amp.GradScaler("cuda") if use_amp else None
    amp_dtype = torch.float16 if use_amp else torch.float32
    print(f"Mixed precision: {'fp16' if use_amp else 'fp32'}")

    # ── Checkpoint & report dirs ──────────────────────────────
    ckpt_dir = Path(config.checkpoint_dir)
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    report_dir = ckpt_dir / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)

    # ── Training ──────────────────────────────────────────────
    best_total_loss = float("inf")
    global_step = 0
    print()
    print(f"Training for {config.epochs} epochs")
    print("=" * 72)

    for epoch in range(1, config.epochs + 1):
        model.train()
        epoch_losses = {"head1": 0.0, "head2": 0.0, "cycle": 0.0, "total": 0.0}
        epoch_steps = 0
        t_epoch = time.time()

        use_cycle = (
            epoch >= config.cycle_loss_start_epoch
            and config.cycle_loss_weight > 0
        )

        for batch in loader:
            # Move to device — Conv1D expects (B, C, T) so transpose
            mel = batch["mel"].to(device).transpose(1, 2)        # (B, 128, T)
            manifold = batch["manifold"].to(device).transpose(1, 2)  # (B, 112, T)
            mask = batch["mask"].to(device)                       # (B, T)

            optimizer.zero_grad()

            with torch.autocast(device.type, dtype=amp_dtype, enabled=use_amp):
                # Head1: mel → manifold_hat
                manifold_hat = model.forward_head1(mel)  # (B, 112, T)
                head1_loss = masked_mse(manifold_hat, manifold, mask)

                # Head2: manifold → mel_hat
                mel_hat = model.forward_head2(manifold)  # (B, 128, T)
                head2_loss = masked_mse(mel_hat, mel, mask)

                total_loss = head1_loss + head2_loss

                # Cycle consistency (Phase 2+)
                cycle_loss = torch.tensor(0.0, device=device)
                if use_cycle:
                    cycle_loss, _ = model.cycle_loss(manifold)
                    total_loss = total_loss + config.cycle_loss_weight * cycle_loss

            # Backward
            if scaler is not None:
                scaler.scale(total_loss).backward()
                scaler.step(optimizer)
                scaler.update()
            else:
                total_loss.backward()
                optimizer.step()

            # Per-dimension MSE for Head1 (detached, no grad)
            with torch.no_grad():
                per_dim = _compute_per_dim_mse(manifold_hat, manifold, mask)

            # Gradient norm (after backward, before zero_grad)
            raw_model = model._orig_mod if hasattr(model, "_orig_mod") else model
            grad_norm = _compute_grad_norm(raw_model)

            # Accumulate
            epoch_losses["head1"] += head1_loss.item()
            epoch_losses["head2"] += head2_loss.item()
            epoch_losses["cycle"] += cycle_loss.item()
            epoch_losses["total"] += total_loss.item()
            epoch_steps += 1
            global_step += 1

            # Log to report
            report.log_step(
                epoch=epoch,
                global_step=global_step,
                head1_loss=head1_loss.item(),
                head2_loss=head2_loss.item(),
                cycle_loss=cycle_loss.item(),
                lr=optimizer.param_groups[0]["lr"],
                per_dim_mse=per_dim,
                grad_norm=grad_norm,
            )

            # Step-level console logging
            if global_step % config.log_every == 0:
                cycle_str = f"{cycle_loss.item():.4f}" if use_cycle else "--"
                print(
                    f"  [E{epoch:03d}/{config.epochs} S{global_step:04d}] "
                    f"h1={head1_loss.item():.4f} "
                    f"h2={head2_loss.item():.4f} "
                    f"cyc={cycle_str} "
                    f"lr={optimizer.param_groups[0]['lr']:.2e} "
                    f"gnorm={grad_norm:.2f}"
                )

        scheduler.step()

        # Epoch summary
        avg = {k: v / max(epoch_steps, 1) for k, v in epoch_losses.items()}
        elapsed = time.time() - t_epoch
        is_best = avg["total"] < best_total_loss
        cycle_str = f"{avg['cycle']:.4f}" if use_cycle else "--"
        best_marker = " *BEST*" if is_best else ""
        print(
            f"[E{epoch:03d}/{config.epochs}] "
            f"h1={avg['head1']:.4f} h2={avg['head2']:.4f} "
            f"cyc={cycle_str} total={avg['total']:.4f} "
            f"({elapsed:.1f}s){best_marker}"
        )

        # Log epoch to report
        report.log_epoch(
            epoch=epoch,
            avg_head1=avg["head1"],
            avg_head2=avg["head2"],
            avg_cycle=avg["cycle"],
            avg_total=avg["total"],
            lr=optimizer.param_groups[0]["lr"],
            elapsed_s=elapsed,
            is_best=is_best,
        )

        # Track best
        if is_best:
            best_total_loss = avg["total"]
            _save_checkpoint(
                ckpt_dir / "best.pt", model, optimizer, scheduler,
                epoch, global_step, best_total_loss,
            )

        # Periodic checkpoint
        if epoch % config.save_every == 0:
            _save_checkpoint(
                ckpt_dir / f"epoch_{epoch:04d}.pt", model, optimizer, scheduler,
                epoch, global_step, avg["total"],
            )

    # ── Final evaluation ──────────────────────────────────────
    print()
    print("Running final evaluation...")
    eval_results = _evaluate(model, dataset, device, use_amp, amp_dtype, config.target_dim)

    # ── Final save ────────────────────────────────────────────
    _save_checkpoint(
        ckpt_dir / "final.pt", model, optimizer, scheduler,
        config.epochs, global_step, avg["total"],
    )

    # ── Save report ───────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = report_dir / f"training_report_{timestamp}.json"
    report.save(
        report_path,
        best_loss=best_total_loss,
        dataset_info=dataset_info,
        eval_results=eval_results,
    )

    print()
    print("=" * 72)
    print(f"Training complete. Best total loss: {best_total_loss:.6f}")
    print(f"Checkpoints: {ckpt_dir}")
    print(f"Report: {report_path}")


# ======================================================================
# Final evaluation — per-layer, per-dimension breakdown
# ======================================================================


@torch.no_grad()
def _evaluate(
    model: torch.nn.Module,
    dataset: BCHDataset,
    device: torch.device,
    use_amp: bool,
    amp_dtype: torch.dtype,
    target_dim: int,
) -> Dict[str, Any]:
    """Run evaluation on all tracks, return per-layer and per-dimension metrics."""
    raw_model = model._orig_mod if hasattr(model, "_orig_mod") else model
    raw_model.eval()

    all_per_dim = []
    head2_losses = []
    cycle_losses = []
    track_results = []

    for idx in range(len(dataset)):
        sample = dataset[idx]
        mel = sample["mel"].unsqueeze(0).to(device).transpose(1, 2)        # (1, 128, T)
        manifold = sample["manifold"].unsqueeze(0).to(device).transpose(1, 2)  # (1, 112, T)
        mask = torch.ones(1, mel.shape[2], dtype=torch.bool, device=device)

        with torch.autocast(device.type, dtype=amp_dtype, enabled=use_amp):
            manifold_hat = raw_model.forward_head1(mel)
            mel_hat = raw_model.forward_head2(manifold)

            h1_loss = masked_mse(manifold_hat, manifold, mask).item()
            h2_loss = masked_mse(mel_hat, mel, mask).item()

            # Cycle: manifold → mel_hat → manifold_hat
            cycle_l, _ = raw_model.cycle_loss(manifold)

        per_dim = _compute_per_dim_mse(manifold_hat, manifold, mask)
        all_per_dim.append(per_dim)
        head2_losses.append(h2_loss)
        cycle_losses.append(cycle_l.item())

        # Per-track report
        track_name = dataset._files[idx].stem
        track_report = {
            "track": track_name,
            "n_frames": sample["mel"].shape[0],
            "head1_mse": round(h1_loss, 6),
            "head2_mse": round(h2_loss, 6),
            "cycle_mse": round(cycle_l.item(), 6),
        }

        # Per-dimension MSE grouped by layer
        for layer_name, info in MANIFOLD_LAYERS.items():
            layer_dims = range(info["start"], min(info["end"], target_dim))
            layer_mse = {}
            for d in layer_dims:
                name = MANIFOLD_DIM_NAMES[d] if d < len(MANIFOLD_DIM_NAMES) else f"dim_{d}"
                layer_mse[name] = round(per_dim[d], 6)
            track_report[f"per_dim_mse_{layer_name}"] = layer_mse

        # Per-dimension correlation (how well head1 tracks pipeline)
        gt_np = manifold.squeeze(0).cpu()      # (112, T)
        hat_np = manifold_hat.squeeze(0).cpu()  # (112, T)
        correlations = {}
        for layer_name, info in MANIFOLD_LAYERS.items():
            layer_corrs = {}
            for d in range(info["start"], min(info["end"], target_dim)):
                gt_d = gt_np[d]
                pr_d = hat_np[d]
                name = MANIFOLD_DIM_NAMES[d] if d < len(MANIFOLD_DIM_NAMES) else f"dim_{d}"
                if gt_d.std() > 1e-6 and pr_d.std() > 1e-6:
                    corr = torch.corrcoef(torch.stack([gt_d, pr_d]))[0, 1].item()
                    layer_corrs[name] = round(corr, 4)
                else:
                    layer_corrs[name] = None
            correlations[layer_name] = layer_corrs
        track_report["per_dim_correlation"] = correlations

        track_results.append(track_report)
        print(
            f"  [{idx+1}/{len(dataset)}] {track_name}: "
            f"h1={h1_loss:.4f} h2={h2_loss:.4f} cyc={cycle_l.item():.4f}"
        )

    # Aggregate per-layer MSE across all tracks
    n = len(all_per_dim)
    avg_per_layer = {}
    avg_per_dim = {}
    for layer_name, info in MANIFOLD_LAYERS.items():
        layer_dims = range(info["start"], min(info["end"], target_dim))
        layer_avg = {}
        layer_total = 0.0
        for d in layer_dims:
            vals = [p[d] for p in all_per_dim]
            name = MANIFOLD_DIM_NAMES[d] if d < len(MANIFOLD_DIM_NAMES) else f"dim_{d}"
            avg_val = sum(vals) / n
            layer_avg[name] = round(avg_val, 6)
            avg_per_dim[name] = round(avg_val, 6)
            layer_total += avg_val
        n_layer_dims = len(list(layer_dims))
        avg_per_layer[layer_name] = {
            "mean_mse": round(layer_total / max(n_layer_dims, 1), 6),
            "per_dim": layer_avg,
        }

    return {
        "n_tracks": len(track_results),
        "avg_head2_mse": round(sum(head2_losses) / n, 6),
        "avg_cycle_mse": round(sum(cycle_losses) / n, 6),
        "avg_per_layer_mse_head1": avg_per_layer,
        "avg_per_dim_mse_head1": avg_per_dim,
        "per_track": track_results,
    }


# ======================================================================
# Checkpoint utilities
# ======================================================================


def _save_checkpoint(
    path: Path,
    model,
    optimizer,
    scheduler,
    epoch: int,
    global_step: int,
    loss: float,
) -> None:
    """Save training checkpoint."""
    state_dict = model.state_dict()
    if hasattr(model, "_orig_mod"):
        state_dict = model._orig_mod.state_dict()

    torch.save(
        {
            "model_state_dict": state_dict,
            "optimizer_state_dict": optimizer.state_dict(),
            "scheduler_state_dict": scheduler.state_dict(),
            "epoch": epoch,
            "global_step": global_step,
            "loss": loss,
        },
        path,
    )


# ======================================================================
# Entry point
# ======================================================================


def main() -> None:
    config = BCHTrainingConfig.from_cli()
    print("BCH Learned Inverse Heads — Training POC (112D Manifold)")
    print(f"  target_dim: {config.target_dim} = R³(16) + H³(50) + BCH(16) + RAM(26) + Neuro(4)")
    print(f"  hidden_dim: {config.hidden_dim}")
    print(f"  kernel_sizes: {config.kernel_sizes}")
    print(f"  device: {config.device}")
    print(f"  epochs: {config.epochs}")
    print(f"  batch_size: {config.batch_size}")
    print(f"  mixed_precision: {config.mixed_precision}")
    print()
    train(config)


if __name__ == "__main__":
    main()
