"""Dataset download manager with progress bars, caching, and integrity checks."""
from __future__ import annotations

import hashlib
import shutil
import subprocess
import zipfile
from pathlib import Path
from typing import Optional

import requests
from tqdm import tqdm

from Validation.config.paths import DATASETS


def download_file(
    url: str,
    dest: Path,
    *,
    chunk_size: int = 8192,
    expected_sha256: Optional[str] = None,
    force: bool = False,
) -> Path:
    """Download a file with progress bar.

    Args:
        url: URL to download from.
        dest: Destination file path.
        chunk_size: Download chunk size in bytes.
        expected_sha256: Optional SHA256 hash for integrity verification.
        force: Re-download even if file exists.

    Returns:
        Path to downloaded file.
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and not force:
        if expected_sha256 is not None:
            if _check_sha256(dest, expected_sha256):
                print(f"[Download] Already exists & verified: {dest.name}")
                return dest
            else:
                print(f"[Download] Hash mismatch, re-downloading: {dest.name}")
        else:
            print(f"[Download] Already exists: {dest.name}")
            return dest

    print(f"[Download] {url}")
    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))

    with open(dest, "wb") as f:
        with tqdm(total=total_size, unit="B", unit_scale=True, desc=dest.name) as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                pbar.update(len(chunk))

    if expected_sha256 is not None:
        if not _check_sha256(dest, expected_sha256):
            raise ValueError(f"SHA256 mismatch for {dest.name}")

    print(f"[Download] Complete: {dest.name} ({dest.stat().st_size / 1e6:.1f} MB)")
    return dest


def download_and_extract(
    url: str,
    dest_dir: Path,
    *,
    expected_sha256: Optional[str] = None,
    force: bool = False,
) -> Path:
    """Download a zip file and extract it.

    Args:
        url: URL to zip archive.
        dest_dir: Directory to extract into.
        expected_sha256: Optional hash for the zip file.
        force: Re-download even if extracted dir exists.

    Returns:
        Path to extraction directory.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Check if already extracted
    marker = dest_dir / ".download_complete"
    if marker.exists() and not force:
        print(f"[Download] Already extracted: {dest_dir.name}")
        return dest_dir

    # Download zip
    zip_name = url.split("/")[-1]
    zip_path = dest_dir / zip_name
    download_file(url, zip_path, expected_sha256=expected_sha256, force=force)

    # Extract
    print(f"[Extract] {zip_name} → {dest_dir}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        zf.extractall(dest_dir)

    # Clean up zip
    zip_path.unlink()

    # Mark as complete
    marker.write_text("ok")
    return dest_dir


def clone_repo(
    url: str,
    dest_dir: Path,
    *,
    shallow: bool = True,
    force: bool = False,
) -> Path:
    """Clone a git repository.

    Args:
        url: Git repository URL.
        dest_dir: Destination directory.
        shallow: Shallow clone (--depth 1).
        force: Re-clone even if directory exists.

    Returns:
        Path to cloned repo.
    """
    dest_dir = Path(dest_dir)
    if dest_dir.exists() and not force:
        if (dest_dir / ".git").exists():
            print(f"[Git] Already cloned: {dest_dir.name}")
            return dest_dir

    if dest_dir.exists() and force:
        shutil.rmtree(dest_dir)

    cmd = ["git", "clone"]
    if shallow:
        cmd += ["--depth", "1"]
    cmd += [url, str(dest_dir)]

    print(f"[Git] Cloning {url}")
    subprocess.run(cmd, check=True, capture_output=True, text=True)
    print(f"[Git] Cloned: {dest_dir.name}")
    return dest_dir


def download_openneuro(
    dataset_id: str,
    dest_dir: Path,
    *,
    n_subjects: Optional[int] = None,
    force: bool = False,
) -> Path:
    """Download an OpenNeuro dataset using openneuro-py or datalad.

    Args:
        dataset_id: OpenNeuro dataset ID (e.g. 'ds002725').
        dest_dir: Destination directory.
        n_subjects: Limit to first N subjects (None = all).
        force: Re-download.

    Returns:
        Path to dataset directory.
    """
    dest_dir = Path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    marker = dest_dir / ".download_complete"
    if marker.exists() and not force:
        print(f"[OpenNeuro] Already downloaded: {dataset_id}")
        return dest_dir

    try:
        import openneuro
        print(f"[OpenNeuro] Downloading {dataset_id} via openneuro-py...")
        openneuro.download(dataset=dataset_id, target_dir=str(dest_dir))
    except ImportError:
        print(f"[OpenNeuro] openneuro-py not available, trying datalad...")
        url = f"https://github.com/OpenNeuroDatasets/{dataset_id}.git"
        clone_repo(url, dest_dir, force=force)

    marker.write_text("ok")
    return dest_dir


def _check_sha256(path: Path, expected: str) -> bool:
    """Verify file SHA256 hash."""
    sha256 = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest() == expected
