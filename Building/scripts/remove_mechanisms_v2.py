#!/usr/bin/env python3
"""Remove REMAINING mechanism references from C³ model documentation files (Pass 2).

After pass 1 (remove_mechanisms.py) removed structural sections (5.2, MECHANISM_NAMES,
mechanism_outputs, etc.), ~1,725 inline references remain. This script handles:

  1. Mechanism labels in diagrams: "Mechanism: BEP.beat_induction"
  2. MECH.sub_section[N:M] arrow lines in Section 4.3 diagrams
  3. MECH.sub_section variable refs in formulas/pseudocode
  4. "at MECH horizons" phrases in prose
  5. Evidence table MI Relevance mechanism prefixes
  6. Mechanism phase description lines
  7. Migration table mechanism entries
  8. Cross-unit mechanism arrows in diagrams
  9. CROSS_UNIT = ("MECH",) code constants
  10. Mechanism section headers (### 7.1 AED Binding)
  11. Mechanism read comments (# AED reads: ...)
  12. Mechanism timeline diagram rows
  13. **Mechanisms**: lines in 00-INDEX.md
  14. Mechanism function parameters in pseudocode
  15. Prose sentences that are purely mechanism explanations
  16. ASCII diagram rows with mechanism horizon labels
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

# All 10 mechanism acronyms (including BEP* variant)
MECHANISMS = {"BEP", "PPC", "TPC", "MEM", "TMH", "AED", "ASA", "C0P", "CPD", "SYN"}
MECH_PATTERN = "|".join(sorted(MECHANISMS))
# Include BEP* variants
MECH_STAR_PATTERN = "|".join(sorted(MECHANISMS)) + "|BEP\\*"

# Files to skip
SKIP_FILES = {"BCH.md"}


def should_delete_line(line: str) -> bool:
    """Return True if this line should be deleted entirely."""
    stripped = line.strip()

    # Empty lines are never deleted by this function
    if not stripped:
        return False

    # --- Pattern 1: "Mechanism: MECH.sub_section" diagram labels ---
    if re.match(r'^.*Mechanism:\s*(' + MECH_STAR_PATTERN + r')[.\s]', line):
        return True

    # --- Pattern 2: MECH.sub_section[N:M] arrow lines in diagrams ---
    # e.g.: BEP.beat_entrainment[0:10] ────┘
    # e.g.: ASA.attention_gating[10:20] ─────┼──►
    # e.g.: MEM.long_term_memory[10:20] ───┘
    if re.search(r'(' + MECH_STAR_PATTERN + r')\.\w+\[\d+:\d+\]\s*[─━═►┘┤┼│]', line):
        return True
    # Also without bracket range:
    # e.g.: BEP*.beat_induction ─────────► RASN.entrainment_state
    if re.search(r'(' + MECH_STAR_PATTERN + r')\.\w+\s+[─━═►┘┤┼│]', line):
        return True

    # --- Pattern 3: Mechanism variable assignments in formulas ---
    # e.g.: mood_fast = AED.arousal_dynamics[0:4].mean()
    # e.g.: trigger_value = CPD.trigger_features[0]
    # e.g.: c0p_mean = C0P.cognitive_state[10]
    if re.search(r'\w+\s*=\s*(' + MECH_STAR_PATTERN + r')\.\w+\[', line):
        return True

    # --- Pattern 4: MotorCoupling = mean(MECH.sub[N:M]) ---
    if re.search(r'=\s*mean\((' + MECH_STAR_PATTERN + r')\.\w+', line):
        return True

    # --- Pattern 5: Mechanism read comments ---
    # e.g.: # AED reads: arousal_dynamics[0:10], expectancy_affect[10:20]
    # e.g.: # CPD reads: trigger_features[0:10], ...
    if re.match(r'\s*#\s*(' + MECH_STAR_PATTERN + r')\s+reads:', line):
        return True
    # Also: # --- BEP* horizons (H6, H11, H16) ---
    if re.match(r'\s*#\s*---\s*(' + MECH_STAR_PATTERN + r')\s+horizons', line):
        return True
    # Also: # --- MEM horizons (H16, H20, H24) ---
    if re.match(r'\s*#\s*---\s*(' + MECH_STAR_PATTERN + r')\b', line):
        return True
    # Also: # BEP* sub-sections (cross-circuit)
    if re.match(r'\s*#\s*(' + MECH_STAR_PATTERN + r')\*?\s+sub-section', line, re.IGNORECASE):
        return True
    # Also: # PPC (pitch deviance)
    if re.match(r'\s*#\s*(' + MECH_STAR_PATTERN + r')\s*\(', line):
        return True

    # --- Pattern 6: CROSS_UNIT = ("MECH",) ---
    if re.search(r'CROSS_UNIT\s*=\s*\("(' + MECH_PATTERN + r')"\)', line):
        return True

    # --- Pattern 7: Mechanism validation/summary rows ---
    # e.g.: | **BEP* Mechanism** | 30D (3 sub-sections, cross-circuit) | Full read |
    if re.search(r'\|\s*\*\*(' + MECH_STAR_PATTERN + r')\*?\s+Mechanism\*\*', line):
        return True

    # --- Pattern 8: Mechanism timeline diagram rows ---
    # Lines in ASCII diagrams that are ONLY mechanism+horizon labels
    # e.g.: │ AED H6 │CPD H7  │        │CPD H12 │        │AED H16 │
    if re.match(r'\s*│', line):
        # Count mechanism matches vs total content
        mech_matches = len(re.findall(r'(' + MECH_PATTERN + r')\s+H\d+', line))
        non_pipe_content = re.sub(r'[│\s]', '', line)
        if mech_matches >= 2 and len(non_pipe_content) < mech_matches * 10:
            return True

    # --- Pattern 9: **Mechanisms**: line in 00-INDEX ---
    if re.match(r'\*\*Mechanisms?\*\*:\s*(' + MECH_PATTERN + r')', line):
        return True

    # --- Pattern 10: Lines that are purely mechanism description sentences ---
    # e.g.: "BEP*.beat_induction provides top-down beat prediction."
    # e.g.: "BEP*.meter_extraction + BEP*.motor_entrainment active."
    # e.g.: "MEM.encoding_state binds rhythmic input with motor output."
    # e.g.: "MEM.familiarity_proxy tracks rhythm recognition."
    if re.match(r'\s*(' + MECH_STAR_PATTERN + r')\*?\.\w+\s+(provides?|binds?|tracks?|integrates?|active|drives?|captures?)', line):
        return True

    # --- Pattern 11: Mechanism section headers ---
    # e.g.: ### 7.1 AED Binding
    # e.g.: ### 7.2 CPD Binding
    if re.match(r'^###\s+\d+\.\d+\s+(' + MECH_PATTERN + r')\s+Binding', line):
        return True

    # --- Pattern 12: Mechanism description blocks (numbered items) ---
    # e.g.: "AED:  Mood state tracking (fast and slow)"
    # e.g.: "CPD:  Therapeutic peak detection"
    # e.g.: "C0P:  Outcome projection"
    if re.match(r'\s*(' + MECH_PATTERN + r'):\s+\w', line):
        # But not in table rows or YAML
        if '|' not in line and ':' == line.strip().split(':')[0][-1:] + ':':
            return True

    # --- Pattern 13: Mechanism sub-section description lines ---
    # e.g.: "MOOD STATE (AED):"
    # e.g.: "THERAPEUTIC PEAKS (CPD):"
    # e.g.: "OUTCOME PROJECTION (C0P):"
    if re.match(r'\s*[A-Z ]+\((' + MECH_PATTERN + r')\):', line):
        return True

    # --- Pattern 14: Mechanism detail lines after description headers ---
    # e.g.: "  AED.arousal_dynamics via H6(200ms) + M0(value)"
    # e.g.: "  CPD.trigger_features via H7(250ms) + M0(value)"
    if re.match(r'\s+(' + MECH_STAR_PATTERN + r')\.\w+\s+via\s+H\d+', line):
        return True

    # --- Pattern 15: Diagram rows referencing mechanism ---
    # e.g.: "║  AED: Affect dynamics tracking ..."
    if re.match(r'\s*[║│]\s*(' + MECH_PATTERN + r'):\s', line):
        return True

    # --- Pattern 16: Mechanism horizon labels in diagrams ---
    # e.g.: "┌── BEP* Horizons (cross-circuit) ─────────────────────┐"
    if re.search(r'[┌└─═]\s*(' + MECH_STAR_PATTERN + r')\*?\s+Horizons', line, re.IGNORECASE):
        return True

    # --- Pattern 17: Window/TMH mapping tables ---
    # e.g.: "Window         Delay       Brain Region      TMH Sub-section   Function"
    if re.search(r'(' + MECH_PATTERN + r')\s+Sub-section', line):
        return True

    # --- Pattern 18: Phase descriptions with mechanism-only content ---
    # e.g.: "BEP*.meter_extraction + BEP*.motor_entrainment active."
    mech_refs = len(re.findall(r'(' + MECH_STAR_PATTERN + r')\*?\.\w+', line))
    if mech_refs >= 2:
        # Line has 2+ mechanism references and little other content
        cleaned = re.sub(r'(' + MECH_STAR_PATTERN + r')\*?\.\w+[\[\]\d:]*', '', line)
        cleaned = re.sub(r'[+×·\s().,]', '', cleaned)
        if len(cleaned) < 15:
            return True

    return False


def clean_inline_mechanism_refs(line: str) -> str:
    """Replace mechanism references within lines that have other useful content."""

    # --- Pattern A: Evidence table MI Relevance ---
    # "**BEP*.beat_induction: auditory-motor entrainment theory**"
    # → "**auditory-motor entrainment theory**"
    line = re.sub(
        r'\*\*(' + MECH_STAR_PATTERN + r')\*?\.\w+:\s*',
        '**',
        line
    )
    # Also: "**TMH horizons**: short/medium/long context"
    # → "**H³ horizons**: short/medium/long context"
    line = re.sub(
        r'\*\*(' + MECH_PATTERN + r')\s+horizons\*\*',
        '**H³ horizons**',
        line
    )
    # Also: "**MEM.encoding_state: description**" already handled above

    # --- Pattern B: "at MECH horizons" in prose ---
    # "at BEP horizons for beat/meter tracking and ASA horizons for attentional gating"
    # → "for beat/meter tracking and attentional gating"
    line = re.sub(
        r'at\s+(' + MECH_PATTERN + r')\s+horizons\s+for\s+',
        'for ',
        line
    )
    # "at three TMH horizons:" → "at three horizons:"
    line = re.sub(
        r'at\s+(\w+\s+)?(' + MECH_PATTERN + r')\s+horizons',
        r'at \1horizons' if r'\1' else 'at horizons',
        line
    )
    # Clean up: "at  horizons" → "at horizons"
    line = re.sub(r'at\s+horizons', 'at these horizons', line)

    # "and ASA horizons for" → "and for"
    line = re.sub(
        r'and\s+(' + MECH_PATTERN + r')\s+horizons\s+for\s+',
        'and for ',
        line
    )

    # --- Pattern C: "aligned with MECH horizons" ---
    # "aligned with PPC+TPC horizons" → "aligned with corresponding H³ horizons"
    line = re.sub(
        r'aligned with\s+(' + MECH_PATTERN + r')[\+/]?(' + MECH_PATTERN + r')?\s+horizons',
        'aligned with corresponding H³ horizons',
        line
    )
    # "aligned with MEM horizons (H16, H20, H24)" → "aligned with H³ horizons (H16, H20, H24)"
    line = re.sub(
        r'aligned with\s+(' + MECH_PATTERN + r')\s+horizons',
        'aligned with H³ horizons',
        line
    )

    # --- Pattern D: "MECH horizons" standalone ---
    # "- **MEM horizons**: H16 (1s)..." → "- **Memory horizons**: H16 (1s)..."
    # "- **BEP* horizons**: H6 (200ms)..." → "- **Beat horizons**: H6 (200ms)..."
    line = re.sub(r'BEP\*?\s+horizons', 'Beat entrainment horizons', line)
    line = re.sub(r'PPC\s+horizons', 'Pitch processing horizons', line)
    line = re.sub(r'TPC\s+horizons', 'Timbre processing horizons', line)
    line = re.sub(r'MEM\s+horizons', 'Memory horizons', line)
    line = re.sub(r'TMH\s+horizons', 'Temporal hierarchy horizons', line)
    line = re.sub(r'AED\s+horizons', 'Affective dynamics horizons', line)
    line = re.sub(r'ASA\s+horizons', 'Auditory scene horizons', line)
    line = re.sub(r'CPD\s+horizons', 'Consummatory dynamics horizons', line)
    line = re.sub(r'C0P\s+horizons', 'Cognitive polarity horizons', line)
    line = re.sub(r'SYN\s+horizons', 'Synthesis horizons', line)

    # --- Pattern E: Migration table MI column ---
    # "R³.spectral_flux[10] × BEP*.beat_induction" → "R³.spectral_flux[10]"
    # "R³.x_l4l5[33:41] × BEP*.motor_entrainment" → "R³.x_l4l5[33:41]"
    line = re.sub(
        r'\s*[×+]\s*(' + MECH_STAR_PATTERN + r')\*?\.\w+(\[\d+:\d+\])?',
        '',
        line
    )
    # Also handle "R³.spectral_flux[10] + BEP.beat_entrainment" pattern
    line = re.sub(
        r'\s*\+\s*(' + MECH_STAR_PATTERN + r')\*?\.\w+(\[\d+:\d+\])?',
        '',
        line
    )

    # --- Pattern F: "for MEM encoding" → "for memory encoding" ---
    line = re.sub(r'for\s+MEM\s+', 'for memory ', line)
    line = re.sub(r'for\s+BEP\*?\s+', 'for beat ', line)

    # --- Pattern G: Inline "MECH.sub_section" in prose (not in formulas) ---
    # "TMH.context_depth ↔ HMCE.gradient" → "context_depth ↔ HMCE.gradient"
    # Only replace when MECH. is followed by a known sub-section pattern
    line = re.sub(
        r'(' + MECH_STAR_PATTERN + r')\*?\.([\w]+)',
        lambda m: m.group(2) if m.group(1).rstrip('*') in MECHANISMS else m.group(0),
        line
    )

    # --- Pattern H: "via the BEP* cross-circuit read" → "via cross-circuit relay" ---
    line = re.sub(
        r'via\s+(the\s+)?(' + MECH_STAR_PATTERN + r')\*?\s+cross-circuit\s+read',
        'via cross-circuit relay',
        line
    )
    # "(also reads BEP*)" → "" or "(cross-circuit read)"
    line = re.sub(
        r'\(also\s+reads?\s+(' + MECH_STAR_PATTERN + r')\*?\)',
        '(cross-circuit read)',
        line
    )

    # --- Pattern I: "via BEP*" or "via BEP" standalone ---
    line = re.sub(
        r'\(via\s+(' + MECH_STAR_PATTERN + r')\*?\)',
        '(via H³ direct)',
        line
    )

    # --- Pattern J: Function parameters ---
    # "def compute_tar(R3, H3, AED, CPD, C0P):" → "def compute_tar(R3, H3):"
    if 'def ' in line and '(' in line:
        # Remove mechanism parameters from function signatures
        for mech in MECHANISMS:
            line = re.sub(r',\s*' + mech + r'\b', '', line)

    # --- Pattern K: Function calls with mechanism args ---
    # "compute_mood(AED)" → "compute_mood()"
    # "compute_breakthrough(CPD)" → "compute_breakthrough()"
    # "extract_c0p(C0P)" → "extract_c0p()"
    for mech in MECHANISMS:
        line = re.sub(r'\(' + mech + r'\)', '()', line)

    # --- Pattern L: "same mechanisms" → "same" ---
    line = re.sub(r'Same mechanisms', 'Same', line, flags=re.IGNORECASE)

    # --- Pattern M: Phase labels with mechanism references ---
    # "Phase 1: BEAT DETECTION (continuous, <200ms, BEP* H6)"
    # → "Phase 1: BEAT DETECTION (continuous, <200ms, H6)"
    line = re.sub(
        r',\s*(' + MECH_STAR_PATTERN + r')\*?\s+(H\d+)',
        r', \2',
        line
    )
    # "Phase 3: ... (1-5s, MEM H16/H20)" → "Phase 3: ... (1-5s, H16/H20)"
    line = re.sub(
        r',\s*(' + MECH_PATTERN + r')\s+(H\d+)',
        r', \2',
        line
    )

    # --- Pattern N: "H³ → AED+CPD+C0P (21 tuples)" → "H³ (21 tuples)" ---
    line = re.sub(
        r'H³\s*→\s*(' + MECH_PATTERN + r')[\+/](' + MECH_PATTERN + r')[\+/]?(' + MECH_PATTERN + r')?\s*',
        'H³ ',
        line
    )
    line = re.sub(
        r'H³\s*→\s*(' + MECH_PATTERN + r')[\+/]?(' + MECH_PATTERN + r')?\s*',
        'H³ ',
        line
    )

    # --- Pattern O: "HC⁰ AED+CPD+C0P" → "HC⁰" ---
    line = re.sub(
        r'HC⁰\s+(' + MECH_PATTERN + r')[\+/](' + MECH_PATTERN + r')[\+/]?(' + MECH_PATTERN + r')?\s*',
        'HC⁰ ',
        line
    )

    # --- Pattern P: "dual-mechanism demand" → "dual-scale demand" ---
    line = re.sub(r'dual-mechanism\s+demand', 'dual-scale demand', line)
    line = re.sub(r'shared temporal mechanisms', 'shared temporal processing', line)

    # --- Pattern Q: Mechanism in Migration table "MECH 3 sub-sections" ---
    line = re.sub(
        r'(' + MECH_PATTERN + r')\s+\d+\s+sub-sections?\s*\([^)]*\)',
        'H³ direct features',
        line
    )
    line = re.sub(
        r'(' + MECH_PATTERN + r')\s+\d+\s+sub-sections',
        'H³ direct features',
        line
    )

    # --- Pattern R: "Harmonic recognition for MEM" → "Harmonic recognition" ---
    line = re.sub(
        r'for\s+(' + MECH_PATTERN + r')\s*$',
        '',
        line
    )

    # --- Pattern S: "TMH short/medium/long" → "short/medium/long" ---
    line = re.sub(r"TMH's", "the temporal hierarchy's", line)
    line = re.sub(r'TMH\.\s*', '', line)

    return line


def clean_section_mechanism_binding(lines: list[str]) -> list[str]:
    """Remove mechanism binding sections (### N.M MECH Binding)."""
    result = []
    in_section = False
    for line in lines:
        # Start of a mechanism binding section
        if re.match(r'^###\s+\d+\.\d+\s+(' + MECH_PATTERN + r')\s+Binding', line):
            in_section = True
            continue
        if in_section:
            # End when we hit next heading of same or higher level
            if re.match(r'^(###\s+\d+\.\d+|##\s|---)', line):
                in_section = False
                result.append(line)
            continue
        result.append(line)
    return result


def clean_mechanism_description_blocks(lines: list[str]) -> list[str]:
    """Remove mechanism description blocks (MOOD STATE (AED): ... multi-line)."""
    result = []
    in_block = False
    for line in lines:
        stripped = line.strip()
        # Start of a mechanism description block
        if re.match(r'[A-Z ]+\((' + MECH_PATTERN + r')\):', stripped):
            in_block = True
            continue
        if in_block:
            # Mechanism detail lines start with spaces and reference mechanism
            if re.match(r'\s+(' + MECH_STAR_PATTERN + r')\*?\.\w+', line):
                continue
            # Empty line or non-mechanism content ends the block
            if stripped == '' or not stripped.startswith((' ', '\t')):
                in_block = False
                result.append(line)
            else:
                # Indented but no mechanism ref — could be continuation
                if re.search(r'(' + MECH_STAR_PATTERN + r')', line):
                    continue
                else:
                    in_block = False
                    result.append(line)
            continue
        result.append(line)
    return result


def process_file(filepath: Path) -> tuple[int, int]:
    """Process a single model .md file.

    Returns:
        (lines_deleted, lines_modified)
    """
    content = filepath.read_text(encoding="utf-8")
    lines = content.split("\n")
    original_count = len(lines)

    # Phase 1: Section-level removals
    lines = clean_section_mechanism_binding(lines)
    lines = clean_mechanism_description_blocks(lines)

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
        new_line = clean_inline_mechanism_refs(line)
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

    # Find all model .md files
    model_files = []
    for subdir in sorted(models_dir.iterdir()):
        if subdir.is_dir():
            for md_file in subdir.glob("*.md"):
                if md_file.name not in SKIP_FILES:
                    model_files.append(md_file)
    # Also process 00-INDEX.md directly
    index_file = models_dir / "00-INDEX.md"
    if index_file.exists():
        model_files.append(index_file)

    print(f"Processing {len(model_files)} files (pass 2)...")
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
            print(f"✓ {rel_path}: {deleted} lines deleted, {modified} lines modified")
        else:
            print(f"  {rel_path}: clean")

    print()
    print(f"Summary: {files_changed} files changed, {total_deleted} lines deleted, {total_modified} lines modified")


if __name__ == "__main__":
    main()
