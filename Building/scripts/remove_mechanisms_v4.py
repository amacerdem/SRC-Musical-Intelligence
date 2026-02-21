#!/usr/bin/env python3
"""Remove REMAINING mechanism references from C³ model docs (Pass 4 — final).

After passes 1-3 reduced from ~1,725 to ~331, this pass handles the last
remaining references by replacing mechanism acronyms with descriptive terms
and deleting mechanism-specific diagram elements.

Strategy: Replace mechanism names used as pathway/route labels with
descriptive neuroscience terms that preserve the scientific meaning.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MECHANISMS = {"BEP", "PPC", "TPC", "MEM", "TMH", "AED", "ASA", "C0P", "CPD", "SYN"}
MECH_PATTERN = "|".join(sorted(MECHANISMS))
MECH_STAR_PATTERN = MECH_PATTERN + "|BEP\\*"
SKIP_FILES = {"BCH.md"}

# Descriptive replacements for mechanism names as pathway labels
MECH_DESCRIPTIONS = {
    "BEP": "beat-entrainment",
    "PPC": "pitch-processing",
    "TPC": "timbre-processing",
    "MEM": "memory-encoding",
    "TMH": "temporal-context",
    "AED": "affective-dynamics",
    "ASA": "auditory-scene",
    "C0P": "cognitive-projection",
    "CPD": "peak-detection",
    "SYN": "synthesis",
}


def should_delete_line(line: str) -> bool:
    """Lines that should be removed entirely."""
    stripped = line.strip()
    if not stripped:
        return False

    # Diagram boxes: "║ │ AED MECHANISM │"
    if re.search(r'│\s*(' + MECH_PATTERN + r')\s+MECHANISM\s*│', line):
        return True

    # Mechanism diagram lines: "║ │ C0P MECHANISM │"
    if re.search(r'(' + MECH_PATTERN + r')\s+MECHANISM', line):
        return True

    # Mechanism description comment lines in diagrams
    # "AED H6 (200ms): Cross-modal binding window (~τ_bind)"
    if re.match(r'\s*(' + MECH_PATTERN + r')\s+H\d+\s*\(\d+m?s\):', line):
        return True

    # Mechanism legacy explanation paragraphs
    # "Legacy used **ASA** ... MI architecture replaces ASA with **C0P** because:"
    if re.search(r'Legacy\s+used\s+\*\*(' + MECH_PATTERN + r')\*\*', line):
        return True
    # "- ASA is not one of the 3 defined ARU mesolimbic mechanisms"
    if re.search(r'(' + MECH_PATTERN + r')\s+is\s+not\s+one\s+of', line):
        return True
    # "- C0P's cognitive integration function better models..."
    if re.match(r'\s*-\s*(' + MECH_PATTERN + r')\'s\s', line):
        return True

    # Mechanism timeline rows in diagrams
    # "│ │ C0P H11 │ │"
    if re.match(r'\s*│\s*│?\s*(' + MECH_PATTERN + r')\s+H\d+\s*│', line):
        return True

    # Mechanism route labels in diagrams that are pure mechanism references
    # "║ │ │ (BEP route) │ │ (BEP route) │ │ (BEP route) │ │ ║"
    if re.search(r'\((' + MECH_PATTERN + r')\s+route\)', line):
        # Count mechanism route refs
        routes = re.findall(r'\((' + MECH_PATTERN + r')\s+route\)', line)
        # If entire line is just route labels in a diagram, delete
        cleaned = re.sub(r'\((' + MECH_PATTERN + r')\s+route\)', '', line)
        cleaned = re.sub(r'[║│\s]', '', cleaned)
        if len(cleaned) < 5:
            return True

    return False


def replace_mechanism_names(line: str) -> str:
    """Replace mechanism acronyms with descriptive terms."""

    # Don't modify lines that are already clean (no mechanism refs)
    if not re.search(r'\b(' + MECH_PATTERN + r')\b', line):
        return line

    # --- Route/pathway labels ---
    # "(BEP route)" → "(beat-entrainment route)"
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'\(' + mech + r'\s+route\)', f'({desc} route)', line)
        line = re.sub(r'\(' + mech + r'\s+pathway\)', f'({desc} pathway)', line)

    # --- "BEP pathway" / "TMH pathway" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'\b' + mech + r'\s+pathway\b', f'{desc} pathway', line)
        line = re.sub(r'\b' + mech + r'\s+route\b', f'{desc} route', line)

    # --- BEP(args) function-style → beat_entrainment(args) ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        pattern = r'\b' + mech + r'\(([^)]+)\)'
        repl = desc.replace('-', '_') + r'(\1)'
        line = re.sub(pattern, repl, line)

    # --- "via BEP" → "via beat-entrainment H³" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'via\s+' + mech + r'\b', f'via {desc} H³', line)

    # --- "from BEP" → "from beat-entrainment H³" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'from\s+' + mech + r'\b', f'from {desc} H³', line)

    # --- "BEP at H6 (200ms)" → "beat-entrainment H³ at H6 (200ms)" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'\b' + mech + r'\s+at\s+(H\d+)', desc + r' H³ at \1', line)

    # --- "BEP motor quality" → "beat-entrainment motor quality" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        # Only replace when followed by a lowercase word (not another acronym)
        line = re.sub(r'\b' + mech + r'\s+([a-z])', desc + r' \1', line)

    # --- "TMH-based" → "temporal-context-based" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'\b' + mech + r'-based\b', desc + '-based', line)

    # --- "× TMH weight" → "× temporal-context weight" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'×\s*' + mech + r'\s+weight', f'× {desc} weight', line)

    # --- BEP in table cells and descriptions ---
    # "| TMH context complexity |" → "| temporal-context complexity |"
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'\b' + mech + r'\s+context\b', desc + ' context', line)

    # --- "# BEP route — Entrainment" → "# Beat-entrainment route — Entrainment" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'#\s+' + mech + r'\s+route', f'# {desc.title()} route', line)

    # --- "High BEP automaticity" → "High beat-entrainment automaticity" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'High\s+' + mech + r'\b', f'High {desc}', line)

    # --- "BEP predicts" → "Beat-entrainment predicts" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'\*\*' + mech + r'\s+predicts', f'**{desc.title()} predicts', line)

    # --- "BEP regularity" → "beat-entrainment regularity" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'\(' + mech + r'\s+(\w+)\)', f'({desc} \\1)', line)

    # --- "TMH long-context" → "temporal-context long-context" → simplify to "long-context" ---
    line = re.sub(r'temporal-context\s+long-context', 'temporal long-context', line)
    line = re.sub(r'temporal-context\s+short-context', 'temporal short-context', line)

    # --- Remaining standalone mechanism names → descriptive ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        # Only replace remaining standalone mechanism names that are clearly labels
        # Be more cautious here — only replace in specific contexts
        # Migration table: "| ... | beat_induction via BEP |"
        line = re.sub(r'via\s+' + mech + r'\s*\|', f'via H³ direct |', line)

    # --- BEP = ..., TMH = ... in definitions ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'\b' + mech + r'\s*=\s*', desc + ' = ', line)

    # --- "BEP aggregation" → "beat-entrainment aggregation" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'\b' + mech + r'\s+(aggregation|weighted|entropy)', desc + r' \1', line)

    # --- "#   AED affect state" → "#   affective-dynamics affect state" ---
    for mech, desc in MECH_DESCRIPTIONS.items():
        line = re.sub(r'(' + mech + r')\s+(affect|arousal|valence)', desc + r' \2', line)

    # --- Final: any remaining standalone mechanism names ---
    # Only in comments, table cells, or prose (not in code/formulas)
    for mech, desc in MECH_DESCRIPTIONS.items():
        # Replace remaining if preceded by specific patterns
        line = re.sub(r'×\s+' + mech + r'\b', f'× {desc}', line)
        line = re.sub(r'\b' + mech + r'\s+automaticity', f'{desc} automaticity', line)
        line = re.sub(r'\b' + mech + r'\s+mastery', f'{desc} mastery', line)
        line = re.sub(r'\b' + mech + r'\s+weighted', f'{desc} weighted', line)

    return line


def process_file(filepath: Path) -> tuple[int, int]:
    """Process a single model .md file."""
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")

    # Phase 1: Line deletions
    kept = []
    deleted = 0
    for line in lines:
        if should_delete_line(line):
            deleted += 1
        else:
            kept.append(line)
    lines = kept

    # Phase 2: Inline replacements
    modified = 0
    cleaned = []
    for line in lines:
        new_line = replace_mechanism_names(line)
        if new_line != line:
            modified += 1
        cleaned.append(new_line)
    lines = cleaned

    # Phase 3: Clean up consecutive empty lines (max 2)
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

    print(f"Processing {len(model_files)} files (pass 4 — final)...")
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
    print(f"Summary: {files_changed} files, {total_deleted} del, {total_modified} mod")


if __name__ == "__main__":
    main()
