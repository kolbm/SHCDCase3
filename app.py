import streamlit as st
import pandas as pd

# Load the dataset from CSV
file_path = "Complete_Case_Database.csv"
case_data = pd.read_csv(file_path)

# Streamlit UI
st.title("Case Lookup Application")

# Dropdown for Code Selection
code_options = case_data["Code"].unique()
selected_code = st.selectbox("Select Entry Code:", code_options)

# Text Input for Entry Number
entry_number = st.text_input("Enter Entry Number:", "")

# Button to Retrieve Entry
display_text = ""
if st.button("Retrieve Entry"):
    if entry_number.isdigit():
        entry_number = int(entry_number)
        entry = case_data[(case_data["Code"] == selected_code) & (case_data["Number"] == entry_number)]
        if not entry.empty:
            location = entry.iloc[0]["Location"]
            full_text = entry.iloc[0]["Full Text"]
            display_text = f"**Location:** {location}\n\n**Details:** {full_text}"
        else:
            display_text = "No entry found for the selected code and number."
    else:
        display_text = "Please enter a valid numeric entry number."

st.markdown(display_text)
