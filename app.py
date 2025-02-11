import streamlit as st
import pandas as pd

# Define the video_id, start_time, and end_time mappings
video_mappings = {
    ("SW", 31): ("M5lSUGeaJz0", 6 * 60 + 45, 8 * 60 + 20),
    ("SW", 15): ("M5lSUGeaJz0", 8 * 60 + 28, 11 * 60 + 56),
    ("EC", 36): ("M5lSUGeaJz0", 12 * 60 + 12, 15 * 60 + 40),
    # Add more entries as needed
}

# Load the real data from the CSV URL
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/kolbm/SHCDCase3/refs/heads/main/Complete_Case_Database.csv"
    return pd.read_csv(url)

df = load_data()

# User inputs for Location Code (renamed to "Code") and Entry Number (renamed to "Number")
location_code = st.selectbox("Select Location Code", df['Code'].unique())
entry_number = st.number_input("Enter Entry Number", min_value=1, max_value=100, step=1)

# Retrieve video details based on user input
key = (location_code, entry_number)
if key in video_mappings:
    video_id, start_time, end_time = video_mappings[key]
    st.markdown(f"""
        <div id="player"></div>
        <script>
          var tag = document.createElement('script');
          tag.src = "https://www.youtube.com/iframe_api";
          var firstScriptTag = document.getElementsByTagName('script')[0];
          firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

          var player;
          function onYouTubeIframeAPIReady() {{
            player = new YT.Player('player', {{
              height: '315',
              width: '560',
              videoId: '{video_id}',
              playerVars: {{ 'start': {start_time}, 'autoplay': 1, 'controls': 0 }},
              events: {{
                'onStateChange': onPlayerStateChange
              }}
            }});
          }}

          function onPlayerStateChange(event) {{
            if (event.data == YT.PlayerState.PLAYING) {{
              var end_time = {end_time};
              var interval = setInterval(function() {{
                if (player.getCurrentTime() >= end_time) {{
                  player.pauseVideo();
                  clearInterval(interval);
                }}
              }}, 1000);
            }}
          }}
        </script>
    """, unsafe_allow_html=True)
else:
    st.warning("No video found for the selected Location Code and Entry Number.")

# Query based on user input for the matching entry
result = df[(df['Code'] == location_code) & (df['Number'] == entry_number)]

if not result.empty:
    st.subheader("Matching Location")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)

    st.subheader("Matching Paragraph")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
else:
    st.error("No matching entry found. Please check the Location Code and Entry Number.")
