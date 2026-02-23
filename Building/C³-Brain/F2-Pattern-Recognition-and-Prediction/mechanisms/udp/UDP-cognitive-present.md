# UDP P-Layer — Cognitive Present (3D)

**Layer**: Cognitive Present (P)
**Indices**: [4:7]
**Scope**: internal
**Activation**: sigmoid

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | P0:reward_mode | [0, 1] | Current reward processing mode. High = confirmation-rewarding mode (atonal/uncertain); Low = error-rewarding mode (tonal/certain). Determines which PE-reward pathway is dominant. Mencke 2019: reward valence inverts under high uncertainty. |
| 5 | P1:uncertainty_tracking | [0, 1] | Real-time uncertainty state. Current context uncertainty level from E0. Drives precision estimation and reward pathway selection. Cheung 2019: hippocampus and NAcc track uncertainty (beta=0.242 NAcc, beta=0.358 pre-SMA). |
| 6 | P2:reward_signal | [0, 1] | Current reward signal magnitude. The active reward signal from whichever pathway is dominant. Represents the moment-by-moment hedonic signal. Salimpoor 2011: caudate (anticipation r=0.71), NAcc (experience r=0.84). |

---

## Design Rationale

1. **Reward Mode (P0)**: Binary-like mode indicator derived from uncertainty level. When uncertainty exceeds threshold (~0.5), the system switches to confirmation-rewarding mode. This is the core UDP mechanism.

2. **Uncertainty Tracking (P1)**: Real-time uncertainty state from E0. Feeds the reward mode determination and downstream precision estimation.

3. **Reward Signal (P2)**: The active hedonic signal — maximum of confirmation and error reward pathways. This is what the reward circuit (ARU) receives.

---

## H³ Demands

No additional unique H³ demands. Reuses E-layer tuples.

| # | R³ idx | Horizon | Morph | Law | Purpose |
|---|--------|---------|-------|-----|---------|
| — | — | — | — | — | No unique H³ demands; reuses E-layer tuples |

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer | E0:uncertainty_level | Context for mode selection |
| E-layer | E1:confirmation_reward | Confirmation pathway |
| E-layer | E2:error_reward | Error pathway |
| E-layer | E3:pleasure_index | Combined pleasure signal |
