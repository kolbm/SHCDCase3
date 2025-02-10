background-image: url('https://cdn.vectorstock.com/i/500p/86/55/vintage-grunge-newspaper-texture-background-vector-20998655.jpg');
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
        .stTitle, .stMarkdown, .stSubheader, .stTextInput > div > div > input, .narrative-text, .stSelectbox > div > div, .stError {{
            color: white !important;
        }}
        .stTitle {{
            font-size: 40px !important;
            text-align: center;
        }}
        .stTextInput > div > div > input {{
            font-size: 24px !important;
            text-align: center;
            width: 80px !important;
        }}
        .stButton > button {{
            font-size: 24px !important;
            border-radius: 10px;
            width: 70px;
            height: 70px;
            text-align: center;
        }}
        .stButton > button[data-testid="clear_button"] {{
            background-color: #d9534f !important; /* Red */
            color: white !important;
        }}
        .stButton > button[data-testid="find_paragraph_button"] {{
            background-color: #5cb85c !important; /* Green */
            color: white !important;
        }}
        .keypad-container {{
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 10px;
            max-width: 250px;
            margin: auto;
        }}
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
        # Display image for specific entries
        image_mapping = {
            ("SW", 15): "Screenshot 2025-02-07 090927.png",
            ("NW", 35): "Screenshot 2025-02-07 141325.png"
        }
        image_path = image_mapping.get((location_code, entry_number))
        if image_path and os.path.exists(image_path):
            st.image(image_path, caption="Relevant Case Image")
        
        # Display map images based on location code
        map_images = {
            "EC": "map_ec.jpg",
            "NW": "map_nw.jpg",
            "SE": "map_se.jpg",
            "SW": "map_sw.jpg",
            "WC": "map_wc.jpg"
        }
        map_image = map_images.get(location_code)
        if map_image and os.path.exists(map_image):
            st.image(map_image, caption="Location Map")
        
        st.subheader("Matching Location")
        st.write(f"<p class='narrative-text'>{result.iloc[0]['Location']}</p>", unsafe_allow_html=True)
        
        st.subheader("Matching Paragraph")
        st.write(f"<p class='narrative-text'>{result.iloc[0]['Full Text']}</p>", unsafe_allow_html=True)
    else:
        st.error("No matching entry found. Please check the Location Code and Entry Number.")
st.markdown("</div>", unsafe_allow_html=True)
