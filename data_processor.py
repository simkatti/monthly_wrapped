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
        
    return 

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

# if __name__ == "__main__":
#     artist_data = [{'external_urls': {'spotify': 'https://open.spotify.com/artist/6wWVKhxIU2cEi0K81v7HvP'}, 'href': 'https://api.spotify.com/v1/artists/6wWVKhxIU2cEi0K81v7HvP', 'id': '6wWVKhxIU2cEi0K81v7HvP', 'images': [{'url': 'https://i.scdn.co/image/ab6761610000e5eb32845b1556f9dbdfe8ee6575', 'height': 640, 'width': 640}, {'url': 'https://i.scdn.co/image/ab6761610000517432845b1556f9dbdfe8ee6575', 'height': 320, 'width': 320}, {'url': 'https://i.scdn.co/image/ab6761610000f17832845b1556f9dbdfe8ee6575', 'height': 160, 'width': 160}], 'name': 'Rammstein', 'type': 'artist', 'uri': 'spotify:artist:6wWVKhxIU2cEi0K81v7HvP'},
#     {'external_urls': {'spotify': 'https://open.spotify.com/artist/5t28BP42x2axFnqOOMg3CM'}, 'href': 'https://api.spotify.com/v1/artists/5t28BP42x2axFnqOOMg3CM', 'id': '5t28BP42x2axFnqOOMg3CM', 'images': [{'url': 'https://i.scdn.co/image/ab6761610000e5eb1e7f796a17c2dc3c28bdeeb9', 'height': 640, 'width': 640}, {'url': 'https://i.scdn.co/image/ab676161000051741e7f796a17c2dc3c28bdeeb9', 'height': 320, 'width': 320}, {'url': 'https://i.scdn.co/image/ab6761610000f1781e7f796a17c2dc3c28bdeeb9', 'height': 160, 'width': 160}], 'name': 'Five Finger Death Punch', 'type': 'artist', 'uri': 'spotify:artist:5t28BP42x2axFnqOOMg3CM'}]
    
#     analysed_data = {'songs': 
#     [{'song_name': 'Carnival of Rust', 'artist_name': 'Poets of the Fall', 'image': 'https://i.scdn.co/image/ab67616d0000b273e5f7b997f1d9a8c3fc4147fc', 'count': 1}, 
#     {'song_name': 'Into The Fire', 'artist_name': 'Thirteen Senses', 'image': 'https://i.scdn.co/image/ab67616d0000b273ba9b3eef6cdc4b5dff0e17ec', 'count': 1}, 
#     {'song_name': 'For You', 'artist_name': 'HIM', 'image': 'https://i.scdn.co/image/ab67616d0000b273c62abeccd25dc4a0003bc754', 'count': 1}, 
#     {'song_name': 'House featuring John Cale', 'artist_name': 'Charli xcx', 'image': 'https://i.scdn.co/image/ab67616d0000b2735048960108f204f627b294b4', 'count': 1}, 
#     {'song_name': 'deep end', 'artist_name': 'Fousheé', 'image': 'https://i.scdn.co/image/ab67616d0000b27308bbdbfb54757bb08d18de46', 'count': 1}, 
#     {'song_name': 'People You Know - sped up to perfection', 'artist_name': 'TommyMuzzic', 'image': 'https://i.scdn.co/image/ab67616d0000b273ad65bda5d4aec2b0ef08c056', 'count': 1}, 
#     {'song_name': '4am', 'artist_name': 'soft siren', 'image': 'https://i.scdn.co/image/ab67616d0000b2733b69697f29a5440abafd21bf', 'count': 1}, 
#     {'song_name': 'Sonne', 'artist_name': 'Rammstein', 'image': 'https://i.scdn.co/image/ab67616d0000b2738b2c42026277efc3e058855b', 'count': 1}, 
#     {'song_name': 'When The Seasons Change', 'artist_name': 'Five Finger Death Punch', 'image': 'https://i.scdn.co/image/ab67616d0000b273fb94cdee49bcfbbefa8400ee', 'count': 1}, 
#     {'song_name': 'Bohemian Rhapsody', 'artist_name': 'Queen', 'image': 'https://i.scdn.co/image/ab67616d0000b273e8b066f70c206551210d902b', 'count': 1}], 

#     'artists': 
#     [{'artist_id': '6wWVKhxIU2cEi0K81v7HvP', 'artist_name': 'Rammstein', 'count': 4}, 
#     {'artist_id': '5t28BP42x2axFnqOOMg3CM', 'artist_name': 'Five Finger Death Punch', 'count': 3}, 
#     {'artist_id': '1AZ30JnvQU1pbX6sbRE0Yn', 'artist_name': 'Poets of the Fall', 'count': 2}, 
#     {'artist_id': '766wIvoqqGrjRDnExOjJls', 'artist_name': 'Thirteen Senses', 'count': 2}, 
#     {'artist_id': '74aLweE8FHHf4yN5TWv1GM', 'artist_name': 'HIM', 'count': 2}, 
#     {'artist_id': '1rKrEdI6GKirxWHxIUPYms', 'artist_name': 'Agnes Obel', 'count': 2}, 
#     {'artist_id': '25uiPmTg16RbhZWAqwLBy5', 'artist_name': 'Charli xcx', 'count': 1}, 
#     {'artist_id': '6trIghKwHRUyxwvm66HLHH', 'artist_name': 'Fousheé', 'count': 1}, 
#     {'artist_id': '2XqXXH9xPa1zucIOtZ3u3A', 'artist_name': 'TommyMuzzic', 'count': 1}, 
#     {'artist_id': '2231C2oqgdZQmJ0vh6bNX2', 'artist_name': 'soft siren', 'count': 1}], 

#     'time_of_day': {'morning': 3, 'afternoon': 15, 'evening': 23, 'night': 0}}
    
#     parse_artist_data(artist_data, analysed_data)