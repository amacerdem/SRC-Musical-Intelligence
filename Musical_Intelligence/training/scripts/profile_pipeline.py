"""Profile MI Teacher + MI-Core forward pass timing.

Benchmarks:
1. MI Teacher pipeline: mel -> R3 -> H3 -> C3 (deterministic)
2. MI-Core encode: mel -> mi_space (neural)
3. MI-Core decode: c3 -> mel (neural)
4. MI-Core fill: c3_masked -> c3_filled (neural)

Reports per-stage timing, throughput, and memory usage.

Usage::

    python -m Musical_Intelligence.training.scripts.profile_pipeline \\
        --duration 10 \\
        --batch_size 1 \\
        --device cuda
"""
from __future__ import annotations

import argparse
import time

import torch

from Musical_Intelligence.training.model.mi_core import MICore
from Musical_Intelligence.training.model.mi_space_layout import (
    C3_DIM,
    COCHLEA_DIM,
    FRAME_RATE_HZ,
    H3_AUX_DIM,
    MI_SPACE_DIM,
    R3_DIM,
)


def profile_mi_core(
    model: MICore,
    batch_size: int,
    n_frames: int,
    device: torch.device,
    n_warmup: int = 3,
    n_runs: int = 10,
) -> dict:
    """Profile MI-Core forward passes.

    Returns timing dict with keys: encode, decode, fill.
    """
    model.eval()
    results = {}

    # Dummy inputs
    mel = torch.randn(batch_size, n_frames, COCHLEA_DIM, device=device)
    c3 = torch.randn(batch_size, n_frames, C3_DIM, device=device)
    c3_masked = c3 * 0.5
    mask = torch.ones_like(c3)
    mask[:, :, ::2] = 0  # Mask every other dim

    with torch.no_grad():
        # Encode
        for _ in range(n_warmup):
            model.encode(mel)
        if device.type == "cuda":
            torch.cuda.synchronize()

        t0 = time.perf_counter()
        for _ in range(n_runs):
            enc_out = model.encode(mel)
            if device.type == "cuda":
                torch.cuda.synchronize()
        encode_time = (time.perf_counter() - t0) / n_runs

        results["encode"] = {
            "time_s": encode_time,
            "input_shape": f"({batch_size}, {n_frames}, {COCHLEA_DIM})",
            "output_shapes": {
                "mi_space": tuple(enc_out.mi_space.shape),
                "h3_hat": tuple(enc_out.h3_hat.shape) if enc_out.h3_hat is not None else None,
            },
        }

        # Decode
        for _ in range(n_warmup):
            model.decode(c3)
        if device.type == "cuda":
            torch.cuda.synchronize()

        t0 = time.perf_counter()
        for _ in range(n_runs):
            dec_out = model.decode(c3)
            if device.type == "cuda":
                torch.cuda.synchronize()
        decode_time = (time.perf_counter() - t0) / n_runs

        results["decode"] = {
            "time_s": decode_time,
            "input_shape": f"({batch_size}, {n_frames}, {C3_DIM})",
            "output_shapes": {
                "mel_rec": tuple(dec_out.mel_rec.shape),
                "r3_rec": tuple(dec_out.r3_rec.shape),
            },
        }

        # Fill
        for _ in range(n_warmup):
            model.fill(c3_masked, mask)
        if device.type == "cuda":
            torch.cuda.synchronize()

        t0 = time.perf_counter()
        for _ in range(n_runs):
            filled = model.fill(c3_masked, mask)
            if device.type == "cuda":
                torch.cuda.synchronize()
        fill_time = (time.perf_counter() - t0) / n_runs

        results["fill"] = {
            "time_s": fill_time,
            "input_shape": f"({batch_size}, {n_frames}, {C3_DIM})",
            "output_shape": tuple(filled.shape),
        }

    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Profile MI pipeline timing."
    )
    parser.add_argument(
        "--duration", type=float, default=10.0,
        help="Audio duration in seconds to simulate.",
    )
    parser.add_argument(
        "--batch_size", type=int, default=1,
        help="Batch size.",
    )
    parser.add_argument(
        "--device", type=str, default="cpu",
        help="Device (cpu or cuda).",
    )
    parser.add_argument(
        "--n_runs", type=int, default=10,
        help="Number of profiling runs.",
    )
    args = parser.parse_args()

    device = torch.device(args.device)
    n_frames = int(args.duration * FRAME_RATE_HZ)

    print("MI Pipeline Profiler")
    print("=" * 60)
    print(f"Duration:    {args.duration}s ({n_frames} frames)")
    print(f"Batch size:  {args.batch_size}")
    print(f"Device:      {device}")
    print(f"Frame rate:  {FRAME_RATE_HZ:.2f} Hz")
    print()

    # MI-Core profiling
    print("Profiling MI-Core neural model...")
    model = MICore()
    model = model.to(device)
    model.eval()
    print(f"Model: {model}")

    if device.type == "cuda":
        mem_before = torch.cuda.memory_allocated(device) / 1e6
        print(f"GPU memory (model): {mem_before:.1f} MB")

    results = profile_mi_core(
        model, args.batch_size, n_frames, device, n_runs=args.n_runs
    )

    if device.type == "cuda":
        mem_peak = torch.cuda.max_memory_allocated(device) / 1e6
        print(f"GPU memory (peak):  {mem_peak:.1f} MB")

    print()
    print("Results:")
    print("-" * 60)
    for mode, data in results.items():
        rt = data["time_s"]
        rtf = rt / args.duration  # Real-time factor
        print(f"  {mode:<8s}: {rt:.4f}s  (RTF={rtf:.4f}x)")
        print(f"           input:  {data['input_shape']}")
        if "output_shapes" in data:
            for k, v in data["output_shapes"].items():
                print(f"           {k}: {v}")
        elif "output_shape" in data:
            print(f"           output: {data['output_shape']}")
    print("-" * 60)

    total = sum(r["time_s"] for r in results.values())
    print(f"  Total:   {total:.4f}s for {args.duration}s audio")
    print(f"  RTF:     {total / args.duration:.4f}x")


if __name__ == "__main__":
    main()
