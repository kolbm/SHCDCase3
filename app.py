import sqlite3
import pandas as pd

# Load the corrected CSV file with explicit encoding
csv_file = "/mnt/data/Complete_Case_Database.csv"

try:
    # Try UTF-8 encoding first
    df = pd.read_csv(csv_file, encoding='utf-8')
except UnicodeDecodeError:
    # If UTF-8 fails, fall back to 'latin1' encoding
    df = pd.read_csv(csv_file, encoding='latin1')

# Database file
db_file = "/mnt/data/case_data.db"

# Connect to SQLite database
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create the table if it does not exist
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
