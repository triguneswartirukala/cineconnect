import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Add username column
cursor.execute("""
ALTER TABLE users
ADD COLUMN username TEXT UNIQUE
""")

conn.commit()
conn.close()

print("Username column added")
