"""Run full MI pipeline on Swan Lake — complete frame-level export.

Saves:
  1. Track summary JSON  → public/data/mi-dataset/tracks/{id}.json
  2. Frame-level binary  → public/data/mi-dataset/tracks/{id}_frames.npz
     - beliefs  (T, 131)
     - neuro    (T, 4)
     - ram      (T, 26)
     - reward   (T,)
     - dim_6d   (T, 6)
     - dim_12d  (T, 12)
     - dim_24d  (T, 24)
     - r3       (T, 97)

Usage:
    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python run_swan_lake.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

# ── Config ────────────────────────────────────────────────────────
WAV_PATH = PROJECT_ROOT / "Test-Audio" / "Swan_Lake_Suite__Op._20a__I._Scene__Swan_Theme_._Moderato_-_Pyotr_Ilyich_Tchaikovsky_ccaa3171.wav"
TRACK_ID = "tchaikovsky__swan_lake_suite_op20a_scene"
ARTIST = "Pyotr Ilyich Tchaikovsky"
TITLE = "Swan Lake Suite, Op. 20a: I. Scene (Swan Theme)"
CATEGORIES = ["Classical", "Orchestral", "Lab"]

MMM_DIR = PROJECT_ROOT / "My Musical Mind (Monetizing)"
TRACKS_DIR = MMM_DIR / "public" / "data" / "mi-dataset" / "tracks"
CATALOG_PATH = MMM_DIR / "public" / "data" / "mi-dataset" / "catalog.json"

# Also write to dist/ for immediate availability
DIST_TRACKS_DIR = MMM_DIR / "dist" / "data" / "mi-dataset" / "tracks"
DIST_CATALOG_PATH = MMM_DIR / "dist" / "data" / "mi-dataset" / "catalog.json"

N_SEGMENTS = 64  # temporal profile segments (high-res)


def _seg_stats(data, n_seg):
    """Segment a (T, D) array into n_seg bins, return means per segment."""
    import numpy as np
    T = data.shape[0]
    seg_size = T // n_seg
    out = []
    for s in range(n_seg):
        start = s * seg_size
        end = (s + 1) * seg_size if s < n_seg - 1 else T
        out.append(data[start:end].mean(axis=0))
    return np.array(out)  # (n_seg, D)


def _round_list(arr, decimals=4):
    return [round(float(v), decimals) for v in arr]


def _round_matrix(mat, decimals=4):
    return [_round_list(row, decimals) for row in mat]


def main():
    import numpy as np

    print(f"[Swan Lake] WAV: {WAV_PATH}")
    print(f"[Swan Lake] Track ID: {TRACK_ID}")
    assert WAV_PATH.exists(), f"WAV file not found: {WAV_PATH}"

    # ── Step 1: Add WAV to catalog temporarily ────────────────────
    from Lab.backend.config import AUDIO_CATALOG
    AUDIO_CATALOG["swan_lake_wav"] = WAV_PATH.name

    # ── Step 2: Initialize pipeline ───────────────────────────────
    print("\n[Swan Lake] Initializing MI Pipeline...")
    t0 = time.perf_counter()
    from Lab.backend.pipeline import MIPipeline
    pipeline = MIPipeline()
    print(f"[Swan Lake] Pipeline ready in {time.perf_counter() - t0:.1f}s")

    # ── Step 3: Run full pipeline (R³ → H³ → C³) ─────────────────
    print("\n[Swan Lake] Running full pipeline (R³ → H³ → C³)...")
    t1 = time.perf_counter()

    def status_cb(phase, progress):
        bar = "█" * int(progress * 30) + "░" * (30 - int(progress * 30))
        print(f"  [{bar}] {phase} ({progress*100:.0f}%)", end="\r")

    result = pipeline.run("swan_lake_wav", excerpt_s=None, status_callback=status_cb)
    elapsed = time.perf_counter() - t1
    print(f"\n[Swan Lake] Pipeline complete: {result.n_frames} frames, "
          f"{result.duration_s:.1f}s, {result.fps:.1f} fps, {elapsed:.1f}s wall")

    T = result.beliefs.shape[0]
    r3 = result.r3  # (T, 97)

    # ── Step 4: Frame-level binary (NPZ) ──────────────────────────
    print(f"\n[Swan Lake] Saving frame-level data ({T} frames)...")
    for tracks_dir in [TRACKS_DIR, DIST_TRACKS_DIR]:
        tracks_dir.mkdir(parents=True, exist_ok=True)
        npz_path = tracks_dir / f"{TRACK_ID}_frames.npz"
        np.savez_compressed(
            npz_path,
            beliefs=result.beliefs.astype(np.float32),   # (T, 131)
            neuro=result.neuro.astype(np.float32),        # (T, 4)
            ram=result.ram.astype(np.float32),             # (T, 26)
            reward=result.reward.astype(np.float32),       # (T,)
            dim_6d=result.dim_6d.astype(np.float32),       # (T, 6)
            dim_12d=result.dim_12d.astype(np.float32),     # (T, 12)
            dim_24d=result.dim_24d.astype(np.float32),     # (T, 24)
            r3=r3.astype(np.float32),                      # (T, 97)
        )
        sz = npz_path.stat().st_size
        print(f"  Saved: {npz_path} ({sz/1024/1024:.1f} MB)")

    # ── Step 5: Temporal profiles (64 segments) ───────────────────
    print(f"\n[Swan Lake] Computing {N_SEGMENTS}-segment temporal profiles...")
    belief_segs = _seg_stats(result.beliefs, N_SEGMENTS)   # (64, 131)
    neuro_segs = _seg_stats(result.neuro, N_SEGMENTS)      # (64, 4)
    ram_segs = _seg_stats(result.ram, N_SEGMENTS)           # (64, 26)
    reward_segs = _seg_stats(result.reward.reshape(-1, 1), N_SEGMENTS)[:, 0]  # (64,)
    dim6_segs = _seg_stats(result.dim_6d, N_SEGMENTS)      # (64, 6)
    dim12_segs = _seg_stats(result.dim_12d, N_SEGMENTS)    # (64, 12)
    dim24_segs = _seg_stats(result.dim_24d, N_SEGMENTS)    # (64, 24)

    # ── Step 6: Compute signal features from R³ ──────────────────
    # R³ groups: A[0:7]=BCH, B[7:12]=Energy, C[12:21]=Timbre, D[21:25]=Change,
    #            F[25:41]=Pitch, G[41:51]=Rhythm, H[51:63]=Harmony, J[63:83]=ExtTimbre, K[83:97]=Modulation
    signal = {
        "energy": round(float(r3[:, 7:12].mean()), 4),
        "valence": round(float(r3[:, 51:63].mean()), 4),
        "tempo": round(float(r3[:, 41:51].mean() * 200), 1),
        "danceability": round(float(r3[:, 41:51].mean()), 4),
        "acousticness": round(float(1.0 - r3[:, 12:21].mean()), 4),
        "harmonicComplexity": round(float(r3[:, 51:63].std()), 4),
        "timbralBrightness": round(float(r3[:, 14].mean()), 4) if r3.shape[1] > 14 else 0.0,
        "duration": round(float(result.duration_s), 1),
    }

    # ── Step 7: Compute genes from dimensions ─────────────────────
    dims_6d = result.dim_6d.mean(axis=0)   # (6,)
    dims_12d = result.dim_12d.mean(axis=0)  # (12,)
    dims_24d = result.dim_24d.mean(axis=0)  # (24,)

    genes = {
        "entropy": round(float(dims_12d[1]) if len(dims_12d) > 1 else 0.5, 4),
        "resolution": round(float(dims_12d[7]) if len(dims_12d) > 7 else 0.5, 4),
        "tension": round(float(dims_12d[2]) if len(dims_12d) > 2 else 0.5, 4),
        "resonance": round(float(dims_12d[8]) if len(dims_12d) > 8 else 0.5, 4),
        "plasticity": round(float(dims_12d[5]) if len(dims_12d) > 5 else 0.5, 4),
    }

    gene_names = list(genes.keys())
    gene_vals = list(genes.values())
    dominant_gene = gene_names[np.argmax(gene_vals)]

    GENE_TO_FAMILY = {
        "entropy": "Explorers",
        "resolution": "Architects",
        "tension": "Seekers",
        "resonance": "Resonants",
        "plasticity": "Kineticists",
    }
    dominant_family = GENE_TO_FAMILY[dominant_gene]

    # ── Step 8: Compute function scores (F1-F9) ──────────────────
    belief_means = result.beliefs.mean(axis=0)  # (131,)
    belief_stds = result.beliefs.std(axis=0)    # (131,)
    function_ranges = {
        "F1": (0, 17), "F2": (17, 32), "F3": (32, 47),
        "F4": (47, 60), "F5": (60, 74), "F6": (74, 90),
        "F7": (90, 107), "F8": (107, 121), "F9": (121, 131),
    }
    functions = {}
    for fn, (start, end) in function_ranges.items():
        functions[fn] = round(float(belief_means[start:end].mean()), 4)

    # ── Step 9: Build track detail JSON ───────────────────────────
    track_json = {
        "id": TRACK_ID,
        "filename": WAV_PATH.name,
        "artist": ARTIST,
        "title": TITLE,
        "categories": CATEGORIES,
        "duration_s": round(float(result.duration_s), 1),
        "n_frames": int(result.n_frames),
        "fps": round(float(result.fps), 2),
        "signal": signal,
        "genes": genes,
        "dominant_gene": dominant_gene,
        "dominant_family": dominant_family,
        # ── Belief summary ────────────────────────────────────
        "beliefs": {
            "means": _round_list(belief_means),
            "stds": _round_list(belief_stds),
        },
        # ── Dimension summary ─────────────────────────────────
        "dimensions": {
            "psychology_6d": _round_list(dims_6d),
            "cognition_12d": _round_list(dims_12d),
            "neuroscience_24d": _round_list(dims_24d),
        },
        # ── Function scores ───────────────────────────────────
        "functions": functions,
        # ── RAM summary ───────────────────────────────────────
        "ram_26d": {
            "means": _round_list(result.ram.mean(axis=0)),
            "stds": _round_list(result.ram.std(axis=0)),
        },
        # ── Neurochemicals summary ────────────────────────────
        "neuro_4d": {
            "DA": round(float(result.neuro[:, 0].mean()), 4),
            "NE": round(float(result.neuro[:, 1].mean()), 4),
            "OPI": round(float(result.neuro[:, 2].mean()), 4),
            "5HT": round(float(result.neuro[:, 3].mean()), 4),
        },
        # ── Reward summary ────────────────────────────────────
        "reward": {
            "mean": round(float(result.reward.mean()), 4),
            "std": round(float(result.reward.std()), 4),
            "max": round(float(result.reward.max()), 4),
            "min": round(float(result.reward.min()), 4),
        },
        # ── Temporal profiles (64 segments) ───────────────────
        "temporal_profile": {
            "segments": N_SEGMENTS,
            "belief_means_per_segment": _round_matrix(belief_segs),
            "dim_6d_per_segment": _round_matrix(dim6_segs),
            "dim_12d_per_segment": _round_matrix(dim12_segs),
            "dim_24d_per_segment": _round_matrix(dim24_segs),
            "neuro_per_segment": _round_matrix(neuro_segs),
            "ram_per_segment": _round_matrix(ram_segs),
            "reward_per_segment": _round_list(reward_segs),
        },
        # ── Frame data reference ──────────────────────────────
        "frames_file": f"{TRACK_ID}_frames.npz",
    }

    # ── Step 10: Save track JSON ──────────────────────────────────
    for tracks_dir in [TRACKS_DIR, DIST_TRACKS_DIR]:
        tracks_dir.mkdir(parents=True, exist_ok=True)
        out_path = tracks_dir / f"{TRACK_ID}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(track_json, f, indent=2, ensure_ascii=False)
        sz = out_path.stat().st_size
        print(f"[Swan Lake] Saved: {out_path} ({sz/1024:.1f} KB)")

    # ── Step 11: Update catalog.json ──────────────────────────────
    catalog_entry = {
        "id": TRACK_ID,
        "filename": WAV_PATH.name,
        "artist": ARTIST,
        "title": TITLE,
        "categories": CATEGORIES,
        "duration_s": track_json["duration_s"],
        "signal": signal,
        "genes": genes,
        "dimensions_6d": track_json["dimensions"]["psychology_6d"],
        "dominant_family": dominant_family,
        "dominant_gene": dominant_gene,
    }

    for cat_path in [CATALOG_PATH, DIST_CATALOG_PATH]:
        if not cat_path.exists():
            print(f"[Swan Lake] WARNING: Catalog not found: {cat_path}")
            continue

        with open(cat_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        tracks = catalog.get("tracks", [])
        tracks = [t for t in tracks if t["id"] != TRACK_ID]
        tracks.append(catalog_entry)
        catalog["tracks"] = tracks
        catalog["total_tracks"] = len(tracks)

        with open(cat_path, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"[Swan Lake] Catalog updated: {cat_path} ({len(tracks)} tracks)")

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "=" * 70)
    print("Swan Lake — Complete Analysis Summary")
    print("=" * 70)
    print(f"  Duration:    {result.duration_s:.1f}s ({result.n_frames} frames @ {result.fps:.1f} fps)")
    print(f"  Gene:        {dominant_gene} → {dominant_family}")
    print(f"  6D:          {_round_list(dims_6d, 3)}")
    print(f"  12D:         {_round_list(dims_12d, 3)}")
    print(f"  Neuro:       DA={track_json['neuro_4d']['DA']:.3f}  "
          f"NE={track_json['neuro_4d']['NE']:.3f}  "
          f"OPI={track_json['neuro_4d']['OPI']:.3f}  "
          f"5HT={track_json['neuro_4d']['5HT']:.3f}")
    print(f"  Reward:      mean={track_json['reward']['mean']:.3f}  "
          f"max={track_json['reward']['max']:.3f}")
    print(f"  Functions:   " + "  ".join(f"{k}={v:.2f}" for k, v in functions.items()))
    print(f"  Temporal:    {N_SEGMENTS} segments × (beliefs+dims+neuro+ram+reward)")
    print(f"  Frame data:  {TRACK_ID}_frames.npz")
    print("=" * 70)


if __name__ == "__main__":
    main()
