#!/usr/bin/env python3
"""Generate a synthetic test experiment for WebLab development.

Creates a fake experiment with mathematically generated data so the frontend
can be tested without running the full MI pipeline (which takes ~150s).

Usage:
    python scripts/generate_synthetic.py
"""
from __future__ import annotations

import json
import math
import struct
import sys
import wave
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np

_SCRIPT_DIR = Path(__file__).resolve().parent
_WEBLAB_DIR = _SCRIPT_DIR.parent
_PROJECT_ROOT = _WEBLAB_DIR.parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

SLUG = "synthetic-test"
EXP_DIR = _WEBLAB_DIR / "experiments" / SLUG
SR = 44100
DURATION_S = 10.0  # 10-second test clip
HOP = 256
FRAME_RATE = SR / HOP
T_FULL = int(DURATION_S * FRAME_RATE)
STRIDE = max(1, T_FULL // 2000)
T_LOD = len(range(0, T_FULL, STRIDE))

R3_DIM = 97
NUM_REGIONS = 26
NUM_NEURO = 4


def _write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, separators=(",", ":")))


def _generate_sine_wav(path: Path) -> None:
    """Create a simple sine wave WAV file for testing audio playback."""
    n_samples = int(DURATION_S * SR)
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        for i in range(n_samples):
            t = i / SR
            # Musical: A4 (440Hz) with harmonics, volume envelope
            envelope = 0.5 * (1 + math.sin(2 * math.pi * 0.3 * t))  # slow swell
            val = envelope * (
                0.5 * math.sin(2 * math.pi * 440 * t)
                + 0.3 * math.sin(2 * math.pi * 880 * t)
                + 0.2 * math.sin(2 * math.pi * 1320 * t)
            )
            sample = int(max(-32767, min(32767, val * 32767)))
            wf.writeframes(struct.pack("<h", sample))


def _generate_r3() -> list[list[float]]:
    """Generate synthetic R³ data: slow oscillations per group."""
    r3 = np.zeros((T_LOD, R3_DIM), dtype=np.float32)
    freqs = [0.5, 1.0, 2.0, 3.0, 0.3, 1.5, 2.5, 0.8, 1.2, 0.6, 1.8]
    group_bounds = [(0,7),(7,12),(12,21),(21,25),(25,49),(49,65),(65,75),(75,87),(87,94),(94,114),(114,128)]

    for gi, (start, end) in enumerate(group_bounds):
        freq = freqs[gi]
        for d in range(start, end):
            phase = d * 0.3
            for t in range(T_LOD):
                ts = t / FRAME_RATE
                r3[t, d] = 0.5 + 0.4 * math.sin(2 * math.pi * freq * ts + phase)

    return np.round(r3, 4).tolist()


def _generate_nucleus_output() -> list[list[float]]:
    """Generate synthetic BCH 12D output."""
    output = np.zeros((T_LOD, 12), dtype=np.float32)
    for d in range(12):
        freq = 0.5 + d * 0.2
        phase = d * 0.5
        for t in range(T_LOD):
            ts = t / FRAME_RATE
            output[t, d] = 0.5 + 0.35 * math.sin(2 * math.pi * freq * ts + phase)
    return np.round(output, 4).tolist()


def _generate_ram() -> list[list[float]]:
    """Generate synthetic RAM (T, 26) data."""
    ram = np.zeros((T_LOD, NUM_REGIONS), dtype=np.float32)
    # Active regions for BCH: AN(22), CN(23), IC(21), MGB(18), A1_HG(0), STG(1)
    active = {0: 0.7, 1: 0.4, 18: 0.6, 21: 0.9, 22: 0.7, 23: 0.5}
    for idx, base in active.items():
        for t in range(T_LOD):
            ts = t / FRAME_RATE
            ram[t, idx] = base * (0.5 + 0.5 * math.sin(2 * math.pi * 0.3 * ts + idx))
    return np.round(np.clip(ram, 0, 1), 4).tolist()


def _generate_neuro() -> list[list[float]]:
    """Generate synthetic neurochemical (T, 4) data."""
    neuro = np.full((T_LOD, NUM_NEURO), 0.5, dtype=np.float32)
    # DA oscillates around 0.5-0.7
    for t in range(T_LOD):
        ts = t / FRAME_RATE
        neuro[t, 0] = 0.55 + 0.15 * math.sin(2 * math.pi * 0.2 * ts)  # DA
        neuro[t, 1] = 0.50 + 0.05 * math.sin(2 * math.pi * 0.5 * ts)  # NE
        neuro[t, 2] = 0.48 + 0.02 * math.sin(2 * math.pi * 0.1 * ts)  # OPI
        neuro[t, 3] = 0.52 + 0.08 * math.sin(2 * math.pi * 0.15 * ts) # 5HT
    return np.round(np.clip(neuro, 0, 1), 4).tolist()


def _generate_psi() -> dict[str, list[list[float]]]:
    """Generate synthetic PsiState data."""
    domains = {
        "affect": 4, "emotion": 7, "aesthetic": 5,
        "bodily": 4, "cognitive": 4, "temporal": 4,
    }
    result = {}
    for name, ndim in domains.items():
        data = np.zeros((T_LOD, ndim), dtype=np.float32)
        for d in range(ndim):
            freq = 0.2 + d * 0.15
            for t in range(T_LOD):
                ts = t / FRAME_RATE
                data[t, d] = 0.5 + 0.3 * math.sin(2 * math.pi * freq * ts + d)
        result[name] = np.round(np.clip(data, 0, 1), 4).tolist()
    return result


def _generate_h3() -> dict[str, list[float]]:
    """Generate synthetic H³ sparse features for BCH demands."""
    # BCH demands 16 tuples — use the actual demand specs
    demands = [
        (0,0,0,2),(0,3,1,2),(0,6,18,0),
        (2,0,0,2),(2,3,1,2),
        (3,0,0,2),(3,6,0,2),
        (5,0,0,2),(5,3,1,2),
        (6,0,0,2),(6,3,1,2),
        (18,0,0,2),(19,0,0,2),(20,0,0,2),
        (41,3,0,0),(41,6,1,0),
    ]
    h3 = {}
    for i, (r, h, m, l) in enumerate(demands):
        key = f"{r}_{h}_{m}_{l}"
        freq = 0.3 + i * 0.1
        data = []
        for t in range(T_LOD):
            ts = t / FRAME_RATE
            data.append(round(0.5 + 0.4 * math.sin(2 * math.pi * freq * ts + i), 4))
        h3[key] = data
    return h3


def main():
    print(f"[Synthetic] Generating test experiment: {SLUG}")
    print(f"  Duration: {DURATION_S}s, T_full={T_FULL}, T_lod={T_LOD}, stride={STRIDE}")

    EXP_DIR.mkdir(parents=True, exist_ok=True)
    (EXP_DIR / "nuclei").mkdir(exist_ok=True)

    # Audio
    print("  Generating audio...")
    _generate_sine_wav(EXP_DIR / "audio.wav")

    # R3
    print("  Generating R³...")
    _write_json(EXP_DIR / "r3.json", _generate_r3())

    # RAM
    print("  Generating RAM...")
    _write_json(EXP_DIR / "ram.json", _generate_ram())

    # Neuro
    print("  Generating neuro...")
    _write_json(EXP_DIR / "neuro.json", _generate_neuro())

    # Psi
    print("  Generating Ψ³...")
    _write_json(EXP_DIR / "psi.json", _generate_psi())

    # H3
    print("  Generating H³...")
    _write_json(EXP_DIR / "h3.json", _generate_h3())

    # BCH nucleus
    print("  Generating BCH nucleus data...")
    bch_data = {
        "name": "BCH",
        "full_name": "Brainstem Consonance Hierarchy",
        "unit": "SPU",
        "role": "relay",
        "depth": 0,
        "output_dim": 12,
        "output": _generate_nucleus_output(),
        "dimension_names": [
            "f01_nps", "f02_harmonicity", "f03_hierarchy", "f04_ffr_behavior",
            "nps_t", "harm_interval",
            "consonance_signal", "template_match", "neural_pitch",
            "consonance_pred", "pitch_propagation", "interval_expect",
        ],
        "layers": [
            {"code": "E", "name": "Extraction", "start": 0, "end": 4, "scope": "internal",
             "dim_names": ["f01_nps", "f02_harmonicity", "f03_hierarchy", "f04_ffr_behavior"]},
            {"code": "M", "name": "Mechanism", "start": 4, "end": 6, "scope": "internal",
             "dim_names": ["nps_t", "harm_interval"]},
            {"code": "P", "name": "Cognitive", "start": 6, "end": 9, "scope": "external",
             "dim_names": ["consonance_signal", "template_match", "neural_pitch"]},
            {"code": "F", "name": "Forecast", "start": 9, "end": 12, "scope": "hybrid",
             "dim_names": ["consonance_pred", "pitch_propagation", "interval_expect"]},
        ],
        "region_links": [
            {"dim_name": "f01_nps", "region": "AN", "weight": 0.7, "citation": "Bidelman 2009"},
            {"dim_name": "f02_harmonicity", "region": "CN", "weight": 0.5, "citation": "Tramo 2001"},
            {"dim_name": "f01_nps", "region": "IC", "weight": 0.9, "citation": "Coffey 2016"},
            {"dim_name": "f03_hierarchy", "region": "IC", "weight": 0.85, "citation": "Bidelman 2009"},
            {"dim_name": "consonance_signal", "region": "MGB", "weight": 0.6, "citation": "Koelsch 2011"},
            {"dim_name": "pitch_propagation", "region": "A1_HG", "weight": 0.7, "citation": "Patterson 2002"},
            {"dim_name": "consonance_signal", "region": "STG", "weight": 0.4, "citation": "Griffiths 2002"},
        ],
        "neuro_links": [
            {"dim_name": "consonance_signal", "channel": 0, "channel_name": "DA",
             "effect": "produce", "weight": 0.3, "citation": "Salimpoor 2011"},
            {"dim_name": "neural_pitch", "channel": 3, "channel_name": "5HT",
             "effect": "amplify", "weight": 0.2, "citation": "Doya 2002"},
        ],
        "h3_demands": [
            {"r3_idx":0, "r3_name":"roughness", "horizon":0, "horizon_label":"5.8ms", "morph":0, "morph_name":"value", "law":2, "law_name":"integration", "purpose":"Instantaneous roughness", "citation":"Plomp & Levelt 1965"},
            {"r3_idx":0, "r3_name":"roughness", "horizon":3, "horizon_label":"46ms", "morph":1, "morph_name":"mean", "law":2, "law_name":"integration", "purpose":"Roughness at note onset", "citation":"Plomp & Levelt 1965"},
            {"r3_idx":0, "r3_name":"roughness", "horizon":6, "horizon_label":"186ms", "morph":18, "morph_name":"trend", "law":0, "law_name":"memory", "purpose":"Roughness trend", "citation":"Vassilakis 2005"},
            {"r3_idx":2, "r3_name":"helmholtz_kang", "horizon":0, "horizon_label":"5.8ms", "morph":0, "morph_name":"value", "law":2, "law_name":"integration", "purpose":"Helmholtz consonance", "citation":"Helmholtz 1863"},
            {"r3_idx":2, "r3_name":"helmholtz_kang", "horizon":3, "horizon_label":"46ms", "morph":1, "morph_name":"mean", "law":2, "law_name":"integration", "purpose":"Note-level consonance", "citation":"Helmholtz 1863"},
            {"r3_idx":3, "r3_name":"stumpf_fusion", "horizon":0, "horizon_label":"5.8ms", "morph":0, "morph_name":"value", "law":2, "law_name":"integration", "purpose":"Tonal fusion", "citation":"Stumpf 1898"},
            {"r3_idx":3, "r3_name":"stumpf_fusion", "horizon":6, "horizon_label":"186ms", "morph":0, "morph_name":"value", "law":2, "law_name":"integration", "purpose":"Phrase-level fusion", "citation":"Stumpf 1898"},
            {"r3_idx":5, "r3_name":"inharmonicity", "horizon":0, "horizon_label":"5.8ms", "morph":0, "morph_name":"value", "law":2, "law_name":"integration", "purpose":"Spectral inharmonicity", "citation":"Rasch & Plomp 1999"},
            {"r3_idx":5, "r3_name":"inharmonicity", "horizon":3, "horizon_label":"46ms", "morph":1, "morph_name":"mean", "law":2, "law_name":"integration", "purpose":"Note inharmonicity", "citation":"Rasch & Plomp 1999"},
            {"r3_idx":6, "r3_name":"harmonic_deviation", "horizon":0, "horizon_label":"5.8ms", "morph":0, "morph_name":"value", "law":2, "law_name":"integration", "purpose":"Harmonic template deviation", "citation":"Terhardt 1984"},
            {"r3_idx":6, "r3_name":"harmonic_deviation", "horizon":3, "horizon_label":"46ms", "morph":1, "morph_name":"mean", "law":2, "law_name":"integration", "purpose":"Note harmonic deviation", "citation":"Terhardt 1984"},
            {"r3_idx":18, "r3_name":"tristimulus1", "horizon":0, "horizon_label":"5.8ms", "morph":0, "morph_name":"value", "law":2, "law_name":"integration", "purpose":"Fundamental energy", "citation":"Pollard & Jansson 1982"},
            {"r3_idx":19, "r3_name":"tristimulus2", "horizon":0, "horizon_label":"5.8ms", "morph":0, "morph_name":"value", "law":2, "law_name":"integration", "purpose":"Mid-partial energy", "citation":"Pollard & Jansson 1982"},
            {"r3_idx":20, "r3_name":"tristimulus3", "horizon":0, "horizon_label":"5.8ms", "morph":0, "morph_name":"value", "law":2, "law_name":"integration", "purpose":"Upper-partial energy", "citation":"Pollard & Jansson 1982"},
            {"r3_idx":41, "r3_name":"x_l5l7_0", "horizon":3, "horizon_label":"46ms", "morph":0, "morph_name":"value", "law":0, "law_name":"memory", "purpose":"Consonance-interaction memory", "citation":"McDermott 2010"},
            {"r3_idx":41, "r3_name":"x_l5l7_0", "horizon":6, "horizon_label":"186ms", "morph":1, "morph_name":"mean", "law":0, "law_name":"memory", "purpose":"Phrase interaction memory", "citation":"McDermott 2010"},
        ],
        "metadata": {
            "evidence_tier": "alpha",
            "confidence_range": [0.90, 0.95],
            "version": "2.0.0",
            "paper_count": 13,
            "citations": [
                {"author": "Bidelman", "year": 2009, "finding": "FFR encodes consonance hierarchy with r=0.84 correlation to behavioral ratings", "effect_size": "r=0.84"},
                {"author": "Tramo", "year": 2001, "finding": "Brainstem nuclei (CN, SOC, IC) process consonance before cortex", "effect_size": "d=1.2"},
                {"author": "Coffey", "year": 2016, "finding": "IC generates FFR at fundamental frequency of consonant intervals", "effect_size": "r=0.81"},
                {"author": "Bones", "year": 2014, "finding": "FFR harmonicity predicts consonance preference", "effect_size": "r=0.79"},
                {"author": "Cousineau", "year": 2012, "finding": "Amusics show reduced brainstem encoding of pitch", "effect_size": "d=0.89"},
                {"author": "Helmholtz", "year": 1863, "finding": "Beating partials theory of consonance and roughness", "effect_size": ""},
                {"author": "Plomp", "year": 1965, "finding": "Critical band model: dissonance peaks at 25% of critical bandwidth", "effect_size": ""},
                {"author": "Stumpf", "year": 1898, "finding": "Tonal fusion: consonant intervals perceived as single tones", "effect_size": ""},
                {"author": "Terhardt", "year": 1984, "finding": "Virtual pitch and harmonic template matching", "effect_size": ""},
                {"author": "Patterson", "year": 2002, "finding": "Pitch center in HG processes resolved harmonics", "effect_size": "d=0.67"},
                {"author": "McDermott", "year": 2010, "finding": "Harmonicity preference linked to neural encoding fidelity", "effect_size": "r=0.72"},
                {"author": "Salimpoor", "year": 2011, "finding": "DA release in NAcc during peak musical pleasure", "effect_size": "BP_ND 8.4%"},
                {"author": "Doya", "year": 2002, "finding": "5HT modulates temporal discount rate in reward evaluation", "effect_size": ""},
            ],
            "falsification_criteria": [
                "Pure tones (no harmonics) should NOT show consonance hierarchy effects",
                "Non-Western listeners should show same NEURAL hierarchy despite different preferences",
                "Sensorineural hearing loss should alter consonance hierarchy",
                "Removing harmonics from stimuli should reduce NPS values",
                "Brainstem lesions (IC) should abolish FFR-based consonance effects",
            ],
        },
    }
    _write_json(EXP_DIR / "nuclei" / "BCH.json", bch_data)

    # Meta
    meta = {
        "slug": SLUG,
        "title": "Synthetic Test — A440 + Harmonics",
        "duration_s": DURATION_S,
        "total_frames": T_FULL,
        "lod_frames": T_LOD,
        "lod_stride": STRIDE,
        "frame_rate": round(FRAME_RATE, 6),
        "nuclei": ["BCH"],
        "r3_dim": R3_DIM,
        "created_at": datetime.now().isoformat(),
    }
    _write_json(EXP_DIR / "meta.json", meta)

    print(f"\n[Synthetic] Done! Experiment at: {EXP_DIR}")
    print(f"  T_lod={T_LOD}, stride={STRIDE}, nuclei=['BCH']")


if __name__ == "__main__":
    main()
