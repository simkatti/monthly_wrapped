import streamlit as st
import requests
import streamlit.components.v1 as components

st.title("10 Recently Played Songs")
st.space(size="medium")


if st.button("Login to Spotify"):
    response = requests.get("http://127.0.0.1:8000/login")
    try:
        data = response.json()
        url = data.get("login_url")
        st.info(f"Please [click here to authorize]({url})")
    except requests.exceptions.JSONDecodeError:
        st.error("Something went wrong with the response")
    
if st.button("Get My 10 Recent Tracks"):
    response = requests.get("http://127.0.0.1:8000/recent")
    st.space(size="small")

    
    if response.status_code == 200:
        tracks = response.json()
        top_10 = tracks[:10]

        for i in range(0, len(top_10), 5):
            row_tracks = top_10[i : i + 5]
            cols = st.columns(5) 
            
            for j, track in enumerate(row_tracks):
                with cols[j]:
                    if track.get('image'):
                        st.image(track['image'], use_container_width=True)
                    
                    st.markdown(f" {j +1}. {track['song_name']} ")
                    st.caption(f"{track['artist']}")
    else:
        st.error("Something went wrong")