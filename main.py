from fastapi import FastAPI
from api import router as spotify_router
from contextlib import asynccontextmanager
from db import get_db_connection

@asynccontextmanager
async def lifespan(app:FastAPI):
    try:
        connection = get_db_connection()
        print("DB connected")
        connection.close()
    except Exception as e:
        print(f"Connection failed {e}")
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(spotify_router, tags=["Spotify"])