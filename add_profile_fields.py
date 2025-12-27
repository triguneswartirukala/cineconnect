import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(users)")
columns = [c[1] for c in cursor.fetchall()]

if "profile_pic" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN profile_pic TEXT")

if "bio" not in columns:
    cursor.execute("ALTER TABLE users ADD COLUMN bio TEXT")

conn.commit()
conn.close()
print("Profile fields ready")
