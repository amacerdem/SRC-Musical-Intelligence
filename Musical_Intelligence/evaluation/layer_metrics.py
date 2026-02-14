"""Per-layer metrics for MI-Core evaluation.

Computes MSE, MAE, and R² at each pipeline layer (Mel, R3, H3, C3)
for both encode and decode directions, with optional per-unit C3
breakdown for the 9 cognitive units.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import torch
from torch import Tensor


@dataclass
class LayerMetric:
    """Metrics for a single pipeline layer.

    Attributes:
        name: Layer name (e.g. "encode_mel", "decode_r3").
        mse: Mean Squared Error.
        mae: Mean Absolute Error.
        r2: Coefficient of determination.
        dim: Dimensionality of this layer.
    """

    name: str
    mse: float
    mae: float
    r2: float
    dim: int


class LayerMetricsEvaluator:
    """Compute per-layer metrics for the MI pipeline.

    Tracks running statistics for both encode and decode directions.
    Can optionally break down C3 metrics by unit (9 cognitive units).

    Parameters
    ----------
    c3_unit_slices : dict, optional
        Maps unit name to ``(start, end)`` within the 1006D C3 space.
        If provided, per-unit C3 metrics will be computed.
    """

    def __init__(
        self,
        c3_unit_slices: Optional[Dict[str, Tuple[int, int]]] = None,
    ) -> None:
        self._c3_unit_slices = c3_unit_slices
        self._buffers: Dict[str, List[Tensor]] = {}

    def reset(self) -> None:
        """Clear all accumulated data."""
        self._buffers.clear()

    def _append(self, key: str, value: Tensor) -> None:
        if key not in self._buffers:
            self._buffers[key] = []
        self._buffers[key].append(value.detach().cpu())

    def update_encode(
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
        """Record one batch of encode direction predictions."""
        self._append("enc_mel_pred", pred_mel)
        self._append("enc_mel_tgt", target_mel)
        self._append("enc_r3_pred", pred_r3)
        self._append("enc_r3_tgt", target_r3)
        self._append("enc_c3_pred", pred_c3)
        self._append("enc_c3_tgt", target_c3)

        if pred_h3 is not None and target_h3 is not None:
            self._append("enc_h3_pred", pred_h3)
            self._append("enc_h3_tgt", target_h3)

    def update_decode(
        self,
        pred_h3: Tensor,
        pred_r3: Tensor,
        pred_mel: Tensor,
        target_h3: Tensor,
        target_r3: Tensor,
        target_mel: Tensor,
    ) -> None:
        """Record one batch of decode direction predictions."""
        self._append("dec_h3_pred", pred_h3)
        self._append("dec_h3_tgt", target_h3)
        self._append("dec_r3_pred", pred_r3)
        self._append("dec_r3_tgt", target_r3)
        self._append("dec_mel_pred", pred_mel)
        self._append("dec_mel_tgt", target_mel)

    def compute(self) -> Dict[str, LayerMetric]:
        """Compute all metrics.

        Returns
        -------
        dict
            Maps metric name to LayerMetric.
        """
        results: Dict[str, LayerMetric] = {}

        # Encode direction
        for key, name in [
            ("enc_mel", "encode_mel"),
            ("enc_r3", "encode_r3"),
            ("enc_h3", "encode_h3"),
            ("enc_c3", "encode_c3"),
        ]:
            pred_key = f"{key}_pred"
            tgt_key = f"{key}_tgt"
            if pred_key in self._buffers:
                pred = torch.cat(self._buffers[pred_key], dim=0)
                tgt = torch.cat(self._buffers[tgt_key], dim=0)
                results[name] = self._compute_metric(name, pred, tgt)

        # Decode direction
        for key, name in [
            ("dec_h3", "decode_h3"),
            ("dec_r3", "decode_r3"),
            ("dec_mel", "decode_mel"),
        ]:
            pred_key = f"{key}_pred"
            tgt_key = f"{key}_tgt"
            if pred_key in self._buffers:
                pred = torch.cat(self._buffers[pred_key], dim=0)
                tgt = torch.cat(self._buffers[tgt_key], dim=0)
                results[name] = self._compute_metric(name, pred, tgt)

        # Per-unit C3 breakdown
        if self._c3_unit_slices and "enc_c3_pred" in self._buffers:
            pred = torch.cat(self._buffers["enc_c3_pred"], dim=0)
            tgt = torch.cat(self._buffers["enc_c3_tgt"], dim=0)
            for unit_name, (start, end) in self._c3_unit_slices.items():
                key = f"encode_c3/{unit_name}"
                results[key] = self._compute_metric(
                    key,
                    pred[..., start:end],
                    tgt[..., start:end],
                )

        return results

    @staticmethod
    def _compute_metric(
        name: str, pred: Tensor, target: Tensor
    ) -> LayerMetric:
        """Compute MSE, MAE, R² for a prediction-target pair."""
        pred_flat = pred.reshape(-1, pred.shape[-1])
        tgt_flat = target.reshape(-1, target.shape[-1])

        mse = ((pred_flat - tgt_flat) ** 2).mean().item()
        mae = (pred_flat - tgt_flat).abs().mean().item()

        ss_res = ((tgt_flat - pred_flat) ** 2).sum().item()
        ss_tot = (
            (tgt_flat - tgt_flat.mean(dim=0, keepdim=True)) ** 2
        ).sum().item()
        r2 = 1.0 - ss_res / max(ss_tot, 1e-8)

        return LayerMetric(
            name=name,
            mse=mse,
            mae=mae,
            r2=r2,
            dim=pred.shape[-1],
        )

    @staticmethod
    def format_results(results: Dict[str, LayerMetric]) -> str:
        """Format results as a human-readable table."""
        lines = ["Per-Layer Metrics", "=" * 65]
        lines.append(f"  {'Layer':<25s} | {'MSE':>10s} | {'MAE':>10s} | {'R²':>8s} | {'D':>4s}")
        lines.append("-" * 65)
        for name, m in sorted(results.items()):
            lines.append(
                f"  {m.name:<25s} | {m.mse:>10.6f} | {m.mae:>10.6f} | "
                f"{m.r2:>8.4f} | {m.dim:>4d}"
            )
        lines.append("=" * 65)
        return "\n".join(lines)
