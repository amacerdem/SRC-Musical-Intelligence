# C³ Cross-Unit Pathways — Index

## Overview

Pathways route signals between units during the two-pass execution model. Independent units (SPU, STU, IMU, ASU, NDU, MPU, PCU) compute first in Phase 2. The `PathwayRunner` then extracts cross-unit signals from their outputs. Finally, dependent units (ARU, RPU) receive routed inputs in Phase 4.

Each pathway is a `CrossUnitPathway` declaration specifying a directed data dependency from a source model in one unit to a target model in another (or the same) unit. Pathways do not carry data — they declare the contract that a source model promises to fulfill and a target model depends on.

## Pathway Catalogue

| pathway_id | Name | Source Unit | Target Unit | Correlation | Citation |
|------------|------|-------------|-------------|-------------|----------|
| P1_SPU_ARU | SPU -> ARU (consonance -> pleasure) | SPU | ARU | r=0.81 | Bidelman 2009 |
| P2_STU_INTERNAL | STU internal (beat -> motor sync) | STU | STU | r=0.70 | Grahn & Brett 2007 |
| P3_IMU_ARU | IMU -> ARU (memory -> affect) | IMU | ARU | r=0.55 | Janata 2009 |
| P4_STU_INTERNAL | STU internal (context -> prediction) | STU | STU | r=0.99 | Mischler 2025 |
| P5_STU_ARU | STU -> ARU (tempo -> emotion) | STU | ARU | r=0.60 | Juslin & Vastfjall 2008 |

## Routing Flow

```
Phase 2: Independent Units Compute
┌──────────────────────────────────────────────────────┐
│  SPU ──────────┐                                     │
│  STU ──────────┤──(unit_outputs)──> PathwayRunner    │
│  IMU ──────────┤                         │           │
│  ASU ──────────┤                         │           │
│  NDU ──────────┤                         ▼           │
│  MPU ──────────┤                  route(outputs)     │
│  PCU ──────────┘                         │           │
└──────────────────────────────────────────│───────────┘
                                           │
                        cross_unit_inputs = {pathway_id: tensor}
                                           │
Phase 4: Dependent Units Receive           ▼
┌──────────────────────────────────────────────────────┐
│  ARU  <── P1_SPU_ARU, P3_IMU_ARU, P5_STU_ARU        │
│  RPU  <── (reads ARU outputs via CROSS_UNIT_READS)   │
└──────────────────────────────────────────────────────┘
```

## Inter-Unit vs Intra-Unit Pathways

**Inter-unit pathways** cross unit boundaries. They create execution-order dependencies — the source unit must complete before the target unit can begin. These enforce the two-pass architecture: independent units first, dependent units second.

| Pathway | Type |
|---------|------|
| P1_SPU_ARU | Inter-unit (SPU -> ARU) |
| P3_IMU_ARU | Inter-unit (IMU -> ARU) |
| P5_STU_ARU | Inter-unit (STU -> ARU) |

**Intra-unit pathways** route signals within the same unit. They express model-to-model dependencies within a single unit's computation graph but do not affect unit-level execution order.

| Pathway | Type |
|---------|------|
| P2_STU_INTERNAL | Intra-unit (STU -> STU) |
| P4_STU_INTERNAL | Intra-unit (STU -> STU) |

## RPU Cross-Unit Dependencies

RPU models declare `CROSS_UNIT_READS = ("ARU",)`, meaning they read ARU outputs after ARU has completed. This creates the dependency chain:

```
Independent units -> PathwayRunner -> ARU -> RPU
```

RPU models with ARU dependency: DAED, MORMR, RPEM, IUCP, MCCN, MEAMR, LDAC, IOTMS, SSPS.

## Code Reference

- Pathway contract: `mi_beta/contracts/pathway_spec.py`
- Pathway declarations: `mi_beta/brain/pathways/p{1-5}_*.py`
- Runner: `mi_beta/brain/pathways/__init__.py`
