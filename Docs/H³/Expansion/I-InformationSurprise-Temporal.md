# Group I: Information & Surprise [87:94] -- Temporal Demand Analysis

> Version 2.0.0 | Updated 2026-02-13

## 1. Group Summary

Group I introduces 7 features that quantify information-theoretic properties of the musical signal -- entropy, surprise, prediction error, and uncertainty across melodic, harmonic, rhythmic, and spectral domains. These are meta-features: they measure properties of the signal's statistical structure rather than the signal itself.

| Feature | Index | Dim | Quality | Description |
|---------|:-----:|:---:|:-------:|-------------|
| melodic_entropy | 87 | 1D | A | Shannon entropy of pitch class distribution (melodic predictability) |
| harmonic_entropy | 88 | 1D | A | Entropy of chroma distribution (harmonic predictability) |
| rhythmic_information_content | 89 | 1D | A | Information content of inter-onset intervals |
| spectral_surprise | 90 | 1D | A | KL divergence between predicted and actual spectral frame |
| information_rate | 91 | 1D | S | Mutual information between successive frames |
| predictive_entropy | 92 | 1D | A | Entropy of the predictive distribution (prediction uncertainty) |
| tonal_ambiguity | 93 | 1D | A | Inverse key clarity weighted by competing key strengths |

**Dependencies**: F chroma, G onset, H key (pipeline stage 3 -- computed after all upstream groups).

**Quality distribution**: 6 Approximate, 1 Standard (information_rate). The Approximate ratings reflect the use of EMA running statistics rather than exact windowed computations.

**Implementation note**: All I group features use exponential moving average (EMA) running statistics with tau=2.0s and a 344-frame warm-up ramp. This warm-up constraint means that early frames produce attenuated values; see Section 8 for interaction with H3 horizons.

---

## 2. Temporal Relevance

Group I features are intrinsically temporal -- they measure surprise, prediction error, and uncertainty, all of which are defined relative to accumulated context. A single frame's "entropy" is meaningful only in the context of the distribution that produced it. This makes I group features uniquely suited for H3 temporal analysis: H3 captures the *dynamics of these dynamics* -- how the overall level of musical surprise, uncertainty, and information flow evolves across the arc of a piece.

Key temporal questions H3 addresses for Group I:
- Is overall surprise increasing or decreasing across this section? (predictive_entropy trend at Macro)
- What is the arc of musical tension across the entire piece? (predictive_entropy trajectory at H18-H20)
- How variable is the information flow rate? (information_rate std at Meso-Macro)
- Are moments of melodic surprise clustering at phrase boundaries? (melodic_entropy peaks at Meso)
- Is tonal ambiguity resolving or deepening? (tonal_ambiguity trend at Macro)

The combination of I group features with H3 temporal morphs creates a powerful second-order representation: "the trend of entropy" or "the periodicity of surprise." This is exactly the substrate that predictive coding models (PCU) and reward prediction models (RPU) require to operate at structural timescales.

---

## 3. Horizon Mapping

| Feature | Indices | Horizons | Band | Rationale |
|---------|---------|----------|------|-----------|
| melodic_entropy [87] | 1D | H6, H9, H12, H16 | Micro-Macro | Melodic predictability at note/phrase/section scale |
| harmonic_entropy [88] | 1D | H9, H12, H16, H18 | Meso-Macro | Harmonic surprise accumulates at chord/phrase/section scale |
| rhythmic_IC [89] | 1D | H9, H11, H12 | Meso | Rhythmic surprise at beat/phrase timescale |
| spectral_surprise [90] | 1D | H6, H9, H12 | Micro-Meso | Spectral prediction error at beat scale (fast response) |
| information_rate [91] | 1D | H12, H16, H18 | Meso-Macro | Information flow rate meaningful at phrase/section scale |
| predictive_entropy [92] | 1D | H9, H12, H16, H18 | Meso-Macro | Prediction uncertainty at phrase/section (tension arc) |
| tonal_ambiguity [93] | 1D | H12, H16, H18, H20 | Meso-Macro | Tonal uncertainty requires section/movement-scale context |

### Horizon Heatmap

```
Horizon  H6   H9   H11  H12  H16  H18  H20
Band     Mic  Meso Meso Meso Mac  Mac  Mac
         ====================================
melodic_entropy   [X]  [X]   .   [X]  [X]   .    .
harmonic_entropy   .   [X]   .   [X]  [X]  [X]   .
rhythmic_IC        .   [X]  [X]  [X]   .    .    .
spectral_surprise [X]  [X]   .   [X]   .    .    .
information_rate   .    .    .   [X]  [X]  [X]   .
predictive_entropy .   [X]   .   [X]  [X]  [X]   .
tonal_ambiguity    .    .    .   [X]  [X]  [X]  [X]
         ====================================
Count              2    5    1    7    5    4    1
```

**Key observations**:
- H12 (525ms, phrase scale) is the universal horizon -- all 7 features are demanded there.
- Demand is concentrated in Meso-Macro bands, reflecting the structural nature of information-theoretic features.
- No Ultra demand; information-theoretic features are consumed at section scale, not movement/piece scale.
- Only melodic_entropy and spectral_surprise reach into Micro (H6), as they can meaningfully characterize note-level surprise.
- rhythmic_IC is the most narrowly banded feature (H9-H12 only), reflecting its beat-specific domain.

---

## 4. Morph Profiles

All I group features share a common morph profile, reflecting their shared information-theoretic character. The key insight is that these features already encode uncertainty/surprise, so H3 morphs compute statistics *of* these statistics -- a second-order representation.

### Universal I Group Morphs

| Morph | ID | Demand | Rationale |
|-------|----|:------:|-----------|
| Value | M0 | High | Instantaneous entropy/surprise level |
| Mean | M1 | High | Average uncertainty level over horizon window |
| Std | M2 | High | Variability of uncertainty -- is surprise steady or volatile? |
| Max | M4 | Medium | Peak surprise moment in window |
| Velocity | M8 | Medium | Rate of uncertainty change -- surprise acceleration |
| Trend | M18 | High | Surprise trajectory arc -- the tension curve |
| Entropy | M20 | Medium | Entropy of entropy -- meta-uncertainty (how predictable is the unpredictability?) |

### Feature-Specific Emphasis

**predictive_entropy [92]**: Most demanded feature in I group. M0, M1, M2, M18 are core -- together they define the "tension arc" that PCU and RPU models require. The combination `predictive_entropy x M18(trend) x L1(Prediction)` captures "how prediction uncertainty is expected to evolve" -- a key input for anticipatory models.

**melodic_entropy [87]**: M0, M1, M4, M8 are primary. M4 (max) identifies moments of peak melodic surprise (unexpected intervals). M8 (velocity) captures how quickly melodic predictability changes -- fast increases signal boundary events.

**information_rate [91]**: M0, M1, M18, M19 (stability) are primary. Stability of information rate indicates compositional consistency; trend indicates complexity trajectory.

---

## 5. Law Preferences

| Law | Code | Primary Users | I Group Application |
|-----|------|---------------|---------------------|
| L0 (Memory) | Past | IMU | Accumulated surprise from past context; emotional memory of uncertainty experienced so far |
| L1 (Prediction) | Future | PCU | Anticipating upcoming surprise; predicting whether uncertainty will increase or resolve |
| L2 (Integration) | Both | RPU | Bidirectional uncertainty assessment; evaluating overall information structure |

**Distribution**: L1 (Prediction) is the most demanded law for I group features, because information-theoretic features are inherently about prediction. PCU models use L1 to predict future surprise trajectories. L0 (Memory) is demanded by IMU models that encode the accumulated emotional impact of past surprises. L2 is used by RPU for retrospective evaluation of information structure.

---

## 6. Consuming Units

| Unit | Models | I Features | Mechanism | Priority |
|------|:------:|-----------|-----------|:--------:|
| PCU | HTP, ICEM, WMED, CHPI, PWUP | All 7, especially predictive_entropy, melodic_entropy, spectral_surprise | PPC, TPC, MEM, C0P | High |
| RPU | Most models | predictive_entropy, melodic_entropy, harmonic_entropy, information_rate | AED, CPD, C0P | Very High |
| IMU | PMIM, HCMC, MSPBA | predictive_entropy, melodic_entropy, harmonic_entropy | MEM, SYN | High |
| NDU | SSNI, EDNR | melodic_entropy, spectral_surprise | ASA | Medium-High |
| ARU | PUPF | predictive_entropy | AED | Medium |

### Demand Concentration

RPU (Reward Prediction Unit) has the highest priority for I group features. RPU's core function is evaluating musical reward, and information-theoretic features provide the substrate for reward prediction error -- the difference between expected and experienced surprise. RPU models demand predictive_entropy and melodic_entropy at H12-H18 under all three laws, creating one of the densest demand clusters in the entire H3 space.

PCU (Predictive Coding Unit) is the second-largest consumer, using all 7 I features across its 5 most relevant models. ICEM (Information-Complexity Estimation Model) and WMED (Weighted Multi-scale Entropy Dynamics) are particularly heavy consumers, demanding I features at 4+ horizons each.

NDU demands I features selectively -- only melodic_entropy and spectral_surprise, which serve as novelty detection inputs at fast timescales (H6-H9 via ASA mechanism).

---

## 7. Estimated Tuple Count

| Source | Features | Horizons | Morphs | Laws | Est. Tuples |
|--------|:--------:|:--------:|:------:|:----:|:-----------:|
| predictive_entropy | 1 | 4 (H9,H12,H16,H18) | 7 (M0,M1,M2,M4,M8,M18,M20) | 3 (all) | ~84 |
| melodic_entropy | 1 | 4 (H6,H9,H12,H16) | 5 (M0,M1,M4,M8,M18) | 2 (L0,L1) | ~40 |
| harmonic_entropy | 1 | 4 (H9,H12,H16,H18) | 5 (M0,M1,M2,M18,M20) | 2 (L0,L2) | ~40 |
| information_rate | 1 | 3 (H12,H16,H18) | 4 (M0,M1,M18,M19) | 2 (L0,L1) | ~24 |
| spectral_surprise | 1 | 3 (H6,H9,H12) | 4 (M0,M1,M2,M4) | 2 (L0,L1) | ~24 |
| tonal_ambiguity | 1 | 4 (H12,H16,H18,H20) | 4 (M0,M1,M18,M2) | 2 (L0,L2) | ~32 |
| rhythmic_IC | 1 | 3 (H9,H11,H12) | 3 (M0,M1,M2) | 2 (L0,L1) | ~18 |
| **Total** | **7** | | | | **~262** |

Deduplication across units reduces the gross count by ~10-20%. Tier-dependent morph expansion (alpha models demanding additional morphs like M6, M7) increases the count by ~15-25%. **Estimated net: ~300-500 tuples**.

Breakdown by consumer: PCU contributes ~100-150, RPU ~100-150, IMU ~50-100, NDU+ARU ~50-100.

---

## 8. Predictive Coding Connection

Group I features occupy a privileged position in the H3 temporal demand landscape because they bridge two levels of temporal processing:

1. **R3 level**: I features encode frame-level prediction error and uncertainty (e.g., "this frame is surprising relative to recent context").
2. **H3 level**: Temporal morphs of I features encode how prediction error evolves over structural timescales (e.g., "surprise is increasing across this section").

This two-level structure maps directly onto hierarchical predictive coding theory (Friston, 2005; Clark, 2013), where prediction errors at one level become the inputs to prediction at the next level. The H3 tuple `(92, H18, M18, L1)` -- predictive_entropy trend at 2s under Prediction law -- encodes exactly this: "how is prediction uncertainty expected to trend over the next 2 seconds?" This is a prediction *about* prediction, the core computation of hierarchical predictive coding.

PCU models (especially ICEM and CHPI) exploit this hierarchical structure extensively. The I group + H3 combination is the primary substrate through which the MI architecture implements multi-level predictive coding.

---

## 9. Warm-Up Interaction

All I group features use EMA running statistics with a 344-frame (~2s) warm-up ramp. During warm-up, feature values are attenuated by a ramp factor that increases linearly from 0 to 1. This has a direct interaction with H3:

- **Micro horizons (H0-H7, up to 250ms)**: H3 morphs computed during the warm-up period will reflect the warm-up attenuation rather than true feature dynamics. However, only melodic_entropy and spectral_surprise are demanded at H6, and this horizon's 200ms window is shorter than the 2s warm-up. In practice, the warm-up has largely stabilized by the time musically meaningful analysis begins (first few seconds of audio are typically onset/introduction).
- **Meso and above (H9+)**: The analysis windows exceed or approach the warm-up duration, so H3 morphs at these horizons are computed over largely stable I feature values.

This warm-up interaction is one reason I group demand is concentrated at Meso-Macro rather than Micro horizons.

---

## 10. Cross-References

- **H3 Architecture**: [../H3-TEMPORAL-ARCHITECTURE.md](../H3-TEMPORAL-ARCHITECTURE.md)
- **Expansion Index**: [00-INDEX.md](00-INDEX.md)
- **R3 Feature Catalog**: [../../R3/Registry/FeatureCatalog.md](../../R3/Registry/FeatureCatalog.md)
- **Horizon Catalog**: [../Registry/HorizonCatalog.md](../Registry/HorizonCatalog.md)
- **Morph Catalog**: [../Registry/MorphCatalog.md](../Registry/MorphCatalog.md)
- **Law Catalog**: [../Registry/LawCatalog.md](../Registry/LawCatalog.md)
- **PCU Demand Profile**: [../Demand/PCU-H3-DEMAND.md](../Demand/PCU-H3-DEMAND.md)
- **RPU Demand Profile**: [../Demand/RPU-H3-DEMAND.md](../Demand/RPU-H3-DEMAND.md)
- **IMU Demand Profile**: [../Demand/IMU-H3-DEMAND.md](../Demand/IMU-H3-DEMAND.md)
- **NDU Demand Profile**: [../Demand/NDU-H3-DEMAND.md](../Demand/NDU-H3-DEMAND.md)
- **ARU Demand Profile**: [../Demand/ARU-H3-DEMAND.md](../Demand/ARU-H3-DEMAND.md)
- **Demand Address Space**: [../Registry/DemandAddressSpace.md](../Registry/DemandAddressSpace.md)
- **Pipeline / WarmUp**: [../Pipeline/WarmUp.md](../Pipeline/WarmUp.md)
- **H Group (dependency -- harmony)**: [H-HarmonyTonality-Temporal.md](H-HarmonyTonality-Temporal.md)
- **F Group (dependency -- chroma)**: [F-PitchChroma-Temporal.md](F-PitchChroma-Temporal.md)
- **G Group (dependency -- onset)**: [G-RhythmGroove-Temporal.md](G-RhythmGroove-Temporal.md)

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 2.0.0 | 2026-02-13 | Initial Group I temporal demand analysis (Phase 4G) |
