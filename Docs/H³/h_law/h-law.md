# H-Law (L) — 3 Causal Attention Modes

**Dimension**: 3 modes
**Position**: Axis 2 of H⁰ tensor (H × M × L)
**Role**: Defines HOW temporal attention flows
**Application**: Applied to each (window, morph) pair

---

## Overview

H-Law defines **HOW attention flows** through the temporal window. The three causal modes determine whether information comes from the past (Forward), future (Backward), or both (Bidirectional).

```
═══════════════════════════════════════════════════════════════════════════════
                    H-LAW: THREE CAUSAL ATTENTION MODES
═══════════════════════════════════════════════════════════════════════════════

    FORWARD (L₀)              BACKWARD (L₁)           BIDIRECTIONAL (L₂)
    Past → Present           Present → Future         Past ↔ Future

       ████░░░░                 ░░░░████               ████████
      ─────────►               ◄─────────              ◄───────►
         t                         t                       t

    "What led to now?"       "What's coming?"        "Full context"

═══════════════════════════════════════════════════════════════════════════════
```

---

## Three Modes

| Index | Name | Direction | Causality | Real-time |
|-------|------|-----------|-----------|-----------|
| [L₀](forward/forward.md) | Forward | Past → Present | Causal | Yes |
| [L₁](backward/backward.md) | Backward | Present → Future | Anti-causal | No (requires lookahead) |
| [L₂](bidirectional/bidirectional.md) | Bidirectional | Past ↔ Future | Acausal | No (requires lookahead) |

---

## Attention Formula

All three modes use exponential decay with mode-specific masks:

```
A(Δt) = exp(-3|Δt|/H) × mask(Δt, mode)

where:
    Δt = t - t_current (time relative to current moment)
    H = window duration (Event Horizon)
    mask = mode-specific binary mask
```

### Mode-Specific Masks

```python
def forward_mask(delta_t):    return 1.0 if delta_t <= 0 else 0.0
def backward_mask(delta_t):   return 1.0 if delta_t >= 0 else 0.0
def bidirectional_mask(delta_t): return 1.0  # No mask
```

---

## Attention Profiles

```
FORWARD (L₀)                BACKWARD (L₁)              BIDIRECTIONAL (L₂)

     ▲ Attention                ▲ Attention               ▲ Attention
     │                          │                         │
     │    ╭─                    │         ─╮              │    ╭───╮
     │   ╱ │                    │         │ ╲             │   ╱     ╲
     │  ╱  │                    │         │  ╲            │  ╱       ╲
     │ ╱   │                    │         │   ╲           │ ╱         ╲
     │╱    │                    │         │    ╲          │╱           ╲
     └─────┼────────►           └─────────┼────►          └─────┼───────►
          Now                            Now                    Now
      Past │ Future               Past │ Future           Past │ Future
```

---

## Usage by Mechanisms

### Mechanisms Preferring Forward (L₀)

| Layer | Mechanism | Rationale |
|-------|-----------|-----------|
| HC⁰ | TIH | Temporal integration is cumulative |
| HC⁰ | PTM | Beat prediction from history |
| HC⁰ | HRM | Hippocampal replay is history-based |
| HC⁰ | SGM | Reward gradient tracking |
| HC⁰ | EFC | Efference copy is causal |
| HC⁰ | C0P | C⁰ projection from processed data |
| HR⁰ | RTI | Real-time integration |
| HR⁰ | GTI | Global form is cumulative |
| HR⁰ | FTO | Form is history-dependent |

### Mechanisms Preferring Bidirectional (L₂)

| Layer | Mechanism | Rationale |
|-------|-----------|-----------|
| HC⁰ | OSC | Phase requires full context |
| HC⁰ | TGC | Coupling needs surrounding context |
| HC⁰ | ATT | Attention to entire context |
| HC⁰ | NPL | Phase-locking bilateral |
| HC⁰ | GRV | Groove from surrounding beats |
| HC⁰ | AED | Emotion from full context |
| HC⁰ | ASA | Streaming needs context |
| HC⁰ | CPD | Peak detection uses context |
| HC⁰ | BND | Binding across time |
| HR⁰ | LTI | Long-term needs full context |
| HR⁰ | XTI | Cross-layer both directions |
| HR⁰ | HRT | Harmonic rhythm bilateral |
| HR⁰ | PST | Phrase boundaries need context |
| HR⁰ | TKT | Key stability from context |

---

## Indexing

```python
def h_law_index(mode: str) -> int:
    """Convert mode name to index."""
    return {'forward': 0, 'backward': 1, 'bidirectional': 2}[mode]

# In flat manifold index:
# flat_idx = 256 + (h × 72) + (m × 3) + l
# where l ∈ {0, 1, 2}
```

---

**Implementation**: `Pipeline/D0/h0/h_law/`
