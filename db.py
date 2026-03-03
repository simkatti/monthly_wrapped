import psycopg2
import psycopg2.extras
import os
from dotenv import load_dotenv
from datetime import datetime


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )


def save_recentplays_to_db(songs):
    connection = get_db_connection()
    cur = connection.cursor()
    
    try: 
        for track in songs:
            cur.execute("""
                        INSERT INTO tracks (track_id, artist_id, song_name, artist_name, image, duration_ms)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (track_id) DO NOTHING;""",
                        (track['track_id'], track['artist_id'], track['song_name'], track['artist_name'], track['image'], track['duration_ms']))
            cur.execute("""
                        INSERT INTO streams (track_id, played_at)
                        VALUES (%s, %s)
                        ON CONFLICT ON CONSTRAINT unique_play DO NOTHING;
                        """, (track['track_id'], track['played_at']))
        connection.commit()
        print(f"Added {len(songs)} tracks into the db")
    except Exception as e:
        connection.rollback()
        print(f"Insertion failed: {e}")
    finally:
        cur.close()
        connection.close()
        
            
def fetch_from_db(month):
    month_num = datetime.strptime(month, "%B").month
    connection = get_db_connection()
    cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query = """
            SELECT t.track_id, t.artist_id, t.song_name, t.artist_name, t.image, t.duration_ms, s.played_at
            FROM streams s
            JOIN tracks t ON s.track_id = t.track_id
            WHERE EXTRACT(MONTH FROM s.played_at) = %s
            ORDER BY s.played_at ASC;
    """
    cur.execute(query, (month_num,))
    data = cur.fetchall()
    cur.close()
    connection.close()
    return data