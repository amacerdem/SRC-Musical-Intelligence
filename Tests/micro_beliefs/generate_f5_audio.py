"""Deterministic MIDI-based test audio generator for F5 (Emotion Systems).

Generates ~55 stimuli across 5 categories for testing all 14 F5 beliefs:
  - VMM  (6): perceived_happy, perceived_sad, mode_detection,
              emotion_certainty, happy_pathway, sad_pathway
  - AAC  (4+1): emotional_arousal, chills_intensity, ans_dominance,
                 driving_signal
  - NEMAC (4): nostalgia_affect, self_referential_nostalgia,
               wellbeing_enhancement, nostalgia_peak_pred

Scientific basis:
  - VMM:   Pallesen 2005 (major=happy, fMRI N=16),
           Koelsch 2013 (mode detection review), Fritz 2009 (cross-cultural N=40)
  - AAC:   Salimpoor 2011 (chills+DA, PET N=217),
           Gomez 2007 (ANS coupling N=24), Rickard 2004 (arousal N=60)
  - NEMAC: Barrett 2010 (nostalgia→wellbeing N=172),
           Janata 2007 (MEAM N=13), Sakakibara 2025 (EEG N=33)

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
    PIANO, ORGAN, STRINGS, FLUTE, CELLO, CHOIR,
    major_triad, minor_triad, chromatic_cluster, diatonic_scale,
    C3, D3, E3, F3, G3, A3, B3,
    C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4,
    C5, D5, E5, F5, G5,
    C6,
)

OUTPUT_DIR = _PROJECT_ROOT / "Test-Audio" / "micro_beliefs" / "f5"
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


def _pm_crescendo(pitch: int, n_beats: int, ioi: float,
                  v_start: int = 20, v_end: int = 120,
                  program: int = PIANO) -> pretty_midi.PrettyMIDI:
    """Crescendo: velocity ramps from v_start to v_end."""
    note_dur = ioi * 0.85
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=program)
    for i in range(n_beats):
        v = int(v_start + (v_end - v_start) * i / max(n_beats - 1, 1))
        t = i * ioi
        inst.notes.append(pretty_midi.Note(
            velocity=v, pitch=pitch,
            start=t, end=t + note_dur,
        ))
    pm.instruments.append(inst)
    return pm


def _pm_near_silence(duration: float = 5.0) -> pretty_midi.PrettyMIDI:
    """Near-silence: single MIDI tick at v=1."""
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    inst.notes.append(pretty_midi.Note(
        velocity=1, pitch=60, start=0.0, end=0.01,
    ))
    pm.instruments.append(inst)
    return pm


def _pm_dense_random(duration: float = 5.0, seed: int = 50,
                     notes_per_sec: int = 16) -> pretty_midi.PrettyMIDI:
    """Dense random MIDI — noise-like, no tonal structure."""
    rng = np.random.RandomState(seed)
    n_notes = int(duration * notes_per_sec)
    pm = pretty_midi.PrettyMIDI()
    inst = pretty_midi.Instrument(program=PIANO)
    for i in range(n_notes):
        p = int(rng.randint(36, 84))
        t = i * (duration / n_notes)
        inst.notes.append(pretty_midi.Note(
            velocity=int(rng.randint(40, 120)),
            pitch=p, start=t, end=t + 0.04,
        ))
    pm.instruments.append(inst)
    return pm


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 1: VMM — Valence-Mode Matching (14 stimuli)
#
# Tests: perceived_happy, perceived_sad, mode_detection,
#        emotion_certainty, happy_pathway, sad_pathway
#
# Mechanism: VMM (12D relay, Phase 0b)
# Key R³: consonance[4], warmth[12], tonalness[14], smoothness[16],
#          tristimulus[18:21]
# Key H³: consonance/warmth/tonalness at H19-H22 (macro scales)
# ═══════════════════════════════════════════════════════════════════════

def generate_vmm_stimuli() -> None:
    """14 stimuli targeting VMM relay and its 6 beliefs."""

    # ── 01: Piano C major triad — HIGH perceived_happy ──────────────
    # Major triad has high consonance → high V1:mode_signal + V2:consonance_valence.
    # Science: Pallesen 2005 — major mode activates reward (N=16)
    pm = _pm_chord(major_triad(C4), 5.0, program=PIANO, velocity=80)
    save(pm, "vmm", "01_piano_major_c4", {
        "description": "Piano C major triad, 5s, v=80",
        "expected": {
            "perceived_happy": "HIGH — major mode + consonance → high V1+V2",
            "perceived_sad": "LOW — inverse of happy",
            "mode_detection": "HIGH — clear harmonic structure",
            "happy_pathway": "HIGH — R0 consonance extraction",
        },
        "science": "Pallesen 2005: major mode → reward activation (fMRI, N=16)",
    })

    # ── 02: Piano C minor triad — HIGH perceived_sad ─────────────────
    # Minor triad: m3 interval → lower consonance → high (1-V1)+(1-V2).
    # Science: Pallesen 2005 — minor mode activates sadness circuits
    pm = _pm_chord(minor_triad(C4), 5.0, program=PIANO, velocity=80)
    save(pm, "vmm", "02_piano_minor_c4", {
        "description": "Piano C minor triad, 5s, v=80",
        "expected": {
            "perceived_happy": "LOW — minor mode → low V1",
            "perceived_sad": "HIGH — minor → high (1-V1)+(1-V2)",
            "mode_detection": "HIGH — harmonic structure present",
            "sad_pathway": "HIGH — R1 sad extraction from low consonance",
        },
        "science": "Pallesen 2005: minor → sadness circuits (fMRI, N=16)",
    })

    # ── 03: Piano 6-note chromatic cluster — LOW happy, HIGH sad ─────
    # Maximal dissonance, low stumpf_fusion, high roughness.
    # Cluster is the reliable floor for VMM beliefs (sigmoid cascade).
    pm = _pm_chord(chromatic_cluster(C4, 6), 5.0, program=PIANO, velocity=80)
    save(pm, "vmm", "03_piano_cluster_6note", {
        "description": "Piano 6-note chromatic cluster C4, 5s, v=80",
        "expected": {
            "perceived_happy": "LOWEST — max dissonance → min V1+V2",
            "happy_pathway": "LOWEST — min consonance extraction",
            "sad_pathway": "HIGHEST — max dissonance → max R1",
        },
        "science": "Plomp-Levelt 1965: cluster within critical bandwidth = max roughness",
    })

    # ── 04: Piano 4-note chromatic cluster — mode detection floor ────
    # Smaller cluster, still dissonant enough to test mode discrimination.
    pm = _pm_chord(chromatic_cluster(C4, 4), 5.0, program=PIANO, velocity=80)
    save(pm, "vmm", "04_piano_cluster_4note", {
        "description": "Piano 4-note chromatic cluster C4, 5s, v=80",
        "expected": {
            "mode_detection": "LOW — unclear harmonic structure",
            "emotion_certainty": "LOW — ambiguous valence",
        },
        "science": "Chromatic cluster ambiguates mode detection",
    })

    # ── 05: Organ C major triad — HIGH happy (warm) ──────────────────
    # Organ: maximum warmth + clear consonance → highest happy+certainty.
    pm = _pm_chord(major_triad(C4), 5.0, program=ORGAN, velocity=75)
    save(pm, "vmm", "05_organ_major_c4", {
        "description": "Organ C major triad, 5s, v=75",
        "expected": {
            "perceived_happy": "HIGHEST — warmth + consonance synergy",
            "emotion_certainty": "HIGH — clear harmonic → confident valence",
            "happy_pathway": "HIGH — R0 warm + consonant",
        },
        "science": "Fritz 2009: cross-cultural valence recognition (N=40)",
    })

    # ── 06: Organ C major sustained — stability test ─────────────────
    pm = _pm_chord(major_triad(C4), 6.0, program=ORGAN, velocity=70)
    save(pm, "vmm", "06_organ_major_sustained", {
        "description": "Organ C major triad, 6s, v=70 — stability test",
        "expected": {
            "perceived_happy": "STABLE — sustained consonance",
            "mode_detection": "STABLE — constant harmonic content",
        },
        "science": "Tau=0.55 produces stable output for sustained stimuli",
    })

    # ── 07: Organ C minor sustained — sad stability test ─────────────
    pm = _pm_chord(minor_triad(C4), 6.0, program=ORGAN, velocity=70)
    save(pm, "vmm", "07_organ_minor_sustained", {
        "description": "Organ C minor triad, 6s, v=70 — sad stability test",
        "expected": {
            "perceived_sad": "STABLE — sustained minor tonality",
        },
        "science": "Minor organ drone maintains stable sadness signal",
    })

    # ── 08: Piano P5 dyad (C4+G4) — HIGH consonance ─────────────────
    # Perfect fifth: 3:2 ratio → maximum consonance for a dyad.
    pm = _pm_chord([C4, G4], 5.0, program=PIANO, velocity=80)
    save(pm, "vmm", "08_piano_p5_dyad", {
        "description": "Piano P5 dyad (C4+G4), 5s, v=80",
        "expected": {
            "perceived_happy": "HIGH — high consonance → high V2",
        },
        "science": "Bidelman 2009: P5 high in Pythagorean hierarchy (r≥0.81)",
    })

    # ── 09: Piano tritone dyad (C4+F#4) — LOW consonance ────────────
    # Tritone: 45:32 ratio → maximum dissonance for a dyad.
    pm = _pm_chord([C4, Gb4], 5.0, program=PIANO, velocity=80)
    save(pm, "vmm", "09_piano_tritone_dyad", {
        "description": "Piano tritone dyad (C4+Gb4), 5s, v=80",
        "expected": {
            "perceived_happy": "LOW — low consonance → low V2",
            "perceived_sad": "HIGH — dissonant → high (1-V2)",
        },
        "science": "Bidelman 2009: TT lowest in FFR hierarchy",
    })

    # ── 10: Cello dark melody — HIGH perceived_sad ───────────────────
    # Cello: dark timbre + low register → low warmth → high (1-V1).
    # C3 region melody.
    dark_mel = [C3, D3, E3, F3, G3, F3, E3, D3]
    pm = _pm_melody(dark_mel, [0.5] * 8, program=CELLO, velocity=70)
    save(pm, "vmm", "10_cello_dark_melody", {
        "description": "Cello C3 diatonic melody, 0.5s×8, v=70",
        "expected": {
            "perceived_sad": "HIGH — dark timbre + low register",
        },
        "science": "Pallesen 2005: dark timbres enhance sadness perception",
    })

    # ── 11: Flute bright melody — HIGH perceived_happy ───────────────
    # Flute: bright timbre + high register → high warmth → high V1.
    bright_mel = [C5, D5, E5, F5, G5, F5, E5, D5]
    pm = _pm_melody(bright_mel, [0.5] * 8, program=FLUTE, velocity=85)
    save(pm, "vmm", "11_flute_bright_melody", {
        "description": "Flute C5 diatonic melody, 0.5s×8, v=85",
        "expected": {
            "perceived_happy": "HIGH — bright timbre + high register",
        },
        "science": "Fritz 2009: bright timbres → positive valence",
    })

    # ── 12: Organ P5 dyad — HIGH emotion_certainty ──────────────────
    # Organ warmth + perfect fifth → very clear valence signal.
    pm = _pm_chord([C4, G4], 5.0, program=ORGAN, velocity=75)
    save(pm, "vmm", "12_organ_p5_dyad", {
        "description": "Organ P5 dyad (C4+G4), 5s, v=75",
        "expected": {
            "emotion_certainty": "HIGH — warm + consonant = clear valence",
        },
        "science": "Koelsch 2013: harmonic clarity → certainty",
    })

    # ── 13: Noise-like dense random — VMM floor comparison ───────────
    # Dense random MIDI as noise substitute for tests.
    pm = _pm_dense_random(5.0, seed=50)
    save(pm, "vmm", "13_noise_like_random", {
        "description": "Dense random MIDI (noise-like, seed=50), 5s",
        "expected": {
            "perceived_happy": "LOW — no consonance",
            "perceived_sad": "MODERATE — ambiguous dissonance",
            "mode_detection": "LOW — no harmonic structure",
        },
        "science": "Control: maximum incoherence for VMM system",
    })

    # ── 14: Near-silence — baseline ──────────────────────────────────
    pm = _pm_near_silence(5.0)
    save(pm, "vmm", "14_near_silence", {
        "description": "Near-silence (single tick), 5s baseline",
        "expected": {
            "perceived_happy": "BASELINE — minimal R³ activation",
            "perceived_sad": "BASELINE — elevated by sigmoid cascade",
        },
        "science": "Control: zero-input baseline for VMM beliefs",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 2: AAC — Autonomic-Affective Coupling (15 stimuli)
#
# Tests: emotional_arousal, chills_intensity, ans_dominance,
#        driving_signal
#
# Mechanism: AAC (14D relay, Phase 0a)
# Key R³: amplitude[7], loudness[10], onset_strength[11],
#          spectral_flux[21], entropy[22]
# Key H³: amplitude at H9 (350ms micro), onset/flux at H16
# ═══════════════════════════════════════════════════════════════════════

def generate_aac_stimuli() -> None:
    """15 stimuli targeting AAC relay and its 4 beliefs."""

    # ── 01: Piano C major loud — HIGH emotional_arousal ──────────────
    # High amplitude → high E0:emotional_arousal extraction.
    # Science: Rickard 2004 — arousal from amplitude (N=60)
    pm = _pm_chord(major_triad(C4), 5.0, program=PIANO, velocity=120)
    save(pm, "aac", "01_piano_major_loud", {
        "description": "Piano C major triad ff (v=120), 5s",
        "expected": {
            "emotional_arousal": "HIGH — max amplitude → max E0",
        },
        "science": "Rickard 2004: amplitude is primary arousal predictor (N=60)",
    })

    # ── 02: Piano C major quiet — LOW emotional_arousal ──────────────
    # Low amplitude → low E0.
    pm = _pm_chord(major_triad(C4), 5.0, program=PIANO, velocity=30)
    save(pm, "aac", "02_piano_major_quiet", {
        "description": "Piano C major triad pp (v=30), 5s",
        "expected": {
            "emotional_arousal": "LOW — minimal amplitude → low E0",
        },
        "science": "Rickard 2004: low amplitude = low arousal",
    })

    # ── 03: Piano fast isochronous 240 BPM — HIGH onset density ──────
    # 240 BPM = IOI 250ms → very high onset_strength → high E0.
    pm = _pm_isochronous(C4, 240.0, 24, program=PIANO, velocity=80)
    save(pm, "aac", "03_piano_iso_240bpm", {
        "description": "Piano C4 @240BPM, 24 beats (6s), v=80",
        "expected": {
            "emotional_arousal": "HIGH — high onset density → high E0",
        },
        "science": "Gomez 2007: onset density drives arousal (N=24)",
    })

    # ── 04: Piano slow isochronous 60 BPM — LOW onset density ────────
    pm = _pm_isochronous(C4, 60.0, 8, program=PIANO, velocity=80)
    save(pm, "aac", "04_piano_iso_60bpm", {
        "description": "Piano C4 @60BPM, 8 beats (8s), v=80",
        "expected": {
            "emotional_arousal": "LOW — sparse onsets → low E0",
        },
        "science": "Slow tempo reduces onset-driven arousal",
    })

    # ── 05: Piano loud + fast — HIGHEST arousal ──────────────────────
    # Combines maximum amplitude (v=120) with high tempo (180 BPM).
    # E0 = amplitude × onset_strength → maximal activation.
    pm = _pm_isochronous(C4, 180.0, 18, program=PIANO, velocity=120)
    save(pm, "aac", "05_piano_loud_fast", {
        "description": "Piano C4 @180BPM ff (v=120), 18 beats (6s)",
        "expected": {
            "emotional_arousal": "HIGHEST — amplitude + onset density combined",
            "ans_dominance": "HIGH — high energy activates ANS",
        },
        "science": "Rickard 2004: amplitude×tempo interaction for arousal",
    })

    # ── 06: Piano quiet sustained note — LOWEST arousal ──────────────
    # Single quiet note: no onsets after attack, low amplitude.
    pm = _pm_note(C4, 5.0, program=PIANO, velocity=30)
    save(pm, "aac", "06_piano_sustained_quiet", {
        "description": "Piano C4 sustained pp (v=30), 5s",
        "expected": {
            "emotional_arousal": "LOWEST — no onsets + low amplitude",
        },
        "science": "Quiet sustained tone minimizes all arousal pathways",
    })

    # ── 07: Piano crescendo — RISING arousal ─────────────────────────
    # Velocity ramps 20→120 over 16 beats at 0.35s IOI.
    # Science: Salimpoor 2011 — chills at loudness peaks (PET, N=217)
    pm = _pm_crescendo(C4, 16, 0.35, v_start=20, v_end=120, program=PIANO)
    save(pm, "aac", "07_piano_crescendo", {
        "description": "Piano C4 crescendo v=20→120, 16 beats @IOI=0.35s",
        "expected": {
            "emotional_arousal": "RISING — increasing amplitude → rising E0",
            "chills_intensity": "RISING — crescendo apex → chills",
        },
        "science": "Salimpoor 2011: chills peak at expectation violations (N=217)",
    })

    # ── 08: Piano C major mf — chills reference ─────────────────────
    pm = _pm_chord(major_triad(C4), 5.0, program=PIANO, velocity=100)
    save(pm, "aac", "08_piano_major_mf", {
        "description": "Piano C major triad mf (v=100), 5s",
        "expected": {
            "emotional_arousal": "MODERATE-HIGH — mf amplitude",
        },
        "science": "Reference stimulus for moderate arousal level",
    })

    # ── 09: Strings C major — chills timbre ──────────────────────────
    # Strings produce sustained tone good for chills testing.
    pm = _pm_chord(major_triad(C4), 5.0, program=STRINGS, velocity=90)
    save(pm, "aac", "09_strings_major_c4", {
        "description": "Strings C major triad, 5s, v=90",
        "expected": {
            "chills_intensity": "MODERATE — warm sustained timbre",
        },
        "science": "Strings timbre associated with frisson responses",
    })

    # ── 10: Organ sustained — stable chills/arousal ──────────────────
    pm = _pm_chord(major_triad(C4), 6.0, program=ORGAN, velocity=75)
    save(pm, "aac", "10_organ_major_sustained", {
        "description": "Organ C major triad, 6s, v=75 — stability test",
        "expected": {
            "emotional_arousal": "STABLE — sustained input",
            "chills_intensity": "STABLE — no dynamic change",
        },
        "science": "Tau=0.5 produces stable output for sustained input",
    })

    # ── 11: Piano isochronous 180BPM v=110 — HIGH ANS ───────────────
    # Strong beats at high velocity → high E1:ans_response.
    # Science: Gomez 2007 — ANS responds to amplitude × onset density
    pm = _pm_isochronous(C4, 180.0, 18, program=PIANO, velocity=110)
    save(pm, "aac", "11_piano_iso_180bpm_v110", {
        "description": "Piano C4 @180BPM (v=110), 18 beats (6s)",
        "expected": {
            "ans_dominance": "HIGH — loud + fast activates ANS",
        },
        "science": "Gomez 2007: ANS coupling with amplitude×onset (N=24)",
    })

    # ── 12: Piano sustained quiet v=35 — LOW ANS ────────────────────
    pm = _pm_note(C4, 5.0, program=PIANO, velocity=35)
    save(pm, "aac", "12_piano_sustained_v35", {
        "description": "Piano C4 sustained (v=35), 5s — low ANS",
        "expected": {
            "ans_dominance": "LOW — quiet sustained → minimal ANS",
        },
        "science": "Low energy input → low autonomic activation",
    })

    # ── 13: Piano isochronous 120BPM v=85 — driving signal ──────────
    # Regular beats → rhythmic driving force.
    pm = _pm_isochronous(C4, 120.0, 12, program=PIANO, velocity=85)
    save(pm, "aac", "13_piano_iso_120bpm_v85", {
        "description": "Piano C4 @120BPM, 12 beats (6s), v=85",
        "expected": {
            "driving_signal": "HIGH — regular onsets → rhythmic drive",
        },
        "science": "Rhythmic regularity activates driving signal prediction",
    })

    # ── 14: Organ static chord — LOW driving signal ──────────────────
    # Sustained chord: no repeated onsets → no rhythmic drive.
    pm = _pm_chord(major_triad(C4), 5.0, program=ORGAN, velocity=70)
    save(pm, "aac", "14_organ_static_chord", {
        "description": "Organ C major sustained, 5s, v=70 — no rhythm",
        "expected": {
            "driving_signal": "LOW — no onsets after initial attack",
        },
        "science": "Sustained tones produce no rhythmic driving force",
    })

    # ── 15: Piano isochronous 120BPM sustained — driving stable ──────
    pm = _pm_isochronous(C4, 120.0, 16, program=PIANO, velocity=80)
    save(pm, "aac", "15_piano_iso_120bpm_stable", {
        "description": "Piano C4 @120BPM, 16 beats (8s), v=80 — stability",
        "expected": {
            "driving_signal": "STABLE — constant rhythmic input",
        },
        "science": "Steady rhythm maintains stable driving signal",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 3: NEMAC — Nostalgia-Evoked Memory-Affect (10 stimuli)
#
# Tests: nostalgia_affect, self_referential_nostalgia,
#        wellbeing_enhancement, nostalgia_peak_pred
#
# Mechanism: NEMAC (11D relay, Phase 0c, Depth 1)
# Key R³: warmth[12], stumpf_fusion[3], tonalness[14],
#          smoothness[16], roughness[5]
# Key H³: warmth/stumpf at H16/H20, tonalness at H19
# ═══════════════════════════════════════════════════════════════════════

def generate_nemac_stimuli() -> None:
    """10 stimuli targeting NEMAC relay and its 4 beliefs."""

    # ── 01: Organ C major 6s — HIGH nostalgia (warm) ─────────────────
    # Organ: max warmth + stumpf → high W0:nostalgia_intens.
    # Science: Sakakibara 2025 — warm timbres enhance nostalgia (N=33)
    pm = _pm_chord(major_triad(C4), 6.0, program=ORGAN, velocity=70)
    save(pm, "nemac", "01_organ_warm_6s", {
        "description": "Organ C major triad, 6s, v=70 — maximum warmth",
        "expected": {
            "nostalgia_affect": "HIGH — warmth + stumpf → high W0",
            "self_referential_nostalgia": "HIGH — M0:mpfc_activation",
            "wellbeing_enhancement": "HIGH — nostalgia → wellbeing cascade",
        },
        "science": "Sakakibara 2025: warm timbres enhance nostalgia (eta_p^2=0.636)",
    })

    # ── 02: Organ C major 5s — nostalgia stable ─────────────────────
    pm = _pm_chord(major_triad(C4), 5.0, program=ORGAN, velocity=70)
    save(pm, "nemac", "02_organ_warm_5s", {
        "description": "Organ C major triad, 5s, v=70",
        "expected": {
            "nostalgia_affect": "STABLE — sustained warmth",
            "nostalgia_peak_pred": "STABLE — F1:vividness_pred",
        },
        "science": "Tau=0.65 produces stable output for sustained warm input",
    })

    # ── 03: Piano diatonic melody — tonal nostalgia ──────────────────
    # Tonal melody: high tonalness + stumpf → nostalgic.
    # Science: Janata 2007 — familiar tonal space triggers MEAM (N=13)
    melody = diatonic_scale(C4, 8)
    pm = _pm_melody(melody, [0.5] * 8, program=PIANO, velocity=80)
    save(pm, "nemac", "03_piano_diatonic_melody", {
        "description": "Piano C major diatonic scale, 0.5s×8, v=80",
        "expected": {
            "nostalgia_affect": "MODERATE — tonal but not warm timbre",
        },
        "science": "Janata 2007: tonal familiarity triggers autobiographical memory",
    })

    # ── 04: Strings melody C5 slow — HIGH nostalgia ──────────────────
    # Strings: warm timbre + slow melody → maximum nostalgia affect.
    melody = [C5, D5, E5, F5, G5, F5, E5, D5]
    pm = _pm_melody(melody, [0.75] * 8, program=STRINGS, velocity=70)
    save(pm, "nemac", "04_strings_melody_slow", {
        "description": "Strings C5 diatonic melody, 0.75s×8, v=70",
        "expected": {
            "nostalgia_affect": "HIGH — warm strings timbre",
        },
        "science": "Sakakibara 2025: strings among warmest timbres for nostalgia",
    })

    # ── 05: Flute diatonic melody — nostalgia peak pred ──────────────
    # Clear tone → F1:vividness_pred test.
    melody = diatonic_scale(C4, 8)
    pm = _pm_melody(melody, [0.5] * 8, program=FLUTE, velocity=85)
    save(pm, "nemac", "05_flute_diatonic_melody", {
        "description": "Flute C4 diatonic melody, 0.5s×8, v=85",
        "expected": {
            "nostalgia_peak_pred": "MODERATE — clear tonal structure",
        },
        "science": "Flute: near-sinusoidal → clear tonalness",
    })

    # ── 06: Piano 6-note cluster — LOW nostalgia ────────────────────
    # Cluster: low stumpf, high roughness → minimal nostalgia.
    # Cluster is the reliable floor for NEMAC (sigmoid cascade).
    pm = _pm_chord(chromatic_cluster(C4, 6), 5.0, program=PIANO, velocity=80)
    save(pm, "nemac", "06_piano_cluster_6note", {
        "description": "Piano 6-note chromatic cluster C4, 5s, v=80",
        "expected": {
            "nostalgia_affect": "LOWEST — max roughness, min stumpf",
            "self_referential_nostalgia": "LOW — no warmth signal",
            "wellbeing_enhancement": "LOW — no nostalgia → no wellbeing",
        },
        "science": "Dissonant cluster inhibits all nostalgia pathways",
    })

    # ── 07: Dense random MIDI (noise-like) — LOW nostalgia ───────────
    pm = _pm_dense_random(6.0, seed=51)
    save(pm, "nemac", "07_noise_like_random", {
        "description": "Dense random MIDI (noise-like, seed=51), 6s",
        "expected": {
            "nostalgia_affect": "LOW — no warmth, no stumpf",
            "wellbeing_enhancement": "LOW — no nostalgia cascade",
        },
        "science": "Control: noise-like input for NEMAC floor",
    })

    # ── 08: Near-silence — BASELINE ──────────────────────────────────
    pm = _pm_near_silence(5.0)
    save(pm, "nemac", "08_near_silence", {
        "description": "Near-silence (single tick), 5s baseline",
        "expected": {
            "nostalgia_affect": "BASELINE — elevated by sigmoid cascade",
            "nostalgia_peak_pred": "BASELINE — regresses toward prior",
        },
        "science": "Control: zero-input baseline for NEMAC beliefs",
    })

    # ── 09: Organ range test 4s ──────────────────────────────────────
    pm = _pm_chord(major_triad(C4), 4.0, program=ORGAN, velocity=70)
    save(pm, "nemac", "09_organ_range_4s", {
        "description": "Organ C major, 4s, v=70 — range test stimulus",
        "expected": {
            "nostalgia_affect": "IN_RANGE [0,1]",
        },
        "science": "Range validation stimulus",
    })

    # ── 10: Noise-like 4s range test ─────────────────────────────────
    pm = _pm_dense_random(4.0, seed=52)
    save(pm, "nemac", "10_noise_range_4s", {
        "description": "Dense random MIDI (seed=52), 4s — range test",
        "expected": {
            "nostalgia_affect": "IN_RANGE [0,1]",
        },
        "science": "Range validation stimulus",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 4: Cross-unit Integration (8 stimuli)
# ═══════════════════════════════════════════════════════════════════════

def generate_cross_stimuli() -> None:
    """8 stimuli testing cross-unit interactions (VMM×AAC×NEMAC)."""

    # ── 01: Piano major loud — happy + aroused ───────────────────────
    # Loud major chord activates both VMM (happy) and AAC (aroused).
    pm = _pm_chord(major_triad(C4), 5.0, program=PIANO, velocity=120)
    save(pm, "cross", "01_piano_major_loud", {
        "description": "Piano C major ff (v=120), 5s — happy + aroused",
        "expected": {
            "perceived_happy": "HIGH — major + consonance",
            "emotional_arousal": "HIGH — loud amplitude",
        },
        "science": "VMM×AAC interaction: valence and arousal co-activation",
    })

    # ── 02: Piano major quiet — happy but calm ───────────────────────
    pm = _pm_chord(major_triad(C4), 5.0, program=PIANO, velocity=30)
    save(pm, "cross", "02_piano_major_quiet", {
        "description": "Piano C major pp (v=30), 5s — happy but calm",
        "expected": {
            "perceived_happy": "MODERATE — consonance preserved",
            "emotional_arousal": "LOW — minimal amplitude",
        },
        "science": "Dissociation of valence (VMM) from arousal (AAC)",
    })

    # ── 03: Piano fast major melody — happy + aroused ────────────────
    # Fast diatonic melody activates both positive valence and arousal.
    melody = diatonic_scale(C4, 8)
    pm = _pm_melody(melody, [0.3] * 8, program=PIANO, velocity=100)
    save(pm, "cross", "03_fast_major_melody", {
        "description": "Piano C major fast melody (0.3s×8), v=100",
        "expected": {
            "perceived_happy": "HIGH — tonal + consonant",
            "emotional_arousal": "HIGH — fast onsets + loud",
        },
        "science": "Fast bright music activates both VMM and AAC",
    })

    # ── 04: Cello slow minor melody — sad + nostalgic ────────────────
    # Dark timbre + minor mode activates sadness and nostalgia.
    min_notes = [C4, C4 + 2, C4 + 3, C4 + 5, C4 + 7,
                 C4 + 8, C4 + 10, C4 + 12]
    pm = _pm_melody(min_notes, [0.8] * 8, program=CELLO, velocity=60)
    save(pm, "cross", "04_cello_slow_minor", {
        "description": "Cello C minor scale, 0.8s×8, v=60",
        "expected": {
            "perceived_sad": "HIGH — minor + dark timbre",
            "nostalgia_affect": "MODERATE-HIGH — warm cello timbre",
        },
        "science": "VMM×NEMAC: sadness and nostalgia co-activation",
    })

    # ── 05: Piano crescendo — chills + arousal ───────────────────────
    # Crescendo activates both chills (I0) and arousal (E0).
    # Science: Salimpoor 2011 — chills at crescendo apex
    pm = _pm_crescendo(C4, 16, 0.35, v_start=20, v_end=120, program=PIANO)
    save(pm, "cross", "05_piano_crescendo", {
        "description": "Piano C4 crescendo v=20→120, 16 beats",
        "expected": {
            "chills_intensity": "RISING — crescendo apex → frisson",
            "emotional_arousal": "RISING — increasing amplitude",
        },
        "science": "Salimpoor 2011: chills at loudness peaks (PET, N=217)",
    })

    # ── 06: Piano note quiet — low chills/arousal baseline ───────────
    pm = _pm_note(C4, 5.0, program=PIANO, velocity=40)
    save(pm, "cross", "06_piano_note_quiet", {
        "description": "Piano C4 sustained (v=40), 5s — low arousal baseline",
        "expected": {
            "chills_intensity": "LOW — no dynamic change",
            "emotional_arousal": "LOW — quiet + sustained",
        },
        "science": "Control for crescendo comparison",
    })

    # ── 07: Organ warm — nostalgia + wellbeing ───────────────────────
    # Warm organ activates NEMAC nostalgia and wellbeing pathways.
    pm = _pm_chord(major_triad(C4), 5.0, program=ORGAN, velocity=70)
    save(pm, "cross", "07_organ_warm", {
        "description": "Organ C major, 5s, v=70 — nostalgia + wellbeing",
        "expected": {
            "nostalgia_affect": "HIGH — warm + consonant",
            "wellbeing_enhancement": "HIGH — nostalgia cascade",
        },
        "science": "Barrett 2010: nostalgia → wellbeing pathway (N=172)",
    })

    # ── 08: Organ major — mode + certainty ───────────────────────────
    pm = _pm_chord(major_triad(C4), 5.0, program=ORGAN, velocity=75)
    save(pm, "cross", "08_organ_mode_certainty", {
        "description": "Organ C major, 5s, v=75 — clear mode + certainty",
        "expected": {
            "mode_detection": "VALID — in-range, stable output",
            "emotion_certainty": "VALID — in-range, stable output",
        },
        "science": "Koelsch 2013: clear harmonic → mode detection + certainty",
    })


# ═══════════════════════════════════════════════════════════════════════
# CATEGORY 5: Boundary Conditions (7 stimuli)
# ═══════════════════════════════════════════════════════════════════════

def generate_boundary_stimuli() -> None:
    """7 edge-case stimuli to validate robustness for all 14 F5 beliefs."""

    # ── 01: Near-silence 2s ──────────────────────────────────────────
    pm = _pm_near_silence(2.0)
    save(pm, "boundary", "01_silence_2s", {
        "description": "Near-silence 2s — no NaN/Inf expected",
        "expected": "All 14 F5 beliefs valid, near baseline",
    })

    # ── 02: DC-like constant — single very quiet note ────────────────
    pm = _pm_note(C4, 2.0, program=ORGAN, velocity=5)
    save(pm, "boundary", "02_dc_like_quiet", {
        "description": "Organ C4 near-silence (v=5), 2s — DC-like",
        "expected": "All beliefs valid, low activation",
    })

    # ── 03: Very short 0.1s ──────────────────────────────────────────
    pm = _pm_chord(major_triad(C4), 0.1, program=PIANO, velocity=80)
    save(pm, "boundary", "03_very_short", {
        "description": "Piano C major 0.1s — minimal duration",
        "expected": "All beliefs valid, pipeline handles short input",
    })

    # ── 04: Very long 10s ────────────────────────────────────────────
    pm = _pm_chord(major_triad(C4), 10.0, program=ORGAN, velocity=70)
    save(pm, "boundary", "04_very_long", {
        "description": "Organ C major 10s — extended duration",
        "expected": "All beliefs valid, no memory overflow",
    })

    # ── 05: Maximum velocity ─────────────────────────────────────────
    pm = _pm_chord(major_triad(C4), 2.0, program=PIANO, velocity=127)
    save(pm, "boundary", "05_max_velocity", {
        "description": "Piano C major fff (v=127), 2s — maximum energy",
        "expected": "All beliefs valid, arousal near ceiling",
    })

    # ── 06: Minimum velocity ─────────────────────────────────────────
    pm = _pm_note(C4, 2.0, program=PIANO, velocity=5)
    save(pm, "boundary", "06_min_velocity", {
        "description": "Piano C4 ppp (v=5), 2s — near-zero energy",
        "expected": "All beliefs valid, near baseline",
    })

    # ── 07: Full 12-note cluster ─────────────────────────────────────
    pm = _pm_chord(chromatic_cluster(C4, 12), 5.0, program=PIANO, velocity=100)
    save(pm, "boundary", "07_full_cluster_12note", {
        "description": "12-note chromatic cluster C4-B4 forte, 5s",
        "expected": "All beliefs valid, max inharmonicity",
    })


# ═══════════════════════════════════════════════════════════════════════
# Metadata & Catalog Writers
# ═══════════════════════════════════════════════════════════════════════

def write_metadata() -> None:
    """Write ground-truth metadata JSON."""
    meta_path = OUTPUT_DIR / "metadata.json"
    with open(meta_path, "w") as f:
        json.dump(ALL_METADATA, f, indent=2, ensure_ascii=False)
    print(f"  Metadata -> {meta_path}")


def write_catalog() -> None:
    """Write STIMULUS-CATALOG.md with ordinal comparisons."""
    cat_path = OUTPUT_DIR / "STIMULUS-CATALOG.md"

    comparisons = [
        # VMM — perceived_happy
        ("vmm/01", "vmm/02", "perceived_happy", "A>B",
         "Pallesen 2005: major > minor for happiness (fMRI, N=16)"),
        ("vmm/01", "vmm/03", "perceived_happy", "A>B",
         "Major triad > 6-note cluster for happiness"),
        ("vmm/05", "vmm/03", "perceived_happy", "A>B",
         "Organ major (warm) > cluster for happiness"),
        ("vmm/08", "vmm/09", "perceived_happy", "A>B",
         "P5 dyad > tritone for happiness (consonance drives V2)"),
        # VMM — perceived_sad
        ("vmm/02", "vmm/01", "perceived_sad", "A>B",
         "Pallesen 2005: minor > major for sadness (fMRI, N=16)"),
        ("vmm/10", "vmm/11", "perceived_sad", "A>B",
         "Cello dark melody > flute bright melody for sadness"),
        ("vmm/02", "vmm/13", "perceived_sad", "A>B",
         "Minor chord > noise for sadness"),
        # VMM — mode_detection
        ("vmm/01", "vmm/13", "mode_detection", "A>B",
         "Koelsch 2013: harmonic structure > noise for mode detection"),
        ("vmm/01", "vmm/04", "mode_detection", "A>B",
         "Major triad > 4-note cluster for mode detection"),
        # VMM — happy_pathway
        ("vmm/01", "vmm/02", "happy_pathway", "A>B",
         "Major > minor for R0 happy extraction"),
        ("vmm/01", "vmm/03", "happy_pathway", "A>B",
         "Major chord > cluster for R0 happy extraction"),
        ("vmm/05", "vmm/03", "happy_pathway", "A>B",
         "Organ major > cluster for R0 extraction"),
        # VMM — sad_pathway
        ("vmm/03", "vmm/01", "sad_pathway", "A>B",
         "Cluster > major chord for R1 sad extraction"),
        ("vmm/03", "vmm/13", "sad_pathway", "A>B",
         "Cluster > noise for sad pathway"),
        # VMM — emotion_certainty
        ("vmm/12", "vmm/13", "emotion_certainty", "A>B",
         "Organ P5 > noise for emotion certainty"),
        ("vmm/01", "vmm/13", "emotion_certainty", "A>B",
         "Major chord > noise for certainty"),
        # AAC — emotional_arousal
        ("aac/01", "aac/02", "emotional_arousal", "A>B",
         "Rickard 2004: loud > quiet for arousal (N=60)"),
        ("aac/03", "aac/04", "emotional_arousal", "A>B",
         "Fast 240BPM > slow 60BPM for arousal (onset density)"),
        ("aac/05", "aac/06", "emotional_arousal", "A>B",
         "Loud+fast > quiet sustained for maximum arousal separation"),
        ("aac/08", "aac/14", "emotional_arousal", "A>B",
         "Piano chord mf > silence for arousal"),
        # AAC — chills_intensity
        ("aac/07", "aac/06", "chills_intensity", "A>B",
         "Salimpoor 2011: crescendo > quiet sustained for chills"),
        ("aac/09", "aac/14", "chills_intensity", "A>B",
         "Strings chord > silence for chills (Salimpoor 2011)"),
        # AAC — ans_dominance
        ("aac/11", "aac/12", "ans_dominance", "A>B",
         "Gomez 2007: loud fast > quiet sustained for ANS (N=24)"),
        # AAC — driving_signal
        ("aac/13", "aac/14", "driving_signal", "A>B",
         "Isochronous beats > sustained chord for driving signal"),
        # NEMAC — nostalgia_affect
        ("nemac/01", "nemac/07", "nostalgia_affect", "A>B",
         "Sakakibara 2025: warm organ > noise for nostalgia"),
        ("nemac/03", "nemac/06", "nostalgia_affect", "A>B",
         "Tonal melody > cluster for nostalgia (Janata 2007)"),
        ("nemac/04", "nemac/07", "nostalgia_affect", "A>B",
         "Strings melody > noise for nostalgia (Sakakibara 2025)"),
        ("nemac/02", "nemac/06", "nostalgia_affect", "A>B",
         "Organ > cluster for nostalgia (warmth)"),
        # NEMAC — self_referential_nostalgia
        ("nemac/01", "nemac/06", "self_referential_nostalgia", "A>B",
         "Warm organ > cluster for vmPFC self-referential (Janata 2007)"),
        # NEMAC — wellbeing_enhancement
        ("nemac/01", "nemac/07", "wellbeing_enhancement", "A>B",
         "Barrett 2010: warm music > noise for wellbeing"),
        ("nemac/02", "nemac/06", "wellbeing_enhancement", "A>B",
         "Organ > cluster for wellbeing"),
        # NEMAC — nostalgia_peak_pred
        ("nemac/02", "nemac/08", "nostalgia_peak_pred", "A>B",
         "Musical input > silence for peak prediction"),
        # Cross-unit
        ("cross/01", "cross/02", "emotional_arousal", "A>B",
         "Loud > quiet for arousal (VMM×AAC integration)"),
        ("cross/03", "cross/06", "perceived_happy", "A>B",
         "Fast melody > quiet note for happiness (cross-unit)"),
        ("cross/03", "cross/06", "emotional_arousal", "A>B",
         "Fast melody > silence for arousal (cross-unit)"),
        ("cross/04", "cross/07", "perceived_sad", "A>B",
         "Cello minor > noise for sadness (VMM×NEMAC)"),
        ("cross/07", "cross/06", "nostalgia_affect", "A>B",
         "Organ > noise for nostalgia (NEMAC cross-unit)"),
    ]

    lines = [
        "# F5 Emotion Systems — Stimulus Catalog",
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
    print(f"  Catalog -> {cat_path}")


# ═══════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════

def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print("Generating F5 Emotion test audio...")
    print()

    print("[1/5] VMM — Valence-Mode Matching (14 stimuli)")
    generate_vmm_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('vmm/'))} files")

    print("[2/5] AAC — Autonomic-Affective Coupling (15 stimuli)")
    generate_aac_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('aac/'))} files")

    print("[3/5] NEMAC — Nostalgia-Evoked Memory-Affect (10 stimuli)")
    generate_nemac_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('nemac/'))} files")

    print("[4/5] Cross-unit Integration (8 stimuli)")
    generate_cross_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('cross/'))} files")

    print("[5/5] Boundary Conditions (7 stimuli)")
    generate_boundary_stimuli()
    print(f"  -> {sum(1 for k in ALL_METADATA if k.startswith('boundary/'))} files")

    print()
    print(f"Total: {len(ALL_METADATA)} stimuli")
    write_metadata()
    write_catalog()
    print()
    print("Done.")


if __name__ == "__main__":
    main()
