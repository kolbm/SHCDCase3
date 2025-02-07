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
entry_number = st.number_input("Entry Number", min_value=0, step=1, format="%d")

# Search for the corresponding paragraph
if st.button("Find Paragraph"):
    result = df[(df["Location Code"] == location_code) & (df["Entry Number"] == entry_number)]
    
    if not result.empty:
        st.subheader("Matching Paragraph")
        st.write(result.iloc[0]["Full Text"])
    else:
        st.error("No matching entry found. Please check the Location Code and Entry Number.")
