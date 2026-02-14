"""Alignment metrics -- MI-Core vs MI Teacher per-layer correlation.

Measures how well the neural MI-Core model has learned to replicate
the deterministic MI Teacher at every pipeline layer:

- Cochlea (Mel): MI-Core mel_hat vs Teacher mel
- R3:            MI-Core r3_hat  vs Teacher r3
- H3:            MI-Core h3_hat  vs Teacher h3_dense
- C3:            MI-Core c3_hat  vs Teacher c3

Reports per-dimension Pearson correlation, R², and MSE.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

import torch
from torch import Tensor


@dataclass
class AlignmentResult:
    """Per-layer alignment between MI-Core and MI Teacher.

    Attributes:
        layer_name: Name of the pipeline layer (mel, r3, h3, c3).
        mse: Mean squared error (scalar).
        mae: Mean absolute error (scalar).
        r2: Coefficient of determination R².
        pearson_per_dim: Per-dimension Pearson correlation (D,).
        pearson_mean: Mean Pearson correlation across all dimensions.
    """

    layer_name: str
    mse: float
    mae: float
    r2: float
    pearson_per_dim: List[float] = field(default_factory=list)
    pearson_mean: float = 0.0


class AlignmentEvaluator:
    """Evaluate MI-Core vs MI Teacher alignment across all pipeline layers.

    Usage::

        evaluator = AlignmentEvaluator()

        for batch in val_loader:
            enc_out = model.encode(batch["mel"])
            evaluator.update(
                pred_mel=enc_out.cochlea_hat,
                pred_r3=enc_out.r3_hat,
                pred_h3=enc_out.h3_hat,
                pred_c3=enc_out.c3_hat,
                target_mel=batch["mel"],
                target_r3=batch["r3"],
                target_h3=batch["h3_dense"],
                target_c3=batch["c3"],
            )

        results = evaluator.compute()
    """

    def __init__(self) -> None:
        self._preds: Dict[str, List[Tensor]] = {
            "mel": [], "r3": [], "h3": [], "c3": [],
        }
        self._targets: Dict[str, List[Tensor]] = {
            "mel": [], "r3": [], "h3": [], "c3": [],
        }

    def reset(self) -> None:
        """Clear accumulated predictions and targets."""
        for key in self._preds:
            self._preds[key].clear()
            self._targets[key].clear()

    def update(
        self,
        pred_mel: Tensor,
        pred_r3: Tensor,
        pred_h3: Optional[Tensor],
        pred_c3: Tensor,
        target_mel: Tensor,
        target_r3: Tensor,
        target_h3: Optional[Tensor],
        target_c3: Tensor,
    ) -> None:
        """Accumulate one batch of predictions and targets."""
        self._preds["mel"].append(pred_mel.detach().cpu())
        self._preds["r3"].append(pred_r3.detach().cpu())
        self._preds["c3"].append(pred_c3.detach().cpu())
        self._targets["mel"].append(target_mel.detach().cpu())
        self._targets["r3"].append(target_r3.detach().cpu())
        self._targets["c3"].append(target_c3.detach().cpu())

        if pred_h3 is not None and target_h3 is not None:
            self._preds["h3"].append(pred_h3.detach().cpu())
            self._targets["h3"].append(target_h3.detach().cpu())

    def compute(self) -> Dict[str, AlignmentResult]:
        """Compute alignment metrics for all layers.

        Returns
        -------
        dict
            Maps layer name to AlignmentResult.
        """
        results = {}
        for layer in ("mel", "r3", "h3", "c3"):
            if not self._preds[layer]:
                continue

            pred = torch.cat(self._preds[layer], dim=0)   # (N, T, D)
            target = torch.cat(self._targets[layer], dim=0)

            # Flatten batch and time: (N*T, D)
            pred_flat = pred.reshape(-1, pred.shape[-1])
            target_flat = target.reshape(-1, target.shape[-1])

            results[layer] = self._compute_layer(layer, pred_flat, target_flat)

        return results

    @staticmethod
    def _compute_layer(
        name: str, pred: Tensor, target: Tensor
    ) -> AlignmentResult:
        """Compute metrics for a single layer.

        Parameters
        ----------
        name : str
            Layer name.
        pred : Tensor
            Shape ``(N, D)`` flattened predictions.
        target : Tensor
            Shape ``(N, D)`` flattened targets.
        """
        mse = ((pred - target) ** 2).mean().item()
        mae = (pred - target).abs().mean().item()

        # R²: 1 - SS_res / SS_tot
        ss_res = ((target - pred) ** 2).sum().item()
        ss_tot = ((target - target.mean(dim=0, keepdim=True)) ** 2).sum().item()
        r2 = 1.0 - ss_res / max(ss_tot, 1e-8)

        # Per-dimension Pearson correlation
        pearson_per_dim = []
        D = pred.shape[-1]
        for d in range(D):
            p = pred[:, d]
            t = target[:, d]
            p_mean = p.mean()
            t_mean = t.mean()
            p_centered = p - p_mean
            t_centered = t - t_mean
            num = (p_centered * t_centered).sum()
            denom = (p_centered.norm() * t_centered.norm()).clamp(min=1e-8)
            pearson_per_dim.append((num / denom).item())

        pearson_mean = sum(pearson_per_dim) / max(len(pearson_per_dim), 1)

        return AlignmentResult(
            layer_name=name,
            mse=mse,
            mae=mae,
            r2=r2,
            pearson_per_dim=pearson_per_dim,
            pearson_mean=pearson_mean,
        )

    @staticmethod
    def format_results(results: Dict[str, AlignmentResult]) -> str:
        """Format results as a human-readable summary."""
        lines = ["MI-Core vs MI Teacher Alignment", "=" * 50]
        for name in ("mel", "r3", "h3", "c3"):
            if name not in results:
                continue
            r = results[name]
            lines.append(
                f"  {r.layer_name:6s} | MSE={r.mse:.6f} | MAE={r.mae:.6f} | "
                f"R²={r.r2:.4f} | Pearson={r.pearson_mean:.4f}"
            )
        lines.append("=" * 50)
        return "\n".join(lines)
