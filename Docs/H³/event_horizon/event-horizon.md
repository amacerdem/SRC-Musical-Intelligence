# Event Horizon (H) — 32 Temporal Windows

**Dimension**: 32 windows
**Range**: 25ms → 981s (5 orders of magnitude)
**Position**: Axis 0 of H⁰ tensor (H × M × L)
**Scientific Basis**: 120+ peer-reviewed papers

---

## Overview

The Event Horizon defines **WHAT temporal scale** is being analyzed. It spans from gamma oscillations (25ms) to piece-level memory (981s), covering the full range of human temporal experience in music.

```
═══════════════════════════════════════════════════════════════════════════════
                    EVENT HORIZON: TEMPORAL COVERAGE
═══════════════════════════════════════════════════════════════════════════════

    25ms                                                              981s
     │                                                                  │
     ▼                                                                  ▼
     ├────────────────────────────────────────────────────────────────────┤
     │  10⁻²s        10⁻¹s        10⁰s        10¹s        10²s        10³s│
     │                                                                    │
     │  ████████████████████████████████████████████████████████████████ │
     │  Gamma  Alpha  Theta  Beat  Phrase  Section  Structural   Piece   │
     │                                                                    │
     └────────────────────────────────────────────────────────────────────┘

     32 windows covering the full range of music-relevant temporal scales

═══════════════════════════════════════════════════════════════════════════════
```

---

## 9 Temporal Scales

| Scale | Windows | Range | Neural Basis | Primary Function |
|-------|---------|-------|--------------|------------------|
| [Gamma](gamma-scale/gamma-scale.md) | H₀-H₁ | 25-50ms | γ oscillations | Feature binding |
| [Alpha-Beta](alpha-beta-scale/alpha-beta-scale.md) | H₂-H₄ | 75-125ms | α/β oscillations | Attention, motor |
| [Theta](theta-scale/theta-scale.md) | H₅-H₇ | 150-250ms | θ oscillations | Beat tracking |
| [Syllable](syllable-scale/syllable-scale.md) | H₈-H₁₁ | 300-500ms | Stream analysis | Segregation |
| [Beat](beat-scale/beat-scale.md) | H₁₂-H₁₆ | 525-1000ms | Motor-timing | Rhythm, groove |
| [Phrase](phrase-scale/phrase-scale.md) | H₁₇-H₂₀ | 1.25-5s | Association | Phrase structure |
| [Section](section-scale/section-scale.md) | H₂₁-H₂₄ | 7.5-36s | Striatal (DLS) | Verse/chorus |
| [Structural](structural-scale/structural-scale.md) | H₂₅-H₂₈ | 100-414s | Striatal (DMS) | Movement form |
| [Piece](piece-scale/piece-scale.md) | H₂₉-H₃₁ | 500-981s | Striatal (VS) | Complete works |

---

## Window Validation Status

### Literature-Validated (20 windows)

Directly derived from neuroscience literature with specific citations:

```
H₀(25ms)   H₁(50ms)   H₂(75ms)   H₃(100ms)  H₄(125ms)
H₆(200ms)  H₇(250ms)  H₈(300ms)  H₉(350ms)  H₁₁(500ms)
H₁₂(525ms) H₁₃(600ms) H₁₄(730ms) H₁₅(800ms) H₁₆(1000ms)
H₁₇(1250ms) H₂₀(5000ms) H₂₄(36s) H₂₈(414s) H₃₁(981s)
```

### Interpolated (12 windows)

Linear interpolation for smooth coverage:

```
H₅(150ms)  H₁₀(400ms)  H₁₈(2s)    H₁₉(3s)
H₂₁(7.5s)  H₂₂(15s)    H₂₃(25s)   H₂₅(100s)
H₂₆(200s)  H₂₇(300s)   H₂₉(500s)  H₃₀(700s)
```

---

## Window Constants

```python
EVENT_HORIZONS_MS = [
    25, 50, 75, 100, 125,           # H0-H4: Gamma/Alpha-Beta
    150, 200, 250,                   # H5-H7: Theta
    300, 350, 400, 500,              # H8-H11: Syllable
    525, 600, 730, 800, 1000,        # H12-H16: Beat
    1250, 2000, 3000, 5000,          # H17-H20: Phrase
    7500, 15000, 25000, 36000,       # H21-H24: Section
    100000, 200000, 300000, 414000,  # H25-H28: Structural
    500000, 700000, 981000           # H29-H31: Piece
]

WINDOW_SCALES = {
    'gamma': (0, 1),           # H0-H1
    'alpha_beta': (2, 4),      # H2-H4
    'theta': (5, 7),           # H5-H7
    'syllable': (8, 11),       # H8-H11
    'beat': (12, 16),          # H12-H16
    'phrase': (17, 20),        # H17-H20
    'section': (21, 24),       # H21-H24
    'structural': (25, 28),    # H25-H28
    'piece': (29, 31)          # H29-H31
}
```

---

## Downstream Consumers

| Branch | Mechanism | Windows Used |
|--------|-----------|--------------|
| **HC⁰** | OSC | H₀, H₁, H₃, H₄, H₁₆ |
| **HC⁰** | TGC | H₄, H₇ |
| **HC⁰** | TIH | H₁, H₈, H₁₇, H₂₀ |
| **HC⁰** | HRM | H₁₄ |
| **HC⁰** | SGM | H₂₄, H₂₈, H₃₁ |
| **HR⁰** | RTI | H₁₈, H₁₉ |
| **HR⁰** | LTI | H₂₃, H₂₄ |
| **HR⁰** | GTI | H₂₅ |
| **HR⁰** | FTO | H₂₅, H₂₆ |

---

**Implementation**: `Pipeline/D0/h0/event_horizon/`
