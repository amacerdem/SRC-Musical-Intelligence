"""MI-Core Evaluation Script -- Run evaluation suite on a checkpoint.

Runs all evaluation metrics on a trained MI-Core checkpoint:
- Alignment (MI-Core vs MI Teacher per layer)
- Layer metrics (MSE, MAE, R² per layer/direction)
- Fill-Net evaluation (completion quality vs mask ratio)
- White-box traceability verification

Usage::

    python -m Musical_Intelligence.training.scripts.evaluate \\
        --checkpoint checkpoints/mi_core_epoch_600.pt \\
        --data_dir data/precomputed \\
        --output_dir evaluation_results/
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from Musical_Intelligence.data.collator import MICollator
from Musical_Intelligence.data.mi_dataset import MIDataset
from Musical_Intelligence.evaluation.alignment import AlignmentEvaluator
from Musical_Intelligence.evaluation.fill_eval import FillEvaluator
from Musical_Intelligence.evaluation.layer_metrics import LayerMetricsEvaluator
from Musical_Intelligence.evaluation.white_box import WhiteBoxTracer
from Musical_Intelligence.training.model.mi_core import MICore


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Evaluate MI-Core checkpoint."
    )
    parser.add_argument(
        "--checkpoint", type=str, required=True,
        help="Path to model checkpoint.",
    )
    parser.add_argument(
        "--data_dir", type=str, required=True,
        help="Directory with pre-computed HDF5 labels.",
    )
    parser.add_argument(
        "--output_dir", type=str, default="evaluation_results",
        help="Output directory for results.",
    )
    parser.add_argument(
        "--batch_size", type=int, default=16,
        help="Evaluation batch size.",
    )
    parser.add_argument(
        "--max_batches", type=int, default=None,
        help="Limit number of evaluation batches.",
    )
    args = parser.parse_args()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load model
    print("Loading model...")
    model = MICore()
    ckpt = torch.load(args.checkpoint, map_location="cpu")
    model.load_state_dict(ckpt["model_state_dict"])
    model = model.to(device)
    model.eval()
    print(f"Model loaded from epoch {ckpt.get('epoch', '?')}")

    # Dataset
    dataset = MIDataset(data_dir=args.data_dir, segment_length=2048)
    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=False,
        num_workers=4,
        collate_fn=MICollator(),
    )
    print(f"Evaluation dataset: {len(dataset)} tracks")

    # Evaluators
    alignment_eval = AlignmentEvaluator()
    layer_eval = LayerMetricsEvaluator()

    # Run evaluation
    print("\nRunning evaluation...")
    with torch.no_grad():
        for i, batch in enumerate(loader):
            if args.max_batches and i >= args.max_batches:
                break

            mel = batch["mel"].to(device)
            r3 = batch["r3"].to(device)
            h3 = batch["h3_dense"].to(device)
            c3 = batch["c3"].to(device)

            # Encode
            enc_out = model.encode(mel)

            # Decode
            dec_out = model.decode(c3)

            # Alignment
            alignment_eval.update(
                pred_mel=enc_out.cochlea_hat,
                pred_r3=enc_out.r3_hat,
                pred_h3=enc_out.h3_hat,
                pred_c3=enc_out.c3_hat,
                target_mel=mel,
                target_r3=r3,
                target_h3=h3,
                target_c3=c3,
            )

            # Layer metrics
            layer_eval.update_encode(
                pred_mel=enc_out.cochlea_hat,
                pred_r3=enc_out.r3_hat,
                pred_h3=enc_out.h3_hat,
                pred_c3=enc_out.c3_hat,
                target_mel=mel,
                target_r3=r3,
                target_h3=h3,
                target_c3=c3,
            )
            layer_eval.update_decode(
                pred_h3=dec_out.h3_rec,
                pred_r3=dec_out.r3_rec,
                pred_mel=dec_out.mel_rec,
                target_h3=h3,
                target_r3=r3,
                target_mel=mel,
            )

            if (i + 1) % 10 == 0:
                print(f"  Processed {i + 1} batches...")

    # Compute results
    print("\nComputing metrics...")

    alignment_results = alignment_eval.compute()
    print("\n" + AlignmentEvaluator.format_results(alignment_results))

    layer_results = layer_eval.compute()
    print("\n" + LayerMetricsEvaluator.format_results(layer_results))

    # Fill-Net evaluation
    print("\nRunning Fill-Net evaluation...")
    fill_eval = FillEvaluator()
    # Use first batch of C3 data
    sample_batch = next(iter(loader))
    c3_sample = sample_batch["c3"].to(device)
    fill_results = fill_eval.evaluate(model.fill_net, c3_sample)
    print("\n" + FillEvaluator.format_results(fill_results))

    # White-box traceability
    print("\nVerifying white-box traceability...")
    tracer = WhiteBoxTracer()
    tracer.build()
    trace_summary = tracer.summary()
    total_traced = sum(
        sum(dims.values()) for dims in trace_summary.values()
    )
    print(f"  Traced {total_traced}/1006 C3 dimensions across {len(trace_summary)} units")

    # Save results
    results = {
        "alignment": {
            k: {"mse": v.mse, "mae": v.mae, "r2": v.r2, "pearson": v.pearson_mean}
            for k, v in alignment_results.items()
        },
        "layers": {
            k: {"mse": v.mse, "mae": v.mae, "r2": v.r2, "dim": v.dim}
            for k, v in layer_results.items()
        },
        "fill": {
            str(k): {"mse": v.mse, "mae": v.mae, "r2": v.r2}
            for k, v in fill_results.items()
        },
        "traceability": {"total_traced": total_traced, "units": trace_summary},
    }

    results_path = output_dir / "evaluation_results.json"
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\nResults saved to {results_path}")


if __name__ == "__main__":
    main()
