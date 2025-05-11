import sqlite3

# Connect to the database
conn = sqlite3.connect('medical_assistant.db')
cursor = conn.cursor()

# Check if age column exists
cursor.execute("PRAGMA table_info(consultations)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

# Add age column if it doesn't exist
if 'age' not in column_names:
    print("Adding 'age' column to consultations table...")
    cursor.execute("ALTER TABLE consultations ADD COLUMN age INTEGER")

# Add gender column if it doesn't exist
if 'gender' not in column_names:
    print("Adding 'gender' column to consultations table...")
    cursor.execute("ALTER TABLE consultations ADD COLUMN gender TEXT")

# Commit changes and close connection
conn.commit()
conn.close()

print("Database migration completed successfully!")