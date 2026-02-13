"""
precompute_fft.py — Extract FFT spectral peaks from WAV for SRC⁹-Studio visualization.

Output: JSON with top N frequency peaks per frame, suitable for fluid sim playback.
Frequency range: 20 Hz – 4000 Hz, logarithmic spacing assumed downstream.

Usage:
    python3 scripts/precompute_fft.py <input.wav> <output.json> [--fps 60] [--peaks 48]
"""

import sys
import json
import numpy as np
from scipy.io import wavfile
from pathlib import Path

def precompute(wav_path, out_path, fps=60, fft_size=4096, peaks_per_frame=48,
               min_freq=20.0, max_freq=4000.0, noise_gate=0.015):
    print(f"Reading {wav_path} ...")
    sr, data = wavfile.read(wav_path)

    # Convert to mono float32 [-1, 1]
    if data.ndim == 2:
        data = data.mean(axis=1)
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.int32:
        data = data.astype(np.float32) / 2147483648.0
    elif data.dtype == np.float64:
        data = data.astype(np.float32)

    duration_s = len(data) / sr
    hop = int(sr / fps)
    num_frames = int(np.ceil(len(data) / hop))

    # Frequency axis
    freqs = np.fft.rfftfreq(fft_size, 1.0 / sr)
    min_bin = int(np.searchsorted(freqs, min_freq))
    max_bin = int(np.searchsorted(freqs, max_freq))
    band_freqs = freqs[min_bin:max_bin + 1]

    # Hann window
    window = np.hanning(fft_size)

    print(f"  Sample rate: {sr} Hz")
    print(f"  Duration: {duration_s:.2f}s")
    print(f"  FFT size: {fft_size}")
    print(f"  Hop: {hop} samples ({fps} fps)")
    print(f"  Frames: {num_frames}")
    print(f"  Freq bins in [{min_freq}-{max_freq}Hz]: {len(band_freqs)} (bins {min_bin}-{max_bin})")
    print(f"  Peaks per frame: {peaks_per_frame}")

    frames = []

    for i in range(num_frames):
        start = i * hop
        end = start + fft_size

        # Zero-pad if needed at the end
        if end > len(data):
            chunk = np.zeros(fft_size, dtype=np.float32)
            chunk[:len(data) - start] = data[start:]
        else:
            chunk = data[start:end]

        # Windowed FFT
        spectrum = np.abs(np.fft.rfft(chunk * window))

        # Normalize to 0-1 range (relative to max possible)
        spectrum = spectrum / (fft_size / 2)

        # Extract band of interest
        band = spectrum[min_bin:max_bin + 1]

        # -60 dB relative threshold: only keep bins within 60dB of frame peak
        peak_amp = band.max()
        if peak_amp < 1e-10:
            frames.append([])
            continue
        db_threshold = peak_amp * 10 ** (-60 / 20)  # -60 dB below peak
        threshold = max(noise_gate, db_threshold)

        above_gate = np.where(band > threshold)[0]
        if len(above_gate) == 0:
            frames.append([])
            continue

        # Sort by amplitude, take top N
        amplitudes = band[above_gate]
        top_indices = np.argsort(amplitudes)[::-1][:peaks_per_frame]

        frame_peaks = []
        for idx in top_indices:
            bin_idx = above_gate[idx]
            freq = float(band_freqs[bin_idx])
            amp = float(amplitudes[idx])
            # Round for compact JSON
            frame_peaks.append([round(freq, 1), round(amp, 4)])

        frames.append(frame_peaks)

    result = {
        "meta": {
            "source": Path(wav_path).name,
            "sample_rate": int(sr),
            "duration_s": round(duration_s, 3),
            "fft_size": fft_size,
            "frame_rate": fps,
            "num_frames": num_frames,
            "peaks_per_frame": peaks_per_frame,
            "min_freq": min_freq,
            "max_freq": max_freq,
            "noise_gate": noise_gate,
        },
        "frames": frames,
    }

    print(f"\nWriting {out_path} ...")
    with open(out_path, 'w') as f:
        json.dump(result, f, separators=(',', ':'))

    file_size = Path(out_path).stat().st_size
    non_empty = sum(1 for fr in frames if len(fr) > 0)
    print(f"  File size: {file_size / 1024 / 1024:.2f} MB")
    print(f"  Non-empty frames: {non_empty}/{num_frames}")
    print("Done.")


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python3 precompute_fft.py <input.wav> <output.json> [--fps N] [--peaks N]")
        sys.exit(1)

    wav = sys.argv[1]
    out = sys.argv[2]

    kwargs = {}
    args = sys.argv[3:]
    i = 0
    while i < len(args):
        if args[i] == '--fps' and i + 1 < len(args):
            kwargs['fps'] = int(args[i + 1]); i += 2
        elif args[i] == '--peaks' and i + 1 < len(args):
            kwargs['peaks_per_frame'] = int(args[i + 1]); i += 2
        else:
            i += 1

    precompute(wav, out, **kwargs)
