#!/bin/bash
# RunPod Setup Script — MI Dataset Download
# Usage: bash runpod_setup.sh [WORKSPACE_DIR]
#
# Downloads Spotify playlist tracks via YouTube search (no Spotify API needed).

set -euo pipefail

WORKSPACE="${1:-/workspace}"
DATASET_DIR="${WORKSPACE}/dataset"
REPO_DIR="${WORKSPACE}/SRC-Musical-Intelligence"

echo "=== MI RunPod Setup ==="
echo "Workspace: ${WORKSPACE}"
echo "Dataset:   ${DATASET_DIR}"

# --- 1. System dependencies ---
echo -e "\n[1/4] Installing system dependencies..."
apt-get update -qq && apt-get install -y -qq ffmpeg git python3-pip > /dev/null 2>&1
echo "  ffmpeg installed"

# --- 2. Clone repo ---
echo -e "\n[2/4] Cloning MI repository..."
if [ -d "${REPO_DIR}" ]; then
    echo "  Repo already exists, pulling latest..."
    cd "${REPO_DIR}" && git pull --ff-only
else
    git clone https://github.com/amacerdem/SRC-Musical-Intelligence.git "${REPO_DIR}"
fi

# --- 3. Install Python dependencies ---
echo -e "\n[3/4] Installing yt-dlp..."
pip install -q yt-dlp

# --- 4. Download playlist ---
echo -e "\n[4/4] Downloading playlist as WAV..."
python3 "${REPO_DIR}/Musical_Intelligence/scripts/download_playlist.py" \
    --output "${DATASET_DIR}" \
    --format wav

# --- Summary ---
echo -e "\n=== Done ==="
TRACK_COUNT=$(find "${DATASET_DIR}" -name "*.wav" 2>/dev/null | wc -l)
TOTAL_SIZE=$(du -sh "${DATASET_DIR}" 2>/dev/null | cut -f1)
echo "Tracks: ${TRACK_COUNT}"
echo "Size:   ${TOTAL_SIZE}"
echo "Path:   ${DATASET_DIR}"
