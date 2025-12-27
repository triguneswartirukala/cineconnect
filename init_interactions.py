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

cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    post_id INTEGER,
    content TEXT
)
""")

conn.commit()
conn.close()
print("Likes & Comments tables ready")
