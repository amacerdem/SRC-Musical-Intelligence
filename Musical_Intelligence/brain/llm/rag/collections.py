"""RAG collection definitions and metadata schema."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

# ── Collection Definitions ──────────────────────────────────────────


@dataclass(frozen=True)
class CollectionDef:
    """ChromaDB collection definition."""

    name: str
    description: str
    source_type: str  # "jsonl", "markdown", "mixed"
    chunk_size: int  # target tokens per chunk
    tier_min: str  # minimum tier to query ("free", "basic", "premium", "research")


COLLECTIONS: dict[str, CollectionDef] = {
    "knowledge_cards": CollectionDef(
        name="knowledge_cards",
        description="Structured knowledge: beliefs, dimensions, concepts, personas, neurochemicals, cross-references",
        source_type="jsonl",
        chunk_size=256,
        tier_min="free",
    ),
    "literature_c3": CollectionDef(
        name="literature_c3",
        description="C³ paper summaries — 492 markdown files from Literature/C³/",
        source_type="markdown",
        chunk_size=512,
        tier_min="premium",
    ),
    "literature_c0": CollectionDef(
        name="literature_c0",
        description="Temporal neuroscience literature — 120 entries from Literature/C⁰-H⁰/",
        source_type="markdown",
        chunk_size=512,
        tier_min="premium",
    ),
    "mechanisms": CollectionDef(
        name="mechanisms",
        description="C³ mechanism docs — extraction, temporal-integration, cognitive-present, forecast from Building/C³-Brain/",
        source_type="markdown",
        chunk_size=512,
        tier_min="research",
    ),
}


# ── Metadata Schema ────────────────────────────────────────────────


def make_metadata(
    *,
    source_file: str,
    collection: str,
    doc_type: str,
    tier_min: str = "free",
    language: str = "bilingual",
    function: str | None = None,
    dimension_6d: str | None = None,
    belief_key: str | None = None,
    framework: str | None = None,
) -> dict[str, Any]:
    """Create ChromaDB metadata dict for a chunk.

    All values must be str, int, float, or bool (ChromaDB constraint).
    """
    meta: dict[str, Any] = {
        "source_file": source_file,
        "collection": collection,
        "doc_type": doc_type,
        "tier_min": tier_min,
        "language": language,
    }
    if function:
        meta["function"] = function
    if dimension_6d:
        meta["dimension_6d"] = dimension_6d
    if belief_key:
        meta["belief_key"] = belief_key
    if framework:
        meta["framework"] = framework
    return meta


# ── Tier Filtering ──────────────────────────────────────────────────

TIER_HIERARCHY = {"free": 0, "basic": 1, "premium": 2, "research": 3}


def tier_allows(user_tier: str, required_tier: str) -> bool:
    """Check if user tier is sufficient to access content."""
    return TIER_HIERARCHY.get(user_tier, 0) >= TIER_HIERARCHY.get(required_tier, 0)
