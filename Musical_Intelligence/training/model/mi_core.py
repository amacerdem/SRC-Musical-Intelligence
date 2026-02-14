"""MICore -- Bidirectional Musical Intelligence Model (~250M params).

The central neural model that learns to both analyse (encode) and
compose (decode) through every layer of the MI pipeline:

- ENCODE: Waveform → Mel → R3 → H3 → C3  (analysis)
- DECODE: C3 → H3 → R3 → Mel → Waveform  (synthesis)
- FILL:   C3_partial → C3_complete          (user intent completion)

All modes share the same Mamba-2 + Sparse Attention backbone.

Architecture::

    Encode: mel → MelEncoder → Backbone → Experts → StateHead → 1366D
                                        ↘ H3AuxHead → ~5210D (training only)

    Decode: c3 → C3Decoder → Backbone → DecodeHeads → {H3, R3, Mel}

    Fill:   c3_masked → FillNet → c3_filled

Reference: MI-VISION Sections 4, 12, 13
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

import torch
import torch.nn as nn
from torch import Tensor

from .backbone.hybrid_backbone import HybridBackbone
from .decoder.c3_decoder import C3Decoder
from .decoder.decode_heads import DecodeH3Head, DecodeMelHead, DecodeR3Head
from .decoder.vocoder_wrapper import VocoderWrapper
from .encoder.mel_encoder import MelEncoder
from .experts.c3_expert import C3Expert
from .experts.cochlea_expert import CochleaExpert
from .experts.cross_expert_refinement import CrossExpertRefinement
from .experts.l3_expert import L3Expert
from .experts.r3_expert import R3Expert
from .experts.router import ExpertRouter
from .fill_net.fill_net import FillNet
from .heads.h3_aux_head import H3AuxiliaryHead
from .heads.planning_head import PlanningHead
from .heads.state_head import StateHead
from .heads.uncertainty_head import UncertaintyHead
from .mi_space_layout import (
    BACKBONE_HIDDEN_DIM,
    BACKBONE_N_LAYERS,
    C3_DIM,
    C3_SLICE,
    COCHLEA_DIM,
    COCHLEA_SLICE,
    H3_AUX_DIM,
    L3_DIM,
    L3_SLICE,
    MAMBA_CONV_KERNEL,
    MAMBA_EXPAND,
    MAMBA_STATE_DIM,
    MI_SPACE_DIM,
    R3_DIM,
    R3_SLICE,
    SPARSE_ATTN_EVERY,
    SPARSE_ATTN_GLOBAL_TOKENS,
    SPARSE_ATTN_N_HEADS,
    SPARSE_ATTN_WINDOW,
)


# ======================================================================
# Output dataclasses
# ======================================================================

@dataclass
class EncodeOutput:
    """Output of the encode (analysis) forward pass.

    Attributes:
        mi_space:     ``(B, T, 1366)`` full MI-space state.
        cochlea_hat:  ``(B, T, 128)`` predicted mel.
        r3_hat:       ``(B, T, 128)`` predicted R3.
        c3_hat:       ``(B, T, 1006)`` predicted C3.
        l3_hat:       ``(B, T, 104)`` predicted L3.
        h3_hat:       ``(B, T, ~5210)`` predicted H3 (training only).
        hidden:       ``(B, T, d_model)`` backbone hidden state.
        uncertainty:  ``(B, T, 1366)`` per-dim confidence.
        planning:     ``(B, T, K, 1366)`` future trajectory.
        balance_loss: Scalar expert routing balance loss.
    """

    mi_space: Tensor
    cochlea_hat: Tensor
    r3_hat: Tensor
    c3_hat: Tensor
    l3_hat: Tensor
    h3_hat: Optional[Tensor]
    hidden: Tensor
    uncertainty: Tensor
    planning: Tensor
    balance_loss: Tensor


@dataclass
class DecodeOutput:
    """Output of the decode (synthesis) forward pass.

    Attributes:
        h3_rec:  ``(B, T, ~5210)`` reconstructed H3.
        r3_rec:  ``(B, T, 128)`` reconstructed R3.
        mel_rec: ``(B, T, 128)`` reconstructed mel.
        hidden:  ``(B, T, d_model)`` backbone hidden state.
    """

    h3_rec: Tensor
    r3_rec: Tensor
    mel_rec: Tensor
    hidden: Tensor


# ======================================================================
# MICore Model
# ======================================================================

class MICore(nn.Module):
    """Bidirectional Musical Intelligence model.

    Three forward modes:
    - ``encode(mel)`` → EncodeOutput (analysis direction)
    - ``decode(c3)``  → DecodeOutput (synthesis direction)
    - ``fill(c3_masked, mask)`` → c3_filled (completion)

    All modes share the same backbone.

    Parameters
    ----------
    d_model : int
        Backbone hidden dimension (default 2048).
    n_layers : int
        Total backbone layers (default 24).
    dropout : float
        Dropout rate (default 0.0).
    """

    def __init__(
        self,
        d_model: int = BACKBONE_HIDDEN_DIM,
        n_layers: int = BACKBONE_N_LAYERS,
        dropout: float = 0.0,
    ) -> None:
        super().__init__()
        self.d_model = d_model

        # ── Backbone ──
        self.backbone = HybridBackbone(
            d_model=d_model,
            n_layers=n_layers,
            d_state=MAMBA_STATE_DIM,
            d_conv=MAMBA_CONV_KERNEL,
            expand=MAMBA_EXPAND,
            attn_every=SPARSE_ATTN_EVERY,
            attn_window=SPARSE_ATTN_WINDOW,
            attn_global_tokens=SPARSE_ATTN_GLOBAL_TOKENS,
            n_heads=SPARSE_ATTN_N_HEADS,
            dropout=dropout,
        )

        # ── Encoder (analysis direction) ──
        self.mel_encoder = MelEncoder(COCHLEA_DIM, d_model)

        # ── Experts (4 MI-aligned) ──
        self.experts = nn.ModuleList([
            CochleaExpert(d_model, dropout),  # 128D
            R3Expert(d_model, dropout),       # 128D
            C3Expert(d_model, dropout),       # 1006D
            L3Expert(d_model, dropout),       # 104D
        ])
        self.router = ExpertRouter(d_model, n_experts=4, top_k=3)
        self.cross_expert = CrossExpertRefinement(dropout=dropout)

        # ── Heads ──
        self.state_head = StateHead(MI_SPACE_DIM, d_model)
        self.planning_head = PlanningHead(d_model)
        self.uncertainty_head = UncertaintyHead(d_model)
        self.h3_aux_head = H3AuxiliaryHead(d_model, H3_AUX_DIM)

        # ── Decoder (synthesis direction) ──
        self.c3_decoder_proj = C3Decoder(C3_DIM, d_model)
        self.decode_h3 = DecodeH3Head(d_model, H3_AUX_DIM)
        self.decode_r3 = DecodeR3Head(d_model, R3_DIM)
        self.decode_mel = DecodeMelHead(d_model, COCHLEA_DIM)

        # ── Fill-Net ──
        self.fill_net = FillNet(C3_DIM)

    # ------------------------------------------------------------------
    # Encode (Analysis)
    # ------------------------------------------------------------------

    def encode(
        self,
        mel: Tensor,
        states: Optional[Dict[int, Tensor]] = None,
    ) -> EncodeOutput:
        """Forward encode: mel → MI-space.

        Parameters
        ----------
        mel : Tensor
            Shape ``(B, T, 128)`` mel spectrogram (time-first).
        states : dict, optional
            Mamba states from previous forward pass.

        Returns
        -------
        EncodeOutput
        """
        # Project mel to backbone space
        x = self.mel_encoder(mel)  # (B, T, d_model)

        # Backbone
        hidden, new_states = self.backbone(x, states)  # (B, T, d_model)

        # Expert routing
        router_out = self.router(hidden)

        # Run all experts
        expert_outputs = [expert(hidden) for expert in self.experts]

        # Weight by routing
        for i, expert_out in enumerate(expert_outputs):
            weight = router_out.weights[:, :, i : i + 1]  # (B, T, 1)
            expert_outputs[i] = expert_out * weight

        # Cross-expert refinement
        expert_outputs = self.cross_expert(expert_outputs)

        # State head: combine into 1366D MI-space
        mi_space = self.state_head(expert_outputs)

        # H3 auxiliary (training only)
        h3_hat = self.h3_aux_head(hidden)

        # Planning and uncertainty
        planning = self.planning_head(hidden)
        uncertainty = self.uncertainty_head(hidden)

        return EncodeOutput(
            mi_space=mi_space,
            cochlea_hat=mi_space[:, :, COCHLEA_SLICE],
            r3_hat=mi_space[:, :, R3_SLICE],
            c3_hat=mi_space[:, :, C3_SLICE],
            l3_hat=mi_space[:, :, L3_SLICE],
            h3_hat=h3_hat,
            hidden=hidden,
            uncertainty=uncertainty,
            planning=planning,
            balance_loss=router_out.balance_loss,
        )

    # ------------------------------------------------------------------
    # Decode (Synthesis)
    # ------------------------------------------------------------------

    def decode(
        self,
        c3: Tensor,
        states: Optional[Dict[int, Tensor]] = None,
    ) -> DecodeOutput:
        """Forward decode: C3 → {H3, R3, Mel}.

        Parameters
        ----------
        c3 : Tensor
            Shape ``(B, T, 1006)`` C3 cognitive output.
        states : dict, optional
            Mamba states from previous forward pass.

        Returns
        -------
        DecodeOutput
        """
        # Project C3 to backbone space
        x = self.c3_decoder_proj(c3)  # (B, T, d_model)

        # Backbone (shared with encode)
        hidden, new_states = self.backbone(x, states)  # (B, T, d_model)

        # Decode heads: reconstruct each layer
        h3_rec = self.decode_h3(hidden)   # (B, T, ~5210)
        r3_rec = self.decode_r3(hidden)   # (B, T, 128)
        mel_rec = self.decode_mel(hidden)  # (B, T, 128)

        return DecodeOutput(
            h3_rec=h3_rec,
            r3_rec=r3_rec,
            mel_rec=mel_rec,
            hidden=hidden,
        )

    # ------------------------------------------------------------------
    # Fill (C3 Completion)
    # ------------------------------------------------------------------

    def fill(self, c3_masked: Tensor, mask: Tensor) -> Tensor:
        """Complete masked C3 dimensions.

        Parameters
        ----------
        c3_masked : Tensor
            Shape ``(B, T, 1006)`` with masked dims zeroed.
        mask : Tensor
            Shape ``(B, T, 1006)`` binary (1=known, 0=masked).

        Returns
        -------
        Tensor
            Shape ``(B, T, 1006)`` completed C3.
        """
        return self.fill_net(c3_masked, mask)

    # ------------------------------------------------------------------
    # H3 Aux Pruning
    # ------------------------------------------------------------------

    def prune_h3_aux(self) -> None:
        """Remove the H3 auxiliary head after training.

        Saves parameters and memory for inference. The backbone
        retains temporal awareness through its Mamba state.
        """
        self.h3_aux_head = None

    # ------------------------------------------------------------------
    # Utilities
    # ------------------------------------------------------------------

    @property
    def param_count(self) -> int:
        """Total parameter count."""
        return sum(p.numel() for p in self.parameters())

    @property
    def trainable_param_count(self) -> int:
        """Trainable parameter count."""
        return sum(p.numel() for p in self.parameters() if p.requires_grad)

    def __repr__(self) -> str:
        total = self.param_count
        trainable = self.trainable_param_count
        return (
            f"MICore(d_model={self.d_model}, "
            f"params={total / 1e6:.1f}M, "
            f"trainable={trainable / 1e6:.1f}M)"
        )
