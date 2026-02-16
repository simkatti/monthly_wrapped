import spotipy
import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from data_processor import parse_recently_played_tracks

load_dotenv()
router = APIRouter()


sp_auth=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-read-recently-played"
    )


@router.get("/login")
async def login():
    auth_url = sp_auth.get_authorize_url()
    return {"login_url": auth_url}

@router.get("/callback")
async def callback(code:str):
    token = sp_auth.get_access_token(code)
    if token:
        return RedirectResponse("http://localhost:8501")
    else:
        return {"authorisation failed"}

@router.get("/recent")
async def root():
    token = sp_auth.validate_token(sp_auth.cache_handler.get_cached_token())
    sp = Spotify(auth=token['access_token'])
    tracks = sp.current_user_recently_played(limit=50, after=None, before=None)
    cleaned_data = parse_recently_played_tracks(tracks)
    
    return cleaned_data
    
