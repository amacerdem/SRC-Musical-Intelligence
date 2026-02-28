"""Spotify OAuth router — login redirect + code-for-token exchange."""
from __future__ import annotations

import os
import urllib.parse

import httpx
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

router = APIRouter()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID", "8be4267057ac4bd69f18e63112a1a92f")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET", "")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:5174/callback")

SCOPES = " ".join([
    "user-top-read",
    "user-read-recently-played",
    "user-read-currently-playing",
    "user-library-read",
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
        "show_dialog": "false",
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
