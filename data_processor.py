from datetime import datetime

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
            'artist_name': track['artists'][0]['name'],
            'played_at': item['played_at'],
            'image': track['album']['images'][0]['url'],
            'duration_ms': track['duration_ms'],
            }
            songs.append(song)            
        
    return songs
        
def analyse_tracks(data):
    if not data:
        return
    stats = {
        "songs": {},
        "artists": {},
        "time_of_day": {"morning": 0, "afternoon":0, "evening": 0, "night": 0}
    }
    for i in range(len(data)):
        current_track = data[i]
        
        track_id = current_track['track_id']
        artist_id = current_track['artist_id']
        artist_name = current_track['artist_name']
        song_name = current_track['song_name']
        duration = current_track['duration_ms']
        image = current_track['image']
    
        if track_id not in stats['songs']:
            stats['songs'][track_id] = {"song_name": song_name, "artist_name": artist_name, "image": image, "count": 1}
        else: 
            stats['songs'][track_id]['count'] += 1
            
        if artist_id not in stats['artists']:
            stats['artists'][artist_id] = {"artist_id": artist_id, "artist_name": artist_name, "count": 1}
        else:
            stats['artists'][artist_id]['count'] += 1
            
        hour = current_track['played_at'].hour
        if 5 <= hour < 12:
            stats["time_of_day"]["morning"] += 1
        elif 12 <= hour < 17:
            stats["time_of_day"]["afternoon"] += 1
        elif 17 <= hour < 21:
            stats["time_of_day"]["evening"] += 1
        else:
            stats["time_of_day"]["night"] += 1
            
    stats["songs"] = sorted(stats["songs"].values(), key=lambda x: x['count'], reverse=True)[:10]
    stats["artists"] = sorted(stats["artists"].values(), key=lambda x: x['count'], reverse=True)[:10]
    return stats