#!/usr/bin/env python
"""Generate metadata JSON for all F1 MIDI test audio files.

Encodes exact ground truth from generate_f1_midi_audio.py:
  - MIDI pitches, chord types, instruments, velocities
  - Time-stamped segments with human-readable labels
  - Expected belief behavior descriptions

Output: Test-Audio/micro_beliefs/f1_midi/metadata.json

Run::

    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/micro_beliefs/generate_midi_metadata.py
"""
from __future__ import annotations

import json
import pathlib
from typing import List, Optional

_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
OUT_PATH = _ROOT / "Test-Audio" / "micro_beliefs" / "f1_midi" / "metadata.json"

# ── MIDI helpers ─────────────────────────────────────────────────────

PITCH_NAMES = ["C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B"]

GM_PROGRAMS = {
    0: "Acoustic Grand Piano",
    6: "Harpsichord",
    19: "Church Organ",
    24: "Nylon String Guitar",
    40: "Violin",
    42: "Cello",
    48: "String Ensemble",
    52: "Choir Aahs",
    56: "Trumpet",
    68: "Oboe",
    73: "Flute",
}


def pname(midi: int) -> str:
    """MIDI note number → 'C4', 'Db4', etc."""
    octave = midi // 12 - 1
    return f"{PITCH_NAMES[midi % 12]}{octave}"


def pnames(pitches: List[int]) -> str:
    """List of MIDI notes → 'C4-E4-G4'."""
    return "-".join(pname(p) for p in pitches)


def freq(midi: int) -> float:
    return round(440.0 * 2 ** ((midi - 69) / 12), 2)


def inst(program: int) -> str:
    return GM_PROGRAMS.get(program, f"GM #{program}")


# ── Chord constructors (mirrors real_audio_stimuli.py) ───────────────

C3, D3, E3, F3, G3, A3, B3 = 48, 50, 52, 53, 55, 57, 59
C4, Db4, D4, Eb4, E4, F4, Gb4, G4, Ab4, A4, Bb4, B4 = range(60, 72)
C5, D5, E5, F5, G5, A5, B5 = 72, 74, 76, 77, 79, 81, 83
C6 = 84


def major_triad(root: int) -> List[int]:
    return [root, root + 4, root + 7]


def minor_triad(root: int) -> List[int]:
    return [root, root + 3, root + 7]


def diminished_triad(root: int) -> List[int]:
    return [root, root + 3, root + 6]


def augmented_triad(root: int) -> List[int]:
    return [root, root + 4, root + 8]


def dominant_seventh(root: int) -> List[int]:
    return [root, root + 4, root + 7, root + 10]


def chromatic_cluster(root: int, n: int) -> List[int]:
    return list(range(root, root + n))


def diatonic_scale(root: int, n: int) -> List[int]:
    steps = [0, 2, 4, 5, 7, 9, 11, 12, 14, 16, 17, 19, 21, 23, 24]
    return [root + steps[i] for i in range(n)]


def chromatic_scale(root: int, n: int) -> List[int]:
    return list(range(root, root + n))


# ── Segment builders ─────────────────────────────────────────────────

def seg_note(start: float, end: float, pitch: int, program: int = 0,
             velocity: int = 80) -> dict:
    return {
        "start": start, "end": end, "type": "note",
        "pitches": [pitch], "label": pname(pitch),
        "detail": f"{pname(pitch)} ({freq(pitch)} Hz), {inst(program)}, v{velocity}",
    }


def seg_chord(start: float, end: float, pitches: List[int], label: str,
              detail: str, program: int = 0, velocity: int = 80) -> dict:
    return {
        "start": start, "end": end, "type": "chord",
        "pitches": pitches, "label": label,
        "detail": f"{pnames(pitches)} — {detail}, {inst(program)}, v{velocity}",
    }


def seg_melody(notes: List[int], durs: List[float], program: int = 0,
               velocity: int = 80) -> List[dict]:
    segs = []
    t = 0.0
    for pitch, dur in zip(notes, durs):
        segs.append({
            "start": round(t, 3), "end": round(t + dur, 3), "type": "note",
            "pitches": [pitch], "label": pname(pitch),
            "detail": f"{pname(pitch)}, {inst(program)}, v{velocity}",
        })
        t += dur
    return segs


def seg_progression(chords: List[List[int]], durs: List[float],
                    labels: List[str], details: List[str],
                    program: int = 0, velocity: int = 80) -> List[dict]:
    segs = []
    t = 0.0
    for pitches, dur, label, detail in zip(chords, durs, labels, details):
        segs.append({
            "start": round(t, 3), "end": round(t + dur, 3), "type": "chord",
            "pitches": pitches, "label": label,
            "detail": f"{pnames(pitches)} — {detail}, {inst(program)}, v{velocity}",
        })
        t += dur
    return segs


# ── Entry builder ────────────────────────────────────────────────────

def entry(relay: str, filename: str, display: str, desc: str,
          dur: float, program: int, segments: List[dict],
          expected: str, velocity: int = 80) -> dict:
    return {
        "relay": relay,
        "filename": filename,
        "displayName": display,
        "description": desc,
        "duration_s": dur,
        "instrument": inst(program),
        "program": program,
        "velocity": velocity,
        "segments": segments,
        "expectedBehavior": expected,
    }


# =====================================================================
# BCH — 17 files
# =====================================================================

def build_bch() -> dict:
    m = {}

    m["bch/01_single_C4_piano"] = entry(
        "bch", "01_single_C4_piano.wav", "Single C4 — Piano",
        "Single note — maximum consonance (no beating partials)",
        4.0, 0, [seg_note(0, 4, C4)],
        "Maximum consonance — single pitch, no intervallic interaction",
    )

    m["bch/02_octave_C4C5_piano"] = entry(
        "bch", "02_octave_C4C5_piano.wav", "Octave C4-C5 — Piano",
        "Most consonant interval (2:1 frequency ratio)",
        4.0, 0, [seg_chord(0, 4, [C4, C5], "P8", "octave, 2:1 ratio")],
        "Very high consonance — octave is the most consonant interval",
    )

    m["bch/03_p5_C4G4_piano"] = entry(
        "bch", "03_p5_C4G4_piano.wav", "Perfect 5th C4-G4 — Piano",
        "Second most consonant interval (3:2 ratio)",
        4.0, 0, [seg_chord(0, 4, [C4, G4], "P5", "perfect fifth, 3:2 ratio")],
        "High consonance — P5 after octave in consonance hierarchy",
    )

    m["bch/04_p4_C4F4_piano"] = entry(
        "bch", "04_p4_C4F4_piano.wav", "Perfect 4th C4-F4 — Piano",
        "Consonant interval (4:3 ratio)",
        4.0, 0, [seg_chord(0, 4, [C4, F4], "P4", "perfect fourth, 4:3 ratio")],
        "Consonant — P4 ranks after P5 in hierarchy",
    )

    m["bch/05_major_triad_piano"] = entry(
        "bch", "05_major_triad_piano.wav", "C Major Triad — Piano",
        "Consonant chord (C-E-G, contains M3+P5)",
        4.0, 0, [seg_chord(0, 4, major_triad(C4), "C maj", "major triad, consonant")],
        "High consonance — major triad is the most consonant chord",
    )

    m["bch/06_minor_triad_piano"] = entry(
        "bch", "06_minor_triad_piano.wav", "C Minor Triad — Piano",
        "Slightly less consonant (C-Eb-G, contains m3+P5)",
        4.0, 0, [seg_chord(0, 4, minor_triad(C4), "C min", "minor triad")],
        "Good consonance — minor slightly less than major",
    )

    m["bch/07_dim_triad_piano"] = entry(
        "bch", "07_dim_triad_piano.wav", "C Dim Triad — Piano",
        "Dissonant chord (C-Eb-Gb, contains tritone Eb-A implied)",
        4.0, 0, [seg_chord(0, 4, diminished_triad(C4), "C dim", "diminished triad, contains tritone")],
        "Moderate dissonance — diminished contains tritone interval",
    )

    m["bch/08_aug_triad_piano"] = entry(
        "bch", "08_aug_triad_piano.wav", "C Aug Triad — Piano",
        "Dissonant chord (C-E-G#, symmetric division of octave)",
        4.0, 0, [seg_chord(0, 4, augmented_triad(C4), "C aug", "augmented triad, symmetrical")],
        "Moderate dissonance — augmented triad is symmetrical and unstable",
    )

    m["bch/09_dom7_G_piano"] = entry(
        "bch", "09_dom7_G_piano.wav", "G Dominant 7th — Piano",
        "Moderate dissonance (G-B-D-F, contains tritone B-F)",
        4.0, 0, [seg_chord(0, 4, dominant_seventh(G3), "G7", "dominant 7th, tritone B-F")],
        "Moderate dissonance — dominant 7th contains tritone B3-F4",
    )

    m["bch/10_cluster_4note_piano"] = entry(
        "bch", "10_cluster_4note_piano.wav", "4-Note Cluster — Piano",
        "High dissonance (4 adjacent semitones C-Db-D-Eb)",
        4.0, 0, [seg_chord(0, 4, chromatic_cluster(C4, 4), "cluster(4)", "4 chromatic notes, maximum roughness")],
        "High dissonance — dense chromatic cluster creates strong beating",
    )

    m["bch/11_cluster_6note_piano"] = entry(
        "bch", "11_cluster_6note_piano.wav", "6-Note Cluster — Piano",
        "Maximum dissonance (6 adjacent semitones C-Db-D-Eb-E-F)",
        4.0, 0, [seg_chord(0, 4, chromatic_cluster(C4, 6), "cluster(6)", "6 chromatic notes")],
        "Maximum dissonance — densest cluster, extreme roughness",
    )

    m["bch/12_I_IV_V_I_piano"] = entry(
        "bch", "12_I_IV_V_I_piano.wav", "I-IV-V-I Cadence — Piano",
        "Classic consonant progression (C→F→G→C, 1.5s each)",
        6.0, 0,
        seg_progression(
            [major_triad(C4), major_triad(F3), major_triad(G3), major_triad(C4)],
            [1.5, 1.5, 1.5, 1.5],
            ["C maj", "F maj", "G maj", "C maj"],
            ["I — tonic", "IV — subdominant", "V — dominant", "I — tonic return"],
        ),
        "Consistently high consonance throughout — all major triads",
    )

    m["bch/13_major_triad_organ"] = entry(
        "bch", "13_major_triad_organ.wav", "C Major Triad — Organ",
        "Same harmony as #05, different timbre (organ)",
        4.0, 19, [seg_chord(0, 4, major_triad(C4), "C maj", "major triad on organ")],
        "High consonance — same as piano but organ timbre has more partials",
    )

    m["bch/14_cluster_4note_organ"] = entry(
        "bch", "14_cluster_4note_organ.wav", "4-Note Cluster — Organ",
        "Same cluster as #10, organ timbre",
        4.0, 19, [seg_chord(0, 4, chromatic_cluster(C4, 4), "cluster(4)", "4 chromatic on organ")],
        "High dissonance — organ partials amplify cluster roughness",
    )

    m["bch/15_major_triad_strings"] = entry(
        "bch", "15_major_triad_strings.wav", "C Major Triad — Strings",
        "Same harmony as #05, string ensemble timbre",
        4.0, 48, [seg_chord(0, 4, major_triad(C4), "C maj", "major triad on strings")],
        "High consonance — strings have smoother partials than piano",
    )

    m["bch/16_consonant_to_dissonant_8s"] = entry(
        "bch", "16_consonant_to_dissonant_8s.wav",
        "Consonant → Dissonant Progression",
        "C maj → C min → C dim → cluster (2s each, increasing dissonance)",
        8.0, 0,
        seg_progression(
            [major_triad(C4), minor_triad(C4), diminished_triad(C4), chromatic_cluster(C4, 4)],
            [2.0, 2.0, 2.0, 2.0],
            ["C maj", "C min", "C dim", "cluster(4)"],
            ["consonant", "slightly less consonant", "dissonant (tritone)", "maximum dissonance"],
        ),
        "Consonance decreases monotonically: major > minor > dim > cluster",
    )

    m["bch/17_dissonant_to_consonant_8s"] = entry(
        "bch", "17_dissonant_to_consonant_8s.wav",
        "Dissonant → Consonant Progression",
        "Cluster → C dim → C min → C maj (2s each, decreasing dissonance)",
        8.0, 0,
        seg_progression(
            [chromatic_cluster(C4, 4), diminished_triad(C4), minor_triad(C4), major_triad(C4)],
            [2.0, 2.0, 2.0, 2.0],
            ["cluster(4)", "C dim", "C min", "C maj"],
            ["maximum dissonance", "dissonant (tritone)", "slightly consonant", "consonant"],
        ),
        "Consonance increases monotonically: cluster < dim < minor < major",
    )

    return m


# =====================================================================
# PSCL — 12 files
# =====================================================================

def build_pscl() -> dict:
    m = {}

    for i, (pitch, prog, label) in enumerate([
        (A4, 0, "piano"), (A4, 40, "violin"), (A4, 73, "flute"),
        (A4, 68, "oboe"), (A4, 56, "trumpet"),
    ], 1):
        m[f"pscl/{i:02d}_A4_{label}"] = entry(
            "pscl", f"{i:02d}_A4_{label}.wav", f"A4 (440 Hz) — {inst(prog)}",
            f"Single A4 on {inst(prog)} — clear pitch, different timbres",
            4.0, prog, [seg_note(0, 4, pitch, prog)],
            "Clear single-pitch salience regardless of instrument timbre",
        )

    for i, (pitch, label) in enumerate([
        (C3, "C3"), (C4, "C4"), (C5, "C5"), (C6, "C6"),
    ], 6):
        m[f"pscl/{i:02d}_{label}_piano"] = entry(
            "pscl", f"{i:02d}_{label}_piano.wav", f"{label} ({freq(pitch)} Hz) — Piano",
            f"Single {label} on piano — pitch clarity across registers",
            4.0, 0, [seg_note(0, 4, pitch)],
            f"Clear pitch salience at {label} register",
        )

    m["pscl/10_chord_C_major"] = entry(
        "pscl", "10_chord_C_major.wav", "C Major Chord — Piano",
        "3-note chord — pitch more ambiguous than single note",
        4.0, 0, [seg_chord(0, 4, major_triad(C4), "C maj", "major triad, ambiguous f0")],
        "Reduced pitch salience — multiple competing fundamentals",
    )

    m["pscl/11_cluster_6note"] = entry(
        "pscl", "11_cluster_6note.wav", "6-Note Cluster — Piano",
        "Dense chord — pitch very ambiguous (6 semitones)",
        4.0, 0, [seg_chord(0, 4, chromatic_cluster(C4, 6), "cluster(6)", "6 chromatic, very ambiguous f0")],
        "Minimal pitch salience — dense cluster destroys pitch clarity",
    )

    scale_notes = diatonic_scale(C4, 8)
    m["pscl/12_melody_diatonic"] = entry(
        "pscl", "12_melody_diatonic.wav", "Diatonic Melody C4→C5 — Piano",
        "8-note ascending C major scale (0.5s each)",
        4.0, 0, seg_melody(scale_notes, [0.5] * 8),
        "Sequential pitch clarity — each note should show clear salience peak",
    )

    return m


# =====================================================================
# PCCR — 11 files
# =====================================================================

def build_pccr() -> dict:
    m = {}
    mel_rel = [0, 2, 4, 5, 7]  # C-D-E-F-G relative

    for i, (base, oct) in enumerate([(C3, 3), (C4, 4), (C5, 5)], 1):
        notes = [base + n for n in mel_rel]
        m[f"pccr/{i:02d}_melody_C_oct{oct}"] = entry(
            "pccr", f"{i:02d}_melody_C_oct{oct}.wav",
            f"C-D-E-F-G Melody — Octave {oct}",
            f"Same chroma pattern at octave {oct} (0.5s each)",
            2.5, 0, seg_melody(notes, [0.5] * 5),
            f"Same chroma class as other octaves — octave equivalence test",
        )

    m["pccr/04_melody_G_oct4"] = entry(
        "pccr", "04_melody_G_oct4.wav", "G-A-B-C-D Melody — Oct 4",
        "Different key (G major start) for chroma comparison",
        2.5, 0, seg_melody([G4, A4, B4, C5, D5], [0.5] * 5),
        "Different chroma than C-based melodies",
    )

    m["pccr/05_melody_Eb_oct4"] = entry(
        "pccr", "05_melody_Eb_oct4.wav", "Eb-F-G-Ab-Bb Melody — Oct 4",
        "Different key (Eb major start) for chroma comparison",
        2.5, 0, seg_melody([Eb4, F4, G4, Ab4, Bb4], [0.5] * 5),
        "Different chroma than C or G melodies",
    )

    m["pccr/06_octave_dyad"] = entry(
        "pccr", "06_octave_dyad.wav", "Octave Dyad C4-C5",
        "Maximum chroma equivalence (same pitch class)",
        4.0, 0, [seg_chord(0, 4, [C4, C5], "P8", "octave — identical chroma")],
        "Maximum octave equivalence — same pitch class",
    )

    m["pccr/07_tritone_dyad"] = entry(
        "pccr", "07_tritone_dyad.wav", "Tritone Dyad C4-Gb4",
        "Minimum chroma equivalence (maximally different pitch class)",
        4.0, 0, [seg_chord(0, 4, [C4, Gb4], "TT", "tritone — opposite chroma")],
        "Low chroma equivalence — tritone is maximally distant",
    )

    m["pccr/08_fifth_dyad"] = entry(
        "pccr", "08_fifth_dyad.wav", "Fifth Dyad C4-G4",
        "Strong harmonic relationship (3:2 ratio)",
        4.0, 0, [seg_chord(0, 4, [C4, G4], "P5", "fifth — strong harmonic relation")],
        "Moderate chroma equivalence — harmonically related but different class",
    )

    m["pccr/09_single_C4"] = entry(
        "pccr", "09_single_C4.wav", "Single C4 — Piano",
        "Single note — strong chroma identity",
        4.0, 0, [seg_note(0, 4, C4)],
        "Strong single-pitch chroma identity",
    )

    m["pccr/10_single_A4"] = entry(
        "pccr", "10_single_A4.wav", "Single A4 — Piano",
        "Single note — strong chroma identity, different class than C",
        4.0, 0, [seg_note(0, 4, A4)],
        "Strong single-pitch chroma identity (A vs C)",
    )

    m["pccr/11_all_12_notes"] = entry(
        "pccr", "11_all_12_notes.wav", "All 12 Chromatic Notes",
        "All pitch classes simultaneous — weakest chroma identity",
        4.0, 0,
        [seg_chord(0, 4, chromatic_scale(C4, 12), "all 12", "all pitch classes — no chroma dominance")],
        "Minimal chroma identity — all 12 classes equally present",
        velocity=50,
    )

    return m


# =====================================================================
# SDED — 8 files
# =====================================================================

def build_sded() -> dict:
    m = {}

    m["sded/01_single_C4"] = entry(
        "sded", "01_single_C4.wav", "Single C4 — Piano",
        "Minimal spectral complexity (single source)",
        4.0, 0, [seg_note(0, 4, C4)],
        "Minimum spectral complexity",
    )

    m["sded/02_octave"] = entry(
        "sded", "02_octave.wav", "Octave C4-C5 — Piano",
        "Very low spectral interaction (aligned partials)",
        4.0, 0, [seg_chord(0, 4, [C4, C5], "P8", "octave, aligned partials")],
        "Very low spectral complexity — partials align perfectly",
    )

    m["sded/03_major_triad"] = entry(
        "sded", "03_major_triad.wav", "C Major Triad — Piano",
        "Low complexity (consonant partials, well-spaced)",
        4.0, 0, [seg_chord(0, 4, major_triad(C4), "C maj", "consonant, well-spaced partials")],
        "Low spectral complexity",
    )

    m["sded/04_m2_dyad"] = entry(
        "sded", "04_m2_dyad.wav", "Minor 2nd Dyad C4-Db4",
        "High roughness from close partials (1 semitone apart)",
        4.0, 0, [seg_chord(0, 4, [C4, Db4], "m2", "1 semitone, maximum roughness for dyad")],
        "High spectral complexity — close partials create strong beating",
    )

    m["sded/05_cluster_4note"] = entry(
        "sded", "05_cluster_4note.wav", "4-Note Cluster — Piano",
        "4 adjacent semitones (C-Db-D-Eb)",
        4.0, 0, [seg_chord(0, 4, chromatic_cluster(C4, 4), "cluster(4)", "dense chromatic")],
        "High spectral complexity — multiple close partials",
    )

    m["sded/06_cluster_6note"] = entry(
        "sded", "06_cluster_6note.wav", "6-Note Cluster — Piano",
        "Maximum spectral density (6 semitones C→F)",
        4.0, 0, [seg_chord(0, 4, chromatic_cluster(C4, 6), "cluster(6)", "very dense chromatic")],
        "Maximum spectral complexity in test set",
    )

    m["sded/07_bitonal_C_Fsharp"] = entry(
        "sded", "07_bitonal_C_Fsharp.wav", "Bitonal C + F# Major",
        "Two keys simultaneously (C maj + F# maj polytonal)",
        4.0, 0, [seg_chord(0, 4, [C4, E4, G4, Gb4, Bb4, C5 + 1],
                           "C+F#", "bitonal — two triads a tritone apart")],
        "Very high spectral complexity — polytonal clash",
    )

    m["sded/08_full_chromatic"] = entry(
        "sded", "08_full_chromatic.wav", "Full Chromatic — All 12 Notes",
        "All 12 pitch classes simultaneously",
        4.0, 0, [seg_chord(0, 4, chromatic_scale(C4, 12), "chromatic(12)",
                           "all 12 notes, maximum density")],
        "Maximum spectral complexity — all pitch classes create dense beating",
        velocity=50,
    )

    return m


# =====================================================================
# CSG — 6 files
# =====================================================================

def build_csg() -> dict:
    m = {}

    m["csg/01_major_triad"] = entry(
        "csg", "01_major_triad.wav", "C Major Triad — Piano",
        "Consonant chord — expected low salience",
        4.0, 0, [seg_chord(0, 4, major_triad(C4), "C maj", "consonant, low salience expected")],
        "Low salience — consonant chord does not strongly engage attention",
    )

    m["csg/02_m2_dyad"] = entry(
        "csg", "02_m2_dyad.wav", "Minor 2nd Dyad C4-Db4",
        "High roughness → high salience (perceptual attention grab)",
        4.0, 0, [seg_chord(0, 4, [C4, Db4], "m2", "1 semitone, high roughness → high salience")],
        "High salience — roughness from close partials engages ACC/AI",
    )

    m["csg/03_cluster"] = entry(
        "csg", "03_cluster.wav", "4-Note Cluster — Piano",
        "Maximum dissonance → maximum salience",
        4.0, 0, [seg_chord(0, 4, chromatic_cluster(C4, 4), "cluster(4)",
                           "dense chromatic — maximum salience")],
        "Maximum salience — dense cluster drives strongest attention response",
    )

    m["csg/04_V7_I_resolution"] = entry(
        "csg", "04_V7_I_resolution.wav", "V7 → I Resolution",
        "Dominant seventh resolves to tonic major — tension→release",
        6.0, 0,
        seg_progression(
            [dominant_seventh(G3), major_triad(C4)],
            [3.0, 3.0],
            ["G7", "C maj"],
            ["dominant 7th — tension (tritone B-F)", "tonic major — resolution"],
        ),
        "High salience during G7 (dissonance), drops sharply at C resolution",
    )

    m["csg/05_I_V7_tension"] = entry(
        "csg", "05_I_V7_tension.wav", "I → V7 Tension Build",
        "Tonic major to dominant seventh — consonance→dissonance",
        6.0, 0,
        seg_progression(
            [major_triad(C4), dominant_seventh(G3)],
            [3.0, 3.0],
            ["C maj", "G7"],
            ["tonic major — relaxed", "dominant 7th — tension rising"],
        ),
        "Low salience during C major, rises sharply when G7 enters",
    )

    m["csg/06_single_note"] = entry(
        "csg", "06_single_note.wav", "Single C4 — Baseline",
        "Single note — baseline salience level (no intervallic content)",
        4.0, 0, [seg_note(0, 4, C4)],
        "Baseline salience — single note, no dissonance to drive attention",
    )

    return m


# =====================================================================
# MPG — 10 files
# =====================================================================

def build_mpg() -> dict:
    m = {}

    asc = diatonic_scale(C4, 8)
    desc = list(reversed(asc))
    chrom13 = chromatic_scale(C4, 13)

    m["mpg/01_ascending_diatonic"] = entry(
        "mpg", "01_ascending_diatonic.wav", "Ascending Diatonic C4→C5",
        "C major scale ascending (0.4s per note, 8 notes)",
        3.2, 0, seg_melody(asc, [0.4] * 8),
        "Strong positive (ascending) contour — stepwise upward motion",
    )

    m["mpg/02_descending_diatonic"] = entry(
        "mpg", "02_descending_diatonic.wav", "Descending Diatonic C5→C4",
        "C major scale descending (0.4s per note, 8 notes)",
        3.2, 0, seg_melody(desc, [0.4] * 8),
        "Strong negative (descending) contour — stepwise downward motion",
    )

    m["mpg/03_ascending_chromatic"] = entry(
        "mpg", "03_ascending_chromatic.wav", "Ascending Chromatic C4→C5",
        "Chromatic scale ascending (0.3s per note, 13 semitones)",
        3.9, 0, seg_melody(chrom13, [0.3] * 13),
        "Ascending contour with semitone steps — dense melodic motion",
    )

    m["mpg/04_arpeggio_arch"] = entry(
        "mpg", "04_arpeggio_arch.wav", "Arpeggio Arch C-E-G-C-G-E-C",
        "C major arpeggio up then down (arch contour, 0.5s each)",
        3.5, 0, seg_melody([C4, E4, G4, C5, G4, E4, C4], [0.5] * 7),
        "Arch contour — ascending then descending, large intervals",
    )

    m["mpg/05_repeated_C4"] = entry(
        "mpg", "05_repeated_C4.wav", "Repeated C4 × 8",
        "Same note repeated 8 times (no pitch motion, 0.4s each)",
        3.2, 0, seg_melody([C4] * 8, [0.4] * 8),
        "Zero melodic contour — no pitch change between notes",
    )

    m["mpg/06_octave_leaps"] = entry(
        "mpg", "06_octave_leaps.wav", "Octave Leaps C4-C5-C4-C5-C4",
        "Large interval jumps (octave up/down, 0.6s each)",
        3.0, 0, seg_melody([C4, C5, C4, C5, C4], [0.6] * 5),
        "Alternating contour with maximum interval (octave jumps)",
    )

    m["mpg/07_mixed_contour"] = entry(
        "mpg", "07_mixed_contour.wav", "Mixed Contour Melody",
        "Up-down-up pattern with varied intervals (0.35s each)",
        3.5, 0, seg_melody(
            [C4, E4, G4, F4, D4, F4, A4, G4, E4, C5], [0.35] * 10
        ),
        "Complex mixed contour — direction changes multiple times",
    )

    m["mpg/08_sustained_C4"] = entry(
        "mpg", "08_sustained_C4.wav", "Sustained C4 — No Motion",
        "Single held note, 4s — zero melodic activity",
        4.0, 0, [seg_note(0, 4, C4)],
        "Zero melodic activity — sustained single note",
    )

    m["mpg/09_ascending_diatonic_violin"] = entry(
        "mpg", "09_ascending_diatonic_violin.wav", "Ascending Diatonic — Violin",
        "Same melody as #01 but on violin",
        3.2, 40, seg_melody(asc, [0.4] * 8, program=40),
        "Same contour as piano — timbre-invariant melodic tracking",
    )

    m["mpg/10_ascending_diatonic_flute"] = entry(
        "mpg", "10_ascending_diatonic_flute.wav", "Ascending Diatonic — Flute",
        "Same melody as #01 but on flute",
        3.2, 73, seg_melody(asc, [0.4] * 8, program=73),
        "Same contour as piano — timbre-invariant melodic tracking",
    )

    return m


# =====================================================================
# MIAA — 14 files
# =====================================================================

def build_miaa() -> dict:
    m = {}

    instruments = [
        (0, "piano"), (40, "violin"), (42, "cello"), (73, "flute"),
        (68, "oboe"), (56, "trumpet"), (19, "organ"), (24, "guitar"),
    ]

    for i, (prog, name) in enumerate(instruments, 1):
        m[f"miaa/{i:02d}_C4_{name}"] = entry(
            "miaa", f"{i:02d}_C4_{name}.wav", f"C4 — {inst(prog)}",
            f"Single C4 on {inst(prog)} — timbral fingerprint",
            5.0, prog, [seg_note(0, 5, C4, prog)],
            f"Unique timbral character of {inst(prog)} at C4",
        )

    m["miaa/09_C4_piano_pp"] = entry(
        "miaa", "09_C4_piano_pp.wav", "C4 Piano — pp (soft)",
        "Same note, soft dynamics (velocity 30) — less timbral brightness",
        5.0, 0, [seg_note(0, 5, C4, 0, 30)],
        "Softer dynamics → less high-frequency content → different timbral character",
        velocity=30,
    )

    m["miaa/10_C4_piano_ff"] = entry(
        "miaa", "10_C4_piano_ff.wav", "C4 Piano — ff (loud)",
        "Same note, max dynamics (velocity 127) — brighter timbre",
        5.0, 0, [seg_note(0, 5, C4, 0, 127)],
        "Louder dynamics → more high-frequency partials → brighter timbral character",
        velocity=127,
    )

    m["miaa/11_C3_piano"] = entry(
        "miaa", "11_C3_piano.wav", "C3 Piano — Low Register",
        "Same instrument, lower register — darker timbre",
        5.0, 0, [seg_note(0, 5, C3)],
        "Lower register → darker, warmer timbral character",
    )

    m["miaa/12_C5_piano"] = entry(
        "miaa", "12_C5_piano.wav", "C5 Piano — High Register",
        "Same instrument, higher register — brighter timbre",
        5.0, 0, [seg_note(0, 5, C5)],
        "Higher register → brighter, thinner timbral character",
    )

    m["miaa/13_chord_C_major_piano"] = entry(
        "miaa", "13_chord_C_major_piano.wav", "C Major Chord — Piano",
        "Chord vs single note — timbral complexity difference",
        5.0, 0, [seg_chord(0, 5, major_triad(C4), "C maj", "chord — richer spectral content than single note")],
        "Chord has richer spectral content than single note on same instrument",
    )

    # Multi-timbre sequence — special case with 4 instruments
    m["miaa/14_timbre_sequence_4inst"] = entry(
        "miaa", "14_timbre_sequence_4inst.wav",
        "Timbre Sequence: Piano→Violin→Flute→Trumpet",
        "Same C4 note, 4 instruments in sequence (1.5s each)",
        6.0, 0,  # mixed program
        [
            {"start": 0.0, "end": 1.5, "type": "note", "pitches": [C4],
             "label": "Piano", "detail": f"C4 on {inst(0)}, v80"},
            {"start": 1.5, "end": 3.0, "type": "note", "pitches": [C4],
             "label": "Violin", "detail": f"C4 on {inst(40)}, v80"},
            {"start": 3.0, "end": 4.5, "type": "note", "pitches": [C4],
             "label": "Flute", "detail": f"C4 on {inst(73)}, v80"},
            {"start": 4.5, "end": 6.0, "type": "note", "pitches": [C4],
             "label": "Trumpet", "detail": f"C4 on {inst(56)}, v80"},
        ],
        "Timbral character changes every 1.5s — same pitch, 4 distinct timbres",
    )

    return m


# =====================================================================
# STAI — 9 files
# =====================================================================

def build_stai() -> dict:
    m = {}

    m["stai/01_beautiful_I_vi_IV_V_strings"] = entry(
        "stai", "01_beautiful_I_vi_IV_V_strings.wav",
        "Beautiful: I-vi-IV-V — Strings",
        "Classic pop/film progression on strings (C-Am-F-G, 2s each)",
        8.0, 48,
        seg_progression(
            [major_triad(C4), minor_triad(A3), major_triad(F3), major_triad(G3)],
            [2.0, 2.0, 2.0, 2.0],
            ["C maj", "A min", "F maj", "G maj"],
            ["I — warm tonic", "vi — gentle minor", "IV — subdominant lift", "V — dominant tension"],
            program=48, velocity=70,
        ),
        "High aesthetic quality — warm string timbre + consonant progression",
        velocity=70,
    )

    m["stai/02_chorale_SATB_choir"] = entry(
        "stai", "02_chorale_SATB_choir.wav",
        "Beautiful: SATB Chorale — Choir",
        "Bach-style 4-part chorale on choir (I-IV-V-I, 2s each)",
        8.0, 52,
        seg_progression(
            [[C4, E4, G4, C5], [F4, A4, C5, F5], [G4, B4, D5, G5], [C4, E4, G4, C5]],
            [2.0, 2.0, 2.0, 2.0],
            ["C maj (4pt)", "F maj (4pt)", "G maj (4pt)", "C maj (4pt)"],
            ["I — open voicing", "IV — bright voicing", "V — dominant", "I — return"],
            program=52, velocity=70,
        ),
        "High aesthetic quality — choir timbre + chorale harmony",
        velocity=70,
    )

    m["stai/03_harsh_chromatic_clusters"] = entry(
        "stai", "03_harsh_chromatic_clusters.wav",
        "Harsh: Chromatic Cluster Sequence",
        "Moving clusters — C→Db→D→Eb (4-note each, 1.5s, forte)",
        6.0, 0,
        seg_progression(
            [chromatic_cluster(C4, 4), chromatic_cluster(Db4, 4),
             chromatic_cluster(D4, 4), chromatic_cluster(Eb4, 4)],
            [1.5, 1.5, 1.5, 1.5],
            ["cluster C", "cluster Db", "cluster D", "cluster Eb"],
            ["4-note cluster", "4-note cluster (up semitone)", "4-note cluster", "4-note cluster"],
            velocity=100,
        ),
        "Low aesthetic quality — sustained dissonance + harsh dynamics",
        velocity=100,
    )

    m["stai/04_minor_key_progression"] = entry(
        "stai", "04_minor_key_progression.wav",
        "Moderate: Minor Key Progression",
        "Am-Bdim-C-E7 — more tension than major (2s each)",
        8.0, 0,
        seg_progression(
            [minor_triad(A3), diminished_triad(B3), major_triad(C4), dominant_seventh(E3)],
            [2.0, 2.0, 2.0, 2.0],
            ["A min", "B dim", "C maj", "E7"],
            ["i — minor tonic", "ii° — diminished tension", "III — relative major", "V7/vi — secondary dominant"],
            velocity=75,
        ),
        "Moderate aesthetic — tension from minor mode + diminished chord",
        velocity=75,
    )

    m["stai/05_melody_with_chords_beautiful"] = entry(
        "stai", "05_melody_with_chords_beautiful.wav",
        "Beautiful: Melody + Chords (Flute+Strings)",
        "Simple melody (Mary Had a Little Lamb fragment) over I-V chords",
        4.0, 73,  # melody on flute
        [
            # Melody segments
            {"start": 0.0, "end": 0.5, "type": "note", "pitches": [E5],
             "label": "E5", "detail": "Melody: E5 on Flute, v90"},
            {"start": 0.5, "end": 1.0, "type": "note", "pitches": [D5],
             "label": "D5", "detail": "Melody: D5 on Flute"},
            {"start": 1.0, "end": 1.5, "type": "note", "pitches": [C5],
             "label": "C5", "detail": "Melody: C5 on Flute"},
            {"start": 1.5, "end": 2.0, "type": "note", "pitches": [D5],
             "label": "D5", "detail": "Melody: D5 on Flute"},
            {"start": 2.0, "end": 2.5, "type": "note", "pitches": [E5],
             "label": "E5", "detail": "Melody: E5 on Flute"},
            {"start": 2.5, "end": 3.0, "type": "note", "pitches": [E5],
             "label": "E5", "detail": "Melody: E5 on Flute"},
            {"start": 3.0, "end": 4.0, "type": "note", "pitches": [E5],
             "label": "E5", "detail": "Melody: E5 on Flute (long)"},
            # Chord accompaniment
            {"start": 0.0, "end": 1.0, "type": "chord", "pitches": major_triad(C4),
             "label": "C maj (acc)", "detail": "Accompaniment: C major on Strings, v60"},
            {"start": 1.0, "end": 2.0, "type": "chord", "pitches": major_triad(G3),
             "label": "G maj (acc)", "detail": "Accompaniment: G major on Strings"},
            {"start": 2.0, "end": 3.0, "type": "chord", "pitches": major_triad(C4),
             "label": "C maj (acc)", "detail": "Accompaniment: C major on Strings"},
            {"start": 3.0, "end": 4.0, "type": "chord", "pitches": major_triad(G3),
             "label": "G maj (acc)", "detail": "Accompaniment: G major on Strings"},
        ],
        "High aesthetic — pleasant melody + consonant harmony + two timbres",
    )

    m["stai/06_dense_cluster_ff"] = entry(
        "stai", "06_dense_cluster_ff.wav", "Harsh: Dense Cluster ff",
        "8-note chromatic cluster at maximum velocity",
        4.0, 0, [seg_chord(0, 4, chromatic_cluster(C4, 8), "cluster(8)",
                           "8 chromatic notes, ff dynamics — maximum harshness")],
        "Very low aesthetic quality — dense cluster + harsh dynamics",
        velocity=127,
    )

    m["stai/07_major_triad_strings_p"] = entry(
        "stai", "07_major_triad_strings_p.wav", "Pleasant: C Major — Strings p",
        "Single consonant chord on strings, soft dynamics — simple beauty",
        4.0, 48, [seg_chord(0, 4, major_triad(C4), "C maj",
                            "major triad on strings, soft — pleasant baseline")],
        "Good aesthetic — warm strings + consonant chord + soft dynamics",
        velocity=60,
    )

    m["stai/08_dissonant_to_resolved"] = entry(
        "stai", "08_dissonant_to_resolved.wav",
        "Aesthetic Arc: Dissonant → Resolved",
        "Cluster → G7 → C major (2s-2s-3s) — aesthetic improvement",
        7.0, 0,
        seg_progression(
            [chromatic_cluster(B3, 4), dominant_seventh(G3), major_triad(C4)],
            [2.0, 2.0, 3.0],
            ["cluster B", "G7", "C maj"],
            ["harsh cluster — low aesthetic", "dominant 7th — tension", "resolution — high aesthetic"],
            velocity=75,
        ),
        "Aesthetic improves: ugly→tense→beautiful (dissonance resolves to consonance)",
        velocity=75,
    )

    m["stai/09_resolved_to_dissonant"] = entry(
        "stai", "09_resolved_to_dissonant.wav",
        "Aesthetic Arc: Resolved → Dissonant",
        "C major → G7 → Cluster (3s-2s-2s) — aesthetic decline",
        7.0, 0,
        seg_progression(
            [major_triad(C4), dominant_seventh(G3), chromatic_cluster(B3, 4)],
            [3.0, 2.0, 2.0],
            ["C maj", "G7", "cluster B"],
            ["consonant — high aesthetic", "dominant 7th — tension building", "harsh cluster — low aesthetic"],
            velocity=75,
        ),
        "Aesthetic worsens: beautiful→tense→ugly (consonance dissolves to dissonance)",
        velocity=75,
    )

    return m


# =====================================================================
# Relay-to-belief mapping
# =====================================================================

RELAY_BELIEFS = {
    "bch": [
        "consonance_salience_gradient",
        "consonance_trajectory",
        "harmonic_stability",
        "harmonic_template_match",
        "interval_quality",
    ],
    "csg": [
        "consonance_salience_gradient",
    ],
    "pscl": [
        "pitch_continuation",
        "pitch_salience",
    ],
    "pccr": [
        "octave_equivalence",
        "pitch_class_stability",
    ],
    "sded": [
        "spectral_complexity",
        "spectral_dissonance_expectation",
    ],
    "mpg": [
        "melodic_contour_tracking",
        "melodic_expectation",
    ],
    "miaa": [
        "timbral_continuity",
        "timbral_novelty",
    ],
    "stai": [
        "aesthetic_quality",
        "aesthetic_trajectory",
    ],
}


# =====================================================================
# Main
# =====================================================================

def main():
    metadata = {}
    metadata.update(build_bch())
    metadata.update(build_pscl())
    metadata.update(build_pccr())
    metadata.update(build_sded())
    metadata.update(build_csg())
    metadata.update(build_mpg())
    metadata.update(build_miaa())
    metadata.update(build_stai())

    # Add relay-beliefs mapping to each entry
    for key, meta in metadata.items():
        relay = meta["relay"]
        meta["relatedBeliefs"] = RELAY_BELIEFS.get(relay, [])

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    print(f"Generated metadata for {len(metadata)} MIDI test files → {OUT_PATH}")

    # Summary by relay
    from collections import Counter
    relay_counts = Counter(m["relay"] for m in metadata.values())
    for relay in sorted(relay_counts):
        print(f"  {relay.upper():6s}: {relay_counts[relay]} files")


if __name__ == "__main__":
    main()
