# Building: 96-Model Cognitive Architecture Build System

## Philosophy

Each of the 96 C³ cognitive models must be a **self-documenting scientific artifact**. Reading only the code — never the markdown doc — a researcher must be able to:

- Follow the complete neural circuit and scientific basis
- See every citation with author, year, finding, and effect size
- Understand which brain regions are involved and why
- Trace every computation back to a specific paper
- Know the falsification criteria and cross-unit pathways

The markdown docs (`Docs/C³/Models/`) are the **design specifications**.
The Python code (`Musical_Intelligence/brain/units/`) is the **living reference**.

## Target: ~700-800 lines per model

| Section | Skeleton (before) | Built (after) |
|---------|-------------------|---------------|
| Class docstring | 2 lines | ~40 lines (full neural circuit) |
| Constants | 0 | ~10 (each citing source paper) |
| LAYERS | generic names | semantic names from doc Section 6 |
| h3_demand | 4 generic tuples | 12-20 specific H3DemandSpec |
| brain_regions | 3 generic | 4-6 with MNI coords + evidence |
| citations | 1 placeholder | 13+ real papers with findings |
| compute() | 20 lines generic | ~150-200 lines with inline science |
| **Total** | **~119 lines** | **~700-800 lines** |

## Quick Start

1. Check today's target: `Building/queue/BACKLOG.md`
2. Follow the process: `Building/checklists/MODEL-BUILD.md`
3. Update progress: `Building/progress/TRACKER.md`
4. Log the day: `Building/progress/DAILY-LOG.md`

## Gold Standard Reference

**BCH** (`Musical_Intelligence/brain/units/spu/models/bch.py`) is the exemplar.
Every other model follows its pattern for depth, structure, and scientific rigor.

## Build Order

7 phases, 96 models. See `Building/queue/BACKLOG.md` for the full sequence.

| Phase | Unit(s) | Models | Dependencies |
|-------|---------|--------|--------------|
| 1 | SPU | 9 | Independent |
| 2 | STU | 14 | Independent |
| 3 | IMU | 15 | Independent |
| 4 | ASU + NDU | 18 | Independent |
| 5 | MPU + PCU | 20 | Independent |
| 6 | ARU | 10 | P1(SPU), P3(IMU), P5(STU) |
| 7 | RPU | 10 | ARU |
