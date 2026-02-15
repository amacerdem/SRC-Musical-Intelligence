"""MI WebLab — FastAPI backend.

Serves pre-computed experiment data and static registry information.

Usage:
    cd Lab/WebLab/server
    uvicorn app:app --port 8600 --reload
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI(title="MI WebLab", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

EXPERIMENTS_DIR = Path(__file__).resolve().parent.parent / "experiments"
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


# ──────────────────────────────────────────────────────
# Experiment endpoints
# ──────────────────────────────────────────────────────

@app.get("/api/experiments")
def list_experiments() -> list[str]:
    """List all experiment slugs."""
    if not EXPERIMENTS_DIR.exists():
        return []
    return sorted(
        d.name for d in EXPERIMENTS_DIR.iterdir()
        if d.is_dir() and (d / "meta.json").exists()
    )


def _exp_path(slug: str) -> Path:
    p = EXPERIMENTS_DIR / slug
    if not p.exists():
        raise HTTPException(404, f"Experiment '{slug}' not found")
    return p


def _read_json(path: Path) -> dict | list:
    if not path.exists():
        raise HTTPException(404, f"File not found: {path.name}")
    return json.loads(path.read_text())


@app.get("/api/experiments/{slug}/meta")
def get_meta(slug: str):
    return _read_json(_exp_path(slug) / "meta.json")


@app.get("/api/experiments/{slug}/audio")
def get_audio(slug: str):
    p = _exp_path(slug) / "audio.wav"
    if not p.exists():
        raise HTTPException(404, "Audio file not found")
    return FileResponse(p, media_type="audio/wav")


@app.get("/api/experiments/{slug}/r3")
def get_r3(slug: str):
    return _read_json(_exp_path(slug) / "r3.json")


@app.get("/api/experiments/{slug}/nuclei/{name}")
def get_nucleus(slug: str, name: str):
    p = _exp_path(slug) / "nuclei" / f"{name}.json"
    return _read_json(p)


@app.get("/api/experiments/{slug}/ram")
def get_ram(slug: str):
    return _read_json(_exp_path(slug) / "ram.json")


@app.get("/api/experiments/{slug}/neuro")
def get_neuro(slug: str):
    return _read_json(_exp_path(slug) / "neuro.json")


@app.get("/api/experiments/{slug}/psi")
def get_psi(slug: str):
    return _read_json(_exp_path(slug) / "psi.json")


@app.get("/api/experiments/{slug}/h3")
def get_h3(slug: str):
    return _read_json(_exp_path(slug) / "h3.json")


# ──────────────────────────────────────────────────────
# Registry endpoints (static data from MI codebase)
# ──────────────────────────────────────────────────────

@app.get("/api/registry/r3")
def get_r3_registry():
    """R³ group boundaries and feature names."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))
    from Musical_Intelligence.ear.r3.constants.group_boundaries import R3_GROUP_BOUNDARIES
    from Musical_Intelligence.ear.r3.constants.feature_names import R3_FEATURE_NAMES

    return {
        "groups": [
            {
                "letter": g.letter,
                "name": g.name,
                "start": g.start,
                "end": g.end,
                "dim": g.dim,
                "stage": g.stage,
            }
            for g in R3_GROUP_BOUNDARIES
        ],
        "feature_names": list(R3_FEATURE_NAMES),
    }


@app.get("/api/registry/regions")
def get_regions_registry():
    """26 brain regions with MNI coordinates."""
    import sys
    sys.path.insert(0, str(PROJECT_ROOT))
    from Musical_Intelligence.brain.regions import ALL_REGIONS

    return [
        {
            "index": r.index,
            "name": r.name,
            "abbreviation": r.abbreviation,
            "hemisphere": r.hemisphere,
            "mni_coords": list(r.mni_coords),
            "brodmann_area": r.brodmann_area,
            "group": r.group,
        }
        for r in ALL_REGIONS
    ]
