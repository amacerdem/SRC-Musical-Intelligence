"""Embedding wrapper — converts text chunks to vectors.

Uses OpenAI text-embedding-3-small (1536D) for production,
with a local fallback for development/testing.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from Musical_Intelligence.brain.llm.config import EMBEDDING_DIM, EMBEDDING_MODEL

# ── Cache ───────────────────────────────────────────────────────────

_CACHE_DIR: Path | None = None


def _get_cache_dir() -> Path:
    global _CACHE_DIR
    if _CACHE_DIR is None:
        from Musical_Intelligence.brain.llm.config import LLM_ROOT
        _CACHE_DIR = LLM_ROOT / ".embed_cache"
        _CACHE_DIR.mkdir(exist_ok=True)
    return _CACHE_DIR


def _cache_key(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def _load_cached(text: str) -> list[float] | None:
    path = _get_cache_dir() / f"{_cache_key(text)}.json"
    if path.exists():
        return json.loads(path.read_text())
    return None


def _save_cached(text: str, embedding: list[float]) -> None:
    path = _get_cache_dir() / f"{_cache_key(text)}.json"
    path.write_text(json.dumps(embedding))


# ── Embedding Functions ─────────────────────────────────────────────


def embed_texts(
    texts: list[str],
    model: str = EMBEDDING_MODEL,
    use_cache: bool = True,
) -> list[list[float]]:
    """Embed a batch of texts using OpenAI API.

    Args:
        texts: List of text strings to embed.
        model: OpenAI embedding model name.
        use_cache: Whether to use local file cache.

    Returns:
        List of embedding vectors (each 1536D float list).

    Raises:
        ImportError: If openai package is not installed.
        RuntimeError: If OPENAI_API_KEY is not set.
    """
    # Check cache first
    results: list[list[float] | None] = []
    uncached_indices: list[int] = []
    uncached_texts: list[str] = []

    if use_cache:
        for i, text in enumerate(texts):
            cached = _load_cached(text)
            results.append(cached)
            if cached is None:
                uncached_indices.append(i)
                uncached_texts.append(text)
    else:
        results = [None] * len(texts)
        uncached_indices = list(range(len(texts)))
        uncached_texts = texts

    # Embed uncached texts
    if uncached_texts:
        try:
            import openai
        except ImportError:
            raise ImportError(
                "openai package required for embeddings. "
                "Install with: pip install openai>=1.50.0"
            )

        import os
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable not set. "
                "Required for text-embedding-3-small."
            )

        client = openai.OpenAI(api_key=api_key)

        # OpenAI batch limit is 2048 texts
        batch_size = 512
        all_embeddings: list[list[float]] = []

        for batch_start in range(0, len(uncached_texts), batch_size):
            batch = uncached_texts[batch_start : batch_start + batch_size]
            response = client.embeddings.create(input=batch, model=model)
            batch_embeddings = [item.embedding for item in response.data]
            all_embeddings.extend(batch_embeddings)

        # Fill results and cache
        for i, idx in enumerate(uncached_indices):
            results[idx] = all_embeddings[i]
            if use_cache:
                _save_cached(texts[idx], all_embeddings[i])

    return results  # type: ignore[return-value]


def embed_single(text: str, model: str = EMBEDDING_MODEL) -> list[float]:
    """Embed a single text string."""
    return embed_texts([text], model=model)[0]


# ── Local Fallback (for development without API key) ────────────────


def embed_texts_local(texts: list[str]) -> list[list[float]]:
    """Simple hash-based pseudo-embeddings for testing.

    NOT suitable for production — no semantic similarity.
    Returns deterministic vectors based on text hash.
    """
    import struct

    results: list[list[float]] = []
    for text in texts:
        h = hashlib.sha256(text.encode()).digest()
        # Extend hash to fill EMBEDDING_DIM floats
        seed_bytes = b""
        for i in range(EMBEDDING_DIM * 4 // 32 + 1):
            seed_bytes += hashlib.sha256(h + i.to_bytes(4, "big")).digest()
        floats = list(struct.unpack(f"{EMBEDDING_DIM}f", seed_bytes[: EMBEDDING_DIM * 4]))
        # Normalize to unit vector
        norm = sum(x * x for x in floats) ** 0.5
        if norm > 0:
            floats = [x / norm for x in floats]
        results.append(floats)
    return results
