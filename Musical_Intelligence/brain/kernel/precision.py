"""PrecisionEngine — PCU role in C³ v1.0.

PCU is NOT a belief owner.  It estimates precision_pred for each belief
and maintains PE history.  It never writes belief values.

RFC §2.2:
  precision_pred_i = g(belief_stability_i, τ_i, PE_history_consistency_i)

v1.0: fixed τ=0.6, pe_history_window=32 frames, stability_decay=0.95.
"""
from __future__ import annotations

from typing import Dict

import torch
from torch import Tensor


class PrecisionEngine:
    """Estimates prediction confidence for each belief.

    Maintains a sliding window of PE magnitudes per belief.
    Higher stability + longer PE history consistency → higher precision_pred.
    """

    def __init__(
        self,
        tau: float = 0.6,
        pe_window: int = 32,
        stability_decay: float = 0.95,
    ) -> None:
        self.tau = tau
        self.pe_window = pe_window
        self.stability_decay = stability_decay
        self._pe_history: Dict[str, Tensor] = {}  # belief_name → (window,) ring
        self._pe_idx: Dict[str, int] = {}          # current write index
        self._precision_prev: Dict[str, Tensor] = {}

    def reset(self) -> None:
        """Clear all history (new piece/session)."""
        self._pe_history.clear()
        self._pe_idx.clear()
        self._precision_prev.clear()

    def record_pe(self, belief_name: str, pe: Tensor) -> None:
        """Record a new prediction error magnitude for a belief.

        Args:
            belief_name: Which belief this PE belongs to.
            pe: Prediction error tensor, shape (B, T).
               We store the mean |PE| across batch and time.
        """
        pe_mag = pe.abs().mean().item()

        if belief_name not in self._pe_history:
            self._pe_history[belief_name] = torch.zeros(self.pe_window)
            self._pe_idx[belief_name] = 0

        idx = self._pe_idx[belief_name] % self.pe_window
        self._pe_history[belief_name][idx] = pe_mag
        self._pe_idx[belief_name] += 1

    def estimate_precision_pred(
        self,
        belief_name: str,
        belief_tau: float,
    ) -> Tensor:
        """Estimate prediction confidence for a belief.

        Higher precision_pred when:
          - PE history is consistently low (good predictions)
          - Belief tau is high (slow, stable beliefs are more predictable)
          - History is long (more evidence)

        Returns:
            Scalar tensor in [0.01, 10.0].
        """
        if belief_name not in self._pe_history:
            # No history yet — return moderate precision
            return torch.tensor(1.0)

        history = self._pe_history[belief_name]
        n_filled = min(self._pe_idx[belief_name], self.pe_window)

        if n_filled < 2:
            return torch.tensor(1.0)

        filled = history[:n_filled]
        pe_mean = filled.mean()
        pe_std = filled.std()

        # Stability: inverse of recent PE magnitude
        # High PE → low stability → low precision_pred
        stability = 1.0 / (pe_mean + 0.1)

        # Consistency: inverse of PE variance
        # Erratic PE → low consistency → low precision_pred
        consistency = 1.0 / (pe_std + 0.1)

        # Tau bonus: slow beliefs (high tau) are more predictable
        tau_factor = 0.5 + belief_tau  # range [0.5, 1.5]

        # Fill factor: more history → more confident estimate
        fill_factor = n_filled / self.pe_window

        precision_pred = stability * consistency * tau_factor * fill_factor

        # EMA smooth with previous estimate
        prev = self._precision_prev.get(belief_name, precision_pred)
        precision_pred = self.tau * prev + (1.0 - self.tau) * precision_pred
        self._precision_prev[belief_name] = precision_pred

        return precision_pred.clamp(0.01, 10.0)
