# Information Domain -- Group I (7D)

**Domain**: Information-theoretic analysis
**Groups**: I:InformationSurprise [87:94] 7D
**Total Dimensions**: 7D
**Code Directory**: `mi_beta/ear/r3/domains/information/`

---

## Domain Description

The Information domain quantifies predictability, surprise, and uncertainty
in the spectral signal. These features measure "how surprising is this moment?"
using information-theoretic frameworks including Shannon entropy, KL divergence,
mutual information, and conditional entropy.

Group I is the only group in Stage 3 of the computation pipeline. It depends
on outputs from three upstream groups:
- Group F (Tonal): chroma vectors for melodic and harmonic entropy
- Group G (Temporal): onset events for rhythmic information content
- Group H (Tonal): key correlations for tonal ambiguity

All features in this group use running statistics with exponential moving
averages (EMA) and a warm-up confidence ramp to handle the initial 2-second
transient period.

## Computation Characteristics

| Property | Group I |
|----------|---------|
| Stage | 3 (after F, G, H) |
| Input | mel (B, 128, T) + F chroma + G onset + H key correlations |
| Dependencies | F[49:61], B[11] (via G), H[75] (shared key correlations) |
| Cost | ~2.0 ms/frame |
| Warm-up | 344 frames (2.0s) -- linear confidence ramp |
| Status | NEW (Phase 3) |

## Running Statistics Framework

All Group I features share a common EMA-based running statistics mechanism:

```
tau = 2.0 seconds (running window time constant)
frame_rate = 172.27 Hz
alpha = 1 - exp(-1 / (tau * frame_rate)) = ~0.0029 (decay factor)

EMA update:    running_avg_t = (1 - alpha) * running_avg_{t-1} + alpha * current_t
Warm-up:       confidence_t = min(1.0, t / 344)  (0 -> 1 ramp over 2s)
Final output:  feature_t = raw_value_t * confidence_t
```

This ensures features are zero during the initial warm-up period and
gradually reach full confidence as sufficient context accumulates.

## Group Specification

- [I-InformationSurprise.md](I-InformationSurprise.md) -- 7D information and surprise features

## Key Literature

- Shannon, C. E. (1948). A mathematical theory of communication. Bell System Technical Journal.
- Pearce, M. T. (2005). The construction and evaluation of statistical models of melodic structure in music perception and composition. PhD thesis, City University London.
- Friston, K. (2010). The free-energy principle: a unified brain theory? Nature Reviews Neuroscience 11(2).
- Gold, B. P. et al. (2019). Musical reward prediction errors engage the nucleus accumbens and motivate learning. PNAS 116(8).
- Spiech, C. et al. (2022). Rhythmic information content and neural synchronization. Cognition 226.
- Dubnov, S. (2006). Spectral anticipation. Computer Music Journal 30(2).
- Cheung, V. K. M. et al. (2019). Uncertainty and surprise jointly predict musical pleasure and amygdala, hippocampus, and auditory cortex activity. Current Biology 29(23).
