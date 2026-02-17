"""Pre-compute BCH manifold training pairs from the deterministic forward pipeline.

Runs mel → R³ → H³ → BCH → RAM/Neuro for each audio file and stores
(mel, manifold) pairs as HDF5 files. The manifold is the full computational
state of BCH plus its downstream effects:
    R³ active dims (16D) + H³ active dims (50D) + BCH output (16D)
    + RAM (26D) + Neuro (4D) = 112D.

These are the teacher labels for Head1 and Head2.

Usage::

    python -m Musical_Intelligence.training.precompute_bch \\
        --audio-dir Test-Audio/ \\
        --output-dir ./cache/bch \\
        --split train

The forward pipeline is the teacher — it produces unlimited (mel, manifold)
pairs for free. No human annotation needed.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import List

import torch

from Musical_Intelligence.data.preprocessing import compute_mel, load_audio
from Musical_Intelligence.training.model.mi_space_layout import (
    BCH_H3_DEMAND_COUNT,
    BCH_MANIFOLD_DIM,
    BCH_R3_ACTIVE_INDICES,
)


def discover_audio_files(audio_dir: Path) -> List[Path]:
    """Find all audio files in a directory."""
    extensions = {".wav", ".flac", ".mp3", ".ogg", ".m4a"}
    files = []
    for ext in extensions:
        files.extend(audio_dir.glob(f"*{ext}"))
    return sorted(files)


@torch.no_grad()
def precompute_single(
    audio_path: Path,
    output_dir: Path,
    r3_extractor,
    h3_extractor,
    bch_nucleus,
    bch_demands: set,
    bch_demand_keys_sorted: list,
) -> dict:
    """Run forward pipeline on one audio file → save (mel, manifold) HDF5.

    The manifold is:
        R³_active(16D) || H³_active(50D) || BCH(16D)
        || RAM(26D) || Neuro(4D) = 112D.

    Returns metadata dict for the manifest.
    """
    import h5py

    from Musical_Intelligence.brain.executor import execute

    track_id = audio_path.stem

    # 1. Load audio
    waveform, sr = load_audio(audio_path)  # (1, samples), 44100

    # 2. Compute mel spectrogram
    mel = compute_mel(waveform)  # (1, 128, T)
    T = mel.shape[-1]

    # 3. R³ extraction
    r3_out = r3_extractor.extract(mel, audio=waveform, sr=sr)
    r3_tensor = r3_out.features  # (1, T, 97)

    # 4. H³ extraction (BCH demands only)
    h3_out = h3_extractor.extract(r3_tensor, bch_demands)
    h3_features = h3_out.features  # Dict[(r3_idx, horizon, morph, law)] -> (1, T)

    # 5. Execute BCH through the brain executor → BCH output + RAM + Neuro
    outputs, ram, neuro = execute(
        [bch_nucleus], h3_features, r3_tensor,
    )
    bch_output = outputs["BCH"]  # (1, T, 16)

    # 6. Build 112D manifold:
    #    R³_active(16) || H³_active(50) || BCH(16) || RAM(26) || Neuro(4)
    r3_active_indices = list(BCH_R3_ACTIVE_INDICES)
    r3_active = r3_tensor[0, :, r3_active_indices]  # (T, 16)

    h3_active = torch.stack(
        [h3_features[k][0] for k in bch_demand_keys_sorted], dim=-1
    )  # (T, 50)

    bch_out = bch_output.squeeze(0)     # (T, 16)
    ram_out = ram.squeeze(0)            # (T, 26)
    neuro_out = neuro.squeeze(0)        # (T, 4)

    manifold = torch.cat(
        [r3_active, h3_active, bch_out, ram_out, neuro_out], dim=-1,
    )  # (T, 112)
    assert manifold.shape[-1] == BCH_MANIFOLD_DIM, (
        f"Manifold dim mismatch: {manifold.shape[-1]} != {BCH_MANIFOLD_DIM}"
    )

    # 7. Save as HDF5 — shapes: mel (T, 128), manifold (T, 112)
    mel_save = mel.squeeze(0).transpose(0, 1).cpu()  # (T, 128)
    manifold_save = manifold.cpu()                     # (T, 112)

    out_path = output_dir / f"{track_id}.h5"
    with h5py.File(out_path, "w") as f:
        f.create_dataset("mel", data=mel_save.numpy(), compression="gzip")
        f.create_dataset("manifold", data=manifold_save.numpy(), compression="gzip")

    duration_s = waveform.shape[-1] / sr
    return {
        "track_id": track_id,
        "n_frames": T,
        "duration_s": round(duration_s, 2),
        "mel_shape": list(mel_save.shape),
        "manifold_shape": list(manifold_save.shape),
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Pre-compute BCH manifold training pairs from forward pipeline."
    )
    parser.add_argument(
        "--audio-dir", type=str, required=True,
        help="Directory containing audio files.",
    )
    parser.add_argument(
        "--output-dir", type=str, default="./cache/bch",
        help="Directory to store HDF5 files (default: ./cache/bch).",
    )
    parser.add_argument(
        "--split", type=str, default="train",
        help="Split name — files saved to {output_dir}/{split}/ (default: train).",
    )
    args = parser.parse_args()

    audio_dir = Path(args.audio_dir)
    output_dir = Path(args.output_dir) / args.split
    output_dir.mkdir(parents=True, exist_ok=True)

    # Discover audio files
    audio_files = discover_audio_files(audio_dir)
    if not audio_files:
        print(f"No audio files found in {audio_dir}")
        return

    print(f"Found {len(audio_files)} audio files in {audio_dir}")
    print(f"Output: {output_dir}")
    print()

    # Initialise pipeline components (once)
    from Musical_Intelligence.brain.units.spu.relays.bch import BCH
    from Musical_Intelligence.ear.h3 import H3Extractor
    from Musical_Intelligence.ear.r3 import R3Extractor

    r3_ext = R3Extractor()
    h3_ext = H3Extractor()
    bch = BCH()

    # Collect BCH H³ demands (sorted for deterministic ordering)
    bch_demands = {spec.as_tuple() for spec in bch.h3_demand}
    bch_demand_keys_sorted = sorted(bch_demands)
    print(f"BCH demands: {len(bch_demands)} H³ tuples")
    print(f"Manifold: R³({len(BCH_R3_ACTIVE_INDICES)}) + H³({BCH_H3_DEMAND_COUNT}) + BCH({BCH_MANIFOLD_DIM - len(BCH_R3_ACTIVE_INDICES) - BCH_H3_DEMAND_COUNT}) = {BCH_MANIFOLD_DIM}D")
    print()

    # Save H³ key ordering for reproducibility
    h3_key_order = [list(k) for k in bch_demand_keys_sorted]

    # Process each file
    manifest = {}
    total_frames = 0
    total_time = 0.0

    for i, audio_path in enumerate(audio_files, 1):
        print(f"[{i}/{len(audio_files)}] {audio_path.name} ... ", end="", flush=True)
        t0 = time.time()

        meta = precompute_single(
            audio_path, output_dir,
            r3_ext, h3_ext, bch, bch_demands,
            bch_demand_keys_sorted,
        )

        elapsed = time.time() - t0
        total_time += elapsed
        total_frames += meta["n_frames"]
        manifest[meta["track_id"]] = meta

        print(f"{meta['n_frames']} frames, {meta['duration_s']}s audio, {elapsed:.1f}s")

    # Save manifest (includes H³ key ordering for reproducibility)
    manifest_meta = {
        "_info": {
            "manifold_dim": BCH_MANIFOLD_DIM,
            "r3_active_indices": list(BCH_R3_ACTIVE_INDICES),
            "h3_key_order": h3_key_order,
            "layout": f"R3_active[0:{len(BCH_R3_ACTIVE_INDICES)}] || "
                       f"H3_active[{len(BCH_R3_ACTIVE_INDICES)}:{len(BCH_R3_ACTIVE_INDICES)+BCH_H3_DEMAND_COUNT}] || "
                       f"BCH[{len(BCH_R3_ACTIVE_INDICES)+BCH_H3_DEMAND_COUNT}:{BCH_MANIFOLD_DIM}]",
        },
        "tracks": manifest,
    }
    manifest_path = output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest_meta, indent=2))

    print()
    print(f"Done. {len(manifest)} tracks, {total_frames} total frames.")
    print(f"Total pipeline time: {total_time:.1f}s")
    print(f"Manifest: {manifest_path}")


if __name__ == "__main__":
    main()
