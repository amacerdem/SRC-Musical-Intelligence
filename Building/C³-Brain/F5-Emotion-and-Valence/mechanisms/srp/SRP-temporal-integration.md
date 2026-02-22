# SRP Temporal Integration — Temporal Response + Musical Meaning (7D)

**Layer**: Temporal Integration (T+M)
**Indices**: [6:13]
**Scope**: internal
**Activation**: sigmoid / clamp [-1, 1] (prediction_match, appraisal)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 6 | T0:tension | [0, 1] | Huron T: preparatory arousal before event. f06 = sigma(0.40 * harmonic_tension + 0.30 * energy_buildup_H20 + 0.30 * uncertainty_H18). Scales with uncertainty x significance. Huron 2006: tension response engages autonomic preparation. |
| 7 | T1:prediction_match | [-1, 1] | Huron P: confirmation/violation signal. f07 = tanh(0.50 * consonance_trajectory + 0.30 * spectral_stability + 0.20 * onset_regularity). +1 = confirmed prediction, -1 = violated. Phasic at event boundaries. |
| 8 | T2:reaction | [0, 1] | Huron R: reflexive brainstem response ~150ms after event. f08 = sigma(0.50 * onset_strength_velocity + 0.30 * loudness_acceleration + 0.20 * spectral_flux_peak). Startle/orienting reflex. |
| 9 | T3:appraisal | [-1, 1] | Huron A: conscious evaluation 0.5-2s after event. f09 = tanh(0.40 * pleasure + 0.30 * prediction_match + 0.30 * opioid_proxy). Context-dependent reappraisal. OFC + vmPFC evaluation circuit. |
| 10 | M0:harmonic_tension | [0, 1] | Tonal distance from tonic. f10 = sigma(0.50 * roughness_trend_H18 + 0.30 * inv_consonance + 0.20 * entropy_H18). High = dominant/applied chord, low = tonic resolved. |
| 11 | M1:dynamic_intensity | [0, 1] | Energy trajectory (crescendo/decrescendo). f11 = sigma(0.70 * energy_velocity_H18 + 0.30 * energy_acceleration_H18). Correlates with arousal. Panksepp 1995: crescendo = most common chill trigger. |
| 12 | M2:peak_detection | [0, 1] | Chill trigger detection. f12 = sigma(0.30 * onset_peak + 0.25 * dynamic_intensity + 0.25 * harmonic_resolution + 0.20 * stg_nacc_coupling). Sloboda 1991: appoggiaturas, crescendos, harmonic changes. |

---

## Design Rationale

1. **Tension (T0)**: Huron's ITPRA tension response — the preparatory arousal that precedes musical events. Combines harmonic tension (tonal instability), energy buildup (crescendo trajectory at phrase level H20), and uncertainty (information-theoretic unpredictability). Engages autonomic system seconds before the event. Speed of musical events determines engagement — slow passages allow full tension buildup, fast passages may bypass.

2. **Prediction Match (T1)**: Huron's P response — the ~130-250ms pre-event signal of whether prediction was confirmed or violated. Uses consonance trajectory (is the harmony heading where expected?), spectral stability (timbral predictability), and onset regularity (rhythmic predictability). Bipolar: confirmed predictions feel good (positive), violations feel jarring (negative) until reappraisal.

3. **Reaction (T2)**: Huron's R response — the reflexive brainstem startle/orienting reflex ~150ms after a musical event. Driven by onset strength velocity (sudden loud attacks), loudness acceleration (rapid dynamic change), and spectral flux peaks (timbral surprises). This is the fastest, most automatic component — cannot be suppressed.

4. **Appraisal (T3)**: Huron's A response — conscious evaluation 0.5-2s after the event. Integrates current pleasure state, prediction match outcome, and opioid hedonic quality. Context-dependent: the same event can receive positive or negative appraisal depending on musical context. OFC and vmPFC evaluation circuit.

5. **Harmonic Tension (M0)**: Musical-theoretic tension — distance from tonic stability. High roughness trend (increasing dissonance), inverse consonance (current dissonance level), and high entropy (spectral unpredictability) all contribute. This feeds the reward pathway: sustained tension followed by resolution produces the classic anticipation-consummation cycle.

6. **Dynamic Intensity (M1)**: Energy trajectory that maps crescendos and decrescendos. Predominantly driven by amplitude velocity (rate of energy change) with acceleration as a secondary cue for natural vs forced dynamics. Panksepp (1995) identified crescendos as the most common trigger for musical chills across all genres.

7. **Peak Detection (M2)**: The composite chill trigger detector. Combines sudden onsets (Sloboda 1991 appoggiaturas), dynamic intensity (crescendos), harmonic resolution (dissonance-to-consonance), and auditory-reward coupling strength. When multiple triggers converge, peak_detection approaches 1.0, signaling a potential chills moment.

---

## Mathematical Formulation

```
ITPRA Temporal Model (Huron 2006):
  I — Imagination: seconds to minutes before (feeds reward_forecast in F-layer)
  T — Tension:     seconds before event     → T0
  P — Prediction:  130-250ms before event    → T1
  R — Reaction:    ~150ms after event        → T2
  A — Appraisal:   0.5-2s after event        → T3

Musical Feature Integration:
  harmonic_tension = sigma(0.50 * roughness_trend + 0.30 * (1 - consonance_mean) + 0.20 * entropy)
  dynamic_intensity = sigma(0.70 * dE/dt + 0.30 * d²E/dt²)
  peak_detection = sigma(0.30 * onset_peak + 0.25 * dyn_int + 0.25 * resolution + 0.20 * coupling)
```

---

## H3 Dependencies (Temporal Integration)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (0, 18, 18, 0) | roughness trend H18 L0 | Roughness trajectory at phrase level — harmonic tension |
| (0, 18, 0, 2) | roughness value H18 L2 | Current dissonance — inv_consonance |
| (22, 18, 0, 2) | distribution_entropy value H18 L2 | Entropy at phrase level — uncertainty |
| (7, 20, 8, 0) | amplitude velocity H20 L0 | Energy buildup rate at 5s — tension ramp |
| (7, 18, 8, 0) | amplitude velocity H18 L0 | Energy velocity at phrase — dynamic_intensity |
| (7, 18, 11, 0) | amplitude acceleration H18 L0 | Energy acceleration at phrase — buildup curvature |
| (4, 18, 8, 0) | sensory_pleasantness velocity H18 L0 | Consonance trajectory — prediction match |
| (16, 18, 19, 2) | spectral_smoothness stability H18 L2 | Spectral stability at phrase — prediction match |
| (11, 16, 14, 2) | onset_strength periodicity H16 L2 | Onset regularity at 1s — prediction match |
| (11, 16, 8, 0) | onset_strength velocity H16 L0 | Onset velocity — reaction trigger |
| (10, 16, 11, 0) | spectral_flux acceleration H16 L0 | Spectral flux jerk — reaction surprise |
| (11, 18, 4, 2) | onset_strength max H18 L2 | Peak onset at phrase — peak detection trigger |
| (4, 18, 18, 0) | sensory_pleasantness trend H18 L0 | Consonance trend — harmonic resolution signal |

## R3 Dependencies

| Index | Feature | Usage |
|-------|---------|-------|
| [0] | roughness | M0: harmonic tension, inverse consonance |
| [4] | sensory_pleasantness | T1: consonance trajectory, M2: resolution |
| [7] | amplitude | T0: energy buildup, M1: dynamic intensity |
| [10] | spectral_flux | T2: reaction trigger (spectral surprise) |
| [11] | onset_strength | T2: reaction (onset velocity), M2: peak trigger |
| [16] | spectral_smoothness | T1: spectral stability for prediction match |
| [22] | distribution_entropy | T0: uncertainty context |

---

## Scientific Foundation

- **Huron 2006**: ITPRA five-response model — Imagination, Tension, Prediction, Reaction, Appraisal (Sweet Anticipation, MIT Press)
- **Sloboda 1991**: Musical structure triggers — appoggiaturas, crescendos, harmonic changes (N=83, survey)
- **Panksepp 1995**: Crescendo = most common chill trigger across genres (N=328, survey)
- **Cheung 2019**: Uncertainty x surprise interaction determines pleasure (fMRI, N=39, d=3.8-8.53)
- **Schultz 2016**: Two-component phasic DA — 40-120ms detection + value-coding RPE
- **Grewe 2009**: Inter-chill refractory ~10-30s, ~3.7 chills per excerpt (N=38)

## Implementation

File: `Musical_Intelligence/brain/functions/f5/mechanisms/srp/temporal_integration.py`
