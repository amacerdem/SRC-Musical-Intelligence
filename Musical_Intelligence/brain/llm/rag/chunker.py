"""Document chunker — splits source documents into embeddable chunks.

Supports two modes:
  1. JSONL → each line becomes one chunk (with structured text rendering)
  2. Markdown → split on headings/paragraphs, respecting chunk_size
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Chunk:
    """A single embeddable text chunk with metadata."""

    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    token_estimate: int = 0

    def __post_init__(self) -> None:
        if self.token_estimate == 0:
            self.token_estimate = len(self.text) // 4


# ── Token Estimation ────────────────────────────────────────────────


def estimate_tokens(text: str) -> int:
    """Rough token count (~4 chars/token for mixed TR/EN)."""
    return len(text) // 4


# ── JSONL Chunking ──────────────────────────────────────────────────


def _render_jsonl_card(record: dict, key_field: str = "key") -> str:
    """Render a JSONL record as readable text for embedding.

    Concatenates all string/list values into a coherent passage.
    """
    parts: list[str] = []
    key = record.get(key_field, record.get("name_en", "unknown"))
    name_en = record.get("name_en", key)
    name_tr = record.get("name_tr", "")

    parts.append(f"{name_en}")
    if name_tr:
        parts.append(f"({name_tr})")

    # Add all descriptive string fields
    for field_name in [
        "summary_en", "summary_tr",
        "what_en", "what_tr",
        "high_en", "high_tr",
        "low_en", "low_tr",
        "deep_en", "deep_tr",
        "fun_fact_en", "fun_fact_tr",
        "description_en", "description_tr",
        "analogy_en", "analogy_tr",
        "detail_en", "detail_tr",
        "tagline_en", "tagline_tr",
        "conversation_tone",
        "metaphor_style",
    ]:
        val = record.get(field_name)
        if val and isinstance(val, str):
            parts.append(val)

    # Add list fields
    for field_name in ["preferred_topics", "citations", "related_6d"]:
        val = record.get(field_name)
        if val and isinstance(val, list):
            parts.append(", ".join(str(v) for v in val))

    return " | ".join(parts)


def chunk_jsonl(
    path: Path,
    collection: str,
    doc_type: str,
    key_field: str = "key",
) -> list[Chunk]:
    """Chunk a JSONL file — one chunk per line.

    Args:
        path: Path to the .jsonl file.
        collection: ChromaDB collection name.
        doc_type: Document type for metadata (e.g., "belief", "dimension_6d").
        key_field: Field name to use as the record key.

    Returns:
        List of Chunk objects ready for embedding.
    """
    chunks: list[Chunk] = []
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        text = _render_jsonl_card(record, key_field)
        metadata = {
            "source_file": path.name,
            "collection": collection,
            "doc_type": doc_type,
            "tier_min": record.get("tier_min", record.get("tier_visible", "free")),
            "language": "bilingual",
        }
        # Add optional metadata fields
        key = record.get(key_field, "")
        if key:
            metadata["key"] = key
        func = record.get("function")
        if func:
            metadata["function"] = func
        dim_6d = record.get("primary_6d")
        if dim_6d and isinstance(dim_6d, str):
            metadata["dimension_6d"] = dim_6d
        elif dim_6d and isinstance(dim_6d, list) and dim_6d:
            metadata["dimension_6d"] = dim_6d[0]
        parent_6d = record.get("parent_6d")
        if parent_6d:
            metadata["dimension_6d"] = parent_6d
        framework = record.get("framework")
        if framework:
            metadata["framework"] = framework

        chunks.append(Chunk(text=text, metadata=metadata))

    return chunks


# ── Markdown Chunking ───────────────────────────────────────────────


def chunk_markdown(
    path: Path,
    collection: str,
    doc_type: str,
    chunk_size: int = 512,
    overlap: int = 64,
    tier_min: str = "premium",
) -> list[Chunk]:
    """Chunk a markdown file by headings and paragraphs.

    Strategy:
      1. Split on ## headings into sections.
      2. If a section exceeds chunk_size tokens, split on paragraphs.
      3. Merge small consecutive paragraphs until chunk_size reached.

    Args:
        path: Path to the .md file.
        collection: ChromaDB collection name.
        doc_type: Document type for metadata.
        chunk_size: Target tokens per chunk.
        overlap: Token overlap between consecutive chunks.
        tier_min: Minimum tier for this content.

    Returns:
        List of Chunk objects ready for embedding.
    """
    text = path.read_text(encoding="utf-8")

    # Split on headings (## or ###)
    sections = re.split(r"\n(?=#{2,3}\s)", text)

    chunks: list[Chunk] = []
    for section in sections:
        section = section.strip()
        if not section:
            continue

        section_tokens = estimate_tokens(section)

        if section_tokens <= chunk_size:
            # Section fits in one chunk
            chunks.append(
                Chunk(
                    text=section,
                    metadata={
                        "source_file": path.name,
                        "collection": collection,
                        "doc_type": doc_type,
                        "tier_min": tier_min,
                        "language": "en",
                    },
                )
            )
        else:
            # Split section into paragraphs and merge
            paragraphs = section.split("\n\n")
            current_parts: list[str] = []
            current_tokens = 0

            for para in paragraphs:
                para = para.strip()
                if not para:
                    continue
                para_tokens = estimate_tokens(para)

                if current_tokens + para_tokens > chunk_size and current_parts:
                    # Emit current chunk
                    chunks.append(
                        Chunk(
                            text="\n\n".join(current_parts),
                            metadata={
                                "source_file": path.name,
                                "collection": collection,
                                "doc_type": doc_type,
                                "tier_min": tier_min,
                                "language": "en",
                            },
                        )
                    )
                    # Keep overlap: last paragraph of previous chunk
                    if overlap > 0 and current_parts:
                        last = current_parts[-1]
                        current_parts = [last]
                        current_tokens = estimate_tokens(last)
                    else:
                        current_parts = []
                        current_tokens = 0

                current_parts.append(para)
                current_tokens += para_tokens

            # Emit remaining
            if current_parts:
                chunks.append(
                    Chunk(
                        text="\n\n".join(current_parts),
                        metadata={
                            "source_file": path.name,
                            "collection": collection,
                            "doc_type": doc_type,
                            "tier_min": tier_min,
                            "language": "en",
                        },
                    )
                )

    return chunks


# ── Convenience ─────────────────────────────────────────────────────


def chunk_file(
    path: Path,
    collection: str,
    doc_type: str,
    chunk_size: int = 512,
    **kwargs: Any,
) -> list[Chunk]:
    """Auto-detect format and chunk a file."""
    if path.suffix == ".jsonl":
        return chunk_jsonl(path, collection, doc_type, **kwargs)
    elif path.suffix in (".md", ".markdown"):
        return chunk_markdown(path, collection, doc_type, chunk_size=chunk_size, **kwargs)
    else:
        raise ValueError(f"Unsupported file format: {path.suffix}")
