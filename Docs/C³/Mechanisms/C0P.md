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

To be populated in Phase 6. Will declare demands for trend, stability, and velocity morphs on consonance and energy R3 features at H18/H19/H20 to track prediction confidence and goal proximity.

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
