#!/usr/bin/env python3
"""Sequential validation runner — optimized for 8 GB RAM.

Runs V1-V7 in a single process, with memory cleanup between modules.
Never run multiple pytest sessions in parallel on constrained hardware.

Usage:
    python Validation/run_all.py              # run all modules
    python Validation/run_all.py v1 v3        # run only V1 and V3
    python Validation/run_all.py --report     # run all + generate reports
"""
from __future__ import annotations

import gc
import subprocess
import sys
import time
from pathlib import Path

VALIDATION_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = VALIDATION_ROOT.parent

MODULES = [
    ("v1", "v1_pharmacology", "Pharmacology (Ferreri, Mallik, Laeng)"),
    ("v2", "v2_idyom", "IDyOM Convergent Validity"),
    ("v3", "v3_krumhansl", "Krumhansl Tonal Hierarchy"),
    ("v4", "v4_deam", "DEAM Continuous Emotion"),
    ("v5", "v5_eeg_encoding", "EEG Encoding Models"),
    ("v6", "v6_fmri_encoding", "fMRI ROI Encoding"),
    ("v7", "v7_rsa", "RSA Analysis"),
]


def run_module(module_dir: str, label: str) -> tuple[int, float]:
    """Run a single validation module via pytest subprocess."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"{'='*60}")

    t0 = time.time()
    result = subprocess.run(
        [
            sys.executable, "-m", "pytest",
            str(VALIDATION_ROOT / module_dir),
            "-v", "--tb=short", "-x",
        ],
        cwd=str(PROJECT_ROOT),
    )
    elapsed = time.time() - t0

    status = "PASS" if result.returncode == 0 else (
        "SKIP" if result.returncode == 5 else "FAIL"
    )
    print(f"\n  [{status}] {label} — {elapsed:.1f}s")

    # Force cleanup between modules
    gc.collect()
    return result.returncode, elapsed


def main() -> None:
    args = sys.argv[1:]
    do_report = "--report" in args
    args = [a for a in args if not a.startswith("--")]

    # Filter modules if specific ones requested
    if args:
        selected = [m for m in MODULES if m[0] in args]
    else:
        selected = MODULES

    print(f"\nMI Validation Suite — {len(selected)} module(s)")
    print(f"RAM optimization: 15s excerpts, gc.collect() between tests\n")

    results = {}
    total_t0 = time.time()

    for tag, module_dir, label in selected:
        rc, elapsed = run_module(module_dir, label)
        results[tag] = {"returncode": rc, "elapsed": elapsed}

    total_elapsed = time.time() - total_t0

    # Summary
    print(f"\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    for tag, module_dir, label in selected:
        r = results[tag]
        status = "PASS" if r["returncode"] == 0 else (
            "SKIP" if r["returncode"] == 5 else "FAIL"
        )
        print(f"  [{status}] {tag.upper()}: {label} ({r['elapsed']:.1f}s)")
    print(f"\n  Total: {total_elapsed:.1f}s")

    passed = sum(1 for r in results.values() if r["returncode"] == 0)
    skipped = sum(1 for r in results.values() if r["returncode"] == 5)
    failed = len(results) - passed - skipped
    print(f"  {passed} passed, {skipped} skipped, {failed} failed")

    if do_report:
        print(f"\n{'='*60}")
        print(f"  Compiling master report from per-module summaries...")
        print(f"{'='*60}")
        _compile_runner_report(results, selected, total_elapsed)

    sys.exit(1 if failed > 0 else 0)


def _compile_runner_report(
    results: dict, selected: list, total_elapsed: float,
) -> None:
    """Compile a master report from run_all.py results + per-module summaries."""
    import json
    import platform
    from datetime import datetime, timezone

    results_dir = VALIDATION_ROOT / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    # Collect per-module summaries
    module_summaries = {}
    for tag, module_dir, label in selected:
        dirname = module_dir  # e.g. "v1_pharmacology"
        summary_file = results_dir / dirname / f"{tag}_summary.txt"
        if summary_file.exists():
            module_summaries[tag] = summary_file.read_text()

    # Build JSON
    report = {
        "meta": {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "runner": "run_all.py",
            "python_version": sys.version,
            "platform": platform.platform(),
            "hostname": platform.node(),
        },
        "summary": {
            "total_modules": len(selected),
            "passed": sum(1 for r in results.values() if r["returncode"] == 0),
            "failed": sum(1 for r in results.values()
                          if r["returncode"] not in (0, 5)),
            "skipped": sum(1 for r in results.values() if r["returncode"] == 5),
            "total_duration_s": round(total_elapsed, 2),
        },
        "modules": {
            tag: {
                "label": label,
                "status": "PASS" if results[tag]["returncode"] == 0 else (
                    "SKIP" if results[tag]["returncode"] == 5 else "FAIL"
                ),
                "duration_s": round(results[tag]["elapsed"], 2),
                "has_summary": tag in module_summaries,
            }
            for tag, _, label in selected
        },
    }

    json_path = results_dir / "master_report.json"
    json_path.write_text(json.dumps(report, indent=2))

    # Build Markdown
    lines = [
        "# MI Validation Suite — Master Report",
        "",
        f"**Generated:** {report['meta']['generated_at']}",
        f"**Platform:** {report['meta']['platform']}",
        f"**Runner:** run_all.py (subprocess per module)",
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Modules | {report['summary']['total_modules']} |",
        f"| Passed | {report['summary']['passed']} |",
        f"| Failed | {report['summary']['failed']} |",
        f"| Skipped | {report['summary']['skipped']} |",
        f"| Duration | {report['summary']['total_duration_s']:.1f}s |",
        "",
        "---",
        "",
        "## Module Results",
        "",
        "| Module | Status | Duration |",
        "|--------|--------|----------|",
    ]
    for tag, _, label in selected:
        m = report["modules"][tag]
        lines.append(f"| {label} | {m['status']} | {m['duration_s']:.1f}s |")

    # Inline per-module summaries
    lines.extend(["", "---", "", "## Detailed Per-Module Reports", ""])
    for tag, _, label in selected:
        if tag in module_summaries:
            lines.extend([
                f"### {label}",
                "",
                "```",
                module_summaries[tag].strip(),
                "```",
                "",
            ])
        else:
            lines.append(f"### {label}\n\n*No summary report generated.*\n")

    md_path = results_dir / "master_report.md"
    md_path.write_text("\n".join(lines))

    print(f"  JSON: {json_path}")
    print(f"  MD:   {md_path}")


if __name__ == "__main__":
    main()
