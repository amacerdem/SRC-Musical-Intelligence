# Temporal Domain -- Groups B + G (15D)

**Domain**: Energy & rhythm analysis
**Groups**: B:Energy [7:12] 5D, G:RhythmGroove [65:75] 10D
**Total Dimensions**: 15D
**Code Directory**: `mi_beta/ear/r3/domains/temporal/`

---

## Domain Description

The Temporal domain tracks when acoustic events occur and how they relate
across time. Group B provides fundamental energy dynamics: amplitude, velocity
(energy change rate), acceleration (energy buildup curvature), loudness
(Stevens' law approximation), and onset strength (spectral flux). Group G
uses onset autocorrelation to extract rhythmic structure: tempo, beat strength,
pulse clarity, syncopation, metricality, isochrony, groove, event density,
tempo stability, and rhythmic regularity.

Together, this domain answers "when do events happen, how loud are they,
and what rhythmic patterns do they form?"

## Computation Characteristics

Group B is Stage 1 (mel-only). Group G is Stage 2 (depends on B's onset_strength).

| Property | Group B | Group G |
|----------|---------|---------|
| Stage | 1 (parallel) | 2 (after B) |
| Input | mel (B, 128, T) | B[11] onset_strength (B, T) |
| Dependencies | None | B[11] onset_strength |
| Cost | <0.1 ms/frame | ~2.0 ms/frame |
| Warm-up | None | 344 frames (~2s) for tempo; 688 frames (~4s) for syncopation |
| Status | EXISTING | NEW (Phase 3) |

## Dependency Chain

```
mel (B, 128, T)
  |
  v
Group B: Energy [7:12]
  |-- amplitude [7]
  |-- velocity_A [8]
  |-- acceleration_A [9]
  |-- loudness [10]
  |-- onset_strength [11]  <-- key output for G
  |
  v  (B[11] passed to Stage 2)
Group G: RhythmGroove [65:75]
  |-- tempo_estimate [65]
  |-- beat_strength [66]
  |-- pulse_clarity [67]
  |-- syncopation_index [68]
  |-- metricality_index [69]
  |-- isochrony_nPVI [70]
  |-- groove_index [71]
  |-- event_density [72]
  |-- tempo_stability [73]
  |-- rhythmic_regularity [74]
```

Group I (Information domain) depends on G's onset events for
rhythmic_information_content [89].

## Group Specifications

- [B-Energy.md](B-Energy.md) -- 5D energy dynamics features
- [G-RhythmGroove.md](G-RhythmGroove.md) -- 10D rhythm and groove features

## Domain-Level Phase 6 Notes

- Group B has a critical Stevens' law double-compression bug in loudness [10]:
  Stevens' exponent (0.3) is applied to log-mel amplitude instead of linear power.
- Group G is entirely new and does not require Phase 6 revision.
- The onset_strength [11] feature in Group B is well-validated (Weineck 2022)
  and serves as the primary input for Group G's rhythm analysis.

## Key Literature

- Stevens, S. S. (1957). On the psychophysical law. Psychological Review 64(3).
- Fraisse, P. (1982). Rhythm and tempo. In The Psychology of Music (Deutsch, ed.).
- Witek, M. A. G. et al. (2014). Effects of polyphonic context, instrumentation, and metrical structure on syncopation in music. Music Perception 32(2).
- Madison, G. (2006). Experiencing groove induced by music. Music Perception 24(2).
- Janata, P. et al. (2012). Sensorimotor coupling in music and the psychology of the groove. J. Exp. Psych: General 141(1).
- Ravignani, A. et al. (2021). The evolution of rhythmic cognition. Trends in Cognitive Sciences.
- Weineck, K. et al. (2022). Neural correlates of spectral flux in music perception. NeuroImage.
