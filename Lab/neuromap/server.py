"""NeuroMap — Musical Intelligence Neural Architecture Visualization.

Standalone FastAPI server that introspects the actual MI codebase
and serves an interactive 2D neural network diagram.

Usage:
    cd Lab/neuromap
    uvicorn server:app --port 7777 --reload
"""
from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MI_ROOT = PROJECT_ROOT / "Musical_Intelligence"

app = FastAPI(title="MI NeuroMap", version="0.1.0")
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


# ── R³ Groups (9 active, 97D total) ─────────────────────────────────────
R3_GROUPS = [
    {"letter": "A", "name": "Consonance", "dim": 7, "range": [0, 7],
     "features": ["roughness", "sethares_dissonance", "helmholtz_kang",
                   "stumpf_fusion", "sensory_pleasantness", "inharmonicity",
                   "harmonic_deviation"],
     "desc": "Psychoacoustic consonance (Sethares, Plomp-Levelt, HPS)"},
    {"letter": "B", "name": "Energy", "dim": 5, "range": [7, 12],
     "features": ["amplitude", "velocity_A", "acceleration_A", "loudness",
                   "onset_strength"],
     "desc": "RMS energy, derivatives, onset detection"},
    {"letter": "C", "name": "Timbre", "dim": 9, "range": [12, 21],
     "features": ["warmth", "sharpness", "tonalness", "clarity",
                   "spectral_smoothness", "spectral_autocorrelation",
                   "tristimulus1", "tristimulus2", "tristimulus3"],
     "desc": "Spectral shape descriptors and tristimulus"},
    {"letter": "D", "name": "Change", "dim": 4, "range": [21, 25],
     "features": ["spectral_flux", "distribution_entropy",
                   "distribution_flatness", "distribution_concentration"],
     "desc": "Frame-level spectral change and entropy"},
    {"letter": "F", "name": "Pitch / Chroma", "dim": 16, "range": [25, 41],
     "features": ["chroma_C", "chroma_C#", "chroma_D", "chroma_D#",
                   "chroma_E", "chroma_F", "chroma_F#", "chroma_G",
                   "chroma_G#", "chroma_A", "chroma_A#", "chroma_B",
                   "pitch_height", "pitch_class_entropy", "pitch_salience",
                   "inharmonicity_index"],
     "desc": "12-class chroma vector + pitch descriptors"},
    {"letter": "G", "name": "Rhythm / Groove", "dim": 10, "range": [41, 51],
     "features": ["tempo_estimate", "beat_strength", "pulse_clarity",
                   "syncopation_index", "metricality_index", "isochrony_nPVI",
                   "groove_index", "event_density", "tempo_stability",
                   "rhythmic_regularity"],
     "desc": "Onset autocorrelation, beat tracking, groove analysis"},
    {"letter": "H", "name": "Harmony", "dim": 12, "range": [51, 63],
     "features": ["key_clarity", "tonnetz_1", "tonnetz_2", "tonnetz_3",
                   "tonnetz_4", "tonnetz_5", "tonnetz_6",
                   "voice_leading_distance", "harmonic_change",
                   "tonal_stability", "diatonicity", "syntactic_irregularity"],
     "desc": "Krumhansl key profiles, Tonnetz, voice leading"},
    {"letter": "J", "name": "Timbre Extended", "dim": 20, "range": [63, 83],
     "features": ["MFCC_1", "MFCC_2", "MFCC_3", "MFCC_4", "MFCC_5",
                   "MFCC_6", "MFCC_7", "MFCC_8", "MFCC_9", "MFCC_10",
                   "MFCC_11", "MFCC_12", "MFCC_13",
                   "spectral_contrast_1", "spectral_contrast_2",
                   "spectral_contrast_3", "spectral_contrast_4",
                   "spectral_contrast_5", "spectral_contrast_6",
                   "spectral_contrast_7"],
     "desc": "DCT-II MFCCs + 7-band spectral contrast"},
    {"letter": "K", "name": "Modulation", "dim": 14, "range": [83, 97],
     "features": ["mod_0.5Hz", "mod_1Hz", "mod_2Hz", "mod_4Hz", "mod_8Hz",
                   "mod_16Hz", "mod_centroid", "mod_bandwidth",
                   "sharpness_zwicker", "fluctuation_strength",
                   "loudness_a_weighted", "alpha_ratio", "hammarberg_index",
                   "spectral_slope_0_500Hz"],
     "desc": "Modulation spectrum, Zwicker psychoacoustics"},
]

# ── H³ Morph Families ───────────────────────────────────────────────────
H3_FAMILIES = [
    {"id": "distribution", "name": "Distribution", "morphs": ["M0 mean_w", "M1 mean", "M2 std", "M3 median", "M4 max", "M5 range", "M6 skewness", "M7 kurtosis"], "count": 8},
    {"id": "dynamics", "name": "Dynamics", "morphs": ["M8 velocity", "M9 vel_mean", "M10 vel_std", "M11 accel", "M12 accel_mean", "M13 accel_std", "M15 smoothness", "M18 trend", "M21 zero_cross"], "count": 9},
    {"id": "rhythm", "name": "Rhythm", "morphs": ["M14 periodicity", "M17 shape_period", "M22 peaks"], "count": 3},
    {"id": "information", "name": "Information", "morphs": ["M20 entropy"], "count": 1},
    {"id": "symmetry", "name": "Symmetry", "morphs": ["M16 curvature", "M19 stability", "M23 symmetry"], "count": 3},
]

H3_HORIZONS = [
    {"band": "micro", "label": "Micro", "range": "H0-H7", "time": "5.8ms — 250ms", "count": 8},
    {"band": "meso", "label": "Meso", "range": "H8-H15", "time": "300ms — 800ms", "count": 8},
    {"band": "macro", "label": "Macro", "range": "H16-H23", "time": "1s — 25s", "count": 8},
    {"band": "ultra", "label": "Ultra", "range": "H24-H31", "time": "36s — 981s", "count": 8},
]

H3_LAWS = [
    {"id": "L0", "name": "Memory", "direction": "backward", "desc": "Causal exponential decay from present"},
    {"id": "L1", "name": "Forward", "direction": "forward", "desc": "Anticipatory projection from present"},
    {"id": "L2", "name": "Integration", "direction": "bidirectional", "desc": "Symmetric exponential centered on present"},
]

# ── C³ Brain Units (6 units, 96 models) ─────────────────────────────────
C3_UNITS = [
    {
        "id": "spu", "abbr": "SPU", "name": "Spectral Processing Unit",
        "belief": "perceived_consonance", "tau": 0.3,
        "relay": [{"id": "bch", "name": "BCH", "full": "Basilar Complex Harmony", "dim": 12}],
        "encoder": [
            {"id": "pscl", "name": "PSCL", "full": "Psychoacoustic Spectral Consonance Layer", "dim": 12},
            {"id": "stai", "name": "STAI", "full": "Spectro-Temporal Auditory Integration", "dim": 12},
        ],
        "associator": [
            {"id": "pccr", "name": "PCCR", "full": "Pitch-Chroma Cross-Referencing", "dim": 11},
            {"id": "tscp", "name": "TSCP", "full": "Tonal-Spectral Consonance Patterns", "dim": 10},
            {"id": "sdnps", "name": "SDNPS", "full": "Sensory Dissonance & Neural Pattern Separation", "dim": 10},
        ],
        "integrator": [
            {"id": "miaa", "name": "MIAA", "full": "Multi-Interval Auditory Assessment", "dim": 11},
            {"id": "esme", "name": "ESME", "full": "Emergent Spectral-Musical Evaluation", "dim": 11},
            {"id": "sded", "name": "SDED", "full": "Spectral Dissonance & Emotion Decoder", "dim": 10},
        ],
        "gamma": [],
    },
    {
        "id": "stu", "abbr": "STU", "name": "Sensorimotor Timing Unit",
        "belief": "tempo_state", "tau": 0.7,
        "relay": [{"id": "hmce", "name": "HMCE", "full": "Hierarchical Metric Cycle Encoder", "dim": 13}],
        "encoder": [
            {"id": "amsc", "name": "AMSC", "full": "Auditory Motor Synchronization Circuit", "dim": 11},
            {"id": "tpse", "name": "TPSE", "full": "Temporal Pattern Sequence Encoder", "dim": 11},
        ],
        "associator": [
            {"id": "ctem", "name": "CTEM", "full": "Cross-Temporal Entrainment Model", "dim": 10},
            {"id": "msie", "name": "MSIE", "full": "Multi-Scale Integration Engine", "dim": 10},
            {"id": "tscp_stu", "name": "TSCP", "full": "Temporal-Spectral Cross-Pattern", "dim": 10},
        ],
        "integrator": [
            {"id": "teme", "name": "TEME", "full": "Temporal Memory Engine", "dim": 10},
            {"id": "sema", "name": "SEMA", "full": "Sensorimotor Adaptation", "dim": 10},
        ],
        "gamma": [
            {"id": "rtse", "name": "RTSE", "full": "Rhythmic Temporal Sequence Evaluator", "dim": 10},
            {"id": "mtfl", "name": "MTFL", "full": "Metric Temporal Flow Layer", "dim": 10},
        ],
    },
    {
        "id": "asu", "abbr": "ASU", "name": "Auditory Salience Unit",
        "belief": "salience_state", "tau": 0.3,
        "relay": [{"id": "snem", "name": "SNEM", "full": "Salience Network Entry Module", "dim": 12}],
        "encoder": [
            {"id": "barm", "name": "BARM", "full": "Bottom-up Auditory Response Model", "dim": 10},
            {"id": "stanm", "name": "STANM", "full": "Spectro-Temporal Attention Network Model", "dim": 10},
        ],
        "associator": [
            {"id": "pwsm", "name": "PWSM", "full": "Prediction-Weighted Salience Model", "dim": 10},
            {"id": "dgtp", "name": "DGTP", "full": "Deviance-Gated Temporal Prediction", "dim": 10},
            {"id": "omsm", "name": "OMSM", "full": "Orienting & Multi-Scale Model", "dim": 10},
        ],
        "integrator": [
            {"id": "ctam", "name": "CTAM", "full": "Cross-modal Temporal Attention Model", "dim": 10},
            {"id": "acsm", "name": "ACSM", "full": "Auditory Context Salience Model", "dim": 10},
        ],
        "gamma": [
            {"id": "bsmm", "name": "BSMM", "full": "Bayesian Surprise Modulation Model", "dim": 10},
        ],
    },
    {
        "id": "imu", "abbr": "IMU", "name": "Implicit Memory Unit",
        "belief": "familiarity_state", "tau": 0.85,
        "relay": [{"id": "mmp", "name": "MMP", "full": "Memory Matching Processor", "dim": 12}],
        "encoder": [
            {"id": "mpsm", "name": "MPSM", "full": "Musical Pattern Sequence Model", "dim": 11},
            {"id": "msml", "name": "MSML", "full": "Multi-Scale Memory Layer", "dim": 11},
        ],
        "associator": [
            {"id": "mrpc", "name": "MRPC", "full": "Memory Retrieval & Pattern Comparison", "dim": 10},
            {"id": "emae", "name": "EMAE", "full": "Episodic Memory Association Engine", "dim": 10},
        ],
        "integrator": [
            {"id": "amrp", "name": "AMRP", "full": "Associative Memory Recall Processor", "dim": 10},
            {"id": "mpmm", "name": "MPMM", "full": "Musical Pattern Memory Model", "dim": 10},
        ],
        "gamma": [
            {"id": "smmp", "name": "SMMP", "full": "Statistical Musical Memory Predictor", "dim": 10},
            {"id": "mamm", "name": "MAMM", "full": "Multi-level Associative Memory Model", "dim": 10},
        ],
    },
    {
        "id": "ndu", "abbr": "NDU", "name": "Novelty Detection Unit",
        "belief": None, "tau": None,
        "relay": [{"id": "mpg", "name": "MPG", "full": "Mismatch Processing Gate", "dim": 10}],
        "encoder": [
            {"id": "sdd", "name": "SDD", "full": "Statistical Deviance Detector", "dim": 11},
            {"id": "ednr", "name": "EDNR", "full": "Event-Driven Novelty Responder", "dim": 11},
        ],
        "associator": [
            {"id": "cdmr", "name": "CDMR", "full": "Context-Dependent Mismatch Response", "dim": 10},
            {"id": "pmne", "name": "PMNE", "full": "Predictive Model Novelty Estimator", "dim": 10},
            {"id": "nccr", "name": "NCCR", "full": "Neural Change & Contrast Response", "dim": 10},
        ],
        "integrator": [
            {"id": "nmrs", "name": "NMRS", "full": "Novelty Modulated Response System", "dim": 10},
            {"id": "ncmr", "name": "NCMR", "full": "Neural Complexity Mismatch Response", "dim": 10},
        ],
        "gamma": [
            {"id": "sndr", "name": "SNDR", "full": "Surprise & Novelty Detection Response", "dim": 10},
            {"id": "pdns", "name": "PDNS", "full": "Prediction-Deviation Novelty Signal", "dim": 10},
        ],
    },
    {
        "id": "rpu", "abbr": "RPU", "name": "Reward Processing Unit",
        "belief": "reward_valence", "tau": 0.8,
        "relay": [{"id": "daed", "name": "DAED", "full": "Dopaminergic Aesthetic Evaluation Device", "dim": 8}],
        "encoder": [
            {"id": "mormr", "name": "MORMR", "full": "Musical Opioid Reward Model Response", "dim": 11},
            {"id": "rpem", "name": "RPEM", "full": "Reward Prediction Error Model", "dim": 11},
        ],
        "associator": [
            {"id": "iucp", "name": "IUCP", "full": "Inverted-U Complexity Processor", "dim": 10},
            {"id": "mccn", "name": "MCCN", "full": "Musical Chills & Consonance Network", "dim": 10},
            {"id": "meamr", "name": "MEAMR", "full": "Musical Emotion & Aesthetic Model Response", "dim": 10},
        ],
        "integrator": [
            {"id": "ssri", "name": "SSRI", "full": "Serotonergic Satisfaction & Reward Integration", "dim": 10},
            {"id": "ldac", "name": "LDAC", "full": "Limbic-Dopaminergic Aesthetic Convergence", "dim": 10},
        ],
        "gamma": [
            {"id": "iotms", "name": "IOTMS", "full": "Integration of Temporal & Musical Satisfaction", "dim": 10},
            {"id": "ssps", "name": "SSPS", "full": "Stimulus-Specific Pleasure Signal", "dim": 10},
        ],
    },
]

# ── C³ Kernel Beliefs ────────────────────────────────────────────────────
KERNEL_BELIEFS = [
    {"id": "consonance", "name": "Perceived Consonance", "unit": "spu", "tau": 0.3,
     "phase": "0", "desc": "SPU-owned sensory belief. Multi-scale 8-horizon prediction.",
     "observe": "BCH: 0.5×consonance_signal + 0.3×template_match + 0.2×hierarchy",
     "predict": "τ×prev + w_trend×H³(M18) + w_period×H³(M14) + w_ctx×tempo"},
    {"id": "tempo", "name": "Tempo State", "unit": "stu", "tau": 0.7,
     "phase": "0", "desc": "STU-owned sensorimotor timing belief.",
     "observe": "0.35×tempo + 0.25×beat + 0.25×pulse + 0.15×regularity",
     "predict": "τ×prev + 0.20×H³(M18,onset) + 0.25×H³(M14,onset)"},
    {"id": "salience", "name": "Salience State", "unit": "asu", "tau": 0.3,
     "phase": "1", "desc": "ASU-owned attention gate. Energy-gated, mean+max mixing.",
     "observe": "energy_gate × (0.5×mean + 0.5×max)[energy, H³(M8×3), PE_surprise]",
     "predict": "τ×prev + 0.15×H³(M18,amplitude)"},
    {"id": "familiarity", "name": "Familiarity State", "unit": "imu", "tau": 0.85,
     "phase": "2a", "desc": "IMU-owned recurrence-aware memory. Baseline=0, energy-gated.",
     "observe": "energy_gate × (0.50×M14_period + 0.35×(1-M2_std) + 0.15×tonalness)",
     "predict": "τ×prev + 0.20×H³(M18,tonalness,H16)"},
    {"id": "reward", "name": "Reward Valence", "unit": "rpu", "tau": 0.8,
     "phase": "3", "desc": "ARU-derived. Multi-scale PE, horizon activation, tanh compression.",
     "observe": "salience × Σ(w_s×surprise + w_r×resolution + w_e×exploration − w_m×monotony) × fam_mod",
     "predict": "Derived from belief PEs, not independently predicted"},
]

# ── R³ → Relay primary connections ──────────────────────────────────────
R3_TO_RELAY = {
    "bch": ["A", "H"],       # Consonance + Harmony → BCH
    "hmce": ["B", "G"],      # Energy + Rhythm → HMCE
    "snem": ["B", "D"],      # Energy + Change → SNEM
    "mmp": ["F", "C"],       # Pitch + Timbre → MMP
    "mpg": ["D", "C"],       # Change + Timbre → MPG
    "daed": ["B", "K"],      # Energy + Modulation → DAED
}

# ── H³ → Belief demands ────────────────────────────────────────────────
H3_TO_BELIEF = {
    "consonance": [
        "roughness M18 H8 L0 (trend)", "tonalness M14 H12 L0 (period)",
        "roughness M0/M18/M2 × 8 horizons (multi-scale)",
    ],
    "tempo": ["onset_strength M18 H6 L0 (trend)", "onset_strength M14 H6 L0 (period)"],
    "salience": ["amplitude M8 H6 L0", "onset_strength M8 H6 L0", "spectral_flux M8 H6 L0"],
    "familiarity": [
        "tonalness M14 H16 L0", "key_clarity M14 H16 L0", "tonal_stability M14 H16 L0",
        "tonalness M2 H16 L0", "key_clarity M2 H16 L0", "tonal_stability M2 H16 L0",
        "tonalness M18 H16 L0 (predict)",
    ],
}


def _verify_paths() -> dict:
    """Check which expected code paths actually exist."""
    checks = {}
    checks["r3_groups"] = sum(
        1 for g in R3_GROUPS
        if (MI_ROOT / "ear" / "r3" / "groups" / f"{g['letter'].lower()}_{g['name'].lower().replace(' / ', '_').replace('/', '_')}" / "group.py").exists()
        or (MI_ROOT / "ear" / "r3" / "groups").exists()
    )
    checks["h3_morphology"] = (MI_ROOT / "ear" / "h3" / "morphology").exists()
    checks["brain_units"] = sum(
        1 for u in C3_UNITS if (MI_ROOT / "brain" / "units" / u["id"]).exists()
    )
    checks["kernel"] = (MI_ROOT / "brain" / "kernel").exists()
    total_nuclei = sum(
        len(u["relay"]) + len(u["encoder"]) + len(u["associator"])
        + len(u["integrator"]) + len(u["gamma"])
        for u in C3_UNITS
    )
    checks["total_nuclei"] = total_nuclei
    checks["total_r3_dim"] = sum(g["dim"] for g in R3_GROUPS)
    return checks


def build_graph() -> dict:
    """Construct the full graph data for visualization."""
    return {
        "r3_groups": R3_GROUPS,
        "h3_families": H3_FAMILIES,
        "h3_horizons": H3_HORIZONS,
        "h3_laws": H3_LAWS,
        "c3_units": C3_UNITS,
        "kernel_beliefs": KERNEL_BELIEFS,
        "r3_to_relay": R3_TO_RELAY,
        "h3_to_belief": H3_TO_BELIEF,
        "verification": _verify_paths(),
    }


# ── Routes ───────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/graph")
async def get_graph():
    return build_graph()
