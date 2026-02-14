"""Fill-Net evaluation -- completion quality vs mask ratio.

Evaluates the FillNet's ability to complete partially specified C3
vectors at various mask ratios (10%, 30%, 50%, 70%, 90%).

Key questions:
- How does completion quality degrade with higher masking?
- Which C3 dimensions are easiest/hardest to predict?
- Do learned correlations match known neuroscience relationships?
  (e.g., pleasure ↑ → da_nacc ↑, r=0.84)
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

import torch
from torch import Tensor


@dataclass
class FillEvalResult:
    """Fill evaluation at a single mask ratio.

    Attributes:
        mask_ratio: Fraction of dimensions masked (0.0 to 1.0).
        mse: MSE on masked dimensions only.
        mae: MAE on masked dimensions only.
        r2: R² on masked dimensions only.
        per_dim_mse: Per-dimension MSE (D,), averaged over samples.
    """

    mask_ratio: float
    mse: float
    mae: float
    r2: float
    per_dim_mse: List[float] = field(default_factory=list)


class FillEvaluator:
    """Evaluate FillNet completion quality across mask ratios.

    Parameters
    ----------
    mask_ratios : tuple
        Mask ratios to evaluate (default (0.1, 0.3, 0.5, 0.7, 0.9)).
    n_trials : int
        Number of random masking trials per ratio (default 5).
    """

    def __init__(
        self,
        mask_ratios: tuple = (0.1, 0.3, 0.5, 0.7, 0.9),
        n_trials: int = 5,
    ) -> None:
        self.mask_ratios = mask_ratios
        self.n_trials = n_trials

    @torch.no_grad()
    def evaluate(
        self,
        fill_net: torch.nn.Module,
        c3_data: Tensor,
    ) -> Dict[float, FillEvalResult]:
        """Evaluate FillNet at multiple mask ratios.

        Parameters
        ----------
        fill_net : nn.Module
            The FillNet model.
        c3_data : Tensor
            Shape ``(B, T, 1006)`` complete C3 data (ground truth).

        Returns
        -------
        dict
            Maps mask ratio to FillEvalResult.
        """
        fill_net.eval()
        device = next(fill_net.parameters()).device
        c3_data = c3_data.to(device)

        results = {}
        for ratio in self.mask_ratios:
            trial_results = []
            for _ in range(self.n_trials):
                result = self._evaluate_single(fill_net, c3_data, ratio)
                trial_results.append(result)

            # Average across trials
            results[ratio] = FillEvalResult(
                mask_ratio=ratio,
                mse=sum(r.mse for r in trial_results) / len(trial_results),
                mae=sum(r.mae for r in trial_results) / len(trial_results),
                r2=sum(r.r2 for r in trial_results) / len(trial_results),
                per_dim_mse=self._average_per_dim(trial_results),
            )

        return results

    def _evaluate_single(
        self,
        fill_net: torch.nn.Module,
        c3_data: Tensor,
        mask_ratio: float,
    ) -> FillEvalResult:
        """Evaluate at a single mask ratio with one random mask."""
        B, T, D = c3_data.shape

        # Create mask at exact ratio
        rand = torch.rand(B, 1, D, device=c3_data.device)
        mask = (rand > mask_ratio).float().expand(B, T, D)

        c3_masked = c3_data * mask
        c3_filled = fill_net(c3_masked, mask)

        # Evaluate only on masked dimensions
        masked_dims = (1 - mask).bool()
        pred_masked = c3_filled[masked_dims]
        target_masked = c3_data[masked_dims]

        if pred_masked.numel() == 0:
            return FillEvalResult(mask_ratio=mask_ratio, mse=0.0, mae=0.0, r2=1.0)

        mse = ((pred_masked - target_masked) ** 2).mean().item()
        mae = (pred_masked - target_masked).abs().mean().item()

        ss_res = ((target_masked - pred_masked) ** 2).sum().item()
        ss_tot = ((target_masked - target_masked.mean()) ** 2).sum().item()
        r2 = 1.0 - ss_res / max(ss_tot, 1e-8)

        # Per-dimension MSE
        per_dim_mse = []
        inv_mask = 1 - mask  # (B, T, D)
        for d in range(D):
            dim_mask = inv_mask[:, :, d].bool()
            if dim_mask.any():
                dim_mse = ((c3_filled[:, :, d][dim_mask] - c3_data[:, :, d][dim_mask]) ** 2).mean().item()
            else:
                dim_mse = 0.0
            per_dim_mse.append(dim_mse)

        return FillEvalResult(
            mask_ratio=mask_ratio,
            mse=mse,
            mae=mae,
            r2=r2,
            per_dim_mse=per_dim_mse,
        )

    @staticmethod
    def _average_per_dim(results: List[FillEvalResult]) -> List[float]:
        """Average per-dimension MSE across trials."""
        if not results or not results[0].per_dim_mse:
            return []
        D = len(results[0].per_dim_mse)
        return [
            sum(r.per_dim_mse[d] for r in results) / len(results)
            for d in range(D)
        ]

    @staticmethod
    def format_results(results: Dict[float, FillEvalResult]) -> str:
        """Format results as a human-readable table."""
        lines = ["Fill-Net Evaluation", "=" * 55]
        lines.append(f"  {'Mask %':>8s} | {'MSE':>10s} | {'MAE':>10s} | {'R²':>8s}")
        lines.append("-" * 55)
        for ratio in sorted(results.keys()):
            r = results[ratio]
            lines.append(
                f"  {r.mask_ratio * 100:>7.1f}% | {r.mse:>10.6f} | "
                f"{r.mae:>10.6f} | {r.r2:>8.4f}"
            )
        lines.append("=" * 55)
        return "\n".join(lines)
