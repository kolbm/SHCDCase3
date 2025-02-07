import streamlit as st
import pandas as pd

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
            text-align: center;
            width: 80px !important;
        }
        .stButton > button {
            font-size: 24px !important;
            background-color: #8b4513;
            color: white;
            border-radius: 10px;
            width: 70px;
            height: 70px;
            text-align: center;
        }
        .stSelectbox > div > div {
            font-size: 24px !important;
        }
        .stSubheader {
            font-size: 30px !important;
            color: #4b2e1e;
        }
        .keypad-container {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            max-width: 250px;
            margin: auto;
        }
        .large-button > button {
            font-size: 28px !important;
            width: 200px !important;
            height: 70px !important;
            background-color: #5a3212 !important;
            color: white !important;
            border-radius: 10px !important;
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

# Keypad layout
keypad_buttons = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
st.markdown("<div class='keypad-container'>", unsafe_allow_html=True)
cols = st.columns(3)
for i, button in enumerate(keypad_buttons):
    with cols[i % 3]:
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
        st.write(f"<p style='font-size:24px; font-family: Times New Roman; font-weight: bold;'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)
        
        st.subheader("Matching Paragraph")
        st.write(f"<p style='font-size:22px; font-family: Times New Roman;'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
        
        # Display image for SW 15
        if location_code == "SW" and entry_number == 15:
            st.image("Screenshot_2025-02-07 090927.png", caption="Relevant Case Image")
        
        # Display image for NW 35
        if location_code == "NW" and entry_number == 35:
            st.image("Screenshot 2025-02-07 141325.png", caption="Relevant Case Image")
    else:
        st.error("No matching entry found. Please check the Location Code and Entry Number.")
st.markdown("</div>", unsafe_allow_html=True)
