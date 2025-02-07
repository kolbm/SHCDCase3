import streamlit as st
import pandas as pd

# Load the CSV file
@st.cache_data
def load_data():
    file_path = "case_data.csv"  # Ensure this file is available in Streamlit deployment
    return pd.read_csv(file_path, encoding="latin1")

df = load_data()

# Extract unique location codes for the dropdown menu
location_codes = sorted(df["Location Code"].unique())

# Streamlit UI
st.title("Case File Paragraph Lookup")

st.write("Enter a Location Code and Entry Number to retrieve the corresponding paragraph.")

# User input fields
location_code = st.selectbox("Location Code", location_codes)

# Keypad entry number
st.write("### Enter Entry Number")
entry_number = st.text_input("", "", max_chars=2, key="entry_number")

def update_entry_number(num):
    current_value = st.session_state.entry_number
    if len(current_value) < 2:
        st.session_state.entry_number = current_value + num

keypad_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
cols = st.columns(5)
for i, button in enumerate(keypad_buttons):
    if cols[i % 5].button(button, key=f"btn_{button}"):
        update_entry_number(button)

# Ensure the entry number is a valid integer
try:
    entry_number = int(st.session_state.entry_number) if st.session_state.entry_number else None
except ValueError:
    entry_number = None

# Search for the corresponding paragraph
if st.button("Find Paragraph") and entry_number is not None:
    result = df[(df["Location Code"] == location_code) & (df["Entry Number"] == entry_number)]
    
    if not result.empty:
        st.subheader("Matching Paragraph")
        st.write(result.iloc[0]["Full Text"])
    else:
        st.error("No matching entry found. Please check the Location Code and Entry Number.")
