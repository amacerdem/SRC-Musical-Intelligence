"""Master report compiler — aggregates all V1-V7 results into comprehensive output.

Called automatically by pytest_sessionfinish hook in root conftest.py.
Generates:
  - Validation/results/master_report.json  (machine-readable)
  - Validation/results/master_report.md    (human-readable)
  - Per-module v{n}_summary.txt via each module's report.py
"""
from __future__ import annotations

import json
import platform
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from Validation.config.paths import RESULTS, ensure_dirs


def compile_master_report(
    test_results: List[Dict[str, Any]],
    module_data: Dict[str, Any],
) -> Path:
    """Compile all validation results into master report files.

    Args:
        test_results: Per-test outcome list from pytest_runtest_makereport hook.
            Each entry: {nodeid, outcome, duration, longrepr, markers}
        module_data: Per-module computed data stashed during fixture execution.
            Keys like "v1", "v2", etc.

    Returns:
        Path to master_report.md.
    """
    ensure_dirs()

    # ── Call per-module report generators ──
    _generate_module_reports(module_data)

    # ── Compute summary statistics ──
    by_module = _group_by_module(test_results)
    total_passed = sum(1 for t in test_results if t["outcome"] == "passed")
    total_failed = sum(1 for t in test_results if t["outcome"] == "failed")
    total_skipped = sum(1 for t in test_results if t["outcome"] == "skipped")
    total_duration = sum(t.get("duration", 0) for t in test_results)

    # ── Build JSON report ──
    report_json = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "python_version": sys.version,
            "platform": platform.platform(),
            "hostname": platform.node(),
        },
        "summary": {
            "total_tests": len(test_results),
            "passed": total_passed,
            "failed": total_failed,
            "skipped": total_skipped,
            "total_duration_s": round(total_duration, 2),
        },
        "modules": {},
        "tests": test_results,
    }

    for module_tag, tests in by_module.items():
        m_passed = sum(1 for t in tests if t["outcome"] == "passed")
        m_failed = sum(1 for t in tests if t["outcome"] == "failed")
        m_skipped = sum(1 for t in tests if t["outcome"] == "skipped")
        m_dur = sum(t.get("duration", 0) for t in tests)

        report_json["modules"][module_tag] = {
            "tests": len(tests),
            "passed": m_passed,
            "failed": m_failed,
            "skipped": m_skipped,
            "duration_s": round(m_dur, 2),
            "status": "PASS" if m_failed == 0 and m_passed > 0 else (
                "SKIP" if m_passed == 0 and m_skipped > 0 else "FAIL"
            ),
        }

    # Write JSON
    json_path = RESULTS / "master_report.json"
    json_path.write_text(json.dumps(report_json, indent=2, default=str))

    # ── Build Markdown report ──
    md = _build_markdown(report_json, by_module, module_data)
    md_path = RESULTS / "master_report.md"
    md_path.write_text(md)

    print(f"\n{'='*60}")
    print(f"  MASTER REPORT")
    print(f"{'='*60}")
    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")
    print(f"  Tests: {total_passed} passed, {total_failed} failed, "
          f"{total_skipped} skipped ({total_duration:.1f}s)")
    print(f"{'='*60}\n")

    return md_path


def _generate_module_reports(module_data: Dict[str, Any]) -> None:
    """Call each module's report.py generator if data is available."""

    # V1 — Pharmacology
    if "v1" in module_data:
        try:
            from Validation.v1_pharmacology.report import generate_summary_report
            d = module_data["v1"]
            generate_summary_report(d["ferreri"], d["mallik"], d["laeng"])
        except Exception as e:
            print(f"[Report] V1 report generation failed: {e}")

    # V2 — IDyOM
    if "v2" in module_data:
        try:
            from Validation.v2_idyom.report import generate_summary_report
            d = module_data["v2"]
            generate_summary_report(d["aggregate"], d["comparisons"])
        except Exception as e:
            print(f"[Report] V2 report generation failed: {e}")

    # V3 — Krumhansl
    if "v3" in module_data:
        try:
            from Validation.v3_krumhansl.report import generate_summary_report
            d = module_data["v3"]
            generate_summary_report(d["mi_major"], d["mi_minor"])
        except Exception as e:
            print(f"[Report] V3 report generation failed: {e}")

    # V4 — DEAM
    if "v4" in module_data:
        try:
            from Validation.v4_deam.report import generate_summary_report
            d = module_data["v4"]
            generate_summary_report(d["aggregate"], d["per_song"])
        except Exception as e:
            print(f"[Report] V4 report generation failed: {e}")

    # V5 — EEG Encoding
    if "v5" in module_data:
        try:
            from Validation.v5_eeg_encoding.report import generate_summary_report
            generate_summary_report(module_data["v5"])
        except Exception as e:
            print(f"[Report] V5 report generation failed: {e}")

    # V6 — fMRI
    if "v6" in module_data:
        try:
            from Validation.v6_fmri_encoding.report import generate_summary_report
            generate_summary_report(module_data["v6"])
        except Exception as e:
            print(f"[Report] V6 report generation failed: {e}")

    # V7 — RSA
    if "v7" in module_data:
        try:
            from Validation.v7_rsa.report import generate_summary_report
            d = module_data["v7"]
            generate_summary_report(
                d["comparisons"], d["rdms"], d["stimulus_names"],
            )
        except Exception as e:
            print(f"[Report] V7 report generation failed: {e}")


def _group_by_module(
    test_results: List[Dict[str, Any]],
) -> Dict[str, List[Dict[str, Any]]]:
    """Group test results by validation module (v1-v7)."""
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for t in test_results:
        nodeid = t.get("nodeid", "")
        module = "unknown"
        for tag in ("v1", "v2", "v3", "v4", "v5", "v6", "v7"):
            if f"/{tag}_" in nodeid or f"\\{tag}_" in nodeid:
                module = tag
                break
        groups.setdefault(module, []).append(t)
    return groups


MODULE_DESCRIPTIONS = {
    "v1": ("V1 Pharmacology", "Ferreri/Mallik/Laeng — DA/OPI modulation of reward & emotion"),
    "v2": ("V2 IDyOM", "Convergent validity — MI surprise vs. IDyOM information content"),
    "v3": ("V3 Krumhansl", "Tonal hierarchy — MI profiles vs. Krumhansl-Kessler 1982"),
    "v4": ("V4 DEAM", "Continuous emotion — MI valence/arousal vs. DEAM crowd-sourced ratings"),
    "v5": ("V5 EEG Encoding", "EEG TRF encoding — MI features predict scalp EEG"),
    "v6": ("V6 fMRI Encoding", "fMRI ROI encoding — MI features predict BOLD in 26 brain regions"),
    "v7": ("V7 RSA", "Representational similarity — MI belief RDM vs. acoustic baselines"),
}


def _build_markdown(
    report_json: Dict,
    by_module: Dict[str, List[Dict]],
    module_data: Dict[str, Any],
) -> str:
    """Build comprehensive Markdown report."""
    lines = [
        "# MI Validation Suite — Master Report",
        "",
        f"**Generated:** {report_json['meta']['generated_at']}",
        f"**Platform:** {report_json['meta']['platform']}",
        f"**Python:** {report_json['meta']['python_version'].split()[0]}",
        f"**Host:** {report_json['meta']['hostname']}",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total tests | {report_json['summary']['total_tests']} |",
        f"| Passed | {report_json['summary']['passed']} |",
        f"| Failed | {report_json['summary']['failed']} |",
        f"| Skipped | {report_json['summary']['skipped']} |",
        f"| Duration | {report_json['summary']['total_duration_s']:.1f}s |",
        "",
        "---",
        "",
        "## Module Results",
        "",
        "| Module | Status | Passed | Failed | Skipped | Duration |",
        "|--------|--------|--------|--------|---------|----------|",
    ]

    for tag in ("v1", "v2", "v3", "v4", "v5", "v6", "v7"):
        if tag in report_json["modules"]:
            m = report_json["modules"][tag]
            name = MODULE_DESCRIPTIONS.get(tag, (tag.upper(), ""))[0]
            status_icon = {"PASS": "PASS", "FAIL": "FAIL", "SKIP": "SKIP"}[m["status"]]
            lines.append(
                f"| {name} | {status_icon} | {m['passed']} | "
                f"{m['failed']} | {m['skipped']} | {m['duration_s']:.1f}s |"
            )

    lines.extend(["", "---", ""])

    # ── Per-module detailed sections ──
    for tag in ("v1", "v2", "v3", "v4", "v5", "v6", "v7"):
        if tag not in by_module:
            continue

        name, desc = MODULE_DESCRIPTIONS.get(tag, (tag.upper(), ""))
        lines.extend([
            f"## {name}",
            "",
            f"*{desc}*",
            "",
        ])

        # Per-test details
        tests = by_module[tag]
        lines.append("| Test | Result | Duration | Details |")
        lines.append("|------|--------|----------|---------|")

        for t in tests:
            # Extract short test name from nodeid
            short = t["nodeid"].split("::")[-1] if "::" in t["nodeid"] else t["nodeid"]
            result_str = t["outcome"].upper()
            dur = f"{t.get('duration', 0):.2f}s"
            detail = ""
            if t.get("longrepr"):
                # Extract just the assertion message (last line)
                repr_lines = str(t["longrepr"]).strip().split("\n")
                for rl in reversed(repr_lines):
                    rl = rl.strip()
                    if rl and not rl.startswith("E ") and "assert" not in rl.lower():
                        continue
                    if rl.startswith("E "):
                        detail = rl[2:].strip()[:120]
                        break
                if not detail and repr_lines:
                    detail = repr_lines[-1].strip()[:120]
            lines.append(f"| {short} | {result_str} | {dur} | {detail} |")

        # Module-specific data section
        if tag in module_data:
            lines.extend(["", "### Detailed Results", ""])
            lines.extend(_module_detail_md(tag, module_data[tag]))

        lines.extend(["", "---", ""])

    # ── Validation Scorecard ──
    lines.extend(_validation_scorecard(module_data))
    lines.extend(["", "---", ""])

    # ── Cross-Module Summary ──
    lines.extend(_cross_module_summary(module_data))
    lines.extend(["", "---", ""])

    # ── Figure Index ──
    lines.extend(_figure_index())
    lines.extend(["", "---", ""])

    # ── Inline per-module summaries if files exist ──
    lines.extend([
        "## Per-Module Summary Reports",
        "",
    ])
    for tag in ("v1", "v2", "v3", "v4", "v5", "v6", "v7"):
        summary_path = RESULTS / f"{tag}_*" / f"{tag}_summary.txt"
        # Check actual paths
        result_dir = RESULTS / f"{tag}_{_module_dirname(tag)}"
        summary_file = result_dir / f"{tag}_summary.txt"
        if summary_file.exists():
            lines.extend([
                f"### {MODULE_DESCRIPTIONS.get(tag, (tag.upper(),))[0]}",
                "",
                "```",
                summary_file.read_text().strip(),
                "```",
                "",
            ])

    return "\n".join(lines)


def _module_dirname(tag: str) -> str:
    """Map module tag to directory suffix."""
    mapping = {
        "v1": "pharmacology",
        "v2": "idyom",
        "v3": "krumhansl",
        "v4": "deam",
        "v5": "eeg_encoding",
        "v6": "fmri_encoding",
        "v7": "rsa",
    }
    return mapping.get(tag, tag)


def _validation_scorecard(module_data: Dict[str, Any]) -> List[str]:
    """Generate a scorecard table: primary metric per module + pass/fail."""
    lines = [
        "## Validation Scorecard",
        "",
        "| Module | Primary Metric | Value | Threshold | Status |",
        "|--------|---------------|-------|-----------|--------|",
    ]

    # V1 — directional concordance
    if "v1" in module_data:
        ferreri = module_data["v1"].get("ferreri", [])
        if ferreri:
            # Check if levodopa increased reward
            placebo = ferreri[2] if len(ferreri) > 2 else None
            if placebo and len(ferreri) > 0:
                levo = ferreri[0]
                delta = levo.reward_mean - placebo.reward_mean
                ok = delta > 0
                lines.append(f"| V1 Pharmacology | Levodopa Δ reward | {delta:+.4f} | > 0 | {'PASS' if ok else 'FAIL'} |")

    # V2 — mean r > 0
    if "v2" in module_data:
        agg = module_data["v2"].get("aggregate", {})
        r = agg.get("mean_pearson_r", 0)
        ok = r > 0
        lines.append(f"| V2 IDyOM | Mean Pearson r | {r:.4f} | > 0 | {'PASS' if ok else 'FAIL'} |")

    # V3 — profile correlation
    if "v3" in module_data:
        from scipy.stats import pearsonr
        mi_maj = module_data["v3"].get("mi_major")
        if mi_maj is not None:
            from Validation.v3_krumhansl.profiles import MAJOR_PROFILE
            r, _ = pearsonr(mi_maj, MAJOR_PROFILE)
            ok = r > 0.5
            lines.append(f"| V3 Krumhansl | Major profile r | {r:.4f} | > 0.5 | {'PASS' if ok else 'FAIL'} |")

    # V4 — mean arousal r > 0
    if "v4" in module_data:
        agg = module_data["v4"].get("aggregate", {})
        r = agg.get("mean_r_arousal", 0)
        ok = r > 0
        lines.append(f"| V4 DEAM | Mean arousal r | {r:.4f} | > 0 | {'PASS' if ok else 'FAIL'} |")

    # V5 — full > envelope
    if "v5" in module_data:
        d = module_data["v5"]
        full_r2 = d.get("full", {}).get("mean_r2", 0)
        env_r2 = d.get("envelope", {}).get("mean_r2", 0)
        ok = full_r2 > env_r2
        lines.append(f"| V5 EEG | Full R² > env R² | {full_r2:.4f} > {env_r2:.4f} | Full > env | {'PASS' if ok else 'FAIL'} |")

    # V6 — sig ROIs ≥ 3
    if "v6" in module_data:
        full = module_data["v6"].get("full", {})
        sig = full.get("significant_rois", 0)
        ok = sig >= 3
        lines.append(f"| V6 fMRI | Significant ROIs | {sig}/26 | ≥ 3 | {'PASS' if ok else 'FAIL'} |")

    # V7 — best rho > 0
    if "v7" in module_data:
        comps = module_data["v7"].get("comparisons", [])
        if comps:
            best = max(comps, key=lambda c: c["spearman_rho"])
            ok = best["spearman_rho"] > 0
            lines.append(f"| V7 RSA | Best Spearman ρ | {best['spearman_rho']:.4f} | > 0 | {'PASS' if ok else 'FAIL'} |")

    return lines


def _cross_module_summary(module_data: Dict[str, Any]) -> List[str]:
    """Cross-module convergent validity matrix."""
    lines = [
        "## Cross-Module Summary",
        "",
        "Which MI components contribute to which validations:",
        "",
        "| Component | V1 | V2 | V3 | V4 | V5 | V6 | V7 |",
        "|-----------|----|----|----|----|----|----|----| ",
        "| R³ (perceptual) | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |",
        "| H³ (temporal) | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |",
        "| C³ beliefs | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |",
        "| Neurochemicals | ✓ | — | — | ✓ | ✓ | ✓ | — |",
        "| RAM (brain regions) | — | — | — | — | ✓ | ✓ | — |",
        "| Ψ³ (psychology) | ✓ | — | — | ✓ | — | — | — |",
    ]
    return lines


def _figure_index() -> List[str]:
    """List all generated figures."""
    from Validation.config.paths import FIGURES
    lines = [
        "## Figure Index",
        "",
    ]

    if not FIGURES.exists():
        lines.append("*No figures directory found.*")
        return lines

    figure_files = sorted(FIGURES.rglob("*.pdf")) + sorted(FIGURES.rglob("*.png"))
    if not figure_files:
        lines.append("*No figures generated yet.*")
        return lines

    current_subdir = None
    for f in sorted(figure_files):
        subdir = f.parent.name if f.parent != FIGURES else "root"
        if subdir != current_subdir:
            current_subdir = subdir
            lines.append(f"\n**{subdir}/**")
        lines.append(f"- `{f.name}`")

    return lines


def _module_detail_md(tag: str, data: Dict[str, Any]) -> List[str]:
    """Generate module-specific Markdown detail section."""
    lines = []

    if tag == "v1":
        lines.append("**Ferreri et al. 2019 — Dopamine & Reward:**")
        lines.append("")
        lines.append("| Drug | Reward Mean | DA Mean | OPI Mean |")
        lines.append("|------|------------|---------|----------|")
        for r in data.get("ferreri", []):
            lines.append(
                f"| {r.target.drug} | {r.reward_mean:.4f} | "
                f"{r.da_mean:.4f} | {r.opi_mean:.4f} |"
            )
        lines.append("")
        lines.append("**Mallik et al. 2017 — Opioids & Emotion:**")
        lines.append("")
        lines.append("| Drug | Emotion Mean | OPI Mean |")
        lines.append("|------|-------------|----------|")
        for r in data.get("mallik", []):
            lines.append(
                f"| {r.target.drug} | {r.emotion_mean:.4f} | {r.opi_mean:.4f} |"
            )
        lines.append("")
        lines.append("**Laeng et al. 2021 — Opioids & Arousal/Valence:**")
        lines.append("")
        lines.append("| Drug | Arousal Mean | Valence Mean |")
        lines.append("|------|-------------|--------------|")
        for r in data.get("laeng", []):
            lines.append(
                f"| {r.target.drug} | {r.arousal_mean:.4f} | {r.valence_mean:.4f} |"
            )

    elif tag == "v2":
        agg = data.get("aggregate", {})
        lines.append(f"- Melodies analyzed: {agg.get('n_melodies', '?')}")
        lines.append(f"- Mean Pearson r: {agg.get('mean_pearson_r', '?'):.4f}")
        lines.append(f"- Mean Spearman rho: {agg.get('mean_spearman_rho', '?'):.4f}")
        lines.append(f"- Significant (p<.05): "
                      f"{agg.get('n_significant_005', '?')}/{agg.get('n_melodies', '?')}")
        lines.append("")
        lines.append("**Top 10 melodies:**")
        lines.append("")
        lines.append("| Melody | r | rho | p | n_notes |")
        lines.append("|--------|---|-----|---|---------|")
        for c in data.get("comparisons", [])[:10]:
            lines.append(
                f"| {c['melody_name'][:30]} | {c['pearson_r']:.3f} | "
                f"{c['spearman_rho']:.3f} | {c['pearson_p']:.2e} | {c['n_notes']} |"
            )

    elif tag == "v3":
        import numpy as np
        mi_maj = data.get("mi_major")
        mi_min = data.get("mi_minor")
        if mi_maj is not None and mi_min is not None:
            from Validation.infrastructure.stats import pearson_with_ci
            from Validation.v3_krumhansl.profiles import MAJOR_PROFILE, MINOR_PROFILE, PITCH_CLASS_NAMES
            r_maj, p_maj, _ = pearson_with_ci(mi_maj, MAJOR_PROFILE)
            r_min, p_min, _ = pearson_with_ci(mi_min, MINOR_PROFILE)
            lines.append(f"- Major profile: r={r_maj:.4f}, p={p_maj:.2e}")
            lines.append(f"- Minor profile: r={r_min:.4f}, p={p_min:.2e}")
            lines.append("")
            lines.append("| PC | K-K Major | MI Major | K-K Minor | MI Minor |")
            lines.append("|----|-----------|----------|-----------|----------|")
            kk_maj_n = MAJOR_PROFILE / MAJOR_PROFILE.max()
            mi_maj_n = mi_maj / mi_maj.max() if mi_maj.max() > 0 else mi_maj
            kk_min_n = MINOR_PROFILE / MINOR_PROFILE.max()
            mi_min_n = mi_min / mi_min.max() if mi_min.max() > 0 else mi_min
            for i, name in enumerate(PITCH_CLASS_NAMES):
                lines.append(
                    f"| {name} | {kk_maj_n[i]:.4f} | {mi_maj_n[i]:.4f} | "
                    f"{kk_min_n[i]:.4f} | {mi_min_n[i]:.4f} |"
                )

    elif tag == "v4":
        agg = data.get("aggregate", {})
        lines.append(f"- Songs analyzed: {agg.get('n_songs', '?')}")
        lines.append(f"- Arousal: mean r={agg.get('mean_r_arousal', '?'):.4f}, "
                      f"sig={agg.get('n_sig_arousal_005', '?')}/{agg.get('n_songs', '?')}")
        lines.append(f"- Valence: mean r={agg.get('mean_r_valence', '?'):.4f}, "
                      f"sig={agg.get('n_sig_valence_005', '?')}/{agg.get('n_songs', '?')}")
        lines.append("")
        lines.append("**Per-song correlations:**")
        lines.append("")
        lines.append("| Song | r_arousal | r_valence | p_arousal | p_valence |")
        lines.append("|------|-----------|-----------|-----------|-----------|")
        for s in data.get("per_song", []):
            lines.append(
                f"| {s.get('song_id', '?')} | {s.get('r_arousal', 0):.3f} | "
                f"{s.get('r_valence', 0):.3f} | {s.get('p_arousal', 0):.2e} | "
                f"{s.get('p_valence', 0):.2e} |"
            )

    elif tag == "v6":
        for model_name in ("r3", "beliefs", "ram", "neuro", "full"):
            if model_name in data:
                r = data[model_name]
                lines.append(
                    f"- **{model_name}**: mean R²={r['mean_r2']:.4f}, "
                    f"max R²={r['max_r2']:.4f}, sig ROIs={r['significant_rois']}/26"
                )

    elif tag == "v7":
        for c in data.get("comparisons", []):
            lines.append(
                f"- **{c['model_name']}**: Spearman rho={c['spearman_rho']:.4f}, "
                f"p(perm)={c['p_permutation']:.4f}"
            )

    return lines
