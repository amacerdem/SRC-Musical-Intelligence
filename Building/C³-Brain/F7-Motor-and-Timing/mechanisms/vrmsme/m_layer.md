# VRMSME — Temporal Integration

**Model**: VR Music Stimulation Motor Enhancement
**Unit**: MPU-β3
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: M — Temporal Integration
**Dimensions**: 3D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 3 | vrms_advantage | VRMS superiority over VRAO/VRMI. vrms_advantage = f16. The degree to which VR music stimulation produces stronger sensorimotor connectivity than VR action observation or VR motor imagery. This is the primary clinical outcome measure. Liang et al. 2025: VRMS > VRAO in bilateral PM&SMA (p<.01 FDR); VRMS > VRMI in bilateral M1 (p<.05 HBT). Range [0, 1]. |
| 4 | bilateral_index | Bilateral activation balance. bilateral_index = f17. The symmetry of sensorimotor activation across hemispheres. Higher values indicate stronger bilateral (versus lateralized) activation, which is the hallmark of VRMS compared to VRMI. Liang et al. 2025: homotopic brain connectivity (HBT) in M1 significantly greater for VRMS vs VRMI. Range [0, 1]. |
| 5 | connectivity_strength | Network connectivity magnitude. connectivity_strength = σ(0.5 * f16 + 0.5 * f18). Integrates music enhancement (f16) with network connectivity (f18) to produce an overall connectivity measure. Both the music-specific enhancement and the PM-DLPFC-M1 network must be active for strong connectivity. Liang et al. 2025: 14 ROI pairs with significant heterogeneous FC in VRMS (p<.05 FDR). Range [0, 1]. |

---

## H³ Demands

This layer does not introduce additional H³ demands beyond E-layer tuples. All computation derives from E-layer features f16, f17, f18.

---

## Computation

The M-layer transforms E-layer features into clinically interpretable measures of VR music stimulation effects.

**vrms_advantage** directly inherits from f16 (music_enhancement). The music enhancement feature IS the VRMS advantage — it directly quantifies how much music adds to VR motor stimulation beyond what observation or imagery provides.

**bilateral_index** directly inherits from f17 (bilateral_activation). The bilateral activation feature IS the bilateral index — it captures the homotopic brain connectivity pattern that distinguishes VRMS from other VR conditions.

**connectivity_strength** combines f16 and f18 through sigmoid with equal weights. This produces a joint measure of overall sensorimotor network connectivity: both the music-specific enhancement (f16, reflecting auditory-motor coupling) and the network-level connectivity (f18, reflecting the PM-DLPFC-M1 hub) must be active for high connectivity strength. This reflects the hierarchical nature of VRMS effects: music first enhances coupling, which then strengthens the broader network.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| E-layer f16 | Music enhancement signal | VRMS advantage derives from music-specific motor enhancement |
| E-layer f17 | Bilateral activation signal | Bilateral index derives from homotopic connectivity |
| E-layer f18 | Network connectivity signal | Connectivity strength requires active PM-DLPFC-M1 network |
| Liang et al. 2025 | fNIRS evidence | Provides the VRMS > VRAO/VRMI comparison framework |
