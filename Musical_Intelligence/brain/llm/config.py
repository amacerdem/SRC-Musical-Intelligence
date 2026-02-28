"""LLM Library configuration."""

from pathlib import Path

# ── Paths ────────────────────────────────────────────────────────────

LLM_ROOT = Path(__file__).parent
KNOWLEDGE_DIR = LLM_ROOT / "knowledge"
PROMPTS_DIR = LLM_ROOT / "prompts"

PROJECT_ROOT = LLM_ROOT.parent.parent.parent  # Musical Intelligence/
LITERATURE_DIR = PROJECT_ROOT / "Literature"
BUILDING_DIR = PROJECT_ROOT / "Building"
DOCS_DIR = PROJECT_ROOT / "Docs"

# ── Model Configuration ─────────────────────────────────────────────

MODELS = {
    "primary": "claude-haiku-4-5-20251001",
    "fast": "claude-haiku-4-5-20251001",
    "deep": "claude-haiku-4-5-20251001",
}

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIM = 1536

# ── Tier Definitions ────────────────────────────────────────────────

TIERS = {
    "free": {"max_dim": 6, "label": "Surface", "domain": "Psychology"},
    "basic": {"max_dim": 12, "label": "Narrative", "domain": "Music Cognition"},
    "premium": {"max_dim": 24, "label": "Deep", "domain": "Neuroscience"},
    "research": {"max_dim": 131, "label": "Research", "domain": "C³ Internals"},
}

# ── RAG Configuration ───────────────────────────────────────────────

CHUNK_SIZE = 512          # target tokens per chunk
CHUNK_OVERLAP = 64        # overlap between chunks
TOP_K = 5                 # retrieval results
CHROMA_DIR = LLM_ROOT / "chroma_db"

# ── Context Budget (tokens) ─────────────────────────────────────────

CONTEXT_BUDGET = {
    "persona": 1500,
    "user_profile": 500,
    "vocabulary": 2000,
    "interpretation_guide": 1200,
    "knowledge_rag": 2000,
    "literature_rag": 1500,
    "conversation": 2000,
}
