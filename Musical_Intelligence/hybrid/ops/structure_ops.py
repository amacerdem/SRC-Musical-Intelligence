"""
Score proxy extraction — beat grid, onset map, chroma, key estimation.

No full polyphonic transcription; just enough structure to guide
tempo warps, swing, and harmonic-function transforms.

Components:
  - Beat grid + downbeats (rhythm skeleton)
  - Onset map (event density)
  - Chroma + key estimate (harmonic center)
  - Chord-change proxy (chroma novelty)
"""

from __future__ import annotations

import numpy as np
from dataclasses import dataclass

from Musical_Intelligence.hybrid.ops.stft_ops import SR, HOP_LENGTH, N_FFT


# ── Score Proxy dataclass ──────────────────────────────────────────────

@dataclass
class ScoreProxy:
    """Lightweight structural representation of audio — no full transcription."""
    beat_times: np.ndarray        # (n_beats,) seconds
    tempo: float                  # BPM estimate
    onset_times: np.ndarray       # (n_onsets,) seconds
    onset_strengths: np.ndarray   # (n_onsets,) normalized [0, 1]
    chroma: np.ndarray            # (12, n_chroma_frames)
    chroma_sr: float              # chroma frame rate (Hz)
    key_idx: int                  # 0=C, 1=C#, ..., 11=B
    mode: str                     # 'major' or 'minor'
    key_confidence: float         # 0-1
    novelty: np.ndarray           # (n_chroma_frames,) chroma novelty


# ── Key templates ──────────────────────────────────────────────────────

MAJOR_TEMPLATE = np.array([1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1], dtype=np.float32)
MINOR_TEMPLATE = np.array([1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0], dtype=np.float32)
PC_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


# ── Extraction functions ───────────────────────────────────────────────

def extract_beat_grid(
    y: np.ndarray,
    sr: int = SR,
    hop_length: int = HOP_LENGTH,
) -> tuple[np.ndarray, float]:
    """
    Extract beat positions and tempo estimate.
    Uses percussive component if provided; otherwise full signal.

    Returns:
        beat_times: (n_beats,) seconds
        tempo:      estimated BPM
    """
    import librosa

    tempo, beat_frames = librosa.beat.beat_track(
        y=y, sr=sr, hop_length=hop_length, units="frames",
    )
    # librosa may return tempo as array
    if hasattr(tempo, "__len__"):
        tempo = float(tempo[0]) if len(tempo) > 0 else 120.0
    else:
        tempo = float(tempo)

    beat_times = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop_length)

    # Fallback: if too few beats detected, use onset peaks
    if len(beat_times) < 4:
        onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
        peaks = librosa.util.peak_pick(
            onset_env, pre_max=3, post_max=3, pre_avg=3, post_avg=5, delta=0.3, wait=10,
        )
        if len(peaks) > 3:
            beat_times = librosa.frames_to_time(peaks, sr=sr, hop_length=hop_length)
            if len(beat_times) > 1:
                median_interval = np.median(np.diff(beat_times))
                tempo = 60.0 / median_interval if median_interval > 0 else 120.0

    return beat_times.astype(np.float64), tempo


def extract_onset_map(
    y: np.ndarray,
    sr: int = SR,
    hop_length: int = HOP_LENGTH,
) -> tuple[np.ndarray, np.ndarray]:
    """
    Extract onset times and strengths.

    Returns:
        onset_times:     (n_onsets,) seconds
        onset_strengths: (n_onsets,) normalized [0, 1]
    """
    import librosa

    onset_env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=hop_length)
    onset_frames = librosa.onset.onset_detect(
        y=y, sr=sr, hop_length=hop_length, onset_envelope=onset_env,
    )
    onset_times = librosa.frames_to_time(onset_frames, sr=sr, hop_length=hop_length)

    # Get strengths at onset positions
    strengths = onset_env[onset_frames] if len(onset_frames) > 0 else np.array([])
    peak = strengths.max() if len(strengths) > 0 and strengths.max() > 0 else 1.0
    strengths = strengths / peak

    return onset_times.astype(np.float64), strengths.astype(np.float32)


def extract_chroma(
    y: np.ndarray,
    sr: int = SR,
    hop_length: int = HOP_LENGTH,
    n_fft: int = N_FFT,
) -> tuple[np.ndarray, float]:
    """
    Extract chromagram (12 pitch classes over time).

    Returns:
        chroma:    (12, n_frames) normalized
        chroma_sr: frame rate in Hz
    """
    import librosa

    chroma = librosa.feature.chroma_stft(
        y=y, sr=sr, hop_length=hop_length, n_fft=n_fft,
    )
    chroma_sr = sr / hop_length
    return chroma.astype(np.float32), float(chroma_sr)


def estimate_key(chroma: np.ndarray) -> tuple[int, str, float]:
    """
    Estimate key and mode from chromagram using Krumhansl-Kessler profiles.

    Returns:
        key_idx:        0-11 (C=0, C#=1, ..., B=11)
        mode:           'major' or 'minor'
        key_confidence: 0-1 (how much better the best key is vs. average)
    """
    # Average chroma across time
    chroma_mean = chroma.mean(axis=1)  # (12,)
    if chroma_mean.max() < 1e-6:
        return 0, "major", 0.0

    chroma_mean = chroma_mean / (chroma_mean.max() + 1e-8)

    best_corr = -1.0
    best_key = 0
    best_mode = "major"
    all_corrs = []

    for key_idx in range(12):
        for template, mode in [(MAJOR_TEMPLATE, "major"), (MINOR_TEMPLATE, "minor")]:
            # Rotate template to key
            rotated = np.roll(template, key_idx)
            corr = float(np.corrcoef(chroma_mean, rotated)[0, 1])
            all_corrs.append(corr)
            if corr > best_corr:
                best_corr = corr
                best_key = key_idx
                best_mode = mode

    # Confidence: how much better than average
    avg_corr = np.mean(all_corrs)
    confidence = max(0.0, min(1.0, (best_corr - avg_corr) / (1.0 - avg_corr + 1e-8)))

    return best_key, best_mode, confidence


def extract_chroma_novelty(chroma: np.ndarray) -> np.ndarray:
    """
    Compute chroma novelty function (proxy for chord change rate).
    High values = rapid harmonic change; low = sustained harmony.

    Returns:
        novelty: (n_frames,) normalized [0, 1]
    """
    if chroma.shape[1] < 2:
        return np.zeros(chroma.shape[1], dtype=np.float32)

    # Cosine distance between consecutive chroma frames
    norms = np.linalg.norm(chroma, axis=0, keepdims=True) + 1e-8
    chroma_norm = chroma / norms
    similarity = np.sum(chroma_norm[:, :-1] * chroma_norm[:, 1:], axis=0)
    novelty = 1.0 - similarity

    # Pad first frame
    novelty = np.concatenate([[0.0], novelty])

    # Normalize
    peak = novelty.max()
    if peak > 0:
        novelty = novelty / peak

    return novelty.astype(np.float32)


# ── Main extraction ────────────────────────────────────────────────────

def extract_score_proxy(
    y: np.ndarray,
    sr: int = SR,
    y_percussive: np.ndarray | None = None,
) -> ScoreProxy:
    """
    Extract complete score proxy from audio.

    Args:
        y:             Full audio waveform
        sr:            Sample rate
        y_percussive:  Optional percussive component (better for beat tracking)

    Returns:
        ScoreProxy with all structural information
    """
    # Beat tracking (prefer percussive for cleaner beats)
    beat_input = y_percussive if y_percussive is not None else y
    beat_times, tempo = extract_beat_grid(beat_input, sr)

    # Onset map
    onset_times, onset_strengths = extract_onset_map(beat_input, sr)

    # Chroma + key (use full signal for harmonic content)
    chroma, chroma_sr = extract_chroma(y, sr)
    key_idx, mode, key_confidence = estimate_key(chroma)

    # Novelty
    novelty = extract_chroma_novelty(chroma)

    return ScoreProxy(
        beat_times=beat_times,
        tempo=tempo,
        onset_times=onset_times,
        onset_strengths=onset_strengths,
        chroma=chroma,
        chroma_sr=chroma_sr,
        key_idx=key_idx,
        mode=mode,
        key_confidence=key_confidence,
        novelty=novelty,
    )
