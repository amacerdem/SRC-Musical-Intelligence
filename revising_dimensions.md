# Revising Dimensions — User-Facing Bipolar Axes

> Usability tests showed that 6D/12D parameters (Valence, Complexity, Tension, etc.) are too abstract for everyday users. This document proposes a **two-radar system** with intuitive bipolar labels that require zero explanation.

## Design Principles

- Every label must be a word a non-musician would naturally use to describe a song
- Bipolar format: user sees both ends of the axis, instantly understands where they land
- Two radars separate **what you hear** (acoustic/musical) from **how it feels** (emotional/experiential)
- These 5+5 dimensions are the primary interface for 90%+ of users

---

## Radar 1: "What You Hear" (Musical Character — 5D)


| #   | Low (0) | Axis        | High (1) | Source                                |
| --- | ------- | ----------- | -------- | ------------------------------------- |
| 1   | Slow    | **Speed**   | Fast     | signal.tempo (normalized)             |
| 2   | Quiet   | **Volume**  | Loud     | signal.energy + B35 (loudness)        |
| 3   | Light   | **Weight**  | Heavy    | spectral density + B16, B35, B36      |
| 4   | Smooth  | **Texture** | Rough    | roughness + spectral_flux + B21       |
| 5   | Thin    | **Depth**   | Deep     | bass energy + layering (B101, mfcc_1) |


### Why these 5?

- **Speed** (Slow ↔ Fast): Strongest discriminator across 131 classical pieces (std=11.1 BPM). Universal.
- **Volume** (Quiet ↔ Loud): The first thing anyone notices about music. Everyone says it.
- **Weight** (Light ↔ Heavy): "Heavy metal", "light jazz" — everyday language, zero ambiguity.
- **Texture** (Smooth ↔ Rough): "Smooth jazz", "rough vocals" — natural language people already use.
- **Depth** (Thin ↔ Deep): "Deep bass", "thin sound" — everyone understands.

### Volume vs Hardness (R2) — why both?

These measure different things. A loud orchestral lullaby is **loud but soft**. Aggressive whisper-rap is **quiet but hard**. R1 Volume = physical sound level. R2 Hardness = emotional edge.

Every label passes the **"would my mom say this about a song?"** test.

---

## Radar 2: "How It Feels" (Emotional Feel — 5D)


| #   | Low (0)    | Axis               | High (1)    | Source                                            |
| --- | ---------- | ------------------ | ----------- | ------------------------------------------------- |
| 1   | Sad        | **Mood**           | Happy       | signal.valence + DA + B67, B68                    |
| 2   | Chill      | **Energy**         | Hyped       | NE + B60, B63 (arousal axis)                      |
| 3   | Soft       | **Hardness**       | Hard        | GEMS tenderness, streaming #1 mood (20%)          |
| 4   | Surprising | **Predictability** | Predictable | gene.entropy + B25 (pred_error) + B84 (reward PE) |
| 5   | Dreamy     | **Focus**          | Focused     | Apple Music top-5 mood, fastest growing category  |


### Why these 5?

- **Mood** (Sad ↔ Happy): Russell's #1 dimension. Apple, Spotify, GEMS all validate. Universal.
- **Energy** (Chill ↔ Hyped): Russell's #2 dimension. Maps to activity (study, workout, party, sleep).
- **Hardness** (Soft ↔ Hard): #1 streaming engagement mood (20% romantic/tender). Soft rock vs hard rock — a 5-year-old understands.
- **Predictability** (Surprising ↔ Predictable): Objective, computable from audio (entropy, prediction error). "Did that chord change catch me off guard?"
- **Focus** (Dreamy ↔ Focused): Apple Music top-5 mood. Fastest growing category (lofi/ambient). Practical daily use.

---

## Evidence Base

### Academic

- **Russell's Circumplex Model**: Valence + Arousal = the 2 most validated emotional dimensions
- **GEMS-9** (Geneva Emotional Music Scale): 9 music-specific dimensions → 3 super-factors (Vitality, Unease, Sublimity)
- **Thayer's 4 moods**: Happy, Sad, Calm, Energetic

### Industry

- **Apple Music's 5 moods**: Feel Good, Energy, Relax, Feeling Blue, Focus
- **Spotify**: Happy, Sad, Calm, Energetic (Thayer-based)
- **2025 streaming engagement**: Romantic/Tender (20%), Dark (18%), Sad/Blue (17%, +50% YoY)
- **Fastest growing**: Chill/Lofi/Focus categories

### Data Analysis (131 classical pieces, 1,569 segments)

- Strongest discriminators: tempo (std=11.1), energy (std=0.027), timbralBrightness (std=0.024)
- 15 PSI dimensions completely dead (zero variance) — not usable
- psy6.valence nearly constant (std=0.001) — needs recalibration
- Best between/within ratio: acousticness (1.63), tempo (1.56)

---

## Migration from Current System


| Current 6D         | → Radar | → New Axis                       |
| ------------------ | ------- | -------------------------------- |
| Energy             | R1      | Volume                           |
| Valence            | R2      | Mood                             |
| Tempo              | R1      | Speed                            |
| Tension            | R2      | Hardness                         |
| Groove             | —       | (dissolved into Weight, Texture) |
| Complexity/Density | R1      | Depth                            |
| —                  | R1      | Weight (new)                     |
| —                  | R1      | Texture (new)                    |
| —                  | R2      | Energy (new)                     |
| —                  | R2      | Predictability (new)             |
| —                  | R2      | Focus (new)                      |


---

## Open Questions

- 12D sub-dimensions: how do they map under the new 5+5 parents?
- PSI layer: 15 dead dimensions need debugging before emotional radar can work
- Valence recalibration: `computeValence()` formula needs update (std=0.001 is unusable)
- Temporal arcs: show how dimensions evolve over time, not just static values
- A/B test with real users: validate new labels against old ones

