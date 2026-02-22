# DDSMI — Cognitive Present

**Model**: Dyadic Dance Social Motor Integration
**Unit**: MPU-β2
**Function**: F7 Motor & Timing
**Tier**: β (Bridging)
**Layer**: P — Cognitive Present
**Dimensions**: 2D

---

## Dimensions

| # | Name | Description |
|---|------|-------------|
| 6 | partner_sync | Current partner synchronization level. The beat-entrainment-driven state of interpersonal motor synchronization during dyadic dance. Reflects real-time quality of movement coordination with the partner. Wohltjen et al. 2023: beat entrainment predicts social synchrony (d=1.37); Kohler et al. 2025: self-produced actions in left M1, other-produced in right PMC. Range [0, 1]. |
| 7 | music_entrainment | Current music entrainment level. The beat-entrainment-driven state of auditory-motor synchronization with the musical stimulus. Reflects how strongly the listener's motor system is locked to the musical beat during social interaction. Bigand et al. 2025: music tracking mTRF, self-movement tracking autonomous from social context (all ps>.224). Range [0, 1]. |

---

## H³ Demands

This layer does not introduce additional H³ demands beyond E-layer and M-layer tuples. All computation derives from upstream layer features.

---

## Computation

The P-layer represents the current-moment state of the two primary motor-coupled processes during dyadic dance.

**partner_sync** captures the instantaneous quality of interpersonal motor synchronization. It is derived from the interaction of social mTRF weight (M-layer) with the fast-scale social coupling signals. When social coordination is strong and the partner's movements are being tracked accurately, partner_sync is high. This signal feeds downstream to ARU (social reward) because successful partner synchronization is inherently rewarding.

**music_entrainment** captures the instantaneous state of auditory-motor coupling with the music. It is derived from the interaction of auditory mTRF weight (M-layer) with music coupling signals. Importantly, this operates somewhat independently of partner_sync — Bigand 2025 found that self-movement (motor control for the music) is autonomous from social context. However, resource competition means that when partner_sync demands increase (visual contact), music_entrainment may decrease.

---

## Dependencies

| Source | What | Why |
|--------|------|-----|
| M-layer mTRF_social | Social processing weight | Partner sync depends on social tracking allocation |
| M-layer mTRF_auditory | Auditory processing weight | Music entrainment depends on auditory tracking allocation |
| M-layer mTRF_balance | Resource balance | Determines relative strength of social vs music processing |
| E-layer f13, f14 | Social and music tracking | Raw tracking signals for present-state computation |
| Downstream: ARU | Social reward signal | Partner synchronization generates social reward |
