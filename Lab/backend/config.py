"""MI-Lab configuration — paths, constants, server settings."""

from pathlib import Path

# ── Project Roots ──
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # /Volumes/SRC-9/SRC Musical Intelligence
MI_MODULE_ROOT = PROJECT_ROOT / "Musical_Intelligence"
LAB_ROOT = PROJECT_ROOT / "Lab"

# ── Audio ──
AUDIO_DIR = PROJECT_ROOT / "Test-Audio"
SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
FRAME_RATE = SAMPLE_RATE / HOP_LENGTH  # 172.27 Hz

# ── Storage ──
DATA_DIR = LAB_ROOT / "data"
EXPERIMENTS_DIR = DATA_DIR / "experiments"
EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Documentation ──
BRAIN_DOCS_DIR = PROJECT_ROOT / "Building" / "C³-Brain"

# ── Server ──
HOST = "0.0.0.0"
PORT = 8741
CORS_ORIGINS = ["http://localhost:5173", "http://127.0.0.1:5173"]

# ── R³ Feature Groups ──
R3_GROUPS = {
    "A": {"name": "Consonance",  "range": (0, 7),   "color": "#60a5fa"},
    "B": {"name": "Energy",      "range": (7, 12),  "color": "#f97316"},
    "C": {"name": "Timbre",      "range": (12, 21), "color": "#14b8a6"},
    "D": {"name": "Change",      "range": (21, 25), "color": "#eab308"},
    "F": {"name": "Pitch/Chroma","range": (25, 41), "color": "#22c55e"},
    "G": {"name": "Rhythm",      "range": (41, 51), "color": "#ef4444"},
    "H": {"name": "Harmony",     "range": (51, 63), "color": "#a78bfa"},
    "J": {"name": "Timbre Ext",  "range": (63, 83), "color": "#6366f1"},
    "K": {"name": "Modulation",  "range": (83, 97), "color": "#ec4899"},
}
