# IACM M-Layer — Temporal Integration (3D)

**Layer**: Mathematical Model (M)
**Indices**: [3:6]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 3 | M0:attention_capture | [0, 1] | P3a-proportional attention capture. sigma(0.5*f04_inharmonic_capture + 0.5*approx_entropy_val). P3a proportional to ApproxEntropy. Basinski 2025: inharmonic sounds elicit involuntary attention capture. |
| 4 | M1:approx_entropy | [0, 1] | Approximate entropy of spectral content. sigma(0.5*spectral_flatness + 0.5*(1-tonalness)). Harmonic M=0.02, Inharmonic M=0.19. Quantifies spectral unpredictability. |
| 5 | M2:object_perception_or | [0, 1] | Object perception odds ratio. sigma(...). OR_inharmonic=16.44, OR_changing=62.80. Basinski 2025: odds of perceiving multiple objects given inharmonic or changing spectra. |

---

## Design Rationale

1. **Attention Capture (M0)**: The core computational model of involuntary attention capture by inharmonic sounds. Combines E-layer inharmonic detection (f04) with raw approximate entropy. This models the P3a ERP component, which reflects involuntary attention switching. The P3a amplitude is proportional to spectral unpredictability.

2. **Approximate Entropy (M1)**: A normalized measure of spectral unpredictability combining spectral flatness (noise-likeness) with inverse tonalness (harmonicity). Harmonic sounds score M=0.02 (highly predictable), while inharmonic sounds score M=0.19 (unpredictable). This captures the fundamental distinction driving attention capture.

3. **Object Perception OR (M2)**: Converts E-layer object segregation into a calibrated odds ratio. Inharmonic sounds have OR=16.44 for eliciting object-related negativity; changing spectra reach OR=62.80. This quantifies how likely the auditory system is to perceive multiple concurrent sound sources.

---

## Mathematical Formulation

```
attention_capture = sigma(0.5 * f04_inharmonic + 0.5 * approx_entropy)

approx_entropy = sigma(0.5 * spectral_flatness + 0.5 * (1 - tonalness))

object_perception_or = sigma(w1 * f05_object_segregation + w2 * approx_entropy)

Effect sizes (Basinski 2025):
  d_P3a = -1.37 (inharmonic > harmonic P3a amplitude)
  OR_inharmonic = 16.44 (ORN odds ratio)
  OR_changing = 62.80 (changing spectrum ORN odds ratio)
```

---

## H3 Dependencies (M-Layer)

No additional direct H3 reads. M-layer dimensions are derived from E-layer computations:

| Source | Derivation |
|--------|-----------|
| E0:inharmonic_capture | f04 feeds M0:attention_capture |
| E1:object_segregation | f05 feeds M2:object_perception_or |
| E2:precision_weighting | f06 provides context modulation |

---

## Scientific Foundation

- **Basinski 2025**: P3a amplitude d=-1.37 for inharmonic vs harmonic (EEG, N=35)
- **Basinski 2025**: OR=16.44 inharmonic ORN, OR=62.80 changing spectrum (N=35)
- **Koelsch 1999**: P3a involuntary attention to spectral deviants in music
- **Alain 2007**: ORN as index of concurrent auditory object segregation

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/iacm/temporal_integration.py`
