import streamlit as st
import requests
import streamlit.components.v1 as components
import datetime

st.title("Spotify monthly wrapped")
st.space(size="medium")

current_month = datetime.datetime.now().month
months = ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December")
available_months = months[:current_month] + ("all year",)



if st.button("Login to Spotify"):
    response = requests.get("http://127.0.0.1:8000/login")
    try:
        data = response.json()
        url = data.get("login_url")
        st.info(f"Please [click here to authorize]({url})")
    except requests.exceptions.JSONDecodeError:
        st.error("Something went wrong with the response")
        
month = st.selectbox(
    label="Choose month",
    options=available_months,
    index=None,
    placeholder="Select month",
    label_visibility="collapsed",
    width=190
)

if month:
    if st.button(f"Get top 10 tracks of {month}"):
        response = requests.get(f"http://127.0.0.1:8000/stats/{month}")

        if response.status_code == 200:
            data = response.json()
            top_songs = data['songs']
            
            if not data:
                st.warning("Not enough data for current month")
                
            st.space(size="small")
            st.subheader("Top 10 most played tracks")
            
            for i in range(0, len(top_songs), 5):
                row_tracks = top_songs[i : i + 5]
                cols = st.columns(5) 
                
                for j, track in enumerate(row_tracks):
                    with cols[j]:
                        if track.get('image'):
                            st.image(track['image'],width='stretch')
                        
                        st.markdown(f" {i +j +1}. {track['song_name']} ")
                        st.caption(f"{track['artist_name']}")
                        st.caption(f"{track['count']} listens")
                        
            st.space(size="small")
            st.subheader("Top 10 most played artists")
            top_artist = data['artists']
            
            for i in range(0, len(top_artist), 5):
                row_artist = top_artist[i : i +5]
                cols = st.columns(5)
                for j, artist in enumerate(row_artist):
                    with cols[j]:
                        if artist.get('image'):
                            st.image(artist['image'],width='stretch')
                        st.markdown(f" {i +j +1}. {artist['artist_name']} ")
                        st.caption(f"{artist['count']} plays")
                    
            st.space(size="small")

            st.subheader(f"You mostly listen during the {data['time_of_day']} between {data['time_slot']}!")
            
            st.space(size="small")
            
            st.subheader(f"Your total listening time in {month} is {data['total_minutes']} minutes which is {data['formatted_time']}")
            
        else:
            st.error("Something went wrong")
