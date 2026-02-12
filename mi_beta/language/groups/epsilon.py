"""
epsilon (Epsilon) -- Learning Dynamics (19D)

Level 5: HOW the listener learns from the music over time.
STATEFUL: maintains online statistics across frames.

Surprise & Entropy (2D):
  eps0: surprise -- transition surprisal                     [Pearce 2005 IDyOM]
  eps1: entropy -- state uncertainty                         [Shannon 1948]

Prediction Errors (3D):
  eps2: pe_short -- short-term prediction error (~58ms)      [Koelsch 2019]
  eps3: pe_medium -- medium-term prediction error (~580ms)   [Koelsch 2019]
  eps4: pe_long -- long-term prediction error (~5.8s)        [Koelsch 2019]

Precision (2D):
  eps5: precision_short -- short-term confidence             [Friston 2010]
  eps6: precision_long -- long-term confidence               [Friston 2010]

Information Dynamics (3D):
  eps7: bayesian_surprise -- belief update magnitude         [Itti & Baldi 2009]
  eps8: information_rate -- mutual information past->present [Dubnov 2008]
  eps9: compression_progress -- learning rate as reward      [Schmidhuber 2009]

Interaction (1D):
  eps10: entropy_x_surprise -- pleasure predictor            [Cheung et al. 2019]

ITPRA (5D):
  eps11: imagination -- long-term pleasure baseline          [Huron 2006 ITPRA-I]
  eps12: tension_uncertainty -- entropy as tension           [Huron 2006 ITPRA-T]
  eps13: prediction_reward -- reward for correct prediction  [Huron 2006 ITPRA-P]
  eps14: reaction_magnitude -- surprise magnitude            [Huron 2006 ITPRA-R]
  eps15: appraisal_learning -- compression progress          [Huron 2006 ITPRA-A]

Reward & Aesthetics (3D):
  eps16: reward_pe -- reward prediction error                [Gold et al. 2019]
  eps17: wundt_position -- inverted-U optimal arousal        [Berlyne 1971]
  eps18: familiarity -- exposure accumulation                [Zajonc 1968]

In mi_beta, epsilon tracks two signals from BrainOutput:
  - "pleasure" (or mean activation as fallback)
  - "arousal" (or brain tensor variance as fallback)
"""

from __future__ import annotations

from typing import Any, List

import torch
from torch import Tensor

from ...contracts.base_semantic_group import BaseSemanticGroup, SemanticGroupOutput
from ...core.types import BrainOutput


def _safe_get_dim(brain_output: BrainOutput, name: str, default: float = 0.5) -> Tensor:
    """Safely extract a named dimension, returning default if not found."""
    try:
        return brain_output.get_dim(name)
    except (ValueError, KeyError):
        B, T, _ = brain_output.tensor.shape
        return torch.full(
            (B, T), default,
            device=brain_output.tensor.device,
            dtype=brain_output.tensor.dtype,
        )


class EpsilonGroup(BaseSemanticGroup):
    LEVEL = 5
    GROUP_NAME = "epsilon"
    DISPLAY_NAME = "epsilon"
    OUTPUT_DIM = 19

    # Hyperparameters
    ALPHA_SHORT: float = 0.1      # ~10 frames (~58ms)
    ALPHA_MEDIUM: float = 0.01    # ~100 frames (~580ms)
    ALPHA_LONG: float = 0.001     # ~1000 frames (~5.8s)
    N_STATES: int = 8             # Markov quantization bins
    BUFFER_SIZE: int = 50         # ring buffer for compression progress
    D_TRACK: int = 2              # pleasure + arousal
    EPS: float = 1e-8

    @property
    def dimension_names(self) -> List[str]:
        return [
            "surprise", "entropy",
            "pe_short", "pe_medium", "pe_long",
            "precision_short", "precision_long",
            "bayesian_surprise", "information_rate", "compression_progress",
            "entropy_x_surprise",
            "imagination", "tension_uncertainty",
            "prediction_reward", "reaction_magnitude", "appraisal_learning",
            "reward_pe", "wundt_position", "familiarity",
        ]

    def __init__(self) -> None:
        self._state_initialized = False

    def reset(self) -> None:
        """Clear all internal state. Call between audio files."""
        self._state_initialized = False

    def _init_state(self, B: int, device: torch.device, dtype: torch.dtype) -> None:
        """Lazily initialize state tensors for batch size B."""
        D = self.D_TRACK

        self._ema_short = torch.full((B, D), 0.5, device=device, dtype=dtype)
        self._ema_medium = torch.full((B, D), 0.5, device=device, dtype=dtype)
        self._ema_long = torch.full((B, D), 0.5, device=device, dtype=dtype)

        self._var_short = torch.full((B, D), 0.1, device=device, dtype=dtype)
        self._var_medium = torch.full((B, D), 0.1, device=device, dtype=dtype)
        self._var_long = torch.full((B, D), 0.1, device=device, dtype=dtype)

        self._welford_count = 0
        self._welford_mean = torch.full((B, D), 0.5, device=device, dtype=dtype)
        self._welford_m2 = torch.zeros(B, D, device=device, dtype=dtype)

        self._prev_state = torch.zeros(B, dtype=torch.long, device=device)
        self._transition_counts = torch.ones(
            B, self.N_STATES, self.N_STATES, device=device, dtype=dtype
        )

        self._buffer = torch.full(
            (B, self.BUFFER_SIZE), 0.5, device=device, dtype=dtype
        )
        self._buffer_idx = 0
        self._buffer_count = 0

        self._prev_pleasure = torch.full((B,), 0.5, device=device, dtype=dtype)

        self._state_initialized = True
        self._batch_size = B

    def compute(self, brain_output: Any, **kwargs: Any) -> SemanticGroupOutput:
        """Compute epsilon group with online state accumulation.

        Tracks pleasure and arousal from BrainOutput (with fallback).
        """
        tensor_full = brain_output.tensor  # (B, T, brain_dim)
        B, T, _ = tensor_full.shape
        device = tensor_full.device
        dtype = tensor_full.dtype

        if not self._state_initialized or self._batch_size != B:
            self._init_state(B, device, dtype)

        # Extract tracked features (with fallback)
        pleasure = _safe_get_dim(brain_output, "pleasure")
        arousal = _safe_get_dim(brain_output, "arousal")

        output = torch.zeros(B, T, self.OUTPUT_DIM, device=device, dtype=dtype)
        log2_n = torch.log2(torch.tensor(float(self.N_STATES), device=device))

        for t in range(T):
            x = pleasure[:, t]
            x_ar = arousal[:, t]
            tracked = torch.stack([x, x_ar], dim=-1)  # (B, 2)

            # EMA updates
            self._ema_short = (
                self.ALPHA_SHORT * tracked
                + (1 - self.ALPHA_SHORT) * self._ema_short
            )
            self._ema_medium = (
                self.ALPHA_MEDIUM * tracked
                + (1 - self.ALPHA_MEDIUM) * self._ema_medium
            )
            self._ema_long = (
                self.ALPHA_LONG * tracked
                + (1 - self.ALPHA_LONG) * self._ema_long
            )

            # EMA variance updates
            diff_s = tracked - self._ema_short
            self._var_short = (
                self.ALPHA_SHORT * diff_s.pow(2)
                + (1 - self.ALPHA_SHORT) * self._var_short
            )
            diff_m = tracked - self._ema_medium
            self._var_medium = (
                self.ALPHA_MEDIUM * diff_m.pow(2)
                + (1 - self.ALPHA_MEDIUM) * self._var_medium
            )
            diff_l = tracked - self._ema_long
            self._var_long = (
                self.ALPHA_LONG * diff_l.pow(2)
                + (1 - self.ALPHA_LONG) * self._var_long
            )

            # Welford global variance
            self._welford_count += 1
            delta_w = tracked - self._welford_mean
            self._welford_mean = self._welford_mean + delta_w / self._welford_count
            delta2_w = tracked - self._welford_mean
            self._welford_m2 = self._welford_m2 + delta_w * delta2_w

            # Markov transition model
            current_state = (x * (self.N_STATES - 1)).long().clamp(
                0, self.N_STATES - 1
            )
            row_sums = self._transition_counts[
                torch.arange(B, device=device), self._prev_state
            ].sum(dim=-1, keepdim=True)
            tp_row = self._transition_counts[
                torch.arange(B, device=device), self._prev_state
            ] / row_sums

            tp_observed = tp_row[torch.arange(B, device=device), current_state]
            surprise = (-torch.log2(tp_observed + self.EPS) / log2_n).clamp(0, 1)

            entropy = -(tp_row * torch.log2(tp_row + self.EPS)).sum(dim=-1) / log2_n
            entropy = entropy.clamp(0, 1)

            self._transition_counts[
                torch.arange(B, device=device),
                self._prev_state,
                current_state,
            ] += 1.0
            self._prev_state = current_state

            # Prediction errors
            sigma_s = (self._var_short[:, 0] + self.EPS).sqrt()
            sigma_m = (self._var_medium[:, 0] + self.EPS).sqrt()
            sigma_l = (self._var_long[:, 0] + self.EPS).sqrt()

            pe_s = torch.tanh(
                (x - self._ema_short[:, 0]) / (sigma_s + self.EPS)
            ) * 0.5 + 0.5
            pe_m = torch.tanh(
                (x - self._ema_medium[:, 0]) / (sigma_m + self.EPS)
            ) * 0.5 + 0.5
            pe_l = torch.tanh(
                (x - self._ema_long[:, 0]) / (sigma_l + self.EPS)
            ) * 0.5 + 0.5

            # Precision
            prec_s = 1.0 / (1.0 + self._var_short[:, 0])
            prec_l = 1.0 / (1.0 + self._var_long[:, 0])

            # Bayesian surprise
            abs_pe_m = (x - self._ema_medium[:, 0]).abs()
            bayes_surp = torch.sigmoid(abs_pe_m * prec_l * 5.0)

            # Information rate
            autocorr = (x * self._prev_pleasure).clamp(0, 1)
            info_rate = entropy * (1.0 - autocorr)
            self._prev_pleasure = x.detach().clone()

            # Compression progress
            self._buffer[:, self._buffer_idx] = x
            self._buffer_idx = (self._buffer_idx + 1) % self.BUFFER_SIZE
            self._buffer_count = min(self._buffer_count + 1, self.BUFFER_SIZE)

            if self._buffer_count >= self.BUFFER_SIZE:
                half = self.BUFFER_SIZE // 2
                idx_start = self._buffer_idx
                indices = torch.arange(self.BUFFER_SIZE, device=device)
                ordered_idx = (indices + idx_start) % self.BUFFER_SIZE
                ordered = self._buffer[:, ordered_idx]
                old_half = ordered[:, :half]
                new_half = ordered[:, half:]
                old_ent = self._buffer_entropy(old_half)
                new_ent = self._buffer_entropy(new_half)
                comp_prog = torch.sigmoid((old_ent - new_ent) * 5.0)
            else:
                comp_prog = torch.full((B,), 0.5, device=device, dtype=dtype)

            # Derived dimensions
            ent_x_surp = entropy * surprise
            imagination = self._ema_long[:, 0]
            tension_unc = entropy
            pred_reward = torch.exp(-abs_pe_m / (sigma_m + self.EPS))
            reaction_mag = (abs_pe_m * prec_l).clamp(0, 1)
            appraisal = comp_prog

            reward_pe = torch.tanh(
                x - self._ema_medium[:, 0]
            ) * 0.5 + 0.5
            wundt = 4.0 * surprise * (1.0 - surprise)
            familiarity = torch.log1p(
                self._transition_counts[
                    torch.arange(B, device=device), current_state
                ].sum(dim=-1)
            ) / torch.log1p(
                torch.tensor(
                    float(self._welford_count + 1), device=device, dtype=dtype,
                )
            )
            familiarity = familiarity.clamp(0, 1)

            # Assemble frame output
            output[:, t, 0] = surprise
            output[:, t, 1] = entropy
            output[:, t, 2] = pe_s
            output[:, t, 3] = pe_m
            output[:, t, 4] = pe_l
            output[:, t, 5] = prec_s
            output[:, t, 6] = prec_l
            output[:, t, 7] = bayes_surp
            output[:, t, 8] = info_rate
            output[:, t, 9] = comp_prog
            output[:, t, 10] = ent_x_surp
            output[:, t, 11] = imagination
            output[:, t, 12] = tension_unc
            output[:, t, 13] = pred_reward
            output[:, t, 14] = reaction_mag
            output[:, t, 15] = appraisal
            output[:, t, 16] = reward_pe
            output[:, t, 17] = wundt
            output[:, t, 18] = familiarity

        return SemanticGroupOutput(
            group_name=self.GROUP_NAME,
            level=self.LEVEL,
            tensor=output.clamp(0, 1),
            dimension_names=tuple(self.dimension_names),
        )

    def _buffer_entropy(self, values: Tensor) -> Tensor:
        """Compute entropy of buffer values via histogram."""
        B, W = values.shape
        bins = (values * (self.N_STATES - 1)).long().clamp(0, self.N_STATES - 1)
        counts = torch.zeros(
            B, self.N_STATES, device=values.device, dtype=values.dtype
        )
        for i in range(self.N_STATES):
            counts[:, i] = (bins == i).float().sum(dim=-1)
        probs = counts / W
        log2_n = torch.log2(
            torch.tensor(float(self.N_STATES), device=values.device)
        )
        ent = -(probs * torch.log2(probs + self.EPS)).sum(dim=-1) / log2_n
        return ent.clamp(0, 1)
