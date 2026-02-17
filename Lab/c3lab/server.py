"""C3 WebLab — Live Belief Annotation Server.

FastAPI backend for interactive C3 belief visualization + annotation.
Serves Alpha-Test traces, audio files, and manages annotations.

Usage:
    cd Lab/c3lab
    uvicorn server:app --port 5555 --reload
"""
from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# ── Paths ─────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
RESULTS_DIR = PROJECT_ROOT / "Lab" / "experiments" / "Alpha-Test" / "results"
AUDIO_DIR = PROJECT_ROOT / "Test-Audio"
ANNOTATIONS_DIR = Path(__file__).resolve().parent / "annotations"
EXPORTS_DIR = Path(__file__).resolve().parent / "exports"

ANNOTATIONS_DIR.mkdir(exist_ok=True)
EXPORTS_DIR.mkdir(exist_ok=True)

# ── Piece registry ────────────────────────────────────────────────
# Maps piece slug → (result JSON filename, audio filename)
PIECE_REGISTRY: Dict[str, Dict[str, str]] = {
    "swan_lake": {
        "result": "Swan_Lake.json",
        "audio": "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky.wav",
        "title": "Swan Lake — Tchaikovsky",
    },
    "bach_cello": {
        "result": "Bach_Cello_Suite.json",
        "audio": "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav",
        "title": "Cello Suite No. 1 — Bach",
    },
    "herald": {
        "result": "Herald_of_the_Change.json",
        "audio": "Herald of the Change - Hans Zimmer.wav",
        "title": "Herald of the Change — Zimmer",
    },
    "beethoven": {
        "result": "Beethoven_Pathetique.json",
        "audio": "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav",
        "title": "Pathétique Sonata — Beethoven",
    },
}

# ── Annotation schema (3-layer) ───────────────────────────────────
#
# Layer 1 — EVENTS: "Something is happening in the music here"
#   category → sub-type.  Always a time RANGE.
#
# Layer 2 — JUDGMENTS: "The system output for X is (agree/wrong/unsure)"
#   target output + judgment enum.  Always a time RANGE.
#
# Layer 3 — QUESTIONS: "Why / What / How is this happening?"
#   Free-form question about what the system does or what the music does.
#   Optional target output.  Always a time RANGE.
#

LAYER1_EVENTS = {
    "HARMONIC_CHANGE": {
        "label": "Harmonic Change", "color": "#58A6FF",
        "parent": "IMPORTANT_CHANGE",
    },
    "RHYTHMIC_CHANGE": {
        "label": "Rhythmic Change", "color": "#3FB950",
        "parent": "IMPORTANT_CHANGE",
    },
    "TEXTURAL_CHANGE": {
        "label": "Textural Change", "color": "#D29922",
        "parent": "IMPORTANT_CHANGE",
    },
    "DYNAMIC_CHANGE": {
        "label": "Dynamic Change", "color": "#BC8CFF",
        "parent": "IMPORTANT_CHANGE",
    },
    "TIMBRAL_CHANGE": {
        "label": "Timbral Change", "color": "#F778BA",
        "parent": "IMPORTANT_CHANGE",
    },
    "STRUCTURAL_BOUNDARY": {
        "label": "Structural Boundary", "color": "#79C0FF",
        "parent": "IMPORTANT_CHANGE",
    },
    "ONSET_ATTACK": {
        "label": "Onset / Attack", "color": "#F0883E",
        "parent": "IMPORTANT_CHANGE",
    },
    "TRANSITION": {
        "label": "Transition / Bridge", "color": "#A5D6FF",
        "parent": "IMPORTANT_CHANGE",
    },
    "TENSION_BUILD": {
        "label": "Tension Build", "color": "#F85149",
        "parent": "TENSION",
    },
    "TENSION_RELEASE": {
        "label": "Tension Release", "color": "#56D364",
        "parent": "TENSION",
    },
    "MONOTONOUS_REGION": {
        "label": "Monotonous Region", "color": "#484F58",
        "parent": "OTHER",
    },
    "HIGH_ENERGY": {
        "label": "High Energy", "color": "#FF7B72",
        "parent": "OTHER",
    },
    "CALM_REST": {
        "label": "Calm / Rest", "color": "#7EE787",
        "parent": "OTHER",
    },
}

# System outputs that Layer 2 can target
LAYER2_OUTPUTS = [
    {"id": "consonance", "label": "Consonance", "color": "#58A6FF"},
    {"id": "tempo", "label": "Tempo", "color": "#3FB950"},
    {"id": "salience", "label": "Salience", "color": "#D29922"},
    {"id": "familiarity", "label": "Familiarity", "color": "#BC8CFF"},
    {"id": "reward", "label": "Reward", "color": "#F78166"},
    {"id": "pe_consonance", "label": "|PE| Consonance", "color": "#58A6FF"},
    {"id": "pe_tempo", "label": "|PE| Tempo", "color": "#3FB950"},
    {"id": "pe_salience", "label": "|PE| Salience", "color": "#D29922"},
    {"id": "pe_familiarity", "label": "|PE| Familiarity", "color": "#BC8CFF"},
    {"id": "precision_consonance", "label": "Precision Cons", "color": "#58A6FF"},
    {"id": "precision_tempo", "label": "Precision Tempo", "color": "#3FB950"},
]

LAYER2_JUDGMENTS = [
    {"id": "AGREE", "label": "This is how I feel", "color": "#3FB950"},
    {"id": "COUNTER_INTUITIVE", "label": "Counter-intuitive (might be true)", "color": "#D29922"},
    {"id": "WRONG", "label": "Definitely not right", "color": "#F85149"},
]

# Layer 3 — QUESTIONS about the music or the system
LAYER3_CATEGORIES = [
    {"id": "WHY", "label": "Why?", "color": "#79C0FF",
     "hint": "Why does X happen here?"},
    {"id": "WHAT", "label": "What?", "color": "#D2A8FF",
     "hint": "What is causing this?"},
    {"id": "HOW", "label": "How?", "color": "#7EE787",
     "hint": "How does the system compute this?"},
    {"id": "BUG", "label": "Bug?", "color": "#F85149",
     "hint": "Is this a bug or expected?"},
]

# ── C3 kernel parameters (tunable) ───────────────────────────────
KERNEL_PARAMS = {
    "beliefs": {
        "consonance_tau": {"value": 0.3, "min": 0.01, "max": 0.99, "step": 0.05,
                           "label": "Consonance tau", "unit": "SPU"},
        "tempo_tau": {"value": 0.7, "min": 0.01, "max": 0.99, "step": 0.05,
                      "label": "Tempo tau", "unit": "STU"},
        "salience_tau": {"value": 0.3, "min": 0.01, "max": 0.99, "step": 0.05,
                         "label": "Salience tau", "unit": "ASU"},
        "familiarity_tau": {"value": 0.85, "min": 0.01, "max": 0.99, "step": 0.05,
                            "label": "Familiarity tau", "unit": "IMU"},
        "reward_tau": {"value": 0.8, "min": 0.01, "max": 0.99, "step": 0.05,
                       "label": "Reward tau", "unit": "ARU"},
    },
    "reward": {
        "w_surprise": {"value": 1.0, "min": 0.0, "max": 3.0, "step": 0.1,
                        "label": "Surprise weight"},
        "w_resolution": {"value": 1.2, "min": 0.0, "max": 3.0, "step": 0.1,
                          "label": "Resolution weight"},
        "w_exploration": {"value": 0.3, "min": 0.0, "max": 3.0, "step": 0.1,
                           "label": "Exploration weight"},
        "w_monotony": {"value": 0.8, "min": 0.0, "max": 3.0, "step": 0.1,
                        "label": "Monotony weight"},
        "precision_scale": {"value": 12.0, "min": 1.0, "max": 30.0, "step": 1.0,
                             "label": "Precision scale (tanh)"},
    },
    "predict": {
        "cons_w_trend": {"value": 0.15, "min": 0.0, "max": 1.0, "step": 0.05,
                          "label": "Consonance trend weight"},
        "cons_w_period": {"value": 0.10, "min": 0.0, "max": 1.0, "step": 0.05,
                           "label": "Consonance period weight"},
        "tempo_w_trend": {"value": 0.20, "min": 0.0, "max": 1.0, "step": 0.05,
                           "label": "Tempo trend weight"},
        "tempo_w_period": {"value": 0.25, "min": 0.0, "max": 1.0, "step": 0.05,
                            "label": "Tempo period weight"},
        "fam_w_trend": {"value": 0.10, "min": 0.0, "max": 1.0, "step": 0.05,
                         "label": "Familiarity trend weight"},
    },
}


# ── Pydantic models ───────────────────────────────────────────────

class AnnotationCreate(BaseModel):
    piece: str
    layer: int                          # 1 = event, 2 = judgment, 3 = question
    time_start: float
    time_end: float                     # always a range (all layers)
    # Layer 1 fields
    event_type: Optional[str] = None    # e.g. "HARMONIC_CHANGE"
    # Layer 2 fields
    output_id: Optional[str] = None     # e.g. "consonance", "pe_tempo"
    judgment: Optional[str] = None      # "AGREE" / "COUNTER_INTUITIVE" / "WRONG"
    # Layer 3 fields
    question_category: Optional[str] = None  # "WHY" / "WHAT" / "HOW" / "BUG"
    question_text: Optional[str] = None      # free-form question
    # Shared
    text: str = ""
    severity: int = 3                   # 1-5


class AnnotationUpdate(BaseModel):
    time_start: Optional[float] = None
    time_end: Optional[float] = None
    event_type: Optional[str] = None
    output_id: Optional[str] = None
    judgment: Optional[str] = None
    question_category: Optional[str] = None
    question_text: Optional[str] = None
    text: Optional[str] = None
    severity: Optional[int] = None


class ParamUpdate(BaseModel):
    group: str
    key: str
    value: float


# ── App ───────────────────────────────────────────────────────────

app = FastAPI(title="C3 WebLab", version="0.1.0")

# Static files and templates
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


# ── Helper: load/save annotations ─────────────────────────────────

def _annotations_path(piece: str) -> Path:
    return ANNOTATIONS_DIR / f"{piece}.json"


def _load_annotations(piece: str) -> List[Dict[str, Any]]:
    path = _annotations_path(piece)
    if path.exists():
        with open(path) as f:
            return json.load(f)
    return []


def _save_annotations(piece: str, annotations: List[Dict[str, Any]]) -> None:
    with open(_annotations_path(piece), "w") as f:
        json.dump(annotations, f, indent=2)


# ── Routes ────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/pieces")
async def list_pieces():
    """List available pieces with metadata."""
    pieces = []
    for slug, info in PIECE_REGISTRY.items():
        result_path = RESULTS_DIR / info["result"]
        has_result = result_path.exists()
        has_audio = (AUDIO_DIR / info["audio"]).exists()
        duration = None
        if has_result:
            with open(result_path) as f:
                data = json.load(f)
                duration = data.get("summary", {}).get("duration_s")
        pieces.append({
            "slug": slug,
            "title": info["title"],
            "has_result": has_result,
            "has_audio": has_audio,
            "duration_s": duration,
        })
    return pieces


@app.get("/api/traces/{piece}")
async def get_traces(piece: str):
    """Return full C3 trace data for a piece."""
    if piece not in PIECE_REGISTRY:
        raise HTTPException(404, f"Unknown piece: {piece}")
    result_path = RESULTS_DIR / PIECE_REGISTRY[piece]["result"]
    if not result_path.exists():
        raise HTTPException(404, f"No results for: {piece}")
    with open(result_path) as f:
        return json.load(f)


@app.get("/api/audio/{piece}")
async def get_audio(piece: str):
    """Serve audio WAV file for a piece."""
    if piece not in PIECE_REGISTRY:
        raise HTTPException(404, f"Unknown piece: {piece}")
    audio_path = AUDIO_DIR / PIECE_REGISTRY[piece]["audio"]
    if not audio_path.exists():
        raise HTTPException(404, f"Audio not found for: {piece}")
    return FileResponse(
        audio_path,
        media_type="audio/wav",
        headers={"Accept-Ranges": "bytes"},
    )


@app.get("/api/annotation-schema")
async def get_annotation_schema():
    """Return the 3-layer annotation schema."""
    return {
        "layer1_events": LAYER1_EVENTS,
        "layer2_outputs": LAYER2_OUTPUTS,
        "layer2_judgments": LAYER2_JUDGMENTS,
        "layer3_categories": LAYER3_CATEGORIES,
    }


@app.get("/api/annotations/{piece}")
async def get_annotations(piece: str):
    """Get all annotations for a piece."""
    return _load_annotations(piece)


@app.post("/api/annotations")
async def create_annotation(ann: AnnotationCreate):
    """Create a new annotation."""
    annotations = _load_annotations(ann.piece)
    new_ann = {
        "id": str(uuid.uuid4())[:8],
        "piece": ann.piece,
        "layer": ann.layer,
        "time_start": ann.time_start,
        "time_end": ann.time_end,
        "event_type": ann.event_type,
        "output_id": ann.output_id,
        "judgment": ann.judgment,
        "question_category": ann.question_category,
        "question_text": ann.question_text,
        "text": ann.text,
        "severity": ann.severity,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    annotations.append(new_ann)
    _save_annotations(ann.piece, annotations)
    return new_ann


@app.put("/api/annotations/{piece}/{ann_id}")
async def update_annotation(piece: str, ann_id: str, update: AnnotationUpdate):
    """Update an existing annotation."""
    annotations = _load_annotations(piece)
    for ann in annotations:
        if ann["id"] == ann_id:
            for field, val in update.model_dump(exclude_none=True).items():
                ann[field] = val
            _save_annotations(piece, annotations)
            return ann
    raise HTTPException(404, f"Annotation {ann_id} not found")


@app.delete("/api/annotations/{piece}/{ann_id}")
async def delete_annotation(piece: str, ann_id: str):
    """Delete an annotation."""
    annotations = _load_annotations(piece)
    annotations = [a for a in annotations if a["id"] != ann_id]
    _save_annotations(piece, annotations)
    return {"deleted": ann_id}


@app.get("/api/kernel/params")
async def get_kernel_params():
    """Return all tunable kernel parameters."""
    return KERNEL_PARAMS


@app.put("/api/kernel/params")
async def update_kernel_param(update: ParamUpdate):
    """Update a single kernel parameter (for live calibration)."""
    group = KERNEL_PARAMS.get(update.group)
    if not group:
        raise HTTPException(404, f"Unknown param group: {update.group}")
    param = group.get(update.key)
    if not param:
        raise HTTPException(404, f"Unknown param: {update.key}")
    if not (param["min"] <= update.value <= param["max"]):
        raise HTTPException(400, f"Value out of range [{param['min']}, {param['max']}]")
    param["value"] = update.value
    return {"group": update.group, "key": update.key, "value": update.value}


@app.post("/api/export/{piece}")
async def export_annotations(piece: str):
    """Export annotations + system snapshot as structured JSON."""
    if piece not in PIECE_REGISTRY:
        raise HTTPException(404, f"Unknown piece: {piece}")

    annotations = _load_annotations(piece)

    # Load trace summary for context
    result_path = RESULTS_DIR / PIECE_REGISTRY[piece]["result"]
    summary = {}
    if result_path.exists():
        with open(result_path) as f:
            data = json.load(f)
            summary = data.get("summary", {})

    # Build system snapshot
    snapshot = {
        "kernel_version": "C3 v2.3 (Precision Compression)",
        "export_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "piece": {
            "slug": piece,
            "title": PIECE_REGISTRY[piece]["title"],
            "duration_s": summary.get("duration_s"),
        },
        "parameters": {
            group: {k: v["value"] for k, v in params.items()}
            for group, params in KERNEL_PARAMS.items()
        },
        "summary": summary,
    }

    export = {
        "system_snapshot": snapshot,
        "annotations": annotations,
        "annotation_count": len(annotations),
        "layers_used": sorted(set(a.get("layer", 1) for a in annotations)),
    }

    # Save to exports directory
    export_path = EXPORTS_DIR / f"{piece}_{time.strftime('%Y%m%d_%H%M%S')}.json"
    with open(export_path, "w") as f:
        json.dump(export, f, indent=2)

    return {
        "export_path": str(export_path),
        "annotation_count": len(annotations),
        "snapshot": snapshot,
    }


@app.get("/api/export/list")
async def list_exports():
    """List all export files."""
    exports = []
    for f in sorted(EXPORTS_DIR.glob("*.json"), reverse=True):
        exports.append({
            "filename": f.name,
            "size_kb": round(f.stat().st_size / 1024, 1),
            "modified": time.strftime(
                "%Y-%m-%d %H:%M:%S",
                time.localtime(f.stat().st_mtime),
            ),
        })
    return exports
