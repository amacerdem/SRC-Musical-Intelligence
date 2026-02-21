#!/usr/bin/env python3
"""Remove mechanism references from all C³ model documentation files.

Mechanisms (BEP, PPC, TPC, MEM, TMH, AED, ASA, C0P, CPD, SYN) are a legacy
concept from the HC⁰ architecture. In the C³ architecture, the depth hierarchy
(Relay → Encoder → Associator → Integrator → Hub) replaces mechanisms entirely.

This script removes mechanism-related content from model .md files while
preserving all scientific content, R³/H³ specifications, and output definitions.

Patterns removed:
  1. Section 5.2 "Mechanism Binding" (entire subsection)
  2. MECHANISM_NAMES in pseudocode
  3. mechanism_outputs parameter and variables
  4. Mechanism sub-section slicing (bep_beat = bep[..., 0:10])
  5. Lines in formulas referencing mechanism names
  6. Validation summary mechanism lines
  7. Legacy "Why X replaces HC⁰ mechanisms" sections
  8. Mechanism names in section headers (e.g., "→ BEP+ASA →")
  9. Mechanism boxes in ASCII diagrams
  10. H³ demand comment labels ("── BEP horizons: ──")
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path


# All 10 mechanism acronyms
MECHANISMS = {"BEP", "PPC", "TPC", "MEM", "TMH", "AED", "ASA", "C0P", "CPD", "SYN"}
MECH_PATTERN = "|".join(MECHANISMS)

# Files to skip (no mechanisms)
SKIP_FILES = {"BCH.md", "00-INDEX.md"}


def remove_section_52(lines: list[str]) -> list[str]:
    """Remove Section 5.2 'Mechanism Binding' (from ### 5.2 to next --- or ##)."""
    result = []
    in_section = False
    for line in lines:
        if re.match(r"^###\s+5\.2\b.*[Mm]echanism", line):
            in_section = True
            continue
        if in_section:
            # End of section: next major heading or horizontal rule before section 6
            if re.match(r"^(---|##\s)", line):
                in_section = False
                result.append(line)
            continue
        result.append(line)
    return result


def remove_legacy_mechanism_section(lines: list[str]) -> list[str]:
    """Remove 'Why X replaces HC⁰ mechanisms' subsection at end of doc."""
    result = []
    in_section = False
    for line in lines:
        if re.match(r"^###\s+Why\s+.*replaces?\s+HC", line, re.IGNORECASE):
            in_section = True
            continue
        if in_section:
            # End when we hit a major heading, horizontal rule, or end of file
            if re.match(r"^(---|##\s|#\s|\*\*Model Status)", line):
                in_section = False
                result.append(line)
            continue
        result.append(line)
    return result


def remove_mechanism_lines(lines: list[str]) -> list[str]:
    """Remove individual lines that are purely mechanism-related."""
    result = []
    skip_next_empty = False

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Skip MECHANISM_NAMES line
        if "MECHANISM_NAMES" in line:
            skip_next_empty = True
            continue

        # Skip mechanism_outputs variable assignments
        # e.g.: bep = mechanism_outputs["BEP"]
        if re.search(r'=\s*mechanism_outputs\[', line):
            skip_next_empty = True
            continue

        # Skip mechanism sub-section slicing
        # e.g.: bep_beat = bep[..., 0:10]
        # Pattern: var = short_var[..., N:M] where short_var is 2-3 chars
        if re.match(r'\s+\w+_\w+\s*=\s*\w{2,4}\[\.\.\.,\s*\d+:\d+\]', line):
            # Check if the variable name starts with a known mechanism-related prefix
            var_match = re.match(r'\s+(\w+)', line)
            if var_match:
                var_name = var_match.group(1).lower()
                # Common patterns: bep_beat, bep_motor, asa_scene, ppc_pitch, etc.
                mech_prefixes = {m.lower() for m in MECHANISMS}
                if any(var_name.startswith(p + "_") for p in mech_prefixes):
                    skip_next_empty = True
                    continue

        # Skip # ASA/BEP/PPC sub-sections comments
        if re.match(r'\s+#\s+(' + MECH_PATTERN + r')\s+sub-section', line, re.IGNORECASE):
            continue

        # Skip standalone mechanism variable comments
        # e.g.: # ── BEP horizons: beat/meter tracking ──
        if re.match(r'\s+#\s+──\s+(' + MECH_PATTERN + r')\s+horizons', line):
            continue

        # Skip mechanism reference in h3_demand comments
        # e.g.: # ── ASA horizons: attentional gating ──
        if re.match(r'\s+#\s+──.*(' + MECH_PATTERN + r').*──', line):
            continue

        # Skip validation summary mechanism lines
        # e.g.: | **BEP Mechanism** | 30D (3 sub-sections) | ...
        if re.match(r'\|\s*\*\*(' + MECH_PATTERN + r')\s+Mechanism\*\*', line):
            continue

        # Skip mechanism interaction lines in cross-unit diagrams
        # e.g.: │  BEP mechanism (30D) ──────────► SNEM (beat/motor processing)
        if re.search(r'(' + MECH_PATTERN + r')\s+mechanism\s+\(\d+D\)', line):
            continue

        # Handle empty line after removed content
        if skip_next_empty and stripped == "":
            skip_next_empty = False
            continue
        skip_next_empty = False

        result.append(line)

    return result


def clean_mechanism_in_formulas(lines: list[str]) -> list[str]:
    """Remove mechanism references within formulas and output specs."""
    result = []

    for line in lines:
        # Remove lines in formulas that reference mechanism[N:M]
        # e.g.: + 0.25 * mean(BEP.beat[0:10]))
        # e.g.: + 0.30 * bep_motor.mean(-1, keepdim=True)
        stripped = line.strip()

        # Pattern: formula continuation with mechanism reference
        if re.search(r'\*\s*mean\((' + MECH_PATTERN + r')\.', line):
            continue
        if re.search(r'\*\s*(' + MECH_PATTERN.lower() + r')_\w+\.mean\(', line, re.IGNORECASE):
            continue

        # Pattern: mechanism variable .mean() calls
        # e.g.: beat_locked = bep_beat.mean(-1, keepdim=True)
        mech_prefixes_lower = {m.lower() for m in MECHANISMS}
        if any(re.search(r'\b' + p + r'_\w+\.mean\(', line) for p in mech_prefixes_lower):
            continue

        # Pattern: lines like "0.5 * bep_beat.mean(-1, keepdim=True)"
        if any(re.search(r'\d+\.?\d*\s*\*\s*' + p + r'_', line) for p in mech_prefixes_lower):
            continue

        # Pattern: standalone mechanism variable reference
        # e.g.: template_match = ppc_cons.mean(-1, keepdim=True)
        if any(re.search(r'=\s*' + p + r'_\w+\.', line) for p in mech_prefixes_lower):
            continue

        result.append(line)

    return result


def clean_pseudocode_compute(lines: list[str]) -> list[str]:
    """Fix compute() signature and docstring to remove mechanism_outputs."""
    result = []
    i = 0
    while i < len(lines):
        line = lines[i]

        # Fix compute() signature: remove mechanism_outputs parameter
        if "def compute(self, mechanism_outputs" in line:
            # Replace with Nucleus-compatible signature
            new_line = re.sub(
                r'def compute\(self,\s*mechanism_outputs:\s*Dict,\s*h3_direct:\s*Dict,',
                'def compute(self, h3_features: Dict,',
                line
            )
            result.append(new_line)
            i += 1
            continue

        # Fix docstring references to mechanism_outputs
        if 'mechanism_outputs:' in line and ('{"' in line or "BEP" in line or "PPC" in line):
            i += 1
            continue

        # Fix class docstring: "Reads: BEP mechanism (30D), ..."
        if re.search(r'Reads:\s+(' + MECH_PATTERN + r')\s+mechanism', line):
            new_line = re.sub(
                r'Reads:\s+.*mechanism.*,\s*R³\s+direct\.?',
                'Reads: R³ + H³ direct.',
                line
            )
            if new_line != line:
                result.append(new_line)
            else:
                result.append(re.sub(r'Reads:.*', 'Reads: R³ + H³ direct.', line))
            i += 1
            continue

        result.append(line)
        i += 1

    return result


def clean_diagram_headers(lines: list[str]) -> list[str]:
    """Clean mechanism names from section headers and diagram labels."""
    result = []

    for line in lines:
        # Section header: "### 2.1 Information Flow Architecture (EAR → BRAIN → BEP+ASA → SNEM)"
        # → "### 2.1 Information Flow Architecture (EAR → BRAIN → SNEM)"
        if re.match(r'^###.*Information Flow', line):
            # Remove mechanism part from the flow
            new_line = re.sub(
                r'→\s*(' + MECH_PATTERN + r')[\+/]?(' + MECH_PATTERN + r')?\s*→',
                '→',
                line
            )
            # Also handle 3-mechanism case: AED+CPD+C0P
            new_line = re.sub(
                r'→\s*(' + MECH_PATTERN + r')[\+/](' + MECH_PATTERN + r')[\+/](' + MECH_PATTERN + r')\s*→',
                '→',
                new_line
            )
            result.append(new_line)
            continue

        # Diagram boxes: "║  │  BEP (30D)      │  │  ASA (30D)      │"
        if re.search(r'(' + MECH_PATTERN + r')\s+\(\d+D\)', line):
            continue

        # Diagram: mechanism horizon labels
        if re.search(r'──\s+(' + MECH_PATTERN + r')\s+Horizons\s+──', line, re.IGNORECASE):
            continue

        result.append(line)

    return result


def clean_output_spec_mechanism_refs(lines: list[str]) -> list[str]:
    """Remove mechanism references from output specification tables."""
    result = []

    for line in lines:
        stripped = line.strip()

        # Remove lines in output spec that contain ONLY mechanism references
        # e.g.: "    │                          │        │       + 0.25 * mean(BEP.beat[0:10]))"
        if re.search(r'mean\((' + MECH_PATTERN + r')\.', line):
            continue

        # Remove lines like: "    │                          │        │ BEP beat-locked neural activity."
        if re.match(r'\s*│.*(' + MECH_PATTERN + r')\s+(beat|motor|pitch|scene|attn|valence|arousal|anticip|peak|tension|expect|approach|memory|groove|working|long|short|spectral|temporal|source|salience)', line):
            # But keep if it's an actual dimension name, not a mechanism reference
            # Check if this is the description column of the output table
            if re.search(r'│\s*(' + MECH_PATTERN + r')\s+\w', line) and "│" in line:
                # This is likely a description — keep but remove the mechanism prefix
                new_line = re.sub(r'(' + MECH_PATTERN + r')\s+', '', line)
                result.append(new_line)
                continue

        result.append(line)

    return result


def process_file(filepath: Path) -> tuple[int, list[str]]:
    """Process a single model .md file.

    Returns:
        (change_count, list_of_changes)
    """
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    original_count = len(lines)

    changes = []

    # Apply transformations in order
    lines = remove_section_52(lines)
    if len(lines) < original_count:
        diff = original_count - len(lines)
        changes.append(f"  Removed Section 5.2 Mechanism Binding ({diff} lines)")
        original_count = len(lines)

    lines = remove_legacy_mechanism_section(lines)
    if len(lines) < original_count:
        diff = original_count - len(lines)
        changes.append(f"  Removed legacy mechanism migration section ({diff} lines)")
        original_count = len(lines)

    lines = remove_mechanism_lines(lines)
    if len(lines) < original_count:
        diff = original_count - len(lines)
        changes.append(f"  Removed mechanism-specific lines ({diff} lines)")
        original_count = len(lines)

    lines = clean_mechanism_in_formulas(lines)
    if len(lines) < original_count:
        diff = original_count - len(lines)
        changes.append(f"  Cleaned mechanism refs in formulas ({diff} lines)")
        original_count = len(lines)

    lines = clean_pseudocode_compute(lines)
    # This may not change line count but modifies content

    lines = clean_diagram_headers(lines)
    if len(lines) < original_count:
        diff = original_count - len(lines)
        changes.append(f"  Cleaned diagram/header mechanism refs ({diff} lines)")
        original_count = len(lines)

    lines = clean_output_spec_mechanism_refs(lines)
    if len(lines) < original_count:
        diff = original_count - len(lines)
        changes.append(f"  Cleaned output spec mechanism refs ({diff} lines)")
        original_count = len(lines)

    new_content = "\n".join(lines)

    if new_content != content:
        filepath.write_text(new_content, encoding="utf-8")
        return (len(changes), changes)

    return (0, [])


def main():
    models_dir = Path("/Volumes/SRC-9/SRC Musical Intelligence/Docs/C³/Models")

    if not models_dir.exists():
        print(f"ERROR: {models_dir} not found")
        sys.exit(1)

    # Find all model .md files
    model_files = []
    for subdir in sorted(models_dir.iterdir()):
        if subdir.is_dir():
            for md_file in subdir.glob("*.md"):
                if md_file.name not in SKIP_FILES:
                    model_files.append(md_file)

    print(f"Processing {len(model_files)} model files...")
    print(f"Skipping: {SKIP_FILES}")
    print()

    total_changed = 0
    total_changes = 0

    for filepath in model_files:
        rel_path = filepath.relative_to(models_dir)
        change_count, changes = process_file(filepath)

        if change_count > 0:
            total_changed += 1
            total_changes += change_count
            print(f"✓ {rel_path} ({change_count} change groups)")
            for change in changes:
                print(change)
        else:
            print(f"  {rel_path} (no mechanism refs found)")

    print()
    print(f"Summary: {total_changed}/{len(model_files)} files modified, {total_changes} change groups")


if __name__ == "__main__":
    main()
