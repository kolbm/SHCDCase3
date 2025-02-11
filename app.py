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

if 'df' not in locals():
    df = pd.DataFrame({
        'Location Code': ['SW', 'SW'],
        'Entry Number': [31, 15],
        'Location': ['Sample Location 1', 'Sample Location 2'],
        'Full Text': ['This is a sample paragraph for Entry 31.', 'This is a sample paragraph for Entry 15.']
    })

query = "Location Code == 'SW' and Entry Number == 31"  # Example query condition
result = df.query(query) if 'df' in locals() else pd.DataFrame()  # Query the DataFrame safely

if result is not None and isinstance(result, pd.DataFrame) and not result.empty:
    st.subheader("Matching Location")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)

    st.subheader("Matching Paragraph")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
else:
    st.error("No matching entry found. Please check the Location Code and Entry Number.")
