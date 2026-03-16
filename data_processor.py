from datetime import datetime

def parse_recently_played_tracks(tracks:dict):
    songs = []
    for item in tracks.get('items', []):
        track = item['track']
        
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

def parse_artist_data(artists:list, analysed_data):
    if not artists:
        return
    
    for i, artist in enumerate(artists):
        name = artist['name']
        a_id = artist['id']
        image = artist['images'][0]['url']
        
        if analysed_data['artists'][i]['artist_name'] == name and analysed_data['artists'][i]['artist_id'] == a_id:
            analysed_data['artists'][i]['image'] = image
            
    return analysed_data
        
def analyse_tracks(data):
    if not data:
        return
    stats = {
        "songs": {},
        "artists": {},
        "time_of_day": {"morning": 0, "afternoon":0, "evening": 0, "night": 0},
        "time_slot": "",
        "total_minutes": 0,
        "formatted_time": "",
        "total_artists": 0,
        "total_songs": 0
        
    }
    for current_track in data:
        track_id = current_track['track_id']
        artist_id = current_track['artist_id']
        artist_name = current_track['artist_name']
        song_name = current_track['song_name']
        duration = current_track['duration_ms']
        image = current_track['image']
    
        #counting streams
        if track_id not in stats['songs']:
            stats['songs'][track_id] = {"song_name": song_name, "artist_name": artist_name, "image": image, "count": 1}
        else: 
            stats['songs'][track_id]['count'] += 1
        
        #counting artist streams
        if artist_id not in stats['artists']:
            stats['artists'][artist_id] = {"artist_id": artist_id, "artist_name": artist_name, "count": 1}
        else:
            stats['artists'][artist_id]['count'] += 1
        
        #counting played at times
        hour = current_track['played_at'].hour
        if 5 <= hour < 12:
            stats["time_of_day"]["morning"] += 1
        elif 12 <= hour < 17:
            stats["time_of_day"]["afternoon"] += 1
        elif 17 <= hour < 21:
            stats["time_of_day"]["evening"] += 1
        else:
            stats["time_of_day"]["night"] += 1
        
        #counting total played milliseconds of every track
        stats['total_minutes'] += duration
    
    
    top_time = max(stats['time_of_day'], key=stats['time_of_day'].get)
    if top_time == "morning":
        time_slot = "5 - 12"
    if top_time == "afternoon":
        time_slot = "12 - 17"
    if top_time == "evening":
        time_slot = "17 - 21"
    if top_time == "night":
        time_slot = "21 - 5"
        
        
    ms = stats['total_minutes']
    minutes = int(ms // (1000 * 60))
    days = minutes // 1440
    hours = (minutes % 1440) // 60
    mins = minutes % 60
    
    stats['total_artists'] = len(stats['artists'])
    stats['total_songs'] = len(stats['songs'])
    stats["songs"] = sorted(stats["songs"].values(), key=lambda x: x['count'], reverse=True)[:10]
    stats["artists"] = sorted(stats["artists"].values(), key=lambda x: x['count'], reverse=True)[:10]
    stats['time_of_day'] = top_time
    stats['time_slot'] = time_slot
    stats['total_minutes'] = minutes
    stats['formatted_time'] = f"{days} days, {hours} hours and {mins} minutes."
    
    return stats

# if __name__ == "__main__":

