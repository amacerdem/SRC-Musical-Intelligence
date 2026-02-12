"""
Export — Save MI outputs to JSON or CSV.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

import torch

from ..core.types import MIOutput


def to_json(output: MIOutput, path: str | Path) -> None:
    """Export MI output to JSON."""
    data: Dict = {}

    # Brain (26D)
    brain = output.brain
    tensor = brain.tensor.detach().cpu()
    data["brain"] = {
        "dimensions": list(brain.dimension_names),
        "shape": list(tensor.shape),
        "values": tensor.squeeze(0).tolist(),
    }

    # Semantics (104D)
    if output.semantics is not None:
        sem = output.semantics
        data["semantics"] = {
            "model": sem.model_name,
            "total_dim": sem.total_dim,
            "shape": list(sem.tensor.shape),
            "groups": {},
        }
        for group_name, group in sem.groups.items():
            data["semantics"]["groups"][group_name] = {
                "dimensions": list(group.dimension_names),
                "dim": group.tensor.shape[-1],
            }

    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def to_csv(output: MIOutput, path: str | Path) -> None:
    """Export MI output to CSV (one row per frame)."""
    brain = output.brain
    tensor = brain.tensor.detach().cpu().squeeze(0)  # (T, D)
    header = ",".join(brain.dimension_names)
    lines = [header]
    for t in range(tensor.shape[0]):
        row = ",".join(f"{v:.6f}" for v in tensor[t].tolist())
        lines.append(row)

    csv_path = Path(path)
    csv_path.write_text("\n".join(lines))
