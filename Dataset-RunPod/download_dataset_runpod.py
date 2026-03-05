#!/usr/bin/env python3
"""
Download Deezer 30s previews on RunPod and save with real Artist - Title names.

Usage (on RunPod):
    python3 download_dataset_runpod.py [--output /workspace/dataset] [--workers 16]

Reads catalog.json from the same directory as this script.
Downloads each track's 30s preview from Deezer CDN.
Saves as "Artist - Title.mp3" + "Artist - Title.json" (metadata).
"""

import argparse
import json
import os
import re
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
CATALOG_PATH = SCRIPT_DIR / "catalog.json"
DEEZER_PREVIEW_URL = "https://cdns-preview-{shard}.dzcdn.net/stream/c-{md5_hash}"
DEEZER_TRACK_API = "https://api.deezer.com/track/{deezer_id}"
MAX_NAME_LEN = 200
MAX_RETRIES = 3
TIMEOUT = 15


def sanitize(s: str) -> str:
    """Remove filesystem-unsafe characters."""
    s = re.sub(r'[/\\:*?"<>|]', '_', s)
    s = re.sub(r'\s+', ' ', s)
    s = s.strip('. ')
    return s


def build_filename_map(tracks: list[dict]) -> dict[int, str]:
    """Map deezer_id -> sanitized filename stem."""
    base_names: dict[int, str] = {}
    for t in tracks:
        artist = sanitize(t["artist"])
        title = sanitize(t["title"])
        stem = f"{artist} - {title}"
        if len(stem) > MAX_NAME_LEN:
            stem = stem[:MAX_NAME_LEN].rstrip('. ')
        base_names[t["deezer_id"]] = stem

    # Case-insensitive duplicate detection
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

    # Final collision pass
    seen: dict[str, int] = {}
    for did in sorted(final.keys()):
        key = final[did].lower()
        if key in seen:
            final[did] = f"{final[did]} ({did})"
        seen[key] = did

    return final


def get_preview_url(deezer_id: int) -> str | None:
    """Fetch preview URL from Deezer API."""
    url = f"https://api.deezer.com/track/{deezer_id}"
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MI-Dataset/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = json.loads(resp.read())
                return data.get("preview")
        except Exception:
            if attempt < MAX_RETRIES - 1:
                time.sleep(1 * (attempt + 1))
    return None


def download_preview(url: str, dest: Path) -> bool:
    """Download MP3 preview to dest path."""
    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "MI-Dataset/1.0"})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
                data = resp.read()
                if len(data) < 1000:  # too small, probably error
                    return False
                dest.write_bytes(data)
                return True
        except Exception:
            if attempt < MAX_RETRIES - 1:
                time.sleep(1 * (attempt + 1))
    return False


def process_track(track: dict, stem: str, output_dir: Path) -> tuple[int, bool, str]:
    """Download and save a single track. Returns (deezer_id, success, error_msg)."""
    did = track["deezer_id"]
    mp3_path = output_dir / f"{stem}.mp3"
    meta_path = output_dir / f"{stem}.json"

    # Skip if already downloaded
    if mp3_path.exists() and mp3_path.stat().st_size > 1000:
        # Still write metadata if missing
        if not meta_path.exists():
            write_metadata(track, stem, meta_path)
        return (did, True, "skipped (exists)")

    # Get preview URL from Deezer API
    preview_url = get_preview_url(did)
    if not preview_url:
        return (did, False, "no preview URL from API")

    # Download
    if not download_preview(preview_url, mp3_path):
        return (did, False, "download failed")

    # Write metadata
    write_metadata(track, stem, meta_path)
    return (did, True, "ok")


def write_metadata(track: dict, stem: str, meta_path: Path):
    """Write metadata JSON for a track."""
    meta = {
        "deezer_id": track["deezer_id"],
        "title": track["title"],
        "artist": track["artist"],
        "artist_id": track.get("artist_id"),
        "album": track.get("album", ""),
        "genre": track.get("genre", ""),
        "duration": track.get("duration", 0),
        "rank": track.get("rank", 0),
        "release_date": track.get("release_date", ""),
        "bpm": track.get("bpm", 0.0),
        "explicit": track.get("explicit", False),
        "cover_url": track.get("cover_url", ""),
        "filename": f"{stem}.mp3",
        "original_deezer_id": track["deezer_id"],
    }
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(description="Download Deezer previews for MI dataset")
    parser.add_argument("--output", "-o", type=str, default="/workspace/dataset",
                        help="Output directory (default: /workspace/dataset)")
    parser.add_argument("--workers", "-w", type=int, default=16,
                        help="Concurrent download threads (default: 16)")
    parser.add_argument("--catalog", "-c", type=str, default=str(CATALOG_PATH),
                        help="Path to catalog.json")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load catalog
    with open(args.catalog) as f:
        catalog = json.load(f)
    tracks = catalog["tracks"]

    print(f"Catalog: {args.catalog}")
    print(f"Output:  {output_dir}")
    print(f"Tracks:  {len(tracks)}")
    print(f"Workers: {args.workers}")
    print()

    # Build filename map
    name_map = build_filename_map(tracks)

    # Download with thread pool
    success = 0
    failed = 0
    skipped = 0
    errors = []
    t0 = time.time()

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {
            pool.submit(process_track, t, name_map[t["deezer_id"]], output_dir): t
            for t in tracks
        }

        for i, future in enumerate(as_completed(futures), 1):
            did, ok, msg = future.result()
            if ok:
                if "skipped" in msg:
                    skipped += 1
                else:
                    success += 1
            else:
                failed += 1
                errors.append({"deezer_id": did, "error": msg})

            if i % 100 == 0:
                elapsed = time.time() - t0
                rate = i / elapsed
                eta = (len(tracks) - i) / rate
                print(f"  [{i}/{len(tracks)}] ok={success} skip={skipped} fail={failed} "
                      f"({rate:.0f} tracks/s, ETA {eta:.0f}s)")

    elapsed = time.time() - t0

    # Write manifest
    manifest = {
        "version": "1.0.0",
        "source": "deezer_api",
        "total_tracks": success + skipped,
        "downloaded": success,
        "skipped_existing": skipped,
        "failed": failed,
        "naming": "Artist - Title.mp3 + Artist - Title.json",
        "genres": catalog.get("genres", {}),
        "errors": errors,
    }
    with open(output_dir / "manifest.json", "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\nDone in {elapsed:.1f}s")
    print(f"  Downloaded: {success}")
    print(f"  Skipped:    {skipped}")
    print(f"  Failed:     {failed}")
    print(f"  Total size: {sum(f.stat().st_size for f in output_dir.glob('*.mp3')) / 1e9:.2f} GB")

    if errors:
        print(f"\nFailed tracks ({len(errors)}):")
        for e in errors[:20]:
            print(f"  - {e['deezer_id']}: {e['error']}")

    # Verification
    mp3_count = len(list(output_dir.glob("*.mp3")))
    json_count = len(list(output_dir.glob("*.json"))) - 1
    print(f"\nVerification:")
    print(f"  MP3:  {mp3_count}")
    print(f"  JSON: {json_count}")
    print(f"  Match: {'YES' if mp3_count == json_count else 'NO'}")


if __name__ == "__main__":
    main()
