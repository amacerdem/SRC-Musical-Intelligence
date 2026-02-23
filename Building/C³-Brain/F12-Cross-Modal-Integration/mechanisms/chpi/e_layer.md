# CHPI — Extraction

**Model**: Cross-Modal Harmonic Predictive Integration
**Unit**: PCU
**Function**: F12 Cross-Modal Integration
**Tier**: beta
**Layer**: E — Extraction
**Dimensions**: 4D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 0 | f01_crossmodal_prediction_gain | Enhancement of harmonic prediction accuracy from cross-modal convergence. Driven by mean cross-modal coupling at 500ms delta timescale, capturing how visual/motor streams improve harmonic anticipation beyond purely auditory prediction. sigma(0.35 * crossmodal_coupling_500ms + 0.35 * tonalness_mean_500ms + 0.30 * periodicity_trend_1s). Moller 2021: FA in left IFOF correlates with visual-auditory gain in pitch discrimination (p < 0.001). Takagi 2025: cross-modal transformer features explain dance-evoked brain activity better than unimodal features. |
| 1 | f02_voiceleading_parsimony | Voice-leading smoothness via minimal pitch movement, grounded in Neo-Riemannian geometry. Computed as inverse of voice-leading velocity and tension velocity at 100ms alpha timescale. sigma(0.40 * (1 - voiceleading_velocity_100ms) + 0.30 * (1 - tension_velocity_100ms) + 0.30 * consonance_100ms). Tymoczko 2011: voice-leading as movement in geometric chord space. Wagner 2018: MMN for harmonic intervals confirms pre-attentive voice-leading sensitivity (MMN=-0.34uV at 173ms, p=0.003). |
| 2 | f03_visual_motor_lead | Temporal advantage of visual/motor streams over purely auditory prediction. Combines mid-level coupling velocity at 125ms theta with cross-modal coupling at 100ms alpha. sigma(0.40 * midlevel_coupling_velocity_125ms + 0.30 * crossmodal_coupling_100ms + 0.30 * harmonic_change_100ms). de Vries & Wurm 2023: hierarchical motion prediction at ~110-500ms timescales (eta_p^2=0.49, p=8.3e-7). Tanaka 2021: mu suppression during audiovisual opera but not auditory-only. |
| 3 | f04_harmonic_surprise_modulation | Modulation of harmonic surprise by cross-modal context, implementing the uncertainty x surprise interaction. Driven by consonance entropy at 1s beat timescale and peak harmonic change at 100ms. sigma(0.35 * consonance_entropy_1s + 0.35 * harmonic_change_max_100ms + 0.30 * roughness_mean_500ms). Cheung 2019: uncertainty x surprise interaction predicts chord pleasure (beta=-0.124, p=0.000246). Gold 2023: replicates in VS and R STG during naturalistic listening. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 6 | 0 | M0 (value) | L2 (bidi) | Harmonic event at 25ms gamma |
| 1 | 6 | 3 | M0 (value) | L2 (bidi) | Harmonic change at 100ms alpha |
| 2 | 6 | 3 | M4 (max) | L2 (bidi) | Peak harmonic change at 100ms |
| 3 | 10 | 1 | M0 (value) | L2 (bidi) | Chord onset at 50ms gamma |
| 4 | 10 | 3 | M14 (periodicity) | L2 (bidi) | Chord periodicity at 100ms alpha |
| 5 | 0 | 3 | M0 (value) | L2 (bidi) | Tension level at 100ms alpha |
| 6 | 0 | 8 | M1 (mean) | L0 (fwd) | Mean tension over 500ms delta |
| 7 | 4 | 3 | M0 (value) | L2 (bidi) | Consonance at 100ms alpha |
| 8 | 4 | 16 | M1 (mean) | L0 (fwd) | Mean consonance over 1s beat |
| 9 | 4 | 16 | M20 (entropy) | L0 (fwd) | Consonance entropy over 1s beat |
| 10 | 23 | 3 | M8 (velocity) | L2 (bidi) | Tension velocity at 100ms alpha |
| 11 | 25 | 3 | M0 (value) | L2 (bidi) | Cross-modal coupling at 100ms alpha |
| 12 | 25 | 8 | M1 (mean) | L0 (fwd) | Mean cross-modal coupling over 500ms delta |
| 13 | 33 | 4 | M8 (velocity) | L0 (fwd) | Mid-level coupling velocity at 125ms theta |

---

## Computation

The E-layer extracts four explicit features characterizing cross-modal harmonic prediction:

1. **Cross-modal prediction gain** (f01): Quantifies the enhancement of harmonic prediction accuracy from cross-modal convergence. Driven by the mean cross-modal coupling strength over a 500ms delta window, combined with tonal context stability. In ecological listening, visual (notation reading, hand position observation) and motor (fingering patterns, bowing anticipation) streams provide temporal lead information that arrives 150-500ms before the auditory harmonic event. Even in audio-only contexts, the R3 interaction features (x_l0l5) capture the implicit multi-scale temporal binding that the brain uses as a substitute for explicit visual/motor information. Moller 2021 demonstrated that left IFOF fractional anisotropy correlates with audiovisual gain in pitch discrimination (p < 0.001), providing the white matter basis for cross-modal prediction enhancement.

2. **Voice-leading parsimony** (f02): Measures voice-leading smoothness through the inverse of spectral change velocity and tension velocity at the 100ms alpha timescale. Grounded in Tymoczko's geometric approach where voice-leading is movement in chord space, and Neo-Riemannian PLR transformations model efficient chord transitions via minimal pitch movement. Low velocity values indicate smooth voice-leading (high parsimony), which facilitates harmonic prediction. Wagner 2018 confirmed pre-attentive sensitivity to harmonic intervals via MMN (p=0.003), and Kim 2021 showed IFG connectivity specifically indexes syntactic irregularity in chords (p=0.024).

3. **Visual-motor lead** (f03): Captures the temporal advantage that visual and motor prediction streams provide over purely auditory statistical prediction. The mid-level coupling velocity at 125ms theta represents motor anticipation timescales, while cross-modal coupling at 100ms alpha represents the fast audiovisual binding. de Vries & Wurm 2023 demonstrated hierarchical cross-modal prediction at multiple timescales (~110ms optical flow, ~200ms view-dependent, ~500ms view-invariant), with eta_p^2=0.49. Tanaka 2021 showed motor mirror system engagement (mu suppression) during audiovisual opera observation but not auditory-only.

4. **Harmonic surprise modulation** (f04): Implements the nonlinear uncertainty x surprise interaction identified by Cheung 2019 (beta=-0.124, p=0.000246) and replicated by Gold 2023. Consonance entropy at 1s provides the uncertainty proxy (high entropy = uncertain harmonic context), while peak harmonic change at 100ms provides the surprise proxy. When cross-modal context is strong, surprise is attenuated; when context is weak, surprise passes through unmodulated. This captures how cross-modal information modulates the hedonic impact of harmonic violations.

All formulas use sigmoid activation with coefficient sums <= 1.0 (saturation rule).

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| R3 [0] | roughness | Harmonic tension proxy for voice-leading dissonance |
| R3 [4] | sensory_pleasantness | Chord consonance for harmonic context |
| R3 [6] | harmonic_change | Chord transition marker for event detection |
| R3 [10] | spectral_flux | Chord onset detection at spectral boundaries |
| R3 [23] | roughness_change | Tension trajectory for voice-leading velocity |
| R3 [25:33] | x_l0l5 | Cross-modal binding for low-level audiovisual coupling |
| R3 [33:41] | x_l4l5 | Mid-level harmonic integration for voice-leading coupling |
| H3 | 14 tuples (see above) | Multi-scale harmonic event detection, tension, cross-modal integration |
