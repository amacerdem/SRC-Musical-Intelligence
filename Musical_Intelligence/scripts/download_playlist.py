#!/usr/bin/env python3
"""
MI Dataset Downloader
=====================
Fetches track info from Spotify oEmbed API (no auth needed),
searches each on YouTube 1-by-1, downloads as WAV.

Usage:
    python download_playlist.py [--output /workspace/dataset] [--dry-run]
    python download_playlist.py --start 50   # resume from track 50
"""

import argparse
import json
import os
import re
import subprocess
import time
import urllib.request
import urllib.parse

# All 240 Spotify track URLs from the playlist
SPOTIFY_URLS = [
    "https://open.spotify.com/track/3ven4ZKSspshBwiLMMibEa",
    "https://open.spotify.com/track/5URbZBwi9r400J633zdd3h",
    "https://open.spotify.com/track/0uniIrDLtvdypzbMtmLmVV",
    "https://open.spotify.com/track/51WozCH6KrpMsf6MSsftkD",
    "https://open.spotify.com/track/0XRBOfz9bPhjazuQCcRkbJ",
    "https://open.spotify.com/track/1zc0ljXCeDuEffAGeGUm9E",
    "https://open.spotify.com/track/0rjo74cgLBqNKsdXIVzv8b",
    "https://open.spotify.com/track/1JNKHxbYDQ5bkheMuWNlm3",
    "https://open.spotify.com/track/6LsYrrlHQdtelOKWxbK9zC",
    "https://open.spotify.com/track/1vdO8aMVXs3OqGkwEmjA2f",
    "https://open.spotify.com/track/3ygIuLAA3adiAX3aFWvyhL",
    "https://open.spotify.com/track/0zL4fkJauyujzpXKTw3evP",
    "https://open.spotify.com/track/0Otf1ZfYNIjhqFIuJk0fsy",
    "https://open.spotify.com/track/57QU4mbld2ll0kG4d97mcZ",
    "https://open.spotify.com/track/4CZfPaDW5madfScpZl0nDU",
    "https://open.spotify.com/track/4UtpVzyAz6lDuTntjqT2Xm",
    "https://open.spotify.com/track/6J18r0R7rQFuZ4hiRW4P4W",
    "https://open.spotify.com/track/6CDQBADsdzJwc3qZ3OPDHH",
    "https://open.spotify.com/track/0ZrNzEqqf3X24aTVQw0pBA",
    "https://open.spotify.com/track/2UaI54w2AQya4Ff167iy4z",
    "https://open.spotify.com/track/2IVUCvFWLrFmpGuGhZDOfR",
    "https://open.spotify.com/track/1o3zNg0OOR4jmWZqh9xx1p",
    "https://open.spotify.com/track/0E8q2Fx2XuzXCO2NSAppkR",
    "https://open.spotify.com/track/0uPkCpuoERqrkBL06Art50",
    "https://open.spotify.com/track/4rmCI9VWrwrJTJ8XQ80BMN",
    "https://open.spotify.com/track/6cU4urQRUieTBH08yKHAqj",
    "https://open.spotify.com/track/6SdnOecNGBzDgAvNVjJ59w",
    "https://open.spotify.com/track/6cvb3FpCl8mQl9AeB5cAIo",
    "https://open.spotify.com/track/085u91ZVgvjq1wkTg99xMb",
    "https://open.spotify.com/track/1EWLhfX3J2xsJTBxK4GJvc",
    "https://open.spotify.com/track/3dlO9TvGitic6qGxaV0jr3",
    "https://open.spotify.com/track/4C2oMCKWziWp01YSLOBZHU",
    "https://open.spotify.com/track/73ksTxytBZIZ60so20jMYX",
    "https://open.spotify.com/track/1fSdcUDXJwZZBpzaA3dGOv",
    "https://open.spotify.com/track/03yPheflmkbafsI4k4Ghi3",
    "https://open.spotify.com/track/5Dmy8NMxUun0zA4qjVjWtt",
    "https://open.spotify.com/track/0F845nujLVqCb0XMZCh5Pc",
    "https://open.spotify.com/track/2Mb0UmjVuMQ1Pgcyko9dW3",
    "https://open.spotify.com/track/1gF8EnsbcFBaYsNig7LhtN",
    "https://open.spotify.com/track/4otY9Lu5JqAcXoVr9E1txB",
    "https://open.spotify.com/track/5TEbPy96mbPIH31c3XMWBK",
    "https://open.spotify.com/track/2AVxKEmgA30BBrFdson59L",
    "https://open.spotify.com/track/57sKFCABC0VPxj4ZKkcEu7",
    "https://open.spotify.com/track/2gNjmvuQiEd2z9SqyYi8HH",
    "https://open.spotify.com/track/4smkJW6uzoHxGReZqqwHS5",
    "https://open.spotify.com/track/1pZn8AX1WulW8IO338hE5D",
    "https://open.spotify.com/track/6AUn7hXlXsNW6Qf5i39JyZ",
    "https://open.spotify.com/track/2x91iJc0UkFcjRMEZ2CoWB",
    "https://open.spotify.com/track/45chgWEwD5M58JBeoeDTnL",
    "https://open.spotify.com/track/03IckTW2qNaWUvrOHtuYhL",
    "https://open.spotify.com/track/6cNsewEICKlNmFT8q3i4b9",
    "https://open.spotify.com/track/1VSQ0KbNTzJvumUk1ubKAY",
    "https://open.spotify.com/track/5fHVpGBodIcXkWlZcjFaj3",
    "https://open.spotify.com/track/4Vkk3iD1VrENHJEACNddvt",
    "https://open.spotify.com/track/4nrQ0ohqu5sXqMg2p4YzkE",
    "https://open.spotify.com/track/3iFlfQ0CXc9URaAvai8VUe",
    "https://open.spotify.com/track/3zIuHdD8dkh1vPxQu334T7",
    "https://open.spotify.com/track/6F1LNg9NcMUqn18Qgu5Jig",
    "https://open.spotify.com/track/7KjGqnLxaJeaSMUZ54DT34",
    "https://open.spotify.com/track/3xb80d9UHrlvl1Ylth8ild",
    "https://open.spotify.com/track/7p6ZeiNtEHJKmc4YWBZELG",
    "https://open.spotify.com/track/1IMHjO3dsAs1SJdmJVlRpq",
    "https://open.spotify.com/track/3NU7cjHO8eqqgvuEW6rDqU",
    "https://open.spotify.com/track/0JDQOo5gYr3lHD4YDqoYMy",
    "https://open.spotify.com/track/16KcymBpArhp5P2ALmELhn",
    "https://open.spotify.com/track/1430Rx277OpkpmTrm6ddCh",
    "https://open.spotify.com/track/0iGm2b1H764OMusrcRaTCG",
    "https://open.spotify.com/track/4dicW3vv5BFHi0RQGXRkc6",
    "https://open.spotify.com/track/2W58kBLhWH1HFaUCukfCdE",
    "https://open.spotify.com/track/791XP1Sj2BCsf2CYTYje5h",
    "https://open.spotify.com/track/2Xtsv7BUMrNodQWH2JPOc0",
    "https://open.spotify.com/track/6Rqn2GFlmvmV4w9Ala0I1e",
    "https://open.spotify.com/track/0v0oL77zDnGTdRwB2q6OIm",
    "https://open.spotify.com/track/4rfh0qEv1HdKRXWiRXfzWF",
    "https://open.spotify.com/track/2Wi5ubKr8zSk8L3CLemyS4",
    "https://open.spotify.com/track/648TTtYB0bH0P8Hfy0FmkL",
    "https://open.spotify.com/track/4QxDOjgpYtQDxxbWPuEJOy",
    "https://open.spotify.com/track/1bbqHoPIr5qHUBcTq6i3NZ",
    "https://open.spotify.com/track/5twNVE0ofszyWolOWwjRSN",
    "https://open.spotify.com/track/1V43BO81I2LLHjy25en933",
    "https://open.spotify.com/track/5YIhyj0uiGSJPLARP7nzte",
    "https://open.spotify.com/track/3ZQ6bCWYPgX7SqZ5AVeKOm",
    "https://open.spotify.com/track/1OtISG0K02k06m1BENey4H",
    "https://open.spotify.com/track/1CDBaGlisZlOJzvx88lL8A",
    "https://open.spotify.com/track/1qHrF4XOI6Pliy7atNjLds",
    "https://open.spotify.com/track/1sce5VJvCOYYDAR9rp9KdG",
    "https://open.spotify.com/track/1BWsQm7kOBjK2aSFYg5HQZ",
    "https://open.spotify.com/track/4LiSdLjUXbS4daVzBJCTwH",
    "https://open.spotify.com/track/3XckH9nZTF2Y2gp6UoMotk",
    "https://open.spotify.com/track/6C1gzKLL8ESwc3wYqSD6IV",
    "https://open.spotify.com/track/1MglqgabKH4iSkw8xHJ0J9",
    "https://open.spotify.com/track/68d6ZfyMUYURol2y15Ta2Y",
    "https://open.spotify.com/track/7uPARjX8n4Sf4ndZ9alTxk",
    "https://open.spotify.com/track/19vVghIuHm3IAfN4xpRF3q",
    "https://open.spotify.com/track/4OzXE9NnSdD9aEAwBcnYBI",
    "https://open.spotify.com/track/6PtZaHjsx2Pnk3x9O92bB2",
    "https://open.spotify.com/track/0kUYnVS6z9YhL22l9pDDcB",
    "https://open.spotify.com/track/6YYu8qFzcY1ZyzzsJIQM12",
    "https://open.spotify.com/track/16nJl8NnriCJxraco5Zssm",
    "https://open.spotify.com/track/2JITVZu8o6ls9k8SoMRy7w",
    "https://open.spotify.com/track/5rQTh8OF3mfjgu0NJkSTOk",
    "https://open.spotify.com/track/3OgEs9t1SIkpKddOsJlmeH",
    "https://open.spotify.com/track/5DDx7lVobjWfLyvRDtW7BX",
    "https://open.spotify.com/track/4P1TebwKnny3sDFsdieibP",
    "https://open.spotify.com/track/5FBf12F4ry9TXoZAvISu6F",
    "https://open.spotify.com/track/3KUSSxjujFcEGhnsm0qeDo",
    "https://open.spotify.com/track/2IdwQxhJn9ZE4zIotcCefR",
    "https://open.spotify.com/track/1kPBT8S2wJFNAyBMnGVZgL",
    "https://open.spotify.com/track/5QC07jdKdQrH1cW7Ag3OJ2",
    "https://open.spotify.com/track/0sjxRg1VlYfx4YG7uxurrq",
    "https://open.spotify.com/track/1ukZalnC6GmPFUDduB6slb",
    "https://open.spotify.com/track/2QHFSR7VUZZfRRwZycKqSa",
    "https://open.spotify.com/track/0RNxWy0PC3AyH4ThH3aGK6",
    "https://open.spotify.com/track/0gCUGnwXiNOHV3KsUxRHuC",
    "https://open.spotify.com/track/1YQWosTIljIvxAgHWTp7KP",
    "https://open.spotify.com/track/3XiFWZoHQtGUYIdtShPwPD",
    "https://open.spotify.com/track/7yED4n2U8RR5LKZVmisiev",
    "https://open.spotify.com/track/5cdBPBfYeRFDZWHAk4UPOH",
    "https://open.spotify.com/track/3Y0LpU5kqQ3vSZvwcGjl1M",
    "https://open.spotify.com/track/0f6Fb3g0DRpCIbhljotYwO",
    "https://open.spotify.com/track/1COHEDYb0h68iDbpjjtfMh",
    "https://open.spotify.com/track/7iORcAVUGZcLA7Iq60K092",
    "https://open.spotify.com/track/06DLt3XsB90lr1yx2kgzQx",
    "https://open.spotify.com/track/3eRAy175Rq7MnVSkgUc1cF",
    "https://open.spotify.com/track/27UPhXYh5M9XoDCeGmZz5J",
    "https://open.spotify.com/track/1QCUrXrY1qlxRhL3a9LYCA",
    "https://open.spotify.com/track/10W125nMbncRGcXRBoACOx",
    "https://open.spotify.com/track/2PcbVKT28p9mOlWBDL371J",
    "https://open.spotify.com/track/5DVVraKICbh1sNNEf8oXh0",
    "https://open.spotify.com/track/47lyo8lCnZAilzcqywusfK",
    "https://open.spotify.com/track/2HUZVffVPXvqnrml0gXggp",
    "https://open.spotify.com/track/0MkINaEoNBJfG9G6ewd4xM",
    "https://open.spotify.com/track/10HdfEE0sausAJu8HJD3Dp",
    "https://open.spotify.com/track/5IMCtjbZEd5L22AeRNC4FI",
    "https://open.spotify.com/track/6YJmV1VRtTxNZUFkDEQE3H",
    "https://open.spotify.com/track/0LYNu9Y9y0XahxyhdMJU2f",
    "https://open.spotify.com/track/1oH53mBZ9LmVF70SZJaxfM",
    "https://open.spotify.com/track/67rN3fFGWcwA5MGxw9mxk6",
    "https://open.spotify.com/track/1MquE8f6XYztVU7RsNRCBX",
    "https://open.spotify.com/track/4RPdeuPph5G6byLEzH9SYS",
    "https://open.spotify.com/track/1oWlt7O00nEndJniJMVEL6",
    "https://open.spotify.com/track/0GIngB5wcmy9yy6G02FiPO",
    "https://open.spotify.com/track/0p5zJBYoJOzVLBiDeA0PvS",
    "https://open.spotify.com/track/0EzykG4pYlmmGTihakWGRL",
    "https://open.spotify.com/track/2P9nh9pTK96dE0b6NBbTSs",
    "https://open.spotify.com/track/6SVdBlIXlYwqcbYZSfjJjy",
    "https://open.spotify.com/track/4YEoVkvvzx5eavtE2u5qG0",
    "https://open.spotify.com/track/09CQq9gQkHaeHfWJr0BaIW",
    "https://open.spotify.com/track/2LtpyfWWnr5V96l3Js7LLX",
    "https://open.spotify.com/track/281GVQAmCh70dfZaQITA2J",
    "https://open.spotify.com/track/2En6kxGCjZxXmKJ1IYu4Fp",
    "https://open.spotify.com/track/7E25omG6JvGlMnfkJdzLwP",
    "https://open.spotify.com/track/0u5DqebxtjYVxQo45xZQU8",
    "https://open.spotify.com/track/4YeuU02HLkvaPPfZlr1hwj",
    "https://open.spotify.com/track/3hGI1BYBnRT2OJ93mIxMX1",
    "https://open.spotify.com/track/62mtesBLb4DRnaESQ8Z2El",
    "https://open.spotify.com/track/5dAoQMVA2jwl1hCTJGeWAm",
    "https://open.spotify.com/track/5RmP7cOkIx2X6DWtTtMuC9",
    "https://open.spotify.com/track/1vIhT2dq49lvpJtsdppmqd",
    "https://open.spotify.com/track/4uIgSgz3oEOV925RfEPfFm",
    "https://open.spotify.com/track/0POgVAMoMUevxeS8ikXjDj",
    "https://open.spotify.com/track/0ESNFiz1ATKj4fQyqJHmhE",
    "https://open.spotify.com/track/7Bmo1L24zfcPK54Jkv0nmg",
    "https://open.spotify.com/track/1LKN5pN5RyB9NCdE7ANvMN",
    "https://open.spotify.com/track/2GOztq545KfhVtznk79MXP",
    "https://open.spotify.com/track/3XdR9Ndao3nucK2R6eb0ba",
    "https://open.spotify.com/track/4BIZpevfE9KRsGahLJJuVR",
    "https://open.spotify.com/track/7vpFJxTz52UkZtLthSxrJC",
    "https://open.spotify.com/track/5V3FhP8RIUCP50UzRXCcWM",
    "https://open.spotify.com/track/3wNoUzJUNXCuoHPj2dQ8DF",
    "https://open.spotify.com/track/3VugbJNiapiakQGLV1vzuf",
    "https://open.spotify.com/track/1lr94UMkc49eWESjcSOwbM",
    "https://open.spotify.com/track/4h0eGqOADntcHwrS7PwSZL",
    "https://open.spotify.com/track/5bC6ONDsL88snGN6QasjZH",
    "https://open.spotify.com/track/1cRTAPP2FG9h2WiYMOIVIK",
    "https://open.spotify.com/track/760clbeDBWmBsBLbszWuNZ",
    "https://open.spotify.com/track/7lbC5pd1ahrDiIf9gLUhxx",
    "https://open.spotify.com/track/1TkliUZNnCeTjZMWPuUoPK",
    "https://open.spotify.com/track/73GEVn1tqk9bn0KbtWsiqj",
    "https://open.spotify.com/track/4SP7Fdwo42okQx8dzWJYjM",
    "https://open.spotify.com/track/1TVtYIucWI5fqdQwwlZFR3",
    "https://open.spotify.com/track/3oRmL7VDUQu8EC16vFNAnL",
    "https://open.spotify.com/track/1pPrO5Lcx9UXNebcloGeHE",
    "https://open.spotify.com/track/4NQfrmGs9iQXVQI9IpRhjM",
    "https://open.spotify.com/track/4DIg6Cu5kWVQA3KO2NQpAM",
    "https://open.spotify.com/track/6ZfSXhqojBGB8BdRFb96Im",
    "https://open.spotify.com/track/2v2XfuQHfRO5jQcKlXVAF5",
    "https://open.spotify.com/track/7EVfyWoxyraAp1rRmuHpV7",
    "https://open.spotify.com/track/66yWyjOGuhsXyGu57unL6B",
    "https://open.spotify.com/track/3uU5htjPpaRaPanmQd320D",
    "https://open.spotify.com/track/0ay8PHNPCP2dmplYOtUJvI",
    "https://open.spotify.com/track/3FIYut05URo0hstrgt5mzI",
    "https://open.spotify.com/track/5PMQGNqd29GaWCX1VqMzGv",
    "https://open.spotify.com/track/6C1kAco7qDQYjFGK3B5xvU",
    "https://open.spotify.com/track/0WatYyA7vSnaA7ShN4rx75",
    "https://open.spotify.com/track/2AxC0hBTjAslD0sZAywCzU",
    "https://open.spotify.com/track/7vJaNv4ItDyYXXCVRJreh6",
    "https://open.spotify.com/track/2dacKJVYe7xsAcUrkOCSHL",
    "https://open.spotify.com/track/3q7em8kVHiHpZbKQuVYwFQ",
    "https://open.spotify.com/track/0oZyonhhYOv2FSnqGpi69j",
    "https://open.spotify.com/track/7oxSfM3FXCdw7EXNreNoRz",
    "https://open.spotify.com/track/4MqFHxNM8uM7UEW4t56nzU",
    "https://open.spotify.com/track/6qnqmducagZ5wljSLYrVoI",
    "https://open.spotify.com/track/1ZBsdS9S7ZItIj6x6a6cNG",
    "https://open.spotify.com/track/4zoQ3EqopTIGmK2c2rPV5t",
    "https://open.spotify.com/track/3XxBSvDZKH5YvZZjTpn6eR",
    "https://open.spotify.com/track/3AaXHBFpwXWmtg3kcfuwhQ",
    "https://open.spotify.com/track/2wnjZXcAT3rCjjqxLeHjv7",
    "https://open.spotify.com/track/1vkEVT81wJQtMZ23FJ1q1i",
    "https://open.spotify.com/track/3ocm1Cf1Dk1ODrdBdybh82",
    "https://open.spotify.com/track/1VFoA9FU8IXhMKFYuFDCsp",
    "https://open.spotify.com/track/6AQSNvOSgW4m3LVJcUSdrB",
    "https://open.spotify.com/track/302TFw9xPEEwflzVvAA4w6",
    "https://open.spotify.com/track/7mW3XmWeDUo02M4GbO0fiC",
    "https://open.spotify.com/track/5SbzJktq4z4iBVkdtYiYly",
    "https://open.spotify.com/track/1huWqmpiYksaPppQHLDhZP",
    "https://open.spotify.com/track/1atDSd7gy75YurFKnV7ykE",
    "https://open.spotify.com/track/5TjuQd2TgP2zQrEZdoCM2S",
    "https://open.spotify.com/track/59yPRAZPquxQdc21gIJ74x",
    "https://open.spotify.com/track/08U6LbPuPqNaWVXttHqkIo",
    "https://open.spotify.com/track/4dgJDo6kvaSv8e1jmsNAY3",
    "https://open.spotify.com/track/7KWJCQbkB0nnE3xO61Higj",
    "https://open.spotify.com/track/7zVZF0OgDJkFJohnlKwEpa",
    "https://open.spotify.com/track/2ROJOb98GorxStuOuZWcGd",
    "https://open.spotify.com/track/3E0VKSvZp76kvBU2WwwBul",
    "https://open.spotify.com/track/2vY3XKWiQ3gb4o0aXRtHjY",
    "https://open.spotify.com/track/6PUabSMXmPnZna361Wwmf7",
    "https://open.spotify.com/track/7cmrFR3BkvK4VlKjZqupLt",
    "https://open.spotify.com/track/4Ik2wOwtDwrCPfd357h4td",
    "https://open.spotify.com/track/3BAEZbpWPNKcryHnysOPqH",
    "https://open.spotify.com/track/5YcsVvdguZVU10TFO17duz",
    "https://open.spotify.com/track/6vl5ybe1Pc0ij64jTCQHWj",
    "https://open.spotify.com/track/4xxo9sAIeVTKIvs0iehYqG",
    "https://open.spotify.com/track/6nF41yFBkDcx1BYJqtj8Na",
    "https://open.spotify.com/track/0GkM9T6C7nzkgWUbK7E2cd",
    "https://open.spotify.com/track/4qTmr1QcPZNzj06rf0GA92",
    "https://open.spotify.com/track/1h80qNOdawNexSq9eloW4t",
    "https://open.spotify.com/track/2FN1mSfq7Kwk5VITuIOwyR",
    "https://open.spotify.com/track/7bDhB3KoyV3ouue0BhtIjv",
    "https://open.spotify.com/track/3TLHIqYpEdtjivr3IN1dMB",
]


def fetch_track_info(spotify_url):
    """Get track title from Spotify oEmbed API (no auth needed)."""
    oembed_url = f"https://open.spotify.com/oembed?url={urllib.parse.quote(spotify_url, safe='')}"
    req = urllib.request.Request(
        oembed_url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; MIBot/1.0)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            # oEmbed returns: {"title": "Song Name by Artist Name", ...}
            title = data.get("title", "")
            return title
    except Exception as e:
        print(f"    oEmbed error: {e}")
        return None


def resolve_all_tracks(urls):
    """Resolve all Spotify URLs to artist - title via oEmbed."""
    tracks = []
    cache_path = "/tmp/spotify_tracks_cache.json"

    # Load cache if exists
    cache = {}
    if os.path.exists(cache_path):
        with open(cache_path) as f:
            cache = json.load(f)

    for i, url in enumerate(urls, 1):
        track_id = url.split("/")[-1]

        if track_id in cache:
            tracks.append(cache[track_id])
            continue

        print(f"  [{i:3d}/{len(urls)}] Resolving: {track_id}", end="", flush=True)
        title = fetch_track_info(url)

        if title:
            # oEmbed title format: "Song Name by Artist Name"
            # Parse it
            if " by " in title:
                parts = title.rsplit(" by ", 1)
                track = {"title": parts[0].strip(), "artist": parts[1].strip(), "spotify_url": url}
            else:
                track = {"title": title, "artist": "", "spotify_url": url}
            tracks.append(track)
            cache[track_id] = track
            print(f" -> {track['artist']} - {track['title']}")
        else:
            tracks.append({"title": f"unknown_{track_id}", "artist": "", "spotify_url": url})
            print(f" -> FAILED")

        # Save cache after each resolve
        with open(cache_path, "w") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)

        # Small delay to avoid rate limiting
        time.sleep(0.3)

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


def download_track(url, output_path, fmt="wav"):
    """Download a single track from YouTube."""
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "-x",
                "--audio-format", fmt,
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
        print(f"    TIMEOUT")
        return False


def main():
    parser = argparse.ArgumentParser(description="MI Dataset Downloader")
    parser.add_argument("--output", default="/workspace/dataset", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Only list tracks, don't download")
    parser.add_argument("--start", type=int, default=1, help="Start from track N (1-indexed)")
    parser.add_argument("--format", default="wav", choices=["wav", "mp3", "flac"], help="Audio format")
    args = parser.parse_args()

    # Step 1: Resolve all Spotify URLs to track names
    print(f"[1/3] Resolving {len(SPOTIFY_URLS)} Spotify track URLs via oEmbed...\n")
    tracks = resolve_all_tracks(SPOTIFY_URLS)
    print(f"\n  Resolved {len(tracks)} tracks\n")

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

        query = f"{track['artist']} - {track['title']}" if track['artist'] else track['title']
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', query)[:200]
        output_file = os.path.join(args.output, f"{safe_name}.{args.format}")

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
        ok = download_track(url, output_file, args.format)
        if ok:
            success += 1
            downloaded[safe_name] = {
                "url": url,
                "query": query,
                "idx": i,
                "spotify": track.get("spotify_url", ""),
            }
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
        failed_path = os.path.join(args.output, "failed_tracks.txt")
        with open(failed_path, "w") as f:
            f.write("\n".join(failed))
        print(f"\n  Failed list saved to: {failed_path}")


if __name__ == "__main__":
    main()
