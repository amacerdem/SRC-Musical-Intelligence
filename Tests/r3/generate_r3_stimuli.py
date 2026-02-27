"""Generate synthetic audio stimuli for R³ dimension testing.

Creates 18 WAV files in Tests/r3/stimuli/, each designed to activate specific
R³ dimensions in predictable ways. All files are 3 seconds at 44100 Hz mono.

Usage:
    python Tests/r3/generate_r3_stimuli.py
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

SAMPLE_RATE = 44100
DURATION_S = 3.0
N_SAMPLES = int(SAMPLE_RATE * DURATION_S)
STIMULI_DIR = Path(__file__).resolve().parent / "stimuli"


def _t() -> np.ndarray:
    """Time axis [0, DURATION_S)."""
    return np.linspace(0, DURATION_S, N_SAMPLES, endpoint=False, dtype=np.float32)


def _sine(freq: float, amp: float = 0.8) -> np.ndarray:
    return (amp * np.sin(2 * np.pi * freq * _t())).astype(np.float32)


def _save(name: str, data: np.ndarray) -> Path:
    import soundfile as sf

    path = STIMULI_DIR / f"{name}.wav"
    sf.write(str(path), data.astype(np.float32), SAMPLE_RATE)
    return path


def generate_all() -> dict[str, Path]:
    """Generate all 18 stimuli. Returns {name: path}."""
    STIMULI_DIR.mkdir(parents=True, exist_ok=True)
    t = _t()
    catalog = {}

    # 1. Silence (near-zero to avoid div-by-zero in max-norm)
    catalog["silence"] = _save("silence", np.full(N_SAMPLES, 1e-6, dtype=np.float32))

    # 2. Pure 440 Hz (A4) — tonal, high pitch salience
    catalog["pure_440"] = _save("pure_440", _sine(440))

    # 3. Pure 100 Hz — low pitch, high warmth
    catalog["pure_100"] = _save("pure_100", _sine(100))

    # 4. Pure 4000 Hz — high pitch, high sharpness
    catalog["pure_4000"] = _save("pure_4000", _sine(4000))

    # 5. White noise — high entropy, flat spectrum
    rng = np.random.default_rng(42)
    noise = (rng.standard_normal(N_SAMPLES) * 0.3).astype(np.float32)
    catalog["white_noise"] = _save("white_noise", noise)

    # 6. Harmonic stack: 440 + 880 + 1320 + 1760 + 2200 (natural partials)
    harmonic = np.zeros(N_SAMPLES, dtype=np.float32)
    for i, n in enumerate([1, 2, 3, 4, 5]):
        harmonic += (0.8 / n) * np.sin(2 * np.pi * 440 * n * t).astype(np.float32)
    catalog["harmonic_440"] = _save("harmonic_440", harmonic * 0.5)

    # 7. Inharmonic partials: 440, 620, 910, 1370 (non-integer ratios)
    inharm = np.zeros(N_SAMPLES, dtype=np.float32)
    for f, a in [(440, 0.8), (620, 0.6), (910, 0.5), (1370, 0.3)]:
        inharm += a * np.sin(2 * np.pi * f * t).astype(np.float32)
    catalog["inharmonic"] = _save("inharmonic", inharm * 0.4)

    # 8. Loud burst: silence 1s → 100ms loud burst → silence 1.9s
    burst = np.zeros(N_SAMPLES, dtype=np.float32)
    burst_start = int(1.0 * SAMPLE_RATE)
    burst_end = int(1.1 * SAMPLE_RATE)
    burst[burst_start:burst_end] = 0.9 * np.sin(
        2 * np.pi * 440 * t[:burst_end - burst_start]
    )
    catalog["loud_burst"] = _save("loud_burst", burst)

    # 9. Crescendo: amplitude ramp 0→0.9 over 3s on 440 Hz
    envelope = np.linspace(0.0, 0.9, N_SAMPLES, dtype=np.float32)
    crescendo = envelope * np.sin(2 * np.pi * 440 * t).astype(np.float32)
    catalog["crescendo"] = _save("crescendo", crescendo)

    # 10. Clicks at 120 BPM (2 Hz) — short 5ms impulses
    clicks_120 = np.zeros(N_SAMPLES, dtype=np.float32)
    click_interval = int(SAMPLE_RATE / 2)  # 0.5s per beat
    click_len = int(0.005 * SAMPLE_RATE)
    for i in range(0, N_SAMPLES, click_interval):
        end = min(i + click_len, N_SAMPLES)
        clicks_120[i:end] = 0.9
    catalog["clicks_120bpm"] = _save("clicks_120bpm", clicks_120)

    # 11. Clicks at 60 BPM (1 Hz)
    clicks_60 = np.zeros(N_SAMPLES, dtype=np.float32)
    click_interval_60 = int(SAMPLE_RATE)  # 1s per beat
    for i in range(0, N_SAMPLES, click_interval_60):
        end = min(i + click_len, N_SAMPLES)
        clicks_60[i:end] = 0.9
    catalog["clicks_60bpm"] = _save("clicks_60bpm", clicks_60)

    # 12. Octave: 440 + 880 Hz (most consonant interval after unison)
    octave = 0.5 * _sine(440) + 0.5 * _sine(880)
    catalog["octave"] = _save("octave", octave)

    # 13. Tritone: 440 + 622.25 Hz (most dissonant interval)
    tritone = 0.5 * _sine(440) + 0.5 * _sine(440 * 2 ** (6 / 12))
    catalog["tritone"] = _save("tritone", tritone)

    # 14. Bright: sawtooth-like with strong high harmonics
    bright = np.zeros(N_SAMPLES, dtype=np.float32)
    for n in range(1, 30):
        bright += (0.5 / n) * np.sin(2 * np.pi * 2000 * n * t).astype(np.float32)
    bright = np.clip(bright * 0.3, -1, 1).astype(np.float32)
    catalog["bright"] = _save("bright", bright)

    # 15. Dark: low-frequency rich content (100 Hz fundamental + low harmonics)
    dark = np.zeros(N_SAMPLES, dtype=np.float32)
    for n in range(1, 6):
        dark += (0.8 / n ** 2) * np.sin(2 * np.pi * 80 * n * t).astype(np.float32)
    catalog["dark"] = _save("dark", dark * 0.5)

    # 16. AM 4Hz: 440Hz carrier, 4Hz AM (for fluctuation strength)
    am_env = 0.5 + 0.5 * np.sin(2 * np.pi * 4.0 * t)
    am_signal = (0.8 * am_env * np.sin(2 * np.pi * 440 * t)).astype(np.float32)
    catalog["am_4hz"] = _save("am_4hz", am_signal)

    # 17. C major chord: C4(261.63) + E4(329.63) + G4(392.00)
    major = (
        0.4 * _sine(261.63) + 0.4 * _sine(329.63) + 0.4 * _sine(392.00)
    )
    catalog["chord_major"] = _save("chord_major", np.clip(major, -1, 1))

    # 18. Steady tone (constant amplitude 440Hz — for zero spectral flux)
    catalog["steady_440"] = _save("steady_440", _sine(440, amp=0.5))

    print(f"Generated {len(catalog)} stimuli in {STIMULI_DIR}")
    for name, path in catalog.items():
        size_kb = path.stat().st_size / 1024
        print(f"  {name:20s} → {size_kb:6.1f} KB")
    return catalog


if __name__ == "__main__":
    generate_all()
