import os
import sqlite3
import pandas as pd

# Possible locations for the file
possible_paths = ["./case_data.csv", "/mnt/data/case_data.csv"]

# Find the correct file path
csv_file = None
for path in possible_paths:
    if os.path.exists(path):
        csv_file = path
        break

if not csv_file:
    print("Error: case_data.csv not found in any expected location.")
    print("Available files:", os.listdir("."))  # Debugging
else:
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file, encoding='utf-8')
    except UnicodeDecodeError:
        df = pd.read_csv(csv_file, encoding='latin1')

    # SQLite database file
    db_file = "./case_data.db"

    # Connect to SQLite
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

    # Insert data
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO CaseEntries (Location_Code, Entry_Number, Location, Full_Text)
            VALUES (?, ?, ?, ?)
        ''', (row['Location Code'], row['Entry Number'], row['Location'], row['Full Text']))

    # Commit and close
    conn.commit()
    conn.close()

    print("Database updated successfully!")
