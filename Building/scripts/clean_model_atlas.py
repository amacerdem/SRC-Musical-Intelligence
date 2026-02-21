#!/usr/bin/env python3
"""Clean mechanism references from MODEL-ATLAS.md.

Removes Mechs column from unit tables, removes mechanism-specific sections,
updates summary text.
"""
from pathlib import Path
import re

MECHANISMS = {"BEP", "PPC", "TPC", "MEM", "TMH", "AED", "ASA", "C0P", "CPD", "SYN"}
MECH_PATTERN = "|".join(sorted(MECHANISMS))

fp = Path("/Volumes/SRC-9/SRC Musical Intelligence/Building/Ontology/C³/MODEL-ATLAS.md")
content = fp.read_text(encoding="utf-8")
lines = content.split("\n")

result = []
in_mech_section = False
skip_section_until_heading = False

for i, line in enumerate(lines):
    stripped = line.strip()

    # --- Remove Mechs column from Reading Key ---
    if '| **Mechs**' in line:
        continue

    # --- Remove Mechs column from table headers ---
    # "| Model ID | Full Name | D | Mechs | H3 | E/M/P/F | Cross-unit | State |"
    if '| Model ID |' in line and '| Mechs |' in line:
        line = line.replace(' Mechs |', '')
        # Fix the alignment - remove extra pipe
        line = re.sub(r'\| D \| ', '| D | ', line)
        result.append(line)
        continue

    # --- Remove Mechs column from separator rows ---
    # "|----------|-----------|---|-------|-----|---------|------------|-------|"
    if re.match(r'\|[-]+\|[-]+\|[-]+\|[-]+\|[-]+\|[-]+\|[-]+\|[-]+\|', stripped):
        # This is a table separator with 8 columns, reduce to 7
        parts = stripped.split('|')
        # Remove the 5th column (Mechs is column 4, 0-indexed)
        if len(parts) >= 9:
            del parts[4]
        result.append('|'.join(parts))
        continue

    # --- Remove Mechs column from data rows ---
    # "| SPU-α1-BCH | Brainstem Consonance Hierarchy | 12 | Relay (none) | 26 | E4+M2+P3+F3 | ..."
    if re.match(r'\|\s*(SPU|ARU|ASU|IMU|MPU|NDU|PCU|RPU|STU)-', stripped):
        parts = line.split('|')
        if len(parts) >= 9:
            del parts[4]  # Remove Mechs column
        line = '|'.join(parts)
        result.append(line)
        continue

    # --- Remove/rewrite summary lines with mechanism references ---
    # "**SPU summary**: ... PPC dominant; TPC at higher tiers..."
    if stripped.startswith('**') and 'summary**:' in stripped:
        # Remove mechanism mentions from summary lines
        line = re.sub(r'BEP\s*\+\s*ASA', 'beat + auditory-scene', line)
        line = re.sub(r'BEP\s*\+\s*TMH', 'beat + temporal', line)
        line = re.sub(r'PPC\s*\+\s*ASA', 'pitch + auditory-scene', line)
        line = re.sub(r'PPC\s*\+\s*TPC\s*\+\s*MEM', 'pitch + timbre + memory', line)
        line = re.sub(r'AED\s*\+\s*CPD\s*\+\s*C0P', 'affect + peak + cognitive', line)
        for mech in MECHANISMS:
            line = re.sub(r'\b' + mech + r'\b', {
                'BEP': 'beat-entrainment', 'PPC': 'pitch-processing',
                'TPC': 'timbre-processing', 'MEM': 'memory', 'TMH': 'temporal-context',
                'AED': 'affect', 'ASA': 'auditory-scene', 'C0P': 'cognitive-projection',
                'CPD': 'peak-detection', 'SYN': 'synthesis'
            }.get(mech, mech), line)
        result.append(line)
        continue

    # --- Remove sections 2, 3, 4 (mechanism-specific summaries) ---
    # "### 2. Mechanism vs Relay Count"
    if stripped.startswith('### 2. Mechanism'):
        skip_section_until_heading = True
        continue
    # "### 3. Mechanism Frequency"
    if stripped.startswith('### 3. Mechanism'):
        skip_section_until_heading = True
        continue
    # "### 4. Unit-Mechanism Binding"
    if stripped.startswith('### 4. Unit-Mechanism'):
        skip_section_until_heading = True
        continue
    # "### 5. Perfect Mechanism Uniformity"
    # (this is in Architectural Findings)

    if skip_section_until_heading:
        if re.match(r'^### \d+\.', line) and not any(x in line for x in ['Mechanism']):
            skip_section_until_heading = False
            result.append(line)
        continue

    # --- Clean architectural findings ---
    # "### 1. Strict Unit-Mechanism Binding" section
    if '### 1. Strict Unit-Mechanism Binding' in line:
        skip_section_until_heading = True
        continue
    # "### 3. IMU as the Cross-Circuit Bridge"
    if 'reads cross-circuit mechanisms' in line:
        line = line.replace('reads cross-circuit mechanisms', 'reads cross-circuit features')
        for mech in MECHANISMS:
            line = re.sub(r'\b' + mech + r'\b', '', line)
        line = re.sub(r'\s+', ' ', line)
        result.append(line)
        continue
    # "### 5. Perfect Mechanism Uniformity in 3 Units"
    if 'Perfect Mechanism Uniformity' in line:
        line = line.replace('Perfect Mechanism Uniformity', 'Perfect Relay Uniformity')
        result.append(line)
        continue
    if 'zero mechanism variation' in line:
        line = line.replace('zero mechanism variation', 'zero variation')
        for mech in MECHANISMS:
            line = re.sub(r'\b' + mech + r'\+' + mech + r'\b', 'consistent', line)
        # Clean remaining mechanism references
        line = re.sub(r'\(BEP\+ASA\)', '', line)
        line = re.sub(r'\(BEP\+TMH\)', '', line)
        line = re.sub(r'\(PPC\+ASA\)', '', line)
        result.append(line)
        continue

    # --- Extreme Models table ---
    if 'Most mechanisms' in line:
        continue
    if 'No mechanisms' in line:
        line = line.replace('No mechanisms', 'Only Relay')
        result.append(line)
        continue

    # --- Tier patterns table ---
    if 'Mechanism Pattern' in line:
        line = line.replace('Mechanism Pattern', 'Notes')
        result.append(line)
        continue
    if 'Full mechanism signatures' in line:
        line = line.replace('Full mechanism signatures', 'Full depth hierarchy')
        result.append(line)
        continue
    if 'May drop M layer' in line:
        result.append(line)
        continue

    # --- Reading Key: remove Mechs row, update E/M/P/F ---
    if '| **E/M/P/F**' in line:
        line = line.replace('Mechanism', 'Mathematical')
        result.append(line)
        continue

    # --- General mechanism name cleanup ---
    if any(re.search(r'\b' + m + r'\b', line) for m in MECHANISMS):
        # Only in non-table, non-code contexts
        if '```' not in line and not stripped.startswith('|'):
            for mech, desc in [
                ('BEP', 'beat-entrainment'), ('PPC', 'pitch-processing'),
                ('TPC', 'timbre-processing'), ('MEM', 'memory'),
                ('TMH', 'temporal-context'), ('AED', 'affect'),
                ('ASA', 'auditory-scene'), ('C0P', 'cognitive-projection'),
                ('CPD', 'peak-detection'), ('SYN', 'synthesis')
            ]:
                line = re.sub(r'\b' + mech + r'\b', desc, line)

    result.append(line)

# Clean consecutive empty lines
final = []
empty_count = 0
for line in result:
    if line.strip() == '':
        empty_count += 1
        if empty_count <= 2:
            final.append(line)
    else:
        empty_count = 0
        final.append(line)

new_content = "\n".join(final)
fp.write_text(new_content, encoding="utf-8")

# Count remaining mechanism refs
remaining = sum(1 for line in final if re.search(r'\b(' + MECH_PATTERN + r')\b', line))
print(f"MODEL-ATLAS.md cleaned. {remaining} mechanism references remaining.")
