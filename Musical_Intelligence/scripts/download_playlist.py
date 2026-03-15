#!/usr/bin/env python3
"""
MI Dataset Downloader
=====================
Step 1: Fetch all track names from Spotify playlist (no auth needed)
Step 2: Search each track on YouTube 1-by-1
Step 3: Download as WAV

Usage:
    python download_playlist.py [--output /workspace/dataset] [--dry-run]
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

PLAYLIST_ID = "069wycJBIq0rvTr7bwbbpv"
SPOTIFY_EMBED_URL = f"https://open.spotify.com/embed/playlist/{PLAYLIST_ID}"


def fetch_spotify_tracks():
    """Fetch track list from Spotify embed page (no auth required)."""
    print("[1/3] Fetching track list from Spotify...")

    # Fetch the embed HTML — it contains JSON with track data
    req = urllib.request.Request(
        SPOTIFY_EMBED_URL,
        headers={"User-Agent": "Mozilla/5.0 (compatible; MIBot/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8")

    # Extract the __NEXT_DATA__ or resource JSON from the embed
    # Try multiple extraction patterns
    tracks = []

    # Pattern 1: Look for track entries in the HTML/JSON
    # The embed page has a <script id="__NEXT_DATA__"> tag
    match = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            # Navigate the JSON structure to find tracks
            tracks = _extract_from_next_data(data)
            if tracks:
                return tracks
        except (json.JSONDecodeError, KeyError):
            pass

    # Pattern 2: Look for trackList or items in embedded JSON
    for pattern in [
        r'"trackList"\s*:\s*(\[.*?\])',
        r'"items"\s*:\s*(\[.*?\])',
    ]:
        match = re.search(pattern, html, re.DOTALL)
        if match:
            try:
                items = json.loads(match.group(1))
                tracks = _extract_from_items(items)
                if tracks:
                    return tracks
            except json.JSONDecodeError:
                continue

    # Pattern 3: Brute-force find all "name" + "artists" patterns
    track_pattern = re.findall(
        r'"name"\s*:\s*"([^"]+)".*?"artists".*?"name"\s*:\s*"([^"]+)"',
        html,
    )
    if track_pattern:
        seen = set()
        for title, artist in track_pattern:
            key = f"{artist} - {title}"
            if key not in seen:
                seen.add(key)
                tracks.append({"title": title, "artist": artist})

    if not tracks:
        print("  WARNING: Could not extract tracks from Spotify embed.")
        print("  Falling back to hardcoded track list...")
        tracks = _hardcoded_tracks()

    return tracks


def _extract_from_next_data(data):
    """Navigate __NEXT_DATA__ JSON to find tracks."""
    tracks = []
    try:
        # Try common paths in the Spotify embed JSON
        props = data.get("props", {}).get("pageProps", {})
        state = props.get("state", {}).get("data", {}).get("entity", {})
        track_list = state.get("trackList", [])
        for item in track_list:
            title = item.get("title", "")
            artists = item.get("subtitle", "")
            if title:
                tracks.append({"title": title, "artist": artists})
    except (AttributeError, TypeError):
        pass

    if not tracks:
        # Recursive search for track-like objects
        _find_tracks_recursive(data, tracks, depth=0)

    return tracks


def _find_tracks_recursive(obj, tracks, depth=0):
    """Recursively search JSON for track data."""
    if depth > 15:
        return
    if isinstance(obj, dict):
        # Check if this looks like a track
        if "track" in obj and isinstance(obj["track"], dict):
            t = obj["track"]
            title = t.get("name", "")
            artists = ", ".join(a.get("name", "") for a in t.get("artists", []))
            if title and artists:
                tracks.append({"title": title, "artist": artists})
        elif "name" in obj and "artists" in obj and isinstance(obj["artists"], list):
            title = obj["name"]
            artists = ", ".join(a.get("name", "") for a in obj["artists"])
            if title and artists:
                tracks.append({"title": title, "artist": artists})
        for v in obj.values():
            _find_tracks_recursive(v, tracks, depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            _find_tracks_recursive(item, tracks, depth + 1)


def _extract_from_items(items):
    """Extract tracks from a Spotify-style items array."""
    tracks = []
    for item in items:
        track = item.get("track", item)
        title = track.get("name", "")
        artists_list = track.get("artists", [])
        if isinstance(artists_list, list) and artists_list:
            artist = artists_list[0].get("name", "")
        else:
            artist = str(artists_list)
        if title:
            tracks.append({"title": title, "artist": artist})
    return tracks


def _hardcoded_tracks():
    """Fallback: hardcoded track list from playlist."""
    raw = """Early Summer - Ryo Fukui
Autumn Leaves - Ryo Fukui
N.E.W. - Hiromi
Seeker - Hiromi
Voice - Hiromi
Desire - Hiromi
Uncertainty - Hiromi
Alive - Hiromi
Dreamer - Hiromi
乙女の祈り - Chihiro Yamanaka
ユートピア - Chihiro Yamanaka
マイ・フェイヴァリット・シングス - Chihiro Yamanaka
Tea for Two - Art Tatum
Blue Skies - Art Tatum
Ahmad's Blues - Ahmad Jamal
Blue in Green - Miles Davis
So What - Miles Davis
Almost Like Being In Love - Red Garland
Portrait of Jenny - Wynton Kelly
Someday My Prince Will Come - Wynton Kelly
Cryin' Blues - Horace Parlan
Wednesday Night Prayer Meeting - Horace Parlan
In A Sentimental Mood - Duke Ellington John Coltrane
My One And Only Love - John Coltrane Johnny Hartman
My Little Brown Book - Duke Ellington John Coltrane
Summertime - Charlie Parker
All The Things You Are - Charlie Parker
Donna Lee - Charlie Parker
Constellation - Charlie Parker
Parker's Mood - Charlie Parker
A Night in Tunisia - Charlie Parker
Ornithology - Charlie Parker
In The Still Of The Night - Charlie Parker
Autumn In New York - Charlie Parker
Night And Day - Charlie Parker
Stella By Starlight - Charlie Parker
I Fall In Love Too Easily - Chet Baker
Almost Blue - Chet Baker
I Wish You Love - Chet Baker
Iris' Secret - loopgarden
I'll Be Around - Chet Baker
Dream A Little Dream Of Me - Ella Fitzgerald Louis Armstrong
La vie en rose - Louis Armstrong
Summertime - Ella Fitzgerald Louis Armstrong
I'll Be Seeing You - Billie Holiday
Blue Moon - Billie Holiday
It Never Entered My Mind - Miles Davis
Freddie Freeloader - Miles Davis
Impressions - Hiromi
FIRST NOTE - Hiromi
BLUE GIANT - Hiromi
Solfeggietto - Luca Sestak
人生のメリーゴーランド - Kazumi Tateishi Trio
Moanin' - Art Blakey
Come Rain Or Come Shine - Art Blakey
Hipsippy Blues - Art Blakey
Blue Train - John Coltrane
All The Things You Are - Dizzy Gillespie
A Night In Tunisia - Dizzy Gillespie
I Believe To My Soul - Farhad Mehrad
Georgia On My Mind - Oscar Peterson Trio
Groovin' High - Dizzy Gillespie
Stompin' At the Savoy - Teddy Wilson
Alone Together - Sonny Stitt
Say It Isn't So - Teddy Wilson
If I Had You - Sonny Stitt
Take Me Back Baby - Jimmy Rushing
Mister Five by Five - Jimmy Rushing
Sent for you Yesterday - Jimmy Rushing
There'll Be Some Changes Made - Dave Brubeck Jimmy Rushing
Caravan - John Wasson
Feeling Good - Nina Simone
Whiplash - Hank Levy
It's Been a Long, Long Time - Harry James
Tank! - SEATBELTS
Unforgettable - Nat King Cole
L-O-V-E - Nat King Cole
A Reluctant Hero - Bernard Herrmann
Damascus Thump - Justin Hurwitz
Mine - George Gershwin
Laura - Charlie Parker
On The Sunny Side Of The Street - Dizzy Gillespie Sonny Stitt Sonny Rollins
Equinox - John Coltrane
Song For My Father - Horace Silver
Isfahan - Duke Ellington
Stolen Moments - Oliver Nelson
Shofukan - Snarky Puppy
Thinkin Bout You - Flea
It Stays With You - Snarky Puppy
Waves Upon Waves - Snarky Puppy
What About Me? - Snarky Puppy
Lingus - Snarky Puppy
Dreaming - Avishai Cohen
Birdland - Weather Report
Teen Town - Weather Report
Blackbird - Brad Mehldau
Dolphin Dance - Ahmad Jamal Trio
Straight No Chaser - Thelonious Monk
Better Git It in Your Soul - Charles Mingus
Footprints - Wayne Shorter"""
    tracks = []
    for line in raw.strip().split("\n"):
        parts = line.split(" - ", 1)
        if len(parts) == 2:
            tracks.append({"title": parts[0].strip(), "artist": parts[1].strip()})
    return tracks


def search_youtube(query):
    """Search YouTube for a track and return the best video URL."""
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                f"ytsearch1:{query}",
                "--get-id",
                "--no-warnings",
                "--no-playlist",
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
        video_id = result.stdout.strip()
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def download_track(url, output_path, title, idx, total):
    """Download a single track as WAV."""
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-x",
                "--audio-format", "wav",
                "--audio-quality", "0",
                "-o", output_path,
                "--no-warnings",
                "--no-playlist",
                url,
            ],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            return True
        else:
            print(f"    ERROR: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"    TIMEOUT downloading {title}")
        return False


def main():
    parser = argparse.ArgumentParser(description="MI Dataset Downloader")
    parser.add_argument("--output", default="/workspace/dataset", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Only list tracks, don't download")
    parser.add_argument("--start", type=int, default=1, help="Start from track N (1-indexed)")
    parser.add_argument("--format", default="wav", choices=["wav", "mp3", "flac"], help="Audio format")
    args = parser.parse_args()

    # Step 1: Get tracks
    tracks = fetch_spotify_tracks()
    print(f"  Found {len(tracks)} tracks\n")

    if args.dry_run:
        for i, t in enumerate(tracks, 1):
            print(f"  {i:3d}. {t['artist']} - {t['title']}")
        print(f"\nTotal: {len(tracks)} tracks")
        return

    # Step 2 & 3: Search YouTube and download
    os.makedirs(args.output, exist_ok=True)

    # Track progress
    log_path = os.path.join(args.output, "download_log.json")
    downloaded = {}
    if os.path.exists(log_path):
        with open(log_path) as f:
            downloaded = json.load(f)

    total = len(tracks)
    success = len(downloaded)
    failed = []

    print(f"[2/3] Searching YouTube & downloading ({total} tracks)...\n")

    for i, track in enumerate(tracks, 1):
        if i < args.start:
            continue

        query = f"{track['artist']} - {track['title']}"
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', query)[:200]
        ext = args.format
        output_file = os.path.join(args.output, f"{safe_name}.{ext}")

        # Skip if already downloaded
        if safe_name in downloaded:
            print(f"  [{i:3d}/{total}] SKIP (exists): {query}")
            continue

        # Search YouTube
        print(f"  [{i:3d}/{total}] Searching: {query}", end="", flush=True)
        url = search_youtube(query)

        if not url:
            print(f" — NOT FOUND")
            failed.append(query)
            continue

        print(f" — found, downloading...", end="", flush=True)

        # Download
        ok = download_track(url, output_file, query, i, total)
        if ok:
            success += 1
            downloaded[safe_name] = {"url": url, "query": query, "idx": i}
            # Save progress
            with open(log_path, "w") as f:
                json.dump(downloaded, f, indent=2, ensure_ascii=False)
            print(f" OK")
        else:
            failed.append(query)
            print(f" FAILED")

        # Small delay to avoid rate limiting
        time.sleep(1)

    # Summary
    print(f"\n[3/3] === Download Complete ===")
    print(f"  Success: {success}/{total}")
    print(f"  Failed:  {len(failed)}/{total}")
    if failed:
        print(f"\n  Failed tracks:")
        for t in failed:
            print(f"    - {t}")

    # Save failed list
    if failed:
        failed_path = os.path.join(args.output, "failed_tracks.txt")
        with open(failed_path, "w") as f:
            f.write("\n".join(failed))
        print(f"\n  Failed list saved to: {failed_path}")


if __name__ == "__main__":
    main()
