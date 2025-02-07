import os
import sqlite3
import pandas as pd

print("🚀 Script started...")  # Force debug message

# List available files in current directory and /mnt/data
print("📂 Current Directory Files:", os.listdir("."))
if os.path.exists("/mnt/data"):
    print("📂 /mnt/data Files:", os.listdir("/mnt/data"))

# Possible locations for the file
possible_paths = ["./case_data.csv", "/mnt/data/case_data.csv"]

# Find the correct file path
csv_file = None
for path in possible_paths:
    if os.path.exists(path):
        csv_file = path
        print(f"✅ Found file: {csv_file}")  # Confirm file found
        break

if not csv_file:
    print("❌ Error: case_data.csv not found in any expected location.")
    exit(1)

try:
    print("📊 Loading CSV file...")
    df = pd.read_csv(csv_file, encoding='utf-8')
    print(f"✅ CSV loaded with {len(df)} entries.")
except UnicodeDecodeError:
    print("⚠️ UnicodeDecodeError! Retrying with Latin-1 encoding.")
    df = pd.read_csv(csv_file, encoding='latin1')

# Ensure required columns exist
required_columns = ["Location Code", "Entry Number", "Location", "Full Text"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"❌ Missing columns: {missing_columns}")
    exit(1)

# SQLite database file
db_file = "./case_data.db"

print(f"🔄 Connecting to SQLite database: {db_file}...")
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Create table
print("🛠️ Creating table if it doesn't exist...")
cursor.execute('''
    CREATE TABLE IF NOT EXISTS CaseEntries (
        Location_Code TEXT,
        Entry_Number INTEGER,
        Location TEXT,
        Full_Text TEXT
    )
''')

# Clear existing data (optional)
print("🧹 Clearing old data...")
cursor.execute("DELETE FROM CaseEntries")

# Insert new data
print(f"⬆️ Inserting {len(df)} records into database...")
for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO CaseEntries (Location_Code, Entry_Number, Location, Full_Text)
        VALUES (?, ?, ?, ?)
    ''', (row['Location Code'], row['Entry Number'], row['Location'], row['Full Text']))

# Commit and close
conn.commit()
conn.close()

print("✅ Database updated successfully!")
