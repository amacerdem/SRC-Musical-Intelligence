#!/usr/bin/env python
"""Generate all F1 micro-belief test audio files as WAV.

Saves to Test-Audio/micro_beliefs/f1/{relay}/*.wav

Run::

    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/micro_beliefs/generate_f1_audio.py
"""
from __future__ import annotations

import pathlib
import sys

import numpy as np
import torch
from scipy.io import wavfile

# Ensure project root on path
_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))

from Tests.micro_beliefs.audio_stimuli import (
    A4, C4, Db4, D4, E4, Eb4, F4, Fsharp4, G4, Ab4, Bb4, B4, C5,
    ascending_scale, crossfade, descending_scale, dyad,
    harmonic_complex, inharmonic_complex, noise, repeated_note,
    rich_dyad, silence, sine_tone,
    SAMPLE_RATE,
)

OUT_DIR = _ROOT / "Test-Audio" / "micro_beliefs" / "f1"


def save(waveform: torch.Tensor, relay: str, name: str) -> pathlib.Path:
    """Save (1, N) waveform as 16-bit WAV."""
    path = OUT_DIR / relay / f"{name}.wav"
    path.parent.mkdir(parents=True, exist_ok=True)
    # Clamp to [-1, 1] and convert to int16
    w = waveform.clamp(-1.0, 1.0).squeeze(0).numpy()
    int16 = (w * 32767).astype(np.int16)
    wavfile.write(str(path), SAMPLE_RATE, int16)
    dur = len(w) / SAMPLE_RATE
    print(f"  {path.relative_to(_ROOT)}  ({dur:.2f}s)")
    return path


def generate_bch():
    """BCH relay — consonance hierarchy tests."""
    print("\n=== BCH (Brainstem Consonance Hierarchy) ===")

    # Rich dyad intervals (6 harmonics each)
    save(rich_dyad(C4, C4), "bch", "01_unison_rich")
    save(rich_dyad(C4, C5), "bch", "02_octave_rich")
    save(rich_dyad(C4, G4), "bch", "03_p5_rich")
    save(rich_dyad(C4, F4), "bch", "04_p4_rich")
    save(rich_dyad(C4, E4), "bch", "05_M3_rich")
    save(rich_dyad(C4, Eb4), "bch", "06_m3_rich")
    save(rich_dyad(C4, Ab4), "bch", "07_m6_rich")
    save(rich_dyad(C4, Fsharp4), "bch", "08_TT_rich")
    save(rich_dyad(C4, Db4), "bch", "09_m2_rich")

    # Pure sine dyads (for comparison)
    save(dyad(C4, C5), "bch", "10_octave_sine")
    save(dyad(C4, G4), "bch", "11_p5_sine")
    save(dyad(C4, Fsharp4), "bch", "12_TT_sine")
    save(dyad(C4, Db4), "bch", "13_m2_sine")

    # Tonal quality
    save(harmonic_complex(C4, 8), "bch", "14_harmonic_complex_C4")
    save(inharmonic_complex(C4, 8, 1.15), "bch", "15_inharmonic_complex_C4")
    save(noise(), "bch", "16_white_noise")
    save(silence(), "bch", "17_silence")

    # Transitions
    save(crossfade(noise(4.0), harmonic_complex(C4, 8, 4.0), 4.0),
         "bch", "18_noise_to_harmonic_4s")
    save(crossfade(harmonic_complex(C4, 8, 4.0), noise(4.0), 4.0),
         "bch", "19_harmonic_to_noise_4s")
    save(crossfade(rich_dyad(C4, Db4, duration_s=4.0),
                   rich_dyad(C4, C4, duration_s=4.0), 4.0),
         "bch", "20_m2_to_unison_4s")
    save(crossfade(rich_dyad(C4, C4, duration_s=4.0),
                   rich_dyad(C4, Db4, duration_s=4.0), 4.0),
         "bch", "21_unison_to_m2_4s")


def generate_pscl():
    """PSCL encoder — pitch salience tests."""
    print("\n=== PSCL (Pitch Salience in Cortex) ===")

    save(harmonic_complex(A4, 10), "pscl", "01_harmonic_A4_10h")
    save(harmonic_complex(A4, 3), "pscl", "02_harmonic_A4_3h")
    save(sine_tone(A4), "pscl", "03_sine_A4")
    save(noise(), "pscl", "04_white_noise")
    save(silence(), "pscl", "05_silence")

    # Transitions
    save(crossfade(harmonic_complex(A4, 10, 3.0), noise(3.0), 3.0),
         "pscl", "06_harmonic_to_noise_3s")
    save(crossfade(noise(3.0), harmonic_complex(A4, 10, 3.0), 3.0),
         "pscl", "07_noise_to_harmonic_3s")

    # Sustained
    save(sine_tone(A4, 3.0), "pscl", "08_sustained_sine_A4_3s")
    save(harmonic_complex(A4, 10, 3.0), "pscl", "09_sustained_harmonic_A4_3s")


def generate_pccr():
    """PCCR associator — pitch chroma identity tests."""
    print("\n=== PCCR (Pitch Chroma Class Recognition) ===")

    save(harmonic_complex(C4, 8), "pccr", "01_harmonic_C4")
    save(harmonic_complex(A4, 8), "pccr", "02_harmonic_A4")
    save(inharmonic_complex(C4, 8, 1.15), "pccr", "03_inharmonic_C4")
    save(noise(), "pccr", "04_white_noise")

    # Octave equivalence
    save(rich_dyad(C4, C5), "pccr", "05_octave_rich")
    save(rich_dyad(C4, G4), "pccr", "06_p5_rich")
    save(rich_dyad(C4, Fsharp4), "pccr", "07_TT_rich")
    save(rich_dyad(C4, Db4), "pccr", "08_m2_rich")


def generate_sded():
    """SDED relay — spectral complexity tests."""
    print("\n=== SDED (Spectral Dissonance Energy Detection) ===")

    save(sine_tone(A4), "sded", "01_sine_A4")
    save(harmonic_complex(C4, 8), "sded", "02_harmonic_C4")
    save(dyad(C4, Db4) + sine_tone(D4, 2.0, 0.3),
         "sded", "03_cluster_C4_Db4_D4")
    save(inharmonic_complex(C4, 6, 1.1) + inharmonic_complex(E4, 6, 1.1),
         "sded", "04_inharmonic_pair_C4_E4")
    save(noise(), "sded", "05_white_noise")
    save(silence(), "sded", "06_silence")


def generate_csg():
    """CSG relay — consonance-salience gradient tests."""
    print("\n=== CSG (Consonance-Salience Gradient) ===")

    save(rich_dyad(C4, Db4), "csg", "01_m2_rich")
    save(rich_dyad(C4, G4), "csg", "02_p5_rich")
    save(rich_dyad(C4, C4), "csg", "03_unison_rich")
    save(noise(), "csg", "04_white_noise")
    save(silence(), "csg", "05_silence")


def generate_mpg():
    """MPG relay — melodic contour tests."""
    print("\n=== MPG (Melodic Pitch Gradient) ===")

    save(ascending_scale(60, 12, 0.25), "mpg", "01_ascending_C4_12notes")
    save(descending_scale(72, 12, 0.25), "mpg", "02_descending_C5_12notes")
    save(repeated_note(60, 12, 0.25, 0.05), "mpg", "03_repeated_C4_12x")
    save(sine_tone(C4, 3.0), "mpg", "04_sustained_C4_3s")
    save(ascending_scale(60, 8, 0.25), "mpg", "05_ascending_C4_8notes")
    save(silence(3.0), "mpg", "06_silence_3s")


def generate_miaa():
    """MIAA relay — timbral character tests."""
    print("\n=== MIAA (Musical Imagery & Auditory Awareness) ===")

    save(harmonic_complex(C4, 8, 3.0), "miaa", "01_harmonic_C4_3s")
    save(inharmonic_complex(C4, 8, 1.15, 3.0), "miaa", "02_inharmonic_C4_3s")
    save(noise(3.0), "miaa", "03_white_noise_3s")
    save(silence(3.0), "miaa", "04_silence_3s")
    save(sine_tone(C4, 3.0), "miaa", "05_sine_C4_3s")

    # Timbre contrast sequence
    from Tests.micro_beliefs.audio_stimuli import multi_timbre_sequence
    save(multi_timbre_sequence(4.0), "miaa", "06_timbre_sequence_4s")


def generate_stai():
    """STAI encoder — aesthetic quality tests."""
    print("\n=== STAI (Spectral-Temporal Aesthetic Integration) ===")

    # Consonant / beautiful
    save(harmonic_complex(C4, 8) + dyad(C4, G4),
         "stai", "01_consonant_C4_P5")
    save(harmonic_complex(C4, 8, 3.0, 0.2) + harmonic_complex(G4, 6, 3.0, 0.15),
         "stai", "02_rich_consonant_C4_G4_3s")

    # Dissonant / ugly
    save(dyad(C4, Db4) + noise(2.0, 0.1),
         "stai", "03_dissonant_m2_noise")
    save(noise(3.0), "stai", "04_white_noise_3s")

    # Transitions
    save(crossfade(harmonic_complex(C4, 8, 3.0), dyad(C4, Db4, 3.0), 3.0),
         "stai", "05_harmonic_to_dissonant_3s")
    save(crossfade(noise(3.0), harmonic_complex(C4, 8, 3.0), 3.0),
         "stai", "06_noise_to_harmonic_3s")


def main():
    print(f"Generating F1 test audio → {OUT_DIR.relative_to(_ROOT)}/")
    generate_bch()
    generate_pscl()
    generate_pccr()
    generate_sded()
    generate_csg()
    generate_mpg()
    generate_miaa()
    generate_stai()

    # Count total files
    count = sum(1 for _ in OUT_DIR.rglob("*.wav"))
    print(f"\nDone — {count} WAV files generated.")


if __name__ == "__main__":
    main()
