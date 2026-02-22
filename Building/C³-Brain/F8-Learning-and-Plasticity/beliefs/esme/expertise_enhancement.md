# expertise_enhancement -- Core Belief (ESME)

**Category**: Core (full Bayesian PE)
**tau**: 0.92
**Owner**: ESME (SPU-gamma2)
**Multi-Scale**: single-scale (Ultra band), T_char = 120s

---

## Definition

"Training strengthens deviation detection." Tracks how strongly musical training amplifies pre-attentive auditory processing -- the mismatch negativity (MMN) enhancement that comes from years of instrument practice. High values indicate that the listener's brain automatically detects deviations in their trained domain with greater sensitivity than non-musicians. This is a gradient effect: the strongest enhancement occurs for features most relevant to the trained instrument/genre.

---

## Multi-Scale Horizons

```
Single-scale in v1.0 kernel.
T_char = 120s (Ultra band -- MMN enhancement reflects years of training)
```

When multi-scale is activated (implementation wave 3-5), expertise enhancement will span Ultra horizons reflecting the extremely slow accumulation of expertise over training sessions.

---

## Observation Formula

```
# ESME mechanism outputs:
value = 0.50 * f04_expertise_enhancement
      + 0.30 * mmn_expertise_function
      + 0.20 * developmental_trajectory

# f04 = sigma(alpha * max(f01_pitch, f02_rhythm, f03_timbre))
#   alpha = EXPERTISE_ALPHA (trainable, domain-specific)
#   Maximum domain-specific MMN modulated by plasticity markers
#   Tervaniemi 2022 principle: "Parameters most important in
#   performance evoke the largest MMN"

# mmn_expertise_fn = sqrt(f04 * max(f01, f02, f03))
#   Geometric mean of expertise and max domain MMN
#   Unified MMN-expertise function

# developmental_trajectory = sigma(0.6 * f04 + 0.4 * mmn_expertise_fn)
#   Long-term plasticity trajectory

# Precision: mmn_expertise_fn * expertise_alpha / (H3_std + eps)
```

---

## Prediction Formula

```
predict = Linear(tau * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred). The very high tau=0.92 reflects that expertise enhancement barely changes within a listening session -- it accumulates over years of training. Frame-to-frame changes are almost entirely absorbed by the prior.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| ESME E3 | f04_expertise_enhancement [3] | Domain-specific expertise modulation |
| ESME M0 | mmn_expertise_function [4] | Unified expertise-MMN function |
| ESME F2 | developmental_trajectory [10] | Long-term plasticity trajectory |
| ESME E0 | f01_pitch_mmn [0] | Pitch MMN (enhanced in singers) |
| ESME E1 | f02_rhythm_mmn [1] | Rhythm MMN (enhanced in drummers) |
| ESME E2 | f03_timbre_mmn [2] | Timbre MMN (enhanced for trained instrument) |

---

## Scientific Foundation

- **Koelsch, Schroger & Tervaniemi 1999**: Violinists show MMN to 0.75% pitch deviants absent in non-musicians (EEG, N~20/group)
- **Vuust et al. 2012**: Genre-specific MMN differentiation -- jazz > rock > pop > non-musicians (EEG, N~40-60)
- **Tervaniemi 2022**: Review -- "Sound parameters most important in performance evoke largest MMN"
- **Criscuolo et al. 2022**: ALE meta-analysis (k=84, N=3005) -- musicians > non-musicians in bilateral STG + L IFG (BA44)
- **Martins et al. 2022**: CONSTRAINT -- no singer vs instrumentalist P2/P3 difference (N=58); clean 3-way dissociation is an oversimplification

## Implementation

File: `Musical_Intelligence/brain/functions/f8/beliefs/expertise_enhancement.py` (Phase 5)
