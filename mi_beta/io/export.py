"""Export -- Save MI-Beta outputs to JSON or CSV."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Dict
from ..core.types import MIBetaOutput


def to_json(output: MIBetaOutput, path: str | Path) -> None:
    data: Dict = {
        "version": "mi_beta-0.1.0",
        "total_dim": output.total_dim,
        "sections": {
            "cochlea": list(output.cochlea_range),
            "r3": list(output.r3_range),
            "brain": list(output.brain_range),
        },
    }
    if output.brain is not None:
        data["brain"] = {
            "dim": output.brain.total_dim,
            "units": list(output.brain.unit_ranges.keys()),
        }
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def to_csv(output: MIBetaOutput, path: str | Path) -> None:
    tensor = output.mi_space.detach().cpu().squeeze(0)  # (T, D)
    header = ",".join(f"d{i}" for i in range(tensor.shape[-1]))
    lines = [header]
    for t in range(tensor.shape[0]):
        row = ",".join(f"{v:.6f}" for v in tensor[t].tolist())
        lines.append(row)
    Path(path).write_text("\n".join(lines))
