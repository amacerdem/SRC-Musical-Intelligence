"""Deep F1 Test Suite — Comprehensive validation of F1 Sensory Processing beliefs.

Tests the full R³→H³→C³ pipeline end-to-end for all 17 F1 beliefs across:
  1. Structural validation (registration, attributes, shapes)
  2. Full consonance hierarchy (9 intervals, Sethares/Plomp-Levelt)
  3. Pitch processing gradient (harmonic > inharmonic > noise > silence)
  4. Octave equivalence (multi-octave chroma invariance)
  5. Timbral differentiation (different complex tones)
  6. Cross-belief consistency (correlated signal pairs)
  7. Determinism (identical runs)
  8. Boundary conditions (silence, DC, Nyquist, extreme lengths)
  9. Range validity (exhaustive [0,1] check)
 10. Effect sizes (Cohen's d for supplementary materials)

Run:
    cd "/Volumes/SRC-9/SRC Musical Intelligence"
    python Tests/deep_f1_test.py
"""
from __future__ import annotations

import math
import sys
import time
import traceback
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

import torch
from torch import Tensor

# Ensure project root on path
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from Tests.micro_beliefs.pipeline_runner import MicroBeliefRunner

# ======================================================================
# Test infrastructure (same pattern as deep_r3_test.py)
# ======================================================================

WARMUP_FRAMES = 50
SR = 44_100


@dataclass
class TestResult:
    name: str
    passed: bool
    message: str = ""
    duration_ms: float = 0.0


@dataclass
class TestSuite:
    name: str
    results: List[TestResult] = field(default_factory=list)

    def add(self, name: str, passed: bool, message: str = "", duration_ms: float = 0.0):
        self.results.append(TestResult(name, passed, message, duration_ms))

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if not r.passed)

    @property
    def total(self) -> int:
        return len(self.results)

    def report(self) -> str:
        lines = [f"\n{'='*70}", f"  {self.name}  ({self.passed}/{self.total} passed)", f"{'='*70}"]
        for r in self.results:
            icon = "PASS" if r.passed else "FAIL"
            dur = f"  [{r.duration_ms:.0f}ms]" if r.duration_ms > 0 else ""
            lines.append(f"  [{icon}] {r.name}{dur}")
            if r.message and not r.passed:
                for line in r.message.split("\n"):
                    lines.append(f"         {line}")
        return "\n".join(lines)


def timed(fn):
    t0 = time.perf_counter()
    result = fn()
    dt = (time.perf_counter() - t0) * 1000
    return result, dt


# ======================================================================
# Audio synthesis helpers
# ======================================================================

C2 = 65.41
C3 = 130.81
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
C6 = 1046.50


def midi_to_hz(midi: int) -> float:
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


def sine_tone(freq_hz: float, duration_s: float = 2.0, amp: float = 0.5) -> Tensor:
    N = int(SR * duration_s)
    t = torch.linspace(0, duration_s, N, dtype=torch.float32)
    return (amp * torch.sin(2 * math.pi * freq_hz * t)).unsqueeze(0)


def harmonic_complex(f0: float, n_harm: int = 8, dur: float = 2.0,
                     amp: float = 0.3) -> Tensor:
    N = int(SR * dur)
    wav = torch.zeros(1, N, dtype=torch.float32)
    for n in range(1, n_harm + 1):
        wav = wav + sine_tone(f0 * n, dur, amp / n)
    return wav


def inharmonic_complex(f0: float, n_part: int = 8, stretch: float = 1.15,
                       dur: float = 2.0, amp: float = 0.3) -> Tensor:
    N = int(SR * dur)
    wav = torch.zeros(1, N, dtype=torch.float32)
    for n in range(1, n_part + 1):
        freq = f0 * (n ** stretch)
        if freq < SR / 2:
            wav = wav + sine_tone(freq, dur, amp / n)
    return wav


def noise(dur: float = 2.0, amp: float = 0.3, seed: int = 999) -> Tensor:
    N = int(SR * dur)
    gen = torch.Generator().manual_seed(seed)
    return amp * torch.randn(1, N, generator=gen)


def silence(dur: float = 2.0) -> Tensor:
    return torch.zeros(1, int(SR * dur), dtype=torch.float32)


def rich_dyad(f1: float, f2: float, n_harm: int = 6, dur: float = 2.0,
              amp: float = 0.2) -> Tensor:
    return harmonic_complex(f1, n_harm, dur, amp) + harmonic_complex(f2, n_harm, dur, amp)


def crossfade(a: Tensor, b: Tensor, dur: float = 4.0) -> Tensor:
    N = int(SR * dur)
    a = a[:, :N] if a.shape[-1] >= N else torch.cat([a, torch.zeros(1, N - a.shape[-1])], dim=-1)
    b = b[:, :N] if b.shape[-1] >= N else torch.cat([b, torch.zeros(1, N - b.shape[-1])], dim=-1)
    fade = torch.linspace(0, 1, N).unsqueeze(0)
    return (1 - fade) * a + fade * b


# ======================================================================
# Helpers
# ======================================================================

def trimmed_mean(t: Tensor) -> float:
    """Mean after warmup trim."""
    if t.shape[-1] > WARMUP_FRAMES * 2:
        return t[:, WARMUP_FRAMES:].mean().item()
    return t.mean().item()


def trimmed_std(t: Tensor) -> float:
    if t.shape[-1] > WARMUP_FRAMES * 2:
        return t[:, WARMUP_FRAMES:].std().item()
    return t.std().item()


def cohens_d(a: Tensor, b: Tensor) -> float:
    """Compute Cohen's d between two belief time-series (after warmup)."""
    ta = a[:, WARMUP_FRAMES:].flatten() if a.shape[-1] > WARMUP_FRAMES * 2 else a.flatten()
    tb = b[:, WARMUP_FRAMES:].flatten() if b.shape[-1] > WARMUP_FRAMES * 2 else b.flatten()
    ma, mb = ta.mean().item(), tb.mean().item()
    sa, sb = ta.std().item(), tb.std().item()
    pooled = math.sqrt((sa**2 + sb**2) / 2) if (sa + sb) > 0 else 1e-8
    return (ma - mb) / max(pooled, 1e-8)


ALL_F1_BELIEFS = [
    "harmonic_stability", "interval_quality", "harmonic_template_match",
    "consonance_trajectory", "pitch_prominence", "pitch_continuation",
    "pitch_identity", "octave_equivalence", "timbral_character",
    "imagery_recognition", "melodic_contour_tracking", "contour_continuation",
    "spectral_complexity", "consonance_salience_gradient", "aesthetic_quality",
    "spectral_temporal_synergy", "reward_response_pred",
]

CORE_BELIEFS = {
    "harmonic_stability": 0.3,
    "pitch_prominence": 0.35,
    "pitch_identity": 0.4,
    "timbral_character": 0.5,
    "aesthetic_quality": 0.4,
}

APPRAISAL_BELIEFS = [
    "interval_quality", "harmonic_template_match", "octave_equivalence",
    "melodic_contour_tracking", "spectral_complexity",
    "consonance_salience_gradient", "spectral_temporal_synergy",
]

ANTICIPATION_BELIEFS = [
    "consonance_trajectory", "pitch_continuation", "imagery_recognition",
    "contour_continuation", "reward_response_pred",
]

BELIEF_MECHANISMS = {
    "harmonic_stability": "BCH", "interval_quality": "BCH",
    "harmonic_template_match": "BCH", "consonance_trajectory": "BCH",
    "pitch_prominence": "PSCL", "pitch_continuation": "PSCL",
    "pitch_identity": "PCCR", "octave_equivalence": "PCCR",
    "timbral_character": "MIAA", "imagery_recognition": "MIAA",
    "melodic_contour_tracking": "MPG", "contour_continuation": "MPG",
    "spectral_complexity": "SDED",
    "consonance_salience_gradient": "CSG",
    "aesthetic_quality": "STAI", "spectral_temporal_synergy": "STAI",
    "reward_response_pred": "STAI",
}

# Consonance hierarchy intervals (root = C4)
INTERVALS = {
    "P1":  (C4, C4),       # Unison
    "P8":  (C4, C5),       # Octave
    "P5":  (C4, G4),       # Perfect fifth
    "P4":  (C4, F4),       # Perfect fourth
    "M3":  (C4, E4),       # Major third
    "m3":  (C4, Eb4),      # Minor third
    "m6":  (C4, Ab4),      # Minor sixth
    "TT":  (C4, Fsharp4),  # Tritone
    "m2":  (C4, Db4),      # Minor second
}

CONSONANCE_ORDER = ["P1", "P8", "P5", "P4", "M3", "m3", "m6", "TT", "m2"]


# ======================================================================
# SUITE 1: Structural Validation
# ======================================================================

def test_structural(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("1. Structural Validation")

    # 1.1: All 17 beliefs registered
    available = set(runner.belief_names)
    f1_available = [b for b in ALL_F1_BELIEFS if b in available]
    missing = [b for b in ALL_F1_BELIEFS if b not in available]
    suite.add("17 F1 beliefs registered",
              len(f1_available) == 17,
              f"Found {len(f1_available)}/17, missing: {missing}" if missing else "All 17 found")

    # 1.2: Each belief has correct FUNCTION
    for name in f1_available:
        belief = runner._beliefs_by_name[name]
        suite.add(f"{name}: FUNCTION=F1",
                  belief.FUNCTION == "F1",
                  f"Got: {belief.FUNCTION}")

    # 1.3: Each belief has correct MECHANISM
    for name in f1_available:
        belief = runner._beliefs_by_name[name]
        expected_mech = BELIEF_MECHANISMS.get(name)
        suite.add(f"{name}: MECHANISM={expected_mech}",
                  belief.MECHANISM == expected_mech,
                  f"Got: {belief.MECHANISM}")

    # 1.4: Core beliefs have TAU attribute with correct value
    from Musical_Intelligence.contracts.bases.belief import CoreBelief
    for name, expected_tau in CORE_BELIEFS.items():
        if name not in available:
            suite.add(f"{name}: is CoreBelief", False, "Not registered")
            continue
        belief = runner._beliefs_by_name[name]
        is_core = isinstance(belief, CoreBelief)
        suite.add(f"{name}: is CoreBelief", is_core,
                  f"Type: {type(belief).__bases__[0].__name__}")
        if is_core:
            suite.add(f"{name}: TAU={expected_tau}",
                      abs(belief.TAU - expected_tau) < 1e-6,
                      f"Got: {belief.TAU}")

    # 1.5: observe() returns correct shape
    audio = harmonic_complex(C4, 8, 2.0)
    results = runner.run(audio, ALL_F1_BELIEFS)
    for name in f1_available:
        if name in results:
            shape = results[name].shape
            suite.add(f"{name}: observe() shape (1, T)",
                      len(shape) == 2 and shape[0] == 1 and shape[1] > 0,
                      f"Shape: {tuple(shape)}")

    # 1.6: Mechanism depth ordering BCH(0) < PSCL(1) < PCCR(2)
    depths = {}
    for m in runner.nuclei:
        if m.NAME in ("BCH", "PSCL", "PCCR"):
            depths[m.NAME] = m.PROCESSING_DEPTH
    if len(depths) == 3:
        suite.add("BCH depth < PSCL depth",
                  depths["BCH"] < depths["PSCL"],
                  f"BCH={depths['BCH']}, PSCL={depths['PSCL']}")
        suite.add("PSCL depth < PCCR depth",
                  depths["PSCL"] < depths["PCCR"],
                  f"PSCL={depths['PSCL']}, PCCR={depths['PCCR']}")

    return suite


# ======================================================================
# SUITE 2: Full Consonance Hierarchy (Sethares/Plomp-Levelt)
# ======================================================================

def test_consonance_hierarchy(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("2. Consonance Hierarchy (9 intervals)")

    # Generate all 9 interval dyads with 6 harmonics per note
    interval_results: Dict[str, Dict[str, Tensor]] = {}
    targets = ["harmonic_stability", "interval_quality", "harmonic_template_match",
               "consonance_salience_gradient"]

    for name, (f1, f2) in INTERVALS.items():
        audio = rich_dyad(f1, f2, n_harm=6, dur=3.0)
        res = runner.run(audio, targets)
        interval_results[name] = res

    # 2.1: harmonic_stability ordering — P1 > P8 > P5 > m2
    hs_means = {k: trimmed_mean(v["harmonic_stability"]) for k, v in interval_results.items()}
    group_order = [("P1", "P8"), ("P8", "P5"), ("P5", "m2")]
    for hi, lo in group_order:
        suite.add(f"HS: {hi} > {lo}",
                  hs_means[hi] > hs_means[lo],
                  f"{hi}={hs_means[hi]:.4f}, {lo}={hs_means[lo]:.4f}")

    # 2.2: P5 > P4 (important for hierarchy validation)
    suite.add("HS: P5 > P4",
              hs_means["P5"] > hs_means["P4"],
              f"P5={hs_means['P5']:.4f}, P4={hs_means['P4']:.4f}")

    # 2.3: Perfect intervals > dissonant (group separation)
    perfect_mean = (hs_means["P1"] + hs_means["P8"] + hs_means["P5"]) / 3
    dissonant_mean = (hs_means["TT"] + hs_means["m2"]) / 2
    suite.add("HS: Perfect group > dissonant group",
              perfect_mean > dissonant_mean,
              f"Perfect={perfect_mean:.4f}, Dissonant={dissonant_mean:.4f}")

    # 2.4: interval_quality — Octave > m2
    iq_means = {k: trimmed_mean(v["interval_quality"]) for k, v in interval_results.items()}
    suite.add("IQ: P8 > m2",
              iq_means["P8"] > iq_means["m2"],
              f"P8={iq_means['P8']:.4f}, m2={iq_means['m2']:.4f}")

    suite.add("IQ: P1 > m2",
              iq_means["P1"] > iq_means["m2"],
              f"P1={iq_means['P1']:.4f}, m2={iq_means['m2']:.4f}")

    # 2.5: harmonic_template_match — all intervals beat noise
    noise_htmp = trimmed_mean(runner.run(noise(3.0), ["harmonic_template_match"])["harmonic_template_match"])
    best_htmp = max(trimmed_mean(v["harmonic_template_match"]) for v in interval_results.values())
    suite.add("HTM: best interval > noise",
              best_htmp > noise_htmp,
              f"Best={best_htmp:.4f}, Noise={noise_htmp:.4f}")

    # 2.6: consonance_salience_gradient — m2 > P1 (dissonance drives salience)
    csg_means = {k: trimmed_mean(v["consonance_salience_gradient"]) for k, v in interval_results.items()}
    suite.add("CSG: m2 > P1 (dissonance → salience)",
              csg_means["m2"] > csg_means["P1"],
              f"m2={csg_means['m2']:.4f}, P1={csg_means['P1']:.4f}")

    # 2.7: Print full hierarchy table
    print("\n  Consonance hierarchy (trimmed means):")
    print(f"  {'Interval':>8}  {'HS':>7}  {'IQ':>7}  {'HTM':>7}  {'CSG':>7}")
    for iv in CONSONANCE_ORDER:
        hs = hs_means[iv]
        iq = iq_means[iv]
        htm = trimmed_mean(interval_results[iv]["harmonic_template_match"])
        csg = csg_means[iv]
        print(f"  {iv:>8}  {hs:7.4f}  {iq:7.4f}  {htm:7.4f}  {csg:7.4f}")

    return suite


# ======================================================================
# SUITE 3: Pitch Processing Gradient
# ======================================================================

def test_pitch_processing(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("3. Pitch Processing Gradient")

    targets = ["pitch_prominence", "pitch_identity"]

    # Generate stimuli: harmonic > inharmonic > noise > silence
    stims = {
        "harmonic": harmonic_complex(C4, 8, 3.0),
        "inharmonic": inharmonic_complex(C4, 8, 1.15, 3.0),
        "noise": noise(3.0),
        "silence": silence(3.0),
    }

    results = {k: runner.run(v, targets) for k, v in stims.items()}

    # 3.1: pitch_prominence gradient
    pp = {k: trimmed_mean(v["pitch_prominence"]) for k, v in results.items()}
    suite.add("PP: harmonic > inharmonic",
              pp["harmonic"] > pp["inharmonic"],
              f"H={pp['harmonic']:.4f}, I={pp['inharmonic']:.4f}")
    suite.add("PP: harmonic > noise",
              pp["harmonic"] > pp["noise"],
              f"H={pp['harmonic']:.4f}, N={pp['noise']:.4f}")
    suite.add("PP: harmonic > silence",
              pp["harmonic"] > pp["silence"],
              f"H={pp['harmonic']:.4f}, S={pp['silence']:.4f}")

    # 3.2: pitch_identity gradient
    pi = {k: trimmed_mean(v["pitch_identity"]) for k, v in results.items()}
    suite.add("PI: harmonic > noise",
              pi["harmonic"] > pi["noise"],
              f"H={pi['harmonic']:.4f}, N={pi['noise']:.4f}")
    suite.add("PI: harmonic > silence",
              pi["harmonic"] > pi["silence"],
              f"H={pi['harmonic']:.4f}, S={pi['silence']:.4f}")

    # 3.3: Register effect — different octaves should produce different pitch_identity
    reg_stims = {
        "C2": harmonic_complex(C2, 8, 3.0),
        "C4": harmonic_complex(C4, 8, 3.0),
        "C6": harmonic_complex(C6, 6, 3.0),
    }
    reg_results = {k: trimmed_mean(runner.run(v, ["pitch_identity"])["pitch_identity"])
                   for k, v in reg_stims.items()}
    # All should have non-zero pitch identity
    for name, val in reg_results.items():
        suite.add(f"PI: {name} non-zero",
                  val > 0.05,
                  f"Mean={val:.4f}")

    return suite


# ======================================================================
# SUITE 4: Octave Equivalence (Deep)
# ======================================================================

def test_octave_equivalence(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("4. Octave Equivalence")

    target = ["octave_equivalence"]

    # 4.1: Octave dyad > tritone dyad
    oct_audio = rich_dyad(C4, C5, 6, 3.0)
    tt_audio = rich_dyad(C4, Fsharp4, 6, 3.0)
    p5_audio = rich_dyad(C4, G4, 6, 3.0)

    oe_oct = trimmed_mean(runner.run(oct_audio, target)["octave_equivalence"])
    oe_tt = trimmed_mean(runner.run(tt_audio, target)["octave_equivalence"])
    oe_p5 = trimmed_mean(runner.run(p5_audio, target)["octave_equivalence"])

    suite.add("OE: octave > tritone",
              oe_oct > oe_tt,
              f"Octave={oe_oct:.4f}, TT={oe_tt:.4f}")
    suite.add("OE: octave > fifth",
              oe_oct > oe_p5,
              f"Octave={oe_oct:.4f}, P5={oe_p5:.4f}")

    # 4.2: Multi-octave chroma invariance — C3/C4, C4/C5, C5/C6 all high
    octave_pairs = {
        "C3-C4": rich_dyad(C3, C4, 6, 3.0),
        "C4-C5": rich_dyad(C4, C5, 6, 3.0),
    }
    for name, audio in octave_pairs.items():
        oe = trimmed_mean(runner.run(audio, target)["octave_equivalence"])
        suite.add(f"OE: {name} > tritone",
                  oe > oe_tt,
                  f"{name}={oe:.4f}, TT={oe_tt:.4f}")

    # 4.3: Non-octave intervals should NOT score as high as octave
    non_octave = {
        "m2": rich_dyad(C4, Db4, 6, 3.0),
        "P5": p5_audio,
    }
    for name, audio in non_octave.items():
        oe = trimmed_mean(runner.run(audio, target)["octave_equivalence"])
        suite.add(f"OE: octave > {name}",
                  oe_oct > oe,
                  f"Octave={oe_oct:.4f}, {name}={oe:.4f}")

    return suite


# ======================================================================
# SUITE 5: Timbral Differentiation
# ======================================================================

def test_timbral(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("5. Timbral Differentiation")

    target = ["timbral_character"]

    # Different timbres at the same pitch (C4)
    # "Piano-like": rich harmonic complex with 12 overtones
    piano_like = harmonic_complex(C4, 12, 3.0, 0.3)
    # "Flute-like": few harmonics, strong fundamental
    flute_like = harmonic_complex(C4, 3, 3.0, 0.4)
    # "Bell-like": inharmonic partials
    bell_like = inharmonic_complex(C4, 8, 1.12, 3.0, 0.3)

    tc_piano = trimmed_mean(runner.run(piano_like, target)["timbral_character"])
    tc_flute = trimmed_mean(runner.run(flute_like, target)["timbral_character"])
    tc_bell = trimmed_mean(runner.run(bell_like, target)["timbral_character"])
    tc_silence = trimmed_mean(runner.run(silence(3.0), target)["timbral_character"])

    # 5.1: All timbres above silence
    for name, val in [("piano", tc_piano), ("flute", tc_flute), ("bell", tc_bell)]:
        suite.add(f"TC: {name} > silence",
                  val > tc_silence,
                  f"{name}={val:.4f}, silence={tc_silence:.4f}")

    # 5.2: Harmonic timbres above inharmonic
    suite.add("TC: piano > bell (harmonic > inharmonic)",
              tc_piano > tc_bell,
              f"Piano={tc_piano:.4f}, Bell={tc_bell:.4f}")

    # 5.3: Different timbres produce different values
    all_tc = [tc_piano, tc_flute, tc_bell]
    max_diff = max(all_tc) - min(all_tc)
    suite.add("TC: timbres differentiated (range > 0.01)",
              max_diff > 0.01,
              f"Piano={tc_piano:.4f}, Flute={tc_flute:.4f}, Bell={tc_bell:.4f}")

    return suite


# ======================================================================
# SUITE 6: Cross-Belief Consistency
# ======================================================================

def test_cross_belief(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("6. Cross-Belief Consistency")

    # Generate a range of stimuli for rank correlation
    stim_set = {
        "P1": rich_dyad(C4, C4, 6, 3.0),
        "P8": rich_dyad(C4, C5, 6, 3.0),
        "P5": rich_dyad(C4, G4, 6, 3.0),
        "M3": rich_dyad(C4, E4, 6, 3.0),
        "TT": rich_dyad(C4, Fsharp4, 6, 3.0),
        "m2": rich_dyad(C4, Db4, 6, 3.0),
    }

    targets = ["harmonic_stability", "consonance_salience_gradient",
               "interval_quality", "pitch_prominence", "pitch_identity",
               "aesthetic_quality"]
    all_results = {k: runner.run(v, targets) for k, v in stim_set.items()}

    # 6.1: harmonic_stability UP <=> consonance_salience_gradient DOWN
    # (consonant intervals have high HS, low CSG; dissonant have opposite)
    hs_P1 = trimmed_mean(all_results["P1"]["harmonic_stability"])
    hs_m2 = trimmed_mean(all_results["m2"]["harmonic_stability"])
    csg_P1 = trimmed_mean(all_results["P1"]["consonance_salience_gradient"])
    csg_m2 = trimmed_mean(all_results["m2"]["consonance_salience_gradient"])
    suite.add("HS↑ ↔ CSG↓: P1 vs m2",
              (hs_P1 > hs_m2) and (csg_m2 > csg_P1),
              f"HS: P1={hs_P1:.4f}>m2={hs_m2:.4f}, CSG: m2={csg_m2:.4f}>P1={csg_P1:.4f}")

    # 6.2: harmonic_stability UP => interval_quality UP
    iq_P1 = trimmed_mean(all_results["P1"]["interval_quality"])
    iq_m2 = trimmed_mean(all_results["m2"]["interval_quality"])
    suite.add("HS↑ → IQ↑: P1 vs m2",
              (hs_P1 > hs_m2) and (iq_P1 > iq_m2),
              f"HS: P1={hs_P1:.4f}>m2={hs_m2:.4f}, IQ: P1={iq_P1:.4f}>m2={iq_m2:.4f}")

    # 6.3: Spearman rank correlation: HS vs IQ across 6 intervals
    hs_ranks = _rank_order({k: trimmed_mean(v["harmonic_stability"]) for k, v in all_results.items()})
    iq_ranks = _rank_order({k: trimmed_mean(v["interval_quality"]) for k, v in all_results.items()})
    rho_hs_iq = _spearman(hs_ranks, iq_ranks)
    suite.add("Spearman HS~IQ > 0.5",
              rho_hs_iq > 0.5,
              f"rho={rho_hs_iq:.3f}")

    # 6.4: aesthetic_quality correlates with HS across intervals
    aq_ranks = _rank_order({k: trimmed_mean(v["aesthetic_quality"]) for k, v in all_results.items()})
    rho_hs_aq = _spearman(hs_ranks, aq_ranks)
    suite.add("Spearman HS~AQ > 0.3",
              rho_hs_aq > 0.3,
              f"rho={rho_hs_aq:.3f}")

    # 6.5: pitch_prominence and pitch_identity co-vary
    pp_harm = trimmed_mean(runner.run(harmonic_complex(C4, 8, 3.0), ["pitch_prominence"])["pitch_prominence"])
    pp_noise = trimmed_mean(runner.run(noise(3.0), ["pitch_prominence"])["pitch_prominence"])
    pi_harm = trimmed_mean(runner.run(harmonic_complex(C4, 8, 3.0), ["pitch_identity"])["pitch_identity"])
    pi_noise = trimmed_mean(runner.run(noise(3.0), ["pitch_identity"])["pitch_identity"])
    suite.add("PP↑ → PI↑: harmonic vs noise",
              (pp_harm > pp_noise) and (pi_harm > pi_noise),
              f"PP: H={pp_harm:.4f}>N={pp_noise:.4f}, PI: H={pi_harm:.4f}>N={pi_noise:.4f}")

    return suite


def _rank_order(d: Dict[str, float]) -> Dict[str, int]:
    """Convert values to rank order (1=highest)."""
    sorted_keys = sorted(d, key=lambda k: -d[k])
    return {k: i + 1 for i, k in enumerate(sorted_keys)}


def _spearman(ranks_a: Dict[str, int], ranks_b: Dict[str, int]) -> float:
    """Spearman rank correlation between two rank dicts."""
    keys = list(ranks_a.keys())
    n = len(keys)
    d_sq = sum((ranks_a[k] - ranks_b[k]) ** 2 for k in keys)
    return 1.0 - 6.0 * d_sq / (n * (n**2 - 1))


# ======================================================================
# SUITE 7: Determinism
# ======================================================================

def test_determinism(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("7. Determinism")

    audio = rich_dyad(C4, G4, 6, 3.0)

    # 7.1: Same audio, two runs, exact match
    run1 = runner.run(audio, ALL_F1_BELIEFS)
    run2 = runner.run(audio, ALL_F1_BELIEFS)

    for name in ALL_F1_BELIEFS:
        if name in run1 and name in run2:
            match = torch.allclose(run1[name], run2[name], atol=1e-6)
            diff = (run1[name] - run2[name]).abs().max().item()
            suite.add(f"Determinism: {name}",
                      match,
                      f"Max diff: {diff:.2e}")

    # 7.2: Different audio produces different results
    audio_b = noise(3.0)
    run_b = runner.run(audio_b, ["harmonic_stability"])
    diff_ab = (run1["harmonic_stability"] - run_b["harmonic_stability"]).abs().mean().item()
    suite.add("Different audio → different output",
              diff_ab > 0.01,
              f"Mean abs diff: {diff_ab:.4f}")

    return suite


# ======================================================================
# SUITE 8: Boundary Conditions
# ======================================================================

def test_boundaries(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("8. Boundary Conditions")

    boundary_stimuli = {
        "silence": silence(2.0),
        "DC offset": torch.full((1, int(SR * 2)), 0.5, dtype=torch.float32),
        "near-Nyquist": sine_tone(20000.0, 2.0, 0.3),
        "very short (0.1s)": harmonic_complex(C4, 8, 0.1),
        "very long (10s)": harmonic_complex(C4, 4, 10.0),
        "max amplitude": sine_tone(C4, 2.0, 1.0),
        "min amplitude": sine_tone(C4, 2.0, 0.001),
    }

    for stim_name, audio in boundary_stimuli.items():
        try:
            results, dt = timed(lambda a=audio: runner.run(a, ALL_F1_BELIEFS))

            # Check no NaN
            has_nan = any(torch.isnan(v).any().item() for v in results.values())
            suite.add(f"{stim_name}: no NaN",
                      not has_nan, duration_ms=dt)

            # Check no Inf
            has_inf = any(torch.isinf(v).any().item() for v in results.values())
            suite.add(f"{stim_name}: no Inf",
                      not has_inf, duration_ms=dt)

            # Check all in [0, 1] (with small margin)
            all_in_range = True
            out_of_range_beliefs = []
            for bname, tensor in results.items():
                mn, mx = tensor.min().item(), tensor.max().item()
                if mn < -0.05 or mx > 1.05:
                    all_in_range = False
                    out_of_range_beliefs.append(f"{bname}=[{mn:.4f},{mx:.4f}]")
            suite.add(f"{stim_name}: all in [0,1]",
                      all_in_range,
                      ", ".join(out_of_range_beliefs) if out_of_range_beliefs else "")

        except Exception as e:
            suite.add(f"{stim_name}: no crash", False, str(e)[:100])

    return suite


# ======================================================================
# SUITE 9: Range Validity (Exhaustive)
# ======================================================================

def test_range_validity(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("9. Range Validity — Exhaustive")

    diverse_stimuli = {
        "harmonic C4": harmonic_complex(C4, 8, 2.0),
        "harmonic A4": harmonic_complex(A4, 8, 2.0),
        "inharmonic": inharmonic_complex(C4, 8, 1.15, 2.0),
        "noise": noise(2.0),
        "silence": silence(2.0),
        "dyad P5": rich_dyad(C4, G4, 6, 2.0),
        "dyad m2": rich_dyad(C4, Db4, 6, 2.0),
        "dyad P8": rich_dyad(C4, C5, 6, 2.0),
        "dyad TT": rich_dyad(C4, Fsharp4, 6, 2.0),
        "sine pure": sine_tone(C4, 2.0),
        "low pitch": harmonic_complex(C2, 6, 2.0),
        "high pitch": harmonic_complex(C6, 4, 2.0),
        "quiet": harmonic_complex(C4, 8, 2.0, 0.01),
        "loud": harmonic_complex(C4, 8, 2.0, 0.8),
        "crossfade": crossfade(harmonic_complex(C4, 8, 4.0), noise(4.0), 4.0),
    }

    violations = []
    total_checked = 0

    for stim_name, audio in diverse_stimuli.items():
        results = runner.run(audio, ALL_F1_BELIEFS)
        for bname, tensor in results.items():
            total_checked += 1
            mn = tensor.min().item()
            mx = tensor.max().item()
            if mn < -0.05 or mx > 1.05:
                violations.append(f"{stim_name}/{bname}: [{mn:.4f}, {mx:.4f}]")

    suite.add(f"Range valid: {total_checked} belief×stimulus checks",
              len(violations) == 0,
              f"Violations: {violations}" if violations else
              f"All {total_checked} checks in [0, 1]")

    return suite


# ======================================================================
# SUITE 10: Effect Sizes (Cohen's d)
# ======================================================================

def test_effect_sizes(runner: MicroBeliefRunner) -> TestSuite:
    suite = TestSuite("10. Effect Sizes (Cohen's d)")

    # Key comparisons for supplementary materials
    comparisons = [
        ("HS: P1 vs m2", "harmonic_stability",
         rich_dyad(C4, C4, 6, 3.0), rich_dyad(C4, Db4, 6, 3.0)),
        ("HS: P5 vs m2", "harmonic_stability",
         rich_dyad(C4, G4, 6, 3.0), rich_dyad(C4, Db4, 6, 3.0)),
        ("HS: harmonic vs noise", "harmonic_stability",
         harmonic_complex(C4, 8, 3.0), noise(3.0)),
        ("PP: harmonic vs noise", "pitch_prominence",
         harmonic_complex(C4, 8, 3.0), noise(3.0)),
        ("PP: harmonic vs silence", "pitch_prominence",
         harmonic_complex(C4, 8, 3.0), silence(3.0)),
        ("PI: harmonic vs noise", "pitch_identity",
         harmonic_complex(C4, 8, 3.0), noise(3.0)),
        ("OE: octave vs TT", "octave_equivalence",
         rich_dyad(C4, C5, 6, 3.0), rich_dyad(C4, Fsharp4, 6, 3.0)),
        ("TC: harmonic vs silence", "timbral_character",
         harmonic_complex(C4, 8, 3.0), silence(3.0)),
        ("AQ: consonant vs dissonant", "aesthetic_quality",
         harmonic_complex(C4, 8, 3.0) + rich_dyad(C4, G4, 6, 3.0, 0.15),
         rich_dyad(C4, Db4, 6, 3.0) + noise(3.0, 0.1)),
        ("RRP: consonant vs noise", "reward_response_pred",
         harmonic_complex(C4, 8, 3.0, 0.2) + harmonic_complex(G4, 6, 3.0, 0.15),
         noise(3.0)),
    ]

    d_values: List[Tuple[str, float]] = []

    for label, belief, audio_a, audio_b in comparisons:
        res_a = runner.run(audio_a, [belief])[belief]
        res_b = runner.run(audio_b, [belief])[belief]
        d = cohens_d(res_a, res_b)
        d_values.append((label, d))

        suite.add(f"d({label}) > 0 (correct direction)",
                  d > 0,
                  f"d={d:.3f}, A={trimmed_mean(res_a):.4f}, B={trimmed_mean(res_b):.4f}")

    # Summary table
    print("\n  Effect size summary (Cohen's d):")
    print(f"  {'Comparison':>35}  {'d':>7}  {'Size':>8}")
    for label, d in d_values:
        size = "large" if abs(d) > 0.8 else "medium" if abs(d) > 0.5 else "small" if abs(d) > 0.2 else "negligible"
        print(f"  {label:>35}  {d:>7.3f}  {size:>8}")

    return suite


# ======================================================================
# Main
# ======================================================================

def main():
    print("=" * 70)
    print("  F1 Deep Test Suite — Sensory Processing (17 beliefs)")
    print(f"  Project: {_PROJECT_ROOT}")
    print("=" * 70)

    print("\nInitializing MicroBeliefRunner (R³→H³→C³ pipeline)...")
    t0 = time.perf_counter()
    runner = MicroBeliefRunner()
    init_time = (time.perf_counter() - t0) * 1000
    print(f"  Pipeline ready ({init_time:.0f}ms)")
    print(f"  Mechanisms: {len(runner.mechanism_names)}")
    print(f"  Beliefs: {len(runner.belief_names)} total, {len([b for b in ALL_F1_BELIEFS if b in runner.belief_names])} F1")

    all_suites: List[TestSuite] = []

    suite_runners = [
        ("1. Structural", lambda: test_structural(runner)),
        ("2. Consonance Hierarchy", lambda: test_consonance_hierarchy(runner)),
        ("3. Pitch Processing", lambda: test_pitch_processing(runner)),
        ("4. Octave Equivalence", lambda: test_octave_equivalence(runner)),
        ("5. Timbral", lambda: test_timbral(runner)),
        ("6. Cross-Belief", lambda: test_cross_belief(runner)),
        ("7. Determinism", lambda: test_determinism(runner)),
        ("8. Boundaries", lambda: test_boundaries(runner)),
        ("9. Range Validity", lambda: test_range_validity(runner)),
        ("10. Effect Sizes", lambda: test_effect_sizes(runner)),
    ]

    for name, fn in suite_runners:
        print(f"\nRunning {name}...")
        try:
            t0 = time.perf_counter()
            suite = fn()
            dt = (time.perf_counter() - t0) * 1000
            all_suites.append(suite)
            print(suite.report())
            print(f"  [{dt:.0f}ms]")
        except Exception as e:
            print(f"  SUITE CRASHED: {e}")
            traceback.print_exc()
            crash_suite = TestSuite(name)
            crash_suite.add("Suite execution", False, traceback.format_exc()[-300:])
            all_suites.append(crash_suite)

    # Grand summary
    total_pass = sum(s.passed for s in all_suites)
    total_fail = sum(s.failed for s in all_suites)
    total_tests = sum(s.total for s in all_suites)

    print("\n" + "=" * 70)
    print(f"  GRAND TOTAL: {total_pass}/{total_tests} PASSED, {total_fail} FAILED")
    print("=" * 70)

    if total_fail > 0:
        print("\n  FAILURES:")
        for s in all_suites:
            for r in s.results:
                if not r.passed:
                    print(f"    [{s.name}] {r.name}")
                    if r.message:
                        print(f"      {r.message[:150]}")

    print()
    return total_fail == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
