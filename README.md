[![Sync sportify data](https://github.com/simkatti/monthly_wrapped/actions/workflows/sync.yml/badge.svg)](https://github.com/simkatti/monthly_wrapped/actions/workflows/sync.yml)

# Monthly wrapped (under construction)
Personal data engineering project that uses spotifys APIs to analyse listening stream. 
The application works in a following way:

The app fetches 50 recently played tracks every night from spotify API by using automated github workflow and puts them to database. The database is hosted by superbase and has two tables: tracks and streams. Tracks hold information about every unique song played while stream records every track and the time the track was played. App contains minimum frontend, done with streamlit library. In the frontend it is possible to select different months for analysis. Upon request the frontend shows 10 most played tracks, artist, time of the day when user listens music the most and minutes spent listening music that month. For the analysis, the backend fetches selected months streams and analyses the data. 




### To run projectc after installing dependencies:
uvicorn main:app --reload

poetry run streamlit run frontend.py
