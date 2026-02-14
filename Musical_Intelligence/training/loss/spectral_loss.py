"""SpectralLoss -- Multi-resolution STFT loss for waveform comparison.

Used for the decode_wav loss term. Compares reconstructed waveform
against the original at multiple STFT resolutions.
"""
from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor


class MultiResolutionSTFTLoss(nn.Module):
    """Multi-resolution STFT loss.

    Computes spectral convergence + log magnitude loss at multiple
    FFT sizes for robust waveform comparison.

    Parameters
    ----------
    fft_sizes : tuple of int
        FFT window sizes (default (512, 1024, 2048)).
    hop_sizes : tuple of int
        Hop sizes (default (128, 256, 512)).
    win_sizes : tuple of int
        Window sizes (default (512, 1024, 2048)).
    """

    def __init__(
        self,
        fft_sizes: tuple = (512, 1024, 2048),
        hop_sizes: tuple = (128, 256, 512),
        win_sizes: tuple = (512, 1024, 2048),
    ) -> None:
        super().__init__()
        self.fft_sizes = fft_sizes
        self.hop_sizes = hop_sizes
        self.win_sizes = win_sizes

    def forward(self, pred: Tensor, target: Tensor) -> Tensor:
        """Compute multi-resolution STFT loss.

        Parameters
        ----------
        pred : Tensor
            Shape ``(B, samples)`` predicted waveform.
        target : Tensor
            Shape ``(B, samples)`` target waveform.

        Returns
        -------
        Tensor
            Scalar loss.
        """
        total_loss = pred.new_tensor(0.0)

        for fft_size, hop_size, win_size in zip(
            self.fft_sizes, self.hop_sizes, self.win_sizes
        ):
            window = torch.hann_window(win_size, device=pred.device)

            pred_stft = torch.stft(
                pred, fft_size, hop_size, win_size,
                window=window, return_complex=True,
            )
            target_stft = torch.stft(
                target, fft_size, hop_size, win_size,
                window=window, return_complex=True,
            )

            pred_mag = pred_stft.abs()
            target_mag = target_stft.abs()

            # Spectral convergence
            sc_loss = (
                (target_mag - pred_mag).norm(dim=(-2, -1))
                / target_mag.norm(dim=(-2, -1)).clamp(min=1e-8)
            ).mean()

            # Log magnitude
            log_loss = F.l1_loss(
                torch.log(pred_mag.clamp(min=1e-8)),
                torch.log(target_mag.clamp(min=1e-8)),
            )

            total_loss = total_loss + sc_loss + log_loss

        return total_loss / len(self.fft_sizes)
