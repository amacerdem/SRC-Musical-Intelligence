# within_connectivity -- Appraisal Belief (EDNR)

**Category**: Appraisal (observe-only)
**Owner**: EDNR (NDU-alpha3)

---

## Definition

"Efficient processing within trained networks." Observes the current intra-network coupling strength -- how tightly connected the processing nodes are within specialized auditory and motor networks. High within-connectivity means that information flows efficiently through established neural pathways for music processing, enabling faster and more accurate processing within the trained domain.

---

## Observation Formula

```
# From EDNR E-layer + P-layer:
within_connectivity = 0.60 * f01_within_connectivity + 0.40 * current_compartm

# f01 = sigma(0.35 * within_mean_1s
#            + 0.35 * within_std_100ms
#            + 0.30 * within_periodicity_1s)
#   within_mean_1s = H3[(25, 16, 1, 2)]  -- x_l0l5[0] mean coupling over 1s
#   within_std_100ms = H3[(25, 3, 2, 2)]  -- x_l0l5[0] coupling variability 100ms
#   within_periodicity_1s = H3[(25, 16, 14, 2)]  -- coupling periodicity 1s
#   Intra-network binding strength from consonance x timbre coupling

# current_compartm = sigma(0.50 * f03.clamp(0,3)/3.0 + 0.50 * within_mean_1s)
#   Real-time network state reflecting compartmentalization degree
```

No prediction -- observe-only appraisal. The value is consumed by downstream models (F4 Memory) to modulate encoding efficiency.

---

## Source Dimensions

| Source | Dimension | Role |
|--------|-----------|------|
| EDNR E0 | f01_within_connectivity [0] | Intra-network coupling strength |
| EDNR P0 | current_compartm [6] | Real-time network state |
| H3 | (25, 16, 1, 2) | Within-network coupling mean at 1s |
| H3 | (25, 3, 2, 2) | Within-network coupling variability at 100ms |
| H3 | (25, 16, 14, 2) | Within-network coupling periodicity at 1s |

---

## Cross-Function Downstream

| Consumer | Purpose |
|----------|---------|
| F4 Memory | Efficient within-network processing enhances memory encoding |
| network_specialization (Core) | Contributes to compartmentalization ratio via f01/f02 |
| ECT | Basis for trade-off hypothesis -- within-efficiency as gain |

---

## Scientific Foundation

- **Paraskevopoulos et al. 2022**: Musicians show 106 within-network edges exceeding non-musicians; IFG area 47m is primary supramodal hub with highest node degree in 5/6 network states (MEG/PTE, N=25)
- **Papadaki et al. 2023**: Greater auditory network strength and global efficiency in aspiring professionals vs amateurs; network strength correlates with interval recognition (rsfMRI, N=41, Cohen's d=0.70)
- **Leipold et al. 2021**: Robust within-hemisphere functional connectivity effects in musicians independent of absolute pitch (fMRI+DWI, N=153)

## Implementation

File: `Musical_Intelligence/brain/functions/f8/mechanisms/ednr/ednr.py` (Phase 5)
