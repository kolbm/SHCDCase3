import streamlit as st
import pandas as pd
import os
import base64

# Load the CSV file
@st.cache_data
def load_data():
    file_path = "case_data.csv"  # Ensure this file is available in Streamlit deployment
    return pd.read_csv(file_path, encoding="latin1")

df = load_data()

# Mapping location codes to detailed, context-based names
location_mapping = {
    "SE": "Kenward Olick's Residence & Surrounding Tenement",
    "SW": "Societies Club - Langdale Pike's Gathering Place",
    "NW": "Davenport's Law Office on Baker Street",
    "WC": "Dr. Trevelyan's Home & Medical Practice",
    "-": "Tower of London Vicinity - Dockside & Market",
    "EC": "Customs House & St. Mary Church Courtyard"
}

df["Location"] = df["Location Code"].map(location_mapping)

# Extract unique location codes for the dropdown menu
location_codes = sorted(df["Location Code"].unique())

# Function to encode an image as base64
@st.cache_data
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

background_image_path = "wordoftheoracle_A_Victorian__Holmsian_scene_appearing_on_wall_214710dc-9ce4-4c9f-8903-7388a8755311_0.png"
if os.path.exists(background_image_path):
    base64_bg = get_base64_image(background_image_path)
    background_css = f"""
    <style>
        .stApp {{
            background-image: url("data:image/png;base64,{base64_bg}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
    </style>
    """
    st.markdown(background_css, unsafe_allow_html=True)

# Streamlit UI Styling
st.markdown(
    """
    <style>
        .stTitle {
            font-size: 40px !important;
            color: #4b2e1e;
            text-align: center;
        }
        .stTextInput > div > div > input {
            font-size: 24px !important;
            text-align: center;
            width: 80px !important;
            color: white !important;
        }
        .stButton > button {
            font-size: 24px !important;
            border-radius: 10px;
            width: 70px;
            height: 70px;
            text-align: center;
        }
        .stButton > button[data-testid="clear_button"] {
            background-color: #d9534f !important; /* Red */
            color: white !important;
        }
        .stButton > button[data-testid="find_paragraph_button"] {
            background-color: #5cb85c !important; /* Green */
            color: white !important;
        }
        .stSelectbox > div > div {
            font-size: 24px !important;
        }
        .stSubheader {
            font-size: 30px !important;
            color: white !important;
        }
        .keypad-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            max-width: 250px;
            margin: auto;
        }
        .narrative-text {
            font-size: 22px;
            font-family: 'Times New Roman';
            color: white !important;
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
st.write("### <span style='color: white;'>Enter Entry Number</span>", unsafe_allow_html=True)
entry_number_display = st.text_input("", st.session_state.entry_number, max_chars=2, key="entry_number_display", disabled=True)

def update_entry_number(num):
    if len(st.session_state.entry_number) < 2:
        st.session_state.entry_number += num
        st.rerun()

def clear_entry_number():
    st.session_state.entry_number = ""
    st.rerun()

# Keypad layout
keypad_buttons = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"], ["", "0", ""]]
st.markdown("<div class='keypad-container'>", unsafe_allow_html=True)
cols = st.columns(3)
for row in keypad_buttons:
    for i, button in enumerate(row):
        if button:
            with cols[i]:
                if st.button(button, key=f"btn_{button}"):
                    update_entry_number(button)
st.markdown("</div>", unsafe_allow_html=True)

# Clear button
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True) 
if st.button("Clear Entry Number", key="clear_button", help="Clear the entered number"):
    clear_entry_number()
st.markdown("</div>", unsafe_allow_html=True)

# Ensure the entry number is a valid integer
try:
    entry_number = int(st.session_state.entry_number) if st.session_state.entry_number else None
except ValueError:
    entry_number = None

# Search for the corresponding paragraph
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button("Find Paragraph", key="find_paragraph_button", help="Retrieve the matching case paragraph") and entry_number is not None:
    result = df[(df["Location Code"] == location_code) & (df["Entry Number"] == entry_number)]
    
    if not result.empty:
        st.subheader("Matching Location")
        st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)
        
        st.subheader("Matching Paragraph")
        st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
    else:
        st.error("No matching entry found. Please check the Location Code and Entry Number.")
st.markdown("</div>", unsafe_allow_html=True)
