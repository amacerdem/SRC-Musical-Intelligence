#!/usr/bin/env python3
"""
MI Dataset Cleanup
==================
1. Remove duplicates (keep "Artist - Title.wav", delete bare "Title.wav")
2. Remove abnormally large files (wrong YouTube matches — full albums)
3. Re-download failed/removed tracks with correct artist names

Usage:
    python cleanup_dataset.py [--dataset /workspace/dataset]
    python cleanup_dataset.py --dry-run   # preview only
"""

import argparse
import json
import os
import re
import subprocess
import time

# Max reasonable WAV size: 20 min @ 44.1kHz stereo 16-bit ≈ 200 MB
MAX_FILE_SIZE = 250 * 1024 * 1024  # 250 MB

# Known correct artist-title pairs for all 240 tracks
# Used for re-downloading when oEmbed failed
CORRECT_TRACKS = [
    ("Ryo Fukui", "Early Summer"),
    ("Ryo Fukui", "Autumn Leaves"),
    ("Hiromi, Tomoaki Baba, Shun Ishiwaka", "N.E.W."),
    ("Hiromi", "Seeker"),
    ("Hiromi", "Voice"),
    ("Hiromi", "Desire"),
    ("Hiromi", "Uncertainty"),
    ("Hiromi", "Alive"),
    ("Hiromi", "Dreamer"),
    ("Chihiro Yamanaka", "乙女の祈り"),
    ("Chihiro Yamanaka", "ユートピア"),
    ("Chihiro Yamanaka", "マイ・フェイヴァリット・シングス"),
    ("Art Tatum", "Tea for Two"),
    ("Art Tatum", "Blue Skies"),
    ("Ahmad Jamal", "Ahmad's Blues"),
    ("Miles Davis", "Blue in Green"),
    ("Miles Davis", "So What"),
    ("Red Garland", "Almost Like Being In Love"),
    ("Wynton Kelly", "Portrait of Jenny"),
    ("Wynton Kelly, Miles Davis", "Someday My Prince Will Come"),
    ("Horace Parlan", "Cryin' Blues"),
    ("Horace Parlan", "Wednesday Night Prayer Meeting"),
    ("Duke Ellington, John Coltrane", "In A Sentimental Mood"),
    ("John Coltrane, Johnny Hartman", "My One And Only Love"),
    ("Duke Ellington, John Coltrane", "My Little Brown Book"),
    ("Charlie Parker", "Summertime"),
    ("Charlie Parker", "All The Things You Are"),
    ("Charlie Parker, Miles Davis", "Donna Lee"),
    ("Charlie Parker, Miles Davis", "Constellation"),
    ("Charlie Parker", "Parker's Mood"),
    ("Charlie Parker", "A Night in Tunisia"),
    ("Charlie Parker", "Ornithology"),
    ("Charlie Parker", "In The Still Of The Night"),
    ("Charlie Parker", "Autumn In New York"),
    ("Charlie Parker", "Night And Day"),
    ("Charlie Parker", "Stella By Starlight"),
    ("Chet Baker", "I Fall In Love Too Easily"),
    ("Chet Baker", "Almost Blue"),
    ("Chet Baker", "I Wish You Love"),
    ("loopgarden", "Iris' Secret"),
    ("Chet Baker", "I'll Be Around"),
    ("Ella Fitzgerald, Louis Armstrong", "Dream A Little Dream Of Me"),
    ("Louis Armstrong", "La vie en rose"),
    ("Ella Fitzgerald, Louis Armstrong", "Summertime"),
    ("Billie Holiday", "I'll Be Seeing You"),
    ("Billie Holiday", "Blue Moon"),
    ("Miles Davis", "It Never Entered My Mind"),
    ("Miles Davis", "Freddie Freeloader"),
    ("Hiromi", "Impressions"),
    ("Hiromi, Tomoaki Baba, Shun Ishiwaka", "FIRST NOTE"),
    ("Hiromi, Tomoaki Baba, Shun Ishiwaka", "BLUE GIANT"),
    ("Luca Sestak", "Solfeggietto"),
    ("Kazumi Tateishi Trio", "人生のメリーゴーランド"),
    ("Art Blakey & The Jazz Messengers", "Moanin'"),
    ("Art Blakey & The Jazz Messengers", "Come Rain Or Come Shine"),
    ("Art Blakey & The Jazz Messengers", "Hipsippy Blues"),
    ("John Coltrane", "Blue Train"),
    ("Dizzy Gillespie", "All The Things You Are"),
    ("Dizzy Gillespie", "A Night In Tunisia"),
    ("Farhad Mehrad", "I Believe To My Soul"),
    ("Oscar Peterson Trio", "Georgia On My Mind"),
    ("Dizzy Gillespie", "Groovin' High"),
    ("Teddy Wilson", "Stompin' At the Savoy"),
    ("Sonny Stitt", "Alone Together"),
    ("Teddy Wilson", "Say It Isn't So"),
    ("Sonny Stitt", "If I Had You"),
    ("Jimmy Rushing", "Take Me Back Baby"),
    ("Jimmy Rushing", "Mister Five by Five"),
    ("Jimmy Rushing", "Sent for you Yesterday"),
    ("Dave Brubeck, Jimmy Rushing", "There'll Be Some Changes Made"),
    ("John Wasson", "Caravan"),
    ("Nina Simone", "Feeling Good"),
    ("Hank Levy", "Whiplash"),
    ("Harry James", "It's Been a Long, Long Time"),
    ("SEATBELTS", "Tank!"),
    ("Nat King Cole", "Unforgettable"),
    ("Nat King Cole", "L-O-V-E"),
    ("Bernard Herrmann", "A Reluctant Hero"),
    ("Justin Hurwitz", "Damascus Thump"),
    ("George Gershwin", "Mine"),
    ("Charlie Parker", "Laura"),
    ("Dizzy Gillespie, Sonny Stitt, Sonny Rollins", "On The Sunny Side Of The Street"),
    ("John Coltrane", "Equinox"),
    ("Horace Silver", "Song For My Father"),
    ("Duke Ellington", "Isfahan"),
    ("Oliver Nelson", "Stolen Moments"),
    ("Snarky Puppy", "Shofukan"),
    ("Flea", "Thinkin Bout You"),
    ("Snarky Puppy, Metropole Orkest", "It Stays With You"),
    ("Snarky Puppy, Metropole Orkest", "Waves Upon Waves"),
    ("Snarky Puppy", "What About Me?"),
    ("Snarky Puppy", "Lingus"),
    ("Avishai Cohen", "Dreaming"),
    ("Weather Report", "Birdland"),
    ("Weather Report", "Teen Town"),
    ("Brad Mehldau", "Blackbird"),
    ("Ahmad Jamal Trio", "Dolphin Dance"),
    ("Thelonious Monk", "Straight, No Chaser"),
    ("Charles Mingus", "Better Git It in Your Soul"),
    ("Wayne Shorter", "Footprints"),
]


def sanitize_for_match(name):
    """Normalize a filename for matching."""
    # Remove extension
    name = os.path.splitext(name)[0]
    # Remove non-breaking spaces and special chars
    name = name.replace('\u00a0', ' ')
    name = re.sub(r'[_\-\s]+', ' ', name).strip().lower()
    return name


def find_duplicates(dataset_dir):
    """Find files that exist both with and without artist prefix."""
    files = [f for f in os.listdir(dataset_dir) if f.endswith('.wav')]

    # Build map: title -> [files with that title]
    artist_files = {}  # files with "Artist - Title" format
    bare_files = {}    # files with just "Title" format

    for f in files:
        name = os.path.splitext(f)[0]
        if ' - ' in name:
            # Has artist prefix
            parts = name.split(' - ', 1)
            title_key = sanitize_for_match(parts[1])
            artist_files.setdefault(title_key, []).append(f)
        else:
            title_key = sanitize_for_match(name)
            bare_files.setdefault(title_key, []).append(f)

    duplicates_to_remove = []
    for title_key, bare_list in bare_files.items():
        if title_key in artist_files:
            # Artist version exists — mark bare version for removal
            duplicates_to_remove.extend(bare_list)

    return duplicates_to_remove


def find_oversized(dataset_dir):
    """Find abnormally large files (likely full albums)."""
    oversized = []
    for f in os.listdir(dataset_dir):
        if not f.endswith('.wav'):
            continue
        path = os.path.join(dataset_dir, f)
        size = os.path.getsize(path)
        if size > MAX_FILE_SIZE:
            oversized.append((f, size))
    return oversized


def search_youtube(query):
    """Search YouTube for a track."""
    try:
        result = subprocess.run(
            ["yt-dlp", f"ytsearch1:{query}", "--get-id", "--no-warnings", "--no-playlist"],
            capture_output=True, text=True, timeout=30,
        )
        vid = result.stdout.strip()
        if vid:
            return f"https://www.youtube.com/watch?v={vid}"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def download_track(url, output_path):
    """Download a single track as WAV."""
    try:
        result = subprocess.run(
            ["yt-dlp", "-x", "--audio-format", "wav", "--audio-quality", "0",
             "-o", output_path, "--no-warnings", "--no-playlist", url],
            capture_output=True, text=True, timeout=300,
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False


def get_expected_filename(artist, title):
    """Generate the expected filename for a track."""
    safe = re.sub(r'[<>:"/\\|?*]', '_', f"{artist} - {title}")[:200]
    return f"{safe}.wav"


def main():
    parser = argparse.ArgumentParser(description="MI Dataset Cleanup")
    parser.add_argument("--dataset", default="/workspace/dataset")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    dataset = args.dataset
    print(f"=== MI Dataset Cleanup ===")
    print(f"  Dataset: {dataset}\n")

    # Step 1: Find duplicates
    print("[1/4] Finding duplicates...")
    dupes = find_duplicates(dataset)
    print(f"  Found {len(dupes)} duplicate bare files")
    for f in sorted(dupes):
        size_mb = os.path.getsize(os.path.join(dataset, f)) / (1024 * 1024)
        print(f"    DEL: {f} ({size_mb:.1f} MB)")

    # Step 2: Find oversized files
    print(f"\n[2/4] Finding oversized files (>{MAX_FILE_SIZE // (1024*1024)} MB)...")
    oversized = find_oversized(dataset)
    # Don't double-count ones already in dupes
    oversized = [(f, s) for f, s in oversized if f not in dupes]
    print(f"  Found {len(oversized)} oversized files")
    for f, size in sorted(oversized):
        print(f"    DEL: {f} ({size / (1024*1024):.1f} MB)")

    # Combine removal list
    to_remove = set(dupes + [f for f, _ in oversized])

    if args.dry_run:
        print(f"\n  DRY RUN — would remove {len(to_remove)} files")
        return

    # Step 3: Delete bad files
    print(f"\n[3/4] Removing {len(to_remove)} files...")
    freed = 0
    for f in sorted(to_remove):
        path = os.path.join(dataset, f)
        size = os.path.getsize(path)
        os.remove(path)
        freed += size
        print(f"    Removed: {f}")

    # Also remove .part files
    for f in os.listdir(dataset):
        if f.endswith('.part'):
            os.remove(os.path.join(dataset, f))
            print(f"    Removed partial: {f}")

    print(f"  Freed: {freed / (1024**3):.2f} GB")

    # Update download log — remove deleted entries
    log_path = os.path.join(dataset, "download_log.json")
    if os.path.exists(log_path):
        with open(log_path) as f:
            dl_log = json.load(f)
        # Remove entries for deleted files
        removed_keys = []
        for key in list(dl_log.keys()):
            filename = f"{key}.wav"
            if filename in to_remove or not os.path.exists(os.path.join(dataset, filename)):
                removed_keys.append(key)
        for key in removed_keys:
            del dl_log[key]
        with open(log_path, 'w') as f:
            json.dump(dl_log, f, indent=2, ensure_ascii=False)

    # Step 4: Re-download missing tracks with correct artist names
    print(f"\n[4/4] Re-downloading missing/bad tracks...")
    existing = set(os.listdir(dataset))

    missing = []
    for artist, title in CORRECT_TRACKS:
        expected = get_expected_filename(artist, title)
        # Check if any file contains this title with artist
        found = False
        title_lower = title.lower()
        artist_first = artist.split(',')[0].strip().lower()
        for f in existing:
            f_lower = f.lower()
            if artist_first in f_lower and title_lower in f_lower:
                found = True
                break
        if not found:
            missing.append((artist, title, expected))

    print(f"  {len(missing)} tracks need re-download")

    for i, (artist, title, expected) in enumerate(missing, 1):
        query = f"{artist} {title}"
        output = os.path.join(dataset, expected)

        print(f"  [{i:3d}/{len(missing)}] {query}", end="", flush=True)

        url = search_youtube(query)
        if not url:
            print(" — NOT FOUND")
            continue

        print(" — downloading...", end="", flush=True)
        ok = download_track(url, output)

        if ok:
            # Verify size
            size = os.path.getsize(output)
            if size > MAX_FILE_SIZE:
                os.remove(output)
                print(f" — TOO LARGE ({size//(1024*1024)} MB), removed")
            else:
                print(f" OK ({size//(1024*1024)} MB)")
        else:
            print(" FAILED")

        time.sleep(1)

    # Final summary
    wav_files = [f for f in os.listdir(dataset) if f.endswith('.wav')]
    total_size = sum(os.path.getsize(os.path.join(dataset, f)) for f in wav_files)
    print(f"\n=== Cleanup Complete ===")
    print(f"  Tracks: {len(wav_files)}")
    print(f"  Size:   {total_size / (1024**3):.2f} GB")


if __name__ == "__main__":
    main()
