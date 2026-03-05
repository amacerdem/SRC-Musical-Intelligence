"""Build enriched catalog from RunPod batch analysis results.

Reads per-track JSON summaries → extracts 6D means + 16-segment temporal arcs
→ produces a single lightweight catalog for the web frontend.

Usage (on RunPod):
    python build_enriched_catalog.py --results /workspace/results --output /workspace/enriched_catalog.json

Output format per track:
    {
        "id": "123456",
        "deezer_id": 123456,
        "title": "...",
        "artist": "...",
        "genre": "...",
        "duration": 240,
        "rank": 500000,
        "preview_url": "...",
        "cover_url": "...",
        "bpm": 120.0,
        "explicit": false,
        "artist_id": 789,
        "dims_6d": [0.72, 0.45, 0.55, 0.68, 0.82, 0.40],
        "arcs_16": {
            "energy":  [0.5, 0.6, ...],   // 16 segments
            "valence": [0.4, 0.3, ...],
            "tempo":   [...],
            "tension": [...],
            "groove":  [...],
            "density": [...]
        }
    }
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path

DIM_6D_KEYS = ("energy", "valence", "tempo", "tension", "groove", "density")
N_ARC_SEGMENTS = 16


def _resample_arc(values: list[float], n_segments: int = N_ARC_SEGMENTS) -> list[float]:
    """Resample a variable-length arc to fixed n_segments via mean pooling."""
    if not values:
        return [0.5] * n_segments
    n = len(values)
    if n <= n_segments:
        # Stretch: repeat values to fill segments
        result = []
        for i in range(n_segments):
            idx = int(i * n / n_segments)
            result.append(round(values[min(idx, n - 1)], 4))
        return result
    # Shrink: mean pool
    result = []
    for i in range(n_segments):
        start = int(i * n / n_segments)
        end = int((i + 1) * n / n_segments)
        chunk = values[start:end]
        result.append(round(sum(chunk) / len(chunk), 4) if chunk else 0.5)
    return result


def _extract_track(json_path: Path, meta: dict, meta_by_id: dict[int, dict] | None = None) -> dict | None:
    """Extract enriched entry from a single track JSON."""
    try:
        with open(json_path, encoding="utf-8", errors="replace") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"  SKIP {json_path.name}: {exc}", file=sys.stderr)
        return None

    # If no metadata from stem match, try deezer_id from JSON content
    if not meta and meta_by_id:
        did = data.get("deezer_id")
        if did and did in meta_by_id:
            meta = meta_by_id[did]

    # Extract 6D means from dimensions.psychology_6d
    dims = data.get("dimensions", {})
    psych_6d = dims.get("psychology_6d", {})

    # psychology_6d can be either:
    # A) dict with named keys: {"energy": 0.72, ...}
    # B) list of 6 floats: [0.72, 0.45, ...]
    if isinstance(psych_6d, dict):
        dims_6d = [round(psych_6d.get(k, 0.5), 4) for k in DIM_6D_KEYS]
    elif isinstance(psych_6d, list) and len(psych_6d) >= 6:
        dims_6d = [round(v, 4) for v in psych_6d[:6]]
    else:
        # Fallback: try dim_6d key
        dim_6d = data.get("dim_6d")
        if isinstance(dim_6d, list) and len(dim_6d) >= 6:
            dims_6d = [round(v, 4) for v in dim_6d[:6]]
        else:
            print(f"  SKIP {json_path.name}: no 6D dims found", file=sys.stderr)
            return None

    # Extract temporal arcs from temporal_profile.dim_6d_per_segment
    # Format: 64×6 matrix (rows=segments, cols=dimensions in order of DIM_6D_KEYS)
    arcs_16: dict[str, list[float]] = {}
    temporal = data.get("temporal_profile", {})
    dim6_segs = temporal.get("dim_6d_per_segment", [])

    if dim6_segs and isinstance(dim6_segs, list) and len(dim6_segs) > 0:
        # Transpose: 64×6 matrix → 6 lists of 64 values → resample to 16
        for dim_idx, key in enumerate(DIM_6D_KEYS):
            col = [row[dim_idx] for row in dim6_segs if isinstance(row, list) and len(row) > dim_idx]
            arcs_16[key] = _resample_arc(col, N_ARC_SEGMENTS)
    else:
        # No temporal data — fill with flat arcs from 6D means
        for dim_idx, key in enumerate(DIM_6D_KEYS):
            arcs_16[key] = [dims_6d[dim_idx]] * N_ARC_SEGMENTS

    # Build enriched entry
    deezer_id = meta.get("deezer_id", data.get("deezer_id", 0))
    return {
        "id": str(deezer_id),
        "deezer_id": deezer_id,
        "title": meta.get("title", data.get("title", "")),
        "artist": meta.get("artist", data.get("artist", "")),
        "genre": meta.get("genre", data.get("genre", "")),
        "duration": meta.get("duration", data.get("duration", 0)),
        "rank": meta.get("rank", data.get("rank", 0)),
        "preview_url": meta.get("preview_url", "") or "",
        "cover_url": meta.get("cover_url", "") or "",
        "bpm": meta.get("bpm", data.get("bpm", 0.0)),
        "explicit": meta.get("explicit", False),
        "artist_id": meta.get("artist_id", 0),
        "dims_6d": dims_6d,
        "arcs_16": arcs_16,
    }


def build(results_dir: Path, catalog_path: Path | None, output_path: Path) -> None:
    """Build enriched catalog from results directory."""
    # Load original catalog for metadata — index by both deezer_id and stem
    meta_by_id: dict[int, dict] = {}
    meta_by_stem: dict[str, dict] = {}
    if catalog_path and catalog_path.exists():
        with open(catalog_path, encoding="utf-8") as f:
            catalog = json.load(f)
        for t in catalog.get("tracks", []):
            did = t.get("deezer_id", 0)
            if did:
                meta_by_id[did] = t
            # Build stem key matching run_batch_analysis filename convention
            artist = t.get("artist", "")
            title = t.get("title", "")
            if artist and title:
                stem_key = f"{artist} - {title}"
                meta_by_stem[stem_key] = t
        print(f"Loaded metadata for {len(meta_by_id)} tracks from catalog")

    # Find all per-track JSON files
    json_files = sorted(results_dir.glob("*.json"))
    # Exclude catalog.json and any summary files
    json_files = [f for f in json_files
                  if f.name not in ("catalog.json", "summary.json", "errors.json")
                  and not f.name.startswith("._")]

    print(f"Found {len(json_files)} track JSON files in {results_dir}")

    enriched_tracks: list[dict] = []
    skipped = 0

    for i, jf in enumerate(json_files):
        if (i + 1) % 500 == 0:
            print(f"  Processing {i + 1}/{len(json_files)}...")

        stem = jf.stem

        # Look up metadata: first try stem match, then deezer_id from inside JSON
        meta = meta_by_stem.get(stem, {})

        entry = _extract_track(jf, meta, meta_by_id)
        if entry:
            enriched_tracks.append(entry)
        else:
            skipped += 1

    print(f"\nEnriched: {len(enriched_tracks)}, Skipped: {skipped}")

    # Write JSON
    result = {
        "version": "2.0",
        "dimensions": list(DIM_6D_KEYS),
        "arc_segments": N_ARC_SEGMENTS,
        "total": len(enriched_tracks),
        "tracks": enriched_tracks,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
    json_size = output_path.stat().st_size
    print(f"Written: {output_path} ({json_size / 1024:.0f} KB)")

    # Also write gzipped version
    gz_path = output_path.with_suffix(".json.gz")
    with gzip.open(gz_path, "wt", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False)
    gz_size = gz_path.stat().st_size
    print(f"Gzipped: {gz_path} ({gz_size / 1024:.0f} KB)")

    # Stats
    print(f"\n{'=' * 60}")
    print(f"Enriched Catalog Summary")
    print(f"{'=' * 60}")
    print(f"  Tracks:       {len(enriched_tracks)}")
    print(f"  JSON size:    {json_size / 1024:.0f} KB")
    print(f"  Gzip size:    {gz_size / 1024:.0f} KB")
    print(f"  Per track:    ~{json_size / max(len(enriched_tracks), 1):.0f} bytes")
    print(f"  Dimensions:   {', '.join(DIM_6D_KEYS)}")
    print(f"  Arc segments: {N_ARC_SEGMENTS}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build enriched catalog from batch analysis results")
    parser.add_argument("--results", type=Path, default=Path("/workspace/results"),
                        help="Directory containing per-track JSON files")
    parser.add_argument("--catalog", type=Path, default=None,
                        help="Original catalog.json for metadata (auto-detected if not given)")
    parser.add_argument("--output", type=Path, default=Path("/workspace/enriched_catalog.json"),
                        help="Output path for enriched catalog")
    args = parser.parse_args()

    # Auto-detect catalog
    if args.catalog is None:
        for candidate in [
            args.results / "catalog.json",
            Path("/workspace/MI/Dataset-RunPod/catalog.json"),
            Path("/workspace/dataset/catalog.json"),
        ]:
            if candidate.exists():
                args.catalog = candidate
                break

    build(args.results, args.catalog, args.output)
