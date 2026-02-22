# VRMSME — Cognitive Present

**Model**: VR Music Stimulation Motor Enhancement
**Unit**: MPU-β3
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | motor_drive | Music-driven motor activation level. The beat-entrainment-driven state of motor cortex engagement elicited by VR music stimulation. Reflects how strongly the music is currently driving motor system activation across bilateral S1/PM/SMA/M1. Li et al. 2025: high-groove music increases hip-ankle coordination 28.7% and muscle synergy complexity (median synergies HG=7 vs LG=6, p=.039). Range [0, 1]. |
| 7 | sensorimotor_sync | Sensorimotor synchronization state. The temporal-context-driven state of multi-modal sensorimotor synchronization during VR music stimulation. Reflects the current quality of binding between auditory, visual (VR), and motor streams. Liang et al. 2025: VRMS produces the strongest sensorimotor integration, with PM-DLPFC-M1 connectivity exceeding VRAO and VRMI conditions. Range [0, 1]. |

---

## H³ Demands

This layer does not introduce additional H³ demands beyond E-layer and M-layer tuples. All computation derives from upstream layer features.

---

## Computation

The P-layer represents the current-moment state of VR-music-driven motor activation.

**motor_drive** captures the instantaneous motor activation level driven by the music in the VR environment. It is derived from the interaction of VRMS advantage (M-layer) with the fast-scale onset and coupling signals. When music enhancement is strong and beat-level signals are active, motor_drive is high. This signal feeds downstream to ARU as a music-driven reward signal, reflecting the inherently motivating quality of groove-driven motor engagement.

**sensorimotor_sync** captures the instantaneous quality of multi-modal binding. It is derived from the interaction of bilateral index (M-layer) with connectivity strength (M-layer) and the fast-scale sensorimotor binding signals. This represents the current synchronization state across the VR music stimulation's three processing streams: auditory (music), visual (VR environment), and motor (movement output). High values indicate that all three streams are well-synchronized.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| M-layer vrms_advantage | Music enhancement | Motor drive depends on VRMS superiority |
| M-layer bilateral_index | Bilateral activation | Sensorimotor sync requires bilateral engagement |
| M-layer connectivity_strength | Network connectivity | Sync quality reflects network-level integration |
| E-layer f16, f17, f18 | Core enhancement signals | Fast-scale inputs for present-state computation |
| Downstream: ARU | Music-driven reward signal | Motor drive generates groove-based reward |
| Downstream: ARU | VR engagement marker | VRMS advantage signals engagement level |
