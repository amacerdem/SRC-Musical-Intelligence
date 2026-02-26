#!/usr/bin/env python3
"""Temporal F1 Belief Diagnostics.

Runs transition/contrast MIDI audio through R3->H3->C3 pipeline and verifies
frame-by-frame belief trajectories.  Generates PNG charts + MD report.

Usage:
    python Tests/micro_beliefs/temporal_f1_diagnostics.py
    python Tests/micro_beliefs/temporal_f1_diagnostics.py --relay bch
    python Tests/micro_beliefs/temporal_f1_diagnostics.py --belief harmonic_stability
"""
from __future__ import annotations

import argparse
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import scipy.io.wavfile as wav
import torch

# -- Matplotlib (headless) ---------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# -- Paths -------------------------------------------------------------------
_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parent.parent  # SRC Musical Intelligence
sys.path.insert(0, str(_ROOT))
sys.path.insert(0, str(_ROOT / "Tests"))

from micro_beliefs.pipeline_runner import MicroBeliefRunner  # noqa: E402

# -- Constants ---------------------------------------------------------------
MIDI_DIR = _ROOT / "Test-Audio" / "micro_beliefs" / "f1_midi"
REPORT_DIR = _SCRIPT_DIR / "reports"
WARMUP_FRAC = 0.05       # skip first 5% of total frames for H3 ramp-up
SEGMENT_INNER = 0.70      # use middle 70% of each segment for averaging
SR = 44_100
HOP = 256


# ============================================================================
# Data classes
# ============================================================================

@dataclass
class TestResult:
    name: str
    belief: str
    relay: str
    test_type: str
    passed: bool
    expected: str
    actual: str
    description: str = ""
    segment_means: List[float] = field(default_factory=list)
    margin: float = 0.0
    trajectory: Optional[np.ndarray] = None


@dataclass
class OrderingTest:
    """Within a single transition file, segment means should follow order."""
    name: str
    belief: str
    relay: str
    audio_file: str
    direction: str          # "decrease" or "increase"
    n_segments: int = 4
    margin: float = 0.003
    description: str = ""


@dataclass
class ComparisonTest:
    """Mean belief value from high_file should exceed that from low_file."""
    name: str
    belief: str
    relay: str
    high_file: str
    low_file: str
    margin: float = 0.003
    description: str = ""


@dataclass
class SensitivityTest:
    """Belief should show temporal variation (not degenerate/flat)."""
    name: str
    belief: str
    relay: str
    audio_file: str
    min_std: float = 0.003
    description: str = ""


# ============================================================================
# Test definitions — 37 tests across 17 F1 beliefs
# ============================================================================

ALL_TESTS: List[Union[OrderingTest, ComparisonTest, SensitivityTest]] = [
    # ── BCH: harmonic_stability (CoreBelief) ──────────────────────────────
    OrderingTest(
        "hs_c2d_order", "harmonic_stability", "bch",
        "bch/16_consonant_to_dissonant_8s.wav", "decrease", 4,
        description="Major->Minor->Dim->Cluster: stability decreases",
    ),
    OrderingTest(
        "hs_d2c_order", "harmonic_stability", "bch",
        "bch/17_dissonant_to_consonant_8s.wav", "increase", 4,
        description="Cluster->Dim->Minor->Major: stability increases",
    ),
    ComparisonTest(
        "hs_major_vs_cluster", "harmonic_stability", "bch",
        "bch/05_major_triad_piano.wav", "bch/10_cluster_4note_piano.wav",
        description="Major triad > 4-note cluster",
    ),

    # ── BCH: interval_quality (AppraisalBelief) ──────────────────────────
    OrderingTest(
        "iq_c2d_order", "interval_quality", "bch",
        "bch/16_consonant_to_dissonant_8s.wav", "decrease", 4,
        description="Pure intervals degrade through transition",
    ),
    ComparisonTest(
        "iq_p5_vs_dim", "interval_quality", "bch",
        "bch/03_p5_C4G4_piano.wav", "bch/07_dim_triad_piano.wav",
        description="Perfect 5th > diminished triad",
    ),

    # ── BCH: harmonic_template_match (AppraisalBelief) ───────────────────
    OrderingTest(
        "htm_c2d_order", "harmonic_template_match", "bch",
        "bch/16_consonant_to_dissonant_8s.wav", "decrease", 4,
        description="Template match decreases with dissonance",
    ),
    ComparisonTest(
        "htm_major_vs_cluster", "harmonic_template_match", "bch",
        "bch/05_major_triad_piano.wav", "bch/11_cluster_6note_piano.wav",
        description="Major triad matches templates > 6-note cluster",
    ),

    # ── BCH: consonance_trajectory (AnticipationBelief) ──────────────────
    SensitivityTest(
        "ct_sensitivity", "consonance_trajectory", "bch",
        "bch/16_consonant_to_dissonant_8s.wav",
        description="Prediction should vary during consonance change",
    ),
    OrderingTest(
        "ct_c2d_track", "consonance_trajectory", "bch",
        "bch/16_consonant_to_dissonant_8s.wav", "decrease", 4,
        margin=0.001,
        description="Predicted consonance decreases (loose margin)",
    ),

    # ── PSCL: pitch_prominence (CoreBelief) ──────────────────────────────
    ComparisonTest(
        "pp_clear_vs_cluster", "pitch_prominence", "pscl",
        "pscl/07_C4_piano.wav", "pscl/11_cluster_6note.wav",
        description="Clear single pitch > 6-note cluster",
    ),
    SensitivityTest(
        "pp_melody_sens", "pitch_prominence", "pscl",
        "pscl/12_melody_diatonic.wav",
        description="Pitch prominence varies during melody",
    ),

    # ── PSCL: pitch_continuation (AnticipationBelief) ────────────────────
    ComparisonTest(
        "pc_clear_vs_cluster", "pitch_continuation", "pscl",
        "pscl/07_C4_piano.wav", "pscl/11_cluster_6note.wav",
        description="Clear pitch = confident continuation > cluster",
    ),
    SensitivityTest(
        "pc_melody_sens", "pitch_continuation", "pscl",
        "pscl/12_melody_diatonic.wav",
        description="Pitch prediction varies during melody",
    ),

    # ── PCCR: pitch_identity (CoreBelief) ────────────────────────────────
    ComparisonTest(
        "pi_single_vs_all12", "pitch_identity", "pccr",
        "pccr/09_single_C4.wav", "pccr/11_all_12_notes.wav",
        description="Single pitch identity > all-12 chromatic",
    ),
    SensitivityTest(
        "pi_melody_sens", "pitch_identity", "pccr",
        "pccr/04_melody_G_oct4.wav",
        description="Pitch identity varies during melody",
    ),

    # ── PCCR: octave_equivalence (AppraisalBelief) ───────────────────────
    ComparisonTest(
        "oe_octave_vs_tritone", "octave_equivalence", "pccr",
        "pccr/06_octave_dyad.wav", "pccr/07_tritone_dyad.wav",
        description="Octave dyad (same chroma) > tritone dyad",
    ),
    SensitivityTest(
        "oe_melody_sens", "octave_equivalence", "pccr",
        "pccr/01_melody_C_oct3.wav",
        description="Octave equivalence varies with pitch changes",
    ),

    # ── SDED: spectral_complexity (AppraisalBelief) ──────────────────────
    ComparisonTest(
        "sc_cluster_vs_single", "spectral_complexity", "sded",
        "sded/06_cluster_6note.wav", "sded/01_single_C4.wav",
        description="6-note cluster more complex than single note",
    ),
    ComparisonTest(
        "sc_chromatic_vs_triad", "spectral_complexity", "sded",
        "sded/08_full_chromatic.wav", "sded/03_major_triad.wav",
        description="Full chromatic more complex than major triad",
    ),

    # ── CSG: consonance_salience_gradient (AppraisalBelief) ──────────────
    ComparisonTest(
        "csg_cluster_vs_single", "consonance_salience_gradient", "csg",
        "csg/03_cluster.wav", "csg/06_single_note.wav",
        description="Cluster has higher salience than single note",
    ),
    OrderingTest(
        "csg_i2v7_tension", "consonance_salience_gradient", "csg",
        "csg/05_I_V7_tension.wav", "increase", 2,
        description="Moving to V7 increases consonance salience",
    ),

    # ── MPG: melodic_contour_tracking (AppraisalBelief) ──────────────────
    ComparisonTest(
        "mct_ascending_vs_repeated", "melodic_contour_tracking", "mpg",
        "mpg/01_ascending_diatonic.wav", "mpg/05_repeated_C4.wav",
        description="Active melody with pitch changes > repeated single note",
    ),
    ComparisonTest(
        "mct_leaps_vs_repeated", "melodic_contour_tracking", "mpg",
        "mpg/06_octave_leaps.wav", "mpg/05_repeated_C4.wav",
        description="Octave leaps (large contour) > repeated note (flat contour)",
    ),
    SensitivityTest(
        "mct_mixed_sens", "melodic_contour_tracking", "mpg",
        "mpg/07_mixed_contour.wav",
        description="Contour tracking varies with direction changes",
    ),

    # ── MPG: contour_continuation (AnticipationBelief) ───────────────────
    ComparisonTest(
        "cc_arpeggio_vs_sustained", "contour_continuation", "mpg",
        "mpg/04_arpeggio_arch.wav", "mpg/08_sustained_C4.wav",
        description="Active contour = confident prediction > sustained",
    ),
    SensitivityTest(
        "cc_ascending_sens", "contour_continuation", "mpg",
        "mpg/01_ascending_diatonic.wav",
        description="Contour prediction varies during melody",
    ),

    # ── MIAA: timbral_character (CoreBelief) ─────────────────────────────
    ComparisonTest(
        "tc_single_vs_chord", "timbral_character", "miaa",
        "miaa/01_C4_piano.wav", "miaa/13_chord_C_major_piano.wav",
        description="Single note = clearer timbral identity > chord",
    ),
    SensitivityTest(
        "tc_multi_timbre_sens", "timbral_character", "miaa",
        "miaa/14_timbre_sequence_4inst.wav",
        description="Timbral character varies across instruments",
    ),

    # ── MIAA: imagery_recognition (AnticipationBelief) ───────────────────
    ComparisonTest(
        "ir_piano_vs_multi", "imagery_recognition", "miaa",
        "miaa/01_C4_piano.wav", "miaa/14_timbre_sequence_4inst.wav",
        description="Stable timbre more predictable than changing",
    ),
    SensitivityTest(
        "ir_multi_sens", "imagery_recognition", "miaa",
        "miaa/14_timbre_sequence_4inst.wav",
        description="Imagery prediction varies with timbre changes",
    ),

    # ── STAI: aesthetic_quality (CoreBelief) ──────────────────────────────
    OrderingTest(
        "aq_d2r_increase", "aesthetic_quality", "stai",
        "stai/08_dissonant_to_resolved.wav", "increase", 2,
        description="Dissonant->Resolved: aesthetic quality increases",
    ),
    OrderingTest(
        "aq_r2d_decrease", "aesthetic_quality", "stai",
        "stai/09_resolved_to_dissonant.wav", "decrease", 2,
        description="Resolved->Dissonant: aesthetic quality decreases",
    ),
    ComparisonTest(
        "aq_beautiful_vs_harsh", "aesthetic_quality", "stai",
        "stai/01_beautiful_I_vi_IV_V_strings.wav",
        "stai/03_harsh_chromatic_clusters.wav",
        description="Beautiful strings > harsh chromatic",
    ),

    # ── STAI: spectral_temporal_synergy (AppraisalBelief) ────────────────
    ComparisonTest(
        "sts_beautiful_vs_harsh", "spectral_temporal_synergy", "stai",
        "stai/01_beautiful_I_vi_IV_V_strings.wav",
        "stai/06_dense_cluster_ff.wav",
        description="Beautiful = high synergy > dense cluster",
    ),
    SensitivityTest(
        "sts_d2r_sens", "spectral_temporal_synergy", "stai",
        "stai/08_dissonant_to_resolved.wav",
        description="Synergy varies during resolution transition",
    ),

    # ── STAI: reward_response_pred (AnticipationBelief) ──────────────────
    ComparisonTest(
        "rrp_beautiful_vs_harsh", "reward_response_pred", "stai",
        "stai/01_beautiful_I_vi_IV_V_strings.wav",
        "stai/03_harsh_chromatic_clusters.wav",
        description="Higher reward prediction for beautiful music",
    ),
    SensitivityTest(
        "rrp_d2r_sens", "reward_response_pred", "stai",
        "stai/08_dissonant_to_resolved.wav",
        description="Reward prediction varies during resolution",
    ),
]


# ============================================================================
# Audio loading
# ============================================================================

def load_wav(path: Path) -> torch.Tensor:
    """Load WAV file as ``(1, N)`` float32 tensor."""
    sr, data = wav.read(str(path))
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.dtype == np.float64:
        data = data.astype(np.float32)
    if data.ndim == 2:
        data = data.mean(axis=1)
    return torch.from_numpy(data).unsqueeze(0)


def _segment_bounds(
    T: int, frac_start: float, frac_end: float,
) -> Tuple[int, int]:
    """Return (inner_start, inner_end) for a segment, respecting warmup."""
    start = int(T * frac_start)
    end = int(T * frac_end)
    seg_len = end - start
    pad = int(seg_len * (1 - SEGMENT_INNER) / 2)
    inner_start = start + pad
    inner_end = end - pad
    warmup = int(T * WARMUP_FRAC)
    inner_start = max(inner_start, warmup)
    if inner_end <= inner_start:
        inner_end = inner_start + 1
    return inner_start, inner_end


def segment_mean(signal: np.ndarray, frac_start: float, frac_end: float) -> float:
    """Mean of signal within fractional range, using inner portion."""
    s, e = _segment_bounds(len(signal), frac_start, frac_end)
    return float(np.mean(signal[s:e]))


# ============================================================================
# Pipeline cache
# ============================================================================

def _get_signal(
    runner: MicroBeliefRunner,
    audio_file: str,
    belief_name: str,
    cache: Dict[str, Dict[str, np.ndarray]],
) -> np.ndarray:
    """Run pipeline for audio file, return belief signal.  Uses cache."""
    if audio_file not in cache:
        wav_path = MIDI_DIR / audio_file
        waveform = load_wav(wav_path)
        results = runner.run(waveform)
        cache[audio_file] = {
            name: tensor.squeeze(0).detach().cpu().numpy()
            for name, tensor in results.items()
        }
    return cache[audio_file][belief_name]


# ============================================================================
# Test execution
# ============================================================================

def run_ordering_test(
    runner: MicroBeliefRunner,
    test: OrderingTest,
    cache: Dict[str, Dict[str, np.ndarray]],
) -> TestResult:
    signal = _get_signal(runner, test.audio_file, test.belief, cache)
    seg = 1.0 / test.n_segments
    means = [segment_mean(signal, i * seg, (i + 1) * seg)
             for i in range(test.n_segments)]

    if test.direction == "decrease":
        pairs_ok = sum(
            1 for i in range(len(means) - 1)
            if means[i] > means[i + 1] - test.margin
        )
    else:
        pairs_ok = sum(
            1 for i in range(len(means) - 1)
            if means[i] < means[i + 1] + test.margin
        )

    total_pairs = test.n_segments - 1
    passed = pairs_ok == total_pairs

    return TestResult(
        name=test.name,
        belief=test.belief,
        relay=test.relay,
        test_type=f"ordering_{test.direction}",
        passed=passed,
        expected=f"{test.direction}: all {total_pairs} pairs",
        actual=f"{pairs_ok}/{total_pairs} OK  means=[{', '.join(f'{m:.4f}' for m in means)}]",
        description=test.description,
        segment_means=means,
        margin=test.margin,
        trajectory=signal,
    )


def run_comparison_test(
    runner: MicroBeliefRunner,
    test: ComparisonTest,
    cache: Dict[str, Dict[str, np.ndarray]],
) -> TestResult:
    sig_h = _get_signal(runner, test.high_file, test.belief, cache)
    sig_l = _get_signal(runner, test.low_file, test.belief, cache)

    wu_h = max(1, int(len(sig_h) * WARMUP_FRAC))
    wu_l = max(1, int(len(sig_l) * WARMUP_FRAC))
    mean_h = float(np.mean(sig_h[wu_h:]))
    mean_l = float(np.mean(sig_l[wu_l:]))

    passed = mean_h > mean_l - test.margin

    return TestResult(
        name=test.name,
        belief=test.belief,
        relay=test.relay,
        test_type="comparison",
        passed=passed,
        expected=f"high > low (margin {test.margin})",
        actual=f"high={mean_h:.4f}  low={mean_l:.4f}  diff={mean_h - mean_l:+.4f}",
        description=test.description,
        segment_means=[mean_h, mean_l],
        margin=test.margin,
    )


def run_sensitivity_test(
    runner: MicroBeliefRunner,
    test: SensitivityTest,
    cache: Dict[str, Dict[str, np.ndarray]],
) -> TestResult:
    signal = _get_signal(runner, test.audio_file, test.belief, cache)
    wu = max(1, int(len(signal) * WARMUP_FRAC))
    active = signal[wu:]
    std_val = float(np.std(active))
    mean_val = float(np.mean(active))

    passed = std_val > test.min_std

    return TestResult(
        name=test.name,
        belief=test.belief,
        relay=test.relay,
        test_type="sensitivity",
        passed=passed,
        expected=f"std > {test.min_std:.4f}",
        actual=f"mean={mean_val:.4f}  std={std_val:.4f}",
        description=test.description,
        segment_means=[mean_val, std_val],
        margin=test.min_std,
        trajectory=signal,
    )


# ============================================================================
# Chart generation
# ============================================================================

def generate_relay_charts(
    results: List[TestResult],
    cache: Dict[str, Dict[str, np.ndarray]],
    output_dir: Path,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    relay_results: Dict[str, List[TestResult]] = {}
    for r in results:
        relay_results.setdefault(r.relay, []).append(r)

    for relay, relay_tests in sorted(relay_results.items()):
        beliefs = list(dict.fromkeys(t.belief for t in relay_tests))
        n = len(beliefs)

        fig, axes = plt.subplots(n, 1, figsize=(14, 3.2 * n), squeeze=False)
        fig.suptitle(
            f"F1 {relay.upper()} — Temporal Belief Diagnostics",
            fontsize=14, fontweight="bold",
        )

        for i, bname in enumerate(beliefs):
            ax = axes[i, 0]
            btests = [t for t in relay_tests if t.belief == bname]

            # Plot trajectories
            plotted = False
            for t in btests:
                if t.trajectory is not None:
                    T = len(t.trajectory)
                    time_s = np.arange(T) * HOP / SR
                    color = "#2ca02c" if t.passed else "#d62728"
                    lbl = f"{t.name} [{'PASS' if t.passed else 'FAIL'}]"
                    ax.plot(time_s, t.trajectory, color=color,
                            alpha=0.75, linewidth=1.1, label=lbl)

                    # Segment markers for ordering tests
                    if t.test_type.startswith("ordering_") and t.segment_means:
                        ns = len(t.segment_means)
                        for j in range(1, ns):
                            x = time_s[-1] * j / ns
                            ax.axvline(x, color="gray", ls="--", alpha=0.5, lw=0.8)
                        # Annotate segment means
                        for j, sm in enumerate(t.segment_means):
                            cx = time_s[-1] * (j + 0.5) / ns
                            ax.text(cx, sm, f"{sm:.3f}", fontsize=7,
                                    ha="center", va="bottom",
                                    bbox=dict(boxstyle="round,pad=0.2",
                                              fc="white", alpha=0.8))
                    plotted = True

            # Annotate comparison tests
            comps = [t for t in btests if t.test_type == "comparison"]
            for j, t in enumerate(comps):
                icon = "PASS" if t.passed else "FAIL"
                color = "#2ca02c" if t.passed else "#d62728"
                txt = f"{t.name}: {icon} (H={t.segment_means[0]:.3f} L={t.segment_means[1]:.3f})"
                ax.text(0.98, 0.95 - j * 0.12, txt,
                        transform=ax.transAxes, fontsize=7,
                        ha="right", va="top", color=color,
                        fontfamily="monospace")

            ax.set_ylabel(bname.replace("_", "\n"), fontsize=8)
            if i == n - 1:
                ax.set_xlabel("Time (s)")
            if plotted:
                ax.legend(loc="upper left", fontsize=7)
            ax.grid(True, alpha=0.25)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        out = output_dir / f"temporal_{relay}.png"
        fig.savefig(out, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"    {out.name}")


def generate_summary_chart(results: List[TestResult], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    stats: Dict[str, Dict[str, int]] = {}
    for r in results:
        s = stats.setdefault(r.belief, {"pass": 0, "fail": 0, "total": 0})
        s["total"] += 1
        s["pass" if r.passed else "fail"] += 1

    beliefs = list(stats.keys())
    n = len(beliefs)
    pcounts = [stats[b]["pass"] for b in beliefs]
    fcounts = [stats[b]["fail"] for b in beliefs]
    totals = [stats[b]["total"] for b in beliefs]
    accs = [p / t * 100 if t > 0 else 0 for p, t in zip(pcounts, totals)]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, max(5, 0.45 * n)))
    y = np.arange(n)

    # Left: stacked bar
    ax1.barh(y, pcounts, color="#2ca02c", alpha=0.75, label="PASS")
    ax1.barh(y, fcounts, left=pcounts, color="#d62728", alpha=0.75, label="FAIL")
    ax1.set_yticks(y)
    ax1.set_yticklabels([b.replace("_", " ") for b in beliefs], fontsize=8)
    ax1.set_xlabel("Tests")
    ax1.set_title("Results per Belief")
    ax1.legend(fontsize=8)
    ax1.invert_yaxis()

    # Right: accuracy
    colors = ["#2ca02c" if a >= 85 else "#ff7f0e" if a >= 50 else "#d62728"
              for a in accs]
    ax2.barh(y, accs, color=colors, alpha=0.75)
    ax2.axvline(85, color="#d62728", ls="--", lw=1, label="85% target")
    ax2.set_yticks(y)
    ax2.set_yticklabels([b.replace("_", " ") for b in beliefs], fontsize=8)
    ax2.set_xlabel("Accuracy (%)")
    ax2.set_title("Per-Belief Accuracy")
    ax2.set_xlim(0, 110)
    ax2.legend(fontsize=8)
    ax2.invert_yaxis()
    for i, (acc, tot) in enumerate(zip(accs, totals)):
        ax2.text(acc + 1, i, f"{acc:.0f}% ({pcounts[i]}/{tot})",
                 va="center", fontsize=7)

    plt.tight_layout()
    out = output_dir / "temporal_summary.png"
    fig.savefig(out, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"    {out.name}")


# ============================================================================
# Report generation
# ============================================================================

def generate_report(results: List[TestResult], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed
    accuracy = passed / total * 100 if total > 0 else 0

    lines = [
        "# F1 Temporal Belief Diagnostics Report",
        "",
        f"**Date**: {time.strftime('%Y-%m-%d %H:%M')}",
        f"**Total tests**: {total}",
        f"**Passed**: {passed} ({accuracy:.1f}%)",
        f"**Failed**: {failed}",
        f"**Target**: 85%",
        f"**Status**: {'PASS' if accuracy >= 85 else 'FAIL'}",
        "",
        "---",
        "",
        "## Summary by Belief",
        "",
        "| Belief | Relay | Tests | Pass | Fail | Accuracy |",
        "|--------|-------|-------|------|------|----------|",
    ]

    belief_order = list(dict.fromkeys(r.belief for r in results))
    for b in belief_order:
        br = [r for r in results if r.belief == b]
        bp = sum(1 for r in br if r.passed)
        bt = len(br)
        bf = bt - bp
        ba = bp / bt * 100 if bt > 0 else 0
        rl = br[0].relay
        mark = "+" if ba >= 85 else "-"
        lines.append(
            f"| {b} | {rl.upper()} | {bt} | {bp} | {bf} | {ba:.0f}% {mark} |"
        )

    lines += ["", "---", "", "## Detailed Results", ""]

    relay_order = list(dict.fromkeys(r.relay for r in results))
    for relay in relay_order:
        rt = [r for r in results if r.relay == relay]
        lines.append(f"### {relay.upper()}")
        lines.append("")

        for r in rt:
            icon = "+" if r.passed else "-"
            lines.append(f"**{icon} {r.name}** ({r.test_type}) — *{r.belief}*")
            if r.description:
                lines.append(f"  {r.description}")
            lines.append(f"- Expected: {r.expected}")
            lines.append(f"- Actual: {r.actual}")
            if r.segment_means:
                lines.append(
                    f"- Segments: [{', '.join(f'{m:.4f}' for m in r.segment_means)}]"
                )
            lines.append("")

    lines += ["---", "", "## Charts", ""]
    for relay in relay_order:
        lines.append(f"![{relay.upper()} Temporal](reports/temporal_{relay}.png)")
        lines.append("")
    lines.append("![Summary](reports/temporal_summary.png)")
    lines.append("")

    output_path.write_text("\n".join(lines))
    print(f"    {output_path.name}")


# ============================================================================
# Main
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="F1 Temporal Belief Diagnostics")
    parser.add_argument("--relay", type=str, default=None,
                        help="Only test beliefs from this relay")
    parser.add_argument("--belief", type=str, default=None,
                        help="Only test this specific belief")
    args = parser.parse_args()

    tests = list(ALL_TESTS)
    if args.relay:
        tests = [t for t in tests if t.relay == args.relay]
    if args.belief:
        tests = [t for t in tests if t.belief == args.belief]

    if not tests:
        print("No tests match the filter criteria.")
        return

    print(f"F1 Temporal Belief Diagnostics")
    print(f"{'=' * 55}")
    print(f"Tests to run: {len(tests)}")
    print()

    # Pipeline init
    print("Initializing pipeline...")
    t0 = time.time()
    runner = MicroBeliefRunner()
    print(f"  Ready in {time.time() - t0:.1f}s")
    print(f"  Beliefs: {len(runner.belief_names)}")
    print()

    # Check files
    missing: List[str] = []
    for test in tests:
        files = ([test.high_file, test.low_file]
                 if isinstance(test, ComparisonTest)
                 else [test.audio_file])
        for f in files:
            if not (MIDI_DIR / f).exists():
                missing.append(f)

    if missing:
        unique = sorted(set(missing))
        print(f"WARNING: {len(unique)} audio files missing:")
        for f in unique:
            print(f"  - {f}")
        print()

        def _files_ok(t):
            if isinstance(t, ComparisonTest):
                return ((MIDI_DIR / t.high_file).exists()
                        and (MIDI_DIR / t.low_file).exists())
            return (MIDI_DIR / t.audio_file).exists()

        tests = [t for t in tests if _files_ok(t)]
        print(f"Running {len(tests)} tests with available audio.\n")

    if not tests:
        print("No runnable tests.")
        return

    # Run
    cache: Dict[str, Dict[str, np.ndarray]] = {}
    results: List[TestResult] = []

    print("Running temporal tests...")
    for i, test in enumerate(tests):
        if isinstance(test, OrderingTest):
            result = run_ordering_test(runner, test, cache)
        elif isinstance(test, ComparisonTest):
            result = run_comparison_test(runner, test, cache)
        elif isinstance(test, SensitivityTest):
            result = run_sensitivity_test(runner, test, cache)
        else:
            continue

        results.append(result)
        icon = "+" if result.passed else "-"
        print(f"  [{i + 1:2d}/{len(tests)}] {icon} {result.name:32s} {result.actual}")

    # Summary
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    accuracy = passed / total * 100 if total > 0 else 0

    print()
    print(f"{'=' * 55}")
    print(f"RESULTS: {passed}/{total} passed ({accuracy:.1f}%)")
    print(f"TARGET:  85%")
    print(f"STATUS:  {'PASS' if accuracy >= 85 else 'FAIL'}")
    print()

    # Charts
    print("Generating charts...")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    generate_relay_charts(results, cache, REPORT_DIR)
    generate_summary_chart(results, REPORT_DIR)

    # Report
    print("Generating report...")
    generate_report(results, _SCRIPT_DIR / "REPORT-F1-TEMPORAL.md")

    print()
    print("Done!")


if __name__ == "__main__":
    main()
