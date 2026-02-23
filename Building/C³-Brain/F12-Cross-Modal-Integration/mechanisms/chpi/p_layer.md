# CHPI — Cognitive Present

**Model**: Cross-Modal Harmonic Predictive Integration
**Unit**: PCU
**Function**: F12 Cross-Modal Integration
**Tier**: beta
**Layer**: P — Cognitive Present
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | harmonic_context_strength | Tonal center stability combining tonalness and periodicity trend. Driven by mean tonalness over 1s beat window and periodicity trend over the same timescale. sigma(0.50 * tonalness_mean_1s + 0.50 * periodicity_trend_1s). High values indicate a strong, stable tonal center that anchors harmonic predictions. Kim 2021: STG connectivity indexes perceptual harmonic context (p < 0.001). Cheung 2019: tonal context modulates uncertainty and downstream pleasure response. |
| 5 | crossmodal_convergence | Degree of multi-stream alignment at the current moment. Combines instantaneous cross-modal coupling at 100ms alpha with mid-level harmonic integration at 500ms delta. sigma(0.50 * crossmodal_coupling_100ms + 0.50 * midlevel_coupling_500ms). Reflects the real-time convergence of visual, motor, and auditory streams in the STS integration hub. Paraskevopoulos 2022: increased intra-network connectivity during multisensory statistical learning (p < 0.001 FDR). |
| 6 | voiceleading_smoothness | Current voice-leading parsimony reflecting how smooth the present harmonic transition is. Computed from the inverse of voice-leading velocity at 100ms alpha timescale. sigma(0.50 * (1 - voiceleading_velocity_100ms) + 0.50 * consonance_100ms). High smoothness indicates minimal pitch movement in chord voices, facilitating prediction. Tymoczko 2011: smooth voice-leading as distance minimization in geometric chord space. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 21 | 3 | M8 (velocity) | L0 (fwd) | Voice-leading velocity at 100ms alpha |
| 1 | 21 | 4 | M0 (value) | L0 (fwd) | Voice-leading at 125ms theta |
| 2 | 14 | 8 | M1 (mean) | L0 (fwd) | Mean tonalness over 500ms delta |
| 3 | 14 | 16 | M1 (mean) | L0 (fwd) | Mean tonalness over 1s beat |
| 4 | 5 | 16 | M18 (trend) | L0 (fwd) | Periodicity trend over 1s beat |
| 5 | 33 | 8 | M0 (value) | L0 (fwd) | Mid-level coupling at 500ms delta |

---

## Computation

The P-layer captures the cognitive present state of cross-modal harmonic processing through three concurrent representations:

1. **Harmonic context strength** (idx 4): Monitors the stability of the tonal center by combining long-timescale tonalness (1s mean) with the trend of periodicity over the same window. A strong, stable tonal center provides the reference frame against which harmonic predictions are evaluated. When harmonic_context_strength is high, the predictive coding system has a confident tonal prior, leading to sharper prediction errors for unexpected chords. When low, the system is in an ambiguous tonal state where many chord progressions are equally likely. This dimension feeds forward into the F-layer's next_chord_prediction and integration_confidence.

2. **Crossmodal convergence** (idx 5): Captures the real-time degree of alignment between multiple sensory and motor streams. The fast 100ms coupling tracks instantaneous audiovisual binding, while the 500ms mid-level coupling captures the slower motor anticipation stream. High convergence indicates that visual, motor, and auditory information are aligned -- the musician is "in the groove" with all streams predicting the same harmonic outcome. Low convergence indicates stream conflict or unimodal processing. Paraskevopoulos 2022 demonstrated that musicians show compartmentalized (increased intra-network, decreased inter-network) connectivity during multisensory learning, consistent with refined cross-modal integration.

3. **Voice-leading smoothness** (idx 6): Provides a real-time readout of how parsimonious the current harmonic transition is. Derived from the inverse of spectral change velocity at 100ms, this captures whether chord voices are moving by minimal intervals (smooth) or large leaps (rough). Smooth voice-leading facilitates prediction because the next chord is geometrically close to the current one in Tymoczko's chord space. This dimension interacts with the E-layer's f02_voiceleading_parsimony but provides the instantaneous present state rather than the extracted feature.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [5] | periodicity | Tonal center stability for harmonic context |
| R3 [14] | tonalness | Key clarity for harmonic context strength |
| R3 [21] | spectral_change | Voice-leading velocity for smoothness computation |
| R3 [25:33] | x_l0l5 | Cross-modal coupling for convergence |
| R3 [33:41] | x_l4l5 | Mid-level coupling for convergence |
| H3 | 6 tuples (see above) | Multi-scale tonalness, periodicity trend, voice-leading, coupling |
| CHPI E-layer | f02_voiceleading_parsimony | Extracted parsimony feeds present-state smoothness |
