"""ConsonanceGroup — Psychoacoustic consonance features (R³ indices [0:7]).

When raw audio is available (via ``compute_from_audio``), uses real
psychoacoustic models:

    [0] roughness          Plomp-Levelt / Sethares pairwise roughness
    [1] sethares_dissonance Sethares 1993 total dissonance (2nd ed. params)
    [2] helmholtz_kang     Harmonic template matching (HPS-based F0)
    [3] stumpf_fusion      Harmonicity ratio (harmonic vs total energy)
    [4] sensory_pleasantness 0.6*(1-sethares) + 0.4*stumpf
    [5] inharmonicity      1 - stumpf
    [6] harmonic_deviation Partial amplitude deviation from 1/n decay

When only mel is available, falls back to the original mel-based proxy
computation (unchanged from Phase 2).

Scientific sources:
    Plomp & Levelt 1965     — critical bandwidth roughness curve
    Sethares 1993, 2005     — pairwise dissonance model (TTSS 2nd ed.)
    Zwicker & Fastl 2007    — critical bandwidth formula
    Bidelman & Krishnan 2009 — consonance hierarchy: P1>P5>P4>M3>m6>TT
"""
from __future__ import annotations

import math

import torch
from torch import Tensor

from .....contracts.bases.base_spectral_group import BaseSpectralGroup

# ======================================================================
# Sethares 1993 constants (2nd edition / Sethares' own code)
# Source: sethares.engr.wisc.edu/comprog.html
# ======================================================================
_DSTAR: float = 0.24      # max dissonance point as fraction of CB
_S1: float = 0.0207       # linear frequency scaling coefficient
_S2: float = 18.96        # constant offset
_C1: float = 5.0          # first exponential amplitude
_C2: float = -5.0         # second exponential amplitude
_A1: float = -3.51        # first exponential decay rate
_A2: float = -5.75        # second exponential decay rate

# Peak picking
_N_FFT: int = 4096        # ~10.7 Hz resolution at 44100 Hz
_TOP_K: int = 20          # max peaks per frame
_MIN_PEAK_DB: float = -60.0  # ignore peaks below this threshold (dB re max)

# Harmonicity
_HPS_R: int = 5           # harmonic product spectrum downsample orders
_F0_MIN: float = 50.0     # Hz — minimum F0 candidate
_F0_MAX: float = 2000.0   # Hz — maximum F0 candidate
_HARM_TOL: float = 0.05   # 5% tolerance for harmonic classification


class ConsonanceGroup(BaseSpectralGroup):
    GROUP_NAME = "consonance"
    DOMAIN = "psychoacoustic"
    OUTPUT_DIM = 7
    INDEX_RANGE = (0, 7)
    STAGE = 1
    DEPENDENCIES = ()

    # ==================================================================
    # Audio-based computation (real psychoacoustic models)
    # ==================================================================

    @torch.no_grad()
    def compute_from_audio(
        self, mel: Tensor, audio: Tensor, sr: int = 44100
    ) -> Tensor:
        """Compute consonance features from raw audio using Sethares model.

        Args:
            mel:   (B, 128, T) log-mel spectrogram (used for frame count).
            audio: (B, N_SAMPLES) raw waveform at *sr* Hz.
            sr:    Sample rate.

        Returns:
            (B, T, 7) consonance features in [0, 1].
        """
        B = audio.shape[0]
        T = mel.shape[-1]
        hop_length = 256  # must match mel frame rate
        device = audio.device

        # --- STFT ---
        window = torch.hann_window(_N_FFT, device=device)
        stft = torch.stft(
            audio,
            n_fft=_N_FFT,
            hop_length=hop_length,
            win_length=_N_FFT,
            window=window,
            return_complex=True,
        )  # (B, n_fft//2+1, T_stft)
        mag = stft.abs()  # (B, F, T_stft)
        T_stft = mag.shape[-1]

        # Align to mel frame count (may differ by 1-2 frames)
        if T_stft > T:
            mag = mag[:, :, :T]
        elif T_stft < T:
            pad = torch.zeros(B, mag.shape[1], T - T_stft, device=device)
            mag = torch.cat([mag, pad], dim=-1)

        # Transpose to (B, T, F) for frame-wise processing
        mag = mag.transpose(1, 2)  # (B, T, F)
        F = mag.shape[-1]

        # Frequency axis (Hz)
        freq_bins = torch.linspace(0, sr / 2, F, device=device)  # (F,)

        # --- Peak picking (vectorized) ---
        freqs, amps = self._pick_peaks(mag, freq_bins)  # (B, T, K), (B, T, K)

        # --- Sethares dissonance [1] ---
        sethares = self._sethares_dissonance(freqs, amps)  # (B, T)

        # --- Roughness [0] — Sethares weighted by critical bandwidth ---
        roughness = self._roughness(freqs, amps)  # (B, T)

        # --- F0 estimation via HPS ---
        f0 = self._estimate_f0(mag, freq_bins, sr)  # (B, T)

        # --- Helmholtz consonance [2] — harmonic template match ---
        helmholtz = self._helmholtz(freqs, amps, f0)  # (B, T)

        # --- Stumpf fusion [3] — harmonicity ratio ---
        stumpf = self._stumpf(freqs, amps, f0)  # (B, T)

        # --- Derived features ---
        pleasantness = 0.6 * (1.0 - sethares) + 0.4 * stumpf  # [4]
        inharmonicity = 1.0 - stumpf                           # [5]
        harmonic_dev = self._harmonic_deviation(freqs, amps, f0)  # [6]

        return torch.stack([
            roughness, sethares, helmholtz, stumpf,
            pleasantness, inharmonicity, harmonic_dev,
        ], dim=-1).clamp(0, 1)  # (B, T, 7)

    # ==================================================================
    # Mel-based fallback (Phase 2 proxy — unchanged)
    # ==================================================================

    @torch.no_grad()
    def compute(self, mel: Tensor) -> Tensor:
        B, N, T = mel.shape
        eps = 1e-8
        mt = mel.transpose(1, 2)  # (B, T, 128)

        # [0] roughness: sigmoid(mel_high.var / mel.mean - 0.5)
        mel_high = mt[:, :, N * 3 // 4:]
        roughness = torch.sigmoid(
            mel_high.var(dim=-1) / mt.mean(dim=-1).clamp(min=eps) - 0.5
        )

        # [1] sethares_dissonance: mean(|diff(mel)|) / max
        spec_diff = torch.diff(mt, dim=-1)
        sethares = spec_diff.abs().mean(dim=-1)
        sethares = sethares / sethares.amax(dim=-1, keepdim=True).clamp(min=eps)

        # [2] helmholtz_kang: lag-1 autocorrelation of spectrum
        m1 = mt[:, :, :-1]
        m2 = mt[:, :, 1:]
        m1c = m1 - m1.mean(dim=-1, keepdim=True)
        m2c = m2 - m2.mean(dim=-1, keepdim=True)
        num = (m1c * m2c).sum(dim=-1)
        den = (m1c.pow(2).sum(dim=-1) * m2c.pow(2).sum(dim=-1)).sqrt().clamp(min=eps)
        helmholtz = (num / den).clamp(0, 1)

        # [3] stumpf_fusion: low-freq energy ratio
        quarter = N // 4
        stumpf = mt[:, :, :quarter].sum(dim=-1) / mt.sum(dim=-1).clamp(min=eps)

        # [4] sensory_pleasantness
        pleasantness = 0.6 * (1.0 - sethares) + 0.4 * stumpf

        # [5] inharmonicity
        inharmonicity = 1.0 - helmholtz

        # [6] harmonic_deviation
        harmonic_dev = 0.5 * sethares + 0.5 * (1.0 - helmholtz)

        return torch.stack([
            roughness, sethares, helmholtz, stumpf,
            pleasantness, inharmonicity, harmonic_dev
        ], dim=-1).clamp(0, 1)

    @property
    def feature_names(self):
        return (
            "roughness", "sethares_dissonance", "helmholtz_kang",
            "stumpf_fusion", "sensory_pleasantness", "inharmonicity",
            "harmonic_deviation",
        )

    # ==================================================================
    # Private: peak picking
    # ==================================================================

    @staticmethod
    def _pick_peaks(
        mag: Tensor, freq_bins: Tensor
    ) -> tuple[Tensor, Tensor]:
        """Spectral peak picking with parabolic interpolation.

        Args:
            mag:       (B, T, F) magnitude spectrum per frame.
            freq_bins: (F,) frequency of each bin in Hz.

        Returns:
            freqs: (B, T, K) interpolated peak frequencies in Hz.
            amps:  (B, T, K) interpolated peak amplitudes.
        """
        B, T, F = mag.shape
        device = mag.device

        # Convert to dB for parabolic interpolation accuracy
        mag_db = 20.0 * torch.log10(mag.clamp(min=1e-10))
        frame_max = mag_db.amax(dim=-1, keepdim=True)  # (B, T, 1)
        threshold = frame_max + _MIN_PEAK_DB  # absolute threshold per frame

        # Local maxima: bin k > bin k-1 AND bin k > bin k+1
        left = mag[:, :, :-2]    # bins 0..F-3
        center = mag[:, :, 1:-1]  # bins 1..F-2
        right = mag[:, :, 2:]    # bins 2..F-1
        is_peak = (center > left) & (center > right)  # (B, T, F-2)

        # Also check threshold
        center_db = mag_db[:, :, 1:-1]
        thresh_inner = threshold[:, :, :1].expand_as(center_db)
        is_peak = is_peak & (center_db > thresh_inner)

        # Pad is_peak to match F (bin 0 and bin F-1 are never peaks)
        is_peak_full = torch.zeros(B, T, F, dtype=torch.bool, device=device)
        is_peak_full[:, :, 1:-1] = is_peak

        # Get peak amplitudes (set non-peaks to 0)
        peak_amps = mag * is_peak_full.float()  # (B, T, F)

        # Select top-K peaks per frame by amplitude
        topk_amps, topk_idx = peak_amps.topk(_TOP_K, dim=-1)  # (B, T, K)

        # Parabolic interpolation for sub-bin frequency
        # Clamp indices to valid range for neighbor access
        idx_left = (topk_idx - 1).clamp(0, F - 1)
        idx_right = (topk_idx + 1).clamp(0, F - 1)

        alpha = mag_db.gather(-1, idx_left)   # (B, T, K)
        beta = mag_db.gather(-1, topk_idx)    # (B, T, K)
        gamma = mag_db.gather(-1, idx_right)  # (B, T, K)

        denom = (alpha - 2.0 * beta + gamma).clamp(min=1e-8)
        p = 0.5 * (alpha - gamma) / denom  # fractional bin offset
        p = p.clamp(-0.5, 0.5)  # safety

        # Interpolated frequency
        bin_spacing = freq_bins[1] - freq_bins[0] if F > 1 else 1.0
        base_freqs = freq_bins[topk_idx.clamp(0, F - 1)]  # (B, T, K)
        freqs = base_freqs + p * bin_spacing  # (B, T, K)
        freqs = freqs.clamp(min=1.0)  # avoid zero frequencies

        # Interpolated amplitude (linear scale from dB)
        interp_db = beta - 0.25 * (alpha - gamma) * p
        amps = (10.0 ** (interp_db / 20.0)) * (topk_amps > 0).float()

        return freqs, amps

    # ==================================================================
    # Private: Sethares dissonance
    # ==================================================================

    @staticmethod
    def _sethares_dissonance(freqs: Tensor, amps: Tensor) -> Tensor:
        """Sethares 1993 (2nd ed.) pairwise dissonance model.

        Args:
            freqs: (B, T, K) partial frequencies in Hz.
            amps:  (B, T, K) partial amplitudes.

        Returns:
            (B, T) total dissonance, normalized to [0, 1].
        """
        B, T, K = freqs.shape

        # Build all pairs (i, j) where i < j using upper-triangular indices
        idx = torch.triu_indices(K, K, offset=1, device=freqs.device)
        i_idx, j_idx = idx[0], idx[1]  # each has K*(K-1)/2 elements

        fi = freqs[:, :, i_idx]  # (B, T, P) where P = K*(K-1)/2
        fj = freqs[:, :, j_idx]
        ai = amps[:, :, i_idx]
        aj = amps[:, :, j_idx]

        f_min = torch.minimum(fi, fj)
        dF = torch.abs(fi - fj)
        a_min = torch.minimum(ai, aj)

        S = _DSTAR / (_S1 * f_min.clamp(min=1.0) + _S2)
        d_ij = a_min * (
            _C1 * torch.exp(_A1 * S * dF)
            + _C2 * torch.exp(_A2 * S * dF)
        )
        d_ij = d_ij.clamp(min=0.0)  # dissonance is non-negative

        total = d_ij.sum(dim=-1)  # (B, T)

        # Normalize: divide by sum of amplitude products (energy-aware)
        energy = (a_min.pow(2).sum(dim=-1) + 1e-8).sqrt()
        total = total / energy.clamp(min=1e-8)

        # Sigmoid normalization to [0, 1]
        return torch.sigmoid(total * 4.0 - 2.0)

    # ==================================================================
    # Private: Roughness (Plomp-Levelt via critical bandwidth weighting)
    # ==================================================================

    @staticmethod
    def _roughness(freqs: Tensor, amps: Tensor) -> Tensor:
        """Plomp-Levelt roughness: Sethares dissonance weighted by CB proximity.

        Roughness is strongest when frequency difference is ~25% of the
        critical bandwidth (Plomp & Levelt 1965, Zwicker & Fastl 2007).

        Args:
            freqs: (B, T, K) partial frequencies.
            amps:  (B, T, K) partial amplitudes.

        Returns:
            (B, T) roughness in [0, 1].
        """
        B, T, K = freqs.shape

        idx = torch.triu_indices(K, K, offset=1, device=freqs.device)
        fi = freqs[:, :, idx[0]]
        fj = freqs[:, :, idx[1]]
        ai = amps[:, :, idx[0]]
        aj = amps[:, :, idx[1]]

        f_min = torch.minimum(fi, fj)
        dF = torch.abs(fi - fj)
        a_min = torch.minimum(ai, aj)

        # Critical bandwidth (Zwicker & Fastl 2007)
        cb = 25.0 + 75.0 * (1.0 + 1.4 * (f_min / 1000.0).pow(2)).pow(0.69)

        # Sethares dissonance curve within critical bandwidth
        S = _DSTAR / (_S1 * f_min.clamp(min=1.0) + _S2)
        d_ij = a_min * (
            _C1 * torch.exp(_A1 * S * dF)
            + _C2 * torch.exp(_A2 * S * dF)
        )
        d_ij = d_ij.clamp(min=0.0)

        # Weight by how close we are to critical bandwidth interaction zone
        # Peak roughness at dF ~ 0.25*CB, decays beyond CB
        cb_ratio = dF / cb.clamp(min=1.0)
        cb_weight = torch.exp(-0.5 * ((cb_ratio - 0.25) / 0.15).pow(2))

        roughness = (d_ij * cb_weight).sum(dim=-1)

        # Normalize
        energy = (a_min.pow(2).sum(dim=-1) + 1e-8).sqrt()
        roughness = roughness / energy.clamp(min=1e-8)
        return torch.sigmoid(roughness * 6.0 - 2.0)

    # ==================================================================
    # Private: F0 estimation via Harmonic Product Spectrum
    # ==================================================================

    @staticmethod
    def _estimate_f0(
        mag: Tensor, freq_bins: Tensor, sr: int
    ) -> Tensor:
        """Estimate F0 per frame using Harmonic Product Spectrum.

        Args:
            mag:       (B, T, F) magnitude spectrum.
            freq_bins: (F,) Hz per bin.
            sr:        Sample rate.

        Returns:
            (B, T) estimated F0 in Hz.
        """
        B, T, F = mag.shape
        device = mag.device

        # Bin indices for valid F0 range
        bin_res = sr / (_N_FFT * 2) if F > 1 else 1.0
        bin_res = freq_bins[1] - freq_bins[0] if F > 1 else torch.tensor(1.0)
        k_min = max(1, int(_F0_MIN / bin_res.item()))
        k_max = min(F // _HPS_R, int(_F0_MAX / bin_res.item()) + 1)

        if k_max <= k_min:
            return torch.full((B, T), 261.63, device=device)

        # Log magnitude for numerical stability
        log_mag = torch.log(mag.clamp(min=1e-10))  # (B, T, F)

        # HPS: sum log magnitudes at harmonic positions
        hps = torch.zeros(B, T, k_max, device=device)
        for r in range(1, _HPS_R + 1):
            # Indices for r-th harmonic: k*r for k in [0, k_max)
            indices = torch.arange(k_max, device=device) * r  # (k_max,)
            valid = indices < F
            safe_indices = indices.clamp(0, F - 1)
            contribution = log_mag[:, :, safe_indices]  # (B, T, k_max)
            # Zero out invalid indices
            contribution = contribution * valid.float().unsqueeze(0).unsqueeze(0)
            hps = hps + contribution

        # Find peak in valid F0 range
        hps_valid = hps[:, :, k_min:k_max]  # (B, T, k_max-k_min)
        peak_idx = hps_valid.argmax(dim=-1) + k_min  # (B, T)

        f0 = peak_idx.float() * bin_res  # (B, T) in Hz
        return f0.clamp(min=_F0_MIN, max=_F0_MAX)

    # ==================================================================
    # Private: Helmholtz consonance (harmonic template match)
    # ==================================================================

    @staticmethod
    def _helmholtz(
        freqs: Tensor, amps: Tensor, f0: Tensor
    ) -> Tensor:
        """Harmonic template matching score.

        For each partial, score how close it is to an integer multiple of F0.
        Weighted by partial amplitude. High score = consonant/harmonic.

        Args:
            freqs: (B, T, K) partial frequencies.
            amps:  (B, T, K) partial amplitudes.
            f0:    (B, T) estimated fundamental frequency.

        Returns:
            (B, T) consonance score in [0, 1].
        """
        f0_exp = f0.unsqueeze(-1).clamp(min=1.0)  # (B, T, 1)

        # Ratio of each partial to F0
        ratio = freqs / f0_exp  # (B, T, K)

        # Distance to nearest integer harmonic
        nearest_n = ratio.round().clamp(min=1.0)
        deviation = (ratio - nearest_n).abs() / nearest_n  # relative deviation

        # Gaussian score: close to harmonic = high score
        harmonic_score = torch.exp(-0.5 * (deviation / _HARM_TOL).pow(2))

        # Weight by amplitude
        weighted = harmonic_score * amps
        total_amp = amps.sum(dim=-1).clamp(min=1e-8)

        return (weighted.sum(dim=-1) / total_amp).clamp(0, 1)

    # ==================================================================
    # Private: Stumpf fusion (harmonicity ratio)
    # ==================================================================

    @staticmethod
    def _stumpf(
        freqs: Tensor, amps: Tensor, f0: Tensor
    ) -> Tensor:
        """Stumpf tonal fusion: ratio of harmonic energy to total energy.

        Args:
            freqs: (B, T, K) partial frequencies.
            amps:  (B, T, K) partial amplitudes.
            f0:    (B, T) estimated fundamental frequency.

        Returns:
            (B, T) fusion score in [0, 1].
        """
        f0_exp = f0.unsqueeze(-1).clamp(min=1.0)
        ratio = freqs / f0_exp
        nearest_n = ratio.round().clamp(min=1.0)
        deviation = (ratio - nearest_n).abs() / nearest_n

        is_harmonic = (deviation < _HARM_TOL).float()  # (B, T, K)

        energy = amps.pow(2)
        harmonic_energy = (energy * is_harmonic).sum(dim=-1)
        total_energy = energy.sum(dim=-1).clamp(min=1e-8)

        return (harmonic_energy / total_energy).clamp(0, 1)

    # ==================================================================
    # Private: Harmonic deviation
    # ==================================================================

    @staticmethod
    def _harmonic_deviation(
        freqs: Tensor, amps: Tensor, f0: Tensor
    ) -> Tensor:
        """Deviation of partial amplitudes from expected 1/n harmonic decay.

        High deviation = inharmonic or unusual spectral shape.

        Args:
            freqs: (B, T, K) partial frequencies.
            amps:  (B, T, K) partial amplitudes.
            f0:    (B, T) estimated fundamental frequency.

        Returns:
            (B, T) deviation score in [0, 1].
        """
        f0_exp = f0.unsqueeze(-1).clamp(min=1.0)
        ratio = freqs / f0_exp
        nearest_n = ratio.round().clamp(min=1.0)
        deviation = (ratio - nearest_n).abs() / nearest_n
        is_harmonic = (deviation < _HARM_TOL).float()

        # Expected amplitude: 1/n decay (normalized)
        expected = 1.0 / nearest_n  # (B, T, K)

        # Normalize observed amplitudes
        amp_max = amps.amax(dim=-1, keepdim=True).clamp(min=1e-8)
        amp_norm = amps / amp_max

        # Deviation between observed and expected for harmonic partials
        amp_diff = (amp_norm - expected).pow(2) * is_harmonic
        n_harmonic = is_harmonic.sum(dim=-1).clamp(min=1.0)

        dev = (amp_diff.sum(dim=-1) / n_harmonic).sqrt()
        return torch.sigmoid(dev * 4.0 - 1.0)
