"""Logging utilities for MI-Core training.

Provides WandB integration and console logging for per-layer metrics.
"""
from __future__ import annotations

from typing import Any, Dict, Optional


class TrainingLogger:
    """Unified logging for MI-Core training.

    Supports console output and optional WandB integration.

    Parameters
    ----------
    project : str
        WandB project name.
    run_name : str, optional
        WandB run name.
    use_wandb : bool
        Whether to use WandB (default False).
    """

    def __init__(
        self,
        project: str = "mi-core-training",
        run_name: Optional[str] = None,
        use_wandb: bool = False,
    ) -> None:
        self._use_wandb = use_wandb
        self._wandb_run = None

        if use_wandb:
            try:
                import wandb
                self._wandb_run = wandb.init(
                    project=project,
                    name=run_name,
                )
            except ImportError:
                print("WandB not installed, falling back to console logging")
                self._use_wandb = False

    def log_metrics(
        self,
        metrics: Dict[str, Any],
        step: int,
        prefix: str = "",
    ) -> None:
        """Log metrics to console and optionally WandB.

        Parameters
        ----------
        metrics : dict
            Metric name → value.
        step : int
            Global step or epoch.
        prefix : str
            Prefix for metric names (e.g. "train/", "val/").
        """
        # Console
        parts = [f"{prefix}{k}={v:.4f}" if isinstance(v, float) else f"{prefix}{k}={v}"
                 for k, v in metrics.items()]
        print(f"  [step {step}] {' | '.join(parts)}")

        # WandB
        if self._use_wandb and self._wandb_run is not None:
            import wandb
            wandb.log(
                {f"{prefix}{k}": v for k, v in metrics.items()},
                step=step,
            )

    def finish(self) -> None:
        """Finish logging session."""
        if self._use_wandb and self._wandb_run is not None:
            import wandb
            wandb.finish()
