# C3 Cognitive Architecture -- Master Index

**Version**: 2.0.0
**Models**: 96 (across 9 cognitive units, 3 evidence tiers)
**Status**: Active -- Phase 6 validation
**Updated**: 2026-02-13

---

## Overview

C3 (Cognitive Layer 3) is the neural modelling subsystem of the MI pipeline. It contains 96 models organised into 9 cognitive units, each implementing biologically-grounded auditory processing with E/M/P/F output layers and BEP+ASA mechanisms.

**Pipeline position**: Audio --> Cochlea (128-mel) --> R3 (128D) --> H3 (sparse) --> **C3 (96 models)** --> Output

---

## Directory Structure

```
Docs/C3/
|-- 00-INDEX.md                     <-- You are here
|-- C3-ARCHITECTURE.md              Architecture overview
|
|-- Models/                         96 model specification docs (9 units)
|-- Units/                          9 cognitive unit summaries
|-- Mechanisms/                     10 neural mechanisms (BEP, ASA, PPC, ...)
|-- Pathways/                       5 cross-unit pathways
|-- Regions/                        3 brain region categories (26 regions)
|-- Neurochemicals/                 4 neurochemical systems
|-- Circuits/                       6 functional circuits
|-- Tiers/                          3 evidence tiers (Alpha, Beta, Gamma)
|-- Matrices/                       5 aggregate data matrices
|-- Contracts/                      8 interface contracts
```

---

## Key Documents

| Document | Purpose |
|----------|---------|
| [C3-ARCHITECTURE.md](C3-ARCHITECTURE.md) | Architecture overview, design rationale |
| [Tiers/00-INDEX.md](Tiers/00-INDEX.md) | Evidence tier breakdown (27/40/29) |
| [Matrices/00-INDEX.md](Matrices/00-INDEX.md) | Aggregate data matrices |
| [Mechanisms/00-INDEX.md](Mechanisms/00-INDEX.md) | Neural mechanism catalogue |

## Cross-References

| Related Document | Location |
|-----------------|----------|
| R3 spectral features | [R3/00-INDEX.md](../R3/00-INDEX.md) |
| H3 temporal demands | [H3/00-INDEX.md](../H3/00-INDEX.md) |
| C3 code | `mi_beta/brain/units/` (9 unit directories) |
