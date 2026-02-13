# C0P — Cognitive Projection

| Field | Value |
|-------|-------|
| NAME | C0P |
| FULL_NAME | Cognitive Projection |
| CIRCUIT | Mesolimbic (reward & pleasure) |
| OUTPUT_DIM | 30 |
| HORIZONS | H18 (2 s), H19 (3 s), H20 (5 s) |

## Description

Cognitive Projection models how top-down cognitive expectations are mapped onto reward pathways in the mesolimbic dopaminergic system. While AED captures bottom-up entrainment and CPD detects autonomic peaks, C0P encodes the anticipatory component — the listener's prediction about what will happen next and the reward signal generated when those predictions are confirmed or violated. This mechanism operates at longer timescales (2-5 s) where conscious musical expectation unfolds.

## 3x10D Sub-Section Structure

| Dims | Horizon | Computes |
|------|---------|----------|
| 0-9 | H18 (2 s) | Phrase-level anticipation: short-range predictions within a musical phrase. Expectation about melodic continuation, harmonic resolution, rhythmic completion (Pearce & Wiggins 2012). Prediction error drives dopaminergic responses in caudate nucleus. |
| 10-19 | H19 (3 s) | Inter-phrase anticipation: predictions spanning phrase boundaries. "What comes next" expectation at section transitions. Aligns with anticipatory dopamine release in caudate (Salimpoor et al. 2011). |
| 20-29 | H20 (5 s) | Anticipation horizon: maximal window of conscious musical prediction. Tracks whether music approaches or retreats from a predicted goal state, modulating the "wanting" component of reward (Berridge 2003). |

## H3 Demand

### R3 Feature Inputs

| R3 Domain | Indices | Features | Consuming Units |
|-----------|---------|----------|-----------------|
| A: Consonance | [0]-[6] | harmonicity, consonance_dissonance, roughness | ARU (PUPF, NEMAC via P1), RPU (MCCN, SSPS), PCU (PWUP) |
| B: Energy | [7]-[11] | loudness, velocity_A, rms_energy | ARU (PUPF, NEMAC via P5), RPU (MCCN, SSPS), PCU (WMED) |
| E: Interactions | [25]-[48] | Cross-domain coupling terms | ARU (PUPF, NEMAC via P3), RPU (MCCN, SSPS), PCU (PWUP, WMED) |
| C: Timbre | [12]-[20] | spectral_centroid, brightness_kuttruff | ARU (NEMAC via P1), RPU (MCCN, SSPS) |
| D: Change | [21]-[24] | spectral_flux | PCU (WMED) |

C0P's R3 inputs reflect cognitive anticipation features: consonance trend (A) tracks harmonic resolution expectation, energy trajectory (B) captures dynamic build-up toward predicted goals, and cross-domain coupling (E) provides the interaction context for coherent prediction. ARU accesses features via pathways; RPU and PCU access directly.

### Per-Horizon Morph Profile

| Horizon | Morphs | Rationale |
|---------|--------|-----------|
| H18 (2 s, 345 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M18 (trend), M19 (stability) | Phrase-level anticipation — short-range predictions within a phrase; trend captures approach/retreat from predicted goal; stability measures prediction confidence |
| H19 (3 s, 517 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M18 (trend), M19 (stability) | Inter-phrase anticipation — predictions spanning phrase boundaries; trend tracks "what comes next" expectation at section transitions |
| H20 (5 s, 861 frames) | M0 (value), M1 (mean), M2 (std), M8 (velocity), M18 (trend), M19 (stability) | Anticipation horizon — maximal conscious musical prediction window; trend and stability modulate the "wanting" component of reward |

All three horizons share the same morph profile. Trend (M18) and stability (M19) are the distinctive morphs — they capture whether music approaches or retreats from a predicted goal state and how confident the prediction is.

### Law Distribution

| Law | Units | Models | Rationale |
|-----|-------|:------:|-----------|
| L0 (Memory) | PCU | 1 | Maintaining prediction priors from accumulated context |
| L1 (Prediction) | ARU, RPU, PCU | 5 | Anticipatory projection — C0P's primary function; generating expectations about what comes next |
| L2 (Integration) | ARU, RPU, PCU | 5 | Integrating anticipatory signals with current sensory evidence for coherent prediction |

L1 (Prediction) and L2 (Integration) are equally represented. C0P is inherently predictive (L1 — projecting expectations forward), while the integration law (L2) combines anticipatory signals with ongoing sensory input.

### Demand Estimate

| Source Unit | Models | Est. Tuples |
|-------------|:------:|:-----------:|
| ARU (PUPF, NEMAC) | 2 | ~40 |
| RPU (MCCN, SSPS) | 2 | ~40 |
| PCU (PWUP, WMED) | 2 | ~40 |
| **Total (deduplicated)** | **6** | **~120** |

C0P has the most uniform cross-unit distribution — exactly 2 models per unit, with balanced tuple contribution.

## Models Using This Mechanism

### ARU (Affective Resonance Unit)
- **SRP** — Striatal Reward Pathway
- **VMM** — Ventral-Medial Mapping

### RPU (Regulatory Processing Unit)
- **MORMR** — Model of Reward Modulation and Regulation
- **IUCP** — Interoceptive Uncertainty and Cognitive Processing

### PCU (Predictive Coding Unit)
- **ICEM** — Interoceptive-Cognitive Emotion Model
- **UDP** — Uncertainty-Driven Prediction

## Neuroscientific Basis

- Salimpoor et al. (2011): Temporal dissociation between caudate (anticipation) and NAcc (peak pleasure) during music listening.
- Berridge (2003): Wanting vs. liking distinction in reward processing; C0P focuses on the "wanting" (anticipatory) component.
- Pearce & Wiggins (2012): IDyOM model of melodic expectation based on statistical learning.
- Huron (2006): ITPRA theory — Imagination, Tension, Prediction, Reaction, Appraisal as stages of anticipatory reward.

## Code Reference

`mi_beta/brain/mechanisms/c0p.py`
