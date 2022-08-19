import os
import asyncio
import json
import random
import requests
import base64

from spotify.markets import _getRandomMarket

try:
    with open("spotify/config.json", "r") as f:
        config = json.load(f)
        clientSecret = config["clientSecret"]

except FileNotFoundError:
    clientSecret = os.environ["CLIENT_SECRET"]

clientId = "bbefcdeb3d194fd496e110bb93db3af2"
apiUrl = "https://api.spotify.com/v1"
authUrl = "https://accounts.spotify.com/api/token"
token = None

async def _refreshToken():
    global token
    auth = base64.b64encode(bytes(f"{clientId}:{clientSecret}", "ascii")).decode("ascii")
    headers = {"Authorization": f"Basic {auth}"}
    data = {"grant_type": "client_credentials"}

    response = requests.post(authUrl, data=data, headers=headers)
    if response.status_code == 200:
        token = response.json()["access_token"]
        return True


async def _getPlaylist():
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{apiUrl}/browse/featured-playlists?country={await _getRandomMarket()}", headers=headers)
    if response.status_code == 200:
        return random.choice(response.json()["playlists"]["items"])["id"]
    elif response.status_code == 429:
        asyncio.sleep(response.headers["Retry-After"])

    await _refreshToken()
    return await _getPlaylist()

async def getTrack():
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.get(f"{apiUrl}/playlists/{await _getPlaylist()}", headers=headers)
    if response.status_code == 200:
        randomTrack = random.choice(response.json()["tracks"]["items"])["track"]
        return randomTrack["id"]

    elif response.status_code == 429:
        asyncio.sleep(response.headers["Retry-After"])

    await _refreshToken()
    return await getTrack()
