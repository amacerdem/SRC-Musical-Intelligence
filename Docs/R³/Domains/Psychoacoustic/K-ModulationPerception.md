# Group K: Modulation & Psychoacoustic [114:128] -- 14D

## Overview
- **Domain**: Psychoacoustic
- **Code**: `mi_beta/ear/r3/domains/psychoacoustic/modulation.py`
- **Status**: NEW (Phase 3)
- **Quality Tier**: Standard (modulation spectrum) / Reference (sharpness_zwicker, loudness_a_weighted)
- **Pipeline Stage**: 1 (parallel, mel-only)
- **Class**: `ModulationPsychoacousticGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 114 | modulation_0_5Hz | Per-band FFT of mel temporal envelope at 0.5 Hz | per-rate max-norm | ~3 ms (all mod) | Chi & Shamma 2005 cortical modulation | Standard |
| 115 | modulation_1Hz | energy at 1 Hz AM rate | per-rate max-norm | (shared) | Phrase-level rhythmic modulation | Standard |
| 116 | modulation_2Hz | energy at 2 Hz AM rate | per-rate max-norm | (shared) | Beat-rate modulation | Standard |
| 117 | modulation_4Hz | energy at 4 Hz AM rate | per-rate max-norm | (shared) | Speech syllabic rate / strong beat | Standard |
| 118 | modulation_8Hz | energy at 8 Hz AM rate | per-rate max-norm | (shared) | Rapid articulation / tremolo | Standard |
| 119 | modulation_16Hz | energy at 16 Hz AM rate | per-rate max-norm | (shared) | Roughness boundary / vibrato upper | Standard |
| 120 | modulation_centroid | Weighted mean of log2(mod rates) | min-max [-1,4]->[0,1] | <0.1 ms | Dominant modulation rate | Standard |
| 121 | modulation_bandwidth | Weighted std of log2(mod rates) | /max_std (2.5) | <0.1 ms | Modulation rate diversity | Standard |
| 122 | sharpness_zwicker | `0.11 * integral(N'(z)*g(z)*z dz) / integral(N'(z) dz)` on Bark | /4.0 acum + clamp | ~0.3 ms | DIN 45692 Zwicker sharpness | Reference |
| 123 | fluctuation_strength | 4 Hz modulation energy (from [117]) | already [0,1] | <0.01 ms | Zwicker/Fastl fluctuation peak at 4 Hz | Approximate |
| 124 | loudness_a_weighted | A-weighting curve applied to mel bands | max-norm (batch) | <0.1 ms | ISO 226:2003 equal-loudness contours | Reference |
| 125 | alpha_ratio | low (0-1kHz) / high (1-5kHz) energy ratio | x/(x+1) -> [0,1] | <0.1 ms | eGeMAPS voice quality balance | Standard |
| 126 | hammarberg_index | peak(0-2kHz) / peak(2-5kHz) in log domain | sigmoid(x/5) | <0.1 ms | eGeMAPS spectral tilt | Standard |
| 127 | spectral_slope_0_500 | Linear regression slope of mel bands 0-500 Hz | sigmoid(slope*10) | <0.1 ms | eGeMAPS low-frequency shape | Standard |

## Computation Pipeline

- **Input**: mel (B, 128, T) -- log-mel spectrogram
- **Dependencies**: None (K[123] depends on K[117] internally)
- **Output**: (B, T, 14) -- all values in [0,1]
- **Estimated cost**: ~3.0 ms/frame peak (amortized ~0.5 ms due to hop-based FFT)
- **Warm-up**: 344 frames (2.0s) for modulation features [114:121]

### Detailed Computation Flow

```
mel (B, 128, T)
  |
  +-- Modulation Spectrum [114:119] (6D):
  |     mel_env = mel.abs()                         # temporal envelope
  |     windows = mel_env.unfold(-1, 344, 86)       # sliding window (2s, 75% overlap)
  |     windowed = windows * hann_window(344)
  |     fft_mag = rfft(windowed).abs()              # per-band temporal FFT
  |     target_bins = [1, 3, 6, 12, 24, 48]        # 0.5, 1, 2, 4, 8, 16 Hz
  |     mod_energy = fft_mag[:, :, :, target_bins].mean(dim=1)  # avg across bands
  |     mod_frame = interpolate(mod_energy, size=T)  # upsample to frame rate
  |     mod_norm = mod_frame / mod_frame.max()       # per-rate max-norm
  |
  +-- Modulation Centroid [120] (1D):
  |     log_rates = log2([0.5, 1, 2, 4, 8, 16])    # [-1, 0, 1, 2, 3, 4]
  |     centroid = (log_rates * mod_energies).sum() / mod_energies.sum()
  |     centroid_norm = (centroid - (-1)) / 5        # [-1,4] -> [0,1]
  |
  +-- Modulation Bandwidth [121] (1D):
  |     mod_std = weighted_std(log_rates, mod_energies)
  |     bandwidth = mod_std / 2.5                    # max_std ~ 2.5
  |
  +-- Sharpness Zwicker [122] (1D):
  |     bark_energy = bark_matrix.T @ exp(mel)       # mel -> Bark (128x24 matmul)
  |     g(z) = 1.0 if z<=15 else 0.066*exp(0.171*z) # Zwicker weighting
  |     S = 0.11 * sum(bark * g * z) / sum(bark)     # weighted centroid
  |     sharpness = S / 4.0                           # scale to [0,1]
  |
  +-- Fluctuation Strength [123] (1D):
  |     fluctuation = modulation_4Hz[117]             # direct reference
  |
  +-- Loudness A-weighted [124] (1D):
  |     mel_linear = exp(mel)
  |     weighted = mel_linear * A_weights             # pre-computed ISO 226
  |     loudness_A = weighted.sum(dim=1) / max
  |
  +-- Alpha Ratio [125] (1D):
  |     low = mel[:, :40, :].sum()   # 0-1kHz
  |     high = mel[:, 40:100, :].sum()  # 1-5kHz
  |     alpha = low / high
  |     alpha_norm = alpha / (alpha + 1)
  |
  +-- Hammarberg Index [126] (1D):
  |     peak_low = mel[:, :55, :].max()    # 0-2kHz
  |     peak_high = mel[:, 55:100, :].max()  # 2-5kHz
  |     hammarberg = sigmoid((peak_low - peak_high) / 5)
  |
  +-- Spectral Slope [127] (1D):
        x = arange(18)                      # bins 0-17 (~0-500 Hz)
        y = mel[:, :18, :]
        slope = cov(x, y) / var(x)          # linear regression
        slope_norm = sigmoid(slope * 10)
```

## PyTorch Implementation Notes

- **Key operations**: `torch.fft.rfft`, `Tensor.unfold`, `F.interpolate`,
  `torch.matmul` (bark mapping), `torch.sigmoid`, `torch.exp`
- **Pre-computed matrices**:
  - `mel_to_chroma` not needed (no chroma dependency)
  - `bark_matrix` (128 x 24) for sharpness_zwicker -- `register_buffer`
  - `g_weights` (24,) Zwicker weighting function -- `register_buffer`
  - `A_weights` (128,) ISO 226 A-weighting at mel bin center freqs -- `register_buffer`
  - `hann_window` (344,) for modulation FFT -- `register_buffer`
- **Warm-up requirements**: Modulation features [114:121] output zero for the
  first 344 frames (~2.0s) because the sliding FFT window is not yet full.
  Frame-level interpolation handles the transition.

### Modulation FFT Parameters

```
window_size = 344 frames (~2.0s)
hop_size    = 86 frames (~0.5s), 75% overlap
fft_size    = 512 (zero-padded for frequency resolution)
freq_resolution = 172.27 Hz / 512 = 0.336 Hz
target_rates = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0] Hz
target_bins  = [1, 3, 6, 12, 24, 48]
```

### Bark Rebinning for Sharpness

The mel-to-Bark conversion matrix maps 128 mel bins to 24 Bark bands. This is
pre-computed in `__init__()` using the mel center frequencies and the Bark scale
formula `z = 13*arctan(0.00076*f) + 3.5*arctan((f/7500)^2)`.

### A-Weighting Curve

The A-weighting values are computed from the IEC 61672-1 formula applied to each
mel bin's center frequency:

```
A(f) = 12194^2 * f^4 / ((f^2 + 20.6^2) * sqrt((f^2 + 107.7^2) * (f^2 + 737.9^2)) * (f^2 + 12194^2))
```

Converted to linear scale and stored as `register_buffer("a_weights", ...)`.

## Phase 6 Notes

Group K is entirely new in R3 v2. No Phase 6 revision is planned.

### Potential Improvements (Phase 6+)

- **Modulation spectrum**: Consider per-Bark-band modulation analysis instead
  of per-mel-band for better psychoacoustic alignment.
- **Fluctuation strength**: Current implementation is a direct reference to
  K[117] modulation_4Hz. A more accurate Zwicker model would include the
  bandpass response shape `F = 0.008 * deltaL / (fmod/4 + 4/fmod)`.
- **Loudness model**: K[124] A-weighted loudness is simpler than full Zwicker
  ISO 532-1 specific loudness. Phase 6+ could implement the full model.

## References

### Primary Papers
- Chi, T. & Shamma, S. A. (2005). Multiresolution spectrotemporal analysis of complex sounds. JASA 118(2), 887-906.
- Zwicker, E. & Fastl, H. (1999). Psychoacoustics: Facts and Models. Springer.
- DIN 45692:2009. Measurement technique for the simulation of the auditory sensation of sharpness.
- ISO 226:2003. Normal equal-loudness-level contours.
- Eyben, F. et al. (2015). The Geneva Minimalistic Acoustic Parameter Set (eGeMAPS). IEEE Trans. Affective Computing 7(2), 190-202.
- Hammarberg, B. et al. (1980). Perceptual and acoustic correlates of abnormal voice qualities. Acta Otolaryngologica 90(1-6), 441-451.

### Toolkit Implementations
- `essentia.LoudnessEBUR128` -- perceptual loudness reference
- `essentia.DynamicComplexity` -- temporal modulation related
- `librosa.feature.tempogram` -- related temporal modulation analysis
- `openSMILE/eGeMAPS` -- alpha_ratio, hammarberg_index, spectral_slope reference implementations
