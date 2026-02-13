# R3 Standards Compliance Matrix

**Phase**: 3C -- Standards Documentation
**Source**: R3-V2-DESIGN.md, R3-DSP-SURVEY-TOOLS.md Section 6, R3-CROSSREF.md Section 5

---

## 1. Fundamental Constraint

All R3 features are computed from a log-mel spectrogram (`mel: (B, 128, T)`, sr=44100, hop=256,
n_mels=128). This means R3 never has access to raw audio waveforms or individual spectral peaks.
Every standard implementation below is a **mel-based approximation** unless otherwise noted.

---

## 2. Standard-to-Feature Mapping

| Standard | Description | R3 Feature(s) | Compliance | Notes |
|----------|-------------|---------------|:----------:|-------|
| **ISO 532-1** | Zwicker loudness (Bark-based) | K:sharpness_zwicker[122] | Approximate | Mel-to-Bark rebinning via pre-computed 128x24 matrix; Zwicker g(z) weighting applied; not full specific loudness calculation |
| **ISO 532-1** | Zwicker fluctuation strength | K:fluctuation_strength[123] | Approximate | Derived from modulation_4Hz[117]; simplified proportional model, not full Zwicker formula `F = 0.008 * sum(dL) / (df_mod/4 + 4/df_mod)` |
| **ISO 226:2003** | Equal-loudness contours | K:loudness_a_weighted[124] | Partial | A-weighting curve applied to mel bin center frequencies; approximates ISO 226 frequency sensitivity but lacks phon-level calibration |
| **ITU-R BS.1770-4** | Loudness (LUFS) | Partial via K domain | Reference Only | No K-weighting filter; no gating algorithm; B:loudness[10] uses Stevens law on log-mel (double compression bug noted); K:loudness_a_weighted[124] is closer but not LUFS-compliant |
| **DIN 45692** | Sharpness (acum) | K:sharpness_zwicker[122] | Approximate | Mel-to-Bark approximation; correct Zwicker weighting g(z) and 0.11 scaling factor applied; mel frequency resolution limits accuracy in low Bark bands |
| **AES17** | Audio measurement (RMS, peak) | B:amplitude[7], B:loudness[10] | Partial | B:amplitude[7] is RMS of log-mel (double compression); B:loudness[10] applies Stevens law on top; raw audio RMS not available |
| **AES-6id** | Spectral analysis | C:spectral_centroid[15], C:spectral_bandwidth[-- via clarity] | Approximate | Spectral moments computed in mel domain; centroid[15] is weighted mean of mel bin indices; true Hz-domain centroid differs due to mel spacing |
| **eGeMAPS** | Extended Geneva Minimalistic Set | K:alpha_ratio[125], K:hammarberg_index[126], K:spectral_slope_0_500[127] | Approximate | Mel-band approximations of eGeMAPS frequency-domain features; band boundaries approximate (mel bins vs Hz cutoffs) |
| **MPEG-7** | Spectral flatness | D:distribution_flatness[23] | Approximate | Wiener entropy (geometric/arithmetic mean ratio) computed on mel bins; MPEG-7 specifies linear frequency bins |

---

## 3. Compliance Level Definitions

| Level | Definition | R3 Implication |
|-------|-----------|----------------|
| **Full** | Implementation follows published algorithm on correct input domain | Extremely rare in R3; would require raw audio or linear spectrum access |
| **Approximate** | Captures the same perceptual dimension using mel-domain computation; known quantitative deviation from standard | Most K-group psychoacoustic features; deviation documented per feature |
| **Partial** | Addresses a subset of the standard or uses a significantly simplified model | B-group energy features; ITU-R BS.1770 coverage |
| **Reference Only** | Standard informed the design philosophy but implementation is fundamentally different | ITU-R BS.1770 LUFS; features inspired by but not conforming to the standard |

---

## 4. Per-Group Standards Summary

| Group | Index Range | Relevant Standards | Compliance Level |
|-------|:-----------:|-------------------|:----------------:|
| A: Consonance | [0:7] | Plomp-Levelt 1965 (informational) | Reference Only |
| B: Energy | [7:12] | AES17 (partial) | Partial |
| C: Timbre | [12:21] | AES-6id (approximate spectral moments) | Approximate |
| D: Change | [21:25] | MPEG-7 spectral flatness | Approximate |
| E: Interactions | [25:49] | None directly | N/A |
| F: Pitch & Chroma | [49:65] | None (Krumhansl tonal hierarchy is research, not standard) | N/A |
| G: Rhythm & Groove | [65:75] | None directly | N/A |
| H: Harmony & Tonality | [75:87] | None directly | N/A |
| I: Information & Surprise | [87:94] | None directly | N/A |
| J: Timbre Extended | [94:114] | None (MFCC is de facto MIR standard, not ISO) | N/A |
| K: Modulation & Psychoacoustic | [114:128] | ISO 532-1, ISO 226, DIN 45692, eGeMAPS | Approximate |

---

## 5. Phase 6 Standards Improvement Plan

| Feature | Current Status | Phase 6 Target | Required Change |
|---------|:-------------:|:--------------:|-----------------|
| B:loudness[10] | Double compression bug | Approximate (ISO 532-1) | Apply Stevens law to `exp(log_mel)` or linear power spectrum |
| K:sharpness_zwicker[122] | Mel-to-Bark approximate | Closer to DIN 45692 | Improved Bark rebinning with ERB overlap correction |
| K:loudness_a_weighted[124] | A-weighting only | Partial ITU-R BS.1770 | Add K-weighting pre-filter; still no gating |
| A:roughness[0] | Proxy (var/mean) | Approximate Plomp-Levelt | Critical band pairwise comparison within ERB bands |

---

## 6. Key Limitations

1. **No raw audio access**: R3 operates on log-mel spectrograms. Standards requiring waveform-level analysis (ITU-R BS.1770 gating, true RMS per AES17) cannot be fully implemented.
2. **Mel frequency resolution**: Below ~200 Hz, mel bins span multiple semitones. This limits accuracy for low-frequency psychoacoustic features (Bark bands 1-3, fundamental frequency detection).
3. **Temporal resolution**: Frame rate is 172.27 Hz (5.8 ms hop). Standards requiring sub-millisecond temporal analysis are not achievable.
4. **Calibration**: R3 features are normalized to [0,1] without absolute calibration. Standards specifying physical units (phon, acum, sone, LUFS) require level calibration not present in the pipeline.

---

*Source: R3-V2-DESIGN.md Sections 2, 7; R3-DSP-SURVEY-TOOLS.md Section 6; R3-CROSSREF.md Section 5*
