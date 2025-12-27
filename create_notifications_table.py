import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    message TEXT,
    is_read INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()
print("Notifications table ready")
