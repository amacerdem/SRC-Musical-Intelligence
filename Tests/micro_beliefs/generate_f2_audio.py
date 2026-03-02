#!/usr/bin/env python
"""Generate F2 (Prediction) micro-belief test audio via MIDI + FluidSynth.

Every stimulus is fully deterministic — we know exactly which notes,
intervals, velocity and instrument program were used, giving us
ground truth for every F2 belief (15 beliefs across 3 mechanisms:
HTP, SPH, ICEM).

Saves to Test-Audio/micro_beliefs/f2/{mechanism}/*.wav + *.mid

Total: 54 stimuli across 5 groups:
  htp/       (14 stimuli) — Hierarchical Temporal Prediction
  sph/       (12 stimuli) — Spatiotemporal Prediction Hierarchy
  icem/      (15 stimuli) — Information Content & Emotion Model
  cross/     (8+ stimuli) — Cross-Mechanism Integration
  boundary/  (5 stimuli)  — Boundary Conditions

Run::
    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/micro_beliefs/generate_f2_audio.py
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Dict, List, Optional

import numpy as np
import pretty_midi
import torch
from scipy.io import wavfile

# ── Project root ─────────────────────────────────────────────────────
_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ROOT))

from Tests.micro_beliefs.real_audio_stimuli import (
    SAMPLE_RATE, _render,
    PIANO, ORGAN, VIOLIN, STRINGS, TRUMPET, FLUTE, CELLO,
    major_triad, minor_triad, diminished_triad, dominant_seventh,
    chromatic_cluster, diatonic_scale, chromatic_scale,
    C2, C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5, A5, B5, C6,
)

OUT_DIR = _ROOT / "Test-Audio" / "micro_beliefs" / "f2"
ALL_METADATA: Dict[str, dict] = {}
_count = 0


# =====================================================================
# Save helper
# =====================================================================

def save(
    pm: pretty_midi.PrettyMIDI,
    group: str,
    name: str,
    meta: dict,
    gain: float = 1.0,
) -> pathlib.Path:
    """Save PrettyMIDI as .mid + rendered .wav, collect metadata."""
    global _count
    _count += 1

    d = OUT_DIR / group
    d.mkdir(parents=True, exist_ok=True)

    # Save MIDI
    mid_path = d / f"{name}.mid"
    pm.write(str(mid_path))

    # Render and save WAV
    has_notes = any(len(inst.notes) > 0 for inst in pm.instruments)
    if has_notes:
        waveform = _render(pm)
    else:
        # Empty MIDI → 5s of silence
        n_samples = 5 * SAMPLE_RATE
        waveform = torch.zeros(1, n_samples)
    wav_path = d / f"{name}.wav"
    w = (waveform * gain).clamp(-1.0, 1.0).squeeze(0).numpy()
    int16 = (w * 32767).astype(np.int16)
    wavfile.write(str(wav_path), SAMPLE_RATE, int16)

    dur = len(w) / SAMPLE_RATE
    meta["duration_s"] = round(dur, 2)
    meta["filename"] = f"{group}/{name}"
    ALL_METADATA[f"{group}/{name}"] = meta
    print(f"  [{_count:02d}] {wav_path.relative_to(_ROOT)}  ({dur:.1f}s)")
    return wav_path


# =====================================================================
# PrettyMIDI builder helpers
# =====================================================================

def _pm_melody(
    notes: List[int],
    durs: List[float],
    program: int = PIANO,
    velocity: int = 80,
    gap: float = 0.02,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI from monophonic note list."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for p, d in zip(notes, durs):
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=p, start=t, end=t + d - gap,
        ))
        t += d
    pm.instruments.append(inst)
    return pm


def _pm_progression(
    chords: List[List[int]],
    durs: List[float],
    program: int = PIANO,
    velocity: int = 70,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI from chord list."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for chord, d in zip(chords, durs):
        for p in chord:
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=p, start=t, end=t + d,
            ))
        t += d
    pm.instruments.append(inst)
    return pm


def _pm_isochronous(
    pitch: int, bpm: float, n_beats: int,
    program: int = PIANO, velocity: int = 80,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI for isochronous (equally spaced) notes."""
    ioi = 60.0 / bpm
    dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_beats):
        t = i * ioi
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch, start=t, end=t + dur,
        ))
    pm.instruments.append(inst)
    return pm


def _pm_note(
    pitch: int, duration_s: float,
    program: int = PIANO, velocity: int = 80,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI for single sustained note."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    inst.notes.append(pretty_midi.Note(
        velocity=velocity, pitch=pitch, start=0.0, end=duration_s,
    ))
    pm.instruments.append(inst)
    return pm


def _pm_chord(
    notes: List[int], duration_s: float,
    program: int = PIANO, velocity: int = 80,
) -> pretty_midi.PrettyMIDI:
    """Build PrettyMIDI for sustained chord."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for p in notes:
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=p, start=0.0, end=duration_s,
        ))
    pm.instruments.append(inst)
    return pm


def _pm_melody_with_chords(
    mel_notes, mel_durs, chd_notes, chd_durs,
    mel_prog=FLUTE, chd_prog=PIANO,
    mel_vel=90, chd_vel=60,
) -> pretty_midi.PrettyMIDI:
    """Melody over chord accompaniment."""
    pm = pretty_midi.PrettyMIDI()
    # Melody
    mi = pretty_midi.Instrument(program=mel_prog)
    t = 0.0
    for p, d in zip(mel_notes, mel_durs):
        mi.notes.append(pretty_midi.Note(
            velocity=mel_vel, pitch=p, start=t, end=t + d - 0.02,
        ))
        t += d
    pm.instruments.append(mi)
    # Chords
    ci = pretty_midi.Instrument(program=chd_prog)
    t = 0.0
    for chord, d in zip(chd_notes, chd_durs):
        for p in chord:
            ci.notes.append(pretty_midi.Note(
                velocity=chd_vel, pitch=p, start=t, end=t + d,
            ))
        t += d
    pm.instruments.append(ci)
    return pm


# =====================================================================
# Chord constructors
# =====================================================================

def _maj7(root: int) -> List[int]:
    return [root, root + 4, root + 7, root + 11]


def _min7(root: int) -> List[int]:
    return [root, root + 3, root + 7, root + 10]


# Common chords
Cmaj = major_triad(C4)
Cmaj_low = major_triad(C3)
Fmaj = major_triad(F3)
Gmaj = major_triad(G3)
Am = minor_triad(A3)
Dm = minor_triad(D3)
Em = minor_triad(E3)
G7 = dominant_seventh(G3)
Abmaj = major_triad(Ab4 - 12)  # Ab3
Cm = minor_triad(C4)
Fm = minor_triad(F3)
Gbmaj = major_triad(Gb4 - 12)  # Gb3
Dbmaj = major_triad(Db4 - 12)  # Db3
Ebmaj = major_triad(Eb4 - 12)  # Eb3
Amaj = major_triad(A3)
Bbmaj = major_triad(Bb4 - 12)  # Bb3
Bmaj = major_triad(B3)
Dmaj = major_triad(D3)
Fsharp_maj = major_triad(Gb4 - 12)  # F#3 = Gb3

Dm7 = _min7(D3)
G7_ext = dominant_seventh(G3)
Cmaj7 = _maj7(C3)
Am7 = _min7(A3)  # A3 — same register as Dm7/Cmaj7


# =====================================================================
# Category 1: Temporal Hierarchy (HTP, 8 stimuli)
# =====================================================================

def generate_htp_hierarchy():
    """Category 1 — Temporal hierarchy structure (8 stimuli)."""
    print("\n=== CATEGORY 1: TEMPORAL HIERARCHY (HTP) ===")
    g = "htp"

    # 1.1  Rich hierarchy: I-IV-V-I cadence with flute melody
    mel = [C5, D5, E5, F5, G5, A5, B5, C6]
    mel_d = [1.0] * 8
    chds = [Cmaj, Cmaj, Fmaj, Fmaj, Gmaj, Gmaj, Cmaj, Cmaj]
    chd_d = [1.0] * 8
    pm = _pm_melody_with_chords(mel, mel_d, chds, chd_d)
    save(pm, g, "01_rich_hierarchy", {
        "description": "I-IV-V-I cadence + ascending flute melody. Full 3-level hierarchy.",
        "tests": ["prediction_hierarchy", "hierarchy_coherence", "abstract_future"],
        "expected": {"prediction_hierarchy": "HIGH", "hierarchy_coherence": "HIGH"},
        "science": "de Vries & Wurm 2023: all 3 levels engaged",
    })

    # 1.2  Flat: repeated C4 at 120 BPM
    pm = _pm_isochronous(C4, 120, 16, PIANO, 80)
    save(pm, g, "02_flat_repeat", {
        "description": "Repeated C4 @120BPM, piano. No harmonic hierarchy.",
        "tests": ["prediction_hierarchy"],
        "expected": {"prediction_hierarchy": "LOW"},
        "science": "Single pitch, no multi-level structure",
    })

    # 1.3  High-level only: slow organ whole notes I-IV-V-I
    pm = _pm_progression(
        [Cmaj, Fmaj, Gmaj, Cmaj], [2.0] * 4, ORGAN, 70,
    )
    save(pm, g, "03_high_level_only", {
        "description": "Slow I-IV-V-I on organ (whole notes). High tonal_stability, no onsets.",
        "tests": ["hierarchy_coherence", "abstract_future"],
        "expected": {"hierarchy_coherence": "HIGH (E0>>E2 -> E3 high)", "abstract_future": "HIGH"},
        "science": "de Vries & Wurm 2023: abstract prediction dominates without sensory events",
    })

    # 1.4  Low-level only: fast staccato C4 at 480 BPM
    pm = _pm_isochronous(C4, 480, 48, PIANO, 90)
    save(pm, g, "04_low_level_only", {
        "description": "Fast staccato C4 @480BPM. High onset periodicity, no harmonic change.",
        "tests": ["hierarchy_coherence"],
        "expected": {"hierarchy_coherence": "LOW (E2>>E0 -> E3 low)"},
        "science": "Sensory-level only, no abstract structure",
    })

    # 1.5  Mid-level: wide-range trumpet melody (maximise sharpness velocity)
    # Spans C4-C6 (2 octaves) with arpeggiated leaps — large brightness changes
    # per note produce high sharpness_velocity at 125ms.  Contrast with 02_flat
    # (constant C4 = zero sharpness velocity).
    mel = [C4, G4, E5, C6, G5, E4, C4, G4, E5, C6, G5, E4, C5, G5, C6, C5]
    pm = _pm_melody(mel, [0.375] * 16, TRUMPET, 100)
    save(pm, g, "05_mid_level_melody", {
        "description": "Trumpet arpeggios C4-C6 (2 octaves). Large sharpness velocity from register changes.",
        "tests": ["midlevel_future"],
        "expected": {"midlevel_future": "HIGH"},
        "science": "de Vries & Wurm 2023: mid-level ~200ms in belt cortex. "
                   "Wide pitch range produces large sharpness_velocity (spectral centroid change rate).",
    })

    # 1.6  Random pitch + timing (anti-hierarchical)
    rng = np.random.RandomState(42)
    pitches = rng.randint(48, 84, size=20).tolist()
    iois = rng.uniform(0.2, 0.8, size=20).tolist()
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for p, ioi in zip(pitches, iois):
        inst.notes.append(pretty_midi.Note(
            velocity=80, pitch=int(p), start=t, end=t + ioi * 0.8,
        ))
        t += ioi
    pm.instruments.append(inst)
    save(pm, g, "06_random_pitch_timing", {
        "description": "Random pitches [48-84], random IOI [0.2-0.8s], seed=42.",
        "tests": ["prediction_hierarchy", "prediction_accuracy"],
        "expected": {"prediction_hierarchy": "LOW", "prediction_accuracy": "LOW"},
        "science": "No structure at any level -> all predictions fail",
    })

    # 1.7  Hierarchy build: random -> repeat -> melody+chord -> cadence
    pm = pretty_midi.PrettyMIDI()
    inst_p = pretty_midi.Instrument(program=PIANO)
    inst_f = pretty_midi.Instrument(program=FLUTE)
    # Section A (0-2s): random notes
    rng = np.random.RandomState(42)
    t = 0.0
    for _ in range(8):
        p = int(rng.randint(60, 73))
        inst_p.notes.append(pretty_midi.Note(80, p, t, t + 0.2))
        t += 0.25
    # Section B (2-4s): repeated C4
    for i in range(8):
        t = 2.0 + i * 0.25
        inst_p.notes.append(pretty_midi.Note(80, C4, t, t + 0.2))
    # Section C (4-6s): C4 melody over Cmaj
    mel_c = [C4, E4, G4, C5]
    for i, p in enumerate(mel_c):
        t = 4.0 + i * 0.5
        inst_f.notes.append(pretty_midi.Note(90, p, t, t + 0.45))
    for p in Cmaj:
        inst_p.notes.append(pretty_midi.Note(60, p, 4.0, 6.0))
    # Section D (6-8s): full I-IV-V-I
    for ci, (chord, start) in enumerate([(Cmaj, 6.0), (Fmaj, 6.5), (G7, 7.0), (Cmaj, 7.5)]):
        for p in chord:
            inst_p.notes.append(pretty_midi.Note(70, p, start, start + 0.5))
    pm.instruments.extend([inst_p, inst_f])
    save(pm, g, "07_hierarchy_build", {
        "description": "4 sections: random(2s)->repeat(2s)->melody+chord(2s)->cadence(2s).",
        "tests": ["prediction_hierarchy"],
        "expected": {"prediction_hierarchy": "PROGRESSIVE INCREASE across sections"},
        "science": "Hierarchy emerges as more levels become structured",
    })

    # 1.8  Hierarchy collapse: I-IV-V-I -> chromatic noise
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # First 3s: clean cadence
    for ci, (chord, start) in enumerate([
        (Cmaj, 0.0), (Fmaj, 0.75), (G7, 1.5), (Cmaj, 2.25),
    ]):
        for p in chord:
            inst.notes.append(pretty_midi.Note(70, p, start, start + 0.75))
    # Last 3s: chromatic noise cluster with random onsets
    rng = np.random.RandomState(99)
    for _ in range(30):
        p = int(rng.randint(48, 84))
        s = 3.0 + float(rng.uniform(0, 2.5))
        e = s + float(rng.uniform(0.05, 0.3))
        inst.notes.append(pretty_midi.Note(90, p, s, min(e, 6.0)))
    pm.instruments.append(inst)
    save(pm, g, "08_hierarchy_collapse", {
        "description": "I-IV-V-I (3s) then chromatic noise cluster (3s).",
        "tests": ["prediction_hierarchy", "hierarchy_coherence"],
        "expected": {"prediction_hierarchy": "DECREASES", "hierarchy_coherence": "DECREASES"},
        "science": "Structure dissolves -> all prediction levels fail",
    })


# =====================================================================
# Category 2: Prediction Accuracy (HTP, 6 stimuli)
# =====================================================================

def generate_htp_accuracy():
    """Category 2 — Prediction accuracy (6 stimuli)."""
    print("\n=== CATEGORY 2: PREDICTION ACCURACY (HTP) ===")
    g = "htp"

    # 2.1  Perfect isochronous
    pm = _pm_isochronous(C4, 120, 20, PIANO, 80)
    save(pm, g, "09_isochronous_C4", {
        "description": "C4 @120BPM, perfect grid, 20 beats. Maximum predictability.",
        "tests": ["prediction_accuracy"],
        "expected": {"prediction_accuracy": "VERY HIGH"},
        "science": "Forseth 2020: timing prediction in HG converges quickly",
    })

    # 2.2  Repeated scale pattern
    scale = diatonic_scale(C4, 8)
    notes = scale * 3
    pm = _pm_melody(notes, [0.4] * len(notes), PIANO, 80)
    save(pm, g, "10_repeated_scale", {
        "description": "C major ascending scale x3. Pitch contour repeats.",
        "tests": ["prediction_accuracy"],
        "expected": {"prediction_accuracy": "HIGH, increasing across repetitions"},
        "science": "Repetition builds predictive model; 2nd/3rd exposure more accurate",
    })

    # 2.3  Cadence repeated
    chords = [Cmaj, Fmaj, G7, Cmaj] * 3
    pm = _pm_progression(chords, [1.0] * 12, PIANO, 70)
    save(pm, g, "11_cadence_repeated", {
        "description": "I-IV-V7-I cadence x3. Harmonic pattern repeats.",
        "tests": ["prediction_accuracy"],
        "expected": {"prediction_accuracy": "HIGH"},
        "science": "Cadential pattern is maximally predictable after first exposure",
    })

    # 2.4  Random melody (C-major pitches, irregular timing)
    rng = np.random.RandomState(43)
    c_major_pool = diatonic_scale(C4, 15)
    pitches = [c_major_pool[i] for i in rng.randint(0, len(c_major_pool), 25)]
    durations = rng.uniform(0.2, 0.6, size=25).tolist()
    pm = _pm_melody(pitches, durations, PIANO, 80)
    save(pm, g, "12_random_melody", {
        "description": "Random C-major pitches, irregular timing, seed=43.",
        "tests": ["prediction_accuracy"],
        "expected": {"prediction_accuracy": "LOW"},
        "science": "Random sequence defeats both timing and content prediction",
    })

    # 2.5  Deceptive cadence: I-IV-V-I x2 then I-IV-V-vi
    chords = (
        [Cmaj, Fmaj, G7, Cmaj]  # bar 1-4: normal
        + [Cmaj, Fmaj, G7, Cmaj]  # bar 5-8: normal
        + [Cmaj, Fmaj, G7, Am]    # bar 9-12: deceptive (vi instead of I)
    )
    pm = _pm_progression(chords, [1.0] * 12, PIANO, 70)
    save(pm, g, "13_deceptive_cadence", {
        "description": "I-IV-V-I x2 then I-IV-V-vi (deceptive). Expectation violated at bar 12.",
        "tests": ["prediction_accuracy"],
        "expected": {"prediction_accuracy": "HIGH then DROP at bar 12 (Am instead of Cmaj)"},
        "science": "de Vries & Wurm 2023: violated expectation generates PE",
    })

    # 2.6  Tempo deviation: isochronous with late beat 9
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    ioi = 0.5  # 120 BPM
    dur = ioi * 0.85
    # Beats 1-8: perfect grid
    for i in range(8):
        t = i * ioi
        inst.notes.append(pretty_midi.Note(80, C4, t, t + dur))
    # Beat 9: delayed 150ms
    t9 = 8 * ioi + 0.15
    inst.notes.append(pretty_midi.Note(80, C4, t9, t9 + dur))
    # Beats 10-16: resume from beat 9 position
    for i in range(1, 8):
        t = t9 + i * ioi
        inst.notes.append(pretty_midi.Note(80, C4, t, t + dur))
    pm.instruments.append(inst)
    save(pm, g, "14_tempo_deviation", {
        "description": "Isochronous 8 beats, beat 9 delayed 150ms, resume. Timing violation.",
        "tests": ["prediction_accuracy"],
        "expected": {"prediction_accuracy": "DIP at beat 9"},
        "science": "Forseth 2020: low-freq phase in HG tracks timing; deviation = PE",
    })


# =====================================================================
# Category 3: Sequence Memory (SPH, 7 stimuli)
# =====================================================================

def generate_sph_memory():
    """Category 3 — Sequence memory and pattern matching (7 stimuli)."""
    print("\n=== CATEGORY 3: SEQUENCE MEMORY (SPH) ===")
    g = "sph"

    # 3.1  Memorised 4-note motif x8
    motif = [C4, E4, G4, C5]
    notes = motif * 8
    pm = _pm_melody(notes, [0.375] * len(notes), PIANO, 80)
    save(pm, g, "01_memorised_4note_x8", {
        "description": "C4-E4-G4-C5 motif repeated 8 times. Pure repetition.",
        "tests": ["sequence_match", "oscillatory_signature"],
        "expected": {"sequence_match": "HIGH (increasing)", "oscillatory_signature": "HIGH (gamma-dominant)"},
        "science": "Bonetti 2024: memorised -> gamma > alpha-beta, feedforward Heschl->Hippo->Cing",
    })

    # 3.2  Varied 4-note groups x8 (all from C major, never repeating)
    groups = [
        [C4, D4, F4, A4],
        [E4, G4, B4, D5],
        [F4, A4, C5, E5],
        [G4, B4, D5, F5],
        [A4, C5, E5, G5],
        [D4, F4, B4, E5],
        [E4, A4, D5, G5],
        [G4, C5, F5, B5],
    ]
    notes = [n for grp in groups for n in grp]
    pm = _pm_melody(notes, [0.375] * len(notes), PIANO, 80)
    save(pm, g, "02_varied_4note_x8", {
        "description": "8 different 4-note groups from C major. No repetition.",
        "tests": ["sequence_match", "error_propagation", "oscillatory_signature"],
        "expected": {
            "sequence_match": "LOW",
            "error_propagation": "HIGH",
            "oscillatory_signature": "LOW (alpha-beta-dominant)",
        },
        "science": "Bonetti 2024: novel -> alpha-beta > gamma, feedback processing",
    })

    # 3.3  Memorised 8-note scale x4
    scale = diatonic_scale(C4, 8)
    notes = scale * 4
    pm = _pm_melody(notes, [0.375] * len(notes), PIANO, 80)
    save(pm, g, "03_memorised_8note_x4", {
        "description": "C major scale (8 notes) repeated 4 times.",
        "tests": ["sequence_match"],
        "expected": {"sequence_match": "HIGH (slower build than 4-note motif)"},
        "science": "Longer patterns take more exposures to consolidate in hippocampus",
    })

    # 3.4  Memorised then deviant: motif x6 + deviant + normal
    motif = [C4, E4, G4, C5]
    deviant_motif = [C4, E4, G4, Db4 + 12]  # Db5 = 73 instead of C5 = 72
    notes = motif * 6 + deviant_motif + motif
    pm = _pm_melody(notes, [0.375] * len(notes), PIANO, 80)
    save(pm, g, "04_memorised_then_deviant", {
        "description": "C4-E4-G4-C5 x6, then Db5 replaces C5 (semitone deviation), then normal.",
        "tests": ["sequence_match", "error_propagation"],
        "expected": {
            "sequence_match": "HIGH then DIP at deviant",
            "error_propagation": "SPIKE at deviant tone (position 25)",
        },
        "science": "Carbajal & Malmierca 2018: SSA/MMN at deviant propagates IC->MGB->AC",
    })

    # 3.5  Memorised chord progression x4
    chords = [Cmaj, Am, Fmaj, Gmaj] * 4
    pm = _pm_progression(chords, [0.75] * len(chords), PIANO, 70)
    save(pm, g, "05_memorised_chords_x4", {
        "description": "I-vi-IV-V chord progression repeated 4 times.",
        "tests": ["sequence_match"],
        "expected": {"sequence_match": "HIGH (harmonic pattern memory)"},
        "science": "Bonetti 2024: recognition extends to harmonic sequences, not just melodic",
    })

    # 3.6  Novel chords (16 different, distant keys)
    novel = [
        Cmaj, Ebmaj, Fsharp_maj, Amaj,
        Dbmaj, major_triad(E3), Gmaj, Bbmaj,
        Dmaj, Fmaj, Abmaj, Bmaj,
        minor_triad(Eb4 - 12), minor_triad(Gb4 - 12),
        minor_triad(A3), Cm,
    ]
    pm = _pm_progression(novel, [0.75] * 16, PIANO, 70)
    save(pm, g, "06_novel_chords", {
        "description": "16 different chords spanning distant keys. No repetition.",
        "tests": ["sequence_match", "error_propagation"],
        "expected": {"sequence_match": "LOW", "error_propagation": "HIGH"},
        "science": "No repeated pattern -> no memory match -> persistent PE",
    })

    # 3.7  Gradual learning: intro -> repeat -> vary (continuous, no gaps)
    motif = [C4, Eb4, G4, Bb4]
    varied = [C4, Eb4, Ab4, Bb4]  # one note changed (G4 -> Ab4)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    note_dur = 0.35
    ioi = 0.375
    # Section A (0-6s): introduce motif x4 — first exposure
    for rep in range(4):
        for p in motif:
            inst.notes.append(pretty_midi.Note(80, p, t, t + note_dur))
            t += ioi
    # Section B (6-12s): repeat same motif x4 — consolidation (continuous)
    for rep in range(4):
        for p in motif:
            inst.notes.append(pretty_midi.Note(80, p, t, t + note_dur))
            t += ioi
    # Section C (12-18s): varied motif x4 — partial match
    for rep in range(4):
        for p in varied:
            inst.notes.append(pretty_midi.Note(80, p, t, t + note_dur))
            t += ioi
    pm.instruments.append(inst)
    save(pm, g, "07_gradual_learning", {
        "description": "Motif x4 (intro) -> same x4 (consolidation) -> varied x4 (partial match). "
                       "Continuous stream, no gaps, so H3 memory accumulates across sections.",
        "tests": ["sequence_match"],
        "expected": {"sequence_match": "LOW(A) -> HIGH(B) -> MODERATE(C)"},
        "science": "Bonetti 2024: memory match builds with repetition, partial match with variation",
    })


# =====================================================================
# Category 4: Sequence Completion (SPH, 5 stimuli)
# =====================================================================

def generate_sph_completion():
    """Category 4 — Sequence completion / phrase boundaries (5 stimuli)."""
    print("\n=== CATEGORY 4: SEQUENCE COMPLETION (SPH) ===")
    g = "sph"

    # 4.1  Authentic cadence I-IV-V7-I
    pm = _pm_progression([Cmaj, Fmaj, G7, Cmaj], [2.0] * 4, PIANO, 70)
    save(pm, g, "08_authentic_cadence", {
        "description": "I-IV-V7-I in C major, 2s per chord. Strong resolution.",
        "tests": ["sequence_completion"],
        "expected": {"sequence_completion": "HIGH at final I (last 2s)"},
        "science": "Bonetti 2024: cingulate assumes top hierarchy position at final tone; Rimmele 2021: delta for boundaries",
    })

    # 4.2  Half cadence (ends on V, no resolution to I)
    pm = _pm_progression(
        [Cmaj, Fmaj, Gmaj, Gmaj], [2.0] * 4, PIANO, 70,
    )
    save(pm, g, "09_half_cadence", {
        "description": "I-IV-V-V, ending on dominant. Half cadence — no resolution to tonic.",
        "tests": ["sequence_completion"],
        "expected": {"sequence_completion": "LOW (V without I resolution)"},
        "science": "Half cadence ends on V; no tonic arrival = no phrase boundary",
    })

    # 4.3  Clear phrase boundary with melodic arc
    mel = [C4, D4, E4, F4, G4, A4, G4, F4, E4, D4, C4, C4]
    durs = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.75, 1.25]
    pm = _pm_melody(mel, durs, PIANO, 80)
    save(pm, g, "10_phrase_boundary", {
        "description": "Melodic arc: ascend C4-A4, descend to C4, long tonic. Clear boundary.",
        "tests": ["sequence_completion"],
        "expected": {"sequence_completion": "HIGH at final C4 (last 2s)"},
        "science": "Rimmele 2021: delta oscillations encode phrase-level boundaries",
    })

    # 4.4  Mid-phrase fragment (ascending, no resolution)
    mel = [C4, D4, E4, F4, G4]
    pm = _pm_melody(mel, [1.0] * 5, PIANO, 80)
    save(pm, g, "11_mid_phrase", {
        "description": "Ascending scale fragment C4-G4, stops. No descent, no tonic.",
        "tests": ["sequence_completion"],
        "expected": {"sequence_completion": "LOW"},
        "science": "No tonic arrival, no melodic closure",
    })

    # 4.5  Deceptive cadence (V7 -> vi)
    pm = _pm_progression([Cmaj, Fmaj, G7, Am], [2.0] * 4, PIANO, 70)
    save(pm, g, "12_deceptive_cadence", {
        "description": "I-IV-V7-vi. Cadential approach but deceptive resolution.",
        "tests": ["sequence_completion"],
        "expected": {"sequence_completion": "MODERATE (approach but no tonic)"},
        "science": "Deceptive cadence approaches completion but diverts; partial boundary",
    })


# =====================================================================
# Category 5: Information Content (ICEM, 8 stimuli)
# =====================================================================

def generate_icem_ic():
    """Category 5 — Information content (8 stimuli)."""
    print("\n=== CATEGORY 5: INFORMATION CONTENT (ICEM) ===")
    g = "icem"

    # 5.1  Diatonic stepwise (low IC)
    scale_up = diatonic_scale(C4, 8)
    scale_down = list(reversed(diatonic_scale(C4, 7)))[1:]  # without repeating top note
    notes = scale_up + scale_down
    pm = _pm_melody(notes, [0.5] * len(notes), PIANO, 80)
    save(pm, g, "01_diatonic_steps", {
        "description": "C major scale ascending then descending. Every note maximally expected.",
        "tests": ["information_content", "valence_inversion"],
        "expected": {"information_content": "LOW", "valence_inversion": "HIGH (low IC -> high valence)"},
        "science": "Egermann 2013: IC = -log2(P), diatonic steps have highest P",
    })

    # 5.2  Chromatic leaps (high IC)
    # Alternating low-high register for MAXIMUM spectral contrast.
    # Every interval > 12 semitones (octave+), producing large spectral_flux.
    # Matched: same IOI (0.5s), velocity (80), instrument (piano), note count (14)
    # as diatonic_steps — the ONLY difference is pitch interval structure.
    leaps = [48, 84, 50, 82, 52, 80, 54, 78, 56, 76, 58, 74, 60, 72]
    pm = _pm_melody(leaps, [0.5] * 14, PIANO, 80)
    save(pm, g, "02_chromatic_leaps", {
        "description": "Alternating low/high register (C3-C6), every interval >12 semitones. "
                       "Same timing/velocity/instrument as diatonic_steps; only intervals differ.",
        "tests": ["information_content", "arousal_scaling"],
        "expected": {"information_content": "HIGH", "arousal_scaling": "HIGH"},
        "science": "Egermann 2013: high IC -> high arousal (p<0.001, N=50). "
                   "Large intervals = high P(unexpected|context) = high IC.",
    })

    # 5.3  Repeated tonic (minimal IC)
    pm = _pm_isochronous(C4, 120, 20, PIANO, 80)
    save(pm, g, "03_repeated_tonic", {
        "description": "C4 repeated 20 times at 120 BPM. IC approaches zero after onset.",
        "tests": ["information_content"],
        "expected": {"information_content": "VERY LOW (after first note)"},
        "science": "Single repeated pitch has P->1.0 after first exposure, IC->0",
    })

    # 5.4  Deceptive surprise: I-IV-V-I x3 then I-IV-V-bVI
    chords = (
        [Cmaj, Fmaj, G7, Cmaj] * 3
        + [Cmaj, Fmaj, G7, Abmaj]  # bVI instead of I
    )
    pm = _pm_progression(chords, [1.0] * 16, PIANO, 70)
    save(pm, g, "04_deceptive_surprise", {
        "description": "I-IV-V-I x3 (establishing expectation), then I-IV-V-bVI (surprise).",
        "tests": ["information_content", "arousal_scaling", "valence_inversion"],
        "expected": {
            "information_content": "SPIKE at bar 16 (Ab major)",
            "arousal_scaling": "SPIKE at bar 16",
            "valence_inversion": "DIP at bar 16",
        },
        "science": "Cheung 2019: precise context maximizes surprise at violation; R2=0.654",
    })

    # 5.5  Gradual chromaticism
    notes = (
        [C4, D4, E4, F4, G4, A4]           # diatonic
        + [G4, Ab4, A4, Bb4, B4, C5]       # mixed
        + [C5, Db4+12, D5, Eb4+12, E5, F5] # chromatic
        + [F5, Gb4+12, G5, Ab4+12, A5, Bb4+12]  # full chromatic
    )
    pm = _pm_melody(notes, [0.4] * len(notes), PIANO, 80)
    save(pm, g, "05_gradual_chromaticism", {
        "description": "Diatonic(6) -> mixed(6) -> chromatic(6) -> full chromatic(6).",
        "tests": ["information_content"],
        "expected": {"information_content": "PROGRESSIVE INCREASE across sections"},
        "science": "Progressive decrease in P(note|context) as chromaticism increases",
    })

    # 5.6  High entropy cluster (random onsets on 12 pitch classes)
    rng = np.random.RandomState(45)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    for pitch in range(C4, C4 + 12):
        for _ in range(4):
            s = float(rng.uniform(0, 5.5))
            e = s + float(rng.uniform(0.05, 0.3))
            inst.notes.append(pretty_midi.Note(70, pitch, s, min(e, 6.0)))
    pm.instruments.append(inst)
    save(pm, g, "06_high_entropy_cluster", {
        "description": "12 chromatic pitches with 4 random onsets each, seed=45. Max entropy.",
        "tests": ["information_content"],
        "expected": {"information_content": "VERY HIGH"},
        "science": "Maximum spectral flux entropy = maximum IC",
    })

    # 5.7  Consonant arpeggios (low IC, high valence)
    arp_c = [C4, E4, G4, C5, G4, E4]
    arp_g = [G3, B3, D4, G4, D4, B3]
    notes = (arp_c + arp_g) * 3
    pm = _pm_melody(notes, [0.22] * len(notes), PIANO, 80)
    save(pm, g, "07_consonant_arpeggios", {
        "description": "Alternating C major and G major arpeggios. Predictable, consonant.",
        "tests": ["information_content", "valence_inversion"],
        "expected": {"information_content": "LOW", "valence_inversion": "HIGH"},
        "science": "Low IC + high consonance -> max valence; Gold 2019: moderate IC optimal",
    })

    # 5.8  Jazz ii-V-I progression
    chords = [Dm7, G7_ext, Cmaj7, Am7] * 2
    pm = _pm_progression(chords, [1.0] * 8, PIANO, 70)
    save(pm, g, "08_jazz_iim7_V7_I", {
        "description": "ii7-V7-Imaj7-vi7 jazz cadence x2. Chromatic but structured.",
        "tests": ["information_content"],
        "expected": {"information_content": "MODERATE"},
        "science": "Jazz harmony: moderate IC within learned schema (Gold 2019: inverted-U)",
    })


# =====================================================================
# Category 6: Arousal / Valence / Defense (ICEM, 7 stimuli)
# =====================================================================

def generate_icem_emotion():
    """Category 6 — Arousal, valence, defense cascade (7 stimuli)."""
    print("\n=== CATEGORY 6: AROUSAL / VALENCE / DEFENSE (ICEM) ===")
    g = "icem"

    # 6.1  Sudden fortissimo (defense cascade)
    # Short quiet setup (2s) followed by LONG loud cluster (4s) so the
    # defense signal dominates the global mean.  Previous design (4s quiet
    # + 2s loud) diluted the spike in the mean.
    pm = pretty_midi.PrettyMIDI()
    # Brief quiet strings for 2s (just enough to establish baseline)
    inst_s = pretty_midi.Instrument(program=STRINGS)
    for p in major_triad(C4):
        inst_s.notes.append(pretty_midi.Note(25, p, 0.0, 2.0))
    pm.instruments.append(inst_s)
    # Sudden fff cluster at 2s, sustained for 4s
    inst_p = pretty_midi.Instrument(program=PIANO)
    cluster = chromatic_cluster(C4, 6)
    for p in cluster:
        inst_p.notes.append(pretty_midi.Note(127, p, 2.0, 6.0))
    pm.instruments.append(inst_p)
    save(pm, g, "09_sudden_fortissimo", {
        "description": "pp strings C major (2s) -> fff chromatic cluster (4s). "
                       "Short baseline, long loud section so defense dominates mean.",
        "tests": ["defense_cascade", "arousal_scaling", "information_content"],
        "expected": {
            "defense_cascade": "HIGH (spike at t=2s dominates mean)",
            "arousal_scaling": "HIGH",
            "information_content": "HIGH",
        },
        "science": "Egermann 2013: defense cascade = IC x arousal + loudness_velocity (SCR up, HR down)",
    }, gain=0.7)

    # 6.2  Gentle resolution (high valence)
    pm = _pm_progression([Cmaj, Fmaj, Gmaj, Cmaj], [2.5] * 4, PIANO, 70)
    save(pm, g, "10_gentle_resolution", {
        "description": "Slow I-IV-V-I at mf. Consonant, stable, predictable.",
        "tests": ["valence_inversion", "defense_cascade"],
        "expected": {"valence_inversion": "HIGH", "defense_cascade": "LOW"},
        "science": "Egermann 2013: low IC -> high valence; no defense trigger",
    })

    # 6.3  Crescendo build (arousal increases)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    n = 20
    for i in range(n):
        v = int(25 + (127 - 25) * i / (n - 1))
        # Accelerating tempo: IOI decreases from 0.8 to 0.2
        ioi = 0.8 - (0.6 * i / (n - 1))
        t = sum(0.8 - (0.6 * j / (n - 1)) for j in range(i))
        inst.notes.append(pretty_midi.Note(v, C4, t, t + ioi * 0.85))
    pm.instruments.append(inst)
    save(pm, g, "11_crescendo_build", {
        "description": "C4 notes: velocity 25->127, tempo accelerating (IOI 0.8->0.2s).",
        "tests": ["arousal_scaling", "arousal_change_pred"],
        "expected": {"arousal_scaling": "PROGRESSIVE INCREASE"},
        "science": "Salimpoor 2011: anticipatory arousal builds toward emotional peak",
    })

    # 6.4  Calm sustained (minimal arousal, max valence)
    pm = _pm_chord(major_triad(C4), 10.0, STRINGS, 50)
    save(pm, g, "12_calm_sustained", {
        "description": "Sustained C major chord on strings, pp, 10s.",
        "tests": ["arousal_scaling", "valence_inversion", "defense_cascade"],
        "expected": {
            "arousal_scaling": "VERY LOW",
            "valence_inversion": "VERY HIGH",
            "defense_cascade": "NEAR ZERO",
        },
        "science": "Minimal change + consonance = minimal IC = max valence, zero arousal/defense",
    }, gain=50.0 / 127.0)

    # 6.5  Dissonant sforzando repeated (moderate defense)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    cluster = chromatic_cluster(C4, 5)
    for i in range(6):
        for p in cluster:
            inst.notes.append(pretty_midi.Note(110, p, float(i), i + 0.3))
    pm.instruments.append(inst)
    save(pm, g, "13_dissonant_sfz_repeated", {
        "description": "Chromatic cluster sfz x6 at 1s intervals. Repeated but dissonant.",
        "tests": ["defense_cascade", "arousal_scaling"],
        "expected": {"defense_cascade": "MODERATE (predictable after 1st)", "arousal_scaling": "HIGH"},
        "science": "First event triggers defense; subsequent become predictable -> defense attenuates",
    })

    # 6.6  Negative-to-positive valence trajectory
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # First 4s: dissonant chromatic clusters
    dissonant_chords = [
        chromatic_cluster(C4, 4),
        diminished_triad(D4),
        [C4, Gb4, B4],  # tritone + aug4
        chromatic_cluster(E4, 5),
    ]
    for i, chord in enumerate(dissonant_chords):
        for p in chord:
            inst.notes.append(pretty_midi.Note(80, p, float(i), i + 1.0))
    # Last 4s: consonant resolution
    consonant_chords = [Gmaj, Cmaj, Fmaj, Cmaj]
    for i, chord in enumerate(consonant_chords):
        for p in chord:
            inst.notes.append(pretty_midi.Note(70, p, 4.0 + i, 5.0 + i))
    pm.instruments.append(inst)
    save(pm, g, "14_neg_to_pos_valence", {
        "description": "Dissonant clusters (4s) -> consonant I-IV-V-I (4s). Valence trajectory.",
        "tests": ["valence_inversion", "valence_shift_pred"],
        "expected": {"valence_inversion": "LOW(0-4s) -> HIGH(4-8s)"},
        "science": "Egermann 2013: valence tracks IC inversely; resolution increases valence",
    })

    # 6.7  High-to-low arousal trajectory
    pm = pretty_midi.PrettyMIDI()
    inst_p = pretty_midi.Instrument(program=PIANO)
    # First 4s: rapid loud staccato
    for i in range(32):
        t = i * 0.125  # 480 BPM
        inst_p.notes.append(pretty_midi.Note(120, C4, t, t + 0.1))
    pm.instruments.append(inst_p)
    # Last 4s: quiet sustained chord
    inst_s = pretty_midi.Instrument(program=STRINGS)
    for p in major_triad(C4):
        inst_s.notes.append(pretty_midi.Note(40, p, 4.0, 8.0))
    pm.instruments.append(inst_s)
    save(pm, g, "15_high_to_low_arousal", {
        "description": "Rapid loud staccato (4s) -> quiet sustained chord (4s).",
        "tests": ["arousal_scaling", "arousal_change_pred"],
        "expected": {"arousal_scaling": "HIGH(0-4s) -> LOW(4-8s)"},
        "science": "Arousal tracks onset density + loudness; sustained quiet = low arousal",
    })


# =====================================================================
# Category 7: Cross-Mechanism Integration (8+ stimuli)
# =====================================================================

def generate_cross():
    """Category 7 — Cross-mechanism integration (8+ stimuli)."""
    print("\n=== CATEGORY 7: CROSS-MECHANISM INTEGRATION ===")
    g = "cross"

    # 7.1  Full musical excerpt (baseline)
    mel = [E5, D5, C5, D5, E5, E5, E5, D5, D5, D5,
           E5, G5, G5, E5, D5, C5, D5, E5, E5, E5]
    mel_d = [0.5] * 20
    chds = [Cmaj, Cmaj, Am, Am, Fmaj, Fmaj, Gmaj, Gmaj, Cmaj, Cmaj]
    chd_d = [1.0] * 10
    pm = _pm_melody_with_chords(mel, mel_d, chds, chd_d)
    save(pm, g, "01_full_musical", {
        "description": "Mary Had a Little Lamb melody (flute) over I-vi-IV-V-I chords (piano).",
        "tests": ["all 15 beliefs"],
        "expected": "Baseline musical stimulus — all mechanisms engaged at moderate levels",
        "science": "Reference stimulus for normalization",
    })

    # 7.2  Predict then surprise: I-V x4 then modulate to Gb
    chords = (
        [Cmaj, Gmaj] * 4  # bars 1-8: predictable
        + [Gbmaj, Dbmaj] * 2  # bars 9-12: tritone modulation
    )
    pm = _pm_progression(chords, [1.0] * 12, PIANO, 70)
    save(pm, g, "02_predict_then_surprise", {
        "description": "I-V x4 (predictable) then modulate to Gb major (tritone away).",
        "tests": ["prediction_accuracy", "information_content", "error_propagation"],
        "expected": {
            "prediction_accuracy": "DROP at bar 9",
            "information_content": "SPIKE at bar 9",
            "error_propagation": "SPIKE at bar 9",
        },
        "science": "Triple mechanism hit: HTP/SPH/ICEM all respond to sudden key change",
    })

    # 7.3  Memorised motif with crescendo
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    motif = [C4, E4, G4, C5]
    for rep in range(8):
        v = int(40 + (127 - 40) * rep / 7)
        for j, p in enumerate(motif):
            t = rep * 1.5 + j * 0.375
            inst.notes.append(pretty_midi.Note(v, p, t, t + 0.35))
    pm.instruments.append(inst)
    save(pm, g, "03_memorised_crescendo", {
        "description": "C4-E4-G4-C5 motif x8 with velocity 40->127.",
        "tests": ["sequence_match", "arousal_scaling"],
        "expected": {"sequence_match": "INCREASING", "arousal_scaling": "INCREASING"},
        "science": "Dual build: Bonetti 2024 (memory) + Egermann 2013 (arousal)",
    })

    # 7.4  Hierarchy + completion: 8-bar arc x2
    arc = [
        Cmaj, Am, Dm, Fmaj,
        Gmaj, Em, G7, Cmaj,
    ]
    chords = arc * 2
    pm = _pm_progression(chords, [1.0] * 16, PIANO, 70)
    save(pm, g, "04_hierarchy_completion", {
        "description": "I-vi-ii-IV-V-iii-V7-I arc repeated twice. Clear phrase endings at bars 8,16.",
        "tests": ["hierarchy_coherence", "sequence_completion"],
        "expected": {
            "hierarchy_coherence": "SUSTAINED HIGH",
            "sequence_completion": "PEAKS at bars 8 and 16",
        },
        "science": "Both HTP hierarchy and SPH completion activate at cadential closures",
    })

    # 7.5  IC in memory context: repeated motif then chromatic deviant
    motif = [C4, E4, G4, C5]
    deviant = [C4, E4, Gb4, C5]  # Gb4 (tritone) instead of G4
    notes = motif * 6 + deviant + motif
    pm = _pm_melody(notes, [0.375] * len(notes), PIANO, 80)
    save(pm, g, "05_IC_in_memory", {
        "description": "C4-E4-G4-C5 x6, then Gb4 replaces G4 (tritone deviation), then normal.",
        "tests": ["information_content", "sequence_match", "error_propagation"],
        "expected": {
            "information_content": "SPIKE at deviant (position 25)",
            "sequence_match": "DIP at deviant",
            "error_propagation": "SPIKE at deviant",
        },
        "science": "Cheung 2019: precise expectation amplifies surprise; IC maximized in clear context",
    })

    # 7.6a  Minor hierarchy
    pm = _pm_progression([Cm, Fm, Gmaj, Cm], [2.0] * 4, PIANO, 70)
    save(pm, g, "06a_minor_hierarchy", {
        "description": "i-iv-V-i in C minor. Same structure as major but different mode.",
        "tests": ["valence_inversion", "hierarchy_coherence"],
        "expected": {"valence_inversion": "LOWER than major", "hierarchy_coherence": "SIMILAR to major"},
        "science": "Minor mode: lower consonance -> lower valence; structure preserved",
    })

    # 7.6b  Major hierarchy (control)
    pm = _pm_progression([Cmaj, Fmaj, Gmaj, Cmaj], [2.0] * 4, PIANO, 70)
    save(pm, g, "06b_major_hierarchy", {
        "description": "I-IV-V-I in C major. Control for minor comparison.",
        "tests": ["valence_inversion", "hierarchy_coherence"],
        "expected": {"valence_inversion": "HIGHER than minor", "hierarchy_coherence": "SIMILAR to minor"},
        "science": "Major mode: higher consonance -> higher valence; matched structure",
    })

    # 7.7  Defense in predictive context
    pm = pretty_midi.PrettyMIDI()
    # Quiet isochronous pattern for 6s
    inst_q = pretty_midi.Instrument(program=PIANO)
    ioi = 0.5
    for i in range(12):
        inst_q.notes.append(pretty_midi.Note(40, C4, i * ioi, i * ioi + ioi * 0.85))
    pm.instruments.append(inst_q)
    # Sudden loud cluster at 6s
    inst_l = pretty_midi.Instrument(program=PIANO)
    for p in chromatic_cluster(C3, 8):
        inst_l.notes.append(pretty_midi.Note(127, p, 6.0, 6.5))
    pm.instruments.append(inst_l)
    # Silence 6.5-8s (just let the MIDI end)
    save(pm, g, "07_defense_in_prediction", {
        "description": "Quiet C4 @120BPM (6s) -> fff chromatic cluster C3 (0.5s) -> silence.",
        "tests": ["defense_cascade", "prediction_accuracy", "information_content"],
        "expected": {
            "defense_cascade": "MASSIVE SPIKE at t=6s",
            "prediction_accuracy": "COLLAPSE at t=6s",
            "information_content": "SPIKE at t=6s",
        },
        "science": "Maximum defense: predictive context amplifies surprise of sudden loud event",
    })

    # 7.8  All mechanisms stressed (orchestral)
    pm = pretty_midi.PrettyMIDI()
    # Flute melody (diatonic, varied rhythm)
    inst_f = pretty_midi.Instrument(program=FLUTE)
    mel = [C5, D5, E5, G5, F5, E5, D5, C5, E5, F5, G5, A5, B5, C6, B5, A5,
           G5, F5, E5, D5, C5, D5, E5, C5]
    t = 0.0
    for i, p in enumerate(mel):
        d = 0.5 if i % 3 != 2 else 0.75
        inst_f.notes.append(pretty_midi.Note(90, p, t, t + d - 0.02))
        t += d
    pm.instruments.append(inst_f)
    # Piano chords (modulating C -> G)
    prog_chords = [
        Cmaj, Fmaj, Gmaj, Am,  # C major
        major_triad(G3), major_triad(C4), major_triad(D3), major_triad(G3),  # modulate to G
    ]
    inst_p = pretty_midi.Instrument(program=PIANO)
    for i, chord in enumerate(prog_chords):
        s = i * 1.5
        for p in chord:
            inst_p.notes.append(pretty_midi.Note(60, p, s, s + 1.5))
    pm.instruments.append(inst_p)
    # Trumpet interjections at bars 4 and 6 (ff)
    inst_t = pretty_midi.Instrument(program=TRUMPET)
    for bar in [4, 6]:
        s = bar * 1.5
        inst_t.notes.append(pretty_midi.Note(120, G5, s, s + 0.3))
        inst_t.notes.append(pretty_midi.Note(120, C6, s + 0.4, s + 0.7))
    pm.instruments.append(inst_t)
    save(pm, g, "08_all_stressed", {
        "description": "Orchestral: flute melody + piano chords (C->G modulation) + trumpet ff interjections.",
        "tests": ["all 15 beliefs"],
        "expected": "All mechanisms engaged at high levels. Maximum F2 complexity.",
        "science": "Stress test: every mechanism processes different aspects simultaneously",
    })


# =====================================================================
# Category 8: Boundary Conditions (5 stimuli)
# =====================================================================

def generate_boundary():
    """Category 8 — Boundary conditions (5 stimuli)."""
    print("\n=== CATEGORY 8: BOUNDARY CONDITIONS ===")
    g = "boundary"

    # 8.1  Silence
    pm = pretty_midi.PrettyMIDI()
    pm.instruments.append(pretty_midi.Instrument(program=PIANO))
    # No notes — just render 5s of silence
    save(pm, g, "01_silence", {
        "description": "Pure silence (empty MIDI). All beliefs should return near baseline.",
        "tests": ["all"],
        "expected": "All Core beliefs converge toward BASELINE=0.5. No NaN/Inf.",
        "science": "Boundary: zero input must produce valid output",
    })

    # 8.2  Single note sustained
    pm = _pm_note(C4, 5.0, PIANO, 80)
    save(pm, g, "02_single_note", {
        "description": "Single C4 piano note, 5s sustained.",
        "tests": ["prediction_accuracy", "information_content"],
        "expected": {
            "prediction_accuracy": "HIGH after onset (fully predictable)",
            "information_content": "SPIKE at onset, then LOW",
        },
        "science": "Boundary: minimal input, single onset event",
    })

    # 8.3  Extreme fast tempo (600 BPM = 10 notes/s)
    pm = _pm_isochronous(C4, 600, 50, PIANO, 80)
    save(pm, g, "03_extreme_fast", {
        "description": "C4 at 600 BPM (10 notes/sec), 50 beats. Near temporal fusion.",
        "tests": ["prediction_hierarchy"],
        "expected": {"prediction_hierarchy": "E2 (sensory) dominant — near-fusion rate"},
        "science": "Boundary: H0(25ms) resolution limit for onset detection",
    })

    # 8.4  Extreme slow tempo (30 BPM = 1 note every 2s)
    pm = _pm_isochronous(C4, 30, 5, PIANO, 80)
    save(pm, g, "04_extreme_slow", {
        "description": "C4 at 30 BPM, 5 notes over 10s. Long gaps between events.",
        "tests": ["prediction_hierarchy", "prediction_accuracy"],
        "expected": "Sparse H16(1s) updates; prediction accuracy limited by sparse input",
        "science": "Boundary: tests whether H16/H18 horizons can track at very slow rates",
    })

    # 8.5  Full chromatic cluster (all 12 notes sustained)
    pm = _pm_chord(chromatic_scale(C4, 12), 5.0, PIANO, 60)
    save(pm, g, "05_chromatic_cluster", {
        "description": "All 12 notes C4-B4 sustained simultaneously, 5s.",
        "tests": ["information_content", "valence_inversion", "prediction_hierarchy"],
        "expected": {
            "information_content": "HIGH (max entropy)",
            "valence_inversion": "LOW (max dissonance)",
            "prediction_hierarchy": "LOW (no structure)",
        },
        "science": "Boundary: maximum spectral complexity, zero tonal clarity",
    })


# =====================================================================
# Metadata & Catalog Writers
# =====================================================================

def write_metadata():
    """Write metadata.json with ground truth for all stimuli."""
    path = OUT_DIR / "metadata.json"
    with open(path, "w") as f:
        json.dump(ALL_METADATA, f, indent=2, ensure_ascii=False)
    print(f"\n  metadata.json -> {path.relative_to(_ROOT)}")


def write_catalog():
    """Write STIMULUS-CATALOG.md summarizing all stimuli."""
    path = OUT_DIR / "STIMULUS-CATALOG.md"
    lines = [
        "# F2 Test Audio Stimulus Catalog",
        "",
        f"**Total stimuli**: {_count}",
        f"**Mechanisms tested**: HTP, SPH, ICEM (15 beliefs)",
        "",
        "## Ordinal Comparisons (Ground Truth)",
        "",
        "| # | A | B | Belief | Expected | Paper |",
        "|---|---|---|--------|----------|-------|",
        "| 1 | htp/01 rich | htp/02 flat | prediction_hierarchy | A>B | de Vries 2023 |",
        "| 2 | htp/01 rich | htp/06 random | prediction_hierarchy | A>B | de Vries 2023 |",
        "| 3 | htp/03 high_level | htp/04 low_level | hierarchy_coherence | A>B | E3=sigma(E0-E2) |",
        "| 4 | htp/03 high_level | htp/02 flat | abstract_future | A>B | tonal_stab@1s |",
        "| 5 | htp/05 melody | htp/02 flat | midlevel_future | A>B | sharpness velocity |",
        "| 6 | htp/09 isochronous | htp/12 random | prediction_accuracy | A>B | Forseth 2020 |",
        "| 7 | htp/10 scale | htp/12 random | prediction_accuracy | A>B | Repetition |",
        "| 8 | htp/11 cadence | htp/12 random | prediction_accuracy | A>B | Structure |",
        "| 9 | sph/01 memorised | sph/02 varied | sequence_match | A>B | Bonetti 2024 |",
        "| 10 | sph/02 varied | sph/01 memorised | error_propagation | A>B | Bonetti 2024 |",
        "| 11 | sph/01 memorised | sph/06 novel | sequence_match | A>B | Repetition |",
        "| 12 | sph/05 chords | sph/06 novel | sequence_match | A>B | Harmonic memory |",
        "| 13 | sph/01 memorised | sph/02 varied | oscillatory_signature | A>B | Bonetti 2024 |",
        "| 14 | sph/08 authentic | sph/11 mid_phrase | sequence_completion | A>B | Bonetti 2024 |",
        "| 15 | sph/08 authentic | sph/12 deceptive | sequence_completion | A>B | I>vi |",
        "| 16 | sph/10 phrase_end | sph/11 mid_phrase | sequence_completion | A>B | Arc closure |",
        "| 17 | sph/08 authentic | sph/09 half | sequence_completion | A>B | V-I > half cadence |",
        "| 18 | icem/02 chromatic | icem/01 diatonic | information_content | A>B | Egermann 2013 |",
        "| 19 | icem/06 cluster | icem/03 repeated | information_content | A>B | Max vs min |",
        "| 20 | icem/01 diatonic | icem/02 chromatic | valence_inversion | A>B | IC->valence inv |",
        "| 21 | icem/07 consonant | icem/06 cluster | valence_inversion | A>B | (1-IC)+cons |",
        "| 22 | icem/02 chromatic | icem/01 diatonic | arousal_scaling | A>B | IC->arousal |",
        "| 23 | icem/09 sudden | icem/12 calm | defense_cascade | A>B | IC*arousal+loud |",
        "| 24 | icem/09 sudden | icem/13 repeated | defense_cascade | A>B | Sudden>repeated |",
        "| 25 | icem/12 calm | icem/09 sudden | valence_inversion | A>B | Low IC=high val |",
        "| 26 | icem/10 gentle | icem/13 dissonant | valence_inversion | A>B | Cons>diss |",
        "| 27 | cross/01 full | boundary/01 silence | prediction_hierarchy | A>B | Music>nothing |",
        "| 28 | boundary/05 cluster | boundary/02 single | information_content | A>B | 12>1 note |",
        "| 29 | boundary/02 single | boundary/05 cluster | prediction_accuracy | A>B | Sustain=pred |",
        "| 30 | cross/06b major | cross/06a minor | valence_inversion | A>B | Major>minor |",
        "",
        "## Stimulus Index",
        "",
    ]

    # Group by directory
    groups = {}
    for key, meta in sorted(ALL_METADATA.items()):
        grp = key.split("/")[0]
        if grp not in groups:
            groups[grp] = []
        groups[grp].append((key, meta))

    for grp_name, items in groups.items():
        lines.append(f"### {grp_name}/")
        lines.append("")
        lines.append("| File | Duration | Description |")
        lines.append("|------|----------|-------------|")
        for key, meta in items:
            fname = key.split("/", 1)[1]
            dur = meta.get("duration_s", "?")
            desc = meta.get("description", "")[:80]
            lines.append(f"| {fname} | {dur}s | {desc} |")
        lines.append("")

    with open(path, "w") as f:
        f.write("\n".join(lines))
    print(f"  STIMULUS-CATALOG.md -> {path.relative_to(_ROOT)}")


# =====================================================================
# Main
# =====================================================================

def main():
    """Generate all F2 test stimuli."""
    print("=" * 70)
    print("  F2 (Prediction) Test Audio Generator")
    print("  Output: Test-Audio/micro_beliefs/f2/")
    print("=" * 70)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Category 1: Temporal Hierarchy (HTP, 8 stimuli)
    generate_htp_hierarchy()

    # Category 2: Prediction Accuracy (HTP, 6 stimuli)
    generate_htp_accuracy()

    # Category 3: Sequence Memory (SPH, 7 stimuli)
    generate_sph_memory()

    # Category 4: Sequence Completion (SPH, 5 stimuli)
    generate_sph_completion()

    # Category 5: Information Content (ICEM, 8 stimuli)
    generate_icem_ic()

    # Category 6: Arousal/Valence/Defense (ICEM, 7 stimuli)
    generate_icem_emotion()

    # Category 7: Cross-Mechanism Integration (8+ stimuli)
    generate_cross()

    # Category 8: Boundary Conditions (5 stimuli)
    generate_boundary()

    # Write metadata and catalog
    write_metadata()
    write_catalog()

    print(f"\n{'=' * 70}")
    print(f"  DONE — {_count} stimuli generated")
    print(f"  Output: {OUT_DIR.relative_to(_ROOT)}/")
    print(f"{'=' * 70}")


if __name__ == "__main__":
    main()
