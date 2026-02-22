# MPG P-Layer — Cognitive Present (2D)

**Layer**: Present (P)
**Indices**: [7:9]
**Scope**: hybrid (relay outputs consumed by kernel)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|------------------|
| 7 | P0:onset_state | [0, 1] | Pitch-processing onset-locked activity. 0.35×E0 + 0.25×M1 + 0.20×E3 + 0.20×onset_mean |
| 8 | P1:contour_state | [0, 1] | Pitch-processing contour tracking. 0.35×E1 + 0.25×M2 + 0.20×E2 + 0.20×(1−E3) |

---

## Relay Output Mapping

These dimensions are the primary relay outputs consumed by the C³ kernel:

```
MPG Relay Wrapper (kernel)
├── onset_state    (P0, idx 7) → SNEM, SDD, EDNR, STU
└── contour_state  (P1, idx 8) → CDMR, STU
```

P0 is high when posterior dominance is strong (onset detection), measured by
gradient_ratio (E3) approaching 1.0.

P1 is high when anterior dominance is strong (contour tracking), measured by
inverse gradient (1−E3) approaching 1.0.

---

## Upstream Dependencies

| Source | Indices | Contribution |
|--------|---------|--------------|
| E-Layer | E0, E1, E2, E3 | Primary signals |
| M-Layer | M1, M2 | Temporal dynamics |
| H³ | (11, 3, 1, 2) | Onset strength mean ~100ms |

---

## Scientific Foundation

- **Rupp 2022**: Posterior AC for onset, anterior AC for contour (MEG n=20)
- **Foo 2016**: Anterior STG dissonant-sensitive, posterior non-selective (ECoG n=8)

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/mpg/cognitive_present.py`
