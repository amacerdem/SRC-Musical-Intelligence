"""Deterministic MIDI-based test audio generator for F4 (Memory Systems).

Generates 60 stimuli across 6 categories for testing all 13 F4 beliefs:
  - MEAMN (7 beliefs): autobiographical_retrieval, nostalgia_intensity,
    emotional_coloring, retrieval_probability, memory_vividness,
    self_relevance, vividness_trajectory
  - MMP (3 beliefs): melodic_recognition, memory_preservation,
    memory_scaffold_pred
  - HCMC (3 beliefs): episodic_encoding, episodic_boundary,
    consolidation_strength

Scientific basis:
  - MEAMN: Janata 2009 (mPFC autobiographical, N=13, p<0.0003),
    Sakakibara 2025 (EEG nostalgia, N=33, eta_p^2=0.636)
  - MMP: Jacobsen 2015 (AD-resistant memory, N=32),
    Derks-Dijkman 2024 (musical mnemonics, 28/37 studies)
  - HCMC: Fernandez-Rubio 2022 (hippocampal binding, N=71, p<0.001),
    Zacks 2007 (event segmentation), Rolls 2013 (CA3 autoassociation)

Output: .wav + .mid + metadata.json + STIMULUS-CATALOG.md
All files at 44,100 Hz, 16-bit PCM WAV.
"""
from __future__ import annotations

import json
import pathlib
import sys

import numpy as np
import pretty_midi
import torch
from scipy.io import wavfile

_PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from Tests.micro_beliefs.real_audio_stimuli import (
    SAMPLE_RATE,
    _render,
    PIANO, ORGAN, VIOLIN, STRINGS, FLUTE, CELLO, TRUMPET,
    GUITAR_NYLON, CHOIR,
    major_triad, minor_triad, diminished_triad, dominant_seventh,
    chromatic_cluster, diatonic_scale,
    C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5,
    C6,
)

OUTPUT_DIR = _PROJECT_ROOT / "Test-Audio" / "micro_beliefs" / "f4"
ALL_METADATA: dict = {}


# ── Save helper ──────────────────────────────────────────────────────

def save(pm: pretty_midi.PrettyMIDI, group: str, name: str,
         meta: dict, gain: float = 1.0) -> None:
    """Render MIDI → WAV + save .mid + collect metadata."""
    out_dir = OUTPUT_DIR / group
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save MIDI
    mid_path = out_dir / f"{name}.mid"
    pm.write(str(mid_path))

    # Render to audio
    audio = _render(pm)
    wav = audio.squeeze(0).numpy()

    # Apply gain and normalize
    if gain != 1.0:
        wav = wav * gain
    peak = np.abs(wav).max()
    if peak > 0:
        wav = wav * (0.95 / peak)
    wav = np.clip(wav, -1.0, 1.0)
    wav_int16 = (wav * 32767).astype(np.int16)

    wav_path = out_dir / f"{name}.wav"
    wavfile.write(str(wav_path), SAMPLE_RATE, wav_int16)

    meta["file"] = f"{group}/{name}.wav"
    meta["duration_s"] = round(len(wav) / SAMPLE_RATE, 2)
    ALL_METADATA[f"{group}/{name}"] = meta


# ── MIDI builder helpers ─────────────────────────────────────────────

def _pm_note(pitch: int, duration: float, program: int = PIANO,
             velocity: int = 80) -> pretty_midi.PrettyMIDI:
    """Single sustained note."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    inst.notes.append(pretty_midi.Note(
        velocity=velocity, pitch=pitch, start=0.0, end=duration,
    ))
    pm.instruments.append(inst)
    return pm


def _pm_chord(pitches: list[int], duration: float, program: int = PIANO,
              velocity: int = 80) -> pretty_midi.PrettyMIDI:
    """Sustained chord."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for p in pitches:
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=p, start=0.0, end=duration,
        ))
    pm.instruments.append(inst)
    return pm


def _pm_melody(notes: list[int], durations: list[float],
               program: int = PIANO, velocity: int = 80) -> pretty_midi.PrettyMIDI:
    """Monophonic melody."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for pitch, dur in zip(notes, durations):
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch,
            start=t, end=t + dur - 0.02,
        ))
        t += dur
    pm.instruments.append(inst)
    return pm


def _pm_progression(chords: list[list[int]], durations: list[float],
                    program: int = PIANO,
                    velocity: int = 80) -> pretty_midi.PrettyMIDI:
    """Chord progression — sequence of chords."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    t = 0.0
    for chord_pitches, dur in zip(chords, durations):
        for p in chord_pitches:
            inst.notes.append(pretty_midi.Note(
                velocity=velocity, pitch=p, start=t, end=t + dur,
            ))
        t += dur
    pm.instruments.append(inst)
    return pm


def _pm_isochronous(pitch: int, bpm: float, n_beats: int,
                    program: int = PIANO,
                    velocity: int = 80) -> pretty_midi.PrettyMIDI:
    """Equally-spaced beats."""
    ioi = 60.0 / bpm
    note_dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_beats):
        t = i * ioi
        inst.notes.append(pretty_midi.Note(
            velocity=velocity, pitch=pitch,
            start=t, end=t + note_dur,
        ))
    pm.instruments.append(inst)
    return pm


def _pm_melody_with_chords(
    melody_notes: list[int], melody_durs: list[float],
    chord_notes: list[list[int]], chord_durs: list[float],
    melody_program: int = FLUTE, chord_program: int = PIANO,
    melody_velocity: int = 90, chord_velocity: int = 60,
) -> pretty_midi.PrettyMIDI:
    """Melody over chord accompaniment."""
    pm = pretty_midi.PrettyMIDI()
    mel_inst = pretty_midi.Instrument(program=melody_program)
    t = 0.0
    for pitch, dur in zip(melody_notes, melody_durs):
        mel_inst.notes.append(pretty_midi.Note(
            velocity=melody_velocity, pitch=pitch,
            start=t, end=t + dur - 0.02,
        ))
        t += dur
    pm.instruments.append(mel_inst)

    chd_inst = pretty_midi.Instrument(program=chord_program)
    t = 0.0
    for chord_pitches, dur in zip(chord_notes, chord_durs):
        for p in chord_pitches:
            chd_inst.notes.append(pretty_midi.Note(
                velocity=chord_velocity, pitch=p, start=t, end=t + dur,
            ))
        t += dur
    pm.instruments.append(chd_inst)
    return pm


def _pm_two_part(part_a: dict, part_b: dict) -> pretty_midi.PrettyMIDI:
    """Concatenate two sections: part_a (0→dur_a) then part_b (dur_a→end).

    Each part dict: {pitches: [[int]], durations: [float], program: int, velocity: int}
    """
    pm = pretty_midi.PrettyMIDI()
    t = 0.0
    for part in [part_a, part_b]:
        inst = pretty_midi.Instrument(program=part["program"])
        for chord_pitches, dur in zip(part["pitches"], part["durations"]):
            for p in chord_pitches:
                inst.notes.append(pretty_midi.Note(
                    velocity=part["velocity"], pitch=p,
                    start=t, end=t + dur,
                ))
            t += dur
        pm.instruments.append(inst)
    return pm


# ── Chord shorthands ─────────────────────────────────────────────────

Cmaj = major_triad(C4)
Fmaj = major_triad(F3)
Gmaj = major_triad(G3)
Am = minor_triad(A3)
G7 = dominant_seventh(G3)
Dm = minor_triad(D4)
Em = minor_triad(E4)

# I-IV-V-I cadence in C major
CADENCE_I_IV_V_I = [Cmaj, Fmaj, G7, Cmaj]
CADENCE_DURS = [2.0, 2.0, 2.0, 2.0]

# I-vi-IV-V-I emotional progression
EMOTIONAL_PROG = [Cmaj, Am, Fmaj, Gmaj, Cmaj]
EMOTIONAL_DURS = [2.0, 2.0, 2.0, 2.0, 2.0]


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 1: MEAMN — Autobiographical Memory & Retrieval (12 stimuli)
#
# Tests: autobiographical_retrieval, nostalgia_intensity,
#        emotional_coloring, retrieval_probability, memory_vividness,
#        self_relevance, vividness_trajectory
#
# Mechanism: MEAMN (12D relay, Phase 0a)
# Key R³ inputs: warmth[12], stumpf_fusion[3], roughness[0], loudness[10],
#                x_l0l5[25:33], x_l5l7[41:49]
# Key H³: warmth M18 trend@H20, tonalness M14 periodicity@H16
# ═══════════════════════════════════════════════════════════════════════

def generate_meamn_stimuli() -> None:
    """12 stimuli targeting MEAMN relay and its 7 beliefs."""

    # ── 01: Warm organ C major — HIGH autobiographical/nostalgia ──────
    # Organ produces high warmth (R³[12]), rich harmonics → high x_l5l7.
    # Sustained consonance → high stumpf_fusion → high E0:f01_retrieval.
    # Science: Janata 2009 — tonal space tracking in mPFC, N=13, p<0.0003
    pm = _pm_chord(major_triad(C3) + major_triad(C4), 8.0,
                   program=ORGAN, velocity=75)
    save(pm, "meamn", "01_warm_organ_cmaj", {
        "description": "Organ C major (warm+consonant), sustained 8s",
        "expected": {
            "autobiographical_retrieval": "HIGH — warm timbre + stumpf_fusion + x_l5l7",
            "nostalgia_intensity": "HIGH — warmth×familiarity via x_l5l7",
            "emotional_coloring": "HIGH — low roughness × moderate loudness",
        },
        "science": "Janata 2009: mPFC tracks tonal familiarity (N=13, p<0.0003)",
    })

    # ── 02: Warm strings slow melody — HIGH warmth/retrieval ──────────
    # Strings (program=48) have high warmth + smooth timbre.
    # Slow diatonic melody → melodic recognition + tonal coherence.
    # Science: Sakakibara 2025 — EEG nostalgia (N=33, eta_p^2=0.636)
    melody = diatonic_scale(C4, 8)
    durs = [1.0] * 8
    pm = _pm_melody(melody, durs, program=STRINGS, velocity=70)
    save(pm, "meamn", "02_warm_strings_melody", {
        "description": "Strings slow C major diatonic melody, 8s",
        "expected": {
            "autobiographical_retrieval": "HIGH — warmth + melodic tonalness",
            "nostalgia_intensity": "HIGH — warm timbre strings (Sakakibara 2025)",
        },
        "science": "Sakakibara 2025: warm timbres enhance nostalgia (eta_p^2=0.636)",
    })

    # ── 03: Piano lullaby I-IV-V-I — HIGH familiarity ────────────────
    # Gentle piano progression → high stumpf_fusion_mean_5s (H3 H20 L0).
    # Slow progression builds familiarity → rising retrieval over time.
    pm = _pm_progression(CADENCE_I_IV_V_I, CADENCE_DURS,
                         program=PIANO, velocity=65)
    save(pm, "meamn", "03_piano_lullaby_cadence", {
        "description": "Piano I-IV-V-I gentle cadence, 8s total",
        "expected": {
            "autobiographical_retrieval": "MODERATE-HIGH — consonant but less warm than organ",
            "nostalgia_intensity": "MODERATE — piano less warm than organ/strings",
            "emotional_coloring": "MODERATE — gentle dynamics, low roughness",
        },
        "science": "Janata 2007: 30-80% of familiar music triggers MEAM",
    })

    # ── 04: 12-note chromatic cluster forte — LOW autobiographical ────
    # Maximum roughness, minimum stumpf_fusion, high entropy.
    # E0 = σ(0.80 × x_l0l5.mean × retrieval × stumpf) → near 0.
    cluster = chromatic_cluster(C4, 12)
    pm = _pm_chord(cluster, 8.0, program=PIANO, velocity=110)
    save(pm, "meamn", "04_harsh_cluster_12note", {
        "description": "12-note chromatic cluster C4-B4, forte, 8s",
        "expected": {
            "autobiographical_retrieval": "LOW — zero stumpf_fusion, max roughness",
            "nostalgia_intensity": "LOW — no warmth signal from inharmonic mass",
            "emotional_coloring": "LOW — high roughness × loudness = negative valence",
        },
        "science": "Plomp & Levelt 1965: max roughness at ~25% critical bandwidth",
    })

    # ── 05: Silence 8s — BASELINE ────────────────────────────────────
    # Zero R³ input → all MEAMN outputs → baseline (~0.3-0.4).
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(pretty_midi.Note(
        velocity=1, pitch=60, start=0.0, end=0.01,
    ))
    pm.instruments.append(inst)
    save(pm, "meamn", "05_near_silence", {
        "description": "Near-silence (single tick), 8s",
        "expected": {
            "autobiographical_retrieval": "BASELINE — minimal input",
            "nostalgia_intensity": "BASELINE",
            "emotional_coloring": "BASELINE",
        },
        "science": "Control stimulus: near-zero R³ activation",
    })

    # ── 06: Consonant → Dissonant transition ─────────────────────────
    # Organ C major (5s) → 12-note cluster (5s).
    # Tests temporal dynamics: autobiographical should FALL in second half.
    # Science: Janata 2009 — retrieval tracks tonal coherence over time
    pm = pretty_midi.PrettyMIDI()
    inst_a = pretty_midi.Instrument(program=ORGAN)
    for p in major_triad(C3) + major_triad(C4):
        inst_a.notes.append(pretty_midi.Note(
            velocity=75, pitch=p, start=0.0, end=5.0,
        ))
    pm.instruments.append(inst_a)
    inst_b = pretty_midi.Instrument(program=PIANO)
    for p in chromatic_cluster(C4, 12):
        inst_b.notes.append(pretty_midi.Note(
            velocity=110, pitch=p, start=5.0, end=10.0,
        ))
    pm.instruments.append(inst_b)
    save(pm, "meamn", "06_consonant_to_dissonant", {
        "description": "Organ C major (5s) → 12-note cluster (5s), 10s total",
        "expected": {
            "autobiographical_retrieval": "FALLING — warm consonant → harsh dissonant",
            "nostalgia_intensity": "FALLING — warmth drops at 5s boundary",
            "emotional_coloring": "FALLING — valence drops (roughness rises)",
        },
        "science": "Temporal tracking of memory dissolution at tonal disruption",
    })

    # ── 07: Dissonant → Consonant transition ─────────────────────────
    # 12-note cluster (5s) → Organ C major (5s).
    # autobiographical should RISE in second half.
    pm = pretty_midi.PrettyMIDI()
    inst_a = pretty_midi.Instrument(program=PIANO)
    for p in chromatic_cluster(C4, 12):
        inst_a.notes.append(pretty_midi.Note(
            velocity=110, pitch=p, start=0.0, end=5.0,
        ))
    pm.instruments.append(inst_a)
    inst_b = pretty_midi.Instrument(program=ORGAN)
    for p in major_triad(C3) + major_triad(C4):
        inst_b.notes.append(pretty_midi.Note(
            velocity=75, pitch=p, start=5.0, end=10.0,
        ))
    pm.instruments.append(inst_b)
    save(pm, "meamn", "07_dissonant_to_consonant", {
        "description": "12-note cluster (5s) → Organ C major (5s), 10s total",
        "expected": {
            "autobiographical_retrieval": "RISING — harsh → warm consonant",
            "nostalgia_intensity": "RISING — warmth recovers at 5s",
            "emotional_coloring": "RISING — valence improves (roughness drops)",
        },
        "science": "Temporal tracking of memory recovery at tonal restoration",
    })

    # ── 08: Loud consonant forte — HIGH emotional_coloring ───────────
    # E2:f03_emotion = σ(0.60 × (1-roughness) × loudness × arousal)
    # High loudness + low roughness = maximum E2.
    pm = _pm_chord(major_triad(C4), 6.0, program=PIANO, velocity=120)
    save(pm, "meamn", "08_loud_consonant_forte", {
        "description": "Piano C major forte (v=120), 6s",
        "expected": {
            "emotional_coloring": "HIGH — (1-roughness)×loudness maximized",
            "autobiographical_retrieval": "MODERATE-HIGH — consonant but not warm timbre",
        },
        "science": "Arousal-valence model: loud+consonant = positive+activated",
    })

    # ── 09: Quiet dissonant piano — LOW emotional_coloring ───────────
    # Low loudness + high roughness = minimum E2.
    pm = _pm_chord([C4, Db4], 6.0, program=PIANO, velocity=30)
    save(pm, "meamn", "09_quiet_dissonant_pp", {
        "description": "Piano m2 (C4+Db4) pp (v=30), 6s",
        "expected": {
            "emotional_coloring": "LOW — high roughness × low loudness",
            "autobiographical_retrieval": "LOW — dissonant, quiet",
        },
        "science": "Low arousal + negative valence = minimal emotional coloring",
    })

    # ── 10: Repeated I-IV-V-I ×3 — RISING familiarity ────────────────
    # Repetition builds stumpf_fusion_mean_5s (H3 H20 L0).
    # tau=0.85 means slow accumulation → measurable rise over 24s.
    # Science: Janata 2009 — familiarity increases retrieval probability
    chords = CADENCE_I_IV_V_I * 3
    durs = CADENCE_DURS * 3
    pm = _pm_progression(chords, durs, program=ORGAN, velocity=70)
    save(pm, "meamn", "10_repeated_cadence_x3", {
        "description": "I-IV-V-I ×3 organ cadence, 24s total",
        "expected": {
            "autobiographical_retrieval": "RISING — familiarity accumulates (tau=0.85)",
            "nostalgia_intensity": "RISING — warmth + repeated pattern builds nostalgia",
            "retrieval_probability": "RISING — P0:memory_state tracks familiarity",
        },
        "science": "Janata 2009: tonal familiarity increases retrieval (N=13)",
    })

    # ── 11: Emotional I-vi-IV-V-I progression — emotional content ────
    # Minor chord (Am) creates contrast → emotional coloring variation.
    # Flute melody over piano chords for rich texture.
    melody_notes = [E5, D5, C5, E5, F5, E5, D5, C5, D5, C5]
    melody_durs = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    pm = _pm_melody_with_chords(
        melody_notes, melody_durs,
        EMOTIONAL_PROG, EMOTIONAL_DURS,
        melody_program=FLUTE, chord_program=ORGAN,
        melody_velocity=85, chord_velocity=60,
    )
    save(pm, "meamn", "11_emotional_flute_organ", {
        "description": "Flute melody over organ I-vi-IV-V-I, 10s",
        "expected": {
            "emotional_coloring": "HIGH — rich texture, varied valence",
            "memory_vividness": "HIGH — E0×P1 product (retrieval × emotion)",
            "self_relevance": "MODERATE — self-referential via complex engagement",
        },
        "science": "Janata 2009: mPFC self-referential processing (N=13, p=0.012)",
    })

    # ── 12: Choir sustained chord — maximal warmth ────────────────────
    # Choir Aahs (GM 52) produces maximum warmth + smooth consonance.
    # Science: Sakakibara 2025 — vocal timbres maximize nostalgia
    pm = _pm_chord(major_triad(C4), 8.0, program=CHOIR, velocity=70)
    save(pm, "meamn", "12_choir_cmaj_sustained", {
        "description": "Choir Aahs C major sustained 8s (maximal warmth)",
        "expected": {
            "nostalgia_intensity": "HIGHEST — vocal warmth × consonance",
            "autobiographical_retrieval": "HIGH — warmth + stumpf_fusion",
            "vividness_trajectory": "HIGH — F0:mem_vividness_fc forecasts vivid memory",
        },
        "science": "Sakakibara 2025: vocal timbre enhances nostalgia (eta_p^2=0.636)",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 2: MMP — Musical Mnemonic Preservation (8 stimuli)
#
# Tests: melodic_recognition, memory_preservation, memory_scaffold_pred
#
# Mechanism: MMP (12D relay, Phase 0a)
# Key R³: warmth[12], tonalness[14], tristimulus[18:21], entropy[22],
#          stumpf_fusion[3], x_l5l7[41:49]
# Key H³: warmth/tonalness/stumpf at H16 L2, warmth mean H20 L0
# ═══════════════════════════════════════════════════════════════════════

def generate_mmp_stimuli() -> None:
    """8 stimuli targeting MMP relay and its 3 beliefs."""

    # ── 01: Clear piano C major melody — HIGH melodic_recognition ─────
    # R1 = σ(familiarity × tonalness_val × trist1_val × preservation_factor)
    # Clear piano produces high tonalness + strong tristimulus1.
    # Science: Jacobsen 2015 — SMA/ACC preserve melodic memory (N=32)
    melody = diatonic_scale(C4, 8)
    durs = [0.5] * 8
    pm = _pm_melody(melody, durs, program=PIANO, velocity=80)
    save(pm, "mmp", "01_tonal_piano_melody", {
        "description": "Piano C major scale melody, 4s",
        "expected": {
            "melodic_recognition": "HIGH — high tonalness × clear tristimulus",
            "memory_preservation": "HIGH — low entropy tonal signal",
        },
        "science": "Jacobsen 2015: musical memory preserved in SMA/ACC (N=32)",
    })

    # ── 02: Organ warm sustained drone — HIGH memory_preservation ─────
    # C0:preservation_index driven by cortical_strength =
    #   0.35×warmth + 0.35×tonalness + 0.30×trist_mean
    # Organ provides maximum warmth + tonalness + clear tristimulus.
    pm = _pm_chord([C3, C4], 8.0, program=ORGAN, velocity=70)
    save(pm, "mmp", "02_organ_warm_drone", {
        "description": "Organ C3+C4 sustained drone, 8s",
        "expected": {
            "memory_preservation": "HIGH — max cortical_strength from warmth+tonalness",
            "memory_scaffold_pred": "HIGH — F2:scaffold_fc positive forecast",
        },
        "science": "Jacobsen 2015: cortically-mediated preservation pathway (N=32)",
    })

    # ── 03: Violin sustained C4 — HIGH tristimulus ────────────────────
    # Violin has distinctive harmonic spectrum → clear trist1.
    pm = _pm_note(C4, 8.0, program=VIOLIN, velocity=75)
    save(pm, "mmp", "03_violin_sustained", {
        "description": "Violin C4 sustained 8s (high tristimulus)",
        "expected": {
            "melodic_recognition": "MODERATE — single note, clear timbre",
            "memory_preservation": "HIGH — violin warmth + tonalness",
        },
        "science": "Tristimulus model: violin has distinctive spectral identity",
    })

    # ── 04: Chromatic wandering — LOW melodic_recognition ─────────────
    # Random chromatic pitches → low tonalness, high entropy.
    # preservation_factor = σ(cortical_strength × 0.9 - entropy × 0.8)
    rng = np.random.RandomState(42)
    notes = [C4 + int(n) for n in rng.randint(0, 12, size=16)]
    durs = [0.4] * 16
    pm = _pm_melody(notes, durs, program=PIANO, velocity=80)
    save(pm, "mmp", "04_chromatic_wandering", {
        "description": "Random chromatic notes (seed=42), 6.4s",
        "expected": {
            "melodic_recognition": "LOW — no tonal center, high entropy",
            "memory_preservation": "LOW — entropy penalizes preservation",
        },
        "science": "High entropy reduces cortical preservation factor",
    })

    # ── 05: Noise baseline — LOWEST preservation ─────────────────────
    # No tonal structure → tonalness≈0, warmth≈0, entropy=max.
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    rng = np.random.RandomState(43)
    for i in range(80):
        p = int(rng.randint(30, 90))
        t = i * 0.1
        inst.notes.append(pretty_midi.Note(
            velocity=int(rng.randint(40, 120)),
            pitch=p, start=t, end=t + 0.08,
        ))
    pm.instruments.append(inst)
    save(pm, "mmp", "05_dense_random_noise", {
        "description": "Dense random MIDI (80 notes in 8s, seed=43) — noise-like",
        "expected": {
            "melodic_recognition": "LOWEST — no melodic coherence",
            "memory_preservation": "LOWEST — max entropy, no cortical anchor",
        },
        "science": "Control: maximum entropy destroys preservation pathway",
    })

    # ── 06: Tonal → Atonal transition — FALLING recognition ──────────
    # C major melody (4s) → random chromatic (4s).
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for p in diatonic_scale(C4, 8):
        inst.notes.append(pretty_midi.Note(
            velocity=80, pitch=p, start=t, end=t + 0.48,
        ))
        t += 0.5
    rng = np.random.RandomState(44)
    for _ in range(8):
        p = C4 + int(rng.randint(0, 12))
        inst.notes.append(pretty_midi.Note(
            velocity=80, pitch=p, start=t, end=t + 0.48,
        ))
        t += 0.5
    pm.instruments.append(inst)
    save(pm, "mmp", "06_tonal_to_atonal", {
        "description": "C major melody (4s) → random chromatic (4s)",
        "expected": {
            "melodic_recognition": "FALLING — tonalness drops at boundary",
            "memory_preservation": "FALLING — cortical_strength decreases",
        },
        "science": "Jacobsen 2015: preservation tracks tonal coherence",
    })

    # ── 07: Flute clear melody — HIGHEST tonal clarity ────────────────
    # Flute has purest fundamental → maximum tonalness.
    melody = [C5, D5, E5, F5, G5, F5, E5, D5, C5, D5, E5, C5]
    durs = [0.5] * 12
    pm = _pm_melody(melody, durs, program=FLUTE, velocity=85)
    save(pm, "mmp", "07_flute_clear_melody", {
        "description": "Flute C major melody, clear tonalness, 6s",
        "expected": {
            "melodic_recognition": "HIGHEST — pure tone + clear pitch",
            "memory_scaffold_pred": "HIGH — scaffold efficacy from clear structure",
        },
        "science": "Flute: near-sinusoidal fundamental → maximum tonalness",
    })

    # ── 08: Guitar nylon warm — medium warmth ─────────────────────────
    pm = _pm_chord(major_triad(C4), 6.0, program=GUITAR_NYLON, velocity=70)
    save(pm, "mmp", "08_guitar_nylon_cmaj", {
        "description": "Nylon guitar C major chord, 6s",
        "expected": {
            "melodic_recognition": "MODERATE — chord, not melody",
            "memory_preservation": "MODERATE — warm but less than organ",
        },
        "science": "Nylon guitar: moderate warmth, moderate tristimulus",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 3: HCMC — Hippocampal-Cortical Memory Circuit (10 stimuli)
#
# Tests: episodic_encoding, episodic_boundary, consolidation_strength
#
# Mechanism: HCMC (11D, Depth 1, reads MEAMN relay)
# Key R³: stumpf_fusion[3], spectral_flux[21], onset_strength[11],
#          loudness[10], amplitude[7], harmonicity[5], tonalness[14],
#          entropy[22], x_l0l5[25:33], x_l5l7[41:49]
# Key H³: stumpf_fusion mean@H16, flux mean@H16, harmonicity mean@H20,
#          tonalness autocorr@H20
# ═══════════════════════════════════════════════════════════════════════

def generate_hcmc_stimuli() -> None:
    """10 stimuli targeting HCMC encoder and its 3 beliefs."""

    # ── 01: Strong beats consonant — HIGH episodic_encoding ──────────
    # E0:fast_binding = σ(0.35×x_l0l5×stumpf_1s + 0.35×stumpf×stumpf_1s
    #                     + 0.30×onset_str×loudness)
    # Strong onsets + high stumpf_fusion = maximum binding.
    # Science: Fernandez-Rubio 2022 — hippocampal binding at 4th tone (N=71)
    pm = _pm_isochronous(C4, 120.0, 20, program=PIANO, velocity=100)
    save(pm, "hcmc", "01_strong_beats_cmaj", {
        "description": "Piano C4 @120BPM forte (v=100), 20 beats, 10s",
        "expected": {
            "episodic_encoding": "HIGH — strong onsets × consonance → max binding",
        },
        "science": "Fernandez-Rubio 2022: hippocampal binding (N=71, p<0.001)",
    })

    # ── 02: Sustained quiet tone — LOW episodic_encoding ─────────────
    # No onsets after initial attack → onset_str≈0 after first beat.
    # Low loudness → minimal arousal contribution.
    pm = _pm_note(C4, 10.0, program=ORGAN, velocity=40)
    save(pm, "hcmc", "02_sustained_quiet_organ", {
        "description": "Organ C4 quiet sustained (v=40), 10s",
        "expected": {
            "episodic_encoding": "LOW — no repeated onsets, low loudness",
            "episodic_boundary": "LOW — no spectral flux (sustained tone)",
            "consolidation_strength": "MODERATE — tonal but static",
        },
        "science": "Continuous tones minimize binding activation",
    })

    # ── 03: Abrupt key transitions — HIGH episodic_boundary ──────────
    # E1:episodic_seg = σ(0.40×flux×flux_1s + 0.30×entropy×flux
    #                     + 0.30×onset_str×flux)
    # Abrupt chord changes → max spectral_flux at boundaries.
    # Science: Zacks 2007 — event segmentation theory
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    transitions = [
        (major_triad(C4), 0.0, 2.0),
        (major_triad(F4), 2.5, 4.5),     # 0.5s gap
        (major_triad(Ab4), 5.0, 7.0),    # distant key
        (major_triad(E4), 7.5, 9.5),     # another distant key
    ]
    for pitches, start, end in transitions:
        for p in pitches:
            inst.notes.append(pretty_midi.Note(
                velocity=90, pitch=p, start=start, end=end,
            ))
    pm.instruments.append(inst)
    save(pm, "hcmc", "03_abrupt_key_transitions", {
        "description": "4 chords in distant keys with 0.5s gaps, 9.5s",
        "expected": {
            "episodic_boundary": "HIGH — max spectral_flux at key changes",
            "episodic_encoding": "MODERATE — onsets present but sparse",
        },
        "science": "Zacks 2007: event boundaries trigger segmentation (N=72)",
    })

    # ── 04: Smooth sustained drone — LOW episodic_boundary ───────────
    # Zero spectral flux, zero onset after attack → E1≈0.
    pm = _pm_chord([C3, G3, C4, E4, G4], 10.0, program=ORGAN, velocity=65)
    save(pm, "hcmc", "04_smooth_organ_drone", {
        "description": "Organ C major spread voicing sustained 10s",
        "expected": {
            "episodic_boundary": "LOWEST — zero flux, zero onset after initial",
            "consolidation_strength": "HIGH — tonal coherence over time",
        },
        "science": "Continuous harmonic → no event boundaries",
    })

    # ── 05: Rapid key changes — HIGH flux, HIGH boundary ─────────────
    # Key change every 1s through circle of fifths.
    # Maximum boundary density → highest episodic_boundary.
    Ab3 = 56
    keys = [C4, G4, D4, A4, E4, B3, Gb4, Db4, Ab3, Eb4]
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for root in keys:
        for p in major_triad(root):
            inst.notes.append(pretty_midi.Note(
                velocity=85, pitch=p, start=t, end=t + 0.95,
            ))
        t += 1.0
    pm.instruments.append(inst)
    save(pm, "hcmc", "05_rapid_key_changes", {
        "description": "Circle of fifths, new key every 1s, 10s total",
        "expected": {
            "episodic_boundary": "HIGH — frequent spectral_flux spikes",
            "episodic_encoding": "HIGH — frequent onsets × consonance",
        },
        "science": "Rapid harmonic change maximizes boundary detection",
    })

    # ── 06: Tonal repetition — HIGH consolidation_strength ───────────
    # E2 = σ(0.35×x_l5l7×harm_5s + 0.35×harmonicity×tonal_autocorr_5s
    #        + 0.30×(1-entropy)×tonalness)
    # Repeated consonant chord → high harmonicity_mean_5s + tonalness.
    # Science: Sikka 2015 — hippocampal→cortical shift for melody (N=40)
    chords = [major_triad(C4)] * 8
    durs = [1.0] * 8
    pm = _pm_progression(chords, durs, program=ORGAN, velocity=70)
    save(pm, "hcmc", "06_tonal_repetition", {
        "description": "Organ C major chord ×8 repetitions, 8s",
        "expected": {
            "consolidation_strength": "HIGH — max harmonicity + tonalness over time",
            "episodic_encoding": "MODERATE — onsets but no novelty",
        },
        "science": "Sikka 2015: hippocampal→cortical melody consolidation (N=40)",
    })

    # ── 07: Entropy chaos — LOW consolidation_strength ────────────────
    # Random atonal cluster sequence → high entropy, low tonalness.
    rng = np.random.RandomState(45)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for _ in range(10):
        n_notes = int(rng.randint(3, 8))
        pitches = [int(rng.randint(48, 84)) for _ in range(n_notes)]
        for p in pitches:
            inst.notes.append(pretty_midi.Note(
                velocity=int(rng.randint(60, 110)),
                pitch=p, start=t, end=t + 0.9,
            ))
        t += 1.0
    pm.instruments.append(inst)
    save(pm, "hcmc", "07_entropy_chaos", {
        "description": "Random atonal cluster sequence (seed=45), 10s",
        "expected": {
            "consolidation_strength": "LOW — max entropy, no tonal coherence",
            "episodic_encoding": "MODERATE — onsets exist but no binding coherence",
        },
        "science": "High entropy prevents cortical consolidation",
    })

    # ── 08: Clear phrase boundaries — HIGH boundary at cadences ───────
    # 4-bar phrases with authentic cadences (V-I) at boundaries.
    # Science: Zacks 2007 — event segmentation at phrase boundaries
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    # Phrase 1: I-IV-V-I (4 beats)
    for chord, dur in zip(CADENCE_I_IV_V_I, [1.5, 1.5, 1.5, 1.5]):
        for p in chord:
            inst.notes.append(pretty_midi.Note(
                velocity=80, pitch=p, start=t, end=t + dur,
            ))
        t += dur
    # Gap (boundary marker)
    t += 0.5
    # Phrase 2: same cadence, different register
    for chord, dur in zip(
        [major_triad(G3), major_triad(C4), dominant_seventh(D4), major_triad(G3)],
        [1.5, 1.5, 1.5, 1.5],
    ):
        for p in chord:
            inst.notes.append(pretty_midi.Note(
                velocity=80, pitch=p, start=t, end=t + dur,
            ))
        t += dur
    pm.instruments.append(inst)
    save(pm, "hcmc", "08_phrase_boundaries", {
        "description": "Two 4-chord phrases with 0.5s gap, ~12.5s",
        "expected": {
            "episodic_boundary": "HIGH at gap — spectral flux spike at silence",
            "episodic_encoding": "HIGH — structured onsets with consonance",
        },
        "science": "Zacks 2007: phrase boundaries trigger event segmentation",
    })

    # ── 09: Crescendo beats — RISING episodic_encoding ────────────────
    # Velocity 40→120 over 10s → increasing onset_str×loudness.
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    n_beats = 20
    for i in range(n_beats):
        v = int(40 + (120 - 40) * i / (n_beats - 1))
        t = i * 0.5
        inst.notes.append(pretty_midi.Note(
            velocity=v, pitch=C4, start=t, end=t + 0.42,
        ))
    pm.instruments.append(inst)
    save(pm, "hcmc", "09_crescendo_beats", {
        "description": "Piano C4 beats v=40→120 @120BPM, 10s",
        "expected": {
            "episodic_encoding": "RISING — onset_str × loudness increases",
        },
        "science": "Crescendo increases binding activation over time",
    })

    # ── 10: Decrescendo beats — FALLING episodic_encoding ─────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    n_beats = 20
    for i in range(n_beats):
        v = int(120 - (120 - 40) * i / (n_beats - 1))
        t = i * 0.5
        inst.notes.append(pretty_midi.Note(
            velocity=v, pitch=C4, start=t, end=t + 0.42,
        ))
    pm.instruments.append(inst)
    save(pm, "hcmc", "10_decrescendo_beats", {
        "description": "Piano C4 beats v=120→40 @120BPM, 10s",
        "expected": {
            "episodic_encoding": "FALLING — onset_str × loudness decreases",
        },
        "science": "Decrescendo reduces binding activation over time",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 4: Cross-mechanism Integration (8 stimuli)
# ═══════════════════════════════════════════════════════════════════════

def generate_cross_stimuli() -> None:
    """8 stimuli testing cross-mechanism interactions."""

    # ── 01: Full musical warm — ALL HIGH ─────────────────────────────
    # Strings+flute+organ: warmth + consonance + beats + melody.
    # Should activate all 13 F4 beliefs strongly.
    pm = pretty_midi.PrettyMIDI()
    # Organ chords
    org = pretty_midi.Instrument(program=ORGAN)
    t = 0.0
    for chord, dur in zip(EMOTIONAL_PROG, EMOTIONAL_DURS):
        for p in chord:
            org.notes.append(pretty_midi.Note(
                velocity=60, pitch=p, start=t, end=t + dur,
            ))
        t += dur
    pm.instruments.append(org)
    # Flute melody
    fl = pretty_midi.Instrument(program=FLUTE)
    melody = [E5, D5, C5, E5, F5, E5, D5, C5, D5, C5]
    t = 0.0
    for p, dur in zip(melody, [1.0] * 10):
        fl.notes.append(pretty_midi.Note(
            velocity=85, pitch=p, start=t, end=t + 0.9,
        ))
        t += dur
    pm.instruments.append(fl)
    save(pm, "cross", "01_full_musical_warm", {
        "description": "Flute+organ I-vi-IV-V-I, warm rich texture, 10s",
        "expected": "ALL beliefs HIGH — maximal musical engagement",
        "science": "Reference stimulus: full musical context",
    })

    # ── 02: Full musical harsh — ALL LOW ─────────────────────────────
    # Dense random clusters at forte — no consonance, no warmth.
    rng = np.random.RandomState(46)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    t = 0.0
    for _ in range(20):
        n_notes = int(rng.randint(6, 12))
        pitches = [int(rng.randint(36, 84)) for _ in range(n_notes)]
        for p in pitches:
            inst.notes.append(pretty_midi.Note(
                velocity=110, pitch=p, start=t, end=t + 0.45,
            ))
        t += 0.5
    pm.instruments.append(inst)
    save(pm, "cross", "02_full_harsh_random", {
        "description": "Dense random clusters forte (seed=46), 10s",
        "expected": "ALL beliefs LOW — no warmth, no tonalness, max entropy",
        "science": "Control: maximum musical incoherence",
    })

    # ── 03: Memory buildup — RISING across all beliefs ────────────────
    # Quiet noise (3s) → soft piano (3s) → warm organ chord (4s).
    # Progressive increase in warmth + consonance + tonalness.
    pm = pretty_midi.PrettyMIDI()
    # Phase 1: sparse random (noise-like)
    rng = np.random.RandomState(47)
    inst1 = pretty_midi.Instrument(program=PIANO)
    for i in range(6):
        p = int(rng.randint(48, 84))
        t = i * 0.5
        inst1.notes.append(pretty_midi.Note(
            velocity=40, pitch=p, start=t, end=t + 0.3,
        ))
    pm.instruments.append(inst1)
    # Phase 2: soft piano tonal
    inst2 = pretty_midi.Instrument(program=PIANO)
    for i, p in enumerate(diatonic_scale(C4, 6)):
        t = 3.0 + i * 0.5
        inst2.notes.append(pretty_midi.Note(
            velocity=60, pitch=p, start=t, end=t + 0.45,
        ))
    pm.instruments.append(inst2)
    # Phase 3: warm organ chord
    inst3 = pretty_midi.Instrument(program=ORGAN)
    for p in major_triad(C3) + major_triad(C4):
        inst3.notes.append(pretty_midi.Note(
            velocity=75, pitch=p, start=6.0, end=10.0,
        ))
    pm.instruments.append(inst3)
    save(pm, "cross", "03_memory_buildup", {
        "description": "Random (3s) → piano melody (3s) → organ chord (4s), 10s",
        "expected": "ALL beliefs RISING — progressive warmth/consonance increase",
        "science": "Progressive musical structure accumulates memory activation",
    })

    # ── 04: Memory decay — FALLING across all beliefs ─────────────────
    # Warm organ chord (4s) → soft piano (3s) → sparse random (3s).
    pm = pretty_midi.PrettyMIDI()
    # Phase 1: warm organ
    inst1 = pretty_midi.Instrument(program=ORGAN)
    for p in major_triad(C3) + major_triad(C4):
        inst1.notes.append(pretty_midi.Note(
            velocity=75, pitch=p, start=0.0, end=4.0,
        ))
    pm.instruments.append(inst1)
    # Phase 2: piano melody
    inst2 = pretty_midi.Instrument(program=PIANO)
    for i, p in enumerate(diatonic_scale(C4, 6)):
        t = 4.0 + i * 0.5
        inst2.notes.append(pretty_midi.Note(
            velocity=60, pitch=p, start=t, end=t + 0.45,
        ))
    pm.instruments.append(inst2)
    # Phase 3: sparse random
    rng = np.random.RandomState(48)
    inst3 = pretty_midi.Instrument(program=PIANO)
    for i in range(6):
        p = int(rng.randint(48, 84))
        t = 7.0 + i * 0.5
        inst3.notes.append(pretty_midi.Note(
            velocity=40, pitch=p, start=t, end=t + 0.3,
        ))
    pm.instruments.append(inst3)
    save(pm, "cross", "04_memory_decay", {
        "description": "Organ chord (4s) → piano melody (3s) → random (3s), 10s",
        "expected": "ALL beliefs FALLING — progressive musical structure loss",
        "science": "Musical incoherence dissolves memory activation",
    })

    # ── 05: Boundary → Consolidation ─────────────────────────────────
    # Key change (high boundary) then sustained tonal (high consolidation).
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    # Boundary: rapid key changes (3s)
    t = 0.0
    Ab3 = 56
    for root in [C4, Ab3, E4]:
        for p in major_triad(root):
            inst.notes.append(pretty_midi.Note(
                velocity=90, pitch=p, start=t, end=t + 0.9,
            ))
        t += 1.0
    # Consolidation: sustained tonal (7s)
    inst2 = pretty_midi.Instrument(program=ORGAN)
    for p in major_triad(C4):
        inst2.notes.append(pretty_midi.Note(
            velocity=70, pitch=p, start=3.0, end=10.0,
        ))
    pm.instruments.append(inst)
    pm.instruments.append(inst2)
    save(pm, "cross", "05_boundary_then_consolidation", {
        "description": "Rapid key changes (3s) → sustained organ C major (7s)",
        "expected": {
            "episodic_boundary": "HIGH first 3s, LOW after",
            "consolidation_strength": "LOW first 3s, HIGH after (tonal coherence)",
        },
        "science": "Boundary triggers encoding; consolidation follows stability",
    })

    # ── 06: Warm → Cold timbre — nostalgia contrast ──────────────────
    # Organ (warm, 5s) → Trumpet (bright, 5s), same pitch.
    pm = pretty_midi.PrettyMIDI()
    inst1 = pretty_midi.Instrument(program=ORGAN)
    for p in major_triad(C4):
        inst1.notes.append(pretty_midi.Note(
            velocity=70, pitch=p, start=0.0, end=5.0,
        ))
    pm.instruments.append(inst1)
    inst2 = pretty_midi.Instrument(program=TRUMPET)
    for p in major_triad(C4):
        inst2.notes.append(pretty_midi.Note(
            velocity=85, pitch=p, start=5.0, end=10.0,
        ))
    pm.instruments.append(inst2)
    save(pm, "cross", "06_warm_to_cold_timbre", {
        "description": "Organ C major (5s) → Trumpet C major (5s)",
        "expected": {
            "nostalgia_intensity": "FALLING — warmth drops at timbre change",
            "autobiographical_retrieval": "Variable — consonance maintained",
        },
        "science": "Timbre warmth modulates nostalgia independently of harmony",
    })

    # ── 07: Silent reference ─────────────────────────────────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(pretty_midi.Note(
        velocity=1, pitch=60, start=0.0, end=0.01,
    ))
    pm.instruments.append(inst)
    save(pm, "cross", "07_silence_reference", {
        "description": "Near-silence (tick), baseline reference",
        "expected": "ALL beliefs at BASELINE — minimal R³ activation",
        "science": "Control: establishes zero-input baseline for all beliefs",
    })

    # ── 08: Maximum complexity orchestral ─────────────────────────────
    # Flute + Organ + Piano + Strings — layered texture.
    pm = pretty_midi.PrettyMIDI()
    # Organ pad
    org = pretty_midi.Instrument(program=ORGAN)
    for p in major_triad(C3):
        org.notes.append(pretty_midi.Note(
            velocity=55, pitch=p, start=0.0, end=10.0,
        ))
    pm.instruments.append(org)
    # Strings
    strs = pretty_midi.Instrument(program=STRINGS)
    for p in major_triad(C4):
        strs.notes.append(pretty_midi.Note(
            velocity=60, pitch=p, start=0.0, end=10.0,
        ))
    pm.instruments.append(strs)
    # Piano melody
    pno = pretty_midi.Instrument(program=PIANO)
    melody = [C5, D5, E5, G5, E5, D5, C5, E5, D5, C5,
              C5, D5, E5, G5, E5, D5, C5, E5, D5, C5]
    t = 0.0
    for p in melody:
        pno.notes.append(pretty_midi.Note(
            velocity=75, pitch=p, start=t, end=t + 0.45,
        ))
        t += 0.5
    pm.instruments.append(pno)
    # Flute counter-melody
    fl = pretty_midi.Instrument(program=FLUTE)
    counter = [G5, F5, E5, D5, E5, F5, G5, E5, F5, G5]
    t = 0.0
    for p in counter:
        fl.notes.append(pretty_midi.Note(
            velocity=80, pitch=p, start=t, end=t + 0.9,
        ))
        t += 1.0
    pm.instruments.append(fl)
    save(pm, "cross", "08_orchestral_maximum", {
        "description": "4-instrument layered texture (organ+strings+piano+flute), 10s",
        "expected": "ALL beliefs HIGH — rich, warm, consonant, rhythmic, melodic",
        "science": "Stress test: maximum musical complexity for F4 system",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 5: Boundary Conditions (5 stimuli)
# ═══════════════════════════════════════════════════════════════════════

def generate_boundary_stimuli() -> None:
    """5 edge-case stimuli to validate robustness."""

    # ── 01: Silence ──────────────────────────────────────────────────
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(pretty_midi.Note(
        velocity=1, pitch=60, start=0.0, end=0.01,
    ))
    pm.instruments.append(inst)
    save(pm, "boundary", "01_silence", {
        "description": "Near-silence 5s — no NaN/Inf expected",
        "expected": "All beliefs valid, near baseline",
    })

    # ── 02: Single note sustained ────────────────────────────────────
    pm = _pm_note(C4, 5.0, program=PIANO, velocity=80)
    save(pm, "boundary", "02_single_note", {
        "description": "Single C4 piano 5s — minimal complexity",
        "expected": "All beliefs valid, low boundary, moderate encoding",
    })

    # ── 03: Extreme fast 600 BPM ────────────────────────────────────
    pm = _pm_isochronous(C4, 600.0, 50, program=PIANO, velocity=80)
    save(pm, "boundary", "03_extreme_fast", {
        "description": "C4 @600BPM (100ms IOI), 50 beats — below perception",
        "expected": "All beliefs valid, encoding may saturate",
    })

    # ── 04: Extreme slow 20 BPM ─────────────────────────────────────
    pm = _pm_isochronous(C4, 20.0, 4, program=PIANO, velocity=80)
    save(pm, "boundary", "04_extreme_slow", {
        "description": "C4 @20BPM (3s IOI), 4 beats — above integration window",
        "expected": "All beliefs valid, low boundary, sparse encoding",
    })

    # ── 05: 12-note cluster sustained ────────────────────────────────
    pm = _pm_chord(chromatic_cluster(C4, 12), 5.0, program=PIANO, velocity=100)
    save(pm, "boundary", "05_full_cluster", {
        "description": "12-note chromatic cluster sustained 5s — max inharmonicity",
        "expected": "All beliefs valid, low retrieval/nostalgia/preservation",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 6: PNH — Pythagorean Neural Hierarchy (6 stimuli)
#
# Tests beliefs indirectly through F4 pipeline: PNH feeds PMIM, OII,
# MSPBA, DMMS, CSSL — these are Depth 1/2 mechanisms.
# PNH itself doesn't have dedicated beliefs but provides ratio_complexity,
# conflict_monitoring, expertise_modulation to downstream.
#
# We test the F4 beliefs' response to consonance hierarchies.
# ═══════════════════════════════════════════════════════════════════════

def generate_pnh_stimuli() -> None:
    """6 stimuli testing F4 belief responses across consonance hierarchy."""

    # ── 01: Unison (P1) — maximum consonance ────────────────────────
    pm = _pm_chord([C4, C4], 6.0, program=PIANO, velocity=80)
    save(pm, "pnh", "01_unison_c4", {
        "description": "Piano unison C4+C4, 6s — maximum ratio simplicity (1:1)",
        "expected": {
            "autobiographical_retrieval": "HIGH — max stumpf_fusion",
            "consolidation_strength": "HIGH — max harmonicity",
        },
        "science": "Bidelman 2009: FFR follows Pythagorean hierarchy (r>=0.81)",
    })

    # ── 02: Perfect fifth (P5) — high consonance ────────────────────
    pm = _pm_chord([C4, G4], 6.0, program=PIANO, velocity=80)
    save(pm, "pnh", "02_fifth_c4g4", {
        "description": "Piano P5 (C4+G4), 6s — 3:2 ratio",
        "expected": "HIGH but < unison for retrieval/consolidation",
        "science": "Bidelman 2009: P5 second in FFR hierarchy",
    })

    # ── 03: Perfect fourth (P4) ─────────────────────────────────────
    pm = _pm_chord([C4, F4], 6.0, program=PIANO, velocity=80)
    save(pm, "pnh", "03_fourth_c4f4", {
        "description": "Piano P4 (C4+F4), 6s — 4:3 ratio",
        "expected": "MODERATE-HIGH for retrieval/consolidation",
        "science": "Bidelman 2009: P4 third in FFR hierarchy",
    })

    # ── 04: Tritone (TT) — maximum dissonance for simple ratio ──────
    pm = _pm_chord([C4, Gb4], 6.0, program=PIANO, velocity=80)
    save(pm, "pnh", "04_tritone_c4gb4", {
        "description": "Piano TT (C4+Gb4), 6s — 45:32 ratio",
        "expected": "LOW for retrieval/consolidation",
        "science": "Bidelman 2009: TT lowest in FFR hierarchy",
    })

    # ── 05: Minor second (m2) — maximum roughness ───────────────────
    pm = _pm_chord([C4, Db4], 6.0, program=PIANO, velocity=80)
    save(pm, "pnh", "05_minor_second_c4db4", {
        "description": "Piano m2 (C4+Db4), 6s — max roughness",
        "expected": "LOWEST for retrieval (roughness + inharmonicity penalty)",
        "science": "Plomp-Levelt 1965: m2 within critical bandwidth = max roughness",
    })

    # ── 06: Major third (M3) ────────────────────────────────────────
    pm = _pm_chord([C4, E4], 6.0, program=PIANO, velocity=80)
    save(pm, "pnh", "06_major_third_c4e4", {
        "description": "Piano M3 (C4+E4), 6s — 5:4 ratio",
        "expected": "MODERATE for retrieval/consolidation",
        "science": "Bidelman 2009: M3 intermediate in FFR hierarchy",
    })


# ═══════════════════════════════════════════════════════════════════════
# Metadata & Catalog Writers
# ═══════════════════════════════════════════════════════════════════════

def write_metadata() -> None:
    """Write ground-truth metadata JSON."""
    meta_path = OUTPUT_DIR / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(ALL_METADATA, f, indent=2, ensure_ascii=False)
    print(f"  Metadata → {meta_path}")


def write_catalog() -> None:
    """Write STIMULUS-CATALOG.md with ordinal comparisons."""
    cat_path = OUTPUT_DIR / "STIMULUS-CATALOG.md"

    comparisons = [
        # MEAMN — autobiographical_retrieval
        ("meamn/01", "meamn/04", "autobiographical_retrieval", "A>B",
         "Janata 2009: warm+consonant > harsh cluster for retrieval"),
        ("meamn/01", "meamn/05", "autobiographical_retrieval", "A>B",
         "Organ chord > silence for retrieval activation"),
        ("meamn/12", "meamn/04", "autobiographical_retrieval", "A>B",
         "Sakakibara 2025: choir warmth > cluster for retrieval"),
        ("meamn/02", "meamn/05", "autobiographical_retrieval", "A>B",
         "Strings melody > silence for retrieval"),
        # MEAMN — nostalgia_intensity
        ("meamn/12", "meamn/01", "nostalgia_intensity", "A>B",
         "Choir > organ for nostalgia (vocal warmth, Sakakibara 2025)"),
        ("meamn/01", "meamn/03", "nostalgia_intensity", "A>B",
         "Organ > piano for nostalgia (warmth difference)"),
        ("meamn/01", "meamn/04", "nostalgia_intensity", "A>B",
         "Organ chord > cluster for nostalgia"),
        # MEAMN — emotional_coloring
        ("meamn/08", "meamn/09", "emotional_coloring", "A>B",
         "Loud consonant > quiet dissonant for emotional coloring"),
        ("meamn/08", "meamn/05", "emotional_coloring", "A>B",
         "Forte chord > silence for emotional coloring"),
        ("meamn/11", "meamn/04", "emotional_coloring", "A>B",
         "Rich flute+organ > harsh cluster for emotional coloring"),
        # MMP — melodic_recognition
        ("mmp/01", "mmp/04", "melodic_recognition", "A>B",
         "Jacobsen 2015: tonal melody > chromatic wandering"),
        ("mmp/07", "mmp/05", "melodic_recognition", "A>B",
         "Flute melody > dense random for recognition"),
        ("mmp/01", "mmp/05", "melodic_recognition", "A>B",
         "Piano melody > noise-like for recognition"),
        # MMP — memory_preservation
        ("mmp/02", "mmp/05", "memory_preservation", "A>B",
         "Organ drone > noise for cortical preservation"),
        ("mmp/03", "mmp/05", "memory_preservation", "A>B",
         "Violin sustained > noise for preservation"),
        # HCMC — episodic_encoding
        ("hcmc/01", "hcmc/02", "episodic_encoding", "A>B",
         "Fernandez-Rubio 2022: strong beats > quiet sustained for binding"),
        ("hcmc/05", "hcmc/04", "episodic_encoding", "A>B",
         "Rapid key changes > smooth drone for encoding (onset density)"),
        # HCMC — episodic_boundary
        ("hcmc/03", "hcmc/04", "episodic_boundary", "A>B",
         "Zacks 2007: abrupt transitions > smooth drone for boundary"),
        ("hcmc/05", "hcmc/04", "episodic_boundary", "A>B",
         "Rapid key changes > smooth drone for boundary"),
        ("hcmc/05", "hcmc/06", "episodic_boundary", "A>B",
         "Key changes > tonal repetition for boundary detection"),
        # HCMC — consolidation_strength
        ("hcmc/06", "hcmc/07", "consolidation_strength", "A>B",
         "Sikka 2015: tonal repetition > entropy chaos for consolidation"),
        ("hcmc/04", "hcmc/07", "consolidation_strength", "A>B",
         "Smooth organ drone > entropy chaos for consolidation"),
        # Cross-mechanism
        ("cross/01", "cross/02", "autobiographical_retrieval", "A>B",
         "Full warm musical > harsh random for all F4 beliefs"),
        ("cross/01", "cross/02", "nostalgia_intensity", "A>B",
         "Full warm musical > harsh random for nostalgia"),
        ("cross/01", "cross/02", "emotional_coloring", "A>B",
         "Full warm musical > harsh random for emotional coloring"),
        ("cross/01", "cross/02", "episodic_encoding", "A>B",
         "Full warm musical > harsh random for encoding"),
        # PNH consonance hierarchy
        ("pnh/01", "pnh/05", "autobiographical_retrieval", "A>B",
         "Bidelman 2009: P1(unison) > m2 for retrieval"),
        ("pnh/02", "pnh/04", "autobiographical_retrieval", "A>B",
         "P5 > TT for retrieval via Pythagorean hierarchy"),
        ("pnh/01", "pnh/04", "consolidation_strength", "A>B",
         "Unison > tritone for consolidation strength"),
    ]

    lines = [
        "# F4 Memory — Stimulus Catalog",
        "",
        f"**Total stimuli:** {len(ALL_METADATA)}",
        f"**Ordinal comparisons:** {len(comparisons)}",
        "",
        "## Ordinal Comparison Matrix",
        "",
        "| # | Stimulus A | Stimulus B | Belief | Direction | Science |",
        "|---|-----------|-----------|--------|-----------|---------|",
    ]
    for i, (a, b, belief, direction, science) in enumerate(comparisons, 1):
        lines.append(f"| {i} | {a} | {b} | {belief} | {direction} | {science} |")

    lines.extend([
        "",
        "## Stimulus Index",
        "",
    ])
    for key, meta in sorted(ALL_METADATA.items()):
        desc = meta.get("description", "")
        dur = meta.get("duration_s", "?")
        lines.append(f"- **{key}** ({dur}s): {desc}")

    with open(cat_path, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"  Catalog → {cat_path}")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating F4 Memory test audio...")
    print()

    print("[1/6] MEAMN — Autobiographical Memory (12 stimuli)")
    generate_meamn_stimuli()
    print(f"  → {sum(1 for k in ALL_METADATA if k.startswith('meamn/'))} files")

    print("[2/6] MMP — Musical Mnemonic Preservation (8 stimuli)")
    generate_mmp_stimuli()
    print(f"  → {sum(1 for k in ALL_METADATA if k.startswith('mmp/'))} files")

    print("[3/6] HCMC — Hippocampal-Cortical Memory Circuit (10 stimuli)")
    generate_hcmc_stimuli()
    print(f"  → {sum(1 for k in ALL_METADATA if k.startswith('hcmc/'))} files")

    print("[4/6] Cross-mechanism Integration (8 stimuli)")
    generate_cross_stimuli()
    print(f"  → {sum(1 for k in ALL_METADATA if k.startswith('cross/'))} files")

    print("[5/6] Boundary Conditions (5 stimuli)")
    generate_boundary_stimuli()
    print(f"  → {sum(1 for k in ALL_METADATA if k.startswith('boundary/'))} files")

    print("[6/6] PNH — Consonance Hierarchy (6 stimuli)")
    generate_pnh_stimuli()
    print(f"  → {sum(1 for k in ALL_METADATA if k.startswith('pnh/'))} files")

    print()
    print(f"Total: {len(ALL_METADATA)} stimuli")
    write_metadata()
    write_catalog()
    print()
    print("Done.")


if __name__ == "__main__":
    main()
