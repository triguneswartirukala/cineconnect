import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
ALTER TABLE posts ADD COLUMN media TEXT
""")

conn.commit()
conn.close()

print("Media column added to posts table")
