# MORMR — Cognitive Present

**Model**: mu-Opioid Receptor Music Reward
**Unit**: RPU
**Function**: F6 Reward & Motivation
**Tier**: α
**Layer**: P — Cognitive Present
**Dimensions**: 1D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 5 | current_opioid_state | Real-time mu-opioid receptor activity state. Represents the present-moment opioid-mediated pleasure experience — the listener's current hedonic engagement via the endogenous opioid system. Integrates E-layer opioid release and M-layer opioid tone with temporal smoothing to reflect the slower pharmacokinetics of opioid signaling (tau_decay = 5.0s, slower than dopamine). Putkinen 2025: music-induced [11C]carfentanil binding changes in VS, OFC, amygdala, thalamus, and temporal pole. |

---

## H³ Demands

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| 0 | 22 | 8 | M8 (velocity) | L0 (fwd) | Energy velocity at 500ms — dynamic modulation rate |
| 1 | 33 | 8 | M1 (mean) | L2 (bidi) | Sustained pleasure mean at 500ms — opioid persistence |
| 2 | 33 | 16 | M18 (trend) | L0 (fwd) | Pleasure trend over 1s — hedonic trajectory |

---

## Computation

The P-layer produces the "present-moment" opioid state that is exported to the C³ kernel scheduler. This is the relay field that downstream beliefs and the reward computation read.

**Current Opioid State**: Combines opioid release (f01), opioid tone (M-layer), and sustained pleasure trajectory to produce a temporally smooth representation of the listener's opioid-mediated pleasure. The longer decay constant (tau = 5.0s vs DAED's tau = 3.0s) reflects the slower pharmacokinetics of the mu-opioid system compared to dopamine.

The P-layer output is critical for:
- The reward computation (opioid contribution to overall reward signal)
- Cross-relay interaction with DAED (dopamine + opioid convergence at NAcc)
- Downstream ARU pleasure/arousal signals (opioid drives hedonic tone)

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | f01_opioid_release | Primary opioid signal |
| E-layer | f02_chills_count | Peak pleasure events |
| M-layer | opioid_tone | Integrated opioid system state |
| H³ | 3 tuples (see above) | Temporal smoothing and trajectory context |
| MORMR relay (RPU) | opioid_release, chills_count | Kernel export: feeds reward hedonic component |
