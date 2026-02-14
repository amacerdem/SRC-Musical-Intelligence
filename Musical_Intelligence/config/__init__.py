"""Configuration management -- Hydra YAML configs for MI-Core training.

Config structure::

    config/
    ├── config.yaml              # Root (composes all sub-configs)
    ├── model/
    │   ├── mi_core.yaml         # Full MI-Core architecture
    │   ├── backbone.yaml        # Mamba-2 + Sparse Attention
    │   └── experts.yaml         # MoE routing config
    ├── training/
    │   ├── default.yaml         # Optimizer, LR, batch size
    │   └── curriculum.yaml      # 5-phase weight schedule
    ├── data/
    │   └── default.yaml         # Dataset, preprocessing, augmentation
    └── evaluation/
        └── default.yaml         # Metrics, thresholds
"""
from __future__ import annotations
