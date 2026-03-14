#!/usr/bin/env python3
"""Batch corpus analysis: run R³→H³→C³→beliefs on all classical segments.

Collects per-mechanism-dim statistics across the entire corpus for
corpus-based normalization. Then recomputes beliefs + 5+5 dimensions
using corpus stats instead of per-piece percentile stretch.

Output:
    corpus_stats.npz  — per-mechanism-dim mean/std/p2/p98 from full corpus
    corpus_5d_results.json — 5+5 dimensions for every segment
"""
from __future__ import annotations

import importlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

import numpy as np
import torch
from torch import Tensor

# ── Constants ──────────────────────────────────────────────────────────
SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048
FRAME_RATE = SAMPLE_RATE / HOP_LENGTH  # 172.27 Hz
TARGET_FPS = 10

PROJECT_ROOT = Path(__file__).resolve().parent
SEGMENTS_DIR = PROJECT_ROOT / "Legacy" / "test-classics" / "segments"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
APP_BACKEND = PROJECT_ROOT / "My Musical Mind (Test-01)" / "backend"
if str(APP_BACKEND) not in sys.path:
    sys.path.insert(0, str(APP_BACKEND))


# ── Audio loading ──────────────────────────────────────────────────────

def load_audio(filepath: Path) -> Tuple[Tensor, Tensor, float]:
    """Load audio → (waveform, mel, duration_s) via ffmpeg."""
    cmd = [
        "ffmpeg", "-i", str(filepath),
        "-f", "f32le", "-acodec", "pcm_f32le",
        "-ar", str(SAMPLE_RATE), "-ac", "1",
        "-v", "quiet", "-",
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=60)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed on {filepath.name}")

    samples = np.frombuffer(result.stdout, dtype=np.float32)
    if len(samples) == 0:
        raise RuntimeError(f"Empty audio: {filepath.name}")
    waveform = torch.from_numpy(samples.copy()).unsqueeze(0)
    duration_s = waveform.shape[-1] / SAMPLE_RATE

    pad_len = N_FFT // 2
    edge_l = waveform[:, :1].expand(-1, pad_len)
    edge_r = waveform[:, -1:].expand(-1, pad_len)
    waveform_padded = torch.cat([edge_l, waveform, edge_r], dim=-1)

    import torchaudio
    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE, n_fft=N_FFT,
        hop_length=HOP_LENGTH, n_mels=N_MELS, power=2.0,
    )
    mel = mel_transform(waveform_padded)
    pad_frames = pad_len // HOP_LENGTH
    mel = mel[:, :, pad_frames: mel.shape[-1] - pad_frames]
    mel = torch.log1p(mel)
    mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
    mel = mel / mel_max
    return waveform, mel, duration_s


# ── Mechanism collection ──────────────────────────────────────────────

_FUNCTION_IDS = ("f1", "f2", "f3", "f4", "f5", "f6", "f7", "f8", "f9")
_ROLE_TO_DEPTH = {"relay": 0, "encoder": 1, "associator": 2, "integrator": 3, "hub": 4}


def collect_mechanisms() -> List[Any]:
    from Musical_Intelligence.contracts.bases.nucleus import _NucleusBase
    instances = []
    for fn in _FUNCTION_IDS:
        mod_path = f"Musical_Intelligence.brain.functions.{fn}.mechanisms"
        try:
            mod = importlib.import_module(mod_path)
            for name in getattr(mod, "__all__", []):
                cls = getattr(mod, name, None)
                if cls and isinstance(cls, type) and issubclass(cls, _NucleusBase):
                    try:
                        instances.append(cls())
                    except Exception:
                        pass
        except Exception:
            pkg_dir = PROJECT_ROOT / "Musical_Intelligence" / "brain" / "functions" / fn / "mechanisms"
            if not pkg_dir.is_dir():
                continue
            for sub in sorted(pkg_dir.iterdir()):
                if not sub.is_dir() or sub.name.startswith(("_", ".")):
                    continue
                try:
                    sub_mod = importlib.import_module(f"{mod_path}.{sub.name}")
                except Exception:
                    continue
                for attr_name in dir(sub_mod):
                    attr = getattr(sub_mod, attr_name, None)
                    if attr and isinstance(attr, type) and issubclass(attr, _NucleusBase) and attr is not _NucleusBase:
                        try:
                            instances.append(attr())
                        except Exception:
                            pass
    return instances


def fix_depths(nuclei):
    for n in nuclei:
        role = getattr(n, "ROLE", "relay")
        min_depth = _ROLE_TO_DEPTH.get(role, 0)
        if n.PROCESSING_DEPTH < min_depth:
            n.PROCESSING_DEPTH = min_depth


# ── Main ──────────────────────────────────────────────────────────────

def main():
    segments = sorted(SEGMENTS_DIR.glob("*.mp3"))
    print(f"Found {len(segments)} segments")

    # Initialize pipeline once
    print("Initializing pipeline...")
    nuclei = collect_mechanisms()
    fix_depths(nuclei)

    h3_demand: Set[Tuple[int, int, int, int]] = set()
    for m in nuclei:
        for spec in m.h3_demand:
            h3_demand.add(spec.as_tuple())

    from Musical_Intelligence.ear.r3 import R3Extractor
    from Musical_Intelligence.ear.h3 import H3Extractor
    from Musical_Intelligence.brain.executor import execute
    from beliefs import compute_beliefs, build_dim_lookup, get_beliefs_registry

    r3_extractor = R3Extractor()
    h3_extractor = H3Extractor()
    print(f"Ready: {len(nuclei)} mechanisms, {len(h3_demand)} H³ demands\n")

    # ── Pass 1: Collect raw mechanism stats across corpus ──────────
    print("=" * 60)
    print("PASS 1: Collecting mechanism-level statistics")
    print("=" * 60)

    # We'll collect all values per (mechanism, dim) using Welford's online algorithm
    # to avoid memory issues with 1570 segments
    mech_dim_info: Dict[str, int] = {}  # name → n_dims
    mech_running_stats: Dict[str, Dict[str, Any]] = {}  # name → {count, mean, M2, min_vals, max_vals, p2_reservoir, p98_reservoir}

    # First, discover mechanism dims from first segment
    print(f"[1/{len(segments)}] Discovering mechanism dims...")
    waveform, mel, dur = load_audio(segments[0])
    with torch.no_grad():
        r3_out = r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
        h3_out = h3_extractor.extract(r3_out.features, h3_demand)
        outputs, _, _ = execute(nuclei, h3_out.features, r3_out.features)

    # We'll store per-dim percentiles using reservoir sampling
    # But simpler: just collect all values in lists (929 dims × ~4000 frames × 1570 segs ≈ too much)
    # Instead: use online percentile approximation with P² or t-digest
    # Simplest viable: collect p2 and p98 per segment, then take median of those
    mech_names_ordered = sorted(outputs.keys())
    for name in mech_names_ordered:
        d = outputs[name].shape[-1]
        mech_dim_info[name] = d

    total_mech_dims = sum(mech_dim_info.values())
    print(f"  {len(mech_dim_info)} mechanisms, {total_mech_dims} total dims\n")

    # Collect per-segment p2/p98 for each mechanism dim
    seg_p2: Dict[str, List[np.ndarray]] = {n: [] for n in mech_names_ordered}
    seg_p98: Dict[str, List[np.ndarray]] = {n: [] for n in mech_names_ordered}
    seg_mean: Dict[str, List[np.ndarray]] = {n: [] for n in mech_names_ordered}
    seg_std: Dict[str, List[np.ndarray]] = {n: [] for n in mech_names_ordered}

    t0 = time.perf_counter()
    failed = []

    for i, seg_path in enumerate(segments):
        try:
            waveform, mel, dur = load_audio(seg_path)
            with torch.no_grad():
                r3_out = r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
                h3_out = h3_extractor.extract(r3_out.features, h3_demand)
                outputs, _, _ = execute(nuclei, h3_out.features, r3_out.features)

            for name in mech_names_ordered:
                if name in outputs:
                    data = outputs[name][0].cpu().numpy()  # (T, D)
                    seg_p2[name].append(np.percentile(data, 2, axis=0))
                    seg_p98[name].append(np.percentile(data, 98, axis=0))
                    seg_mean[name].append(data.mean(axis=0))
                    seg_std[name].append(data.std(axis=0))

            elapsed = time.perf_counter() - t0
            rate = (i + 1) / elapsed
            eta = (len(segments) - i - 1) / rate
            if (i + 1) % 50 == 0 or i == 0:
                print(f"  [{i+1:4d}/{len(segments)}]  {rate:.1f} seg/s  ETA {eta:.0f}s  ({seg_path.name[:40]})")

        except Exception as e:
            failed.append((seg_path.name, str(e)))
            if len(failed) <= 5:
                print(f"  [{i+1:4d}] FAILED: {seg_path.name[:50]} — {e}")

    elapsed_p1 = time.perf_counter() - t0
    print(f"\nPass 1 done: {len(segments) - len(failed)}/{len(segments)} OK in {elapsed_p1:.0f}s")
    if failed:
        print(f"  {len(failed)} failures")

    # ── Compute corpus-wide stats ──────────────────────────────────
    print("\nComputing corpus-wide mechanism stats...")
    corpus_p2 = {}
    corpus_p98 = {}
    corpus_mean = {}
    corpus_std = {}

    for name in mech_names_ordered:
        if seg_p2[name]:
            p2_all = np.stack(seg_p2[name])   # (N_segs, D)
            p98_all = np.stack(seg_p98[name])
            mean_all = np.stack(seg_mean[name])
            std_all = np.stack(seg_std[name])

            # Corpus floor/ceiling = median of per-segment percentiles
            corpus_p2[name] = np.median(p2_all, axis=0)
            corpus_p98[name] = np.median(p98_all, axis=0)
            corpus_mean[name] = mean_all.mean(axis=0)
            corpus_std[name] = std_all.mean(axis=0)

    # Save corpus stats
    stats_path = PROJECT_ROOT / "corpus_mech_stats.npz"
    save_dict = {}
    for name in mech_names_ordered:
        if name in corpus_p2:
            save_dict[f"{name}_p2"] = corpus_p2[name]
            save_dict[f"{name}_p98"] = corpus_p98[name]
            save_dict[f"{name}_mean"] = corpus_mean[name]
            save_dict[f"{name}_std"] = corpus_std[name]
    save_dict["mechanism_names"] = np.array(mech_names_ordered)
    np.savez_compressed(stats_path, **save_dict)
    print(f"Corpus stats saved: {stats_path}")

    # Print summary
    print(f"\n{'Mechanism':12s} {'Dims':>4s}  {'Corpus p2':>10s}  {'Corpus p98':>10s}  {'Range':>10s}")
    print("-" * 55)
    for name in mech_names_ordered[:20]:
        if name in corpus_p2:
            p2_mean = corpus_p2[name].mean()
            p98_mean = corpus_p98[name].mean()
            rng = p98_mean - p2_mean
            print(f"{name:12s} {mech_dim_info.get(name, 0):4d}  {p2_mean:10.4f}  {p98_mean:10.4f}  {rng:10.4f}")
    if len(mech_names_ordered) > 20:
        print(f"  ... and {len(mech_names_ordered) - 20} more")

    # ── Pass 2: Recompute beliefs + 5+5 with corpus normalization ──
    print("\n" + "=" * 60)
    print("PASS 2: Computing 5+5 dimensions with corpus normalization")
    print("=" * 60)

    from Musical_Intelligence.brain.dimensions import DimensionInterpreter
    from Musical_Intelligence.brain.dimensions.models.musical import MUSICAL_NAMES
    from Musical_Intelligence.brain.dimensions.models.emotional import EMOTIONAL_NAMES

    dim_interp = DimensionInterpreter()
    beliefs_reg = get_beliefs_registry()
    dim_lookup = build_dim_lookup(nuclei)

    all_results = []
    # Collect global 5+5 stats
    all_musical = []
    all_emotional = []

    t1 = time.perf_counter()

    for i, seg_path in enumerate(segments):
        try:
            waveform, mel, dur = load_audio(seg_path)
            with torch.no_grad():
                r3_out = r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
                h3_out = h3_extractor.extract(r3_out.features, h3_demand)
                outputs, _, _ = execute(nuclei, h3_out.features, r3_out.features)

            # Corpus-normalize mechanism outputs
            relays = {}
            for n in nuclei:
                if n.NAME in outputs:
                    data = outputs[n.NAME][0].cpu().numpy()
                    if n.NAME in corpus_p2:
                        lo = corpus_p2[n.NAME]
                        hi = corpus_p98[n.NAME]
                        rng = hi - lo
                        mask = rng >= 0.01
                        out = data.copy()
                        for d in range(data.shape[1]):
                            if mask[d]:
                                out[:, d] = np.clip((data[:, d] - lo[d]) / rng[d], 0.0, 1.0)
                        relays[n.NAME] = out
                    else:
                        relays[n.NAME] = data

            # Compute beliefs (normalize=False, already corpus-normed)
            beliefs = compute_beliefs(relays, nuclei, normalize=False)

            # 5+5 dimensions
            dim_result = dim_interp.interpret_numpy(beliefs)
            musical_5d = dim_result["musical_5d"]
            emotional_5d = dim_result["emotional_5d"]

            all_musical.append(musical_5d)
            all_emotional.append(emotional_5d)

            # Resample to 10fps
            def resample(data, native_fps, target_fps):
                T, D = data.shape
                w = max(1, int(round(native_fps / target_fps)))
                n = T // w
                if n == 0:
                    return data[:1]
                return data[:n * w].reshape(n, w, D).mean(axis=1)

            m10 = resample(musical_5d, FRAME_RATE, TARGET_FPS)
            e10 = resample(emotional_5d, FRAME_RATE, TARGET_FPS)

            # Parse piece name
            fname = seg_path.stem
            piece = fname.rsplit("__", 1)[0] if "__" in fname else fname
            seg_id = fname.rsplit("__", 1)[1] if "__" in fname else "full"

            all_results.append({
                "file": seg_path.name,
                "piece": piece,
                "segment": seg_id,
                "duration_s": round(dur, 2),
                "n_frames": m10.shape[0],
                "musical_mean": {MUSICAL_NAMES[j]: round(float(m10[:, j].mean()), 4) for j in range(5)},
                "emotional_mean": {EMOTIONAL_NAMES[j]: round(float(e10[:, j].mean()), 4) for j in range(5)},
                "musical_std": {MUSICAL_NAMES[j]: round(float(m10[:, j].std()), 4) for j in range(5)},
                "emotional_std": {EMOTIONAL_NAMES[j]: round(float(e10[:, j].std()), 4) for j in range(5)},
            })

            elapsed = time.perf_counter() - t1
            rate = (i + 1) / elapsed
            eta = (len(segments) - i - 1) / rate
            if (i + 1) % 100 == 0 or i == 0:
                print(f"  [{i+1:4d}/{len(segments)}]  {rate:.1f} seg/s  ETA {eta:.0f}s")

        except Exception as e:
            if (i + 1) <= 5:
                print(f"  [{i+1:4d}] FAILED: {seg_path.name[:50]} — {e}")

    elapsed_p2 = time.perf_counter() - t1
    print(f"\nPass 2 done in {elapsed_p2:.0f}s")

    # ── Save results ───────────────────────────────────────────────
    output = {
        "corpus": "classical-segments",
        "n_segments": len(all_results),
        "n_pieces": len(set(r["piece"] for r in all_results)),
        "normalization": "corpus-based mechanism-level (median p2/p98)",
        "fps": TARGET_FPS,
        "segments": all_results,
    }

    out_path = PROJECT_ROOT / "corpus_5d_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved: {out_path}")

    # ── Corpus-wide 5+5 summary ───────────────────────────────────
    if all_musical:
        all_m = np.concatenate(all_musical, axis=0)
        all_e = np.concatenate(all_emotional, axis=0)

        print("\n" + "=" * 60)
        print("CORPUS-WIDE 5+5 STATISTICS (all frames pooled)")
        print("=" * 60)

        print(f"\nMusical 5D ({all_m.shape[0]} total frames):")
        for j, name in enumerate(MUSICAL_NAMES):
            col = all_m[:, j]
            print(f"  {name:16s}  mean={col.mean():.3f}  std={col.std():.3f}  "
                  f"p2={np.percentile(col, 2):.3f}  p98={np.percentile(col, 98):.3f}  "
                  f"min={col.min():.3f}  max={col.max():.3f}")

        print(f"\nEmotional 5D ({all_e.shape[0]} total frames):")
        for j, name in enumerate(EMOTIONAL_NAMES):
            col = all_e[:, j]
            print(f"  {name:16s}  mean={col.mean():.3f}  std={col.std():.3f}  "
                  f"p2={np.percentile(col, 2):.3f}  p98={np.percentile(col, 98):.3f}  "
                  f"min={col.min():.3f}  max={col.max():.3f}")

    total = time.perf_counter() - t0
    print(f"\nTotal time: {total:.0f}s ({total/60:.1f}min)")


if __name__ == "__main__":
    main()
