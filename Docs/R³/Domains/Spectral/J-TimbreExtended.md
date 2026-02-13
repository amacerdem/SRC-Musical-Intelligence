# Group J: Timbre Extended [94:114] -- 20D

## Overview
- **Domain**: Spectral
- **Code**: `mi_beta/ear/r3/domains/spectral/timbre_extended.py`
- **Status**: NEW (Phase 3)
- **Quality Tier**: Reference (MFCC is the most validated MIR feature; spectral contrast is well-established)
- **Pipeline Stage**: 1 (parallel, mel-only)
- **Class**: `TimbreExtendedGroup(BaseSpectralGroup)`

## Feature Table

| Index | Feature Name | Formula | Normalization | Cost | Psychoacoustic Basis | Quality |
|-------|-------------|---------|---------------|------|---------------------|---------|
| 94 | mfcc_1 | DCT-II coefficient 1 of log-mel | per-coeff scale -> [0,1] | ~0.3 ms (all) | Cepstral timbre -- vocal tract shape | Reference |
| 95 | mfcc_2 | DCT-II coefficient 2 | (same) | (shared) | Spectral tilt | Reference |
| 96 | mfcc_3 | DCT-II coefficient 3 | (same) | (shared) | Fine spectral shape | Reference |
| 97 | mfcc_4 | DCT-II coefficient 4 | (same) | (shared) | Fine spectral shape | Reference |
| 98 | mfcc_5 | DCT-II coefficient 5 | (same) | (shared) | Fine spectral shape | Reference |
| 99 | mfcc_6 | DCT-II coefficient 6 | (same) | (shared) | Fine spectral shape | Reference |
| 100 | mfcc_7 | DCT-II coefficient 7 | (same) | (shared) | Fine spectral shape | Reference |
| 101 | mfcc_8 | DCT-II coefficient 8 | (same) | (shared) | Fine spectral shape | Reference |
| 102 | mfcc_9 | DCT-II coefficient 9 | (same) | (shared) | Fine spectral shape | Reference |
| 103 | mfcc_10 | DCT-II coefficient 10 | (same) | (shared) | Fine spectral shape | Reference |
| 104 | mfcc_11 | DCT-II coefficient 11 | (same) | (shared) | Fine spectral detail | Reference |
| 105 | mfcc_12 | DCT-II coefficient 12 | (same) | (shared) | Fine spectral detail | Reference |
| 106 | mfcc_13 | DCT-II coefficient 13 | (same) | (shared) | Fine spectral detail | Reference |
| 107 | spectral_contrast_1 | Octave sub-band 1 peak-valley difference | /10 + clamp | ~0.2 ms (all) | Harmonic vs noise texture (Jiang 2002) | Standard |
| 108 | spectral_contrast_2 | Sub-band 2 peak-valley | (same) | (shared) | (same) | Standard |
| 109 | spectral_contrast_3 | Sub-band 3 peak-valley | (same) | (shared) | (same) | Standard |
| 110 | spectral_contrast_4 | Sub-band 4 peak-valley | (same) | (shared) | (same) | Standard |
| 111 | spectral_contrast_5 | Sub-band 5 peak-valley | (same) | (shared) | (same) | Standard |
| 112 | spectral_contrast_6 | Sub-band 6 peak-valley | (same) | (shared) | (same) | Standard |
| 113 | spectral_contrast_7 | Sub-band 7 (residual) peak-valley | (same) | (shared) | (same) | Standard |

## Computation Pipeline

- **Input**: mel (B, 128, T) -- log-mel spectrogram
- **Dependencies**: None
- **Output**: (B, T, 20) -- all values in [0,1]
- **Estimated cost**: ~0.5 ms/frame total (0.3 ms MFCC + 0.2 ms contrast)
- **Warm-up**: None

### MFCC Computation [94:106]

```
Input: mel (B, 128, T) -- already in log domain

1. Pre-compute DCT-II matrix D (128 x 13):
   D[m, k] = sqrt(2/128) * cos(pi * k * (2*m + 1) / (2 * 128))
   for k = 1..13 (k=0 DC component is skipped)

2. Apply DCT:
   mfcc_raw = D.T @ mel                    # (B, 13, T)

3. Per-coefficient normalization:
   mfcc_scale = [40, 80, 60, 50, 40, 35, 30, 25, 22, 20, 18, 16, 15]
   mfcc_norm = (mfcc_raw / mfcc_scale + 1) / 2   # [-1,1] -> [0,1]
   mfcc = mfcc_norm.clamp(0, 1)

Output: (B, T, 13) in [0,1]
```

**DCT Matrix Construction** (in `__init__`):
```python
n = 128  # mel bins
k = torch.arange(1, 14)  # coefficients 1-13
m = torch.arange(n)
D = torch.sqrt(torch.tensor(2.0 / n)) * torch.cos(
    math.pi * k.unsqueeze(0) * (2 * m.unsqueeze(1) + 1) / (2 * n)
)
self.register_buffer("dct_matrix", D)  # (128, 13)
```

**MFCC Scale Factors**: Empirical per-coefficient maximum absolute values
derived from music dataset statistics. These ensure each coefficient maps
to approximately [-1, 1] before the shift to [0, 1].

### Spectral Contrast Computation [107:113]

```
Input: mel (B, 128, T) -- log-mel spectrogram

1. Define 7 octave sub-bands (mel bin indices):
   bands = [(0,4), (4,8), (8,16), (16,32), (32,64), (64,96), (96,128)]

2. For each band:
   band = mel_t[:, :, start:end]            # (B, T, band_width)
   sorted_band = sort(band, dim=-1)
   n = band_width
   alpha = max(1, round(0.2 * n))           # 20% quantile

   peak = sorted_band[:, :, -alpha:].mean(dim=-1)     # top 20% mean
   valley = sorted_band[:, :, :alpha].mean(dim=-1)    # bottom 20% mean
   contrast = peak - valley                             # in log domain

3. Stack and normalize:
   contrast_all = stack(contrasts, dim=-1)   # (B, T, 7)
   contrast_norm = (contrast_all / 10.0).clamp(0, 1)

Output: (B, T, 7) in [0,1]
```

**Band Boundaries Rationale**: The 7 bands approximate octave spacing on the
mel scale. Band widths are: 4, 4, 8, 16, 32, 32, 32 mel bins. The first
bands cover low frequencies with narrower analysis windows; upper bands are
broader, matching the mel scale's logarithmic compression.

## PyTorch Implementation Notes

- **Key operations**: `torch.matmul` (DCT), `torch.sort` (per-band),
  `torch.clamp`, slicing
- **Pre-computed matrices**:
  - `dct_matrix` (128, 13): DCT-II basis -- `register_buffer`
  - `mfcc_scale` (13,): per-coefficient normalization -- `register_buffer`
- **Warm-up requirements**: None
- **Memory**: DCT matrix is 128x13 = 1,664 floats (6.5 KB). Negligible.

### MFCC vs librosa Comparison

Our MFCC differs from `librosa.feature.mfcc` in:
1. We skip MFCC-0 (DC component) -- indices 1-13 instead of 0-12
2. Input is already log-mel (librosa applies log internally)
3. Normalization is per-coefficient empirical scaling rather than liftering

These differences are intentional: MFCC-0 correlates with loudness (already
captured in B[10]), and our normalization ensures [0,1] output range.

## Phase 6 Notes

Group J is entirely new in R3 v2. No Phase 6 revision is planned.

### Design Notes

- MFCC and spectral contrast were not directly requested by C3 model gap
  analysis (R1), but are the most evidence-based features in MIR research.
  R3 survey (R3 report) identified them as HIGH mel-compatibility features
  present in all major toolkits.
- Potential beneficiary models: SPU (timbre discrimination), IMU (instrument
  recognition), ARU (acoustic environment classification).
- Delta-MFCC and delta-delta-MFCC were considered but excluded to stay within
  128D budget. They can be computed in H3 temporal layer if needed.

## References

### Primary Papers
- Davis, S. & Mermelstein, P. (1980). Comparison of parametric representations for monosyllabic word recognition in continuously spoken sentences. IEEE Trans. ASSP 28(4), 357-366.
- Jiang, D. N. et al. (2002). Music type classification by spectral contrast feature. Proc. IEEE ICME 2002.
- Peeters, G. (2004). A large set of audio features for sound description. IRCAM Technical Report.
- Logan, B. (2000). Mel Frequency Cepstral Coefficients for Music Modeling. Proc. ISMIR.

### Toolkit Implementations
- `librosa.feature.mfcc` -- MFCC reference implementation
- `librosa.feature.spectral_contrast` -- spectral contrast reference
- `essentia.MFCC` -- alternative MFCC implementation
- `essentia.SpectralContrast` -- spectral contrast
