"""RAG Retriever — query ChromaDB collections with tier-gated filtering.

Usage:
    from Musical_Intelligence.brain.llm.rag.retriever import retrieve

    results = retrieve(
        query="prediction error dopamine",
        user_tier="basic",
        top_k=5,
    )
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from Musical_Intelligence.brain.llm.config import CHROMA_DIR, TOP_K
from Musical_Intelligence.brain.llm.rag.collections import TIER_HIERARCHY, tier_allows

# ── Result Type ─────────────────────────────────────────────────────


@dataclass
class RetrievalResult:
    """A single retrieval result."""

    text: str
    score: float  # cosine similarity (higher = more relevant)
    metadata: dict[str, Any]
    collection: str

    @property
    def tier_min(self) -> str:
        return self.metadata.get("tier_min", "free")

    @property
    def doc_type(self) -> str:
        return self.metadata.get("doc_type", "unknown")

    @property
    def source_file(self) -> str:
        return self.metadata.get("source_file", "unknown")


# ── ChromaDB Client (cached) ───────────────────────────────────────

_client: Any = None


def _get_client() -> Any:
    global _client
    if _client is None:
        try:
            import chromadb
        except ImportError:
            raise ImportError("chromadb package required: pip install chromadb>=0.5.0")
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _client


# ── Core Retrieval ──────────────────────────────────────────────────


def retrieve(
    query: str,
    user_tier: str = "free",
    collections: list[str] | None = None,
    top_k: int = TOP_K,
    doc_type_filter: str | None = None,
    dimension_filter: str | None = None,
    use_local_embeddings: bool = False,
) -> list[RetrievalResult]:
    """Retrieve relevant chunks from ChromaDB with tier filtering.

    Args:
        query: User's search query or message text.
        user_tier: User's subscription tier for content filtering.
        collections: Which collections to search (default: all accessible).
        top_k: Number of results to return per collection.
        doc_type_filter: Optional filter by doc_type metadata.
        dimension_filter: Optional filter by dimension_6d metadata.
        use_local_embeddings: Use hash-based embeddings (dev mode).

    Returns:
        List of RetrievalResult sorted by relevance (highest first).
    """
    client = _get_client()

    # Determine which collections to search
    if collections is None:
        from Musical_Intelligence.brain.llm.rag.collections import COLLECTIONS
        collections = [
            name
            for name, coll_def in COLLECTIONS.items()
            if tier_allows(user_tier, coll_def.tier_min)
        ]

    # Generate query embedding
    if use_local_embeddings:
        from Musical_Intelligence.brain.llm.rag.embedder import embed_texts_local
        query_embedding = embed_texts_local([query])[0]
    else:
        from Musical_Intelligence.brain.llm.rag.embedder import embed_single
        query_embedding = embed_single(query)

    # Query each collection
    all_results: list[RetrievalResult] = []

    for coll_name in collections:
        try:
            collection = client.get_collection(coll_name)
        except Exception:
            continue  # Collection doesn't exist yet

        # Build where filter
        where_filter: dict[str, Any] | None = None
        conditions: list[dict] = []

        if doc_type_filter:
            conditions.append({"doc_type": {"$eq": doc_type_filter}})
        if dimension_filter:
            conditions.append({"dimension_6d": {"$eq": dimension_filter}})

        if len(conditions) == 1:
            where_filter = conditions[0]
        elif len(conditions) > 1:
            where_filter = {"$and": conditions}

        try:
            query_result = collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
                where=where_filter if where_filter else None,
                include=["documents", "metadatas", "distances"],
            )
        except Exception:
            continue

        # Process results
        if query_result and query_result["documents"]:
            docs = query_result["documents"][0]
            metadatas = query_result["metadatas"][0] if query_result["metadatas"] else [{}] * len(docs)
            distances = query_result["distances"][0] if query_result["distances"] else [1.0] * len(docs)

            for doc, meta, dist in zip(docs, metadatas, distances):
                # ChromaDB cosine distance → similarity
                similarity = 1.0 - dist

                # Tier-gate the result
                result_tier = meta.get("tier_min", "free")
                if not tier_allows(user_tier, result_tier):
                    continue

                all_results.append(
                    RetrievalResult(
                        text=doc,
                        score=similarity,
                        metadata=meta,
                        collection=coll_name,
                    )
                )

    # Sort by relevance (highest similarity first)
    all_results.sort(key=lambda r: r.score, reverse=True)

    # Return top_k overall
    return all_results[:top_k]


# ── Convenience Functions ───────────────────────────────────────────


def retrieve_knowledge(
    query: str,
    user_tier: str = "free",
    top_k: int = 5,
    **kwargs: Any,
) -> list[RetrievalResult]:
    """Retrieve from knowledge_cards collection only."""
    return retrieve(
        query, user_tier, collections=["knowledge_cards"], top_k=top_k, **kwargs
    )


def retrieve_literature(
    query: str,
    user_tier: str = "premium",
    top_k: int = 3,
    **kwargs: Any,
) -> list[RetrievalResult]:
    """Retrieve from literature collections only."""
    return retrieve(
        query,
        user_tier,
        collections=["literature_c3", "literature_c0"],
        top_k=top_k,
        **kwargs,
    )


def retrieve_mechanisms(
    query: str,
    top_k: int = 3,
    **kwargs: Any,
) -> list[RetrievalResult]:
    """Retrieve from mechanisms collection (research tier only)."""
    return retrieve(
        query,
        "research",
        collections=["mechanisms"],
        top_k=top_k,
        **kwargs,
    )


def format_results_for_prompt(
    results: list[RetrievalResult],
    max_tokens: int = 2000,
) -> str:
    """Format retrieval results as context text for LLM prompt injection.

    Args:
        results: List of RetrievalResult from retrieve().
        max_tokens: Token budget for the formatted output.

    Returns:
        Formatted text suitable for prompt injection.
    """
    lines: list[str] = []
    token_count = 0

    for r in results:
        text = r.text.strip()
        text_tokens = len(text) // 4
        if token_count + text_tokens > max_tokens:
            break
        lines.append(f"[{r.doc_type}] {text}")
        token_count += text_tokens

    return "\n\n".join(lines)
