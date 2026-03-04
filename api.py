from spotify_client import sp_auth
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from data_processor import analyse_tracks, parse_artist_data
from db import fetch_from_db

router = APIRouter()

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


@router.get("/stats/{month}") 
async def get_monthly_data(month:str):
    data = fetch_from_db(month)
    analysed_data = analyse_tracks(data)
    
    cached_token = sp_auth.cache_handler.get_cached_token()
    token = sp_auth.validate_token(cached_token)
    if not token: 
        return {"error": "Token is not valid"}
    sp = Spotify(auth=token['access_token'])
    top_artists = analysed_data['artists']
    artist_ids = [a['artist_id'] for a in top_artists]
    artist_data = [sp.artist(a_id) for a_id in artist_ids]
    if artist_data:
        final_data = parse_artist_data(artist_data,analysed_data)

    return final_data
 