# DAED — Cognitive Present

**Model**: Dopamine Anticipation-Experience Dissociation
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | caudate_activation | Current caudate nucleus activation state. Real-time anticipatory dopamine level reflecting the listener's present anticipatory engagement. High values during musical build-ups, crescendos, and approach to expected peaks. Salimpoor 2011: caudate [11C]raclopride binding decreases (DA release) 15-30s before peak emotion (t = 3.2). |
| 7 | nacc_activation | Current nucleus accumbens activation state. Real-time consummatory dopamine level reflecting the listener's present hedonic experience. High values at moments of peak pleasure, resolution, and chills. Salimpoor 2011: NAcc [11C]raclopride binding decreases at peak moment (t = 2.8, r = 0.84 vs pleasure rating). |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 22 | 8 | M8 (velocity) | L0 (fwd) | Energy velocity at 500ms — dynamic build-up rate |
| 1 | 25 | 8 | M0 (value) | L2 (bidi) | Coupling at 500ms — present cross-domain state |

---

## Computation

The P-layer produces the "present-moment" cognitive state of the mesolimbic dopamine system. These are the exported relay fields that the C³ kernel scheduler reads.

1. **Caudate Activation**: Represents the current level of anticipatory engagement. Combines E-layer anticipatory DA (f01) with wanting index (f03) and real-time energy velocity to capture the dynamic build-up state. High caudate activation signals that the listener is in an approach/anticipation state — the music is building toward something.

2. **NAcc Activation**: Represents the current level of consummatory pleasure. Combines E-layer consummatory DA (f02) with liking index (f04) and present coupling state to capture the hedonic experience. High NAcc activation signals that the listener is experiencing peak pleasure or resolution.

The temporal dissociation between these two signals (caudate leads, NAcc follows) is the fundamental finding of Salimpoor (2011) and the core output of the DAED model.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_anticipatory_da | Primary anticipatory signal for caudate state |
| E-layer | f02_consummatory_da | Primary consummatory signal for NAcc state |
| E-layer | f03_wanting_index | Wanting component for caudate state |
| E-layer | f04_liking_index | Liking component for NAcc state |
| M-layer | temporal_phase | Phase context for activation balance |
| H³ | 2 tuples (see above) | Real-time dynamic context |
| DAED relay (RPU) | wanting_index, liking_index | Kernel export: DAED feeds wanting/liking to SRP (ARU) |
| DAED relay (RPU) | caudate_activation, nacc_activation | Kernel export: feeds reward and salience computations |
