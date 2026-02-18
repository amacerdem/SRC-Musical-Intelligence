"""RAM — Region Activation Map assembler for C³ Kernel v3.1.

Aggregates relay P-layer outputs into a 26-dimensional brain region
activation map.  Each relay dimension is mapped to brain regions via
the relay's region_links ontology.

Pipeline: Σ(relay_dim × link_weight) → ReLU → z-normalize → sigmoid → [0,1]

The RAM is non-computational — it does NOT affect beliefs or reward.
It provides spatial brain output for visualization and the HYBRID layer.

Literature: Naselaris et al. 2011, Huth et al. 2016.
"""
from __future__ import annotations

from typing import Any, Dict, Tuple

import torch
from torch import Tensor


# ======================================================================
# 26 brain regions (from Musical_Intelligence/brain/regions/registry.py)
# ======================================================================

REGIONS: Tuple[str, ...] = (
    # Cortical (0-11)
    "A1_HG", "STG", "STS", "IFG", "dlPFC", "vmPFC", "OFC", "ACC",
    "SMA", "PMC", "AG", "TP",
    # Subcortical (12-20)
    "VTA", "NAcc", "caudate", "amygdala", "hippocampus", "putamen",
    "MGB", "hypothalamus", "insula",
    # Brainstem (21-25)
    "IC", "AN", "CN", "SOC", "PAG",
)

REGION_TO_IDX: Dict[str, int] = {r: i for i, r in enumerate(REGIONS)}
NUM_REGIONS: int = len(REGIONS)


# ======================================================================
# Static region link table
# ======================================================================
# Maps (wrapper_name, field_name) → {region_name: link_weight}.
# Derived from each relay's region_links ontology property.
# Non-standard region names mapped to closest registry equivalents:
#   MTG → STS, dACC → ACC, Medial_HG/Anterolateral_HG → A1_HG,
#   Planum_Temporale/Planum_Polare → STG, R_STG → STG.

REGION_LINK_TABLE: Dict[Tuple[str, str], Dict[str, float]] = {
    # ── BCH (Brainstem Consonance Hierarchy, SPU) ─────────────────
    ("BCH", "hierarchy"): {"IC": 0.85},
    ("BCH", "consonance_signal"): {"MGB": 0.6, "STG": 0.4},
    # template_match: no region_links in relay

    # ── HMCE (Hierarchical Musical Context Encoding, STU) ─────────
    ("HMCE", "a1_encoding"): {"A1_HG": 0.85},
    ("HMCE", "stg_encoding"): {"STG": 0.80},
    ("HMCE", "mtg_encoding"): {"STS": 0.75},       # MTG → STS
    ("HMCE", "context_prediction"): {"hippocampus": 0.50},
    ("HMCE", "structure_predict"): {"IFG": 0.60},
    # phrase_expect: no region_links in relay

    # ── SNEM (Steady-State Evoked Potential Monitor, ASU) ─────────
    ("SNEM", "beat_locked_activity"): {"SMA": 0.80},
    ("SNEM", "entrainment_strength"): {"putamen": 0.85},
    ("SNEM", "selective_gain"): {"ACC": 0.50},      # dACC → ACC
    ("SNEM", "beat_onset_pred"): {"PMC": 0.60},
    # meter_position_pred, enhancement_pred: no region_links

    # ── MMP (Musical Mnemonic Preservation, IMU) ──────────────────
    ("MMP", "recognition_state"): {"SMA": 0.90},
    ("MMP", "melodic_identity"): {"STG": 0.70},
    ("MMP", "familiarity_level"): {"hippocampus": 0.50},
    ("MMP", "emotional_forecast"): {"amygdala": 0.60},
    ("MMP", "scaffold_forecast"): {"ACC": 0.80},
    # recognition_forecast: no region_links

    # ── DAED (Dopamine Anticipation-Experience Dissociation, RPU) ──
    ("DAED", "wanting_index"): {"amygdala": 0.60, "hippocampus": 0.40},
    ("DAED", "liking_index"): {"putamen": 0.60, "OFC": 0.70},
    ("DAED", "caudate_activation"): {"caudate": 0.85},
    ("DAED", "nacc_activation"): {"NAcc": 0.85},

    # ── MPG (Melodic Processing Gradient, NDU) ────────────────────
    ("MPG", "onset_state"): {"STG": 0.60},          # Planum_Temporale → STG
    ("MPG", "contour_state"): {"STG": 0.70},        # Planum_Polare → STG
    # phrase_boundary_pred: no region_links
}


# ======================================================================
# RAM assembly function
# ======================================================================

def assemble_ram(
    relay_outputs: Dict[str, Any],
    B: int,
    T: int,
    device: torch.device,
) -> Tensor:
    """Assemble 26D RAM from relay wrapper outputs.

    For each approved relay output dimension, looks up region_links
    and accumulates: ``ram[region] += output_value × link_weight``.

    Pipeline: accumulate → ReLU → z-normalize → sigmoid → (B, T, 26).

    For single-frame mode (T=1), z-normalization yields all zeros
    (std=0 → z=0), and sigmoid maps to 0.5 (neutral activation).
    This is correct: one frame gives no temporal context for relative
    activation.

    Args:
        relay_outputs: ``{wrapper_name: wrapper_output_dataclass}``.
        B: Batch size.
        T: Temporal frames.
        device: Torch device.

    Returns:
        RAM tensor of shape ``(B, T, 26)`` in [0, 1].
    """
    ram = torch.zeros(B, T, NUM_REGIONS, device=device)

    for (wrapper_name, field_name), links in REGION_LINK_TABLE.items():
        wrapper_out = relay_outputs.get(wrapper_name)
        if wrapper_out is None:
            continue

        value = getattr(wrapper_out, field_name, None)
        if value is None:
            continue

        # value is (B, T) — accumulate into region slots
        for region_name, weight in links.items():
            idx = REGION_TO_IDX.get(region_name)
            if idx is not None:
                ram[..., idx] = ram[..., idx] + weight * value

    # Pipeline: ReLU → z-normalize → sigmoid
    ram = torch.relu(ram)

    # Z-normalize per region across time
    # For T=1: std is undefined (0 dof) → skip normalization → sigmoid(ReLU) ∈ [0.5, 1)
    if T > 1:
        ram_mean = ram.mean(dim=1, keepdim=True)
        ram_std = ram.std(dim=1, keepdim=True, correction=0).clamp(min=1e-6)
        ram = (ram - ram_mean) / ram_std

    # Sigmoid to [0, 1]
    ram = torch.sigmoid(ram)

    return ram
