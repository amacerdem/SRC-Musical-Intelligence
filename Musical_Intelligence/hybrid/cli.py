"""
CLI for HYBRID emotion transform.

Usage:
    # Single transform with sliders
    python -m Musical_Intelligence.hybrid.cli input.wav -o output.wav \
        --valence 0.5 --arousal 0.3 --tension -0.2 --strength 0.6

    # Use a named preset
    python -m Musical_Intelligence.hybrid.cli input.wav -o output.wav --preset joyful

    # Batch: apply all presets for comparison
    python -m Musical_Intelligence.hybrid.cli input.wav --batch --output-dir results/

    # No calibration (faster, less consistent)
    python -m Musical_Intelligence.hybrid.cli input.wav -o output.wav --preset intense --no-calibrate

    # STFT roundtrip test (verify phase preservation)
    python -m Musical_Intelligence.hybrid.cli input.wav --roundtrip-test
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="HYBRID v0.1 — Emotion Override Transform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.wav -o joyful.wav --preset joyful
  %(prog)s input.wav -o custom.wav --valence 0.5 --arousal 0.3
  %(prog)s input.wav --batch --output-dir results/
  %(prog)s input.wav --roundtrip-test
        """,
    )

    parser.add_argument("input", help="Input audio file path")
    parser.add_argument("-o", "--output", help="Output audio file path")
    parser.add_argument("--output-dir", help="Output directory for batch mode")

    # Emotion sliders
    parser.add_argument("--valence", type=float, default=0.0,
                        help="Valence: -1 (negative) to +1 (positive)")
    parser.add_argument("--arousal", type=float, default=0.0,
                        help="Arousal: -1 (calm) to +1 (energetic)")
    parser.add_argument("--tension", type=float, default=0.0,
                        help="Tension: -1 (relaxed) to +1 (tense)")
    parser.add_argument("--warmth", type=float, default=0.0,
                        help="Warmth: -1 (cool) to +1 (warm)")
    parser.add_argument("--brightness", type=float, default=0.0,
                        help="Brightness: -1 (dark) to +1 (bright)")
    parser.add_argument("--strength", type=float, default=0.6,
                        help="Global effect strength: 0 (none) to 1 (full)")

    # Preset
    parser.add_argument("--preset", choices=[
        "joyful", "melancholic", "intense", "calm", "tense", "bright_warm",
    ], help="Use a named emotion preset")

    # Modes
    parser.add_argument("--batch", action="store_true",
                        help="Apply all presets for A/B comparison")
    parser.add_argument("--no-calibrate", action="store_true",
                        help="Skip R³ calibration (faster but less consistent)")
    parser.add_argument("--roundtrip-test", action="store_true",
                        help="Run STFT roundtrip test (verify phase preservation)")

    args = parser.parse_args()

    # ── Roundtrip test ──
    if args.roundtrip_test:
        from Musical_Intelligence.hybrid.ops.stft_ops import load_audio, verify_roundtrip
        print(f"STFT Roundtrip Test: {args.input}")
        y = load_audio(args.input)
        result = verify_roundtrip(y)
        print(f"  Correlation: {result['correlation']:.6f}")
        print(f"  Max error:   {result['max_error']:.6f}")
        print(f"  RMS error:   {result['rms_error']:.6f}")
        print(f"  PASS:        {result['pass']}")
        sys.exit(0 if result["pass"] else 1)

    # ── Import transformer ──
    from Musical_Intelligence.hybrid.hybrid_transformer import (
        HybridTransformer, EMOTION_PRESETS,
    )
    from Musical_Intelligence.hybrid.controls import EmotionControls

    transformer = HybridTransformer(calibrate=not args.no_calibrate)

    # ── Batch mode ──
    if args.batch:
        output_dir = args.output_dir or "hybrid_output"
        print(f"Batch mode: applying {len(EMOTION_PRESETS)} presets")
        print(f"  Input:  {args.input}")
        print(f"  Output: {output_dir}/")
        results = transformer.transform_batch(
            args.input, EMOTION_PRESETS, output_dir,
        )
        print(f"\nDone! {len(results)} transforms saved.")
        sys.exit(0)

    # ── Single transform ──
    if args.preset:
        controls = EMOTION_PRESETS[args.preset]
        print(f"Preset: {args.preset}")
    else:
        controls = EmotionControls(
            valence=args.valence,
            arousal=args.arousal,
            tension=args.tension,
            warmth=args.warmth,
            brightness=args.brightness,
            strength=args.strength,
        )

    output_path = args.output
    if not output_path:
        stem = Path(args.input).stem
        tag = args.preset or "hybrid"
        output_path = f"{stem}_{tag}.wav"

    print(f"HYBRID Transform:")
    print(f"  Input:      {args.input}")
    print(f"  Output:     {output_path}")
    print(f"  Valence:    {controls.valence:+.2f}")
    print(f"  Arousal:    {controls.arousal:+.2f}")
    print(f"  Tension:    {controls.tension:+.2f}")
    print(f"  Warmth:     {controls.warmth:+.2f}")
    print(f"  Brightness: {controls.brightness:+.2f}")
    print(f"  Strength:   {controls.strength:.2f}")
    print(f"  Calibrate:  {not args.no_calibrate}")
    print()

    result = transformer.transform(args.input, controls)
    result.save(output_path)

    print(f"Done! Saved to {output_path}")

    if result.calibration_result is not None:
        cal = result.calibration_result
        print(f"\nCalibration:")
        print(f"  Iterations:     {cal.iterations}")
        print(f"  Final strength: {cal.final_strength:.3f}")
        if cal.error_history:
            print(f"  Error history:  {[f'{e:.4f}' for e in cal.error_history]}")
        if cal.r3_deltas_target:
            print(f"\n  R³ Delta Targets vs Achieved:")
            for idx in sorted(cal.r3_deltas_target.keys()):
                target = cal.r3_deltas_target[idx]
                achieved = cal.r3_deltas_achieved.get(idx, 0.0)
                hit = "OK" if abs(target - achieved) < abs(target) * 0.5 else "MISS"
                print(f"    [{idx:3d}] target={target:+.4f}  actual={achieved:+.4f}  {hit}")


if __name__ == "__main__":
    main()
