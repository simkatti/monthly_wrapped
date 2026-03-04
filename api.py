from spotify_client import sp_auth
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from data_processor import parse_recently_played_tracks, analyse_tracks
from db import save_recentplays_to_db, fetch_from_db

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
        return {"error": "No valid token. Visit /login"}
    sp = Spotify(auth=token['access_token'])
    try:
        top_artists = analysed_data['artists']
        artist_ids = [a['artist_id'] for a in top_artists]
        artist_data = sp.artists(artist_ids)
    except Exception as e:
        print(f"DEBUG: Spotify API Error: {e}")
        return {"error": str(e)}
    
    #TO DO: PUT ARITST DATA INTO ANALYSED DATA AND RETURN TO FRONT END TO GET GENRES AND IMAGES!
    #GITHUB ACTIONS
    
    return analysed_data
 