#!/usr/bin/env python3
"""
Prepare dataset_5k for RunPod deployment.

Converts:
  dataset_5k/previews/258700.mp3        → dataset_runpod/Nezih Uzel - Taksim makam nihavend.mp3
  dataset_5k/metadata/258700.json       → dataset_runpod/Nezih Uzel - Taksim makam nihavend.json

Rules:
  - Filenames: "Artist - Title.ext"
  - Special chars sanitized: / \ : * ? " < > |
  - Max filename length: 200 chars (before extension)
  - Duplicate names get " (deezer_id)" suffix
  - Metadata JSON updated with new filename + original deezer_id preserved
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path

SRC_DIR = Path(__file__).parent / "dataset_5k"
DST_DIR = Path(__file__).parent / "dataset_runpod"
MAX_NAME_LEN = 200


def sanitize(s: str) -> str:
    """Remove filesystem-unsafe characters."""
    s = re.sub(r'[/\\:*?"<>|]', '_', s)
    s = re.sub(r'\s+', ' ', s)       # collapse whitespace
    s = s.strip('. ')                 # Windows doesn't like trailing dots/spaces
    return s


def build_filename_map(tracks: list[dict]) -> dict[int, str]:
    """Map deezer_id → sanitized filename stem (no extension)."""
    # First pass: generate base names
    base_names: dict[int, str] = {}
    for t in tracks:
        artist = sanitize(t["artist"])
        title = sanitize(t["title"])
        stem = f"{artist} - {title}"
        if len(stem) > MAX_NAME_LEN:
            stem = stem[:MAX_NAME_LEN].rstrip('. ')
        base_names[t["deezer_id"]] = stem

    # Second pass: detect duplicates (case-insensitive for macOS/RunPod compatibility)
    name_counts: dict[str, list[int]] = {}
    for did, stem in base_names.items():
        key = stem.lower()
        name_counts.setdefault(key, []).append(did)

    final: dict[int, str] = {}
    for key, ids in name_counts.items():
        if len(ids) == 1:
            final[ids[0]] = base_names[ids[0]]
        else:
            for did in ids:
                stem = base_names[did]
                suffixed = f"{stem} ({did})"
                if len(suffixed) > MAX_NAME_LEN + 15:
                    suffixed = f"{stem[:MAX_NAME_LEN - 15]} ({did})"
                final[did] = suffixed

    # Final pass: catch any remaining case-insensitive collisions
    seen: dict[str, int] = {}
    for did in sorted(final.keys()):
        key = final[did].lower()
        if key in seen:
            final[did] = f"{final[did]} ({did})"
        seen[key] = did

    return final


def main():
    # Load catalog
    catalog_path = SRC_DIR / "catalog.json"
    with open(catalog_path) as f:
        catalog = json.load(f)
    tracks = catalog["tracks"]

    print(f"Source: {SRC_DIR}")
    print(f"Destination: {DST_DIR}")
    print(f"Tracks in catalog: {len(tracks)}")

    # Build filename map
    name_map = build_filename_map(tracks)

    # Create destination
    DST_DIR.mkdir(parents=True, exist_ok=True)

    # Track stats
    copied = 0
    skipped = 0
    errors = []

    for t in tracks:
        did = t["deezer_id"]
        stem = name_map[did]

        src_mp3 = SRC_DIR / "previews" / f"{did}.mp3"
        src_meta = SRC_DIR / "metadata" / f"{did}.json"

        dst_mp3 = DST_DIR / f"{stem}.mp3"
        dst_meta = DST_DIR / f"{stem}.json"

        # Copy MP3
        if not src_mp3.exists():
            errors.append(f"MP3 missing: {did}")
            skipped += 1
            continue

        shutil.copy2(src_mp3, dst_mp3)

        # Build enriched metadata
        if src_meta.exists():
            with open(src_meta) as f:
                meta = json.load(f)
        else:
            # Fallback: use catalog entry
            meta = {
                "deezer_id": did,
                "title": t["title"],
                "artist": t["artist"],
                "artist_id": t.get("artist_id"),
                "album": t.get("album", ""),
                "genre": t.get("genre", ""),
                "duration": t.get("duration", 0),
                "rank": t.get("rank", 0),
                "release_date": t.get("release_date", ""),
                "bpm": t.get("bpm", 0.0),
                "explicit": t.get("explicit", False),
                "cover_url": t.get("cover_url", ""),
            }

        # Add filename reference
        meta["filename"] = f"{stem}.mp3"
        meta["original_deezer_file"] = f"{did}.mp3"

        with open(dst_meta, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)

        copied += 1

        if copied % 500 == 0:
            print(f"  ... {copied}/{len(tracks)}")

    # Write manifest for RunPod
    manifest = {
        "version": "1.0.0",
        "source": "deezer_api",
        "total_tracks": copied,
        "total_skipped": skipped,
        "naming": "Artist - Title.mp3 + Artist - Title.json",
        "genres": catalog.get("genres", {}),
        "errors": errors,
    }
    with open(DST_DIR / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    print(f"\nDone!")
    print(f"  Copied: {copied}")
    print(f"  Skipped: {skipped}")
    if errors:
        print(f"  Errors: {len(errors)}")
        for e in errors[:10]:
            print(f"    - {e}")

    # Quick verification
    mp3_count = len(list(DST_DIR.glob("*.mp3")))
    json_count = len(list(DST_DIR.glob("*.json"))) - 1  # exclude manifest
    print(f"\nVerification:")
    print(f"  MP3 files:  {mp3_count}")
    print(f"  JSON files: {json_count}")
    print(f"  Matched:    {'YES' if mp3_count == json_count else 'NO'}")


if __name__ == "__main__":
    main()
