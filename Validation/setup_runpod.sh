#!/usr/bin/env bash
# ============================================================================
# MI Validation — RunPod Full Setup Script
# ============================================================================
# Usage:  bash setup_runpod.sh
#
# What it does:
#   1. Clones MI project from GitHub
#   2. Installs system + Python dependencies
#   3. Downloads ALL validation datasets (V1–V7)
#   4. Patches paths.py for RunPod environment
#   5. Runs the full validation suite
#
# Requirements:
#   - RunPod pod with GPU + Network Volume mounted at /workspace
#   - Internet access
#   - ~100 GB disk space for datasets
# ============================================================================

set -euo pipefail

WORKSPACE="/workspace"
MI_DIR="${WORKSPACE}/MI"
DATASETS="${MI_DIR}/Validation/datasets"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${CYAN}[MI-SETUP]${NC} $*"; }
ok()   { echo -e "${GREEN}[  OK  ]${NC} $*"; }
warn() { echo -e "${YELLOW}[ WARN ]${NC} $*"; }
err()  { echo -e "${RED}[ERROR ]${NC} $*"; }

# ============================================================================
# 1. CLONE PROJECT
# ============================================================================
clone_project() {
    log "Step 1/5: Cloning MI project..."
    if [ -d "${MI_DIR}/.git" ]; then
        ok "Project already cloned, pulling latest..."
        cd "${MI_DIR}" && git pull origin main
    else
        git clone https://github.com/amacerdem/SRC-Musical-Intelligence.git "${MI_DIR}"
    fi
    cd "${MI_DIR}"
    ok "Project ready at ${MI_DIR}"
}

# ============================================================================
# 2. INSTALL DEPENDENCIES
# ============================================================================
install_deps() {
    log "Step 2/5: Installing dependencies..."

    # System packages
    apt-get update -qq
    apt-get install -y -qq git-annex ffmpeg libsndfile1 > /dev/null 2>&1
    ok "System packages installed"

    # Python packages
    pip install -q --upgrade pip

    # Core MI dependencies
    pip install -q \
        numpy scipy librosa soundfile torchaudio \
        tqdm requests

    # Validation-specific
    pip install -q \
        datalad \
        mne \
        nilearn nibabel \
        pretty_midi \
        scikit-learn \
        statsmodels \
        pytest pytest-timeout \
        yt-dlp

    ok "Python packages installed"
}

# ============================================================================
# 3. PATCH PATHS FOR RUNPOD
# ============================================================================
patch_paths() {
    log "Step 3/5: Patching paths for RunPod environment..."

    PATHS_FILE="${MI_DIR}/Validation/config/paths.py"

    # Backup original
    cp "${PATHS_FILE}" "${PATHS_FILE}.bak"

    # Replace hardcoded macOS path with RunPod path
    sed -i "s|Path(\"/Volumes/SRC-9/SRC Musical Intelligence\")|Path(\"${MI_DIR}\")|g" "${PATHS_FILE}"

    ok "Paths patched: PROJECT_ROOT → ${MI_DIR}"
}

# ============================================================================
# 4. DOWNLOAD ALL DATASETS
# ============================================================================
download_datasets() {
    log "Step 4/5: Downloading all datasets..."
    mkdir -p "${DATASETS}"

    # ── V1: Pharmacology (hardcoded, no download needed) ──
    ok "V1 Pharmacology: No download needed (hardcoded data)"

    # ── V2: IDyOM / Essen Folksong Collection (~10 MB) ──
    download_v2_idyom

    # ── V3: Krumhansl (hardcoded, no download needed) ──
    ok "V3 Krumhansl: No download needed (hardcoded profiles)"

    # ── V4: DEAM (~1.3 GB) ──
    download_v4_deam

    # ── V5: NMED-T EEG (~7 GB cleaned) ──
    download_v5_nmedt

    # ── V6a: OpenNeuro ds002725 (~25 GB) ──
    download_v6_ds002725

    # ── V6b: OpenNeuro ds003720 (~40 GB) ──
    download_v6_ds003720

    # ── V7: RSA (Test-Audio — download public domain recordings) ──
    download_v7_test_audio

    log "All datasets downloaded!"
    du -sh "${DATASETS}"/*/ 2>/dev/null || true
}

# ── V2: Essen Folksong Collection ──
download_v2_idyom() {
    local DEST="${DATASETS}/idyom_corpora/essen"
    if [ -d "${DEST}/.git" ]; then
        ok "V2 IDyOM: Already downloaded"
        return
    fi
    log "V2 IDyOM: Cloning Essen Folksong Collection (~10 MB)..."
    git clone --depth 1 \
        https://github.com/ccarh/essen-folksong-collection \
        "${DEST}"
    ok "V2 IDyOM: Done"
}

# ── V4: DEAM ──
download_v4_deam() {
    local DEST="${DATASETS}/deam"
    local MARKER="${DEST}/.download_complete"
    if [ -f "${MARKER}" ]; then
        ok "V4 DEAM: Already downloaded"
        return
    fi

    mkdir -p "${DEST}/annotations" "${DEST}/audio"
    log "V4 DEAM: Downloading annotations..."
    cd "${DEST}/annotations"
    curl -L -O "https://cvml.unige.ch/databases/DEAM/DEAM_Annotations.zip"
    unzip -q -o DEAM_Annotations.zip && rm -f DEAM_Annotations.zip

    log "V4 DEAM: Downloading audio (~1.3 GB)..."
    cd "${DEST}/audio"
    curl -L -O "https://cvml.unige.ch/databases/DEAM/DEAM_audio.zip"
    unzip -q -o DEAM_audio.zip && rm -f DEAM_audio.zip

    echo "ok" > "${MARKER}"
    ok "V4 DEAM: Done"
}

# ── V5: NMED-T (Stanford Digital Repository) ──
download_v5_nmedt() {
    local DEST="${DATASETS}/nmed_t"
    local MARKER="${DEST}/.download_complete"
    if [ -f "${MARKER}" ]; then
        ok "V5 NMED-T: Already downloaded"
        return
    fi

    mkdir -p "${DEST}/cleaned_eeg"
    local BASE="https://stacks.stanford.edu/file/jn859kj8079"

    log "V5 NMED-T: Downloading 10 cleaned EEG files (~7 GB)..."
    cd "${DEST}/cleaned_eeg"
    for i in 21 22 23 24 25 26 27 28 29 30; do
        if [ ! -f "song${i}_Imputed.mat" ]; then
            log "  Downloading song${i}_Imputed.mat..."
            curl -L -o "song${i}_Imputed.mat" "${BASE}/song${i}_Imputed.mat" &
        fi
    done

    # Participant info
    cd "${DEST}"
    if [ ! -f "participantInfo.mat" ]; then
        curl -L -o "participantInfo.mat" "${BASE}/participantInfo.mat" &
    fi

    # Wait for all background downloads
    wait

    # Verify all files exist
    local COUNT
    COUNT=$(ls "${DEST}/cleaned_eeg"/song*_Imputed.mat 2>/dev/null | wc -l)
    if [ "${COUNT}" -ge 10 ]; then
        echo "ok" > "${MARKER}"
        ok "V5 NMED-T: Done (${COUNT} songs)"
    else
        warn "V5 NMED-T: Only ${COUNT}/10 songs downloaded"
    fi
}

# ── V6a: OpenNeuro ds002725 (EEG-fMRI, ~25 GB) ──
download_v6_ds002725() {
    local DEST="${DATASETS}/openneuro_ds002725"
    local MARKER="${DEST}/.download_complete"
    if [ -f "${MARKER}" ]; then
        ok "V6 ds002725: Already downloaded"
        return
    fi

    log "V6 ds002725: Installing via datalad (~25 GB)..."
    if [ ! -d "${DEST}/.git" ]; then
        datalad install \
            -s "https://github.com/OpenNeuroDatasets/ds002725.git" \
            "${DEST}"
    fi

    cd "${DEST}"
    log "V6 ds002725: Fetching binary data (all 21 subjects)..."
    datalad get .

    echo "ok" > "${MARKER}"
    ok "V6 ds002725: Done"
}

# ── V6b: OpenNeuro ds003720 (Genre fMRI, ~40 GB) ──
download_v6_ds003720() {
    local DEST="${DATASETS}/openneuro_ds003720"
    local MARKER="${DEST}/.download_complete"
    if [ -f "${MARKER}" ]; then
        ok "V6 ds003720: Already downloaded"
        return
    fi

    log "V6 ds003720: Installing via datalad (~40 GB)..."
    if [ ! -d "${DEST}/.git" ]; then
        datalad install \
            -s "https://github.com/OpenNeuroDatasets/ds003720.git" \
            "${DEST}"
    fi

    cd "${DEST}"
    log "V6 ds003720: Fetching binary data (all 5 subjects)..."
    datalad get .

    echo "ok" > "${MARKER}"
    ok "V6 ds003720: Done"
}

# ── V7: Test-Audio (public domain classical recordings via yt-dlp) ──
download_v7_test_audio() {
    local DEST="${MI_DIR}/Test-Audio"
    if [ -d "${DEST}" ] && [ "$(ls "${DEST}"/*.wav 2>/dev/null | wc -l)" -ge 3 ]; then
        ok "V7 Test-Audio: Already downloaded ($(ls "${DEST}"/*.wav | wc -l) WAVs)"
        return
    fi

    mkdir -p "${DEST}"
    pip install -q yt-dlp

    log "V7 Test-Audio: Downloading public domain classical recordings..."

    # Bach Cello Suite No. 1 BWV 1007 - Prelude (public domain composition)
    yt-dlp -x --audio-format wav --audio-quality 0 \
        -o "${DEST}/Cello Suite No. 1 in G Major, BWV 1007 I. Prélude.%(ext)s" \
        "ytsearch1:Bach Cello Suite No 1 Prelude BWV 1007 audio" \
        2>/dev/null || warn "Bach Cello Suite download failed"

    # Beethoven Pathetique Sonata Op.13 I. Grave (public domain composition)
    yt-dlp -x --audio-format wav --audio-quality 0 \
        -o "${DEST}/Beethoven - Pathetique Sonata Op13 I. Grave - Allegro.%(ext)s" \
        "ytsearch1:Beethoven Pathetique Sonata Op 13 Grave Allegro audio" \
        2>/dev/null || warn "Beethoven Pathetique download failed"

    # Tchaikovsky Swan Lake - Swan Theme (public domain composition)
    yt-dlp -x --audio-format wav --audio-quality 0 \
        -o "${DEST}/Swan Lake Suite, Op. 20a_ I. Scene _Swan Theme_. Moderato - Pyotr Ilyich Tchaikovsky.%(ext)s" \
        "ytsearch1:Tchaikovsky Swan Lake Swan Theme Moderato audio" \
        2>/dev/null || warn "Swan Lake download failed"

    # Zimmer - Herald of the Change
    yt-dlp -x --audio-format wav --audio-quality 0 \
        -o "${DEST}/Herald of the Change - Hans Zimmer.%(ext)s" \
        "ytsearch1:Hans Zimmer Herald of the Change audio" \
        2>/dev/null || warn "Herald of the Change download failed"

    # Duel of the Fates
    yt-dlp -x --audio-format wav --audio-quality 0 \
        -o "${DEST}/Duel of the Fates - Epic Version.%(ext)s" \
        "ytsearch1:Duel of the Fates epic version audio" \
        2>/dev/null || warn "Duel of the Fates download failed"

    local N_WAV
    N_WAV=$(ls "${DEST}"/*.wav 2>/dev/null | wc -l)
    if [ "${N_WAV}" -ge 3 ]; then
        ok "V7 Test-Audio: Done (${N_WAV} WAVs)"
    else
        warn "V7 Test-Audio: Only ${N_WAV} WAVs (need ≥3 for RSA)"
    fi
}

# ============================================================================
# 5. VERIFY & REPORT
# ============================================================================
verify_datasets() {
    log "Step 5/5: Verifying datasets..."
    echo ""
    echo "═══════════════════════════════════════════════════════"
    echo "  DATASET STATUS"
    echo "═══════════════════════════════════════════════════════"

    local ALL_OK=true

    # V1 - Pharmacology
    echo -n "  V1 Pharmacology (hardcoded)       : "
    echo -e "${GREEN}READY${NC}"

    # V2 - IDyOM
    echo -n "  V2 IDyOM Essen Folksong           : "
    if [ -d "${DATASETS}/idyom_corpora/essen/.git" ]; then
        local N_KRN
        N_KRN=$(find "${DATASETS}/idyom_corpora/essen" -name "*.krn" 2>/dev/null | wc -l)
        echo -e "${GREEN}READY${NC} (${N_KRN} .krn files)"
    else
        echo -e "${RED}MISSING${NC}"; ALL_OK=false
    fi

    # V3 - Krumhansl
    echo -n "  V3 Krumhansl (hardcoded)           : "
    echo -e "${GREEN}READY${NC}"

    # V4 - DEAM
    echo -n "  V4 DEAM                            : "
    if [ -f "${DATASETS}/deam/.download_complete" ]; then
        local N_MP3
        N_MP3=$(find "${DATASETS}/deam" -name "*.mp3" 2>/dev/null | wc -l)
        echo -e "${GREEN}READY${NC} (${N_MP3} songs)"
    else
        echo -e "${RED}MISSING${NC}"; ALL_OK=false
    fi

    # V5 - NMED-T
    echo -n "  V5 NMED-T EEG                      : "
    if [ -f "${DATASETS}/nmed_t/.download_complete" ]; then
        local N_MAT
        N_MAT=$(ls "${DATASETS}/nmed_t/cleaned_eeg"/song*_Imputed.mat 2>/dev/null | wc -l)
        echo -e "${GREEN}READY${NC} (${N_MAT} songs)"
    else
        echo -e "${RED}MISSING${NC}"; ALL_OK=false
    fi

    # V6a - ds002725
    echo -n "  V6 ds002725 EEG-fMRI               : "
    if [ -f "${DATASETS}/openneuro_ds002725/.download_complete" ]; then
        echo -e "${GREEN}READY${NC}"
    else
        echo -e "${RED}MISSING${NC}"; ALL_OK=false
    fi

    # V6b - ds003720
    echo -n "  V6 ds003720 Genre fMRI              : "
    if [ -f "${DATASETS}/openneuro_ds003720/.download_complete" ]; then
        echo -e "${GREEN}READY${NC}"
    else
        echo -e "${RED}MISSING${NC}"; ALL_OK=false
    fi

    # V7 - RSA
    echo -n "  V7 RSA (Test-Audio)                : "
    if [ -d "${MI_DIR}/Test-Audio" ]; then
        local N_WAV
        N_WAV=$(ls "${MI_DIR}/Test-Audio"/*.wav 2>/dev/null | wc -l)
        if [ "${N_WAV}" -ge 3 ]; then
            echo -e "${GREEN}READY${NC} (${N_WAV} WAVs)"
        else
            echo -e "${YELLOW}WARN${NC} (only ${N_WAV} WAVs, need ≥3)"
        fi
    else
        echo -e "${RED}MISSING${NC}"; ALL_OK=false
    fi

    echo "═══════════════════════════════════════════════════════"
    echo ""

    # Disk usage
    log "Disk usage:"
    du -sh "${DATASETS}"/*/ 2>/dev/null || true
    echo ""
    du -sh "${DATASETS}" 2>/dev/null || true

    if [ "${ALL_OK}" = true ]; then
        ok "All datasets ready!"
    else
        warn "Some datasets are missing — check above"
    fi
}

# ============================================================================
# MAIN
# ============================================================================
main() {
    echo ""
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║   MI Validation — RunPod Setup                        ║"
    echo "║   Datasets: V1–V7 (~75 GB total)                      ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""

    clone_project
    install_deps
    patch_paths
    download_datasets
    verify_datasets

    echo ""
    log "Setup complete! Run validation with:"
    echo ""
    echo "  cd ${MI_DIR}"
    echo "  python -m pytest Validation/ -v --timeout=600"
    echo ""
}

main "$@"
