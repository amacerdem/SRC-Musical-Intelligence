# CTBB — Temporal Integration

**Model**: Cerebellar Theta-Burst Balance
**Unit**: MPU
**Function**: F7 Motor & Timing
**Tier**: γ
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | timing_enhancement | iTBS timing improvement magnitude. Tracks the cumulative cerebellar timing enhancement effect by propagating f25 across time. Reflects the LTP-like facilitation lasting ~20-30 min post-iTBS (Huang 2005). TAU_DECAY = 1800s governs the temporal envelope. |
| 4 | sway_reduction | Postural sway reduction estimate. Combines postural control (f27) with inverted balance variability to estimate the net reduction in postural sway. Sansare 2025: greatest sway reduction at 10-20 min post-iTBS, eta-sq = 0.202. sway_reduction = sigma(0.5 * f27 + 0.5 * (1 - balance_var_1s)). |
| 5 | cerebellar_m1_coupling | Cerebellar-M1 pathway strength. Integrates cerebellar timing (f25) and M1 modulation (f26) to estimate the functional coupling between cerebellum and primary motor cortex. cerebellar_m1_coupling = sigma(0.5 * f25 + 0.5 * f26). Sansare 2025 CBI null suggests this pathway is indirect. |

---

## H3 Demands

| # | R3 idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 10 | 3 | M0 (value) | L2 (bidi) | Timing onset 100ms |
| 1 | 10 | 16 | M1 (mean) | L0 (fwd) | Mean timing 1s |
| 2 | 10 | 16 | M2 (std) | L0 (fwd) | Timing variability 1s |

---

## Computation

The M-layer performs temporal integration of the E-layer features to derive time-evolving estimates of cerebellar motor enhancement. It bridges the instantaneous E-layer extractions with the temporal dynamics of the iTBS effect.

1. **timing_enhancement**: Directly propagates f25 (cerebellar timing) as the temporal enhancement signal. The iTBS effect follows an LTP-like time course (Huang 2005), with peak facilitation at ~20-30 min. The TAU_DECAY = 1800s parameter governs the exponential decay envelope, though Sansare 2025 shows the effect is not strictly linear.

2. **sway_reduction**: Combines the postural control assessment (f27) with the raw balance variability signal. This dual integration ensures that sway reduction reflects both the high-level postural control state and the ongoing balance fluctuations. The sigmoid activation keeps the output in [0, 1], where higher values indicate greater sway reduction (better balance).

3. **cerebellar_m1_coupling**: Averages the cerebellar timing and M1 modulation signals to estimate functional coupling strength. This is modeled cautiously given the CBI null result (Sansare 2025, eta-sq = 0.045 n.s.), which suggests the behavioral improvement may not be mediated by the direct cerebellar-M1 inhibitory pathway.

H3 tuples at this layer focus on spectral_flux dynamics (H3 at 100ms for onset detection, H16 at 1s for mean and variability), providing the temporal scaffolding for timing enhancement estimation.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f25 | Cerebellar timing | Primary input for timing_enhancement and coupling |
| E-layer f26 | M1 modulation | Input for cerebellar_m1_coupling estimation |
| E-layer f27 | Postural control | Input for sway_reduction computation |
| R3[10] spectral_flux | Timing dynamics | Temporal onset and variability features |
| H3 (3 tuples) | Spectral flux temporal morphology | Timing onset, mean, and variability at 100ms-1s |
