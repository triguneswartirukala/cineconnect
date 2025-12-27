import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE notifications ADD COLUMN seen INTEGER DEFAULT 0")
    conn.commit()
    print("✅ 'seen' column added successfully")
except sqlite3.OperationalError as e:
    print("⚠️ Column already exists or error:", e)

conn.close()
