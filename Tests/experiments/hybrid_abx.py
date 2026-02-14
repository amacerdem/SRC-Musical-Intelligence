"""
ABX Listening Test Harness
============================
Quick perceptual validation: "filtre gibi mi, yoksa gerçekten duygu değişimi var mı?"

Generates randomized A/B pairs for blind listening comparison.

Usage:
    python Tests/experiments/hybrid_abx.py [audio_file]

Output:
    Tests/reports/hybrid_abx/
    ├── trial_01_A.wav   (original or transformed, random order)
    ├── trial_01_B.wav
    ├── trial_02_A.wav
    ├── ...
    └── answer_key.txt   (which is which, don't peek!)
"""

from __future__ import annotations

import os
import sys
import random
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))


def generate_abx_trials(
    audio_path: str,
    output_dir: str = "Tests/reports/hybrid_abx",
    duration_sec: float = 10.0,
) -> None:
    """Generate ABX trial pairs for all presets."""
    from Musical_Intelligence.hybrid.hybrid_transformer import (
        HybridTransformer, EMOTION_PRESETS,
    )
    from Musical_Intelligence.hybrid.ops.stft_ops import load_audio, save_audio

    os.makedirs(output_dir, exist_ok=True)

    # Load audio
    y = load_audio(audio_path)
    n_samples = int(duration_sec * 44100)
    if len(y) > n_samples:
        y = y[:n_samples]

    # Save temp input
    import tempfile
    tmp = tempfile.mktemp(suffix=".wav")
    save_audio(tmp, y)

    transformer = HybridTransformer(calibrate=False)
    answer_key = []

    for i, (name, controls) in enumerate(EMOTION_PRESETS.items(), 1):
        # Transform
        result = transformer.transform(tmp, controls, calibrate=False)
        y_trans = result.audio

        # Random assignment: A=original or A=transformed
        original_is_A = random.random() < 0.5

        if original_is_A:
            y_A, y_B = y, y_trans
            answer = f"A=original, B={name}"
        else:
            y_A, y_B = y_trans, y
            answer = f"A={name}, B=original"

        # Trim to same length
        n = min(len(y_A), len(y_B))

        save_audio(os.path.join(output_dir, f"trial_{i:02d}_A.wav"), y_A[:n])
        save_audio(os.path.join(output_dir, f"trial_{i:02d}_B.wav"), y_B[:n])

        answer_key.append(f"Trial {i:02d} ({name}): {answer}")
        print(f"  Trial {i:02d}: {name}")

    # Save answer key
    key_path = os.path.join(output_dir, "answer_key.txt")
    with open(key_path, "w") as f:
        f.write("ABX ANSWER KEY — Don't peek before listening!\n")
        f.write("=" * 50 + "\n\n")
        f.write("Question for each trial:\n")
        f.write("  'Which sounds more [preset_name]? A or B?'\n\n")
        for line in answer_key:
            f.write(line + "\n")

    os.unlink(tmp)
    print(f"\nDone! {len(answer_key)} trials saved to {output_dir}/")
    print(f"Answer key: {key_path}")
    print("\nListening instructions:")
    print("  1. Open trial_XX_A.wav and trial_XX_B.wav")
    print("  2. Listen to both")
    print("  3. Ask: 'Which one sounds more emotional/transformed?'")
    print("  4. Check answer_key.txt after all trials")


def main():
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
    else:
        # Default to Swan Lake
        audio_path = str(
            PROJECT_ROOT / "Test-Audio"
            / "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato"
            " - Pyotr Ilyich Tchaikovsky.wav"
        )

    if not os.path.exists(audio_path):
        print(f"Audio file not found: {audio_path}")
        sys.exit(1)

    print("ABX Listening Test Generator")
    print(f"Input: {audio_path}")
    print()
    generate_abx_trials(audio_path)


if __name__ == "__main__":
    main()
