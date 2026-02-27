"""MI-Lab Backend — FastAPI server for Musical Intelligence pipeline.

Run::

    cd Lab/backend
    python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""
from __future__ import annotations

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure project root is on sys.path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize MI pipeline on startup."""
    from .pipeline import MIPipeline

    print("[MI-Lab] Starting backend...")
    app.state.pipeline = MIPipeline()
    print("[MI-Lab] Backend ready.")
    yield
    print("[MI-Lab] Shutting down.")


app = FastAPI(
    title="MI-Lab",
    description="Musical Intelligence Laboratory Backend",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — allow Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Relay-Dim", "X-H3-Count", "X-H3-Frames", "X-Mel-Bins", "X-Frames"],
)

# Import and mount routers
from .routers.audio import router as audio_router
from .routers.pipeline import router as pipeline_router
from .routers.experiments import router as experiments_router
from .routers.c3_compat import router as c3_compat_router
from .routers.agent import router as agent_router

app.include_router(audio_router, prefix="/api/audio")
app.include_router(pipeline_router, prefix="/api/pipeline")
app.include_router(experiments_router, prefix="/api/experiments")
app.include_router(c3_compat_router, prefix="/api/c3")
app.include_router(agent_router, prefix="/api/agent")


@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "version": "2.0.0"}
