#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════
#  setup_test_audio.sh — Download & generate Test-Audio on RunPod
#
#  Creates:
#   1. Test-Audio/*.wav — Main reference tracks via yt-dlp
#   2. Test-Audio/micro_beliefs/ — Synthesized stimuli via generators
#
#  Usage:
#    cd /workspace/MI
#    bash Validation/setup_test_audio.sh
# ═══════════════════════════════════════════════════════════════════
set -euo pipefail

MI_ROOT="${MI_ROOT:-/workspace/MI}"
cd "$MI_ROOT"

AUDIO_DIR="$MI_ROOT/Test-Audio"
MICRO_DIR="$AUDIO_DIR/micro_beliefs"

echo "═══════════════════════════════════════════════════════"
echo "  MI Test-Audio Setup"
echo "═══════════════════════════════════════════════════════"

# ── Step 1: Install dependencies ─────────────────────────────────
echo "[STEP 1/4] Installing dependencies..."
pip install -q yt-dlp pretty_midi pyfluidsynth 2>/dev/null || true

# FluidSynth + SoundFont (for MIDI→WAV rendering)
if ! command -v fluidsynth &>/dev/null; then
    echo "  Installing FluidSynth..."
    apt-get update -qq && apt-get install -y -qq fluidsynth fluid-soundfont-gm 2>/dev/null || true
fi

# Ensure SoundFont exists
SF2_PATH=""
for sf in \
    /usr/share/sounds/sf2/FluidR3_GM.sf2 \
    /usr/local/share/fluidsynth/default.sf2 \
    /usr/share/sounds/sf2/TimGM6mb.sf2; do
    if [ -f "$sf" ]; then
        SF2_PATH="$sf"
        break
    fi
done

# If no system SF2, download TimGM6mb
if [ -z "$SF2_PATH" ]; then
    echo "  Downloading TimGM6mb SoundFont..."
    SF2_DIR="$MI_ROOT/.soundfonts"
    mkdir -p "$SF2_DIR"
    SF2_PATH="$SF2_DIR/TimGM6mb.sf2"
    if [ ! -f "$SF2_PATH" ]; then
        python3 -c "
import pretty_midi
import shutil, pathlib
# pretty_midi ships with TimGM6mb.sf2
pm_dir = pathlib.Path(pretty_midi.__file__).parent
sf2 = pm_dir / 'TimGM6mb.sf2'
if sf2.exists():
    shutil.copy(sf2, '$SF2_PATH')
    print(f'  Copied from pretty_midi: {sf2}')
else:
    print('  WARNING: No SoundFont found — MIDI generation may fail')
"
    fi
fi
echo "  SoundFont: ${SF2_PATH:-NONE}"

# ── Step 2: Download main reference tracks via yt-dlp ────────────
echo ""
echo "[STEP 2/4] Downloading main reference tracks..."
mkdir -p "$AUDIO_DIR"

download_track() {
    local SEARCH="$1"
    local TARGET="$2"

    if [ -f "$AUDIO_DIR/$TARGET" ]; then
        echo "  [EXISTS] $TARGET"
        return 0
    fi

    echo "  [DL] $TARGET ..."
    # Download to temp name, then rename
    local TMPNAME="$AUDIO_DIR/_tmp_download"
    yt-dlp -x --audio-format wav \
        --no-playlist \
        -o "${TMPNAME}.%(ext)s" \
        "ytsearch:$SEARCH" 2>/dev/null || {
        echo "  [WARN] Failed to download: $SEARCH"
        return 1
    }

    # Find the downloaded file
    local DL_FILE=$(ls "${TMPNAME}".* 2>/dev/null | head -1)
    if [ -n "$DL_FILE" ]; then
        mv "$DL_FILE" "$AUDIO_DIR/$TARGET"
        echo "  [OK] $TARGET"
    else
        echo "  [WARN] Download produced no file: $SEARCH"
        return 1
    fi
}

# Core tracks needed by Validation fixtures
download_track \
    "Bach Cello Suite No 1 Prelude Yo-Yo Ma" \
    "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav"

download_track \
    "Herald of the Change Hans Zimmer Dune" \
    "Herald of the Change - Hans Zimmer.wav"

# Additional tracks for V7 RSA (needs ≥3 unique stimuli)
download_track \
    "Beethoven Pathetique Sonata Op 13 first movement" \
    "Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.wav"

download_track \
    "Tchaikovsky Swan Lake Suite Op 20a Scene" \
    "Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky.wav"

download_track \
    "Duel of the Fates Star Wars epic orchestral" \
    "Duel of the Fates - Epic Version.wav"

# Count what we have
MAIN_COUNT=$(ls "$AUDIO_DIR"/*.wav 2>/dev/null | wc -l)
echo "  Main tracks: $MAIN_COUNT wav files"

# ── Step 3: Generate micro-belief test stimuli ───────────────────
echo ""
echo "[STEP 3/4] Generating micro-belief test stimuli..."
echo "  This creates ~1000 deterministic WAV files via synthesis/MIDI."
echo "  Takes ~2-5 minutes..."
mkdir -p "$MICRO_DIR"

# Ensure project root is on PYTHONPATH
export PYTHONPATH="$MI_ROOT:${PYTHONPATH:-}"

# F1 — Sensory (synthetic waveforms + MIDI)
echo "  [F1] Generating sensory stimuli..."
python3 Tests/micro_beliefs/generate_f1_audio.py 2>&1 | tail -3 || echo "  [WARN] F1 audio failed"
python3 Tests/micro_beliefs/generate_f1_midi_audio.py 2>&1 | tail -3 || echo "  [WARN] F1 MIDI failed"

# F2 — Prediction
echo "  [F2] Generating prediction stimuli..."
python3 Tests/micro_beliefs/generate_f2_audio.py 2>&1 | tail -3 || echo "  [WARN] F2 failed"

# F3 — Attention & Salience
echo "  [F3] Generating attention stimuli..."
python3 Tests/micro_beliefs/generate_f3_audio.py 2>&1 | tail -3 || echo "  [WARN] F3 failed"

# F4 — Memory
echo "  [F4] Generating memory stimuli..."
python3 Tests/micro_beliefs/generate_f4_audio.py 2>&1 | tail -3 || echo "  [WARN] F4 failed"

# F5 — Emotion
echo "  [F5] Generating emotion stimuli..."
python3 Tests/micro_beliefs/generate_f5_audio.py 2>&1 | tail -3 || echo "  [WARN] F5 failed"

# F6 — Reward
echo "  [F6] Generating reward stimuli..."
python3 Tests/micro_beliefs/generate_f6_audio.py 2>&1 | tail -3 || echo "  [WARN] F6 failed"

# F7 — Motor & Timing
echo "  [F7] Generating motor stimuli..."
python3 Tests/micro_beliefs/generate_f7_audio.py 2>&1 | tail -3 || echo "  [WARN] F7 failed"

# F8 — Learning & Plasticity
echo "  [F8] Generating learning stimuli..."
python3 Tests/micro_beliefs/generate_f8_audio.py 2>&1 | tail -3 || echo "  [WARN] F8 failed"

# F9 — Social Cognition
echo "  [F9] Generating social stimuli..."
python3 Tests/micro_beliefs/generate_f9_audio.py 2>&1 | tail -3 || echo "  [WARN] F9 failed"

# R³ — Early Perceptual (97D)
echo "  [R3] Generating R³ verification stimuli..."
python3 Tests/micro_beliefs/generate_r3_midi_audio.py 2>&1 | tail -3 || echo "  [WARN] R3 MIDI failed"

# ── Step 4: Verify ───────────────────────────────────────────────
echo ""
echo "[STEP 4/4] Verifying..."

MAIN_WAV=$(find "$AUDIO_DIR" -maxdepth 1 -name "*.wav" | wc -l)
MICRO_WAV=$(find "$MICRO_DIR" -name "*.wav" 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "$AUDIO_DIR" 2>/dev/null | cut -f1)

echo ""
echo "═══════════════════════════════════════════════════════"
echo "  TEST-AUDIO STATUS"
echo "═══════════════════════════════════════════════════════"
echo "  Main reference tracks:     $MAIN_WAV wav files"
echo "  Micro-belief stimuli:      $MICRO_WAV wav files"
echo "  Total size:                $TOTAL_SIZE"
echo ""

# Check critical files
CRITICAL_FILES=(
    "Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.wav"
    "Herald of the Change - Hans Zimmer.wav"
)
ALL_OK=true
for f in "${CRITICAL_FILES[@]}"; do
    if [ -f "$AUDIO_DIR/$f" ]; then
        echo "  [OK] $f"
    else
        echo "  [MISSING] $f"
        ALL_OK=false
    fi
done

# Check micro dirs
for fn in f1 f2 f3 f4 f5 f6 f7 f8 f9 r3_midi; do
    count=$(find "$MICRO_DIR/$fn" -name "*.wav" 2>/dev/null | wc -l)
    if [ "$count" -gt 0 ]; then
        echo "  [OK] micro_beliefs/$fn: $count files"
    else
        echo "  [MISSING] micro_beliefs/$fn"
        ALL_OK=false
    fi
done

echo "═══════════════════════════════════════════════════════"

if $ALL_OK; then
    echo "  All test audio ready!"
else
    echo "  Some files missing — check warnings above"
fi

echo ""
echo "  Next: run validation with"
echo "    python -m pytest Validation/ -v --timeout=600"
echo ""
