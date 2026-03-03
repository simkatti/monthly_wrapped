import os
from dotenv import load_dotenv
from spotify_client import sp_auth, Spotify
from data_processor import parse_recently_played_tracks
from db import save_recentplays_to_db

def run_job():
    token = sp_auth.validate_token(sp_auth.cache_handler.get_cached_token())
    sp = Spotify(auth=token['access_token'])
    tracks = sp.current_user_recently_played(limit=50, after=None, before=None)
    cleaned_data = parse_recently_played_tracks(tracks)
    if cleaned_data:
        save_recentplays_to_db(cleaned_data)
        
if __name__ == "__main__":
    run_job()