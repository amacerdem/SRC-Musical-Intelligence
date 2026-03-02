"""Spotify OAuth router — login, exchange, and MI profile computation."""
from __future__ import annotations

import asyncio
import os
import urllib.parse
from typing import Any

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

from ..spotify_mi_bridge import compute_user_profile

router = APIRouter()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "8be4267057ac4bd69f18e63112a1a92f")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5174/callback")

SCOPES = " ".join([
    "user-top-read",
    "user-read-recently-played",
    "user-read-currently-playing",
    "user-library-read",
    "user-read-playback-state",
    "user-modify-playback-state",
    "playlist-read-private",
])


@router.get("/login")
async def spotify_login():
    """Redirect user to Spotify authorization page."""
    if not SPOTIFY_CLIENT_SECRET:
        raise HTTPException(503, "SPOTIFY_CLIENT_SECRET not configured in .env")

    params = urllib.parse.urlencode({
        "client_id": SPOTIFY_CLIENT_ID,
        "response_type": "code",
        "redirect_uri": SPOTIFY_REDIRECT_URI,
        "scope": SCOPES,
        "show_dialog": "true",
    })
    return RedirectResponse(f"https://accounts.spotify.com/authorize?{params}")


class ExchangeRequest(BaseModel):
    code: str


@router.post("/exchange")
async def spotify_exchange(body: ExchangeRequest):
    """Exchange authorization code for access + refresh tokens."""
    if not SPOTIFY_CLIENT_SECRET:
        raise HTTPException(503, "SPOTIFY_CLIENT_SECRET not configured in .env")

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://accounts.spotify.com/api/token",
            data={
                "grant_type": "authorization_code",
                "code": body.code,
                "redirect_uri": SPOTIFY_REDIRECT_URI,
                "client_id": SPOTIFY_CLIENT_ID,
                "client_secret": SPOTIFY_CLIENT_SECRET,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )

    if resp.status_code != 200:
        detail = resp.json().get("error_description", resp.text)
        raise HTTPException(resp.status_code, f"Spotify token exchange failed: {detail}")

    data = resp.json()
    return {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token"),
        "expires_in": data.get("expires_in", 3600),
        "token_type": data.get("token_type", "Bearer"),
    }


# ── Spotify → MI Profile ─────────────────────────────────────────────

SPOTIFY_API = "https://api.spotify.com/v1"


class ProfileRequest(BaseModel):
    access_token: str


async def _sp_get(
    client: httpx.AsyncClient, path: str, token: str
) -> dict[str, Any]:
    """GET from Spotify API, return JSON or empty dict on error."""
    resp = await client.get(
        f"{SPOTIFY_API}{path}",
        headers={"Authorization": f"Bearer {token}"},
    )
    if resp.status_code != 200:
        return {}
    return resp.json()


async def _sp_get_audio_features(
    client: httpx.AsyncClient, ids: list[str], token: str
) -> dict[str, dict[str, float]]:
    """Try to fetch audio features; return empty dict on 403/error."""
    if not ids:
        return {}
    # Batch in chunks of 100 (Spotify limit)
    result: dict[str, dict[str, float]] = {}
    for i in range(0, len(ids), 100):
        chunk = ids[i : i + 100]
        resp = await client.get(
            f"{SPOTIFY_API}/audio-features?ids={','.join(chunk)}",
            headers={"Authorization": f"Bearer {token}"},
        )
        if resp.status_code != 200:
            return {}  # audio features endpoint blocked
        data = resp.json()
        for af in data.get("audio_features", []):
            if af and af.get("id"):
                result[af["id"]] = af
    return result


@router.post("/profile")
async def spotify_profile(body: ProfileRequest):
    """Fetch user's Spotify library and compute MI profile.

    Returns genes(5D), dimensions(6D/12D/24D), persona, family distribution,
    and per-track MI features for all fetched tracks.
    """
    token = body.access_token

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Fetch everything in parallel
        (
            me_data,
            top_artists_short,
            top_artists_medium,
            top_artists_long,
            top_tracks_short,
            top_tracks_medium,
            top_tracks_long,
            recent_data,
            saved_data,
        ) = await asyncio.gather(
            _sp_get(client, "/me", token),
            _sp_get(client, "/me/top/artists?time_range=short_term&limit=50", token),
            _sp_get(client, "/me/top/artists?time_range=medium_term&limit=50", token),
            _sp_get(client, "/me/top/artists?time_range=long_term&limit=50", token),
            _sp_get(client, "/me/top/tracks?time_range=short_term&limit=50", token),
            _sp_get(client, "/me/top/tracks?time_range=medium_term&limit=50", token),
            _sp_get(client, "/me/top/tracks?time_range=long_term&limit=50", token),
            _sp_get(client, "/me/player/recently-played?limit=50", token),
            _sp_get(client, "/me/tracks?limit=50", token),
        )

        # Build artist list with genres
        all_artists: dict[str, dict[str, Any]] = {}
        for src in (top_artists_short, top_artists_medium, top_artists_long):
            for a in src.get("items", []):
                all_artists[a["id"]] = {
                    "id": a["id"],
                    "name": a.get("name", ""),
                    "genres": a.get("genres", []),
                    "popularity": a.get("popularity", 0),
                }

        # Build artist name → genres lookup
        artist_name_genres: dict[str, list[str]] = {}
        for a in all_artists.values():
            artist_name_genres[a["name"].lower()] = a["genres"]

        # Collect unique tracks
        seen_ids: set[str] = set()
        all_tracks: list[dict[str, Any]] = []

        def _add_tracks(items: list[dict], tag: str) -> None:
            for item in items:
                track = item.get("track", item)
                tid = track.get("id")
                if not tid or tid in seen_ids:
                    continue
                seen_ids.add(tid)
                artist_name = track["artists"][0]["name"] if track.get("artists") else ""
                genres = artist_name_genres.get(artist_name.lower(), [])
                all_tracks.append({
                    "id": tid,
                    "name": track.get("name", ""),
                    "artist": artist_name,
                    "album_art": (track.get("album", {}).get("images", [{}])[0].get("url", "")),
                    "duration_ms": track.get("duration_ms", 0),
                    "genres": genres,
                    "audio_features": None,  # filled below
                    "tag": tag,
                })

        _add_tracks(top_tracks_short.get("items", []), "top_short")
        _add_tracks(top_tracks_medium.get("items", []), "top_medium")
        _add_tracks(top_tracks_long.get("items", []), "top_long")
        _add_tracks(recent_data.get("items", []), "recent")
        _add_tracks(saved_data.get("items", []), "saved")

        # Try fetching audio features
        track_ids = [t["id"] for t in all_tracks if t["id"]]
        af_map = await _sp_get_audio_features(client, track_ids, token)

    # Attach audio features to tracks
    for t in all_tracks:
        t["audio_features"] = af_map.get(t["id"])

    # Build Spotify user info
    spotify_user = {
        "id": me_data.get("id", ""),
        "display_name": me_data.get("display_name", ""),
        "product": me_data.get("product", "free"),
    }

    # Compute MI profile via bridge
    profile = compute_user_profile(
        tracks=all_tracks,
        artists=list(all_artists.values()),
        spotify_user=spotify_user,
    )

    return profile
