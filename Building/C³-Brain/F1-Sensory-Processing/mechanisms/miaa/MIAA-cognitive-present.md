# MIAA P-Layer — Cognitive Present (3D)

**Layer**: Present (P)
**Indices**: [5:8]
**Scope**: hybrid
**Activation**: weighted sum (P0) / sigmoid (P1, P2)

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|------------------|
| 5 | P0:melody_retrieval | [0, 1] | Template retrieval strength. 0.35×M0 + 0.25×E1 + 0.20×(1−inharm) + 0.20×clarity_mean. Halpern 2004: perception-imagery overlap. |
| 6 | P1:continuation_prediction | [0, 1] | Next-note prediction from template. σ(0.50×tonalness_mean + 0.50×trist_balance). Di Liberto 2021: imagery pitch ≈ perception. |
| 7 | P2:phrase_structure | [0, 1] | Phrase boundary awareness during imagery. σ(spectral_flux_entropy). High entropy = structural transition. |

---

## Design Rationale

1. **Melody Retrieval (P0)**: Aggregates composite activation (M0), familiarity (E1), harmonic instrument identity (1−inharmonicity), and signal clarity over 300ms. Represents how strongly the auditory cortex is retrieving a stored melodic template.

2. **Continuation Prediction (P1)**: Uses sustained tonal quality (tonalness_mean at 46ms) and spectral balance (tristimulus_balance from R³) to predict whether the current note will continue a familiar pattern. Sigmoid activation.

3. **Phrase Structure (P2)**: Direct sigmoid of spectral flux entropy at 300ms. High entropy = unpredictable spectral evolution = likely approaching a phrase boundary during imagery.

---

## H³ Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (5, 5, 0, 2) | inharmonicity value H5 L2 | Harmonic instrument identity |
| (15, 8, 1, 0) | clarity mean H8 L0 | Signal clarity context |
| (14, 5, 1, 0) | tonalness mean H5 L0 | Tonal quality (reused from E) |
| (21, 8, 13, 0) | spectral_flux entropy H8 L0 | Structural transition proxy |

---

## Relay Consumption

```
MIAA Relay Wrapper (kernel)
├── melody_retrieval (P0, idx 5) → MEAMN (memory binding)
├── continuation_prediction (P1, idx 6) → internal context
└── phrase_structure (P2, idx 7) → MPG phrase context
```

---

## Scientific Foundation

- **Halpern 2004**: Timbre perception-imagery overlap in posterior PT (r=0.84)
- **Di Liberto 2021**: Imagery pitch encoding comparable to perception (p=0.19 n.s.)
- **Bellier 2023**: Music reconstructed from STG — 68% of significant electrodes

## Implementation

File: `Musical_Intelligence/brain/functions/f1/mechanisms/miaa/cognitive_present.py`
