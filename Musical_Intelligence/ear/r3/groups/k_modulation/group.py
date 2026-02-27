from __future__ import annotations
import math
import torch
from torch import Tensor
from .....contracts.bases.base_spectral_group import BaseSpectralGroup

# Frame rate and modulation FFT parameters
_FRAME_RATE = 172.27  # Hz
_MOD_WINDOW = 344     # frames (~2.0s)
_MOD_HOP = 86         # frames (~0.5s, 75% overlap)
_FFT_SIZE = 512
_FREQ_RES = _FRAME_RATE / _FFT_SIZE  # ~0.336 Hz

# Target modulation rates and their FFT bin indices
_MOD_RATES = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0]  # Hz
_MOD_BINS = [round(r / _FREQ_RES) for r in _MOD_RATES]  # [1, 3, 6, 12, 24, 48]


def _build_bark_matrix(n_mels: int = 128) -> Tensor:
    """Build mel-to-24-Bark-band rebinning matrix."""
    f_min, f_max = 0.0, 22050.0
    mel_min = 2595.0 * math.log10(1.0 + f_min / 700.0)
    mel_max = 2595.0 * math.log10(1.0 + f_max / 700.0)
    mels = torch.linspace(mel_min, mel_max, n_mels)
    freqs = 700.0 * (10.0 ** (mels / 2595.0) - 1.0)

    matrix = torch.zeros(n_mels, 24)
    for k in range(n_mels):
        f = freqs[k].item()
        z = 13.0 * math.atan(0.00076 * f) + 3.5 * math.atan((f / 7500.0) ** 2)
        z_int = int(z)
        if 0 <= z_int < 24:
            frac = z - z_int
            matrix[k, z_int] = 1.0 - frac
            if z_int + 1 < 24:
                matrix[k, z_int + 1] = frac
    return matrix


def _build_a_weights(n_mels: int = 128) -> Tensor:
    """Build A-weighting curve per mel bin (IEC 61672-1)."""
    f_min, f_max = 0.0, 22050.0
    mel_min = 2595.0 * math.log10(1.0 + f_min / 700.0)
    mel_max = 2595.0 * math.log10(1.0 + f_max / 700.0)
    mels = torch.linspace(mel_min, mel_max, n_mels)
    freqs = 700.0 * (10.0 ** (mels / 2595.0) - 1.0)

    weights = torch.zeros(n_mels)
    for k in range(n_mels):
        f = max(freqs[k].item(), 1.0)
        f2 = f * f
        num = 12194.0**2 * f2**2
        den = (f2 + 20.6**2) * (f2 + 12194.0**2) * math.sqrt((f2 + 107.7**2) * (f2 + 737.9**2))
        ra = num / max(den, 1e-12)
        a_db = 20.0 * math.log10(max(ra, 1e-12)) + 2.0
        weights[k] = 10.0 ** (a_db / 20.0)  # linear amplitude weighting

    # Normalize so max weight = 1
    weights = weights / weights.max().clamp(min=1e-8)
    return weights


def _zwicker_g_weights(n_bark: int = 24) -> Tensor:
    """Zwicker sharpness weighting function g(z)."""
    g = torch.ones(n_bark)
    for z in range(n_bark):
        if z >= 15:  # Bark > 15: increasing weight
            g[z] = 0.066 * math.exp(0.171 * (z + 1))
    return g


class ModulationGroup(BaseSpectralGroup):
    GROUP_NAME = "modulation"
    DOMAIN = "psychoacoustic"
    OUTPUT_DIM = 14
    INDEX_RANGE = (83, 97)
    STAGE = 1
    DEPENDENCIES = ()

    def __init__(self):
        super().__init__()
        self._bark_matrix = _build_bark_matrix()       # (128, 24)
        self._a_weights = _build_a_weights()            # (128,)
        self._g_weights = _zwicker_g_weights()          # (24,)
        self._hann = torch.hann_window(_MOD_WINDOW)     # (344,)

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        eps = 1e-8
        mt = mel.transpose(1, 2)  # (B, T, 128)
        device, dtype = mel.device, mel.dtype

        bark_mat = self._bark_matrix.to(device, dtype)
        a_wt = self._a_weights.to(device, dtype)
        g_wt = self._g_weights.to(device, dtype)
        hann = self._hann.to(device, dtype)

        # ---- Modulation spectrum [114-121] ----
        # Average mel across frequency to get temporal envelope
        envelope = mt.mean(dim=-1)  # (B, T)

        # Sliding window FFT for modulation rates
        mod_energies = torch.zeros(B, T, 6, device=device, dtype=dtype)

        if T >= _MOD_WINDOW:
            n_windows = (T - _MOD_WINDOW) // _MOD_HOP + 1
            for w in range(n_windows):
                start = w * _MOD_HOP
                end = start + _MOD_WINDOW
                center = (start + end) // 2

                segment = envelope[:, start:end] * hann  # (B, 344)
                # Zero-pad to FFT size
                padded = torch.zeros(B, _FFT_SIZE, device=device, dtype=dtype)
                padded[:, :_MOD_WINDOW] = segment

                spectrum = torch.fft.rfft(padded, dim=-1).abs()  # (B, 257)

                for i, bin_idx in enumerate(_MOD_BINS):
                    if bin_idx < spectrum.shape[-1]:
                        mod_energies[:, center, i] = spectrum[:, bin_idx]

            # Per-rate max-norm
            for i in range(6):
                rate_max = mod_energies[:, :, i].amax(dim=-1, keepdim=True).clamp(min=eps)
                mod_energies[:, :, i] = mod_energies[:, :, i] / rate_max
        # else: all zeros (warmup not met)

        # [120] modulation_centroid: weighted mean of log2(rates)
        log2_rates = torch.tensor([math.log2(r) for r in _MOD_RATES], device=device, dtype=dtype)
        mod_sum = mod_energies.sum(dim=-1).clamp(min=eps)  # (B, T)
        mod_centroid = (mod_energies * log2_rates).sum(dim=-1) / mod_sum
        # Min-max [-1, 4] -> [0, 1]
        mod_centroid = (mod_centroid - (-1.0)) / (4.0 - (-1.0))
        mod_centroid = mod_centroid.clamp(0, 1)

        # [121] modulation_bandwidth: weighted std of log2(rates)
        mean_lr = (mod_energies * log2_rates).sum(dim=-1) / mod_sum
        var_lr = (mod_energies * (log2_rates - mean_lr.unsqueeze(-1)).pow(2)).sum(dim=-1) / mod_sum
        mod_bw = var_lr.sqrt() / 2.5
        mod_bw = mod_bw.clamp(0, 1)

        # ---- Psychoacoustic features [122-127] ----

        # [122] sharpness_zwicker: DIN 45692
        bark = torch.matmul(mt, bark_mat)  # (B, T, 24)
        bark_total = bark.sum(dim=-1).clamp(min=eps)
        z_indices = torch.arange(1, 25, device=device, dtype=dtype)
        sharpness = 0.11 * (bark * g_wt * z_indices).sum(dim=-1) / bark_total
        sharpness = (sharpness / 4.0).clamp(0, 1)

        # [123] fluctuation_strength: = 4Hz modulation energy (index 3)
        fluctuation = mod_energies[:, :, 3]  # already [0,1] from max-norm

        # [124] loudness_a_weighted: A-weighted mel, sum, max-norm
        a_mel = mt * a_wt  # (B, T, 128)
        loudness_aw = a_mel.sum(dim=-1)
        loudness_aw = loudness_aw / loudness_aw.amax(dim=-1, keepdim=True).clamp(min=eps)

        # [125] alpha_ratio: low(0-1kHz) / (low+high)
        # Approximate: bins 0-42 ≈ 0-1kHz (mel scale)
        low = mt[:, :, :43].sum(dim=-1)
        high = mt[:, :, 43:].sum(dim=-1)
        alpha = low / (low + high).clamp(min=eps)

        # [126] hammarberg_index: peak(0-2kHz) / peak(2-5kHz) in log, sigmoid
        # bins 0-68 ≈ 0-2kHz, bins 68-100 ≈ 2-5kHz
        peak_low = mt[:, :, :69].max(dim=-1).values
        peak_high = mt[:, :, 69:101].max(dim=-1).values.clamp(min=eps)
        hammarberg = torch.sigmoid(peak_low / peak_high / 5.0)

        # [127] spectral_slope_0_500Hz: regression slope bins 0-17, sigmoid
        # bins 0-17 ≈ 0-500Hz
        x = torch.arange(18, device=device, dtype=dtype)
        x_mean = x.mean()
        x_var = ((x - x_mean) ** 2).sum()
        y = mt[:, :, :18]  # (B, T, 18)
        y_mean = y.mean(dim=-1, keepdim=True)
        slope = ((y - y_mean) * (x - x_mean)).sum(dim=-1) / x_var.clamp(min=eps)
        spec_slope = torch.sigmoid(slope * 10.0)

        return torch.stack([
            mod_energies[:, :, 0], mod_energies[:, :, 1], mod_energies[:, :, 2],
            mod_energies[:, :, 3], mod_energies[:, :, 4], mod_energies[:, :, 5],
            mod_centroid, mod_bw,
            sharpness, fluctuation, loudness_aw,
            alpha, hammarberg, spec_slope,
        ], dim=-1).clamp(0, 1)  # (B, T, 14)

    @property
    def feature_names(self):
        return (
            "modulation_0_5Hz", "modulation_1Hz", "modulation_2Hz",
            "modulation_4Hz", "modulation_8Hz", "modulation_16Hz",
            "modulation_centroid", "modulation_bandwidth",
            "sharpness_zwicker", "fluctuation_strength",
            "loudness_a_weighted", "alpha_ratio",
            "hammarberg_index", "spectral_slope_0_500",
        )
