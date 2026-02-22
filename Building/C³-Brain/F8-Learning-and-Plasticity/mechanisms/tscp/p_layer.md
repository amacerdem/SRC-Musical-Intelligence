# TSCP — Cognitive Present

**Model**: Timbre-Specific Cortical Plasticity
**Unit**: SPU
**Function**: F8 Learning & Plasticity
**Tier**: β
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | recognition_quality | Template matching quality. Aggregation of instrument identity features measuring how well the current timbre matches stored instrument templates. Maps to L-SMG/HG (Bellmann & Asano 2024: ALE peak, 4640 mm³ — primary timbre processing cluster for template storage). |
| 5 | enhanced_response | Training-dependent cortical response enhancement. Attention-like instrument-focused processing driven by plasticity markers. σ(0.60 * enhancement_function + 0.40 * tonalness). Alluri et al. 2012: timbral brightness bilateral STG Z=8.13, timbral fullness Z=7.35 during naturalistic music. |
| 6 | timbre_identity | Feature binding coherence. Coherence of spectral envelope, tristimulus, and temporal envelope into a unified instrument identity. σ(0.40 * trist_balance + 0.30 * (1-inharmonicity) + 0.30 * spectral_autocorrelation). Sturm et al. 2014: spectral centroid (timbre) has distinct activation spots in STG separate from lyrics and harmony. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 6 | 12 | 2 | M0 (value) | L2 (bidi) | Current warmth at 17ms |
| 7 | 13 | 2 | M0 (value) | L2 (bidi) | Current sharpness at 17ms |

---

## Computation

The P-layer computes the real-time cognitive state of timbre perception and plasticity:

1. **Recognition quality** (idx 4): Template matching that evaluates how well the incoming spectral envelope corresponds to stored instrument representations. Based on instrument identity aggregation across spectral features. Maps to the primary timbre processing cluster in L-SMG/HG identified by ALE meta-analysis (Bellmann & Asano 2024: 4640 mm³).

2. **Enhanced response** (idx 5): Combines the M-layer enhancement function with current tonalness to produce a real-time measure of training-dependent cortical enhancement. This captures the ATT-like (attention) boost that trained instrument timbres receive during auditory processing. Higher values indicate that the current stimulus is being processed with expert-level cortical resources.

3. **Timbre identity** (idx 6): Binds multiple spectral features (tristimulus balance, inharmonicity inverse, spectral autocorrelation) into a unified instrument identity representation. This coherent binding is what allows timbre to serve as a perceptual object — a "violin sound" rather than a collection of spectral features. Maps to distinct STG sub-regions (Sturm et al. 2014: ECoG high-gamma).

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| M-layer | enhancement_function | Training-dependent enhancement for response computation |
| E-layer | f01_trained_timbre_response | Tristimulus balance for identity binding |
| R³ [14] | tonalness | Harmonic-to-noise ratio for enhanced response |
| R³ [5] | inharmonicity | Instrument character for identity binding |
| R³ [17] | spectral_autocorrelation | Harmonic periodicity for identity coherence |
| R³ [12] | warmth | Current spectral warmth for template matching |
| R³ [13] | sharpness | Current spectral sharpness for template matching |
| H³ | 2 tuples (see above) | Fast spectral envelope at 17ms for real-time processing |
