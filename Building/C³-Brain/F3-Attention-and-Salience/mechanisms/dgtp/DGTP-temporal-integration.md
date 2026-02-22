# DGTP M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [3:5]
**Scope**: internal
**Activation**: sigmoid
**Model**: ASU-gamma2, Domain-General Temporal Processing (9D, gamma-tier 50-70%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:domain_correlation | [0, 1] | Correlation between music and speech timing. sigma(0.5*f22*f23 + 0.5*coupling_mean_1s). Product of music/speech timing captures co-activation; coupling mean adds sustained baseline. Dalla Bella 2024: ML classifiers identify shared timing features r>0.6. |
| 4 | M1:shared_variance | [0, 1] | Common timing factor variance. sigma(0.5*f24 + 0.5*coupling_stability_1s). Combines geometric-mean shared mechanism with coupling stability to estimate how much variance is truly domain-general. Di Stefano 2025: cross-domain training transfer mediated by shared variance. |

---

## Design Rationale

1. **Domain Correlation (M0)**: Computes the online correlation between music timing (f22) and speech timing (f23). The product f22*f23 gives instantaneous co-activation, while coupling_mean_1s provides a 1s smoothed baseline. High values indicate that both domains are simultaneously well-timed — evidence of shared processing.

2. **Shared Variance (M1)**: Quantifies the portion of timing that is truly domain-general. Uses the geometric-mean shared mechanism (f24) as the primary signal and coupling stability as a reliability indicator. This captures the latent common factor in the Dalla Bella 2024 ML framework.

---

## Mathematical Formulation

```
domain_correlation = sigma(0.5 * f22 * f23 + 0.5 * coupling_mean_1s)

  f22 = music_timing (E-layer)
  f23 = speech_timing (E-layer)
  coupling_mean_1s from H3 tuple (25, 16, 1, 0)

shared_variance = sigma(0.5 * f24 + 0.5 * coupling_stability_1s)

  f24 = shared_mechanism = sqrt(f22 * f23) (E-layer)
  coupling_stability_1s from H3 tuple (25, 16, 19, 0)
```

---

## H3 Dependencies (M-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (25, 16, 1, 0) | x_l0l5[0] mean H16 L0 | Coupling mean at 1s — baseline co-activation |
| (25, 16, 19, 0) | x_l0l5[0] stability H16 L0 | Coupling stability at 1s — reliability of shared timing |

---

## Scientific Foundation

- **Dalla Bella 2024**: ML classifiers identify shared timing features across music and speech (r>0.6)
- **Di Stefano 2025**: Cross-domain training transfer mediated by shared variance in temporal processing
- **Liu 2025**: D2-MSNs in striatum encode domain-general timing signals

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/dgtp/temporal_integration.py` (pending)
