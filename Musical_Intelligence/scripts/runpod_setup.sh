#!/bin/bash
# RunPod Setup Script — MI Dataset Download
# Usage: bash runpod_setup.sh [WORKSPACE_DIR]
#
# Downloads the Spotify playlist as WAV files via YouTube matching.

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
echo "  ffmpeg $(ffmpeg -version 2>&1 | head -1 | cut -d' ' -f3) installed"

# --- 2. Clone repo ---
echo -e "\n[2/4] Cloning MI repository..."
if [ -d "${REPO_DIR}" ]; then
    echo "  Repo already exists, pulling latest..."
    cd "${REPO_DIR}" && git pull --ff-only
else
    git clone https://github.com/amacerdem/SRC-Musical-Intelligence.git "${REPO_DIR}"
fi

# --- 3. Install Python dependencies ---
echo -e "\n[3/4] Installing Python dependencies..."
pip install -q spotdl yt-dlp

# --- 4. Download playlist ---
echo -e "\n[4/4] Downloading playlist as WAV..."
mkdir -p "${DATASET_DIR}"
cd "${DATASET_DIR}"

SPOTIFY_URL="https://open.spotify.com/playlist/069wycJBIq0rvTr7bwbbpv"

# spotdl: searches YouTube for exact match, downloads and converts to WAV
spotdl download "${SPOTIFY_URL}" \
    --output "{artist} - {title}" \
    --format wav \
    --threads 4 \
    --bitrate 320k

# --- Summary ---
echo -e "\n=== Download Complete ==="
TRACK_COUNT=$(find "${DATASET_DIR}" -name "*.wav" | wc -l)
TOTAL_SIZE=$(du -sh "${DATASET_DIR}" | cut -f1)
echo "Tracks: ${TRACK_COUNT}"
echo "Size:   ${TOTAL_SIZE}"
echo "Path:   ${DATASET_DIR}"
