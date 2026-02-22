# SLEE — Cognitive Present

**Model**: Statistical Learning Expertise Enhancement
**Unit**: NDU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 7 | expectation_formation | Current distribution model state. Represents the instantaneous expectation formed from the statistical model, combining the E-layer distribution estimate with accumulated exposure. Reflects the online statistical learning process where expectations are continuously updated from incoming auditory regularities. Fong et al. 2020: MMN as prediction error under Bayesian framework with hierarchical processing. |
| 8 | cross_modal_binding | Current multisensory integration strength. Measures the real-time binding of cross-modal features, reflecting the IFG area 47m supramodal hub activity (Paraskevopoulos 2022: highest node degree in 5/6 network states). Porfyri et al. 2025: left MFG, IFS, and insula show greatest effective connectivity reorganization. |
| 9 | pattern_segmentation | Current boundary detection. Identifies segment boundaries in the auditory stream where statistical regularities shift, using spectral change and pitch change dynamics. Bridwell 2017: cortical sensitivity distinguishes patterned from random sequences (45% amplitude reduction). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 3 | M0 (value) | L2 (bidi) | Spectral change 100ms for segmentation |
| 1 | 21 | 4 | M18 (trend) | L0 (fwd) | Spectral trend 125ms for boundary detection |
| 2 | 23 | 3 | M0 (value) | L2 (bidi) | Pitch change 100ms for segmentation |
| 3 | 23 | 16 | M1 (mean) | L2 (bidi) | Mean pitch change 1s for regularity baseline |

---

## Computation

The P-layer captures the instantaneous cognitive state of the statistical learning system, reflecting what is happening in the current perceptual moment.

1. **expectation_formation**: Combines the E-layer statistical model (f01) with the M-layer exposure history to produce the current expectation state. Under the Bayesian predictive coding framework (Fong et al. 2020), this represents the prior that generates predictions about upcoming auditory events.

2. **cross_modal_binding**: Reflects the real-time strength of multisensory integration, drawing from the E-layer f03 (multisensory integration) and current interaction feature values. This captures the ongoing activity of the IFG supramodal hub in binding auditory, visual, and proprioceptive streams.

3. **pattern_segmentation**: Detects statistical boundaries using spectral change at 100ms, spectral trend at 125ms, pitch change at 100ms, and mean pitch change over 1s. When spectral or pitch dynamics shift sharply relative to their running baselines, a segment boundary is identified, signaling a transition between statistical contexts.

The P-layer provides the real-time snapshot that the F-layer uses for forward predictions.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f01 | Statistical model | Base expectation for formation |
| E-layer f03 | Multisensory integration | Current binding level |
| M-layer exposure_model | Accumulated exposure | Temporal context for expectation |
| R³[21] spectral_change | Spectral dynamics | Boundary detection signal |
| R³[23] pitch_change | Pitch dynamics | Sequence segmentation |
| H³ (4 tuples) | Multi-scale temporal morphology | Change and trend dynamics at 100ms-1s |
