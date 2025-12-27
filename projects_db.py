import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    required_roles TEXT,
    location TEXT,
    creator_id INTEGER
)
""")

conn.commit()
conn.close()

print("Projects table created successfully")
