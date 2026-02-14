"""MotorEncoder -- Encodes 7 heterogeneous motor channels into 256D.

Handles multiple input modalities (touch, MediaPipe, MIDI, gamepad,
accelerometer, emotion) with per-channel encoders fused into a
fixed 256D embedding. Missing channels are zero-filled.

Channel dimensions::

    touch:          3D  (x, y, pressure)
    mediapipe:     63D  (21 landmarks x 3D)
    midi_notes:   128D  (128 note velocities)
    midi_cc:      128D  (128 CC values)
    gamepad:        8D  (joysticks + triggers + buttons)
    accelerometer:  3D  (3-axis)
    emotion:        4D  (arousal, valence, tension, power)
    ─────────────────
    Total:        337D → per-channel (64D each) → fusion → 256D
"""
from __future__ import annotations

from typing import Dict

import torch
import torch.nn as nn
from torch import Tensor

from ..mi_space_layout import MOTOR_CHANNEL_DIMS, MOTOR_EMBED_DIM


class MotorEncoder(nn.Module):
    """Motor input encoder: 7 channels (337D) → 256D embedding.

    Each channel has an independent encoder (Linear → GELU → Linear → 64D).
    The 7 × 64D = 448D channel embeddings are fused via an MLP into 256D.

    Missing channels are zero-filled for graceful degradation.

    Parameters
    ----------
    channel_dims : dict
        Maps channel name to input dimension.
    embed_dim : int
        Output embedding dimension (default 256).
    channel_hidden : int
        Per-channel hidden dimension (default 64).
    """

    def __init__(
        self,
        channel_dims: Dict[str, int] | None = None,
        embed_dim: int = MOTOR_EMBED_DIM,
        channel_hidden: int = 64,
    ) -> None:
        super().__init__()
        if channel_dims is None:
            channel_dims = dict(MOTOR_CHANNEL_DIMS)

        self.channel_dims = channel_dims
        self.embed_dim = embed_dim
        self.channel_hidden = channel_hidden

        # Per-channel encoders
        self.channel_encoders = nn.ModuleDict({
            name: nn.Sequential(
                nn.Linear(dim, channel_hidden),
                nn.GELU(),
                nn.Linear(channel_hidden, channel_hidden),
            )
            for name, dim in channel_dims.items()
        })

        # Fusion MLP
        total_channel_dim = channel_hidden * len(channel_dims)
        self.fusion = nn.Sequential(
            nn.Linear(total_channel_dim, embed_dim),
            nn.LayerNorm(embed_dim),
            nn.GELU(),
            nn.Linear(embed_dim, embed_dim),
            nn.LayerNorm(embed_dim),
        )

    def forward(self, motor: Dict[str, Tensor]) -> Tensor:
        """Encode motor inputs.

        Parameters
        ----------
        motor : dict
            Maps channel name to tensor. Each tensor is ``(B, T, dim)``.
            Missing channels are zero-filled.

        Returns
        -------
        Tensor
            Shape ``(B, T, embed_dim)``.
        """
        # Determine B, T from any available channel
        sample_key = next(iter(motor))
        B, T = motor[sample_key].shape[:2]
        device = motor[sample_key].device

        encoded_channels = []
        for name, encoder in self.channel_encoders.items():
            if name in motor:
                encoded = encoder(motor[name])
            else:
                encoded = torch.zeros(
                    B, T, self.channel_hidden, device=device
                )
            encoded_channels.append(encoded)

        # Concatenate and fuse
        concat = torch.cat(encoded_channels, dim=-1)  # (B, T, 7*64)
        return self.fusion(concat)  # (B, T, 256)
