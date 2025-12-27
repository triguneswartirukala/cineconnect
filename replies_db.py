import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS replies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    user_id INTEGER,
    post_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()

print("Replies table created")
