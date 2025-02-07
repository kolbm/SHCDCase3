import streamlit as st
import pandas as pd

# Load the database
file_path = "/mnt/data/case_data.csv"

# Try to read the file
try:
    df = pd.read_csv(file_path, encoding='utf-8')
    
    # Ensure correct column names
    expected_columns = ["Location Code", "Entry Number", "Locations", "Text"]
    df.columns = expected_columns
    
    # Streamlit App
    st.title("Sherlock Holmes Case Database")
    st.write("Select a location code and enter an encounter number to retrieve case details.")

    # Dropdown for Location Code
    location_codes = df["Location Code"].unique()
    selected_location = st.selectbox("Select Location Code:", location_codes)

    # Input for Entry Number
    entry_number = st.number_input("Enter Encounter Number:", min_value=1, step=1)

    # Retrieve and display result
    result = df[(df["Location Code"] == selected_location) & (df["Entry Number"] == entry_number)]
    
    if not result.empty:
        st.subheader("Case Details")
        st.write(f"**Location:** {result.iloc[0]['Locations']}")
        st.write(f"**Entry Text:** {result.iloc[0]['Text']}")
    else:
        st.warning("No matching case found. Please check your inputs.")

except FileNotFoundError:
    st.error("The database file was not found. Please ensure the file is correctly uploaded.")
except Exception as e:
    st.error(f"An error occurred: {e}")
