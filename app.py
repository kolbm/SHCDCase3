import streamlit as st
import pandas as pd
from streamlit_player import st_player

# Load the CSV file
@st.cache_data
def load_data():
    file_path = "case_data.csv"
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
background_css = """
<style>
    .stApp {
        background-image: url('https://raw.githubusercontent.com/kolbm/SHCDCase3/main/background.jpg');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .stTitle, .stMarkdown, .stSubheader, .stTextInput > div > div > input, .narrative-text, .stSelectbox > div > div {
        color: black !important; font-family: 'Courier New', Courier, monospace !important;
    }
    .stTitle {
        font-size: 40px !important;
        text-align: center;
    }
    .stTextInput > div > div > input {
        font-size: 24px !important;
        text-align: center;
        width: 80px !important;
    }
    .stButton > button { font-size: 24px !important; border-radius: 10px; font-family: 'Courier New', Courier, monospace !important; padding: 10px 20px; background-color: silver !important; color: black !important; font-weight: bold; border: 2px solid black; }
    .stButton > button[data-testid="clear_button"] { background-color: red !important; color: white !important; font-weight: bold !important; border: 2px solid black; }
    .stButton > button[data-testid="find_paragraph_button"] { background-color: green !important; color: white !important; font-weight: bold !important; border: 2px solid black; }
    .keypad-container {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: 10px;
        max-width: 250px;
        margin: auto;
    }
</style>
"""

st.markdown(background_css, unsafe_allow_html=True)

# Title
st.image('https://raw.githubusercontent.com/kolbm/SHCDCase3/refs/heads/main/title_picture.png', use_container_width=True)

st.write("Enter a Location Code and Entry Number to retrieve the corresponding paragraph.")

# User input fields
st.write("### <span style='color: black;'>Location Code</span>", unsafe_allow_html=True)
location_code = st.selectbox("", location_codes)

# Initialize session state for entry_number if not set
if "entry_number" not in st.session_state:
    st.session_state.entry_number = ""

# Keypad entry number
st.write("### <span style='color: black;'>Enter Entry Number</span>", unsafe_allow_html=True)
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
for row in keypad_buttons:
    cols = st.columns(3)
    for i, button in enumerate(row):
        if button:
            with cols[i]:
                if st.button(button, key=f"btn_{button}"):
                    update_entry_number(button)
st.markdown("</div>", unsafe_allow_html=True)

# Clear button
if st.button("Clear Entry Number", key="clear_button"):
    clear_entry_number()

# Ensure the entry number is a valid integer
try:
    entry_number = int(st.session_state.entry_number) if st.session_state.entry_number else None
except ValueError:
    entry_number = None

# YouTube video mapping
video_mapping = {
    ("SW", 31): ("M5lSUGeaJz0", 405, 500),
    ("SW", 15): ("M5lSUGeaJz0", 508, 716),
    ("EC", 36): ("M5lSUGeaJz0", 732, 940),
    ("EC", 52): ("M5lSUGeaJz0", 949, 1055),
    ("SW", 19): ("M5lSUGeaJz0", 1064, 1156),
    ("SW", 13): ("M5lSUGeaJz0", 1508, 1544),
    ("EC", 30): ("M5lSUGeaJz0", 1553, 1561),
    ("EC", 35): ("M5lSUGeaJz0", 1598, 1609),
    ("SW", 5): ("M5lSUGeaJz0", 1615, 1658),
    ("EC", 38): ("M5lSUGeaJz0", 1665, 1695),
    ("SW", 22): ("M5lSUGeaJz0", 1700, 1768),
    ("WC", 14): ("M5lSUGeaJz0", 1773, 1792),
    ("SW", 2): ("M5lSUGeaJz0", 1797, 1899),
    ("SW", 30): ("M5lSUGeaJz0", 1910, 1973),
    ("SW", 50): ("M5lSUGeaJz0", 1981, 2001),
    ("SW", 12): ("M5lSUGeaJz0", 2010, 2059),
    ("SW", 39): ("M5lSUGeaJz0", 2067, 2095),
    ("SW", 27): ("M5lSUGeaJz0", 2105, 2127),
    ("SW", 25): ("M5lSUGeaJz0", 2137, 2196),
    ("SW", 24): ("M5lSUGeaJz0", 2205, 2238),
    ("WC", 34): ("M5lSUGeaJz0", 2245, 2288),
    ("WC", 46): ("M5lSUGeaJz0", 2298, 2398),
    ("SW", 21): ("M5lSUGeaJz0", 2405, 2502),
    ("WC", 29): ("M5lSUGeaJz0", 2514, 2539),
    ("SW", 48): ("M5lSUGeaJz0", 2547, 2597),
    ("SE", 21): ("M5lSUGeaJz0", 2609, 2620),
    ("SE", 16): ("M5lSUGeaJz0", 2631, 2645),
    ("WC", 17): ("M5lSUGeaJz0", 2739, 2760),
    ("WC", 13): ("M5lSUGeaJz0", 2768, 2817),
    ("WC", 22): ("M5lSUGeaJz0", 2827, 2858),
    ("EC", 26): ("M5lSUGeaJz0", 2885, 2897),
    ("EC", 36): ("M5lSUGeaJz0", 732, 940),
    ("EC", 52): ("M5lSUGeaJz0", 949, 1055)
    # Add the rest of the mappings here...
}

# Search for the corresponding paragraph
if st.button("Find Paragraph", key="find_paragraph_button") and entry_number is not None:
    result = df[(df["Location Code"] == location_code) & (df["Entry Number"] == entry_number)]
    
    if not result.empty:
        # Display image for specific entries
        image_mapping = {
            ("SW", 15): "https://raw.githubusercontent.com/kolbm/SHCDCase3/refs/heads/main/Screenshot%202025-02-07%20090927.png",
            ("NW", 35): "https://raw.githubusercontent.com/kolbm/SHCDCase3/refs/heads/main/Screenshot%202025-02-07%20141325.png"
        }
        image_path = image_mapping.get((location_code, entry_number))
        if image_path:
            st.image(image_path, caption="Relevant Evidence")
        
        # Display video for the matching entry if available
        video_info = video_mapping.get((location_code, entry_number))
        if video_info:
            video_id, start_time, end_time = video_info
            st.markdown(f"""
                <div>
                    <iframe width="560" height="315" 
                    src="https://www.youtube.com/embed/{video_id}?start={start_time}&autoplay=1&controls=0" 
                    id="ytplayer" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
                    <script>
                        var player = document.getElementById('ytplayer');
                        var endTime = {end_time};
                        var checkTime = setInterval(function() {
                            if (player.currentTime >= endTime) {
                                player.pause();
                                clearInterval(checkTime);
                            }
                        }, 1000);
                    </script>
                </div>
            """, unsafe_allow_html=True)
        
        st.subheader("Matching Location")
        st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)
        
        st.subheader("Matching Paragraph")
        st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
    else:
        st.error("No matching entry found. Please check the Location Code and Entry Number.")
