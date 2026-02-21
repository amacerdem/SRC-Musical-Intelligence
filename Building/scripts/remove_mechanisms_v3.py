#!/usr/bin/env python3
"""Remove REMAINING mechanism references from C³ model docs (Pass 3).

After passes 1+2 reduced from ~1,725 to ~472, this pass handles:
  1. Mechanism sub-section detail blocks (#### AED — ..., #### CPD — ...)
  2. Multi-line mechanism variable assignment blocks (aed_arousal = mean(AED[0:8]))
  3. Mechanism sharing explanation paragraphs
  4. Diagram boxes with mechanism dimensions (AED(30D), CPD(30D))
  5. Direct mechanism dimension access (AED[D15], CPD[D0])
  6. Mechanism feed descriptions in diagrams
  7. Remaining inline mechanism references
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MECHANISMS = {"BEP", "PPC", "TPC", "MEM", "TMH", "AED", "ASA", "C0P", "CPD", "SYN"}
MECH_PATTERN = "|".join(sorted(MECHANISMS))
MECH_STAR_PATTERN = MECH_PATTERN + "|BEP\\*"
SKIP_FILES = {"BCH.md"}


def remove_mechanism_subsections(lines: list[str]) -> list[str]:
    """Remove #### MECH — Name (30D) subsections entirely."""
    result = []
    in_section = False
    for line in lines:
        # Match: #### AED — Affective Entrainment Dynamics (30D)
        # Also: ### ASA Mechanism
        if re.match(r'^#{3,4}\s+(' + MECH_PATTERN + r')\s*[—–-]', line):
            in_section = True
            continue
        if re.match(r'^#{3,4}\s+(' + MECH_PATTERN + r')\s+Mechanism', line):
            in_section = True
            continue
        if in_section:
            # End at next heading of same or higher level, or horizontal rule
            if re.match(r'^(#{2,4}\s|---)', line):
                in_section = False
                result.append(line)
            continue
        result.append(line)
    return result


def remove_mechanism_sharing_blocks(lines: list[str]) -> list[str]:
    """Remove mechanism sharing explanation blocks."""
    result = []
    in_block = False
    for line in lines:
        stripped = line.strip()
        # Detect start of mechanism sharing blocks:
        # "AED: SHARED between SRP..."
        # "CPD: SHARED between SRP..."
        # "C0P: SRP ONLY..."
        # "ASA: AAC ONLY..."
        if re.match(r'\s*(' + MECH_PATTERN + r'):\s*(SHARED|.+ONLY)', line):
            in_block = True
            continue
        if in_block:
            # Continue skipping while we see mechanism-related content
            if re.match(r'\s*(' + MECH_PATTERN + r'):\s', line):
                continue
            # Also skip empty lines within the block
            if stripped == '':
                in_block = False
                result.append(line)
                continue
            in_block = False
            result.append(line)
            continue
        result.append(line)
    return result


def remove_mechanism_variable_blocks(lines: list[str]) -> list[str]:
    """Remove consecutive mechanism variable assignment lines."""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Detect mechanism variable assignment:
        # aed_arousal = mean(AED[0:8])   # comment
        # cpd_buildup = mean(CPD[0:10])  # comment
        # asa_segregation = mean(ASA[0:10])
        # Also: c0p_cognitive = mean(C0P[0:10])
        if re.match(r'\s*\w+\s*=\s*mean\((' + MECH_PATTERN + r')\[', line):
            # Skip this and consecutive mechanism variable lines
            while i < len(lines) and (
                re.match(r'\s*\w+\s*=\s*mean\((' + MECH_PATTERN + r')\[', lines[i]) or
                re.match(r'\s*\w+\s*=\s*(' + MECH_PATTERN + r')\[D?\d+\]', lines[i]) or
                lines[i].strip() == ''
            ):
                i += 1
            continue

        # Also: aed_onset_rate = AED[D1]
        if re.match(r'\s*\w+\s*=\s*(' + MECH_PATTERN + r')\[D?\d+\]', line):
            i += 1
            continue

        result.append(line)
        i += 1
    return result


def remove_mechanism_formula_lines(lines: list[str]) -> list[str]:
    """Remove formula lines that reference mechanisms directly."""
    result = []
    for line in lines:
        # Pattern: prediction_error = tanh(AED[D13])
        if re.search(r'=\s*\w*\((' + MECH_PATTERN + r')\[D?\d+\]', line):
            continue
        # Pattern: reaction = σ(0.5 * CPD[D0] + 0.5 * AED[D1])
        if re.search(r'\*\s*(' + MECH_PATTERN + r')\[D?\d+\]', line):
            continue
        # Pattern: prediction_match = tanh(AED[D12] - AED[D11])
        if re.search(r'(' + MECH_PATTERN + r')\[D\d+\]\s*[-+]', line):
            continue
        # Pattern: AED[D15] standalone in formulas
        if re.search(r'(' + MECH_PATTERN + r')\[D\d+\]', line):
            continue
        # Pattern: mean(AED[0:8]) in any context
        if re.search(r'mean\((' + MECH_PATTERN + r')\[', line):
            continue
        result.append(line)
    return result


def should_delete_line(line: str) -> bool:
    """Return True if this line should be deleted entirely."""
    stripped = line.strip()
    if not stripped:
        return False

    # --- Mechanism dimension boxes in diagrams ---
    # "       AED(30D)    CPD(30D)    ASA(30D)"
    if re.match(r'\s+(' + MECH_PATTERN + r')\(\d+D\)', stripped):
        return True
    # Multiple mechanisms on one diagram line
    mech_dim_matches = re.findall(r'(' + MECH_PATTERN + r')\(\d+D\)', line)
    if len(mech_dim_matches) >= 2:
        return True

    # --- Feed descriptions in diagrams ---
    # "│  Feeds: AED (arousal, expectancy), CPD (triggers, peaks),"
    # "│         C0P (cognitive state)"
    if re.search(r'Feeds:\s*(' + MECH_PATTERN + r')\s', line):
        return True
    # Continuation of feeds
    if re.match(r'[│\s]+(' + MECH_PATTERN + r')\s+\(', stripped):
        return True

    # --- Mechanism table header rows ---
    # "AED       │ H6 (200ms),         │ 21 pairs           │ 21 × 2 = 42"
    if re.match(r'\s*(' + MECH_PATTERN + r')\s+│', line):
        return True

    # --- Mechanism arrows in diagrams ---
    # "  AED (arousal dynamics) ──► SRP reads arousal → wanting"
    # "  CPD (peak detection)  ──► SRP reads buildup → tension"
    if re.match(r'\s+(' + MECH_PATTERN + r')\s+\([\w\s]+\)\s*[─═►]', line):
        return True

    # --- Mechanism sharing lines ---
    # "Shared:    AED → SRP + AAC + VMM     (3 readers)"
    # "AAC only:  ASA → AAC                 (1 reader)"
    if re.search(r'(Shared|only):\s+(' + MECH_PATTERN + r')\s*→', line):
        return True

    # --- "The SRP model reads from AED, CPD, C0P mechanisms..." ---
    if re.search(r'reads?\s+from\s+(' + MECH_PATTERN + r')', line):
        return True

    # --- "VMM adds no new mechanisms" ---
    if re.search(r'no new mechanisms', line, re.IGNORECASE):
        return True

    # --- Mechanism descriptions in bullet points ---
    # "- SRP reads AED arousal + expectancy + motor-affective for **reward dynamics**"
    if re.match(r'\s*-\s+\w+\s+reads?\s+(' + MECH_PATTERN + r')\s', line):
        return True

    # --- "# Real-time emotional intensity (AED drives, CPD modulates)" ---
    if re.search(r'\((' + MECH_PATTERN + r')\s+(drives?|modulates?)', line):
        return True

    # --- "Note: The three delay windows map cleanly onto TMH's" ---
    if re.search(r"map\w*\s+.*onto\s+.*(" + MECH_PATTERN + r")", line):
        return True

    # --- "Window   Delay   Brain Region   TMH Sub-section   Function" ---
    if re.search(r'(' + MECH_PATTERN + r')\s+Sub-section', line):
        return True

    # --- Mechanism-only comment lines ---
    # "# VMM COMPUTATION: AED(30D) + C0P(30D) + 7 H³ direct reads → 12D"
    if re.search(r'(' + MECH_PATTERN + r')\(\d+D\)\s*\+\s*(' + MECH_PATTERN + r')\(\d+D\)', line):
        return True

    # --- Diagram lines with mechanism references ---
    # "    (AED/CPD mechanisms)                     (Direct H³ reads)"
    if re.search(r'\((' + MECH_PATTERN + r')[/+](' + MECH_PATTERN + r')\s+mechanisms?\)', line):
        return True

    # --- Mechanism column in process tables ---
    # Lines in table that start with mechanism name in italic or bold
    if re.match(r'\s*\|.*(' + MECH_PATTERN + r')\s+(mechanism|reads|shared|drives|Mechanism)', line):
        return True

    return False


def clean_inline_refs(line: str) -> str:
    """Clean remaining inline mechanism references."""

    # "adding the ASA mechanism" → "adding auditory scene analysis"
    line = re.sub(r'the\s+ASA\s+mechanism', 'auditory scene analysis', line)
    line = re.sub(r'the\s+AED\s+mechanism', 'affective entrainment dynamics', line)
    line = re.sub(r'the\s+CPD\s+mechanism', 'consummatory phase dynamics', line)
    line = re.sub(r'the\s+C0P\s+mechanism', 'cognitive projection', line)
    line = re.sub(r'the\s+BEP\s+mechanism', 'beat entrainment processing', line)
    line = re.sub(r'the\s+PPC\s+mechanism', 'pitch processing', line)
    line = re.sub(r'the\s+TPC\s+mechanism', 'timbre processing', line)
    line = re.sub(r'the\s+MEM\s+mechanism', 'memory integration', line)
    line = re.sub(r'the\s+TMH\s+mechanism', 'temporal memory hierarchy', line)
    line = re.sub(r'the\s+SYN\s+mechanism', 'synthesis', line)

    # "AED and CPD mechanisms" → "affective and consummatory mechanisms"
    line = re.sub(r'(' + MECH_PATTERN + r')\s+and\s+(' + MECH_PATTERN + r')\s+mechanisms', 'shared reward', line)

    # "sharing AED and CPD mechanisms with SRP" → "sharing reward pathways with SRP"
    line = re.sub(r'sharing\s+(' + MECH_PATTERN + r')\s+and\s+(' + MECH_PATTERN + r')\s+mechanisms', 'sharing reward pathways', line)

    # "Prediction error (AED/CPD) → DA release" → "Prediction error → DA release"
    line = re.sub(r'\((' + MECH_PATTERN + r')[/+](' + MECH_PATTERN + r')\)', '', line)
    # Also: "(AED)" → ""
    line = re.sub(r'\((' + MECH_PATTERN + r')\)', '', line)

    # "in addition to mechanism sub-section means" → ""
    line = re.sub(r',?\s*in addition to mechanism sub-section means', '', line)

    # "NOT covered by AED (H6+H16) or C0P (H11)" → "at longer timescales"
    line = re.sub(
        r'NOT covered by (' + MECH_PATTERN + r')\s*\([^)]+\)\s*(or|and)\s*(' + MECH_PATTERN + r')\s*\([^)]+\)',
        'at longer timescales',
        line
    )

    # "Mechanisms: AED, CPD, C0P, ASA" → remove
    line = re.sub(r'Mechanisms?:\s*(' + MECH_PATTERN + r')[\s,]*(' + MECH_PATTERN + r')?[\s,]*(' + MECH_PATTERN + r')?[\s,]*(' + MECH_PATTERN + r')?', '', line)

    # "| No independent ASA→AAC effect → ASA redundant |" — clean mechanism names
    line = re.sub(r'(' + MECH_PATTERN + r')→(' + MECH_PATTERN + r')', lambda m: f'{m.group(1)}→{m.group(2)}' if m.group(1) not in MECHANISMS else '', line)

    # Clean "AED + CPD + C0P" patterns
    line = re.sub(r'\b(' + MECH_PATTERN + r')\s*\+\s*(' + MECH_PATTERN + r')\s*\+\s*(' + MECH_PATTERN + r')\b', 'H³ direct', line)
    line = re.sub(r'\b(' + MECH_PATTERN + r')\s*\+\s*(' + MECH_PATTERN + r')\b', 'H³ direct', line)

    # "SRP and AAC share AED and CPD mechanisms" → remove
    if re.search(r'share\s+(' + MECH_PATTERN + r')\s+and', line):
        line = re.sub(r'share\s+(' + MECH_PATTERN + r')\s+and\s+(' + MECH_PATTERN + r')\s+mechanisms?\.?', 'share reward pathway mechanisms.', line)

    # "adding only ~15 new H³ tuples (ASA + new direct reads)" → clean
    line = re.sub(r'\((' + MECH_PATTERN + r')\s*\+\s*new', '(new', line)

    # "— VMM does NOT use CPD" → remove
    line = re.sub(r'—\s+\w+\s+does\s+NOT\s+use\s+(' + MECH_PATTERN + r')', '', line)

    # Clean double spaces
    line = re.sub(r'  +', ' ', line)
    # Clean trailing spaces
    line = line.rstrip()

    return line


def process_file(filepath: Path) -> tuple[int, int]:
    """Process a single model .md file."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Phase 1: Section-level removals
    lines = remove_mechanism_subsections(lines)
    lines = remove_mechanism_sharing_blocks(lines)
    lines = remove_mechanism_variable_blocks(lines)
    lines = remove_mechanism_formula_lines(lines)

    # Phase 2: Line-level deletions
    kept = []
    deleted = 0
    for line in lines:
        if should_delete_line(line):
            deleted += 1
        else:
            kept.append(line)
    lines = kept

    # Phase 3: Inline substitutions
    modified = 0
    cleaned = []
    for line in lines:
        new_line = clean_inline_refs(line)
        if new_line != line:
            modified += 1
        cleaned.append(new_line)
    lines = cleaned

    # Phase 4: Clean up consecutive empty lines (max 2)
    final = []
    empty_count = 0
    for line in lines:
        if line.strip() == '':
            empty_count += 1
            if empty_count <= 2:
                final.append(line)
        else:
            empty_count = 0
            final.append(line)
    lines = final

    new_content = "\n".join(lines)
    if new_content != content:
        filepath.write_text(new_content, encoding="utf-8")
        return (deleted, modified)
    return (0, 0)


def main():
    models_dir = Path("/Volumes/SRC-9/SRC Musical Intelligence/Docs/C³/Models")
    if not models_dir.exists():
        print(f"ERROR: {models_dir} not found")
        sys.exit(1)

    model_files = []
    for subdir in sorted(models_dir.iterdir()):
        if subdir.is_dir():
            for md_file in subdir.glob("*.md"):
                if md_file.name not in SKIP_FILES:
                    model_files.append(md_file)
    index_file = models_dir / "00-INDEX.md"
    if index_file.exists():
        model_files.append(index_file)

    print(f"Processing {len(model_files)} files (pass 3)...")
    print()

    total_deleted = 0
    total_modified = 0
    files_changed = 0

    for filepath in sorted(model_files):
        rel_path = filepath.relative_to(models_dir)
        deleted, modified = process_file(filepath)
        if deleted > 0 or modified > 0:
            files_changed += 1
            total_deleted += deleted
            total_modified += modified
            print(f"✓ {rel_path}: {deleted} del, {modified} mod")

    print()
    print(f"Summary: {files_changed} files changed, {total_deleted} del, {total_modified} mod")


if __name__ == "__main__":
    main()
