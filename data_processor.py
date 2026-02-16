def parse_recently_played_tracks(tracks:dict):
    songs = []
    track_ids = set()
    for item in tracks.get('items', []):
        track = item['track']
        
        if track['id'] not in track_ids:
            track_ids.add(track['id'])
        
            song = {
            'track_id': track['id'],
            'artist_id': track['artists'][0]['id'],
            'song_name': track['name'],
            'artist': track['artists'][0]['name'],
            'played_at': item['played_at'],
            'image': track['album']['images'][0]['url'],
            'duration': track['duration_ms'],
            }
            songs.append(song)
            
        
    return songs
        
        