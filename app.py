import os
import sqlite3
import pandas as pd

# Define the correct file path
csv_file = "/mnt/data/case_data.csv"

# Check if the file exists before trying to read it
if not os.path.exists(csv_file):
    print(f"Error: The file '{csv_file}' was not found. Listing available files in /mnt/data:")
    print(os.listdir("/mnt/data"))  # Print available files for debugging
else:
    try:
        # Read the CSV file using UTF-8 encoding
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        # If UTF-8 fails, fall back to Latin-1 encoding
        df = pd.read_csv(csv_file, encoding='latin1')

    # Define SQLite database file
    db_file = "/mnt/data/case_data.db"

    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it does not exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CaseEntries (
            Location_Code TEXT,
            Entry_Number INTEGER,
            Location TEXT,
            Full_Text TEXT
        )
    ''')

    # Clear existing data (optional)
    cursor.execute("DELETE FROM CaseEntries")

    # Insert data into the table
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO CaseEntries (Location_Code, Entry_Number, Location, Full_Text)
            VALUES (?, ?, ?, ?)
        ''', (row['Location Code'], row['Entry Number'], row['Location'], row['Full Text']))

    # Commit and close the connection
    conn.commit()
    conn.close()

    print("Database updated successfully!")
