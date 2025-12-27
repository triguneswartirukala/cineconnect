import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    message TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
print("Chat table ready")
