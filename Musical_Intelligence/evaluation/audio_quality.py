"""Audio quality metrics for decode direction evaluation.

Measures the quality of the neural MI-Core's decoded audio
(C3 → mel → waveform) against the original audio:

- Multi-Resolution STFT Distance (spectral fidelity)
- Mel Cepstral Distortion (MCD)
- Signal-to-Noise Ratio (SNR)

Optional (requires external packages):
- PESQ (Perceptual Evaluation of Speech Quality)
- STOI (Short-Time Objective Intelligibility)
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import torch
import torch.nn.functional as F
from torch import Tensor


@dataclass
class AudioQualityResult:
    """Audio quality metrics.

    Attributes:
        multi_res_stft: Multi-resolution STFT distance.
        mel_cepstral_distortion: Mel Cepstral Distortion in dB.
        snr: Signal-to-Noise Ratio in dB.
        pesq: PESQ score (if available).
        stoi: STOI score (if available).
    """

    multi_res_stft: float
    mel_cepstral_distortion: float
    snr: float
    pesq: Optional[float] = None
    stoi: Optional[float] = None


class AudioQualityEvaluator:
    """Evaluate audio quality of decoded/reconstructed waveforms.

    Parameters
    ----------
    sample_rate : int
        Audio sample rate (default 44100).
    stft_sizes : tuple
        FFT sizes for multi-resolution STFT (default (512, 1024, 2048)).
    """

    def __init__(
        self,
        sample_rate: int = 44100,
        stft_sizes: tuple = (512, 1024, 2048),
    ) -> None:
        self.sample_rate = sample_rate
        self.stft_sizes = stft_sizes

    def evaluate_mel(
        self,
        pred_mel: Tensor,
        target_mel: Tensor,
    ) -> float:
        """Compute Mel Cepstral Distortion between mel spectrograms.

        Parameters
        ----------
        pred_mel : Tensor
            Shape ``(B, T, N_MELS)`` predicted mel spectrogram.
        target_mel : Tensor
            Shape ``(B, T, N_MELS)`` target mel spectrogram.

        Returns
        -------
        float
            MCD in dB.
        """
        diff = pred_mel - target_mel
        mcd = (diff ** 2).sum(dim=-1).sqrt().mean()
        return mcd.item()

    def evaluate_waveform(
        self,
        pred_wav: Tensor,
        target_wav: Tensor,
    ) -> AudioQualityResult:
        """Evaluate waveform quality with multiple metrics.

        Parameters
        ----------
        pred_wav : Tensor
            Shape ``(B, T_samples)`` predicted waveform.
        target_wav : Tensor
            Shape ``(B, T_samples)`` reference waveform.

        Returns
        -------
        AudioQualityResult
        """
        # Truncate to same length
        min_len = min(pred_wav.shape[-1], target_wav.shape[-1])
        pred_wav = pred_wav[..., :min_len]
        target_wav = target_wav[..., :min_len]

        mr_stft = self._multi_res_stft(pred_wav, target_wav)
        mcd = self._mel_cepstral_distortion(pred_wav, target_wav)
        snr = self._snr(pred_wav, target_wav)

        # Optional external metrics
        pesq_score = self._try_pesq(pred_wav, target_wav)
        stoi_score = self._try_stoi(pred_wav, target_wav)

        return AudioQualityResult(
            multi_res_stft=mr_stft,
            mel_cepstral_distortion=mcd,
            snr=snr,
            pesq=pesq_score,
            stoi=stoi_score,
        )

    def _multi_res_stft(
        self, pred: Tensor, target: Tensor
    ) -> float:
        """Multi-resolution STFT distance."""
        total = 0.0
        for n_fft in self.stft_sizes:
            hop = n_fft // 4
            pred_stft = torch.stft(
                pred.reshape(-1, pred.shape[-1]),
                n_fft=n_fft,
                hop_length=hop,
                return_complex=True,
            )
            target_stft = torch.stft(
                target.reshape(-1, target.shape[-1]),
                n_fft=n_fft,
                hop_length=hop,
                return_complex=True,
            )

            # Spectral convergence
            sc = (
                (target_stft.abs() - pred_stft.abs()).norm()
                / target_stft.abs().norm().clamp(min=1e-8)
            )
            # Log STFT magnitude
            log_stft = F.l1_loss(
                torch.log(pred_stft.abs().clamp(min=1e-7)),
                torch.log(target_stft.abs().clamp(min=1e-7)),
            )
            total += sc.item() + log_stft.item()

        return total / len(self.stft_sizes)

    def _mel_cepstral_distortion(
        self, pred: Tensor, target: Tensor
    ) -> float:
        """Approximate MCD from waveform using STFT."""
        n_fft = 2048
        hop = 256
        pred_stft = torch.stft(
            pred.reshape(-1, pred.shape[-1]),
            n_fft=n_fft, hop_length=hop, return_complex=True,
        )
        target_stft = torch.stft(
            target.reshape(-1, target.shape[-1]),
            n_fft=n_fft, hop_length=hop, return_complex=True,
        )
        diff = torch.log(pred_stft.abs().clamp(min=1e-7)) - torch.log(
            target_stft.abs().clamp(min=1e-7)
        )
        mcd = (diff ** 2).sum(dim=-2).sqrt().mean()
        return mcd.item()

    @staticmethod
    def _snr(pred: Tensor, target: Tensor) -> float:
        """Signal-to-Noise Ratio in dB."""
        noise = pred - target
        signal_power = (target ** 2).mean()
        noise_power = (noise ** 2).mean().clamp(min=1e-10)
        snr = 10.0 * torch.log10(signal_power / noise_power)
        return snr.item()

    def _try_pesq(
        self, pred: Tensor, target: Tensor
    ) -> Optional[float]:
        """Try to compute PESQ score (requires pesq package)."""
        try:
            from pesq import pesq as pesq_fn

            pred_np = pred[0].cpu().numpy()
            target_np = target[0].cpu().numpy()
            sr = min(self.sample_rate, 16000)
            return pesq_fn(sr, target_np, pred_np, "wb")
        except (ImportError, Exception):
            return None

    def _try_stoi(
        self, pred: Tensor, target: Tensor
    ) -> Optional[float]:
        """Try to compute STOI score (requires pystoi package)."""
        try:
            from pystoi import stoi as stoi_fn

            pred_np = pred[0].cpu().numpy()
            target_np = target[0].cpu().numpy()
            return stoi_fn(target_np, pred_np, self.sample_rate)
        except (ImportError, Exception):
            return None
