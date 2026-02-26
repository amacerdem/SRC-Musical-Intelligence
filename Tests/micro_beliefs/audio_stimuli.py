"""Synthetic audio stimulus library for micro-belief tests.

Deterministic waveform generators that produce targeted audio stimuli
for isolating specific C³ beliefs.  Every function returns a ``(1, N)``
float32 tensor at 44 100 Hz.
"""
from __future__ import annotations

import math

import torch
from torch import Tensor

SAMPLE_RATE = 44_100

# ── Named frequencies (equal temperament, A4 = 440 Hz) ──────────────
C4 = 261.63
Db4 = 277.18
D4 = 293.66
Eb4 = 311.13
E4 = 329.63
F4 = 349.23
Fsharp4 = 369.99
G4 = 392.00
Ab4 = 415.30
A4 = 440.00
Bb4 = 466.16
B4 = 493.88
C5 = 523.25


def midi_to_hz(midi: int) -> float:
    """Convert MIDI note number to frequency in Hz."""
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


# ── Primitives ───────────────────────────────────────────────────────

def sine_tone(
    freq_hz: float,
    duration_s: float = 2.0,
    amp: float = 0.5,
) -> Tensor:
    """Pure sine tone.  Shape ``(1, N)``."""
    N = int(SAMPLE_RATE * duration_s)
    t = torch.linspace(0, duration_s, N, dtype=torch.float32)
    return (amp * torch.sin(2 * math.pi * freq_hz * t)).unsqueeze(0)


def dyad(
    f1_hz: float,
    f2_hz: float,
    duration_s: float = 2.0,
    amp: float = 0.35,
) -> Tensor:
    """Two simultaneous sine tones (musical interval)."""
    return sine_tone(f1_hz, duration_s, amp) + sine_tone(f2_hz, duration_s, amp)


def harmonic_complex(
    f0_hz: float,
    n_harmonics: int = 8,
    duration_s: float = 2.0,
    amp: float = 0.3,
) -> Tensor:
    """Harmonic complex tone — f0 + overtones with 1/n amplitude decay."""
    N = int(SAMPLE_RATE * duration_s)
    waveform = torch.zeros(1, N, dtype=torch.float32)
    for n in range(1, n_harmonics + 1):
        waveform = waveform + sine_tone(f0_hz * n, duration_s, amp / n)
    return waveform


def inharmonic_complex(
    f0_hz: float,
    n_partials: int = 8,
    stretch: float = 1.15,
    duration_s: float = 2.0,
    amp: float = 0.3,
) -> Tensor:
    """Inharmonic complex tone — partials at f0 * n^stretch."""
    N = int(SAMPLE_RATE * duration_s)
    waveform = torch.zeros(1, N, dtype=torch.float32)
    for n in range(1, n_partials + 1):
        freq = f0_hz * (n ** stretch)
        if freq < SAMPLE_RATE / 2:  # Nyquist guard
            waveform = waveform + sine_tone(freq, duration_s, amp / n)
    return waveform


def noise(duration_s: float = 2.0, amp: float = 0.3, seed: int = 999) -> Tensor:
    """Deterministic white noise.  Shape ``(1, N)``."""
    N = int(SAMPLE_RATE * duration_s)
    gen = torch.Generator().manual_seed(seed)
    return (amp * torch.randn(1, N, generator=gen))


def silence(duration_s: float = 2.0) -> Tensor:
    """Digital silence.  Shape ``(1, N)``."""
    N = int(SAMPLE_RATE * duration_s)
    return torch.zeros(1, N, dtype=torch.float32)


# ── Temporal combinators ─────────────────────────────────────────────

def crossfade(audio_a: Tensor, audio_b: Tensor, duration_s: float = 4.0) -> Tensor:
    """Linear crossfade from *audio_a* to *audio_b* over *duration_s*.

    Both inputs are truncated/padded to ``int(SR * duration_s)`` samples.
    """
    N = int(SAMPLE_RATE * duration_s)
    a = _pad_or_trim(audio_a, N)
    b = _pad_or_trim(audio_b, N)
    fade = torch.linspace(0.0, 1.0, N, dtype=torch.float32).unsqueeze(0)
    return (1.0 - fade) * a + fade * b


def concatenate(*segments: Tensor) -> Tensor:
    """Concatenate multiple audio tensors along the time axis."""
    return torch.cat(segments, dim=-1)


# ── Melodic generators ───────────────────────────────────────────────

def ascending_scale(
    start_midi: int = 60,
    n_notes: int = 8,
    note_dur_s: float = 0.25,
    amp: float = 0.4,
) -> Tensor:
    """Ascending chromatic scale from *start_midi*."""
    segments = []
    for i in range(n_notes):
        freq = midi_to_hz(start_midi + i)
        segments.append(sine_tone(freq, note_dur_s, amp))
    return torch.cat(segments, dim=-1)


def descending_scale(
    start_midi: int = 72,
    n_notes: int = 8,
    note_dur_s: float = 0.25,
    amp: float = 0.4,
) -> Tensor:
    """Descending chromatic scale from *start_midi*."""
    segments = []
    for i in range(n_notes):
        freq = midi_to_hz(start_midi - i)
        segments.append(sine_tone(freq, note_dur_s, amp))
    return torch.cat(segments, dim=-1)


def repeated_note(
    midi: int = 60,
    n_repeats: int = 8,
    note_dur_s: float = 0.25,
    gap_dur_s: float = 0.05,
    amp: float = 0.4,
) -> Tensor:
    """Repeated single note with short gaps."""
    freq = midi_to_hz(midi)
    segments = []
    for _ in range(n_repeats):
        segments.append(sine_tone(freq, note_dur_s, amp))
        if gap_dur_s > 0:
            segments.append(silence(gap_dur_s))
    return torch.cat(segments, dim=-1)


def rich_dyad(
    f1_hz: float,
    f2_hz: float,
    n_harmonics: int = 6,
    duration_s: float = 2.0,
    amp: float = 0.2,
) -> Tensor:
    """Two harmonic complex tones sounding together (musical interval).

    Unlike ``dyad()`` which uses pure sines, this produces realistic
    interval stimuli with multiple overtones — critical for Sethares /
    Plomp-Levelt psychoacoustic consonance models.
    """
    return (
        harmonic_complex(f1_hz, n_harmonics, duration_s, amp)
        + harmonic_complex(f2_hz, n_harmonics, duration_s, amp)
    )


def octave_pair(
    f0_hz: float = 261.63,
    duration_s: float = 2.0,
    amp: float = 0.35,
) -> Tensor:
    """Two tones separated by an octave (f0 + 2*f0)."""
    return dyad(f0_hz, f0_hz * 2.0, duration_s, amp)


def multi_timbre_sequence(duration_s: float = 4.0) -> Tensor:
    """Sequence: pure sine → harmonic complex → inharmonic, equal segments."""
    seg = duration_s / 3.0
    return torch.cat([
        sine_tone(C4, seg, 0.4),
        harmonic_complex(C4, 8, seg, 0.3),
        inharmonic_complex(C4, 8, 1.15, seg, 0.3),
    ], dim=-1)


# ── Internal helpers ─────────────────────────────────────────────────

def _pad_or_trim(audio: Tensor, target_n: int) -> Tensor:
    """Pad with zeros or trim to *target_n* samples."""
    n = audio.shape[-1]
    if n >= target_n:
        return audio[:, :target_n]
    pad = torch.zeros(1, target_n - n, dtype=audio.dtype)
    return torch.cat([audio, pad], dim=-1)
