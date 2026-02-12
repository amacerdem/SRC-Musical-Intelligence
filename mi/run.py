"""
MI CLI — Command-line entry point.

Usage:
    python -m mi audio.wav [--json output.json] [--csv output.csv] [--plot]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Musical Intelligence — white-box music cognition model"
    )
    parser.add_argument("audio", type=str, help="Path to audio file")
    parser.add_argument("--json", type=str, help="Export to JSON")
    parser.add_argument("--csv", type=str, help="Export to CSV")
    parser.add_argument("--plot", action="store_true", help="Show plot")
    parser.add_argument("--no-semantics", action="store_true", help="Skip L³ semantic layer")

    args = parser.parse_args()

    audio_path = Path(args.audio)
    if not audio_path.exists():
        print(f"Error: {audio_path} not found", file=sys.stderr)
        sys.exit(1)

    # Import here to avoid slow startup for --help
    from .core.config import MI_CONFIG
    from .pipeline import MIPipeline
    from .io.audio import load_audio

    config = MI_CONFIG
    pipeline = MIPipeline(config)

    print(f"Loading: {audio_path}")
    waveform = load_audio(audio_path, config)
    print(f"  Samples: {waveform.shape[-1]:,} ({waveform.shape[-1]/config.sample_rate:.1f}s)")

    print("Processing...")
    output = pipeline.process(
        waveform,
        return_semantics=not args.no_semantics,
    )

    # Brain output (26D)
    brain = output.brain
    B, T, D = brain.tensor.shape
    print(f"  Brain: {D}D × {T} frames ({T/config.frame_rate:.1f}s)")
    tensor = brain.tensor.squeeze(0)
    for i, dim_name in enumerate(brain.dimension_names):
        vals = tensor[:, i]
        print(f"    {dim_name:25s}  mean={vals.mean():.3f}  "
              f"std={vals.std():.3f}  min={vals.min():.3f}  max={vals.max():.3f}")

    # Semantics (104D)
    if output.semantics is not None:
        sem = output.semantics
        print(f"  L³ Semantics: {sem.total_dim}D")
        for name, group in sem.groups.items():
            print(f"    {name}: {group.tensor.shape[-1]}D")

    if args.json:
        from .io.export import to_json
        to_json(output, args.json)
        print(f"  Exported: {args.json}")

    if args.csv:
        from .io.export import to_csv
        to_csv(output, args.csv)
        print(f"  Exported: {args.csv}")

    if args.plot:
        _plot(output, config)


def _plot(output, config) -> None:
    """Simple matplotlib visualization."""
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed. Skip --plot.")
        return

    brain = output.brain
    tensor = brain.tensor.squeeze(0).detach().cpu()
    T, D = tensor.shape
    time = [t / config.frame_rate for t in range(T)]

    fig, axes = plt.subplots(D, 1, figsize=(14, D * 1.2), sharex=True)
    if D == 1:
        axes = [axes]

    for i, (ax, dim_name) in enumerate(zip(axes, brain.dimension_names)):
        ax.plot(time, tensor[:, i].numpy(), linewidth=0.5)
        ax.set_ylabel(dim_name, fontsize=7, rotation=0, ha="right")
        ax.set_ylim(-1.1, 1.1)
        ax.tick_params(labelsize=6)

    axes[-1].set_xlabel("Time (s)")
    fig.suptitle(f"MI — Brain ({D}D)")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
