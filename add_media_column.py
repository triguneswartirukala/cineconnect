import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE posts ADD COLUMN media TEXT")
except:
    pass

conn.commit()
conn.close()
print("Media column ready")
