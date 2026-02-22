# compartmentalization_cost -- Appraisal Belief (ECT)

**Category**: Appraisal (observe-only)
**Owner**: ECT (NDU-gamma3)

---

## Definition

"Cross-domain integration harder (flexibility cost)." Observes the cost side of expertise compartmentalization -- the reduction in cross-network connectivity that accompanies increased within-network specialization. High compartmentalization cost means the brain has traded flexibility for efficiency: information flows fast within trained networks but struggles to cross network boundaries. This is the structural basis of potential transfer limitations in musical expertise.

---

## Observation Formula

```
# From ECT E-layer + P-layer:
compartmentalization_cost = 0.60 * f02_between_reduction + 0.40 * network_isolation

# f02 = sigma(0.35 * cross_network_mean_1s
#            + 0.35 * cross_entropy_1s)
#   cross_network_mean_1s = H3[(41, 16, 1, 2)]  -- x_l5l6[0] mean over 1s
#   cross_entropy_1s = H3[(41, 16, 20, 2)]  -- x_l5l6[0] entropy over 1s
#   Inter-network connectivity level -- lower in musicians
#   Paraskevopoulos 2022: 192 between-network edges in NM > 106 in M

# network_isolation = current cross-network reduction state
#   Boundary maintenance: how isolated the specialized networks are
```

No prediction -- observe-only appraisal. The value is consumed as evidence for the trade-off analysis and feeds flexibility assessment.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| ECT E1 | f02_between_reduction [1] | Cross-network connectivity loss |
| ECT P1 | network_isolation [8] | Current cross-network reduction |
| H3 | (41, 16, 1, 2) | Cross-network binding mean over 1s |
| H3 | (41, 16, 20, 2) | Cross-network binding entropy over 1s |
| H3 | (41, 3, 2, 2) | Cross-network binding variability at 100ms |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F9 Social | Network flexibility affects social coordination capacity |
| transfer_limitation (Anticipation) | Cost feeds the transfer prediction |
| SLEE | Behavioral benefit assessed despite compartmentalization cost |

---

## Scientific Foundation

- **Paraskevopoulos et al. 2022**: Non-musicians show 192 between-network edges vs musicians 106 -- compartmentalization directly demonstrated (MEG/PTE, N=25)
- **Moller et al. 2021**: Musicians show ONLY local CT correlations; non-musicians show distributed visual-auditory pattern; NM benefit more from visual cues (BCG: t(42.3)=3.06, p=0.004) (DTI+CT, N=45) -- **direct behavioral evidence of trade-off cost**
- **Wu-Chung et al. 2025**: Music creativity benefits depend on baseline network FLEXIBILITY; higher flexibility leads to more cognitive benefit (fMRI, N=52) -- flexibility as precondition for transfer
- **SPECULATIVE**: Full functional consequences of compartmentalization remain partially tested. Structural observation confirmed; behavioral cost demonstrated by Moller BCG finding; broad functional testing still needed.

## Implementation

File: `Musical_Intelligence/brain/functions/f8/mechanisms/ect/ect.py` (Phase 5)
