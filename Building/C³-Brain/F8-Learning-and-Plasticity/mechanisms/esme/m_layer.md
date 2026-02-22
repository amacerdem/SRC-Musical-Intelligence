# ESME — Temporal Integration

**Model**: Expertise-Specific MMN Enhancement
**Unit**: SPU
**Function**: F8 Learning & Plasticity
**Tier**: γ
**Layer**: M — Temporal Integration
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 4 | mmn_expertise_function | Unified MMN-expertise function. Models the interaction between deviance magnitude and expertise modulation across all three domains (pitch, rhythm, timbre). Computed as the geometric mean of expertise enhancement (f04) and the maximum domain-specific MMN: mmn_expertise_function = sqrt(f04 * max(f01, f02, f03)). Yu et al. 2015: MMN as comprehensive indicator of perception of regularities — the unified function integrates the domain-specific gradient into a single expertise metric. Doelling & Poeppel 2015: enhanced PLV across all tempi in musicians reflects general expertise mechanism. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|

No additional H³ demands beyond those consumed by the E-layer. The M-layer operates on derived E-layer features.

---

## Computation

The M-layer computes a single unified expertise-MMN function that integrates across all three deviance domains. Unlike SLEE which has three M-layer dimensions tracking different temporal dynamics, ESME's M-layer focuses on a single integrated metric.

1. **mmn_expertise_function**: Takes the geometric mean of the expertise enhancement modulation (f04) and the maximum domain-specific MMN response (max across f01, f02, f03). The geometric mean is used rather than arithmetic mean because it captures the interaction: both expertise and deviance must be present for the function to be high. A musician with no deviant present produces low output; a non-musician encountering a deviant also produces low output.

This single dimension summarizes the overall expertise-dependent enhancement state, which the P-layer then decomposes into domain-specific present-moment detection signals.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f01 | Pitch MMN amplitude | Max-domain input to unified function |
| E-layer f02 | Rhythm MMN amplitude | Max-domain input to unified function |
| E-layer f03 | Timbre MMN amplitude | Max-domain input to unified function |
| E-layer f04 | Expertise enhancement | Modulation factor for unified function |
