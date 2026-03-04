#!/usr/bin/env python3
"""
Download Deezer Preview MP3s for MI Pipeline Analysis
=====================================================
Reads catalog_5k.json and downloads all preview MP3s.
Output: data/catalog/previews/{deezer_id}.mp3 (30s each)

For RunPod H200 batch processing:
  - Total: ~5000 files × ~500KB = ~2.5GB
  - MI Pipeline: R³(97D) → H³ → C³(131D) per track
  - At 172.27Hz, 30s = ~5,168 frames per track
"""

import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ─── Config ───────────────────────────────────────────────────────────────────

CATALOG_FILE = Path(__file__).parent.parent / "data" / "catalog" / "catalog_5k.json"
PREVIEW_DIR = Path(__file__).parent.parent / "data" / "catalog" / "previews"
MANIFEST_FILE = Path(__file__).parent.parent / "data" / "catalog" / "mi_pipeline_manifest.json"
MAX_WORKERS = 8  # parallel downloads
RATE_LIMIT = 0.05  # seconds between downloads per worker

# ─── Download Logic ───────────────────────────────────────────────────────────

def download_preview(track):
    """Download a single preview MP3."""
    deezer_id = track["deezer_id"]
    preview_url = track.get("preview_url", "")
    out_path = PREVIEW_DIR / f"{deezer_id}.mp3"

    if out_path.exists() and out_path.stat().st_size > 10000:
        return {"id": deezer_id, "status": "exists", "path": str(out_path)}

    if not preview_url:
        return {"id": deezer_id, "status": "no_url", "path": None}

    try:
        req = urllib.request.Request(preview_url)
        req.add_header("User-Agent", "M3-Catalog-Builder/1.0")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
            with open(out_path, "wb") as f:
                f.write(data)
        time.sleep(RATE_LIMIT)
        return {"id": deezer_id, "status": "ok", "path": str(out_path), "size": len(data)}
    except Exception as e:
        return {"id": deezer_id, "status": "error", "error": str(e)}


def generate_mi_manifest(catalog, download_results):
    """Generate manifest for MI pipeline batch processing."""
    manifest = {
        "version": "1.0.0",
        "pipeline": "R³(97D) → H³ → C³(131D)",
        "sample_rate": 22050,
        "frame_rate_hz": 172.27,
        "expected_frames_per_30s": 5168,
        "tracks": []
    }

    ok_results = {r["id"]: r for r in download_results if r["status"] in ("ok", "exists")}

    for track in catalog:
        did = track["deezer_id"]
        if did in ok_results:
            manifest["tracks"].append({
                "id": str(did),
                "file": f"previews/{did}.mp3",
                "title": track["title"],
                "artist": track["artist"],
                "duration": min(track.get("duration", 30), 30),  # preview is 30s max
                "deezer_id": did,
                "isrc": track.get("isrc", ""),
                "genre_id": track.get("genre_id"),
                "genre_name": track.get("genre_name", ""),
                "bpm_deezer": track.get("bpm", 0),
                "gain_deezer": track.get("gain", 0),
                "rank_deezer": track.get("rank", 0),
            })

    manifest["total_tracks"] = len(manifest["tracks"])
    manifest["estimated_total_frames"] = len(manifest["tracks"]) * 5168

    with open(MANIFEST_FILE, "w") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return manifest


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  M³ Preview Downloader")
    print("=" * 60)

    if not CATALOG_FILE.exists():
        print(f"  ERROR: Catalog not found at {CATALOG_FILE}")
        print(f"  Run build_catalog_5k.py first.")
        sys.exit(1)

    with open(CATALOG_FILE) as f:
        data = json.load(f)

    tracks = data["tracks"]
    print(f"  Catalog: {len(tracks)} tracks")

    PREVIEW_DIR.mkdir(parents=True, exist_ok=True)

    # Check existing
    existing = set(int(f.stem) for f in PREVIEW_DIR.glob("*.mp3") if f.stat().st_size > 10000)
    to_download = [t for t in tracks if t["deezer_id"] not in existing and t.get("preview_url")]
    already = len(existing)

    print(f"  Already downloaded: {already}")
    print(f"  To download: {len(to_download)}")
    print(f"  No preview URL: {len(tracks) - len(to_download) - already}")
    print(f"  Estimated size: ~{len(to_download) * 500 / 1024:.0f} MB")
    print()

    if not to_download:
        print("  Nothing to download!")
        # Still generate manifest
        results = [{"id": t["deezer_id"], "status": "exists"} for t in tracks if t["deezer_id"] in existing]
        manifest = generate_mi_manifest(tracks, results)
        print(f"  MI manifest: {manifest['total_tracks']} tracks ready")
        return

    # Download with thread pool
    results = []
    # Add existing as "exists" results
    for eid in existing:
        results.append({"id": eid, "status": "exists"})

    start = time.time()
    ok = 0
    errors = 0

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {pool.submit(download_preview, t): t for t in to_download}
        for i, future in enumerate(as_completed(futures)):
            result = future.result()
            results.append(result)
            if result["status"] == "ok":
                ok += 1
            elif result["status"] == "error":
                errors += 1
            total_done = already + ok + errors
            if (i + 1) % 100 == 0:
                elapsed = time.time() - start
                rate = (i + 1) / elapsed
                eta = (len(to_download) - i - 1) / rate / 60
                print(f"  [{total_done}/{len(tracks)}] ok:{ok} err:{errors} | {rate:.1f}/s | ETA: {eta:.1f}m")

    elapsed = time.time() - start
    print(f"\n  Downloaded: {ok} | Errors: {errors} | Time: {elapsed/60:.1f}m")

    # Generate MI pipeline manifest
    manifest = generate_mi_manifest(tracks, results)
    print(f"\n  MI Pipeline Manifest: {MANIFEST_FILE}")
    print(f"  Tracks ready for analysis: {manifest['total_tracks']}")
    print(f"  Estimated total frames: {manifest['estimated_total_frames']:,}")
    print(f"  Estimated RunPod H200 time: ~{manifest['total_tracks'] * 0.5 / 60:.0f} minutes")


if __name__ == "__main__":
    main()
