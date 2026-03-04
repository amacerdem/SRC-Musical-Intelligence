"""IDyOM corpora management — load and prepare melodic corpora for benchmarking."""
from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from Validation.config.paths import IDYOM_DIR
from Validation.infrastructure.downloader import clone_repo


# ── Corpus sources ──
CORPUS_URLS = {
    "essen": "https://github.com/ccarh/essen-folksong-collection",
}


def download_corpora(force: bool = False) -> Dict[str, Path]:
    """Download all IDyOM benchmark corpora.

    Returns:
        Dict mapping corpus name to local directory path.
    """
    paths = {}
    for name, url in CORPUS_URLS.items():
        dest = IDYOM_DIR / name
        paths[name] = clone_repo(url, dest, force=force)
    return paths


def load_kern_melodies(corpus_dir: Path, max_melodies: int = 100) -> List[Dict]:
    """Load melodies from **kern format files.

    Args:
        corpus_dir: Path to corpus directory containing .krn files.
        max_melodies: Maximum number of melodies to load.

    Returns:
        List of melody dicts with 'pitches' (MIDI), 'durations' (beats), 'name'.
    """
    krn_files = sorted(corpus_dir.rglob("*.krn"))[:max_melodies]
    melodies = []

    for path in krn_files:
        try:
            melody = _parse_kern_file(path)
            if melody is not None and len(melody["pitches"]) >= 10:
                melodies.append(melody)
        except Exception:
            continue

    return melodies


def load_midi_melodies(
    corpus_dir: Path,
    max_melodies: int = 100,
) -> List[Dict]:
    """Load melodies from MIDI files.

    Args:
        corpus_dir: Directory containing .mid/.midi files.
        max_melodies: Maximum number to load.

    Returns:
        List of melody dicts with 'pitches', 'onsets', 'durations', 'name'.
    """
    import pretty_midi

    midi_files = sorted(corpus_dir.rglob("*.mid"))[:max_melodies]
    melodies = []

    for path in midi_files:
        try:
            pm = pretty_midi.PrettyMIDI(str(path))
            if not pm.instruments:
                continue
            inst = pm.instruments[0]
            if len(inst.notes) < 10:
                continue

            pitches = [n.pitch for n in inst.notes]
            onsets = [n.start for n in inst.notes]
            durations = [n.end - n.start for n in inst.notes]

            melodies.append({
                "pitches": np.array(pitches),
                "onsets": np.array(onsets),
                "durations": np.array(durations),
                "name": path.stem,
            })
        except Exception:
            continue

    return melodies


def melodies_to_audio(
    melodies: List[Dict],
    output_dir: Path,
    sr: int = 44100,
) -> List[Tuple[Dict, Path]]:
    """Synthesize melodies to WAV files for MI processing.

    Args:
        melodies: List of melody dicts from load_* functions.
        output_dir: Directory for WAV output.
        sr: Sample rate.

    Returns:
        List of (melody_dict, wav_path) tuples.
    """
    import pretty_midi
    import soundfile as sf

    output_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for melody in melodies:
        wav_path = output_dir / f"{melody['name']}.wav"
        if wav_path.exists():
            results.append((melody, wav_path))
            continue

        pm = pretty_midi.PrettyMIDI()
        inst = pretty_midi.Instrument(program=0)  # piano

        pitches = melody["pitches"]
        if "onsets" in melody:
            onsets = melody["onsets"]
            durations = melody["durations"]
        else:
            # Generate onsets from durations (quarter note = 0.5s)
            onsets = np.cumsum(np.concatenate([[0], melody["durations"][:-1]])) * 0.5
            durations = melody["durations"] * 0.5

        for p, o, d in zip(pitches, onsets, durations):
            note = pretty_midi.Note(velocity=80, pitch=int(p), start=float(o), end=float(o + d))
            inst.notes.append(note)

        pm.instruments.append(inst)
        audio = pm.fluidsynth(fs=sr)
        if audio.ndim == 2:
            audio = audio.mean(axis=0)
        peak = np.abs(audio).max()
        if peak > 0:
            audio = audio / peak * 0.9

        sf.write(str(wav_path), audio, sr)
        results.append((melody, wav_path))

    return results


def _parse_kern_file(path: Path) -> Optional[Dict]:
    """Parse a simple **kern file and extract the melody.

    Only handles single-voice monophonic melodies.
    """
    pitches = []
    durations = []

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("!") or line.startswith("*") or line.startswith("="):
                continue
            if line == ".":
                continue

            tokens = line.split("\t")
            if not tokens:
                continue

            token = tokens[0]
            if "r" in token:  # rest
                continue

            midi = _kern_to_midi(token)
            dur = _kern_to_duration(token)
            if midi is not None and dur is not None:
                pitches.append(midi)
                durations.append(dur)

    if len(pitches) < 10:
        return None

    return {
        "pitches": np.array(pitches),
        "durations": np.array(durations),
        "name": path.stem,
    }


def _kern_to_midi(token: str) -> Optional[int]:
    """Convert kern pitch token to MIDI note number."""
    # Count pitch characters
    pitch_chars = ""
    for ch in token:
        if ch.isalpha() and ch.lower() in "abcdefg":
            pitch_chars += ch
        elif ch in "#-":
            pitch_chars += ch

    if not pitch_chars:
        return None

    base_char = pitch_chars[0]
    is_lower = base_char.islower()
    note_name = base_char.upper()

    note_map = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}
    if note_name not in note_map:
        return None

    midi = note_map[note_name]

    # Octave
    letter_count = sum(1 for c in pitch_chars if c.isalpha())
    if is_lower:
        midi += 60 + (letter_count - 1) * 12  # c=60, cc=72, etc.
    else:
        midi += 48 - (letter_count - 1) * 12  # C=48, CC=36, etc.

    # Accidentals
    midi += pitch_chars.count("#") - pitch_chars.count("-")

    return midi


def _kern_to_duration(token: str) -> Optional[float]:
    """Convert kern duration token to beats."""
    # Extract numeric prefix
    num_str = ""
    for ch in token:
        if ch.isdigit():
            num_str += ch
        elif num_str:
            break

    if not num_str:
        return 1.0

    denom = int(num_str)
    if denom == 0:
        return 4.0  # breve

    dur = 4.0 / denom

    # Dots
    dot_count = token.count(".")
    if dot_count > 0:
        dur *= 2.0 - (0.5 ** dot_count)

    return dur
