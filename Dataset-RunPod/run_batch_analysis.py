#!/usr/bin/env python3
"""Batch MI analysis for all dataset tracks on RunPod.

Runs the full R³ → H³ → C³ pipeline on every MP3 in the dataset directory.
Saves per-track JSON with complete analysis + NPZ with frame-level data.

Usage (on RunPod):
    cd /workspace/MI
    python Dataset-RunPod/run_batch_analysis.py \
        --input /workspace/dataset \
        --output /workspace/results \
        --workers 1 \
        --excerpt 30.0

Output per track:
    results/
    ├── Artist - Title.json          ← summary (beliefs, dims, neuro, reward, genes, temporal)
    ├── Artist - Title_frames.npz    ← frame-level binary (beliefs, r3, ram, neuro, reward, dims)
    └── ...
    ├── catalog.json                 ← master catalog of all analyzed tracks
    └── errors.json                  ← any failed tracks
"""
from __future__ import annotations

import argparse
import gc
import json
import sys
import time
import traceback
from pathlib import Path

import numpy as np

# Ensure project root on path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

N_SEGMENTS = 64  # temporal profile resolution


# ── Helpers ──────────────────────────────────────────────────────────

def _seg_stats(data, n_seg):
    """Segment a (T, D) array into n_seg bins, return means."""
    T = data.shape[0]
    if T < n_seg:
        n_seg = T
    seg_size = T // n_seg
    out = []
    for s in range(n_seg):
        start = s * seg_size
        end = (s + 1) * seg_size if s < n_seg - 1 else T
        out.append(data[start:end].mean(axis=0))
    return np.array(out)


def _round_list(arr, decimals=4):
    return [round(float(v), decimals) for v in arr]


def _round_matrix(mat, decimals=4):
    return [_round_list(row, decimals) for row in mat]


# ── Gene computation (mirrors run_swan_lake.py / useM3Store.ts) ──────

GENE_TO_FAMILY = {
    "entropy": "Explorers",
    "resolution": "Architects",
    "tension": "Alchemists",
    "resonance": "Anchors",
    "plasticity": "Kineticists",
}

FUNCTION_RANGES = {
    "F1": (0, 17), "F2": (17, 32), "F3": (32, 47),
    "F4": (47, 60), "F5": (60, 74), "F6": (74, 90),
    "F7": (90, 107), "F8": (107, 121), "F9": (121, 131),
}


def compute_signal(r3, duration_s):
    """Compute signal features from R³ (97D)."""
    return {
        "energy": round(float(r3[:, 7:12].mean()), 4),
        "valence": round(float(r3[:, 51:63].mean()), 4),
        "tempo": round(float(r3[:, 41:51].mean() * 200), 1),
        "danceability": round(float(r3[:, 41:51].mean()), 4),
        "acousticness": round(float(1.0 - r3[:, 12:21].mean()), 4),
        "harmonicComplexity": round(float(r3[:, 51:63].std()), 4),
        "timbralBrightness": round(float(r3[:, 14].mean()), 4),
        "duration": round(float(duration_s), 1),
    }


def compute_genes(signal):
    """Compute musical genes from signal features."""
    energy = signal["energy"]
    valence = signal["valence"]
    tempo = signal["tempo"]
    danceability = signal["danceability"]
    acousticness = signal["acousticness"]
    hc = signal["harmonicComplexity"]
    tempo_norm = min(1.0, tempo / 200.0)

    genes = {
        "entropy": round(float(np.clip(
            (1 - acousticness) * 0.25 + energy * 0.15 + danceability * 0.15 + 0.05
            + (0.15 if tempo_norm > 0.6 else 0.05) + hc * 0.1, 0, 1)), 4),
        "resolution": round(float(np.clip(
            (1 - energy) * 0.25 + acousticness * 0.25 + hc * 0.2
            + (1 - abs(valence - 0.5) * 2) * 0.2 + (0.1 if tempo_norm < 0.5 else 0.0), 0, 1)), 4),
        "tension": round(float(np.clip(
            energy * 0.2 + (1 - valence) * 0.15 + abs(energy - 0.5) * 2 * 0.25
            + hc * 0.15 + (0.15 if tempo_norm > 0.5 else 0.05), 0, 1)), 4),
        "resonance": round(float(np.clip(
            valence * 0.15 + acousticness * 0.25 + (1 - energy) * 0.2
            + (0.2 if tempo_norm < 0.45 else 0.1) + 0.05, 0, 1)), 4),
        "plasticity": round(float(np.clip(
            danceability * 0.3 + energy * 0.2 + (0.2 if tempo_norm > 0.55 else 0.1)
            + (1 - acousticness) * 0.1 + (1 - abs(valence - 0.5) * 2) * 0.1, 0, 1)), 4),
    }
    gene_names = list(genes.keys())
    gene_vals = list(genes.values())
    dominant_gene = gene_names[int(np.argmax(gene_vals))]
    dominant_family = GENE_TO_FAMILY[dominant_gene]
    return genes, dominant_gene, dominant_family


# ── Ψ³ domain names ─────────────────────────────────────────────────

PSI_DOMAIN_LABELS = {
    "affect": ["valence", "arousal", "tension", "dominance"],
    "emotion": ["joy", "sadness", "fear", "awe", "nostalgia", "tenderness", "serenity"],
    "aesthetic": ["beauty", "groove", "flow", "surprise", "closure"],
    "bodily": ["chills", "movement_urge", "breathing_change", "tension_release"],
    "cognitive": ["familiarity", "absorption", "expectation", "attention_focus"],
    "temporal": ["anticipation", "resolution", "buildup", "release"],
}


# ── Build track JSON ─────────────────────────────────────────────────

def build_track_json(result, meta, stem):
    """Build comprehensive track JSON from ExperimentResult + metadata."""
    r3 = result.r3
    T = result.beliefs.shape[0]

    # Signal & genes
    signal = compute_signal(r3, result.duration_s)
    genes, dominant_gene, dominant_family = compute_genes(signal)

    # Belief stats
    belief_means = result.beliefs.mean(axis=0)
    belief_stds = result.beliefs.std(axis=0)

    # Function scores
    functions = {}
    for fn, (start, end) in FUNCTION_RANGES.items():
        functions[fn] = round(float(belief_means[start:end].mean()), 4)

    # Dimension means
    dims_6d = result.dim_6d.mean(axis=0)
    dims_12d = result.dim_12d.mean(axis=0)
    dims_24d = result.dim_24d.mean(axis=0)

    # Temporal profiles
    belief_segs = _seg_stats(result.beliefs, N_SEGMENTS)
    neuro_segs = _seg_stats(result.neuro, N_SEGMENTS)
    ram_segs = _seg_stats(result.ram, N_SEGMENTS)
    reward_segs = _seg_stats(result.reward.reshape(-1, 1), N_SEGMENTS)[:, 0]
    dim6_segs = _seg_stats(result.dim_6d, N_SEGMENTS)
    dim12_segs = _seg_stats(result.dim_12d, N_SEGMENTS)
    dim24_segs = _seg_stats(result.dim_24d, N_SEGMENTS)

    # Ψ³ domain summaries
    psi_summary = {}
    for domain, labels in PSI_DOMAIN_LABELS.items():
        if domain in result.psi:
            arr = result.psi[domain]  # (T, D)
            means = arr.mean(axis=0)
            psi_summary[domain] = {
                labels[i]: round(float(means[i]), 4)
                for i in range(min(len(labels), len(means)))
            }

    track_json = {
        # ── Identity ─────────────────────────────────────────
        "id": stem,
        "filename": f"{stem}.mp3",
        "artist": meta.get("artist", ""),
        "title": meta.get("title", ""),
        "album": meta.get("album", ""),
        "genre": meta.get("genre", ""),
        "deezer_id": meta.get("deezer_id"),
        "duration_original_s": meta.get("duration", 0),
        "cover_url": meta.get("cover_url", ""),

        # ── Pipeline metadata ────────────────────────────────
        "duration_analyzed_s": round(float(result.duration_s), 2),
        "n_frames": int(result.n_frames),
        "fps": round(float(result.fps), 2),

        # ── R³ signal features ───────────────────────────────
        "signal": signal,

        # ── Musical genes ────────────────────────────────────
        "genes": genes,
        "dominant_gene": dominant_gene,
        "dominant_family": dominant_family,

        # ── C³ beliefs (131D) ────────────────────────────────
        "beliefs": {
            "means": _round_list(belief_means),
            "stds": _round_list(belief_stds),
        },

        # ── Function scores (F1-F9) ─────────────────────────
        "functions": functions,

        # ── Hierarchical dimensions ──────────────────────────
        "dimensions": {
            "psychology_6d": _round_list(dims_6d),
            "cognition_12d": _round_list(dims_12d),
            "neuroscience_24d": _round_list(dims_24d),
        },

        # ── Ψ³ cognitive domains ─────────────────────────────
        "psi": psi_summary,

        # ── RAM (26 brain regions) ───────────────────────────
        "ram_26d": {
            "means": _round_list(result.ram.mean(axis=0)),
            "stds": _round_list(result.ram.std(axis=0)),
        },

        # ── Neurochemicals (DA, NE, OPI, 5HT) ───────────────
        "neuro_4d": {
            "DA": round(float(result.neuro[:, 0].mean()), 4),
            "NE": round(float(result.neuro[:, 1].mean()), 4),
            "OPI": round(float(result.neuro[:, 2].mean()), 4),
            "5HT": round(float(result.neuro[:, 3].mean()), 4),
        },

        # ── Reward ───────────────────────────────────────────
        "reward": {
            "mean": round(float(result.reward.mean()), 4),
            "std": round(float(result.reward.std()), 4),
            "max": round(float(result.reward.max()), 4),
            "min": round(float(result.reward.min()), 4),
        },

        # ── Temporal profiles (64 segments) ──────────────────
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

        # ── Frame data reference ─────────────────────────────
        "frames_file": f"{stem}_frames.npz",
    }

    return track_json


# ── Main ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Batch MI analysis on RunPod")
    parser.add_argument("--input", "-i", type=str, default="/workspace/dataset",
                        help="Input directory with MP3 + JSON files")
    parser.add_argument("--output", "-o", type=str, default="/workspace/results",
                        help="Output directory for analysis results")
    parser.add_argument("--excerpt", "-e", type=float, default=30.0,
                        help="Max audio duration in seconds (default: 30.0, 0=full)")
    parser.add_argument("--resume", action="store_true",
                        help="Skip already-analyzed tracks")
    args = parser.parse_args()

    input_dir = Path(args.input)
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    excerpt_s = args.excerpt if args.excerpt > 0 else None

    # Discover tracks (skip macOS resource fork files)
    mp3_files = sorted(f for f in input_dir.glob("*.mp3") if not f.name.startswith("._"))
    print(f"[Batch] Input:   {input_dir}")
    print(f"[Batch] Output:  {output_dir}")
    print(f"[Batch] Tracks:  {len(mp3_files)}")
    print(f"[Batch] Excerpt: {excerpt_s or 'full'}s")
    print()

    if not mp3_files:
        print("[Batch] No MP3 files found!")
        return

    # Filter already done if --resume
    if args.resume:
        todo = []
        for mp3 in mp3_files:
            json_out = output_dir / f"{mp3.stem}.json"
            if json_out.exists():
                continue
            todo.append(mp3)
        print(f"[Batch] Resume: {len(mp3_files) - len(todo)} already done, {len(todo)} remaining")
        mp3_files = todo

    # Initialize pipeline once
    print("[Batch] Initializing MI Pipeline...")
    t0 = time.perf_counter()

    from Lab.backend.config import AUDIO_CATALOG, AUDIO_DIR
    from Lab.backend.pipeline import MIPipeline

    pipeline = MIPipeline()
    print(f"[Batch] Pipeline ready in {time.perf_counter() - t0:.1f}s\n")

    # Process tracks
    success = 0
    failed = 0
    errors = []
    catalog_entries = []
    t_start = time.perf_counter()

    for i, mp3_path in enumerate(mp3_files):
        stem = mp3_path.stem
        json_out = output_dir / f"{stem}.json"
        npz_out = output_dir / f"{stem}_frames.npz"

        # Load metadata
        meta_path = input_dir / f"{stem}.json"
        meta = {}
        if meta_path.exists():
            try:
                with open(meta_path, encoding="utf-8", errors="replace") as f:
                    meta = json.load(f)
            except (json.JSONDecodeError, UnicodeDecodeError):
                meta = {}

        # Register in audio catalog and redirect AUDIO_DIR to input directory.
        # _load_audio uses module-level AUDIO_DIR from both config and pipeline,
        # so we must patch both references.
        catalog_key = f"__batch_{i}"
        AUDIO_CATALOG[catalog_key] = mp3_path.name

        import Lab.backend.config as cfg
        import Lab.backend.pipeline as pipe_mod
        orig_cfg_dir = cfg.AUDIO_DIR
        orig_pipe_dir = pipe_mod.AUDIO_DIR
        cfg.AUDIO_DIR = input_dir
        pipe_mod.AUDIO_DIR = input_dir

        try:
            t1 = time.perf_counter()
            result = pipeline.run(catalog_key, excerpt_s=excerpt_s)
            elapsed = time.perf_counter() - t1

            # Build and save JSON
            track_json = build_track_json(result, meta, stem)
            with open(json_out, "w", encoding="utf-8") as f:
                json.dump(track_json, f, indent=2, ensure_ascii=False)

            # Save frame-level NPZ
            np.savez_compressed(
                npz_out,
                beliefs=result.beliefs.astype(np.float32),
                r3=result.r3.astype(np.float32),
                ram=result.ram.astype(np.float32),
                neuro=result.neuro.astype(np.float32),
                reward=result.reward.astype(np.float32),
                dim_6d=result.dim_6d.astype(np.float32),
                dim_12d=result.dim_12d.astype(np.float32),
                dim_24d=result.dim_24d.astype(np.float32),
            )

            # Catalog entry (lightweight)
            catalog_entries.append({
                "id": stem,
                "artist": meta.get("artist", ""),
                "title": meta.get("title", ""),
                "genre": meta.get("genre", ""),
                "deezer_id": meta.get("deezer_id"),
                "duration_s": track_json["duration_analyzed_s"],
                "dominant_gene": track_json["dominant_gene"],
                "dominant_family": track_json["dominant_family"],
                "reward_mean": track_json["reward"]["mean"],
                "functions": track_json["functions"],
                "signal": track_json["signal"],
                "dimensions_6d": track_json["dimensions"]["psychology_6d"],
            })

            success += 1
            rate = success / (time.perf_counter() - t_start)
            remaining = len(mp3_files) - (i + 1)
            eta = remaining / rate if rate > 0 else 0

            if (i + 1) % 10 == 0 or (i + 1) == len(mp3_files):
                print(f"  [{i+1}/{len(mp3_files)}] {stem[:60]}... "
                      f"{elapsed:.1f}s | ok={success} fail={failed} "
                      f"({rate:.1f}/min, ETA {eta:.0f}s)")

        except Exception as e:
            failed += 1
            err_msg = f"{type(e).__name__}: {e}"
            errors.append({"file": stem, "error": err_msg})
            print(f"  [{i+1}/{len(mp3_files)}] FAIL: {stem[:50]}... — {err_msg}")
            traceback.print_exc()

        finally:
            # Cleanup
            cfg.AUDIO_DIR = orig_cfg_dir
            pipe_mod.AUDIO_DIR = orig_pipe_dir
            AUDIO_CATALOG.pop(catalog_key, None)
            gc.collect()

    # Save master catalog
    total_elapsed = time.perf_counter() - t_start
    master_catalog = {
        "version": "1.0.0",
        "pipeline": "MI R³→H³→C³",
        "total_tracks": success,
        "total_failed": failed,
        "excerpt_s": excerpt_s,
        "analysis_time_s": round(total_elapsed, 1),
        "tracks": catalog_entries,
    }
    with open(output_dir / "catalog.json", "w", encoding="utf-8") as f:
        json.dump(master_catalog, f, indent=2, ensure_ascii=False)

    # Save errors
    if errors:
        with open(output_dir / "errors.json", "w", encoding="utf-8") as f:
            json.dump(errors, f, indent=2, ensure_ascii=False)

    # Summary
    print(f"\n{'='*70}")
    print(f"Batch Analysis Complete")
    print(f"{'='*70}")
    print(f"  Total:     {len(mp3_files)}")
    print(f"  Success:   {success}")
    print(f"  Failed:    {failed}")
    print(f"  Time:      {total_elapsed:.0f}s ({total_elapsed/60:.1f}min)")
    if success > 0:
        print(f"  Avg/track: {total_elapsed/success:.1f}s")
    print(f"  Output:    {output_dir}")
    print(f"  Catalog:   {output_dir / 'catalog.json'}")

    json_size = sum(f.stat().st_size for f in output_dir.glob("*.json"))
    npz_size = sum(f.stat().st_size for f in output_dir.glob("*.npz"))
    print(f"  JSON size: {json_size/1e6:.0f} MB")
    print(f"  NPZ size:  {npz_size/1e6:.0f} MB")
    print(f"  Total:     {(json_size+npz_size)/1e9:.2f} GB")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
