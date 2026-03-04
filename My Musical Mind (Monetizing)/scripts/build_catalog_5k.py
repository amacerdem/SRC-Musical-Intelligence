#!/usr/bin/env python3
"""
Build 5K Music Catalog from Deezer API
========================================
Phase 1: Resolve seed playlist tracks on Deezer
Phase 2: Analyze taste DNA (genre distribution, BPM range, era, mood)
Phase 3: Expand via related artists + genre charts + curated quality artists
Phase 4: Fetch full metadata for all tracks
Phase 5: Compute cognitive dimension labels (energy, complexity, darkness, novelty)
Phase 6: Output catalog_5k.json

Rate limiting: Deezer allows ~50 requests per 5 seconds (10/s)
"""

import json
import os
import sys
import time
import math
import urllib.request
import urllib.parse
import urllib.error
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime

# ─── Config ───────────────────────────────────────────────────────────────────

OUTPUT_DIR = Path(__file__).parent.parent / "data" / "catalog"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PROGRESS_FILE = OUTPUT_DIR / "_progress.json"
CATALOG_FILE = OUTPUT_DIR / "catalog_5k.json"
SEED_ANALYSIS_FILE = OUTPUT_DIR / "seed_analysis.json"

TARGET_CATALOG_SIZE = 5000
DEEZER_RATE_LIMIT = 0.12  # seconds between requests (~8/s, safe margin)
MAX_RETRIES = 3

# ─── Deezer Genre Map ────────────────────────────────────────────────────────

DEEZER_GENRES = {
    0: "All", 85: "Alternative", 106: "Electro", 129: "Jazz",
    132: "Pop", 152: "Rock", 464: "Metal", 466: "Classical",
    113: "Dance", 165: "R&B", 116: "Rap/Hip Hop", 144: "Reggae",
    169: "Soul & Funk", 98: "Folk", 173: "Films/Games", 153: "Blues",
    197: "Latin Music", 2: "Kids", 16: "African Music",
    75: "Brazilian Music", 81: "Indian Music", 95: "Turkish Music",
}

# Genre → Cognitive dimension biases (energy, complexity, darkness, novelty_boost)
GENRE_COGNITIVE_MAP = {
    152: (0.65, 0.50, 0.45, 0.0),   # Rock
    85:  (0.55, 0.60, 0.50, 0.15),   # Alternative
    464: (0.85, 0.65, 0.75, 0.10),   # Metal
    466: (0.30, 0.85, 0.35, 0.20),   # Classical
    129: (0.40, 0.80, 0.30, 0.20),   # Jazz
    106: (0.70, 0.55, 0.40, 0.10),   # Electro
    132: (0.55, 0.35, 0.25, -0.10),  # Pop
    113: (0.75, 0.30, 0.20, -0.05),  # Dance
    116: (0.65, 0.50, 0.55, 0.0),    # Rap/Hip Hop
    165: (0.50, 0.45, 0.35, 0.0),    # R&B
    169: (0.50, 0.45, 0.25, 0.10),   # Soul & Funk
    98:  (0.30, 0.40, 0.30, 0.15),   # Folk
    173: (0.50, 0.60, 0.50, 0.10),   # Films/Games
    153: (0.45, 0.50, 0.50, 0.15),   # Blues
    197: (0.60, 0.45, 0.25, 0.10),   # Latin
    95:  (0.55, 0.55, 0.40, 0.15),   # Turkish Music
}

# ─── Seed Playlist (from Spotify embed scrape) ───────────────────────────────

SEED_TRACKS = [
    ("Fazıl Say, Serenad Bağcan", "Düşerim"),
    ("Fazıl Say, Serenad Bağcan", "Ey Kör, Op. 61"),
    ("Fazıl Say, Serenad Bağcan", "Akılla Bir Konuşmam Oldu"),
    ("Özkan Manav, Dilbağ Tokay, Emine Serdaroğlu", "3 Türkü: No. 1, Ah Bir Ateş Ver"),
    ("Mehmet Güreli", "Kimse Bilmez"),
    ("Büyük Ev Ablukada", "Tayyar Ahmet'in Sonsuz Sayılı Günleri"),
    ("Büyük Ev Ablukada", "Çıldırmicam"),
    ("Yok Öyle Kararlı Şeyler", "Bir Sherlock Değilsin"),
    ("Gaye Su Akyol", "Ölü Bir Adama"),
    ("Büyük Ev Ablukada", "Nasıl İstediysen Öyle İşte"),
    ("Adamlar", "Utanmazsan Unutmam"),
    ("Gaye Su Akyol", "İstikrarlı Hayal Hakikattir"),
    ("Şirin Soysal", "Kuralsız Kahraman"),
    ("Cem Adrian", "Ah Bir Ataş Ver"),
    ("Bulutsuzluk Özlemi", "Sözlerimi Geri Alamam"),
    ("Flört", "Lan Oğlum Böyle Olmaz"),
    ("Ayhan Sicimoğlu", "Istanbul Pas Constantinople"),
    ("Yasemin Mori", "Aslında Bir Konu Var"),
    ("Athena", "Geberiyorum"),
    ("Bulutsuzluk Özlemi", "Bedel"),
    ("Gaye Su Akyol", "Zaman Asla Affetmez"),
    ("Fazıl Say, Cem Adrian", "İnsan İnsan"),
    ("MFÖ", "Olduramadım"),
    ("Kaan Tangöze", "Bekle Dedi Gitti"),
    ("Müzeyyen Senar", "Kimseye Etmem Şikayet"),
    ("Dave Brubeck", "Blue Rondo à la Turk"),
    ("The Vandals", "Mohawk Town"),
    ("Jerry Martin", "Bohemian Street Jam"),
    ("Akeboshi", "Wind"),
    ("Nicholas Britell", "Succession Main Title Theme"),
    ("Nicholas Britell", "Adagio in C Minor"),
    ("Jess Gillam", "Merry Christmas Mr. Lawrence"),
    ("Gia Margaret", "Smoke"),
    ("Sonata Arctica", "Tallulah"),
    ("Karsu", "Ben Nası Büyük Adam Olucam"),
    ("Leonard Cohen", "Famous Blue Raincoat"),
    ("Wheel", "Wheel"),
    ("Charles Mingus", "Boogie Stop Shuffle"),
    ("Charles Mingus", "GG Train"),
    ("Herbie Hancock", "Cantaloupe Island"),
    ("Buddy Rich", "The Surrey With The Fringe On Top"),
    ("John Coltrane", "Giant Steps"),
    ("Ryan Kisor", "Boogie Stop Shuffle"),
    ("Chico Hamilton", "I Want To Be Happy"),
    ("Franck Avitabile", "Tempus Fugit"),
    ("Yo-Yo Ma", "Allegretto from Partita"),
    ("Finnur Karlsson", "Öll náttúran enn fer að deyja"),
    ("The Ghost of Johnny Cash", "House of the Rising Sun"),
    ("Joe Satriani", "The Extremist"),
    ("Özkan Uğur", "Olduramadım"),
    ("Sagopa Kajmer", "Al 1'de Burdan Yak"),
    ("Bir Şeyler Eksik", "Bas Konuş Bırak Dinle"),
    ("Athena", "Sende Yap"),
    ("They Might Be Giants", "Istanbul Not Constantinople"),
    ("Nil Karaibrahimgil", "Ben Buraya Çıplak Geldim"),
    ("Nil Karaibrahimgil", "Kanatlarım Var Ruhumda"),
    ("AURORA", "Runaway"),
    ("Charles Mingus", "Moanin'"),
    ("Yo-Yo Ma, Kathryn Stott", "Après un rêve"),
    ("Mazhar Alanson", "Bu Ne Biçim Hikaye Böyle"),
    ("Jean Sibelius, Yo-Yo Ma", "Was it a Dream?"),
    ("Flört", "Dün Trt'de İzledim"),
    ("Tarkan", "Geççek"),
    ("Duman", "Belki Alışman Lazım"),
    ("Zeynep Ucbasaran", "Anadolu'dan"),
    ("Ennio Morricone", "The Ecstasy Of Gold"),
    ("Ari Barokas", "Yaşıyorum Sil Baştan"),
    ("Roy Hargrove", "Strasbourg St. Denis"),
    ("Ari Barokas", "Salaksın"),
    ("Maurice Ravel, Bertrand Chamayou", "Gaspard de la nuit Le Gibet"),
    ("Christopher Dennis Coleman", "Don't Go"),
    ("The Tallis Scholars", "Allegri Miserere"),
    ("Gregorio Allegri", "Miserere mei Deus"),
    ("Christine Southworth", "Charged"),
    ("Adrienne Albert", "L.A. Tango Nuevo"),
    ("Nina C. Young", "Kolokol"),
    ("Cem Karaca, Dervişan", "Beni Siz Delirttiniz"),
    ("Michael Giacchino", "Credit Where Credit Is Due"),
    ("Julia Wolfe", "Anthracite Fields Flowers"),
    ("Johann Sebastian Bach", "Little Fugue in G minor"),
    ("Valerie Capers", "Sweet Mister Jelly Roll"),
    ("Johann Sebastian Bach, Tatiana Nikolayeva", "Fugue in G Minor BWV 578"),
    ("Lønelo, DWELLS", "Take Off Everything"),
    ("Ekaterina Shelehova, Furkan Usta", "Ateş and Moon"),
    ("Ludwig van Beethoven, Vladimir Horowitz", "Waldstein Allegro con brio"),
    ("Ludwig van Beethoven, Igor Levit", "Waldstein Allegro con brio"),
    ("Felix Rösch, mondëna quartet", "Berceuse Rework"),
    ("renewwed, capella", "Take Off Everything"),
    ("Yüzyüzeyken Konuşuruz", "Ölmemişiz"),
    ("Nora Van Elken", "Celestial"),
    ("Atlas Plug", "Truth Be Known"),
    ("KXLLSWXTCH", "WASTE"),
    ("Athena", "Serseri Mayın"),
    ("The Hot Club Of San Francisco", "Place De Brouckrère"),
    ("Sıla, Kenan Doğulu", "...dan sonra"),
    ("Too Many Zooz", "Tricerahops"),
    ("Dope", "Die MF Die"),
    ("Franz Ferdinand", "Take Me Out"),
    ("CSO, Tim", "This is Halloween"),
    ("Şirin Soysal", "Ne Yaptım Şu Hayatta"),
]

# ─── Curated Quality Artists (cross-genre, universally acclaimed) ─────────────
# These ensure the catalog has undeniable quality depth even beyond the seed taste

CURATED_QUALITY_ARTISTS = [
    # Jazz legends & modern
    "Miles Davis", "Bill Evans", "Thelonious Monk", "Chet Baker",
    "Brad Mehldau", "Avishai Cohen", "Esbjörn Svensson Trio", "GoGo Penguin",
    "Kamasi Washington", "Robert Glasper", "Tigran Hamasyan", "Snarky Puppy",
    "Pat Metheny", "Wes Montgomery", "Oscar Peterson", "Keith Jarrett",

    # Classical — solo & orchestral
    "Glenn Gould", "Martha Argerich", "Hélène Grimaud", "Daniil Trifonov",
    "Hilary Hahn", "Jacqueline du Pré", "Lang Lang", "Víkingur Ólafsson",
    "Max Richter", "Ólafur Arnalds", "Nils Frahm", "Ludovico Einaudi",
    "Joep Beving", "Khatia Buniatishvili", "Yuja Wang",
    "Philip Glass", "Steve Reich", "Arvo Pärt", "Erik Satie",

    # Film/TV scores
    "Hans Zimmer", "Ennio Morricone", "John Williams", "Joe Hisaishi",
    "Alexandre Desplat", "Thomas Newman", "Clint Mansell", "Jonny Greenwood",
    "Ramin Djawadi", "Ludwig Göransson", "Trent Reznor",

    # Rock — classic & quality
    "Radiohead", "Pink Floyd", "Led Zeppelin", "Queen",
    "Tool", "Porcupine Tree", "Opeth", "Sigur Rós",
    "Muse", "Arctic Monkeys", "The Strokes", "Tame Impala",
    "King Crimson", "Yes", "Rush", "Jethro Tull",
    "Nick Cave & The Bad Seeds", "Tom Waits", "Jeff Buckley",

    # Alt/Indie quality
    "Bon Iver", "Fleet Foxes", "Sufjan Stevens", "Nick Drake",
    "Elliott Smith", "Iron & Wine", "José González",
    "Agnes Obel", "Ane Brun", "Daughter", "London Grammar",
    "Cigarettes After Sex", "Khruangbin", "Bonobo",
    "Alt-J", "Glass Animals", "Everything Everything",

    # Electronic — quality
    "Aphex Twin", "Boards of Canada", "Jon Hopkins", "Four Tet",
    "Burial", "Moderat", "Amon Tobin", "Floating Points",
    "Tycho", "Kiasmos", "Rival Consoles", "Max Cooper",
    "Bicep", "Jamie xx", "Nicolas Jaar", "Apparat",

    # Soul / R&B / Funk quality
    "Marvin Gaye", "Stevie Wonder", "Nina Simone", "Aretha Franklin",
    "D'Angelo", "Erykah Badu", "Hiatus Kaiyote", "Sault",
    "Michael Kiwanuka", "Curtis Harding", "Cleo Sol", "Jorja Smith",

    # Turkish music depth
    "Barış Manço", "Erkin Koray", "Selda Bağcan", "Zülfü Livaneli",
    "Neşet Ertaş", "Aşık Veysel", "Ruhi Su",
    "Mor ve Ötesi", "Duman", "maNga", "Pentagram",
    "Gaye Su Akyol", "Jakuzi", "Altin Gün", "Derya Yıldırım",
    "Baba Zula", "İlhan Erşahin", "Mercan Dede",
    "Fazıl Say", "İdil Biret", "Güher & Süher Pekinel",
    "Sezen Aksu", "Müslüm Gürses", "Zeki Müren",
    "Model", "No Land", "Lalalar", "Turkodiroma",

    # World / Fusion
    "Anouar Brahem", "Tinariwen", "Ali Farka Touré",
    "Ravi Shankar", "Ry Cooder", "Buena Vista Social Club",
    "Rodrigo y Gabriela", "Hermanos Gutiérrez",
    "Ibrahim Maalouf", "Dhafer Youssef",

    # Singer-Songwriter quality
    "Leonard Cohen", "Joni Mitchell", "Bob Dylan",
    "Townes Van Zandt", "Tom Waits", "Phoebe Bridgers",
    "Adrianne Lenker", "Big Thief", "Wye Oak",
    "Damien Rice", "Glen Hansard",

    # Post-rock / Ambient
    "Godspeed You! Black Emperor", "Explosions in the Sky",
    "Mogwai", "This Will Destroy You", "Mono",
    "Brian Eno", "Harold Budd", "Stars of the Lid",

    # Hip Hop — quality/conscious
    "Kendrick Lamar", "J Dilla", "MF DOOM", "Madlib",
    "A Tribe Called Quest", "Nujabes", "Little Simz",

    # Metal — quality/prog
    "Meshuggah", "Gojira", "Between the Buried and Me",
    "Devin Townsend", "Mastodon", "Leprous", "Haken",
]

# ─── API Helpers ──────────────────────────────────────────────────────────────

_last_request_time = 0

def deezer_get(path, params=None):
    """Make a rate-limited Deezer API request."""
    global _last_request_time
    elapsed = time.time() - _last_request_time
    if elapsed < DEEZER_RATE_LIMIT:
        time.sleep(DEEZER_RATE_LIMIT - elapsed)

    url = f"https://api.deezer.com{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    for attempt in range(MAX_RETRIES):
        try:
            req = urllib.request.Request(url)
            req.add_header("Accept-Language", "en")
            with urllib.request.urlopen(req, timeout=15) as resp:
                _last_request_time = time.time()
                data = json.loads(resp.read())
                if "error" in data:
                    if data["error"].get("code") == 4:  # Rate limit
                        print(f"    Rate limited, waiting 5s...")
                        time.sleep(5)
                        continue
                    return None
                return data
        except (urllib.error.HTTPError, urllib.error.URLError, Exception) as e:
            if attempt < MAX_RETRIES - 1:
                time.sleep(2 ** attempt)
            else:
                return None
    return None


def search_track(artist, title):
    """Search for a track on Deezer, return best match or None."""
    # Try exact first
    q = f'artist:"{artist.split(",")[0].strip()}" track:"{title}"'
    data = deezer_get("/search", {"q": q, "limit": 3})
    if data and data.get("data"):
        return data["data"][0]

    # Fallback: simple search
    q = f"{artist.split(',')[0].strip()} {title}"
    data = deezer_get("/search", {"q": q, "limit": 3})
    if data and data.get("data"):
        return data["data"][0]
    return None


def get_track_detail(track_id):
    """Get full track detail from Deezer."""
    return deezer_get(f"/track/{track_id}")


def get_album_detail(album_id):
    """Get album detail (for genre_id)."""
    return deezer_get(f"/album/{album_id}")


def get_artist_detail(artist_id):
    """Get artist detail."""
    return deezer_get(f"/artist/{artist_id}")


def get_artist_top(artist_id, limit=25):
    """Get artist's top tracks."""
    data = deezer_get(f"/artist/{artist_id}/top", {"limit": limit})
    return data.get("data", []) if data else []


def get_artist_related(artist_id, limit=10):
    """Get related artists."""
    data = deezer_get(f"/artist/{artist_id}/related", {"limit": limit})
    return data.get("data", []) if data else []


def search_artist(name):
    """Search for an artist on Deezer."""
    data = deezer_get("/search/artist", {"q": name, "limit": 1})
    if data and data.get("data"):
        return data["data"][0]
    return None


# ─── Cognitive Dimension Computation ─────────────────────────────────────────

def compute_cognitive_labels(track, genre_id=None):
    """Compute 4 cognitive dimension labels from Deezer metadata."""
    bpm = track.get("bpm", 0) or 0
    gain = track.get("gain", -10) or -10
    duration = track.get("duration", 200) or 200
    rank = track.get("rank", 500000) or 500000
    artist_fans = track.get("_artist_fans", 100000) or 100000

    # Normalize BPM (60-200 range)
    bpm_norm = max(0, min(1, (bpm - 60) / 140)) if bpm > 0 else 0.5

    # Normalize gain (-20 to 0 dB, higher = louder)
    gain_norm = max(0, min(1, (gain + 20) / 20))

    # Normalize duration (60-600s range)
    dur_norm = max(0, min(1, (duration - 60) / 540))

    # Normalize rank (0-1M, higher = more popular)
    pop_norm = max(0, min(1, rank / 1000000))

    # Normalize artist fans (log scale)
    fan_norm = max(0, min(1, math.log10(max(artist_fans, 1)) / 7))  # 10M = 1.0

    # Genre biases
    genre_bias = GENRE_COGNITIVE_MAP.get(genre_id, (0.5, 0.5, 0.5, 0.0))

    # ENERGY: BPM + loudness + genre energy
    energy = (
        bpm_norm * 0.35 +
        gain_norm * 0.25 +
        genre_bias[0] * 0.40
    )

    # COMPLEXITY: duration + genre complexity + BPM deviation from center
    bpm_deviation = abs(bpm_norm - 0.5) * 2  # How far from "normal" tempo
    complexity = (
        dur_norm * 0.25 +
        genre_bias[1] * 0.45 +
        bpm_deviation * 0.15 +
        (1 - pop_norm) * 0.15  # Less popular = often more complex
    )

    # DARKNESS: genre mood + loudness (louder often darker in rock/metal)
    darkness = (
        genre_bias[2] * 0.50 +
        gain_norm * 0.20 +
        (1 - pop_norm) * 0.15 +
        0.15 * (0.5 if bpm > 0 and bpm < 90 else 0.3)  # Slow = slightly darker
    )

    # NOVELTY: inverse popularity + inverse artist size + genre novelty boost
    novelty = (
        (1 - pop_norm) * 0.35 +
        (1 - fan_norm) * 0.30 +
        genre_bias[3] * 0.15 +
        0.20 * (0.6 if duration > 360 else 0.4)  # Longer tracks = slightly more novel
    )

    return {
        "energy": round(max(0, min(1, energy)), 3),
        "complexity": round(max(0, min(1, complexity)), 3),
        "darkness": round(max(0, min(1, darkness)), 3),
        "novelty": round(max(0, min(1, novelty)), 3),
    }


# ─── Track Processing ────────────────────────────────────────────────────────

def process_track(search_result, source="unknown", genre_cache=None, artist_cache=None):
    """Process a Deezer search result into a catalog entry."""
    if genre_cache is None:
        genre_cache = {}
    if artist_cache is None:
        artist_cache = {}

    track_id = search_result["id"]

    # Get full track detail
    detail = get_track_detail(track_id)
    if not detail or not detail.get("preview"):
        return None

    # Get album genre
    album_id = detail.get("album", {}).get("id")
    genre_id = None
    genre_name = "Unknown"
    if album_id:
        if album_id in genre_cache:
            genre_id, genre_name = genre_cache[album_id]
        else:
            album = get_album_detail(album_id)
            if album:
                genre_id = album.get("genre_id", 0)
                genres_data = album.get("genres", {}).get("data", [])
                if genres_data:
                    genre_name = genres_data[0].get("name", DEEZER_GENRES.get(genre_id, "Unknown"))
                else:
                    genre_name = DEEZER_GENRES.get(genre_id, "Unknown")
                genre_cache[album_id] = (genre_id, genre_name)

    # Get artist fans
    artist_id = detail.get("artist", {}).get("id")
    artist_fans = 0
    if artist_id:
        if artist_id in artist_cache:
            artist_fans = artist_cache[artist_id]
        else:
            artist = get_artist_detail(artist_id)
            if artist:
                artist_fans = artist.get("nb_fan", 0) or 0
                artist_cache[artist_id] = artist_fans

    # Build entry
    entry = {
        "id": str(track_id),
        "deezer_id": track_id,
        "title": detail.get("title_short", detail.get("title", "")),
        "title_full": detail.get("title", ""),
        "artist": detail.get("artist", {}).get("name", ""),
        "artist_id": artist_id,
        "artist_fans": artist_fans,
        "album": detail.get("album", {}).get("title", ""),
        "album_id": album_id,
        "genre_id": genre_id,
        "genre_name": genre_name,
        "bpm": detail.get("bpm", 0) or 0,
        "gain": detail.get("gain", 0) or 0,
        "duration": detail.get("duration", 0),
        "rank": detail.get("rank", 0) or 0,
        "release_date": detail.get("release_date", ""),
        "isrc": detail.get("isrc", ""),
        "explicit": detail.get("explicit_lyrics", False),
        "preview_url": detail.get("preview", ""),
        "cover_small": detail.get("album", {}).get("cover_small", ""),
        "cover_medium": detail.get("album", {}).get("cover_medium", ""),
        "cover_large": detail.get("album", {}).get("cover_big", ""),
        "cover_xl": detail.get("album", {}).get("cover_xl", ""),
        "deezer_link": detail.get("link", ""),
        "source": source,
        "added_at": datetime.now().isoformat(),
    }

    # Add artist fans for cognitive computation
    entry["_artist_fans"] = artist_fans
    entry["cognitive"] = compute_cognitive_labels(entry, genre_id)
    del entry["_artist_fans"]

    return entry


# ─── Progress Management ─────────────────────────────────────────────────────

def save_progress(phase, data):
    """Save progress to disk for resume capability."""
    progress = {}
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            progress = json.load(f)
    progress[phase] = data
    progress["last_updated"] = datetime.now().isoformat()
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2, ensure_ascii=False)


def load_progress(phase):
    """Load progress from disk."""
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE) as f:
            progress = json.load(f)
            return progress.get(phase)
    return None


# ─── Phase 1: Resolve Seed Playlist ──────────────────────────────────────────

def phase1_resolve_seeds():
    """Resolve all seed tracks on Deezer."""
    print("\n" + "=" * 60)
    print("PHASE 1: Resolving seed playlist tracks on Deezer")
    print("=" * 60)

    cached = load_progress("phase1")
    if cached and len(cached) > 0:
        print(f"  Resuming: {len(cached)} tracks already resolved")
        return cached

    resolved = []
    genre_cache = {}
    artist_cache = {}

    for i, (artist, title) in enumerate(SEED_TRACKS):
        print(f"  [{i+1}/{len(SEED_TRACKS)}] {artist} - {title}...", end=" ", flush=True)
        result = search_track(artist, title)
        if result:
            entry = process_track(result, source="seed_playlist", genre_cache=genre_cache, artist_cache=artist_cache)
            if entry:
                resolved.append(entry)
                print(f"✓ BPM:{entry['bpm']} G:{entry['gain']} {entry['genre_name']}")
            else:
                print("✗ no preview")
        else:
            print("✗ not found")

        # Save progress every 20 tracks
        if (i + 1) % 20 == 0:
            save_progress("phase1", resolved)

    save_progress("phase1", resolved)
    print(f"\n  Resolved: {len(resolved)}/{len(SEED_TRACKS)} seed tracks")
    return resolved


# ─── Phase 2: Analyze Taste DNA ──────────────────────────────────────────────

def phase2_analyze_taste(seeds):
    """Analyze taste DNA from resolved seed tracks."""
    print("\n" + "=" * 60)
    print("PHASE 2: Analyzing taste DNA")
    print("=" * 60)

    # Genre distribution
    genre_counts = Counter(t["genre_name"] for t in seeds if t["genre_name"] != "Unknown")
    total = sum(genre_counts.values())
    genre_dist = {g: round(c / total, 3) for g, c in genre_counts.most_common(20)}

    # BPM statistics
    bpms = [t["bpm"] for t in seeds if t["bpm"] > 0]
    bpm_stats = {
        "mean": round(sum(bpms) / len(bpms), 1) if bpms else 0,
        "min": min(bpms) if bpms else 0,
        "max": max(bpms) if bpms else 0,
        "std": round((sum((b - sum(bpms)/len(bpms))**2 for b in bpms) / len(bpms))**0.5, 1) if bpms else 0,
    }

    # Era distribution
    eras = Counter()
    for t in seeds:
        rd = t.get("release_date", "")
        if rd:
            try:
                year = int(rd[:4])
                decade = f"{(year // 10) * 10}s"
                eras[decade] += 1
            except:
                pass

    # Unique artists
    unique_artists = list(set((t["artist_id"], t["artist"]) for t in seeds))

    # Average cognitive profile
    cog_means = {"energy": 0, "complexity": 0, "darkness": 0, "novelty": 0}
    for t in seeds:
        for k in cog_means:
            cog_means[k] += t["cognitive"][k]
    for k in cog_means:
        cog_means[k] = round(cog_means[k] / len(seeds), 3)

    analysis = {
        "total_seeds": len(seeds),
        "genre_distribution": genre_dist,
        "bpm_stats": bpm_stats,
        "era_distribution": dict(eras.most_common()),
        "unique_artists": len(unique_artists),
        "artist_ids": [a[0] for a in unique_artists],
        "cognitive_centroid": cog_means,
    }

    # Print analysis
    print(f"\n  Genre distribution:")
    for g, p in list(genre_dist.items())[:10]:
        bar = "█" * int(p * 40)
        print(f"    {g:20} {bar} {p:.1%}")

    print(f"\n  BPM: mean={bpm_stats['mean']}, range=[{bpm_stats['min']}-{bpm_stats['max']}], std={bpm_stats['std']}")
    print(f"  Era: {dict(eras.most_common(5))}")
    print(f"  Unique artists: {len(unique_artists)}")
    print(f"  Cognitive centroid: {cog_means}")

    with open(SEED_ANALYSIS_FILE, "w") as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)

    save_progress("phase2", analysis)
    return analysis


# ─── Phase 3: Discover Tracks ────────────────────────────────────────────────

def phase3_discover(seeds, taste):
    """Discover tracks to fill the 5K catalog."""
    print("\n" + "=" * 60)
    print("PHASE 3: Discovering tracks for 5K catalog")
    print("=" * 60)

    # Track dedup by ISRC or (artist_id, title_short)
    seen_isrcs = set()
    seen_keys = set()
    catalog = list(seeds)  # Start with seeds

    for t in catalog:
        if t.get("isrc"):
            seen_isrcs.add(t["isrc"])
        seen_keys.add((t["artist_id"], t["title"].lower()))

    genre_cache = {}
    artist_cache = {}
    processed_artists = set()

    def add_track(entry):
        """Add track to catalog if not duplicate."""
        if not entry or not entry.get("preview_url"):
            return False
        isrc = entry.get("isrc", "")
        key = (entry["artist_id"], entry["title"].lower())
        if isrc and isrc in seen_isrcs:
            return False
        if key in seen_keys:
            return False
        if isrc:
            seen_isrcs.add(isrc)
        seen_keys.add(key)
        catalog.append(entry)
        return True

    def process_artist_tops(artist_id, artist_name, source_tag, limit=20):
        """Get and process top tracks from an artist."""
        if artist_id in processed_artists:
            return 0
        processed_artists.add(artist_id)
        tops = get_artist_top(artist_id, limit=limit)
        added = 0
        for t in tops:
            if len(catalog) >= TARGET_CATALOG_SIZE:
                return added
            entry = process_track(t, source=source_tag, genre_cache=genre_cache, artist_cache=artist_cache)
            if add_track(entry):
                added += 1
        return added

    # ─── 3A: Seed artist top tracks ──────────────────────────────────────
    print(f"\n  3A: Seed artist top tracks...")
    seed_artist_ids = taste["artist_ids"]
    for i, aid in enumerate(seed_artist_ids):
        if len(catalog) >= TARGET_CATALOG_SIZE:
            break
        artist_name = next((t["artist"] for t in seeds if t["artist_id"] == aid), "?")
        added = process_artist_tops(aid, artist_name, "seed_artist_top", limit=20)
        if added > 0:
            print(f"    [{i+1}/{len(seed_artist_ids)}] {artist_name}: +{added} tracks (total: {len(catalog)})")

        # Save progress periodically
        if i % 10 == 0:
            save_progress("phase3_catalog_size", len(catalog))

    print(f"  After 3A: {len(catalog)} tracks")

    # ─── 3B: Related artists from seeds ──────────────────────────────────
    print(f"\n  3B: Related artists from seeds...")
    related_artist_ids = []
    for i, aid in enumerate(seed_artist_ids):
        if len(catalog) >= TARGET_CATALOG_SIZE:
            break
        related = get_artist_related(aid, limit=5)
        for r in related:
            rid = r["id"]
            if rid not in processed_artists:
                related_artist_ids.append((rid, r["name"]))

    # Deduplicate related artists
    seen_related = set()
    unique_related = []
    for rid, rname in related_artist_ids:
        if rid not in seen_related:
            seen_related.add(rid)
            unique_related.append((rid, rname))

    print(f"    Found {len(unique_related)} unique related artists")
    for i, (rid, rname) in enumerate(unique_related):
        if len(catalog) >= TARGET_CATALOG_SIZE:
            break
        added = process_artist_tops(rid, rname, "related_artist", limit=15)
        if added > 0:
            print(f"    [{i+1}/{len(unique_related)}] {rname}: +{added} (total: {len(catalog)})")
        if i % 20 == 0:
            save_progress("phase3_catalog_size", len(catalog))

    print(f"  After 3B: {len(catalog)} tracks")

    # ─── 3C: Curated quality artists ─────────────────────────────────────
    print(f"\n  3C: Curated quality artists...")
    for i, artist_name in enumerate(CURATED_QUALITY_ARTISTS):
        if len(catalog) >= TARGET_CATALOG_SIZE:
            break
        result = search_artist(artist_name)
        if result:
            aid = result["id"]
            added = process_artist_tops(aid, artist_name, "curated_quality", limit=15)
            if added > 0:
                print(f"    [{i+1}/{len(CURATED_QUALITY_ARTISTS)}] {artist_name}: +{added} (total: {len(catalog)})")
        if i % 20 == 0:
            save_progress("phase3_catalog_size", len(catalog))

    print(f"  After 3C: {len(catalog)} tracks")

    # ─── 3D: Genre chart tracks (fill remaining) ─────────────────────────
    if len(catalog) < TARGET_CATALOG_SIZE:
        print(f"\n  3D: Genre chart tracks to fill remaining {TARGET_CATALOG_SIZE - len(catalog)}...")
        chart_genres = [0, 152, 129, 85, 106, 132, 464, 466, 169, 116, 98, 173, 95]
        for gid in chart_genres:
            if len(catalog) >= TARGET_CATALOG_SIZE:
                break
            data = deezer_get(f"/chart/{gid}/tracks", {"limit": 50})
            if data and data.get("data"):
                added = 0
                for t in data["data"]:
                    if len(catalog) >= TARGET_CATALOG_SIZE:
                        break
                    entry = process_track(t, source=f"chart_{DEEZER_GENRES.get(gid, gid)}", genre_cache=genre_cache, artist_cache=artist_cache)
                    if add_track(entry):
                        added += 1
                if added > 0:
                    print(f"    Chart {DEEZER_GENRES.get(gid, gid)}: +{added} (total: {len(catalog)})")

    print(f"\n  Final catalog size: {len(catalog)} tracks")
    return catalog


# ─── Phase 4: Output ─────────────────────────────────────────────────────────

def phase4_output(catalog):
    """Write final catalog to disk."""
    print("\n" + "=" * 60)
    print("PHASE 4: Writing catalog")
    print("=" * 60)

    # Sort by source priority, then rank
    source_priority = {"seed_playlist": 0, "seed_artist_top": 1, "related_artist": 2, "curated_quality": 3}
    catalog.sort(key=lambda t: (source_priority.get(t["source"], 5), -(t.get("rank") or 0)))

    # Stats
    source_counts = Counter(t["source"] for t in catalog)
    genre_counts = Counter(t["genre_name"] for t in catalog)
    has_bpm = sum(1 for t in catalog if t["bpm"] > 0)
    has_preview = sum(1 for t in catalog if t["preview_url"])

    output = {
        "version": "1.0.0",
        "generated_at": datetime.now().isoformat(),
        "total_tracks": len(catalog),
        "stats": {
            "by_source": dict(source_counts.most_common()),
            "by_genre": dict(genre_counts.most_common(20)),
            "has_bpm": has_bpm,
            "has_preview": has_preview,
            "unique_artists": len(set(t["artist_id"] for t in catalog)),
        },
        "tracks": catalog,
    }

    with open(CATALOG_FILE, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n  Written to: {CATALOG_FILE}")
    print(f"  Total tracks: {len(catalog)}")
    print(f"  With preview: {has_preview}")
    print(f"  With BPM: {has_bpm}")
    print(f"  Unique artists: {output['stats']['unique_artists']}")
    print(f"\n  Source breakdown:")
    for src, count in source_counts.most_common():
        print(f"    {src:25} {count:5}")
    print(f"\n  Top genres:")
    for g, count in genre_counts.most_common(10):
        print(f"    {g:25} {count:5}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  M³ CATALOG BUILDER — 5K Track Manifold")
    print(f"  Target: {TARGET_CATALOG_SIZE} tracks")
    print(f"  Output: {CATALOG_FILE}")
    print("=" * 60)

    start = time.time()

    # Phase 1
    seeds = phase1_resolve_seeds()

    # Phase 2
    taste = phase2_analyze_taste(seeds)

    # Phase 3
    catalog = phase3_discover(seeds, taste)

    # Phase 4
    phase4_output(catalog)

    elapsed = time.time() - start
    print(f"\n  Total time: {elapsed/60:.1f} minutes")
    print("  Done! ✓")


if __name__ == "__main__":
    main()
