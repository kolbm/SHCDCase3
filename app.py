if 'video_id' in locals() and 'start_time' in locals() and 'end_time' in locals():
    video_id, start_time, end_time = video_info
st.markdown(f"""
    <iframe width="560" height="315" 
    src="https://www.youtube.com/embed/{video_id}?start={start_time}&end={end_time}&autoplay=1&controls=0" 
    frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
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
