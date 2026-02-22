# emotional_coloring — Core Belief (MEAMN)

**Category**: Core (full Bayesian PE)
**τ**: 0.75
**Owner**: MEAMN (IMU-α1)
**Multi-Scale**: 4 horizons, T_char = 2s

---

## Definition

"This makes me feel..." Affective tag strength on retrieved memory. Tracks the intensity of the emotional label applied to a music-evoked autobiographical memory — how strongly the retrieved memory is colored by a specific emotion (joy, sadness, longing, excitement). τ=0.75 reflects that emotional coloring is stable once a memory is retrieved but can shift more readily than the memory itself.

---

## Multi-Scale Horizons

```
H13(600ms)  H16(1s)  H18(2s)  H21(8s)
```

T_char = 2s reflects the characteristic timescale of emotional tagging. H13 captures the initial affective flash at memory retrieval; H16 tracks the primary emotional response; H18 captures the sustained emotional coloring over a phrase; H21 tracks emotional persistence across musical sections.

---

## Observation Formula

```
# Provisional (not yet implemented):
value = 0.40 × emotional_color + 0.30 × f03_emotion + 0.30 × meam_retrieval

# emotional_color = arousal × (1 - roughness) — valence-arousal product
# f03_emotion     = sigma(0.60 × (1-roughness) × loudness × arousal)
# meam_retrieval  = familiarity × emotional_intensity × self_relevance

# Precision: emotional_color × arousal / (M2_valence + ε)
```

The emotional_color (P1) provides the primary signal: the valence-arousal product from the current acoustic frame. The E-layer emotion response (E2) provides the raw affective tagging signal via amygdala engagement. The M-layer MEAM retrieval (M0) modulates: emotional coloring is strongest when the full autobiographical retrieval chain is active.

Relay components: MEAMN.emotional_color[P1] + MEAMN.f03_emotion[E2] + MEAMN.meam_retrieval[M0].

---

## Prediction Formula

```
predict = Linear(τ × prev + w_trend × M18 + w_period × M14 + w_ctx × beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = π_obs / (π_obs + π_pred). With τ=0.75, emotional coloring has the lowest inertia among F4 Core beliefs — it can shift between emotions within a few seconds if the music changes character. Context from beliefs_{t-1} includes autobiographical_retrieval (emotion requires active memory) and nostalgia_intensity (nostalgia biases toward warm/positive emotions).

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| MEAMN P1 | emotional_color [6] | Primary valence-arousal product (40%) |
| MEAMN E2 | f03_emotion [2] | Amygdala affective tagging (30%) |
| MEAMN M0 | meam_retrieval [3] | Full retrieval chain modulation (30%) |
| R³ [0] | roughness | Valence proxy (inverse) |
| R³ [10] | loudness | Arousal correlate |
| H³ | (0, 16, 0, 2) roughness value H16 L2 | Current dissonance |
| H³ | (10, 16, 0, 2) loudness value H16 L2 | Current arousal |

---

## Scientific Foundation

- **Context-dependent study 2021**: Multimodal integration in STS and hippocampus — emotional memories are context-dependent (fMRI, N=84, d=0.17, p<0.0001)
- **Janata 2009**: Emotional evocation strong vs weak autobiographical (t(9)=3.442, p<0.008); mPFC self-referential processing (fMRI 3T, N=13)
- **Sakakibara et al. 2025**: Nostalgia enhances memory vividness (eta_p^2=0.541); emotional intensity amplifies MEAM

## Implementation

File: `Musical_Intelligence/brain/kernel/beliefs/emotional_coloring.py`
