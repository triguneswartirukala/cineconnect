import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    actor_id INTEGER,
    type TEXT,
    post_id INTEGER,
    seen INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()
print("Notifications table ready")
