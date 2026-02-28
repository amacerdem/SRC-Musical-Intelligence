"""Run full MI pipeline on Swan Lake and export to My Musical Mind dataset format.

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
CATEGORIES = ["Classical", "Orchestral"]

MMM_DIR = PROJECT_ROOT / "My Musical Mind (Monetizing)"
TRACKS_DIR = MMM_DIR / "public" / "data" / "mi-dataset" / "tracks"
CATALOG_PATH = MMM_DIR / "public" / "data" / "mi-dataset" / "catalog.json"

# Also write to dist/ for immediate availability
DIST_TRACKS_DIR = MMM_DIR / "dist" / "data" / "mi-dataset" / "tracks"
DIST_CATALOG_PATH = MMM_DIR / "dist" / "data" / "mi-dataset" / "catalog.json"

N_SEGMENTS = 8  # temporal profile segments


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

    # ── Step 3: Run full pipeline (no excerpt limit for full piece) ─
    print("\n[Swan Lake] Running full pipeline (R³ → H³ → C³)...")
    t1 = time.perf_counter()

    def status_cb(phase, progress):
        bar = "█" * int(progress * 30) + "░" * (30 - int(progress * 30))
        print(f"  [{bar}] {phase} ({progress*100:.0f}%)", end="\r")

    result = pipeline.run("swan_lake_wav", excerpt_s=None, status_callback=status_cb)
    elapsed = time.perf_counter() - t1
    print(f"\n[Swan Lake] Pipeline complete: {result.n_frames} frames, "
          f"{result.duration_s:.1f}s, {result.fps:.1f} fps, {elapsed:.1f}s wall")

    # ── Step 4: Compute temporal profile (8 segments) ─────────────
    print("\n[Swan Lake] Computing temporal profile...")
    T = result.beliefs.shape[0]
    seg_size = T // N_SEGMENTS
    belief_means_per_segment = []
    for s in range(N_SEGMENTS):
        start = s * seg_size
        end = (s + 1) * seg_size if s < N_SEGMENTS - 1 else T
        seg_means = result.beliefs[start:end].mean(axis=0)
        belief_means_per_segment.append([round(float(v), 4) for v in seg_means])

    # ── Step 5: Compute signal features from R³ ──────────────────
    r3 = result.r3  # (T, 97)
    # R³ groups: A[0:7]=BCH, B[7:12]=Energy, C[12:21]=Timbre, D[21:25]=Change,
    #            F[25:41]=Pitch, G[41:51]=Rhythm, H[51:63]=Harmony, J[63:83]=ExtTimbre, K[83:97]=Modulation
    signal = {
        "energy": round(float(r3[:, 7:12].mean()), 4),
        "valence": round(float(r3[:, 51:63].mean()), 4),  # harmony proxy
        "tempo": round(float(r3[:, 41:51].mean() * 200), 1),  # rhythm scaled
        "danceability": round(float(r3[:, 41:51].mean()), 4),  # groove
        "acousticness": round(float(1.0 - r3[:, 12:21].mean()), 4),  # inverse brightness
        "harmonicComplexity": round(float(r3[:, 51:63].std()), 4),
        "timbralBrightness": round(float(r3[:, 14].mean()), 4) if r3.shape[1] > 14 else 0.0,
        "duration": round(float(result.duration_s), 1),
    }

    # ── Step 6: Compute genes from dimensions ─────────────────────
    dims_6d = result.dim_6d.mean(axis=0)  # (6,)
    dims_12d = result.dim_12d.mean(axis=0)  # (12,)
    dims_24d = result.dim_24d.mean(axis=0)  # (24,)

    # Genes: entropy, resolution, tension, resonance, plasticity
    # Map from dimensions following the pattern in existing data
    genes = {
        "entropy": round(float(dims_12d[1]) if len(dims_12d) > 1 else 0.5, 4),       # information_rate
        "resolution": round(float(dims_12d[7]) if len(dims_12d) > 7 else 0.5, 4),     # reward
        "tension": round(float(dims_12d[2]) if len(dims_12d) > 2 else 0.5, 4),        # tension_arc
        "resonance": round(float(dims_12d[8]) if len(dims_12d) > 8 else 0.5, 4),      # episodic_resonance
        "plasticity": round(float(dims_12d[5]) if len(dims_12d) > 5 else 0.5, 4),     # groove
    }

    # Dominant gene
    gene_names = list(genes.keys())
    gene_vals = list(genes.values())
    dominant_gene = gene_names[np.argmax(gene_vals)]

    # Dominant family mapping
    GENE_TO_FAMILY = {
        "entropy": "Explorers",
        "resolution": "Architects",
        "tension": "Seekers",
        "resonance": "Resonants",
        "plasticity": "Kineticists",
    }
    dominant_family = GENE_TO_FAMILY[dominant_gene]

    # ── Step 7: Compute function scores (F1-F9) ──────────────────
    # F1-F9 belief ranges: F1[0:17], F2[17:32], F3[32:47], F4[47:60],
    # F5[60:74], F6[74:90], F7[90:107], F8[107:121], F9[121:131]
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

    # ── Step 8: Build track detail JSON ───────────────────────────
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
        "beliefs": {
            "means": [round(float(v), 4) for v in belief_means],
            "stds": [round(float(v), 4) for v in belief_stds],
        },
        "dimensions": {
            "psychology_6d": [round(float(v), 4) for v in dims_6d],
            "cognition_12d": [round(float(v), 4) for v in dims_12d],
            "neuroscience_24d": [round(float(v), 4) for v in dims_24d],
        },
        "functions": functions,
        "ram_26d": {
            "means": [round(float(v), 4) for v in result.ram.mean(axis=0)],
            "stds": [round(float(v), 4) for v in result.ram.std(axis=0)],
        },
        "neuro_4d": {
            "DA": round(float(result.neuro[:, 0].mean()), 4),
            "NE": round(float(result.neuro[:, 1].mean()), 4),
            "OPI": round(float(result.neuro[:, 2].mean()), 4),
            "5HT": round(float(result.neuro[:, 3].mean()), 4),
        },
        "temporal_profile": {
            "segments": N_SEGMENTS,
            "belief_means_per_segment": belief_means_per_segment,
        },
    }

    # ── Step 9: Save track JSON ───────────────────────────────────
    for tracks_dir in [TRACKS_DIR, DIST_TRACKS_DIR]:
        tracks_dir.mkdir(parents=True, exist_ok=True)
        out_path = tracks_dir / f"{TRACK_ID}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(track_json, f, indent=2, ensure_ascii=False)
        print(f"[Swan Lake] Saved: {out_path}")

    # ── Step 10: Update catalog.json ──────────────────────────────
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

        # Remove existing entry if present
        tracks = catalog.get("tracks", [])
        tracks = [t for t in tracks if t["id"] != TRACK_ID]

        # Add new entry
        tracks.append(catalog_entry)
        catalog["tracks"] = tracks
        catalog["total_tracks"] = len(tracks)

        with open(cat_path, "w", encoding="utf-8") as f:
            json.dump(catalog, f, indent=2, ensure_ascii=False)
        print(f"[Swan Lake] Catalog updated: {cat_path} ({len(tracks)} tracks)")

    # ── Summary ───────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("Swan Lake Analysis Summary")
    print("=" * 60)
    print(f"  Duration:    {result.duration_s:.1f}s ({result.n_frames} frames)")
    print(f"  FPS:         {result.fps:.1f}")
    print(f"  Gene:        {dominant_gene} → {dominant_family}")
    print(f"  6D:          {[round(float(v), 3) for v in dims_6d]}")
    print(f"  Neuro:       DA={track_json['neuro_4d']['DA']:.3f}  "
          f"NE={track_json['neuro_4d']['NE']:.3f}  "
          f"OPI={track_json['neuro_4d']['OPI']:.3f}  "
          f"5HT={track_json['neuro_4d']['5HT']:.3f}")
    print(f"  Functions:   " + "  ".join(f"{k}={v:.2f}" for k, v in functions.items()))
    print("=" * 60)


if __name__ == "__main__":
    main()
