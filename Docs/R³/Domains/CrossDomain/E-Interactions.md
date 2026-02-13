# Group E: Interactions [25:49] -- 24D

## Overview
- **Domain**: CrossDomain
- **Code**: `mi_beta/ear/r3/cross_domain/interactions.py`
- **Status**: EXISTING
- **Quality Tier**: Proxy (uses independent mel-based proxies instead of real A-D outputs)
- **Pipeline Stage**: 2 (should depend on A, B, C, D; currently computes independently)
- **Class**: `InteractionsGroup(BaseSpectralGroup)`

## Feature Table

### Block 1: x_l0l5 -- Energy x Consonance [25:32] (8D)

| Index | Feature Name | Formula (current proxy) | Normalization | Cost | Interaction Type |
|-------|-------------|------------------------|---------------|------|-----------------|
| 25 | x_amp_roughness | amp_proxy * roughness_proxy | product [0,1] | <0.01 ms | Energy modulates roughness perception |
| 26 | x_amp_sethares | amp_proxy * sethares_proxy | product [0,1] | <0.01 ms | Energy modulates dissonance |
| 27 | x_amp_helmholtz | amp_proxy * helmholtz_proxy | product [0,1] | <0.01 ms | Energy modulates harmonicity |
| 28 | x_amp_stumpf | amp_proxy * stumpf_proxy | product [0,1] | <0.01 ms | Energy modulates tonal fusion |
| 29 | x_vel_roughness | vel_proxy * roughness_proxy | product [0,1] | <0.01 ms | Change rate modulates roughness |
| 30 | x_vel_sethares | vel_proxy * sethares_proxy | product [0,1] | <0.01 ms | Change rate modulates dissonance |
| 31 | x_vel_helmholtz | vel_proxy * helmholtz_proxy | product [0,1] | <0.01 ms | Change rate modulates harmonicity |
| 32 | x_vel_stumpf | vel_proxy * stumpf_proxy | product [0,1] | <0.01 ms | Change rate modulates fusion |

### Block 2: x_l4l5 -- Change x Consonance [33:40] (8D)

| Index | Feature Name | Formula (current proxy) | Normalization | Cost | Interaction Type |
|-------|-------------|------------------------|---------------|------|-----------------|
| 33 | x_flux_roughness | flux_proxy * roughness_proxy | product [0,1] | <0.01 ms | Spectral change x roughness |
| 34 | x_flux_sethares | flux_proxy * sethares_proxy | product [0,1] | <0.01 ms | Spectral change x dissonance |
| 35 | x_flux_helmholtz | flux_proxy * helmholtz_proxy | product [0,1] | <0.01 ms | Spectral change x harmonicity |
| 36 | x_flux_stumpf | flux_proxy * stumpf_proxy | product [0,1] | <0.01 ms | Spectral change x fusion |
| 37 | x_entropy_roughness | entropy_proxy * roughness_proxy | product [0,1] | <0.01 ms | Spectral uniformity x roughness |
| 38 | x_entropy_sethares | entropy_proxy * sethares_proxy | product [0,1] | <0.01 ms | Spectral uniformity x dissonance |
| 39 | x_entropy_helmholtz | entropy_proxy * helmholtz_proxy | product [0,1] | <0.01 ms | Spectral uniformity x harmonicity |
| 40 | x_entropy_stumpf | entropy_proxy * stumpf_proxy | product [0,1] | <0.01 ms | Spectral uniformity x fusion |

### Block 3: x_l5l7 -- Consonance x Timbre [41:48] (8D)

| Index | Feature Name | Formula (current proxy) | Normalization | Cost | Interaction Type |
|-------|-------------|------------------------|---------------|------|-----------------|
| 41 | x_roughness_warmth | roughness_proxy * warmth_proxy | product [0,1] | <0.01 ms | Roughness in warm timbres |
| 42 | x_roughness_sharpness | roughness_proxy * sharpness_proxy | product [0,1] | <0.01 ms | Roughness in sharp timbres |
| 43 | x_sethares_warmth | sethares_proxy * warmth_proxy | product [0,1] | <0.01 ms | Dissonance in warm timbres |
| 44 | x_sethares_sharpness | sethares_proxy * sharpness_proxy | product [0,1] | <0.01 ms | Dissonance in sharp timbres |
| 45 | x_helmholtz_tonalness | helmholtz_proxy * tonalness_proxy | product [0,1] | <0.01 ms | Harmonicity x tonalness |
| 46 | x_helmholtz_clarity | helmholtz_proxy * clarity_proxy | product [0,1] | <0.01 ms | Harmonicity x spectral centroid |
| 47 | x_stumpf_smoothness | stumpf_proxy * smoothness_proxy | product [0,1] | <0.01 ms | Fusion x spectral smoothness |
| 48 | x_stumpf_autocorr | stumpf_proxy * autocorr_proxy | product [0,1] | <0.01 ms | Fusion x spectral periodicity |

## Computation Pipeline

- **Input**: mel (B, 128, T) -- log-mel spectrogram (currently computes all proxies independently)
- **Dependencies**: Should depend on A, B, C, D; currently independent
- **Output**: (B, T, 24) -- all values in [0,1]
- **Estimated cost**: ~0.1 ms/frame total (24 element-wise multiplications + proxy computation)
- **Warm-up**: None

### Current Proxy Computation

The existing implementation computes ALL base features independently from mel,
rather than referencing the outputs of Groups A-D:

```
mel (B, 128, T) -> mel_t (B, T, 128)
  |
  +-- Energy proxies:
  |     amp_proxy = RMS(mel_t) / max                    # matches B[7]
  |     vel_proxy = sigmoid(diff(amp) * 5)              # matches B[8]
  |
  +-- Consonance proxies:
  |     roughness_proxy = sigmoid(var(high_bins) - 0.5)
  |         MISMATCH: real A[0] = sigmoid(var/mean - 0.5)  # missing /mean
  |
  |     sethares_proxy = diff(mel_t).abs().mean() / max  # matches A[1]
  |
  |     helmholtz_proxy = max(mel_t) / sum(mel_t)
  |         MISMATCH: real A[2] = lag-1 autocorrelation
  |         helmholtz_proxy actually = C[14] tonalness
  |
  |     stumpf_proxy = mel_t[:,:,:N//4].sum() / total    # matches A[3]
  |
  +-- Change proxies:
  |     flux_proxy = norm(diff(mel_t)) / max             # matches D[21]
  |     entropy_proxy = -sum(p*log(p)) / log(N)          # matches D[22]
  |
  +-- Timbre proxies:
  |     warmth_proxy = stumpf_proxy                      # matches C[12] = A[3]
  |     sharpness_proxy = mel_t[:,:,3N//4:].sum() / total  # matches C[13]
  |     tonalness_proxy = helmholtz_proxy                # = C[14] not A[2]
  |     clarity_proxy = centroid / N                     # matches C[15]
  |     smoothness_proxy = 1 - irregularity / max        # matches C[16]
  |     autocorr_proxy = lag-1 autocorrelation           # matches C[17] = A[2]
  |
  +-- Cross products:
        x_l0l5 = outer_product(energy_proxies[:4], consonance_proxies[:2]) -> 8D
        x_l4l5 = outer_product(change_proxies[:4], consonance_proxies[:2]) -> 8D
        x_l5l7 = mixed_product(consonance_proxies[:4], timbre_proxies[:2]) -> 8D
```

### Proxy Mismatches (Detailed)

| Proxy | E Group Computation | Real Group Output | Discrepancy |
|-------|-------------------|-------------------|-------------|
| roughness_proxy | `sigmoid(mel_high.var() - 0.5)` | A[0]: `sigmoid(mel_high.var() / mel.mean() - 0.5)` | Missing `/mean` denominator |
| helmholtz_proxy | `mel.max() / mel.sum()` | A[2]: lag-1 spectral autocorrelation | Completely different computation (=C[14] tonalness) |
| sethares_proxy | `diff.abs().mean() / max` | A[1]: same formula | Match |
| stumpf_proxy | `mel[:N//4].sum() / total` | A[3]: same formula | Match |
| amp_proxy | `RMS(mel) / max` | B[7]: same formula | Match |
| vel_proxy | `sigmoid(diff(amp) * 5)` | B[8]: same formula | Match |
| flux_proxy | `norm(diff) / max` | D[21]: same formula | Match |
| entropy_proxy | `-sum(p*log(p)) / log(N)` | D[22]: same formula | Match |

**Summary**: 2 out of 8 base proxies have mismatches (roughness, helmholtz).
The remaining 6 correctly replicate the base group formulas.

## PyTorch Implementation Notes

- **Key operations**: Element-wise multiply (`*`), all proxy operations
  (var, diff, abs, mean, max, sum, norm, log, sigmoid)
- **Pre-computed matrices**: None
- **Warm-up requirements**: None
- **Code structure**: `InteractionsGroup.compute(mel)` is a large monolithic
  method that recomputes all base features, then creates 3 blocks of 8 products.

### Current Code Analysis

The existing `interactions.py` implements:
- `GROUP_NAME = "interactions"`, `OUTPUT_DIM = 24`, `INDEX_RANGE = (25, 49)`
- 24 feature names explicitly listed matching the 3-block structure
- All proxies computed from `mel_t` with `total_energy = mel_t.sum(dim=-1)`
- Cross products via `torch.cat` of element-wise products
- Final `clamp(0, 1)` on all outputs

### Proxy Duplication Analysis

The proxy computation effectively duplicates work already done by Groups A-D:
- roughness_proxy: ~95% identical to A[0] (minor formula difference)
- sethares_proxy: 100% identical to A[1]
- helmholtz_proxy: 0% match with A[2] (completely wrong proxy)
- stumpf_proxy: 100% identical to A[3] and C[12]
- amp_proxy: 100% identical to B[7]
- vel_proxy: 100% identical to B[8]
- flux_proxy: 100% identical to D[21]
- entropy_proxy: 100% identical to D[22]

This means ~1/3 of E's computation is redundant (already done by A-D),
and 1 proxy (helmholtz) is fundamentally wrong.

## Phase 6 Notes

### Phase 6 Stage 1: Proxy Fix (24D preserved)

Replace all proxy computations with references to actual group outputs:

```python
# CURRENT (v1 -- proxy-based):
def compute(self, mel: Tensor) -> Tensor:
    roughness_proxy = mel.var(...)   # wrong
    helmholtz_proxy = mel.max()/mel.sum()  # wrong

# TARGET (Phase 6 -- reference-based):
def compute_with_deps(self, mel: Tensor, group_outputs: dict) -> Tensor:
    A = group_outputs['consonance']   # (B, T, 7)
    B = group_outputs['energy']       # (B, T, 5)
    C = group_outputs['timbre']       # (B, T, 9)
    D = group_outputs['change']       # (B, T, 4)

    roughness = A[:, :, 0:1]         # real A[0]
    sethares  = A[:, :, 1:2]         # real A[1]
    helmholtz = A[:, :, 2:3]         # real A[2] (was wrong!)
    stumpf    = A[:, :, 3:4]         # real A[3]

    amp = B[:, :, 0:1]              # real B[7]
    vel = B[:, :, 1:2]              # real B[8]

    flux    = D[:, :, 0:1]          # real D[21]
    entropy = D[:, :, 1:2]          # real D[22]

    warmth    = C[:, :, 0:1]        # real C[12]
    sharpness = C[:, :, 1:2]        # real C[13]
    # ... etc.
```

**Impact**: Computation becomes trivially cheap (24 multiplications instead
of recomputing all base features). More importantly, helmholtz_proxy is
corrected from `max/sum` (tonalness) to actual lag-1 autocorrelation.

### Phase 6+ Stage 2: Expansion (PROPOSAL, deferred to R3 v2.1)

New psychoacoustically motivated cross-group interactions:

| Pair | Dims | Features | Psychoacoustic Rationale |
|------|------|----------|------------------------|
| F x A | 4D | chroma_entropy*roughness, pitch_height*harmonicity, salience*fusion, inharmonicity*dissonance | Pitch perception modulated by consonance |
| G x B | 4D | tempo*amplitude, syncopation*onset_strength, beat_strength*velocity, groove*loudness | Rhythmic structure energized by dynamics |
| H x D | 4D | key_clarity*flux, tonal_stability*entropy, harmonic_change*flux, diatonicity*flatness | Harmonic context modulated by change |
| I x all | 4D | mean(I)*mean(A), mean(I)*mean(B), mean(I)*mean(F), mean(I)*mean(G) | Surprise interaction with base domains |

Total expansion: +16D -> E grows from 24D to 40D.

**Decision**: Deferred to R3 v2.1 (Phase 6+). The 128D budget would be
exceeded. This expansion requires experimental evidence that the additional
interactions improve downstream C3 model performance.

### Alternative Interaction Operations (Phase 6 evaluation)

| Operation | Formula | Pros | Cons |
|-----------|---------|------|------|
| Product (current) | `a * b` | Simple, "simultaneous presence" | Zero bias for low values |
| Geometric mean | `sqrt(a * b)` | Less zero bias | Still zero-biased |
| Harmonic product | `2ab / (a + b)` | Less zero bias | Undefined at a=0 or b=0 |
| Concatenate | `[a; b]` | No information loss | Doubles dimensionality |
| Cosine similarity | `cos(a, b)` | Direction similarity | Only for vector pairs |

**Recommendation**: Keep element-wise product for Phase 6 Stage 1 (simplicity).
Test geometric mean as alternative in Phase 6 experiments.

### Phase 6 Priority: MEDIUM
The proxy fix (Stage 1) is straightforward and should be bundled with the
dependency injection refactoring of R3Extractor. The expansion (Stage 2)
is lower priority and requires empirical justification.

## References

### Primary Papers
- Harrison, P. M. C. & Pearce, M. T. (2020). Simultaneous consonance in music perception and composition. Psychological Review 127(2), 216-244.
- Sethares, W. A. (1993). Local consonance and the relationship between timbre and scale. JASA 94(3).
- Witek, M. A. G. et al. (2014). Effects of polyphonic context, instrumentation, and metrical structure on syncopation. Music Perception 32(2).
- Lerdahl, F. (2001). Tonal Pitch Space. Oxford UP.

### Toolkit Implementations
- No direct toolkit equivalents for cross-feature interactions.
- Cross-feature products are a custom R3 design pattern.
