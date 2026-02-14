"""ExpertRouter -- Top-K expert routing with load balancing.

Routes backbone hidden states to 4 MI-aligned experts using a
learned gating network. Top-3 routing activates 3 of 4 experts
per token, keeping ~75% of expert parameters active.

Load balancing auxiliary loss prevents expert collapse
(all tokens routing to the same expert).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


@dataclass
class RouterOutput:
    """Output of the expert router.

    Attributes:
        weights:     ``(B, T, n_experts)`` routing weights (sparse, only top-k non-zero).
        indices:     ``(B, T, top_k)`` indices of selected experts.
        balance_loss: Scalar load balancing auxiliary loss.
    """

    weights: Tensor
    indices: Tensor
    balance_loss: Tensor


class ExpertRouter(nn.Module):
    """Top-K expert router with load balancing.

    Parameters
    ----------
    d_model : int
        Input dimension from backbone.
    n_experts : int
        Number of experts (default 4: Cochlea, R3, C3, L3).
    top_k : int
        Number of experts to activate per token (default 3).
    capacity_factor : float
        Expert capacity factor for load balancing (default 1.25).
    """

    def __init__(
        self,
        d_model: int = 2048,
        n_experts: int = 4,
        top_k: int = 3,
        capacity_factor: float = 1.25,
    ) -> None:
        super().__init__()
        self.n_experts = n_experts
        self.top_k = top_k
        self.capacity_factor = capacity_factor

        self.gate = nn.Linear(d_model, n_experts, bias=False)

    def forward(self, x: Tensor) -> RouterOutput:
        """Compute expert routing weights.

        Parameters
        ----------
        x : Tensor
            Shape ``(B, T, d_model)`` backbone hidden states.

        Returns
        -------
        RouterOutput
            Routing weights, selected indices, and balance loss.
        """
        B, T, D = x.shape

        # Gate logits
        logits = self.gate(x)  # (B, T, n_experts)
        probs = F.softmax(logits, dim=-1)

        # Top-K selection
        top_k_weights, top_k_indices = torch.topk(
            probs, self.top_k, dim=-1
        )  # Each (B, T, top_k)

        # Normalise selected weights to sum to 1
        top_k_weights = top_k_weights / top_k_weights.sum(dim=-1, keepdim=True)

        # Build sparse weight tensor
        weights = torch.zeros_like(probs)
        weights.scatter_(-1, top_k_indices, top_k_weights)

        # Load balancing loss (Switch Transformer style)
        balance_loss = self._compute_balance_loss(probs)

        return RouterOutput(
            weights=weights,
            indices=top_k_indices,
            balance_loss=balance_loss,
        )

    def _compute_balance_loss(self, probs: Tensor) -> Tensor:
        """Compute load balancing auxiliary loss.

        Encourages uniform expert utilisation across the batch.
        Loss = n_experts * sum_i(f_i * P_i) where:
        - f_i = fraction of tokens dispatched to expert i
        - P_i = average probability assigned to expert i
        """
        # f_i: fraction of tokens routing to each expert
        # Use argmax to determine primary expert assignment
        assignments = probs.argmax(dim=-1)  # (B, T)
        f = torch.zeros(self.n_experts, device=probs.device)
        for i in range(self.n_experts):
            f[i] = (assignments == i).float().mean()

        # P_i: mean probability per expert across all tokens
        P = probs.mean(dim=(0, 1))  # (n_experts,)

        # Balance loss: we want f and P both to be uniform (1/n_experts)
        balance_loss = self.n_experts * (f * P).sum()

        return balance_loss
