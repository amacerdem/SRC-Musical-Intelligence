"""Centralized path constants for the Validation infrastructure."""
from __future__ import annotations

from pathlib import Path

# ── Root paths ──
PROJECT_ROOT = Path("/Volumes/SRC-9/SRC Musical Intelligence")
VALIDATION_ROOT = PROJECT_ROOT / "Validation"
MI_ROOT = PROJECT_ROOT / "Musical_Intelligence"
TEST_AUDIO = PROJECT_ROOT / "Test-Audio"

# ── Dataset directories ──
DATASETS = VALIDATION_ROOT / "datasets"
DEAM_DIR = DATASETS / "deam"
NMED_T_DIR = DATASETS / "nmed_t"
OPENNEURO_EEG_FMRI_DIR = DATASETS / "openneuro_ds002725"
OPENNEURO_GENRE_FMRI_DIR = DATASETS / "openneuro_ds003720"
KRUMHANSL_DIR = DATASETS / "krumhansl"
IDYOM_DIR = DATASETS / "idyom_corpora"
PHARMA_DIR = DATASETS / "pharmacology"

# ── Output directories ──
RESULTS = VALIDATION_ROOT / "results"
FIGURES = VALIDATION_ROOT / "figures"

# ── Per-module result directories ──
V1_RESULTS = RESULTS / "v1_pharmacology"
V2_RESULTS = RESULTS / "v2_idyom"
V3_RESULTS = RESULTS / "v3_krumhansl"
V4_RESULTS = RESULTS / "v4_deam"
V5_RESULTS = RESULTS / "v5_eeg_encoding"
V6_RESULTS = RESULTS / "v6_fmri_encoding"
V7_RESULTS = RESULTS / "v7_rsa"


def ensure_dirs() -> None:
    """Create all output directories if they don't exist."""
    for d in (RESULTS, FIGURES, V1_RESULTS, V2_RESULTS, V3_RESULTS,
              V4_RESULTS, V5_RESULTS, V6_RESULTS, V7_RESULTS):
        d.mkdir(parents=True, exist_ok=True)
