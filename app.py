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

# Streamlit UI Styling
st.markdown(
    """
    <style>
        body {
            background-color: #f5f5dc;
            font-family: 'Times New Roman', serif;
        }
        .stTitle {
            font-size: 40px !important;
            color: #4b2e1e;
            text-align: center;
        }
        .stTextInput > div > div > input {
            font-size: 24px !important;
        }
        .stButton > button {
            font-size: 20px !important;
            background-color: #8b4513;
            color: white;
            border-radius: 5px;
        }
        .stSelectbox > div > div {
            font-size: 24px !important;
        }
        .stSubheader {
            font-size: 30px !important;
            color: #4b2e1e;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("Case File Paragraph Lookup")

st.write("Enter a Location Code and Entry Number to retrieve the corresponding paragraph.")

# User input fields
location_code = st.selectbox("Location Code", location_codes)

# Initialize session state for entry_number if not set
if "entry_number" not in st.session_state:
    st.session_state.entry_number = ""

# Keypad entry number
st.write("### Enter Entry Number")
entry_number_display = st.text_input("", st.session_state.entry_number, max_chars=2, key="entry_number_display", disabled=True)

def update_entry_number(num):
    if len(st.session_state.entry_number) < 2:
        st.session_state.entry_number += num
        st.rerun()

def clear_entry_number():
    st.session_state.entry_number = ""
    st.rerun()

keypad_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
cols = st.columns(5)
for i, button in enumerate(keypad_buttons):
    if cols[i % 5].button(button, key=f"btn_{button}"):
        update_entry_number(button)

# Clear button
if st.button("Clear Entry Number"):
    clear_entry_number()

# Ensure the entry number is a valid integer
try:
    entry_number = int(st.session_state.entry_number) if st.session_state.entry_number else None
except ValueError:
    entry_number = None

# Search for the corresponding paragraph
if st.button("Find Paragraph") and entry_number is not None:
    result = df[(df["Location Code"] == location_code) & (df["Entry Number"] == entry_number)]
    
    if not result.empty:
        st.subheader("Matching Location")
        st.write(f"<p style='font-size:24px; font-family: Times New Roman; font-weight: bold;'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)
        
        st.subheader("Matching Paragraph")
        st.write(f"<p style='font-size:22px; font-family: Times New Roman;'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
        
        # Display image for SW 15
        if location_code == "SW" and entry_number == 15:
            st.image("Screenshot 2025-02-07 090927.png", caption="Relevant Case Image")
    else:
        st.error("No matching entry found. Please check the Location Code and Entry Number.")
