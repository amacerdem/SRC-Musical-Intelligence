# AMSS M-Layer — Temporal Integration (2D)

**Layer**: Mathematical Model (M)
**Indices**: [5:7]
**Scope**: internal
**Activation**: sigmoid
**Model**: AMSS (STU-B1, Attention-Modulated Stream Segregation, 11D, beta-tier 70-90%)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | M0:stream_coherence | [0, 1] | Degree of perceptual stream formation. Object binding strength — how well acoustic elements cohere into a unified percept. Combines harmonic segregation (E1), spectral stream (E2), and temporal stream (E3). Bellier 2023: coherent STRF patterns reflect stream binding. |
| 6 | M1:segregation_depth | [0, 1] | Number of simultaneous streams tracked, normalized. ORN-related segregation depth — higher values indicate more concurrent streams successfully segregated. Basinski 2025: ORN scales with segregation demands. |

---

## Design Rationale

1. **Stream Coherence (M0)**: The integration of E-layer features into a single measure of how well the auditory scene is organized into perceptual objects. High coherence means strong harmonic grouping (E1), clear spectral boundaries (E2), and stable temporal continuity (E3) all converge. This is the "binding" signal — the degree to which acoustic features form a coherent stream.

2. **Segregation Depth (M1)**: Quantifies how many simultaneous streams are being maintained. In monophonic music this is low (~1 stream); in polyphonic music with multiple instruments, segregation depth increases. The ORN (Object-Related Negativity) amplitude scales with segregation demands, providing the neurophysiological basis.

---

## Mathematical Formulation

```
stream_coherence = sigma(w_harm * E1 + w_spec * E2 + w_temp * E3)

Parameters:
  w_harm = 0.40 (harmonic grouping weight — strongest cue)
  w_spec = 0.35 (spectral boundary weight)
  w_temp = 0.25 (temporal continuity weight)

segregation_depth = sigma(w_gate * E4 * (E2 + E3) / 2 + w_onset * E0)

Parameters:
  w_gate = 0.60 (attention-gated segregation)
  w_onset = 0.40 (onset-driven stream counting)
```

---

## H3 Dependencies (M-Layer)

M-layer primarily integrates E-layer outputs rather than reading new H3 tuples directly. Any additional H3 dependencies are inherited through the E-layer computation.

| Tuple | Feature | Purpose |
|-------|---------|---------|
| — | (inherited from E-layer) | Stream coherence integrates E1+E2+E3 |
| — | (inherited from E-layer) | Segregation depth integrates E0+E2+E3+E4 |

---

## Scientific Foundation

- **Basinski et al. 2025**: ORN amplitude scales with segregation demands F(2,170)=31.38 (EEG)
- **Bellier et al. 2023**: STRF coherence reflects perceptual stream binding in auditory cortex
- **Hausfeld et al. 2021**: Stream formation measurable via fMRI with attention modulation (d=0.60)

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/amss/temporal_integration.py`
