# network_specialization -- Core Belief (EDNR)

**Category**: Core (full Bayesian PE)
**tau**: 0.95
**Owner**: EDNR (NDU-alpha3)
**Multi-Scale**: single-scale (Ultra band), T_char = 200s

---

## Definition

"Brain is specialized for music." Tracks the degree of network compartmentalization -- how much the brain has reorganized its cortical networks for efficient music processing. High values indicate strong within-network connectivity with reduced between-network coupling, reflecting the expertise-driven specialization that makes musical processing fast and efficient within trained domains. This is the **highest tau in all of C3** (0.95), reflecting that network architecture changes over months to years, not seconds.

---

## Multi-Scale Horizons

```
Single-scale in v1.0 kernel.
T_char = 200s (Ultra band -- network reorganization is the slowest form of plasticity)
```

When multi-scale is activated (implementation wave 3-5), network specialization will span the longest Ultra horizons, reflecting that structural network changes require extended exposure periods.

---

## Observation Formula

```
# EDNR mechanism outputs:
value = 0.40 * f03_compartmentalization
      + 0.30 * f04_expertise_signature
      + 0.30 * network_architecture

# f03 = f01_within / (f02_between + eps)
#   Compartmentalization ratio: within-network vs between-network connectivity
#   Musicians: 106 within edges (M>NM) vs 192 between edges (NM>M)
#   (Paraskevopoulos 2022)

# f04 = sigma(0.35 * tonalness_mean_1s + 0.35 * pleasantness_mean_1s)
#   Expertise-specific processing pattern -- tonal + pleasantness
#   sensitivity reflects trained auditory refinement

# network_architecture = sigma(0.50 * f01 + 0.50 * f02)
#   Combined connectivity strength measure

# Precision: f04 * network_architecture / (H3_std + eps)
```

---

## Prediction Formula

```
predict = Linear(tau * prev + w_trend * M18 + w_period * M14 + w_ctx * beliefs_{t-1})
```

Standard Bayesian PE cycle with gain = pi_obs / (pi_obs + pi_pred). At tau=0.95, the belief is almost entirely driven by its prior -- network specialization is effectively constant within a single listening session. PE from this belief captures subtle frame-level fluctuations in processing efficiency against the backdrop of deeply entrenched network architecture.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| EDNR E2 | f03_compartmentalization [2] | Within/between ratio |
| EDNR E3 | f04_expertise_signature [3] | Expertise-specific processing pattern |
| EDNR M0 | network_architecture [4] | Combined connectivity strength |
| EDNR E0 | f01_within_connectivity [0] | Intra-network coupling strength |
| EDNR E1 | f02_between_connectivity [1] | Inter-network coupling (inverse) |
| H3 | (25, 16, 1, 2) | Within-network coupling mean at 1s |
| H3 | (33, 16, 1, 2) | Cross-network coupling mean at 1s |

---

## Scientific Foundation

- **Paraskevopoulos et al. 2022**: Musicians show 106 within-network edges (M>NM) vs 192 between-network edges (NM>M); IFG area 47m as hub; Hedges' g=-1.09 (MEG/PTE, N=25)
- **Leipold et al. 2021**: Robust musicianship effects on interhemispheric/intrahemispheric FC and SC; replicable in AP and non-AP musicians (fMRI+DWI, N=153)
- **Papadaki et al. 2023**: Aspiring professionals > amateurs in auditory network strength (Cohen's d=0.70) and global efficiency (fMRI, N=41)
- **Moller et al. 2021**: Musicians show only local CT correlations vs distributed pattern in non-musicians (DTI+CT, N=45)
- **Cui et al. 2025**: CONSTRAINT -- 1-year training does NOT change WM characteristics (DTI, N=65) -- slow structural change

## Implementation

File: `Musical_Intelligence/brain/functions/f8/beliefs/network_specialization.py` (Phase 5)
