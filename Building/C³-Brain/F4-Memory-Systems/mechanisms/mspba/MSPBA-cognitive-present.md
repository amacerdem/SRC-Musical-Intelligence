# MSPBA P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [5:8]
**Scope**: exported (kernel relay)
**Activation**: sigmoid / mean

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 5 | P0:harmonic_context | [0, 1] | Current harmonic context depth. harmony.mean() -- accumulated tonal context from the Brain pathway. Deeper context produces stronger expectations and larger mERAN on violation. Maess et al. 2001: position effect (2:1 ratio). |
| 6 | P1:violation_state | [0, 1] | Current violation detection state. pred_error.mean() -- IFG activity reflecting real-time syntactic violation processing. Kim et al. 2021: IFG connectivity enhanced for syntactic irregularity (F=6.53, p=0.024). |
| 7 | P2:domain_general_load | [0, 1] | Domain-general syntactic processing load. struct_expect.mean() x entropy. SSIRH: shared processing load between music and language syntax in Broca's area. Patel 2003: concurrent music + language syntax compete for shared resources. |

---

## Design Rationale

1. **Harmonic Context (P0)**: The summary "present-moment" signal for how much harmonic context has been accumulated. This drives the position effect: later chords in a progression have deeper context, producing stronger expectations. The kernel reads this as the harmonic prediction confidence level.

2. **Violation State (P1)**: Indicates whether the current frame contains an active syntactic violation being processed by IFG. High violation state means Broca's area is actively processing a harmonic syntax error (like a Neapolitan substitution). This is the primary relay output for prediction error.

3. **Domain-General Load (P2)**: Measures the total syntactic processing load in Broca's area, combining structural expectation with entropy. Per the SSIRH (Patel 2003), this load is shared between musical and linguistic syntax. High load means fewer resources available for concurrent language processing.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports for MSPBA:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `harmonic_context` | P0 [5] | Harmonic stability belief: context depth |
| `violation_state` | P1 [6] | Prediction error: syntactic component |
| `domain_general_load` | P2 [7] | Salience mixer: syntactic surprise |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (3, 14, 1, 2) | stumpf_fusion mean H14 L2 | Fusion stability over chord progression |
| (22, 10, 0, 2) | entropy value H10 L2 | Current harmonic unpredictability |
| (0, 10, 0, 2) | roughness value H10 L2 | Current dissonance for violation detection |

P-layer primarily aggregates E+M outputs with real-time H3 features.

---

## Brain Regions

| Region | MNI / Talairach | P-Layer Role |
|--------|-----------------|--------------|
| L-IFG (BA 44) | MNI -44, 14, 28; Tal -40.8, 18.5, 15.6 | P1+P2: Broca's area syntactic processing |
| R-IFG (BA 44 homol.) | MNI 44, 14, 28; Tal 37.6, 21.2, 15.1 | P1: mERAN primary generator |
| L-IFG (BA 45) | Approx. -44, 30, 10 | P2: domain-general semantic integration |
| STG | Tal L: -45.1, -8.9, 1.9; R: 43.1, -2.6, 2.0 | P0: prediction error integration |

---

## Scientific Foundation

- **Kim et al. 2021**: IFG connectivity enhanced for syntactic irregularity; STG for ambiguity (MEG, N=19, F=6.53 p=0.024)
- **Patel 2003**: SSIRH -- shared syntactic resources between music and language (review)
- **Maess et al. 2001**: mERAN source 2.5 cm anterior, 1.0 cm superior to P2m -- syntactic vs sensory dissociation (MEG, N=28)
- **Yang et al. 2022**: Musicians detect more clause boundaries -- music syntax training transfers to language (behavioral)

## Implementation

File: `Musical_Intelligence/brain/functions/f4/mechanisms/mspba/cognitive_present.py`
