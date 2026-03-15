#!/usr/bin/env python3
"""Evaluate trained glass-box model — inference on audio, comparison with ground truth.

Usage:
    # Single file analysis
    python Training/evaluate.py --checkpoint Training/runs/v1/checkpoints/best.pt --audio song.mp3

    # Compare with ground truth (from MI pipeline)
    python Training/evaluate.py --checkpoint Training/runs/v1/checkpoints/best.pt --npz training_data/000002.npz

    # Batch evaluate on test set
    python Training/evaluate.py --checkpoint Training/runs/v1/checkpoints/best.pt --data-dir training_data --manifest test_manifest.json

    # Export predictions as JSON
    python Training/evaluate.py --checkpoint Training/runs/v1/checkpoints/best.pt --audio song.mp3 --export result.json
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np
import torch
import torch.nn as nn
from torch import Tensor

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Training.train import (
    GlassBoxMI, MIDataset,
    R3_GROUPS, R3_NAMES, BELIEF_NAMES, BELIEF_FUNCTIONS, DIM_NAMES,
    per_dim_mse, per_dim_mae, per_dim_corr,
)

SAMPLE_RATE = 44100
HOP_LENGTH = 256
N_MELS = 128
N_FFT = 2048


# ======================================================================
# AUDIO → MEL
# ======================================================================

def load_audio_to_mel(filepath: Path, device: torch.device) -> Tensor:
    """Load audio file → mel spectrogram tensor. Returns (1, 128, T)."""
    import torchaudio

    cmd = [
        "ffmpeg", "-i", str(filepath),
        "-f", "f32le", "-acodec", "pcm_f32le",
        "-ar", str(SAMPLE_RATE), "-ac", "1",
        "-v", "quiet", "-",
    ]
    result = subprocess.run(cmd, capture_output=True, timeout=120)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed on {filepath}")
    samples = np.frombuffer(result.stdout, dtype=np.float32)
    if len(samples) == 0:
        raise RuntimeError(f"Empty audio: {filepath}")

    waveform = torch.from_numpy(samples.copy()).unsqueeze(0)
    duration_s = waveform.shape[-1] / SAMPLE_RATE

    # Pad edges
    pad_len = N_FFT // 2
    edge_l = waveform[:, :1].expand(-1, pad_len)
    edge_r = waveform[:, -1:].expand(-1, pad_len)
    waveform_padded = torch.cat([edge_l, waveform, edge_r], dim=-1).to(device)

    mel_transform = torchaudio.transforms.MelSpectrogram(
        sample_rate=SAMPLE_RATE, n_fft=N_FFT,
        hop_length=HOP_LENGTH, n_mels=N_MELS, power=2.0,
    ).to(device)

    mel = mel_transform(waveform_padded)
    pad_frames = pad_len // HOP_LENGTH
    mel = mel[:, :, pad_frames: mel.shape[-1] - pad_frames]
    mel = torch.log1p(mel)
    mel_max = mel.amax(dim=(-2, -1), keepdim=True).clamp(min=1e-8)
    mel = mel / mel_max

    print(f"Loaded: {filepath.name} ({duration_s:.1f}s, {mel.shape[2]} frames)", flush=True)
    return mel


# ======================================================================
# MODEL LOADING
# ======================================================================

def load_model(checkpoint: Path, device: torch.device, n_h3: int = 637) -> GlassBoxMI:
    """Load trained model from checkpoint."""
    model = GlassBoxMI(n_h3=n_h3).to(device)
    state = torch.load(checkpoint, map_location=device, weights_only=True)
    model.load_state_dict(state)
    model.eval()
    params = sum(p.numel() for p in model.parameters())
    print(f"Model loaded: {checkpoint.name} ({params:,} params)", flush=True)
    return model


# ======================================================================
# INFERENCE
# ======================================================================

@torch.no_grad()
def predict(model: GlassBoxMI, mel: Tensor) -> Dict[str, np.ndarray]:
    """Run model on mel → dict of numpy arrays."""
    result = model(mel)
    return {k: v.cpu().numpy()[0] for k, v in result.items()}


def format_predictions(preds: Dict[str, np.ndarray]) -> Dict:
    """Format predictions into a human-readable dict."""
    T = preds["dims"].shape[1]
    duration_s = T * HOP_LENGTH / SAMPLE_RATE

    output = {
        "duration_s": round(duration_s, 2),
        "n_frames": T,
        "frame_rate_hz": round(SAMPLE_RATE / HOP_LENGTH, 2),
    }

    # 5+5 dimensions — mean over time
    dims = preds["dims"]  # (10, T)
    output["dimensions"] = {
        "musical": {DIM_NAMES[i]: round(float(dims[i].mean()), 4) for i in range(5)},
        "emotional": {DIM_NAMES[i]: round(float(dims[i].mean()), 4) for i in range(5, 10)},
    }

    # Dimension temporal stats
    output["dimension_stats"] = {}
    for i, name in enumerate(DIM_NAMES):
        d = dims[i]
        output["dimension_stats"][name] = {
            "mean": round(float(d.mean()), 4),
            "std": round(float(d.std()), 4),
            "min": round(float(d.min()), 4),
            "max": round(float(d.max()), 4),
        }

    # Top active beliefs (mean > 0.5)
    beliefs = preds["beliefs"]  # (131, T)
    belief_means = beliefs.mean(axis=1)
    active = [(BELIEF_NAMES[i], float(belief_means[i])) for i in range(131) if belief_means[i] > 0.3]
    active.sort(key=lambda x: -x[1])
    output["active_beliefs"] = [{"name": n, "activation": round(v, 4)} for n, v in active[:20]]

    # R³ summary by group
    r3 = preds["r3"]  # (97, T)
    output["r3_groups"] = {}
    for gname, (gs, ge) in R3_GROUPS.items():
        group_means = {R3_NAMES[i]: round(float(r3[i].mean()), 4) for i in range(gs, ge)}
        output["r3_groups"][gname] = group_means

    return output


# ======================================================================
# GROUND TRUTH COMPARISON
# ======================================================================

def compare_with_ground_truth(preds: Dict[str, np.ndarray], npz_path: Path) -> Dict:
    """Compare model predictions with ground truth from NPZ."""
    with np.load(npz_path) as data:
        gt = {
            "r3": data["r3"].T,        # (97, T)
            "h3": data["h3"].T,        # (N_h3, T)
            "beliefs": data["beliefs"].T,  # (131, T)
            "dims": data["dims"].T,    # (10, T)
        }

    result = {}
    for key in ["r3", "h3", "beliefs", "dims"]:
        p = preds[key]
        t = gt[key]
        # Align lengths
        T = min(p.shape[1], t.shape[1])
        p = p[:, :T]
        t = t[:, :T]

        p_t = torch.from_numpy(p).unsqueeze(0)
        t_t = torch.from_numpy(t).unsqueeze(0)

        mse = per_dim_mse(p_t, t_t).numpy()
        mae = per_dim_mae(p_t, t_t).numpy()
        corr = per_dim_corr(p_t, t_t).numpy()

        result[key] = {
            "mse_mean": float(mse.mean()),
            "mae_mean": float(mae.mean()),
            "corr_mean": float(corr.mean()),
            "mse_per_dim": mse.tolist(),
            "corr_per_dim": corr.tolist(),
        }

    # Detailed dim comparison
    result["dims_detail"] = {}
    p = preds["dims"][:, :min(preds["dims"].shape[1], gt["dims"].shape[1])]
    t = gt["dims"][:, :p.shape[1]]
    for i, name in enumerate(DIM_NAMES):
        result["dims_detail"][name] = {
            "pred_mean": round(float(p[i].mean()), 4),
            "gt_mean": round(float(t[i].mean()), 4),
            "mse": round(float(((p[i] - t[i]) ** 2).mean()), 6),
            "corr": round(float(np.corrcoef(p[i], t[i])[0, 1]) if p[i].std() > 1e-8 else 0.0, 4),
        }

    return result


# ======================================================================
# BATCH EVALUATION
# ======================================================================

@torch.no_grad()
def batch_evaluate(model: GlassBoxMI, data_dir: Path, manifest: List[str],
                   device: torch.device, chunk_size: int = 512) -> Dict:
    """Evaluate model on a set of NPZ files."""
    from torch.utils.data import DataLoader

    ds = MIDataset(data_dir, manifest, chunk_size=chunk_size)
    dl = DataLoader(ds, batch_size=64, shuffle=False, num_workers=0, pin_memory=True)

    W = {"r3": 1.0, "h3": 1.5, "beliefs": 2.0, "dims": 1.0}
    total_loss = {k: 0.0 for k in W}
    total_mse = {k: None for k in W}
    total_corr = {k: None for k in W}
    n = 0

    for batch in dl:
        mel = batch["mel"].to(device)
        targets = {k: batch[k].to(device) for k in W}

        r3 = model.r3_head(mel)
        h3 = model.h3_head(r3)
        b = model.belief_head(r3, h3)
        d = model.dim_head(b)
        preds = {"r3": r3, "h3": h3, "beliefs": b, "dims": d}

        bs = mel.shape[0]
        for k in W:
            loss = nn.functional.mse_loss(preds[k], targets[k]).item()
            total_loss[k] += loss * bs

            mse = per_dim_mse(preds[k], targets[k]).cpu()
            if total_mse[k] is None:
                total_mse[k] = mse * bs
            else:
                total_mse[k] += mse * bs

        n += bs

    result = {}
    for k in W:
        avg_loss = total_loss[k] / n
        avg_mse = (total_mse[k] / n).numpy()
        result[k] = {
            "loss": avg_loss,
            "mse_mean": float(avg_mse.mean()),
            "mse_per_dim": avg_mse.tolist(),
        }

    result["total_weighted"] = sum(W[k] * result[k]["loss"] for k in W)
    result["n_chunks"] = n
    return result


# ======================================================================
# MAIN
# ======================================================================

def main():
    parser = argparse.ArgumentParser(description="Evaluate glass-box MI model")
    parser.add_argument("--checkpoint", type=str, required=True, help="Model checkpoint path")
    parser.add_argument("--audio", type=str, help="Audio file to analyze")
    parser.add_argument("--npz", type=str, help="NPZ file for ground truth comparison")
    parser.add_argument("--data-dir", type=str, help="Data directory for batch evaluation")
    parser.add_argument("--manifest", type=str, help="Manifest JSON for batch evaluation")
    parser.add_argument("--export", type=str, help="Export predictions to JSON")
    parser.add_argument("--n-h3", type=int, default=637, help="H³ dimension")
    args = parser.parse_args()

    device = (
        torch.device("cuda") if torch.cuda.is_available()
        else torch.device("mps") if torch.backends.mps.is_available()
        else torch.device("cpu")
    )
    print(f"Device: {device}", flush=True)

    model = load_model(Path(args.checkpoint), device, n_h3=args.n_h3)

    if args.audio:
        # Single file inference
        mel = load_audio_to_mel(Path(args.audio), device)
        t0 = time.perf_counter()
        preds = predict(model, mel)
        elapsed = time.perf_counter() - t0
        print(f"Inference: {elapsed:.3f}s ({mel.shape[2]} frames)", flush=True)

        output = format_predictions(preds)

        # Print summary
        print(f"\n{'='*60}")
        print(f"5+5 Dimensions:")
        print(f"  Musical:   ", end="")
        for name, val in output["dimensions"]["musical"].items():
            print(f" {name}={val:.3f}", end="")
        print()
        print(f"  Emotional: ", end="")
        for name, val in output["dimensions"]["emotional"].items():
            print(f" {name}={val:.3f}", end="")
        print()

        print(f"\nTop active beliefs:")
        for b in output["active_beliefs"][:10]:
            print(f"  {b['name']:30s} {b['activation']:.3f}")

        # Ground truth comparison
        if args.npz:
            print(f"\n{'='*60}")
            print(f"Ground Truth Comparison ({args.npz}):")
            comp = compare_with_ground_truth(preds, Path(args.npz))
            for k in ["r3", "h3", "beliefs", "dims"]:
                print(f"  {k:>8s}  MSE={comp[k]['mse_mean']:.6f}  r={comp[k]['corr_mean']:+.4f}")
            print(f"\n  Dims detail:")
            for name, d in comp["dims_detail"].items():
                print(f"    {name:15s}  pred={d['pred_mean']:.3f}  gt={d['gt_mean']:.3f}  "
                      f"MSE={d['mse']:.6f}  r={d['corr']:+.4f}")
            output["ground_truth_comparison"] = comp

        # Export
        if args.export:
            with open(args.export, "w") as f:
                json.dump(output, f, indent=2)
            print(f"\nExported to: {args.export}")

    elif args.data_dir and args.manifest:
        # Batch evaluation
        data_dir = Path(args.data_dir)
        with open(args.manifest) as f:
            manifest = json.load(f)
        print(f"\nBatch evaluating {len(manifest)} segments...", flush=True)
        result = batch_evaluate(model, data_dir, manifest, device)
        print(f"\nResults ({result['n_chunks']} chunks):")
        print(f"  Total weighted loss: {result['total_weighted']:.6f}")
        for k in ["r3", "h3", "beliefs", "dims"]:
            print(f"  {k:>8s}  MSE={result[k]['mse_mean']:.6f}")
        if args.export:
            with open(args.export, "w") as f:
                json.dump(result, f, indent=2)
            print(f"\nExported to: {args.export}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
