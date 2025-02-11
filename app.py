if 'video_id' in locals() and 'start_time' in locals() and 'end_time' in locals():
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

import streamlit as st  # Ensure Streamlit is imported
import pandas as pd  # Ensure pandas is imported

import streamlit as st
import pandas as pd

@st.cache
def load_data():
    return pd.read_csv('your_file.csv')  # Replace 'your_file.csv' with your actual data file

df = load_data()

location_code = st.selectbox("Select Location Code", df['Location Code'].unique())
entry_number = st.number_input("Enter Entry Number", min_value=1, max_value=100, step=1)

result = df[(df['Location Code'] == location_code) & (df['Entry Number'] == entry_number)])

if not result.empty:
    st.subheader("Matching Location")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)

    st.subheader("Matching Paragraph")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
else:
    st.error("No matching entry found. Please check the Location Code and Entry Number.")

if result is not None and isinstance(result, pd.DataFrame) and not result.empty:
    st.subheader("Matching Location")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)

    st.subheader("Matching Paragraph")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
else:
    st.error("No matching entry found. Please check the Location Code and Entry Number.")
