# MI-Lab v2.0 — Neuroacoustic Intelligence Laboratory

> *A deep experiment environment for the Musical Intelligence pipeline*
> *Apple Liquid Glass 2026 · Dark Glassmorphism · Scientific Precision*

---

## Vision

MI-Lab is the **primary observation, analysis, and experimentation interface** for the Musical Intelligence system — a 756-file neuroscientific audio cognition pipeline spanning 97D spectral features (R³), 223K-dimensional temporal morphology (H³), and a 131-belief cognitive brain (C³) mapped to 26 brain regions and 4 neurochemical channels.

The lab must expose **every layer, every belief, every mechanism, every signal** with the depth and precision of a research-grade neuroscience workstation — wrapped in the aesthetic clarity of Apple's 2026 Liquid Glass design language.

---

## Design Language — Apple Liquid Glass 2026

### Philosophy
- **Depth through transparency**: Layered glass surfaces reveal structure beneath
- **Information density without clutter**: Every pixel earns its place
- **Scientific elegance**: Data is beautiful when presented with precision
- **Dark-first**: Deep backgrounds (#07070c → #0a0a0f) with luminous glass overlays

### Core Tokens

```
Backgrounds (4 layers)
  --bg-deep:      #07070c     abyss
  --bg:           #0a0a0f     primary
  --bg-elevated:  #0d0d14     raised surface
  --bg-surface:   #101018     content area

Glass Hierarchy (4 tiers)
  --glass-0:  rgba(255,255,255, 0.02)   flush / dormant
  --glass-1:  rgba(255,255,255, 0.04)   subtle / card
  --glass-2:  rgba(255,255,255, 0.06)   standard / panel
  --glass-3:  rgba(255,255,255, 0.10)   prominent / active

Blur Cascade
  --blur-sm:  12px    cards, tooltips
  --blur-md:  24px    panels, sidebar
  --blur-lg:  40px    elevated modals, overlays

Apple Liquid Glass Signature
  inset 0 1px 0 rgba(255,255,255, 0.06)     subtle top-edge highlight
  backdrop-filter: blur(24px) saturate(1.3)  frosted depth + color richness

Borders
  --border-subtle:   rgba(255,255,255, 0.04)
  --border-default:  rgba(255,255,255, 0.08)
  --border-strong:   rgba(255,255,255, 0.14)

Shadows (layered depth)
  --shadow-sm:  0 2px 8px rgba(0,0,0, 0.3)
  --shadow-md:  0 8px 32px rgba(0,0,0, 0.4)
  --shadow-lg:  0 16px 48px rgba(0,0,0, 0.5)

Typography
  UI:   Inter / -apple-system / SF Pro
  Data: JetBrains Mono / SF Mono (tabular-nums)
  Labels: 10px uppercase, letter-spacing 0.06em, --text-muted

Accent Colors
  Pipeline:  R³=#3b82f6  H³=#8b5cf6  C³=#10b981  Reward=#f59e0b
  Functions: F1=#3b82f6  F2=#8b5cf6  F3=#f97316  F4=#14b8a6
             F5=#ec4899  F6=#f59e0b  F7=#22c55e  F8=#6366f1  F9=#06b6d4
  Beliefs:   Core=#10b981  Appraisal=#3b82f6  Anticipation=#f59e0b
```

### Component Library

| Component | Purpose | Glass Tier | Blur |
|-----------|---------|:----------:|:----:|
| `GlassPanel` | Primary container | glass-2 | 24px |
| `GlassCard` | Interactive card (expandable, hover lift) | glass-1 | 16px |
| `GlassBadge` | Inline type label (Core/Appraisal/Anticipation) | — | — |
| `GlassChip` | Pill tag (mechanism name, group) | glass-1 | — |
| `GlassTabs` | Tab bar with sliding indicator | glass-0 | — |
| `GlassButton` | Action button with inset highlight | glass-2 | — |
| `GlassTooltip` | Hover detail popup | glass-3 | 40px |
| `GlassSelect` | Dropdown selector | glass-2 | 24px |
| `PageShell` | Standard page wrapper (header + scroll) | — | — |
| `SectionDivider` | Labeled horizontal divider | — | — |

### Animation System

```
Page enter:     opacity 0→1, translateY(6px→0), 250ms ease-out
Card expand:    max-height transition, 250ms cubic-bezier(0.4, 0, 0.2, 1)
Sidebar toggle: width 240px↔56px, 200ms ease
Tab slide:      translateX indicator, 150ms
Hover lift:     translateY(-1px), border brighten, shadow deepen
Number morph:   requestAnimationFrame lerp for live cursor values
Loading pulse:  opacity 1→0.6→1, 1.5s ease infinite
Stagger grid:   30ms delay per child (fadeIn 300ms)
```

---

## Architecture

### Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend | React + TypeScript | 19.x + 5.9 |
| Build | Vite | 7.x |
| Styling | Tailwind CSS | 4.x |
| State | Zustand | 5.x |
| 3D/Viz | Three.js (R3F) | 0.183 |
| Charts | Canvas 2D (custom, high-perf) | — |
| Markdown | react-markdown + remark-gfm | 10.x |
| Backend | FastAPI + uvicorn | 0.115 |
| Storage | HDF5 + JSON | — |
| Pipeline | Musical_Intelligence (PyTorch) | — |

### Data Flow

```
                    ┌─────────────────────────────────────────┐
                    │              MI-Lab Frontend             │
                    │                                         │
                    │  Zustand Stores                         │
                    │  ┌──────────┐ ┌──────────┐ ┌────────┐  │
                    │  │audioStore│ │pipelineS.│ │ c3Store│  │
                    │  └──────────┘ └──────────┘ └────────┘  │
                    │         ▲           ▲           ▲       │
                    │         │    Binary Float32     │       │
                    └─────────┼───────────┼───────────┼───────┘
                              │           │           │
                    ┌─────────┼───────────┼───────────┼───────┐
                    │         ▼           ▼           ▼       │
                    │              FastAPI Backend             │
                    │                                         │
                    │  ┌──────┐  ┌──────────┐  ┌──────────┐  │
                    │  │Audio │  │ Pipeline │  │Experiment│  │
                    │  │Router│  │  Runner  │  │  Store   │  │
                    │  └──────┘  └──────────┘  └──────────┘  │
                    └─────────────────┼───────────────────────┘
                                      │
                    ┌─────────────────┼───────────────────────┐
                    │                 ▼                        │
                    │       Musical_Intelligence Pipeline      │
                    │                                         │
                    │  R³ Extractor ─→ H³ Extractor ─→ C³    │
                    │  (97D/frame)    (131 tuples)    Brain   │
                    │                                         │
                    │  Output: beliefs(131) + relays(9) +     │
                    │     RAM(26) + neuro(4) + Ψ³(28) + reward │
                    └─────────────────────────────────────────┘
```

### API Surface (Existing — No Changes Needed)

| Endpoint | Method | Returns | Binary |
|----------|:------:|---------|:------:|
| `/api/audio/list` | GET | AudioFile[] | — |
| `/api/audio/stream/{name}` | GET | WAV stream | — |
| `/api/audio/waveform/{name}` | GET | Float32 envelope | Yes |
| `/api/audio/spectrogram/{name}` | GET | Float32 (128×T) | Yes |
| `/api/pipeline/run` | POST | experiment_id | — |
| `/api/pipeline/status/{id}` | GET | phase, progress, fps | — |
| `/api/pipeline/results/{id}/summary` | GET | metadata JSON | — |
| `/api/pipeline/results/{id}/r3` | GET | Float32 (T×97) | Yes |
| `/api/pipeline/results/{id}/h3` | GET | Int32+Float32 | Yes |
| `/api/pipeline/results/{id}/c3/beliefs` | GET | Float32 (T×131) | Yes |
| `/api/pipeline/results/{id}/c3/relays/{name}` | GET | Float32 (T×D) | Yes |
| `/api/pipeline/results/{id}/c3/ram` | GET | Float32 (T×26) | Yes |
| `/api/pipeline/results/{id}/c3/reward` | GET | Float32 (T,) | Yes |
| `/api/experiments/list` | GET | ExperimentMeta[] | — |
| `/api/experiments/{id}` | DELETE | status | — |
| `/api/docs/tree` | GET | DocNode tree | — |
| `/api/docs/content?path=` | GET | markdown text | — |

### New API Endpoints (Required)

| Endpoint | Method | Returns | Purpose |
|----------|:------:|---------|---------|
| `/api/pipeline/results/{id}/c3/neuro` | GET | Float32 (T×4) | Neurochemical channels |
| `/api/pipeline/results/{id}/c3/salience` | GET | Float32 (T,) | Salience signal |
| `/api/pipeline/results/{id}/c3/psi` | GET | JSON (6 domains) | Ψ³ cognitive state |
| `/api/tests/list` | GET | TestSuite[] | Available test suites |
| `/api/tests/run` | POST | run_id, status | Execute test suite |
| `/api/tests/status/{run_id}` | GET | TestRunStatus | Test progress + results |
| `/api/tests/results/{run_id}` | GET | TestResults | Full test output |
| `/api/benchmarks/list` | GET | BenchmarkSuite[] | Available benchmarks |
| `/api/benchmarks/run` | POST | run_id | Execute benchmark |
| `/api/benchmarks/results/{run_id}` | GET | BenchmarkResults | Benchmark metrics |

---

## Navigation Structure

```
┌──────────────────────────────────────────────────────────────┐
│ MI-Lab v2.0                                        ≡  ▶ Run │
├──────────┬───────────────────────────────────────────────────┤
│          │                                                   │
│ OVERVIEW │                                                   │
│ ○ Home   │              MAIN CONTENT AREA                    │
│          │                                                   │
│ ──────── │          (page-specific content)                  │
│ EAR      │                                                   │
│ ◉ R³     │                                                   │
│ ◎ H³     │                                                   │
│          │                                                   │
│ ──────── │                                                   │
│ BRAIN    │                                                   │
│ ● F1  17 │                                                   │
│ ● F2  15 │                                                   │
│ ● F3  15 │                                                   │
│ ● F4  13 │                                                   │
│ ● F5  14 │                                                   │
│ ● F6  16 │                                                   │
│ ● F7  17 │                                                   │
│ ● F8  14 │                                                   │
│ ● F9  10 │                                                   │
│          │                                                   │
│ ──────── │                                                   │
│ OUTPUT   │                                                   │
│ ◆ Reward │                                                   │
│ ◇ RAM    │                                                   │
│ ◈ Ψ³     │                                                   │
│ ♦ Neuro  │                                                   │
│          │                                                   │
│ ──────── │                                                   │
│ TESTING  │                                                   │
│ ▸ Smoke  │                                                   │
│ ▸ Bench  │                                                   │
│          │                                                   │
│ ──────── │                                                   │
│ TOOLS    │                                                   │
│ ▶ Pipe   │                                                   │
│ ⬡ Atlas  │                                                   │
│ ☰ Docs   │                                                   │
│          │                                                   │
│ ──────── │                                                   │
│ v2.0     │                                                   │
│ K v4.0   │                                                   │
└──────────┴───────────────────────────────────────────────────┘
```

Sidebar: 240px expanded / 56px collapsed (icon-only mode).
Each F-item: colored accent dot + belief count badge `[17]`.

---

## Pages — Detailed Specification

### 1. Overview (Home)

**Route**: `/`

The command center. At a glance: which audio is loaded, which experiment is active, key metrics, and quick access to run pipeline.

```
┌─────────────────────────────────────────────────────┐
│ ░ AUDIO LIBRARY           ░ ACTIVE EXPERIMENT       │
│ ┌──────────────────────┐  ┌──────────────────────┐  │
│ │ bach    │ 4:12 │ wav │  │ 20260224_143022      │  │
│ │ swan    │ 6:38 │ wav │  │ bach · 30.0s · 5168f │  │
│ │ herald  │ 5:01 │ wav │  │ 249 fps · K v4.0     │  │
│ │ beetho  │ 8:14 │ wav │  │ reward: +0.149       │  │
│ │ duel    │ 4:56 │ wav │  │ positive: 100%       │  │
│ │ enigma  │ 6:02 │ wav │  └──────────────────────┘  │
│ │ yang    │ 3:44 │ mp3 │                            │
│ └──────────────────────┘  ░ PIPELINE METRICS        │
│                           ┌───────┬───────┬───────┐ │
│ ░ MINI REWARD TRACE       │R³ 97D │H³ 131│C³ 131 │ │
│ ┌──────────────────────┐  │ 10%   │ 50%  │ 40%   │ │
│ │ ~~∿~~∿~~∿~~∿~~∿∿~~~ │  │ time  │ time │ time  │ │
│ │     reward signal     │  └───────┴───────┴───────┘ │
│ └──────────────────────┘                             │
│                                                      │
│ ░ RECENT EXPERIMENTS                                 │
│ ┌────────────────────────────────────────────────┐   │
│ │ ID           │ Audio │ Duration │ Reward │ FPS  │   │
│ │ 0224_1430    │ bach  │ 30.0s    │ +0.149 │ 249  │   │
│ │ 0224_1122    │ swan  │ 30.0s    │ +0.147 │ 245  │   │
│ │ 0223_0901    │ herald│ 30.0s    │ +0.146 │ 251  │   │
│ └────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────┘
```

### 2. R³ Explorer

**Route**: `/r3`

Full 97D spectral feature inspection across 9 groups.

- **Audio Timeline** (35px compact waveform strip with cursor)
- **9 Group Panels** (expandable glass cards):
  - Group header: name, color dot, dim range, feature count
  - Collapsed: SparkLine overview of group mean
  - Expanded: SignalTrace per feature, per-feature stats table
- **Group Comparison Mode**: overlay group means on single canvas
- **Feature Distribution Panel**: histogram of selected feature across time
- **Statistics Summary**: global mean, std, dynamic range per group

### 3. H³ Explorer

**Route**: `/h3`

Multi-scale temporal morphology viewer.

- **Demand Browser**: filter by r3_idx, horizon band, morph type, law
- **Heatmap View**: 32 horizons × T frames (selectable morph/law)
- **Horizon Comparison**: same feature at different temporal scales
- **Morph Family View**: M0(mean), M2(std), M8(velocity), M14(periodicity), M18(trend) overlaid
- **Law Comparison**: L0 (backward) vs L1 (forward) vs L2 (bidirectional)
- **Demand Coverage Report**: which tuples are active, occupancy %

### 4. Function Pages (F1–F9) — The Core

**Routes**: `/brain/f1` through `/brain/f9`

All 9 pages share a single `FunctionPage` component, parameterized by `functionId`. This is the **heart of the lab** — each function is a deep-dive into its beliefs, mechanisms, and relay outputs.

```
┌──────────────────────────────────────────────────────────┐
│ F1 SENSORY PROCESSING                              SPU   │
│ ┌──────┐ ┌───────────┐ ┌──────────────┐                 │
│ │6 Core│ │8 Appraisal│ │3 Anticipation│  8 mechanisms    │
│ └──────┘ └───────────┘ └──────────────┘  Phase 0a        │
├──────────────────────────────────────────────────────────┤
│ ░ AUDIO TIMELINE  ~~∿~~∿~~∿~~∿~~|~~∿~~∿~~∿~~           │
├──────────────────────────────────────────────────────────┤
│ [Beliefs (17)]  [Mechanisms (8)]  [Relay Output]         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  BELIEFS TAB                                             │
│  ┌─────────────────────────────────────────────────┐     │
│  │ Filter: [All] [Core] [Appraisal] [Anticipation] │     │
│  │ Group:  [By Mechanism] [By Type]                 │     │
│  └─────────────────────────────────────────────────┘     │
│                                                          │
│  ── BCH (4 beliefs) ──────────────────────────────       │
│                                                          │
│  ┌─ harmonic_stability ──────────────────────────┐       │
│  │ [Core] τ=0.30  baseline=0.50       BCH        │       │
│  │                                                │       │
│  │ Source Dimensions:                             │       │
│  │  P0:consonance_signal  ████████░░  0.50       │       │
│  │  P1:template_match     ██████░░░░  0.30       │       │
│  │  E2:hierarchy          ████░░░░░░  0.20       │       │
│  │                                                │       │
│  │ ┌──────────────────────────────────────────┐   │       │
│  │ │ ~~∿~~∿~~∿∿~~∿~~∿∿~~∿~~∿∿~~|~~~∿~~∿~~  │   │       │
│  │ │              signal trace                │   │       │
│  │ └──────────────────────────────────────────┘   │       │
│  │                                                │       │
│  │ mean: 0.4231  std: 0.0872  min: 0.201         │       │
│  │ max:  0.7124  current: 0.4451                  │       │
│  │                                                │       │
│  │ ┌─ Bayesian Detail ─────────────────────────┐  │       │
│  │ │ τ ──●─────────────── 0.30 (fast)          │  │       │
│  │ │ PE mean: 0.032  PE std: 0.018             │  │       │
│  │ │ π_pred: 2.41   π_obs: 1.87               │  │       │
│  │ │ gain: 0.437    update strength: moderate  │  │       │
│  │ └──────────────────────────────────────────┘  │       │
│  └────────────────────────────────────────────────┘       │
│                                                          │
│  ┌─ interval_quality ────────────────────────────┐       │
│  │ [Appraisal]                         BCH       │       │
│  │ E2:hierarchy ██████████ 1.00                  │       │
│  │ ~~~~~~ sparkline ~~~~~~                       │       │
│  │ mean: 0.5821  std: 0.1203                     │       │
│  └────────────────────────────────────────────────┘       │
│                                                          │
│  ── CSG (1 belief) ───────────────────────────────       │
│  ── MIAA (2 beliefs) ─────────────────────────────       │
│  ...                                                     │
│                                                          │
│  MECHANISMS TAB                                          │
│  ┌─ BCH ─────────────────────┐ ┌─ CSG ────────────────┐ │
│  │ SPU · Relay · Depth 0     │ │ ASU · Relay · Depth 0│ │
│  │ Output: 16D               │ │ Output: 12D          │ │
│  │ H³ demand: 48 tuples      │ │ H³ demand: 18 tuples │ │
│  │                           │ │                      │ │
│  │ Layers:                   │ │ Layers:              │ │
│  │ E ████  4D  Extraction    │ │ E ███  3D  Extract   │ │
│  │ M ████  4D  Memory        │ │ M ███  3D  Memory    │ │
│  │ P ████  4D  Present       │ │ P ███  3D  Present   │ │
│  │ F ████  4D  Forecast      │ │ F ███  3D  Forecast  │ │
│  │                           │ │                      │ │
│  │ 4 beliefs linked          │ │ 1 belief linked      │ │
│  │ RegionLinks: A1,STG,MGB   │ │ RegionLinks: ACC,AI  │ │
│  │ NeuroLinks: DA(0.15)      │ │ NeuroLinks: DA(0.15) │ │
│  └───────────────────────────┘ └──────────────────────┘ │
│                                                          │
│  RELAY TAB                                               │
│  BCH Output: 16 dimensions                               │
│  ┌──────────────────────────────────────────────────┐    │
│  │ ∿∿∿∿∿∿  multi-signal trace (16 dims)  ∿∿∿∿∿∿   │    │
│  └──────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────┐    │
│  │ Dim │ Name              │ Scope    │ Spark │ μ   │    │
│  │  0  │ salience_activ.   │ internal │ ~~~   │.42  │    │
│  │  1  │ sensory_evidence  │ internal │ ~~~   │.61  │    │
│  │  6  │ consonance_signal │ hybrid   │ ~~~   │.55  │    │
│  │ ... │ ...               │ ...      │ ...   │...  │    │
│  └──────────────────────────────────────────────────┘    │
└──────────────────────────────────────────────────────────┘
```

#### Function-Specific Content

| Function | Route | Unit | Beliefs | Mechanisms | Relays | Depth Range | Special Features |
|----------|-------|------|:-------:|:----------:|:------:|:-----------:|------------------|
| **F1** Sensory | `/brain/f1` | SPU/ASU/NDU | 17 (5C+7A+5N) | 11 | BCH(16D), CSG(12D), MIAA(11D), MPG(10D) | 0–2 | Consonance hierarchy, pitch salience |
| **F2** Prediction | `/brain/f2` | PCU | 15 (4C+6A+5N) | 10 | HTP(12D), SPH(14D), ICEM(13D) | 0–5 | 3 Integrators + 2 Hubs, deepest cascade |
| **F3** Attention | `/brain/f3` | ASU/STU | 15 (4C+7A+4N) | 12 | SNEM(12D), IACM(11D) | 0–2 | Beat entrainment, selective gain gate |
| **F4** Memory | `/brain/f4` | IMU | 13 (4C+7A+2N) | 15 | MEAMN(12D), MMP(12D), PNH(11D) | 0–2 | Largest mech count, autobiographical |
| **F5** Emotion | `/brain/f5` | ARU | 14 (4C+8A+2N) | 12 | SRP(19D), AAC(14D), VMM(12D) | 0–2 | Valence/arousal, wanting/liking/pleasure |
| **F6** Reward | `/brain/f6` | RPU | 16 (5C+7A+4N) | 10 | DAED(8D), MORMR(7D), RPEM(8D) | 0–2 | DA pathways, reward formula |
| **F7** Motor | `/brain/f7` | MPU/STU | 17 (4C+9A+4N) | 12 | PEOM(11D), MSR(11D), GSSM(11D) | 0–2 | Period entrainment, groove, dance |
| **F8** Learning | `/brain/f8` | SPU/NDU | 14 (4C+8A+2N) | 6 | EDNR(10D) | 0–2 | Plasticity, expertise, τ up to 0.95 |
| **F9** Social | `/brain/f9` | — | 10 (2C+6A+2N) | **0** | — | — | Pure belief layer, fed by F5/F6/F7 |

> **Total**: 131 beliefs (36 Core + 65 Appraisal + 30 Anticipation) across **88 mechanisms** (26 Relays + 33 Encoders + 26 Associators + 3 Integrators + 2 Hubs). F9 has zero mechanisms — a pure inference layer.

### 5. Reward Analyzer

**Route**: `/reward`

Deep reward signal analysis with the full formula decomposition.

- **Reward Trace**: Full T-length signal with cursor, stats overlay
- **Formula Components**: surprise, resolution, exploration, monotony (4 sub-traces)
- **Familiarity Modulation**: inverted-U curve overlay, familiarity trace
- **Emotional Modulation**: MEAMN emotional mod trace
- **DA Gain**: DAED dopamine gain trace
- **SRP Hedonic Blend**: wanting + liking + pleasure + tension weights
- **Statistics Panel**: mean, positive %, peak, trough, smoothness, dynamic range

### 6. RAM Viewer

**Route**: `/ram`

26 brain region activation visualization.

- **Region Heatmap**: 26 regions × T frames
- **3D Brain View** (optional): Three.js brain model with activation overlay
- **Category View**: Cortical (12) / Subcortical (9) / Brainstem (5) grouped
- **Convergence Hubs**: STG (6 feeds), NAcc (2 feeds), Hippocampus (3 feeds) highlighted
- **Per-Region Traces**: expandable activation traces with feeding relay info
- **Region Link Map**: which relays feed which regions, with weights

### 7. Ψ³ Cognitive State

**Route**: `/psi`

The 6-domain experiential readout (28D total).

- **Affect** (4D): valence, arousal, tension, dominance
- **Emotion** (7D): joy, sadness, fear, awe, nostalgia, tenderness, serenity
- **Aesthetic** (5D): beauty, groove, flow, surprise, closure
- **Bodily** (4D): chills, movement_urge, breathing_change, tension_release
- **Cognitive** (4D): familiarity, absorption, expectation, attention_focus
- **Temporal** (4D): anticipation, resolution, buildup, release

Each domain: multi-signal trace, radar/polar chart at cursor, stats table.

### 8. Neurochemical Viewer

**Route**: `/neuro`

4-channel neurochemical dynamics.

- **4 Channel Traces**: DA (amber), NE (red), OPI (violet), 5HT (emerald)
- **Interaction View**: wanting(DA) vs liking(OPI) dissociation overlay
- **Source Mapping**: which relays produce/amplify/inhibit each channel
- **Baseline Reference**: horizontal line at 0.5 baseline

### 9. Test Runner — Smoke Tests

**Route**: `/tests/smoke`

Run and monitor the 11-layer smoke test suite (synthetic data).

```
┌──────────────────────────────────────────────────────────┐
│ SMOKE TEST SUITE · 11 Layers · Synthetic Data            │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  [▶ Run All]  [Run Selected]           Status: IDLE      │
│                                                          │
│  ┌─ Layer 01 — Contracts ─────────────── ✓ PASS ──────┐  │
│  │ 25 tests · H3DemandSpec, LayerSpec, beliefs, nuclei │  │
│  │ Duration: 0.3s                                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌─ Layer 02 — R³ Spectral ───────────── ✓ PASS ──────┐  │
│  │ 18 tests · Shape (2,100,97), bounds [0,1], 9 groups │  │
│  │ Duration: 1.2s                                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌─ Layer 03 — H³ Temporal ───────────── ✓ PASS ──────┐  │
│  │ 15 tests · Demand coverage, tuple validity, bounds  │  │
│  │ Duration: 2.1s                                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌─ Layer 04 — Mechanism Anatomy ──────── ✓ PASS ──────┐ │
│  │ 40+ tests · Metadata, dims, layers, H³ demands      │ │
│  │ Duration: 0.8s                                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                          │
│  ... Layers 05-11 ...                                    │
│                                                          │
│  ┌─ Layer 11 — Integration ───────────── ✓ PASS ──────┐  │
│  │ 12 tests · R³→H³→C³ end-to-end pipeline             │  │
│  │ Duration: 8.4s                                      │  │
│  └─────────────────────────────────────────────────────┘  │
│                                                          │
│  SUMMARY: 11/11 PASS · 180 tests · 14.2s total          │
└──────────────────────────────────────────────────────────┘
```

**Layers**:
| # | Name | Tests | What It Validates |
|:-:|------|:-----:|-------------------|
| 01 | Contracts | ~25 | H3DemandSpec, LayerSpec, RegionLink, NeuroLink, belief/nucleus ABCs |
| 02 | R³ Spectral | ~18 | Shape (B,T,97), bounds [0,1], 9 groups, temporal variation |
| 03 | H³ Temporal | ~15 | Demand completeness, tuple components, differentiation, determinism |
| 04 | Mechanism Anatomy | ~40 | Class attrs, dims, layers, H³ demands, region/neuro links, metadata |
| 05 | Relay Compute | ~30 | Output shape, [0,1] bounds, EMPF layers, determinism, edge cases |
| 06 | Deep Compute | ~20 | Encoder/Associator forward pass, depth ordering, scope |
| 07 | Belief Anatomy | ~25 | 131 count (36C+65A+30N), per-function counts, TAU/BASELINE values |
| 08 | Belief observe() | ~131 | Shape (B,T), no NaN/Inf, [0,1] bounds, determinism |
| 09 | Belief predict() | ~36 | Core only: shape, no NaN, TAU inertia, baseline convergence |
| 10 | RAM & Neuro | ~15 | 26 regions, 4 channels, index mapping, accumulation |
| 11 | Integration | ~12 | Full R³→H³→C³ pipeline, BrainOutput validation |

### 10. Benchmark Runner — Real Audio

**Route**: `/tests/benchmark`

Run and monitor the 11-layer benchmark suite (real audio, ~30s excerpts).

```
┌──────────────────────────────────────────────────────────┐
│ BENCHMARK SUITE · 11 Tests · Real Audio                  │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  Audio Catalog: 7 files (bach, swan, herald, beethoven,  │
│                          duel, enigma, yang)              │
│                                                          │
│  [▶ Run All]  [Run Selected]          Status: RUNNING    │
│                                                          │
│  ┌─ 01 Audio Integrity ──────────────── ✓ PASS ──────┐  │
│  │ 7 files loaded · all shapes valid · mel [0,1]      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌─ 02 R³ Benchmark ─────────────────── ✓ PASS ──────┐  │
│  │ 7 files · avg 4,230 fps · 97D · all groups active   │  │
│  │ ┌──────────────────────────────────────────────┐    │  │
│  │ │ File     │ Frames │  FPS  │ Status           │    │  │
│  │ │ bach     │  5168  │ 4,812 │ ████████████ FAST│    │  │
│  │ │ swan     │  5168  │ 3,991 │ ██████████░░ FAST│    │  │
│  │ │ herald   │  5168  │ 4,102 │ ██████████░░ FAST│    │  │
│  │ └──────────────────────────────────────────────┘    │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ... Tests 03-11 ...                                     │
│                                                          │
│  ┌─ 07 Memory Profile ───────────────── ✓ PASS ──────┐  │
│  │ Peak: 1.7 GB (< 6 GB limit) · linear scaling       │  │
│  │ ┌──────────────────────────────────┐                │  │
│  │ │ Duration │ Peak MB │ MB/frame    │                │  │
│  │ │ 5s       │ 342     │ 0.40        │                │  │
│  │ │ 30s      │ 1,712   │ 0.33        │                │  │
│  │ │ 60s      │ 3,280   │ 0.32        │                │  │
│  │ └──────────────────────────────────┘                │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  ┌─ 08 Determinism ──────────────────── ✓ PASS ──────┐  │
│  │ R³ bit-identical: ✓ · H³ bit-identical: ✓          │  │
│  │ Relay deterministic: ✓ · max diff: 0.0             │  │
│  └────────────────────────────────────────────────────┘  │
│                                                          │
│  SUMMARY: 11/11 PASS · 7 audio files · 82.3s total      │
└──────────────────────────────────────────────────────────┘
```

**Benchmarks**:
| # | Name | Files | Measures |
|:-:|------|:-----:|----------|
| 01 | Audio Integrity | 7 | Load time, shape, mel bounds, energy |
| 02 | R³ Benchmark | 7 | FPS, group activation, temporal variation |
| 03 | R³ Distributions | 7 | Per-group stats, inter-piece differentiation, correlation |
| 04 | H³ Benchmark | 7 | FPS, demand coverage, morph differentiation |
| 05 | H³ Multi-Scale | 3 | Horizon smoothness, cross-horizon correlation |
| 06 | Full Pipeline | 3 | R³→H³→C³ timing breakdown, per-stage FPS |
| 07 | Memory Profile | 6 | Peak MB per stage, MB/frame, M2 8GB safety |
| 08 | Determinism | 3 | Bit-identical R³, H³, relays across runs |
| 09 | Cross-Genre | 7 | Genre fingerprints, clustering, temporal complexity |
| 10 | Reward & Salience | 7 | Salience peaks, reward dynamics, energy predictor |
| 11 | Duration Scaling | 6 | 5s→120s FPS stability, memory linear growth |

### 11. Pipeline Runner

**Route**: `/pipeline`

Execute the full R³→H³→C³ pipeline with live progress.

- **Audio Selection**: dropdown of available files
- **Excerpt Config**: start time, duration (default 30s)
- **Execution Console**: live phase updates (loading → mel → R³ → H³ → C³ → saving)
- **Progress Bar**: animated with phase label and FPS
- **Result Summary**: upon completion, metrics + links to explore results

### 12. Atlas

**Route**: `/atlas`

**UNCHANGED** — The existing NeuroacousticAtlas (2200×1400 interactive canvas diagram with 140 nodes, 60+ edges, particle animations).

### 13. Documentation Browser

**Route**: `/docs`

Browse Building/C³-Brain documentation tree with markdown rendering.

- **Left panel**: File tree (collapsible directories)
- **Right panel**: Markdown content viewer (react-markdown + remark-gfm)
- **Breadcrumb**: current doc path
- **Quick Links**: Ontology specs, Belief Cycle, Reward Formula, Precision Engine

---

## Static Data Registries

All C³ metadata is known at build-time from the Python sources. The frontend maintains static TypeScript registries:

### `data/functions.ts` — 9 Entries

```typescript
interface FunctionDef {
  id: string;           // "F1"–"F9"
  name: string;         // "Sensory Processing"
  unit: string;         // "SPU"
  description: string;  // one-line summary
  color: string;        // accent hex
  beliefs: { core: number; appraisal: number; anticipation: number; total: number };
  mechanisms: string[];
  relays: string[];     // relay names owned (subset of 9)
  phase: string;        // scheduler phase
}
```

### `data/beliefs.ts` — 131 Entries

```typescript
interface BeliefDef {
  index: number;                        // position in T×131 array
  name: string;                         // "harmonic_stability"
  fullName: string;                     // "Harmonic Stability"
  type: 'core' | 'appraisal' | 'anticipation';
  functionId: string;                   // "F1"
  mechanism: string;                    // "BCH"
  sourceDims: [string, number][];       // [["P0:consonance_signal", 0.50], ...]
  tau?: number;                         // Core only (0.0–1.0)
  baseline?: number;                    // Core only (~0.3–0.5)
}
```

### `data/mechanisms.ts` — 88 Entries

```typescript
interface MechanismDef {
  name: string;              // "BCH"
  fullName: string;          // "Brainstem Cochlear Hierarchy"
  functionId: string;        // "F1"
  unit: string;              // "SPU"
  role: string;              // "relay" | "encoder" | "associator" | "integrator" | "hub"
  outputDim: number;         // 16
  processingDepth: number;   // 0
  layers: LayerDef[];        // E/M/P/F breakdown
  h3DemandCount: number;     // 48
  beliefs: string[];         // belief names
  regionLinks: { dim: string; region: string; weight: number }[];
  neuroLinks: { dim: string; channel: string; weight: number; mode: string }[];
}
```

### `data/relays.ts` — 9 Entries

```typescript
interface RelayDef {
  name: string;       // "BCH"
  unit: string;       // "SPU"
  functionId: string; // "F1"
  outputDim: number;  // 16
  color: string;      // "#60a5fa"
  dimNames: string[]; // dimension name per output index
}
```

---

## Zustand Store Architecture

### Existing (Keep)

| Store | Purpose |
|-------|---------|
| `audioStore` | Playback state, cursor, waveform/spectrogram data |
| `pipelineStore` | Run state, R³/H³ data, experiment metadata |

### New

| Store | Purpose |
|-------|---------|
| `c3Store` | Bulk beliefs (T×131), relay cache (lazy), neuro, salience |
| `uiStore` | Sidebar collapsed, active section, theme |
| `testStore` | Test run state, results, progress per layer |

### `c3Store` Shape

```typescript
interface C3State {
  beliefsData: Float32Array | null;  // T × 131
  beliefNames: string[];
  nBeliefs: number;
  nFrames: number;
  relayCache: Record<string, { data: Float32Array; dim: number }>;
  neuroData: Float32Array | null;    // T × 4
  salienceData: Float32Array | null; // T
  beliefsLoading: boolean;
  relayLoading: Record<string, boolean>;
  loadBeliefs(experimentId: string): Promise<void>;
  loadRelay(experimentId: string, relayName: string): Promise<void>;
  loadNeuro(experimentId: string): Promise<void>;
  clear(): void;
}
```

---

## File Structure

```
Lab/frontend/src/
├── App.tsx                              REWRITE — new router
├── main.tsx                             KEEP
├── index.css                            REWRITE — Liquid Glass CSS
│
├── api/
│   ├── client.ts                        KEEP — extend with test endpoints
│   └── c3Client.ts                      NEW — C³-specific loaders
│
├── design/
│   ├── tokens.ts                        REWRITE — expanded tokens
│   └── functionMeta.ts                  NEW — F1–F9 colors/names
│
├── data/
│   ├── functions.ts                     NEW — 9 function definitions
│   ├── beliefs.ts                       NEW — 131 belief definitions
│   ├── mechanisms.ts                    NEW — 88 mechanism definitions
│   └── relays.ts                        NEW — 9 relay mappings
│
├── stores/
│   ├── audioStore.ts                    KEEP
│   ├── pipelineStore.ts                 MODIFY — remove C³ beliefs (→ c3Store)
│   ├── c3Store.ts                       NEW — beliefs + relay + neuro cache
│   ├── uiStore.ts                       NEW — sidebar, theme
│   └── testStore.ts                     NEW — test runner state
│
├── hooks/
│   ├── useBeliefData.ts                 NEW — per-function belief filter
│   ├── useRelayData.ts                  NEW — lazy relay loader
│   ├── useFunctionData.ts              NEW — combined F-page loader
│   └── useTestRunner.ts                NEW — test execution hook
│
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx                  REWRITE — grouped nav
│   │   ├── TopBar.tsx                   REWRITE — breadcrumb + run button
│   │   ├── GlassPanel.tsx               REWRITE — enhanced variants
│   │   ├── PageShell.tsx                NEW — page wrapper
│   │   └── SectionDivider.tsx           NEW — labeled divider
│   │
│   ├── glass/
│   │   ├── GlassCard.tsx                NEW — expandable card
│   │   ├── GlassBadge.tsx               NEW — type badge
│   │   ├── GlassChip.tsx                NEW — pill tag
│   │   ├── GlassTabs.tsx                NEW — tab bar
│   │   ├── GlassButton.tsx              NEW — button
│   │   ├── GlassSelect.tsx              NEW — dropdown
│   │   └── GlassTooltip.tsx             NEW — hover detail
│   │
│   ├── audio/
│   │   ├── AudioPlayer.tsx              KEEP
│   │   ├── Waveform.tsx                 KEEP
│   │   ├── Spectrogram.tsx              KEEP
│   │   └── AudioTimeline.tsx            NEW — compact 35px strip
│   │
│   ├── charts/
│   │   ├── SignalTrace.tsx              KEEP — core renderer
│   │   ├── HeatmapChart.tsx             KEEP
│   │   ├── BeliefTrace.tsx              NEW — single belief + stats
│   │   ├── SparkLine.tsx                NEW — tiny inline trace
│   │   ├── StatsSummary.tsx             NEW — compact stat row
│   │   └── MechanismLayerChart.tsx      NEW — E/M/P/F bar
│   │
│   ├── c3/
│   │   ├── FunctionHeader.tsx           NEW — function page header
│   │   ├── MechanismCard.tsx            NEW — expandable mechanism
│   │   ├── BeliefCard.tsx               NEW — expandable belief
│   │   ├── BeliefGrid.tsx               NEW — filtered belief list
│   │   ├── BeliefTypeFilter.tsx         NEW — type filter bar
│   │   ├── RelayPanel.tsx               NEW — relay dim traces
│   │   ├── SourceDimsTable.tsx          NEW — dim weights
│   │   └── BayesianDetail.tsx           NEW — Core PE/precision
│   │
│   └── testing/
│       ├── TestSuiteCard.tsx            NEW — test suite panel
│       ├── TestLayerRow.tsx             NEW — individual layer result
│       ├── TestProgressBar.tsx          NEW — animated progress
│       ├── BenchmarkTable.tsx           NEW — benchmark metrics table
│       └── BenchmarkChart.tsx           NEW — FPS/memory chart
│
├── pages/
│   ├── Overview.tsx                     NEW — replaces Dashboard
│   ├── ear/
│   │   ├── R3Explorer.tsx               REWRITE — new glass aesthetic
│   │   └── H3Explorer.tsx               REWRITE — new glass aesthetic
│   ├── brain/
│   │   └── FunctionPage.tsx             NEW — shared F1–F9 page
│   ├── output/
│   │   ├── RewardAnalyzer.tsx           REWRITE
│   │   ├── RamViewer.tsx                NEW
│   │   ├── PsiViewer.tsx                NEW — Ψ³ cognitive state
│   │   └── NeuroViewer.tsx              NEW — neurochemical channels
│   ├── testing/
│   │   ├── SmokeTestRunner.tsx          NEW
│   │   └── BenchmarkRunner.tsx          NEW
│   ├── tools/
│   │   ├── PipelineRunner.tsx           REWRITE
│   │   └── DocumentationBrowser.tsx     REWRITE
│   └── NeuroacousticAtlas.tsx           KEEP — untouched
│
└── vite.config.ts                       MODIFY — proxy test endpoints
```

### Files Deleted (4)
- `pages/Dashboard.tsx` → replaced by Overview
- `pages/C3Explorer.tsx` → replaced by 9 F-page routes
- `pages/ExperimentCompare.tsx` → removed
- `pages/Documentation.tsx` → replaced by DocumentationBrowser

---

## Backend Extensions

### New Router: `/api/tests` (`routers/tests.py`)

```python
@router.get("/list")
async def list_test_suites() -> List[TestSuiteInfo]:
    """List available test suites (smoke_test_001, benchmark_real_audio)."""

@router.post("/run")
async def run_tests(request: TestRunRequest) -> TestRunResponse:
    """Execute a test suite. Runs pytest in subprocess."""

@router.get("/status/{run_id}")
async def get_test_status(run_id: str) -> TestRunStatus:
    """Get running test progress (parsing pytest output)."""

@router.get("/results/{run_id}")
async def get_test_results(run_id: str) -> TestResults:
    """Get completed test results (parsed from pytest JSON)."""
```

### New Service: `test_runner.py`

```python
class TestRunner:
    def run_suite(suite: str, layers: List[int] | None = None) -> str:
        """Run pytest with --json-report, return run_id."""

    def get_status(run_id: str) -> TestRunStatus:
        """Parse live pytest output for progress."""

    def get_results(run_id: str) -> TestResults:
        """Parse pytest JSON report into structured results."""
```

### New Endpoints on Pipeline Router

```python
@router.get("/results/{id}/c3/neuro")
async def get_neuro(id: str) -> Response:
    """Binary float32 (T×4) neurochemical channels."""

@router.get("/results/{id}/c3/salience")
async def get_salience(id: str) -> Response:
    """Binary float32 (T,) salience signal."""

@router.get("/results/{id}/c3/psi")
async def get_psi(id: str) -> JSONResponse:
    """Ψ³ cognitive state — 6 domains as JSON arrays."""
```

---

## Implementation Phases

### Phase 1 — Foundation (Design System + Data Layer)
- [ ] Enhanced `index.css` with Liquid Glass tokens
- [ ] Expanded `design/tokens.ts` + `functionMeta.ts`
- [ ] Static data registries: `functions.ts`, `beliefs.ts`, `mechanisms.ts`, `relays.ts`
- [ ] Verify belief index alignment with backend `X-Belief-Names` header

### Phase 2 — Stores + Hooks
- [ ] `c3Store.ts` — beliefs + relay + neuro cache
- [ ] `uiStore.ts` — sidebar state
- [ ] `testStore.ts` — test runner state
- [ ] Custom hooks: `useBeliefData`, `useRelayData`, `useFunctionData`

### Phase 3 — Glass Component Library
- [ ] Glass primitives: Card, Badge, Chip, Tabs, Button, Select, Tooltip
- [ ] Layout: PageShell, SectionDivider
- [ ] Charts: BeliefTrace, SparkLine, StatsSummary, MechanismLayerChart
- [ ] Audio: AudioTimeline (compact strip)

### Phase 4 — C³ Brain Components
- [ ] FunctionHeader, MechanismCard, BeliefCard, BeliefGrid
- [ ] BeliefTypeFilter, RelayPanel, SourceDimsTable, BayesianDetail

### Phase 5 — Pages
- [ ] `FunctionPage.tsx` — shared F1–F9 component
- [ ] `Overview.tsx` — new home page
- [ ] Restyled: R3Explorer, H3Explorer, RewardAnalyzer
- [ ] New: RamViewer, PsiViewer, NeuroViewer
- [ ] Restyled: PipelineRunner, DocumentationBrowser

### Phase 6 — Testing UI
- [ ] Backend: `routers/tests.py`, `services/test_runner.py`
- [ ] Frontend: SmokeTestRunner, BenchmarkRunner pages
- [ ] Testing components: TestSuiteCard, TestLayerRow, BenchmarkTable

### Phase 7 — Router + Layout Integration
- [ ] `App.tsx` — new route structure (17 routes)
- [ ] `Sidebar.tsx` — full rewrite with grouped sections
- [ ] `TopBar.tsx` — breadcrumb + quick run button

### Phase 8 — Polish + Performance
- [ ] Loading states (pulse animation on glass cards)
- [ ] Error boundaries with glass error panels
- [ ] Empty states (no experiment selected)
- [ ] Canvas RAF optimization (IntersectionObserver for off-screen traces)
- [ ] Collapsed card SparkLine (lightweight) vs expanded full trace
- [ ] `npm run build` — verify TypeScript compiles clean

---

## Performance Considerations

| Concern | Strategy |
|---------|----------|
| 131 belief traces on F-page | Only render RAF loops for visible cards (IntersectionObserver) |
| Bulk beliefs data (T×131×4B ≈ 2.5MB) | Single fetch, client-side slicing per function |
| Relay lazy loading | Fetch on first tab activation, cache in c3Store |
| Canvas repaints during playback | 60fps RAF loop with cursor sync (existing pattern) |
| Collapsed belief cards | SparkLine (60×20px, no RAF) instead of full SignalTrace |
| Stats computation | useMemo keyed on (data, currentFrame), only "current" updates at 60fps |
| Test runner | Subprocess with streaming output, parsed incrementally |

---

## Metrics & Observability

### What the Lab Measures

| Domain | Metric | Source |
|--------|--------|--------|
| **R³** | 97 features × T frames | R3Extractor |
| **H³** | 131+ demand tuples × T | H3Extractor |
| **C³ Beliefs** | 131 belief values × T | Scheduler |
| **C³ Relays** | 9 relays (5–19D each) × T | Relay mechanisms |
| **RAM** | 26 brain regions × T | RegionLink accumulation |
| **Neuro** | 4 channels × T | NeuroLink accumulation |
| **Reward** | scalar × T | Reward formula |
| **Salience** | scalar × T | Salience mixer |
| **Ψ³** | 28D (6 domains) × T | PsiInterpreter |
| **Performance** | FPS per stage | Pipeline timing |
| **Memory** | Peak MB per stage | torch profiler |
| **Determinism** | Bit-identical verification | Dual-run comparison |

### Test Coverage Map

| Layer | Module | Tests | Type |
|-------|--------|:-----:|------|
| Contracts | contracts/ | 25 | Smoke |
| R³ Extraction | ear/r3/ | 18 + 7×3 | Smoke + Bench |
| R³ Distributions | ear/r3/ | 7×4 | Bench |
| H³ Extraction | ear/h3/ | 15 + 7×3 | Smoke + Bench |
| H³ Multi-Scale | ear/h3/ | 12 | Bench |
| Mechanism Anatomy | brain/functions/ | 40 | Smoke |
| Relay Compute | brain/functions/ | 30 | Smoke |
| Deep Compute | brain/functions/ | 20 | Smoke |
| Belief Anatomy | brain/functions/ | 25 | Smoke |
| Belief observe() | brain/functions/ | 131 | Smoke |
| Belief predict() | brain/functions/ | 36 | Smoke |
| RAM & Neuro | brain/regions/ | 15 | Smoke |
| Integration | brain/ | 12 | Smoke |
| Full Pipeline | all | 3×5 | Bench |
| Memory Profile | all | 6×3 | Bench |
| Determinism | all | 3×5 | Bench |
| Cross-Genre | all | 7×4 | Bench |
| Reward & Salience | brain/kernel/ | 7×3 | Bench |
| Duration Scaling | all | 6×3 | Bench |

---

## Appendix A — Complete Route Table

| Route | Page Component | Data Required |
|-------|---------------|---------------|
| `/` | Overview | experiments, audio list |
| `/r3` | R3Explorer | r3Features (T×97) |
| `/h3` | H3Explorer | h3Tuples + h3Values |
| `/brain/f1` | FunctionPage("F1") | beliefs (T×131), BCH relay |
| `/brain/f2` | FunctionPage("F2") | beliefs, HTP relay |
| `/brain/f3` | FunctionPage("F3") | beliefs, SNEM relay |
| `/brain/f4` | FunctionPage("F4") | beliefs, MEAMN relay |
| `/brain/f5` | FunctionPage("F5") | beliefs, SRP relay |
| `/brain/f6` | FunctionPage("F6") | beliefs, DAED relay |
| `/brain/f7` | FunctionPage("F7") | beliefs, PEOM+HMCE relays |
| `/brain/f8` | FunctionPage("F8") | beliefs, EDNR relay |
| `/brain/f9` | FunctionPage("F9") | beliefs |
| `/reward` | RewardAnalyzer | reward, salience, beliefs |
| `/ram` | RamViewer | ram (T×26) |
| `/psi` | PsiViewer | psi (6 domains) |
| `/neuro` | NeuroViewer | neuro (T×4) |
| `/tests/smoke` | SmokeTestRunner | test results |
| `/tests/benchmark` | BenchmarkRunner | benchmark results |
| `/pipeline` | PipelineRunner | pipeline state |
| `/atlas` | NeuroacousticAtlas | none (static) |
| `/docs` | DocumentationBrowser | doc tree + content |

---

## Appendix B — Complete 131-Belief Registry

**Legend**: Type: **C**=Core (Bayesian update) · **A**=Appraisal (observe-only) · **N**=Anticipation (prediction)

### F1: Sensory Processing — 17 beliefs (5C + 7A + 5N)

| # | Name | Type | Mech | τ | β₀ | Key Source Dims |
|:-:|------|:----:|:----:|:-:|:--:|-----------------|
| 0 | consonance_salience_gradient | A | CSG | — | — | P0:salience_network(0.40), E0:salience_activation(0.30) |
| 1 | contour_continuation | A | MPG | — | — | F0:phrase_boundary_pred(1.00) |
| 2 | melodic_contour_tracking | A | MPG | — | — | P1:contour_state(0.45), E2:contour_complexity(0.30) |
| 3 | consonance_trajectory | A | BCH | — | — | F0:consonance_forecast(1.00) |
| 4 | harmonic_stability | **C** | BCH | 0.30 | 0.50 | P0:consonance_signal(0.50), P1:template_match(0.30), E2:hierarchy(0.20) |
| 5 | harmonic_template_match | A | BCH | — | — | P1:template_match(1.00) |
| 6 | interval_quality | A | BCH | — | — | E2:hierarchy(1.00) |
| 7 | pitch_continuation | A | PSCL | — | — | F0:pitch_continuation(1.00) |
| 8 | pitch_prominence | **C** | PSCL | 0.35 | 0.50 | P0:pitch_prominence_sig(0.60), P1:hg_cortical_response(0.25) |
| 9 | octave_equivalence | A | PCCR | — | — | P1:octave_equivalence_index(1.00) |
| 10 | pitch_identity | **C** | PCCR | 0.40 | 0.50 | P0:chroma_identity_signal(0.55), P2:chroma_salience(0.25) |
| 11 | aesthetic_quality | **C** | STAI | 0.40 | 0.50 | E2:aesthetic_integration(0.40), P2:aesthetic_response(0.30) |
| 12 | reward_response_pred | A | STAI | — | — | F1:reward_response_pred(0.50), P2:aesthetic_response(0.30) |
| 13 | spectral_temporal_synergy | A | STAI | — | — | M1:spectral_temporal_interaction(0.50), E2:aesthetic_integration(0.30) |
| 14 | imagery_recognition | A | MIAA | — | — | F2:recognition_pred(1.00) |
| 15 | timbral_character | **C** | MIAA | 0.50 | 0.50 | P0:melody_retrieval(0.50), E0:imagery_activation(0.30) |
| 16 | spectral_complexity | A | SDED | — | — | M0:detection_function(0.40), P0:roughness_detection(0.30) |

### F2: Pattern Recognition & Prediction — 15 beliefs (4C + 6A + 5N)

| # | Name | Type | Mech | τ | β₀ | Key Source Dims |
|:-:|------|:----:|:----:|:-:|:--:|-----------------|
| 17 | abstract_future | A | HTP | — | — | F0:abstract_future_500ms(1.00) |
| 18 | hierarchy_coherence | A | HTP | — | — | E3:hierarchy_gradient(0.50), P2:abstract_prediction(0.30) |
| 19 | midlevel_future | A | HTP | — | — | F1:midlevel_future_200ms(1.00) |
| 20 | prediction_accuracy | **C** | HTP | 0.50 | 0.50 | P0:sensory_match(0.50), P1:pitch_prediction(0.30) |
| 21 | prediction_hierarchy | **C** | HTP | 0.40 | 0.50 | E0:high_level_lead(0.40), E1:mid_level_lead(0.30) |
| 22 | arousal_change_pred | A | ICEM | — | — | F0:arousal_change_1_3s(1.00) |
| 23 | arousal_scaling | A | ICEM | — | — | E1:arousal_response(0.40), M1:arousal_pred(0.30) |
| 24 | defense_cascade | A | ICEM | — | — | E3:defense_cascade(0.50), M3:scr_pred(0.30) |
| 25 | information_content | **C** | ICEM | 0.35 | 0.50 | E0:information_content(0.40), M0:ic_value(0.30) |
| 26 | valence_inversion | A | ICEM | — | — | E2:valence_response(0.40), M2:valence_pred(0.30) |
| 27 | valence_shift_pred | A | ICEM | — | — | F1:valence_shift_2_5s(1.00) |
| 28 | error_propagation | A | SPH | — | — | E1:alpha_beta_error(0.40), P1:prediction_error(0.30) |
| 29 | oscillatory_signature | A | SPH | — | — | M2:gamma_power(0.40), M3:alpha_beta_power(0.30) |
| 30 | sequence_completion | A | SPH | — | — | F1:sequence_completion_2s(1.00) |
| 31 | sequence_match | **C** | SPH | 0.45 | 0.50 | E0:gamma_match(0.40), P0:memory_match(0.30) |

### F3: Attention & Salience — 15 beliefs (4C + 7A + 4N)

| # | Name | Type | Mech | τ | β₀ | Key Source Dims |
|:-:|------|:----:|:----:|:-:|:--:|-----------------|
| 32 | consonance_valence_mapping | A | CSG | — | — | P1:affective_evaluation(1.00) |
| 33 | processing_load_pred | A | CSG | — | — | F1:processing_pred(1.00) |
| 34 | salience_network_activation | **C** | CSG | 0.30 | 0.40 | P0:salience_network(0.40), E0:salience_activation(0.30) |
| 35 | sensory_load | A | CSG | — | — | P2:sensory_load(0.60), E1:sensory_evidence(0.40) |
| 36 | attention_capture | **C** | IACM | 0.25 | 0.30 | E0:inharmonic_capture(0.40), M0:attention_capture(0.30) |
| 37 | attention_shift_pred | A | IACM | — | — | F1:attention_shift_pred(1.00) |
| 38 | object_segregation | A | IACM | — | — | P1:spectral_encoding(0.60), M2:object_perception_or(0.40) |
| 39 | precision_weighting | A | IACM | — | — | E2:precision_weighting(1.00) |
| 40 | aesthetic_engagement | A | AACM | — | — | P0:n1p2_engagement(0.60), M0:aesthetic_engagement(0.40) |
| 41 | savoring_effect | A | AACM | — | — | P1:aesthetic_judgment(0.60), E2:savoring_effect(0.40) |
| 42 | beat_entrainment | **C** | SNEM | 0.35 | 0.50 | P0:beat_locked_activity(0.40), M0:ssep_enhancement(0.30) |
| 43 | beat_onset_pred | A | SNEM | — | — | F0:beat_onset_pred(1.00) |
| 44 | meter_hierarchy | **C** | SNEM | 0.40 | 0.50 | M0:ssep_enhancement(0.40), E1:meter_entrainment(0.30) |
| 45 | meter_position_pred | A | SNEM | — | — | F1:meter_position_pred(0.50), M2:beat_salience(0.50) |
| 46 | selective_gain | A | SNEM | — | — | P2:selective_gain(1.00) |

### F4: Memory & Retrieval — 13 beliefs (4C + 7A + 2N)

| # | Name | Type | Mech | τ | β₀ | Key Source Dims |
|:-:|------|:----:|:----:|:-:|:--:|-----------------|
| 47 | melodic_recognition | A | MMP | — | — | P1:melodic_identification(0.60), R1:melodic_recognition(0.40) |
| 48 | memory_preservation | A | MMP | — | — | C0:preservation_index(1.00) |
| 49 | memory_scaffold_pred | A | MMP | — | — | F2:scaffold_fc(1.00) |
| 50 | autobiographical_retrieval | **C** | MEAMN | 0.85 | 0.30 | P0:memory_state(0.40), E0:f01_retrieval(0.30) |
| 51 | emotional_coloring | **C** | MEAMN | 0.75 | 0.30 | P1:emotional_color(0.40), E2:f03_emotion(0.30) |
| 52 | memory_vividness | A | MEAMN | — | — | E0:f01_retrieval(0.50), P1:emotional_color(0.50) |
| 53 | nostalgia_intensity | **C** | MEAMN | 0.80 | 0.20 | P2:nostalgia_link(0.40), E1:f02_nostalgia(0.30) |
| 54 | retrieval_probability | A | MEAMN | — | — | P0:memory_state(1.00) |
| 55 | self_relevance | A | MEAMN | — | — | F2:self_ref_fc(1.00) |
| 56 | vividness_trajectory | A | MEAMN | — | — | F0:mem_vividness_fc(1.00) |
| 57 | consolidation_strength | A | HCMC | — | — | P2:storage_state(1.00) |
| 58 | episodic_boundary | A | HCMC | — | — | P1:segmentation_state(1.00) |
| 59 | episodic_encoding | **C** | HCMC | 0.70 | 0.40 | P0:binding_state(0.40), E0:fast_binding(0.30) |

### F5: Emotion — 14 beliefs (4C + 8A + 2N)

| # | Name | Type | Mech | τ | β₀ | Key Source Dims |
|:-:|------|:----:|:----:|:-:|:--:|-----------------|
| 60 | ans_dominance | A | AAC | — | — | E1:ans_response(1.00) |
| 61 | chills_intensity | A | AAC | — | — | I0:chills_intensity(1.00) |
| 62 | driving_signal | A | AAC | — | — | P1:driving_signal(1.00) |
| 63 | emotional_arousal | **C** | AAC | 0.50 | 0.50 | E0:emotional_arousal(0.50), P0:current_intensity(0.30) |
| 64 | emotion_certainty | A | VMM | — | — | P2:emotion_certainty(1.00) |
| 65 | happy_pathway | A | VMM | — | — | R0:happy_pathway(1.00) |
| 66 | mode_detection | A | VMM | — | — | C0:mode_detection_state(1.00) |
| 67 | perceived_happy | **C** | VMM | 0.55 | 0.50 | P0:perceived_happy(0.40), V1:mode_signal(0.30) |
| 68 | perceived_sad | **C** | VMM | 0.55 | 0.50 | P1:perceived_sad(0.40), 1-V1:mode_signal(0.30) |
| 69 | sad_pathway | A | VMM | — | — | R1:sad_pathway(1.00) |
| 70 | nostalgia_affect | **C** | NEMAC | 0.65 | 0.30 | W0:nostalgia_intens(0.40), E1:nostalgia(0.30) |
| 71 | nostalgia_peak_pred | A | NEMAC | — | — | F1:vividness_pred(1.00) |
| 72 | self_referential_nostalgia | A | NEMAC | — | — | M0:mpfc_activation(1.00) |
| 73 | wellbeing_enhancement | A | NEMAC | — | — | W1:wellbeing_enhance(1.00) |

### F6: Reward & Motivation — 16 beliefs (5C + 7A + 4N)

| # | Name | Type | Mech | τ | β₀ | Key Source Dims |
|:-:|------|:----:|:----:|:-:|:--:|-----------------|
| 74 | da_caudate | A | DAED | — | — | caudate_activation(1.00) |
| 75 | da_nacc | A | DAED | — | — | nacc_activation(1.00) |
| 76 | dissociation_index | A | DAED | — | — | dissociation_index(1.00) |
| 77 | temporal_phase | A | DAED | — | — | temporal_phase(1.00) |
| 78 | wanting_ramp | A | DAED | — | — | f03:wanting_index(1.00) |
| 79 | chills_proximity | A | SRP | — | — | F1:chills_proximity(1.00) |
| 80 | harmonic_tension | A | SRP | — | — | M0:harmonic_tension(1.00) |
| 81 | liking | **C** | SRP | 0.65 | 0.50 | P1:liking(1.00) |
| 82 | peak_detection | A | SRP | — | — | M2:peak_detection(1.00) |
| 83 | pleasure | **C** | SRP | 0.70 | 0.50 | P2:pleasure(1.00) |
| 84 | prediction_error | **C** | SRP | 0.50 | 0.00 | C2:prediction_error(1.00) |
| 85 | prediction_match | A | SRP | — | — | T1:prediction_match(1.00) |
| 86 | resolution_expectation | A | SRP | — | — | F2:resolution_expect(1.00) |
| 87 | reward_forecast | A | SRP | — | — | F0:reward_forecast(1.00) |
| 88 | tension | **C** | SRP | 0.55 | 0.00 | T0:tension(1.00) |
| 89 | wanting | **C** | SRP | 0.60 | 0.50 | P0:wanting(1.00) |

### F7: Motor & Timing — 17 beliefs (4C + 9A + 4N)

| # | Name | Type | Mech | τ | β₀ | Key Source Dims |
|:-:|------|:----:|:----:|:-:|:--:|-----------------|
| 90 | auditory_motor_coupling | A | HGSIC | — | — | coupling_strength(1.00) |
| 91 | beat_prominence | A | HGSIC | — | — | f01:beat_gamma(0.50), pstg_activation(0.50) |
| 92 | groove_quality | **C** | HGSIC | 0.55 | 0.50 | groove_index(0.50), f03:motor_groove(0.30) |
| 93 | groove_trajectory | A | HGSIC | — | — | groove_prediction(1.00) |
| 94 | meter_structure | A | HGSIC | — | — | f02:meter_integration(1.00) |
| 95 | motor_preparation | A | HGSIC | — | — | motor_preparation(1.00) |
| 96 | kinematic_efficiency | **C** | PEOM | 0.60 | 0.50 | f02:velocity_optimization(0.40), velocity(0.30) |
| 97 | next_beat_pred | A | PEOM | — | — | next_beat_pred_T(1.00) |
| 98 | period_entrainment | **C** | PEOM | 0.65 | 0.50 | f01:period_entrainment(0.50), period_lock_strength(0.30) |
| 99 | period_lock_strength | A | PEOM | — | — | period_lock_strength(1.00) |
| 100 | timing_precision | A | PEOM | — | — | f03:variability_reduction(0.50), cv_reduction(0.50) |
| 101 | context_depth | **C** | HMCE | 0.70 | 0.50 | context_depth(0.50), f01:short_context(0.20) |
| 102 | long_context | A | HMCE | — | — | f03:long_context(1.00) |
| 103 | medium_context | A | HMCE | — | — | f02:medium_context(1.00) |
| 104 | phrase_boundary_pred | A | HMCE | — | — | phrase_boundary_pred(1.00) |
| 105 | short_context | A | HMCE | — | — | f01:short_context(1.00) |
| 106 | structure_pred | A | HMCE | — | — | structure_pred(1.00) |

### F8: Learning & Expertise — 14 beliefs (4C + 8A + 2N)

| # | Name | Type | Mech | τ | β₀ | Key Source Dims |
|:-:|------|:----:|:----:|:-:|:--:|-----------------|
| 107 | detection_accuracy | A | SLEE | — | — | f02:detection_accuracy(0.60), P0:expectation_formation(0.40) |
| 108 | multisensory_binding | A | SLEE | — | — | f03:multisensory_integration(0.60), P1:cross_modal_binding(0.40) |
| 109 | statistical_model | **C** | SLEE | 0.88 | 0.50 | f01:statistical_model(0.40), M0:exposure_model(0.30) |
| 110 | plasticity_magnitude | A | TSCP | — | — | f03:plasticity_magnitude(0.60), M0:enhancement_function(0.40) |
| 111 | trained_timbre_recognition | **C** | TSCP | 0.90 | 0.50 | f01:trained_timbre_response(0.40), P2:timbre_identity(0.30) |
| 112 | compartmentalization_cost | A | ECT | — | — | f02:between_reduction(0.60), network_isolation(0.40) |
| 113 | transfer_limitation | A | ECT | — | — | transfer_limit(1.00) |
| 114 | expertise_enhancement | **C** | ESME | 0.92 | 0.50 | f04:expertise_enhancement(0.50), M0:mmn_expertise_function(0.30) |
| 115 | expertise_trajectory | A | ESME | — | — | F2:developmental_trajectory(1.00) |
| 116 | pitch_mmn | A | ESME | — | — | f01:pitch_mmn(0.60), P0:pitch_deviance_detection(0.40) |
| 117 | rhythm_mmn | A | ESME | — | — | f02:rhythm_mmn(0.60), P1:rhythm_deviance_detection(0.40) |
| 118 | timbre_mmn | A | ESME | — | — | f03:timbre_mmn(0.60), P2:timbre_deviance_detection(0.40) |
| 119 | network_specialization | **C** | EDNR | 0.95 | 0.50 | f03:compartmentalization(0.40), f04:expertise_signature(0.30) |
| 120 | within_connectivity | A | EDNR | — | — | f01:within_connectivity(0.60), current_compartm(0.40) |

### F9: Social Cognition — 10 beliefs (2C + 6A + 2N)

> F9 has **zero mechanisms**. All beliefs source from cross-function mechanisms: SSRI (F6), NSCP (F7), DDSMI (F7).

| # | Name | Type | Mech | τ | β₀ | Key Source Dims |
|:-:|------|:----:|:----:|:-:|:--:|-----------------|
| 121 | collective_pleasure_pred | A | SSRI | — | — | F1:flow_sustain_pred(0.50), f05:collective_pleasure(0.50) |
| 122 | entrainment_quality | A | SSRI | — | — | f04:entrainment_quality(1.00) |
| 123 | group_flow | A | SSRI | — | — | f03:group_flow_state(0.60), M1:synchrony_amplification(0.40) |
| 124 | social_bonding | A | SSRI | — | — | f02:social_bonding_index(0.60), P1:endorphin_proxy(0.40) |
| 125 | social_prediction_error | A | SSRI | — | — | M0:social_prediction_error(1.00) |
| 126 | synchrony_reward | A | SSRI | — | — | f01:synchrony_reward(0.70), P0:prefrontal_coupling(0.30) |
| 127 | catchiness_pred | A | NSCP | — | — | F2:catchiness_pred(1.00) |
| 128 | neural_synchrony | **C** | NSCP | 0.65 | 0.50 | E0:f22_neural_synchrony(0.50), M0:isc_magnitude(0.30) |
| 129 | resource_allocation | A | DDSMI | — | — | E2:f15_visual_modulation(0.60), M2:mTRF_balance(0.40) |
| 130 | social_coordination | **C** | DDSMI | 0.60 | 0.50 | E0:f13_social_coordination(0.50), P0:partner_sync(0.30) |

### Core Belief τ Distribution

| Range | Count | Beliefs |
|-------|:-----:|---------|
| **Low (0.25–0.40)** | 9 | attention_capture(0.25), harmonic_stability(0.30), salience_network_activation(0.30), pitch_prominence(0.35), beat_entrainment(0.35), information_content(0.35), pitch_identity(0.40), prediction_hierarchy(0.40), aesthetic_quality(0.40) |
| **Medium (0.45–0.60)** | 12 | sequence_match(0.45), timbral_character(0.50), prediction_accuracy(0.50), emotional_arousal(0.50), prediction_error(0.50), perceived_happy(0.55), perceived_sad(0.55), groove_quality(0.55), tension(0.55), kinematic_efficiency(0.60), wanting(0.60), social_coordination(0.60) |
| **High (0.65–0.70)** | 7 | nostalgia_affect(0.65), liking(0.65), neural_synchrony(0.65), period_entrainment(0.65), pleasure(0.70), episodic_encoding(0.70), context_depth(0.70) |
| **Very High (0.75+)** | 8 | emotional_coloring(0.75), nostalgia_intensity(0.80), autobiographical_retrieval(0.85), statistical_model(0.88), trained_timbre_recognition(0.90), expertise_enhancement(0.92), network_specialization(0.95) |

---

## Appendix C — Relay Dimension Map

### BCH (F1, SPU) — 16D
```
E[0:4]   salience_activation, sensory_evidence, hierarchy, consonance_core     internal
M[4:8]   roughness_memory, brightness_memory, harmonic_memory, spectral_memory  internal
P[8:12]  consonance_signal, template_match, stability_index, binding_strength   hybrid
F[12:16] consonance_forecast, harmonic_forecast, template_forecast, trend_fc    external
```

### SNEM (F3, ASU) — 12D
```
E[0:3]   beat_entrainment, meter_entrainment, selective_enhancement   internal
M[3:6]   ssep_enhancement, enhancement_index, beat_salience           internal
P[6:9]   beat_locked_activity, entrainment_strength, selective_gain   hybrid
F[9:12]  beat_onset_pred, meter_position_pred, enhancement_pred       external
```

### MEAMN (F4, IMU) — 12D
```
E[0:3]   f01_retrieval, f02_nostalgia, f03_emotion    internal
M[3:5]   meam_retrieval, p_recall                      internal
P[5:8]   memory_state, emotional_color, nostalgia_link  hybrid
F[8:12]  mem_vividness_fc, emo_response_fc, self_ref_fc, reserved  external
```

### SRP (F5, ARU) — 19D
```
N+C[0:6]   da_caudate, da_nacc, opioid_proxy, vta_drive, stg_nacc_coupling, prediction_error  internal
T+M[6:13]  tension, prediction_match, reaction, appraisal, harmonic_tension, dynamic_intensity, peak_detection  internal
P[13:16]   wanting, liking, pleasure                                                            hybrid
F[16:19]   reward_forecast, chills_proximity, resolution_expect                                 external
```

### DAED (F6, RPU) — 8D
```
E[0:4]  anticipatory_da, consummatory_da, wanting_index, liking_index  internal
M[4:6]  dissociation_index, temporal_phase                              internal
P[6:8]  caudate_activation, nacc_activation                             hybrid
```

### PEOM (F7, MPU) — 11D
```
E[0:3]   period_entrainment, velocity_optimization, variability_reduction  internal
M[3:7]   motor_period, velocity, acceleration, cv_reduction                internal
P[7:9]   period_lock_strength, kinematic_smoothness                        hybrid
F[9:11]  next_beat_pred_T, velocity_profile_pred                           external
```

### HMCE (F7, STU) — 11D
```
E[0:3]   short_context, medium_context, long_context              internal
M[3:6]   context_depth, structure_regularity, transition_dynamics  internal
P[6:9]   a1_stg_encoding, context_predict, phrase_expect           hybrid
F[9:11]  phrase_boundary_pred, structure_pred                      external
```

### HTP (F2, PCU) — 12D
```
E[0:4]  high_level_lead, mid_level_lead, low_level_lead, hierarchy_gradient  internal
M[4:7]  match_history, prediction_stability, error_magnitude                  internal
P[7:10] sensory_match, pitch_prediction, abstract_prediction                  hybrid
F[10:12] abstract_future_500ms, midlevel_future_200ms                         external
```

### EDNR (F8, NDU) — 10D
```
E[0:3]  network_specialization, within_connectivity, between_connectivity  internal
M[3:6]  plasticity_rate, efficiency_gain, consolidation_index              internal
P[6:8]  current_expertise, learning_trajectory                             hybrid
F[8:10] expertise_forecast, efficiency_forecast                            external
```

---

## Appendix D — 26 Brain Regions (RAM Tensor Mapping)

The **Region Activation Map (RAM)** is a `(B, T, 26)` tensor. Each region receives weighted contributions from mechanism RegionLinks via `ram[:, :, reg_idx] += output[:, :, dim_idx] * weight`.

### Cortical Regions (Indices 0–11)

| Idx | Name | Abbr | MNI (x,y,z) | BA | Functional Role |
|:---:|------|:----:|:-----------:|:--:|-----------------|
| 0 | Primary Auditory Cortex (Heschl's Gyrus) | A1_HG | (48, -18, 8) | 41 | Tonotopic frequency analysis; rightward pitch, leftward temporal fine structure |
| 1 | Superior Temporal Gyrus | STG | (58, -22, 4) | 22 | Auditory association; melody, harmony, timbre. **Convergence hub** (6+ relay feeds) |
| 2 | Superior Temporal Sulcus | STS | (54, -32, 4) | 21 | Multimodal stream integration; voice/music discrimination, audiovisual binding |
| 3 | Inferior Frontal Gyrus (Broca's Area) | IFG | (48, 18, 8) | 44 | Musical syntax processing; ERAN for harmonic violations, hierarchical parsing |
| 4 | Dorsolateral Prefrontal Cortex | dlPFC | (42, 32, 30) | 46 | Working memory; tonal context maintenance, executive control |
| 5 | Ventromedial Prefrontal Cortex | vmPFC | (2, 46, -10) | 10 | Subjective value computation; reward integration, musical autobiography |
| 6 | Orbitofrontal Cortex | OFC | (28, 34, -16) | 11 | Reward valuation; conscious aesthetic value of music |
| 7 | Anterior Cingulate Cortex | ACC | (2, 30, 28) | 32 | Conflict monitoring; harmonic violation detection, salience hub |
| 8 | Supplementary Motor Area | SMA | (2, -2, 56) | 6 | Internal timing; beat-level metric structure during listening |
| 9 | Premotor Cortex | PMC | (46, 0, 48) | 6 | Auditory-motor coupling; rhythm entrainment, sensorimotor sync |
| 10 | Angular Gyrus | AG | (48, -60, 30) | 39 | Cross-modal integration; binds auditory, visual, somatosensory |
| 11 | Temporal Pole | TP | (42, 12, -32) | 38 | Semantic memory hub; abstract musical knowledge, genre schemas |

### Subcortical Regions (Indices 12–20)

| Idx | Name | Abbr | MNI (x,y,z) | Functional Role |
|:---:|------|:----:|:-----------:|-----------------|
| 12 | Ventral Tegmental Area | VTA | (0, -16, -8) | DA source; reward prediction error during unexpected progressions |
| 13 | Nucleus Accumbens | NAcc | (10, 12, -8) | Consummatory reward; DA + OPI for peak pleasure (Salimpoor 2011, r=0.84) |
| 14 | Caudate Nucleus | caudate | (12, 10, 10) | Anticipatory reward; DA release 10–15s before pleasure (Salimpoor r=0.71) |
| 15 | Amygdala | amygdala | (24, -4, -18) | Emotional valence tagging; dissonance, tension, affective salience |
| 16 | Hippocampus | hippocampus | (28, -22, -12) | Musical memory; familiarity detection, episodic associations, statistical learning |
| 17 | Putamen | putamen | (26, 4, 2) | Beat-based motor timing; entrainment to regular rhythm (Grahn & Rowe d=0.67) |
| 18 | Thalamus (MGB) | MGB | (14, -24, -2) | Primary auditory relay; gates ascending spectrotemporal with attention |
| 19 | Hypothalamus | hypothalamus | (0, -4, -8) | Autonomic regulation; heart rate, chills, skin conductance |
| 20 | Insula | insula | (36, 16, 0) | Interoceptive awareness; bodily arousal + emotional context integration |

### Brainstem Regions (Indices 21–25)

| Idx | Name | Abbr | MNI (x,y,z) | Functional Role |
|:---:|------|:----:|:-----------:|-----------------|
| 21 | Inferior Colliculus | IC | (0, -34, -8) | Midbrain auditory relay; frequency-following response (FFR) for pitch |
| 22 | Auditory Nerve | AN | (8, -26, -24) | Peripheral encoding; phase-locked spike trains for spectrotemporal info |
| 23 | Cochlear Nucleus | CN | (10, -38, -32) | First central station; parallel spectral/temporal extraction |
| 24 | Superior Olivary Complex | SOC | (6, -34, -24) | First binaural stage; interaural time/level differences for spatial hearing |
| 25 | Periaqueductal Gray | PAG | (0, -30, -10) | Autonomic/emotional regulation; chills, piloerection, respiratory changes |

---

## Appendix E — Ψ³ Cognitive State Computation (28D)

The **Ψ³ Cognitive State** is the experiential readout layer. `PsiInterpreter` maps C³ outputs (tensor, RAM, neuro) into 6 domains totaling **28 dimensions**, all clamped to [0, 1].

### Domain 1: Affect (4D) — Core Emotional Coordinates

| Dim | Name | Formula | Sources |
|:---:|------|---------|---------|
| 0 | **Valence** | `0.6 × DA + 0.4 × OPI` | DA wanting + OPI liking |
| 1 | **Arousal** | `NE` | Norepinephrine directly |
| 2 | **Tension** | `0.5 × amygdala + 0.5 × (1.0 - 5HT)` | Amygdala + inverse serotonin |
| 3 | **Dominance** | `dlPFC` | Dorsolateral prefrontal activation |

### Domain 2: Emotion (7D) — Categorical Emotions

| Dim | Name | Formula | Basis |
|:---:|------|---------|-------|
| 0 | **Joy** | `valence × arousal` | High positive + high arousal |
| 1 | **Sadness** | `(1 - valence) × (1 - arousal)` | Low affect negative |
| 2 | **Fear** | `tension × arousal` | Tension + arousal combined |
| 3 | **Awe** | `valence × arousal × NAcc` | Reward integration (Salimpoor 2011) |
| 4 | **Nostalgia** | `valence × hippocampus` | Memory hub (Janata 2009) |
| 5 | **Tenderness** | `valence × (1 - arousal) × (1 - tension)` | Positive low-tension |
| 6 | **Serenity** | `valence × (1 - tension) × (1 - arousal)` | Positive calm |

### Domain 3: Aesthetic (5D) — Musical Judgement

| Dim | Name | Formula | Basis |
|:---:|------|---------|-------|
| 0 | **Beauty** | `0.5 × DA + 0.5 × OPI` | Reward integration (Salimpoor 2013) |
| 1 | **Groove** | `0.5 × putamen + 0.5 × SMA` | Motor areas + rhythm (Janata 2012) |
| 2 | **Flow** | `NAcc × (1 - 0.5×(1 - 5HT))` | Engagement + low tension |
| 3 | **Surprise** | `ReLU(DA - 0.6)` | DA phasic bursts above threshold (Schultz 1997) |
| 4 | **Closure** | `1.0 - surprise` | Inverse surprise (resolution) |

### Domain 4: Bodily (4D) — Felt Sensations

| Dim | Name | Formula | Basis |
|:---:|------|---------|-------|
| 0 | **Chills** | `0.3×PAG + 0.3×hypothalamus + 0.4×OPI` | Blood & Zatorre 2001 |
| 1 | **Movement Urge** | `0.5×putamen + 0.5×SMA` | Motor planning (Grahn & Rowe 2009) |
| 2 | **Breathing Change** | `hypothalamus` | Autonomic hub |
| 3 | **Tension Release** | `OPI × (1.0 - NE)` | Opioid × low arousal |

### Domain 5: Cognitive (4D) — Mental States

| Dim | Name | Formula | Basis |
|:---:|------|---------|-------|
| 0 | **Familiarity** | `hippocampus` | Episodic/semantic memory (Janata 2009) |
| 1 | **Absorption** | `0.5×insula + 0.5×NAcc` | Interoception + reward (Craig 2009) |
| 2 | **Expectation** | `dlPFC` | Working memory / anticipation |
| 3 | **Attention Focus** | `dlPFC` | Executive attention |

### Domain 6: Temporal (4D) — Moment-in-Time Dynamics

| Dim | Name | Formula | Basis |
|:---:|------|---------|-------|
| 0 | **Anticipation** | `clamp(2 × ReLU(DA - 0.5), 0, 1)` | DA rising above baseline (Salimpoor 2011, caudate 10–15s before) |
| 1 | **Resolution** | `OPI` | Opioid peak (consummatory) |
| 2 | **Buildup** | `clamp(2 × ReLU(NE - 0.5), 0, 1)` | NE rising arousal |
| 3 | **Release** | `5HT` | Serotonin-mediated calm (Doya 2002) |

---

## Appendix F — Neurochemical Channels (4D)

The **neuro tensor** is `(B, T, 4)`, all channels initialized to **0.5 baseline**.

### Channel Summary

| Ch | Name | Abbr | Baseline | Role | Key Reference |
|:--:|------|:----:|:--------:|------|---------------|
| 0 | Dopamine | DA | 0.5 | Reward prediction error: wanting vs liking | Doya 2002, Berridge 2003 |
| 1 | Norepinephrine | NE | 0.5 | Exploration-exploitation (LC-mediated) | Aston-Jones & Cohen 2005 |
| 2 | Opioid | OPI | 0.5 | Hedonic evaluation (mu-opioid in NAcc) | Blood & Zatorre 2001, Mallik 2017 |
| 3 | Serotonin | 5HT | 0.5 | Temporal discount rate, mood baseline | Doya 2002, Crockett 2009 |

### Reference Values

| Channel | State | Value | Source |
|---------|-------|:-----:|--------|
| DA | Phasic threshold | 0.60 | Above=burst, below=tonic |
| DA | Peak anticipatory (caudate) | 0.78 | Salimpoor 2011, 10–15s before pleasure |
| DA | Peak consummatory (NAcc) | 0.88 | Salimpoor 2011, at pleasure moment |
| DA | Levodopa enhancement | 0.92 | +14.7% pleasure (Ferreri 2019) |
| DA | Risperidone blockade | 0.28 | -10.2% pleasure (Ferreri 2019) |
| NE | Unexpected event (phasic) | 0.75 | Burst to surprising musical event |
| NE | Familiar/predictable | 0.35 | Low tonic during predictable sequences |
| OPI | Peak chills | 0.85 | Blood & Zatorre 2001 |
| OPI | Naltrexone blockade | 0.30 | Mallik 2017 (antagonist) |
| 5HT | Elevated/calm/patient | 0.70 | Long-horizon reward sensitivity |
| 5HT | Depleted/anxious | 0.30 | Tryptophan depletion, short-horizon bias |

### Accumulation Semantics

Mechanism `NeuroLinks` modify channels with three effects:

```
produce:  neuro[ch] = dim_value × weight         (direct set)
amplify:  neuro[ch] += dim_value × weight × (1 - neuro[ch])  (toward 1.0)
inhibit:  neuro[ch] -= dim_value × weight × neuro[ch]        (toward 0.0)

All channels clamped to [0, 1] after each nucleus.
```

### Cross-Channel Interactions

| Pair | Relationship |
|------|-------------|
| DA ↔ OPI | Wanting-liking dissociation in NAcc (Berridge 2003); both needed for peak pleasure |
| DA ↔ 5HT | 5HT2C on VTA inhibits DA release; 5HT1B on NAcc facilitates DA |
| NE ↔ 5HT | Inverse: high arousal (NE) ↔ low mood (5HT) |
| NE ↔ OPI | Arousal potentiates hedonic response; NE amplifies OPI-mediated pleasure |
| 5HT ↔ OPI | Mood baseline modulates hedonic capacity; low 5HT blunts opioid pleasure |
| DA ↔ NE | Phasic NE burst enhances DA reward prediction error signal |

---

## Appendix G — Complete Mechanism Catalog (88 Mechanisms)

### Summary by Type

| Type | Count | Depth | Description |
|------|:-----:|:-----:|-------------|
| **Relay** | 26 | 0 | Direct R³/H³ readers — signal entry points |
| **Encoder** | 33 | 1 | Reads relay outputs — primary cortical encoding |
| **Associator** | 26 | 2 | Reads encoder outputs — binding and association |
| **Integrator** | 3 | 3 | Reads all upstream — feedforward consolidation |
| **Hub** | 2 | 4–5 | Rich-club nodes — global integration |

### F1: Sensory Processing — 11 mechanisms

| Mechanism | Type | Unit | Depth | Dim | Full Name |
|-----------|:----:|:----:|:-----:|:---:|-----------|
| BCH | Relay | SPU | 0 | 16D | Brainstem Consonance Hierarchy |
| CSG | Relay | ASU | 0 | 12D | Consonance-Salience Gradient |
| MIAA | Relay | SPU | 0 | 11D | Musical Imagery Auditory Activation |
| MPG | Relay | NDU | 0 | 10D | Melodic Processing Gradient |
| PNH | Relay | IMU | 0 | 11D | Pythagorean Neural Hierarchy |
| SDNPS | Relay | SPU | 0 | 10D | Stimulus-Dependent NPS |
| SDED | Relay | SPU | 0 | 10D | Sensory Dissonance Early Detection |
| TPIO | Relay | SPU | 0 | 10D | Timbre Perception-Imagery Overlap |
| PSCL | Encoder | SPU | 1 | 16D | Pitch Salience in Cortical Lateralization |
| PCCR | Associator | SPU | 2 | 11D | Pitch Chroma Cortical Representation |
| STAI | Encoder | SPU | 1 | 12D | Spectral-Temporal Aesthetic Integration |

### F2: Pattern Recognition & Prediction — 10 mechanisms

| Mechanism | Type | Depth | Dim | Full Name |
|-----------|:----:|:-----:|:---:|-----------|
| HTP | Relay | 0 | 12D | Hierarchical Temporal Prediction |
| SPH | Relay | 0 | 14D | Sequence Prediction Hierarchy |
| ICEM | Relay | 0 | 13D | Information Content & Emotional Modulation |
| PWUP | Encoder | 1 | 10D | Precision-Weighted Uncertainty Processing |
| WMED | Associator | 2 | 11D | Working Memory Expectation Dynamics |
| UDP | Integrator | 3 | 10D | Uncertainty-Driven Pleasure |
| CHPI | Integrator | 3 | 11D | Cross-Modal Harmonic Predictive Integration |
| IGFE | Integrator | 3 | 9D | Information-Gain Feature Extraction |
| MAA | Hub | 4 | 10D | Musical Appreciation of Atonality |
| PSH | Hub | 5 | 10D | Prediction Surprise Hierarchy |

> F2 has the **deepest cascade** (Depth 0→5) with 3 Integrators and 2 Hubs.

### F3: Attention & Salience — 12 mechanisms

| Mechanism | Type | Unit | Depth | Dim | Full Name |
|-----------|:----:|:----:|:-----:|:---:|-----------|
| SNEM | Relay | ASU | 0 | 12D | Sensory Novelty & Expectation Model |
| IACM | Relay | ASU | 0 | 11D | Inharmonic Attention Capture Model |
| BARM | Encoder | ASU | 1 | 10D | Beat-Aligned Resource Model |
| STANM | Encoder | ASU | 1 | 11D | Sustained Tonal Attention Network Model |
| AACM | Encoder | ASU | 1 | 10D | Aesthetic Attention Coupling Model |
| AMSS | Encoder | STU | 1 | 11D | Attentional Modulation of Sound Streams |
| ETAM | Encoder | STU | 1 | 11D | Entrainment-Triggered Attention Model |
| DGTP | Associator | ASU | 2 | 9D | Dynamic Gain & Timing Precision |
| SDL | Associator | ASU | 2 | 9D | Sensory Discrimination Learning |
| NEWMD | Associator | STU | 2 | 10D | Neural Event-Window Model of Deviance |
| IGFE | Associator | PCU | 2 | 9D | Information-Gain Feature Extraction |
| PWSM | Associator | ASU | 2 | 9D | Precision-Weighted Salience Mixer |

### F4: Memory & Retrieval — 15 mechanisms

| Mechanism | Type | Depth | Dim | Full Name |
|-----------|:----:|:-----:|:---:|-----------|
| MEAMN | Relay | 0 | 12D | Music-Evoked Autobiographical Memory Network |
| MMP | Relay | 0 | 12D | Multi-Modal Perceptual Processing |
| PNH | Relay | 0 | 11D | Pythagorean Neural Hierarchy (shared F1) |
| HCMC | Encoder | 1 | 11D | Hippocampal-Cortical Memory Circuit |
| RASN | Encoder | 1 | 11D | Rhythmic Auditory Stimulation Neuroplasticity |
| PMIM | Encoder | 1 | 11D | Predictive Memory Integration Model |
| OII | Encoder | 1 | 10D | Oscillatory Intelligence Integration |
| RIRI | Encoder | 1 | 10D | RAS-Intelligent Rehabilitation Integration |
| MSPBA | Encoder | 1 | 11D | Musical Syntax Processing in Broca's Area |
| DMMS | Associator | 2 | 10D | Developmental Music Memory Scaffold |
| CSSL | Associator | 2 | 10D | Cross-Species Song Learning |
| CDEM | Associator | 2 | 10D | Context-Dependent Emotional Memory |
| TPRD | Associator | 2 | 10D | Tonotopy-Pitch Representation Dissociation |
| CMAPCC | Associator | 2 | 10D | Cross-Modal Action-Perception Common Code |
| VRIAP | Associator | 2 | 10D | VR-Integrated Analgesia Paradigm |

> F4 has the **most mechanisms** (15) — reflecting memory's deep integration needs.

### F5: Emotion — 12 mechanisms

| Mechanism | Type | Depth | Dim | Full Name |
|-----------|:----:|:-----:|:---:|-----------|
| SRP | Relay | 0 | 19D | Salience-Reward Pathway |
| AAC | Relay | 0 | 14D | Affective Attentional Coupling |
| VMM | Relay | 0 | 12D | Valence-Mood Modulation |
| PUPF | Encoder | 1 | 12D | Pleasure-Uncertainty Prediction Function |
| CLAM | Encoder | 1 | 11D | Closed-Loop Affective Modulation |
| MAD | Encoder | 1 | 11D | Musical Anhedonia Disconnection |
| NEMAC | Encoder | 1 | 11D | Nostalgia-Evoked Memory-Affect Circuit |
| STAI | Encoder | 1 | 12D | Spectral-Temporal Aesthetic Integration |
| DAP | Associator | 2 | 10D | Developmental Affective Plasticity |
| CMAT | Associator | 2 | 10D | Cross-Modal Affective Transfer |
| TAR | Associator | 2 | 10D | Therapeutic Affective Resonance |
| MAA | Associator | 2 | 10D | Musical Appreciation of Atonality |

### F6: Reward & Motivation — 10 mechanisms

| Mechanism | Type | Depth | Dim | Full Name |
|-----------|:----:|:-----:|:---:|-----------|
| DAED | Relay | 0 | 8D | Dopamine Anticipation-Experience Dissociation |
| MORMR | Relay | 0 | 7D | Mesolimbic Opioid-Reward Modulation Route |
| RPEM | Relay | 0 | 8D | Reward Prediction Error Modulation |
| IUCP | Encoder | 1 | 6D | Inverted-U Complexity Preference |
| MCCN | Encoder | 1 | 7D | Musical Chills Cortical Network |
| MEAMR | Encoder | 1 | 6D | Music-Evoked Autobiographical Memory Reward |
| SSRI | Encoder | 1 | 11D | Social Synchrony Reward Integration |
| LDAC | Associator | 2 | 6D | Liking-Dependent Auditory Cortex |
| IOTMS | Associator | 2 | 5D | Individual Opioid Tone Music Sensitivity |
| SSPS | Associator | 2 | 6D | Saddle-Shaped Preference Surface |

### F7: Motor & Timing — 12 mechanisms

| Mechanism | Type | Unit | Depth | Dim | Full Name |
|-----------|:----:|:----:|:-----:|:---:|-----------|
| PEOM | Relay | MPU | 0 | 11D | Period Entrainment Optimization Model |
| MSR | Relay | MPU | 0 | 11D | Motor Synchronization Response |
| GSSM | Relay | MPU | 0 | 11D | Groove State Sensorimotor Mapping |
| HMCE | Relay | STU | 0 | 11D | Hierarchical Musical Context Encoding |
| ASAP | Encoder | MPU | 1 | 11D | Action Simulation for Auditory Prediction |
| DDSMI | Encoder | MPU | 1 | 11D | Dyadic Dance Social Motor Integration |
| VRMSME | Encoder | MPU | 1 | 11D | VR Music Stimulation Motor Enhancement |
| SPMC | Encoder | MPU | 1 | 11D | SMA-Premotor-M1 Motor Circuit |
| HGSIC | Encoder | STU | 1 | 11D | Hierarchical Groove State Integration Circuit |
| NSCP | Associator | MPU | 2 | 11D | Neural Synchrony Commercial Prediction |
| CTBB | Associator | MPU | 2 | 11D | Cerebellar Theta-Burst Balance |
| STC | Associator | MPU | 2 | 11D | Singing Training Connectivity |

### F8: Learning & Expertise — 6 mechanisms

| Mechanism | Type | Unit | Depth | Dim | Full Name |
|-----------|:----:|:----:|:-----:|:---:|-----------|
| EDNR | Relay | NDU | 0 | 10D | Error-Driven Neural Refinement |
| TSCP | Encoder | SPU | 1 | 10D | Temporal Synaptic Consolidation Processor |
| CDMR | Encoder | NDU | 1 | 11D | Context-Dependent Mismatch Response |
| SLEE | Encoder | NDU | 1 | 13D | Synaptic Long-term Encoding Engine |
| ESME | Associator | SPU | 2 | 11D | Error-Signal Modulated Encoding |
| ECT | Associator | NDU | 2 | 12D | Expertise Compartmentalization Trade-off |

### F9: Social Cognition — 0 mechanisms

> F9 is a **pure belief layer** with zero mechanisms. All 10 beliefs source from cross-function mechanisms: **SSRI** (F6 Encoder), **NSCP** (F7 Associator), **DDSMI** (F7 Encoder).

---

## Appendix H — H³ Demand Specifications (277 Tuples)

Each mechanism declares H³ demands as `(r3_idx, horizon, morph, law)` tuples specifying which temporal morphology features it needs.

### Demand Counts per Mechanism

| Mechanism | Fn | Type | H³ Demands | OUTPUT_DIM |
|-----------|:--:|:----:|:----------:|:----------:|
| BCH | F1 | Relay | **48** | 16D |
| SRP | F5 | Relay | **31** | 19D |
| PSCL | F1 | Encoder | 20 | 16D |
| MEAMN | F4 | Relay | 19 | 12D |
| CSG | F1 | Relay | 18 | 12D |
| HTP | F2 | Relay | 18 | 12D |
| HMCE | F7 | Relay | 17 | 11D |
| DAED | F6 | Relay | 16 | 8D |
| MPG | F1 | Relay | 16 | 10D |
| PEOM | F7 | Relay | 15 | 11D |
| SNEM | F3 | Relay | 14 | 12D |
| PCCR | F1 | Assoc. | 14 | 11D |
| MIAA | F1 | Relay | 11 | 11D |
| SDED | F1 | Relay | 9 | 10D |
| **TOTAL** | | | **277** | |

### H³ Tuple Format

```
(r3_idx, horizon, morph, law)

r3_idx:  0–96 (R³ feature index)
horizon: 0–31 (time scale: H0≈25ms, H3≈100ms, H8≈500ms, H16≈1s, H20≈5s, H24≈36s)
morph:   0=value, 1=mean, 2=std, 4=max, 8=velocity, 13=entropy, 14=periodicity, 18=trend, 20=entropy, 22=peaks
law:     0=L0(memory/backward), 1=L1(forward), 2=L2(integration/bidirectional)
```

### BCH Demands (48 tuples — sample)

```
(0, roughness, H0, M0:value, L2)      — Instantaneous roughness
(5, helmholtz, H0, M0:value, L2)      — Helmholtz consonance now
(38, PCE, H0, M0:value, L2)           — Pitch class entropy now
(0, roughness, H6, M18:trend, L0)     — Roughness trend 200ms backward
(0, roughness, H12, M1:mean, L0)      — Roughness memory mean 525ms
(0, roughness, H6, M1:mean, L1)       — Expected roughness 200ms ahead
(5, helmholtz, H6, M1:mean, L1)       — Expected consonance 200ms ahead
```

### SRP Demands (31 tuples — multi-scale reward)

```
(7, amplitude, H24, M8:velocity, L0)  — Energy velocity 36s (caudate ramp)
(0, roughness, H24, M18:trend, L0)    — Harmonic tension trajectory 36s
(7, amplitude, H20, M4:max, L1)       — Future max energy 5s (anticipation)
(21, sflux, H16, M8:velocity, L0)     — Spectral change rate (RPE)
(4, pleasantness, H16, M8:velocity, L0) — Consonance surprise (PE)
(7, amplitude, H20, M8:velocity, L1)  — Forward energy velocity (chills)
(4, pleasantness, H20, M18:trend, L1) — Consonance trend 5s (forecast)
```

### SNEM Demands (14 tuples — beat entrainment)

```
(10, sflux, H16, M14:periodicity, L2)   — Beat periodicity 1s
(11, onset, H16, M14:periodicity, L2)    — Onset periodicity 1s
(25, coupling, H16, M14:periodicity, L2) — Motor-auditory coupling 1s
(7, amplitude, H16, M1:mean, L2)         — Amplitude context 1s
(21, spectral_change, H4, M8:velocity, L0) — Spectral change velocity 125ms
```

---

## Appendix I — SRP Reward Formula Decomposition

### SRP Architecture (19D, 4 Layers)

```
N+C [0:6]    Extraction (neurochemical drives)
T+M [6:13]   Temporal Integration (tension, prediction match, dynamics)
P   [13:16]  Present — PRIMARY REWARD SIGNALS (wanting, liking, pleasure)
F   [16:19]  Forecast (reward_forecast, chills_proximity, resolution_expect)
```

### P-Layer: The Three Reward Signals

**P0: Wanting** (Anticipatory Reward)
```
P0 = σ(0.30×N0:da_caudate + 0.25×T0:tension + 0.25×M1:dynamic_intensity + 0.20×amplitude×C0:vta_drive)
```
> Caudate DA ramps 9–15s before peak (Salimpoor 2011)

**P1: Liking** (Consummatory Reward)
```
P1 = σ(0.30×N1:da_nacc + 0.25×M2:peak_detection + 0.25×T1:prediction_match + 0.20×coupling×consonance)
```
> NAcc DA burst at peak moments (Salimpoor 2011, r=0.84)

**P2: Pleasure** (Hedonic Impact)
```
P2 = σ(0.30×N2:opioid_proxy + 0.25×T3:appraisal×pleasantness + 0.25×consonance_trend×consonance + 0.20×C1:stg_nacc_coupling×N1:da_nacc)
```
> Opioid + DA integration (Mallik 2017: naltrexone blocks pleasure)

### N+C Layer: Extraction Components

**N0: Caudate Anticipatory DA** — ramps when future energy exceeds current
```
anticipation_gap = σ(amp_max_5s_fwd - amp_val_1s)
N0 = σ(0.35×amp_vel_36s×gap + 0.30×amplitude×amp_val_1s + 0.35×rough_trend_36s×consonance)
```

**N1: NAcc Consummatory DA** — bursts at peaks (high energy + consonance + surprise)
```
surprise = σ(sflux_vel_1s + entropy_vel_1s)
N1 = σ(0.35×amp_val_1s×consonance + 0.30×surprise×pleasantness + 0.35×pleas_vel_1s×onset_peaks_1s)
```

**N2: Opioid Hedonic Proxy** — consonance + smoothness + harmonic stability
```
N2 = σ(0.35×pleas_val_2s×consonance + 0.35×smooth_2s×pleasantness + 0.30×(1-rough_val_2s)×smoothness)
```

### F-Layer: Forecast

**F0: Reward Forecast** (5–15s ahead)
```
F0 = σ(0.30×P0:wanting + 0.30×amp_max_15s_fwd×N0 + 0.20×T0:tension + 0.20×M1×C0)
```

**F1: Chills Proximity**
```
F1 = σ(0.30×P1:liking + 0.30×amp_vel_5s_fwd×M2 + 0.20×P2:pleasure + 0.20×N1×M1)
```

**F2: Resolution Expectation**
```
F2 = σ(0.30×M0:tension×consonance_trend + 0.30×(1-rough_trend_5s)×stability + 0.20×P2 + 0.20×C2:PE)
```

### Global Reward Formula (v4.0)

```
Reward = Σ salience × (1.5×surprise + 0.8×resolution + 0.5×exploration − 0.6×monotony) × fam_mod × da_gain

Where:
  salience   = 0.5×weighted_avg + 0.5×element_max (peak preservation)
             = 0.25×R³_energy + 0.25×H³_velocity + 0.15×PE_carry + 0.35×relay_salience
  surprise   = PE magnitude from precision engine
  resolution = consonance trend (dissonance → consonance)
  exploration= entropy/uncertainty (novelty bonus)
  monotony   = lack of change (penalizes flat sections)
  fam_mod    = inverted-U curve on recurrence
  da_gain    = dopamine gain with tanh(π/12) compression
```

---

## Appendix J — Execution Engine Architecture

### Code Structure (NOT phase-scheduled)

The C³ kernel uses **depth-ordered execution**, not the logical phase schedule described in ontology docs. The actual code flow:

```
orchestrator.py: BrainOrchestrator.process(r3, h3, cross_unit_inputs)
    └── executor.py: execute(nuclei, h3, r3, cross_unit_inputs)
        ├── init ram = (B, T, 26) zeros
        ├── init neuro = (B, T, 4) filled with 0.5
        │
        ├── DEPTH 0 (26 Relays — all parallel):
        │   BCH, CSG, MIAA, MPG, SNEM, IACM, HTP, SPH, ICEM,
        │   MEAMN, MMP, PNH, SRP, AAC, VMM, DAED, MORMR, RPEM,
        │   PEOM, MSR, GSSM, HMCE, EDNR, SDNPS, SDED, TPIO
        │   → Each: output = nucleus.compute(h3, r3)
        │   → Each: _apply_region_links(ram, nucleus, output)
        │   → Each: accumulate_neuro(neuro, nucleus, output)
        │
        ├── DEPTH 1 (33 Encoders — parallel within depth):
        │   PSCL, STAI, PWUP, BARM, STANM, AACM, AMSS, ETAM,
        │   HCMC, RASN, PMIM, OII, RIRI, MSPBA, PUPF, CLAM, MAD,
        │   NEMAC, IUCP, MCCN, MEAMR, SSRI, ASAP, DDSMI, VRMSME,
        │   SPMC, HGSIC, TSCP, CDMR, SLEE, ...
        │   → Each reads: R³ + H³ + upstream relay outputs
        │
        ├── DEPTH 2 (26 Associators — parallel):
        │   PCCR, DGTP, SDL, NEWMD, DMMS, CSSL, CDEM, TPRD,
        │   CMAPCC, VRIAP, DAP, CMAT, TAR, LDAC, IOTMS, SSPS,
        │   NSCP, CTBB, STC, ESME, ECT, PWSM, WMED, ...
        │   → Each reads: R³ + H³ + relay + encoder outputs
        │
        ├── DEPTH 3 (3 Integrators):
        │   UDP, CHPI, IGFE (all F2)
        │   → Read ALL upstream
        │
        ├── DEPTH 4-5 (2 Hubs):
        │   MAA (D4), PSH (D5) — both F2
        │   → Rich-club global integration
        │
        └── psi_interpreter.py: PsiInterpreter.interpret(tensor, ram, neuro)
            ├── affect = _compute_affect(neuro, ram)        → (B, T, 4)
            ├── emotion = _compute_emotion(affect, ram)     → (B, T, 7)
            ├── aesthetic = _compute_aesthetic(tensor, neuro, ram) → (B, T, 5)
            ├── bodily = _compute_bodily(ram, neuro)        → (B, T, 4)
            ├── cognitive = _compute_cognitive(ram, tensor)  → (B, T, 4)
            └── temporal = _compute_temporal(tensor, neuro)  → (B, T, 4)

Final: BrainOutput(tensor, ram, neuro, psi=PsiState(6 domains))
```

### RAM Accumulation

```python
# Per-nucleus, after compute():
for region_link in nucleus.region_links:
    dim_idx = name_to_idx[region_link.dim_name]
    reg_idx = region_index(region_link.region)
    ram[:, :, reg_idx] += output[:, :, dim_idx] * region_link.weight
```

### Bayesian Belief Update (Core Beliefs Only)

```
predict:  pred_t = τ × prev + w_trend×H³(M18) + w_period×H³(M14) + w_ctx×beliefs_{t-1}
observe:  obs_t  = Σ(source_dim_i × weight_i)  from mechanism P/E/M layers
gain:     g = π_obs / (π_obs + π_pred)         Bayesian precision weighting
update:   belief_t = prev + g × (obs_t - pred_t)
precision: tanh(π_raw / 12)                    compression to prevent divergence
```

### Salience Computation (4-Signal Mix)

```
energy:     0.25 × R³ amplitude features
h3_velocity: 0.25 × H³ velocity morphs
pe_carry:   0.15 × prediction error carry-over from precision engine
relay:      0.35 × SNEM(entrainment + beat_onset + meter_pos)
                 + MPG(onset + contour + boundary)
                 + SRP.tension

mixing = 0.5 × weighted_average + 0.5 × element_max  (peak preservation)
SNEM.selective_gain: multiplicative attention gate after mixing
```

---

*MI-Lab v2.0 — Where every signal tells a story, and every belief has a trace.*
