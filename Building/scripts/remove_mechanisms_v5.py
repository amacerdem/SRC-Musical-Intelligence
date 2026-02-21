#!/usr/bin/env python3
"""Remove FINAL mechanism references from C³ model docs (Pass 5).

~145 remaining references after passes 1-4. This pass handles:
  1. CROSS_CIRCUIT/CROSS_UNIT = ("MECH",) code constants
  2. Cross-circuit diagram arrows with mechanism names
  3. Formula abbreviations using mechanism as variable names
  4. Dimension descriptions referencing mechanisms
  5. Evidence table mechanism labels in MI Relevance column
  6. Cross-unit pathway arrows with mechanism targets (ARU.AED)
  7. Prose sentences with mechanism names
  8. Migration table HC⁰.MECH entries (clean mechanism name, keep HC⁰ ref)
  9. CROSS-CIRCUIT section headers
  10. Mechanism validation section headers
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MECHANISMS = {"BEP", "PPC", "TPC", "MEM", "TMH", "AED", "ASA", "C0P", "CPD", "SYN"}
MECH_PATTERN = "|".join(sorted(MECHANISMS))
SKIP_FILES = {"BCH.md"}


def should_delete_line(line: str) -> bool:
    """Lines that should be removed entirely."""
    stripped = line.strip()
    if not stripped:
        return False

    # Cross-circuit diagram arrows
    # "│ CROSS-CIRCUIT (AED* read from mesolimbic): │"
    if re.search(r'CROSS-CIRCUIT\s*\((' + MECH_PATTERN + r')\*?\s', line):
        return True
    # "│ ARU mesolimbic ──────────► CDEM.AED* (arousal + expectancy signals) │"
    if re.search(r'──+►.*\.(' + MECH_PATTERN + r')\*?\s', line):
        return True
    # "│ TPC* mechanism (30D) ────► TPIO"
    if re.search(r'(' + MECH_PATTERN + r')\*?\s+mechanism\s*\(\d+D\)', line):
        return True
    # "│ CROSS-CIRCUIT (BEP* from STU sensorimotor circuit): │"
    if re.search(r'CROSS-CIRCUIT\s*\((' + MECH_PATTERN + r')\*?', line):
        return True

    # Cross-unit pathway arrows with mechanism targets
    # "│ AMSC.motor_preparation ──► ARU.AED (motor coupling → arousal) │"
    if re.search(r'──+►\s*\w+\.(' + MECH_PATTERN + r')\s', line):
        return True
    # "│ HGSIC.groove_index ──► ARU.AED (groove → arousal modulation) │"
    if re.search(r'──+►\s*(' + MECH_PATTERN + r')\.', line):
        return True

    # "SYN ◄──────── PNH, PMIM, MSPBA, TPRD, CMAPCC"
    if re.match(r'\s*│?\s*(' + MECH_PATTERN + r')\s*◄──', line):
        return True
    # "MEM ◄──────── MEAMN, MMP, HCMC, RASN, RIRI, VRIAP, DMMS, CSSL, CDEM"
    if re.match(r'\s*│?\s*(' + MECH_PATTERN + r')\s*◄', line):
        return True

    # Mechanism description block lines
    # "AED: Mood state tracking (fast and slow)"
    if re.match(r'\s*(' + MECH_PATTERN + r'):\s+[A-Z]\w+\s', stripped):
        return True

    # Mechanism validation section headers
    # "## 5. ASA Mechanism Validation"
    if re.search(r'(' + MECH_PATTERN + r')\s+Mechanism\s+Validation', line):
        return True

    # "│ SYN Horizons: MEM Horizons: │"
    if re.search(r'(' + MECH_PATTERN + r')\s+Horizons:', line):
        return True

    return False


def clean_inline_refs(line: str) -> str:
    """Clean remaining inline mechanism references."""

    if not re.search(r'\b(' + MECH_PATTERN + r')\b', line):
        return line

    # --- CROSS_CIRCUIT = ("MECH",) → CROSS_UNIT_READS = () ---
    line = re.sub(
        r'CROSS_CIRCUIT\s*=\s*\("(' + MECH_PATTERN + r')",?\)',
        'CROSS_UNIT_READS = ()  # TODO: populate from Nucleus contract',
        line
    )
    # CROSS_UNIT = ("MECH",) → CROSS_UNIT_READS = ()
    line = re.sub(
        r'CROSS_UNIT\s*=\s*\("(' + MECH_PATTERN + r')",?\)',
        'CROSS_UNIT_READS = ()  # TODO: populate from Nucleus contract',
        line
    )
    # INTRA_CIRCUIT = ("MECH",)
    line = re.sub(
        r'INTRA_CIRCUIT\s*=\s*\("(' + MECH_PATTERN + r')",?\)',
        'UPSTREAM_READS = ()  # TODO: populate from Nucleus contract',
        line
    )

    # --- Evidence table mechanism labels ---
    # "**BEP**: neural oscillation mechanism" → "**beat-entrainment H³**: neural oscillation mechanism"
    # "**BEP→social**: beat entrainment enables..." → "**beat→social**: ..."
    line = re.sub(r'\*\*BEP→', '**beat→', line)
    line = re.sub(r'\*\*BEP\*?\*?\*?:', '**Beat-entrainment H³**:', line)
    line = re.sub(r'\*\*TMH\*?\*?\*?:', '**Temporal-context H³**:', line)
    line = re.sub(r'\*\*AED\*?\*?:', '**Affective-dynamics**:', line)
    line = re.sub(r'\*\*MEM\*?\*?:', '**Memory-encoding**:', line)
    line = re.sub(r'\*\*PPC\*?\*?:', '**Pitch-processing**:', line)
    line = re.sub(r'\*\*TPC\*?\*?:', '**Timbre-processing**:', line)

    # "**memory-encoding x BEP*: ..." → "**memory-encoding x beat-entrainment: ..."
    line = re.sub(r'BEP\*', 'beat-entrainment', line)
    line = re.sub(r'TPC\*', 'timbre-processing', line)
    line = re.sub(r'PPC\*', 'pitch-processing', line)
    line = re.sub(r'AED\*', 'affective-dynamics', line)

    # --- Migration table HC⁰ entries ---
    # "HC⁰.AED" → "HC⁰ affect"
    line = re.sub(r'HC⁰\.AED', 'HC⁰ affect', line)
    line = re.sub(r'HC⁰\.CPD', 'HC⁰ peak', line)
    line = re.sub(r'HC⁰\.ASA', 'HC⁰ scene', line)
    line = re.sub(r'HC⁰\.C0P', 'HC⁰ cognitive', line)
    line = re.sub(r'HC⁰\.BEP', 'HC⁰ beat', line)
    line = re.sub(r'HC⁰\.PPC', 'HC⁰ pitch', line)
    line = re.sub(r'HC⁰\.TPC', 'HC⁰ timbre', line)
    line = re.sub(r'HC⁰\.MEM', 'HC⁰ memory', line)
    line = re.sub(r'HC⁰\.TMH', 'HC⁰ temporal', line)
    line = re.sub(r'HC⁰\.SYN', 'HC⁰ synthesis', line)
    # Also: HC⁰.AED/CPD → HC⁰ affect/peak
    line = re.sub(r'HC⁰\s+(' + MECH_PATTERN + r')/(' + MECH_PATTERN + r')', 'HC⁰ legacy', line)
    # Also: HC0.AED (without ⁰)
    line = re.sub(r'HC0\.AED', 'HC⁰ affect', line)

    # --- Formula abbreviations ---
    # "f01 = σ(w · flux · onset · BEP)" → "f01 = σ(w · flux · onset · beat_h3)"
    line = re.sub(r'·\s*BEP\b\)?', '· beat_h3)', line)
    line = re.sub(r'·\s*TMH\b', '· temporal_h3', line)
    line = re.sub(r'·\s*MEM\b', '· memory_h3', line)
    line = re.sub(r'·\s*SYN\b', '· synth_h3', line)
    line = re.sub(r'·\s*AED\b', '· affect_h3', line)

    # --- Function calls with mechanism args ---
    # "compute_warmth(AED, R3)" → "compute_warmth(h3, R3)"
    # "compute_response_strength(AED, R3)" → "compute_response_strength(h3, R3)"
    for mech in MECHANISMS:
        line = re.sub(r'\(' + mech + r',\s*R3\)', '(h3, R3)', line)
        line = re.sub(r'\(' + mech + r',\s*(' + MECH_PATTERN + r'),\s*R3\)', '(h3, R3)', line)

    # --- Dimension descriptions ---
    # "TMH SMA planning activation level" → "temporal-context SMA planning activation level"
    line = re.sub(r'\bTMH\s+SMA\b', 'temporal-context SMA', line)
    # "BEP M1 execution output" → "beat-entrainment M1 execution"
    line = re.sub(r'\bBEP\s+M1\b', 'beat-entrainment M1', line)
    # "PPC/memory-encoding" → "pitch/memory-encoding"
    line = re.sub(r'\bPPC/', 'pitch-processing/', line)
    # "PPC/timbre-processing" → "pitch/timbre-processing"
    line = re.sub(r'\bTPC\b', 'timbre-processing', line)

    # --- Information flow header ---
    # "(EAR → BRAIN → TPC* + TMH → TPIO)" already partially cleaned
    # "(EAR -> BRAIN -> MEM -> DMMS)" → "(EAR → BRAIN → DMMS)"
    line = re.sub(r'→\s*(' + MECH_PATTERN + r')\s*→', '→', line)
    line = re.sub(r'->\s*(' + MECH_PATTERN + r')\s*->', '->', line)
    # "TPC* + TMH → TPIO" → "→ TPIO"
    line = re.sub(r'→\s*(' + MECH_PATTERN + r')\*?\s*\+\s*(' + MECH_PATTERN + r')\s*→', '→', line)

    # --- Pathway validation lines ---
    # "ASA → auditory salience → SCR" → "auditory scene → salience → SCR"
    line = re.sub(r'\bASA\s*→\s*auditory', 'auditory scene → auditory', line)
    # "CPD → AAC" → "peak-detection → AAC"
    line = re.sub(r'\bCPD\s*→\s*AAC', 'peak-detection → AAC', line)

    # --- Cross-unit references ---
    # "► ARU.AED" → "► ARU reward"
    line = re.sub(r'ARU\.AED', 'ARU reward', line)
    # "IMU.MEM" → "IMU memory"
    line = re.sub(r'IMU\.MEM', 'IMU memory', line)

    # --- Prose patterns ---
    # "SYN-derived" → "synthesis-derived"
    line = re.sub(r'\bSYN-derived', 'synthesis-derived', line)
    # "SYN × memory-encoding" → "synthesis × memory-encoding"
    line = re.sub(r'\bSYN\s*×', 'synthesis ×', line)
    # "within BEP H11 (500 ms)" → "within H11 (500 ms)"
    line = re.sub(r'within\s+(' + MECH_PATTERN + r')\s+(H\d+)', r'within \2', line)
    # "BEP × temporal-context interaction" → "beat × temporal-context interaction"
    line = re.sub(r'BEP\s*×\s*temporal', 'beat × temporal', line)
    # "BEP, training_range" → "beat_h3, training_range"
    line = re.sub(r'f\(BEP,', 'f(beat_h3,', line)
    # "spanning BEP (H6)" → "spanning H6"
    line = re.sub(r'spanning\s+(' + MECH_PATTERN + r')\s*\((H\d+)\)', r'spanning \2', line)
    # "and TMH (H8, H11, H14)" → "and H8, H11, H14"
    line = re.sub(r'and\s+(' + MECH_PATTERN + r')\s*\(', 'and (', line)
    # "uses BEP* H6/H11" → "uses H6/H11"
    line = re.sub(r'uses\s+(' + MECH_PATTERN + r')\*?\s+(H\d+)', r'uses \2', line)
    # "uses MEM H16" → "uses H16"
    line = re.sub(r'uses\s+(' + MECH_PATTERN + r')\s+(H\d+)', r'uses \2', line)
    # "Acoustic input → TPC" → "Acoustic input → timbre processing"
    line = re.sub(r'→\s*TPC\b', '→ timbre processing', line)
    # "Memory retrieval → TMH" → "Memory retrieval → temporal context"
    line = re.sub(r'→\s*TMH\b', '→ temporal context', line)
    # "Intensity × beat-level BEP" → "Intensity × beat-level H³"
    line = re.sub(r'×\s*beat-level\s+BEP', '× beat-level H³', line)
    # "TMH-driven" → "temporal-context-driven"
    line = re.sub(r'TMH-driven', 'temporal-context-driven', line)

    # --- Mechanism in code doc audit tables ---
    # '`("BEP",)`' → '`()  # TODO`'
    line = re.sub(r'`\("(' + MECH_PATTERN + r')",?\)`', '`() # TODO`', line)

    # --- CROSS_UNIT_READS = () but doc specifies TPC* cross-circuit read ---
    line = re.sub(r'(' + MECH_PATTERN + r')\*?\s+cross-circuit\s+read', 'cross-circuit relay read', line)

    # --- Remaining "uses AED" / "uses only AED" / "AED-only" ---
    line = re.sub(r'uses\s+only\s+\*\*(' + MECH_PATTERN + r')\*\*', 'uses only **H³ direct**', line)
    line = re.sub(r'\b(' + MECH_PATTERN + r')-only\b', 'H³-only', line)

    # --- Mechanism validation in section 14 tables ---
    # "| **Mechanisms** | PPC (primary) + TPC (secondary) | Dual mechanism |"
    line = re.sub(r'\*\*Mechanisms?\*\*\s*\|\s*(' + MECH_PATTERN + r').*\|', '**H³ Direct** | Relay + H³ |', line)

    # "representations (TPC*)" → "representations"
    line = re.sub(r'\s*\((' + MECH_PATTERN + r')\*?\)', '', line)

    # "no CPD" → "no peak-detection mechanism"
    line = re.sub(r'no\s+(' + MECH_PATTERN + r')\b', 'no peak-detection mechanism', line)
    # Generalize: clean remaining "No ASA" etc
    line = re.sub(r'No\s+(' + MECH_PATTERN + r')\b', 'No separate mechanism', line)

    # --- "MEM IC computation" → "memory IC computation" ---
    line = re.sub(r'\bMEM\s+IC\b', 'memory IC', line)
    # "MEM-only" → "memory-only"
    line = re.sub(r'\bMEM-only\b', 'memory-only', line)
    # "MEM (intra-circuit" → "memory (intra-circuit"
    line = re.sub(r'\bMEM\s+\(intra', 'memory (intra', line)

    # --- "H³ direct replaced by CPD" ---
    line = re.sub(r'replaced by\s+(' + MECH_PATTERN + r')', 'replaced by H³ direct', line)

    # --- "R³→PPC* brainstem pathway" → "R³ brainstem pathway" ---
    line = re.sub(r'R³→(' + MECH_PATTERN + r')\*?', 'R³ →', line)

    # --- "ASA 350ms window" → "Auditory scene 350ms window" ---
    line = re.sub(r'\bASA\s+(\d+ms)', r'Auditory scene \1', line)
    # "ASA→AAC effect → auditory-scene redundant"
    line = re.sub(r'\bASA→', 'auditory-scene→', line)

    # --- "AED H6+H16 average" → "H6+H16 average" ---
    line = re.sub(r'\bAED\s+(H\d+)', r'\1', line)
    line = re.sub(r'\bAED\s+(D\d+)', r'\1', line)

    # --- Migration table "No C0P" etc. ---
    line = re.sub(r'No\s+C0P', 'No separate mechanism', line)
    line = re.sub(r'no\s+C0P', 'no separate mechanism', line)
    line = re.sub(r'no\s+ASA', 'no separate mechanism', line)

    # "### 7.3 Control Law (No C0P..." → "### 7.3 Control Law (H³ direct..."
    line = re.sub(r'\(No\s+separate mechanism\s*—', '(H³ direct —', line)

    # --- "BEP mechanism (cross-circuit read from sensorimotor)" ---
    line = re.sub(
        r'(' + MECH_PATTERN + r')\*?\s+mechanism\s*\(cross-circuit',
        'Beat-entrainment relay (cross-circuit',
        line
    )

    # --- "H³ direct (no separate mechanism)" → "H³ direct" when in bold context ---
    line = re.sub(r'two mesolimbic mechanisms: \*\*H³ direct\*\*', 'H³ direct features', line)

    # --- "AED" standalone remaining → "affect" ---
    # This is aggressive but necessary for the last ~20 refs
    # Only in specific contexts
    line = re.sub(r'weighted by AED\b', 'weighted by affect dynamics', line)
    line = re.sub(r'\bAED\s+affect\b', 'affect dynamics', line)
    line = re.sub(r'compute_\w+\(AED\)', 'compute_affect(h3)', line)
    line = re.sub(r'x\s+AED\b', 'x affect_dynamics', line)

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
        new_line = clean_inline_refs(line)
        if new_line != line:
            modified += 1
        cleaned.append(new_line)
    lines = cleaned

    # Phase 3: Clean consecutive empty lines
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

    new_content = "\n".join(final)
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

    print(f"Processing {len(model_files)} files (pass 5 — final cleanup)...")
    print()

    total_del = 0
    total_mod = 0
    files_changed = 0

    for filepath in sorted(model_files):
        rel_path = filepath.relative_to(models_dir)
        d, m = process_file(filepath)
        if d > 0 or m > 0:
            files_changed += 1
            total_del += d
            total_mod += m
            print(f"✓ {rel_path}: {d} del, {m} mod")

    print()
    print(f"Summary: {files_changed} files, {total_del} del, {total_mod} mod")


if __name__ == "__main__":
    main()
