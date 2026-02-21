#!/usr/bin/env python3
"""Final 19 targeted mechanism reference fixes."""
from pathlib import Path

BASE = Path("/Volumes/SRC-9/SRC Musical Intelligence/Docs/C³/Models")

fixes = [
    ("SPU-β1-STAI/STAI.md", "weighted product with PPC", "weighted product with pitch processing"),
    ("ARU-α2-AAC/AAC.md", "controlling for AED", "controlling for affect dynamics"),
    ("STU-β2-TPIO/TPIO.md", "timbre-processing + TMH → TPIO", "TPIO"),
    ("ARU-β2-CLAM/CLAM.md", "C0P [120:128]", "Cognitive-projection [120:128]"),
    ("IMU-β9-CMAPCC/CMAPCC.md", "MEM (30D, primary) + beat-entrainment (30D, cross-circuit)", "H³ direct (memory + beat-entrainment)"),
    ("STU-γ5-MPFS/MPFS.md", "BEP (H6/H11/H16) + TMH (H8/H14/H20)", "H³ direct (H6/H11/H16 + H8/H14/H20)"),
    ("IMU-β1-RASN/RASN.md", "Without BEP, RASN", "Without beat-entrainment H³, RASN"),
    ("IMU-γ1-DMMS/DMMS.md", "AED (indirect)", "affect dynamics (indirect)"),
    ("STU-γ1-TMRM/TMRM.md", "Within BEP H11", "Within H11"),
    ("IMU-α1-MEAMN/MEAMN.md", "from R³ + AED]", "from R³ + affect dynamics]"),
    ("IMU-γ2-CSSL/CSSL.md", "R³ and MEM", "R³ and memory H³"),
    ("PCU-α3-ICEM/ICEM.md", "PPC (pitch context)", "pitch processing (pitch context)"),
    ("SPU-γ3-SDED/SDED.md", "PPC-modulated", "pitch-modulated"),
    ("SPU-γ3-SDED/SDED.md", "+ PPC |", "+ pitch processing |"),
    ("STU-β4-ETAM/ETAM.md", "BEP-trend based", "beat-trend based"),
    ("STU-β4-ETAM/ETAM.md", "BEP (30D, primary) + TMH (30D, secondary)", "H³ direct (beat + temporal)"),
    ("STU-β4-ETAM/ETAM.md", "+ TMH |", "+ temporal-context |"),
    ("PCU-β3-UDP/UDP.md", "HC⁰ affect/CPD", "HC⁰ affect/peak"),
    ("ASU-α2-IACM/IACM.md", "+ BEP |", "+ beat-entrainment H³ |"),
]

count = 0
for rel_path, old, new in fixes:
    fp = BASE / rel_path
    if not fp.exists():
        print(f"  SKIP {rel_path} (not found)")
        continue
    content = fp.read_text(encoding="utf-8")
    if old in content:
        content = content.replace(old, new, 1)
        fp.write_text(content, encoding="utf-8")
        count += 1
        print(f"✓ {rel_path}: '{old[:40]}...' → '{new[:40]}...'")
    else:
        print(f"  {rel_path}: pattern not found: '{old[:50]}'")

print(f"\nFixed {count}/{len(fixes)} replacements")
