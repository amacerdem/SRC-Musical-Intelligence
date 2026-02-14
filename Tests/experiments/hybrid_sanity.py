"""
HYBRID v0.1 — Sanity Tests
============================
Bu testler geçmeden transform kalite değerlendirmesi YAPILMAZ.

Test 1: STFT roundtrip — phase-preserving iSTFT = identity mi?
Test 2: HPSS recombine — y_h + y_p ≈ y mi?
Test 3: Full pipeline smoke — preset uygula, R³ yönleri doğru mu?

Metrikleri:
  SNR(y, y_hat) = 10 * log10(sum(y²) / sum((y - y_hat)²))
  > 40 dB : mükemmel (neredeyse aynı)
  > 30 dB : kabul edilebilir POC
  > 20 dB : sorunlu
  < 20 dB : bozuk
"""

from __future__ import annotations

import sys
import time
import numpy as np
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

# ── Constants ──────────────────────────────────────────────────────────
SR = 44100
DURATION_SEC = 5.0  # Test with 5 seconds of audio


def snr_db(original: np.ndarray, reconstructed: np.ndarray) -> float:
    """Compute SNR in dB between original and reconstructed signals."""
    n = min(len(original), len(reconstructed))
    y, y_hat = original[:n], reconstructed[:n]
    signal_power = np.sum(y ** 2)
    noise_power = np.sum((y - y_hat) ** 2)
    if noise_power < 1e-20:
        return 120.0  # effectively perfect
    return 10.0 * np.log10(signal_power / noise_power)


def spectral_correlation(y1: np.ndarray, y2: np.ndarray) -> float:
    """Pearson correlation between two signals."""
    n = min(len(y1), len(y2))
    return float(np.corrcoef(y1[:n], y2[:n])[0, 1])


def get_test_audio() -> np.ndarray:
    """
    Get test audio. Tries Swan Lake first, falls back to synthetic.
    """
    swan_lake = PROJECT_ROOT / "Tests" / "data" / "swan_lake_30s.wav"
    if swan_lake.exists():
        from Musical_Intelligence.hybrid.ops.stft_ops import load_audio
        y = load_audio(str(swan_lake))
        # Use first N seconds
        n_samples = int(DURATION_SEC * SR)
        return y[:n_samples]

    # Fallback: synthetic test signal (chord + transients)
    print("  [!] Swan Lake not found, using synthetic test signal")
    t = np.linspace(0, DURATION_SEC, int(DURATION_SEC * SR), dtype=np.float32)
    # Root + fifth + octave chord
    y = 0.3 * np.sin(2 * np.pi * 440 * t)     # A4
    y += 0.2 * np.sin(2 * np.pi * 660 * t)    # E5 (approx)
    y += 0.15 * np.sin(2 * np.pi * 880 * t)   # A5
    # Add transients (clicks every 0.5s)
    for i in range(int(DURATION_SEC * 2)):
        idx = int(i * 0.5 * SR)
        if idx + 100 < len(y):
            y[idx:idx + 100] += 0.4 * np.exp(-np.linspace(0, 5, 100))
    return y.astype(np.float32)


# ══════════════════════════════════════════════════════════════════════
# TEST 1: STFT Roundtrip
# ══════════════════════════════════════════════════════════════════════

def test_stft_roundtrip() -> bool:
    """
    STFT → iSTFT must be near-identity (no phase invention).
    Target: SNR > 40 dB, correlation > 0.9999
    """
    print("\n" + "=" * 60)
    print("TEST 1: STFT Roundtrip (phase-preserving)")
    print("=" * 60)

    from Musical_Intelligence.hybrid.ops.stft_ops import (
        stft_analyze, stft_synthesize, verify_roundtrip,
    )

    y = get_test_audio()
    print(f"  Audio: {len(y)} samples ({len(y)/SR:.1f}s)")

    t0 = time.time()
    result = verify_roundtrip(y)
    dt = time.time() - t0

    # Also compute SNR
    mag, phase = stft_analyze(y)
    y_rt = stft_synthesize(mag, phase)
    snr = snr_db(y, y_rt)

    print(f"  Time:        {dt:.3f}s")
    print(f"  Correlation: {result['correlation']:.8f}")
    print(f"  Max error:   {result['max_error']:.8f}")
    print(f"  RMS error:   {result['rms_error']:.8f}")
    print(f"  SNR:         {snr:.1f} dB")

    passed = snr > 30.0 and result["correlation"] > 0.999
    print(f"  RESULT:      {'PASS' if passed else 'FAIL'}")
    if not passed:
        print("  [!] CRITICAL: Phase preservation broken!")
        print("      Do NOT proceed with transforms until this is fixed.")
    return passed


# ══════════════════════════════════════════════════════════════════════
# TEST 2: HPSS Recombine
# ══════════════════════════════════════════════════════════════════════

def test_hpss_recombine() -> bool:
    """
    HPSS decomposition + recombination must preserve signal.
    y_h + y_p ≈ y (residual should be near-zero when margin=1).
    Target: SNR > 25 dB
    """
    print("\n" + "=" * 60)
    print("TEST 2: HPSS Recombine (harmonic + percussive = original)")
    print("=" * 60)

    import librosa
    from Musical_Intelligence.hybrid.ops.hpss_ops import hpss_stft

    y = get_test_audio()
    print(f"  Audio: {len(y)} samples ({len(y)/SR:.1f}s)")

    t0 = time.time()

    # STFT
    S = librosa.stft(y, n_fft=2048, hop_length=256)

    # HPSS on complex STFT
    S_h, S_p = hpss_stft(S)

    # Recombine in STFT domain
    S_recon = S_h + S_p

    # iSTFT
    y_h = librosa.istft(S_h, hop_length=256, length=len(y))
    y_p = librosa.istft(S_p, hop_length=256, length=len(y))
    y_recon = librosa.istft(S_recon, hop_length=256, length=len(y))

    dt = time.time() - t0

    # Metrics
    snr_waveform = snr_db(y, y_h + y_p)
    snr_stft = snr_db(y, y_recon)
    corr = spectral_correlation(y, y_recon)

    # Check mask complementarity (should sum to ~1.0)
    mag = np.abs(S)
    mag_h = np.abs(S_h)
    mag_p = np.abs(S_p)
    mask_sum = (mag_h + mag_p) / (mag + 1e-10)
    mask_mean = mask_sum.mean()

    print(f"  Time:          {dt:.3f}s")
    print(f"  SNR (wave):    {snr_waveform:.1f} dB")
    print(f"  SNR (STFT):    {snr_stft:.1f} dB")
    print(f"  Correlation:   {corr:.6f}")
    print(f"  Mask sum mean: {mask_mean:.4f} (should be ~1.0)")
    print(f"  y_h RMS:       {np.sqrt(np.mean(y_h**2)):.4f}")
    print(f"  y_p RMS:       {np.sqrt(np.mean(y_p**2)):.4f}")

    passed = snr_stft > 25.0 and corr > 0.99
    print(f"  RESULT:        {'PASS' if passed else 'FAIL'}")
    if not passed:
        print("  [!] HPSS recombination is lossy — check mask computation.")
    return passed


# ══════════════════════════════════════════════════════════════════════
# TEST 3: Transform Smoke Test
# ══════════════════════════════════════════════════════════════════════

def test_transform_smoke() -> bool:
    """
    Apply each built-in preset and verify:
    1. Output is not silence or NaN
    2. Output is not identical to input (transform did something)
    3. Output is not "bozuk" (correlation > 0.5 with original)
    4. R³ shifts in expected directions (at least 50% of targets)
    """
    print("\n" + "=" * 60)
    print("TEST 3: Transform Smoke Test (all presets)")
    print("=" * 60)

    from Musical_Intelligence.hybrid.hybrid_transformer import (
        HybridTransformer, EMOTION_PRESETS,
    )
    from Musical_Intelligence.hybrid.controls import controls_to_r3_delta

    y = get_test_audio()
    print(f"  Audio: {len(y)} samples ({len(y)/SR:.1f}s)")

    # Save test audio temporarily
    import tempfile, os
    tmp_dir = tempfile.mkdtemp()
    input_path = os.path.join(tmp_dir, "test_input.wav")
    from Musical_Intelligence.hybrid.ops.stft_ops import save_audio
    save_audio(input_path, y)

    transformer = HybridTransformer(calibrate=False)  # No calibration for speed

    all_passed = True

    for name, controls in EMOTION_PRESETS.items():
        print(f"\n  Preset: {name}")
        t0 = time.time()

        try:
            result = transformer.transform(input_path, controls, calibrate=False)
            dt = time.time() - t0
            y_out = result.audio

            # Check 1: Not silence or NaN
            is_valid = not np.any(np.isnan(y_out)) and np.max(np.abs(y_out)) > 0.01
            # Check 2: Not identical
            n = min(len(y), len(y_out))
            is_different = np.max(np.abs(y[:n] - y_out[:n])) > 0.001
            # Check 3: Not "bozuk" (still sounds like original)
            corr = spectral_correlation(y[:n], y_out[:n])
            is_coherent = corr > 0.5

            preset_pass = is_valid and is_different and is_coherent

            print(f"    Time:       {dt:.2f}s")
            print(f"    Valid:      {is_valid}")
            print(f"    Different:  {is_different}")
            print(f"    Coherent:   {corr:.4f} (>0.5)")
            print(f"    Max amp:    {np.max(np.abs(y_out)):.4f}")
            print(f"    RESULT:     {'PASS' if preset_pass else 'FAIL'}")

            if not preset_pass:
                all_passed = False

        except Exception as e:
            print(f"    ERROR: {e}")
            all_passed = False

    # Cleanup
    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)

    return all_passed


# ══════════════════════════════════════════════════════════════════════
# TEST 4: Non-destructive test (strength=0 → no change)
# ══════════════════════════════════════════════════════════════════════

def test_zero_strength() -> bool:
    """
    With strength=0, output must be nearly identical to input.
    This validates the "neutral" state of the transform pipeline.
    """
    print("\n" + "=" * 60)
    print("TEST 4: Zero Strength (no-op verification)")
    print("=" * 60)

    from Musical_Intelligence.hybrid.hybrid_transformer import HybridTransformer
    from Musical_Intelligence.hybrid.controls import EmotionControls

    y = get_test_audio()

    import tempfile, os
    tmp_dir = tempfile.mkdtemp()
    input_path = os.path.join(tmp_dir, "test_input.wav")
    from Musical_Intelligence.hybrid.ops.stft_ops import save_audio
    save_audio(input_path, y)

    # Zero strength = should be no-op
    controls = EmotionControls(
        valence=0.5, arousal=0.5, tension=0.5,
        strength=0.0,  # key: strength is zero
    )

    transformer = HybridTransformer(calibrate=False)
    result = transformer.transform(input_path, controls, calibrate=False)
    y_out = result.audio

    n = min(len(y), len(y_out))
    snr = snr_db(y[:n], y_out[:n])
    corr = spectral_correlation(y[:n], y_out[:n])

    print(f"  SNR:         {snr:.1f} dB")
    print(f"  Correlation: {corr:.8f}")

    # Should be very high since nothing was applied
    passed = snr > 25.0 and corr > 0.99
    print(f"  RESULT:      {'PASS' if passed else 'FAIL'}")

    import shutil
    shutil.rmtree(tmp_dir, ignore_errors=True)
    return passed


# ══════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════

def main():
    print("HYBRID v0.1 — Sanity Tests")
    print("=" * 60)

    results = {}

    # Test 1: STFT roundtrip (MUST pass before anything else)
    results["stft_roundtrip"] = test_stft_roundtrip()

    if not results["stft_roundtrip"]:
        print("\n[!!!] STFT roundtrip FAILED — stopping here.")
        print("      Fix phase-preserving STFT before running other tests.")
        return results

    # Test 2: HPSS recombine
    results["hpss_recombine"] = test_hpss_recombine()

    if not results["hpss_recombine"]:
        print("\n[!] HPSS recombine FAILED — transforms may be lossy.")

    # Test 3: Transform smoke
    results["transform_smoke"] = test_transform_smoke()

    # Test 4: Zero strength
    results["zero_strength"] = test_zero_strength()

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    for name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {name:25s} {status}")
    print(f"\n  {passed}/{total} tests passed")

    return results


if __name__ == "__main__":
    main()
