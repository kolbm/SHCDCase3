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

if not result.empty:
    st.subheader("Matching Location")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)

    st.subheader("Matching Paragraph")
    st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
else:
    st.error("No matching entry found. Please check the Location Code and Entry Number.")
