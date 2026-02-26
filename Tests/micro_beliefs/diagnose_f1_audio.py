#!/usr/bin/env python
"""Diagnose F1 audio files — show all R³/mechanism/belief dimensions per WAV.

Runs each WAV through the full R³→H³→C³ pipeline and prints a detailed
breakdown of every dimension so you can manually verify correctness.

Run::

    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/micro_beliefs/diagnose_f1_audio.py

Optional arguments::

    python Tests/micro_beliefs/diagnose_f1_audio.py --relay bch
    python Tests/micro_beliefs/diagnose_f1_audio.py --file bch/01_unison_rich.wav
    python Tests/micro_beliefs/diagnose_f1_audio.py --compact
"""
from __future__ import annotations

import argparse
import pathlib
import sys
import time

import numpy as np
import torch
from scipy.io import wavfile

# Ensure project root on path
_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))

from Musical_Intelligence.ear.r3.constants.feature_names import (
    R3_FEATURE_NAMES,
)
from Tests.micro_beliefs.pipeline_runner import (
    MicroBeliefRunner,
    SAMPLE_RATE,
)

AUDIO_DIR = _ROOT / "Test-Audio" / "micro_beliefs" / "f1"

# R³ groups for structured display
R3_GROUPS = {
    "A (Consonance)":       (0, 7),
    "B (Energy)":           (7, 12),
    "C (Timbre)":           (12, 21),
    "D (Change)":           (21, 25),
    "F (Pitch & Chroma)":   (25, 41),
    "G (Rhythm & Groove)":  (41, 51),
    "H (Harmony & Tonality)": (51, 63),
    "J (Timbre Extended)":  (63, 83),
    "K (Modulation & Psych)": (83, 97),
}

# F1 relay → associated belief names
F1_BELIEFS = {
    "bch": [
        "harmonic_stability",
        "interval_quality",
        "harmonic_template_match",
        "consonance_trajectory",
    ],
    "pscl": [
        "pitch_prominence",
        "pitch_continuation",
    ],
    "pccr": [
        "pitch_identity",
        "octave_equivalence",
    ],
    "sded": [
        "spectral_complexity",
    ],
    "csg": [
        "consonance_salience_gradient",
    ],
    "mpg": [
        "melodic_contour_tracking",
        "contour_continuation",
    ],
    "miaa": [
        "timbral_character",
        "imagery_recognition",
    ],
    "stai": [
        "aesthetic_quality",
        "spectral_temporal_synergy",
        "reward_response_pred",
    ],
}

# F1 mechanism names (uppercase relay code → mechanism NAME)
F1_MECHANISMS = ["BCH", "PSCL", "PCCR", "SDED", "CSG", "MPG", "MIAA",
                 "PNH", "TPIO", "SDNPS", "TPRD"]

ALL_F1_BELIEFS = []
for beliefs in F1_BELIEFS.values():
    ALL_F1_BELIEFS.extend(beliefs)


def fmt(val: float) -> str:
    """Format float for display."""
    if abs(val) < 0.0001:
        return f"{val:+.6f}"
    return f"{val:+.4f}"


def load_wav(path: pathlib.Path) -> torch.Tensor:
    """Load WAV file as (1, N) float32 tensor in [-1, 1]."""
    sr, data = wavfile.read(str(path))
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32767.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483647.0
    elif data.dtype != np.float32:
        data = data.astype(np.float32)
    if data.ndim == 2:
        data = data.mean(axis=1)
    waveform = torch.from_numpy(data).unsqueeze(0)  # (1, N)
    return waveform


def diagnose_file(
    runner: MicroBeliefRunner,
    wav_path: pathlib.Path,
    relay: str,
    compact: bool = False,
) -> dict:
    """Run full pipeline on a single WAV and print diagnostics.

    Returns dict with summary statistics for later comparison.
    """
    from Musical_Intelligence.brain.executor import execute

    rel_path = wav_path.relative_to(_ROOT)
    waveform = load_wav(wav_path)
    duration = waveform.shape[-1] / SAMPLE_RATE

    print(f"\n{'='*80}")
    print(f"  {rel_path}  ({duration:.2f}s)")
    print(f"{'='*80}")

    with torch.no_grad():
        mel = runner.audio_to_mel(waveform)
        r3_out = runner.r3_extractor.extract(mel, audio=waveform, sr=SAMPLE_RATE)
        r3_features = r3_out.features  # (1, T, 97)
        h3_out = runner.h3_extractor.extract(r3_features, runner.h3_demands)
        outputs, _ram, _neuro = execute(
            runner.nuclei, h3_out.features, r3_features,
        )

    T = r3_features.shape[1]
    # Trim warmup frames for stats
    WARMUP = min(50, T // 4)
    r3_trimmed = r3_features[:, WARMUP:, :]  # (1, T', 97)

    # ── R³ Features ───────────────────────────────────────────────
    print(f"\n  R³ Features  (T={T} frames, showing mean after warmup={WARMUP})")
    print(f"  {'─'*74}")

    r3_summary = {}
    for group_name, (start, end) in R3_GROUPS.items():
        if compact:
            # Compact: one line per group
            means = r3_trimmed[0, :, start:end].mean(dim=0)
            for i in range(end - start):
                r3_summary[R3_FEATURE_NAMES[start + i]] = means[i].item()
            vals = "  ".join(
                f"{R3_FEATURE_NAMES[start + i][:12]:>12s}={means[i]:.4f}"
                for i in range(end - start)
                if abs(means[i]) > 0.0001
            )
            if vals:
                print(f"  {group_name:26s}  {vals}")
        else:
            print(f"\n  {group_name}")
            for idx in range(start, end):
                col = r3_trimmed[0, :, idx]
                mean_v = col.mean().item()
                std_v = col.std().item()
                min_v = col.min().item()
                max_v = col.max().item()
                name = R3_FEATURE_NAMES[idx]
                r3_summary[name] = mean_v
                bar_len = int(abs(mean_v) * 30)
                bar = "█" * min(bar_len, 30)
                print(
                    f"    [{idx:2d}] {name:28s}  "
                    f"mean={fmt(mean_v)}  std={std_v:.4f}  "
                    f"[{fmt(min_v)}, {fmt(max_v)}]  {bar}"
                )

    # ── F1 Mechanism Outputs ──────────────────────────────────────
    print(f"\n  F1 Mechanism Outputs")
    print(f"  {'─'*74}")

    mech_summary = {}
    for mech in runner.nuclei:
        if mech.NAME not in F1_MECHANISMS:
            continue
        if mech.NAME not in outputs:
            print(f"  {mech.NAME:8s}  — not in outputs (skipped)")
            continue

        mech_out = outputs[mech.NAME]  # (1, T, D)
        D = mech_out.shape[-1]
        mech_trimmed = mech_out[:, WARMUP:, :]

        dim_names = getattr(mech, "dimension_names", None)
        if dim_names is None:
            dim_names = tuple(f"dim_{i}" for i in range(D))

        print(f"\n  {mech.NAME} (D={D}, role={getattr(mech, 'ROLE', '?')})")
        for d in range(D):
            col = mech_trimmed[0, :, d]
            mean_v = col.mean().item()
            dname = dim_names[d] if d < len(dim_names) else f"dim_{d}"
            mech_summary[f"{mech.NAME}.{dname}"] = mean_v
            bar_len = int(abs(mean_v) * 30)
            bar = "█" * min(bar_len, 30)
            if compact and abs(mean_v) < 0.001:
                continue
            print(f"    [{d:2d}] {dname:32s}  mean={fmt(mean_v)}  {bar}")

    # ── F1 Beliefs ────────────────────────────────────────────────
    print(f"\n  F1 Beliefs (17 beliefs)")
    print(f"  {'─'*74}")

    belief_summary = {}
    target_beliefs = F1_BELIEFS.get(relay, ALL_F1_BELIEFS)

    for bname in ALL_F1_BELIEFS:
        belief = runner._beliefs_by_name.get(bname)
        if belief is None:
            print(f"    {bname:35s}  — not found")
            continue
        mech_name = belief.MECHANISM
        if mech_name not in outputs:
            print(f"    {bname:35s}  — mechanism {mech_name} not in outputs")
            continue

        mech_out = outputs[mech_name]
        observed = belief.observe(mech_out)  # (B, T)
        obs_trimmed = observed[:, WARMUP:]
        mean_v = obs_trimmed.mean().item()
        std_v = obs_trimmed.std().item()
        min_v = obs_trimmed.min().item()
        max_v = obs_trimmed.max().item()
        belief_summary[bname] = mean_v

        # Mark if this is the "home" relay
        marker = " ◄" if bname in target_beliefs else ""
        btype = getattr(belief, "__class__", type(belief)).__bases__[0].__name__
        bar_len = int(abs(mean_v) * 40)
        bar = "█" * min(bar_len, 40)
        print(
            f"    {bname:35s}  {btype:15s}  "
            f"mean={fmt(mean_v)}  std={std_v:.4f}  "
            f"[{fmt(min_v)}, {fmt(max_v)}]  {bar}{marker}"
        )

    return {
        "file": str(rel_path),
        "duration": duration,
        "frames": T,
        "r3": r3_summary,
        "mechanisms": mech_summary,
        "beliefs": belief_summary,
    }


def print_comparison_table(results: list[dict], relay: str):
    """Print a compact comparison table of belief values across files."""
    if not results:
        return

    beliefs = F1_BELIEFS.get(relay, ALL_F1_BELIEFS)

    print(f"\n\n{'='*80}")
    print(f"  COMPARISON TABLE — {relay.upper()} relay beliefs")
    print(f"{'='*80}")

    # Header
    header = f"  {'File':40s}"
    for b in beliefs:
        header += f"  {b[:16]:>16s}"
    print(header)
    print(f"  {'─'*40}" + "─" * (18 * len(beliefs)))

    # Rows
    for r in results:
        fname = pathlib.Path(r["file"]).name
        row = f"  {fname:40s}"
        for b in beliefs:
            val = r["beliefs"].get(b, float("nan"))
            row += f"  {val:16.4f}"
        print(row)

    # Key R³ dimensions comparison
    key_r3 = {
        "bch": ["roughness", "sethares_dissonance", "helmholtz_kang",
                "sensory_pleasantness", "tonalness"],
        "pscl": ["pitch_salience", "tonalness", "pitch_height",
                 "spectral_autocorrelation"],
        "pccr": ["pitch_salience", "pitch_class_entropy", "pitch_height"],
        "sded": ["roughness", "spectral_flux", "sethares_dissonance"],
        "csg": ["roughness", "sensory_pleasantness", "sethares_dissonance"],
        "mpg": ["onset_strength", "pitch_height", "spectral_flux"],
        "miaa": ["tonalness", "spectral_autocorrelation", "warmth"],
        "stai": ["sensory_pleasantness", "tonalness", "roughness"],
    }

    r3_dims = key_r3.get(relay, ["roughness", "tonalness", "pitch_salience"])

    print(f"\n  Key R³ dimensions:")
    header2 = f"  {'File':40s}"
    for d in r3_dims:
        header2 += f"  {d[:16]:>16s}"
    print(header2)
    print(f"  {'─'*40}" + "─" * (18 * len(r3_dims)))

    for r in results:
        fname = pathlib.Path(r["file"]).name
        row = f"  {fname:40s}"
        for d in r3_dims:
            val = r["r3"].get(d, float("nan"))
            row += f"  {val:16.4f}"
        print(row)


def main():
    parser = argparse.ArgumentParser(description="F1 audio diagnostics")
    parser.add_argument("--relay", type=str, default=None,
                        help="Only process a specific relay (e.g., bch, pscl)")
    parser.add_argument("--file", type=str, default=None,
                        help="Process a single file (e.g., bch/01_unison_rich.wav)")
    parser.add_argument("--compact", action="store_true",
                        help="Compact output (skip near-zero dimensions)")
    parser.add_argument("--source", choices=["synthetic", "midi", "both"],
                        default="synthetic",
                        help="Audio source: synthetic (f1/), midi (f1_midi/), both")
    args = parser.parse_args()

    # Determine audio directory based on source
    source_dirs = []
    if args.source in ("synthetic", "both"):
        source_dirs.append(("synthetic", AUDIO_DIR))
    if args.source in ("midi", "both"):
        midi_dir = _ROOT / "Test-Audio" / "micro_beliefs" / "f1_midi"
        source_dirs.append(("midi", midi_dir))

    if not source_dirs:
        print("No source selected.")
        sys.exit(1)

    for label, d in source_dirs:
        if not d.exists():
            print(f"Audio directory not found: {d}")
            print(f"Run the appropriate generate script first.")
            sys.exit(1)

    print(f"Initialising pipeline (R³→H³→C³) ...")
    t0 = time.time()
    runner = MicroBeliefRunner()
    init_time = time.time() - t0
    print(f"Pipeline ready in {init_time:.1f}s")
    print(f"  Mechanisms: {len(runner.nuclei)}")
    print(f"  Beliefs: {len(runner._beliefs_by_name)}")
    print(f"  H³ demands: {len(runner.h3_demands)} tuples")

    total_files = 0
    total_time = 0.0

    for source_label, audio_dir in source_dirs:
        print(f"\n{'#'*80}")
        print(f"  SOURCE: {source_label.upper()} — {audio_dir.relative_to(_ROOT)}")
        print(f"{'#'*80}")

        # Collect WAV files
        if args.file:
            wav_files = [(audio_dir / args.file,
                          args.file.split("/")[0] if "/" in args.file else "unknown")]
        elif args.relay:
            relay_dir = audio_dir / args.relay
            if not relay_dir.exists():
                print(f"Relay directory not found: {relay_dir}")
                continue
            wav_files = [(f, args.relay) for f in sorted(relay_dir.glob("*.wav"))]
        else:
            wav_files = []
            for relay in F1_BELIEFS:
                relay_dir = audio_dir / relay
                if relay_dir.exists():
                    for f in sorted(relay_dir.glob("*.wav")):
                        wav_files.append((f, relay))

        if not wav_files:
            print("No WAV files found.")
            continue

        print(f"\nProcessing {len(wav_files)} WAV files ...")

        # Group results by relay for comparison tables
        results_by_relay: dict[str, list[dict]] = {}

        for wav_path, relay in wav_files:
            t0 = time.time()
            result = diagnose_file(runner, wav_path, relay, compact=args.compact)
            elapsed = time.time() - t0
            total_time += elapsed
            print(f"\n  ⏱ {elapsed:.2f}s")
            results_by_relay.setdefault(relay, []).append(result)

        # Print comparison tables
        for relay, results in results_by_relay.items():
            print_comparison_table(results, relay)

        total_files += len(wav_files)

    print(f"\n\n{'='*80}")
    print(f"  DONE — {total_files} files processed in {total_time:.1f}s")
    print(f"{'='*80}")


if __name__ == "__main__":
    main()
