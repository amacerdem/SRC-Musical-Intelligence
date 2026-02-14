"""Export MI-Core for inference -- prune training-only components.

Removes:
- H3 auxiliary head (training-only, ~5210D)
- Gradient buffers
- Optimizer / scheduler state

The exported model retains full encode/decode/fill capability
with the backbone's temporal awareness intact in Mamba state.

Usage::

    python -m Musical_Intelligence.training.scripts.export_model \\
        --checkpoint checkpoints/mi_core_epoch_600.pt \\
        --output models/mi_core_inference.pt
"""
from __future__ import annotations

import argparse
from pathlib import Path

import torch

from Musical_Intelligence.training.model.mi_core import MICore


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export MI-Core for inference."
    )
    parser.add_argument(
        "--checkpoint", type=str, required=True,
        help="Path to training checkpoint.",
    )
    parser.add_argument(
        "--output", type=str, required=True,
        help="Output path for inference model.",
    )
    parser.add_argument(
        "--verify", action="store_true",
        help="Verify exported model with a dummy forward pass.",
    )
    args = parser.parse_args()

    # Load checkpoint
    print(f"Loading checkpoint: {args.checkpoint}")
    ckpt = torch.load(args.checkpoint, map_location="cpu")

    model = MICore()
    model.load_state_dict(ckpt["model_state_dict"])
    print(f"Model loaded: {model}")
    print(f"  Epoch: {ckpt.get('epoch', '?')}")
    print(f"  Global step: {ckpt.get('global_step', '?')}")

    # Count params before pruning
    params_before = model.param_count

    # Prune H3 auxiliary head
    model.prune_h3_aux()

    # Collect inference-only state dict
    state_dict = {
        k: v for k, v in model.state_dict().items()
        if "h3_aux_head" not in k
    }

    params_after = sum(p.numel() for p in model.parameters() if p is not None)
    print(f"  Params before: {params_before / 1e6:.1f}M")
    print(f"  Params after:  {params_after / 1e6:.1f}M")
    print(f"  Pruned:        {(params_before - params_after) / 1e6:.1f}M")

    # Save
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    torch.save({
        "model_state_dict": state_dict,
        "pruned": True,
        "source_epoch": ckpt.get("epoch"),
        "source_step": ckpt.get("global_step"),
    }, output_path)
    print(f"Exported to: {output_path}")

    # Verify
    if args.verify:
        print("\nVerifying exported model...")
        verify_model = MICore()
        verify_model.prune_h3_aux()

        # Load only the non-h3-aux keys
        verify_model.load_state_dict(state_dict, strict=False)

        dummy_mel = torch.randn(1, 64, 128)
        enc_out = verify_model.encode(dummy_mel)
        print(f"  Encode: mel (1,64,128) -> mi_space {enc_out.mi_space.shape}")

        dummy_c3 = torch.randn(1, 64, 1006)
        dec_out = verify_model.decode(dummy_c3)
        print(f"  Decode: c3 (1,64,1006) -> mel_rec {dec_out.mel_rec.shape}")

        print("  Verification PASSED")


if __name__ == "__main__":
    main()
