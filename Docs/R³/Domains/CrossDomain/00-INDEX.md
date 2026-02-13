# CrossDomain Domain -- Group E (24D)

**Domain**: Inter-group interactions
**Groups**: E:Interactions [25:49] 24D
**Total Dimensions**: 24D
**Code Directory**: `mi_beta/ear/r3/domains/cross_domain/`

---

## Domain Description

The CrossDomain domain captures how features from different spectral groups
modulate each other. Rather than analyzing spectral properties independently,
Group E computes pairwise interaction terms between groups A-D. These
interactions encode questions like "how does consonance change with energy?"
and "does timbral sharpness amplify dissonance?"

The current implementation uses 24 element-wise products organized into
three 8-dimensional blocks:
- **Energy x Consonance** [25:32]: How energy dynamics modulate consonance perception
- **Change x Consonance** [33:40]: How spectral change interacts with harmonic quality
- **Consonance x Timbre** [41:48]: How consonance relates to timbral shape

## Computation Characteristics

| Property | Group E |
|----------|---------|
| Stage | 2 (depends on A, B, C, D outputs) |
| Input | mel (B, 128, T) -- currently uses independent proxies |
| Dependencies | A, B, C, D outputs (Phase 6: real references) |
| Cost | ~0.1 ms/frame |
| Warm-up | None |
| Status | EXISTING (proxy-based, Phase 6 revision planned) |

## Current Architecture Issues

Group E is the most problematic existing group. Three fundamental issues:

1. **Proxy Mismatch**: E computes its own independent proxies for A-D features
   instead of referencing actual A-D outputs. Two specific mismatches:
   - `roughness_proxy = var(high_bins)` vs real A[0] = `sigmoid(var/mean - 0.5)`
   - `helmholtz_proxy = max/sum` (=tonalness C[14]) vs real A[2] = lag-1 autocorrelation

2. **Limited Coverage**: Only 3 group pairs (A-B, D-A, A-C) out of 55 possible
   pairs for 11 groups. Groups F-K have no interaction representation.

3. **Zero-Bias Product**: Element-wise product of [0,1] values biases toward
   zero. Low-value features lose signal in the product.

## Group Specification

- [E-Interactions.md](E-Interactions.md) -- 24D cross-group interaction features

## Phase 6 Redesign Roadmap

### Phase 6 Stage 1: Proxy Fix (24D preserved)
Replace independent proxies with real A-D group outputs via dependency injection.
No dimensionality or structural change.

### Phase 6+ Stage 2: Expansion (proposed 24D + 16D = 40D)
Add psychoacoustically motivated F-K cross-group interactions:
- F x A (Pitch x Consonance): 4D
- G x B (Rhythm x Energy): 4D
- H x D (Harmony x Change): 4D
- I x all (Surprise aggregates): 4D

This would expand E from 24D to 40D, exceeding the 128D budget.
Decision deferred to R3 v2.1 (Phase 6+), pending experimental validation.

## Key Literature

- Harrison, P. M. C. & Pearce, M. T. (2020). Simultaneous consonance in music perception and composition. Psychological Review 127(2).
- Witek, M. A. G. et al. (2014). Effects of polyphonic context on syncopation. Music Perception 32(2).
- Lerdahl, F. (2001). Tonal Pitch Space. Oxford UP.
