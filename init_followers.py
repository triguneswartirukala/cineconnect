import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS followers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    follower_id INTEGER,
    following_id INTEGER,
    UNIQUE(follower_id, following_id)
)
""")

conn.commit()
conn.close()

print("Followers table ready")
