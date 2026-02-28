"""RAG Indexer — builds ChromaDB collections from knowledge files and literature.

Usage:
    python -m Musical_Intelligence.brain.llm.rag.indexer [--local]

    --local: Use hash-based pseudo-embeddings (no API key needed, for dev only)
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from Musical_Intelligence.brain.llm.config import CHROMA_DIR, KNOWLEDGE_DIR
from Musical_Intelligence.brain.llm.rag.chunker import Chunk, chunk_file, chunk_jsonl
from Musical_Intelligence.brain.llm.rag.collections import COLLECTIONS

# ── ChromaDB Client ─────────────────────────────────────────────────


def _get_client() -> Any:
    """Get or create a persistent ChromaDB client."""
    try:
        import chromadb
    except ImportError:
        raise ImportError(
            "chromadb package required. Install with: pip install chromadb>=0.5.0"
        )
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def _get_or_create_collection(client: Any, name: str) -> Any:
    """Get or create a ChromaDB collection."""
    return client.get_or_create_collection(
        name=name,
        metadata={"hnsw:space": "cosine"},
    )


# ── Indexing Functions ──────────────────────────────────────────────


def index_knowledge_cards(
    client: Any | None = None,
    use_local_embeddings: bool = False,
) -> int:
    """Index all JSONL knowledge files into the knowledge_cards collection.

    Returns:
        Number of chunks indexed.
    """
    if client is None:
        client = _get_client()

    collection = _get_or_create_collection(client, "knowledge_cards")

    # Define source files and their doc_types
    sources: list[tuple[str, str, str]] = [
        ("beliefs.jsonl", "belief", "key"),
        ("dimensions_6d.jsonl", "dimension_6d", "key"),
        ("dimensions_12d.jsonl", "dimension_12d", "key"),
        ("dimensions_24d.jsonl", "dimension_24d", "key"),
        ("personas.jsonl", "persona", "name"),
        ("concepts.jsonl", "concept", "key"),
        ("neurochemicals.jsonl", "neurochemical", "key"),
        ("cross_references.jsonl", "cross_reference", "factor_key"),
        ("observations.jsonl", "observation", "type"),
        ("analysis_guide.jsonl", "analysis_guide", "key"),
    ]

    all_chunks: list[Chunk] = []
    for filename, doc_type, key_field in sources:
        path = KNOWLEDGE_DIR / filename
        if path.exists():
            chunks = chunk_jsonl(path, "knowledge_cards", doc_type, key_field=key_field)
            all_chunks.extend(chunks)

    if not all_chunks:
        return 0

    # Generate embeddings
    texts = [c.text for c in all_chunks]
    if use_local_embeddings:
        from Musical_Intelligence.brain.llm.rag.embedder import embed_texts_local
        embeddings = embed_texts_local(texts)
    else:
        from Musical_Intelligence.brain.llm.rag.embedder import embed_texts
        embeddings = embed_texts(texts)

    # Upsert into ChromaDB
    ids = [f"kc_{i:04d}" for i in range(len(all_chunks))]
    metadatas = [c.metadata for c in all_chunks]

    # ChromaDB batch limit
    batch_size = 500
    for start in range(0, len(all_chunks), batch_size):
        end = min(start + batch_size, len(all_chunks))
        collection.upsert(
            ids=ids[start:end],
            documents=texts[start:end],
            embeddings=embeddings[start:end],
            metadatas=metadatas[start:end],
        )

    return len(all_chunks)


def index_literature(
    literature_dir: Path,
    collection_name: str,
    client: Any | None = None,
    use_local_embeddings: bool = False,
    tier_min: str = "premium",
) -> int:
    """Index markdown literature files into a ChromaDB collection.

    Args:
        literature_dir: Directory containing .md files.
        collection_name: ChromaDB collection name.
        client: Optional ChromaDB client.
        use_local_embeddings: Use hash-based embeddings for dev.
        tier_min: Minimum tier for this content.

    Returns:
        Number of chunks indexed.
    """
    if client is None:
        client = _get_client()

    collection = _get_or_create_collection(client, collection_name)

    # Find all markdown files
    md_files = sorted(literature_dir.rglob("*.md"))
    if not md_files:
        return 0

    all_chunks: list[Chunk] = []
    for md_path in md_files:
        chunks = chunk_file(
            md_path,
            collection_name,
            "literature",
            chunk_size=512,
            tier_min=tier_min,
        )
        all_chunks.extend(chunks)

    if not all_chunks:
        return 0

    # Generate embeddings
    texts = [c.text for c in all_chunks]
    if use_local_embeddings:
        from Musical_Intelligence.brain.llm.rag.embedder import embed_texts_local
        embeddings = embed_texts_local(texts)
    else:
        from Musical_Intelligence.brain.llm.rag.embedder import embed_texts
        embeddings = embed_texts(texts)

    # Upsert
    ids = [f"{collection_name}_{i:05d}" for i in range(len(all_chunks))]
    metadatas = [c.metadata for c in all_chunks]

    batch_size = 500
    for start in range(0, len(all_chunks), batch_size):
        end = min(start + batch_size, len(all_chunks))
        collection.upsert(
            ids=ids[start:end],
            documents=texts[start:end],
            embeddings=embeddings[start:end],
            metadatas=metadatas[start:end],
        )

    return len(all_chunks)


def index_all(use_local_embeddings: bool = False) -> dict[str, int]:
    """Index everything: knowledge cards + literature + mechanisms.

    Returns:
        Dict mapping collection name to chunk count.
    """
    from Musical_Intelligence.brain.llm.config import (
        BUILDING_DIR,
        LITERATURE_DIR,
    )

    client = _get_client()
    results: dict[str, int] = {}

    # 1. Knowledge cards (always)
    count = index_knowledge_cards(client, use_local_embeddings)
    results["knowledge_cards"] = count
    print(f"  knowledge_cards: {count} chunks")

    # 2. C³ literature
    lit_c3 = LITERATURE_DIR / "C³"
    if lit_c3.exists():
        count = index_literature(
            lit_c3, "literature_c3", client, use_local_embeddings, "premium"
        )
        results["literature_c3"] = count
        print(f"  literature_c3: {count} chunks")

    # 3. C⁰/H⁰ literature
    lit_c0 = LITERATURE_DIR / "C⁰-H⁰"
    if lit_c0.exists():
        count = index_literature(
            lit_c0, "literature_c0", client, use_local_embeddings, "premium"
        )
        results["literature_c0"] = count
        print(f"  literature_c0: {count} chunks")

    # 4. Mechanism docs
    mech_dir = BUILDING_DIR / "C³-Brain"
    if mech_dir.exists():
        count = index_literature(
            mech_dir, "mechanisms", client, use_local_embeddings, "research"
        )
        results["mechanisms"] = count
        print(f"  mechanisms: {count} chunks")

    return results


# ── CLI Entry Point ─────────────────────────────────────────────────

if __name__ == "__main__":
    import sys

    use_local = "--local" in sys.argv
    if use_local:
        print("Using local pseudo-embeddings (dev mode)")
    else:
        print("Using OpenAI text-embedding-3-small")

    print("Indexing all collections...")
    results = index_all(use_local_embeddings=use_local)
    total = sum(results.values())
    print(f"\nTotal: {total} chunks across {len(results)} collections")
