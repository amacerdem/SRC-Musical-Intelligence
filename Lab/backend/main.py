"""MI-Lab Backend — FastAPI application."""

import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import CORS_ORIGINS, MI_MODULE_ROOT, PROJECT_ROOT

# Ensure Musical_Intelligence is importable
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup/shutdown lifecycle."""
    print(f"MI-Lab Backend starting...")
    print(f"  Project root: {PROJECT_ROOT}")
    print(f"  MI module:    {MI_MODULE_ROOT}")
    yield
    print("MI-Lab Backend shutting down.")


app = FastAPI(
    title="MI-Lab",
    description="Musical Intelligence Scientific Experiment Platform",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Register routers ──
from routers.audio import router as audio_router
from routers.docs import router as docs_router

app.include_router(audio_router, prefix="/api/audio", tags=["audio"])
app.include_router(docs_router, prefix="/api/docs", tags=["docs"])


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
