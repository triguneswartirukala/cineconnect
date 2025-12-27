import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS likes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    post_id INTEGER,
    UNIQUE(user_id, post_id)
)
""")

conn.commit()
conn.close()

print("Likes table created")
