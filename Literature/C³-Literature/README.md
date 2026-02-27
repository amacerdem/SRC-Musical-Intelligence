# C³-Literature

## Research Literature Database for Cognitive Consonance Circuit

[![Papers](https://img.shields.io/badge/PDFs-387-blue.svg)]()
[![Extractions](https://img.shields.io/badge/Extractions-448-brightgreen.svg)]()
[![Claims](https://img.shields.io/badge/Claims-1116-orange.svg)]()
[![License](https://img.shields.io/badge/license-Research_Only-blueviolet.svg)](../LICENSE)

---

> **Comprehensive literature foundation** — 448 peer-reviewed studies organized by 9 cognitive units

---

## 📊 Database Statistics

| Metric | Value |
|--------|-------|
| **Total PDFs** | 387 |
| **Total Extractions** | 448 |
| **Markdown Summaries** | 389 |
| **Empirical Claims** | 1,116 |
| **Effect Sizes** | 634 |
| **Unique Brain Regions** | 540 |

---

## 📁 Structure

```
C³-Literature/
├── C³-Collected/                    # Central repository
│   ├── PDF/                         # All PDFs (387 files)
│   └── MD/                          # Markdown summaries (389 files)
├── C³-STU-Cognitive-Timing/         # 104 papers
├── C³-SPU-Spectral-Representations/ # 46 papers
├── C³-IMU-Integration-Relational/   # 213 papers
├── C³-ARU-Affect/                   # 42 papers
├── C³-ASU-Salience-Attention/       # 7 papers
├── C³-MPU-Prediction-Interpretation/# 21 papers
├── C³-PCU-Inference-Expectation/    # 6 papers
├── C³-RPU-Reward-Valence/           # 6 papers
├── C³-NDU-Novelty-Surprise/         # 3 papers
└── paper_database.json              # Master index
```

---

## 🧠 C³ Cognitive Units

### Core-4 VALIDATED (k ≥ 10, Meta-Analyzed)

| Unit | Full Name | Papers | k | Pooled d | Focus Areas |
|------|-----------|-------:|---:|----------|-------------|
| **SPU** | Spectral Processing | 46 | 13 | 0.84 | Pitch, consonance, Heschl's gyrus, tonotopy |
| **STU** | Sensorimotor Timing | 104 | 60 | 0.67 | Beat entrainment, rhythm, motor cortex, PLV |
| **IMU** | Integrative Memory | 213 | 60 | 0.53 | Hippocampus, mPFC, autobiographical memory |
| **ARU** | Affective Resonance | 42 | 16 | 0.83 | NAcc, VTA, dopamine, hedonic evaluation |

### Experimental-5 (k < 10, Descriptive)

| Unit | Full Name | Papers | Mean d | Focus Areas |
|------|-----------|-------:|--------|-------------|
| **ASU** | Auditory Salience | 7 | 1.62 | Bottom-up attention, N1/P2 responses |
| **MPU** | Motor Planning | 21 | 1.19 | SMA, cerebellum, beta rebound, imagery |
| **PCU** | Predictive Coding | 6 | 0.24 | P3 responses, schema matching |
| **RPU** | Reward Prediction | 6 | 1.81 | Dopamine, nucleus accumbens |
| **NDU** | Novelty Detection | 3 | -0.07 | MMN responses, expectation violation |

---

## 🔬 V3.0 Extraction Schema

Each paper extraction follows the standardized V3.0 JSON schema:

```json
{
  "paper_id": "koelsch_2014_brain_correlates",
  "doi": "10.1016/j.neubiorev.2014.02.005",
  "c3_units": ["ARU", "IMU"],
  "claims": [
    {
      "claim_id": "C001",
      "text": "Music-evoked chills correlate with NAcc activation",
      "evidence_tier": "α",
      "effect_size": {"d": 0.84, "ci_lower": 0.61, "ci_upper": 1.05},
      "brain_regions": ["NAcc", "VTA"],
      "r3_dimensions": ["L8.pleasure", "L5.chroma_salience"]
    }
  ]
}
```

---

## 📖 Usage

### Adding New Papers

1. Copy PDFs to `C³-Collected/PDF/`
2. Copy MD summaries to `C³-Collected/MD/`
3. Run reorganization:

```bash
python reorganize_by_units.py
```

### Querying the Database

```python
import json

with open('paper_database.json') as f:
    db = json.load(f)

# Find all ARU papers
aru_papers = [p for p in db if 'ARU' in p['c3_units']]
print(f"ARU papers: {len(aru_papers)}")

# Find papers with effect sizes > 0.8
high_effect = [p for p in db if any(
    c.get('effect_size', {}).get('d', 0) > 0.8 
    for c in p.get('claims', [])
)]
```

---

## 🗂️ Legacy Category Mapping

Previous category folders are preserved for reference:

| Legacy Category | → Maps To |
|-----------------|-----------|
| C³-I-Harmonic-Perception | **SPU** |
| C³-II-Timbre-Spectral | **SPU** |
| C³-III-Rhythm-Motor | **STU**, **MPU** |
| C³-IV-Expectation-Surprise | **PCU**, **NDU** |
| C³-V-Emotion-Reward | **RPU**, **ARU** |
| C³-VI-Memory-Imagery | **IMU**, **MPU** |
| C³-VII-Melody-Form | **IMU**, **PCU** |
| C³-VIII-Microtonality | **SPU** |
| C³-IX-Empathy-Simulation | **ARU**, **IMU** |
| C³-X-EEG-BCI | **NDU**, **PCU** |
| C³-XI-Integrative | **IMU** |
| C³-XII-Amplitude-BCI | **ASU**, **NDU** |

---

## 📚 Related Resources

| Resource | Location |
|----------|----------|
| **C³ Meta-Theory** | `../C³-Meta-Theory/` |
| **C³ Meta-Analysis** | `../C³-Meta-Analysis/` |
| **C³ Engine** | `../C³-Engine/` |
| **R³ Literature** | `../../R³-Resonance-Based-Realational-Reasoning/R³-Literature/` |

---

## 👤 Author

**Amaç Erdem** — Composer, Researcher, Interactive Media Artist

| | |
|---|---|
| **Education** | M.M. Composition (Boston University) · B.M. Composition & Conducting |
| **Self-Taught** | Neuroscience, Mathematics, Software Engineering — *no formal training* |
| **Project Started** | April 1, 2025 |

---

## 📄 License

**SRC⁹ Source-Available Research License**  
Copyright © 2024-2026 Amaç Erdem. All Rights Reserved.

---

*C³-Literature — The evidence foundation for music cognition research* 📚🧠

*Project Started: April 1, 2025 | Last Updated: January 2026 | Version: 2.0.0*
