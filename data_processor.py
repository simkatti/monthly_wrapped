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

if __name__ == "__main__":
    result = {
  "href": "https://api.spotify.com/v1/me/player/recently-played?limit=3",
  "limit": 3,
  "next": "https://api.spotify.com/v1/me/player/recently-played?before=1772636133869&limit=3",
  "cursors": {
    "after": "1772640184625",
    "before": "1772636133869"
  },
  "items": [
    {
      "track": {
        "album": {
          "album_type": "album",
          "total_tracks": 10,
          "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
          "external_urls": {
            "spotify": "https://open.spotify.com/album/0fayDgcekIaW0yQtUQ8CDm"
          },
          "href": "https://api.spotify.com/v1/albums/0fayDgcekIaW0yQtUQ8CDm",
          "id": "0fayDgcekIaW0yQtUQ8CDm",
          "images": [
            {
              "url": "https://i.scdn.co/image/ab67616d0000b273e43bd4878a9915fad4587e63",
              "height": 640,
              "width": 640
            },
            {
              "url": "https://i.scdn.co/image/ab67616d00001e02e43bd4878a9915fad4587e63",
              "height": 300,
              "width": 300
            },
            {
              "url": "https://i.scdn.co/image/ab67616d00004851e43bd4878a9915fad4587e63",
              "height": 64,
              "width": 64
            }
          ],
          "name": "Watershed (Special Edition)",
          "release_date": "2008-06-03",
          "release_date_precision": "day",
          "type": "album",
          "uri": "spotify:album:0fayDgcekIaW0yQtUQ8CDm",
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/0ybFZ2Ab08V8hueghSXm6E"
              },
              "href": "https://api.spotify.com/v1/artists/0ybFZ2Ab08V8hueghSXm6E",
              "id": "0ybFZ2Ab08V8hueghSXm6E",
              "name": "Opeth",
              "type": "artist",
              "uri": "spotify:artist:0ybFZ2Ab08V8hueghSXm6E"
            }
          ]
        },
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/0ybFZ2Ab08V8hueghSXm6E"
            },
            "href": "https://api.spotify.com/v1/artists/0ybFZ2Ab08V8hueghSXm6E",
            "id": "0ybFZ2Ab08V8hueghSXm6E",
            "name": "Opeth",
            "type": "artist",
            "uri": "spotify:artist:0ybFZ2Ab08V8hueghSXm6E"
          }
        ],
        "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
        "disc_number": 1,
        "duration_ms": 190693,
        "explicit": False,
        "external_ids": {
          "isrc": "NLA320886536"
        },
        "external_urls": {
          "spotify": "https://open.spotify.com/track/3P0LXXybFHgu2aY1NyGViV"
        },
        "href": "https://api.spotify.com/v1/tracks/3P0LXXybFHgu2aY1NyGViV",
        "id": "3P0LXXybFHgu2aY1NyGViV",
        "name": "Coil",
        "popularity": 44,
        "preview_url": "null",
        "track_number": 1,
        "type": "track",
        "uri": "spotify:track:3P0LXXybFHgu2aY1NyGViV",
        "is_local": False
      },
      "played_at": "2026-03-04T16:03:04.625Z",
      "context": {
        "type": "playlist",
        "href": "https://api.spotify.com/v1/playlists/65a3JbsD63CV3dCGbiVvSQ",
        "external_urls": {
          "spotify": "https://open.spotify.com/playlist/65a3JbsD63CV3dCGbiVvSQ"
        },
        "uri": "spotify:playlist:65a3JbsD63CV3dCGbiVvSQ"
      }
    },
    {
      "track": {
        "album": {
          "album_type": "album",
          "total_tracks": 10,
          "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
          "external_urls": {
            "spotify": "https://open.spotify.com/album/0fayDgcekIaW0yQtUQ8CDm"
          },
          "href": "https://api.spotify.com/v1/albums/0fayDgcekIaW0yQtUQ8CDm",
          "id": "0fayDgcekIaW0yQtUQ8CDm",
          "images": [
            {
              "url": "https://i.scdn.co/image/ab67616d0000b273e43bd4878a9915fad4587e63",
              "height": 640,
              "width": 640
            },
            {
              "url": "https://i.scdn.co/image/ab67616d00001e02e43bd4878a9915fad4587e63",
              "height": 300,
              "width": 300
            },
            {
              "url": "https://i.scdn.co/image/ab67616d00004851e43bd4878a9915fad4587e63",
              "height": 64,
              "width": 64
            }
          ],
          "name": "Watershed (Special Edition)",
          "release_date": "2008-06-03",
          "release_date_precision": "day",
          "type": "album",
          "uri": "spotify:album:0fayDgcekIaW0yQtUQ8CDm",
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/0ybFZ2Ab08V8hueghSXm6E"
              },
              "href": "https://api.spotify.com/v1/artists/0ybFZ2Ab08V8hueghSXm6E",
              "id": "0ybFZ2Ab08V8hueghSXm6E",
              "name": "Opeth",
              "type": "artist",
              "uri": "spotify:artist:0ybFZ2Ab08V8hueghSXm6E"
            }
          ]
        },
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/0ybFZ2Ab08V8hueghSXm6E"
            },
            "href": "https://api.spotify.com/v1/artists/0ybFZ2Ab08V8hueghSXm6E",
            "id": "0ybFZ2Ab08V8hueghSXm6E",
            "name": "Opeth",
            "type": "artist",
            "uri": "spotify:artist:0ybFZ2Ab08V8hueghSXm6E"
          }
        ],
        "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
        "disc_number": 1,
        "duration_ms": 190693,
        "explicit": False,
        "external_ids": {
          "isrc": "NLA320886536"
        },
        "external_urls": {
          "spotify": "https://open.spotify.com/track/3P0LXXybFHgu2aY1NyGViV"
        },
        "href": "https://api.spotify.com/v1/tracks/3P0LXXybFHgu2aY1NyGViV",
        "id": "3P0LXXybFHgu2aY1NyGViV",
        "name": "Coil",
        "popularity": 44,
        "preview_url": "null",
        "track_number": 1,
        "type": "track",
        "uri": "spotify:track:3P0LXXybFHgu2aY1NyGViV",
        "is_local": False
      },
      "played_at": "2026-03-04T15:59:59.037Z",
      "context": {
        "type": "playlist",
        "href": "https://api.spotify.com/v1/playlists/65a3JbsD63CV3dCGbiVvSQ",
        "external_urls": {
          "spotify": "https://open.spotify.com/playlist/65a3JbsD63CV3dCGbiVvSQ"
        },
        "uri": "spotify:playlist:65a3JbsD63CV3dCGbiVvSQ"
      }
    },
    {
      "track": {
        "album": {
          "album_type": "single",
          "total_tracks": 29,
          "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "PR", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
          "external_urls": {
            "spotify": "https://open.spotify.com/album/0c2eDi1S58XzaqxwOC1FMZ"
          },
          "href": "https://api.spotify.com/v1/albums/0c2eDi1S58XzaqxwOC1FMZ",
          "id": "0c2eDi1S58XzaqxwOC1FMZ",
          "images": [
            {
              "url": "https://i.scdn.co/image/ab67616d0000b273972ac79d249efed1c7b2c8c1",
              "height": 640,
              "width": 640
            },
            {
              "url": "https://i.scdn.co/image/ab67616d00001e02972ac79d249efed1c7b2c8c1",
              "height": 300,
              "width": 300
            },
            {
              "url": "https://i.scdn.co/image/ab67616d00004851972ac79d249efed1c7b2c8c1",
              "height": 64,
              "width": 64
            }
          ],
          "name": "Violator | The 12\" Singles",
          "release_date": "2022-04-01",
          "release_date_precision": "day",
          "type": "album",
          "uri": "spotify:album:0c2eDi1S58XzaqxwOC1FMZ",
          "artists": [
            {
              "external_urls": {
                "spotify": "https://open.spotify.com/artist/762310PdDnwsDxAQxzQkfX"
              },
              "href": "https://api.spotify.com/v1/artists/762310PdDnwsDxAQxzQkfX",
              "id": "762310PdDnwsDxAQxzQkfX",
              "name": "Depeche Mode",
              "type": "artist",
              "uri": "spotify:artist:762310PdDnwsDxAQxzQkfX"
            }
          ]
        },
        "artists": [
          {
            "external_urls": {
              "spotify": "https://open.spotify.com/artist/762310PdDnwsDxAQxzQkfX"
            },
            "href": "https://api.spotify.com/v1/artists/762310PdDnwsDxAQxzQkfX",
            "id": "762310PdDnwsDxAQxzQkfX",
            "name": "Depeche Mode",
            "type": "artist",
            "uri": "spotify:artist:762310PdDnwsDxAQxzQkfX"
          }
        ],
        "available_markets": ["AR", "AU", "AT", "BE", "BO", "BR", "BG", "CA", "CL", "CO", "CR", "CY", "CZ", "DK", "DO", "DE", "EC", "EE", "SV", "FI", "FR", "GR", "GT", "HN", "HK", "HU", "IS", "IE", "IT", "LV", "LT", "LU", "MY", "MT", "MX", "NL", "NZ", "NI", "NO", "PA", "PY", "PE", "PH", "PL", "PT", "SG", "SK", "ES", "SE", "CH", "TW", "TR", "UY", "US", "GB", "AD", "LI", "MC", "ID", "JP", "TH", "VN", "RO", "IL", "ZA", "SA", "AE", "BH", "QA", "OM", "KW", "EG", "MA", "DZ", "TN", "LB", "JO", "PS", "IN", "BY", "KZ", "MD", "UA", "AL", "BA", "HR", "ME", "MK", "RS", "SI", "KR", "BD", "PK", "LK", "GH", "KE", "NG", "TZ", "UG", "AG", "AM", "BS", "BB", "BZ", "BT", "BW", "BF", "CV", "CW", "DM", "FJ", "GM", "GE", "GD", "GW", "GY", "HT", "JM", "KI", "LS", "LR", "MW", "MV", "ML", "MH", "FM", "NA", "NR", "NE", "PW", "PG", "PR", "WS", "SM", "ST", "SN", "SC", "SL", "SB", "KN", "LC", "VC", "SR", "TL", "TO", "TT", "TV", "VU", "AZ", "BN", "BI", "KH", "CM", "TD", "KM", "GQ", "SZ", "GA", "GN", "KG", "LA", "MO", "MR", "MN", "NP", "RW", "TG", "UZ", "ZW", "BJ", "MG", "MU", "MZ", "AO", "CI", "DJ", "ZM", "CD", "CG", "IQ", "LY", "TJ", "VE", "ET", "XK"],
        "disc_number": 1,
        "duration_ms": 257630,
        "explicit": False,
        "external_ids": {
          "isrc": "GBAJH0400045"
        },
        "external_urls": {
          "spotify": "https://open.spotify.com/track/0yp3TvJNlG50Q4tAHWNCRm"
        },
        "href": "https://api.spotify.com/v1/tracks/0yp3TvJNlG50Q4tAHWNCRm",
        "id": "0yp3TvJNlG50Q4tAHWNCRm",
        "name": "Enjoy the Silence",
        "popularity": 78,
        "preview_url": "null",
        "track_number": 7,
        "type": "track",
        "uri": "spotify:track:0yp3TvJNlG50Q4tAHWNCRm",
        "is_local": False
      },
      "played_at": "2026-03-04T14:55:33.869Z",
      "context": {
        "type": "playlist",
        "href": "https://api.spotify.com/v1/playlists/37i9dQZF1Epz3zAsG5lgYU",
        "external_urls": {
          "spotify": "https://open.spotify.com/playlist/37i9dQZF1Epz3zAsG5lgYU"
        },
        "uri": "spotify:playlist:37i9dQZF1Epz3zAsG5lgYU"
      }
    }
  ]
}
    print(parse_recently_played_tracks(result))