# Literature — Musical Intelligence Ground Truth

This directory contains the scientific literature foundation for Musical Intelligence.
It is organized for efficient access by AI agents building C³ cognitive models and R³ spectral features.

## Directory Structure

```
Literature/
├── CATALOG.md              # Master index with statistics and full paper list
├── catalog.json            # Machine-readable structured index
├── README.md               # This file
│
├── c3/                     # C³ Cognitive Neuroscience Literature
│   ├── papers/             # Unique PDFs (one copy per paper)
│   ├── summaries/          # Markdown summaries (AI-extracted)
│   └── extractions/        # JSON extractions (v3.0 schema, structured claims)
│
└── r3/                     # R³ Spectral / Music Theory / DSP Literature
    ├── psychoacoustics/          # Consonance, dissonance, pitch, tuning, JI
    ├── computational-music-theory/  # Neo-Riemannian, geometry, group theory
    ├── spectral-music/           # Spectral composition techniques
    ├── dsp-and-ml/               # Genre classification, spectral features
    └── music-theory-analysis/    # Serial music, set theory, general analysis
```

## How to Use (AI Agent Guide)

### Find papers by C³ cognitive unit
```bash
# In catalog.json, search by unit tag
grep '"ARU"' catalog.json

# Or search CATALOG.md for the unit section
grep -A 50 "### ARU" CATALOG.md
```

### Find papers by R³ category
```bash
# List all computational music theory papers
ls r3/computational-music-theory/

# Search catalog for category
grep '"psychoacoustics"' catalog.json
```

### Find papers by keyword
```bash
# Search all summaries for a topic
grep -rl "dopamine" c3/summaries/

# Search all R³ literature
grep -rl "consonance" r3/
```

### JSON Extraction Schema (v3.0)
Structured extractions in `c3/extractions/` contain:
- `metadata`: Paper info, DOI, authors, year
- `claims[]`: Scientific findings with effect sizes, brain regions, statistics
- `c3_associations[]`: Links to cognitive units with confidence scores
- `r3_coordinates`: Mappings to R³ ontology dimensions (L0-L9)
- `brain_regions_summary`: MNI coordinates, Brodmann areas
- `validation`: Schema compliance and data quality metrics

### Cross-referencing
Papers may be relevant to multiple C³ units. The `catalog.json` `units[]` field
lists ALL relevant units for each paper. Physical files exist in ONE location only —
use catalog metadata for cross-unit queries.

## Key Numbers
See CATALOG.md for current statistics (paper counts per unit, per category, format coverage).

---
*Reorganized: 2026-02-12*
