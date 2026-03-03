import spotipy
import os
from dotenv import load_dotenv
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from data_processor import parse_recently_played_tracks, analyse_tracks
from db import save_recentplays_to_db, fetch_from_db

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


@router.get("/stats/{month}") 
async def get_monthly_data(month:str):
    data = fetch_from_db(month)
    analysed_data = analyse_tracks(data)
    
    token = sp_auth.validate_token(sp_auth.cache_handler.get_cached_token())
    sp = Spotify(auth=token['access_token'])
    
    top_artists = analysed_data['artists']
    artist_ids = [a['artist_id'] for a in top_artists]
    artist_data = sp.artists(artist_ids)
    
    #TO DO: PUT ARITST DATA INTO ANALYSED DATA AND RETURN TO FRONT END TO GET GENRES AND IMAGES!
    #GITHUB ACTIONS
    
    return analysed_data
 
# Function fetches recently played tracks from spotify APi, cleans it and saves it to db. Runs once a day with github actions   
# @router.get("/recent")
# async def root():
#     token = sp_auth.validate_token(sp_auth.cache_handler.get_cached_token())
#     sp = Spotify(auth=token['access_token'])
#     tracks = sp.current_user_recently_played(limit=50, after=None, before=None)
#     cleaned_data = parse_recently_played_tracks(tracks)
#     save_recentplays_to_db(cleaned_data)
    
#     return cleaned_data
    