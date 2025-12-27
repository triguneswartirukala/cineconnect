import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(posts)")
columns = [c[1] for c in cursor.fetchall()]

if "media_type" not in columns:
    cursor.execute("ALTER TABLE posts ADD COLUMN media_type TEXT")
    print("media_type column added")

conn.commit()
conn.close()
