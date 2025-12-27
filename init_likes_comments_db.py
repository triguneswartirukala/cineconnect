import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS likes (
    user_id INTEGER,
    post_id INTEGER,
    UNIQUE(user_id, post_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER,
    user_id INTEGER,
    comment TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("✅ Likes & comments tables created")
