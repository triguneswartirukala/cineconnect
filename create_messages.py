import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER,
    receiver_id INTEGER,
    content TEXT
)
""")

conn.commit()
conn.close()
print("Messages table ready")
