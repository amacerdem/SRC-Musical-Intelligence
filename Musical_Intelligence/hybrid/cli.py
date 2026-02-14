"""
CLI for HYBRID v0.2 emotion + structure transform.

Usage:
    # Timbral transform (v0.1)
    python -m Musical_Intelligence.hybrid.cli input.wav -o out.wav --preset joyful

    # Structural transforms (v0.2)
    python -m Musical_Intelligence.hybrid.cli input.wav -o out.wav --tempo-shift 0.08 --swing 0.6
    python -m Musical_Intelligence.hybrid.cli input.wav -o out.wav --harmonic-mode-bias -0.7 --tension 0.6
    python -m Musical_Intelligence.hybrid.cli input.wav -o out.wav --preset rubato_minor

    # Batch: all presets
    python -m Musical_Intelligence.hybrid.cli input.wav --batch --output-dir results/

    # STFT roundtrip test
    python -m Musical_Intelligence.hybrid.cli input.wav --roundtrip-test
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="HYBRID v0.2 — Emotion + Structure Transform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.wav -o joyful.wav --preset joyful
  %(prog)s input.wav -o out.wav --valence 0.5 --arousal 0.3
  %(prog)s input.wav -o out.wav --tempo-shift 0.08 --swing 0.6
  %(prog)s input.wav -o out.wav --harmonic-mode-bias -0.7 --tension 0.6
  %(prog)s input.wav -o out.wav --preset rubato_minor
  %(prog)s input.wav --batch --output-dir results/
  %(prog)s input.wav --roundtrip-test
        """,
    )

    parser.add_argument("input", help="Input audio file path")
    parser.add_argument("-o", "--output", help="Output audio file path")
    parser.add_argument("--output-dir", help="Output directory for batch mode")

    # v0.1: Emotion sliders
    g1 = parser.add_argument_group("Emotion sliders (v0.1)")
    g1.add_argument("--valence", type=float, default=0.0)
    g1.add_argument("--arousal", type=float, default=0.0)
    g1.add_argument("--tension", type=float, default=0.0)
    g1.add_argument("--warmth", type=float, default=0.0)
    g1.add_argument("--brightness", type=float, default=0.0)

    # v0.2: Structural sliders
    g2 = parser.add_argument_group("Structure sliders (v0.2)")
    g2.add_argument("--tempo-shift", type=float, default=0.0,
                     help="Relative BPM change (-0.2 to +0.2)")
    g2.add_argument("--rubato", type=float, default=0.0,
                     help="Tempo variation (0 to 1)")
    g2.add_argument("--swing", type=float, default=0.0,
                     help="Off-beat shift (-1 to +1; +1 = jazz swing)")
    g2.add_argument("--push-pull", type=float, default=0.0,
                     help="Micro-timing offset (-1 to +1)")
    g2.add_argument("--rhythm-density", type=float, default=0.0,
                     help="Event density (-1 to +1)")
    g2.add_argument("--harmonic-mode-bias", type=float, default=0.0,
                     help="Major/minor tilt (-1 to +1)")
    g2.add_argument("--harmonic-rhythm", type=float, default=0.0,
                     help="Chord-change rate feel (-1 to +1)")

    # Global
    parser.add_argument("--strength", type=float, default=0.6)
    parser.add_argument("--preset", choices=[
        "joyful", "melancholic", "intense", "calm", "tense", "bright_warm",
        "rubato_minor", "swing_bright", "driving", "spacious",
    ])
    parser.add_argument("--batch", action="store_true")
    parser.add_argument("--no-calibrate", action="store_true")
    parser.add_argument("--roundtrip-test", action="store_true")

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

    from Musical_Intelligence.hybrid.hybrid_transformer import (
        HybridTransformer, EMOTION_PRESETS,
    )
    from Musical_Intelligence.hybrid.controls import EmotionControls

    transformer = HybridTransformer(calibrate=not args.no_calibrate)

    # ── Batch ──
    if args.batch:
        output_dir = args.output_dir or "hybrid_output"
        print(f"Batch mode: {len(EMOTION_PRESETS)} presets → {output_dir}/")
        transformer.transform_batch(args.input, EMOTION_PRESETS, output_dir)
        print("Done!")
        sys.exit(0)

    # ── Single ──
    if args.preset:
        controls = EMOTION_PRESETS[args.preset]
        print(f"Preset: {args.preset}")
    else:
        controls = EmotionControls(
            valence=args.valence, arousal=args.arousal,
            tension=args.tension, warmth=args.warmth,
            brightness=args.brightness,
            tempo_shift=args.tempo_shift, rubato=args.rubato,
            swing=args.swing, push_pull=args.push_pull,
            rhythm_density=args.rhythm_density,
            harmonic_mode_bias=args.harmonic_mode_bias,
            harmonic_rhythm=args.harmonic_rhythm,
            strength=args.strength,
        )

    output_path = args.output
    if not output_path:
        stem = Path(args.input).stem
        tag = args.preset or "hybrid"
        output_path = f"{stem}_{tag}.wav"

    print(f"HYBRID v0.2 Transform:")
    print(f"  Input:           {args.input}")
    print(f"  Output:          {output_path}")
    print(f"  -- Emotion --")
    print(f"  Valence:         {controls.valence:+.2f}")
    print(f"  Arousal:         {controls.arousal:+.2f}")
    print(f"  Tension:         {controls.tension:+.2f}")
    print(f"  Warmth:          {controls.warmth:+.2f}")
    print(f"  Brightness:      {controls.brightness:+.2f}")
    print(f"  -- Structure --")
    print(f"  Tempo shift:     {controls.tempo_shift:+.3f}")
    print(f"  Rubato:          {controls.rubato:.2f}")
    print(f"  Swing:           {controls.swing:+.2f}")
    print(f"  Push/pull:       {controls.push_pull:+.2f}")
    print(f"  Rhythm density:  {controls.rhythm_density:+.2f}")
    print(f"  Mode bias:       {controls.harmonic_mode_bias:+.2f}")
    print(f"  Harmonic rhythm: {controls.harmonic_rhythm:+.2f}")
    print(f"  -- Global --")
    print(f"  Strength:        {controls.strength:.2f}")
    print(f"  Calibrate:       {not args.no_calibrate}")
    print()

    result = transformer.transform(args.input, controls)
    result.save(output_path)
    print(f"Done! Saved to {output_path}")

    if result.score_proxy:
        s = result.score_proxy
        print(f"\nScore proxy:")
        print(f"  Tempo:  {s.tempo:.1f} BPM")
        print(f"  Beats:  {len(s.beat_times)}")
        print(f"  Key:    {['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][s.key_idx]} {s.mode} (conf={s.key_confidence:.2f})")

    if result.calibration_result is not None:
        cal = result.calibration_result
        print(f"\nCalibration: {cal.iterations} iterations, final strength={cal.final_strength:.3f}")


if __name__ == "__main__":
    main()
