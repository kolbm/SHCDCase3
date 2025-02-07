import streamlit as st
import pandas as pd
import base64

# Load the dataset from CSV
file_path = "Complete_Case_Database.csv"
case_data = pd.read_csv(file_path)

# Set background image
def set_bg_from_url(url):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url({url});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Apply background image
set_bg_from_url("https://wallpapers.com/images/featured/old-paper-w3ydso7e9qtan8er.jpg")

# Streamlit UI
image_path = "7e3642ea39f283b64a5c40a18c963a5c.png"
st.image(image_path, use_container_width=True)

# Dropdown for Code Selection
location_code_image = "dc1b539d62ee4bea2a607f393f276191.png"
st.image(location_code_image, use_container_width=False)
code_options = case_data["Code"].unique()
selected_code = st.selectbox("", code_options)

# Text Input for Entry Number
entry_number_image = "dd2411aafb9c0f03efad90819b680c8a.png"
st.image(entry_number_image, use_container_width=False)
entry_number = st.text_input("", "", key='entry_number', help='Enter the case entry number here.', label_visibility='collapsed')
st.markdown("""<style>
    div[data-baseweb="input"] > div {
        font-size: 24px !important;
        padding: 10px !important;
    }
</style>""", unsafe_allow_html=True)

# Button to Retrieve Entry
display_text = ""
if st.button("Retrieve Entry"):
    if entry_number.isdigit():
        entry_number = int(entry_number)
        entry = case_data[(case_data["Code"] == selected_code) & (case_data["Number"] == entry_number)]
        if not entry.empty:
            if selected_code == 'SW' and entry_number == 15:
                image_sw15 = "Screenshot 2025-02-07 090927.png"
                st.image(image_sw15, use_container_width=True)
            location = entry.iloc[0]["Location"]
            full_text = entry.iloc[0]["Full Text"]
            display_text = f"**Location:** {location}\n\n**Details:** {full_text}"
        else:
            display_text = "No entry found for the selected code and number."
    else:
        display_text = "Please enter a valid numeric entry number."

st.markdown(display_text)
