# IGFE P-Layer — Cognitive Present (3D)

**Layer**: Present Processing (P)
**Indices**: [4:7]
**Scope**: exported (kernel relay)
**Activation**: sigmoid
**Model**: PCU-γ1 (Individual Gamma Frequency Enhancement, 9D, γ-tier 50-70%)
**Note**: IGFE has NO M-layer. P-layer follows E-layer directly (indices 4-6).

---

## Output Dimensions

| Idx | Name | Range | Scientific Basis |
|-----|------|-------|-----------------|
| 4 | P0:gamma_synchronization | [0, 1] | Gamma entrainment strength. ASSR-based synchronization to stimulus gamma content. Combines coupling and modulation tuples for real-time gamma phase-locking signal. Dobri 2023: gamma synchronization correlates with GABA concentration. |
| 5 | P1:dose_accumulation | [0, 1] | = f04 (dose_response). Memory-encoding integration over time. Carries forward the E-layer dose signal as a present-moment state. Bolland 2025: enhancement accumulates with exposure duration. |
| 6 | P2:memory_access | [0, 1] | Memory-encoding recall enhancement signal. The real-time "how available is the enhanced memory trace" signal. Reflects hippocampal-cortical gamma coupling during retrieval. Yokota 2025: post-stimulation memory access. |

---

## Design Rationale

1. **Gamma Synchronization (P0)**: The present-moment gamma entrainment state. Uses a dedicated set of H3 coupling and modulation tuples to track real-time gamma phase-locking. This goes beyond E0 (IGF match, which is about alignment) to capture how strongly the brain is actually synchronized. ASSR-based — auditory steady-state response is the gold standard for gamma entrainment measurement.

2. **Dose Accumulation (P1)**: Carries forward the E-layer dose response (E3:f04) as a present-moment state variable. Enhancement does not reset between frames — it accumulates. This state is critical for the F-layer predictions, which depend on how much dose has been delivered.

3. **Memory Access (P2)**: The present-moment signal for enhanced memory retrieval. During and after gamma stimulation, memory traces are more accessible. This captures the hippocampal-cortical gamma coupling that facilitates recall. Distinct from E1 (which tracks encoding) — P2 tracks retrieval accessibility.

---

## Kernel Relay Export

P-layer outputs are the primary relay exports:

| Export Field | P-Layer Idx | Kernel Usage |
|-------------|-------------|-------------|
| `gamma_synchronization` | P0 [4] | Salience context: gamma-based attentional amplification |
| `dose_accumulation` | P1 [5] | Precision engine: dose-dependent confidence adjustment |
| `memory_access` | P2 [6] | F4 Memory: retrieval enhancement modulation |

---

## H3 Dependencies (P-Layer)

| Tuple | Feature | Purpose |
|-------|---------|---------|
| (25, 0, 0, 2) | x_l0l5[0] value H0 L2 | Coupling instantaneous at 25ms — gamma sync |
| (25, 1, 0, 2) | x_l0l5[0] value H1 L2 | Coupling at 50ms — gamma sync |
| (25, 3, 14, 2) | x_l0l5[0] periodicity H3 L2 | Coupling periodicity 100ms — sync regularity |
| (25, 16, 14, 2) | x_l0l5[0] periodicity H16 L2 | Coupling periodicity 1s — sustained sync |
| (10, 0, 0, 2) | spectral_flux value H0 L2 | Modulation onset 25ms — gamma modulation |
| (10, 1, 14, 2) | spectral_flux periodicity H1 L2 | Modulation periodicity 50ms — gamma modulation |
| (10, 3, 1, 2) | spectral_flux mean H3 L2 | Modulation mean 100ms — sustained gamma |

---

## Scientific Foundation

- **Dobri et al. 2023**: R²=0.31 GABA-gamma relationship — gamma synchronization has neurochemical basis (N=42)
- **Yokota et al. 2025**: Post-stimulation memory access improved with IGF-matched gamma (N=29)
- **Leeuwis et al. 2021**: R²adj=0.40 gamma-cognition relationship — synchronization predicts benefit
- **Bolland et al. 2025**: Dose-dependent gamma effects confirmed across k=62 studies

## Implementation

File: `Musical_Intelligence/brain/functions/f3/mechanisms/igfe/cognitive_present.py` (pending)
